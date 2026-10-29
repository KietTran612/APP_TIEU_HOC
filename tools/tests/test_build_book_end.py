"""Phần dựng cho cuối tập 1 (bài 79–80): bảng ôn vần (rime_grid) và câu đố nghe chọn tranh."""

import unittest

from tapdoc.build import BuildError, build_lesson
from tests.test_build import src_of


def step_of(step):
    return build_lesson(src_of(part1=[step])).lesson["part1"][0]


class RimeGridTest(unittest.TestCase):
    def test_grid(self):
        st = step_of({
            "type": "rime_grid",
            "finals": ["n", "i-y"],
            "rows": [
                {"vowel": "a", "cells": ["an", "ai - ay"]},
                {"vowel": "ư", "cells": ["", "ưi"]},
            ],
        })
        self.assertEqual(st["type"], "rime_grid")
        cells = [(i["row"], i["col"], i["text"], len(i["spells"])) for i in st["items"] if i["role"] == "cell"]
        self.assertEqual(cells, [(0, 0, "an", 1), (0, 1, "ai - ay", 2), (1, 1, "ưi", 1)])
        self.assertEqual([(i["role"], i["text"]) for i in st["items"][:2]], [("final", "n"), ("final", "i-y")])
        vowels = [(i["row"], i["text"]) for i in st["items"] if i["role"] == "vowel"]
        self.assertEqual(vowels, [(0, "a"), (1, "ư")])
        ai_ay = next(i for i in st["items"] if i["role"] == "cell" and i["text"] == "ai - ay")
        self.assertEqual(
            [[p["audio"] for p in sp["parts"]] for sp in ai_ay["spells"]],
            [["van_a", "van_i", "van_ai"], ["van_a", "van_y", "van_ay"]],
        )

    def test_row_length_mismatch_is_an_error(self):
        with self.assertRaises(BuildError):
            step_of({
                "type": "rime_grid",
                "finals": ["n", "m"],
                "rows": [{"vowel": "a", "cells": ["an"]}],
            })

    def test_unspellable_rime_is_an_error(self):
        with self.assertRaises(BuildError):
            step_of({
                "type": "rime_grid",
                "finals": ["n"],
                "rows": [{"vowel": "a", "cells": ["xyz"]}],
            })

    def test_cell_audio_registered(self):
        r = build_lesson(src_of(part1=[{
            "type": "rime_grid",
            "finals": ["n", "i-y"],
            "rows": [{"vowel": "a", "cells": ["an", "ai - ay"]}],
        }]))
        self.assertIn("van_ai", r.audio)
        self.assertIn("van_ay", r.audio)


class RiddleRoundTest(unittest.TestCase):
    IMAGES = {
        "img_b80_con_lownj": "Con lợn",
        "img_b80_con_meof": "Con mèo",
        "img_b80_con_gaf": "Con gà",
    }
    PART1 = [
        {"type": "keyword", "text": "con lợn", "image": "img_b80_con_lownj"},
        {"type": "keyword", "text": "con mèo", "image": "img_b80_con_meof"},
        {"type": "keyword", "text": "con gà", "image": "img_b80_con_gaf"},
    ]
    RIDDLE = "Con gì ăn no, má to mắt híp, mồm kêu ụt ịt, nằm thở phì phò?"

    def test_prompt_is_riddle_not_answer(self):
        r = build_lesson(src_of(
            part1=self.PART1,
            part2=[{
                "kind": "listen_picture",
                "word": "con lợn",
                "prompt": self.RIDDLE,
                "answer": "img_b80_con_lownj",
                "options": ["img_b80_con_lownj", "img_b80_con_meof", "img_b80_con_gaf"],
            }],
            lesson_id="tv1_t1_b80",
            lesson_no=80,
            images=self.IMAGES,
        ))
        rd = r.lesson["part2"][0]
        self.assertTrue(rd["prompt_audio"].startswith("cau_b80_"))
        self.assertNotEqual(rd["prompt_audio"], "tu_con_lownj")
        self.assertEqual(rd["instruction_audio"], "hd_nghe_do_chon_tranh")
        self.assertEqual(r.audio[rd["prompt_audio"]], (self.RIDDLE, "cau"))

    def test_without_prompt_unchanged(self):
        r = build_lesson(src_of(
            part1=self.PART1,
            part2=[{
                "kind": "listen_picture",
                "word": "con lợn",
                "answer": "img_b80_con_lownj",
                "options": ["img_b80_con_lownj", "img_b80_con_meof", "img_b80_con_gaf"],
            }],
            lesson_id="tv1_t1_b80",
            lesson_no=80,
            images=self.IMAGES,
        ))
        rd = r.lesson["part2"][0]
        self.assertEqual(rd["prompt_audio"], "tu_con_lownj")
        self.assertEqual(rd["instruction_audio"], "hd_nghe_chon_tranh")


if __name__ == "__main__":
    unittest.main()
