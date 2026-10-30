import copy
import io
import json
import shutil
import tempfile
import unicodedata
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from tapdoc import __main__ as cli
from tapdoc import validate
from tapdoc.build import build_lesson
from tapdoc.curriculum import learned_until, load_curriculum
from tapdoc.manifest import update_audio_manifest, update_image_manifest
from tapdoc.paths import LESSON_INDEX
from tapdoc.validate import (
    Issue,
    check_files,
    check_nfc,
    check_no_scans,
    check_part1,
    check_part2,
    check_refs,
    southern_key,
    validate_all,
)
from tapdoc.viet import TONE_INFO, split_syllable, strip_tone

BOOK = "tv1_t1_1990"
CUR = load_curriculum(LESSON_INDEX)
L13 = learned_until(CUR, 13)
L5 = learned_until(CUR, 5)


# ---- hàm dựng dữ liệu nhỏ ----

def _opt(text="", audio="", image="", tone=""):
    return {"text": text, "audio": audio, "image": image, "tone": tone}


def _round(kind, **fields):
    rd = {"kind": kind, "tag": "", "instruction_audio": "hd_x", "prompt_audio": "", "prompt_text": "",
          "base_text": "", "image": "", "options": [], "answer": 0}
    rd.update(fields)
    return rd


def listen(answer, texts):
    return _round("listen_choose", prompt_audio="tieng_x",
                  options=[_opt(text=t, audio=f"tieng_{t}") for t in texts], answer=texts.index(answer))


def look_tone(model, tones):
    tone = split_syllable(model).tone
    return _round("look_tone", prompt_text=model, base_text=strip_tone(model),
                  options=[_opt(text=TONE_INFO[k][1], tone=k) for k in tones],
                  answer=tones.index(tone) if tone in tones else 0)


def compose(word, template, answer, texts, image=""):
    return _round("compose", prompt_text=template, prompt_audio="tu_x", image=image,
                  options=[_opt(text=t, audio=f"tieng_{t}") for t in texts], answer=texts.index(answer))


def picture(answer_image, images, texts=None):
    texts = texts or [image.rsplit("_", 1)[-1] for image in images]
    return _round("listen_picture", prompt_audio="tu_x",
                  options=[_opt(text=t, image=image) for t, image in zip(texts, images)],
                  answer=images.index(answer_image))


def lesson_with_rounds(rounds, lesson_no=13):
    return {"lesson_id": "tv1_t1_b13", "book": BOOK, "lesson_no": lesson_no, "part1": [], "part2": list(rounds)}


def lesson_with_steps(steps):
    return {"lesson_id": "tv1_t1_b13", "book": BOOK, "lesson_no": 13, "part1": list(steps), "part2": []}


def lesson_using_audio(audio_id):
    return lesson_with_steps([{"type": "unit", "text": "u", "audio": audio_id, "hl": []}])


def _make_dirs():
    path = Path(tempfile.mkdtemp())
    unittest.addModuleCleanup(shutil.rmtree, path, ignore_errors=True)
    return path


def assets_with(*names):
    """Thư mục `Assets` tạm chứa các file có đường dẫn tương đối đã cho."""
    assets = _make_dirs() / "Assets"
    assets.mkdir()
    for name in names:
        path = assets / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"x")
    return assets


def _spell(*audio_ids):
    return {"target": "đu", "drag_tone": False,
            "parts": [{"kind": "unit", "text": "u", "audio": a} for a in audio_ids]}


def messages(issues):
    return [i.message for i in issues]


class SouthernKeyTest(unittest.TestCase):
    def test_southern_key(self):
        self.assertEqual(southern_key("củ"), southern_key("cũ")); self.assertEqual(southern_key("dù"), southern_key("vù"))
        self.assertEqual(southern_key("giù"), southern_key("dù")); self.assertEqual(southern_key("sa"), southern_key("xa"))
        self.assertEqual(southern_key("tra"), southern_key("cha")); self.assertEqual(southern_key("lang"), southern_key("lan"))
        self.assertEqual(southern_key("các"), southern_key("cát")); self.assertNotEqual(southern_key("ca"), southern_key("cà"))

    def test_gi_with_vowel_i(self):
        self.assertEqual(southern_key("gì"), southern_key("dì"))

    def test_multi_syllable(self):
        self.assertEqual(southern_key("tra dù"), southern_key("cha vù"))
        self.assertEqual(southern_key("xa lang"), southern_key("sa lan"))
        self.assertEqual(southern_key("củ từ"), southern_key("cũ từ"))

    def test_syllable_order_and_count_matter(self):
        self.assertNotEqual(southern_key("củ từ"), southern_key("từ củ"))
        self.assertNotEqual(southern_key("củ từ"), southern_key("củ"))
        self.assertNotEqual(southern_key("a ba"), southern_key("ab a"))

    def test_case_and_punctuation_ignored(self):
        self.assertEqual(southern_key("Củ Từ"), southern_key("cũ từ"))
        self.assertEqual(southern_key("má có củ từ."), southern_key("má có cũ từ"))

    def test_other_tones_not_merged(self):
        for a, b in [("cà", "cá"), ("cạ", "cả"), ("cạ", "cà"), ("cả", "cá")]:
            self.assertNotEqual(southern_key(a), southern_key(b), (a, b))

    def test_unsplittable_token_kept_lowercased(self):
        self.assertEqual(southern_key("Đ"), southern_key("đ"))
        self.assertNotEqual(southern_key("d"), southern_key("đ"))
        self.assertEqual(southern_key("b củ"), southern_key("b cũ"))

    def test_key_is_nfc_independent(self):
        self.assertEqual(southern_key(unicodedata.normalize("NFD", "củ")), southern_key("cũ"))


def match_case(model, answer, texts):
    return _round("match_case", instruction_audio="hd_nhin_chon_chu_hoa", prompt_text=model,
                  options=[_opt(text=t) for t in texts], answer=texts.index(answer))


class SouthernConsonantTest(unittest.TestCase):
    """Review Focus 1: phụ âm đứng riêng (phương án ở bài nghe chọn chữ) cũng gộp theo giọng miền Nam."""

    def test_lone_consonants_merge(self):
        self.assertEqual(southern_key("s"), southern_key("x"))
        self.assertEqual(southern_key("d"), southern_key("gi"))
        self.assertEqual(southern_key("v"), southern_key("d"))
        self.assertEqual(southern_key("tr"), southern_key("ch"))
        self.assertEqual(southern_key("X"), southern_key("s"))
        self.assertNotEqual(southern_key("s"), southern_key("t"))
        self.assertNotEqual(southern_key("d"), southern_key("đ"))

    def test_lone_consonant_differs_from_syllable(self):
        self.assertNotEqual(southern_key("d"), southern_key("da"))
        self.assertEqual(southern_key("gì"), southern_key("dì"))

    def test_listen_round_with_s_and_x_is_rejected(self):
        issues = check_part2(lesson_with_rounds([listen("s", ["s", "x"])] * 6, lesson_no=24), learned_until(CUR, 24))
        self.assertTrue(any("giọng miền Nam" in m for m in messages(issues)))

    def test_listen_round_with_ch_and_tr_is_rejected(self):
        issues = check_part2(lesson_with_rounds([listen("tr", ["ch", "tr"])] * 6, lesson_no=34), learned_until(CUR, 34))
        self.assertTrue(any("giọng miền Nam" in m for m in messages(issues)))


class MatchCaseValidateTest(unittest.TestCase):
    def test_match_case_is_valid_and_exempt_from_southern(self):
        rounds = [match_case("s", "S", ["S", "X", "T"])] * 6
        self.assertEqual(check_part2(lesson_with_rounds(rounds, lesson_no=41), learned_until(CUR, 41)), [])

    def test_match_case_unlearned_upper_option(self):
        issues = check_part2(lesson_with_rounds([match_case("a", "A", ["A", "Q"])] * 6, lesson_no=13), L13)
        self.assertTrue(any("chưa học" in m and "'Q'" in m for m in messages(issues)))

    def test_upper_option_counts_as_learned(self):
        issues = check_part2(lesson_with_rounds([listen("Đ", ["Đ", "Ô"])] * 6), L13)
        self.assertFalse(any("chưa học" in m for m in messages(issues)))


class Part2Test(unittest.TestCase):
    def test_part2_rules(self):
        l13 = learned_until(load_curriculum(LESSON_INDEX), 13)
        issues = check_part2(lesson_with_rounds([listen("củ", ["củ", "cũ"])] * 6), l13)
        self.assertTrue(any("giọng miền Nam" in i.message for i in issues))
        self.assertEqual(check_part2(lesson_with_rounds([look_tone("cũ", ["hoi", "nga"])] * 6), l13), [])
        self.assertTrue(any("chưa học" in i.message for i in check_part2(lesson_with_rounds([listen("lá", ["lá", "má"])] * 6), l13)))
        self.assertTrue(any("6–10" in i.message for i in check_part2(lesson_with_rounds([listen("u", ["u", "ư"])] * 3), l13)))
        self.assertTrue(check_part2(lesson_with_rounds([picture("img_b20_x", ["img_b20_x", "img_b13_y"])] + [listen("u", ["u", "ư"])] * 5), l13))

    def test_clean_rounds_have_no_issues(self):
        rounds = [listen("u", ["u", "ư"])] * 2 + [
            compose("củ", "_ủ", "c", ["c", "m"]),
            picture("img_b13_x", ["img_b13_x", "img_b9_y", "img_chung_z"]),
            look_tone("cũ", ["hoi", "nga"]),
            listen("o", ["o", "u", "ư"]),
        ]
        self.assertEqual(check_part2(lesson_with_rounds(rounds), L13), [])

    def test_round_count_bounds(self):
        one = [listen("u", ["u", "ư"])]
        for count, ok in [(0, False), (5, False), (6, True), (10, True), (11, False)]:
            issues = check_part2(lesson_with_rounds(one * count), L13)
            self.assertEqual(any("6–10" in i.message for i in issues), not ok, count)

    def test_round_count_uses_en_dash(self):
        issue = check_part2(lesson_with_rounds([]), L13)[0]
        self.assertIn("6–10", issue.message)

    def test_unlearned_option_is_reported_with_position(self):
        issues = check_part2(lesson_with_rounds([listen("u", ["u", "lá"])] * 6), L13)
        unlearned = [i for i in issues if "chưa học" in i.message]
        self.assertEqual([i.where for i in unlearned], [f"part2[{n}].options[1].text" for n in range(6)])
        self.assertTrue(all("lá" in i.message for i in unlearned))

    def test_compose_unlearned_and_southern(self):
        bad = compose("củ", "_ủ", "c", ["c", "l"])
        self.assertTrue(any("chưa học" in m for m in messages(check_part2(lesson_with_rounds([bad] * 6), L13))))
        merged = compose("củ", "c_", "ủ", ["ủ", "ũ"])
        self.assertTrue(any("giọng miền Nam" in m for m in messages(check_part2(lesson_with_rounds([merged] * 6), L13))))

    def test_southern_merges_inside_listen_choose(self):
        for pair in (["dù", "vù"], ["giù", "dù"], ["trù", "chù"], ["sù", "xù"], ["củ", "cũ"], ["cát", "các"]):
            issues = check_part2(lesson_with_rounds([listen(pair[0], pair)] * 6), learned_until(CUR, 99))
            self.assertTrue(any("giọng miền Nam" in m for m in messages(issues)), pair)

    def test_southern_merge_reports_both_options(self):
        issues = check_part2(lesson_with_rounds([listen("củ", ["củ", "cũ"])] * 6), L13)
        southern = [i for i in issues if "giọng miền Nam" in i.message]
        self.assertEqual(len(southern), 6)
        self.assertEqual(southern[0].where, "part2[0].options[1].text")
        self.assertIn("củ", southern[0].message)
        self.assertIn("cũ", southern[0].message)

    def test_look_tone_is_exempt_from_southern(self):
        lesson = lesson_with_rounds([look_tone("cũ", ["hoi", "nga"])] * 6)
        self.assertFalse(any("giọng miền Nam" in m for m in messages(check_part2(lesson, L13))))

    def test_look_tone_unlearned_tone_and_model(self):
        self.assertEqual(check_part2(lesson_with_rounds([look_tone("cà", ["huyen", "sac"])] * 6, 5), L5), [])
        issues = check_part2(lesson_with_rounds([look_tone("cà", ["huyen", "hoi"])] * 6, 5), L5)
        self.assertEqual([i.where for i in issues], [f"part2[{n}].options[1].tone" for n in range(6)])
        self.assertTrue(all("chưa học" in i.message for i in issues))
        issues = check_part2(lesson_with_rounds([look_tone("cũ", ["huyen", "sac"])] * 6, 5), L5)
        self.assertTrue(any(i.where == "part2[0].prompt_text" and "chưa học" in i.message for i in issues))

    def test_listen_picture_has_no_text_check(self):
        lesson = lesson_with_rounds([picture("img_b13_x", ["img_b13_x", "img_b13_y"], ["lá", "xyz"])] * 6)
        self.assertEqual(check_part2(lesson, L13), [])

    def test_listen_picture_southern_uses_option_text(self):
        lesson = lesson_with_rounds([picture("img_b13_x", ["img_b13_x", "img_b13_y"], ["củ", "cũ"])] * 6)
        self.assertTrue(any("giọng miền Nam" in m for m in messages(check_part2(lesson, L13))))

    def test_picture_from_later_lesson(self):
        rounds = [picture("img_b13_x", ["img_b13_x", "img_b14_y"])] + [listen("u", ["u", "ư"])] * 5
        issues = check_part2(lesson_with_rounds(rounds), L13)
        self.assertEqual([i.where for i in issues], ["part2[0].options[1].image"])
        self.assertIn("chưa học", issues[0].message)
        self.assertIn("img_b14_y", issues[0].message)

    def test_picture_from_same_or_earlier_lesson_and_shared(self):
        rounds = [picture("img_b13_x", ["img_b13_x", "img_b04_y", "img_chung_z", "img_b013_w"])] \
            + [listen("u", ["u", "ư"])] * 5
        self.assertEqual(check_part2(lesson_with_rounds(rounds), L13), [])

    def test_picture_limit_follows_lesson_no(self):
        rounds = [picture("img_b13_x", ["img_b13_x", "img_b09_y"])] + [listen("u", ["u", "ư"])] * 5
        self.assertTrue(check_part2(lesson_with_rounds(rounds, 8), learned_until(CUR, 8)))

    def test_compose_picture_from_later_lesson(self):
        later = compose("củ", "_ủ", "c", ["c", "m"], image="img_b14_x")
        issues = check_part2(lesson_with_rounds([later] * 6), L13)
        self.assertEqual([i.where for i in issues], [f"part2[{n}].image" for n in range(6)])
        ok = compose("củ", "_ủ", "c", ["c", "m"], image="img_b13_x")
        self.assertEqual(check_part2(lesson_with_rounds([ok] * 6), L13), [])

    def test_answer_index_out_of_range(self):
        bad = listen("u", ["u", "ư"])
        bad["answer"] = 2
        issues = check_part2(lesson_with_rounds([bad] * 6), L13)
        self.assertEqual([i.where for i in issues], [f"part2[{n}].answer" for n in range(6)])

    def test_empty_option_text(self):
        bad = listen("u", ["u", "ư"])
        bad["options"][1]["text"] = ""
        issues = check_part2(lesson_with_rounds([bad] * 6), L13)
        self.assertEqual(len(issues), 6)
        self.assertTrue(all(i.where == f"part2[{n}].options[1].text" for n, i in enumerate(issues)))

    def test_unknown_kind(self):
        rd = listen("u", ["u", "ư"])
        rd["kind"] = "lạ"
        issues = check_part2(lesson_with_rounds([rd] * 6), L13)
        self.assertEqual([i.where for i in issues], [f"part2[{n}]" for n in range(6)])

    def test_issue_carries_lesson_id(self):
        issues = check_part2(lesson_with_rounds([]), L13)
        self.assertEqual(issues, [Issue("tv1_t1_b13", "part2", issues[0].message)])


class Part1Test(unittest.TestCase):
    def test_empty_spell_parts_in_step(self):
        lesson = lesson_with_steps([
            {"type": "spell", "spell": {"target": "an", "drag_tone": False, "parts": []}},
            {"type": "spell", "spell": _spell("van_u")},
        ])
        issues = check_part1(lesson)
        self.assertEqual([i.where for i in issues], ["part1[0].spell"])
        self.assertEqual(issues[0].lesson, "tv1_t1_b13")
        self.assertIn("đánh vần rỗng (chưa có quy tắc) — xem can_duyet", issues[0].message)

    def test_empty_spell_parts_in_items(self):
        lesson = lesson_with_steps([
            {"type": "words", "marker": "", "items": [
                {"text": "an", "audio": "van_an", "hl": [], "spells": [_spell("van_u"), _spell()]}]},
            {"type": "sentence", "marker": "●", "text": "an", "audio": "cau_b13_01", "items": [
                {"text": "an", "audio": "van_an", "spells": [_spell()]}]},
            {"type": "reading", "marker": "", "items": [
                {"text": "an", "audio": "van_an", "row": 0, "spells": [_spell(), _spell("van_u")]}]},
            {"type": "tone_attach", "image": "img_b13_x", "spell": _spell()},
        ])
        self.assertEqual([i.where for i in check_part1(lesson)],
                         ["part1[0].items[0].spells[1]", "part1[1].items[0].spells[0]",
                          "part1[2].items[0].spells[0]", "part1[3].spell"])

    def test_non_empty_spells_are_fine(self):
        lesson = lesson_with_steps([
            {"type": "spell", "spell": _spell("van_u")},
            {"type": "words", "marker": "", "items": [{"text": "u", "audio": "van_u", "hl": [], "spells": []}]},
        ])
        self.assertEqual(check_part1(lesson), [])

    def test_valid_markers(self):
        for marker in ("", "●", "⌂", "●▨"):
            lesson = lesson_with_steps([{"type": "words", "marker": marker, "items": []}])
            self.assertEqual(check_part1(lesson), [], repr(marker))

    def test_bad_marker(self):
        steps = [
            {"type": "words", "marker": "★", "items": []},
            {"type": "reading", "marker": "●", "items": []},
            {"type": "sentence", "marker": "▨●", "text": "", "audio": "", "items": []},
            {"type": "words", "marker": " ", "items": []},
        ]
        issues = check_part1(lesson_with_steps(steps))
        self.assertEqual([i.where for i in issues], ["part1[0].marker", "part1[2].marker", "part1[3].marker"])
        self.assertIn("ký hiệu", issues[0].message)
        self.assertIn("★", issues[0].message)

    def test_steps_without_marker_are_fine(self):
        lesson = lesson_with_steps([{"type": "unit", "text": "u", "audio": "van_u", "hl": []}])
        self.assertEqual(check_part1(lesson), [])


class NfcRefsFilesScansTest(unittest.TestCase):
    def test_nfc_refs_files_scans(self):
        empty_res = _make_dirs()
        self.assertTrue(check_nfc({"lesson_id": "x", "title": unicodedata.normalize("NFD", "cử"), "part1": [], "part2": []}))
        self.assertTrue(check_refs(lesson_using_audio("tieng_khong_co"), {"am_dd"}, set()))
        self.assertTrue(check_files([{"id": "am_dd", "file": "audio/am_dd.mp3"}], empty_res))
        for name, bad in [("Foo/010_Trang_18.jpg", True), ("Content/Resources/images/img_b13_a.png", False),
                          ("Content/Resources/images/random.png", True)]:
            self.assertEqual(bool(check_no_scans(assets_with(name))), bad, name)


class NfcTest(unittest.TestCase):
    def test_clean_lesson(self):
        self.assertEqual(check_nfc({"lesson_id": "x", "title": "cử", "part1": [{"text": "đu"}], "part2": []}), [])

    def test_path_of_nested_value(self):
        nfd = unicodedata.normalize("NFD", "cử")
        lesson = {"lesson_id": "x", "title": "u ư",
                  "part1": [{"type": "unit", "text": "u"}, {"type": "words", "items": [{"text": "a"}, {"text": nfd}]}],
                  "part2": [{"options": [{"text": nfd}]}]}
        issues = check_nfc(lesson)
        self.assertEqual([i.where for i in issues],
                         ["part1[1].items[1].text", "part2[0].options[0].text"])
        self.assertTrue(all(i.lesson == "x" for i in issues))
        self.assertTrue(all("NFC" in i.message for i in issues))

    def test_top_level_value(self):
        nfd = unicodedata.normalize("NFD", "cử")
        issues = check_nfc({"lesson_id": "x", "title": nfd})
        self.assertEqual([i.where for i in issues], ["title"])

    def test_keys_are_checked_too(self):
        nfd = unicodedata.normalize("NFD", "cử")
        issues = check_nfc({"lesson_id": "x", "part1": [{nfd: "u"}]})
        self.assertEqual([i.where for i in issues], [f"part1[0].{nfd}"])

    def test_non_string_values_are_ignored(self):
        self.assertEqual(check_nfc({"lesson_id": "x", "lesson_no": 13, "ok": True, "none": None, "x": 1.5}), [])


def _everything_lesson():
    """Một bài dùng mã âm thanh/tranh ở mọi chỗ có thể; mã tên theo vị trí của nó."""
    def spell(tag):
        return {"target": "đu", "drag_tone": False, "parts": [{"kind": "unit", "text": "đ", "audio": f"a_{tag}"}]}
    return {
        "lesson_id": "x",
        "part1": [
            {"type": "unit", "text": "u", "audio": "a_unit", "hl": []},
            {"type": "keyword", "text": "cái đu", "audio": "a_kw", "image": "i_kw", "hl": []},
            {"type": "analyze", "rows": [{"text": "u", "audio": "a_row", "hl": []}]},
            {"type": "spell", "spell": spell("sp"), "then_text": "đu", "then_audio": "a_then"},
            {"type": "tone_intro", "tone": "sac", "text": "sắc", "glyph": "ˊ", "audio": "a_tone"},
            {"type": "tone_attach", "image": "i_ta", "spell": spell("ta")},
            {"type": "picture", "image": "i_pic", "audio": "a_pic"},
            {"type": "words", "marker": "", "items": [
                {"text": "củ", "audio": "a_w", "image": "i_w", "hl": [], "spells": [spell("ws")]}]},
            {"type": "reading", "marker": "", "items": [{"text": "cù", "audio": "a_r", "row": 0, "spells": [spell("rs")]}]},
            {"type": "sentence", "marker": "", "text": "má", "audio": "a_s", "items": [
                {"text": "má", "audio": "a_si", "spells": [spell("ss")]}]},
        ],
        "part2": [
            _round("compose", instruction_audio="a_ins", prompt_audio="a_prompt", image="i_cmp",
                   options=[_opt(text="u", audio="a_opt", image="i_opt")]),
        ],
    }


EVERYTHING_AUDIO = {
    "part1[0].audio": "a_unit", "part1[1].audio": "a_kw", "part1[2].rows[0].audio": "a_row",
    "part1[3].spell.parts[0].audio": "a_sp", "part1[3].then_audio": "a_then", "part1[4].audio": "a_tone",
    "part1[5].spell.parts[0].audio": "a_ta", "part1[6].audio": "a_pic", "part1[7].items[0].audio": "a_w",
    "part1[7].items[0].spells[0].parts[0].audio": "a_ws", "part1[8].items[0].audio": "a_r",
    "part1[8].items[0].spells[0].parts[0].audio": "a_rs", "part1[9].audio": "a_s",
    "part1[9].items[0].audio": "a_si", "part1[9].items[0].spells[0].parts[0].audio": "a_ss",
    "part2[0].instruction_audio": "a_ins", "part2[0].prompt_audio": "a_prompt", "part2[0].options[0].audio": "a_opt",
}
EVERYTHING_IMAGES = {
    "part1[1].image": "i_kw", "part1[5].image": "i_ta", "part1[6].image": "i_pic", "part1[7].items[0].image": "i_w",
    "part2[0].image": "i_cmp", "part2[0].options[0].image": "i_opt",
}


class RefsTest(unittest.TestCase):
    def test_every_reference_is_checked(self):
        issues = check_refs(_everything_lesson(), set(), set())
        self.assertEqual({i.where for i in issues}, set(EVERYTHING_AUDIO) | set(EVERYTHING_IMAGES))
        by_where = {i.where: i for i in issues}
        for where, audio_id in EVERYTHING_AUDIO.items():
            self.assertIn(audio_id, by_where[where].message, where)
        for where, image_id in EVERYTHING_IMAGES.items():
            self.assertIn(image_id, by_where[where].message, where)
        self.assertTrue(all(i.lesson == "x" for i in issues))

    def test_all_present_is_clean(self):
        self.assertEqual(check_refs(_everything_lesson(), set(EVERYTHING_AUDIO.values()),
                                    set(EVERYTHING_IMAGES.values())), [])

    def test_missing_audio_and_image_are_told_apart(self):
        issues = check_refs(_everything_lesson(), set(EVERYTHING_AUDIO.values()), set())
        self.assertEqual({i.where for i in issues}, set(EVERYTHING_IMAGES))
        self.assertTrue(all("tranh" in i.message for i in issues))
        issues = check_refs(_everything_lesson(), set(), set(EVERYTHING_IMAGES.values()))
        self.assertEqual({i.where for i in issues}, set(EVERYTHING_AUDIO))
        self.assertTrue(all("âm thanh" in i.message for i in issues))

    def test_empty_round_and_option_references_are_not_flagged(self):
        lesson = lesson_with_rounds([listen("u", ["u", "ư"])])
        lesson["part2"][0]["prompt_audio"] = ""
        lesson["part2"][0]["options"][0]["audio"] = ""
        self.assertEqual(check_refs(lesson, {"hd_x", "tieng_ư"}, set()), [])

    def test_empty_step_image_is_not_flagged(self):
        lesson = lesson_with_steps([{"type": "words", "marker": "", "items": [
            {"text": "u", "audio": "van_u", "image": "", "hl": [], "spells": []}]}])
        self.assertEqual(check_refs(lesson, {"van_u"}, set()), [])

    def test_empty_step_audio_is_flagged(self):
        issues = check_refs(lesson_using_audio(""), {"van_u"}, set())
        self.assertEqual([i.where for i in issues], ["part1[0].audio"])

    def test_accepts_any_container(self):
        self.assertEqual(check_refs(lesson_using_audio("van_u"), ["van_u"], ()), [])


class FilesTest(unittest.TestCase):
    def test_existing_and_missing(self):
        res = _make_dirs()
        (res / "audio").mkdir()
        (res / "audio" / "am_dd.mp3").write_bytes(b"x")
        rows = [{"id": "am_dd", "file": "audio/am_dd.mp3"}, {"id": "am_k", "file": "audio/am_k.mp3"}]
        issues = check_files(rows, res)
        self.assertEqual([(i.lesson, i.where) for i in issues], [("-", "am_k")])
        self.assertIn("audio/am_k.mp3", issues[0].message)

    def test_row_without_file_field(self):
        issues = check_files([{"id": "am_dd"}], _make_dirs())
        self.assertEqual([i.where for i in issues], ["am_dd"])

    def test_no_rows(self):
        self.assertEqual(check_files([], _make_dirs()), [])


class ScansTest(unittest.TestCase):
    def flagged(self, *names):
        return check_no_scans(assets_with(*names))

    def test_jpg_anywhere_any_case(self):
        for name in ("a.jpg", "x/y/b.JPG", "x/c.jpeg", "d.JPEG", "Content/Resources/images/img_b13_a.jpg"):
            self.assertEqual(len(self.flagged(name)), 1, name)

    def test_scan_names(self):
        for name in ("x/page_Trang_18.png", "x/TRANG_05.png", "y/thuongmaitruongxua_01.png", "z/ThuongMaiTruongXua.pdf"):
            self.assertEqual(len(self.flagged(name)), 1, name)

    def test_png_images_dir_rules(self):
        self.assertEqual(self.flagged("Content/Resources/images/img_b13_a.png"), [])
        self.assertEqual(len(self.flagged("Content/Resources/images/random.png")), 1)
        self.assertEqual(len(self.flagged("Content/Resources/images/Img_b13_a.png")), 1)

    def test_meta_files_ignored_in_images_dir(self):
        self.assertEqual(self.flagged("Content/Resources/images/random.png.meta"), [])
        self.assertEqual(self.flagged("Content/Resources/images/img_b13_a.png", "Content/Resources/images/img_b13_a.png.meta"), [])

    def test_other_dirs_are_free(self):
        self.assertEqual(self.flagged("Content/Resources/audio/am_dd.mp3", "Scripts/Foo.cs", "Content/Resources/fonts/Andika.ttf"), [])

    def test_one_issue_per_file(self):
        issues = self.flagged("Content/Resources/images/Trang_18.jpg")
        self.assertEqual(len(issues), 1)
        self.assertEqual((issues[0].lesson, issues[0].where), ("-", "Content/Resources/images/Trang_18.jpg"))

    def test_where_is_relative_posix_path_and_sorted(self):
        issues = self.flagged("b/y.jpg", "a/x.jpg", "a/w.jpeg")
        self.assertEqual([i.where for i in issues], ["a/w.jpeg", "a/x.jpg", "b/y.jpg"])

    def test_missing_assets_dir(self):
        self.assertEqual(check_no_scans(_make_dirs() / "khong_co"), [])


# ---- validate_all với dữ liệu tạm ----

SRC = {
    "lesson_id": "tv1_t1_b13", "book": BOOK, "lesson_no": 13, "type": "am_moi", "title": "u ư",
    "source": {"pages": [18], "scan_file": "010", "verification": "page_verified"},
    "new_units": ["u", "ư"],
    "images": {
        "img_b13_cais_ddu": "Bé gái ngồi trên ván đu, hai tay nắm hai sợi dây đu",
        "img_b13_cur_tuwf": "Một củ từ (khoai từ) vỏ sần, có vài rễ con",
    },
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
        {"kind": "listen_choose", "rounds": [{"answer": "u", "options": ["ư", "u", "o"]},
                                             {"answer": "ư", "options": ["ư", "o"]}]},
        {"kind": "listen_choose", "tag": "look_alike",
         "rounds": [{"answer": "u", "options": ["u", "ư"]}, {"answer": "ư", "options": ["u", "ư"]}]},
        {"kind": "compose", "word": "củ từ", "template": "củ t_", "answer": "ừ", "options": ["ừ", "ù", "à"],
         "image": "img_b13_cur_tuwf"},
        {"kind": "listen_picture", "word": "củ từ", "answer": "img_b13_cur_tuwf",
         "options": ["img_b13_cais_ddu", "img_b13_cur_tuwf"]},
    ],
}

CSV_ROWS = [
    ("tv1_t1_1990", 1, "am_moi", "o"), ("tv1_t1_1990", 2, "am_moi", "c"), ("tv1_t1_1990", 3, "am_moi", "a"),
    ("tv1_t1_1990", 4, "dau_thanh", "dấu huyền; dấu sắc"), ("tv1_t1_1990", 5, "am_moi", "d; đ"),
    ("tv1_t1_1990", 6, "dau_thanh", "dấu hỏi; dấu ngã; dấu nặng"), ("tv1_t1_1990", 8, "am_moi", "ô; ơ"),
    ("tv1_t1_1990", 10, "am_moi", "i; t"), ("tv1_t1_1990", 12, "am_moi", "n; m"),
    ("tv1_t1_1990", 13, "am_moi", "u; ư"), ("tv1_t1_1990", 15, "am_moi", "l"),
]


class ValidateAllTest(unittest.TestCase):
    def setUp(self):
        root = _make_dirs()
        self.assets = root / "unity" / "Assets"
        self.res = self.assets / "Content" / "Resources"
        self.lessons = self.res / "lessons"
        self.manifests = root / "content" / "manifests"
        self.csv = root / "LESSON_INDEX.csv"
        lines = ["book_id,bai_so,loai_bai,noi_dung_chinh"] + [f"{b},{n},{k},{c}" for b, n, k, c in CSV_ROWS]
        self.csv.write_text("\n".join(lines) + "\n", encoding="utf-8")
        for name, value in (("UNITY_ASSETS", self.assets), ("UNITY_RES", self.res),
                            ("MANIFESTS", self.manifests), ("LESSON_INDEX", self.csv)):
            patcher = mock.patch.object(validate, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        # Tiếng động thật chưa chọn file (giay_phep rỗng): bài kiểm tra dùng một mã CC0 giả.
        patcher = mock.patch.object(validate, "SYSTEM_SFX", {"sfx_cham": {"mo_ta": "", "nguon": "", "giay_phep": "CC0"}})
        patcher.start()
        self.addCleanup(patcher.stop)

    def write_json(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def build_all_good(self, src=None):
        """Dựng bài mẫu, ghi file bài, hai danh mục và mọi file âm thanh/tranh mà danh mục đòi."""
        result = build_lesson(copy.deepcopy(src or SRC))
        self.lesson_path = self.lessons / f"{result.lesson['lesson_id']}.json"
        self.write_json(self.lesson_path, result.lesson)
        self.write_json(self.lessons / "index.json", {"lessons": [
            {"lesson_id": result.lesson["lesson_id"], "lesson_no": result.lesson["lesson_no"],
             "title": result.lesson["title"], "type": result.lesson["type"]}]})
        self.audio_rows = update_audio_manifest([result], [], self.res / "audio")
        self.image_rows = update_image_manifest([result], [], self.res / "images")
        self.write_json(self.manifests / "audio_manifest.json", self.audio_rows)
        self.write_json(self.manifests / "image_manifest.json", self.image_rows)
        for row in self.audio_rows + self.image_rows:
            path = self.res / row["file"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"x")
        (self.res / "sfx").mkdir(parents=True, exist_ok=True)
        (self.res / "sfx" / "sfx_cham.ogg").write_bytes(b"x")
        return result

    def test_built_lesson_with_files_is_clean(self):
        self.build_all_good()
        self.assertEqual(validate_all(), [])

    def test_no_lessons_dir(self):
        issues = validate_all()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].lesson, "-")
        self.assertEqual(issues[0].message, "chưa có bài nào được dựng — chạy build trước")

    def test_only_index_json_counts_as_no_lessons(self):
        self.write_json(self.lessons / "index.json", {"lessons": []})
        issues = validate_all()
        self.assertEqual(messages(issues), ["chưa có bài nào được dựng — chạy build trước"])
        self.assertEqual(messages(validate_all(allow_missing=True)), messages(issues))

    def test_no_lessons_reports_only_that_issue(self):
        assets_jpg = self.assets / "Foo" / "Trang_1.jpg"
        assets_jpg.parent.mkdir(parents=True)
        assets_jpg.write_bytes(b"x")
        self.assertEqual(len(validate_all()), 1)

    def test_missing_files_flagged_unless_allowed(self):
        self.build_all_good()
        (self.res / "audio" / "van_u.mp3").unlink()
        next(self.res.joinpath("images").glob("img_b13_cur_*.png")).unlink()
        issues = validate_all()
        self.assertEqual({i.where for i in issues}, {"van_u", "img_b13_cur_tuwf"})
        self.assertTrue(all(i.lesson == "-" and "không có file" in i.message for i in issues))
        self.assertEqual(validate_all(allow_missing=True), [])

    def test_missing_manifests_make_refs_fail(self):
        self.build_all_good()
        (self.manifests / "audio_manifest.json").unlink()
        (self.manifests / "image_manifest.json").unlink()
        issues = validate_all(allow_missing=True)
        self.assertTrue(issues)
        self.assertTrue(all(i.lesson == "tv1_t1_b13" for i in issues))
        self.assertTrue(any("không có trong danh mục" in i.message for i in issues))

    def test_lesson_checks_use_lesson_no_and_book(self):
        self.build_all_good()
        data = json.loads(self.lesson_path.read_text(encoding="utf-8"))
        data["lesson_no"] = 5
        self.write_json(self.lesson_path, data)
        issues = validate_all()
        self.assertTrue(any("chưa học" in i.message for i in issues))
        self.assertTrue(all(i.lesson == "tv1_t1_b13" for i in issues))
        self.assertTrue(all(i.where.startswith("part2") for i in issues))

    def test_issue_order_lessons_then_manifest_files_then_scans(self):
        self.build_all_good()
        data = json.loads(self.lesson_path.read_text(encoding="utf-8"))
        data["title"] = unicodedata.normalize("NFD", "u ư")
        data["part1"][5]["marker"] = "★"
        self.write_json(self.lesson_path, data)
        (self.res / "audio" / "van_u.mp3").unlink()
        scan = self.assets / "Foo" / "010_Trang_18.jpg"
        scan.parent.mkdir(parents=True)
        scan.write_bytes(b"x")
        issues = validate_all()
        self.assertEqual([i.lesson for i in issues], ["tv1_t1_b13", "tv1_t1_b13", "-", "-"])
        self.assertEqual([i.where for i in issues], ["title", "part1[5].marker", "van_u", "Foo/010_Trang_18.jpg"])

    def test_issues_are_grouped_lesson_by_lesson(self):
        self.build_all_good()
        second = json.loads(self.lesson_path.read_text(encoding="utf-8"))
        second["lesson_id"] = "tv1_t1_b13_copy"
        second["title"] = unicodedata.normalize("NFD", "ư")
        self.write_json(self.lessons / "tv1_t1_b13_copy.json", second)
        first = json.loads(self.lesson_path.read_text(encoding="utf-8"))
        first["part1"][0]["marker"] = "★"
        self.write_json(self.lesson_path, first)
        issues = validate_all()
        self.assertEqual([(i.lesson, i.where) for i in issues],
                         [("tv1_t1_b13", "part1[0].marker"), ("tv1_t1_b13_copy", "title")])

    def test_empty_spell_and_marker_rulings_via_validate_all(self):
        self.build_all_good()
        data = json.loads(self.lesson_path.read_text(encoding="utf-8"))
        data["part1"][3]["spell"]["parts"] = []
        data["part1"][4]["marker"] = "?"
        self.write_json(self.lesson_path, data)
        issues = validate_all(allow_missing=True)
        self.assertEqual([i.where for i in issues], ["part1[3].spell", "part1[4].marker"])

    def test_unreadable_lesson_json_is_an_issue(self):
        self.build_all_good()
        (self.lessons / "hong.json").write_text("{ không phải json", encoding="utf-8")
        issues = validate_all()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].lesson, "hong")
        self.assertIn("không đọc được", issues[0].message)

    def test_lesson_json_that_is_not_an_object_is_an_issue(self):
        self.build_all_good()
        self.write_json(self.lessons / "mang.json", [1, 2])
        issues = validate_all()
        self.assertEqual([i.lesson for i in issues], ["mang"])

    def test_lesson_missing_book_or_number_is_an_issue(self):
        self.build_all_good()
        data = json.loads(self.lesson_path.read_text(encoding="utf-8"))
        del data["book"]
        self.write_json(self.lesson_path, data)
        issues = validate_all()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].lesson, "tv1_t1_b13")
        self.assertIn("book", issues[0].message)

    def test_unknown_book_is_one_issue(self):
        self.build_all_good()
        data = json.loads(self.lesson_path.read_text(encoding="utf-8"))
        data["book"] = "sach_la"
        self.write_json(self.lesson_path, data)
        issues = validate_all()
        self.assertEqual(len(issues), 1)
        self.assertIn("sach_la", issues[0].message)

    def test_bad_manifest_is_an_issue_not_a_crash(self):
        self.build_all_good()
        (self.manifests / "audio_manifest.json").write_text("{ hỏng", encoding="utf-8")
        issues = validate_all(allow_missing=True)
        self.assertTrue(any(i.lesson == "-" and i.where == "audio_manifest.json" for i in issues))


class ReleaseTest(ValidateAllTest):
    """`validate --release`: bài trong app phải đã duyệt; âm thanh/tranh không còn `chua_co`, `cho_duyet`."""

    def set_status(self, lesson_status=None, row_status="dat", bad_ids=()):
        if lesson_status is not None:
            lesson = json.loads(self.lesson_path.read_text(encoding="utf-8"))
            lesson["review"]["status"] = lesson_status
            self.write_json(self.lesson_path, lesson)
        for rows, name in ((self.audio_rows, "audio_manifest.json"), (self.image_rows, "image_manifest.json")):
            for row in rows:
                row["status"] = "khong_dat" if row["id"] in bad_ids else row_status
            self.write_json(self.manifests / name, rows)

    def test_release_accepts_reviewed_lesson_and_assets(self):
        self.build_all_good()
        self.set_status("da_duyet", "dat", bad_ids=(self.audio_rows[0]["id"],))  # khong_dat vẫn dùng tạm
        self.assertEqual(validate_all(release=True), [])

    def test_release_rejects_unreviewed(self):
        self.build_all_good()
        self.set_status("chua_duyet", "dat")
        issues = validate_all(release=True)
        self.assertEqual([(i.lesson, i.where) for i in issues], [("tv1_t1_b13", "review.status")])
        self.assertIn("chưa duyệt", issues[0].message)
        self.assertEqual(validate_all(), [])  # không --release thì không kiểm tra

    def test_release_ignores_lesson_not_in_app(self):
        src = copy.deepcopy(SRC)
        src["in_app"] = False
        self.build_all_good(src)
        self.set_status("chua_duyet", "dat")
        self.assertEqual(validate_all(release=True), [])

    def test_release_rejects_pending_assets(self):
        self.build_all_good()
        self.set_status("da_duyet", "cho_duyet")
        issues = validate_all(release=True)
        self.assertEqual(len(issues), len(self.audio_rows) + len(self.image_rows))
        self.assertTrue(all(i.lesson == "-" and "cho_duyet" in i.message for i in issues))

    def test_release_rejects_missing_assets(self):
        self.build_all_good()
        self.set_status("da_duyet", "dat")
        self.audio_rows[0]["status"] = "chua_co"
        self.write_json(self.manifests / "audio_manifest.json", self.audio_rows)
        issues = validate_all(release=True)
        self.assertEqual([i.where for i in issues], [self.audio_rows[0]["id"]])
        self.assertIn("chua_co", issues[0].message)


class CliTest(unittest.TestCase):
    def test_release_warns_on_edge_source_without_error(self):
        rows = [{"id": "am_b", "source": "tts_edge_hoaimy", "status": "dat"},
                {"id": "am_c", "source": "azure", "status": "dat"}]
        warnings = validate.release_warnings(rows)
        self.assertEqual(len(warnings), 1)
        self.assertIn("am_b", warnings[0])
        self.assertEqual(validate.check_release_rows(rows, "âm thanh"), [])
        many = [{"id": f"am_{i}", "source": "tts_edge_hoaimy", "status": "dat"} for i in range(500)]
        summary = validate.release_warnings(many)
        self.assertEqual(len(summary), 1)  # một dòng tóm tắt, không in 500 dòng
        self.assertIn("500", summary[0])
        out = io.StringIO()
        with mock.patch.object(cli, "validate_all", return_value=[]), \
                mock.patch.object(cli, "load_rows", return_value=rows), redirect_stdout(out):
            code = cli.main(["validate", "--release"])
        self.assertEqual(code, 0)
        self.assertIn("Cảnh báo:", out.getvalue())
        self.assertIn("OK", out.getvalue())

    def run_cli(self, issues, argv=("validate",)):
        out = io.StringIO()
        with mock.patch.object(cli, "validate_all", return_value=issues) as fake, redirect_stdout(out):
            code = cli.main(list(argv))
        return code, out.getvalue().splitlines(), fake

    def test_ok(self):
        code, lines, fake = self.run_cli([])
        self.assertEqual((code, lines), (0, ["OK"]))
        fake.assert_called_once_with(allow_missing=False, release=False)

    def test_issues(self):
        issues = [Issue("tv1_t1_b13", "part2[3]", "chưa học"), Issue("-", "am_dd", "không có file audio/am_dd.mp3")]
        code, lines, _ = self.run_cli(issues)
        self.assertEqual(code, 1)
        self.assertEqual(lines, ["tv1_t1_b13 part2[3]: chưa học", "- am_dd: không có file audio/am_dd.mp3", "2 lỗi"])

    def test_allow_missing_flag(self):
        _, _, fake = self.run_cli([], ("validate", "--allow-missing"))
        fake.assert_called_once_with(allow_missing=True, release=False)

    def test_release_flag(self):
        _, _, fake = self.run_cli([], ("validate", "--release"))
        fake.assert_called_once_with(allow_missing=False, release=True)

    def test_control_characters_in_file_names_are_escaped(self):
        code, lines, _ = self.run_cli([Issue("-", "a\x1b[2Jb.jpg", "ảnh scan")])
        self.assertEqual(code, 1)
        self.assertNotIn("\x1b", "".join(lines))


if __name__ == "__main__":
    unittest.main()


class SfxCheckTest(unittest.TestCase):
    """Tiếng động: mỗi mã trong `SYSTEM_SFX` có đúng một file ở `sfx/`, giấy phép CC0."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.res = Path(self._tmp.name)
        (self.res / "sfx").mkdir()
        self.registry = {"sfx_cham": {"mo_ta": "tách", "nguon": "Kenney", "giay_phep": "CC0"}}

    def tearDown(self):
        self._tmp.cleanup()

    def check(self, allow_missing=False):
        with mock.patch.object(validate, "SYSTEM_SFX", self.registry):
            return validate.check_sfx(self.res, allow_missing)

    def test_ok_with_one_cc0_file(self):
        (self.res / "sfx" / "sfx_cham.ogg").write_bytes(b"o")
        self.assertEqual(self.check(), [])

    def test_missing_file_reported_unless_allowed(self):
        issues = self.check()
        self.assertEqual([i.where for i in issues], ["sfx_cham"])
        self.assertEqual(self.check(allow_missing=True), [])

    def test_non_cc0_reported(self):
        (self.res / "sfx" / "sfx_cham.wav").write_bytes(b"w")
        self.registry["sfx_cham"]["giay_phep"] = "CC-BY"
        issues = self.check()
        self.assertEqual(len(issues), 1)
        self.assertIn("CC0", issues[0].message)

    def test_two_formats_same_id_reported(self):
        (self.res / "sfx" / "sfx_cham.ogg").write_bytes(b"o")
        (self.res / "sfx" / "sfx_cham.wav").write_bytes(b"w")
        self.assertEqual(len(self.check()), 1)


class SfxSeparationTest(unittest.TestCase):
    """Tiếng động tách hẳn khỏi âm thanh phát âm: không lẫn thư mục, danh mục hay mã."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.res = Path(self._tmp.name)
        (self.res / "audio").mkdir()
        (self.res / "sfx").mkdir()
        (self.res / "audio" / "tieng_ca.mp3").write_bytes(b"a")
        (self.res / "audio" / "tieng_ca.mp3.meta").write_bytes(b"m")
        (self.res / "sfx" / "sfx_cham.ogg").write_bytes(b"o")
        (self.res / "sfx" / "sfx_cham.ogg.meta").write_bytes(b"m")
        self.rows = [{"id": "tieng_ca"}]
        self.sfx = {"sfx_cham": {"mo_ta": "tách", "nguon": "", "giay_phep": ""}}
        self.audio = {"khen_01": "Đúng rồi!"}

    def tearDown(self):
        self._tmp.cleanup()

    def check(self):
        with mock.patch.object(validate, "SYSTEM_SFX", self.sfx), \
                mock.patch.object(validate, "SYSTEM_AUDIO", self.audio):
            return validate.check_sfx_separation(self.res, self.rows)

    def test_clean_layout_ok(self):
        self.assertEqual(self.check(), [])

    def test_sfx_file_in_audio_dir_reported(self):
        (self.res / "audio" / "sfx_cham.mp3").write_bytes(b"a")
        self.assertEqual(len(self.check()), 1)

    def test_sfx_id_in_audio_manifest_reported(self):
        self.rows.append({"id": "sfx_dung"})
        self.assertEqual(len(self.check()), 1)

    def test_unknown_file_in_sfx_dir_reported(self):
        (self.res / "sfx" / "tieng_ca.ogg").write_bytes(b"o")
        self.assertEqual(len(self.check()), 1)

    def test_registry_without_prefix_reported(self):
        self.sfx["cham"] = {"mo_ta": "", "nguon": "", "giay_phep": ""}
        self.assertEqual(len(self.check()), 1)

    def test_speech_registry_with_sfx_prefix_reported(self):
        self.audio["sfx_khen"] = "Giỏi lắm!"
        self.assertEqual(len(self.check()), 1)

    def test_registries_keep_prefixes(self):
        from tapdoc.system_assets import SYSTEM_AUDIO, SYSTEM_SFX
        self.assertEqual(len(SYSTEM_SFX), 6)
        self.assertTrue(all(v["giay_phep"] == "CC0" for v in SYSTEM_SFX.values()))
        self.assertTrue(all(k.startswith("sfx_") for k in SYSTEM_SFX))
        self.assertFalse(any(k.startswith("sfx_") for k in SYSTEM_AUDIO))
