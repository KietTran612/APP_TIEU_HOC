"""Sửa công cụ cho tập 2 không được làm đổi file bài tập 1 đã dựng (thiết kế tập 2, mục 3)."""

import tempfile
import unittest
from pathlib import Path

from tapdoc.build import build_all
from tapdoc.paths import CONTENT_SRC, UNITY_RES


class Tap1RegressionTest(unittest.TestCase):
    def test_rebuild_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            build_all(CONTENT_SRC, tmp)
            built = sorted(Path(tmp).glob("tv1_t1_*.json"))
            self.assertEqual(len(built), 80)
            for path in built:
                shipped = UNITY_RES / "lessons" / path.name
                self.assertEqual(path.read_bytes(), shipped.read_bytes(), path.name)


if __name__ == "__main__":
    unittest.main()
