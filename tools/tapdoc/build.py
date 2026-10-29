"""Dựng file bài học (JSON cho Unity đọc) từ nguồn bài soạn tay.

Nguồn là bản chép từ trang sách; file dựng chứa sẵn chuỗi đánh vần, mã âm thanh, mã tranh,
đoạn tô màu phần mới (`hl`) và các bài tập đã dàn phẳng. Hình dạng file dựng theo hợp đồng
dữ liệu của dự án; Unity đọc đúng các tên trường này.
"""

import json
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from .ids import audio_for, text_audio, tone_audio
from .spelling import Part, SpellResult, spell_rime, spell_syllable
from .viet import TONE_INFO, nfc, split_syllable, strip_tone, syllables, tokens

SCHEMA = 1

# Loại âm thanh của lời dẫn tranh và của câu (cột `loai` trong danh mục âm thanh).
_PICTURE_KIND = "huong_dan"
_SENTENCE_KIND = "cau"

PICTURE_NOTE = "lời dẫn tranh do Claude đề xuất"
Q_NOTE = "tên đọc của 'q' là \"cu\" theo tr.122 (tạm)"

# Bảng chữ thường / chữ hoa của bài 41 xếp 4 cột, đọc theo hàng.
_PAIR_COLUMNS = 4

# Lời hướng dẫn của từng loại bài tập (mã nằm trong `system_assets.SYSTEM_AUDIO`).
INSTRUCTION_AUDIO = {
    "listen_choose": "hd_nghe_chon_chu",
    "look_tone": "hd_nhin_keo_dau",
    "compose": "hd_keo_vao_cho_trong",
    "listen_picture": "hd_nghe_chon_tranh",
    "match_case": "hd_nhin_chon_chu_hoa",
}
# Lượt nghe chọn tranh có câu đố (bài 80): đọc câu đố thay cho từ đáp án.
RIDDLE_INSTRUCTION_AUDIO = "hd_nghe_do_chon_tranh"

_REQUIRED_FIELDS = ("lesson_id", "book", "lesson_no", "type", "title", "source", "new_units", "images",
                    "part1", "part2")
_HEAD = "(đầu bài)"
_RIME_LESSON_TYPES = ("van_moi", "on_tap_van", "on_tap_cuoi_ki")


class BuildError(Exception):
    """Lỗi trong nguồn bài. Thông điệp bắt đầu bằng "<lesson_id> <vị trí>: "."""


@dataclass
class BuildResult:
    lesson: dict
    audio: dict[str, tuple[str, str]]  # mã -> (lời đọc, loại)
    images: dict[str, str]  # mã -> mô tả


def _nfc_deep(obj):
    """Chuẩn hóa NFC mọi chuỗi (cả khóa) trong dữ liệu JSON."""
    if isinstance(obj, str):
        return nfc(obj)
    if isinstance(obj, list):
        return [_nfc_deep(x) for x in obj]
    if isinstance(obj, dict):
        return {_nfc_deep(k): _nfc_deep(v) for k, v in obj.items()}
    return obj


def _normalized_say(text: str) -> str:
    """Lời đọc đem so sánh: bỏ dấu câu, thu gọn khoảng trắng, chữ thường."""
    words = syllables(text)
    return " ".join(words).lower() if words else text.strip().lower()


def _option(text: str = "", audio: str = "", image: str = "", tone: str = "") -> dict:
    return {"text": text, "audio": audio, "image": image, "tone": tone}


def _make_round(kind: str, tag: str, **fields) -> dict:
    """Một lượt luôn có đủ mọi khóa; trường không dùng để chuỗi rỗng."""
    rd = {"kind": kind, "tag": tag, "instruction_audio": INSTRUCTION_AUDIO[kind], "prompt_audio": "",
          "prompt_text": "", "base_text": "", "image": "", "options": [], "answer": 0}
    rd.update(fields)
    return rd


def _join_part(text: str) -> Part:
    audio_id, say, akind = text_audio(text)
    return Part("join", text, audio_id, None, say, akind)


def _tone_part(tone: str) -> Part:
    audio_id, say, akind = tone_audio(tone)
    return Part("tone", TONE_INFO[tone][1], audio_id, tone, say, akind)


def _combined(onset: str, vowel: str) -> str:
    """Tiếng ghép âm đầu với nguyên âm trong bảng ghép; gi + i viết là "gi" (không lặp i)."""
    return "gi" if (onset, vowel) == ("gi", "i") else onset + vowel


class _Builder:
    def __init__(self, src: dict):
        self.src = src
        self.lid = src.get("lesson_id", "?")
        self.audio: dict[str, tuple[str, str]] = {}
        self.images: dict[str, str] = {}
        self.can_duyet: list[dict] = []
        self.image_text: dict[str, str] = {}  # mã tranh -> chữ của bước Phần 1 có tranh đó (R6)
        self.picture_count = 0
        self.sentence_count = 0
        self.nn = ""
        self.new_units: frozenset[str] = frozenset()
        self.colour_sentences = False

    # ---- lỗi và vị trí ----

    def error(self, where: str, message: str) -> BuildError:
        return BuildError(f"{self.lid} {where}: {message}")

    @contextmanager
    def _located(self, where: str):
        """Đổi lỗi dữ liệu thiếu/sai bên trong thành BuildError có vị trí."""
        try:
            yield
        except KeyError as e:
            raise self.error(where, f"thiếu trường {e.args[0]!r}") from e
        except ValueError as e:
            raise self.error(where, str(e)) from e
        except (TypeError, AttributeError) as e:
            raise self.error(where, f"dữ liệu sai kiểu: {e}") from e

    # ---- thu thập âm thanh, tranh, ghi chú ----

    def _register_audio(self, audio_id: str, say: str, akind: str, where: str) -> str:
        """Ghi một mã âm thanh.

        Cùng mã mà lời đọc khác (sau chuẩn hóa) là lỗi; chỉ khác hoa/thường hay dấu câu thì giữ bản đầu.
        """
        known = self.audio.get(audio_id)
        if known is None:
            self.audio[audio_id] = (say, akind)
        elif _normalized_say(known[0]) != _normalized_say(say):
            raise self.error(where, f"mã âm thanh {audio_id!r} trùng nhau nhưng lời đọc khác: "
                                    f"{known[0]!r} và {say!r}")
        return audio_id

    def _audio(self, triple: tuple[str, str, str], where: str) -> str:
        audio_id, say, akind = triple
        return self._register_audio(audio_id, say, akind, where)

    def _image(self, image_id: str, where: str) -> str:
        description = self.src["images"].get(image_id)
        if description is None:
            raise self.error(where, f"mã tranh {image_id!r} không có trong images")
        self.images[image_id] = description
        return image_id

    def _note(self, where: str, note: str) -> None:
        entry = {"where": where, "note": note}
        if entry not in self.can_duyet:
            self.can_duyet.append(entry)

    def _spell(self, result: SpellResult, where: str, drag_tone: bool = False) -> dict:
        for part in result.parts:
            self._register_audio(part.audio, part.say, part.akind, where)
        for note in result.can_duyet:
            self._note(where, note)
        return {"target": result.target, "drag_tone": drag_tone, "parts": [p.to_json() for p in result.parts]}

    def _spells_of(self, text: str, where: str) -> list[dict]:
        return [self._spell(spell_syllable(s), where) for s in syllables(text)]

    # ---- tô màu phần mới ----

    def _highlights(self, text: str) -> list[dict]:
        spans = []
        for tok, start in tokens(text):
            if tok.lower() in self.new_units:
                spans.append({"s": start, "n": len(tok)})
                continue
            try:
                syl = split_syllable(tok)
            except ValueError:
                continue  # chữ chỉ có phụ âm ("b", "ng"): không tách được âm đầu/vần nên không tô
            if syl.onset and syl.onset in self.new_units:
                spans.append({"s": start, "n": len(syl.onset)})
            rime_len = len(tok) - len(syl.onset)
            if syl.rime in self.new_units and rime_len > 0:
                spans.append({"s": start + len(syl.onset), "n": rime_len})
        return spans

    # ---- Phần 1 ----

    def _step_unit(self, step: dict, where: str) -> dict:
        text = step["text"]
        return {"type": "unit", "text": text, "audio": self._audio(audio_for(text), where),
                "hl": self._highlights(text)}

    def _step_keyword(self, step: dict, where: str) -> dict:
        text, image = step["text"], step["image"]
        out = {"type": "keyword", "text": text, "audio": self._audio(text_audio(text), where),
               "image": self._image(image, where), "hl": self._highlights(text)}
        self.image_text.setdefault(image, text)
        return out

    def _step_analyze(self, step: dict, where: str) -> dict:
        rows = [{"text": row, "audio": self._audio(audio_for(row), where), "hl": self._highlights(row)}
                for row in step["rows"]]
        return {"type": "analyze", "rows": rows}

    def _step_spell(self, step: dict, where: str) -> dict:
        result = spell_rime(step["target"]) if step.get("rime") else spell_syllable(step["target"])
        out = {"type": "spell", "spell": self._spell(result, where, bool(step.get("drag_tone", False)))}
        if "then" in step:
            out["then_text"] = step["then"]
            out["then_audio"] = self._audio(text_audio(step["then"]), where)
        return out

    def _step_tone_intro(self, step: dict, where: str) -> dict:
        tone = step["tone"]
        if tone not in TONE_INFO:
            raise self.error(where, f"dấu không hợp lệ: {tone!r}")
        name, glyph = TONE_INFO[tone]
        return {"type": "tone_intro", "tone": tone, "text": name, "glyph": glyph,
                "audio": self._audio(tone_audio(tone), where)}

    def _step_tone_attach(self, step: dict, where: str) -> dict:
        target, image = step["target"].lower(), step["image"]
        tone = split_syllable(target).tone
        if tone is None:
            raise self.error(where, f"tiếng {target!r} không có dấu thanh để gắn")
        parts = [_join_part(strip_tone(target)), _tone_part(tone), _join_part(target)]
        out = {"type": "tone_attach", "image": self._image(image, where),
               "spell": self._spell(SpellResult(target, parts), where, drag_tone=True)}
        self.image_text.setdefault(image, target)
        return out

    def _step_picture(self, step: dict, where: str) -> dict:
        image, say = step["image"], step["say"]
        self._image(image, where)
        self.picture_count += 1
        audio_id = f"hd_b{self.nn}_tranh_{self.picture_count:02d}"
        self._register_audio(audio_id, say, _PICTURE_KIND, where)
        self._note(where, PICTURE_NOTE)
        if step.get("word"):  # tranh không có chữ trên trang: `word` chỉ để làm bài nghe chọn tranh
            self.image_text.setdefault(image, step["word"])
        return {"type": "picture", "image": image, "audio": audio_id}

    # ---- bảng dấu, khung chữ, bảng ghép (bài dấu thanh và bài ôn tập) ----

    def _toned_from(self, base: str, toned: str, where: str) -> tuple[str, dict]:
        """(dấu, đánh vần "tiếng gốc – dấu – tiếng có dấu") của một tiếng có dấu dựng từ `base`."""
        toned = toned.lower()
        tone = split_syllable(toned).tone
        if tone is None:
            raise self.error(where, f"tiếng {toned!r} không có dấu thanh")
        if strip_tone(toned) != base:
            raise self.error(where, f"tiếng {toned!r} không dựng từ {base!r}")
        parts = [_join_part(base), _tone_part(tone), _join_part(toned)]
        return tone, self._spell(SpellResult(toned, parts), where)

    def _step_tone_table(self, step: dict, where: str) -> dict:
        base = step["base"].lower()
        if split_syllable(base).tone is not None:
            raise self.error(where, f"tiếng gốc {base!r} phải không có dấu")
        items, seen = [], set()
        for j, text in enumerate(step["results"]):
            item_where = f"{where}.items[{j}]"
            tone, spell = self._toned_from(base, text, item_where)
            if tone in seen:
                raise self.error(item_where, f"hai ô cùng dấu {tone!r}")
            seen.add(tone)
            items.append({"text": text, "audio": self._audio(text_audio(text), item_where), "role": "cell",
                          "tone": tone, "glyph": TONE_INFO[tone][1], "spells": [spell]})
        return {"type": "tone_table", "text": base, "audio": self._audio(text_audio(base), where), "items": items}

    def _step_letter_grid(self, step: dict, where: str) -> dict:
        items = []
        for letter in step["letters"]:
            item_where = f"{where}.items[{len(items)}]"
            items.append({"text": letter, "audio": self._audio(audio_for(letter), item_where), "role": "letter",
                          "row": 0, "col": len(items)})
        for k, tone in enumerate(step.get("tones", [])):
            item_where = f"{where}.items[{len(items)}]"
            if tone not in TONE_INFO:
                raise self.error(item_where, f"dấu không hợp lệ: {tone!r}")
            items.append({"text": TONE_INFO[tone][1], "audio": self._audio(tone_audio(tone), item_where),
                          "role": "tone", "row": 1, "col": k, "tone": tone, "glyph": TONE_INFO[tone][1]})
        return {"type": "letter_grid", "items": items}

    def _step_combine_table(self, step: dict, where: str) -> dict:
        items: list[dict] = []
        vowels: list[str] = []

        def column(vowel: str, cell_where: str) -> int:
            if vowel not in vowels:
                vowels.append(vowel)
                items.append({"text": vowel, "audio": self._audio(audio_for(vowel), cell_where),
                              "role": "vowel", "row": 0, "col": len(vowels) - 1})
            return vowels.index(vowel)

        for i, row in enumerate(step["rows"]):
            onset = row["onset"]
            items.append({"text": onset, "audio": self._audio(audio_for(onset), f"{where}.rows[{i}]"),
                          "role": "onset", "row": i, "col": 0})
            blocked = list(row.get("blocked", []))
            for vowel, forms in row["cells"].items():
                cell_where = f"{where}.rows[{i}].cells[{vowel!r}]"
                if vowel in blocked:
                    raise self.error(cell_where, f"nguyên âm {vowel!r} vừa có ô vừa bị chặn")
                col = column(vowel, cell_where)
                if not forms:
                    raise self.error(cell_where, "ô trống")
                base = forms[0].lower()
                if base != _combined(onset, vowel):
                    raise self.error(cell_where, f"tiếng đầu ô {base!r} phải là {onset!r} + {vowel!r}")
                items.append({"text": base, "audio": self._audio(text_audio(base), cell_where), "role": "base",
                              "row": i, "col": col, "spells": [self._spell(spell_syllable(base), cell_where)]})
                for form in forms[1:]:
                    tone, spell = self._toned_from(base, form, cell_where)
                    items.append({"text": form, "audio": self._audio(text_audio(form), cell_where), "role": "form",
                                  "row": i, "col": col, "tone": tone, "glyph": TONE_INFO[tone][1],
                                  "spells": [spell]})
            # Ô gạch chéo trên trang: âm đầu không ghép với nguyên âm này (k + a, gh + o).
            for vowel in blocked:
                cell_where = f"{where}.rows[{i}].blocked[{vowel!r}]"
                items.append({"text": "", "role": "blocked", "row": i,
                              "col": column(vowel, cell_where)})
        return {"type": "combine_table", "marker": step.get("marker", ""), "items": items}

    def _step_rime_table(self, step: dict, where: str) -> dict:
        """Mỗi hàng gồm vần mới và từ chứa vần đó; chỉ tô vần của hàng."""
        items = []
        for k, row in enumerate(step["rows"]):
            row_where = f"{where}.rows[{k}]"
            rime, word = row["rime"], row["word"]
            result = spell_rime(rime)
            if len(result.parts) != 3 or result.parts[-1].kind != "join":
                raise self.error(row_where, f"vần {rime!r} phải đánh vần thành nguyên âm, âm cuối và vần")
            items.append({"text": rime, "audio": self._audio(audio_for(rime), row_where),
                          "role": "rime", "row": k, "spells": [self._spell(result, row_where)]})
            spans = []
            for tok, start in tokens(word):
                syl = split_syllable(tok)
                if syl.rime == strip_tone(rime.lower()):
                    spans.append({"s": start + len(syl.onset), "n": len(tok) - len(syl.onset)})
            items.append({"text": word, "audio": self._audio(text_audio(word), row_where),
                          "role": "word", "row": k, "hl": spans,
                          "spells": self._spells_of(word, row_where)})
        return {"type": "rime_table", "marker": step.get("marker", ""), "items": items}

    def _step_rime_grid(self, step: dict, where: str) -> dict:
        """Bảng ôn các vần (bài 79): hàng đầu là âm cuối, mỗi hàng tiếp là nguyên âm và các ô vần."""
        finals = list(step["finals"])
        items: list[dict] = [{"text": final, "role": "final", "col": c} for c, final in enumerate(finals)]
        for r, row in enumerate(step["rows"]):
            vowel, cells = row["vowel"], list(row["cells"])
            if len(cells) != len(finals):
                raise self.error(where, f"hàng {vowel!r} có {len(cells)} ô, khác số âm cuối ({len(finals)})")
            items.append({"text": vowel, "role": "vowel", "row": r})
            for c, cell in enumerate(cells):
                if not cell:
                    continue
                spells = []
                for rime in (part.strip() for part in cell.split(" - ")):
                    res = spell_rime(rime)
                    if not res.parts:
                        raise self.error(where, f"không đánh vần được vần {rime!r}")
                    spells.append(self._spell(res, where))
                items.append({"text": cell, "role": "cell", "row": r, "col": c, "spells": spells})
        return {"type": "rime_grid", "items": items}

    def _step_letter_pairs(self, step: dict, where: str) -> dict:
        items = []
        for k, letter in enumerate(step["letters"]):
            item_where = f"{where}.items[{k}]"
            if letter == "q":
                self._note(item_where, Q_NOTE)
            items.append({"text": letter, "upper": letter.upper(), "audio": self._audio(audio_for(letter), item_where),
                          "role": "pair", "row": k // _PAIR_COLUMNS, "col": k % _PAIR_COLUMNS})
        return {"type": "letter_pairs", "items": items}

    def _step_rule(self, step: dict, where: str) -> dict:
        """Luật chính tả in trên trang (k, gh, ngh chỉ ghép với e, ê, i): mỗi dòng đọc liền như một câu."""
        items = [{"text": line, "audio": self._sentence_audio(line, f"{where}.items[{k}]"), "role": "line"}
                 for k, line in enumerate(step["lines"])]
        return {"type": "rule", "marker": step.get("marker", ""), "items": items}

    def _sentence_audio(self, text: str, where: str) -> str:
        """Mã âm thanh `cau_bNN_kk` kế tiếp cho một câu (hoặc dòng luật) đọc liền."""
        self.sentence_count += 1
        audio_id = f"cau_b{self.nn}_{self.sentence_count:02d}"
        return self._register_audio(audio_id, text, _SENTENCE_KIND, where)

    def _step_words(self, step: dict, where: str) -> dict:
        items = []
        for j, item in enumerate(step["items"]):
            item_where = f"{where}.items[{j}]"
            text = item["text"]
            out = {"text": text, "audio": self._audio(text_audio(text), item_where)}
            if item.get("image"):
                out["image"] = self._image(item["image"], item_where)
                self.image_text.setdefault(item["image"], text)
            if item.get("note"):
                out["note"] = item["note"]
            out["hl"] = self._highlights(text)
            to_spell = item["spell"] if "spell" in item else syllables(text)
            out["spells"] = [self._spell(spell_syllable(s), item_where) for s in to_spell]
            items.append(out)
        return {"type": "words", "marker": step.get("marker", ""), "items": items}

    def _step_reading(self, step: dict, where: str) -> dict:
        """Mỗi hàng là danh sách chữ, hoặc `{"label": …, "items": […]}` khi hàng có nhãn ở đầu (bài ôn tập)."""
        items, labels = [], []
        for row, texts in enumerate(step["rows"]):
            label = ""
            if isinstance(texts, dict):
                label, texts = texts.get("label", ""), texts["items"]
            if not isinstance(texts, list):
                raise self.error(where, f"hàng {row} phải là danh sách chữ, không phải {texts!r}")
            labels.append(label)
            for text in texts:
                item_where = f"{where}.items[{len(items)}]"
                items.append({"text": text, "audio": self._audio(text_audio(text), item_where), "row": row,
                              "spells": self._spells_of(text, item_where)})
        return {"type": "reading", "marker": step.get("marker", ""), "labels": labels, "items": items}

    def _step_sentence(self, step: dict, where: str) -> dict:
        text = step["text"]
        words = syllables(text)
        if not words:
            raise self.error(where, "câu không có tiếng nào")
        audio_id = self._sentence_audio(text, where)
        items = []
        for j, word in enumerate(words):
            item_where = f"{where}.items[{j}]"
            items.append({"text": word, "audio": self._audio(text_audio(word), item_where),
                          "hl": self._highlights(word) if self.colour_sentences else [],
                          "spells": [self._spell(spell_syllable(word), item_where)]})
        return {"type": "sentence", "marker": step.get("marker", ""), "text": text, "audio": audio_id,
                "items": items}

    _STEPS = {
        "unit": _step_unit,
        "keyword": _step_keyword,
        "analyze": _step_analyze,
        "spell": _step_spell,
        "tone_intro": _step_tone_intro,
        "tone_attach": _step_tone_attach,
        "picture": _step_picture,
        "words": _step_words,
        "reading": _step_reading,
        "sentence": _step_sentence,
        "tone_table": _step_tone_table,
        "letter_grid": _step_letter_grid,
        "combine_table": _step_combine_table,
        "rime_table": _step_rime_table,
        "rime_grid": _step_rime_grid,
        "letter_pairs": _step_letter_pairs,
        "rule": _step_rule,
    }

    def _build_part1(self) -> list[dict]:
        steps = []
        for i, step in enumerate(self.src["part1"]):
            where = f"part1[{i}]"
            with self._located(where):
                kind = step["type"]
                build = self._STEPS.get(kind)
                if build is None:
                    raise self.error(where, f"type lạ {kind!r}")
                steps.append(build(self, step, where))
        return steps

    # ---- Phần 2 ----

    def _answer_index(self, options: list, answer, where: str) -> int:
        if answer not in options:
            raise self.error(where, f"đáp án {answer!r} không nằm trong options {options!r}")
        return options.index(answer)

    def _round_listen_choose(self, rd: dict, where: str) -> dict:
        answer, texts = rd["answer"], list(rd["options"])
        index = self._answer_index(texts, answer, where)
        return {"prompt_audio": self._audio(audio_for(answer), where),
                "options": [_option(text=t, audio=self._audio(audio_for(t), where)) for t in texts], "answer": index}

    def _round_look_tone(self, rd: dict, where: str) -> dict:
        model, keys = rd["model"], list(rd["options"])
        for key in keys:
            if key not in TONE_INFO:
                raise self.error(where, f"dấu không hợp lệ trong options: {key!r}")
        tone = split_syllable(model).tone
        if tone not in keys:
            raise self.error(where, f"dấu của chữ mẫu {model!r} ({tone}) không có trong options {keys!r}")
        return {"prompt_text": model, "base_text": strip_tone(model),
                "options": [_option(text=TONE_INFO[k][1], tone=k) for k in keys], "answer": keys.index(tone)}

    def _round_compose(self, rd: dict, where: str) -> dict:
        word, template, answer, texts = rd["word"], rd["template"], rd["answer"], list(rd["options"])
        index = self._answer_index(texts, answer, where)
        if template.replace("_", answer) != word:
            raise self.error(where, f"khuôn {template!r} điền {answer!r} không ra từ {word!r}")
        image = rd.get("image", "")
        if image:
            self._image(image, where)
        return {"prompt_text": template, "prompt_audio": self._audio(text_audio(word), where), "image": image,
                "options": [_option(text=t, audio=self._audio(audio_for(t), where)) for t in texts], "answer": index}

    def _round_listen_picture(self, rd: dict, where: str) -> dict:
        word, answer, image_ids = rd["word"], rd["answer"], list(rd["options"])
        index = self._answer_index(image_ids, answer, where)
        options = []
        for image in image_ids:
            self._image(image, where)
            text = self.image_text.get(image)
            if text is None:
                raise self.error(where, f"tranh {image!r} không gắn với chữ nào ở Phần 1")
            options.append(_option(text=text, image=image))
        answer_text = self.image_text[answer]
        if _normalized_say(answer_text) != _normalized_say(word):
            raise self.error(where, f"tranh đáp án {answer!r} là chữ {answer_text!r}, "
                                    f"không khớp với từ đề {word!r}")
        if rd.get("prompt"):
            return {"instruction_audio": RIDDLE_INSTRUCTION_AUDIO,
                    "prompt_audio": self._sentence_audio(rd["prompt"], where),
                    "options": options, "answer": index}
        return {"prompt_audio": self._audio(text_audio(word), where), "options": options, "answer": index}

    def _round_match_case(self, rd: dict, where: str) -> dict:
        model, answer, texts = rd["model"], rd["answer"], list(rd["options"])
        index = self._answer_index(texts, answer, where)
        if answer != model.upper():
            raise self.error(where, f"đáp án {answer!r} không phải chữ hoa của {model!r}")
        return {"prompt_text": model, "options": [_option(text=t) for t in texts], "answer": index}

    _ROUNDS = {
        "listen_choose": _round_listen_choose,
        "look_tone": _round_look_tone,
        "compose": _round_compose,
        "listen_picture": _round_listen_picture,
        "match_case": _round_match_case,
    }

    def _build_part2(self) -> list[dict]:
        rounds = []
        for i, exercise in enumerate(self.src["part2"]):
            where = f"part2[{i}]"
            with self._located(where):
                kind = exercise["kind"]
                build = self._ROUNDS.get(kind)
                if build is None:
                    raise self.error(where, f"kind lạ {kind!r}")
                tag = exercise.get("tag", "")
                if "rounds" in exercise:
                    authored = [(rd, f"{where}.rounds[{j}]") for j, rd in enumerate(exercise["rounds"])]
                else:
                    authored = [(exercise, where)]
                for rd, round_where in authored:
                    with self._located(round_where):
                        rounds.append(_make_round(kind, tag, **build(self, rd, round_where)))
        return rounds

    # ---- cả bài ----

    def build(self) -> BuildResult:
        src = self.src
        for field in _REQUIRED_FIELDS:
            if field not in src:
                raise self.error(_HEAD, f"thiếu trường {field!r}")
        with self._located(_HEAD):
            if not isinstance(src["lesson_no"], int):
                raise self.error(_HEAD, f"lesson_no phải là số nguyên: {src['lesson_no']!r}")
            self.nn = f"{src['lesson_no']:02d}"
            self.new_units = frozenset(src["new_units"])
            # Sách chỉ tô vần mới trong câu ở phần vần; câu ở bài âm mới không tô chữ mới.
            self.colour_sentences = src["type"] in _RIME_LESSON_TYPES
            in_app = src.get("in_app", True)
            if not isinstance(in_app, bool):
                raise self.error(_HEAD, f"in_app phải là true/false: {in_app!r}")
        part1 = self._build_part1()
        part2 = self._build_part2()

        review = src.get("review") or {}
        with self._located("review.notes"):
            source_notes = [{"where": n["where"], "note": n["note"]} for n in review.get("notes", [])]
        lesson = {
            "schema": SCHEMA,
            "lesson_id": src["lesson_id"],
            "book": src["book"],
            "lesson_no": src["lesson_no"],
            "type": src["type"],
            "title": src["title"],
            "in_app": in_app,
            "new_units": list(src["new_units"]),
            "source": dict(src["source"]),
            "review": {"status": review.get("status", "chua_duyet"), "can_duyet": source_notes + self.can_duyet},
            "part1": part1,
            "part2": part2,
        }
        return BuildResult(lesson, self.audio, self.images)


def build_lesson(src: dict) -> BuildResult:
    """Dựng một bài từ nguồn. Không sửa `src`; chuỗi được chuẩn hóa NFC trên bản sao."""
    return _Builder(_nfc_deep(src)).build()


def load_sources(src_dir) -> list[dict]:
    """Đọc mọi `*.json` trong thư mục (theo thứ tự tên file), chuẩn hóa NFC mọi chuỗi."""
    sources = []
    for path in sorted(Path(src_dir).glob("*.json")):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError) as e:  # JSONDecodeError và UnicodeDecodeError đều là ValueError
            raise BuildError(f"{path.stem} {path.name}: không đọc được: {e}") from e
        if not isinstance(data, dict):
            raise BuildError(f"{path.stem} {path.name}: nguồn bài phải là một đối tượng JSON")
        sources.append(_nfc_deep(data))
    return sources


def _write_json(path: Path, data: dict) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def build_all(src_dir, out_dir) -> list[BuildResult]:
    """Dựng mọi bài trong `src_dir`, ghi `<lesson_id>.json` và `index.json` vào `out_dir`."""
    results = [build_lesson(src) for src in load_sources(src_dir)]
    seen: set[str] = set()
    for result in results:
        lesson_id = result.lesson["lesson_id"]
        if lesson_id in seen:
            raise BuildError(f"{lesson_id} {_HEAD}: trùng lesson_id giữa hai nguồn bài")
        seen.add(lesson_id)

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for result in results:
        _write_json(out / f"{result.lesson['lesson_id']}.json", result.lesson)
    # Bài `in_app: false` (bài mẫu 42) vẫn được dựng để test nạp được, nhưng không hiện trong danh sách bài.
    by_no = sorted((r.lesson for r in results if r.lesson["in_app"]), key=lambda lesson: lesson["lesson_no"])
    index = {"lessons": [{"lesson_id": l["lesson_id"], "lesson_no": l["lesson_no"], "title": l["title"],
                          "type": l["type"]} for l in by_no]}
    _write_json(out / "index.json", index)
    return results
