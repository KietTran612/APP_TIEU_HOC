"""Nội dung TV1 Tập 2 (bài 81–171): kiểm tra chung cho mọi bài và các điểm đối chiếu với trang sách."""

import unittest

from tests.test_book_content import L

PREDRAWN_81_90 = {  # mã tranh session gốc chốt trước (docs/superpowers/notes/2026-11-05-tranh-tap-2-dot-1.md)
    81: {"img_b81_caay_canhr", "img_b81_quar_owts"},
    82: {"img_b82_caauf_baapj_beenh", "img_b82_hocj_sinh", "img_b82_con_keenh_caauf_xinh"},
    83: {"img_b83_lof_gachj", "img_b83_nhaf_sachj"},
    84: {"img_b84_con_eechs", "img_b84_towf_lichj", "img_b84_chim_chichs"},
    85: {"img_b85_ddoongf_hoof_tichs_tawcs"},
    86: {"img_b86_trang_sachs", "img_b86_cais_xengr", "img_b86_vaaps_phair_ddas"},
    87: {"img_b87_bups_mawng", "img_b87_nhaf_cao_taangf", "img_b87_lawng_bacs"},
    88: {"img_b88_chumf_bongs", "img_b88_boong_hoongf", "img_b88_caauf_sawts"},
    89: {"img_b89_boong_sungs", "img_b89_banhs_chuwng", "img_b89_trung_thu"},
    90: {"img_b90_ddaamf_sen"},
}


def lid_of(no):
    return f"tv1_t2_b{no:02d}"


def steps(no, kind):
    return [s for s in L[lid_of(no)]["part1"] if s["type"] == kind]


def texts(no, kind):
    return [s["text"] for s in steps(no, kind)]


def images_of(no):
    """Mọi mã tranh xuất hiện ở Phần 1 của bài."""
    found = set()
    for st in L[lid_of(no)]["part1"]:
        if st.get("image"):
            found.add(st["image"])
        found.update(it["image"] for it in st.get("items", []) if it.get("image"))
    return found


class Tap2TestCase(unittest.TestCase):
    def assert_lesson_basics(self, no, min_rounds=6):
        """Dựng được, đã đối chiếu trang, Phần 2 đủ lượt, mọi đánh vần không rỗng, đúng quyển."""
        lid = lid_of(no)
        self.assertIn(lid, L, f"chưa có bài {no}")
        lesson = L[lid]
        self.assertEqual(lesson["book"], "tv1_t2_1996", lid)
        self.assertEqual(lesson["source"]["verification"], "page_verified", lid)
        self.assertTrue(min_rounds <= len(lesson["part2"]) <= 10, f"{lid}: {len(lesson['part2'])} lượt")
        for i, st in enumerate(lesson["part1"]):
            spells = [st["spell"]] if "spell" in st else []
            spells += [sp for it in st.get("items", []) for sp in it.get("spells", [])]
            for sp in spells:
                self.assertTrue(sp["parts"], f"{lid} part1[{i}]: đánh vần rỗng")


class Tap2Lessons81To90(Tap2TestCase):
    def test_basics(self):
        for no in range(81, 91):
            with self.subTest(no=no):
                self.assert_lesson_basics(no)

    def test_predrawn_picture_ids_used_verbatim(self):
        for no, ids in PREDRAWN_81_90.items():
            with self.subTest(no=no):
                self.assertLessEqual(ids, images_of(no))

    def test_keywords(self):
        self.assertEqual(texts(81, "keyword"), ["cây cảnh"])
        self.assertEqual(texts(82, "keyword"), ["cầu bập bênh", "học sinh"])
        self.assertEqual(texts(84, "keyword"), ["con ếch", "tờ lịch"])
        self.assertEqual(texts(86, "keyword"), ["trang sách", "cái xẻng"])
        self.assertEqual(texts(89, "keyword"), ["bông súng", "bánh chưng"])

    def test_b81_riddle(self):
        lines = texts(81, "sentence")
        self.assertEqual(lines[0], "Đố vui")
        self.assertEqual(lines[-1], "(quả gì?)")
        riddle = L[lid_of(81)]["part2"][0]
        self.assertEqual(riddle["kind"], "listen_picture")
        self.assertTrue(riddle["prompt_audio"])

    def test_poems_first_and_last_lines(self):
        self.assertEqual(texts(82, "sentence")[0], "Con kênh xanh xanh")
        self.assertEqual(texts(85, "sentence")[-1], "Em chăm chỉ học.")
        self.assertEqual(texts(87, "sentence"), ["Vâng lời cô giáo, các bạn học sinh xếp hàng vào thăm lăng Bác."])
        self.assertEqual(texts(90, "sentence")[-1], "Gần bùn mà chẳng hôi tanh mùi bùn.")

    def test_review_tables(self):
        b85 = steps(85, "rime_table")[0]
        self.assertEqual([it["text"] for it in b85["items"] if it["role"] == "rime"],
                         ["anh", "ênh", "inh", "ach", "êch", "ich"])
        b90 = steps(90, "rime_table")[0]
        self.assertEqual([it["text"] for it in b90["items"] if it["role"] == "word"][-1], "quả trứng")

    def test_real_building_needs_review(self):
        self.assertTrue([n for n in L[lid_of(87)]["review"]["can_duyet"] if "lăng Bác" in n["note"]])



class Tap2Lessons91To99(Tap2TestCase):
    def test_basics(self):
        for no in range(91, 100):
            with self.subTest(no=no):
                self.assert_lesson_basics(no)

    def test_keywords(self):
        self.assertEqual(texts(91, "keyword"), ["cây mía", "con rùa", "dưa hấu"])
        self.assertEqual(texts(93, "keyword"), ["đèn điện", "yên ngựa"])
        self.assertEqual(texts(97, "keyword"), ["tập viết", "Yết Kiêu"])
        self.assertEqual(texts(98, "keyword"), ["quả sầu riêng", "con yểng"])

    def test_digraph_spelling_keeps_ie_as_one_piece(self):
        rime = steps(92, "spell")[0]["spell"]
        self.assertEqual([p["text"] for p in rime["parts"]], ["iê", "c", "iêc"])
        notes = [n["note"] for n in L[lid_of(92)]["review"]["can_duyet"]]
        self.assertIn("quy tắc tạm: nguyên âm đôi", notes)

    def test_first_digraph_lesson_explains_rule_to_parents(self):
        app_notes = [n["text"] for n in L[lid_of(92)]["notes"] if n["kind"] == "khac_sach"]
        self.assertTrue([t for t in app_notes if "i-ê" in t])

    def test_book_glosses(self):
        sach = [n["text"] for n in L[lid_of(98)]["notes"] if n["kind"] == "sach"]
        self.assertTrue([t for t in sach if "chăm học" in t])

    def test_review_tables(self):
        b95 = steps(95, "rime_table")[0]
        self.assertEqual(len([it for it in b95["items"] if it["role"] == "rime"]), 9)
        self.assertEqual(texts(99, "sentence")[-1], "Phơi trên nong trời.")


class Tap2Lessons100To125(Tap2TestCase):
    def test_basics(self):
        for no in range(100, 126):
            with self.subTest(no=no):
                self.assert_lesson_basics(no)

    def test_keywords(self):
        self.assertEqual(texts(100, "keyword"), ["quả chuối", "cánh buồm"])
        self.assertEqual(texts(109, "keyword"), ["cái loa", "chích chòe"])
        self.assertEqual(texts(118, "keyword"), ["sản xuất", "ngoe nguẩy đuôi"])
        self.assertEqual(texts(119, "keyword"), ["chim vành khuyên", "duyệt binh"])

    def test_glide_spelling_follows_book_diagram(self):
        rime = steps(110, "spell")[2]["spell"]  # vần oan
        self.assertEqual([p["text"] for p in rime["parts"]], ["oa", "n", "oan"])
        b115 = steps(115, "rime_table")[0]
        self.assertEqual(len([it for it in b115["items"] if it["role"] == "rime"]), 12)

    def test_rare_rime_tables_have_sentences(self):
        for no, count in ((121, 10), (122, 8)):
            table = steps(no, "rime_table")[0]
            sentences = [it for it in table["items"] if it["role"] == "sentence"]
            self.assertEqual(len(sentences), count, no)
        self.assertEqual(steps(121, "rime_table")[0]["items"][-1]["text"], "Bé mặc quần soóc.")

    def test_oo_rime_id_differs_from_ong(self):
        table = steps(121, "rime_table")[0]
        oong = [it for it in table["items"] if it["role"] == "rime" and it["text"] == "oong"][0]
        self.assertEqual(oong["audio"], "van_ooong")

    def test_riddle_b102(self):
        self.assertEqual(texts(102, "sentence")[0], "Đố vui")
        self.assertEqual(L[lid_of(102)]["part2"][0]["kind"], "listen_picture")

    def test_real_people_replaced(self):
        for no in (107, 115, 124):
            app_notes = [n["text"] for n in L[lid_of(no)]["notes"] if n["kind"] == "khac_sach"]
            self.assertTrue([t for t in app_notes if "không vẽ người thật" in t], no)

    def test_on_luyen_poems(self):
        self.assertEqual(texts(123, "sentence")[0], "Tổ quốc Việt Nam")
        self.assertEqual(texts(124, "sentence")[-1], "- Khiêm tốn, thật thà, dũng cảm")
        self.assertEqual(texts(125, "sentence")[-1], "Cùng bay nào, cho trái đất quay!")


def targets(no, k):
    """Các tiếng đúng (chữ thường, không lặp) của bước find_words thứ k trong bài."""
    step = steps(no, "find_words")[k]
    return sorted({it["text"].lower() for it in step["items"] if it["role"] == "target"})


class Tap2Reading126To138(Tap2TestCase):
    def test_basics(self):
        for no in range(126, 139):
            with self.subTest(no=no):
                self.assert_lesson_basics(no)

    def test_index_labels_and_weeks(self):
        import json
        from tapdoc.paths import UNITY_RES
        index = json.loads((UNITY_RES / "lessons" / "index.json").read_text(encoding="utf-8"))
        by_id = {e["lesson_id"]: e for e in index["lessons"]}
        self.assertEqual((by_id["tv1_t2_b126"]["label"], by_id["tv1_t2_b126"]["week"]), ("Bài 1", 27))
        self.assertEqual(by_id["tv1_t2_b131"]["label"], "Chính tả")
        self.assertEqual((by_id["tv1_t2_b137"]["label"], by_id["tv1_t2_b137"]["week"]), ("Câu đố", 28))
        self.assertEqual(by_id["tv1_t2_b136"]["label"], "Bài 10")

    def test_truong_em(self):
        self.assertEqual(texts(126, "sentence")[0], "Trường em ngói mới đỏ hồng")
        self.assertEqual(targets(126, 0), ["trường", "tươi"])
        self.assertEqual(targets(126, 1), ["những", "vẫy"])
        self.assertEqual(steps(126, "passage")[0]["labels"], ["NGUYỄN BÙI VỢI", "poem"])

    def test_qu_rimes_found(self):
        self.assertEqual(targets(127, 1), ["quyển", "quỳnh"])
        self.assertIn("quýt", targets(134, 1))

    def test_memorize_for_hoc_thuoc_long(self):
        for no in (128, 134):
            self.assertEqual(len(steps(no, "memorize")), 1, no)
            self.assertEqual(steps(no, "memorize")[0]["text"], "Học thuộc lòng cả bài.")

    def test_doc_them_has_no_questions(self):
        for no in (130, 136):
            self.assertEqual(steps(no, "question") + steps(no, "find_words"), [], no)

    def test_riddles_answers_from_page_138(self):
        answers = [s["text"] for s in steps(137, "riddle_answer")]
        self.assertEqual(answers, ["Cái tẩy", "Bút chì (viết chì)"])

    def test_dictation_pages(self):
        fills = steps(138, "fill_blank")
        self.assertEqual(fills[0]["labels"], ["l", "n"])
        self.assertEqual([it["answer"] for it in fills[1]["items"]], ["oa", "oa", "oa", "a", "a"])
        self.assertEqual(targets(138, 1), ["sáng", "sóc", "xanh", "xuống"])


class Tap2Reading139To151(Tap2TestCase):
    def test_basics(self):
        for no in range(139, 152):
            with self.subTest(no=no):
                self.assert_lesson_basics(no)

    def test_spelling_lists_follow_instruction(self):
        # "Đánh vần và đọc những tiếng: ..." là câu lệnh rồi đến các tiếng sách nêu.
        self.assertEqual([it["text"] for it in steps(141, "words")[0]["items"]],
                         ["Hoạch", "mừng quýnh", "nhễ nhại", "nước lọc"])
        self.assertEqual(steps(142, "memorize")[0]["text"], "Học thuộc lòng cả bài.")

    def test_book_footnotes(self):
        for no, word in ((143, "Phì"), (146, "Na")):
            sach = [n["text"] for n in L[lid_of(no)]["notes"] if n["kind"] == "sach"]
            self.assertTrue([t for t in sach if t.startswith(word)], no)

    def test_tone_questions(self):
        self.assertEqual(targets(140, 1), ["cả", "giữa", "ngủ", "võng", "ả"])

    def test_riddles_page_115(self):
        self.assertEqual([s["text"] for s in steps(150, "riddle_answer")], ["Trâu (hoặc bò)", "Ong", "Gà trống"])

    def test_dictation_tone_fill(self):
        tones = [s for s in steps(144, "fill_blank") if set(s["labels"]) <= {"huyền", "sắc", "hỏi", "ngã", "nặng"}]
        self.assertEqual([it["answer"] for it in tones[0]["items"]], ["ngã", "hỏi", "ngã", "hỏi"])


class Tap2Reading152To171(Tap2TestCase):
    def test_basics(self):
        for no in range(152, 172):
            with self.subTest(no=no):
                self.assert_lesson_basics(no)

    def test_every_reading_lesson_has_title_and_passage(self):
        for no in range(126, 172):
            ltype = L[lid_of(no)]["type"]
            if ltype in ("tap_doc", "hoc_thuoc_long", "doc_them"):
                with self.subTest(no=no):
                    self.assertEqual(len(steps(no, "passage")), 1)
                    self.assertTrue(steps(no, "title"))

    def test_hoc_thuoc_long_have_memorize(self):
        hoc_thuoc = [no for no in range(126, 172) if L[lid_of(no)]["type"] == "hoc_thuoc_long"]
        self.assertEqual(hoc_thuoc, [128, 134, 142, 147, 154, 161, 168])
        for no in hoc_thuoc:
            self.assertEqual(len(steps(no, "memorize")), 1, no)

    def test_last_page_poem(self):
        self.assertEqual(texts(170, "sentence")[-1], "Gửi lời chào tiến bước!")
        self.assertEqual(len(texts(170, "sentence")), 16)

    def test_riddles_page_128(self):
        self.assertEqual([s["text"] for s in steps(163, "riddle_answer")], ["Lưỡi cày", "Hòn gạch"])

    def test_vo_thi_sau_title_from_page(self):
        self.assertEqual(L[lid_of(168)]["title"], "Võ Thị Sáu")

    def test_tone_fill_from_page_137(self):
        fills = steps(171, "fill_blank")
        self.assertEqual([it["answer"] for it in fills[-1]["items"]], ["hỏi", "hỏi", "ngã", "sắc", "nặng", "nặng"])

if __name__ == "__main__":
    unittest.main()
