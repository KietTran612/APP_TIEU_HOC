"""Sửa công cụ (tập 2, lớp 2) không được làm đổi file bài lớp 1 đã dựng (thiết kế tập 2 mục 3, lớp 2 mục 11)."""

import tempfile
import unittest
from pathlib import Path

from tapdoc.build import build_all
from tapdoc.paths import CONTENT_SRC, UNITY_RES


class Tap1RegressionTest(unittest.TestCase):
    def test_rebuild_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            build_all(CONTENT_SRC, tmp)
            built = sorted(Path(tmp).glob("tv1_t*.json"))
            self.assertEqual(len(built), 171)
            for path in built:
                shipped = UNITY_RES / "lessons" / path.name
                self.assertEqual(path.read_bytes(), shipped.read_bytes(), path.name)


if __name__ == "__main__":
    unittest.main()
