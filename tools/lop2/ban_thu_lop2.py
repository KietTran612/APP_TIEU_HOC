"""Bản thử ngoài danh mục cho mã âm thanh lớp 2 (QUY-TRINH §6, thiết kế TV2 tập hai mục 9).

Tạo vài cách đọc cho một mã mà không đụng file trong Unity, danh mục hay settings; root nhận dạng (asr_thu,
so_ban_thu) rồi mới cài bản được chọn. Cài thì giữ bản cũ ở content/tts/prev như lệnh tts, kiểm file cài trùng từng
byte với bản thử.

Dùng (từ gốc repo):
    python tools/lop2/ban_thu_lop2.py tao <thư mục> MÃ:cách[#nhãn][=chữ đọc] ...
    python tools/lop2/ban_thu_lop2.py cai <thư mục> MÃ__cách ... --ghi-chu "…"
Cách: cham (chậm hơn mặc định 20%; "cham=25" chậm hơn 25), ngat (chữ đọc riêng, cần =chữ),
cham_ngat (cả hai), ghep (ghép các tiếng đã có file, "," ở dấu câu; "ghep=a|,|doc:…" ghép đúng các phần
cho sẵn: mã có file, "," hoặc "doc:<chữ>" do bộ đọc đọc), le (một tiếng: đọc "X, X." rồi giữ tiếng đầu).
Chữ đọc riêng đã có của mã được giữ, trừ khi cách cho chữ mới.
Ra: <thư mục>/mp3, wav (16 kHz mono), marks, chi_muc.json {MÃ__cách: {id, chu, cach, doc, rate, keep_first, wav,
co_wav, override, do_cao_do, hang}}; tạo thêm vào thư mục cũ thì chi_muc gộp.
Chỉ một tiến trình đọc trên máy: mọi cách gọi bộ đọc, trừ ghep chỉ gồm mã có file; hỏi root trước khi chạy.
"""
import copy
import json
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from tapdoc.manifest import load_rows, save_rows  # noqa: E402
from tapdoc.paths import ROOT, UNITY_RES  # noqa: E402
from tapdoc.tts_engine import TtsError  # noqa: E402
from tapdoc.tts_generate import generate_one  # noqa: E402
from tapdoc.tts_settings import effective_params, load_settings, save_settings, set_override, signature  # noqa: E402
from tapdoc.viet import nfc, tokens  # noqa: E402

CACH = ("cham", "ngat", "cham_ngat", "ghep", "le")
SLOWER = 20
GAP = 0.08
MANIFEST = ROOT / "content/manifests/audio_manifest.json"
SETTINGS = ROOT / "content/tts/settings.json"
PREV = ROOT / "content/tts/prev"
MARKS = ROOT / "content/tts/marks"


def _split_tag(spec: str) -> tuple[str, str, str, str]:
    head, _, doc = spec.partition("=")
    audio_id, _, cach = head.partition(":")
    cach, _, tag = cach.partition("#")
    return audio_id, cach, tag, doc


def take_name(spec: str) -> str:
    """Tên bản thử: MÃ__cách, có nhãn thì MÃ__cách_nhãn (hai kiểu cùng cách của một mã)."""
    audio_id, cach, tag, _ = _split_tag(spec)
    return f"{audio_id}__{cach}" + (f"_{tag}" if tag else "")


def parse_spec(spec: str) -> tuple[str, str, str | None]:
    """"MÃ:cách[#nhãn][=chữ đọc]" → (mã, cách, chữ đọc hoặc None)."""
    audio_id, cach, _, doc = _split_tag(spec)
    if cach not in CACH:
        raise ValueError(f"{spec}: cách phải là một trong {', '.join(CACH)}")
    if cach in ("ngat", "cham_ngat") and not doc.strip():
        raise ValueError(f"{spec}: cách {cach} cần chữ đọc sau dấu =")
    return audio_id, cach, (doc.strip() or None)


def join_parts_for(text: str, audio_dir: Path) -> list[str]:
    """Mã tiếng của từng tiếng (tiếng mở đầu bằng nguyên âm có thể nằm ở mã vần `van_*`), "," ở dấu câu giữa câu."""
    from sua_hoi_nga_lop2 import join_parts  # cùng cách ghép của tập một

    def has(audio_id):
        return (Path(audio_dir) / f"{audio_id}.mp3").is_file()

    parts = [p if p == "," or has(p) or not has("van_" + p[6:]) else "van_" + p[6:] for p in join_parts(text)]
    missing = [p for p in parts if p != "," and not has(p)]
    if missing:
        raise ValueError(f"thiếu file tiếng để ghép: {missing}")
    if len([p for p in parts if p != ","]) < 2:
        raise ValueError("chỉ một tiếng: dùng cách le, không ghép")
    return _with_numbers(text, parts)


def _with_numbers(text: str, parts: list[str]) -> list[str]:
    """Chữ số không có file tiếng (`tokens` bỏ qua): chèn "doc:<số>" ngay sau tiếng đứng trước nó; số có dấu câu
    theo sau ("2. Vì…") thì nghỉ "," trước tiếng kế."""
    s = nfc(text)
    toks = tokens(s)
    at = [k for k, p in enumerate(parts) if p != ","]  # vị trí phần của từng tiếng
    inserts: dict[int, list[str]] = {}
    for m in re.finditer(r"\d+(?:[.,]\d+)*\.?", s):
        before = [k for k, (_, start) in enumerate(toks) if start < m.start()]
        nxt = next((start for _, start in toks if start > m.start()), None)
        new = ["doc:" + m.group()]
        if nxt is not None and (m.group().endswith(".") or any(c in ",.;:?!)…" for c in s[m.end():nxt])):
            new.append(",")
        inserts.setdefault(at[before[-1]] + 1 if before else 0, []).extend(new)
    out: list[str] = []
    for k in range(len(parts) + 1):
        for p in inserts.get(k, []) + parts[k:k + 1]:
            if not (p == "," and (not out or out[-1] == ",")):
                out.append(p)
    while out and out[-1] == ",":
        out.pop()
    return out


def explicit_parts(spec: str, audio_dir: Path) -> list[str]:
    """Danh sách ghép cho sẵn, "|" ngăn phần: mã có file, "," (nghỉ dài) hoặc "doc:<chữ>" (bộ đọc đọc phần đó)."""
    parts = [p.strip() for p in spec.split("|") if p.strip()]
    missing = [p for p in parts if p != "," and not p.startswith("doc:") and not (Path(audio_dir) / f"{p}.mp3").is_file()]
    if missing:
        raise ValueError(f"thiếu file để ghép: {missing}")
    return parts


def override_for(row, settings, cach: str, doc: str | None, audio_dir: Path) -> dict:
    """Chỉnh riêng của bản thử: chỉnh riêng hiện có của mã, đổi theo cách."""
    out = dict(settings["overrides"].get(row["id"]) or {})
    if cach == "cham" and doc is not None:  # "cham=25": chậm hơn mặc định 25 thay vì 20
        if not doc.isdigit():
            raise ValueError(f"{row['id']}: cham=<số> là mức chậm hơn mặc định, không phải chữ đọc")
        out["rate"] = settings["defaults"][row["kind"]]["rate"] - int(doc)
    elif cach in ("cham", "cham_ngat"):
        out["rate"] = settings["defaults"][row["kind"]]["rate"] - SLOWER
    if cach in ("ngat", "cham_ngat"):
        out["doc"] = doc
    if cach == "ghep":
        out = {k: v for k, v in out.items() if k not in ("doc", "keep_first")}
        out.update(join=explicit_parts(doc, audio_dir) if doc else join_parts_for(row["text"], audio_dir), join_gap=GAP)
    if cach == "le":
        if len(tokens(row["text"])) != 1:
            raise ValueError(f"{row['id']}: cách le chỉ cho mã một tiếng")
        word = row["text"].strip()
        out.update(doc=doc or f"{word}, {word}.", keep_first=True)
    return out


def take_settings(settings, row, override: dict) -> dict:
    s = copy.deepcopy(settings)
    s["overrides"].pop(row["id"], None)
    set_override(s, row, **override)
    return s


def make_take(row, settings, override, engine, out_dir: Path, name: str, audio_dir: Path, tries: int = 3,
              pause: float = 20.0) -> dict:
    """Tạo một bản thử vào out_dir/mp3/<name>.mp3 (mốc ở out_dir/marks/<name>.json); trả dòng danh mục như lệnh tts
    sẽ ghi. Không ghi gì vào audio_dir."""
    s = take_settings(settings, row, override)
    p = effective_params(s, row)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        work = tmp / "audio"
        work.mkdir()
        for part in p.join:
            if part != "," and not part.startswith("doc:"):
                shutil.copy(Path(audio_dir) / f"{part}.mp3", work / f"{part}.mp3")
        for k in range(tries):
            try:
                updated = generate_one(row, s, engine, work, tmp / "prev", tmp / "marks")
                break
            except TtsError:
                if k == tries - 1:
                    raise
                time.sleep(pause)
        (out_dir / "mp3").mkdir(parents=True, exist_ok=True)
        shutil.copy(work / f"{row['id']}.mp3", out_dir / "mp3" / f"{name}.mp3")
        marks = tmp / "marks" / f"{row['id']}.json"
        if marks.is_file():
            (out_dir / "marks").mkdir(parents=True, exist_ok=True)
            shutil.copy(marks, out_dir / "marks" / f"{name}.json")
    return updated


def entry_for(row, updated, cach, override, name, has_wav, pitch=None) -> dict:
    tts = updated["tts"]
    doc = "ghép: " + " ".join(tts["join"]) if tts["join"] else tts["doc"]
    return {"id": row["id"], "chu": row["text"], "cach": cach, "doc": doc,
            "rate": None if tts["join"] else tts["rate"], "keep_first": tts["keep_first"],
            "wav": f"wav/{name}.wav", "co_wav": has_wav, "override": override, "do_cao_do": pitch or [],
            "hang": {"source": updated["source"], "tts": tts}}


def install(entry, out_dir: Path, rows_by_id: dict, settings, audio_dir: Path, prev_dir: Path, marks_dir: Path,
            note: str) -> dict:
    """Cài bản thử: bản cũ vào prev (như lệnh tts), file mới trùng từng byte với bản thử, chỉnh riêng vào settings,
    dòng danh mục cho_duyet với cách đọc của bản thử và thêm ghi chú. Trả dòng mới (settings sửa tại chỗ)."""
    row = rows_by_id[entry["id"]]
    if row.get("status") == "dat":
        raise ValueError(f"{row['id']}: đã duyệt, không tự thay")
    name = Path(entry["wav"]).stem
    take = (out_dir / "mp3" / f"{name}.mp3").read_bytes()
    dest = Path(audio_dir) / f"{row['id']}.mp3"
    prev_dir = Path(prev_dir)
    prev_dir.mkdir(parents=True, exist_ok=True)
    if dest.is_file():
        old = {key: copy.deepcopy(row[key]) for key in ("tts", "status", "source") if key in row}
        old["override"] = copy.deepcopy(settings["overrides"].get(row["id"]))
        (prev_dir / f"{row['id']}.mp3").write_bytes(dest.read_bytes())
        (prev_dir / f"{row['id']}.json").write_text(json.dumps(old, ensure_ascii=False, indent=2) + "\n",
                                                    encoding="utf-8")
    dest.write_bytes(take)
    if dest.read_bytes() != take:
        raise OSError(f"{row['id']}: file cài không trùng bản thử")
    marks = out_dir / "marks" / f"{name}.json"
    if marks.is_file():
        Path(marks_dir).mkdir(parents=True, exist_ok=True)
        shutil.copy(marks, Path(marks_dir) / f"{row['id']}.json")
    else:
        (Path(marks_dir) / f"{row['id']}.json").unlink(missing_ok=True)
    settings["overrides"].pop(row["id"], None)
    set_override(settings, row, **entry["override"])
    updated = copy.deepcopy(row)
    updated.update(status="cho_duyet", source=entry["hang"]["source"], tts=copy.deepcopy(entry["hang"]["tts"]))
    if signature(effective_params(settings, updated)) != updated["tts"]["sig"]:
        raise ValueError(f"{row['id']}: cách đọc trong settings không khớp bản thử")
    old_note = (row.get("ghi_chu") or "").strip()
    updated["ghi_chu"] = (old_note + " " if old_note else "") + note.strip()
    return updated


def _measure(entries: dict, out_dir: Path) -> None:
    """Đo hỏi/ngã từng bản thử như do_cao_do_lop2 (tiếng lẻ, cuối cụm: dat/sai/co_the_sai)."""
    from tapdoc import pitch_check as pc
    from do_cao_do_lop2 import CACHE, classify
    rows = load_rows(MANIFEST)
    templates = pc.reference_templates(rows, UNITY_RES / "audio", CACHE / "refs")
    for name, e in entries.items():
        wav = out_dir / e["wav"]
        mp = out_dir / "marks" / f"{name}.json"
        marks = json.loads(mp.read_text(encoding="utf-8")) if mp.is_file() else None
        row = {"id": e["id"], "text": e["chu"], "tts": e["hang"]["tts"]}
        e["do_cao_do"] = [{k: x.get(k) for k in ("word", "verdict", "rise")}
                          for x in classify(row, wav if wav.is_file() else None, marks, templates)]


def main(argv) -> int:
    if len(argv) < 3 or argv[0] not in ("tao", "cai"):
        print(__doc__)
        return 2
    action, out_dir, rest = argv[0], Path(argv[1]), argv[2:]
    index_path = out_dir / "chi_muc.json"
    index = json.loads(index_path.read_text(encoding="utf-8")) if index_path.is_file() else {}
    rows = load_rows(MANIFEST)
    by_id = {r["id"]: r for r in rows}
    settings = load_settings(SETTINGS)
    audio = UNITY_RES / "audio"
    if action == "tao":
        from tapdoc import pitch_check as pc
        from tapdoc.tts_engine import EdgeEngine
        engine = EdgeEngine()
        made = {}
        for spec in rest:
            audio_id, cach, doc = parse_spec(spec)
            row = by_id[audio_id]
            name = take_name(spec)
            try:
                override = override_for(row, settings, cach, doc, audio)
                updated = make_take(row, settings, override, engine, out_dir, name, audio)
            except (TtsError, ValueError, OSError) as e:
                print(f"LỖI {name}: {e}")
                continue
            made[name] = entry_for(row, updated, cach, override, name, False)
        wavs = pc.decode([out_dir / "mp3" / f"{n}.mp3" for n in made], out_dir / "wav")
        for name, e in made.items():
            e["co_wav"] = (out_dir / "mp3" / f"{name}.mp3") in wavs
        _measure(made, out_dir)
        for name, e in made.items():
            pitch = ", ".join(f"{x['word']} {x['verdict']}" + (f" {x['rise']}" if x.get("rise") is not None else "")
                              for x in e["do_cao_do"])
            print(f"{name}: {e['doc']}" + (f" | {pitch}" if pitch else ""))
        index.update(made)
        out_dir.mkdir(parents=True, exist_ok=True)
        index_path.write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        return 0 if len(made) == len(rest) else 1
    note = ""
    if "--ghi-chu" in rest:
        k = rest.index("--ghi-chu")
        note, rest = rest[k + 1], rest[:k] + rest[k + 2:]
    if not note:
        print("cần --ghi-chu")
        return 2
    ids = [index[n]["id"] for n in rest]
    if len(set(ids)) != len(ids):
        print("mỗi mã chỉ cài một bản")
        return 2
    for name in rest:
        e = index[name]
        updated = install(e, out_dir, by_id, settings, audio, PREV, MARKS, f"{note} Bản thử {e['cach']}.")
        by_id[e["id"]] = updated
        print(f"cài {name} → {e['id']}.mp3 (trùng từng byte)")
    save_rows(MANIFEST, [by_id[r["id"]] for r in rows])
    save_settings(SETTINGS, settings)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
