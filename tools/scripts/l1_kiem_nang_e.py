"""Lớp 1, đợt thanh nặng và âm ê (10/11): kiểm bản mới, trả bản cũ nếu lạ, ghi chú "chờ nghe xác nhận".

Chạy sau khi `regen_runner.py scripts/l1_nang_e_ids.txt …` đã tạo xong (từ thư mục tools):
    python scripts/l1_kiem_nang_e.py          # chỉ in kết quả
    python scripts/l1_kiem_nang_e.py --ghi    # trả bản cũ cho mã lạ, ghi chú mọi mã, lưu danh mục

"Lạ": thanh nặng có phần hữu thanh dài hơn 0,45 giây (tiếng nặng đã đạt: 0,18–0,41) hoặc cao độ không giống nặng/huyền;
tiếng có ê thì cao độ ra sai thanh của chính nó. Đo bằng tapdoc.pitch_check (mẫu từ các tiếng đã `dat`).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tapdoc import pitch_check as pc  # noqa: E402
from tapdoc.manifest import load_rows, save_rows  # noqa: E402
from tapdoc.paths import ROOT, UNITY_RES  # noqa: E402
from tapdoc.tts_generate import restore_previous  # noqa: E402
from tapdoc.tts_settings import effective_params, load_settings, save_settings, signature  # noqa: E402

IDS = (Path(__file__).parent / "l1_nang_e_ids.txt").read_text(encoding="utf-8").split()
CACHE = ROOT / "content/tts/pitch_cache"
STOPS = ("p", "t", "c", "ch")
NOTE_TAG ="Rà soát thanh nặng/âm ê 10/11"
DONE_BY_OWNER = {"tieng_nuj": "chủ dự án chọn bản 5 \"nụ hoa.\" trên trang nghe thử"}


def main(write: bool) -> None:
    audio = UNITY_RES / "audio"
    path = ROOT / "content/manifests/audio_manifest.json"
    settings_path = ROOT / "content/tts/settings.json"
    rows = load_rows(path)
    settings = load_settings(settings_path)
    by_id = {r["id"]: r for r in rows}
    templates = pc.reference_templates(rows, audio, CACHE / "refs")
    done = [i for i in IDS if (by_id[i].get("tts") or {}).get("sig") == signature(effective_params(settings, by_id[i]))]
    single = [i for i in done if (settings["overrides"].get(i) or {}).get("keep_first")]
    wavs = pc.decode([audio / f"{i}.mp3" for i in single], CACHE)
    odd = {}
    for i in single:
        tone = pc.tone_of(by_id[i]["text"])
        values = pc.contour(wavs[audio / f"{i}.mp3"]) if audio / f"{i}.mp3" in wavs else []
        best = pc.nearest(values, templates) if len(values) >= 5 else "?"
        dur = len(values) * 0.01
        if best == "?":
            odd[i] = "không đo được cao độ"
        elif tone == "nang" and dur > 0.45:
            odd[i] = f"phần hữu thanh dài {dur:.2f} giây"
        elif tone == "nang" and best not in ("nang", "huyen"):
            odd[i] = f"cao độ đo ra như thanh {best}"
        elif tone in ("hoi", "nga") and best not in ("hoi", "nga"):
            odd[i] = f"cao độ đo ra như thanh {best}"
        elif tone == "ngang" and by_id[i]["text"].endswith(STOPS) and best in ("ngang", "sac"):
            pass  # vần tắc không dấu (êt, mêt): khi đọc vốn cao như sắc
        elif tone == "huyen" and best in ("huyen", "nang"):
            pass  # cao độ không tách được huyền với nặng
        elif tone in ("ngang", "sac", "huyen") and best != tone:
            odd[i] = f"cao độ đo ra như thanh {best}"
    print(f"đã có bản mới {len(done)}/{len(IDS)}; đo {len(single)}; lạ {len(odd)}")
    for i, why in odd.items():
        print(f"  lạ {i} ({by_id[i]['text']}): {why}")
    if not write:
        return
    prev_dir = ROOT / "content/tts/prev"
    same = {i for i in done if (prev_dir / f"{i}.mp3").is_file()
            and (prev_dir / f"{i}.mp3").read_bytes() == (audio / f"{i}.mp3").read_bytes()}
    print(f"trùng từng byte với bản cũ: {len(same)}")
    for k, r in enumerate(rows):
        if r["id"] not in done or NOTE_TAG in (r.get("ghi_chu") or ""):
            continue
        p = effective_params(settings, r)
        if r["id"] in same:
            why = f" Đo: {odd[r['id']]}." if r["id"] in odd else ""
            note = (f"{NOTE_TAG}: đọc \"{p.doc}\" rồi giữ tiếng đầu ra file TRÙNG từng byte với bản cũ "
                    f"(edge-tts tạo từng câu riêng nên câu đầu = đọc tiếng trần) — âm thanh không đổi.{why} "
                    "Nếu nghe vẫn sai thì cần đặt trong ngữ cảnh như \"nụ hoa.\". Chờ nghe xác nhận.")
        elif r["id"] in odd:
            r = rows[k] = restore_previous(r, settings, audio, ROOT / "content/tts/prev")
            note = f"{NOTE_TAG}: bản mới ({p.doc}) đo lạ — {odd[r['id']]} → giữ bản cũ. Chờ nghe xác nhận."
        elif r["id"] in DONE_BY_OWNER:
            note = f"{NOTE_TAG}: {DONE_BY_OWNER[r['id']]} (keep_first). Chờ nghe xác nhận."
        elif p.join:
            note = f"{NOTE_TAG}: ghép mượt {' + '.join(x for x in p.join if x != ',')}. Chờ nghe xác nhận."
        elif p.keep_first:
            note = f"{NOTE_TAG}: đọc \"{p.doc}\" rồi giữ tiếng đầu (keep_first), theo cách chủ dự án đã chọn cho bạ/ế. Chờ nghe xác nhận. Bản cũ ở prev."
        else:
            note = f"{NOTE_TAG}: đọc \"{p.doc}\" (tốc độ {p.rate}%), chủ dự án chọn trên trang nghe thử. Chờ nghe xác nhận. Bản cũ ở prev."
        r["ghi_chu"] = f"{r['ghi_chu']} | {note}" if r.get("ghi_chu") else note
    save_rows(path, rows)
    save_settings(settings_path, settings)
    print("đã ghi chú và lưu danh mục")


if __name__ == "__main__":
    main("--ghi" in sys.argv)
