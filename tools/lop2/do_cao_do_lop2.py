"""Đo cao độ hỏi/ngã cho mọi mã riêng lớp 2 và phân loại theo cách hiệu chỉnh trong QUY-TRINH-LAM-VIEC.md mục 12:

- Tiếng lẻ, hoặc tiếng ở **cuối cụm** (cuối câu hoặc ngay trước dấu câu): đo tin được. Đường cao độ phải võng rồi lên:
  lên (cao nhất nửa sau − thấp nhất) ≥ 7 bán âm → đạt; ≤ 1 bán âm → **sai**; ở giữa → theo mẫu (`pitch_check.judge`):
  không giống hỏi/ngã thì **sai**, giống thì đạt.
- Tiếng ở **giữa cụm**: tiêu chí yếu, không giống mẫu hỏi/ngã chỉ coi là **có thể sai** (để tai người nghe).

Dùng (từ gốc repo, không gọi mạng):
    python tools/lop2/do_cao_do_lop2.py [--ma MÃ ...] [--json ra.json]
In: mỗi mã có tiếng **sai** một dòng; cuối cùng là bảng đếm. `--json` ghi kết quả từng tiếng.
"""
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from tapdoc import pitch_check as pc  # noqa: E402
from tapdoc.manifest import load_rows  # noqa: E402
from tapdoc.paths import ROOT, UNITY_RES  # noqa: E402
from tapdoc.viet import nfc, tokens  # noqa: E402

PREFIX = "tv2_t1_"
CACHE = ROOT / "content/tts/pitch_cache"
MARKS = ROOT / "content/tts/marks"
PUNCT = set(",.?!;:…")
RISE_OK, RISE_BAD = 7.0, 1.0


def lop2(row) -> bool:
    bai = row.get("bai") or []
    return bool(bai) and all(b.startswith(PREFIX) for b in bai)


def phrase_final(text: str, k: int) -> bool:
    """Tiếng thứ k là tiếng cuối, hoặc ngay sau nó (bỏ khoảng trắng, ngoặc kép) là dấu câu."""
    toks = tokens(text)
    if k == len(toks) - 1:
        return True
    tok, start = toks[k]
    rest = nfc(text)[start + len(tok):toks[k + 1][1]]
    return any(ch in PUNCT for ch in rest)


def rise(values) -> float:
    half = values[len(values) // 2:]
    return max(half) - min(values) if values else 0.0


def classify(row, wav, marks, templates) -> list[dict]:
    text = row["text"]
    count = len(tokens(text))
    spans = (marks or {}).get("words") or []
    out = []
    for k, word, tone in pc.words_to_check(text):
        res = {"id": row["id"], "word": word, "tone": tone, "pos": k}
        if wav is None:
            out.append({**res, "verdict": "chua_do", "why": "không giải mã được"})
            continue
        if count > 1 and len(spans) != count:
            out.append({**res, "verdict": "chua_do", "why": "không có mốc từng tiếng"})
            continue
        start, end = (None, None) if count == 1 else spans[k]
        values = pc.contour(wav, start, end)
        if len(values) < 5:
            out.append({**res, "verdict": "chua_do", "why": "quá ít điểm hữu thanh"})
            continue
        final = count == 1 or phrase_final(text, k)
        r = rise(values)
        like = pc.judge(values, tone, templates)
        if final:
            verdict = "dat" if r >= RISE_OK else "sai" if r <= RISE_BAD else ("dat" if like else "sai")
        else:
            verdict = "dat" if like else "co_the_sai"
        out.append({**res, "final": final, "rise": round(r, 1), "best": pc.nearest(values, templates),
                    "verdict": verdict})
    return out


def main(argv):
    ids = None
    out_json = None
    if "--ma" in argv:
        i = argv.index("--ma")
        ids = set()
        for a in argv[i + 1:]:
            if a.startswith("--"):
                break
            ids.add(a)
    if "--json" in argv:
        out_json = Path(argv[argv.index("--json") + 1])
    rows = load_rows(ROOT / "content/manifests/audio_manifest.json")
    audio = UNITY_RES / "audio"
    templates = pc.reference_templates(rows, audio, CACHE / "refs")
    if not pc.has_dip_rise_templates(templates):
        print("Thiếu mẫu hỏi/ngã (cần tiếng đã `dat` có file trên máy).")
        return 2
    targets = [r for r in rows if lop2(r) and (ids is None or r["id"] in ids) and pc.words_to_check(r["text"])
               and (audio / f"{r['id']}.mp3").is_file()]
    wavs = pc.decode([audio / f"{r['id']}.mp3" for r in targets], CACHE)
    results = []
    for r in targets:
        mp3 = audio / f"{r['id']}.mp3"
        mp = MARKS / f"{r['id']}.json"
        fresh = mp.is_file() and mp.stat().st_mtime >= mp3.stat().st_mtime
        marks = json.loads(mp.read_text(encoding="utf-8")) if fresh else None
        results += classify(r, wavs.get(mp3), marks, templates)
    by_id = {}
    for x in results:
        by_id.setdefault(x["id"], []).append(x)
    for audio_id, xs in by_id.items():
        bad = [x for x in xs if x["verdict"] == "sai"]
        if bad:
            print(f"SAI {audio_id}: " + ", ".join(f"{x['word']}(lên {x['rise']})" for x in bad))
    count = {}
    for x in results:
        count[x["verdict"]] = count.get(x["verdict"], 0) + 1
    ids_bad = sorted({x["id"] for x in results if x["verdict"] == "sai"})
    ids_maybe = sorted({x["id"] for x in results if x["verdict"] == "co_the_sai"} - set(ids_bad))
    print(f"Đã đo {len(targets)} mã, {len(results)} tiếng hỏi/ngã: {count}")
    print(f"Mã có tiếng sai: {len(ids_bad)}; mã chỉ có tiếng có thể sai: {len(ids_maybe)}")
    if out_json:
        out_json.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
