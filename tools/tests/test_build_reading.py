"""Các bước Phần 1 của phần Tập đọc (thiết kế tập 2, mục 7–8): tên bài, cả bài, tìm tiếng, câu hỏi, học thuộc,
điền chữ, đáp án câu đố."""

import unittest

from tapdoc.build import BuildError, build_lesson
from tests.test_build import src_of

TRUONG_EM = ["Trường em ngói mới đỏ hồng", "Mọc lên tươi thắm giữa đồng lúa xanh.",
             "Gió về đồng lúa reo quanh", "Vẫy chào những bước chân nhanh tới trường."]


def reading_src(part1, part2=(), images=None, lesson_type="tap_doc"):
    src = src_of(part1=part1, part2=part2, images=images, lesson_id="tv1_t2_b126", lesson_no=126)
    src.update({"book": "tv1_t2_1996", "type": lesson_type, "title": "Trường em", "td_no": 1, "week": 27})
    return src


def poem_steps(lines=TRUONG_EM):
    return [{"type": "title", "text": "Trường em"}] + [{"type": "sentence", "text": t} for t in lines]


def built(*steps, lines=TRUONG_EM, **kw):
    return build_lesson(reading_src(poem_steps(lines) + list(steps), **kw))


def last_step(*steps, **kw):
    return built(*steps, **kw).lesson["part1"][-1]


class TitleTest(unittest.TestCase):
    def test_title_with_sub(self):
        st = build_lesson(reading_src([{"type": "title", "text": "Cô dạy", "sub": "Học thuộc lòng"}])).lesson["part1"][0]
        self.assertEqual((st["type"], st["text"], st["labels"]), ("title", "Cô dạy", ["Học thuộc lòng"]))
        self.assertTrue(st["audio"].startswith("cau_b126_"))

    def test_title_without_sub(self):
        st = build_lesson(reading_src([{"type": "title", "text": "Trường em"}])).lesson["part1"][0]
        self.assertEqual(st["labels"], [])


class InstructionTitleTest(unittest.TestCase):
    def test_instruction_keeps_reading(self):
        # "Đánh vần và đọc những tiếng: cho, chợ..." (bài Cái bống) đứng giữa các câu hỏi, trước bước học thuộc lòng.
        st = last_step({"type": "title", "text": "Đánh vần và đọc những tiếng: cho, chợ.", "instruction": True},
                       {"type": "memorize"})
        self.assertEqual(st["type"], "memorize")
        self.assertEqual(len(st["rows"]), len(TRUONG_EM))


class PassageTest(unittest.TestCase):
    def test_reuses_sentence_audio(self):
        r = built({"type": "passage", "layout": "poem", "author": "NGUYỄN BÙI VỢI"})
        steps = r.lesson["part1"]
        sentence_audio = [s["audio"] for s in steps if s["type"] == "sentence"]
        passage = steps[-1]
        self.assertEqual([row["audio"] for row in passage["rows"]], sentence_audio)
        self.assertEqual(passage["labels"], ["NGUYỄN BÙI VỢI", "poem"])
        self.assertEqual(len([a for a in r.audio if a.startswith("cau_")]), 5)  # tên bài + 4 dòng, không thêm mã

    def test_words_carry_sentence_and_position(self):
        passage = last_step({"type": "passage", "layout": "poem"})
        first = passage["items"][0]
        self.assertEqual((first["text"], first["row"], first["col"]), ("Trường", 0, 0))
        self.assertTrue(first["spells"][0]["parts"])
        self.assertEqual(len(passage["items"]), sum(len(t.split()) for t in TRUONG_EM))

    def test_breaks_set_rows(self):
        passage = last_step({"type": "passage", "layout": "prose", "breaks": [2]})
        self.assertEqual([row["row"] for row in passage["rows"]], [0, 0, 1, 1])

    def test_only_after_last_title(self):
        steps = poem_steps() + [{"type": "title", "text": "Chính tả"}, {"type": "sentence", "text": "Chim non"},
                                {"type": "passage", "layout": "prose"}]
        passage = build_lesson(reading_src(steps)).lesson["part1"][-1]
        self.assertEqual([row["text"] for row in passage["rows"]], ["Chim non"])

    def test_no_sentence_raises(self):
        with self.assertRaises(BuildError):
            build_lesson(reading_src([{"type": "title", "text": "x"}, {"type": "passage", "layout": "poem"}]))


class FindWordsTest(unittest.TestCase):
    def find(self, **step):
        return last_step({"type": "find_words", "question": "Tìm tiếng?", **step})

    def targets(self, st):
        return [it["text"] for it in st["items"] if it["role"] == "target"]

    def test_rime_match(self):
        st = self.find(match={"rime": ["ương", "ươi"]}, **{"in": [0, 1]})
        self.assertEqual(self.targets(st), ["Trường", "tươi"])
        self.assertEqual(st["need"], 2)
        self.assertTrue(st["audio"].startswith("hoi_b126_"))
        self.assertEqual(len(st["rows"]), 2)
        trường = st["items"][0]
        self.assertEqual(trường["hl"], [{"s": 2, "n": 4}])  # phần "ường"

    def test_repeated_word_counts_once(self):
        st = last_step({"type": "find_words", "question": "Tìm tiếng có vần on?", "match": {"rime": ["on"]}},
                       lines=["Chim non chăm học.", "Chim non hát hay.", "Bạn khen Chim non."])
        self.assertEqual(len(self.targets(st)), 3)
        self.assertEqual(st["need"], 1)

    def test_case_insensitive_match(self):
        st = self.find(match={"onset": ["tr"]})
        self.assertEqual(self.targets(st), ["Trường", "trường"])
        self.assertEqual(st["need"], 1)

    def test_count_overrides(self):
        st = self.find(match={"rime": ["anh"]}, count=1)
        self.assertEqual(st["need"], 1)

    def test_count_above_distinct_raises(self):
        with self.assertRaises(BuildError):
            self.find(match={"rime": ["ương"]}, count=3)

    def test_no_match_raises(self):
        with self.assertRaises(BuildError):
            self.find(match={"rime": ["oac"]})

    def test_tone_match_nga(self):
        st = self.find(match={"tone": ["ngã"]}, **{"in": [3]})
        self.assertEqual(self.targets(st), ["Vẫy", "những"])
        self.assertEqual(st["items"][0]["hl"], [{"s": 0, "n": 3}])

    def test_onset_match_gi(self):
        st = self.find(match={"onset": ["gi"]})
        self.assertEqual(self.targets(st), ["giữa", "Gió"])
        self.assertEqual(st["items"][[it["text"] for it in st["items"]].index("Gió")]["hl"], [{"s": 0, "n": 2}])

    def test_qu_rime_includes_u(self):
        # Sách coi "quyển" có vần uyên, "Quỳnh" có vần uynh (bài Quyển sách mới, tr.92).
        st = last_step({"type": "find_words", "question": "Tìm tiếng có vần uyên, uynh.",
                        "match": {"rime": ["uyên", "uynh"]}},
                       lines=["Hôm nay cô giáo phát cho Quỳnh quyển sách mới."])
        self.assertEqual(self.targets(st), ["Quỳnh", "quyển"])
        quynh = [it for it in st["items"] if it["text"] == "Quỳnh"][0]
        self.assertEqual(quynh["hl"], [{"s": 1, "n": 4}])  # "uỳnh"

    def test_one_match_kind_only(self):
        with self.assertRaises(BuildError):
            self.find(match={"rime": ["ương"], "onset": ["tr"]})

    def test_text_sentences_from_other_page(self):
        r = built({"type": "find_words", "question": "Tìm hai tiếng có vần oc?",
                   "text": ["Sáng nào, Chim non cũng dậy sớm học bài."], "match": {"rime": ["oc"]}, "count": 1})
        st = r.lesson["part1"][-1]
        self.assertEqual(self.targets(st), ["học"])
        self.assertIn(st["rows"][0]["audio"], r.audio)

    def test_no_spell_reads_only(self):
        st = self.find(match={"rime": ["ương"]}, spell=False)
        self.assertTrue(all(it["spells"] == [] for it in st["items"]))


class QuestionTest(unittest.TestCase):
    def test_question(self):
        st = last_step({"type": "question", "text": "Ngôi trường nói trong bài nằm ở đâu? Vì sao em biết?",
                        "marker": "?"})
        self.assertEqual(st["type"], "question")
        self.assertEqual(st["marker"], "?")
        self.assertTrue(st["audio"].startswith("hoi_b126_"))


class MemorizeTest(unittest.TestCase):
    def levels(self):
        st = last_step({"type": "memorize"})
        return st, [(it["row"], it["col"], it["level"]) for it in st["items"]]

    def test_first_word_never_hidden(self):
        _, levels = self.levels()
        self.assertTrue(all(level == 0 for _, col, level in levels if col == 0))
        self.assertTrue(all(level > 0 for _, col, level in levels if col > 0))

    def test_levels_roughly_thirds(self):
        _, levels = self.levels()
        rest = [level for _, col, level in levels if col > 0]
        level1 = sum(1 for level in rest if level == 1) / len(rest)
        upto2 = sum(1 for level in rest if level <= 2) / len(rest)
        self.assertTrue(0.25 <= level1 <= 0.45, level1)
        self.assertTrue(0.55 <= upto2 <= 0.8, upto2)
        self.assertEqual(max(rest), 3)

    def test_optional_question_text(self):
        st = last_step({"type": "memorize", "question": "Học thuộc lòng cả bài.", "marker": "?"})
        self.assertEqual(st["text"], "Học thuộc lòng cả bài.")
        self.assertTrue(st["audio"].startswith("hoi_b126_"))

    def test_deterministic(self):
        self.assertEqual(self.levels()[1], self.levels()[1])


class FillBlankTest(unittest.TestCase):
    def fill(self, **step):
        return build_lesson(reading_src([{"type": "fill_blank", **step}])).lesson["part1"][0]

    def test_letter_blank(self):
        st = self.fill(mode="letter", choices=["l", "n"],
                       items=[{"word": "chạy lon ton", "blank": "lon", "fill": "l"}])
        item = st["items"][0]
        self.assertEqual((item["role"], item["text"], item["answer"]), ("blank", "chạy lon ton", "l"))
        self.assertEqual(item["hl"], [{"s": 5, "n": 1}])
        self.assertEqual(st["labels"], ["l", "n"])
        self.assertTrue(item["audio"].startswith("tu_"))

    def test_middle_blank(self):
        item = self.fill(mode="letter", choices=["oa", "a"],
                         items=[{"word": "toa tàu", "blank": "toa", "fill": "oa"}])["items"][0]
        self.assertEqual(item["hl"], [{"s": 1, "n": 2}])

    def test_letter_blank_ignores_tone(self):
        # Sách cho "ua hay au" không dấu, chữ cần điền mang dấu: "đồng l..." -> "lúa".
        item = self.fill(mode="letter", choices=["ua", "au"],
                         items=[{"word": "đồng lúa", "blank": "lúa", "fill": "ua"}])["items"][0]
        self.assertEqual(item["hl"], [{"s": 6, "n": 2}])

    def test_tone_blank(self):
        item = self.fill(mode="tone", choices=["huyền", "sắc", "hỏi", "ngã", "nặng"],
                         items=[{"word": "thoang thoảng", "blank": "thoảng", "fill": "hỏi"}])["items"][0]
        self.assertEqual((item["answer"], item["hl"]), ("hỏi", [{"s": 7, "n": 6}]))

    def test_tone_blank_wrong_tone_raises(self):
        with self.assertRaises(BuildError):
            self.fill(mode="tone", choices=["hỏi", "ngã"], items=[{"word": "thoang thoảng", "blank": "thoảng", "fill": "ngã"}])

    def test_fill_not_in_choices_raises(self):
        with self.assertRaises(BuildError):
            self.fill(mode="letter", choices=["l", "n"], items=[{"word": "nón", "blank": "nón", "fill": "x"}])

    def test_blank_not_in_word_raises(self):
        with self.assertRaises(BuildError):
            self.fill(mode="letter", choices=["l", "n"], items=[{"word": "nón lá", "blank": "lon", "fill": "l"}])


OPTIONS = [{"image": "img_b126_b", "text": "quả cam"}, {"image": "img_b126_c", "text": "con mèo"}]


class RiddleAnswerTest(unittest.TestCase):
    IMAGES = {"img_b126_a": "đáp án", "img_b126_b": "nhiễu 1", "img_b126_c": "nhiễu 2"}

    def riddle(self, **step):
        return build_lesson(reading_src([{"type": "riddle_answer", **step}], images=self.IMAGES)).lesson["part1"][0]

    def test_three_options_contains_answer(self):
        st = self.riddle(answer="Cái tẩy", image="img_b126_a", options=OPTIONS)
        self.assertEqual(st["text"], "Cái tẩy")
        self.assertEqual(st["image"], "img_b126_a")
        self.assertEqual(sorted(it["image"] for it in st["items"]), ["img_b126_a", "img_b126_b", "img_b126_c"])
        self.assertTrue(all(it["role"] == "option" for it in st["items"]))
        self.assertEqual(st, self.riddle(answer="Cái tẩy", image="img_b126_a", options=OPTIONS))

    def test_answer_in_options_raises(self):
        with self.assertRaises(BuildError):
            self.riddle(answer="Cái tẩy", image="img_b126_a",
                        options=[{"image": "img_b126_a", "text": "cái tẩy"}, OPTIONS[1]])

    def test_answer_picture_usable_in_listen_picture(self):
        src = reading_src([{"type": "riddle_answer", "answer": "Cái tẩy", "image": "img_b126_a",
                            "options": OPTIONS}],
                          part2=[{"kind": "listen_picture", "rounds": [
                              {"word": "Cái tẩy", "prompt": "Nhỏ như cái kẹo", "answer": "img_b126_a",
                               "options": ["img_b126_b", "img_b126_a", "img_b126_c"]}]}],
                          images=self.IMAGES)
        build_lesson(src)


class MarkerTest(unittest.TestCase):
    def test_question_marker_valid(self):
        from tapdoc.validate import VALID_MARKERS
        self.assertIn("?", VALID_MARKERS)


if __name__ == "__main__":
    unittest.main()


class SystemAssetsTest(unittest.TestCase):
    """Lời hướng dẫn và kí hiệu dùng chung cho các màn Tập đọc."""

    def test_reading_instructions(self):
        from tapdoc.system_assets import SYSTEM_AUDIO
        self.assertEqual(SYSTEM_AUDIO["hd_tim_tieng"], "Con chạm vào các tiếng đúng nhé.")
        self.assertEqual(SYSTEM_AUDIO["hd_tra_loi_mieng"], "Con trả lời cùng bố mẹ nhé.")
        self.assertEqual(SYSTEM_AUDIO["hd_hoc_thuoc"], "Con đọc thuộc lòng, quên tiếng nào thì chạm vào nhé.")
        self.assertEqual(SYSTEM_AUDIO["hd_doan_do"], "Con đoán xem là gì nhé.")

    def test_question_marker_image(self):
        from tapdoc.system_assets import SYSTEM_IMAGES
        self.assertIn("img_chung_cau_hoi", SYSTEM_IMAGES)
