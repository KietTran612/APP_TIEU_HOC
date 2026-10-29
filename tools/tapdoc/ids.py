"""Mã âm thanh dạng Telex ASCII và tên đọc của âm, vần, dấu, tiếng, từ."""

from .viet import TONE_INFO, nfc, split_syllable, strip_tone, syllables

# Tên đọc của phụ âm (SGK tr.120-121, tr.122 cho các âm nhiều cách ghi).
CONSONANT_NAMES: dict[str, str] = {
    "b": "bờ",
    "c": "cờ",
    "ch": "chờ",
    "d": "dờ",
    "đ": "đờ",
    "g": "gờ đơn",
    "gh": "gờ kép",
    "gi": "di",
    "h": "hờ",
    "k": "ca",
    "kh": "khờ",
    "l": "lờ",
    "m": "mờ",
    "n": "nờ",
    "ng": "ngờ đơn",
    "ngh": "ngờ kép",
    "nh": "nhờ",
    "p": "pờ",
    "ph": "phờ",
    "q": "cu",
    "qu": "quờ",
    "r": "rờ",
    "s": "sờ",
    "t": "tờ",
    "th": "thờ",
    "tr": "trờ",
    "v": "vờ",
    "x": "xờ",
}

# Tên đọc của nguyên âm đơn.
VOWEL_NAMES: dict[str, str] = {
    "a": "a",
    "ă": "á",
    "â": "ớ",
    "e": "e",
    "ê": "ê",
    "i": "i ngắn",
    "o": "o",
    "ô": "ô",
    "ơ": "ơ",
    "u": "u",
    "ư": "ư",
    "y": "i dài",
}

_LETTER_TELEX = {
    "ă": "aw",
    "â": "aa",
    "ê": "ee",
    "ô": "oo",
    "ơ": "ow",
    "ư": "uw",
    "đ": "dd",
}

_TONE_TELEX = {
    "huyen": "f",
    "sac": "s",
    "hoi": "r",
    "nga": "x",
    "nang": "j",
}

Audio = tuple[str, str, str]  # (id, chữ đọc, loại)


def _ascii(s: str) -> str:
    """Đổi từng chữ sang Telex, chưa xét dấu thanh."""
    return "".join(_LETTER_TELEX.get(ch, ch) for ch in s)


def _require_ascii(code: str) -> str:
    """Mã âm thanh dùng làm tên file nên phải thuần ASCII; sinh ra chữ lạ thì báo lỗi ngay."""
    if not code.isascii():
        raise ValueError(f"mã không phải ASCII: {code!r}")
    return code


def _checked(audio: Audio) -> Audio:
    _require_ascii(audio[0])
    return audio


def telex(text: str) -> str:
    """Telex của cả văn bản: bỏ dấu câu, chữ thường, các âm tiết nối bằng `_`, chữ dấu ở cuối mỗi âm tiết."""
    words = syllables(text)
    if not words:
        raise ValueError(f"không có âm tiết nào: {text!r}")
    parts = []
    for word in words:
        syl = split_syllable(word)  # kiểm tra âm tiết hợp lệ và lấy dấu thanh
        # Dựng từ chữ viết (không từ onset + rime) để "gì" ra "gif", không phải "giif".
        written = strip_tone(word.lower())
        parts.append(_ascii(written) + (_TONE_TELEX[syl.tone] if syl.tone else ""))
    return _require_ascii("_".join(parts))


def unit_audio(unit: str) -> Audio:
    """Âm thanh của một phụ âm, nguyên âm hoặc vần."""
    unit = nfc(unit)
    if unit in CONSONANT_NAMES:
        audio = (f"am_{_ascii(unit)}", CONSONANT_NAMES[unit], "am")
    elif unit in VOWEL_NAMES:
        audio = (f"van_{_ascii(unit)}", VOWEL_NAMES[unit], "van")
    else:
        # Vần nhiều chữ được đọc đúng như chữ viết.
        syl = split_syllable(unit)
        if syl.onset or syl.tone is not None or syl.rime != unit:
            raise ValueError(f"không phải âm hoặc vần: {unit!r}")
        audio = (f"van_{_ascii(unit)}", unit, "van")
    return _checked(audio)


def final_audio(final: str) -> Audio:
    """Âm thanh của âm cuối; `ng` đứng cuối đọc là "ngờ"."""
    if final == "ng":
        return "am_ng_cuoi", "ngờ", "am"
    return unit_audio(final)


def tone_audio(tone: str) -> Audio:
    if tone not in TONE_INFO:
        raise ValueError(f"dấu không hợp lệ: {tone!r}")
    return f"dau_{tone}", TONE_INFO[tone][0], "dau"


def text_audio(text: str) -> Audio:
    """Âm thanh của một tiếng (`tieng_`), một từ nhiều tiếng (`tu_`), hoặc vần không âm đầu (`van_`)."""
    words = syllables(text)
    if not words:
        raise ValueError(f"không có âm tiết nào: {text!r}")
    spoken = nfc(text)
    if len(words) > 1:
        return _checked((f"tu_{telex(text)}", spoken, "tu"))
    syl = split_syllable(words[0])
    if not syl.onset and syl.tone is None:
        audio = unit_audio(syl.rime)
        if audio[1] == syl.rime:
            return audio
    return _checked((f"tieng_{telex(text)}", spoken, "tieng"))


def audio_for(text: str) -> Audio:
    """Phụ âm hoặc nguyên âm đơn dùng `unit_audio` (ă đọc là "á"), còn lại dùng `text_audio`.

    Chữ hoa của một âm ("Đ", "Gh") đọc như chữ thường.
    """
    text = nfc(text)
    letter = text.lower()
    if letter in CONSONANT_NAMES or letter in VOWEL_NAMES:
        return unit_audio(letter)
    return text_audio(text)
