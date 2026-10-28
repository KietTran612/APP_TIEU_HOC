import unittest

from tapdoc.curriculum import Learned, is_learned_text, learned_until, load_curriculum
from tapdoc.paths import LESSON_INDEX

cur = load_curriculum(LESSON_INDEX)


class LoadTest(unittest.TestCase):
    def test_load_real_index(self):
        self.assertEqual(cur[4], ("dau_thanh", "dấu huyền; dấu sắc"))
        self.assertEqual(cur[43], ("van_moi", "chữ ă; vần ăn"))
        self.assertEqual(cur[11], ("on_tap_am", ""))
        self.assertTrue(all(isinstance(no, int) for no in cur))

    def test_other_book_is_not_mixed_in(self):
        other = load_curriculum(LESSON_INDEX, "tv1_t2_1996")
        self.assertNotEqual(other, cur)


class LearnedUntilTest(unittest.TestCase):
    def test_lesson_4(self):
        l = learned_until(cur, 4)
        self.assertEqual(l.letters, {"o", "c", "a"}); self.assertEqual(l.tones, {"huyen", "sac"}); self.assertEqual(l.rimes, set())

    def test_lesson_13(self):
        l = learned_until(cur, 13)
        self.assertTrue({"u", "ư", "d", "đ", "n", "m", "t", "i", "e", "ê", "ô", "ơ"} <= l.letters)
        self.assertNotIn("l", l.letters); self.assertEqual(l.tones, {"huyen", "sac", "hoi", "nga", "nang"})

    def test_lesson_42(self):
        l = learned_until(cur, 42)
        self.assertEqual(l.rimes, {"an"}); self.assertTrue({"ng", "gh", "qu", "ph", "b", "l", "kh"} <= l.letters)

    def test_review_and_capital_lessons_add_nothing(self):
        # Bài 7 (on_tap_am) và bài 41 (chu_hoa) có chữ trong noi_dung_chinh nhưng không dạy gì mới.
        self.assertEqual(learned_until(cur, 7), learned_until(cur, 6))
        self.assertEqual(learned_until(cur, 41), learned_until(cur, 40))

    def test_lesson_43_adds_letter_and_rime(self):
        l = learned_until(cur, 43)
        self.assertIn("ă", l.letters); self.assertEqual(l.rimes, {"an", "ăn"})

    def test_result_is_frozen(self):
        l = learned_until(cur, 4)
        self.assertIsInstance(l, Learned)
        for field in (l.letters, l.rimes, l.tones):
            self.assertIsInstance(field, frozenset)

    def test_before_first_lesson(self):
        self.assertEqual(learned_until(cur, 0), Learned(frozenset(), frozenset(), frozenset()))


class IsLearnedTest(unittest.TestCase):
    def test_is_learned(self):
        self.assertTrue(is_learned_text("củ từ", learned_until(cur, 13))); self.assertFalse(is_learned_text("lá", learned_until(cur, 13)))
        self.assertFalse(is_learned_text("củ", learned_until(cur, 4))); self.assertTrue(is_learned_text("đ", learned_until(cur, 13)))
        self.assertTrue(is_learned_text("bàn", learned_until(cur, 42))); self.assertFalse(is_learned_text("ăn", learned_until(cur, 42)))
        self.assertTrue(is_learned_text("ừ", learned_until(cur, 13)))

    def test_rime_alone_and_non_syllable(self):
        self.assertTrue(is_learned_text("an", learned_until(cur, 42)))
        self.assertFalse(is_learned_text("an", learned_until(cur, 13)))
        self.assertFalse(is_learned_text("đ", learned_until(cur, 4)))
        self.assertFalse(is_learned_text("", learned_until(cur, 42)))


if __name__ == "__main__":
    unittest.main()
