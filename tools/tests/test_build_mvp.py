"""Phần dựng thêm cho bản đầu tiên: bảng dấu, khung chữ, bảng ghép, tranh có từ, `in_app`."""

import json
import tempfile
import unittest
from pathlib import Path

from tapdoc.build import BuildError, build_all, build_lesson
from tests.test_build import src_of


def mini(**kw):
    return src_of(**kw)


TONE_TABLE = {"type": "tone_table", "base": "đo", "results": ["đò", "đó", "đỏ", "đõ", "đọ"]}


class ToneTableTest(unittest.TestCase):
    def test_tone_table(self):
        st = build_lesson(mini(part1=[TONE_TABLE])).lesson["part1"][0]
        self.assertEqual((st["type"], st["text"], st["audio"]), ("tone_table", "đo", "tieng_ddo"))
        self.assertEqual([i["tone"] for i in st["items"]], ["huyen", "sac", "hoi", "nga", "nang"])
        self.assertEqual([i["text"] for i in st["items"]], ["đò", "đó", "đỏ", "đõ", "đọ"])
        self.assertEqual({i["role"] for i in st["items"]}, {"cell"})
        self.assertEqual(st["items"][2]["glyph"], "ˀ")
        self.assertEqual([p["audio"] for p in st["items"][3]["spells"][0]["parts"]],
                         ["tieng_ddo", "dau_nga", "tieng_ddox"])

    def test_tone_table_audio_is_registered(self):
        r = build_lesson(mini(part1=[TONE_TABLE]))
        for audio_id in ("tieng_ddo", "tieng_ddof", "tieng_ddox", "dau_nga"):
            self.assertIn(audio_id, r.audio)

    def test_tone_table_rejects_wrong_base(self):
        with self.assertRaises(BuildError):
            build_lesson(mini(part1=[{"type": "tone_table", "base": "đo", "results": ["đà"]}]))

    def test_tone_table_rejects_result_without_tone(self):
        with self.assertRaises(BuildError):
            build_lesson(mini(part1=[{"type": "tone_table", "base": "đo", "results": ["đo"]}]))

    def test_tone_table_rejects_duplicate_tone(self):
        with self.assertRaises(BuildError):
            build_lesson(mini(part1=[{"type": "tone_table", "base": "đo", "results": ["đò", "đò"]}]))


class LetterGridTest(unittest.TestCase):
    def test_letter_grid(self):
        st = build_lesson(mini(part1=[{"type": "letter_grid", "letters": ["o", "c"], "tones": ["sac"]}])).lesson["part1"][0]
        self.assertEqual(st["type"], "letter_grid")
        self.assertEqual([(i["role"], i["text"], i["audio"], i["row"]) for i in st["items"]],
                         [("letter", "o", "van_o", 0), ("letter", "c", "am_c", 0), ("tone", "ˊ", "dau_sac", 1)])
        self.assertEqual(st["items"][2]["tone"], "sac")

    def test_letter_grid_without_tones(self):
        st = build_lesson(mini(part1=[{"type": "letter_grid", "letters": ["ô", "t"]}])).lesson["part1"][0]
        self.assertEqual([i["role"] for i in st["items"]], ["letter", "letter"])

    def test_letter_grid_rejects_bad_tone(self):
        with self.assertRaises(BuildError):
            build_lesson(mini(part1=[{"type": "letter_grid", "letters": ["o"], "tones": ["sắc"]}]))


class CombineTableTest(unittest.TestCase):
    ROWS = [{"onset": "c", "cells": {"o": ["co", "có"], "a": ["ca"]}}, {"onset": "d", "cells": {"o": ["do"]}}]

    def build(self, rows=None):
        return build_lesson(mini(part1=[{"type": "combine_table", "rows": rows or self.ROWS}]))

    def test_combine_table(self):
        st = self.build().lesson["part1"][0]
        self.assertEqual(st["type"], "combine_table")
        roles = [(i["role"], i["text"], i["row"], i["col"]) for i in st["items"]]
        self.assertIn(("onset", "c", 0, 0), roles)
        self.assertIn(("onset", "d", 1, 0), roles)
        self.assertIn(("vowel", "o", 0, 0), roles)
        self.assertIn(("vowel", "a", 0, 1), roles)
        self.assertIn(("base", "co", 0, 0), roles)
        self.assertIn(("form", "có", 0, 0), roles)
        self.assertIn(("base", "do", 1, 0), roles)
        self.assertEqual(len([r for r in roles if r[0] == "vowel"]), 2)

    def test_base_spells_onset_vowel_join(self):
        st = self.build().lesson["part1"][0]
        base = next(i for i in st["items"] if i["role"] == "base" and i["text"] == "co")
        self.assertEqual(base["audio"], "tieng_co")
        self.assertEqual([p["audio"] for p in base["spells"][0]["parts"]], ["am_c", "van_o", "tieng_co"])

    def test_form_spells_from_base(self):
        st = self.build().lesson["part1"][0]
        form = next(i for i in st["items"] if i["role"] == "form")
        self.assertEqual((form["text"], form["tone"], form["audio"]), ("có", "sac", "tieng_cos"))
        self.assertEqual([p["audio"] for p in form["spells"][0]["parts"]], ["tieng_co", "dau_sac", "tieng_cos"])

    def test_marker_passthrough(self):  # sách in ● trước bảng ghép
        st = build_lesson(mini(part1=[{"type": "combine_table", "marker": "●", "rows": self.ROWS}])).lesson["part1"][0]
        self.assertEqual(st["marker"], "●")
        self.assertEqual(self.build().lesson["part1"][0]["marker"], "")

    def test_rejects_base_not_onset_plus_vowel(self):
        with self.assertRaises(BuildError):
            self.build([{"onset": "c", "cells": {"o": ["ca"]}}])

    def test_rejects_form_with_other_base(self):
        with self.assertRaises(BuildError):
            self.build([{"onset": "c", "cells": {"o": ["co", "cá"]}}])


class PictureWordTest(unittest.TestCase):
    def test_picture_word_usable_in_listen_picture(self):
        s = mini(images={"img_b02_cof": "con cò", "img_b02_keos_co": "kéo co"},
                 part1=[{"type": "keyword", "text": "kéo co", "image": "img_b02_keos_co"},
                        {"type": "picture", "image": "img_b02_cof", "say": "con cò", "word": "con cò"}],
                 part2=[{"kind": "listen_picture", "word": "con cò", "answer": "img_b02_cof",
                         "options": ["img_b02_keos_co", "img_b02_cof"]}])
        r = build_lesson(s)
        self.assertEqual(r.lesson["part2"][0]["options"][1]["text"], "con cò")
        self.assertNotIn("word", r.lesson["part1"][1])

    def test_picture_without_word_still_not_in_listen_picture(self):
        s = mini(images={"img_b02_cof": "con cò"},
                 part1=[{"type": "picture", "image": "img_b02_cof", "say": "con cò"}],
                 part2=[{"kind": "listen_picture", "word": "con cò", "answer": "img_b02_cof",
                         "options": ["img_b02_cof"]}])
        with self.assertRaises(BuildError):
            build_lesson(s)


class InAppTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.src_dir = self.root / "src"
        self.src_dir.mkdir()

    def write_src(self, name, data):
        (self.src_dir / name).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def test_in_app_false_excluded_from_index(self):
        hidden = mini()
        hidden["in_app"] = False
        self.write_src("b99.json", hidden)
        self.write_src("b98.json", mini(lesson_id="tv1_t1_b98", lesson_no=98))
        out = self.root / "out"
        build_all(self.src_dir, out)
        ids = [e["lesson_id"] for e in json.loads((out / "index.json").read_text("utf-8"))["lessons"]]
        self.assertEqual(ids, ["tv1_t1_b98"])
        self.assertTrue((out / "tv1_t1_b99.json").exists())

    def test_in_app_is_written_to_lesson(self):
        hidden = mini()
        hidden["in_app"] = False
        self.assertIs(build_lesson(hidden).lesson["in_app"], False)
        self.assertIs(build_lesson(mini()).lesson["in_app"], True)

    def test_in_app_must_be_bool(self):
        bad = mini()
        bad["in_app"] = "no"
        with self.assertRaises(BuildError):
            build_lesson(bad)


if __name__ == "__main__":
    unittest.main()
