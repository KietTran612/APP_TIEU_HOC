import copy
import io
import json
import tempfile
import unicodedata
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from tapdoc import __main__ as cli
from tapdoc.build import BuildError, BuildResult, _Builder, build_all, build_lesson, load_sources
from tapdoc.system_assets import SYSTEM_AUDIO, SYSTEM_IMAGES

HUYEN = "ˋ"  # ˋ
SAC = "ˊ"  # ˊ

SRC13 = {
    "lesson_id": "tv1_t1_b13", "book": "tv1_t1_1990", "lesson_no": 13, "type": "am_moi", "title": "u ư",
    "source": {"pages": [18], "scan_file": "010", "verification": "page_verified"},
    "new_units": ["u", "ư"],
    "images": {
        "img_b13_cais_ddu": "Bé gái ngồi trên ván đu, hai tay nắm hai sợi dây đu",
        "img_b13_cur_tuwf": "Một củ từ (khoai từ) vỏ sần, có vài rễ con",
        "img_b13_unused": "Tranh không dùng đến",
    },
    "review": {"status": "chua_duyet", "notes": [{"where": "part1[0]", "note": "ghi chú từ nguồn"}]},
    "part1": [
        {"type": "unit", "text": "u"},
        {"type": "keyword", "text": "cái đu", "image": "img_b13_cais_ddu"},
        {"type": "analyze", "rows": ["cái đu", "đu", "u"]},
        {"type": "spell", "target": "đu", "then": "cái đu"},
        {"type": "words", "marker": "", "items": [{"text": "củ từ", "image": "img_b13_cur_tuwf"}]},
        {"type": "sentence", "marker": "●", "text": "má có củ từ"},
        {"type": "reading", "marker": "⌂", "rows": [["cù", "dù"], ["từ từ"]]},
    ],
    "part2": [
        {"kind": "listen_choose", "rounds": [{"answer": "u", "options": ["ư", "u", "o"]}]},
        {"kind": "listen_choose", "tag": "look_alike",
         "rounds": [{"answer": "u", "options": ["u", "ư"]}, {"answer": "ư", "options": ["u", "ư"]}]},
        {"kind": "compose", "word": "củ từ", "template": "củ t_", "answer": "ừ", "options": ["ừ", "ù", "à"],
         "image": "img_b13_cur_tuwf"},
        {"kind": "listen_picture", "word": "củ từ", "answer": "img_b13_cur_tuwf",
         "options": ["img_b13_cais_ddu", "img_b13_cur_tuwf"]},
    ],
}

SRC04 = {
    "lesson_id": "tv1_t1_b04", "book": "tv1_t1_1990", "lesson_no": 4, "type": "dau_thanh", "title": "Dấu huyền - Dấu sắc",
    "source": {"pages": [9], "scan_file": "005", "verification": "page_verified"},
    "new_units": ["huyen", "sac"],
    "images": {
        "img_b04_ca": "Cái ca có quai",
        "img_b04_caf": "Quả cà tròn",
        "img_b04_cas": "Con cá có vảy",
        "img_b04_mua": "Năm bạn gái múa",
    },
    "review": {"status": "chua_duyet", "notes": [{"where": "part1[7]", "note": "ghi chú nguồn"}]},
    "part1": [
        {"type": "keyword", "text": "ca", "image": "img_b04_ca"},
        {"type": "spell", "target": "ca"},
        {"type": "tone_intro", "tone": "huyen"},
        {"type": "tone_attach", "target": "cà", "image": "img_b04_caf"},
        {"type": "tone_intro", "tone": "sac"},
        {"type": "tone_attach", "target": "cá", "image": "img_b04_cas"},
        {"type": "picture", "image": "img_b04_mua", "say": "Các bạn đang múa."},
        {"type": "words", "marker": "●", "items": [{"text": "có cà"}, {"text": "có cá"}]},
    ],
    "part2": [
        {"kind": "look_tone", "tag": "look_alike",
         "rounds": [{"model": "cá", "options": ["huyen", "sac"]}, {"model": "cà", "options": ["huyen", "sac"]}]},
        {"kind": "listen_picture", "rounds": [
            {"word": "cá", "answer": "img_b04_cas", "options": ["img_b04_ca", "img_b04_caf", "img_b04_cas"]}]},
    ],
}


def src_of(part1=(), part2=(), new_units=(), images=None, notes=(), lesson_id="tv1_t1_b99", lesson_no=99):
    return {
        "lesson_id": lesson_id, "book": "tv1_t1_1990", "lesson_no": lesson_no, "type": "am_moi", "title": "thử",
        "source": {"pages": [1], "scan_file": "001", "verification": "page_verified"},
        "new_units": list(new_units), "images": dict(images or {}),
        "review": {"status": "chua_duyet", "notes": list(notes)},
        "part1": list(part1), "part2": list(part2),
    }


def hl_of(text, new_units):
    r = build_lesson(src_of(part1=[{"type": "unit", "text": text}], new_units=new_units))
    return r.lesson["part1"][0]["hl"]


def collect_audio_ids(node, found=None):
    """Mọi mã âm thanh (không tính instruction_audio) xuất hiện trong file bài."""
    found = set() if found is None else found
    if isinstance(node, dict):
        for key, value in node.items():
            if key in ("audio", "then_audio", "prompt_audio") and isinstance(value, str) and value:
                found.add(value)
            else:
                collect_audio_ids(value, found)
    elif isinstance(node, list):
        for item in node:
            collect_audio_ids(item, found)
    return found


class Lesson13Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = build_lesson(copy.deepcopy(SRC13))
        cls.p1 = cls.r.lesson["part1"]
        cls.p2 = cls.r.lesson["part2"]

    def test_unit(self):
        self.assertEqual(self.p1[0], {"type": "unit", "text": "u", "audio": "van_u", "hl": [{"s": 0, "n": 1}]})

    def test_keyword(self):
        p = self.p1[1]
        self.assertEqual(set(p), {"type", "text", "audio", "image", "hl"})
        self.assertEqual((p["audio"], p["hl"], p["image"]), ("tu_cais_ddu", [{"s": 5, "n": 1}], "img_b13_cais_ddu"))

    def test_analyze(self):
        rows = self.p1[2]["rows"]
        self.assertEqual([x["audio"] for x in rows], ["tu_cais_ddu", "tieng_ddu", "van_u"])
        self.assertEqual([x["hl"] for x in rows], [[{"s": 5, "n": 1}], [{"s": 1, "n": 1}], [{"s": 0, "n": 1}]])
        self.assertEqual(set(rows[0]), {"text", "audio", "hl"})

    def test_spell_then(self):
        p = self.p1[3]
        self.assertEqual(set(p), {"type", "spell", "then_text", "then_audio"})
        self.assertEqual([x["audio"] for x in p["spell"]["parts"]], ["am_dd", "van_u", "tieng_ddu"])
        self.assertEqual((p["then_text"], p["then_audio"], p["spell"]["drag_tone"]), ("cái đu", "tu_cais_ddu", False))
        self.assertEqual(p["spell"]["target"], "đu")

    def test_words(self):
        item = self.p1[4]["items"][0]
        self.assertEqual(set(self.p1[4]), {"type", "marker", "items"})
        self.assertEqual(set(item), {"text", "audio", "image", "hl", "spells"})
        self.assertEqual(item["hl"], [{"s": 1, "n": 1}, {"s": 4, "n": 1}])
        self.assertEqual([s["target"] for s in item["spells"]], ["củ", "từ"])
        self.assertEqual(item["audio"], "tu_cur_tuwf")

    def test_sentence(self):
        p = self.p1[5]
        self.assertEqual(set(p), {"type", "marker", "text", "audio", "items"})
        self.assertEqual(p["marker"], "●")
        self.assertEqual((p["audio"], [i["text"] for i in p["items"]]), ("cau_b13_01", ["má", "có", "củ", "từ"]))
        self.assertEqual([i["audio"] for i in p["items"]], ["tieng_mas", "tieng_cos", "tieng_cur", "tieng_tuwf"])
        self.assertEqual([[s["target"] for s in i["spells"]] for i in p["items"]], [["má"], ["có"], ["củ"], ["từ"]])
        self.assertEqual(set(p["items"][0]), {"text", "audio", "hl", "spells"})
        self.assertEqual(p["items"][0]["hl"], [])  # bài âm mới: câu không tô chữ mới

    def test_reading_flattened(self):
        p = self.p1[6]
        self.assertEqual(set(p), {"type", "marker", "labels", "items"})
        self.assertEqual(p["labels"], ["", ""])
        self.assertEqual(p["marker"], "⌂")
        self.assertEqual([(i["text"], i["row"]) for i in p["items"]], [("cù", 0), ("dù", 0), ("từ từ", 1)])
        self.assertEqual(p["items"][2]["audio"], "tu_tuwf_tuwf")
        self.assertEqual([s["target"] for s in p["items"][2]["spells"]], ["từ", "từ"])
        self.assertEqual(set(p["items"][0]), {"text", "audio", "row", "spells"})

    def test_part2_listen_choose(self):
        self.assertEqual(len(self.p2), 5)
        r0 = self.p2[0]
        self.assertEqual((r0["kind"], r0["answer"], r0["prompt_audio"], r0["instruction_audio"]),
                         ("listen_choose", 1, "van_u", "hd_nghe_chon_chu"))
        self.assertEqual([o["text"] for o in r0["options"]], ["ư", "u", "o"])
        self.assertEqual([o["audio"] for o in r0["options"]], ["van_uw", "van_u", "van_o"])

    def test_part2_rounds_share_tag(self):
        self.assertEqual([r["tag"] for r in self.p2], ["", "look_alike", "look_alike", "", ""])
        self.assertEqual([r["answer"] for r in self.p2[1:3]], [0, 1])

    def test_part2_compose(self):
        r = self.p2[3]
        self.assertEqual((r["kind"], r["prompt_text"], r["prompt_audio"], r["answer"]),
                         ("compose", "củ t_", "tu_cur_tuwf", 0))
        self.assertEqual((r["image"], r["instruction_audio"]), ("img_b13_cur_tuwf", "hd_keo_vao_cho_trong"))
        self.assertEqual([o["text"] for o in r["options"]], ["ừ", "ù", "à"])
        self.assertEqual(r["options"][0]["audio"], "tieng_uwf")

    def test_part2_listen_picture(self):
        r = self.p2[4]
        self.assertEqual(([o["text"] for o in r["options"]], r["answer"]), (["cái đu", "củ từ"], 1))
        self.assertEqual([o["image"] for o in r["options"]], ["img_b13_cais_ddu", "img_b13_cur_tuwf"])
        self.assertEqual((r["prompt_audio"], r["instruction_audio"]), ("tu_cur_tuwf", "hd_nghe_chon_tranh"))
        self.assertEqual([o["audio"] for o in r["options"]], ["", ""])

    def test_every_round_has_every_key(self):
        round_keys = {"kind", "tag", "instruction_audio", "prompt_audio", "prompt_text", "base_text", "image",
                      "options", "answer"}
        option_keys = {"text", "audio", "image", "tone"}
        for r in self.p2:
            self.assertEqual(set(r), round_keys)
            for o in r["options"]:
                self.assertEqual(set(o), option_keys)
        self.assertEqual(self.p2[0]["base_text"], "")
        self.assertEqual(self.p2[0]["image"], "")
        self.assertEqual(self.p2[0]["options"][0]["tone"], "")

    def test_audio_entries(self):
        self.assertEqual(self.r.audio["am_dd"], ("đờ", "am"))
        self.assertEqual(self.r.audio["cau_b13_01"], ("má có củ từ", "cau"))
        self.assertEqual(self.r.audio["van_u"], ("u", "van"))
        self.assertEqual(self.r.audio["tu_cais_ddu"], ("cái đu", "tu"))

    def test_audio_covers_every_reference_but_not_instructions(self):
        referenced = collect_audio_ids(self.r.lesson)
        self.assertEqual(referenced - set(self.r.audio), set())
        self.assertEqual(set(self.r.audio) - referenced, set())
        self.assertFalse(any(k in self.r.audio for k in SYSTEM_AUDIO))

    def test_images_only_those_referenced(self):
        self.assertEqual(self.r.images, {"img_b13_cais_ddu": SRC13["images"]["img_b13_cais_ddu"],
                                         "img_b13_cur_tuwf": SRC13["images"]["img_b13_cur_tuwf"]})

    def test_top_level(self):
        lesson = self.r.lesson
        self.assertEqual(list(lesson), ["schema", "lesson_id", "book", "lesson_no", "type", "title", "in_app", "new_units",
                                        "source", "notes", "review", "part1", "part2"])
        self.assertEqual(lesson["notes"], [])  # u, ư không có tên đọc riêng, trang không có chú thích
        self.assertEqual((lesson["schema"], lesson["lesson_id"], lesson["lesson_no"], lesson["type"]),
                         (1, "tv1_t1_b13", 13, "am_moi"))
        self.assertEqual(lesson["new_units"], ["u", "ư"])
        self.assertEqual(lesson["source"], SRC13["source"])
        self.assertIsInstance(self.r, BuildResult)

    def test_review_keeps_source_notes(self):
        self.assertEqual(self.r.lesson["review"],
                         {"status": "chua_duyet", "can_duyet": [{"where": "part1[0]", "note": "ghi chú từ nguồn"}]})

    def test_result_is_json_serializable_and_source_untouched(self):
        before = copy.deepcopy(SRC13)
        r = build_lesson(SRC13)
        json.dumps(r.lesson, ensure_ascii=False)
        self.assertEqual(SRC13, before)


class Lesson04Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = build_lesson(copy.deepcopy(SRC04))
        cls.p1 = cls.r.lesson["part1"]
        cls.p2 = cls.r.lesson["part2"]

    def test_tone_intro(self):
        self.assertEqual(self.p1[2], {"type": "tone_intro", "tone": "huyen", "text": "huyền", "glyph": HUYEN,
                                      "audio": "dau_huyen"})
        self.assertEqual(self.r.audio["dau_huyen"], ("huyền", "dau"))

    def test_tone_attach(self):
        p = self.p1[3]
        self.assertEqual(set(p), {"type", "image", "spell"})
        self.assertEqual(p["image"], "img_b04_caf")
        self.assertEqual([x["text"] for x in p["spell"]["parts"]], ["ca", HUYEN, "cà"])
        self.assertEqual([x["audio"] for x in p["spell"]["parts"]], ["tieng_ca", "dau_huyen", "tieng_caf"])
        self.assertEqual([x["kind"] for x in p["spell"]["parts"]], ["join", "tone", "join"])
        self.assertEqual(p["spell"]["parts"][1]["tone"], "huyen")
        self.assertNotIn("tone", p["spell"]["parts"][0])
        self.assertIs(p["spell"]["drag_tone"], True)
        self.assertEqual(p["spell"]["target"], "cà")
        self.assertEqual(self.r.audio["tieng_caf"], ("cà", "tieng"))
        self.assertEqual(self.r.audio["tieng_ca"], ("ca", "tieng"))

    def test_picture(self):
        self.assertEqual(self.p1[6], {"type": "picture", "image": "img_b04_mua", "audio": "hd_b04_tranh_01"})
        self.assertEqual(self.r.audio["hd_b04_tranh_01"], ("Các bạn đang múa.", "huong_dan"))

    def test_picture_adds_can_duyet_after_source_notes(self):
        self.assertEqual(self.r.lesson["review"]["can_duyet"], [
            {"where": "part1[7]", "note": "ghi chú nguồn"},
            {"where": "part1[6]", "note": "lời dẫn tranh do Claude đề xuất"},
        ])

    def test_words_without_image_or_note(self):
        item = self.p1[7]["items"][0]
        self.assertEqual(set(item), {"text", "audio", "hl", "spells"})
        self.assertEqual(item["hl"], [])
        self.assertEqual([s["target"] for s in item["spells"]], ["có", "cà"])

    def test_look_tone(self):
        r0, r1 = self.p2[0], self.p2[1]
        self.assertEqual((r0["kind"], r0["tag"], r0["prompt_text"], r0["base_text"], r0["prompt_audio"]),
                         ("look_tone", "look_alike", "cá", "ca", ""))
        self.assertEqual((r0["answer"], r1["answer"]), (1, 0))
        self.assertEqual([(o["text"], o["tone"], o["audio"], o["image"]) for o in r0["options"]],
                         [(HUYEN, "huyen", "", ""), (SAC, "sac", "", "")])
        self.assertEqual(r0["instruction_audio"], "hd_nhin_keo_dau")

    def test_listen_picture_uses_tone_attach_and_keyword_text(self):
        r = self.p2[2]
        self.assertEqual([o["text"] for o in r["options"]], ["ca", "cà", "cá"])
        self.assertEqual(r["answer"], 2)

    def test_second_picture_counts_up(self):
        src = src_of(part1=[{"type": "picture", "image": "img_b04_mua", "say": "Một."},
                            {"type": "picture", "image": "img_b04_mua", "say": "Hai."}],
                     images={"img_b04_mua": "Tranh"}, lesson_id="tv1_t1_b04", lesson_no=4)
        r = build_lesson(src)
        self.assertEqual([s["audio"] for s in r.lesson["part1"]], ["hd_b04_tranh_01", "hd_b04_tranh_02"])
        self.assertEqual([n["where"] for n in r.lesson["review"]["can_duyet"]], ["part1[0]", "part1[1]"])


class SpellStepTest(unittest.TestCase):
    def test_rime(self):
        r = build_lesson(src_of(part1=[{"type": "spell", "target": "an", "rime": True}]))
        self.assertEqual([p["audio"] for p in r.lesson["part1"][0]["spell"]["parts"]], ["van_a", "am_n", "van_an"])
        self.assertEqual(r.audio["am_n"], ("nờ", "am"))

    def test_without_rime_flag_is_syllable(self):
        r = build_lesson(src_of(part1=[{"type": "spell", "target": "an"}]))
        self.assertEqual([p["audio"] for p in r.lesson["part1"][0]["spell"]["parts"]], ["van_an"])

    def test_drag_tone_flag_and_no_then(self):
        r = build_lesson(src_of(part1=[{"type": "spell", "target": "sàn", "drag_tone": True}]))
        p = r.lesson["part1"][0]
        self.assertEqual(set(p), {"type", "spell"})
        self.assertIs(p["spell"]["drag_tone"], True)
        self.assertEqual([x["audio"] for x in p["spell"]["parts"]],
                         ["am_s", "van_an", "tieng_san", "dau_huyen", "tieng_sanf"])

    def test_ngan_adds_can_duyet(self):
        r = build_lesson(src_of(part1=[{"type": "spell", "target": "ngan"}]))
        notes = r.lesson["review"]["can_duyet"]
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["where"], "part1[0]")
        self.assertIn("ng", notes[0]["note"])

    def test_item_spell_notes_point_at_item(self):
        r = build_lesson(src_of(part1=[
            {"type": "unit", "text": "an"},
            {"type": "words", "marker": "●", "items": [{"text": "lan can"}, {"text": "đàn ngan"}]}]))
        self.assertEqual([n["where"] for n in r.lesson["review"]["can_duyet"]], ["part1[1].items[1]"])

    def test_same_note_not_repeated_within_one_item(self):
        r = build_lesson(src_of(part1=[{"type": "words", "marker": "", "items": [{"text": "ngan ngan"}]}]))
        self.assertEqual(len(r.lesson["review"]["can_duyet"]), 1)

    def test_words_spell_list_overrides_syllables(self):
        r = build_lesson(src_of(part1=[{"type": "words", "marker": "", "items": [{"text": "bàn ghế", "spell": ["bàn"]}]}]))
        item = r.lesson["part1"][0]["items"][0]
        self.assertEqual([s["target"] for s in item["spells"]], ["bàn"])

    def test_words_note_and_image(self):
        r = build_lesson(src_of(
            part1=[{"type": "words", "marker": "●", "items": [
                {"text": "đàn ngan", "image": "img_b42_ngan", "note": "ngan: vịt xiêm."}]}],
            images={"img_b42_ngan": "Đàn ngan"}))
        item = r.lesson["part1"][0]["items"][0]
        self.assertEqual((item["image"], item["note"]), ("img_b42_ngan", "ngan: vịt xiêm."))
        self.assertEqual(list(item), ["text", "audio", "image", "note", "hl", "spells"])


class HighlightTest(unittest.TestCase):
    def test_whole_syllable_wins_over_parts(self):
        self.assertEqual(hl_of("ca", ["ca", "a"]), [{"s": 0, "n": 2}])

    def test_onset(self):
        self.assertEqual(hl_of("nhà", ["nh"]), [{"s": 0, "n": 2}])

    def test_rime_keeps_tone_letter(self):
        self.assertEqual(hl_of("nhà sàn", ["an"]), [{"s": 5, "n": 2}])

    def test_rime_without_tone_matches_toned_syllable(self):
        self.assertEqual(hl_of("ừ", ["ư"]), [{"s": 0, "n": 1}])

    def test_onset_and_rime_both_new(self):
        self.assertEqual(hl_of("đu", ["đ", "u"]), [{"s": 0, "n": 1}, {"s": 1, "n": 1}])

    def test_empty_rime_span_is_skipped(self):
        self.assertEqual(hl_of("gì", ["i"]), [])

    def test_nothing_new(self):
        self.assertEqual(hl_of("lá", ["u"]), [])

    def test_consonant_unit_does_not_crash(self):
        self.assertEqual(hl_of("b", []), [])

    def test_consonant_unit_with_other_new_units(self):
        self.assertEqual(hl_of("ng", ["ngh"]), [])

    def test_consonant_unit_that_is_new_is_highlighted_whole(self):
        self.assertEqual(hl_of("b", ["b"]), [{"s": 0, "n": 1}])

    def test_analyze_row_with_consonant(self):
        r = build_lesson(src_of(part1=[{"type": "analyze", "rows": ["bê", "b"]}], new_units=["ê"]))
        rows = r.lesson["part1"][0]["rows"]
        self.assertEqual([x["audio"] for x in rows], ["tieng_bee", "am_b"])
        self.assertEqual([x["hl"] for x in rows], [[{"s": 1, "n": 1}], []])

    def test_unit_step_new_units_are_nfc(self):
        r = build_lesson(src_of(part1=[{"type": "unit", "text": unicodedata.normalize("NFD", "ư")}],
                                new_units=[unicodedata.normalize("NFD", "ư")]))
        self.assertEqual(r.lesson["part1"][0]["hl"], [{"s": 0, "n": 1}])
        self.assertEqual(r.lesson["part1"][0]["audio"], "van_uw")

    def test_only_listed_steps_have_hl(self):
        r = build_lesson(SRC13)
        for step in r.lesson["part1"]:
            self.assertEqual("hl" in step, step["type"] in ("unit", "keyword"), step["type"])


class ToneErrorTest(unittest.TestCase):
    def test_unknown_tone_in_tone_intro(self):
        with self.assertRaises(BuildError) as cm:
            build_lesson(src_of(part1=[{"type": "tone_intro", "tone": "bang"}]))
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b99 part1[0]: "))

    def test_tone_attach_target_needs_a_tone(self):
        with self.assertRaises(BuildError) as cm:
            build_lesson(src_of(part1=[{"type": "tone_attach", "target": "ca", "image": "img_x"}],
                                images={"img_x": "x"}))
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b99 part1[0]: "))


class BuildErrorTest(unittest.TestCase):
    def test_unknown_image_id(self):
        src = copy.deepcopy(SRC13)
        src["part1"][1]["image"] = "img_b13_khong_co"
        with self.assertRaises(BuildError) as cm:
            build_lesson(src)
        self.assertIn("tv1_t1_b13", str(cm.exception))
        self.assertIn("img_b13_khong_co", str(cm.exception))
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b13 part1[1]: "))

    def test_unknown_image_in_part2(self):
        src = copy.deepcopy(SRC13)
        src["part2"][2]["image"] = "img_b13_khong_co"
        with self.assertRaises(BuildError) as cm:
            build_lesson(src)
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b13 part2[2]: "))
        self.assertIn("img_b13_khong_co", str(cm.exception))

    def test_answer_not_in_options(self):
        src = copy.deepcopy(SRC13)
        src["part2"][0]["rounds"][0]["options"] = ["ư", "o"]
        with self.assertRaises(BuildError) as cm:
            build_lesson(src)
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b13 part2[0].rounds[0]: "))

    def test_listen_picture_answer_not_in_options(self):
        src = copy.deepcopy(SRC13)
        src["part2"][3]["answer"] = "img_b13_unused"
        with self.assertRaises(BuildError):
            build_lesson(src)

    def test_look_tone_model_tone_not_in_options(self):
        src = src_of(part2=[{"kind": "look_tone", "model": "cá", "options": ["huyen", "hoi"]}])
        with self.assertRaises(BuildError) as cm:
            build_lesson(src)
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b99 part2[0]: "))

    def test_look_tone_unknown_option_key(self):
        src = src_of(part2=[{"kind": "look_tone", "model": "cá", "options": ["sac", "bang"]}])
        with self.assertRaises(BuildError):
            build_lesson(src)

    def test_compose_template_does_not_make_word(self):
        src = copy.deepcopy(SRC13)
        src["part2"][2]["answer"] = "ù"
        with self.assertRaises(BuildError) as cm:
            build_lesson(src)
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b13 part2[2]: "))

    def test_listen_picture_with_wordless_picture_step(self):
        src = copy.deepcopy(SRC04)
        src["part2"][1]["rounds"][0]["options"].append("img_b04_mua")
        with self.assertRaises(BuildError) as cm:
            build_lesson(src)
        self.assertIn("img_b04_mua", str(cm.exception))
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b04 part2[1].rounds[0]: "))

    def test_listen_picture_with_unmapped_picture(self):
        src = copy.deepcopy(SRC13)
        src["part2"][3]["options"].append("img_b13_unused")
        with self.assertRaises(BuildError) as cm:
            build_lesson(src)
        self.assertIn("img_b13_unused", str(cm.exception))

    def test_unknown_step_type(self):
        with self.assertRaises(BuildError) as cm:
            build_lesson(src_of(part1=[{"type": "unit", "text": "u"}, {"type": "video"}]))
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b99 part1[1]: "))
        self.assertIn("video", str(cm.exception))

    def test_unknown_exercise_kind(self):
        with self.assertRaises(BuildError) as cm:
            build_lesson(src_of(part2=[{"kind": "memory", "rounds": []}]))
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b99 part2[0]: "))
        self.assertIn("memory", str(cm.exception))

    def test_invalid_syllable_is_wrapped_with_location(self):
        with self.assertRaises(BuildError) as cm:
            build_lesson(src_of(part1=[{"type": "keyword", "text": "ca7", "image": "img_x"}], images={"img_x": "x"}))
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b99 part1[0]: "))

    def test_invalid_syllable_in_round_is_wrapped(self):
        with self.assertRaises(BuildError) as cm:
            build_lesson(src_of(part2=[{"kind": "listen_choose", "answer": "x1", "options": ["x1"]}]))
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b99 part2[0]: "))

    def test_missing_field_names_the_field(self):
        with self.assertRaises(BuildError) as cm:
            build_lesson(src_of(part1=[{"type": "keyword", "text": "ca"}]))
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b99 part1[0]: "))
        self.assertIn("image", str(cm.exception))

    def test_reading_rows_must_be_lists(self):
        with self.assertRaises(BuildError) as cm:
            build_lesson(src_of(part1=[{"type": "reading", "marker": "⌂", "rows": ["cù", "dù"]}]))
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b99 part1[0]: "))

    def test_missing_top_level_field(self):
        src = copy.deepcopy(SRC13)
        del src["title"]
        with self.assertRaises(BuildError) as cm:
            build_lesson(src)
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b13 (đầu bài): "))
        self.assertIn("title", str(cm.exception))

    def test_lesson_no_must_be_an_integer(self):
        src = copy.deepcopy(SRC13)
        src["lesson_no"] = "13"
        with self.assertRaises(BuildError) as cm:
            build_lesson(src)
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b13 (đầu bài): "))

    def test_build_error_is_not_value_error(self):
        self.assertFalse(issubclass(BuildError, ValueError))


class AudioCollisionTest(unittest.TestCase):
    """Một mã âm thanh chỉ được có một lời đọc trong cả bài."""

    def test_spell_part_collides_with_earlier_step(self):
        # telex("xoong") == telex("xông"): "oong" và "ông" cùng mã van_oong
        with self.assertRaises(BuildError) as cm:
            build_lesson(src_of(part1=[{"type": "unit", "text": "ông"}, {"type": "spell", "target": "xoong"}]))
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b99 part1[1]: "))
        self.assertIn("van_oong", str(cm.exception))
        self.assertIn("'ông'", str(cm.exception))
        self.assertIn("'oong'", str(cm.exception))

    def test_item_audio_collides_between_two_items(self):
        src = src_of(part1=[{"type": "words", "marker": "", "items": [{"text": "xông"}, {"text": "xoong"}]}])
        with self.assertRaises(BuildError) as cm:
            build_lesson(src)
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b99 part1[0].items[1]: "))
        self.assertIn("tieng_xoong", str(cm.exception))

    def test_collision_in_part2(self):
        src = src_of(part1=[{"type": "unit", "text": "ông"}],
                     part2=[{"kind": "listen_choose", "answer": "oong", "options": ["oong", "a"]}])
        with self.assertRaises(BuildError) as cm:
            build_lesson(src)
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b99 part2[0]: "))

    def test_sentence_id_collision_is_not_overwritten(self):
        builder = _Builder(src_of(part1=[{"type": "sentence", "marker": "●", "text": "má có"}]))
        builder.audio["cau_b99_01"] = ("câu khác", "cau")
        with self.assertRaises(BuildError) as cm:
            builder.build()
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b99 part1[0]: "))
        self.assertIn("cau_b99_01", str(cm.exception))

    def test_picture_id_collision_is_not_overwritten(self):
        builder = _Builder(src_of(part1=[{"type": "picture", "image": "img_x", "say": "Lời dẫn."}],
                                  images={"img_x": "x"}))
        builder.audio["hd_b99_tranh_01"] = ("lời khác", "huong_dan")
        with self.assertRaises(BuildError) as cm:
            builder.build()
        self.assertIn("hd_b99_tranh_01", str(cm.exception))

    def test_case_and_punctuation_differences_keep_the_first(self):
        r = build_lesson(src_of(part1=[
            {"type": "words", "marker": "", "items": [{"text": "Má"}, {"text": "má"}, {"text": "má."}]},
            {"type": "sentence", "marker": "●", "text": "Má có củ từ."},
            {"type": "reading", "marker": "⌂", "rows": [["má", "Má"]]}]))
        self.assertEqual(r.audio["tieng_mas"], ("Má", "tieng"))
        self.assertEqual(r.audio["cau_b99_01"], ("Má có củ từ.", "cau"))

    def test_same_text_twice_is_fine(self):
        r = build_lesson(src_of(part1=[{"type": "unit", "text": "u"}, {"type": "unit", "text": "u"}]))
        self.assertEqual(r.audio["van_u"], ("u", "van"))


class ListenPictureAnswerTest(unittest.TestCase):
    def test_word_must_match_the_answer_picture(self):
        src = copy.deepcopy(SRC13)
        src["part2"][3]["word"] = "cái đu"  # đáp án vẫn là tranh củ từ
        with self.assertRaises(BuildError) as cm:
            build_lesson(src)
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b13 part2[3]: "))
        self.assertIn("img_b13_cur_tuwf", str(cm.exception))

    def test_mismatch_inside_rounds_names_the_round(self):
        src = copy.deepcopy(SRC04)
        src["part2"][1]["rounds"][0]["word"] = "cà"  # đáp án vẫn là tranh cá
        with self.assertRaises(BuildError) as cm:
            build_lesson(src)
        self.assertTrue(str(cm.exception).startswith("tv1_t1_b04 part2[1].rounds[0]: "))

    def test_case_only_difference_passes(self):
        src = src_of(
            part1=[{"type": "keyword", "text": "Cái ca", "image": "img_a"},
                   {"type": "keyword", "text": "cái đu", "image": "img_b"}],
            part2=[{"kind": "listen_picture", "word": "cái ca", "answer": "img_a", "options": ["img_a", "img_b"]}],
            images={"img_a": "a", "img_b": "b"})
        r = build_lesson(src)
        self.assertEqual(r.lesson["part2"][0]["answer"], 0)
        self.assertEqual(r.lesson["part2"][0]["options"][0]["text"], "Cái ca")

    def test_tone_attach_target_matches_word(self):
        r = build_lesson(copy.deepcopy(SRC04))
        self.assertEqual(r.lesson["part2"][2]["answer"], 2)

    def test_unmapped_picture_keeps_its_own_message(self):
        src = copy.deepcopy(SRC13)
        src["part2"][3]["word"] = "cái đu"  # cũng sai từ đề, nhưng tranh lạ phải báo trước
        src["part2"][3]["options"].append("img_b13_unused")
        with self.assertRaises(BuildError) as cm:
            build_lesson(src)
        self.assertIn("img_b13_unused", str(cm.exception))
        self.assertNotIn("không khớp", str(cm.exception))


class SystemAssetsTest(unittest.TestCase):
    def test_system_audio(self):
        self.assertEqual(set(SYSTEM_AUDIO), {
            "hd_nghe_chon_chu", "hd_nghe_chon_tranh", "hd_nhin_keo_dau", "hd_keo_vao_cho_trong", "hd_danh_van_theo",
            "hd_keo_dau_vao_chu", "hd_thu_lai", "khen_01", "khen_02", "khen_hoan_thanh",
            "hd_nhin_chon_chu_hoa", "hd_nghe_do_chon_tranh"})
        self.assertEqual(SYSTEM_AUDIO["hd_nghe_chon_chu"], "Con nghe rồi chọn chữ đúng nhé.")
        self.assertEqual(SYSTEM_AUDIO["khen_hoan_thanh"], "Con học xong bài rồi. Giỏi lắm!")
        self.assertTrue(all(k.isascii() and unicodedata.is_normalized("NFC", v) for k, v in SYSTEM_AUDIO.items()))

    def test_system_audio_covers_round_instructions(self):
        r = build_lesson(copy.deepcopy(SRC13))
        for round_ in r.lesson["part2"]:
            self.assertIn(round_["instruction_audio"], SYSTEM_AUDIO)
        r4 = build_lesson(copy.deepcopy(SRC04))
        for round_ in r4.lesson["part2"]:
            self.assertIn(round_["instruction_audio"], SYSTEM_AUDIO)

    def test_system_images(self):
        avatars = {f"img_chung_avatar_{n:02d}" for n in range(1, 7)}  # hình đại diện cho bé chọn (MVP Task 5)
        # Giao diện mới: hoa bé ngoan, gà con và 12 biểu tượng trên nút (hình mặc định của `ui-icons`).
        ui = {"img_chung_hoa_be_ngoan", "img_chung_ga_con"} | {
            f"img_ui_{n}" for n in ("nha", "loa", "tiep", "lui", "so", "on_lai", "xong", "khoa",
                                    "lat_truoc", "lat_sau", "sao_giay", "canh_hoa")}
        self.assertEqual(set(SYSTEM_IMAGES),
                         {"img_chung_sao", "img_chung_em_doc", "img_chung_luyen_tap"} | avatars | ui)
        self.assertIn("con mèo", SYSTEM_IMAGES["img_chung_avatar_01"])
        self.assertTrue(all(unicodedata.is_normalized("NFC", v) for v in SYSTEM_IMAGES.values()))


class FilesTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.src_dir = self.root / "src"
        self.src_dir.mkdir()

    def write_src(self, name, data):
        with open(self.src_dir / name, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def test_load_sources_sorted_and_nfc(self):
        b13 = copy.deepcopy(SRC13)
        b13["title"] = unicodedata.normalize("NFD", "u ư")
        b13["part1"][1]["text"] = unicodedata.normalize("NFD", "cái đu")
        self.write_src("b13.json", b13)
        self.write_src("b04.json", SRC04)
        (self.src_dir / "ghi_chu.txt").write_text("bỏ qua", encoding="utf-8")
        sources = load_sources(self.src_dir)
        self.assertEqual([s["lesson_id"] for s in sources], ["tv1_t1_b04", "tv1_t1_b13"])
        self.assertEqual(sources[1]["title"], "u ư")
        self.assertTrue(unicodedata.is_normalized("NFC", sources[1]["part1"][1]["text"]))
        self.assertTrue(unicodedata.is_normalized("NFC", json.dumps(sources[1], ensure_ascii=False)))

    def test_build_all_writes_lessons_and_index_sorted_by_lesson_no(self):
        self.write_src("a_b13.json", SRC13)  # tên file sắp trước nhưng số bài lớn hơn
        self.write_src("b_b04.json", SRC04)
        out = self.root / "out" / "lessons"
        results = build_all(self.src_dir, out)
        self.assertEqual(sorted(p.name for p in out.iterdir()), ["index.json", "tv1_t1_b04.json", "tv1_t1_b13.json"])
        self.assertEqual({r.lesson["lesson_id"] for r in results}, {"tv1_t1_b04", "tv1_t1_b13"})
        index = json.loads((out / "index.json").read_text(encoding="utf-8"))
        self.assertEqual(index, {"lessons": [
            {"lesson_id": "tv1_t1_b04", "lesson_no": 4, "title": "Dấu huyền - Dấu sắc", "type": "dau_thanh",
             "book": "tv1_t1_1990"},
            {"lesson_id": "tv1_t1_b13", "lesson_no": 13, "title": "u ư", "type": "am_moi", "book": "tv1_t1_1990"},
        ]})
        built = json.loads((out / "tv1_t1_b13.json").read_text(encoding="utf-8"))
        self.assertEqual(built, build_lesson(SRC13).lesson)

    def test_written_files_are_utf8_readable_indented_with_trailing_newline(self):
        self.write_src("b13.json", SRC13)
        out = self.root / "lessons"
        build_all(self.src_dir, out)
        raw = (out / "tv1_t1_b13.json").read_bytes()
        text = raw.decode("utf-8")
        self.assertIn("cái đu", text)
        self.assertNotIn("\\u", text)
        self.assertTrue(text.endswith("}\n"))
        self.assertIn('\n  "schema": 1,', text)
        self.assertNotIn(b"\r\n", raw)
        self.assertTrue((out / "index.json").read_text(encoding="utf-8").endswith("}\n"))

    def test_build_all_creates_missing_out_dir(self):
        self.write_src("b13.json", SRC13)
        out = self.root / "a" / "b" / "lessons"
        build_all(self.src_dir, out)
        self.assertTrue((out / "index.json").is_file())

    def test_duplicate_lesson_id_is_an_error(self):
        self.write_src("a.json", SRC13)
        self.write_src("b.json", SRC13)
        with self.assertRaises(BuildError) as cm:
            build_all(self.src_dir, self.root / "out")
        self.assertIn("tv1_t1_b13", str(cm.exception))

    def test_bad_json_file_names_the_file(self):
        (self.src_dir / "hong.json").write_text("{", encoding="utf-8")
        with self.assertRaises(BuildError) as cm:
            load_sources(self.src_dir)
        self.assertTrue(str(cm.exception).startswith("hong "))


class CliTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def run_cli(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_build_without_source_dir(self):
        missing = self.root / "khong_co"
        with mock.patch.object(cli, "CONTENT_SRC", missing), mock.patch.object(cli, "UNITY_RES", self.root / "res"):
            code, out, _ = self.run_cli(["build"])
        self.assertEqual(code, 1)
        self.assertIn(f"Không có nguồn bài trong {missing}", out)
        self.assertFalse((self.root / "res").exists())

    def test_build_with_empty_source_dir(self):
        src = self.root / "src"
        src.mkdir()
        with mock.patch.object(cli, "CONTENT_SRC", src), mock.patch.object(cli, "UNITY_RES", self.root / "res"):
            code, out, _ = self.run_cli(["build"])
        self.assertEqual(code, 1)
        self.assertIn("Không có nguồn bài trong", out)

    def test_build_prints_count_and_can_duyet(self):
        src = self.root / "src"
        src.mkdir()
        with open(src / "b04.json", "w", encoding="utf-8") as f:
            json.dump(SRC04, f, ensure_ascii=False)
        with mock.patch.object(cli, "CONTENT_SRC", src), mock.patch.object(cli, "UNITY_RES", self.root / "res"), \
                mock.patch.object(cli, "MANIFESTS", self.root / "manifests"):  # lệnh build cũng ghi danh mục
            code, out, _ = self.run_cli(["build"])
        self.assertEqual(code, 0)
        self.assertIn("1 bài", out)
        self.assertIn("tv1_t1_b04", out)
        self.assertIn("part1[6]", out)
        self.assertIn("lời dẫn tranh do Claude đề xuất", out)
        self.assertTrue((self.root / "res" / "lessons" / "index.json").is_file())

    def test_build_error_exits_1_with_message(self):
        src = self.root / "src"
        src.mkdir()
        bad = copy.deepcopy(SRC13)
        bad["part1"][1]["image"] = "img_b13_khong_co"
        with open(src / "b13.json", "w", encoding="utf-8") as f:
            json.dump(bad, f, ensure_ascii=False)
        with mock.patch.object(cli, "CONTENT_SRC", src), mock.patch.object(cli, "UNITY_RES", self.root / "res"):
            code, out, err = self.run_cli(["build"])
        self.assertEqual(code, 1)
        self.assertIn("img_b13_khong_co", out + err)


if __name__ == "__main__":
    unittest.main()
