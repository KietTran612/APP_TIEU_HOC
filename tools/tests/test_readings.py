"""Các cách đọc của một chữ: đọc khi học (tr.122), âm chuẩn (Ghi âm, tr.120–121), tên chữ cái (tr.120)."""

import unittest

from tapdoc.build import build_lesson
from tapdoc.readings import unit_readings
from tests.test_build import src_of

BOOK = "tv1_t1_1990"


def simple(unit):
    return [(r["kinds"], r["text"], r["audio"]) for r in unit_readings(BOOK, unit)]


class UnitReadingsTest(unittest.TestCase):
    def test_letter_with_three_readings(self):
        self.assertEqual(simple("g"), [(["hoc"], "gờ đơn", "am_g"), (["chuan"], "gờ", "ghiam_g"),
                                       (["tenchu"], "giê", "tenchu_g")])

    def test_digraph_has_no_letter_name(self):
        self.assertEqual(simple("gh"), [(["hoc"], "gờ kép", "am_gh"), (["chuan"], "gờ", "ghiam_gh")])
        self.assertEqual(simple("gi"), [(["hoc"], "di", "am_gi"), (["chuan"], "giờ", "ghiam_gi")])

    def test_same_text_shares_one_file(self):
        # k: tên chữ cái trùng tên đọc khi học ("ca"); b: âm chuẩn trùng tên đọc khi học ("bờ").
        self.assertEqual(simple("k"), [(["hoc", "tenchu"], "ca", "am_k"), (["chuan"], "cờ", "ghiam_k")])
        self.assertEqual(simple("b"), [(["hoc", "chuan"], "bờ", "am_b"), (["tenchu"], "bê", "tenchu_b")])
        self.assertEqual(simple("i"), [(["hoc", "tenchu"], "i ngắn", "van_i"), (["chuan"], "i", "ghiam_i")])

    def test_single_reading_needs_no_buttons(self):
        for unit in ("a", "ch", "kh", "an", "qu"):
            self.assertEqual(simple(unit), [], unit)

    def test_hint_says_which_letters_the_learning_name_separates(self):
        hint = {r["audio"]: r.get("hint") for r in unit_readings(BOOK, "g")}
        self.assertEqual(hint["am_g"], "để phân biệt g và gh")
        self.assertIsNone(hint["ghiam_g"])
        self.assertEqual(unit_readings(BOOK, "c")[0]["hint"], "để phân biệt c, k, q")
        self.assertNotIn("hint", unit_readings(BOOK, "b")[0])

    def test_other_book_without_appendix_has_no_readings(self):
        self.assertEqual(unit_readings("sach_khac", "g"), [])

    def test_new_audio_files_are_the_24_planned(self):
        letters = "a ă â b c d đ e ê g h i k l m n o ô ơ p q r s t u ư v x y gh gi ng ngh".split()
        new = {r["audio"] for u in letters for r in unit_readings(BOOK, u)
               if r["audio"].startswith(("ghiam_", "tenchu_"))}
        self.assertEqual(sorted(a for a in new if a.startswith("ghiam_")),
                         ["ghiam_g", "ghiam_gh", "ghiam_gi", "ghiam_i", "ghiam_k", "ghiam_ng", "ghiam_ngh",
                          "ghiam_q", "ghiam_y"])
        self.assertEqual(sorted(a.removeprefix("tenchu_") for a in new if a.startswith("tenchu_")),
                         ["b", "c", "d", "dd", "g", "h", "l", "m", "n", "p", "r", "s", "t", "v", "x"])


class UnitStepReadingsTest(unittest.TestCase):
    def test_unit_step_carries_readings_and_registers_their_audio(self):
        r = build_lesson(src_of(part1=[{"type": "unit", "text": "g"}], new_units=["g"]))
        step = r.lesson["part1"][0]
        self.assertEqual([x["audio"] for x in step["readings"]], ["am_g", "ghiam_g", "tenchu_g"])
        self.assertEqual(r.audio["ghiam_g"], ("gờ", "am"))
        self.assertEqual(r.audio["tenchu_g"], ("giê", "am"))

    def test_unit_step_without_other_readings_has_no_readings_key(self):
        step = build_lesson(src_of(part1=[{"type": "unit", "text": "ch"}], new_units=["ch"])).lesson["part1"][0]
        self.assertNotIn("readings", step)


if __name__ == "__main__":
    unittest.main()


class Tap2Test(unittest.TestCase):
    def test_appendix_falls_back_to_tap1(self):
        from tapdoc.readings import appendix_row
        self.assertEqual(appendix_row("tv1_t2_1996", "iê"), appendix_row("tv1_t1_1990", "iê"))
        self.assertIsNotNone(appendix_row("tv1_t2_1996", "iê"))
