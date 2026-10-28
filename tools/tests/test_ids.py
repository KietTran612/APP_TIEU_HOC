import unicodedata
import unittest
from unittest import mock

from tapdoc import ids
from tapdoc.ids import audio_for, final_audio, telex, text_audio, tone_audio, unit_audio


def nfd(s):
    return unicodedata.normalize("NFD", s)


class IdsTest(unittest.TestCase):
    def test_telex(self):
        self.assertEqual(telex("cử"), "cuwr")
        self.assertEqual(telex("cái đu"), "cais_ddu")
        self.assertEqual(telex("đàn ngan"), "ddanf_ngan")
        self.assertEqual(telex("bàn ghế"), "banf_ghees")
        self.assertEqual(telex("má có củ từ."), "mas_cos_cur_tuwf")

    def test_telex_gi_does_not_double_i(self):
        self.assertEqual(telex("gì"), "gif")
        self.assertEqual(telex("giữ gìn"), "giuwx_ginf")

    def test_units(self):
        self.assertEqual(unit_audio("đ"), ("am_dd", "đờ", "am"))
        self.assertEqual(unit_audio("k"), ("am_k", "ca", "am"))
        self.assertEqual(unit_audio("gh"), ("am_gh", "gờ kép", "am"))
        self.assertEqual(unit_audio("g"), ("am_g", "gờ đơn", "am"))
        self.assertEqual(unit_audio("ng"), ("am_ng", "ngờ đơn", "am"))
        self.assertEqual(unit_audio("gi"), ("am_gi", "di", "am"))
        self.assertEqual(unit_audio("qu"), ("am_qu", "quờ", "am"))
        self.assertEqual(unit_audio("ư"), ("van_uw", "ư", "van"))
        self.assertEqual(unit_audio("an"), ("van_an", "an", "van"))
        self.assertEqual(final_audio("ng"), ("am_ng_cuoi", "ngờ", "am"))
        self.assertEqual(final_audio("n"), ("am_n", "nờ", "am"))
        self.assertEqual(tone_audio("hoi"), ("dau_hoi", "hỏi", "dau"))

    def test_text_audio(self):
        self.assertEqual(text_audio("cử"), ("tieng_cuwr", "cử", "tieng"))
        self.assertEqual(text_audio("u"), ("van_u", "u", "van"))
        self.assertEqual(text_audio("an"), ("van_an", "an", "van"))
        self.assertEqual(text_audio("cái đu"), ("tu_cais_ddu", "cái đu", "tu"))
        self.assertEqual(audio_for("c"), ("am_c", "cờ", "am"))

    def test_text_audio_i_and_y_are_tieng(self):
        self.assertEqual(text_audio("i"), ("tieng_i", "i", "tieng"))
        self.assertEqual(text_audio("y"), ("tieng_y", "y", "tieng"))

    def test_unit_audio_normalizes_nfd(self):
        self.assertEqual(unit_audio(nfd("ư")), ("van_uw", "ư", "van"))
        self.assertEqual(unit_audio(nfd("ưa")), ("van_uwa", "ưa", "van"))
        self.assertEqual(final_audio(nfd("ư")), ("van_uw", "ư", "van"))

    def test_text_audio_normalizes_nfd(self):
        self.assertEqual(text_audio(nfd("cử")), ("tieng_cuwr", "cử", "tieng"))

    def test_non_letters_are_rejected(self):
        with self.assertRaises(ValueError):
            telex("“đu” a-b")
        with self.assertRaises(ValueError):
            text_audio("đu-đu")
        with self.assertRaises(ValueError):
            unit_audio("an1")

    def test_telex_rejects_text_without_syllables(self):
        for empty in ("", "   ", "...", ", ."):
            with self.assertRaises(ValueError):
                telex(empty)

    def test_ids_must_be_ascii(self):
        # Nếu bảng Telex bị sửa sai và sinh ra chữ ngoài ASCII thì phải báo lỗi, không được ghi mã lạ ra file.
        with mock.patch.dict(ids._LETTER_TELEX, {"ư": "ư"}):
            with self.assertRaises(ValueError):
                unit_audio("ư")
            with self.assertRaises(ValueError):
                unit_audio("ưa")
            with self.assertRaises(ValueError):
                telex("cử")
            with self.assertRaises(ValueError):
                text_audio("cử")
            with self.assertRaises(ValueError):
                text_audio("cử cử")

    def test_audio_for(self):
        self.assertEqual(audio_for("c"), ("am_c", "cờ", "am"))
        self.assertEqual(audio_for("ă"), ("van_aw", "á", "van"))
        self.assertEqual(audio_for("i"), ("van_i", "i ngắn", "van"))
        self.assertEqual(audio_for("u"), ("van_u", "u", "van"))
        self.assertEqual(audio_for("cử"), ("tieng_cuwr", "cử", "tieng"))
        self.assertEqual(audio_for("an"), ("van_an", "an", "van"))
        self.assertEqual(audio_for(nfd("ă")), ("van_aw", "á", "van"))
