"""Ghi chú cho phụ huynh trong bài: chú thích sách, tên đọc riêng (tr.122), chỗ app khác sách."""

import unittest

from tapdoc.build import BuildError, build_lesson
from tests.test_build import src_of


def notes_of(src):
    return build_lesson(src).lesson["notes"]


def with_notes(src, notes, lesson_type=None):
    src["notes"] = notes
    if lesson_type:
        src["type"] = lesson_type
    return src


class LessonNotesTest(unittest.TestCase):
    def test_lesson_without_notes_has_empty_list(self):
        self.assertEqual(notes_of(src_of(part1=[{"type": "unit", "text": "ch"}], new_units=["ch"])), [])

    def test_book_and_app_notes_kept_in_order(self):
        src = with_notes(src_of(part1=[{"type": "unit", "text": "b"}], new_units=["b"]),
                         [{"kind": "khac_sach", "text": "Bảng chia 2 bước cho vừa màn hình."},
                          {"kind": "sach", "text": "* Vần ec rất ít gặp, không dạy để trẻ bớt khó khăn."}])
        self.assertEqual([n for n in notes_of(src) if n["kind"] != "ten_doc"], [
            {"kind": "sach", "text": "* Vần ec rất ít gặp, không dạy để trẻ bớt khó khăn."},
            {"kind": "khac_sach", "text": "Bảng chia 2 bước cho vừa màn hình."}])
        self.assertEqual([n["kind"] for n in notes_of(src)], ["sach", "ten_doc", "khac_sach"])

    def test_word_notes_become_book_notes_once(self):
        words = {"type": "words", "marker": "●", "items": [{"text": "cá lóc", "note": "cá lóc: cá quả."}, {"text": "con cóc"}]}
        src = with_notes(src_of(part1=[words], new_units=["oc"]),
                         [{"kind": "sach", "text": "cá lóc: cá quả."}], lesson_type="van_moi")
        self.assertEqual(notes_of(src), [{"kind": "sach", "text": "cá lóc: cá quả."}])

    def test_reading_name_note_for_new_letter_with_special_name(self):
        # Bài 20 dạy k, kh: chỉ k có tên đọc riêng ("ca"), âm thật theo Phụ lục là "cờ".
        notes = notes_of(src_of(part1=[{"type": "unit", "text": "k"}, {"type": "unit", "text": "kh"}],
                                new_units=["k", "kh"]))
        self.assertEqual([n["kind"] for n in notes], ["ten_doc"])
        self.assertEqual(notes[0]["text"],
                         'Chữ "k" khi học đọc là "ca" để bé phân biệt c, k, q (sách dặn ở mục Chú ý, tr.122). '
                         'Âm chuẩn của chữ là "cờ" (Phụ lục, tr.120). "ca" cũng là tên chữ cái (Bảng chữ cái, tr.120).')

    def test_reading_name_note_follows_the_app_reading(self):
        notes = notes_of(src_of(part1=[{"type": "unit", "text": "gh"}], new_units=["g", "gh"]))
        texts = " ".join(n["text"] for n in notes)
        self.assertIn('"g" khi học đọc là "gờ đơn"', texts)
        self.assertIn('Tên chữ cái là "giê" (Bảng chữ cái, tr.120)', texts)
        self.assertIn('"gh" khi học đọc là "gờ kép"', texts)
        self.assertIn('Âm chuẩn của chữ là "gờ" (Phụ lục, tr.121)', texts)

    def test_letter_name_note_when_only_the_letter_name_differs(self):
        notes = notes_of(src_of(part1=[{"type": "unit", "text": "b"}], new_units=["b"]))
        self.assertEqual(notes, [{"kind": "ten_doc", "text":
                                  'Chữ "b": bài đọc theo âm chuẩn "bờ" (Phụ lục, tr.120). Tên chữ cái là "bê" '
                                  '(Bảng chữ cái, tr.120), dùng khi gọi tên chữ trong bảng chữ cái.'}])

    def test_learning_name_that_is_also_the_standard_sound(self):
        notes = notes_of(src_of(part1=[{"type": "unit", "text": "c"}], new_units=["c"]))
        self.assertEqual(notes[0]["text"],
                         'Chữ "c" khi học đọc là "cờ" để bé phân biệt c, k, q (sách dặn ở mục Chú ý, tr.122). '
                         'Đây cũng là âm chuẩn của chữ (Phụ lục, tr.120). Tên chữ cái là "xê" (Bảng chữ cái, tr.120).')

    def test_no_reading_note_for_digraph_with_one_reading(self):
        self.assertEqual(notes_of(src_of(part1=[{"type": "unit", "text": "ch"}], new_units=["ch"])), [])

    def test_review_lessons_get_no_reading_notes(self):
        src = src_of(part1=[{"type": "unit", "text": "c"}], new_units=["c", "k"])
        src["type"] = "on_tap_am"
        self.assertEqual(notes_of(src), [])

    def test_bad_note_kind_is_error(self):
        src = with_notes(src_of(part1=[{"type": "unit", "text": "ch"}], new_units=["ch"]),
                         [{"kind": "ten_doc", "text": "tự viết"}])
        with self.assertRaises(BuildError):
            build_lesson(src)

    def test_empty_note_text_is_error(self):
        src = with_notes(src_of(part1=[{"type": "unit", "text": "b"}], new_units=["b"]),
                         [{"kind": "sach", "text": "  "}])
        with self.assertRaises(BuildError):
            build_lesson(src)


if __name__ == "__main__":
    unittest.main()
