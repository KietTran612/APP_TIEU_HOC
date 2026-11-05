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
_QU_Y_NOTE = "qu + vần bắt đầu bằng y: tách âm đầu và vần chưa chắc, cần duyệt"

# Tập 2 (thiết kế tập 2, mục 5): sách không in cách đánh vần, app chọn tạm; mọi chuỗi gắn nhãn để chủ dự án duyệt.
_VOWEL_DIGRAPHS = ("iê", "yê", "uô", "ươ")
_RULE_DIGRAPH = "quy tắc tạm: nguyên âm đôi"
_RULE_GLIDE = "quy tắc tạm: âm đệm"
_RULE_OO = "quy tắc tạm: oo"
# Âm đệm: o đứng trước a, ă, e; u đứng trước â, ê, y, ơ.
_GLIDES = {"o": frozenset("aăe"), "u": frozenset("âêyơ")}


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
    if syl.onset == "qu" and syl.rime.startswith("y") and len(syl.rime) > 1:
        notes.append(_QU_Y_NOTE)
    return SpellResult(word, parts, notes)


def _second_of(rest: str) -> Part | None:
    """Mảnh thứ hai của vần sau nguyên âm đầu: âm cuối, hoặc một nguyên âm đơn."""
    if rest in _FINALS:
        return _final(rest)
    if len(rest) == 1 and rest in _SINGLE_VOWELS:
        return _unit(rest)
    return None


def spell_rime(rime: str) -> SpellResult:
    """Đánh vần một vần thành 3 mảnh: [đầu, sau, vần].

    - Tập 1: nguyên âm + âm cuối (c, ch, m, n, ng, nh, p, t), hoặc hai nguyên âm đơn ("a – o – ao", "i – a – ia").
    - Tập 2, quy tắc tạm (gắn nhãn cần duyệt), xét theo thứ tự:
      1. chữ ghép nguyên âm iê, yê, uô, ươ, oo ở đầu, rồi âm cuối hoặc nguyên âm: "iê – nờ – iên";
      2. âm đệm (o trước a/ă/e, u trước â/ê/y/ơ): vần chỉ có âm đệm + âm chính thì đọc từng âm ("o – a – oa");
         còn lại đọc khối âm đệm + âm chính rồi đến âm cuối, như sơ đồ bảng ôn tr.72, tr.82 ("oa – nờ – oan",
         "uâ – nờ – uân", "uyê – nờ – uyên").
    """
    target = nfc(rime).lower()
    first = second = None
    rule = None
    head = target[:2]
    if head in _VOWEL_DIGRAPHS or head == "oo":
        second = _second_of(target[2:])
        if second is not None:
            first, rule = _unit(head), (_RULE_OO if head == "oo" else _RULE_DIGRAPH)
    elif len(target) >= 2 and target[1] in _GLIDES.get(target[0], ()):
        # Khối âm đệm + âm chính (oa, oă, uâ, uê, uy, uyê…) như sơ đồ bảng ôn tr.72, tr.82; rồi đến âm cuối.
        head = target[:3] if target.startswith("uyê") else target[:2]
        rest = target[len(head):]
        if not rest:
            first, second = _unit(target[0]), _unit(target[1:])
        else:
            second = _second_of(rest)
            if second is not None:
                first = _unit(head)
        if first is not None:
            rule = _RULE_GLIDE
    elif len(target) >= 2 and target[0] in _SINGLE_VOWELS:
        second = _second_of(target[1:])
        if second is not None:
            first = _unit(target[0])

    if first is None or second is None:
        return SpellResult(target, [], [f"chưa có quy tắc đánh vần cho vần '{target}'"])

    parts = [first, second, _part("join", target, unit_audio(target))]
    notes = ([rule] if rule else []) + _vowel_notes(parts)
    return SpellResult(target, parts, notes)
