"""Tạo âm thanh HoaiMy cho các mã lớp 2 còn `chua_co`: 1 tiến trình, mỗi mã tối đa 90 giây, tiếng lẻ đọc trong câu
đệm (--tieng-keep-first), chạy thêm lượt bù cho mã còn rỗng. Dùng (từ gốc repo): python tools/lop2/tts_lop2.py <số lượt> [bài đầu=172] [bài cuối=304] [--giu-may-thuc]
Log: .superpowers/tts_lop2.log. --giu-may-thuc: xin Windows không cho máy nghỉ khi script còn chạy."""
import json
import subprocess
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
MANIFEST = TOOLS.parent / "content" / "manifests" / "audio_manifest.json"
LOG = TOOLS.parent / ".superpowers" / "tts_lop2.log"  # ngoài git


sys.path.insert(0, str(TOOLS))
from tapdoc.tts_settings import load_settings, differs_from_settings  # noqa: E402
SETTINGS = TOOLS.parent / "content" / "tts" / "settings.json"


def pending(lo, hi):
    """Mã chỉ thuộc bài lớp 2 (mọi bài tv2_t1_*), chưa 'dat', còn chua_co hoặc khác cấu hình (cần tạo lại)."""
    rows = json.loads(MANIFEST.read_text(encoding="utf-8"))
    settings = load_settings(SETTINGS)
    out = []
    for r in rows:
        bai = r.get("bai", [])
        if not bai or not all(b.startswith("tv2_t1_b") for b in bai) or r.get("status") == "dat":
            continue
        nos = [int(b.rsplit("_b", 1)[1]) for b in bai]
        if any(lo <= n <= hi for n in nos) and (r.get("status") == "chua_co" or differs_from_settings(settings, r)):
            out.append(r["id"])
    return out


def log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(time.strftime("%H:%M:%S ") + msg + "\n")


def keep_awake():
    """Xin Windows không cho máy nghỉ khi tiến trình này còn chạy (ES_CONTINUOUS | ES_SYSTEM_REQUIRED); tự hết khi tiến trình thoát."""
    try:
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
    except Exception:
        pass


def main():
    if "--giu-may-thuc" in sys.argv:
        sys.argv.remove("--giu-may-thuc")
        keep_awake()
    passes = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    lo = int(sys.argv[2]) if len(sys.argv) > 2 else 172
    hi = int(sys.argv[3]) if len(sys.argv) > 3 else 304
    for p in range(passes):
        ids = pending(lo, hi)
        log(f"lượt {p + 1}: {len(ids)} mã")
        ok = fail = 0
        for audio_id in ids:
            try:
                res = subprocess.run([sys.executable, "-m", "tapdoc", "tts", "--tieng-keep-first", "--ma", audio_id],
                                     cwd=TOOLS, capture_output=True, timeout=90)
                if res.returncode == 0:
                    ok += 1
                else:
                    fail += 1
                    log(f"lỗi {audio_id}: {res.stderr.decode('utf-8', 'replace').strip()[-160:]}")
            except subprocess.TimeoutExpired:
                fail += 1
                log(f"quá 90 giây {audio_id}")
        log(f"xong lượt {p + 1}: tạo {ok}, lỗi {fail}")
    log(f"còn chua_co: {len(pending(lo, hi))}")


if __name__ == "__main__":
    main()
