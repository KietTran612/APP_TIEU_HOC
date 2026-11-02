"""Ghi chú cho phụ huynh trong bài: chú thích sách in trên trang, các cách đọc của chữ (Phụ lục tr.120–122), chỗ app khác sách."""

from .ids import CONSONANT_NAMES
from .readings import DISTINGUISH, appendix, appendix_row, unit_readings

# Loại ghi chú người soạn được viết; "ten_doc" do công cụ tự sinh từ các cách đọc trong Phụ lục (readings.py).
AUTHORED_KINDS = ("sach", "khac_sach")
# Chỉ bài dạy chữ mới mới cần giải thích cách đọc; bài ôn tập đã có ghi chú ở bài dạy chữ đó.
_LETTER_LESSON_TYPES = ("am_moi",)


def _reading_note(book: str, unit: str) -> str | None:
    """Giải thích vì sao chữ có nhiều cách đọc: cách đọc khi học (tr.122), âm chuẩn và tên chữ cái (Phụ lục)."""
    data = appendix(book)
    if data is None:
        return None
    chu_y = data["chu_y"]["page"]
    if unit == "qu":  # Phụ lục không có "qu"; mục Chú ý dặn đọc là "quờ".
        return f'Chữ "qu" đọc là "{CONSONANT_NAMES[unit]}" (mục Chú ý, tr.{chu_y}).'
    readings = unit_readings(book, unit)
    if not readings:
        return None
    name, sound, page = appendix_row(book, unit)
    learn = readings[0]["text"]
    letters = data["alphabet"]["page"]
    if unit not in DISTINGUISH:
        return (f'Chữ "{unit}": bài đọc theo âm chuẩn "{sound}" (Phụ lục, tr.{page}). Tên chữ cái là "{name}" '
                f'(Bảng chữ cái, tr.{letters}), dùng khi gọi tên chữ trong bảng chữ cái.')
    text = (f'Chữ "{unit}" khi học đọc là "{learn}" để bé phân biệt {DISTINGUISH[unit]} '
            f'(sách dặn ở mục Chú ý, tr.{chu_y}).')
    text += (f' Âm chuẩn của chữ là "{sound}" (Phụ lục, tr.{page}).' if sound != learn
             else f' Đây cũng là âm chuẩn của chữ (Phụ lục, tr.{page}).')
    if name == learn:
        text += f' "{learn}" cũng là tên chữ cái (Bảng chữ cái, tr.{letters}).'
    elif name is not None and name != sound:
        text += f' Tên chữ cái là "{name}" (Bảng chữ cái, tr.{letters}).'
    return text


def lesson_notes(authored, lesson_type: str, new_units, word_notes, book_id: str) -> list[dict]:
    """Thứ tự: chú thích sách (cả chú thích dưới từ), tên đọc riêng, chỗ app khác sách. Lỗi dữ liệu báo ValueError."""
    if not isinstance(authored, list):
        raise ValueError("notes phải là danh sách")
    by_kind = {kind: [] for kind in AUTHORED_KINDS}
    for k, note in enumerate(authored):
        if not isinstance(note, dict) or note.get("kind") not in AUTHORED_KINDS:
            raise ValueError(f"notes[{k}]: kind phải là một trong {', '.join(AUTHORED_KINDS)}")
        text = note.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"notes[{k}]: thiếu nội dung ghi chú")
        by_kind[note["kind"]].append(text.strip())
    book = by_kind["sach"] + [n for n in dict.fromkeys(word_notes) if n not in by_kind["sach"]]
    reading = []
    if lesson_type in _LETTER_LESSON_TYPES:
        reading = [text for text in (_reading_note(book_id, u) for u in new_units) if text]
    return ([{"kind": "sach", "text": t} for t in book] + [{"kind": "ten_doc", "text": t} for t in reading]
            + [{"kind": "khac_sach", "text": t} for t in by_kind["khac_sach"]])
