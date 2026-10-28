import unicodedata
import unittest

from tapdoc.spelling import Part, SpellResult, spell_rime, spell_syllable


def triples(r):
    return [(p.kind, p.text, p.audio) for p in r.parts]


class SpellSyllableTest(unittest.TestCase):
    def test_du(self):
        r = spell_syllable("đu")
        self.assertEqual(triples(r), [("unit", "đ", "am_dd"), ("unit", "u", "van_u"), ("join", "đu", "tieng_ddu")])
        self.assertEqual(r.can_duyet, [])

    def test_cu_hoi(self):
        r = spell_syllable("cử")
        self.assertEqual(triples(r), [("unit", "c", "am_c"), ("unit", "ư", "van_uw"), ("join", "cư", "tieng_cuw"),
                                      ("tone", "ˀ", "dau_hoi"), ("join", "cử", "tieng_cuwr")])
        self.assertEqual(r.parts[3].tone, "hoi")
        self.assertEqual(r.parts[0].say, "cờ")
        self.assertEqual(r.parts[3].say, "hỏi")

    def test_san_keeps_rime_block(self):
        self.assertEqual(triples(spell_syllable("sàn")),
                         [("unit", "s", "am_s"), ("unit", "an", "van_an"), ("join", "san", "tieng_san"),
                          ("tone", "ˋ", "dau_huyen"), ("join", "sàn", "tieng_sanf")])

    def test_no_onset(self):
        self.assertEqual(triples(spell_syllable("ụ")),
                         [("unit", "u", "van_u"), ("tone", ".", "dau_nang"), ("join", "ụ", "tieng_uj")])

    def test_no_onset_no_tone_is_single_unit(self):
        r = spell_syllable("u")
        self.assertEqual(len(r.parts), 1)
        self.assertEqual(triples(r), [("unit", "u", "van_u")])
        self.assertEqual(r.can_duyet, [])
        self.assertEqual(len(spell_syllable("an").parts), 1)
        self.assertEqual(len(spell_syllable("ia").parts), 1)

    def test_no_onset_rime_read_differently_from_written_gets_join(self):
        # "y" đọc "i dài": bé phải nghe lại cả tiếng "y" (bài 14 "y tá").
        r = spell_syllable("y")
        self.assertEqual(triples(r), [("unit", "y", "van_y"), ("join", "y", "tieng_y")])
        self.assertEqual([(p.say, p.akind) for p in r.parts], [("i dài", "van"), ("y", "tieng")])
        self.assertTrue(any("i dài" in n for n in r.can_duyet))
        r = spell_syllable("i")
        self.assertEqual(triples(r), [("unit", "i", "van_i"), ("join", "i", "tieng_i")])
        self.assertEqual([(p.say, p.akind) for p in r.parts], [("i ngắn", "van"), ("i", "tieng")])
        # Có dấu thì vẫn như cũ: [vần, dấu, tiếng có dấu].
        self.assertEqual(triples(spell_syllable("ý")),
                         [("unit", "y", "van_y"), ("tone", "ˊ", "dau_sac"), ("join", "ý", "tieng_ys")])

    def test_textbook_examples_full_sequence(self):
        # (say, audio) của cả chuỗi, đúng như lời đọc trong sách.
        cases = [
            (spell_rime("an"), [("a", "van_a"), ("nờ", "am_n"), ("an", "van_an")]),
            (spell_syllable("sàn"), [("sờ", "am_s"), ("an", "van_an"), ("san", "tieng_san"),
                                     ("huyền", "dau_huyen"), ("sàn", "tieng_sanf")]),
            (spell_syllable("đu"), [("đờ", "am_dd"), ("u", "van_u"), ("đu", "tieng_ddu")]),
            (spell_syllable("cử"), [("cờ", "am_c"), ("ư", "van_uw"), ("cư", "tieng_cuw"),
                                    ("hỏi", "dau_hoi"), ("cử", "tieng_cuwr")]),
            (spell_syllable("kẻ"), [("ca", "am_k"), ("e", "van_e"), ("ke", "tieng_ke"),
                                    ("hỏi", "dau_hoi"), ("kẻ", "tieng_ker")]),
            (spell_syllable("ghế"), [("gờ kép", "am_gh"), ("ê", "van_ee"), ("ghê", "tieng_ghee"),
                                     ("sắc", "dau_sac"), ("ghế", "tieng_ghees")]),
            (spell_syllable("qua"), [("quờ", "am_qu"), ("a", "van_a"), ("qua", "tieng_qua")]),
        ]
        for result, expected in cases:
            self.assertEqual([(p.say, p.audio) for p in result.parts], expected, result.target)

    def test_target_is_nfc_lowercase(self):
        self.assertEqual(spell_syllable("cử").target, "cử")
        self.assertEqual(spell_syllable("Đu").target, "đu")
        # Chuỗi dạng NFD vẫn ra cùng kết quả như NFC.
        nfd = unicodedata.normalize("NFD", "cử")
        self.assertNotEqual(nfd, "cử")
        self.assertEqual(spell_syllable(nfd), spell_syllable("cử"))

    def test_say_and_akind(self):
        r = spell_syllable("sàn")
        self.assertEqual([(p.say, p.akind) for p in r.parts],
                         [("sờ", "am"), ("an", "van"), ("san", "tieng"), ("huyền", "dau"), ("sàn", "tieng")])

    def test_tone_part_carries_tone_key(self):
        for word, tone, glyph in [("bà", "huyen", "ˋ"), ("bá", "sac", "ˊ"), ("bả", "hoi", "ˀ"),
                                  ("bã", "nga", "˜"), ("bạ", "nang", ".")]:
            tone_part = spell_syllable(word).parts[3]
            self.assertEqual((tone_part.kind, tone_part.text, tone_part.tone, tone_part.audio),
                             ("tone", glyph, tone, f"dau_{tone}"))

    def test_join_uses_written_form_not_onset_plus_rime(self):
        r = spell_syllable("gì")
        self.assertEqual(triples(r), [("unit", "gi", "am_gi"), ("unit", "i", "van_i"), ("join", "gi", "tieng_gi"),
                                      ("tone", "ˋ", "dau_huyen"), ("join", "gì", "tieng_gif")])
        self.assertNotIn("gii", [p.text for p in r.parts])

    def test_giuw_not_flagged_as_gi_plus_i(self):
        r = spell_syllable("giữ")
        self.assertEqual(triples(r), [("unit", "gi", "am_gi"), ("unit", "ư", "van_uw"), ("join", "giư", "tieng_giuw"),
                                      ("tone", "˜", "dau_nga"), ("join", "giữ", "tieng_giuwx")])
        self.assertFalse(any("không đánh vần thẳng được" in n for n in r.can_duyet))


class CanDuyetTest(unittest.TestCase):
    def test_flags(self):
        self.assertTrue(spell_syllable("ngan").can_duyet)  # tên đọc riêng tr.122 (tạm)
        self.assertTrue(any("gi" in n for n in spell_syllable("gì").can_duyet))

    def test_separate_name_note_for_each_listed_onset(self):
        for word, onset in [("ke", "k"), ("qua", "qu"), ("ga", "g"), ("ghe", "gh"), ("nga", "ng"),
                            ("nghe", "ngh"), ("gia", "gi")]:
            notes = spell_syllable(word).can_duyet
            self.assertTrue(any("tr.122" in n and f"'{onset}'" in n and "(tạm)" in n for n in notes), (word, notes))

    def test_q_note(self):
        # "q" chỉ đứng trước "u" nên bị tách thành "qu"; ghi chú nêu "qu".
        self.assertTrue(any("'qu'" in n for n in spell_syllable("quả").can_duyet))

    def test_plain_onsets_have_no_note(self):
        for word in ["đu", "cử", "sàn", "ba", "xe", "lá", "chó", "nhà", "thỏ"]:
            self.assertEqual(spell_syllable(word).can_duyet, [], word)

    def test_gieng_gets_gi_note(self):
        r = spell_syllable("giếng")
        self.assertEqual(triples(r), [("unit", "gi", "am_gi"), ("unit", "êng", "van_eeng"),
                                      ("join", "giêng", "tieng_gieeng"),
                                      ("tone", "ˊ", "dau_sac"), ("join", "giếng", "tieng_gieengs")])
        self.assertIn("gi + vần có i: không đánh vần thẳng được, cần duyệt", r.can_duyet)

    def test_gi_plus_i_gets_gi_note(self):
        r = spell_syllable("gì")
        self.assertIn("gi + vần có i: không đánh vần thẳng được, cần duyệt", r.can_duyet)
        # gì còn bị nêu: tên đọc riêng của "gi" và cách đọc tạm của "i".
        self.assertEqual(len(r.can_duyet), 3)

    def test_gi_with_other_rime_has_only_separate_name_note(self):
        notes = spell_syllable("giá").can_duyet
        self.assertEqual(len(notes), 1)
        self.assertIn("tr.122", notes[0])

    def test_i_and_y_rime_note(self):
        notes_i = spell_syllable("bì").can_duyet
        notes_y = spell_syllable("ý").can_duyet
        self.assertEqual(len(notes_i), 1)
        self.assertIn("i ngắn", notes_i[0])
        self.assertEqual(len(notes_y), 1)
        self.assertIn("i dài", notes_y[0])

    def test_multi_letter_rime_containing_i_is_not_flagged(self):
        self.assertEqual(spell_syllable("bài").can_duyet, [])
        self.assertEqual(spell_syllable("tin").can_duyet, [])


class SpellRimeTest(unittest.TestCase):
    def test_rime(self):
        self.assertEqual(triples(spell_rime("an")), [("unit", "a", "van_a"), ("unit", "n", "am_n"), ("join", "an", "van_an")])
        self.assertEqual(triples(spell_rime("ia")), [("unit", "i", "van_i"), ("unit", "a", "van_a"), ("join", "ia", "van_ia")])
        r = spell_rime("uôn")
        self.assertEqual(r.parts, [])
        self.assertTrue(r.can_duyet)

    def test_final_ng_uses_final_audio(self):
        r = spell_rime("ang")
        self.assertEqual(triples(r), [("unit", "a", "van_a"), ("unit", "ng", "am_ng_cuoi"), ("join", "ang", "van_ang")])
        self.assertEqual(r.parts[1].say, "ngờ")
        self.assertEqual(r.can_duyet, [])  # âm cuối "ng" không bị gắn tên đọc riêng tr.122

    def test_longest_final_first(self):
        self.assertEqual(triples(spell_rime("anh")), [("unit", "a", "van_a"), ("unit", "nh", "am_nh"), ("join", "anh", "van_anh")])
        self.assertEqual(triples(spell_rime("ach")), [("unit", "a", "van_a"), ("unit", "ch", "am_ch"), ("join", "ach", "van_ach")])

    def test_every_final(self):
        for final in ["c", "ch", "m", "n", "ng", "nh", "p", "t"]:
            r = spell_rime("a" + final)
            self.assertEqual(len(r.parts), 3, final)
            self.assertEqual(r.parts[2].audio, f"van_a{final}")

    def test_vowel_with_diacritic_and_final(self):
        self.assertEqual(triples(spell_rime("ăt")), [("unit", "ă", "van_aw"), ("unit", "t", "am_t"), ("join", "ăt", "van_awt")])

    def test_two_vowels(self):
        for rime in ["ua", "ưa", "ai", "ao", "oa"]:
            r = spell_rime(rime)
            self.assertEqual(len(r.parts), 3, rime)
            self.assertEqual([p.text for p in r.parts], [rime[0], rime[1], rime])
            self.assertEqual(r.parts[2].kind, "join")

    def test_rime_part_say_and_akind(self):
        r = spell_rime("an")
        self.assertEqual([(p.say, p.akind) for p in r.parts], [("a", "van"), ("nờ", "am"), ("an", "van")])

    def test_rime_i_y_note(self):
        self.assertTrue(any("i ngắn" in n for n in spell_rime("ia").can_duyet))
        self.assertTrue(any("i ngắn" in n for n in spell_rime("ai").can_duyet))
        self.assertTrue(any("i ngắn" in n for n in spell_rime("in").can_duyet))
        self.assertTrue(any("i dài" in n for n in spell_rime("ay").can_duyet))
        self.assertEqual(spell_rime("an").can_duyet, [])
        self.assertEqual(spell_rime("ua").can_duyet, [])

    def test_unsupported_shapes(self):
        for rime in ["uôn", "iêng", "ươn", "a", "ng", "anhh", "", "ach t"]:
            r = spell_rime(rime)
            self.assertEqual(r.parts, [], rime)
            self.assertEqual(len(r.can_duyet), 1, rime)
            self.assertIn("chưa có quy tắc", r.can_duyet[0])

    def test_target(self):
        self.assertEqual(spell_rime("an").target, "an")


class PartJsonTest(unittest.TestCase):
    def test_to_json_omits_tone_for_non_tone_parts(self):
        r = spell_syllable("cử")
        self.assertEqual(r.parts[0].to_json(), {"kind": "unit", "text": "c", "audio": "am_c"})
        self.assertEqual(r.parts[2].to_json(), {"kind": "join", "text": "cư", "audio": "tieng_cuw"})
        self.assertNotIn("tone", r.parts[0].to_json())

    def test_to_json_includes_tone_for_tone_parts(self):
        r = spell_syllable("cử")
        self.assertEqual(r.parts[3].to_json(), {"kind": "tone", "text": "ˀ", "audio": "dau_hoi", "tone": "hoi"})

    def test_to_json_has_no_say_or_akind(self):
        for p in spell_syllable("sàn").parts:
            self.assertEqual(set(p.to_json()) - {"tone"}, {"kind", "text", "audio"})

    def test_part_defaults(self):
        p = Part("unit", "a", "van_a")
        self.assertIsNone(p.tone)
        self.assertEqual(p.to_json(), {"kind": "unit", "text": "a", "audio": "van_a"})

    def test_spell_result_fields(self):
        r = SpellResult("x", [], [])
        self.assertEqual((r.target, r.parts, r.can_duyet), ("x", [], []))


if __name__ == "__main__":
    unittest.main()
