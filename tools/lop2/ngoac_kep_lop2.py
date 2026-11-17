"""Ngoặc kép giữa câu: HoaiMy chèn một tiếng ngắn ở chỗ ngoặc kép ("với từ "can đảm"" → "với từ y can đảm",
"bố nói: "Ngày…" → "bố nói ở ngày…", ""Xắc" là" → "Sắc e là"; root nhận dạng đợt 1 TV2 tập hai, 17/11). Ngoặc kép
mở ở đầu câu thì không chèn. Sửa bằng chữ đọc riêng (`doc` trong content/tts/settings.json), chữ hiển thị giữ nguyên:
- kiểu a (root chọn 17/11, nghe tự nhiên, không thêm chỗ ngắt): bỏ mọi ngoặc kép;
- kiểu b (bản thử): ngoặc kép mở giữa câu thành dấu phẩy (sau dấu câu thì chỉ bỏ), bỏ ngoặc kép đóng.
Chỉ đổi chữ có ngoặc kép "giữa câu": mở mà không ở đầu chữ, hoặc đóng mà sau nó còn chữ.

Dùng (từ gốc repo): python tools/lop2/ngoac_kep_lop2.py [--t2] [--kieu a|b] [--ghi]   (mặc định kiểu a)
Không --ghi: chỉ liệt kê. Mã đã `dat` không đổi. Mã đã có chữ đọc riêng thì áp lên chữ đọc đó.
"""
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sach import only_book_ids, prefix  # noqa: E402

QUOTE = '"'
PUNCT = set(".,:;!?…()-–—")


def _is_open(text: str, i: int) -> bool:
    nxt = text[i + 1] if i + 1 < len(text) else ""
    prev = text[i - 1] if i else ""
    return bool(nxt) and not nxt.isspace() and nxt not in PUNCT and (not prev or prev.isspace() or prev in "(:")


def _mid(text: str, i: int, opening: bool) -> bool:
    if opening:
        return bool(text[:i].strip())
    return any(not (c.isspace() or c in PUNCT or c == QUOTE) for c in text[i + 1:])


def doc_ngoac(text: str, kieu: str) -> str | None:
    """Chữ đọc không còn ngoặc kép theo kiểu a/b; None nếu không có ngoặc kép giữa câu (không cần đổi)."""
    if kieu not in ("a", "b"):
        raise ValueError("kiểu phải là a hoặc b")
    marks = [(i, _is_open(text, i)) for i, c in enumerate(text) if c == QUOTE]
    if not any(_mid(text, i, opening) for i, opening in marks):
        return None
    out = ""
    for i, c in enumerate(text):
        if c != QUOTE:
            out += c
            continue
        before = out.rstrip()
        if kieu == "b" and _is_open(text, i) and before and before[-1] not in PUNCT:
            out = before + ", "
    out = re.sub(r" {2,}", " ", out)
    out = re.sub(r" +([.,:;!?…)])", r"\1", out)
    return out.strip()


def targets(rows, settings, pre: str, kieu: str) -> list[tuple[dict, str, str]]:
    """(dòng, chữ đọc cũ, chữ đọc mới) cho mã chỉ thuộc tập `pre`, chưa `dat`, có ngoặc kép giữa câu."""
    out = []
    for r in only_book_ids(rows, pre):
        if r.get("status") == "dat":
            continue
        old = (settings["overrides"].get(r["id"]) or {}).get("doc") or r["text"]
        new = doc_ngoac(old, kieu)
        if new is not None and new != old:
            out.append((r, old, new))
    return out


def main(argv) -> int:
    from tapdoc.manifest import load_rows
    from tapdoc.paths import ROOT
    from tapdoc.tts_settings import load_settings, save_settings, set_override
    pre = prefix(argv)
    kieu = argv[argv.index("--kieu") + 1] if "--kieu" in argv else "a"
    settings_path = ROOT / "content/tts/settings.json"
    settings = load_settings(settings_path)
    found = targets(load_rows(ROOT / "content/manifests/audio_manifest.json"), settings, pre, kieu)
    for r, old, new in found:
        print(f"{r['id']} [{r.get('status')}]: {old!r} -> {new!r}")
    print(f"{len(found)} mã có ngoặc kép giữa câu (kiểu {kieu})")
    if "--ghi" in argv:
        for r, _, new in found:
            set_override(settings, r, doc=new)
        save_settings(settings_path, settings)
        print("đã ghi chữ đọc vào content/tts/settings.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
