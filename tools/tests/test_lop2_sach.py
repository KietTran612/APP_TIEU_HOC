"""Script lớp 2 chọn tập bằng cờ --t2 (thiết kế TV2 tập hai mục 7): mặc định tập một, không đụng mã dùng chung."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lop2"))
from sach import RANGES, only_book_ids, prefix  # noqa: E402


class SachTest(unittest.TestCase):
    def test_prefix_default_t1(self):
        argv = ["4"]
        self.assertEqual(prefix(argv), "tv2_t1_")
        self.assertEqual(argv, ["4"])

    def test_prefix_t2_removes_flag(self):
        argv = ["4", "--t2", "305"]
        self.assertEqual(prefix(argv), "tv2_t2_")
        self.assertEqual(argv, ["4", "305"])

    def test_ranges(self):
        self.assertEqual(RANGES["tv2_t1_"], (172, 304))
        self.assertEqual(RANGES["tv2_t2_"], (305, 434))

    def test_only_book_ids_excludes_shared(self):
        rows = [{"id": "cau_b305_01", "bai": ["tv2_t2_b305"]},
                {"id": "tu_sa_pa", "bai": ["tv2_t1_b172", "tv2_t2_b305"]},
                {"id": "tieng_a", "bai": ["tv1_t1_b1", "tv2_t2_b306"]},
                {"id": "img_chung_x", "bai": []},
                {"id": "tieng_b", "bai": ["tv2_t2_b306", "tv2_t2_b320"]}]
        self.assertEqual([r["id"] for r in only_book_ids(rows, "tv2_t2_")], ["cau_b305_01", "tieng_b"])
        self.assertEqual(only_book_ids(rows, "tv2_t1_"), [])


if __name__ == "__main__":
    unittest.main()
