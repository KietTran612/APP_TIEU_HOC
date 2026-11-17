"""Ngoặc kép giữa câu làm HoaiMy chèn một tiếng ngắn ("từ "can đảm"" → "từ y can đảm", root nhận dạng 17/11):
chữ đọc bỏ ngoặc kép (kiểu a) hoặc thay ngoặc kép mở bằng dấu phẩy (kiểu b); chữ hiển thị giữ nguyên."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lop2"))
from ngoac_kep_lop2 import doc_ngoac, targets  # noqa: E402


class DocNgoacTest(unittest.TestCase):
    def test_root_trials(self):
        # đúng chữ của bốn bản thử root nhận dạng (L2T2-ngoac)
        t = '*4. Tìm từ trái nghĩa với từ "can đảm".'
        self.assertEqual(doc_ngoac(t, "a"), "*4. Tìm từ trái nghĩa với từ can đảm.")
        self.assertEqual(doc_ngoac(t, "b"), "*4. Tìm từ trái nghĩa với từ, can đảm.")
        t = '*2. Vì sao mặt trăng được coi là "trạm đầu vũ trụ"? (xem chú giải)'
        self.assertEqual(doc_ngoac(t, "a"), "*2. Vì sao mặt trăng được coi là trạm đầu vũ trụ? (xem chú giải)")
        self.assertEqual(doc_ngoac(t, "b"), "*2. Vì sao mặt trăng được coi là, trạm đầu vũ trụ? (xem chú giải)")

    def test_after_punctuation_quote_is_just_dropped(self):
        # sau dấu câu đã có chỗ nghỉ: kiểu b không thêm dấu phẩy
        t = "Bác thợ nghiêm trang bảo: \"Cháu nói đúng,"
        for kieu in "ab":
            self.assertEqual(doc_ngoac(t, kieu), "Bác thợ nghiêm trang bảo: Cháu nói đúng,")
        t = '*5. "Xắc" là từ chỉ đồ vật.'
        for kieu in "ab":
            self.assertEqual(doc_ngoac(t, kieu), "*5. Xắc là từ chỉ đồ vật.")

    def test_closing_quote_mid_sentence_counts(self):
        # mở ở đầu câu thì không chèn tiếng, nhưng đóng giữa câu ("Xắc" là) thì có
        self.assertEqual(doc_ngoac('"Tấc đất, tấc vàng" là câu thành ngữ.', "b"), "Tấc đất, tấc vàng là câu thành ngữ.")
        self.assertEqual(doc_ngoac('Thành ngữ: "Tấc đất..." (Nói như thế nghĩa là thế nào?)', "a"),
                         "Thành ngữ: Tấc đất... (Nói như thế nghĩa là thế nào?)")

    def test_mid_open_words(self):
        self.assertEqual(doc_ngoac('Thư đề "Thượng khẩn"', "a"), "Thư đề Thượng khẩn")
        self.assertEqual(doc_ngoac('Thư đề "Thượng khẩn"', "b"), "Thư đề, Thượng khẩn")
        self.assertEqual(doc_ngoac('rúc "cú cú" nghe rợn người', "b"), "rúc, cú cú nghe rợn người")

    def test_no_change_when_quotes_only_at_edges(self):
        for t in ('"Các vua Hùng đã có công dựng nước,',
                  "làm việc gì cũng phải làm đến nơi đến chốn mới khỏi phí công vô ích\".",
                  '"Mình đánh lừa được tất cả mọi người, tài thật!".',
                  "Không có ngoặc kép."):
            for kieu in "ab":
                with self.subTest(t=t, kieu=kieu):
                    self.assertIsNone(doc_ngoac(t, kieu))

    def test_bad_kieu(self):
        with self.assertRaises(ValueError):
            doc_ngoac('Thư đề "Thượng khẩn"', "c")


class TargetsTest(unittest.TestCase):
    def rows(self):
        def r(i, text, status="cho_duyet", bai="tv2_t2_b322"):
            return {"id": i, "text": text, "status": status, "bai": [bai]}
        return [r("hoi_b322_02", '*2. Vì sao mặt trăng được coi là "trạm đầu vũ trụ"? (xem chú giải)'),
                r("cau_b348_13", '"Các vua Hùng đã có công dựng nước,'),  # mở ở đầu câu: đọc sạch, giữ
                r("cau_b309_02", 'Bài viết: "Một hôm, ông để... gãy được bó đũa".'),  # chữ đọc riêng không còn ngoặc
                r("hoi_b330_01", 'Từ "cú" là gì?', status="dat"),  # đã duyệt: không tự đổi
                r("hoi_b189_01", 'Đáp lời "chào cô ạ!"', bai="tv2_t1_b189"),  # tập khác
                r("cau_b323_09", 'mẹ nói "ở lại"')]

    def test_kieu_a_on_text_or_existing_doc(self):
        settings = {"overrides": {"cau_b309_02": {"doc": "Bài viết: đoạn từ Một hôm, ông để đến gãy được bó đũa."},
                                  "cau_b323_09": {"doc": 'mẹ nói "ở lại".', "rate": -35}}}
        found = {r["id"]: (old, new) for r, old, new in targets(self.rows(), settings, "tv2_t2_", "a")}
        self.assertEqual(found, {
            "hoi_b322_02": ('*2. Vì sao mặt trăng được coi là "trạm đầu vũ trụ"? (xem chú giải)',
                            "*2. Vì sao mặt trăng được coi là trạm đầu vũ trụ? (xem chú giải)"),
            "cau_b323_09": ('mẹ nói "ở lại".', "mẹ nói ở lại."),
        })


if __name__ == "__main__":
    unittest.main()
