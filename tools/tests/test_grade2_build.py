"""Công cụ cho sách lớp 2 (thiết kế TV2 tập một, mục 4 và 7): quyển, phần, nhãn, tuần, chủ điểm."""

import unittest

from tapdoc.books import grade_of, part_of, spells
from tapdoc.build import BuildError, build_lesson
from tests.test_build import src_of


def grade2_src(part1, part2=(), images=None, lesson_type="tu_ngu", **extra):
    src = src_of(part1=part1, part2=part2, images=images, lesson_id="tv2_t1_b177", lesson_no=177)
    src.update({"book": "tv2_t1_2001", "type": lesson_type, "title": "Ngày khai trường",
                "week": 1, "theme": "Nhà trường"})
    src.update(extra)
    return src


def index_of(src):
    return build_lesson(src).index


class BooksGradeTest(unittest.TestCase):
    def test_grade_of(self):
        self.assertEqual(grade_of("tv2_t1_2001"), 2)
        self.assertEqual(grade_of("tv1_t2_1996"), 1)
        self.assertEqual(grade_of("tv1_t1_1990"), 1)

    def test_spells(self):
        self.assertFalse(spells("tv2_t1_2001"))
        self.assertTrue(spells("tv1_t1_1990"))

    def test_part_lop2(self):
        self.assertEqual(part_of("tu_ngu", 2), "lop2")
        self.assertEqual(part_of("tap_doc", 2), "lop2")
        self.assertEqual(part_of("tap_doc", 1), "tap_doc")

    def test_part_unknown_grade2_raises(self):
        with self.assertRaises(ValueError):
            part_of("van_moi", 2)

    def test_grade1_rejects_grade2_types(self):
        with self.assertRaises(ValueError):
            part_of("tu_ngu", 1)


class Grade2IndexTest(unittest.TestCase):
    def test_index_entry_grade2(self):
        entry = index_of(grade2_src([{"type": "title", "text": "Ngày khai trường"}]))
        self.assertEqual(entry, {"part": "lop2", "label": "Từ ngữ", "week": 1, "grade": 2, "theme": "Nhà trường"})

    def test_labels_by_type(self):
        for lesson_type, label in (("tap_chep_chinh_ta", "Chính tả"), ("ngu_phap", "Ngữ pháp"),
                                   ("tap_lam_van", "Tập làm văn"), ("cau_do", "Câu đố")):
            entry = index_of(grade2_src([{"type": "title", "text": "x"}], lesson_type=lesson_type))
            self.assertEqual(entry["label"], label, lesson_type)

    def test_reading_label_uses_td_no(self):
        entry = index_of(grade2_src([{"type": "title", "text": "Đi học"}], lesson_type="hoc_thuoc_long", td_no=6))
        self.assertEqual(entry["label"], "Bài 6")

    def test_grade1_index_has_grade_no_theme(self):
        src = src_of(part1=[{"type": "title", "text": "o"}], part2=(), images=None)
        entry = index_of(src)
        self.assertEqual(entry["grade"], 1)
        self.assertNotIn("theme", entry)

    def test_grade2_requires_theme(self):
        src = grade2_src([{"type": "title", "text": "x"}])
        del src["theme"]
        with self.assertRaises(BuildError):
            build_lesson(src)

    def test_grade2_week_range(self):
        with self.assertRaises(BuildError):
            build_lesson(grade2_src([{"type": "title", "text": "x"}], week=18))


def _all_spells(node, found):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "spells":
                found.append(value)
            _all_spells(value, found)
    elif isinstance(node, list):
        for value in node:
            _all_spells(value, found)
    return found


class NoSpellTest(unittest.TestCase):
    LINES = ["Cái trống trường em", "Mùa hè cũng nghỉ."]

    def build(self):
        steps = [{"type": "title", "text": "Cái trống trường em"}]
        steps += [{"type": "sentence", "text": t} for t in self.LINES]
        steps += [{"type": "passage", "layout": "poem", "author": "THANH HÀO"},
                  {"type": "words", "items": [{"text": "giá trống"}]},
                  {"type": "find_words", "question": "Tìm tiếng có vần ông.", "match": {"rime": ["ông"]}, "in": [0]},
                  {"type": "memorize"}]
        return build_lesson(grade2_src(steps, lesson_type="hoc_thuoc_long", td_no=2))

    def test_no_spell_grade2(self):
        result = self.build()
        spells_lists = _all_spells(result.lesson["part1"], [])
        self.assertTrue(spells_lists)
        self.assertTrue(all(lst == [] for lst in spells_lists), spells_lists[:3])

    def test_no_phonics_audio_grade2(self):
        ids = set(self.build().audio)
        self.assertFalse({i for i in ids if i.startswith(("am_", "dau_"))})
        # "em" là cả tiếng (không có âm đầu) nên mã của chính tiếng đó là van_em; không có mảnh vần nào khác.
        self.assertEqual({i for i in ids if i.startswith("van_")}, {"van_em"})
        self.assertIn("tieng_troongs", ids)


if __name__ == "__main__":
    unittest.main()
