"""Danh sách quyển (content/books.json): Phụ lục dùng cho từng quyển và phần của từng loại bài."""

import unittest

from tapdoc.books import appendix_book, load_books, part_of


class BooksTest(unittest.TestCase):
    def test_books_in_program_order(self):
        self.assertEqual([b["book_id"] for b in load_books()], ["tv1_t1_1990", "tv1_t2_1996", "tv2_t1_2001"])

    def test_tap2_uses_tap1_appendix(self):
        self.assertEqual(appendix_book("tv1_t2_1996"), "tv1_t1_1990")
        self.assertEqual(appendix_book("tv1_t1_1990"), "tv1_t1_1990")

    def test_unknown_book_has_no_appendix(self):
        self.assertIsNone(appendix_book("tv3_t1_2000"))

    def test_part_of(self):
        self.assertEqual(part_of("am_moi"), "chu_cai")
        self.assertEqual(part_of("on_tap_cuoi_ki"), "van")
        self.assertEqual(part_of("on_luyen"), "van")
        self.assertEqual(part_of("cau_do"), "tap_doc")
        self.assertEqual(part_of("hoc_thuoc_long"), "tap_doc")

    def test_unknown_type_raises(self):
        with self.assertRaises(ValueError):
            part_of("tra_loi_cau_do")


if __name__ == "__main__":
    unittest.main()
