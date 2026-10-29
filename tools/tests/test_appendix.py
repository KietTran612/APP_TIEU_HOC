"""Phụ lục TV1 Tập 1 trong app: chép đúng Bảng chữ cái (tr.120), Bảng gọi tên (tr.121) và mục Chú ý (tr.122)."""

import json
import unittest

from tapdoc.ids import CONSONANT_NAMES, VOWEL_NAMES
from tapdoc.paths import UNITY_RES

APPENDIX = UNITY_RES / "appendix" / "tv1_t1.json"
ALPHABET = "a ă â b c d đ e ê g h i k l m n o ô ơ p q r s t u ư v x y".split()


def load():
    return json.loads(APPENDIX.read_text(encoding="utf-8"))


class AppendixTest(unittest.TestCase):
    def test_alphabet_table_like_page_120(self):
        rows = load()["alphabet"]["rows"]
        self.assertEqual([r["no"] for r in rows], list(range(1, 30)))
        self.assertEqual([r["lower"] for r in rows], ALPHABET)
        self.assertEqual([r["upper"] for r in rows], [c.upper() for c in ALPHABET])
        by = {r["lower"]: (r["name"], r["sound"]) for r in rows}
        self.assertEqual(by["b"], ("bê", "bờ"))
        self.assertEqual(by["c"], ("xê", "cờ"))
        self.assertEqual(by["g"], ("giê", "gờ"))
        self.assertEqual(by["h"], ("hát", "hờ"))
        self.assertEqual(by["i"], ("i ngắn", "i"))
        self.assertEqual(by["k"], ("ca", "cờ"))
        self.assertEqual(by["q"], ("cu", "cờ"))
        self.assertEqual(by["r"], ("e-rờ", "rờ"))
        self.assertEqual(by["s"], ("ét-sì", "sờ"))
        self.assertEqual(by["x"], ("ích-xì", "xờ"))
        self.assertEqual(by["y"], ("i dài", "i"))

    def test_digraph_table_like_page_121(self):
        rows = load()["digraphs"]["rows"]
        self.assertEqual([(r["letters"], r["reading"]) for r in rows], [
            ("iê", "i-ê"), ("yê", "i-ê"), ("uô", "u-ô"), ("ươ", "ư-ơ"), ("ch", "chờ"), ("kh", "khờ"),
            ("nh", "nhờ"), ("th", "thờ"), ("ph", "phờ"), ("gh", "gờ"), ("ng", "ngờ"), ("ngh", "ngờ"),
            ("tr", "trờ"), ("gi", "giờ")])

    def test_chu_y_page_122_lists_the_names_the_app_uses_when_spelling(self):
        chu_y = " ".join(load()["chu_y"]["paragraphs"])
        self.assertIn("giáo viên và phụ huynh học sinh", chu_y)
        for letter in ("k", "q", "gi", "i", "y", "g", "gh", "ng", "ngh"):
            name = CONSONANT_NAMES.get(letter) or VOWEL_NAMES[letter]
            with self.subTest(letter=letter):
                self.assertIn(f"{letter} ({name})", chu_y)
        self.assertIn("quờ", chu_y)
        self.assertIn("sờ-an-san huyền sàn", chu_y)

    def test_general_app_notes_present(self):
        notes = load()["app_notes"]
        self.assertTrue(notes and all(isinstance(n, str) and n.strip() for n in notes))
        self.assertTrue(any("Phần luyện tập" in n for n in notes))


if __name__ == "__main__":
    unittest.main()
