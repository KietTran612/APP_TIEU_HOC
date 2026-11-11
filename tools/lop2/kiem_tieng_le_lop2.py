"""Kiểm tiếng lẻ lớp 2 (mã `tieng_*` chỉ thuộc bài tv2_t1_) theo cách của L1 (`tools/scripts/l1_kiem_nang_e.py`, 10/11):

- thanh nặng: phần hữu thanh dài hơn 0,45 giây (tiếng nặng đã đạt: 0,18–0,41) hoặc cao độ không giống nặng/huyền → lạ;
- hỏi/ngã: cao độ không giống hỏi/ngã → lạ;
- ngang/sắc/huyền (gồm tiếng có ê): cao độ ra thanh khác → lạ (bỏ qua vần tắc không dấu đo ra sắc, huyền đo ra nặng).

Chỉ đo, không ghi gì (từ gốc repo, không gọi mạng):
    python tools/lop2/kiem_tieng_le_lop2.py [--json ra.json]
"""
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from tapdoc import pitch_check as pc  # noqa: E402
from tapdoc.manifest import load_rows  # noqa: E402
from tapdoc.paths import ROOT, UNITY_RES  # noqa: E402

PREFIX = "tv2_t1_"
CACHE = ROOT / "content/tts/pitch_cache"
STOPS = ("p", "t", "c", "ch")
NANG_MAX = 0.45


def odd_reason(text: str, values, templates) -> str | None:
    tone = pc.tone_of(text)
    if len(values) < 5:
        return "không đo được cao độ"
    best = pc.nearest(values, templates)
    dur = len(values) * 0.01
    if tone == "nang" and dur > NANG_MAX:
        return f"phần hữu thanh dài {dur:.2f} giây"
    if tone == "nang":
        return None if best in ("nang", "huyen") else f"cao độ đo ra như thanh {best}"
    if tone in ("hoi", "nga"):
        return None if best in ("hoi", "nga") else f"cao độ đo ra như thanh {best}"
    if tone == "ngang" and text.lower().endswith(STOPS) and best in ("ngang", "sac"):
        return None
    if tone == "huyen" and best in ("huyen", "nang"):
        return None
    return None if best == tone else f"cao độ đo ra như thanh {best}"


def main(argv):
    rows = load_rows(ROOT / "content/manifests/audio_manifest.json")
    audio = UNITY_RES / "audio"
    templates = pc.reference_templates(rows, audio, CACHE / "refs")
    targets = [r for r in rows if r["id"].startswith("tieng_") and r.get("bai")
               and all(b.startswith(PREFIX) for b in r["bai"]) and (audio / f"{r['id']}.mp3").is_file()]
    wavs = pc.decode([audio / f"{r['id']}.mp3" for r in targets], CACHE)
    out = []
    for r in targets:
        wav = wavs.get(audio / f"{r['id']}.mp3")
        values = pc.contour(wav) if wav else []
        why = odd_reason(r["text"], values, templates)
        out.append({"id": r["id"], "text": r["text"], "tone": pc.tone_of(r["text"]), "la": why})
        if why:
            print(f"LẠ {r['id']} ({r['text']}): {why}")
    n = sum(1 for x in out if x["la"])
    print(f"Đã đo {len(out)} tiếng lẻ lớp 2; lạ {n}")
    if "--json" in argv:
        Path(argv[argv.index("--json") + 1]).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
