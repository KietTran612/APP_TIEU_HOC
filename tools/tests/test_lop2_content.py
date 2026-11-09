"""Nội dung lớp 2 – Tiếng Việt 2 tập một (thiết kế TV2 tập một, mục 3–4): đủ mục theo đợt, nhãn, tuần, chủ điểm."""

import json
import unittest

from tapdoc.paths import CONTENT_SRC, UNITY_RES

DONE = 24  # số mục lớp 2 đã chép (tăng theo đợt: 24, 63, 102, 133)
LABELS = {"tap_chep_chinh_ta": "Chính tả", "tu_ngu": "Từ ngữ", "ngu_phap": "Ngữ pháp", "tap_lam_van": "Tập làm văn",
          "cau_do": "Câu đố"}


def theme_of(week):
    return "Nhà trường" if week <= 5 else "Gia đình" if week <= 9 else "Đất nước ta"


def sources():
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(CONTENT_SRC.glob("tv2_t1_b*.json"))]


def index_rows():
    index = json.loads((UNITY_RES / "lessons" / "index.json").read_text(encoding="utf-8"))
    return [r for r in index["lessons"] if r["book"] == "tv2_t1_2001"]


class Lop2ContentTest(unittest.TestCase):
    def test_count_so_far(self):
        self.assertEqual(len(sources()), DONE)
        self.assertEqual([s["lesson_no"] for s in sources()], list(range(172, 172 + DONE)))

    def test_labels_weeks_themes(self):
        for row in index_rows():
            with self.subTest(row["lesson_id"]):
                self.assertEqual(row["grade"], 2)
                self.assertEqual(row["part"], "lop2")
                self.assertTrue(1 <= row["week"] <= 17)
                self.assertEqual(row["theme"], theme_of(row["week"]))
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
            self.assertEqual(s["source"]["verification"], "page_verified", s["lesson_id"])

    def test_no_spell(self):
        def spells(node):
            if isinstance(node, dict):
                for k, v in node.items():
                    if k == "spells":
                        yield v
                    yield from spells(v)
            elif isinstance(node, list):
                for v in node:
                    yield from spells(v)

        for row in index_rows():
            lesson = json.loads((UNITY_RES / "lessons" / f"{row['lesson_id']}.json").read_text(encoding="utf-8"))
            self.assertTrue(all(s == [] for s in spells(lesson["part1"])), row["lesson_id"])


if __name__ == "__main__":
    unittest.main()
