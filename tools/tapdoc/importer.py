"""Nhập file tải về từ ChatGPT (ZIP âm thanh, tranh PNG) vào project Unity theo mã.

File tải về là dữ liệu không đáng tin, nên:
- ZIP không bao giờ được giải nén ra đĩa: từng mục được đọc thẳng vào bộ nhớ, và chỉ ghi ra
  `audio_dir/<mã>.mp3`. Đường dẫn trong ZIP không bao giờ được dùng để dựng đường dẫn ghi.
- Mã (tên file) chỉ gồm `a-z`, `0-9`, `_`, và phải có trong danh mục.
- Nội dung phải đúng loại (MP3, PNG) và không quá lớn.
- Ghi vào file tạm cạnh đích rồi `os.replace`, nên không bao giờ để lại file ghi dở.

File nhập xong được đánh dấu `cho_duyet`, nguồn `chatgpt_tam` trong danh mục.
"""

import contextlib
import os
import re
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

from .manifest import STATUS_PENDING, TEXT_CHANGED_NOTE, load_rows, save_rows

SOURCE_TEMP = "chatgpt_tam"  # file tạm lấy từ ChatGPT, chờ chủ dự án duyệt

_MB = 1024 * 1024
MAX_AUDIO_BYTES = 5 * _MB  # trần dung lượng giải nén của một mục âm thanh (chặn zip bomb)
MAX_IMAGE_BYTES = 20 * _MB

_ID_RE = re.compile(r"[a-z0-9_]+")
_AUDIO_NAME_RE = re.compile(r"([a-z0-9_]+)\.mp3")  # fullmatch: `$` sẽ chấp nhận cả "\n" ở cuối
_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


@dataclass
class ImportReport:
    imported: list[str] = field(default_factory=list)  # các mã đã nhập
    skipped: list[tuple[str, str]] = field(default_factory=list)  # (tên mục trong ZIP, lý do bỏ qua)


def _looks_like_mp3(data: bytes) -> bool:
    """Bắt đầu bằng thẻ ID3, hoặc bằng byte đồng bộ khung MPEG (0xFF rồi 3 bit cao của byte sau đều là 1)."""
    if data.startswith(b"ID3"):
        return True
    return len(data) >= 2 and data[0] == 0xFF and (data[1] & 0xE0) == 0xE0


def _write_atomic(dest: Path, data: bytes) -> None:
    """Ghi `data` vào `dest` qua file tạm cùng thư mục (tên bắt đầu bằng "." nên Unity bỏ qua)."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=dest.parent, prefix=".nhap_", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp_name, dest)
    except BaseException:
        with contextlib.suppress(OSError):
            os.unlink(tmp_name)
        raise


def _without_changed_note(note: str) -> str:
    """Bỏ ghi chú tự động `TEXT_CHANGED_NOTE` khi đã nhập file mới, giữ lại ghi chú riêng (nếu có)."""
    if TEXT_CHANGED_NOTE not in note:
        return note
    parts = [part.strip() for part in note.split(";") if part.strip() and part.strip() != TEXT_CHANGED_NOTE]
    return "; ".join(parts)


def import_audio_zip(zip_path, audio_dir, manifest_path) -> ImportReport:
    """Nhập các file `<mã>.mp3` trong ZIP vào `audio_dir`; mục không hợp lệ thì bỏ qua kèm lý do.

    Chỉ xét tên file cuối của mỗi mục (tách theo `/` và `\\`); mục thư mục bị bỏ qua im lặng.
    Một mã xuất hiện nhiều lần trong ZIP thì mục nhập được đầu tiên thắng. Danh mục được lưu
    một lần ở cuối, và chỉ khi có mã được nhập. File không phải ZIP thì báo `ValueError`.
    """
    zip_path = Path(zip_path)
    audio_dir = Path(audio_dir)
    try:
        archive_ctx = zipfile.ZipFile(zip_path)
    except (zipfile.BadZipFile, NotImplementedError, UnicodeDecodeError) as e:
        raise ValueError(f"{zip_path} không phải file ZIP hợp lệ") from e
    except OSError as e:
        raise ValueError(f"Không mở được file ZIP {zip_path}: {e}") from e

    with archive_ctx as archive:
        all_rows = load_rows(manifest_path)
        rows = {row["id"]: row for row in all_rows}
        report = ImportReport()
        try:
            for info in archive.infolist():
                name = info.filename
                base = re.split(r"[/\\]", name)[-1]
                if not base:
                    continue  # mục thư mục
                match = _AUDIO_NAME_RE.fullmatch(base)
                if match is None:
                    report.skipped.append(
                        (name, "tên file không đúng dạng <mã>.mp3 (mã chỉ gồm a-z, 0-9, gạch dưới)"))
                    continue
                audio_id = match.group(1)
                row = rows.get(audio_id)
                if row is None:
                    report.skipped.append((name, f"mã {audio_id} không có trong danh mục âm thanh"))
                    continue
                if info.file_size > MAX_AUDIO_BYTES:
                    report.skipped.append(
                        (name, f"quá lớn ({info.file_size / _MB:.1f} MB, tối đa {MAX_AUDIO_BYTES // _MB} MB)"))
                    continue
                if audio_id in report.imported:
                    report.skipped.append((name, f"trùng mã {audio_id}: đã nhập từ mục trước trong ZIP"))
                    continue
                try:
                    with archive.open(info) as member_file:
                        data = member_file.read(MAX_AUDIO_BYTES + 1)
                except Exception as e:  # zipfile, zlib, lzma... báo nhiều loại lỗi khi mục bị hỏng hoặc mã hóa
                    report.skipped.append((name, f"không đọc được mục này trong ZIP ({e})"))
                    continue
                if len(data) > MAX_AUDIO_BYTES:
                    report.skipped.append((name, f"quá lớn (vượt tối đa {MAX_AUDIO_BYTES // _MB} MB)"))
                    continue
                if not _looks_like_mp3(data):
                    report.skipped.append(
                        (name, "nội dung không phải MP3 (không bắt đầu bằng ID3 hay đồng bộ khung MPEG)"))
                    continue
                try:
                    _write_atomic(audio_dir / f"{audio_id}.mp3", data)
                except OSError as e:
                    report.skipped.append((name, f"không ghi được file {audio_id}.mp3: {e}"))
                    continue
                row["status"] = STATUS_PENDING
                row["source"] = SOURCE_TEMP
                row["ghi_chu"] = _without_changed_note(row.get("ghi_chu", ""))
                report.imported.append(audio_id)
        finally:
            if report.imported:
                save_rows(manifest_path, all_rows)
    return report


def import_image(file_path, image_id, image_dir, manifest_path) -> None:
    """Chép tranh PNG thành `image_dir/<image_id>.png` và đánh dấu `cho_duyet`; sai thì báo `ValueError`."""
    file_path = Path(file_path)
    image_dir = Path(image_dir)
    if not file_path.is_file():
        raise ValueError(f"Không tìm thấy file tranh: {file_path}")
    try:
        with open(file_path, "rb") as f:
            data = f.read(MAX_IMAGE_BYTES + 1)  # đọc quá trần một byte để biết file có vượt trần không
    except OSError as e:
        raise ValueError(f"Không đọc được file tranh {file_path}: {e}") from e
    if not data.startswith(_PNG_SIGNATURE):
        raise ValueError(f"{file_path.name} không phải file PNG (đầu file không có chữ ký PNG)")
    all_rows = load_rows(manifest_path)
    row = next((r for r in all_rows if r["id"] == image_id), None)
    if row is None or not _ID_RE.fullmatch(image_id):
        raise ValueError(f"Mã tranh {image_id} không có trong danh mục tranh")
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError(f"{file_path.name} quá lớn (tối đa {MAX_IMAGE_BYTES // _MB} MB)")
    _write_atomic(image_dir / f"{image_id}.png", data)
    row["status"] = STATUS_PENDING
    row["source"] = SOURCE_TEMP
    row["ghi_chu"] = _without_changed_note(row.get("ghi_chu", ""))
    save_rows(manifest_path, all_rows)
