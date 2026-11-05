"""Các quyển trong app (content/books.json) và phần của từng loại bài.

Số bài chạy liền cả chương trình (tập 1: 1–80, tập 2: 81–171), nên thứ tự quyển trong file là thứ tự học.
Tập 2 không in Phụ lục bảng chữ cái, nên dùng Phụ lục của tập 1 (trường `appendix`).
"""

import json
from functools import cache

from .paths import BOOKS_FILE
from .viet import nfc

_PARTS = {
    "chu_cai": ("am_moi", "dau_thanh", "on_tap_am", "chu_hoa"),
    "van": ("van_moi", "on_tap_van", "on_tap_cuoi_ki", "van_it_dung", "on_luyen"),
    "tap_doc": ("tap_doc", "hoc_thuoc_long", "doc_them", "cau_do", "tap_chep_chinh_ta"),
}
_PART_OF = {kind: part for part, kinds in _PARTS.items() for kind in kinds}


@cache
def _books() -> tuple[dict, ...]:
    data = json.loads(nfc(BOOKS_FILE.read_text(encoding="utf-8")))
    return tuple(data["books"])


def load_books() -> list[dict]:
    """Các quyển theo thứ tự học (bản sao, sửa không ảnh hưởng bộ nhớ đệm)."""
    return [dict(book) for book in _books()]


def appendix_book(book_id: str) -> str | None:
    """Mã sách có Phụ lục dùng cho quyển `book_id`; quyển không có trong danh sách thì None."""
    for book in _books():
        if book["book_id"] == book_id:
            return book.get("appendix") or None
    return None


def part_of(lesson_type: str) -> str:
    """`chu_cai`, `van` hoặc `tap_doc`; loại bài lạ báo ValueError."""
    try:
        return _PART_OF[lesson_type]
    except KeyError:
        raise ValueError(f"loại bài không thuộc phần nào: {lesson_type!r}") from None
