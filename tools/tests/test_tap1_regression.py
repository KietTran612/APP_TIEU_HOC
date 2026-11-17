"""Sửa công cụ (tập 2, lớp 2, TV2 tập hai) không được làm đổi file bài đã dựng của các cuốn đã chốt
(thiết kế tập 2 mục 3, lớp 2 mục 11, TV2 tập hai mục 11)."""

import tempfile
import unittest
from pathlib import Path

from tapdoc.build import build_all
from tapdoc.paths import CONTENT_SRC, UNITY_RES


class Tap1RegressionTest(unittest.TestCase):
    def test_rebuild_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            build_all(CONTENT_SRC, tmp)
            # Lớp 1 (171 mục) và TV2 tập một (133 mục) đã chốt: sửa công cụ cho tập hai không được đổi file nào.
            for pattern, count in (("tv1_t*.json", 171), ("tv2_t1_*.json", 133)):
                built = sorted(Path(tmp).glob(pattern))
                self.assertEqual(len(built), count, pattern)
                for path in built:
                    shipped = UNITY_RES / "lessons" / path.name
                    self.assertEqual(path.read_bytes(), shipped.read_bytes(), path.name)


if __name__ == "__main__":
    unittest.main()
