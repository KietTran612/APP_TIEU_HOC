"""Các cách đọc của một chữ, lấy từ dữ liệu Phụ lục của sách (Resources/appendix/<mã sách>.json).

- `hoc`: cách bài học đọc chữ, theo mục Chú ý tr.122 (ids.py: CONSONANT_NAMES, VOWEL_NAMES);
- `chuan`: âm chuẩn, cột "Ghi âm" (tr.120) hoặc "Đọc là" (tr.121) của Phụ lục;
- `tenchu`: tên chữ cái, cột "Tên chữ cái" (tr.120).

Cách đọc trùng chữ thì dùng chung một file âm thanh; chữ chỉ có một cách đọc thì không cần nút phát âm thêm.
"""

import json
from functools import cache

from .ids import _ascii, unit_audio
from .paths import UNITY_RES
from .viet import nfc

KINDS = ("hoc", "chuan", "tenchu")

# Nhóm chữ mà mục Chú ý tr.122 dặn đọc riêng để trẻ phân biệt.
DISTINGUISH = {
    "c": "c, k, q", "k": "c, k, q", "q": "c, k, q",
    "d": "d và gi", "gi": "d và gi",
    "g": "g và gh", "gh": "g và gh",
    "ng": "ng và ngh", "ngh": "ng và ngh",
    "i": "i và y", "y": "i và y",
}


@cache
def appendix(book: str) -> dict | None:
    """Phụ lục của sách (chuẩn hóa NFC); sách chưa có Phụ lục thì trả None."""
    path = UNITY_RES / "appendix" / f"{book}.json"
    if not path.is_file():
        return None
    return json.loads(nfc(path.read_text(encoding="utf-8")))


def appendix_row(book: str, unit: str) -> tuple[str | None, str, int] | None:
    """(tên chữ cái hoặc None, âm chuẩn, trang) của chữ trong Phụ lục; chữ không có trong Phụ lục thì None."""
    data = appendix(book)
    if data is None:
        return None
    for row in data["alphabet"]["rows"]:
        if row["lower"] == unit:
            return row["name"], row["sound"], data["alphabet"]["page"]
    for row in data["digraphs"]["rows"]:
        if row["letters"] == unit:
            return None, row["reading"], data["digraphs"]["page"]
    return None


def unit_readings(book: str, unit: str) -> list[dict]:
    """Các cách đọc khác nhau của chữ, theo thứ tự hoc, chuan, tenchu: [{kinds, text, audio, (say, akind), hint?}].

    Danh sách rỗng khi chữ chỉ có một cách đọc hoặc không có trong Phụ lục.
    """
    unit = nfc(unit)
    row = appendix_row(book, unit)
    if row is None:
        return []
    name, sound, _ = row
    learn_id, learn_text, learn_kind = unit_audio(unit)
    readings = [{"kinds": ["hoc"], "text": learn_text, "audio": learn_id, "spoken": (learn_text, learn_kind)}]
    for kind, text, prefix in (("chuan", sound, "ghiam"), ("tenchu", name, "tenchu")):
        if text is None:
            continue
        same = next((r for r in readings if r["text"] == text), None)
        if same is not None:
            same["kinds"].append(kind)
        else:
            readings.append({"kinds": [kind], "text": text, "audio": f"{prefix}_{_ascii(unit)}",
                             "spoken": (text, "am")})
    if len(readings) == 1:
        return []
    if unit in DISTINGUISH:
        readings[0]["hint"] = f"để phân biệt {DISTINGUISH[unit]}"
    return readings
