"""Xuất WAV 16 kHz mono của các mã âm thanh lớp 2 để root nhận dạng giọng nói (thiết kế TV2 tập hai mục 9).

Chỉ mã mà mọi bài đều thuộc tập đã chọn và có ít nhất một bài trong khoảng; mã có file mp3 trong Unity.
Ra: <thư mục>/wav/<mã>.wav và <thư mục>/chi_muc.json {mã: {"id", "loai", "chu", "doc", "wav", "co_wav"}}
("chu" là chữ hiển thị, "doc" là chữ đưa cho bộ đọc theo content/tts/settings.json).

Dùng (từ gốc repo): python tools/lop2/xuat_wav_lop2.py [--t2] <bài đầu> <bài cuối> --ra <thư mục> [--ma MÃ …]
"""
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from sach import only_book_ids, prefix  # noqa: E402
from tapdoc import pitch_check as pc  # noqa: E402
from tapdoc.manifest import load_rows  # noqa: E402
from tapdoc.paths import ROOT, UNITY_RES  # noqa: E402
from tapdoc.tts_settings import load_settings  # noqa: E402


def _arg_list(argv, flag):
    if flag not in argv:
        return None
    i = argv.index(flag)
    out = []
    for a in argv[i + 1:]:
        if a.startswith("--"):
            break
        out.append(a)
    del argv[i:i + 1 + len(out)]
    return out


def chosen(rows, pre, lo, hi, ids=None):
    """Dòng chỉ thuộc tập `pre`, có bài trong [lo, hi] (và thuộc `ids` nếu có)."""
    out = []
    for r in only_book_ids(rows, pre):
        nos = [int(b.rsplit("_b", 1)[1]) for b in r["bai"]]
        if any(lo <= n <= hi for n in nos) and (ids is None or r["id"] in ids):
            out.append(r)
    return out


def main(argv):
    pre = prefix(argv)
    ra = _arg_list(argv, "--ra")
    ids = _arg_list(argv, "--ma")
    if not ra or len(argv) < 3:
        print(__doc__)
        return 2
    lo, hi, out_dir = int(argv[1]), int(argv[2]), Path(ra[0])
    rows = chosen(load_rows(ROOT / "content/manifests/audio_manifest.json"), pre, lo, hi,
                  set(ids) if ids is not None else None)
    settings = load_settings(ROOT / "content/tts/settings.json")
    audio = UNITY_RES / "audio"
    mp3s = [audio / f"{r['id']}.mp3" for r in rows if (audio / f"{r['id']}.mp3").is_file()]
    wavs = pc.decode(mp3s, out_dir / "wav")
    index = {}
    for r in rows:
        wav = wavs.get(audio / f"{r['id']}.mp3")
        doc = (settings["overrides"].get(r["id"]) or {}).get("doc") or r["text"]
        index[r["id"]] = {"id": r["id"], "loai": r.get("kind", ""), "chu": r["text"], "doc": doc,
                          "wav": f"wav/{r['id']}.wav", "co_wav": bool(wav)}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "chi_muc.json").write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    missing = [k for k, v in index.items() if not v["co_wav"]]
    print(f"{len(index)} mã, có WAV {len(index) - len(missing)}, thiếu {len(missing)}: {missing[:20]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
