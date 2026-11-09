"""Công cụ cho sách lớp 2 (thiết kế TV2 tập một, mục 4 và 7): quyển, phần, nhãn, tuần, chủ điểm."""

import unittest

from tapdoc.books import grade_of, part_of, spells
from tapdoc.build import BuildError, build_lesson
from tests.test_build import src_of


def grade2_src(part1, part2=(), images=None, lesson_type="tu_ngu", **extra):
    src = src_of(part1=part1, part2=part2, images=images, lesson_id="tv2_t1_b177", lesson_no=177)
    src.update({"book": "tv2_t1_2001", "type": lesson_type, "title": "Ngày khai trường",
                "week": 1, "theme": "Nhà trường"})
    src.update(extra)
    return src


def index_of(src):
    return build_lesson(src).index


class BooksGradeTest(unittest.TestCase):
    def test_grade_of(self):
        self.assertEqual(grade_of("tv2_t1_2001"), 2)
        self.assertEqual(grade_of("tv1_t2_1996"), 1)
        self.assertEqual(grade_of("tv1_t1_1990"), 1)

    def test_spells(self):
        self.assertFalse(spells("tv2_t1_2001"))
        self.assertTrue(spells("tv1_t1_1990"))

    def test_part_lop2(self):
        self.assertEqual(part_of("tu_ngu", 2), "lop2")
        self.assertEqual(part_of("tap_doc", 2), "lop2")
        self.assertEqual(part_of("tap_doc", 1), "tap_doc")

    def test_part_unknown_grade2_raises(self):
        with self.assertRaises(ValueError):
            part_of("van_moi", 2)

    def test_grade1_rejects_grade2_types(self):
        with self.assertRaises(ValueError):
            part_of("tu_ngu", 1)


class Grade2IndexTest(unittest.TestCase):
    def test_index_entry_grade2(self):
        entry = index_of(grade2_src([{"type": "title", "text": "Ngày khai trường"}]))
        self.assertEqual(entry, {"part": "lop2", "label": "Từ ngữ", "week": 1, "grade": 2, "theme": "Nhà trường"})

    def test_labels_by_type(self):
        for lesson_type, label in (("tap_chep_chinh_ta", "Chính tả"), ("ngu_phap", "Ngữ pháp"),
                                   ("tap_lam_van", "Tập làm văn"), ("cau_do", "Câu đố")):
            entry = index_of(grade2_src([{"type": "title", "text": "x"}], lesson_type=lesson_type))
            self.assertEqual(entry["label"], label, lesson_type)

    def test_reading_label_uses_td_no(self):
        entry = index_of(grade2_src([{"type": "title", "text": "Đi học"}], lesson_type="hoc_thuoc_long", td_no=6))
        self.assertEqual(entry["label"], "Bài 6")

    def test_grade1_index_has_grade_no_theme(self):
        src = src_of(part1=[{"type": "title", "text": "o"}], part2=(), images=None)
        entry = index_of(src)
        self.assertEqual(entry["grade"], 1)
        self.assertNotIn("theme", entry)

    def test_grade2_requires_theme(self):
        src = grade2_src([{"type": "title", "text": "x"}])
        del src["theme"]
        with self.assertRaises(BuildError):
            build_lesson(src)

    def test_grade2_week_range(self):
        with self.assertRaises(BuildError):
            build_lesson(grade2_src([{"type": "title", "text": "x"}], week=18))


def _all_spells(node, found):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "spells":
                found.append(value)
            _all_spells(value, found)
    elif isinstance(node, list):
        for value in node:
            _all_spells(value, found)
    return found


class NoSpellTest(unittest.TestCase):
    LINES = ["Cái trống trường em", "Mùa hè cũng nghỉ."]

    def build(self):
        steps = [{"type": "title", "text": "Cái trống trường em"}]
        steps += [{"type": "sentence", "text": t} for t in self.LINES]
        steps += [{"type": "passage", "layout": "poem", "author": "THANH HÀO"},
                  {"type": "words", "items": [{"text": "giá trống"}]},
                  {"type": "find_words", "question": "Tìm tiếng có vần ông.", "match": {"rime": ["ông"]}, "in": [0]},
                  {"type": "memorize"}]
        return build_lesson(grade2_src(steps, lesson_type="hoc_thuoc_long", td_no=2))

    def test_no_spell_grade2(self):
        result = self.build()
        spells_lists = _all_spells(result.lesson["part1"], [])
        self.assertTrue(spells_lists)
        self.assertTrue(all(lst == [] for lst in spells_lists), spells_lists[:3])

    def test_no_phonics_audio_grade2(self):
        ids = set(self.build().audio)
        self.assertFalse({i for i in ids if i.startswith(("am_", "dau_"))})
        # "em" là cả tiếng (không có âm đầu) nên mã của chính tiếng đó là van_em; không có mảnh vần nào khác.
        self.assertEqual({i for i in ids if i.startswith("van_")}, {"van_em"})
        self.assertIn("tieng_troongs", ids)


def step_of(step, lesson_type="tap_chep_chinh_ta", pre=()):
    return build_lesson(grade2_src(list(pre) + [step], lesson_type=lesson_type)).lesson["part1"][-1]


BANK = ["vui sướng", "khai trường", "năm học", "siêng học"]
NOT_SENTENCES = ["Ngày khai trường", "Bác rất vui lòng.", "Cái trống trường em",
                 "Trong cặp có bốn quyển vở.", "Lan chưa"]


class CombineWordsTest(unittest.TestCase):
    def test_combine_words_after(self):
        st = step_of({"type": "combine_words", "base": "dúm", "items": [{"with": "lông", "at": "after"},
                                                                         {"with": "muối", "at": "after"}]})
        self.assertEqual(st["type"], "combine_words")
        self.assertEqual(st["text"], "dúm")
        self.assertTrue(st["audio"].startswith("tieng_"))
        self.assertEqual([i["text"] for i in st["items"]], ["dúm lông", "dúm muối"])
        self.assertEqual((st["items"][0]["part"], st["items"][0]["role"]), ("lông", "after"))
        self.assertTrue(st["items"][0]["audio"].startswith("tu_"))

    def test_combine_words_before(self):
        st = step_of({"type": "combine_words", "base": "quạt", "items": [{"with": "cái", "at": "before"}]})
        self.assertEqual(st["items"][0]["text"], "cái quạt")

    def test_combine_words_bad_position_fails(self):
        with self.assertRaises(BuildError):
            step_of({"type": "combine_words", "base": "quạt", "items": [{"with": "cái", "at": "giữa"}]})


class FillPassageTest(unittest.TestCase):
    def test_fill_passage_bank(self):
        st = step_of({"type": "fill_passage", "bank": BANK,
                      "text": ["Sắp đến ngày [khai trường], nhận được quà của bố, Lan càng thêm náo nức."]},
                     lesson_type="tap_lam_van")
        row = st["rows"][0]
        self.assertEqual(row["text"], "Sắp đến ngày khai trường, nhận được quà của bố, Lan càng thêm náo nức.")
        self.assertTrue(row["audio"].startswith("cau_b177_"))
        self.assertEqual(st["items"][0], {"text": "Sắp đến ngày", "row": 0, "role": "text"})
        self.assertEqual(st["items"][1], {"text": "khai trường", "row": 0, "role": "blank", "answer": "khai trường",
                                          "choices": BANK})
        self.assertEqual(st["items"][2]["text"], ", nhận được quà của bố, Lan càng thêm náo nức.")
        self.assertEqual(st["labels"], BANK)

    def test_fill_passage_own_choices(self):
        st = step_of({"type": "fill_passage", "text": ["Một năm có [mười hai|mười|mười một] tháng."]},
                     lesson_type="tu_ngu")
        blank = [i for i in st["items"] if i["role"] == "blank"][0]
        self.assertEqual((blank["answer"], blank["choices"]), ("mười hai", ["mười hai", "mười", "mười một"]))
        self.assertEqual(st["rows"][0]["text"], "Một năm có mười hai tháng.")
        self.assertEqual(st["labels"], [])

    def test_fill_passage_answer_not_in_bank_fails(self):
        with self.assertRaises(BuildError):
            step_of({"type": "fill_passage", "bank": BANK, "text": ["Em là [học trò]."]}, lesson_type="tu_ngu")

    def test_fill_passage_bank_too_small_fails(self):
        with self.assertRaises(BuildError):
            step_of({"type": "fill_passage", "bank": ["năm học"], "text": ["[năm học] và [năm học]."]},
                    lesson_type="tu_ngu")

    def test_fill_passage_no_bank_no_choices_fails(self):
        with self.assertRaises(BuildError):
            step_of({"type": "fill_passage", "text": ["Một năm có [mười hai] tháng."]}, lesson_type="tu_ngu")

    def test_fill_passage_without_blank_fails(self):
        with self.assertRaises(BuildError):
            step_of({"type": "fill_passage", "bank": BANK, "text": ["Không có ô nào."]}, lesson_type="tu_ngu")


class ChooseLineTest(unittest.TestCase):
    def test_choose_line(self):
        st = step_of({"type": "choose_line", "question": "Dòng nào viết chưa thành câu?",
                      "lines": NOT_SENTENCES, "answers": [0, 2, 4]}, lesson_type="ngu_phap")
        self.assertEqual(st["type"], "choose_line")
        self.assertEqual(st["text"], "Dòng nào viết chưa thành câu?")
        self.assertTrue(st["audio"].startswith("hoi_b177_"))
        self.assertEqual([i["role"] for i in st["items"]], ["target", "other", "target", "other", "target"])
        self.assertEqual(st["need"], 3)
        self.assertTrue(st["items"][1]["audio"].startswith("cau_b177_"))

    def test_choose_line_bad_index_fails(self):
        with self.assertRaises(BuildError):
            step_of({"type": "choose_line", "question": "?", "lines": NOT_SENTENCES, "answers": [9]},
                    lesson_type="ngu_phap")

    def test_choose_line_no_answer_fails(self):
        with self.assertRaises(BuildError):
            step_of({"type": "choose_line", "question": "?", "lines": NOT_SENTENCES, "answers": []},
                    lesson_type="ngu_phap")


class FindWordsWordTest(unittest.TestCase):
    def test_find_words_word(self):
        st = step_of({"type": "find_words", "question": "Gạch dưới chữ tỏa.", "match": {"word": ["tỏa", "phếch"]},
                      "text": ["Cây tỏa bóng mát.", "Khói tỏa mịt mù."]})
        targets = [i["text"] for i in st["items"] if i["role"] == "target"]
        self.assertEqual(targets, ["tỏa", "tỏa"])
        self.assertEqual(st["need"], 1)  # một tiếng lặp lại chỉ tính một lần


class QuestionLinesTest(unittest.TestCase):
    def test_question_lines(self):
        st = step_of({"type": "question", "text": "Đặt câu hỏi để tìm bộ phận chính thứ nhất trong hai câu sau:",
                      "lines": ["Con chìa vôi vừa hót vừa bay.", "Hoa mướp nở vàng rực."]}, lesson_type="ngu_phap")
        self.assertEqual([r["text"] for r in st["rows"]], ["Con chìa vôi vừa hót vừa bay.", "Hoa mướp nở vàng rực."])
        self.assertTrue(all(r["audio"].startswith("cau_b177_") for r in st["rows"]))

    def test_question_without_lines_unchanged(self):
        st = step_of({"type": "question", "text": "Vì sao?"}, lesson_type="ngu_phap")
        self.assertNotIn("rows", st)


class ColonMarkerTest(unittest.TestCase):
    def test_rule_colon_marker_valid(self):
        from tapdoc.validate import VALID_MARKERS
        self.assertIn(":", VALID_MARKERS)


if __name__ == "__main__":
    unittest.main()
