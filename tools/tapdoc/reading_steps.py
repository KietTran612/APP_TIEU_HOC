"""Dựng các bước Phần 1 của phần Tập đọc (thiết kế tập 2, mục 7–8).

Mỗi hàm nhận `(b, step, where)`, với `b` là bộ dựng bài (`build._Builder`), và trả về bước đã dựng.
Bộ dựng giữ danh sách câu của bài đọc hiện tại (`b.reading`): đặt lại ở mỗi bước `title`, thêm vào ở mỗi bước
`sentence`. Bước `passage` và `memorize` dùng lại đúng mã âm thanh của các câu đó.
"""

import re

from .ids import text_audio
from .spelling import spell_syllable
from .viet import TONE_INFO, nfc, split_syllable, strip_tone, tokens

_TONE_BY_NAME = {name: key for key, (name, _) in TONE_INFO.items()}
_MATCH_KINDS = ("rime", "onset", "tone", "word")  # word: danh sách tiếng đúng (lớp 2, Claude chọn)
_QUESTION_KIND = "cau"  # câu hỏi đọc như câu (cùng thông số giọng), mã riêng hoi_bNN_kk


def question_audio(b, text: str, where: str) -> str:
    b.question_count += 1
    return b._register_audio(f"hoi_b{b.nn}_{b.question_count:02d}", text, _QUESTION_KIND, where)


def _word_items(b, sentences: list[dict], where: str, spell: bool = True) -> list[dict]:
    """Mỗi tiếng của các câu: chữ, âm thanh, đánh vần, `row` là chỉ số câu, `col` là chỉ số tiếng trong câu."""
    items = []
    for row, sentence in enumerate(sentences):
        for col, (tok, _) in enumerate(tokens(sentence["text"])):
            item_where = f"{where}.rows[{row}].items[{col}]"
            items.append({"text": tok, "audio": b._audio(text_audio(tok), item_where), "row": row, "col": col,
                          "spells": [b._spell(spell_syllable(tok), item_where)] if spell else []})
    return items


def _sentence_rows(sentences: list[dict], breaks=()) -> list[dict]:
    rows, paragraph = [], 0
    for k, sentence in enumerate(sentences):
        if k in breaks and k > 0:
            paragraph += 1
        rows.append({"text": sentence["text"], "audio": sentence["audio"], "row": paragraph})
    return rows


def _current_reading(b, where: str) -> list[dict]:
    if not b.reading:
        raise b.error(where, "chưa có câu nào của bài đọc (cần các bước sentence sau bước title)")
    return list(b.reading)


def step_title(b, step: dict, where: str) -> dict:
    # Tên bài (hoặc tên phần trang chính tả) mở một bài đọc mới; câu lệnh giữa các câu hỏi ("instruction") thì không.
    if not step.get("instruction"):
        b.reading = []
    sub = step.get("sub", "")
    return {"type": "title", "marker": step.get("marker", ""), "text": step["text"],
            "audio": b._sentence_audio(step["text"], where), "labels": [sub] if sub else []}


def step_passage(b, step: dict, where: str) -> dict:
    sentences = _current_reading(b, where)
    layout = step.get("layout", "prose")
    if layout not in ("poem", "prose"):
        raise b.error(where, f"layout phải là poem hoặc prose: {layout!r}")
    items = _word_items(b, sentences, where)
    return {"type": "passage", "marker": step.get("marker", ""),
            "rows": _sentence_rows(sentences, set(step.get("breaks", []))), "items": items,
            "labels": [step.get("author", ""), layout]}


def _match(b, match, where: str) -> tuple[str, frozenset[str]]:
    if not isinstance(match, dict) or len(match) != 1 or next(iter(match)) not in _MATCH_KINDS:
        raise b.error(where, f"match cần đúng một khoá trong {', '.join(_MATCH_KINDS)}: {match!r}")
    kind, values = next(iter(match.items()))
    values = [nfc(v).lower() for v in values]
    if kind == "tone":
        unknown = [v for v in values if v not in _TONE_BY_NAME]
        if unknown:
            raise b.error(where, f"tên dấu không biết: {unknown!r}")
        values = [_TONE_BY_NAME[v] for v in values]
    return kind, frozenset(values)


def _hit(kind: str, values: frozenset[str], tok: str) -> dict | None:
    """Vị trí phần được hỏi trong tiếng (tương đối đầu tiếng), hoặc None nếu tiếng không khớp."""
    if kind == "word":
        return {"s": 0, "n": len(tok)} if tok.lower() in values else None
    syl = split_syllable(tok)
    # Sách coi chữ u của "qu" là âm đệm của vần: "quyển" có vần uyên, "Quỳnh" có vần uynh.
    onset, rime = ("q", "u" + syl.rime) if syl.onset == "qu" else (syl.onset, syl.rime)
    if kind == "rime" and (strip_tone(rime) in values or strip_tone(syl.rime) in values):
        start = len(onset) if strip_tone(rime) in values else len(syl.onset)
        return {"s": start, "n": len(tok) - start}
    if kind == "onset" and syl.onset in values:
        return {"s": 0, "n": len(syl.onset)}
    if kind == "tone" and syl.tone in values:
        return {"s": 0, "n": len(tok)}
    return None


def step_find_words(b, step: dict, where: str) -> dict:
    if "text" in step:
        sentences = [{"text": t, "audio": b._sentence_audio(t, f"{where}.text[{k}]")}
                     for k, t in enumerate(step["text"])]
    else:
        reading = _current_reading(b, where)
        picked = step.get("in")
        sentences = reading if picked is None else [reading[k] for k in picked]
    kind, values = _match(b, step.get("match"), where)
    items = _word_items(b, sentences, where, spell=step.get("spell", True))
    found = set()
    for item in items:
        hit = _hit(kind, values, item["text"])
        if hit is None:
            item["role"], item["hl"] = "other", []
        else:
            item["role"], item["hl"] = "target", [hit]
            found.add(item["text"].lower())
    if not found:
        raise b.error(where, f"không có tiếng nào khớp {step.get('match')!r}")
    count = step.get("count", 0)
    if count > len(found):
        raise b.error(where, f"count {count} lớn hơn số tiếng khớp ({len(found)})")
    return {"type": "find_words", "marker": step.get("marker", ""), "text": step["question"],
            "audio": question_audio(b, step["question"], where), "rows": _sentence_rows(sentences),
            "items": items, "need": count if count > 0 else len(found)}


def step_question(b, step: dict, where: str) -> dict:
    built = {"type": "question", "marker": step.get("marker", ""), "text": step["text"],
             "audio": question_audio(b, step["text"], where)}
    if step.get("lines"):
        # Các câu sách in kèm câu hỏi (lớp 2): hiện dưới câu hỏi, chạm để nghe.
        built["rows"] = [{"text": t, "audio": b._sentence_audio(t, f"{where}.lines[{k}]")}
                         for k, t in enumerate(step["lines"])]
    return built


def step_combine_words(b, step: dict, where: str) -> dict:
    """Ghép chữ rồi đọc lên (lớp 2): chữ gốc (`text`) ghép trước hoặc sau từng chữ cho sẵn (`items[].part`)."""
    base = nfc(step["base"])
    items = []
    for k, entry in enumerate(step["items"]):
        item_where = f"{where}.items[{k}]"
        part, at = nfc(entry["with"]), entry.get("at", "after")
        if at not in ("before", "after"):
            raise b.error(item_where, f"at phải là before hoặc after: {at!r}")
        text = f"{base} {part}" if at == "after" else f"{part} {base}"
        items.append({"text": text, "audio": b._audio(text_audio(text), item_where), "part": part, "role": at})
    if not items:
        raise b.error(where, "combine_words cần ít nhất một chữ để ghép")
    return {"type": "combine_words", "marker": step.get("marker", ""), "text": base,
            "audio": b._audio(text_audio(base), where), "items": items}


_BLANK_RE = re.compile(r"\[([^\]]+)\]")


def step_fill_passage(b, step: dict, where: str) -> dict:
    """Điền từ vào đoạn văn (lớp 2): ô viết "[đáp án]" khi có `bank`, "[đáp án|nhiễu|nhiễu]" khi không có.

    `rows`: các câu đủ chữ (âm thanh đọc cả câu); `items`: các mảnh chữ (`role` text) và ô (`role` blank, có
    `answer`, `choices`) theo thứ tự, `row` là chỉ số câu; `labels`: các từ cho sẵn (rỗng khi mỗi ô có lựa chọn riêng).
    """
    bank = [nfc(w) for w in step.get("bank", [])]
    rows, items, answers = [], [], []
    for k, raw in enumerate(step["text"]):
        line_where = f"{where}.text[{k}]"
        line, full, pos = nfc(raw), [], 0
        for m in _BLANK_RE.finditer(line):
            if line[pos:m.start()].strip():
                items.append({"text": line[pos:m.start()].strip(), "row": k, "role": "text"})
            full.append(line[pos:m.start()])
            options = [o.strip() for o in m.group(1).split("|")]
            answer = options[0]
            if bank:
                if len(options) > 1:
                    raise b.error(line_where, f"đã có bank thì ô không ghi lựa chọn riêng: {m.group(0)!r}")
                if answer not in bank:
                    raise b.error(line_where, f"đáp án {answer!r} không có trong bank {bank!r}")
                choices = list(bank)
            else:
                if len(options) < 2:
                    raise b.error(line_where, f"không có bank thì ô cần lựa chọn riêng [đáp án|nhiễu]: {m.group(0)!r}")
                choices = options
            items.append({"text": answer, "row": k, "role": "blank", "answer": answer, "choices": choices})
            full.append(answer)
            answers.append(answer)
            pos = m.end()
        if line[pos:].strip():
            items.append({"text": line[pos:].strip(), "row": k, "role": "text"})
        full.append(line[pos:])
        text = "".join(full)
        rows.append({"text": text, "audio": b._sentence_audio(text, line_where), "row": k})
    if not answers:
        raise b.error(where, "fill_passage cần ít nhất một ô trống")
    for word in set(answers) if bank else ():
        if answers.count(word) > bank.count(word):
            raise b.error(where, f"{word!r} điền {answers.count(word)} ô nhưng bank chỉ có {bank.count(word)}")
    return {"type": "fill_passage", "marker": step.get("marker", ""), "labels": bank, "rows": rows, "items": items}


def step_choose_line(b, step: dict, where: str) -> dict:
    """Chọn các dòng đúng yêu cầu ("dòng nào viết chưa thành câu?"): dòng đúng `role` target; đáp án Claude soạn."""
    lines, answers = step["lines"], step.get("answers", [])
    if not answers:
        raise b.error(where, "choose_line cần ít nhất một đáp án")
    bad = [a for a in answers if not isinstance(a, int) or isinstance(a, bool) or not 0 <= a < len(lines)]
    if bad:
        raise b.error(where, f"answers ngoài danh sách dòng: {bad!r}")
    items = [{"text": t, "audio": b._sentence_audio(t, f"{where}.lines[{k}]"),
              "role": "target" if k in answers else "other"} for k, t in enumerate(lines)]
    return {"type": "choose_line", "marker": step.get("marker", ""), "text": step["question"],
            "audio": question_audio(b, step["question"], where), "items": items, "need": len(set(answers))}


def step_memorize(b, step: dict, where: str) -> dict:
    sentences = _current_reading(b, where)
    items = _word_items(b, sentences, where)
    for item in items:
        # Tiếng đầu dòng luôn hiện; các tiếng sau lần lượt mức 1, 2, 3 (ẩn dần khoảng 1/3, 2/3, hết).
        item["level"] = 0 if item["col"] == 0 else 1 + (item["col"] - 1) % 3
    built = {"type": "memorize", "marker": step.get("marker", ""), "rows": _sentence_rows(sentences), "items": items}
    if step.get("question"):
        built["text"] = step["question"]
        built["audio"] = question_audio(b, step["question"], where)
    return built


def step_fill_blank(b, step: dict, where: str) -> dict:
    mode, choices = step.get("mode", "letter"), [nfc(c) for c in step["choices"]]
    if mode not in ("letter", "tone"):
        raise b.error(where, f"mode phải là letter hoặc tone: {mode!r}")
    items = []
    for k, entry in enumerate(step["items"]):
        item_where = f"{where}.items[{k}]"
        word, blank, fill = nfc(entry["word"]), nfc(entry["blank"]), nfc(entry["fill"])
        if fill not in choices:
            raise b.error(item_where, f"{fill!r} không có trong choices {choices!r}")
        starts = [start for tok, start in tokens(word) if tok == blank]
        if not starts:
            raise b.error(item_where, f"tiếng {blank!r} không có trong {word!r}")
        if mode == "tone":
            if split_syllable(blank).tone != _TONE_BY_NAME.get(fill):
                raise b.error(item_where, f"tiếng {blank!r} không mang dấu {fill!r}")
            hl = {"s": starts[0], "n": len(blank)}
        else:
            at = blank.find(fill)
            if at < 0:
                # Lựa chọn của sách không dấu ("ua hay au"), chữ cần điền mang dấu ("lúa"): so khi đã bỏ dấu thanh.
                at = strip_tone(blank).find(strip_tone(fill))
            if at < 0:
                raise b.error(item_where, f"{fill!r} không có trong tiếng {blank!r}")
            hl = {"s": starts[0] + at, "n": len(fill)}
        items.append({"role": "blank", "text": word, "audio": b._audio(text_audio(word), item_where),
                      "answer": fill, "hl": [hl]})
    return {"type": "fill_blank", "marker": step.get("marker", ""), "labels": choices, "items": items}


def step_riddle_answer(b, step: dict, where: str) -> dict:
    answer, image = step["answer"], step["image"]
    options = list(step["options"])
    if any(o["image"] == image for o in options):
        raise b.error(where, f"tranh đáp án {image!r} không được nằm trong phương án nhiễu")
    b._image(image, where)
    b.image_text.setdefault(image, answer)
    for k, option in enumerate(options):
        b._image(option["image"], f"{where}.options[{k}]")
        b.image_text.setdefault(option["image"], option["text"])
    images = [o["image"] for o in options]
    images.insert(len(answer) % (len(images) + 1), image)  # chỗ đáp án cố định theo chữ, không ngẫu nhiên
    return {"type": "riddle_answer", "marker": step.get("marker", ""), "text": answer,
            "audio": b._audio(text_audio(answer), where), "image": image,
            "items": [{"role": "option", "image": img} for img in images]}


STEPS = {
    "title": step_title,
    "passage": step_passage,
    "find_words": step_find_words,
    "question": step_question,
    "memorize": step_memorize,
    "fill_blank": step_fill_blank,
    "riddle_answer": step_riddle_answer,
    "combine_words": step_combine_words,
    "fill_passage": step_fill_passage,
    "choose_line": step_choose_line,
}
