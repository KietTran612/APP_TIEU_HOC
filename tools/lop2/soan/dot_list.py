"""Viết content/requests/images_tv2_t1_dot_N.md: các mã tranh `chua_co` của mục lo..hi. Dùng: dot_list.py N lo hi tuần"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
n, lo, hi, weeks = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
rows = {r["id"]: r for r in json.loads((REPO / "content/manifests/image_manifest.json").read_text(encoding="utf-8"))}
seen, lines = set(), []
for f in sorted((REPO / "content/src").glob("tv2_t1_b*.json")):
    s = json.loads(f.read_text(encoding="utf-8"))
    if not lo <= s["lesson_no"] <= hi:
        continue
    for img, desc in s["images"].items():
        if img in seen or rows.get(img, {}).get("status") != "chua_co":
            continue
        seen.add(img)
        lab = f"Bài {s['td_no']}. {s['title']}" if "td_no" in s else s["title"]
        pages = "–".join(map(str, s["source"]["pages"]))
        lines.append(f"| `{img}` | {s['lesson_no']} | {lab} (tr.{pages}) | {desc} |")
head = [f"# Tranh Tiếng Việt 2 tập một — đợt L2-{n} (tuần {weeks}, mục {lo}–{hi})", "",
        "Session TV2 tập 1 gửi session \"Vẽ tranh SGK Tiếng Việt 2 tập 1\". Phiếu vẽ đủ phong cách từng bài ở "
        "`content/requests/images_tv2_t1_bNNN.md`. Nhập bằng `python -m tapdoc import-image` như các đợt trước. "
        "Tranh dùng lại tranh đã có (bút chì, quyển vở, đu đủ, vải...) không nằm trong danh sách này.", "",
        "| Mã | Mục | Bài (trang sách) | Mô tả cảnh |", "|---|---|---|---|"]
out = REPO / f"content/requests/images_tv2_t1_dot_{n}.md"
out.write_text("\n".join(head + lines + ["", f"Tổng: {len(lines)} tranh."]) + "\n", encoding="utf-8")
print(len(lines), " ".join(sorted(seen)))
