"""Đóng gói và nhập gói media của TapDoc: tranh, âm thanh (kèm .meta, giữ GUID) và clip tranh động.

Tranh và âm thanh không nằm trong git. Đóng gói xong thì đưa hai file trong `dist/` lên thư mục Google Drive
của dự án; máy mới tải về rồi nhập gói (xem CHUYEN-MAY-MOI.md).

Gói bổ sung: sau khi gói lớn đã lên Drive, chỉ gói phần tranh, âm thanh (kèm .meta) và clip đã đổi so với khoá
thành `dist/TapDoc-bosung-<ngày>.zip`; máy mới nhập gói lớn rồi nhập lần lượt các gói bổ sung.

Cách dùng (chạy từ thư mục tools/, Unity Editor phải đang đóng):
    python run_unity_media.py pack
    python run_unity_media.py bosung
    python run_unity_media.py unpack ../dist/TapDoc-media-2026-11-02.unitypackage --clips ../dist/TapDoc-clips-2026-11-02.zip \
        --bosung ../dist/TapDoc-bosung-2026-11-10.zip
"""
import argparse
import datetime
import json
import subprocess
import zlib
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
from tapdoc.media_lock import compare, describe, missing_meta, snapshot, write_lock
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


def _zip_crcs(zip_path: Path, prefix: str = "") -> dict[str, int]:
    """Tên file (bỏ tiền tố) và CRC32 trong zip; dùng để biết clip nào đã gửi."""
    with zipfile.ZipFile(zip_path) as z:
        return {i.filename[len(prefix):]: i.CRC for i in z.infolist()
                if not i.is_dir() and i.filename.startswith(prefix)}


def _bosung_path(date: str) -> Path:
    path = DIST_DIR / f"TapDoc-bosung-{date}.zip"
    n = 2
    while path.exists():
        path = DIST_DIR / f"TapDoc-bosung-{date}-{n}.zip"
        n += 1
    return path


def pack_bosung() -> int:
    """Gói phần media đổi so với khoá (kèm .meta) và clip chưa có trong các gói trước; xong thì cập nhật khoá."""
    if not LOCK_PATH.is_file():
        print(f"Chưa có khoá media {LOCK_PATH}: đóng gói đầy đủ trước (python run_unity_media.py pack).")
        return 1
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    base_clips = DIST_DIR / lock["package"].replace("TapDoc-media-", "TapDoc-clips-").replace(".unitypackage", ".zip")
    if not base_clips.is_file():
        print(f"Không thấy zip clip của gói gốc: {base_clips}")
        return 1
    sent = _zip_crcs(base_clips)
    for name in lock.get("bosung", []):
        if (DIST_DIR / name).is_file():
            sent.update(_zip_crcs(DIST_DIR / name, "clips/"))
    diff = compare(RES_DIR, LOCK_PATH)
    media = diff.changed + diff.extra
    no_meta = [rel for rel in media if not (RES_DIR / (rel + ".meta")).is_file()]
    if no_meta:
        print(f"{len(no_meta)} file chưa có .meta (ví dụ {no_meta[0]}): mở Unity cho nhập xong rồi đóng gói lại.")
        return 1
    clips = []
    if CLIPS_DIR.is_dir():
        for clip in sorted(CLIPS_DIR.rglob("*")):
            rel = clip.relative_to(CLIPS_DIR).as_posix()
            if clip.is_file() and sent.get(rel) != zlib.crc32(clip.read_bytes()):
                clips.append(rel)
    if not (media or clips or diff.missing):
        print("Không có media nào đổi so với khoá: không cần gói bổ sung.")
        return 0
    out = _bosung_path(today())
    # MP3, PNG, MP4 đã nén sẵn: chỉ gom vào một file, không nén lại.
    with zipfile.ZipFile(out, "w", zipfile.ZIP_STORED) as z:
        z.writestr("bosung.json", json.dumps({"goc": lock["package"], "xoa": diff.missing}, ensure_ascii=False, indent=2))
        for rel in media:
            z.write(RES_DIR / rel, f"Resources/{rel}")
            z.write(RES_DIR / (rel + ".meta"), f"Resources/{rel}.meta")
        for rel in clips:
            z.write(CLIPS_DIR / rel, f"clips/{rel}")
    lock = {"package": lock["package"], "bosung": [*lock.get("bosung", []), out.name], "files": snapshot(RES_DIR)}
    LOCK_PATH.write_text(json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out)
    print(f"Tranh, âm thanh: đổi {len(diff.changed)}, mới {len(diff.extra)}, xoá {len(diff.missing)}; clip: {len(clips)}")
    print(f"Đã cập nhật khoá media: {LOCK_PATH}")
    return 0


def _inside(base: Path, rel: str) -> Path | None:
    """Đường dẫn đích nếu nằm trong base; đường dẫn lạ (../) thì None."""
    target = (base / rel).resolve()
    return target if target.is_relative_to(base.resolve()) else None


def apply_bosung(zip_path: Path) -> int:
    """Chép file trong gói bổ sung vào Resources và thư mục clip, xoá file gói ghi là đã bỏ."""
    with zipfile.ZipFile(zip_path) as z:
        info = json.loads(z.read("bosung.json"))
        plan = []
        for name in z.namelist():
            if name == "bosung.json" or name.endswith("/"):
                continue
            target = None
            for prefix, base in (("Resources/", RES_DIR), ("clips/", CLIPS_DIR)):
                if name.startswith(prefix):
                    target = _inside(base, name[len(prefix):])
            if target is None:
                print(f"Gói bổ sung {zip_path.name} có đường dẫn lạ: {name}")
                return 1
            plan.append((name, target))
        for name, target in plan:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(z.read(name))
    removed = info.get("xoa", [])
    for rel in removed:
        target = _inside(RES_DIR, rel)
        if target is not None:
            target.unlink(missing_ok=True)
            target.with_name(target.name + ".meta").unlink(missing_ok=True)
    print(f"Đã nhập gói bổ sung {zip_path.name}: {len(plan)} file, xoá {len(removed)}")
    return 0


def unpack(package: Path, clips_zip: Path | None, timeout: int = 3600, bosung: list[Path] | None = None) -> int:
    """Nhập gói media (giữ .meta, GUID), giải nén clip, nhập các gói bổ sung theo thứ tự; xong thì so với khoá."""
    package = Path(package)
    if not package.is_file():
        print(f"Không tìm thấy gói: {package}")
        return 1
    bosung = [Path(b) for b in bosung or []]
    missing = [b for b in bosung if not b.is_file()]
    if missing:
        print(f"Không tìm thấy gói bổ sung: {missing[0]}")
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
    for zip_path in bosung:
        if apply_bosung(zip_path) != 0:
            return 1
    warning = describe(compare(RES_DIR, LOCK_PATH))
    print(f"Cảnh báo: {warning}" if warning else "Đã nhập gói media.")
    return 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Đóng gói hoặc nhập gói media (tranh, âm thanh, clip) của TapDoc.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("pack", help="xuất dist/TapDoc-media-<ngày>.unitypackage và dist/TapDoc-clips-<ngày>.zip")
    commands.add_parser("bosung", help="gói phần media đổi so với khoá ra dist/TapDoc-bosung-<ngày>.zip")
    unpack_cmd = commands.add_parser("unpack", help="nhập gói .unitypackage (và zip clip, gói bổ sung) vào project")
    unpack_cmd.add_argument("package", type=Path)
    unpack_cmd.add_argument("--clips", type=Path, help="file zip clip tranh động")
    unpack_cmd.add_argument("--bosung", type=Path, action="append", default=[],
                            help="gói bổ sung, nhập sau gói chính; nhiều gói thì ghi nhiều lần theo thứ tự")
    parser.add_argument("--timeout", type=int, default=3600, metavar="SECONDS", help="Thời gian chờ Unity tối đa (giây)")
    args = parser.parse_args()
    if args.command == "pack":
        return pack(timeout=args.timeout)
    if args.command == "bosung":
        return pack_bosung()
    return unpack(args.package, args.clips, timeout=args.timeout, bosung=args.bosung)


if __name__ == "__main__":
    sys.exit(main())
