"""Xử lý âm tiết tiếng Việt: tách âm đầu, vần, dấu thanh."""

import re
import unicodedata
from dataclasses import dataclass

# Tên dấu và ký hiệu hiển thị (ký hiệu: huyền U+02CB, sắc U+02CA, hỏi U+02C0, ngã U+02DC, nặng U+002E).
TONE_INFO: dict[str, tuple[str, str]] = {
    "huyen": ("huyền", "ˋ"),
    "sac": ("sắc", "ˊ"),
    "hoi": ("hỏi", "ˀ"),
    "nga": ("ngã", "˜"),
    "nang": ("nặng", "."),
}

# Dấu thanh ở dạng tổ hợp (sau khi phân rã NFD).
_TONE_MARKS = {
    "̀": "huyen",
    "́": "sac",
    "̉": "hoi",
    "̃": "nga",
    "̣": "nang",
}

# Âm đầu, thử theo độ dài giảm dần.
_ONSETS = (
    "ngh",
    "ng", "gh", "gi", "kh", "nh", "ph", "th", "tr", "ch", "qu",
    "b", "c", "d", "đ", "g", "h", "k", "l", "m", "n", "p", "r", "s", "t", "v", "x",
)

_VOWELS = frozenset("aăâeêioôơuưy")

# Chữ cái tiếng Việt (không có f, j, w, z); ký tự khác trong một âm tiết là không hợp lệ.
_LETTERS = frozenset("abcdeghiklmnopqrstuvxyăâđêôơư")

_TOKEN_RE = re.compile(r'[^\s,.?!;:*"]+')


@dataclass(frozen=True)
class Syllable:
    onset: str
    rime: str  # không dấu thanh, chữ thường
    tone: str | None


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def is_nfc(s: str) -> bool:
    return unicodedata.is_normalized("NFC", s)


def strip_tone(s: str) -> str:
    """Bỏ dấu thanh, giữ dấu ở nguyên âm (ă, â, ê, ô, ơ, ư) và đ."""
    decomposed = unicodedata.normalize("NFD", s)
    return nfc("".join(ch for ch in decomposed if ch not in _TONE_MARKS))


def split_syllable(s: str) -> Syllable:
    """Tách một âm tiết thành âm đầu, vần (không dấu thanh) và dấu thanh."""
    if not s or any(ch.isspace() for ch in s):
        raise ValueError(f"không phải một âm tiết: {s!r}")
    decomposed = unicodedata.normalize("NFD", nfc(s).lower())
    marks = [_TONE_MARKS[ch] for ch in decomposed if ch in _TONE_MARKS]
    if len(marks) > 1:
        raise ValueError(f"nhiều hơn một dấu thanh: {s!r}")
    tone = marks[0] if marks else None
    plain = strip_tone(decomposed)
    if any(ch not in _LETTERS for ch in plain):
        raise ValueError(f"có ký tự không phải chữ tiếng Việt: {s!r}")

    for onset in _ONSETS:
        if plain.startswith(onset):
            break
    else:
        onset = ""
    rime = plain[len(onset):]
    # "gi" không còn nguyên âm nào phía sau thì chữ i là vần ("gì" -> gi + i, "gìn" -> gi + in).
    if onset == "gi" and not any(ch in _VOWELS for ch in rime):
        rime = "i" + rime
    if not any(ch in _VOWELS for ch in rime):
        raise ValueError(f"vần không có nguyên âm: {s!r}")
    return Syllable(onset, rime, tone)


def tokens(text: str) -> list[tuple[str, int]]:
    """Các âm tiết kèm vị trí bắt đầu (tính theo ký tự NFC); bỏ dấu câu `,.?!;:*"`."""
    return [(m.group(), m.start()) for m in _TOKEN_RE.finditer(nfc(text))]


def syllables(text: str) -> list[str]:
    return [token for token, _ in tokens(text)]
