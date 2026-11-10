"""Cách đọc tiếng lẻ lớp 2 theo lựa chọn chủ dự án ở lớp 1 (9/11):
- thanh nặng: "X. X." giữ tiếng đầu;
- có ê thanh sắc (ế): "X, X, X." giữ tiếng đầu;
- còn lại: "X, X." giữ tiếng đầu.
Chỉ mã tieng_* mà mọi bài đều là tv2_t1_*, chưa 'dat', và override hiện tại trống hoặc là "X, X." mặc định.
Dùng: python tools/lop2/tieng_doc_lop2.py [--ghi]  (không --ghi: chỉ in)"""
import json
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from tapdoc.tts_settings import load_settings, save_settings  # noqa: E402

MANIFEST = ROOT / "content" / "manifests" / "audio_manifest.json"
SETTINGS = ROOT / "content" / "tts" / "settings.json"
DOT_BELOW = "\u0323"


def want_doc(text):
    nfd = unicodedata.normalize("NFD", text.lower())
    if DOT_BELOW in nfd:
        return f"{text}. {text}."
    if "ế" in unicodedata.normalize("NFC", text.lower()):
        return f"{text}, {text}, {text}."
    return f"{text}, {text}."


def main():
    write = "--ghi" in sys.argv
    rows = json.loads(MANIFEST.read_text(encoding="utf-8"))
    settings = load_settings(SETTINGS)
    changed = {"nang": [], "e_sac": []}
    for r in rows:
        bai = r.get("bai", [])
        if r.get("kind") != "tieng" or not bai or not all(b.startswith("tv2_t1_") for b in bai):
            continue
        if r.get("status") == "dat":
            continue
        text = r["text"]
        cur = settings["overrides"].get(r["id"])
        default = {"doc": f"{text}, {text}.", "keep_first": True}
        if cur not in (None, default):
            continue
        doc = want_doc(text)
        if doc == default["doc"]:
            continue
        settings["overrides"][r["id"]] = {"doc": doc, "keep_first": True}
        changed["nang" if doc.endswith(f"{text}.") and ". " in doc else "e_sac"].append(r["id"])
    print({k: len(v) for k, v in changed.items()})
    print(changed)
    if write:
        save_settings(SETTINGS, settings)
        print("đã ghi")


if __name__ == "__main__":
    main()
