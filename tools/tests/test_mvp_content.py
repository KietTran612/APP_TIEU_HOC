"""Nội dung bản đầu tiên (bài 1–17): đối chiếu với trang sách đã chép trong kế hoạch MVP."""

import csv
import json
import unittest

from tapdoc.build import build_lesson, load_sources
from tapdoc.paths import CONTENT_SRC, LESSON_INDEX, UNITY_RES

L = {r.lesson["lesson_id"]: r.lesson for r in (build_lesson(s) for s in load_sources(CONTENT_SRC))}


def aud(spell):
    return [p["audio"] for p in spell["parts"]]


def types(lid):
    return [s["type"] for s in L[lid]["part1"]]


class MvpLessons1To6Test(unittest.TestCase):
    def test_b01_has_no_spelling(self):
        self.assertEqual(types("tv1_t1_b01"), ["unit", "keyword", "analyze", "picture", "picture"])
        self.assertFalse(any(s["type"] == "spell" for s in L["tv1_t1_b01"]["part1"]))

    def test_b01_listen_picture_uses_keyword_text(self):
        prompts = [r["prompt_audio"] for r in L["tv1_t1_b01"]["part2"]]
        self.assertEqual(prompts[0], L["tv1_t1_b01"]["part1"][1]["audio"])  # "ò ó o... o!"
        self.assertTrue(all(r["kind"] == "listen_picture" and len(r["options"]) == 3 for r in L["tv1_t1_b01"]["part2"]))

    def test_b02_spell(self):
        self.assertEqual(aud(L["tv1_t1_b02"]["part1"][3]["spell"]), ["am_c", "van_o", "tieng_co"])

    def test_b05_two_units_and_reading(self):
        self.assertEqual(types("tv1_t1_b05").count("unit"), 2)
        self.assertEqual([i["text"] for i in L["tv1_t1_b05"]["part1"][-1]["items"]], ["do", "dò", "dó", "đa", "đò", "đá"])

    def test_b06_tone_table(self):
        st = L["tv1_t1_b06"]["part1"][6]
        self.assertEqual(st["type"], "tone_table")
        self.assertEqual([i["text"] for i in st["items"]], ["đò", "đó", "đỏ", "đõ", "đọ"])

    def test_b06_nga_is_flagged(self):
        self.assertTrue(any(n["where"] == "part1[3]" for n in L["tv1_t1_b06"]["review"]["can_duyet"]))

    def test_round_counts(self):
        for lid in ("tv1_t1_b01", "tv1_t1_b02", "tv1_t1_b03", "tv1_t1_b05", "tv1_t1_b06"):
            self.assertTrue(6 <= len(L[lid]["part2"]) <= 10, lid)

    def test_pictures_are_flagged_for_review(self):
        for lid in ("tv1_t1_b01", "tv1_t1_b03"):
            notes = L[lid]["review"]["can_duyet"]
            pictures = [i for i, s in enumerate(L[lid]["part1"]) if s["type"] == "picture"]
            for i in pictures:
                self.assertTrue(any(n["where"] == f"part1[{i}]" for n in notes), (lid, i))


class MvpLessons7To11Test(unittest.TestCase):
    def test_b07_review_tables(self):
        self.assertEqual(types("tv1_t1_b07"), ["letter_grid", "combine_table"])
        grid = L["tv1_t1_b07"]["part1"][0]["items"]
        self.assertEqual([i["text"] for i in grid if i["role"] == "letter"], ["o", "a", "c", "d", "đ"])
        self.assertEqual([i["tone"] for i in grid if i["role"] == "tone"], ["sac", "huyen", "hoi", "nga", "nang"])
        st = L["tv1_t1_b07"]["part1"][1]
        self.assertEqual(st["marker"], "●")
        self.assertEqual(sorted(i["text"] for i in st["items"] if i["role"] == "base"), ["ca", "co", "da", "do", "đa", "đo"])

    def test_b11_table_has_21_bases(self):
        st = L["tv1_t1_b11"]["part1"][1]
        self.assertEqual(len([i for i in st["items"] if i["role"] == "base"]), 21)
        self.assertEqual([i["text"] for i in st["items"] if i["role"] == "vowel"], ["a", "o", "ô", "ơ", "e", "ê", "i"])

    def test_b10_sentence_and_i_note(self):
        self.assertEqual(L["tv1_t1_b10"]["part1"][-2]["text"], "tí đi ô tô")
        self.assertTrue(any(n["where"].startswith("part1[3]") for n in L["tv1_t1_b10"]["review"]["can_duyet"]))

    def test_b08_b09_spells(self):
        self.assertEqual(aud(L["tv1_t1_b08"]["part1"][6]["spell"]), ["am_c", "van_ow", "tieng_cow", "dau_huyen", "tieng_cowf"])
        self.assertEqual(aud(L["tv1_t1_b09"]["part1"][7]["spell"]), ["am_d", "van_ee", "tieng_dee", "dau_sac", "tieng_dees"])

    def test_round_counts(self):
        for lid in ("tv1_t1_b07", "tv1_t1_b08", "tv1_t1_b09", "tv1_t1_b10", "tv1_t1_b11"):
            self.assertTrue(6 <= len(L[lid]["part2"]) <= 10, lid)


class MvpLessons12To17Test(unittest.TestCase):
    def test_b14_y_spells_with_tieng(self):
        self.assertEqual(aud(L["tv1_t1_b14"]["part1"][3]["spell"]), ["van_y", "tieng_y"])

    def test_b15_reading_has_13_items(self):
        self.assertEqual(len(L["tv1_t1_b15"]["part1"][-1]["items"]), 13)

    def test_b15_xe_lu_spells_only_lu(self):
        words = next(s for s in L["tv1_t1_b15"]["part1"] if s["type"] == "words")
        xe_lu = next(i for i in words["items"] if i["text"] == "xe lu")
        self.assertEqual([sp["target"] for sp in xe_lu["spells"]], ["lu"])

    def test_b16_two_sentences(self):
        self.assertEqual(types("tv1_t1_b16").count("sentence"), 2)

    def test_b17_table(self):
        st = L["tv1_t1_b17"]["part1"][1]
        self.assertEqual(len([i for i in st["items"] if i["role"] == "base"]), 36)
        self.assertEqual([i["text"] for i in L["tv1_t1_b17"]["part1"][2]["items"]], ["y tế", "y tá", "y bạ"])

    def test_index_lists_lessons_1_to_17(self):
        ids = [e["lesson_id"] for e in json.loads((UNITY_RES / "lessons" / "index.json").read_text("utf-8"))["lessons"]]
        self.assertEqual(ids[:17], [f"tv1_t1_b{n:02d}" for n in range(1, 18)])  # bài 1–17 đứng đầu, đúng thứ tự
        self.assertNotIn("tv1_t1_b42", ids)  # bài 42 còn in_app false

    def test_y_and_i_never_together_in_listening(self):  # y và i cùng đọc /i/
        for lid, lesson in L.items():
            for r in lesson["part2"]:
                if r["kind"] == "listen_choose":
                    self.assertFalse({"i", "y"} <= {o["text"] for o in r["options"]}, lid)

    def test_round_counts_all_lessons(self):
        for n in range(1, 18):
            lid = f"tv1_t1_b{n:02d}"
            self.assertTrue(6 <= len(L[lid]["part2"]) <= 10, lid)

    def test_curriculum_marks_lessons_page_verified(self):
        rows = [r for r in csv.DictReader(LESSON_INDEX.read_text("utf-8-sig").splitlines())
                if r["book_id"] == "tv1_t1_1990" and r["bai_so"].isdigit() and 1 <= int(r["bai_so"]) <= 17]
        self.assertEqual({r["muc_xac_minh"] for r in rows}, {"page_verified"})


if __name__ == "__main__":
    unittest.main()
