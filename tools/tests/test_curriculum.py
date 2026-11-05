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


class ProgramTest(unittest.TestCase):
    """Chữ đã học tính liền cả chương trình: bài 81 (tập 2) đã học mọi thứ của tập 1."""

    def test_tap2_lesson_knows_tap1(self):
        from tapdoc.curriculum import load_program
        learned = learned_until(load_program(LESSON_INDEX), 81)
        self.assertIn("an", learned.rimes)   # bài 42, tập 1
        self.assertIn("anh", learned.rimes)  # bài 81, tập 2
        self.assertNotIn("ach", learned.rimes)  # bài 83 chưa học

    def test_reading_rows_skipped(self):
        from tapdoc.curriculum import load_program
        program = load_program(LESSON_INDEX)
        self.assertEqual(max(program), 125)
        self.assertEqual(program[80], cur[80])


class RareRimesTest(unittest.TestCase):
    def test_rare_rimes_count_as_learned(self):
        from tapdoc.curriculum import load_program
        learned = learned_until(load_program(LESSON_INDEX), 122)
        self.assertIn("oay", learned.rimes)
        self.assertIn("uynh", learned.rimes)


class QuRimeLearnedTest(unittest.TestCase):
    def test_qu_word_learned_when_u_rime_learned(self):
        # "quýnh" có vần uynh (bài 122), "quýt" có vần uyt (bài 122): sách coi u của qu là âm đệm.
        from tapdoc.curriculum import load_program
        learned = learned_until(load_program(LESSON_INDEX), 141)
        self.assertTrue(is_learned_text("mừng quýnh", learned))
        self.assertTrue(is_learned_text("quả quýt", learned))
        early = learned_until(load_program(LESSON_INDEX), 100)
        self.assertFalse(is_learned_text("quýnh", early))
