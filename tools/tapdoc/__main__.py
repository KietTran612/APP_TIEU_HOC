"""Giao diện dòng lệnh: `python -m tapdoc <lệnh>` (chạy từ thư mục `tools`)."""

import argparse
import sys
import threading
import webbrowser

from .books import load_books
from .build import BuildError, build_all
from .chatgpt_requests import write_request_files
from .importer import import_audio_zip, import_clips, import_image
from .launcher import ensure_edge_tts, tool_running
from .manifest import (ManifestError, keep_concurrent_tts, load_rows, save_rows, update_audio_manifest,
                       update_image_manifest)
from .media_lock import compare as compare_media, describe as describe_media
from .paths import CLIPS, CONTENT_SRC, MANIFESTS, MEDIA_LOCK, REQUESTS_DIR, ROOT, STYLE_FILE, UNITY_RES
from .review_server import make_server
from .sfx_default import write_missing as write_default_sfx
from .ui_icons import write_all as write_ui_icons
from .validate import release_warnings, validate_all
from .viet import nfc

_STATUSES = ("chua_co", "cho_duyet", "dat", "khong_dat")
TTS_SETTINGS = ROOT / "content" / "tts" / "settings.json"
TTS_PREV = ROOT / "content" / "tts" / "prev"
TTS_PITCH_CACHE = ROOT / "content" / "tts" / "pitch_cache"  # WAV giải mã để đo cao độ (chỉ trên máy)
TTS_MARKS = ROOT / "content" / "tts" / "marks"  # mốc từng tiếng của file vừa tạo (chỉ trên máy), để đo cao độ
REVIEW_PORT = 8765  # cổng của công cụ duyệt, dùng chung cho lệnh review và mo


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
        read_rows = load_rows(audio_path)
        audio_rows = update_audio_manifest(results, read_rows, UNITY_RES / "audio")
        image_rows = update_image_manifest(results, load_rows(image_path), UNITY_RES / "images")
        # Lệnh tts có thể đang chạy song song: đọc lại ngay trước khi ghi để không xoá kết quả vừa tạo.
        audio_rows = keep_concurrent_tts(audio_rows, read_rows, load_rows(audio_path))
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
        import_image(args.file, args.id, image_dir, manifest_path, scan_placeholder=args.scan_tam)
    except ValueError as e:
        print(f"Lỗi nhập tranh: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"Lỗi ghi file tranh {args.id}: {e}", file=sys.stderr)
        return 1
    print(f"Đã nhập tranh {args.id} vào {image_dir / (args.id + '.png')} (chờ duyệt)")
    return 0


def _cmd_import_clips(args: argparse.Namespace) -> int:
    try:
        report = import_clips(args.folder, CLIPS, MANIFESTS / "video_manifest.json",
                              MANIFESTS / "image_manifest.json")
    except ManifestError as e:
        print(f"Lỗi đọc danh mục: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"Lỗi ghi clip: {e}", file=sys.stderr)
        return 1
    print(f"Đã nhập {len(report.imported)} clip vào {CLIPS} (chờ duyệt)")
    if report.skipped:
        print(f"Bỏ qua {len(report.skipped)} file:")
        for name, reason in report.skipped:
            print(f"  {_printable(name)}: {_printable(reason)}")
    return 0


def _cmd_ui_icons(args: argparse.Namespace) -> int:
    image_dir = UNITY_RES / "images"
    written = write_ui_icons(image_dir, force=args.force, book_ids=[b["book_id"] for b in load_books()])
    for image_id in written:
        print(f"Đã ghi {image_dir / (image_id + '.png')}")
    print(f"Hình mặc định: ghi {len(written)} file" if written else "Hình mặc định: đã đủ, không ghi gì")
    return 0


def _cmd_sfx_default(args: argparse.Namespace) -> int:
    sfx_dir = UNITY_RES / "sfx"
    written = write_default_sfx(sfx_dir)
    for sfx_id in written:
        print(f"Đã ghi {sfx_dir / (sfx_id + '.wav')}")
    print(f"Tiếng động mặc định: ghi {len(written)} file" if written else "Tiếng động mặc định: đã đủ, không ghi gì")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    issues = validate_all(allow_missing=args.allow_missing, release=args.release)
    if args.release:
        try:
            rows = load_rows(MANIFESTS / "audio_manifest.json")
        except ManifestError:
            rows = []  # validate_all đã báo lỗi đọc danh mục
        for warning in release_warnings(rows):
            print(_printable(f"Cảnh báo: {warning}"))
    media = describe_media(compare_media(UNITY_RES, MEDIA_LOCK))
    if media:
        print(_printable(f"Cảnh báo: {media}"))
    for issue in issues:
        print(_printable(f"{issue.lesson} {issue.where}: {issue.message}"))
    if not issues:
        print("OK")
        return 0
    print(f"{len(issues)} lỗi")
    return 1


def _review_server(port: int, engine_factory=None):
    return make_server(port, MANIFESTS, UNITY_RES,
                       settings_path=TTS_SETTINGS, prev_dir=TTS_PREV,
                       lessons_dir=UNITY_RES / "lessons",
                       notes_path=ROOT / "content/review/chain_notes.json",
                       engine_factory=engine_factory)


def _serve(server) -> int:
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


def _cmd_review(args: argparse.Namespace) -> int:
    try:
        server = _review_server(args.port, getattr(args, "engine_factory", None))
    except OSError as e:
        print(f"Cổng {args.port} đang bận (có thể công cụ duyệt đã mở sẵn): {e}")
        return 1
    print(f"Mở http://127.0.0.1:{server.server_address[1]}/")  # cổng thật, kể cả khi --port 0
    return _serve(server)


def _cmd_open(args: argparse.Namespace) -> int:
    url = f"http://127.0.0.1:{args.port}/"
    if tool_running(args.port):
        print(f"Công cụ duyệt đang chạy, mở lại trang {url}", flush=True)
        webbrowser.open(url)
        return 0
    ensure_edge_tts()
    try:
        server = _review_server(args.port)
    except OSError:
        server = _review_server(0)  # chương trình khác đang giữ cổng thì lấy cổng trống bất kỳ
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    print(f"Đang chạy công cụ duyệt tại {url}", flush=True)
    print("Đóng cửa sổ này để tắt công cụ.", flush=True)
    # Máy chủ đã nghe trên cổng từ lúc tạo, trình duyệt mở trước serve_forever vẫn được trả lời.
    threading.Thread(target=webbrowser.open, args=(url,), daemon=True).start()
    return _serve(server)


def _cmd_tts(args: argparse.Namespace) -> int:
    from .tts_engine import EdgeEngine, TtsUnavailable
    from .tts_generate import run_batch, selected
    from .tts_settings import ensure_keep_first, load_settings, save_settings

    path = MANIFESTS / "audio_manifest.json"
    try:
        if not path.is_file():
            raise ValueError(f"Chưa có danh mục âm thanh: {path}")
        rows = load_rows(path)
        settings = load_settings(TTS_SETTINGS)
        filters = dict(lesson=args.bai, kind=args.loai, ids=args.ma,
                       include_approved=args.gom_da_duyet)
        if args.tieng_keep_first:
            # Tiếng lẻ đọc trong câu đệm "X, X." (HoaiMy đọc hỏi/ngã lẻ thành huyền). Áp TRƯỚC khi chọn mã, để tiếng đã
            # có file theo cách đọc cũ cũng được tạo lại. Mã đã duyệt chỉ đổi khi có --gom-da-duyet.
            # Đọc lại cấu hình ngay trước khi ghi để không xoá chỉnh sửa vừa lưu từ công cụ duyệt.
            fresh = load_settings(TTS_SETTINGS)
            candidates = [r for r in rows if r.get("kind") == "tieng"
                          and (args.bai is None or args.bai in r.get("bai", []))
                          and (args.loai is None or args.loai == "tieng")
                          and (args.ma is None or r["id"] in args.ma)
                          and (args.gom_da_duyet or r.get("status") != "dat")]
            changed = [r["id"] for r in candidates if ensure_keep_first(fresh, r["id"], r["text"])]
            settings = fresh
            if changed and not args.thu:
                save_settings(TTS_SETTINGS, fresh)
                print(f"Đọc trong câu đệm: {len(changed)} tiếng lẻ")
        wanted = [row for row in rows if selected(row, settings, **filters)]
        if args.thu:
            for row in wanted:
                print(row["id"])
            print(f"Sẽ tạo {len(wanted)} mã")
            return 0
        if not wanted:
            print(f"Đã tạo 0, lỗi 0, bỏ qua {len(rows)}")
            return 0
        engine = (args.engine_factory or EdgeEngine)()
        written = list(rows)

        def save(updated):
            # Chỉ ghi dòng vừa tạo vào danh mục mới nhất: đánh giá lưu từ trang duyệt trong lúc chạy không bị ghi đè.
            fresh = {}
            for index, current in enumerate(updated):
                if current is not written[index]:
                    fresh[current["id"]] = current
                    written[index] = current
            if fresh:
                save_rows(path, [fresh.get(r["id"], r) for r in load_rows(path)])

        report = run_batch(rows, settings, engine, UNITY_RES / "audio", TTS_PREV, **filters, save=save,
                           marks_dir=TTS_MARKS)
    except TtsUnavailable as e:
        print(str(e), file=sys.stderr)
        return 2
    except (OSError, ValueError) as e:
        print(f"Lỗi tạo âm thanh: {e}", file=sys.stderr)
        return 1
    print(f"Đã tạo {len(report.done)}, lỗi {len(report.failed)}, bỏ qua {report.skipped}")
    for audio_id, reason in report.failed.items():
        print(_printable(f"  {audio_id}: {reason}"), file=sys.stderr)
    return 1 if report.failed else 0


def _cmd_pitch(args: argparse.Namespace) -> int:
    """Đo cao độ các tiếng hỏi/ngã của mã đã chọn; in mã không đạt (thiết kế TV2 tập một, mục 9)."""
    from . import pitch_check

    rows = load_rows(MANIFESTS / "audio_manifest.json")
    wanted = [r for r in rows if (args.bai is None or args.bai in r.get("bai", []))
              and (args.ma is None or r["id"] in args.ma)]
    audio_dir = UNITY_RES / "audio"
    templates = pitch_check.reference_templates(rows, audio_dir, TTS_PITCH_CACHE / "refs")
    if not pitch_check.has_dip_rise_templates(templates):
        print("Chưa đủ mẫu thanh điệu: cần tiếng lẻ đã duyệt (dat) có file âm thanh trên máy "
              "(nhập gói media trước: python tools/run_unity_media.py unpack)")
        return 2
    results = pitch_check.check_rows(wanted, audio_dir, TTS_MARKS, TTS_PITCH_CACHE, templates)
    failed = [r for r in results if r["ok"] is False]
    unchecked = [r for r in results if r["ok"] is None]
    for r in failed:
        print(_printable(f"KHÔNG ĐẠT {r['id']}: {r['word']} ({r['tone']}) nghe như {r['best']}"))
    for r in unchecked:
        print(_printable(f"chưa đo {r['id']}: {r['word']} — {r['why']}"))
    print(f"Đã đo {len(results)} tiếng hỏi/ngã: đạt {len(results) - len(failed) - len(unchecked)}, "
          f"không đạt {len(failed)}, chưa đo {len(unchecked)}")
    return 1 if failed else 0


def main(argv: list[str] | None = None, *, engine_factory=None) -> int:
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
    image_cmd.add_argument("--scan-tam", action="store_true",
                           help="tranh cắt tạm từ ảnh scan sách (chủ dự án cho dùng tạm); bản phát hành sẽ bị chặn")
    image_cmd.set_defaults(func=_cmd_import_image)
    clips_cmd = commands.add_parser("import-clips", help="nhập clip tranh động <mã tranh>.mp4 trong một thư mục")
    clips_cmd.add_argument("folder", help="thư mục chứa các file <mã tranh>.mp4")
    clips_cmd.set_defaults(func=_cmd_import_clips)
    icons_cmd = commands.add_parser("ui-icons", help="sinh biểu tượng giao diện, hoa và gà con mặc định còn thiếu")
    icons_cmd.add_argument("--force", action="store_true", help="vẽ lại mọi biểu tượng (không đụng hoa và gà con)")
    icons_cmd.set_defaults(func=_cmd_ui_icons)
    sfx_cmd = commands.add_parser("sfx-default", help="sinh tiếng động mặc định cho mã còn thiếu file")
    sfx_cmd.set_defaults(func=_cmd_sfx_default)
    validate_cmd = commands.add_parser("validate", help="kiểm tra file bài đã dựng, danh mục và project Unity")
    validate_cmd.add_argument("--allow-missing", action="store_true",
                              help="bỏ qua việc kiểm tra file âm thanh/tranh còn thiếu")
    validate_cmd.add_argument("--release", action="store_true",
                              help="thêm điều kiện phát hành: bài trong app đã duyệt, âm thanh/tranh đã duyệt")
    validate_cmd.set_defaults(func=_cmd_validate)
    review_cmd = commands.add_parser("review", help="mở trang web nội bộ để nghe duyệt âm thanh, xem duyệt tranh và tranh động")
    review_cmd.add_argument("--port", type=int, default=REVIEW_PORT,
                            help=f"cổng lắng nghe trên 127.0.0.1 (mặc định {REVIEW_PORT})")
    review_cmd.set_defaults(func=_cmd_review)
    open_cmd = commands.add_parser("mo", help="mở công cụ duyệt trong trình duyệt; đang chạy rồi thì chỉ mở trang")
    open_cmd.add_argument("--port", type=int, default=REVIEW_PORT, help=f"cổng của công cụ duyệt (mặc định {REVIEW_PORT})")
    open_cmd.set_defaults(func=_cmd_open)
    tts_cmd = commands.add_parser("tts", help="tạo âm thanh bằng edge-tts theo cấu hình giọng đọc")
    tts_cmd.add_argument("--bai", help="chỉ tạo mã dùng trong bài này")
    tts_cmd.add_argument("--loai", choices=("am", "van", "dau", "tieng", "tu", "cau", "huong_dan", "khen"),
                         help="chỉ tạo loại âm thanh này")
    tts_cmd.add_argument("--ma", nargs="+", help="chỉ tạo các mã này")
    tts_cmd.add_argument("--gom-da-duyet", action="store_true", help="tạo lại cả mã đã duyệt")
    tts_cmd.add_argument("--thu", action="store_true", help="chỉ liệt kê mã sẽ tạo, không ghi file")
    tts_cmd.add_argument("--tieng-keep-first", action="store_true",
                         help="tiếng lẻ chưa có chỉnh riêng thì đọc trong câu đệm \"X, X.\" rồi giữ tiếng đầu")
    tts_cmd.set_defaults(func=_cmd_tts, engine_factory=engine_factory)
    pitch_cmd = commands.add_parser("pitch", help="đo cao độ thanh hỏi/ngã trong âm thanh đã tạo")
    pitch_cmd.add_argument("--bai", help="chỉ đo mã dùng trong bài này")
    pitch_cmd.add_argument("--ma", nargs="+", help="chỉ đo các mã này")
    pitch_cmd.set_defaults(func=_cmd_pitch)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
