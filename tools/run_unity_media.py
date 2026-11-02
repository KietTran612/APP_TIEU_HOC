"""Đóng gói và nhập gói media của TapDoc: tranh, âm thanh (kèm .meta, giữ GUID) và clip tranh động.

Tranh và âm thanh không nằm trong git. Đóng gói xong thì đưa hai file trong `dist/` lên thư mục Google Drive
của dự án; máy mới tải về rồi nhập gói (xem SETUP-MAY-MOI.md).

Cách dùng (chạy từ thư mục tools/, Unity Editor phải đang đóng):
    python run_unity_media.py pack
    python run_unity_media.py unpack ../dist/TapDoc-media-2026-11-02.unitypackage --clips ../dist/TapDoc-clips-2026-11-02.zip
"""
import argparse
import datetime
import subprocess
import sys
import zipfile
from pathlib import Path

from run_unity_tests import (
    BUSY_MARKER,
    BUSY_MESSAGE,
    OUTPUT,
    PROJECT,
    UNITY_EXE,
    print_log_errors,
    project_is_open,
    read_log,
)
from tapdoc.media_lock import compare, describe, missing_meta, write_lock
from tapdoc.paths import CLIPS, MEDIA_LOCK, ROOT, UNITY_RES

RES_DIR = UNITY_RES
CLIPS_DIR = CLIPS
DIST_DIR = ROOT / "dist"
LOCK_PATH = MEDIA_LOCK


def today() -> str:
    return datetime.date.today().isoformat()


def _run_unity(args: list[str], log_name: str, timeout: int) -> tuple[int, str]:
    """Chạy Unity batchmode; trả (mã thoát, log). Mã 2: thiếu Unity, project đang mở hoặc quá giờ."""
    if not UNITY_EXE.exists():
        print(f"Không tìm thấy Unity: {UNITY_EXE}", file=sys.stderr)
        return 2, ""
    if project_is_open():
        print(BUSY_MESSAGE)
        return 2, ""
    OUTPUT.mkdir(parents=True, exist_ok=True)
    log_path = OUTPUT / log_name
    log_path.unlink(missing_ok=True)
    cmd = [str(UNITY_EXE), "-batchmode", "-projectPath", str(PROJECT), *args, "-logFile", str(log_path)]
    try:
        completed = subprocess.run(cmd, timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"Unity chạy quá {timeout} giây, đã dừng.", file=sys.stderr)
        return 2, read_log(log_path)
    log_text = read_log(log_path)
    if BUSY_MARKER in log_text.lower():
        print(BUSY_MESSAGE)
        return 2, log_text
    return completed.returncode, log_text


def pack(timeout: int = 3600) -> int:
    """Xuất tranh và âm thanh (kèm .meta) ra .unitypackage, nén clip ra .zip, rồi ghi khoá media."""
    no_meta = missing_meta(RES_DIR)
    if no_meta:
        print(f"{len(no_meta)} file chưa có .meta (ví dụ {no_meta[0]}): mở Unity cho nhập xong rồi đóng gói lại.")
        return 1
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    package = DIST_DIR / f"TapDoc-media-{today()}.unitypackage"
    package.unlink(missing_ok=True)
    code, log_text = _run_unity(["-executeMethod", "TapDoc.EditorTools.MediaPackage.Export", "-mediaOut", str(package)],
                                "media_pack.log", timeout)
    if code == 2:
        return 2
    if code != 0 or not package.is_file():
        print(f"Đóng gói media thất bại (mã thoát {code}).")
        print_log_errors(log_text)
        return 1
    print(package)
    if CLIPS_DIR.is_dir():
        clips_zip = DIST_DIR / f"TapDoc-clips-{today()}.zip"
        # MP4 đã nén sẵn: chỉ gom vào một file, không nén lại.
        with zipfile.ZipFile(clips_zip, "w", zipfile.ZIP_STORED) as z:
            for clip in sorted(CLIPS_DIR.rglob("*")):
                if clip.is_file():
                    z.write(clip, clip.relative_to(CLIPS_DIR).as_posix())
        print(clips_zip)
    write_lock(RES_DIR, LOCK_PATH, package.name)
    print(f"Đã ghi khoá media: {LOCK_PATH}")
    return 0


def unpack(package: Path, clips_zip: Path | None, timeout: int = 3600) -> int:
    """Nhập gói media vào project (giữ .meta, GUID) và giải nén clip; xong thì so với khoá media."""
    package = Path(package)
    if not package.is_file():
        print(f"Không tìm thấy gói: {package}")
        return 1
    code, log_text = _run_unity(["-importPackage", str(package.resolve()), "-quit"], "media_unpack.log", timeout)
    if code == 2:
        return 2
    if code != 0:
        print(f"Nhập gói media thất bại (mã thoát {code}).")
        print_log_errors(log_text)
        return 1
    if clips_zip is not None:
        CLIPS_DIR.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(clips_zip) as z:
            z.extractall(CLIPS_DIR)
    warning = describe(compare(RES_DIR, LOCK_PATH))
    print(f"Cảnh báo: {warning}" if warning else "Đã nhập gói media.")
    return 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Đóng gói hoặc nhập gói media (tranh, âm thanh, clip) của TapDoc.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("pack", help="xuất dist/TapDoc-media-<ngày>.unitypackage và dist/TapDoc-clips-<ngày>.zip")
    unpack_cmd = commands.add_parser("unpack", help="nhập gói .unitypackage (và zip clip) vào project")
    unpack_cmd.add_argument("package", type=Path)
    unpack_cmd.add_argument("--clips", type=Path, help="file zip clip tranh động")
    parser.add_argument("--timeout", type=int, default=3600, metavar="SECONDS", help="Thời gian chờ Unity tối đa (giây)")
    args = parser.parse_args()
    if args.command == "pack":
        return pack(timeout=args.timeout)
    return unpack(args.package, args.clips, timeout=args.timeout)


if __name__ == "__main__":
    sys.exit(main())
