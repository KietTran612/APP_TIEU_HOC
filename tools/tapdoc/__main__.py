"""Giao diện dòng lệnh: `python -m tapdoc <lệnh>` (chạy từ thư mục `tools`)."""

import argparse
import sys

from .build import BuildError, build_all
from .chatgpt_requests import write_request_files
from .importer import import_audio_zip, import_image
from .manifest import ManifestError, load_rows, save_rows, update_audio_manifest, update_image_manifest
from .paths import CONTENT_SRC, MANIFESTS, REQUESTS_DIR, STYLE_FILE, UNITY_RES
from .review_server import make_server
from .validate import validate_all
from .viet import nfc

_STATUSES = ("chua_co", "cho_duyet", "dat", "khong_dat")


def _status_counts(rows: list[dict]) -> str:
    return ", ".join(f"{status} {sum(1 for row in rows if row['status'] == status)}" for status in _STATUSES)


def _cmd_build(args: argparse.Namespace) -> int:
    if not CONTENT_SRC.is_dir() or not any(CONTENT_SRC.glob("*.json")):
        print(f"Không có nguồn bài trong {CONTENT_SRC}")
        return 1
    out_dir = UNITY_RES / "lessons"
    try:
        results = build_all(CONTENT_SRC, out_dir)
    except BuildError as e:
        print(f"Lỗi dựng bài: {e}", file=sys.stderr)
        return 1
    print(f"Đã dựng {len(results)} bài vào {out_dir}")
    for result in results:
        lesson = result.lesson
        notes = lesson["review"]["can_duyet"]
        print(f"{lesson['lesson_id']} ({lesson['title']}): {len(notes)} mục cần duyệt")
        for note in notes:
            print(f"  {note['where']}: {note['note']}")

    audio_path = MANIFESTS / "audio_manifest.json"
    image_path = MANIFESTS / "image_manifest.json"
    try:
        audio_rows = update_audio_manifest(results, load_rows(audio_path), UNITY_RES / "audio")
        image_rows = update_image_manifest(results, load_rows(image_path), UNITY_RES / "images")
    except ManifestError as e:
        print(f"Lỗi danh mục: {e}", file=sys.stderr)
        return 1
    save_rows(audio_path, audio_rows)
    save_rows(image_path, image_rows)
    print(f"Danh mục âm thanh {audio_path}: {len(audio_rows)} mã ({_status_counts(audio_rows)})")
    print(f"Danh mục tranh {image_path}: {len(image_rows)} mã ({_status_counts(image_rows)})")
    return 0


def _cmd_requests(args: argparse.Namespace) -> int:
    audio_path = MANIFESTS / "audio_manifest.json"
    image_path = MANIFESTS / "image_manifest.json"
    missing = [path for path in (audio_path, image_path) if not path.is_file()]
    if missing:
        print(f"Chưa có danh mục: {', '.join(str(path) for path in missing)}. "
              "Hãy chạy `python -m tapdoc build` trước.", file=sys.stderr)
        return 1
    if not STYLE_FILE.is_file():
        print(f"Không có file phong cách tranh: {STYLE_FILE}", file=sys.stderr)
        return 1
    try:
        audio_rows = load_rows(audio_path)
        image_rows = load_rows(image_path)
    except ManifestError as e:
        print(f"Lỗi danh mục: {e}", file=sys.stderr)
        return 1
    with open(STYLE_FILE, encoding="utf-8") as f:
        style_text = nfc(f.read()).strip()
    written = write_request_files(audio_rows, image_rows, style_text, REQUESTS_DIR, include_khong_dat=args.redo)
    if not written:
        print(f"Không có mã nào cần yêu cầu; đã xóa các file yêu cầu cũ trong {REQUESTS_DIR}")
        return 0
    print(f"Đã ghi {len(written)} file yêu cầu vào {REQUESTS_DIR}:")
    for path in written:
        print(f"  {path.name}")
    return 0


def _printable(text: str) -> str:
    """Tên mục trong ZIP là dữ liệu không đáng tin: đổi ký tự điều khiển thành dạng `\\x1b` trước khi in."""
    return "".join(ch if ch.isprintable() else ch.encode("unicode_escape").decode("ascii") for ch in text)


def _cmd_import_audio(args: argparse.Namespace) -> int:
    manifest_path = MANIFESTS / "audio_manifest.json"
    if not manifest_path.is_file():
        print(f"Chưa có danh mục âm thanh: {manifest_path}. Hãy chạy `python -m tapdoc build` trước.",
              file=sys.stderr)
        return 1
    audio_dir = UNITY_RES / "audio"
    try:
        report = import_audio_zip(args.zip, audio_dir, manifest_path)
    except ValueError as e:
        print(f"Lỗi nhập âm thanh: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"Lỗi ghi file âm thanh: {e}", file=sys.stderr)
        return 1
    print(f"Đã nhập {len(report.imported)} âm thanh vào {audio_dir} (chờ duyệt):")
    for audio_id in report.imported:
        print(f"  {audio_id}")
    if report.skipped:
        print(f"Bỏ qua {len(report.skipped)} mục:")
        for name, reason in report.skipped:
            print(f"  {_printable(name)}: {_printable(reason)}")
    return 0


def _cmd_import_image(args: argparse.Namespace) -> int:
    manifest_path = MANIFESTS / "image_manifest.json"
    if not manifest_path.is_file():
        print(f"Chưa có danh mục tranh: {manifest_path}. Hãy chạy `python -m tapdoc build` trước.", file=sys.stderr)
        return 1
    image_dir = UNITY_RES / "images"
    try:
        import_image(args.file, args.id, image_dir, manifest_path)
    except ValueError as e:
        print(f"Lỗi nhập tranh: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"Lỗi ghi file tranh {args.id}: {e}", file=sys.stderr)
        return 1
    print(f"Đã nhập tranh {args.id} vào {image_dir / (args.id + '.png')} (chờ duyệt)")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    issues = validate_all(allow_missing=args.allow_missing)
    for issue in issues:
        print(_printable(f"{issue.lesson} {issue.where}: {issue.message}"))
    if not issues:
        print("OK")
        return 0
    print(f"{len(issues)} lỗi")
    return 1


def _cmd_review(args: argparse.Namespace) -> int:
    server = make_server(args.port, MANIFESTS, UNITY_RES)
    print(f"Mở http://127.0.0.1:{args.port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(prog="python -m tapdoc", description="Công cụ nội dung của app Tập đọc.")
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("build", help="dựng file bài học từ nguồn trong content/src")
    build.set_defaults(func=_cmd_build)
    requests = commands.add_parser(
        "requests", help="ghi gói yêu cầu ChatGPT (âm thanh, tranh) cho các mã chưa có file")
    requests.add_argument("--redo", action="store_true", help="yêu cầu cả các mã đã đánh dấu khong_dat")
    requests.set_defaults(func=_cmd_requests)
    audio_cmd = commands.add_parser("import-audio", help="nhập file ZIP âm thanh đã tải về từ ChatGPT")
    audio_cmd.add_argument("zip", help="đường dẫn file ZIP")
    audio_cmd.set_defaults(func=_cmd_import_audio)
    image_cmd = commands.add_parser("import-image", help="nhập một tranh PNG đã tải về từ ChatGPT")
    image_cmd.add_argument("file", help="đường dẫn file PNG")
    image_cmd.add_argument("id", help="mã tranh trong danh mục (ví dụ img_b13_cais_ddu)")
    image_cmd.set_defaults(func=_cmd_import_image)
    validate_cmd = commands.add_parser("validate", help="kiểm tra file bài đã dựng, danh mục và project Unity")
    validate_cmd.add_argument("--allow-missing", action="store_true",
                              help="bỏ qua việc kiểm tra file âm thanh/tranh còn thiếu")
    validate_cmd.set_defaults(func=_cmd_validate)
    review_cmd = commands.add_parser("review", help="mở trang web nội bộ để nghe duyệt âm thanh và xem duyệt tranh")
    review_cmd.add_argument("--port", type=int, default=8765, help="cổng lắng nghe trên 127.0.0.1 (mặc định 8765)")
    review_cmd.set_defaults(func=_cmd_review)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
