"""Sửa mã lớp 2 đọc sai hỏi/ngã theo thứ tự chủ dự án chọn (9/11): đọc chậm (−20% so với mặc định) → ghép mượt.

Chỉ đặt cách đọc trong `content/tts/settings.json` và ghi chú; việc tạo lại do `tts_lop2.py` làm (mã khác cấu hình
được chọn lại), đo lại bằng `do_cao_do_lop2.py --ma …`. Chạy từ gốc repo:
    python tools/lop2/sua_hoi_nga_lop2.py cham MÃ ...        # rate = mặc định − 20
    python tools/lop2/sua_hoi_nga_lop2.py ghep MÃ ...        # join từ các tiếng có file, "," ở dấu câu giữa câu
    python tools/lop2/sua_hoi_nga_lop2.py ghi-chu cham|ghep|kho MÃ ...   # thêm ghi chú sau khi tạo/đo xong
"""
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from tapdoc.ids import telex  # noqa: E402
from tapdoc.manifest import load_rows, save_rows  # noqa: E402
from tapdoc.paths import ROOT, UNITY_RES  # noqa: E402
from tapdoc.tts_settings import load_settings, save_settings, set_override  # noqa: E402
from tapdoc.viet import nfc, tokens  # noqa: E402

MANIFEST = ROOT / "content/manifests/audio_manifest.json"
SETTINGS = ROOT / "content/tts/settings.json"
TAG = "Rà soát hỏi/ngã lớp 2 11/11"
PAUSE = set(",;:…")
SLOWER = 20
GAP = 0.08


def join_parts(text: str) -> list[str]:
    """Mã tiếng của từng tiếng trong câu, chèn "," nơi giữa hai tiếng có dấu phẩy, chấm phẩy, hai chấm, chấm lửng."""
    toks = tokens(text)
    s = nfc(text)
    out = []
    for k, (tok, start) in enumerate(toks):
        if k:
            prev, pstart = toks[k - 1]
            if any(ch in PAUSE or ch in ".?!()–-" for ch in s[pstart + len(prev):start]):
                out.append(",")
        out.append(f"tieng_{telex(tok)}")
    return out


def van_thay(parts: list[str], has) -> list[str]:
    """Tiếng bắt đầu bằng nguyên âm ("em", "ông") có file ở mã vần `van_*`: thay `tieng_X` thiếu file bằng `van_X`
    khi `van_X` có file (`has(mã)` → có file). Tiếng đã có file, dấu "," và tiếng thiếu cả hai giữ nguyên."""
    out = []
    for p in parts:
        van = "van_" + p.removeprefix("tieng_")
        out.append(van if p.startswith("tieng_") and not has(p) and has(van) else p)
    return out


def main(argv) -> int:
    action, ids = argv[0], argv[1:]
    rows = load_rows(MANIFEST)
    by_id = {r["id"]: r for r in rows}
    settings = load_settings(SETTINGS)
    audio = UNITY_RES / "audio"
    if action == "cham":
        for i in ids:
            r = by_id[i]
            rate = settings["defaults"][r["kind"]]["rate"] - SLOWER
            set_override(settings, r, rate=rate)
            print(f"{i}: rate {rate}")
        save_settings(SETTINGS, settings)
        return 0
    if action == "ghep":
        bad = 0
        for i in ids:
            if any(ch.isdigit() for ch in by_id[i]["text"]):
                print(f"{i}: câu có chữ số — không ghép")
                bad += 1
                continue
            parts = join_parts(by_id[i]["text"])
            if len(parts) < 2:
                print(f"{i}: chỉ một tiếng — đọc như tiếng lẻ (\"X, X.\" giữ tiếng đầu), không ghép")
                bad += 1
                continue
            def has(p):
                return p in by_id and (audio / f"{p}.mp3").is_file()

            parts = van_thay(parts, has)
            missing = [p for p in parts if p != "," and not has(p)]
            if missing:
                print(f"{i}: thiếu tiếng {missing} — không ghép")
                bad += 1
                continue
            set_override(settings, by_id[i], join=parts, join_gap=GAP)
            print(f"{i}: ghép {' '.join(parts)}")
        save_settings(SETTINGS, settings)
        return 1 if bad else 0
    if action == "ghi-chu":
        how, ids = ids[0], ids[1:]
        for r in rows:
            if r["id"] not in ids or TAG in (r.get("ghi_chu") or ""):
                continue
            if how == "cham":
                note = f"{TAG}: tiếng hỏi/ngã cuối cụm lên chưa đủ → đọc chậm hơn 20%, đo lại đạt. Chờ nghe xác nhận. Bản cũ ở prev."
            elif how == "ghep":
                parts = " + ".join(p for p in (settings["overrides"].get(r["id"]) or {}).get("join", []) if p != ",")
                note = (f"{TAG}: đọc nguyên câu và đọc chậm 20% vẫn lên chưa đủ → ghép mượt {parts} "
                        f"(khoảng nghỉ {GAP} s, nghỉ 0,25 s ở dấu câu). Chờ nghe xác nhận. Bản cũ ở prev.")
            else:
                note = f"{TAG}: máy đo tiếng hỏi/ngã cuối cụm lên chưa đủ, chưa sửa được — cần nghe."
            r["ghi_chu"] = f"{r['ghi_chu']} | {note}" if r.get("ghi_chu") else note
            r["status"] = "cho_duyet"
        save_rows(MANIFEST, rows)
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
