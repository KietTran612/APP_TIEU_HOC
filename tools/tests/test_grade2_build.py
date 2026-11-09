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


if __name__ == "__main__":
    unittest.main()
