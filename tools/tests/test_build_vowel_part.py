"""Bảng vần, đánh vần các vần Tập 1 và chữ hoa trong câu."""

import unittest

from tapdoc.build import BuildError, build_lesson
from tapdoc.curriculum import is_learned_text, learned_until, load_curriculum
from tapdoc.paths import LESSON_INDEX
from tapdoc.spelling import spell_rime
from tests.test_build import src_of


def step_of(step, new_units=(), kind="van_moi"):
    src = src_of(part1=[step], new_units=new_units)
    src["type"] = kind
    return build_lesson(src).lesson["part1"][0]


class RimeTableTest(unittest.TestCase):
    def test_rows(self):
        st = step_of({"type": "rime_table", "rows": [
            {"rime": "an", "word": "nhà sàn"}, {"rime": "ăn", "word": "củ sắn"}]})
        self.assertEqual(st["type"], "rime_table")
        self.assertEqual(st["marker"], "")
        self.assertEqual([(i["role"], i["row"], i["text"]) for i in st["items"]],
                         [("rime", 0, "an"), ("word", 0, "nhà sàn"), ("rime", 1, "ăn"), ("word", 1, "củ sắn")])
        self.assertEqual([p["audio"] for p in st["items"][0]["spells"][0]["parts"]],
                         ["van_a", "am_n", "van_an"])
        self.assertEqual(st["items"][1]["hl"], [{"s": 5, "n": 2}])
        self.assertEqual(st["items"][3]["hl"], [{"s": 4, "n": 2}])
        self.assertEqual([s["target"] for s in st["items"][1]["spells"]], ["nhà", "sàn"])

    def test_audio_registered(self):
        r = build_lesson(src_of(part1=[{"type": "rime_table", "rows": [
            {"rime": "an", "word": "nhà sàn"}]}]))
        self.assertIn("van_an", r.audio)
        self.assertIn("tu_nhaf_sanf", r.audio)

    def test_rime_that_cannot_be_spelled_is_an_error(self):
        with self.assertRaises(BuildError):
            step_of({"type": "rime_table", "rows": [{"rime": "uôi", "word": "con muỗi"}]})

    def test_all_matching_syllables_and_marker(self):
        st = step_of({"type": "rime_table", "marker": "●", "rows": [
            {"rime": "an", "word": "Lan, sàn ngan"}]}, new_units=["l"])
        self.assertEqual(st["marker"], "●")
        self.assertEqual(st["items"][1]["hl"], [{"s": 1, "n": 2}, {"s": 6, "n": 2}, {"s": 11, "n": 2}])


class AllRimesTest(unittest.TestCase):
    def test_every_rime_spells_vowel_final_join(self):
        rimes = []
        for no, (kind, content) in load_curriculum(LESSON_INDEX).items():
            if 42 <= no <= 78 and kind == "van_moi":
                for item in content.split(";"):
                    item = item.strip()
                    if item and not item.startswith("chữ "):
                        rimes.append(item.removeprefix("vần "))
        self.assertGreaterEqual(len(rimes), 40)
        self.assertTrue({"an", "ay", "ưu", "ip"}.issubset(rimes))
        for rime in rimes:
            with self.subTest(rime=rime):
                result = spell_rime(rime)
                self.assertEqual(len(result.parts), 3)
                self.assertEqual(tuple(p.kind for p in result.parts), ("unit", "unit", "join"))
                self.assertEqual(result.parts[2].text, rime)
                self.assertEqual(result.parts[0].text + result.parts[1].text, rime)

    def test_ay_reads_i_dai_with_note(self):
        result = spell_rime("ay")
        self.assertEqual(result.parts[1].audio, "van_y")
        self.assertTrue(any("i dài" in note for note in result.can_duyet))


class CapitalsTest(unittest.TestCase):
    def test_sentence_with_capitals_and_names(self):
        st = step_of({"type": "sentence", "text": "Lan cho ngan ăn giun, bà khen Lan."},
                     new_units=["an", "en", "un"])
        self.assertEqual(st["items"][0]["audio"], "tieng_lan")
        self.assertTrue(st["items"][0]["hl"])
        self.assertEqual(st["items"][0]["text"], "Lan")
        self.assertEqual(st["items"][0]["hl"], [{"s": 1, "n": 2}])
        self.assertEqual(st["items"][-1]["hl"], [{"s": 1, "n": 2}])

    def test_letter_lessons_do_not_colour_sentences(self):
        # Sách: câu ở bài âm mới không tô chữ mới (bài 28 "mẹ bế bé ngủ"); bài vần thì tô vần mới.
        st = step_of({"type": "sentence", "text": "mẹ bế bé ngủ"}, new_units=["ng"], kind="am_moi")
        self.assertEqual([i["hl"] for i in st["items"]], [[], [], [], []])
        st = step_of({"type": "sentence", "text": "Cô hôn bé."}, new_units=["ôn"], kind="van_moi")
        self.assertEqual(st["items"][1]["hl"], [{"s": 1, "n": 2}])
        st = step_of({"type": "sentence", "text": "Bé chăm làm."}, new_units=["ăm", "am"], kind="on_tap_van")
        self.assertTrue(st["items"][1]["hl"])

    def test_curly_quotes_and_dialogue_dash(self):
        st = step_of({"type": "sentence", "text": "“Ủn à ủn ỉn!”"}, new_units=["un", "in"])
        self.assertEqual([i["text"] for i in st["items"]], ["Ủn", "à", "ủn", "ỉn"])
        st = step_of({"type": "sentence", "text": "– Ai gọi đó?"})
        self.assertEqual([i["text"] for i in st["items"]], ["Ai", "gọi", "đó"])

    def test_capitals_count_as_learned(self):
        self.assertTrue(is_learned_text("Lan", learned_until(load_curriculum(LESSON_INDEX), 48)))


if __name__ == "__main__":
    unittest.main()
