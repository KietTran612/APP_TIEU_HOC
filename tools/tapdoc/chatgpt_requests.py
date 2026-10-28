"""Gói yêu cầu để dán vào ChatGPT: tạo âm thanh tạm và tranh tạm (chủ dự án duyệt rồi thay bản thật)."""

import re
from pathlib import Path

from .manifest import STATUS_BAD, STATUS_NONE

AUDIO_HEADER = (
    "Hãy tạo file âm thanh tiếng Việt, giọng nữ miền Nam, đọc chậm và rõ, mỗi dòng một file.\n"
    "- Tên file: đúng cột id, đuôi .mp3 (ví dụ am_dd.mp3).\n"
    "- Chỉ đọc đúng chữ ở cột text, không thêm lời nào khác.\n"
    "- Dòng có doc_ky = x: đọc rõ theo chính tả, phân biệt dấu hỏi và dấu ngã.\n"
    "- Gom tất cả vào một file ZIP để tải về.\n"
    "\n"
    "id,text,doc_ky\n"
)

AUDIO_BATCH_SIZE = 60

_AUDIO_FILE_GLOB = "audio_*.txt"
_IMAGE_FILE_GLOB = "images_*.md"
_NEWLINES = re.compile(r"\s*[\r\n]+\s*")


def _wanted(rows: list[dict], include_khong_dat: bool) -> list[dict]:
    statuses = {STATUS_NONE, STATUS_BAD} if include_khong_dat else {STATUS_NONE}
    return [row for row in rows if row.get("status") in statuses]


def _csv_text(text: str) -> str:
    one_line = _NEWLINES.sub(" ", text).strip()
    if "," in one_line:
        return '"' + one_line.replace('"', '""') + '"'
    return one_line


def audio_requests(rows: list[dict], batch_size: int = AUDIO_BATCH_SIZE,
                   include_khong_dat: bool = False) -> list[str]:
    """Lời yêu cầu tạo âm thanh cho các dòng `chua_co` (thêm `khong_dat` nếu `include_khong_dat`).

    Mỗi lời yêu cầu gồm phần mở đầu cố định và tối đa `batch_size` dòng `id,text,doc_ky`.
    """
    if batch_size < 1:
        raise ValueError(f"batch_size phải từ 1 trở lên: {batch_size}")
    wanted = _wanted(rows, include_khong_dat)
    prompts = []
    for start in range(0, len(wanted), batch_size):
        lines = [f"{row['id']},{_csv_text(row['text'])},{'x' if row.get('can_nghe_ky') else ''}\n"
                 for row in wanted[start:start + batch_size]]
        prompts.append(AUDIO_HEADER + "".join(lines))
    return prompts


def image_requests(rows: list[dict], style_text: str,
                   include_khong_dat: bool = False) -> dict[str, list[tuple[str, str]]]:
    """Mã bài (hoặc "chung") -> [(mã tranh, lời yêu cầu)] cho các dòng `chua_co` (và `khong_dat` nếu được hỏi)."""
    grouped: dict[str, list[tuple[str, str]]] = {}
    for row in _wanted(rows, include_khong_dat):
        prompt = (style_text + "\nVẽ: " + row["mo_ta"]
                  + "\n(Mã tranh: " + row["id"] + ". Không viết mã này lên tranh.)")
        grouped.setdefault(row["bai"][0], []).append((row["id"], prompt))
    return grouped


def _write_text(path: Path, text: str) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_request_files(audio_rows: list[dict], image_rows: list[dict], style_text: str, out_dir,
                        include_khong_dat: bool = False) -> list[Path]:
    """Xóa các file yêu cầu cũ rồi ghi `audio_NN.txt` và `images_<bài hoặc chung>.md`; trả về các file đã ghi."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for pattern in (_AUDIO_FILE_GLOB, _IMAGE_FILE_GLOB):
        for old in out.glob(pattern):
            if old.is_file():
                old.unlink()

    written = []
    for number, prompt in enumerate(audio_requests(audio_rows, include_khong_dat=include_khong_dat), start=1):
        path = out / f"audio_{number:02d}.txt"
        _write_text(path, prompt)
        written.append(path)
    by_lesson = image_requests(image_rows, style_text, include_khong_dat=include_khong_dat)
    for lesson_id in sorted(by_lesson):
        path = out / f"images_{lesson_id}.md"
        _write_text(path, "".join(f"## {image_id}\n\n{prompt}\n\n" for image_id, prompt in by_lesson[lesson_id]))
        written.append(path)
    return written
