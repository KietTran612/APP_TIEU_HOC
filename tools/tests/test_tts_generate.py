import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from tapdoc import __main__ as cli
from tapdoc.manifest import save_rows
from tapdoc.tts_engine import EdgeEngine, TtsError, TtsUnavailable
from tapdoc.tts_generate import approve, generate_one, restore_previous, run_batch
from tapdoc.tts_settings import effective_params, needs_regen, set_override, signature
from tests.test_tts_settings import row, settings
from tests.tts_fakes import FakeEngine, fake_mp3


class TempCase(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.audio = self.root / "audio"
        self.audio.mkdir()
        self.prev = self.root / "prev"
        self.s = settings()
        self.r = row()
        self.path = self.audio / "am_b.mp3"
        self.path.write_bytes("bản cũ".encode())


class GenerateTest(TempCase):
    def test_source_follows_voice(self):
        for voice, source in (("vi-VN-HoaiMyNeural", "tts_edge_hoaimy"),
                              ("vi-VN-NamMinhNeural", "tts_edge_namminh")):
            with self.subTest(voice=voice):
                set_override(self.s, self.r, voice=voice)
                engine = FakeEngine()
                result = generate_one(self.r, self.s, engine, self.audio, self.prev)
                self.assertEqual(result["source"], source)
                self.assertEqual(result["tts"]["voice"], voice)
                self.assertEqual(engine.calls[-1].voice, voice)


    def test_writes_file_row_and_prev(self):
        before = copy.deepcopy(self.r)
        result = generate_one(self.r, self.s, FakeEngine(), self.audio, self.prev)
        self.assertEqual(self.r, before)
        self.assertEqual(result["status"], "cho_duyet")
        self.assertEqual(result["source"], "tts_edge_hoaimy")
        self.assertEqual(result["tts"]["sig"], signature(effective_params(self.s, self.r)))
        self.assertEqual((self.prev / "am_b.mp3").read_bytes(), "bản cũ".encode())
        metadata = json.loads((self.prev / "am_b.json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["source"], "cu")
        self.assertFalse(needs_regen(self.s, result))

    def test_prev_is_the_take_before_last(self):
        first = generate_one(self.r, self.s, FakeEngine(), self.audio, self.prev)
        take = self.path.read_bytes()
        second = generate_one(first, self.s, FakeEngine(audio=fake_mp3(2), speech_end=1.4),
                              self.audio, self.prev)
        self.assertEqual((self.prev / "am_b.mp3").read_bytes(), take)
        self.assertNotEqual(self.path.read_bytes(), take)
        metadata = json.loads((self.prev / "am_b.json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["tts"], first["tts"])
        self.assertEqual(second["status"], "cho_duyet")

    def test_engine_error_leaves_everything(self):
        first = generate_one(self.r, self.s, FakeEngine(), self.audio, self.prev)
        before = copy.deepcopy((first, self.s))
        files = {p: p.read_bytes() for p in (self.path, *self.prev.iterdir())}
        with self.assertRaises(TtsError):
            generate_one(first, self.s, FakeEngine(failures={"bờ"}), self.audio, self.prev)
        self.assertEqual((first, self.s), before)
        self.assertEqual({p: p.read_bytes() for p in files}, files)

    def test_trim_applied_and_flag(self):
        result = generate_one(self.r, self.s, FakeEngine(), self.audio, self.prev)
        self.assertTrue(result["tts"]["trimmed"])
        self.assertLess(len(self.path.read_bytes()), len(fake_mp3(1.2)))
        result = generate_one(result, self.s, FakeEngine(speech_start=None, speech_end=None),
                              self.audio, self.prev)
        self.assertFalse(result["tts"]["trimmed"])
        self.assertEqual(self.path.read_bytes(), fake_mp3(1.2))

    def test_empty_or_invalid_audio_does_not_replace_old(self):
        for audio in (b"", b"not mp3"):
            with self.assertRaises(TtsError):
                generate_one(self.r, self.s, FakeEngine(audio=audio), self.audio, self.prev)
            self.assertEqual(self.path.read_bytes(), "bản cũ".encode())
            self.assertFalse(self.prev.exists())

    def test_write_failure_keeps_previous_take(self):
        from tapdoc.importer import _write_atomic

        first = generate_one(self.r, self.s, FakeEngine(), self.audio, self.prev)
        files = {p: p.read_bytes() for p in (self.path, *self.prev.iterdir())}

        def fail_dest(dest, data):
            if dest == self.path:
                raise OSError("đĩa đầy")
            _write_atomic(dest, data)

        with mock.patch("tapdoc.tts_generate._write_atomic", side_effect=fail_dest):
            with self.assertRaises(OSError):
                generate_one(first, self.s, FakeEngine(), self.audio, self.prev)
        self.assertEqual({p: p.read_bytes() for p in files}, files)

    def test_missing_current_file_drops_stale_previous(self):
        first = generate_one(self.r, self.s, FakeEngine(), self.audio, self.prev)
        self.path.unlink()
        generate_one(first, self.s, FakeEngine(), self.audio, self.prev)
        self.assertEqual(list(self.prev.iterdir()), [])


class RestoreTest(TempCase):
    def test_restore_previous_restores_other_voice(self):
        set_override(self.s, self.r, voice="vi-VN-NamMinhNeural", doc="cu", rate=-40,
                     pitch=2, volume=3)
        first = generate_one(self.r, self.s, FakeEngine(), self.audio, self.prev)
        take = self.path.read_bytes()
        set_override(self.s, first, voice=self.s["voice"], doc="bờ", rate=-30,
                     pitch=0, volume=0)
        second = generate_one(first, self.s, FakeEngine(), self.audio, self.prev)
        restored = restore_previous(second, self.s, self.audio, self.prev)
        self.assertEqual(self.path.read_bytes(), take)
        self.assertEqual(restored["tts"], first["tts"])
        self.assertEqual(restored["source"], "tts_edge_namminh")
        self.assertEqual(self.s["voice"], "vi-VN-HoaiMyNeural")
        self.assertEqual(self.s["overrides"]["am_b"], dict(
            voice="vi-VN-NamMinhNeural", doc="cu", rate=-40, pitch=2, volume=3))
        self.assertFalse(needs_regen(self.s, restored))
        self.assertEqual(list(self.prev.iterdir()), [])

    def test_restore_unknown_voice_leaves_everything(self):
        first = generate_one(self.r, self.s, FakeEngine(), self.audio, self.prev)
        second = generate_one(first, self.s, FakeEngine(), self.audio, self.prev)
        metadata = self.prev / "am_b.json"
        old = json.loads(metadata.read_text(encoding="utf-8"))
        old["tts"]["voice"] = "khác"
        metadata.write_text(json.dumps(old), encoding="utf-8")
        before = copy.deepcopy((second, self.s))
        files = {p: p.read_bytes() for p in (self.path, *self.prev.iterdir())}
        with self.assertRaisesRegex(ValueError, "Giọng đọc"):
            restore_previous(second, self.s, self.audio, self.prev)
        self.assertEqual((second, self.s), before)
        self.assertEqual({p: p.read_bytes() for p in files}, files)


    def test_restore_brings_back_file_and_settings(self):
        set_override(self.s, self.r, doc="cu", rate=-40)
        first = generate_one(self.r, self.s, FakeEngine(), self.audio, self.prev)
        take = self.path.read_bytes()
        set_override(self.s, first, doc="cờ", rate=-20)
        second = generate_one(first, self.s, FakeEngine(), self.audio, self.prev)
        restored = restore_previous(second, self.s, self.audio, self.prev)
        self.assertEqual(self.path.read_bytes(), take)
        self.assertEqual(restored["tts"], first["tts"])
        self.assertEqual(restored["source"], first["source"])
        self.assertEqual(restored["status"], first["status"])
        self.assertEqual(self.s["overrides"]["am_b"], {"doc": "cu", "rate": -40})
        self.assertFalse(needs_regen(self.s, restored))

    def test_restore_legacy_without_tts(self):
        generated = generate_one(self.r, self.s, FakeEngine(), self.audio, self.prev)
        restored = restore_previous(generated, self.s, self.audio, self.prev)
        self.assertNotIn("tts", restored)
        self.assertEqual(restored["source"], "cu")
        self.assertEqual(self.path.read_bytes(), "bản cũ".encode())

    def test_restore_after_defaults_changed(self):
        first = generate_one(self.r, self.s, FakeEngine(), self.audio, self.prev)
        self.s["defaults"]["am"]["rate"] = -20
        second = generate_one(first, self.s, FakeEngine(), self.audio, self.prev)
        restored = restore_previous(second, self.s, self.audio, self.prev)
        self.assertEqual(self.s["overrides"]["am_b"], {"rate": -30})
        self.assertFalse(needs_regen(self.s, restored))


class ApproveTest(TempCase):
    def test_approve_deletes_prev(self):
        generated = generate_one(self.r, self.s, FakeEngine(), self.audio, self.prev)
        approved = approve(generated, self.prev)
        self.assertEqual(approved["status"], "dat")
        self.assertEqual(approved["tts"], generated["tts"])
        self.assertEqual(generated["status"], "cho_duyet")
        self.assertEqual(list(self.prev.iterdir()), [])


class BatchTest(TempCase):
    def test_failure_keeps_old_file_and_continues(self):
        self.r["tts"] = {"doc": "bờ", "rate": -30, "pitch": 0, "volume": 0,
                         "voice": "vi-VN-HoaiMyNeural", "sig": "bản cũ", "trimmed": False}
        rows = [self.r, row("am_c", "cờ")]
        before = copy.deepcopy(rows[0])
        saved = []
        report = run_batch(rows, self.s, FakeEngine(failures={"am_b"}, rows=rows), self.audio, self.prev,
                           save=lambda rs: saved.append(copy.deepcopy(rs)))
        self.assertEqual(report.done, ["am_c"])
        self.assertIn("am_b", report.failed)
        self.assertIn("bờ", report.failed["am_b"])
        self.assertEqual(rows[0], before)
        self.assertEqual(self.path.read_bytes(), "bản cũ".encode())
        self.assertTrue((self.audio / "am_c.mp3").is_file())
        self.assertEqual(saved[-1], rows)

    def test_skips_approved_unless_asked(self):
        rows = [row(status="dat")]
        engine = FakeEngine()
        self.assertEqual(run_batch(rows, self.s, engine, self.audio, self.prev).skipped, 1)
        self.assertEqual(engine.calls, [])
        self.assertEqual(run_batch(rows, self.s, engine, self.audio, self.prev,
                                   include_approved=True).done, ["am_b"])

    def test_include_approved_still_skips_up_to_date_rows(self):
        # "Gồm mã đã duyệt" thêm mã đã duyệt mà khác thông số, không tạo lại mã đã khớp cấu hình.
        fresh = generate_one(row("am_c", "cờ"), self.s, FakeEngine(), self.audio, self.prev)
        approved_fresh = {**fresh, "id": "am_d", "file": "audio/am_d.mp3", "status": "dat"}  # cùng chữ, cùng chữ ký
        approved_stale = row("am_dd", "đờ", status="dat")
        rows = [fresh, approved_fresh, approved_stale]
        report = run_batch(rows, self.s, FakeEngine(), self.audio, self.prev, include_approved=True)
        self.assertEqual(report.done, ["am_dd"])
        self.assertEqual(report.skipped, 2)

    def test_filters_lesson_kind(self):
        rows = [self.r, row("cau_x", "bé đi", "cau"), row("am_c", "cờ")]
        rows[2]["bai"] = ["tv1_t1_b02"]
        report = run_batch(rows, self.s, FakeEngine(), self.audio, self.prev,
                           lesson="tv1_t1_b01", kind="am", ids=["am_b", "am_c"])
        self.assertEqual((report.done, report.skipped), (["am_b"], 2))


class CliTest(TempCase):
    def call_cli(self, argv, factory):
        manifests = self.root / "manifests"
        save_rows(manifests / "audio_manifest.json", [self.r])
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(cli, "MANIFESTS", manifests), \
                mock.patch.object(cli, "UNITY_RES", self.root), \
                mock.patch.object(cli, "TTS_SETTINGS", self.root / "settings.json"), \
                mock.patch.object(cli, "TTS_PREV", self.prev), \
                redirect_stdout(out), redirect_stderr(err):
            from tapdoc.tts_settings import save_settings
            save_settings(self.root / "settings.json", self.s)
            code = cli.main(argv, engine_factory=factory)
        return code, out.getvalue() + err.getvalue()

    def test_cli_tts_dry_run_lists_ids(self):
        factory = mock.Mock(side_effect=AssertionError("không được tạo bộ đọc"))
        code, output = self.call_cli(["tts", "--thu"], factory)
        self.assertEqual(code, 0)
        self.assertIn("am_b", output)
        self.assertEqual(self.path.read_bytes(), "bản cũ".encode())

    def test_cli_tts_missing_package_exit_2(self):
        code, output = self.call_cli(["tts"], mock.Mock(side_effect=TtsUnavailable()))
        self.assertEqual(code, 2)
        self.assertIn("python -m pip install -r tools/requirements-tts.txt", output)

    def test_cli_tts_success_and_failure_summary(self):
        code, output = self.call_cli(["tts"], FakeEngine)
        self.assertEqual(code, 0)
        self.assertIn("Đã tạo 1, lỗi 0, bỏ qua 0", output)
        code, output = self.call_cli(["tts"], lambda: FakeEngine(failures={"bờ"}))
        self.assertEqual(code, 1)
        self.assertIn("am_b", output)
        self.assertIn("Đã tạo 0, lỗi 1", output)

    def test_cli_tts_keeps_reviews_saved_meanwhile(self):
        # Chủ dự án duyệt trên trang trong lúc lệnh tts chạy: lệnh chỉ ghi dòng vừa tạo vào danh mục mới nhất.
        manifest = self.root / "manifests" / "audio_manifest.json"
        rows = [self.r, row("am_c", "cờ"), row("am_d", "dờ", status="dat")]
        save_rows(manifest, rows)
        base = FakeEngine()

        class ReviewMeanwhile:
            def synthesize(self, p):
                if p.doc == "cờ":
                    live = json.loads(manifest.read_text(encoding="utf-8"))
                    for r in live:
                        if r["id"] == "am_b":
                            r["status"] = "dat"
                        if r["id"] == "am_d":
                            r["ghi_chu"] = "chủ dự án ghi"
                    save_rows(manifest, live)
                return base.synthesize(p)
        out = io.StringIO()
        with mock.patch.object(cli, "MANIFESTS", manifest.parent), \
                mock.patch.object(cli, "UNITY_RES", self.root), \
                mock.patch.object(cli, "TTS_SETTINGS", self.root / "settings.json"), \
                mock.patch.object(cli, "TTS_PREV", self.prev), redirect_stdout(out), redirect_stderr(out):
            from tapdoc.tts_settings import save_settings
            save_settings(self.root / "settings.json", self.s)
            self.assertEqual(cli.main(["tts"], engine_factory=ReviewMeanwhile), 0, out.getvalue())
        live = {r["id"]: r for r in json.loads(manifest.read_text(encoding="utf-8"))}
        self.assertEqual(live["am_b"]["status"], "dat")
        self.assertEqual(live["am_b"]["source"], "tts_edge_hoaimy")
        self.assertEqual(live["am_d"]["ghi_chu"], "chủ dự án ghi")
        self.assertEqual(live["am_c"]["source"], "tts_edge_hoaimy")
        self.assertEqual(live["am_c"]["status"], "cho_duyet")


class EdgeEngineTest(unittest.TestCase):
    def test_lazy_missing_package(self):
        with mock.patch.dict("sys.modules", {"edge_tts": None}):
            with self.assertRaises(TtsUnavailable):
                EdgeEngine()

    def test_retry_and_word_boundaries(self):
        attempts = []

        class Communicate:
            def __init__(self, *args, **kwargs):
                attempts.append((args, kwargs))

            async def stream(self):
                if len(attempts) < 4:
                    raise OSError("mất mạng")
                yield {"type": "audio", "data": fake_mp3(1.2)}
                yield {"type": "WordBoundary", "offset": 1750000, "duration": 4285830}

        with mock.patch.dict("sys.modules", {"edge_tts": mock.Mock(Communicate=Communicate)}), \
                mock.patch("tapdoc.tts_engine.asyncio.sleep", new_callable=mock.AsyncMock) as wait:
            result = EdgeEngine().synthesize(effective_params(settings(), row()))
        self.assertEqual(len(attempts), 4)
        self.assertEqual([c.args[0] for c in wait.call_args_list], [1, 2, 4])
        self.assertEqual(attempts[-1][1], {"rate": "-30%", "pitch": "+0Hz", "volume": "+0%",
                                         "boundary": "WordBoundary"})
        self.assertAlmostEqual(result.speech_start, 0.175)
        self.assertAlmostEqual(result.speech_end, 0.603583)

    def test_empty_audio_fails_after_four_tries(self):
        class Communicate:
            async def stream(self):
                if False:
                    yield

        factory = mock.Mock(return_value=Communicate())
        with mock.patch.dict("sys.modules", {"edge_tts": mock.Mock(Communicate=factory)}), \
                mock.patch("tapdoc.tts_engine.asyncio.sleep", new_callable=mock.AsyncMock):
            with self.assertRaises(TtsError):
                EdgeEngine().synthesize(effective_params(settings(), row()))
        self.assertEqual(factory.call_count, 4)


class EdgeEngineNoRetryTest(unittest.TestCase):
    def test_bad_parameters_fail_at_once_without_waiting(self):
        # Sai tên giọng hay thông số thì thử lại cũng hỏng y như cũ: báo ngay, không chờ 1+2+4 giây.
        factory = mock.Mock(side_effect=ValueError("Invalid voice 'vi-VN-Sai'"))
        with mock.patch.dict("sys.modules", {"edge_tts": mock.Mock(Communicate=factory)}), \
                mock.patch("tapdoc.tts_engine.asyncio.sleep", new_callable=mock.AsyncMock) as wait:
            with self.assertRaises(TtsError) as ctx:
                EdgeEngine().synthesize(effective_params(settings(), row()))
        self.assertEqual(factory.call_count, 1)
        wait.assert_not_called()
        self.assertIn("Invalid voice", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
