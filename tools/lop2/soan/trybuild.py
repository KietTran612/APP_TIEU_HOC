import sys, json
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tapdoc.build import build_lesson, BuildError
lo, hi = int(sys.argv[1]), int(sys.argv[2])
for n in range(lo, hi + 1):
    p = Path(__file__).resolve().parents[3] / "content" / "src" / f"tv2_t1_b{n}.json"
    if not p.is_file():
        print(n, "chưa có"); continue
    try:
        r = build_lesson(json.loads(p.read_text(encoding="utf-8")))
        print(n, "ok", len(r.lesson["part1"]), "bước,", len(r.audio), "mã âm,", len(r.lesson["review"]["can_duyet"]), "cần duyệt")
    except BuildError as e:
        print(n, "LỖI", e)
