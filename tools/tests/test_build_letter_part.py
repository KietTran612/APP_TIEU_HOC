"""Phần dựng thêm cho đợt 1 (bài 18–41): cặp chữ hoa, luật chính tả, nhãn hàng đọc thêm, ô bị chặn, chọn chữ hoa."""

import unittest

from tapdoc.build import BuildError, build_lesson
from tapdoc.ids import audio_for
from tests.test_build import src_of


def mini(**kw):
    return src_of(**kw)


def step_of(step):
    return build_lesson(mini(part1=[step])).lesson["part1"][0]


class LetterPairsTest(unittest.TestCase):
    def test_letter_pairs(self):
        st = step_of({"type": "letter_pairs", "letters": ["a", "đ", "q"]})
        self.assertEqual(st["type"], "letter_pairs")
        self.assertEqual([(i["text"], i["upper"], i["audio"]) for i in st["items"]],
                         [("a", "A", "van_a"), ("đ", "Đ", "am_dd"), ("q", "Q", "am_q")])
        self.assertEqual({i["role"] for i in st["items"]}, {"pair"})

    def test_letter_pairs_flow_in_four_columns(self):
        st = step_of({"type": "letter_pairs", "letters": ["a", "ă", "â", "b", "c"]})
        self.assertEqual([(i["row"], i["col"]) for i in st["items"]], [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0)])

    def test_q_name_needs_review(self):
        r = build_lesson(mini(part1=[{"type": "letter_pairs", "letters": ["q"]}]))
        self.assertTrue(any("'q'" in n["note"] for n in r.lesson["review"]["can_duyet"]))

    def test_letter_pairs_audio_is_registered(self):
        r = build_lesson(mini(part1=[{"type": "letter_pairs", "letters": ["a", "q"]}]))
        self.assertIn("van_a", r.audio)
        self.assertIn("am_q", r.audio)


class RuleTest(unittest.TestCase):
    def test_rule_lines_get_sentence_audio(self):
        r = build_lesson(mini(part1=[{"type": "rule", "lines": ["k chỉ ghép với e, ê, i", "gh chỉ ghép với e, ê, i"]}]))
        st = r.lesson["part1"][0]
        self.assertEqual(st["type"], "rule")
        self.assertEqual([i["audio"] for i in st["items"]], ["cau_b99_01", "cau_b99_02"])
        self.assertEqual([i["role"] for i in st["items"]], ["line", "line"])
        self.assertEqual(r.audio["cau_b99_01"][0], "k chỉ ghép với e, ê, i")

    def test_rule_shares_counter_with_sentences(self):
        r = build_lesson(mini(part1=[{"type": "sentence", "text": "bé có bê."},
                                     {"type": "rule", "lines": ["k chỉ ghép với e, ê, i"]}]))
        self.assertEqual(r.lesson["part1"][1]["items"][0]["audio"], "cau_b99_02")


class ReadingLabelsTest(unittest.TestCase):
    def test_reading_labels(self):
        st = step_of({"type": "reading", "rows": [{"label": "a – a", "items": ["ra rả", "khà khà"]}, ["lò dò"]]})
        self.assertEqual(st["labels"], ["a – a", ""])
        self.assertEqual([i["row"] for i in st["items"]], [0, 0, 1])

    def test_reading_without_labels_has_empty_labels(self):
        st = step_of({"type": "reading", "rows": [["bé"], ["bê"]]})
        self.assertEqual(st["labels"], ["", ""])


class CombineBlockedTest(unittest.TestCase):
    def test_combine_blocked(self):
        st = step_of({"type": "combine_table",
                      "rows": [{"onset": "k", "cells": {"e": ["ke"]}, "blocked": ["a", "o"]}]})
        roles = [(i["role"], i["row"], i["col"]) for i in st["items"]]
        self.assertIn(("blocked", 0, 1), roles)  # cột theo thứ tự gặp: e, a, o
        self.assertIn(("blocked", 0, 2), roles)
        self.assertIn(("vowel", 0, 1), roles)  # nguyên âm chỉ có ở `blocked` vẫn có cột
        blocked = [i for i in st["items"] if i["role"] == "blocked"]
        self.assertEqual({i["text"] for i in blocked}, {""})
        self.assertFalse(any("audio" in i for i in blocked))  # ô gạch chéo không có âm thanh nào

    def test_combine_blocked_conflict(self):
        with self.assertRaises(BuildError):
            step_of({"type": "combine_table",
                     "rows": [{"onset": "k", "cells": {"e": ["ke"]}, "blocked": ["e"]}]})

    def test_blocked_column_shared_with_later_rows(self):
        st = step_of({"type": "combine_table",
                      "rows": [{"onset": "k", "cells": {"e": ["ke"]}, "blocked": ["a"]},
                               {"onset": "c", "cells": {"a": ["ca"]}, "blocked": ["e"]}]})
        cells = [(i["role"], i["row"], i["col"]) for i in st["items"] if i["role"] in ("base", "blocked")]
        self.assertEqual(cells, [("base", 0, 0), ("blocked", 0, 1), ("base", 1, 1), ("blocked", 1, 0)])


class GiRowTest(unittest.TestCase):
    def test_gi_with_i_makes_gi(self):
        st = step_of({"type": "combine_table", "rows": [{"onset": "gi", "cells": {"a": ["gia"], "i": ["gi"]}}]})
        self.assertIn(("base", "gi", 1), [(i["role"], i["text"], i["col"]) for i in st["items"]])

    def test_other_onsets_still_need_onset_plus_vowel(self):
        with self.assertRaises(BuildError):
            step_of({"type": "combine_table", "rows": [{"onset": "g", "cells": {"i": ["g"]}}]})


class RuleMarkerTest(unittest.TestCase):
    def test_rule_keeps_marker(self):
        st = step_of({"type": "rule", "marker": "⌂", "lines": ["Ghép thêm dấu thanh để tạo tiếng mới ở nhà."]})
        self.assertEqual(st["marker"], "⌂")
        self.assertEqual(step_of({"type": "rule", "lines": ["k chỉ ghép với e, ê, i"]})["marker"], "")


class MatchCaseTest(unittest.TestCase):
    def test_match_case_round(self):
        rd = build_lesson(mini(part2=[{"kind": "match_case",
                                       "rounds": [{"model": "a", "answer": "A", "options": ["Ă", "A", "Â"]}]}])
                          ).lesson["part2"][0]
        self.assertEqual((rd["kind"], rd["prompt_text"], rd["answer"], rd["instruction_audio"]),
                         ("match_case", "a", 1, "hd_nhin_chon_chu_hoa"))
        self.assertEqual([o["text"] for o in rd["options"]], ["Ă", "A", "Â"])
        self.assertEqual(rd["prompt_audio"], "")

    def test_match_case_answer_must_be_upper_of_model(self):
        with self.assertRaises(BuildError):
            build_lesson(mini(part2=[{"kind": "match_case",
                                      "rounds": [{"model": "a", "answer": "Ă", "options": ["Ă", "A"]}]}]))


class UpperLetterAudioTest(unittest.TestCase):
    def test_upper_letter_reads_like_lower(self):
        self.assertEqual(audio_for("Đ"), audio_for("đ"))
        self.assertEqual(audio_for("A"), audio_for("a"))
        self.assertEqual(audio_for("Gh"), audio_for("gh"))

    def test_listen_choose_with_upper_options(self):
        rd = build_lesson(mini(part2=[{"kind": "listen_choose", "answer": "Đ", "options": ["Đ", "B"]}])).lesson["part2"][0]
        self.assertEqual(rd["prompt_audio"], "am_dd")
        self.assertEqual([o["audio"] for o in rd["options"]], ["am_dd", "am_b"])


if __name__ == "__main__":
    unittest.main()
