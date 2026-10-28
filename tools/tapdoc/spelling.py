"""Sinh chuỗi đánh vần theo SGK Tiếng Việt 1 cũ (mục 5.1).

Đánh vần vần trước, tiếng sau; khi đánh vần tiếng, vần giữ nguyên một khối.
Dấu thanh: tiếng không dấu -> tên dấu -> tiếng có dấu.
"""

from dataclasses import dataclass, field

from .ids import VOWEL_NAMES, Audio, final_audio, text_audio, tone_audio, unit_audio
from .viet import TONE_INFO, nfc, split_syllable, strip_tone

# Âm đầu có nhiều cách ghi: dùng tên đọc riêng ở tr.122 (tạm).
_SEPARATE_NAME_ONSETS = frozenset({"k", "q", "qu", "g", "gh", "ng", "ngh", "gi"})

# Âm cuối cho `spell_rime`, thử theo độ dài giảm dần.
_FINALS = ("ch", "ng", "nh", "c", "m", "n", "p", "t")

_SINGLE_VOWELS = frozenset(VOWEL_NAMES)

_GI_NOTE = "gi + vần có i: không đánh vần thẳng được, cần duyệt"


@dataclass
class Part:
    kind: str  # "unit" | "join" | "tone"
    text: str
    audio: str
    tone: str | None = None
    say: str = ""  # lời đọc của file âm thanh
    akind: str = ""  # loại mảnh âm thanh (dùng cho danh mục)

    def to_json(self) -> dict:
        data = {"kind": self.kind, "text": self.text, "audio": self.audio}
        if self.tone is not None:
            data["tone"] = self.tone
        return data


@dataclass
class SpellResult:
    target: str
    parts: list[Part]
    can_duyet: list[str] = field(default_factory=list)


def _part(kind: str, text: str, audio: Audio, tone: str | None = None) -> Part:
    audio_id, say, akind = audio
    return Part(kind, text, audio_id, tone, say, akind)


def _unit(text: str) -> Part:
    return _part("unit", text, unit_audio(text))


def _final(text: str) -> Part:
    return _part("unit", text, final_audio(text))


def _join(written: str) -> Part:
    # `written` là chữ viết của tiếng (không dựng từ âm đầu + vần: "gì" sẽ thành "gii").
    return _part("join", written, text_audio(written))


def _tone(tone: str) -> Part:
    return _part("tone", TONE_INFO[tone][1], tone_audio(tone), tone)


def _vowel_notes(parts: list[Part]) -> list[str]:
    """Ghi chú cách đọc tạm "i ngắn"/"i dài" cho mỗi chữ i, y làm một mảnh nguyên âm."""
    notes = []
    for letter in ("i", "y"):
        if any(p.kind == "unit" and p.text == letter for p in parts):
            notes.append(f"chữ '{letter}' đọc là '{VOWEL_NAMES[letter]}' (tạm)")
    return notes


def spell_syllable(s: str) -> SpellResult:
    """Đánh vần một tiếng: [âm đầu, vần, tiếng không dấu] rồi [dấu, tiếng có dấu] nếu có dấu.

    Tiếng không âm đầu, không dấu chỉ có [vần]; riêng vần đọc khác chữ viết ("y") thêm [tiếng].
    """
    word = nfc(s).lower()
    syl = split_syllable(word)
    parts: list[Part] = []
    notes: list[str] = []

    if syl.onset:
        parts.append(_unit(syl.onset))
    rime_part = _unit(syl.rime)
    parts.append(rime_part)
    if syl.onset:
        parts.append(_join(strip_tone(word)))
    elif syl.tone is None and rime_part.say != syl.rime:
        # Không âm đầu, không dấu: vần đọc khác chữ viết ("y" đọc "i dài") thì bé phải nghe lại cả tiếng.
        parts.append(_join(word))
    if syl.tone is not None:
        parts.append(_tone(syl.tone))
        parts.append(_join(word))

    if syl.onset in _SEPARATE_NAME_ONSETS:
        notes.append(f"dùng tên đọc riêng tr.122 cho '{syl.onset}' (tạm)")
    notes.extend(_vowel_notes(parts))
    if syl.onset == "gi" and syl.rime[0] in ("i", "ê"):
        notes.append(_GI_NOTE)
    return SpellResult(word, parts, notes)


def spell_rime(rime: str) -> SpellResult:
    """Đánh vần một vần: [nguyên âm, âm cuối hoặc nguyên âm thứ hai, vần].

    Hỗ trợ một nguyên âm + âm cuối (c, ch, m, n, ng, nh, p, t) và hai nguyên âm đơn đi liền nhau.
    """
    target = nfc(rime).lower()
    second = None  # mảnh thứ hai: âm cuối hoặc nguyên âm
    if len(target) >= 2 and target[0] in _SINGLE_VOWELS:
        for final in _FINALS:
            if target[1:] == final:
                second = _final(final)
                break
        else:
            if len(target) == 2 and target[1] in _SINGLE_VOWELS:
                second = _unit(target[1])

    if second is None:
        return SpellResult(target, [], [f"chưa có quy tắc đánh vần cho vần '{target}'"])

    parts = [_unit(target[0]), second, _part("join", target, unit_audio(target))]
    return SpellResult(target, parts, _vowel_notes(parts))
