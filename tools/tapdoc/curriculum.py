"""Đọc giáo trình: tính chữ, vần và dấu thanh bé đã học tới một bài."""

import csv
from dataclasses import dataclass
from pathlib import Path

from tapdoc.viet import TONE_INFO, nfc, split_syllable, syllables

DEFAULT_BOOK = "tv1_t1_1990"

# Chỉ các loại bài này dạy cái mới; các loại khác (ôn tập, chữ hoa, ...) bị bỏ qua.
_TEACHING = ("dau_thanh", "am_moi", "van_moi")

_TONE_BY_NAME = {name: key for key, (name, _) in TONE_INFO.items()}


@dataclass(frozen=True)
class Learned:
    letters: frozenset[str]
    rimes: frozenset[str]
    tones: frozenset[str]


def load_curriculum(csv_path: Path, book_id: str = DEFAULT_BOOK) -> dict[int, tuple[str, str]]:
    """Số bài -> (loai_bai, noi_dung_chinh) của một cuốn sách; bỏ dòng có bai_so không phải số."""
    result: dict[int, tuple[str, str]] = {}
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if row["book_id"] != book_id or not row["bai_so"].isdecimal():
                continue
            result[int(row["bai_so"])] = (row["loai_bai"], nfc(row["noi_dung_chinh"]))
    return result


def learned_until(cur: dict[int, tuple[str, str]], lesson_no: int) -> Learned:
    """Gộp những gì các bài 1..lesson_no đã dạy."""
    letters: set[str] = set()
    rimes: set[str] = set()
    tones: set[str] = set()
    for no in sorted(cur):
        if no > lesson_no:
            break
        kind, content = cur[no]
        if kind not in _TEACHING:
            continue
        for item in (part.strip() for part in content.split(";")):
            if not item:
                continue
            head, _, tail = item.partition(" ")
            if head == "dấu":
                if tail not in _TONE_BY_NAME:
                    raise ValueError(f"bài {no}: dấu không biết: {item!r}")
                tones.add(_TONE_BY_NAME[tail])
            elif head == "chữ" and tail:
                letters.add(tail)
            elif head == "vần" and tail:
                rimes.add(tail)
            elif tail or kind == "dau_thanh":
                raise ValueError(f"bài {no} ({kind}): không hiểu mục {item!r}")
            elif kind == "am_moi":
                letters.add(item)
            else:
                rimes.add(item)
    return Learned(frozenset(letters), frozenset(rimes), frozenset(tones))


def is_learned_text(text: str, learned: Learned) -> bool:
    """True nếu mọi âm, vần, dấu trong `text` đều đã học (hoặc `text` là một chữ/vần đã học)."""
    text = nfc(text)
    if text in learned.letters or text in learned.rimes:
        return True
    words = syllables(text)
    if not words:
        return False
    for word in words:
        try:
            syl = split_syllable(word)
        except ValueError:
            return False
        if syl.onset and syl.onset not in learned.letters:
            return False
        rime_set = learned.letters if len(syl.rime) == 1 else learned.rimes
        if syl.rime not in rime_set:
            return False
        if syl.tone is not None and syl.tone not in learned.tones:
            return False
    return True
