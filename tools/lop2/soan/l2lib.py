"""Khuôn dựng nguồn bài lớp 2 (content/src/tv2_t1_bNNN.json) cho session TV2 tập một."""
import json
import re
from pathlib import Path

SRC = Path(__file__).resolve().parents[3] / "content" / "src"
TOC = {r["lesson_no"]: r for r in json.loads(
    (Path(__file__).parent / "toc_l2.json").read_text(encoding="utf-8"))}

KS_NO_SPELL = ("Lớp 2: bé đã đọc trơn, nên chạm vào tiếng thì app chỉ đọc tiếng đó, không đánh vần như lớp 1.")
KS_ORAL = "Câu hỏi hiểu bài, câu hỏi tìm từ, đặt câu: bé trả lời miệng cùng bố mẹ, app không chấm."
KS_SPLIT = "Câu dài được tách thành nhiều bước theo dấu phẩy để bé đọc từng đoạn ngắn; bước \"Đọc cả bài\" vẫn đủ cả câu."
KS_WRITE = "Phần chép, viết vào vở không có trong app: bé viết vào vở cùng bố mẹ. Mục \"Viết đúng\" thành bước đọc."
KS_HTL = "Bài học thuộc lòng: app thêm bước \"Ẩn bớt\" để bé tập đọc thuộc (sách chỉ ghi \"Học thuộc lòng\")."


def scan_of(page):
    if page in (56, 57):
        return "030"
    if page in (58, 59):
        return "029"
    return f"{page // 2 + 1:03d}"


def lesson(no, pages, part1, part2, images=None, notes=(), review=(), title=None, **extra):
    """Ghi file nguồn; mục lục (tuần, chủ điểm, loại, số bài) lấy từ toc_l2.json."""
    t = TOC[no]
    # Ghi chú duyệt viết theo chỉ số bước trước khi tách câu dài / chia quy tắc: dời sang chỉ số thật.
    old_to_new, old = {}, 0
    for new, step in enumerate(part1):
        if not step.pop("_cont", False):
            old_to_new[old] = new
            old += 1
    fixed = []
    for where, note in review:
        if where.startswith("part1[") and where.endswith("]"):
            where = f"part1[{old_to_new[int(where[6:-1])]}]"
        fixed.append((where, note))
    review = fixed
    src = {
        "lesson_id": f"tv2_t1_b{no}", "book": "tv2_t1_2001", "lesson_no": no, "type": t["type"],
        "title": title or t["title"], "week": t["week"], "theme": t["theme"],
    }
    if "td_no" in t:
        src["td_no"] = t["td_no"]
    src.update({
        "source": {"pages": list(pages), "scan_file": scan_of(pages[0]), "verification": "page_verified"},
        "new_units": [], "images": dict(images or {}),
        "review": {"status": "chua_duyet", "notes": [{"where": w, "note": n} for w, n in review]},
        "notes": [{"kind": k, "text": x} for k, x in notes],
        "part1": part1, "part2": part2,
    })
    src.update(extra)
    path = SRC / f"tv2_t1_b{no}.json"
    path.write_text(json.dumps(src, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return path


# ---- bước ----

MAX_SUB = 70  # dòng phụ của tên bài dài hơn thì tràn khung (smoke test lớp 2)
MAX_WORDS = 15  # câu dài hơn thì tách theo dấu phẩy (màn đọc từng câu chứa tối đa khoảng 16 tiếng)
MAX_RULE_LINES = 3  # màn quy tắc / giải nghĩa chứa tối đa 3 dòng


def title(text, sub=""):
    if len(sub) > MAX_SUB and ": " in sub:
        sub = sub.split(": ")[0] + "."  # danh sách từ cho sẵn đã hiện thành thẻ
    assert len(sub) <= MAX_SUB, sub
    return {"type": "title", "text": text, **({"sub": sub} if sub else {})}


def _words(text):
    return len(re.findall(r"[^\s,.!?:;\"()\-–]+", text))


def split_long(text):
    """Câu quá dài cho màn đọc từng câu: tách theo dấu phẩy thành các đoạn ≤ MAX_WORDS tiếng, giữ thứ tự."""
    if _words(text) <= MAX_WORDS:
        return [text]
    parts = re.split(r"(?<=,)\s+", text)
    out, cur = [], ""
    for part in parts:
        trial = f"{cur} {part}".strip()
        if cur and _words(trial) > MAX_WORDS:
            out.append(cur)
            cur = part
        else:
            cur = trial
    out.append(cur)
    final = []
    for chunk in out:
        if _words(chunk) <= MAX_WORDS + 1:
            final.append(chunk)
            continue
        words = chunk.split(" ")  # không có dấu phẩy: tách đôi ở giữa
        mid = len(words) // 2
        final += [" ".join(words[:mid]), " ".join(words[mid:])]
    return final


def sentences(*texts):
    # Mảnh thứ hai trở đi đánh dấu "_cont": chỉ số bước trong ghi chú duyệt viết theo câu gốc, lesson() tự dời.
    return [dict({"type": "sentence", "text": piece}, **({"_cont": True} if k else {}))
            for t in texts for k, piece in enumerate(split_long(t))]


def passage(layout, author="", breaks=()):
    st = {"type": "passage", "layout": layout}
    if author:
        st["author"] = author
    if breaks:
        st["breaks"] = list(breaks)
    return st


def _chunks(lines):
    lines = list(lines)
    return [lines[k:k + MAX_RULE_LINES] for k in range(0, len(lines), MAX_RULE_LINES)]


def glossary(*lines):
    """Danh sách bước (dùng *glossary(...)): mỗi bước tối đa 3 dòng."""
    return [dict({"type": "rule", "marker": ":", "lines": c}, **({"_cont": True} if k else {}))
            for k, c in enumerate(_chunks(lines))]


def rule(*lines):
    return [dict({"type": "rule", "marker": "", "lines": c}, **({"_cont": True} if k else {}))
            for k, c in enumerate(_chunks(lines))]


def q(text, marker="", lines=()):
    st = {"type": "question", "text": text}
    if marker:
        st["marker"] = marker
    if lines:
        st["lines"] = list(lines)
    return st


def words(*texts, marker=""):
    return {"type": "words", "marker": marker, "items": [{"text": t} for t in texts]}


def picture(image, say, word):
    return {"type": "picture", "image": image, "say": say, "word": word}


def fill(choices, *items, mode="letter"):
    return {"type": "fill_blank", "mode": mode, "choices": list(choices),
            "items": [{"word": w, "blank": b, "fill": f} for w, b, f in items]}


def combine(base, *parts, at="after"):
    return {"type": "combine_words", "base": base, "items": [{"with": p, "at": at} for p in parts]}


def fill_passage(text, bank=()):
    st = {"type": "fill_passage", "text": list(text)}
    if bank:
        st["bank"] = list(bank)
    return st


def choose(question, lines, answers, marker=""):
    st = {"type": "choose_line", "question": question, "lines": list(lines), "answers": list(answers)}
    if marker:
        st["marker"] = marker
    return st


def find(question, match, sentences_in=None, text=None, marker=""):
    st = {"type": "find_words", "question": question, "match": match}
    if sentences_in is not None:
        st["in"] = list(sentences_in)
    if text is not None:
        st["text"] = list(text)
    if marker:
        st["marker"] = marker
    return st


def memorize():
    return {"type": "memorize"}


def listen(*rounds):
    """Phần 2: mỗi lượt (đáp án, nhiễu 1, nhiễu 2)."""
    return [{"kind": "listen_choose", "rounds": [{"answer": r[0], "options": list(r)} for r in rounds]}]


def prose(author, *paragraphs, layout="prose"):
    """Các đoạn (mỗi đoạn là danh sách câu) → bước câu + bước đọc cả bài với chỗ xuống đoạn tự tính."""
    steps, breaks, k = [], [], 0
    for para in paragraphs:
        if k:
            breaks.append(k)
        para_steps = sentences(*para)
        steps += para_steps
        k += len(para_steps)
    return steps + [passage(layout, author, breaks=breaks)]
