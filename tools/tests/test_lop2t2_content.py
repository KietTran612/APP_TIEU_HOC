"""Nội dung Tiếng Việt 2 tập hai (thiết kế TV2 tập hai, mục 3–6): đủ mục theo đợt, nhãn, tuần 18–33, chủ điểm,
trang scan, tranh Tập làm văn dùng lại tranh bài đọc."""

import json
import sys
import unittest
from pathlib import Path

from tapdoc.paths import CONTENT_SRC, UNITY_RES

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lop2" / "soan_t2"))
from toc_t2 import image_of  # noqa: E402

FIRST = 305
DONE = 130  # số mục tập hai đã chép (tăng theo đợt: 34, 66, 98, 130)
LABELS = {"tap_chep_chinh_ta": "Chính tả", "tu_ngu": "Từ ngữ", "ngu_phap": "Ngữ pháp", "tap_lam_van": "Tập làm văn"}


def theme_of(week):
    return "Thiếu nhi" if week <= 22 else "Nhân dân ta" if week <= 30 else "Bác Hồ"


def sources():
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(CONTENT_SRC.glob("tv2_t2_b*.json"))]


def index_rows():
    index = json.loads((UNITY_RES / "lessons" / "index.json").read_text(encoding="utf-8"))
    return [r for r in index["lessons"] if r["book"] == "tv2_t2_2002"]


def _steps(node, kind):
    if isinstance(node, dict):
        if node.get("type") == kind:
            yield node
        for v in node.values():
            yield from _steps(v, kind)
    elif isinstance(node, list):
        for v in node:
            yield from _steps(v, kind)


class Tap2ContentTest(unittest.TestCase):
    def test_count_so_far(self):
        self.assertEqual([s["lesson_no"] for s in sources()], list(range(FIRST, FIRST + DONE)))
        self.assertEqual(sorted(r["lesson_no"] for r in index_rows()), list(range(FIRST, FIRST + DONE)))

    def test_weeks_and_themes(self):
        for row in index_rows():
            with self.subTest(row["lesson_id"]):
                self.assertEqual((row["grade"], row["part"]), (2, "lop2"))
                self.assertTrue(18 <= row["week"] <= 33)
                self.assertEqual(row["theme"], theme_of(row["week"]))

    def test_labels(self):
        for row in index_rows():
            with self.subTest(row["lesson_id"]):
                expected = LABELS.get(row["type"])
                if expected:
                    self.assertEqual(row["label"], expected)
                else:
                    self.assertRegex(row["label"], r"^Bài \d+$")

    def test_td_no_sequence(self):
        numbers = [s["td_no"] for s in sources() if "td_no" in s]
        self.assertEqual(numbers, list(range(1, len(numbers) + 1)))

    def test_page_verified(self):
        for s in sources():
            with self.subTest(s["lesson_id"]):
                self.assertEqual(s["source"]["verification"], "page_verified")
                self.assertEqual(s["source"]["scan_file"], image_of(s["source"]["pages"][0]))

    def test_no_spell(self):
        for row in index_rows():
            lesson = json.loads((UNITY_RES / "lessons" / f"{row['lesson_id']}.json").read_text(encoding="utf-8"))
            spells = [v for st in lesson["part1"] for k, v in _walk(st) if k == "spells"]
            self.assertTrue(all(v == [] for v in spells), row["lesson_id"])

    def test_tlv_reuses_reading_picture(self):
        """Tập làm văn "Trả lời câu hỏi" dùng lại tranh bài đọc: cùng mã, cùng mô tả, không vẽ tranh mới."""
        reading_images = {}
        for s in sources():
            if "td_no" in s:
                reading_images.update(s["images"])
        for s in sources():
            if s["type"] != "tap_lam_van":
                continue
            with self.subTest(s["lesson_id"]):
                for step in _steps(s["part1"], "picture"):
                    self.assertIn(step["image"], reading_images)
                for image, desc in s["images"].items():
                    self.assertEqual(desc, reading_images.get(image))


def _walk(node):
    if isinstance(node, dict):
        for k, v in node.items():
            yield k, v
            yield from _walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from _walk(v)


if __name__ == "__main__":
    unittest.main()
