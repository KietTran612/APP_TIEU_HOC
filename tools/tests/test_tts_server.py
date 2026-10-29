"""Hợp đồng HTTP công cụ giọng đọc; chỉ dùng file tạm và bộ đọc giả."""
import http.client
import json
import tempfile
import threading
import unittest
from pathlib import Path

from tapdoc.manifest import load_rows, save_rows
from tapdoc.review_server import make_server
from tapdoc.tts_settings import save_settings
from tests.tts_fakes import FakeEngine, fake_mp3


class TtsServerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.manifests = self.root / "manifests"
        self.res = self.root / "res"
        self.prev = self.root / "prev"
        self.settings_path = self.root / "settings.json"
        self.notes = self.root / "chain_notes.json"
        self.lessons = self.res / "lessons"
        self.lessons.mkdir(parents=True)
        (self.res / "audio").mkdir()
        self.rows = [dict(id="am_q", text="q", kind="am", bai=["b01"],
                          status="cho_duyet", source="tam", ghi_chu="",
                          file="audio/am_q.mp3"),
                     dict(id="am_a", text="a", kind="am", bai=["b01"],
                          status="dat", source="tam", ghi_chu="",
                          file="audio/am_a.mp3")]
        save_rows(self.manifests / "audio_manifest.json", self.rows)
        save_rows(self.manifests / "image_manifest.json", [])
        self.settings = dict(voice="vi-VN-HoaiMyNeural", overrides={}, defaults={
            k: dict(rate=-30 if k in ("am", "van", "dau") else -25 if k == "tieng" else -15,
                    pitch=0, volume=0)
            for k in ("am", "van", "dau", "tieng", "tu", "cau", "huong_dan", "khen")})
        save_settings(self.settings_path, self.settings)
        self.old = fake_mp3(0.2)
        for row in self.rows:
            (self.res / row["file"]).write_bytes(self.old)
        self.lesson = dict(lesson_id="b01", title="Bài một", part1=[
            dict(type="spell", spell=dict(target="q", parts=[dict(text="q", audio="am_q")]))])
        (self.lessons / "index.json").write_text(json.dumps(dict(lessons=[
            dict(lesson_id="b01", title="Bài một", lesson_no=1)])), encoding="utf-8")
        (self.lessons / "b01.json").write_text(json.dumps(self.lesson), encoding="utf-8")
        self.engine = FakeEngine(rows=self.rows)
        self.release = threading.Event()
        self.server = make_server(0, self.manifests, self.res,
            settings_path=self.settings_path, prev_dir=self.prev,
            lessons_dir=self.lessons, notes_path=self.notes,
            engine_factory=lambda: self.engine)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop)

    def stop(self):
        self.release.set()
        worker = getattr(self.server, "batch_thread", None)
        if worker is not None:
            worker.join(3)
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(3)

    def request(self, path, payload=None, *, raw=False):
        conn = http.client.HTTPConnection(*self.server.server_address, timeout=5)
        try:
            body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
            conn.request("GET" if payload is None else "POST", path, body=body,
                         headers={"Content-Type": "application/json"})
            resp = conn.getresponse()
            data = resp.read()
            return resp.status, data if raw else json.loads(data)
        finally:
            conn.close()

    def post(self, path, payload):
        status, data = self.request(path, payload)
        self.assertEqual(status, 200, data)
        return data

    def row(self):
        status, data = self.request("/api/tts")
        self.assertEqual(status, 200, data)
        return data["rows"][0]

    def test_row_voice_override_and_voices_listed(self):
        status, data = self.request("/api/tts")
        self.assertEqual(status, 200)
        self.assertEqual(data["voice"], "vi-VN-HoaiMyNeural")
        self.assertEqual(data["voices"], [
            dict(id="vi-VN-HoaiMyNeural", label="HoaiMy (nữ)"),
            dict(id="vi-VN-NamMinhNeural", label="NamMinh (nam)")])
        self.post("/api/tts/generate", dict(id="am_q"))
        row = self.post("/api/tts/row", dict(id="am_q", voice="vi-VN-NamMinhNeural"))
        self.assertEqual(row["params"]["voice"], "vi-VN-NamMinhNeural")
        self.assertTrue(row["needs_regen"])
        self.assertTrue(row["overridden"])
        saved = json.loads(self.settings_path.read_text(encoding="utf-8"))
        self.assertEqual(saved["voice"], "vi-VN-HoaiMyNeural")
        self.assertEqual(saved["overrides"]["am_q"], dict(voice="vi-VN-NamMinhNeural"))
        self.assertEqual(self.row()["params"]["voice"], "vi-VN-NamMinhNeural")
        restored = self.post("/api/tts/row", dict(id="am_q", voice=data["voice"]))
        self.assertFalse(restored["needs_regen"])
        self.assertFalse(restored["overridden"])

    def test_row_unknown_voice_400(self):
        before = self.settings_path.read_bytes()
        manifest = (self.manifests / "audio_manifest.json").read_bytes()
        for voice in ("khác", "", 123, [], None):
            with self.subTest(voice=voice):
                status, data = self.request("/api/tts/row", dict(id="am_q", voice=voice))
                self.assertEqual(status, 400)
                self.assertIn("error", data)
                self.assertEqual(self.settings_path.read_bytes(), before)
                self.assertEqual((self.manifests / "audio_manifest.json").read_bytes(), manifest)
                self.assertEqual((self.res / "audio/am_q.mp3").read_bytes(), self.old)

    def test_generate_then_prev_served(self):
        row = self.post("/api/tts/generate", dict(id="am_q"))
        self.assertEqual(row["status"], "cho_duyet")
        self.assertEqual(row["source"], "tts_edge_hoaimy")
        self.assertFalse(row["needs_regen"])
        self.assertTrue(row["has_prev"])
        self.assertEqual(self.request("/media/prev/am_q.mp3", raw=True), (200, self.old))
        self.assertNotEqual((self.res / "audio/am_q.mp3").read_bytes(), self.old)
        self.assertEqual(len(self.engine.calls), 1)

    def test_row_override_marks_needs_regen(self):
        self.post("/api/tts/generate", dict(id="am_q"))
        row = self.post("/api/tts/row", dict(id="am_q", doc="cu", rate=-40))
        self.assertEqual(row["params"]["doc"], "cu")
        self.assertEqual(row["params"]["rate"], -40)
        self.assertTrue(row["needs_regen"])
        self.assertEqual(json.loads(self.settings_path.read_text(encoding="utf-8"))["overrides"]["am_q"],
                         dict(doc="cu", rate=-40))

    def test_defaults_change_counts(self):
        self.post("/api/tts/generate", dict(id="am_q"))
        result = self.post("/api/tts/defaults", dict(kind="am", rate=-35, pitch=2, volume=3))
        self.assertEqual(result["needs_regen"], 1)
        _, data = self.request("/api/tts")
        self.assertTrue(data["rows"][0]["needs_regen"])
        self.assertFalse(data["rows"][1]["needs_regen"])
        self.assertTrue(data["rows"][1]["differs"])

    def test_restore_and_approve(self):
        first = self.post("/api/tts/generate", dict(id="am_q"))
        audio = (self.res / "audio/am_q.mp3").read_bytes()
        self.post("/api/tts/row", dict(id="am_q", rate=-40))
        self.post("/api/tts/generate", dict(id="am_q"))
        restored = self.post("/api/tts/restore", dict(id="am_q"))
        self.assertEqual(restored["tts"], first["tts"])
        self.assertFalse(restored["needs_regen"])
        self.assertEqual((self.res / "audio/am_q.mp3").read_bytes(), audio)
        self.post("/api/tts/generate", dict(id="am_q"))
        self.post("/api/review", dict(manifest="audio", id="am_q", status="dat"))
        self.assertFalse(self.row()["has_prev"])
        self.assertFalse((self.prev / "am_q.json").exists())

    def test_batch_job_progress_and_409(self):
        entered = threading.Event()
        base = self.engine
        release = self.release
        class SlowEngine:
            def synthesize(self, params):
                entered.set()
                if not release.wait(3):
                    raise RuntimeError("Hết thời gian chờ test")
                return base.synthesize(params)
        self.engine = SlowEngine()
        self.post("/api/tts/batch", dict(lesson="b01", kind="am"))
        self.assertTrue(entered.wait(2))
        status, job = self.request("/api/tts/job")
        self.assertEqual(status, 200)
        self.assertTrue(job["running"])
        self.assertEqual(job["total"], 1)
        self.assertEqual(job["current"], "am_q")
        self.assertEqual(self.request("/api/tts/batch", {})[0], 409)
        # Duyệt mã khác khi bộ đọc đang chờ: không bị khoá cả lô hay ghi đè sau đó.
        self.post("/api/review", dict(manifest="audio", id="am_a", status="khong_dat", ghi_chu="giữ"))
        self.release.set()
        self.server.batch_thread.join(3)
        _, job = self.request("/api/tts/job")
        self.assertFalse(job["running"])
        self.assertEqual(job["done"], 1)
        self.assertEqual(job["failed"], {})
        rows = load_rows(self.manifests / "audio_manifest.json")
        self.assertIn("tts", rows[0])
        self.assertEqual(rows[1]["ghi_chu"], "giữ")
        self.assertNotIn("tts", rows[1])

    def test_engine_failure_502_keeps_file(self):
        self.engine.failures.add("q")
        before = (self.manifests / "audio_manifest.json").read_bytes()
        status, result = self.request("/api/tts/generate", dict(id="am_q"))
        self.assertEqual(status, 502)
        self.assertIn("không đọc được", result["error"])
        self.assertEqual((self.res / "audio/am_q.mp3").read_bytes(), self.old)
        self.assertEqual((self.manifests / "audio_manifest.json").read_bytes(), before)
        self.assertFalse(self.prev.exists())

    def test_chain_note_roundtrip(self):
        self.assertEqual(self.request("/api/chain-notes"), (200, []))
        note = dict(lesson="b01", where="part1[0].spell", chain="q", note="nghe lại")
        self.post("/api/chain-notes", note)
        self.assertEqual(self.request("/api/chain-notes"), (200, [note]))
        self.post("/api/chain-notes", {**note, "note": "sửa"})
        self.assertEqual(len(json.loads(self.notes.read_text(encoding="utf-8"))), 1)
        self.post("/api/chain-notes", {**note, "note": ""})
        self.assertEqual(self.request("/api/chain-notes"), (200, []))

    def test_bad_input_400(self):
        for path, payload in [
            ("/api/tts/row", dict(id="missing")),
            ("/api/tts/row", dict(id="am_q", rate=True)),
            ("/api/tts/row", dict(id="am_q", doc=123)),
            ("/api/tts/row", dict(id="am_q", rate=None)),
            ("/api/tts/defaults", dict(kind="other", rate=0, pitch=0, volume=0)),
            ("/api/tts/defaults", dict(kind="am", rate=31, pitch=0, volume=0)),
            ("/api/tts/batch", dict(include_approved="yes")),
            ("/api/tts/batch", dict(kind=[])),
            ("/api/tts/generate", dict(id="../secret")),
            ("/api/tts/restore", dict(id="am_q")),
            ("/api/chain-notes", dict(lesson="b01", where="x", chain=[], note="x")),
            ("/api/tts/row", []),
        ]:
            with self.subTest(path=path, payload=payload):
                self.assertEqual(self.request(path, payload)[0], 400)

    def test_lessons_and_safe_paths(self):
        self.assertEqual(self.request("/api/lessons")[1][0]["lesson_id"], "b01")
        self.assertEqual(self.request("/api/lesson/b01"), (200, self.lesson))
        for path in ("/api/lesson/..%2Fsettings", "/api/lesson/index",
                     "/media/prev/..%2Fsettings.mp3", "/media/prev/AM_Q.mp3"):
            self.assertIn(self.request(path)[0], (400, 404))

    def test_index_has_tts_controls(self):
        status, raw = self.request("/", raw=True)
        self.assertEqual(status, 200)
        html = raw.decode("utf-8")
        for element_id in ("tts-defaults", "tts-batch", "tab-lesson"):
            self.assertIn('id="' + element_id + '"', html)
        for text in ("tts-row", "tts-voice", "/api/tts/job", "/api/chain-notes", "500",
                     "Cách đọc", "Dùng lại bản trước", "Cần tạo lại", "Đã chỉnh tay"):
            self.assertIn(text, html)

    def test_batch_saves_each_id_and_continues_after_failure(self):
        entered = threading.Event()
        base = self.engine
        base.failures.add("a")
        release = self.release
        class PausedSecondEngine:
            def synthesize(self, params):
                if params.doc == "a":
                    entered.set()
                    if not release.wait(3):
                        raise RuntimeError("Hết thời gian chờ test")
                return base.synthesize(params)
        self.engine = PausedSecondEngine()
        self.post("/api/tts/batch", dict(include_approved=True))
        self.assertTrue(entered.wait(2))
        saved = load_rows(self.manifests / "audio_manifest.json")
        self.assertIn("tts", saved[0])
        self.assertNotIn("tts", saved[1])
        _, job = self.request("/api/tts/job")
        self.assertEqual(job["done"], 1)
        self.assertEqual(job["total"], 2)
        self.release.set()
        self.server.batch_thread.join(3)
        _, job = self.request("/api/tts/job")
        self.assertFalse(job["running"])
        self.assertEqual(job["done"], 1)
        self.assertIn("am_a", job["failed"])
        self.assertEqual((self.res / "audio/am_a.mp3").read_bytes(), self.old)
        self.assertEqual(len(base.calls), 2)

    def test_batch_keeps_audio_approved_while_synthesizing(self):
        entered = threading.Event()
        base = self.engine
        release = self.release
        class SlowEngine:
            def synthesize(self, params):
                entered.set()
                if not release.wait(3):
                    raise RuntimeError("Hết thời gian chờ test")
                return base.synthesize(params)
        self.engine = SlowEngine()
        self.post("/api/tts/batch", {})
        self.assertTrue(entered.wait(2))
        self.post("/api/review", dict(manifest="audio", id="am_q", status="dat", ghi_chu="giữ bản này"))
        self.release.set()
        self.server.batch_thread.join(3)
        self.assertEqual((self.res / "audio/am_q.mp3").read_bytes(), self.old)
        self.assertEqual(self.row()["status"], "dat")
        self.assertEqual(self.row()["ghi_chu"], "giữ bản này")
        self.assertFalse(self.row()["has_prev"])

    def test_lesson_scan_is_cached_until_a_lesson_changes(self):
        import os
        from unittest import mock
        from tapdoc import review_server
        with mock.patch.object(review_server, "shown_in_app", wraps=review_server.shown_in_app) as scan:
            self.tts_rows()
            self.tts_rows()
            self.assertEqual(scan.call_count, 1)
            lesson = self.lessons / "b01.json"
            lesson.write_text(json.dumps({**self.lesson, "title": "Bài một (sửa)"}), encoding="utf-8")
            stat = lesson.stat()
            os.utime(lesson, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000_000))
            self.tts_rows()
            self.assertEqual(scan.call_count, 2)

    def test_second_server_on_same_port_is_refused(self):
        # Windows cho hai máy chủ cùng nghe một cổng nếu bật SO_REUSEADDR: yêu cầu sẽ chia lung tung.
        port = self.server.server_address[1]
        with self.assertRaises(OSError):
            make_server(port, self.manifests, self.res).server_close()

    def test_rows_show_text_displayed_in_app(self):
        # Cột "Hiển thị": chữ bé nhìn thấy khi mã được đọc, ưu tiên phần học chính, rồi tới câu hỏi luyện tập.
        lesson = dict(lesson_id="b01", title="Bài một",
                      part1=[dict(type="spell", spell=dict(target="q", parts=[dict(text="q", audio="am_q")])),
                             dict(type="letter_pairs", items=[dict(text="q", upper="Q", audio="am_q"),
                                                              dict(text="Q", audio="am_q")])],
                      part2=[dict(prompt_audio="am_q", prompt_text="q_"),
                             dict(prompt_audio="am_a", prompt_text="a_", instruction_audio="hd_b01_01")])
        (self.lessons / "b01.json").write_text(json.dumps(lesson, ensure_ascii=False), encoding="utf-8")
        rows = self.tts_rows()
        self.assertEqual(rows["am_q"]["hien_thi"], ["q", "Q"])
        self.assertEqual(rows["am_a"]["hien_thi"], ["a_"])

    def tts_rows(self):
        status, data = self.request("/api/tts")
        self.assertEqual(status, 200, data)
        return {row["id"]: row for row in data["rows"]}

    def test_row_without_text_in_app_shows_nothing(self):
        (self.lessons / "b01.json").write_text(json.dumps(dict(lesson_id="b01", part1=[], part2=[
            dict(prompt_audio="am_a", prompt_text="", instruction_audio="am_q")])), encoding="utf-8")
        rows = self.tts_rows()
        self.assertEqual(rows["am_a"]["hien_thi"], [])
        self.assertEqual(rows["am_q"]["hien_thi"], [])

    def test_missing_engine_dependency_finishes_job(self):
        from tapdoc.tts_engine import TtsUnavailable
        class UnavailableEngine:
            def synthesize(self, params):
                raise TtsUnavailable()
        self.engine = UnavailableEngine()
        self.assertEqual(self.request("/api/tts/generate", dict(id="am_q"))[0], 502)
        self.post("/api/tts/batch", {})
        self.server.batch_thread.join(3)
        _, job = self.request("/api/tts/job")
        self.assertFalse(job["running"])
        self.assertIn("edge-tts", job["failed"]["am_q"])
        self.assertEqual((self.res / "audio/am_q.mp3").read_bytes(), self.old)

    def test_missing_engine_at_start_reported_for_whole_batch(self):
        from tapdoc.tts_engine import TtsUnavailable
        def missing():
            raise TtsUnavailable()
        self.server.engine_factory = missing
        status, data = self.request("/api/tts/generate", dict(id="am_q"))
        self.assertEqual(status, 502)
        self.assertIn("edge-tts", data["error"])
        self.post("/api/tts/batch", {})
        self.server.batch_thread.join(3)
        _, job = self.request("/api/tts/job")
        self.assertFalse(job["running"])
        self.assertEqual(list(job["failed"]), ["batch"])
        self.assertIn("edge-tts", job["failed"]["batch"])

    def test_unexpected_error_returns_500_json(self):
        class BrokenEngine:
            def synthesize(self, params):
                raise RuntimeError("hỏng bất ngờ")
        self.engine = BrokenEngine()
        status, data = self.request("/api/tts/generate", dict(id="am_q"))
        self.assertEqual(status, 500)
        self.assertIn("hỏng bất ngờ", data["error"])
        self.assertEqual((self.res / "audio/am_q.mp3").read_bytes(), self.old)

    def test_generate_keeps_page_usable_and_records_actual_params(self):
        entered = threading.Event()
        base = self.engine
        release = self.release
        class SlowEngine:
            def synthesize(self, params):
                entered.set()
                if not release.wait(5):
                    raise RuntimeError("Hết thời gian chờ test")
                return base.synthesize(params)
        self.engine = SlowEngine()
        result = []
        errors = []
        def generate():
            try:
                result.append(self.request("/api/tts/generate", dict(id="am_q")))
            except Exception as error:
                errors.append(error)
        worker = threading.Thread(target=generate)
        worker.start()
        try:
            self.assertTrue(entered.wait(2))
            self.post("/api/tts/defaults", dict(kind="am", rate=-40, pitch=0, volume=0))
            self.post("/api/review", dict(manifest="audio", id="am_a", status="dat", ghi_chu="nghe rõ"))
        finally:
            self.release.set()
            worker.join(5)
        self.assertFalse(worker.is_alive())
        self.assertEqual(errors, [])
        self.assertEqual(result[0][0], 200)
        row = result[0][1]
        self.assertEqual(row["tts"]["rate"], -30)
        self.assertEqual(row["params"]["rate"], -40)
        self.assertTrue(row["needs_regen"])
        self.assertEqual(load_rows(self.manifests / "audio_manifest.json")[1]["ghi_chu"], "nghe rõ")
