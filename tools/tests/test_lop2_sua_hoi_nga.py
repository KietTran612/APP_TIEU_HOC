"""Ghép mượt câu lớp 2 (sua_hoi_nga_lop2.py ghep, 16/11): tiếng bắt đầu bằng nguyên âm ("em", "ông", "ăn") không có
file `tieng_*` mà có ở mã vần `van_*`, nên phần ghép `tieng_X` thiếu file được thay bằng `van_X` khi `van_X` có file."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lop2"))
from sua_hoi_nga_lop2 import van_thay  # noqa: E402


def has_of(*ids):
    present = set(ids)
    return lambda audio_id: audio_id in present


class VanThayTest(unittest.TestCase):
    def test_missing_tieng_uses_van_file(self):
        has = has_of("tieng_chaof", "van_em")
        self.assertEqual(van_thay(["tieng_chaof", "tieng_em"], has), ["tieng_chaof", "van_em"])

    def test_tieng_with_file_kept_even_if_van_exists(self):
        has = has_of("tieng_oong", "van_oong")
        self.assertEqual(van_thay(["tieng_oong"], has), ["tieng_oong"])

    def test_comma_pause_kept(self):
        has = has_of("tieng_bes", "van_anh")
        self.assertEqual(van_thay(["tieng_bes", ",", "tieng_anh"], has), ["tieng_bes", ",", "van_anh"])

    def test_both_missing_left_as_tieng_for_missing_report(self):
        has = has_of("tieng_bes")
        self.assertEqual(van_thay(["tieng_bes", "tieng_nguwx"], has), ["tieng_bes", "tieng_nguwx"])


if __name__ == "__main__":
    unittest.main()
