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


if __name__ == "__main__":
    unittest.main()
