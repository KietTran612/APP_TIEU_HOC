import unicodedata
import unittest

from tapdoc.viet import TONE_INFO, Syllable, split_syllable, strip_tone, syllables, tokens


class ToneInfoTest(unittest.TestCase):
    def test_tone_glyphs(self):
        self.assertEqual(TONE_INFO["huyen"], ("huyền", "ˋ"))
        self.assertEqual(TONE_INFO["sac"], ("sắc", "ˊ"))
        self.assertEqual(TONE_INFO["hoi"], ("hỏi", "ˀ"))
        self.assertEqual(TONE_INFO["nga"], ("ngã", "˜"))
        self.assertEqual(TONE_INFO["nang"], ("nặng", "."))


class SplitTest(unittest.TestCase):
    def test_split(self):
        S = Syllable
        self.assertEqual(split_syllable("cử"), S("c", "ư", "hoi"))
        self.assertEqual(split_syllable("đu"), S("đ", "u", None))
        self.assertEqual(split_syllable("sàn"), S("s", "an", "huyen"))
        self.assertEqual(split_syllable("ngan"), S("ng", "an", None))
        self.assertEqual(split_syllable("nghỉ"), S("ngh", "i", "hoi"))
        self.assertEqual(split_syllable("qua"), S("qu", "a", None))
        self.assertEqual(split_syllable("gì"), S("gi", "i", "huyen"))
        self.assertEqual(split_syllable("u"), S("", "u", None))
        self.assertEqual(split_syllable("ụ"), S("", "u", "nang"))

    def test_split_gi_without_other_vowel_shares_i(self):
        self.assertEqual(split_syllable("gìn"), Syllable("gi", "in", "huyen"))

    def test_split_normalizes_nfd(self):
        self.assertEqual(split_syllable(unicodedata.normalize("NFD", "cử")), Syllable("c", "ư", "hoi"))

    def test_split_rejects(self):
        for bad in ("c", "cu tá", "", "cáà"):
            with self.assertRaises(ValueError):
                split_syllable(bad)

    def test_split_rejects_non_letters(self):
        for bad in ("đu-đu", "an1", "“đu”"):
            with self.assertRaises(ValueError):
                split_syllable(bad)

    def test_strip_tone_and_tokens(self):
        self.assertEqual(strip_tone("cử"), "cư")
        self.assertEqual(tokens("cái đu"), [("cái", 0), ("đu", 4)])
        self.assertEqual(syllables("có cà, có cá"), ["có", "cà", "có", "cá"])

    def test_tokens_index_counts_nfc_characters(self):
        self.assertEqual(tokens(unicodedata.normalize("NFD", "cái đu")), [("cái", 0), ("đu", 4)])

    def test_other_book_punctuation_is_dropped(self):
        # Sách còn dùng gạch dài, ngoặc đơn cong và dấu ba chấm liền một ký tự.
        self.assertEqual(syllables("—Ai gọi đó? ‘Ếp ếp’ thật là vui…"),
                         ["Ai", "gọi", "đó", "Ếp", "ếp", "thật", "là", "vui"])

    def test_hyphen_separates_loan_word_syllables(self):
        self.assertEqual(syllables("ra-đi-ô"), ["ra", "đi", "ô"])
        self.assertEqual(tokens("ra-đi-ô"), [("ra", 0), ("đi", 3), ("ô", 6)])
