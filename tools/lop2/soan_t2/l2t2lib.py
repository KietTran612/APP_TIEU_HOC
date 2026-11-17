"""Khuôn dựng nguồn bài Tiếng Việt 2 tập hai (content/src/tv2_t2_bNNN.json): dùng lại các bước của tập một
(`tools/lop2/soan/l2lib.py`), chỉ đổi mã bài, quyển, mục lục và ảnh scan (thiết kế TV2 tập hai mục 7)."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "soan"))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]))
from tapdoc.ids import telex  # noqa: E402
from l2lib import *  # noqa: E402,F401,F403  (title, sentences, prose, glossary, rule, q, words, picture, fill, …)
from l2lib import KS_HTL, KS_NO_SPELL, KS_ORAL, KS_SPLIT, KS_WRITE, SRC  # noqa: E402,F401
from toc_t2 import image_of  # noqa: E402

TOC = {r["lesson_no"]: r for r in json.loads((HERE / "toc_t2.json").read_text(encoding="utf-8"))}

KS_REAL = "Sách vẽ {who}; app vẽ {what} (không vẽ người thật)."
KS_TLC = "Câu hỏi về bài đã đọc: bé trả lời miệng cùng bố mẹ, app hiện lại tranh của bài đó."
KS_DAT_CAU = "Đặt câu: bé nói câu của mình cùng bố mẹ, app không chấm. Các từ cho sẵn hiện thành thẻ, chạm để nghe."
KS_XEP_TEN = "Xếp tên theo thứ tự bảng chữ cái: bé xếp bằng miệng cùng bố mẹ (như tập một)."


def scan_of(page):
    return image_of(page)


def sentences(*texts):
    """Như tập một, thêm chỗ ngắt tay " | " cho câu dài: tách ở đó trước (đúng nhịp câu), rồi mới tách theo dấu phẩy.
    Câu không có dấu phẩy mà quá dài thì l2lib cắt đôi giữa chừng, có khi ngang qua hai câu thoại: ghi " | " để tránh."""
    out = []
    for t in texts:
        k = 0
        for part in t.split(" | "):
            for piece in split_long(part):
                out.append(dict({"type": "sentence", "text": piece}, **({"_cont": True} if k else {})))
                k += 1
    return out


def prose(author, *paragraphs, layout="prose"):
    """Như l2lib.prose nhưng dùng `sentences` có chỗ ngắt tay."""
    steps, breaks, k = [], [], 0
    for para in paragraphs:
        if k:
            breaks.append(k)
        para_steps = sentences(*para)
        steps += para_steps
        k += len(para_steps)
    return steps + [passage(layout, author, breaks=breaks)]


def img(no, word):
    """Mã tranh `img_b<số bài>_<telex>` như tập một."""
    return f"img_b{no}_{telex(word)}"


def picture_of(no):
    """(mã, mô tả) tranh đầu tiên của bài đọc `no` đã soạn: Tập làm văn "Trả lời câu hỏi" dùng lại tranh này."""
    images = json.loads((SRC / f"tv2_t2_b{no}.json").read_text(encoding="utf-8"))["images"]
    return next(iter(images.items()))


def combine_mixed(base, *items):
    """Ghép chữ, mỗi chữ ghép trước hay sau chữ gốc: combine_mixed("gãy", ("bẻ", "before"), ("gọn", "after"))."""
    return {"type": "combine_words", "base": base, "items": [{"with": w, "at": at} for w, at in items]}


def lesson(no, pages, part1, part2, images=None, notes=(), review=(), title=None, **extra):
    """Ghi file nguồn; mục lục (tuần, chủ điểm, loại, số bài) lấy từ toc_t2.json."""
    t = TOC[no]
    # Ghi chú duyệt viết theo chỉ số bước trước khi tách câu dài / chia quy tắc: dời sang chỉ số thật.
    old_to_new, old = {}, 0
    for new, step in enumerate(part1):
        if not step.pop("_cont", False):
            old_to_new[old] = new
            old += 1
    fixed = []
    for where, note in review:
        if where.startswith("@"):  # trỏ bước theo chữ đầu của câu hỏi / tên bước: "@4. Tìm những từ láy"
            hits = [k for k, st in enumerate(part1)
                    if str(st.get("question") or st.get("text") or "").startswith(where[1:])]
            assert len(hits) == 1, (no, where, hits)
            where = f"part1[{hits[0]}]"
        elif where.startswith("part1[") and where.endswith("]"):
            where = f"part1[{old_to_new[int(where[6:-1])]}]"
        fixed.append((where, note))
    src = {
        "lesson_id": f"tv2_t2_b{no}", "book": "tv2_t2_2002", "lesson_no": no, "type": t["type"],
        "title": title or t["title"], "week": t["week"], "theme": t["theme"],
    }
    if "td_no" in t:
        src["td_no"] = t["td_no"]
    src.update({
        "source": {"pages": list(pages), "scan_file": scan_of(pages[0]), "verification": "page_verified"},
        "new_units": [], "images": dict(images or {}),
        "review": {"status": "chua_duyet", "notes": [{"where": w, "note": n} for w, n in fixed]},
        "notes": [{"kind": k, "text": x} for k, x in notes],
        "part1": part1, "part2": part2,
    })
    src.update(extra)
    path = SRC / f"tv2_t2_b{no}.json"
    path.write_text(json.dumps(src, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return path
