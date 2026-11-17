"""Bản thử ngoài danh mục cho mã lớp 2 (tools/lop2/ban_thu_lop2.py): tạo không đụng file trong Unity, cài thì giữ
bản cũ ở prev, file cài trùng từng byte, settings khớp cách đọc của bản thử."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lop2"))
import ban_thu_lop2 as bt  # noqa: E402
from tapdoc.tts_settings import effective_params, set_override, signature  # noqa: E402
from tests.test_tts_settings import row, settings  # noqa: E402
from tests.tts_fakes import FakeEngine, fake_mp3  # noqa: E402


class SpecTest(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(bt.parse_spec("cau_b334_17:cham"), ("cau_b334_17", "cham", None))
        self.assertEqual(bt.parse_spec("cau_b1_01:ngat=Chính, tả: Hòn đá to"),
                         ("cau_b1_01", "ngat", "Chính, tả: Hòn đá to"))

    def test_tag_names_take(self):
        # hai kiểu cùng cách của một mã cần tên bản thử khác nhau
        self.assertEqual(bt.parse_spec("hoi_b315_04:ngat#a=Tìm từ can đảm."),
                         ("hoi_b315_04", "ngat", "Tìm từ can đảm."))
        self.assertEqual(bt.take_name("hoi_b315_04:ngat#a=Tìm từ can đảm."), "hoi_b315_04__ngat_a")
        self.assertEqual(bt.take_name("hoi_b315_04:cham"), "hoi_b315_04__cham")

    def test_bad_specs(self):
        for spec in ("cau_b1_01:nhanh", "cau_b1_01", "cau_b1_01:ngat", "cau_b1_01:cham_ngat= "):
            with self.subTest(spec=spec), self.assertRaises(ValueError):
                bt.parse_spec(spec)


class TempCase(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.audio = self.root / "audio"
        self.audio.mkdir()
        self.out = self.root / "thu"
        self.s = settings()
        self.r = row("cau_b999_01", "hoa quả", "cau")
        (self.audio / "cau_b999_01.mp3").write_bytes("bản cũ".encode())


class OverrideTest(TempCase):
    def test_cham_keeps_existing_doc(self):
        set_override(self.s, self.r, doc="hoa, quả")
        o = bt.override_for(self.r, self.s, "cham", None, self.audio)
        self.assertEqual(o, {"doc": "hoa, quả", "rate": self.s["defaults"]["cau"]["rate"] - 20})

    def test_cham_custom_amount(self):
        # "cham=25": chậm hơn mặc định 25 (root hỏi bản −25%)
        audio_id, cach, doc = bt.parse_spec("cau_b999_01:cham#25=25")
        o = bt.override_for(self.r, self.s, cach, doc, self.audio)
        self.assertEqual(o["rate"], self.s["defaults"]["cau"]["rate"] - 25)
        self.assertNotIn("doc", o)
        with self.assertRaises(ValueError):
            bt.override_for(self.r, self.s, "cham", "nhanh", self.audio)

    def test_cham_ngat(self):
        o = bt.override_for(self.r, self.s, "cham_ngat", "hoa. quả.", self.audio)
        self.assertEqual(o["doc"], "hoa. quả.")
        self.assertEqual(o["rate"], self.s["defaults"]["cau"]["rate"] - 20)

    def test_ghep_needs_tieng_files(self):
        with self.assertRaises(ValueError):
            bt.override_for(self.r, self.s, "ghep", None, self.audio)
        for t in ("tieng_hoa", "tieng_quar"):
            (self.audio / f"{t}.mp3").write_bytes(fake_mp3(0.3))
        set_override(self.s, self.r, doc="hoa, quả")
        o = bt.override_for(self.r, self.s, "ghep", None, self.audio)
        self.assertEqual(o, {"join": ["tieng_hoa", "tieng_quar"], "join_gap": 0.08})

    def test_ghep_explicit_parts(self):
        # ghép theo danh sách cho sẵn ("|" ngăn phần): dùng mã từ có sẵn, phần "doc:" do bộ đọc đọc
        (self.audio / "tieng_hoa.mp3").write_bytes(fake_mp3(0.3))
        spec = "cau_b999_01:ghep#tu=tieng_hoa|,|doc:quả chín"
        audio_id, cach, doc = bt.parse_spec(spec)
        o = bt.override_for(self.r, self.s, cach, doc, self.audio)
        self.assertEqual(o, {"join": ["tieng_hoa", ",", "doc:quả chín"], "join_gap": 0.08})
        with self.assertRaises(ValueError):  # phần không có file
            bt.override_for(self.r, self.s, "ghep", "tieng_hoa|tu_khong_co", self.audio)

    def test_le_only_single_word(self):
        with self.assertRaises(ValueError):
            bt.override_for(self.r, self.s, "le", None, self.audio)
        one = row("cau_b999_02", "gà", "cau")
        self.assertEqual(bt.override_for(one, self.s, "le", None, self.audio),
                         {"doc": "gà, gà.", "keep_first": True})


class TakeAndInstallTest(TempCase):
    def make(self, cach="cham", doc=None):
        o = bt.override_for(self.r, self.s, cach, doc, self.audio)
        updated = bt.make_take(self.r, self.s, o, FakeEngine(), self.out, f"cau_b999_01__{cach}", self.audio,
                               pause=0)
        return bt.entry_for(self.r, updated, cach, o, f"cau_b999_01__{cach}", True)

    def test_take_leaves_unity_audio_and_settings_alone(self):
        before = json.dumps(self.s, sort_keys=True)
        e = self.make()
        self.assertEqual((self.audio / "cau_b999_01.mp3").read_bytes(), "bản cũ".encode())
        self.assertEqual(json.dumps(self.s, sort_keys=True), before)
        self.assertTrue((self.out / "mp3" / "cau_b999_01__cham.mp3").is_file())
        self.assertEqual(e["rate"], self.s["defaults"]["cau"]["rate"] - 20)
        self.assertEqual(e["wav"], "wav/cau_b999_01__cham.wav")

    def test_ghep_take_copies_parts_not_into_unity(self):
        self.r["text"] = "hoa, quả"  # dấu phẩy thành "," trong danh sách ghép (nghỉ dài), không phải file
        for t in ("tieng_hoa", "tieng_quar"):
            (self.audio / f"{t}.mp3").write_bytes(fake_mp3(0.3))
        with mock.patch("tapdoc.tts_generate.audio_join.join_files", return_value=fake_mp3(0.8)) as join:
            e = self.make("ghep")
        self.assertEqual([Path(p).name for p in join.call_args[0][0]], ["tieng_hoa.mp3", "tieng_quar.mp3"])
        self.assertEqual(e["doc"], "ghép: tieng_hoa , tieng_quar")
        self.assertIsNone(e["rate"])
        self.assertEqual((self.audio / "cau_b999_01.mp3").read_bytes(), "bản cũ".encode())

    def test_install_backs_up_matches_bytes_and_settings(self):
        e = self.make()
        rows = {self.r["id"]: dict(self.r, ghi_chu="Ghi chú cũ.")}
        prev, marks = self.root / "prev", self.root / "marks"
        new = bt.install(e, self.out, rows, self.s, self.audio, prev, marks, "Root soát 17/11: đọc chậm.")
        self.assertEqual((self.audio / "cau_b999_01.mp3").read_bytes(),
                         (self.out / "mp3" / "cau_b999_01__cham.mp3").read_bytes())
        self.assertEqual((prev / "cau_b999_01.mp3").read_bytes(), "bản cũ".encode())
        self.assertEqual(new["status"], "cho_duyet")
        self.assertEqual(new["ghi_chu"], "Ghi chú cũ. Root soát 17/11: đọc chậm.")
        self.assertEqual(signature(effective_params(self.s, new)), new["tts"]["sig"])
        self.assertEqual(self.s["overrides"]["cau_b999_01"], {"rate": self.s["defaults"]["cau"]["rate"] - 20})

    def test_install_refuses_approved(self):
        e = self.make()
        rows = {self.r["id"]: dict(self.r, status="dat")}
        with self.assertRaises(ValueError):
            bt.install(e, self.out, rows, self.s, self.audio, self.root / "prev", self.root / "marks", "x")
        self.assertEqual((self.audio / "cau_b999_01.mp3").read_bytes(), "bản cũ".encode())


if __name__ == "__main__":
    unittest.main()
