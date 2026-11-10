"""Stage chỉ phần lớp 2 của danh mục (thêm dòng mới và mã bài tv2_t1_ trong `bai`), giữ nguyên chỉnh sửa duyệt
chưa commit của chủ dự án: dựng blob từ HEAD + phần lớp 2 rồi `git hash-object -w` + `git update-index --cacheinfo`.

Dùng: python tools/lop2/stage_lop2.py content/manifests/audio_manifest.json [content/tts/settings.json ...]
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PREFIX = "tv2_t1_"


def git(*args, input=None):
    return subprocess.run(["git", *args], cwd=REPO, check=True, capture_output=True, input=input).stdout


EXTRA_IDS = {"img_chung_giai_nghia"}  # kí hiệu [:] của lớp 2 (bài "chung")


def mine(row):
    return row["id"] in EXTRA_IDS or any(b.startswith(PREFIX) for b in row.get("bai", []))


def stage(rel):
    head = {r["id"]: r for r in json.loads(git("show", f"HEAD:{rel}").decode("utf-8"))}
    work = json.loads((REPO / rel).read_text(encoding="utf-8"))
    out, added, touched = [], 0, 0
    for row in work:
        base = head.get(row["id"])
        if base is None:
            if mine(row):
                out.append(row)
                added += 1
            continue
        if row.get("bai") and all(b.startswith(PREFIX) for b in row["bai"]):
            out.append(row)  # dòng chỉ của lớp 2 (do session này tạo): lấy cả trạng thái âm thanh vừa tạo
            continue
        extra = [b for b in row.get("bai", []) if b.startswith(PREFIX) and b not in base.get("bai", [])]
        if extra:
            base = dict(base, bai=base.get("bai", []) + extra)
            touched += 1
        out.append(base)
    missing = set(head) - {r["id"] for r in out}
    for mid in sorted(missing):  # dòng HEAD đã bị xoá ở bản làm việc: giữ như HEAD
        out.append(head[mid])
    text = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="\n", suffix=".json", delete=False) as f:
        f.write(text)
        tmp = f.name
    sha = git("hash-object", "-w", tmp).decode().strip()
    mode = git("ls-files", "-s", rel).decode().split()[0]
    git("update-index", "--cacheinfo", f"{mode},{sha},{rel}")
    Path(tmp).unlink()
    print(f"{rel}: thêm {added} dòng, thêm mã bài lớp 2 vào {touched} dòng có sẵn")


def stage_settings(rel="content/tts/settings.json", manifest="content/manifests/audio_manifest.json"):
    """Stage settings.json = HEAD + overrides (bản làm việc) của các mã chỉ thuộc bài lớp 2; phần khác giữ như HEAD."""
    head = json.loads(git("show", f"HEAD:{rel}").decode("utf-8"))
    work = json.loads((REPO / rel).read_text(encoding="utf-8"))
    rows = json.loads((REPO / manifest).read_text(encoding="utf-8"))
    ids = {r["id"] for r in rows if r.get("bai") and all(b.startswith(PREFIX) for b in r["bai"])}
    n = 0
    for audio_id in sorted(ids):
        if audio_id in work["overrides"] and head["overrides"].get(audio_id) != work["overrides"][audio_id]:
            head["overrides"][audio_id] = work["overrides"][audio_id]
            n += 1
    text = json.dumps(head, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="\n", suffix=".json", delete=False) as f:
        f.write(text)
        tmp = f.name
    sha = git("hash-object", "-w", tmp).decode().strip()
    mode = git("ls-files", "-s", rel).decode().split()[0]
    git("update-index", "--cacheinfo", f"{mode},{sha},{rel}")
    Path(tmp).unlink()
    print(f"{rel}: {n} cách đọc riêng của mã lớp 2")


if __name__ == "__main__":
    for rel in sys.argv[1:]:
        if rel.endswith("settings.json"):
            stage_settings(rel)
        else:
            stage(rel)
