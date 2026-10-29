"""Ghi chú cho phụ huynh trong bài: chú thích sách in trên trang, tên đọc riêng (mục Chú ý tr.122), chỗ app khác sách."""

from .ids import CONSONANT_NAMES, VOWEL_NAMES

# Loại ghi chú người soạn được viết; "ten_doc" do công cụ tự sinh từ tên đọc trong ids.py.
AUTHORED_KINDS = ("sach", "khac_sach")

# Âm có nhiều cách ghi mà sách dặn đọc riêng để trẻ phân biệt (tr.122): nhóm chữ dễ lẫn và âm ghi ở Phụ lục tr.120–121.
_CONFUSABLE = {
    "c": ("c, k, q", "cờ"), "k": ("c, k, q", "cờ"), "q": ("c, k, q", "cờ"),
    "d": ("d và gi", "dờ"), "gi": ("d và gi", "giờ"),
    "g": ("g và gh", "gờ"), "gh": ("g và gh", "gờ"),
    "ng": ("ng và ngh", "ngờ"), "ngh": ("ng và ngh", "ngờ"),
    "i": ("i và y", "i"), "y": ("i và y", "i"),
}
# Chỉ bài dạy chữ mới mới cần giải thích tên đọc; bài ôn tập đã có ghi chú ở bài dạy chữ đó.
_LETTER_LESSON_TYPES = ("am_moi",)


def _reading_note(unit: str) -> str | None:
    name = CONSONANT_NAMES.get(unit) or VOWEL_NAMES.get(unit)
    if unit == "qu":
        return f'Chữ "qu" đọc là "{name}" (mục Chú ý, tr.122).'
    if unit not in _CONFUSABLE or name is None:
        return None
    group, sound = _CONFUSABLE[unit]
    text = f'Chữ "{unit}" đọc là "{name}": sách dặn đọc riêng để bé phân biệt {group} (mục Chú ý, tr.122).'
    if sound != name:
        text += f' Phụ lục tr.120–121 ghi âm của chữ này là "{sound}".'
    return text


def lesson_notes(authored, lesson_type: str, new_units, word_notes) -> list[dict]:
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
        reading = [text for text in map(_reading_note, new_units) if text]
    return ([{"kind": "sach", "text": t} for t in book] + [{"kind": "ten_doc", "text": t} for t in reading]
            + [{"kind": "khac_sach", "text": t} for t in by_kind["khac_sach"]])
