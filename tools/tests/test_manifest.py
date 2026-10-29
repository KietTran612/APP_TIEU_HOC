import copy
import io
import json
import tempfile
import unicodedata
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from tapdoc import __main__ as cli
from tapdoc.build import BuildResult, build_lesson
from tapdoc.manifest import (
    ManifestError,
    careful_listen,
    load_rows,
    save_rows,
    update_audio_manifest,
    update_image_manifest,
)
from tapdoc.system_assets import SYSTEM_AUDIO, SYSTEM_IMAGES

AUDIO_FIELDS = ["id", "text", "kind", "file", "source", "status", "can_nghe_ky", "ghi_chu", "bai"]
IMAGE_FIELDS = ["id", "mo_ta", "bai", "file", "source", "status", "ghi_chu"]
CHANGED = "chữ đã đổi, cần tạo lại"

# Bài mẫu nhỏ kiểu bài 13, thêm một bước đánh vần "cử" để có mã tieng_cuwr.
SRC13 = {
    "lesson_id": "tv1_t1_b13", "book": "tv1_t1_1990", "lesson_no": 13, "type": "am_moi", "title": "u ư",
    "source": {"pages": [18], "scan_file": "010", "verification": "page_verified"},
    "new_units": ["u", "ư"],
    "images": {
        "img_b13_cais_ddu": "Bé gái ngồi trên ván đu, hai tay nắm hai sợi dây đu",
        "img_b13_cur_tuwf": "Một củ từ (khoai từ) vỏ sần, có vài rễ con",
    },
    "part1": [
        {"type": "unit", "text": "u"},
        {"type": "keyword", "text": "cái đu", "image": "img_b13_cais_ddu"},
        {"type": "spell", "target": "đu", "then": "cái đu"},
        {"type": "words", "marker": "", "items": [{"text": "củ từ", "image": "img_b13_cur_tuwf"}]},
        {"type": "sentence", "marker": "●", "text": "má có củ từ"},
        {"type": "spell", "target": "cử"},
    ],
    "part2": [],
}


def fake(lesson_id, audio=None, images=None):
    """Kết quả dựng giả: danh mục chỉ đọc lesson_id, audio và images."""
    return BuildResult({"lesson_id": lesson_id}, dict(audio or {}), dict(images or {}))


def touch(directory, *ids, ext="mp3"):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for i in ids:
        (directory / f"{i}.{ext}").write_bytes(b"x")


class TempDirCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.audio_dir = self.root / "audio"
        self.audio_dir.mkdir()
        self.image_dir = self.root / "images"
        self.image_dir.mkdir()


class CarefulListenTest(unittest.TestCase):
    def test_careful(self):
        for t, want in [("cử", True), ("ca", False), ("dù", True), ("lan", True), ("má", False), ("cá", False),
                        ("cũ", True)]:
            self.assertEqual(careful_listen(t), want, t)

    def test_onsets(self):
        for t in ["da", "gia", "va", "sa", "xa", "cha", "tra", "gì"]:
            self.assertTrue(careful_listen(t), t)
        for t in ["ba", "nga", "nha", "kha", "tho", "đa", "ca", "la"]:
            self.assertFalse(careful_listen(t), t)

    def test_rime_endings(self):
        for t in ["an", "tung", "bát", "bạc", "lên", "ông"]:
            self.assertTrue(careful_listen(t), t)
        for t in ["anh", "bách", "inh", "mai", "mao"]:  # kết thúc nh, ch, i, o: không tính
            self.assertFalse(careful_listen(t), t)

    def test_tone_hoi_nga(self):
        self.assertTrue(careful_listen("bể"))
        self.assertTrue(careful_listen("bẽ"))
        for t in ["bè", "bé", "bẹ"]:  # huyền, sắc, nặng: không tính
            self.assertFalse(careful_listen(t), t)

    def test_any_syllable_counts(self):
        self.assertFalse(careful_listen("má cá"))
        self.assertTrue(careful_listen("má dù"))
        self.assertTrue(careful_listen("củ từ"))

    def test_skips_non_syllables(self):
        self.assertFalse(careful_listen("123 ca"))
        self.assertTrue(careful_listen("123 dù"))
        self.assertFalse(careful_listen(""))
        self.assertFalse(careful_listen("?!"))

    def test_nfd_input(self):
        self.assertTrue(careful_listen(unicodedata.normalize("NFD", "cử")))


class RowsFileTest(TempDirCase):
    def test_missing_file_is_empty(self):
        self.assertEqual(load_rows(self.root / "khong_co.json"), [])

    def test_round_trip_and_format(self):
        path = self.root / "con" / "sau" / "m.json"
        rows = [{"id": "am_dd", "text": "đờ", "bai": ["chung"]}, {"id": "b", "text": "bờ"}]
        save_rows(path, rows)
        self.assertEqual(load_rows(path), rows)
        raw = path.read_bytes().decode("utf-8")
        self.assertIn("đờ", raw)  # ensure_ascii=False
        self.assertTrue(raw.endswith("]\n"))
        self.assertFalse(raw.endswith("\n\n"))
        self.assertIn('\n  {\n    "id": "am_dd"', raw)  # indent=2
        self.assertNotIn(b"\r", path.read_bytes())

    def test_empty_list(self):
        path = self.root / "r.json"
        save_rows(path, [])
        self.assertEqual(load_rows(path), [])

    def test_save_rows_is_atomic(self):
        path = self.root / "m.json"
        save_rows(path, [{"id": "a"}])
        with mock.patch("tapdoc.manifest.os.replace", side_effect=OSError("đĩa đầy")):
            with self.assertRaises(OSError):
                save_rows(path, [{"id": "b"}])
        self.assertEqual(load_rows(path), [{"id": "a"}])
        self.assertEqual(list(self.root.glob("*.tmp")), [])

    def test_bad_file_is_manifest_error(self):
        path = self.root / "hong.json"
        path.write_text("{khong phai json", encoding="utf-8")
        with self.assertRaises(ManifestError):
            load_rows(path)
        path.write_text('{"id": "a"}', encoding="utf-8")
        with self.assertRaises(ManifestError):
            load_rows(path)
        path.write_text('["a"]', encoding="utf-8")
        with self.assertRaises(ManifestError):
            load_rows(path)
        path.write_text('[{"text": "không có id"}]', encoding="utf-8")
        with self.assertRaises(ManifestError):
            load_rows(path)


class AudioManifestTest(TempDirCase):
    @classmethod
    def setUpClass(cls):
        cls.res13 = build_lesson(copy.deepcopy(SRC13))

    def test_status_rules(self):  # có am_dd.mp3, không có van_u.mp3
        touch(self.audio_dir, "am_dd")
        rows = update_audio_manifest(
            [self.res13],
            [{"id": "am_dd", "status": "dat", "source": "chatgpt_tam", "ghi_chu": "ok", "text": "đờ"}],
            self.audio_dir)
        by = {r["id"]: r for r in rows}
        self.assertEqual((by["am_dd"]["status"], by["am_dd"]["ghi_chu"]), ("dat", "ok"))
        self.assertEqual(by["am_dd"]["source"], "chatgpt_tam")
        self.assertEqual(by["van_u"]["status"], "chua_co")
        self.assertEqual(by["khen_01"]["bai"], ["chung"])
        self.assertEqual(by["cau_b13_01"]["kind"], "cau")
        self.assertTrue(by["tieng_cuwr"]["can_nghe_ky"])

    def test_fields_order_file_and_defaults(self):
        rows = update_audio_manifest([self.res13], [], self.audio_dir)
        by = {r["id"]: r for r in rows}
        for r in rows:
            self.assertEqual(list(r), AUDIO_FIELDS, r["id"])
            self.assertEqual(r["file"], f"audio/{r['id']}.mp3")
        self.assertEqual(by["am_dd"]["text"], "đờ")
        self.assertEqual(by["am_dd"]["kind"], "am")
        self.assertEqual(by["am_dd"]["bai"], ["tv1_t1_b13"])
        self.assertEqual((by["am_dd"]["source"], by["am_dd"]["ghi_chu"], by["am_dd"]["status"]), ("", "", "chua_co"))
        self.assertIs(by["am_dd"]["can_nghe_ky"], False)
        self.assertIs(by["tieng_cuwr"]["can_nghe_ky"], True)

    def test_sorted_by_id_and_covers_lessons_and_system(self):
        rows = update_audio_manifest([self.res13], [], self.audio_dir)
        ids = [r["id"] for r in rows]
        self.assertEqual(ids, sorted(ids))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(set(self.res13.audio) <= set(ids))
        self.assertTrue(set(SYSTEM_AUDIO) <= set(ids))
        self.assertEqual(len(ids), len(set(self.res13.audio) | set(SYSTEM_AUDIO)))

    def test_system_rows(self):
        by = {r["id"]: r for r in update_audio_manifest([], [], self.audio_dir)}
        self.assertEqual(set(by), set(SYSTEM_AUDIO))
        for sid, text in SYSTEM_AUDIO.items():
            self.assertEqual(by[sid]["text"], text)
            self.assertEqual(by[sid]["bai"], ["chung"])
            self.assertEqual(by[sid]["kind"], "huong_dan" if sid.startswith("hd_") else "khen", sid)
        self.assertEqual(by["khen_02"]["kind"], "khen")
        self.assertEqual(by["hd_thu_lai"]["kind"], "huong_dan")

    def test_bai_lists_every_lesson_using_the_id(self):
        a = fake("tv1_t1_b14", {"am_dd": ("đờ", "am"), "van_u": ("u", "van")})
        b = fake("tv1_t1_b02", {"am_dd": ("đờ", "am")})
        by = {r["id"]: r for r in update_audio_manifest([a, b], [], self.audio_dir)}
        self.assertEqual(by["am_dd"]["bai"], ["tv1_t1_b02", "tv1_t1_b14"])
        self.assertEqual(by["van_u"]["bai"], ["tv1_t1_b14"])

    def test_new_row_with_file_is_cho_duyet(self):
        touch(self.audio_dir, "am_dd")
        by = {r["id"]: r for r in update_audio_manifest([self.res13], [], self.audio_dir)}
        self.assertEqual(by["am_dd"]["status"], "cho_duyet")

    def test_old_chua_co_with_file_is_cho_duyet(self):
        touch(self.audio_dir, "am_dd")
        old = [{"id": "am_dd", "text": "đờ", "status": "chua_co", "source": "s", "ghi_chu": "n"}]
        by = {r["id"]: r for r in update_audio_manifest([self.res13], old, self.audio_dir)}
        self.assertEqual((by["am_dd"]["status"], by["am_dd"]["source"], by["am_dd"]["ghi_chu"]),
                         ("cho_duyet", "s", "n"))

    def test_old_status_kept_when_file_exists(self):
        touch(self.audio_dir, "am_dd", "am_c", "am_m")
        old = [{"id": "am_dd", "text": "đờ", "status": "dat"},
               {"id": "am_c", "text": "cờ", "status": "khong_dat", "ghi_chu": "giọng nam"},
               {"id": "am_m", "text": "mờ", "status": "cho_duyet"}]
        by = {r["id"]: r for r in update_audio_manifest([self.res13], old, self.audio_dir)}
        self.assertEqual(by["am_dd"]["status"], "dat")
        self.assertEqual((by["am_c"]["status"], by["am_c"]["ghi_chu"]), ("khong_dat", "giọng nam"))
        self.assertEqual(by["am_m"]["status"], "cho_duyet")

    def test_missing_file_is_chua_co_whatever_the_old_status(self):
        old = [{"id": "am_dd", "text": "đờ", "status": "dat", "source": "chatgpt_tam", "ghi_chu": "ok"}]
        by = {r["id"]: r for r in update_audio_manifest([self.res13], old, self.audio_dir)}
        self.assertEqual(by["am_dd"]["status"], "chua_co")
        self.assertEqual((by["am_dd"]["source"], by["am_dd"]["ghi_chu"]), ("chatgpt_tam", "ok"))

    def test_only_mp3_files_count(self):
        touch(self.audio_dir, "am_dd", ext="wav")
        (self.audio_dir / "am_c.mp3").mkdir()  # thư mục, không phải file
        by = {r["id"]: r for r in update_audio_manifest([self.res13], [], self.audio_dir)}
        self.assertEqual(by["am_dd"]["status"], "chua_co")
        self.assertEqual(by["am_c"]["status"], "chua_co")

    def test_missing_audio_dir(self):
        rows = update_audio_manifest([self.res13], [], self.root / "khong_co")
        self.assertTrue(all(r["status"] == "chua_co" for r in rows))

    def test_text_changed(self):  # cau_b13_01 cũ là "má có củ"; có file
        touch(self.audio_dir, "cau_b13_01")
        rows = update_audio_manifest([self.res13], [{"id": "cau_b13_01", "text": "má có củ", "status": "dat"}],
                                     self.audio_dir)
        r = next(x for x in rows if x["id"] == "cau_b13_01")
        self.assertEqual(r["status"], "khong_dat")
        self.assertIn("chữ đã đổi", r["ghi_chu"])
        self.assertEqual(r["text"], "má có củ từ")

    def test_text_changed_prefixes_old_note_once(self):
        touch(self.audio_dir, "cau_b13_01")
        old = [{"id": "cau_b13_01", "text": "má có củ", "status": "dat", "ghi_chu": "ok"}]
        r = next(x for x in update_audio_manifest([self.res13], old, self.audio_dir) if x["id"] == "cau_b13_01")
        self.assertTrue(r["ghi_chu"].startswith(CHANGED), r["ghi_chu"])
        self.assertTrue(r["ghi_chu"].endswith("ok"), r["ghi_chu"])
        # Dựng lại lần nữa: chữ không đổi nữa, trạng thái và ghi chú giữ nguyên, không lặp ghi chú.
        again = next(x for x in update_audio_manifest([self.res13], [r], self.audio_dir) if x["id"] == "cau_b13_01")
        self.assertEqual((again["status"], again["ghi_chu"]), ("khong_dat", r["ghi_chu"]))
        self.assertEqual(again["ghi_chu"].count("chữ đã đổi"), 1)

    def test_text_changed_does_not_duplicate_existing_note(self):
        touch(self.audio_dir, "cau_b13_01")
        old = [{"id": "cau_b13_01", "text": "má có", "status": "khong_dat", "ghi_chu": CHANGED}]
        r = next(x for x in update_audio_manifest([self.res13], old, self.audio_dir) if x["id"] == "cau_b13_01")
        self.assertEqual((r["status"], r["ghi_chu"]), ("khong_dat", CHANGED))

    def test_text_changed_without_file_stays_chua_co(self):
        old = [{"id": "cau_b13_01", "text": "má có củ", "status": "dat", "ghi_chu": "ok"}]
        r = next(x for x in update_audio_manifest([self.res13], old, self.audio_dir) if x["id"] == "cau_b13_01")
        self.assertEqual((r["status"], r["ghi_chu"]), ("chua_co", "ok"))

    def test_case_or_punctuation_only_change_is_not_a_change(self):
        touch(self.audio_dir, "cau_b13_01")
        old = [{"id": "cau_b13_01", "text": "Má có củ từ!", "status": "dat", "ghi_chu": "ok"}]
        r = next(x for x in update_audio_manifest([self.res13], old, self.audio_dir) if x["id"] == "cau_b13_01")
        self.assertEqual((r["status"], r["ghi_chu"]), ("dat", "ok"))

    def test_old_rows_of_unused_ids_are_dropped(self):
        old = [{"id": "van_khong_dung", "text": "x", "status": "dat"}]
        ids = [r["id"] for r in update_audio_manifest([self.res13], old, self.audio_dir)]
        self.assertNotIn("van_khong_dung", ids)

    def test_does_not_modify_old_rows(self):
        old = [{"id": "am_dd", "text": "đờ", "status": "dat", "ghi_chu": "ok"}]
        snapshot = copy.deepcopy(old)
        touch(self.audio_dir, "am_dd")
        update_audio_manifest([self.res13], old, self.audio_dir)
        self.assertEqual(old, snapshot)

    def test_conflicting_text_across_lessons(self):
        a = fake("tv1_t1_b20", {"tieng_xoong": ("xoong", "tieng")})
        b = fake("tv1_t1_b21", {"tieng_xoong": ("xông", "tieng")})
        with self.assertRaises(ManifestError) as cm:
            update_audio_manifest([a, b], [], self.audio_dir)
        message = str(cm.exception)
        for part in ("tieng_xoong", "xoong", "xông"):
            self.assertIn(part, message)
        self.assertIsInstance(cm.exception, ValueError)

    def test_conflicting_text_against_system_audio(self):
        a = fake("tv1_t1_b20", {"khen_01": ("Giỏi quá", "khen")})
        with self.assertRaises(ManifestError) as cm:
            update_audio_manifest([a], [], self.audio_dir)
        message = str(cm.exception)
        for part in ("khen_01", "Giỏi quá", SYSTEM_AUDIO["khen_01"]):
            self.assertIn(part, message)

    def test_same_text_different_case_or_punctuation_is_not_a_conflict(self):
        a = fake("tv1_t1_b20", {"tieng_mas": ("Má", "tieng"), "khen_01": ("đúng rồi", "khen")})
        b = fake("tv1_t1_b21", {"tieng_mas": ("má", "tieng")})
        c = fake("tv1_t1_b22", {"tieng_mas": ("má.", "tieng"),
                                "tu_x": ("cá  mè", "tu")})
        d = fake("tv1_t1_b23", {"tu_x": ("cá mè!", "tu")})
        rows = update_audio_manifest([a, b, c, d], [], self.audio_dir)
        by = {r["id"]: r for r in rows}
        self.assertEqual(by["tieng_mas"]["text"], "Má")  # giữ lời đọc gặp đầu tiên
        self.assertEqual(by["tieng_mas"]["bai"], ["tv1_t1_b20", "tv1_t1_b21", "tv1_t1_b22"])
        self.assertEqual(by["tu_x"]["text"], "cá  mè")
        self.assertEqual(by["tu_x"]["bai"], ["tv1_t1_b22", "tv1_t1_b23"])
        self.assertEqual(by["khen_01"]["bai"], ["chung", "tv1_t1_b20"])
        self.assertEqual(by["khen_01"]["text"], SYSTEM_AUDIO["khen_01"])  # lời hệ thống được xét trước

    def test_nfd_text_is_not_a_conflict(self):
        nfd = unicodedata.normalize("NFD", "má")
        a = fake("tv1_t1_b20", {"tieng_mas": ("má", "tieng")})
        b = fake("tv1_t1_b21", {"tieng_mas": (nfd, "tieng")})
        by = {r["id"]: r for r in update_audio_manifest([a, b], [], self.audio_dir)}
        self.assertEqual(by["tieng_mas"]["text"], "má")

    def test_texts_are_nfc(self):
        nfd = unicodedata.normalize("NFD", "má")
        a = fake("tv1_t1_b20", {"tieng_mas": (nfd, "tieng")})
        by = {r["id"]: r for r in update_audio_manifest([a], [], self.audio_dir)}
        self.assertEqual(by["tieng_mas"]["text"], "má")
        self.assertTrue(unicodedata.is_normalized("NFC", by["tieng_mas"]["text"]))


class TtsFieldTest(TempDirCase):
    def test_build_keeps_tts_record(self):
        from tapdoc.tts_generate import generate_one
        from tests.test_build import src_of
        from tests.test_tts_settings import settings
        from tests.tts_fakes import FakeEngine

        result = build_lesson(src_of(part1=[{"type": "unit", "text": "b"}], new_units=["b"]))
        rows = update_audio_manifest([result], [], self.audio_dir)
        old = next(r for r in rows if r["id"] == "am_b")
        generated = generate_one(old, settings(), FakeEngine(), self.audio_dir, self.root / "prev")
        generated["status"] = "dat"
        rebuilt = update_audio_manifest([result], [generated], self.audio_dir)
        actual = next(r for r in rebuilt if r["id"] == "am_b")
        for key in ("tts", "source", "status"):
            self.assertEqual(actual[key], generated[key])


class ImageManifestTest(TempDirCase):
    @classmethod
    def setUpClass(cls):
        cls.res13 = build_lesson(copy.deepcopy(SRC13))

    def test_rows(self):
        rows = update_image_manifest([self.res13], [], self.image_dir)
        by = {r["id"]: r for r in rows}
        for r in rows:
            self.assertEqual(list(r), IMAGE_FIELDS, r["id"])
            self.assertEqual(r["file"], f"images/{r['id']}.png")
        self.assertEqual(set(by), set(SYSTEM_IMAGES) | {"img_b13_cais_ddu", "img_b13_cur_tuwf"})
        self.assertEqual([r["id"] for r in rows], sorted(by))
        self.assertEqual(by["img_b13_cais_ddu"]["mo_ta"], SRC13["images"]["img_b13_cais_ddu"])
        self.assertEqual(by["img_b13_cais_ddu"]["bai"], ["tv1_t1_b13"])
        self.assertEqual((by["img_b13_cais_ddu"]["source"], by["img_b13_cais_ddu"]["status"],
                          by["img_b13_cais_ddu"]["ghi_chu"]), ("", "chua_co", ""))
        for sid, text in SYSTEM_IMAGES.items():
            self.assertEqual((by[sid]["mo_ta"], by[sid]["bai"]), (text, ["chung"]))

    def test_system_only(self):
        rows = update_image_manifest([], [], self.image_dir)
        self.assertEqual({r["id"] for r in rows}, set(SYSTEM_IMAGES))

    def test_bai_lists_every_lesson(self):
        a = fake("tv1_t1_b14", images={"img_b14_x": "Tranh x"})
        b = fake("tv1_t1_b02", images={"img_b14_x": "Tranh x"})
        by = {r["id"]: r for r in update_image_manifest([a, b], [], self.image_dir)}
        self.assertEqual(by["img_b14_x"]["bai"], ["tv1_t1_b02", "tv1_t1_b14"])

    def test_status_rules(self):
        touch(self.image_dir, "img_b13_cais_ddu", "img_b13_cur_tuwf", "img_chung_sao", ext="png")
        old = [{"id": "img_b13_cais_ddu", "status": "dat", "source": "chatgpt_tam", "ghi_chu": "ok"},
               {"id": "img_b13_cur_tuwf", "status": "chua_co"},
               {"id": "img_chung_sao", "status": "khong_dat", "ghi_chu": "sai màu"},
               {"id": "img_chung_em_doc", "status": "dat"}]  # không có file
        by = {r["id"]: r for r in update_image_manifest([self.res13], old, self.image_dir)}
        self.assertEqual((by["img_b13_cais_ddu"]["status"], by["img_b13_cais_ddu"]["source"],
                          by["img_b13_cais_ddu"]["ghi_chu"]), ("dat", "chatgpt_tam", "ok"))
        self.assertEqual(by["img_b13_cur_tuwf"]["status"], "cho_duyet")
        self.assertEqual((by["img_chung_sao"]["status"], by["img_chung_sao"]["ghi_chu"]), ("khong_dat", "sai màu"))
        self.assertEqual(by["img_chung_em_doc"]["status"], "chua_co")
        self.assertEqual(by["img_chung_luyen_tap"]["status"], "chua_co")

    def test_new_image_with_file_is_cho_duyet(self):
        touch(self.image_dir, "img_b13_cais_ddu", ext="png")
        by = {r["id"]: r for r in update_image_manifest([self.res13], [], self.image_dir)}
        self.assertEqual(by["img_b13_cais_ddu"]["status"], "cho_duyet")

    def test_only_png_files_count(self):
        touch(self.image_dir, "img_b13_cais_ddu", ext="jpg")
        by = {r["id"]: r for r in update_image_manifest([self.res13], [], self.image_dir)}
        self.assertEqual(by["img_b13_cais_ddu"]["status"], "chua_co")


class BuildCliManifestTest(TempDirCase):
    """`python -m tapdoc build` cập nhật hai danh mục (mọi đường dẫn đều trong thư mục tạm)."""

    def setUp(self):
        super().setUp()
        self.src = self.root / "src"
        self.src.mkdir()
        with open(self.src / "b13.json", "w", encoding="utf-8") as f:
            json.dump(SRC13, f, ensure_ascii=False)
        self.res = self.root / "res"
        self.manifests = self.root / "manifests"

    def run_cli(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(cli, "CONTENT_SRC", self.src), mock.patch.object(cli, "UNITY_RES", self.res), \
                mock.patch.object(cli, "MANIFESTS", self.manifests), redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_build_writes_both_manifests_and_prints_counts(self):
        code, out, err = self.run_cli(["build"])
        self.assertEqual(code, 0, err)
        audio = load_rows(self.manifests / "audio_manifest.json")
        images = load_rows(self.manifests / "image_manifest.json")
        self.assertTrue(any(r["id"] == "tieng_cuwr" for r in audio))
        self.assertTrue(any(r["id"] == "img_chung_sao" for r in images))
        self.assertTrue(all(r["status"] == "chua_co" for r in audio + images))
        self.assertIn(f"chua_co {len(audio)}", out)
        self.assertIn(f"chua_co {len(images)}", out)
        for status in ("cho_duyet", "dat", "khong_dat"):
            self.assertIn(f"{status} 0", out)

    def test_build_reads_old_status_and_the_audio_and_image_folders(self):
        touch(self.res / "audio", "am_dd", "tieng_cuwr")
        touch(self.res / "images", "img_b13_cais_ddu", ext="png")
        save_rows(self.manifests / "audio_manifest.json",
                  [{"id": "am_dd", "text": "đờ", "status": "dat", "source": "chatgpt_tam", "ghi_chu": "ok"}])
        code, out, err = self.run_cli(["build"])
        self.assertEqual(code, 0, err)
        by = {r["id"]: r for r in load_rows(self.manifests / "audio_manifest.json")}
        self.assertEqual((by["am_dd"]["status"], by["am_dd"]["source"]), ("dat", "chatgpt_tam"))
        self.assertEqual(by["tieng_cuwr"]["status"], "cho_duyet")
        imgs = {r["id"]: r for r in load_rows(self.manifests / "image_manifest.json")}
        self.assertEqual(imgs["img_b13_cais_ddu"]["status"], "cho_duyet")
        audio = load_rows(self.manifests / "audio_manifest.json")
        self.assertIn(f"chua_co {len(audio) - 2}, cho_duyet 1, dat 1, khong_dat 0", out)
        images = load_rows(self.manifests / "image_manifest.json")
        self.assertIn(f"chua_co {len(images) - 1}, cho_duyet 1, dat 0, khong_dat 0", out)

    def test_manifest_error_exits_1_with_message(self):
        with mock.patch.object(cli, "update_audio_manifest", side_effect=ManifestError("tieng_xoong: hai lời đọc")):
            code, out, err = self.run_cli(["build"])
        self.assertEqual(code, 1)
        self.assertIn("tieng_xoong: hai lời đọc", out + err)
        self.assertFalse((self.manifests / "audio_manifest.json").exists())
        self.assertFalse((self.manifests / "image_manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
