"""Đo cao độ lớp 2 (tools/lop2/do_cao_do_lop2.py): tiếng nào là tiếng cuối cụm (đo tin được).
Chữ số đứng ngay sau một tiếng được đọc liền thành tiếng ("khổ 2" → "khổ hai"), nên tiếng đó nằm giữa cụm, dù
`tokens` bỏ chữ số (root 17/11: hoi_b364_02 "(khổ 2).", hoi_b364_03 "(khổ 3)." bị chấm sai nhầm)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lop2"))
from do_cao_do_lop2 import phrase_final  # noqa: E402
from tapdoc.viet import nfc, tokens  # noqa: E402


def pos(text: str, word: str, nth: int = -1) -> int:
    """Vị trí trong `tokens(text)` của lần xuất hiện thứ `nth` của `word` (mặc định lần cuối)."""
    found = [k for k, (tok, _) in enumerate(tokens(text)) if nfc(tok) == nfc(word)]
    return found[nth]


class PhraseFinalTest(unittest.TestCase):
    def test_number_after_word_is_not_final(self):
        t = "2. Những câu nào, từ ngữ nào cho biết nỗi vất vả, gian khổ của chú hải quân? (Tìm trong khổ 1 và khổ 2)."
        self.assertFalse(phrase_final(t, pos(t, "khổ")))
        t = "3. Những hình ảnh nào nói lên niềm mong ước của em bé? (khổ 3)."
        self.assertFalse(phrase_final(t, pos(t, "khổ")))
        t = "Tìm trong khổ 1"  # tiếng cuối trong `tokens` nhưng còn chữ số đọc sau nó
        self.assertFalse(phrase_final(t, pos(t, "khổ")))

    def test_real_final_word_stays_final(self):
        t = "Bài thơ có ba khổ."
        self.assertTrue(phrase_final(t, pos(t, "khổ")))
        t = "Học thuộc lòng hai khổ thơ cuối, đọc lại khổ, rồi kể."
        self.assertTrue(phrase_final(t, pos(t, "khổ")))
        self.assertFalse(phrase_final(t, pos(t, "khổ", 0)))
        t = "Chính tả: Hai con chim"
        self.assertTrue(phrase_final(t, pos(t, "tả")))
        t = "2. Vì sao vất vả?"  # chữ số đứng trước, không phải sau
        self.assertTrue(phrase_final(t, pos(t, "vả")))


if __name__ == "__main__":
    unittest.main()
