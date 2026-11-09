"""Máy chủ HTTP nội bộ để chủ dự án nghe duyệt âm thanh và xem duyệt tranh."""

import collections
import copy
import json
import re
import sys
import threading
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from .manifest import ManifestError, load_rows, save_rows
from .tts_engine import EdgeEngine, TtsError
from .tts_generate import approve, generate_one, restore_previous, run_batch, selected
from .tts_settings import (load_settings, save_settings, effective_params, set_override,
                           needs_regen, differs_from_settings, VOICES)
from .viet import nfc

INDEX_HTML_PATH = Path(__file__).resolve().parent / "review" / "index.html"

_MEDIA_NAME_RE = re.compile(r"^[a-z0-9_]+\.(mp3|png|mp4)$")
_VALID_MANIFESTS = {"audio": "audio_manifest.json", "images": "image_manifest.json",
                    "videos": "video_manifest.json"}
_VALID_REVIEW_STATUSES = frozenset({"dat", "khong_dat", "cho_duyet"})
_MAX_BODY_BYTES = 1_000_000
# Thư mục ảnh scan của từng quyển trong bản clone sách gốc (ngoài git, chỉ để đối chiếu trên máy).
SCAN_BOOK_DIRS = {"tv1_t1_1990": "Tiếng Việt 1 (tập 1 1990)", "tv1_t2_1996": "Tiếng Việt 1 (tập 2 1996)",
                  "tv2_t1_2001": "Tiếng Việt 2 (tập 1 2001)"}


def _collect_shown(node, found) -> None:
    """Gom chữ đi kèm mỗi khoá *audio (text, prompt_text, then_text; chữ hoa ở cặp chữ)."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key.endswith("audio") and isinstance(value, str) and value:
                prefix = key[:-len("audio")]
                for shown_key in (prefix + "text", "upper" if not prefix else None):
                    shown = node.get(shown_key) if shown_key else None
                    if isinstance(shown, str) and shown.strip():
                        found.setdefault(value, collections.Counter())[nfc(shown.strip())] += 1
        for value in node.values():
            _collect_shown(value, found)
    elif isinstance(node, list):
        for value in node:
            _collect_shown(value, found)


def shown_in_app(lessons_dir) -> dict[str, list[str]]:
    """Chữ bé nhìn thấy khi mỗi mã được đọc: lấy ở phần học chính, không có mới lấy ở câu hỏi luyện tập."""
    main, practice = {}, {}
    for path in sorted(Path(lessons_dir).glob("*.json")):
        if path.name == "index.json":
            continue
        try:
            lesson = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue  # bài hỏng không được làm hỏng trang duyệt
        if isinstance(lesson, dict):
            _collect_shown(lesson.get("part1"), main)
            _collect_shown(lesson.get("part2"), practice)
    return {audio_id: [text for text, _ in (main.get(audio_id) or practice[audio_id]).most_common()]
            for audio_id in main.keys() | practice.keys()}


STEP_LABELS = {
    "unit": "Âm, vần mới", "keyword": "Từ khoá", "analyze": "Phân tích tiếng", "spell": "Đánh vần",
    "sentence": "Câu ứng dụng", "reading": "Đọc thêm", "picture": "Tranh", "words": "Từ ngữ",
    "letter_grid": "Bảng chữ", "combine_table": "Bảng ghép", "rime_table": "Bảng ôn vần",
    "tone_table": "Bảng dấu thanh", "tone_intro": "Dấu thanh mới", "tone_attach": "Ghép dấu thanh",
    "rule": "Luật chính tả", "letter_pairs": "Cặp chữ", "rime_grid": "Bảng nhóm vần",
}
PRACTICE_LABELS = {
    "listen_choose": "Nghe chọn chữ", "listen_picture": "Nghe chọn tranh", "compose": "Ghép chữ",
    "look_tone": "Nhìn chọn dấu", "match_case": "Nối chữ thường với chữ hoa",
}
OTHER_GROUP = "Danh mục ghi dùng ở bài này nhưng file bài không dùng"


def _step_label(step) -> str:
    """Tên bước cho người duyệt: loại bước, kèm chữ chính của bước nếu có."""
    if not isinstance(step, dict):
        return ""
    if "type" in step:
        name = STEP_LABELS.get(step["type"], step["type"])
    else:
        kind = step.get("kind")
        name = PRACTICE_LABELS.get(kind, kind or "Luyện tập")
    spell = step.get("spell")
    text = (step.get("text") or step.get("then_text") or (spell.get("target") if isinstance(spell, dict) else None)
            or "")
    return f"{name}: {text}" if isinstance(text, str) and text.strip() else name


def lesson_media(lesson, lesson_id, audio_rows, image_rows, video_rows) -> list[dict]:
    """Âm thanh, tranh và tranh động của một bài theo thứ tự xuất hiện trong file bài, mỗi mục một lần.

    Mỗi mục ghi bước đầu tiên dùng nó (``part`` là part1/part2, ``step`` đếm từ 1, ``label`` là tên bước).
    Clip đứng ngay sau tranh cùng mã. Mã không có trong danh mục bị bỏ qua; mã danh mục ghi dùng ở bài này mà
    không thấy trong file bài thì xếp cuối (âm thanh trước, tranh sau) trong nhóm ``khac``.
    """
    audio_ids = {row["id"] for row in audio_rows}
    image_ids = {row["id"] for row in image_rows}
    video_ids = {row["id"] for row in video_rows}
    items, seen = [], set()
    group = {"part": "khac", "step": 0, "label": OTHER_GROUP}

    def add(manifest, item_id):
        if (manifest, item_id) not in seen:
            seen.add((manifest, item_id))
            items.append({"manifest": manifest, "id": item_id, **group})

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, str):
                    if key.endswith("audio") and value in audio_ids:
                        add("audio", value)
                    elif key == "image" and value in image_ids:
                        add("images", value)
                        if value in video_ids:
                            add("videos", value)
                else:
                    walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    if isinstance(lesson, dict):
        for part in ("part1", "part2"):
            for number, step in enumerate(lesson.get(part) or [], start=1):
                group = {"part": part, "step": number, "label": _step_label(step)}
                walk(step)
        group = {"part": "khac", "step": 0, "label": OTHER_GROUP}
        walk({k: v for k, v in lesson.items() if k not in ("part1", "part2")})
    for manifest, rows in (("audio", audio_rows), ("images", image_rows)):
        for row in rows:
            if lesson_id in (row.get("bai") or []):
                add(manifest, row["id"])
                if manifest == "images" and row["id"] in video_ids:
                    add("videos", row["id"])
    return items


def in_book(row, book) -> bool:
    """Mã thuộc quyển khi dùng trong một bài của quyển; mã không gắn bài nào của sách (dùng chung) thuộc mọi quyển.

    ``book`` là cặp (bài của quyển, mọi bài có trong index.json).
    """
    mine, known = book
    bai = [b for b in row.get("bai") or [] if b in known]
    return not bai or any(b in mine for b in bai)


class _ReviewHTTPServer(ThreadingHTTPServer):
    # Trên Windows SO_REUSEADDR cho máy chủ thứ hai cùng nghe cổng đang dùng mà không báo lỗi.
    allow_reuse_address = sys.platform != "win32"

    def __init__(self, server_address: tuple[str, int], manifests_dir: Path, res_dir: Path,
                 *, settings_path=None, prev_dir=None, lessons_dir=None, notes_path=None,
                 clips_dir=None, scans_dir=None, engine_factory=None):
        super().__init__(server_address, _ReviewRequestHandler)
        self.manifests_dir = Path(manifests_dir)
        self.res_dir = Path(res_dir)
        self.lock = threading.Lock()
        # Mặc định nằm cạnh danh mục, không phụ thuộc thư mục làm việc.
        content_dir = self.manifests_dir.parent
        self.settings_path = Path(settings_path) if settings_path is not None else content_dir / "tts/settings.json"
        self.prev_dir = Path(prev_dir) if prev_dir is not None else content_dir / "tts/prev"
        self.lessons_dir = Path(lessons_dir) if lessons_dir is not None else self.res_dir / "lessons"
        self.notes_path = Path(notes_path) if notes_path is not None else content_dir / "review/chain_notes.json"
        # Clip tranh động nằm ngoài git (content/clips), không nằm trong thư mục tài nguyên Unity.
        self.clips_dir = Path(clips_dir) if clips_dir is not None else content_dir / "clips"
        # Ảnh scan sách gốc không bao giờ vào repo hay app; trang duyệt chỉ đọc từ bản clone trên máy.
        self.scans_dir = Path(scans_dir) if scans_dir is not None else content_dir.parent / "sach-giao-khoa-viet-nam"
        self.engine_factory = engine_factory or EdgeEngine
        self.job = dict(running=False, total=0, done=0, current=None, failed={})
        self.batch_thread = None
        self._shown = (None, {})

    def shown(self):
        """Chữ hiển thị trong app theo mã; chỉ quét lại bài khi có file bài đổi (thời điểm sửa, kích thước)."""
        key = tuple((p.name, st.st_mtime_ns, st.st_size)
                    for p in sorted(self.lessons_dir.glob("*.json")) for st in (p.stat(),))
        if key != self._shown[0]:
            self._shown = (key, shown_in_app(self.lessons_dir))
        return self._shown[1]

    def scan_path(self, lesson_id):
        """Ảnh trang đôi trong sách gốc chứa bài; ``None`` khi bài không ghi trang hoặc máy chưa có ảnh."""
        if not re.fullmatch(r"[a-z0-9_]+", lesson_id) or lesson_id == "index":
            return None
        lesson_path = self.lessons_dir / (lesson_id + ".json")
        try:
            lesson = json.loads(lesson_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        scan = (lesson.get("source") or {}).get("scan_file") if isinstance(lesson, dict) else None
        folder = SCAN_BOOK_DIRS.get(lesson.get("book")) if isinstance(lesson, dict) else None
        if not isinstance(scan, str) or not re.fullmatch(r"\d{3}", scan) or folder is None:
            return None
        matches = sorted((self.scans_dir / folder).glob(scan + "_*.jpg"))
        return matches[0] if matches else None

    def book_lessons(self, book):
        """(mã các bài thuộc quyển ``book``, mã mọi bài) theo index.json; quyển không có thì báo lỗi."""
        index = json.loads((self.lessons_dir / "index.json").read_text(encoding="utf-8"))
        lessons = {lesson["lesson_id"] for lesson in index["lessons"] if lesson.get("book") == book}
        if not lessons:
            raise ValueError("Không có sách " + book)
        return lessons, {lesson["lesson_id"] for lesson in index["lessons"]}

    def audio_rows(self):
        return load_rows(self.manifests_dir / "audio_manifest.json")

    def describe(self, row, settings):
        return {**row, "params": asdict(effective_params(settings, row)),
                "needs_regen": needs_regen(settings, row),
                "differs": differs_from_settings(settings, row),
                "has_prev": (self.prev_dir / (row["id"] + ".mp3")).is_file()
                            and (self.prev_dir / (row["id"] + ".json")).is_file(),
                "overridden": bool(settings["overrides"].get(row["id"]))}

    def chain_notes(self):
        if not self.notes_path.exists():
            return []
        notes = json.loads(self.notes_path.read_text(encoding="utf-8"))
        if not isinstance(notes, list):
            raise ValueError("Ghi chú chuỗi phải là danh sách")
        return notes

    def batch(self, rows, settings, filters):
        # Chỉ nhập lại mã vừa xử lý, giữ đánh giá mã khác đã lưu khi chờ bộ đọc.
        server = self
        held = False
        cursor = 0
        originals = list(rows)

        class BatchEngine:
            def synthesize(self, params):
                nonlocal held
                with server.lock:
                    server.job["current"] = rows[cursor]["id"]
                result = engine.synthesize(params)
                server.lock.acquire()
                held = True
                live = next((r for r in server.audio_rows() if r["id"] == rows[cursor]["id"]), None)
                if live is None:
                    raise ValueError("Mã không còn trong danh mục")
                if live.get("status") == "dat" and not filters["include_approved"]:
                    raise TtsError("Mã vừa được duyệt; giữ nguyên bản đã duyệt")
                rows[cursor].update(live)
                return result

        def save(updated):
            nonlocal held
            if not held:
                server.lock.acquire()
                held = True
            try:
                live = server.audio_rows()
                # Khi tạo lỗi, run_batch giữ nguyên đối tượng dòng.
                if updated[cursor] is not originals[cursor]:
                    changed = updated[cursor]
                    live = [changed if r["id"] == changed["id"] else r for r in live]
                save_rows(server.manifests_dir / "audio_manifest.json", live)
            finally:
                held = False
                server.lock.release()

        def progress(item_id, report):
            nonlocal cursor
            with server.lock:
                server.job.update(done=len(report.done), failed=dict(report.failed), current=item_id)
            cursor += 1

        engine = None
        try:
            engine = self.engine_factory()
            run_batch(rows, settings, BatchEngine(), self.res_dir / "audio", self.prev_dir,
                      include_approved=filters["include_approved"], save=save, on_progress=progress)
        except Exception as error:
            # Kể cả thiếu edge-tts, trạng thái lô luôn kết thúc và còn thông báo.
            if held:
                held = False
                self.lock.release()
            # Chưa có bộ đọc thì lỗi thuộc cả lô, không gán cho mã đầu tiên.
            key = rows[cursor]["id"] if engine is not None and cursor < len(rows) else "batch"
            with self.lock:
                self.job["failed"][key] = str(error)
        finally:
            if held:
                self.lock.release()
            with self.lock:
                self.job.update(running=False, current=None)


class _ReviewRequestHandler(BaseHTTPRequestHandler):
    server: _ReviewHTTPServer

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        return

    def _send_bytes(self, status: int, content_type: str, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, data) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self._send_bytes(status, "application/json; charset=utf-8", body)

    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path in ("/", "/index.html"):
            try:
                body = INDEX_HTML_PATH.read_text(encoding="utf-8").encode("utf-8")
            except OSError:
                self._send_json(404, {"error": "Không tìm thấy trang duyệt"})
                return
            self._send_bytes(200, "text/html; charset=utf-8", body)
            return

        if path == "/api/data":
            with self.server.lock:
                audio = load_rows(self.server.manifests_dir / "audio_manifest.json")
                images = load_rows(self.server.manifests_dir / "image_manifest.json")
                videos = load_rows(self.server.manifests_dir / "video_manifest.json")
            self._send_json(200, {"audio": audio, "images": images, "videos": videos})
            return

        if path.startswith("/api/tts") or path in ("/api/lessons", "/api/chain-notes") or path.startswith(
                ("/api/lesson/", "/api/lesson-media/")):
            try:
                with self.server.lock:
                    result = self._get_tool(path)
                self._send_json(200, result)
            except (OSError, ValueError, ManifestError) as error:
                self._send_json(400, {"error": str(error)})
            except LookupError:
                self._send_json(404, {"error": "Không tìm thấy đường dẫn"})
            return

        if path.startswith("/media/prev/"):
            self._serve_media(path[len("/media/prev/"):], "prev", ".mp3", "audio/mpeg")
            return

        if path.startswith("/media/audio/"):
            self._serve_media(path[len("/media/audio/"):], "audio", ".mp3", "audio/mpeg")
            return

        if path.startswith("/media/images/"):
            self._serve_media(path[len("/media/images/"):], "images", ".png", "image/png")
            return

        if path.startswith("/media/scan/"):
            name = path[len("/media/scan/"):]
            scan = self.server.scan_path(name[:-len(".jpg")]) if name.endswith(".jpg") else None
            if scan is None:
                self._send_json(404, {"error": "Máy này chưa có ảnh trang sách của bài"})
            else:
                self._send_bytes(200, "image/jpeg", scan.read_bytes())
            return

        if path.startswith("/media/clips/"):
            self._serve_media(path[len("/media/clips/"):], "clips", ".mp4", "video/mp4")
            return

        self._send_json(404, {"error": "Không tìm thấy đường dẫn"})

    def _serve_media(self, raw_name: str, folder: str, expected_ext: str, content_type: str) -> None:
        name = unquote(raw_name)
        if (
            not _MEDIA_NAME_RE.fullmatch(raw_name)
            or not _MEDIA_NAME_RE.fullmatch(name)
            or not name.endswith(expected_ext)
        ):
            self._send_json(404, {"error": "Tên file không hợp lệ"})
            return
        if folder == "prev":
            base_dir = self.server.prev_dir.resolve()
        elif folder == "clips":
            base_dir = self.server.clips_dir.resolve()
        else:
            base_dir = (self.server.res_dir / folder).resolve()
        file_path = (base_dir / name).resolve()
        if file_path.parent != base_dir or not file_path.is_file():
            self._send_json(404, {"error": "Chưa có file"})
            return
        try:
            body = file_path.read_bytes()
        except OSError:
            self._send_json(404, {"error": "Không đọc được file"})
            return
        if folder == "clips":
            self._send_ranged(content_type, body)
            return
        self._send_bytes(200, content_type, body)

    def _send_ranged(self, content_type: str, body: bytes) -> None:
        """Gửi video, hỗ trợ một khoảng byte để trình duyệt tua và phát lặp."""
        match = re.fullmatch(r"bytes=(\d*)-(\d*)", self.headers.get("Range", "").strip())
        if not match or match.groups() == ("", ""):
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        first, last = match.groups()
        size = len(body)
        if first == "":  # "bytes=-N": N byte cuối
            start, end = max(0, size - int(last)), size - 1
        else:
            start, end = int(first), min(int(last), size - 1) if last else size - 1
        if start >= size or start > end:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        chunk = body[start:end + 1]
        self.send_response(206)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(chunk)))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(chunk)

    def do_POST(self) -> None:
        path = urlsplit(self.path).path
        if path not in {"/api/review", "/api/tts/defaults", "/api/tts/row",
                        "/api/tts/generate", "/api/tts/restore", "/api/tts/batch",
                        "/api/chain-notes"}:
            self._send_json(404, {"error": "Không tìm thấy đường dẫn"})
            return

        length_header = self.headers.get("Content-Length")
        if length_header is None:
            self._send_json(400, {"error": "Thiếu Content-Length"})
            return
        try:
            length = int(length_header)
        except ValueError:
            self._send_json(400, {"error": "Content-Length không hợp lệ"})
            return
        if length <= 0 or length > _MAX_BODY_BYTES:
            self._send_json(400, {"error": "Kích thước dữ liệu không hợp lệ"})
            return

        try:
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode("utf-8"))
        except (OSError, UnicodeDecodeError, ValueError):
            self._send_json(400, {"error": "JSON không hợp lệ"})
            return

        if not isinstance(payload, dict):
            self._send_json(400, {"error": "Dữ liệu gửi lên phải là đối tượng JSON"})
            return

        if path != "/api/review":
            try:
                self._post_tool(path, payload)
            except TtsError as error:
                self._send_json(502, {"error": str(error)})
            except (OSError, ValueError, ManifestError) as error:
                self._send_json(400, {"error": str(error)})
            except Exception as error:
                # Lỗi chưa lường trước vẫn trả lời JSON để trang báo được, không cắt kết nối.
                self._send_json(500, {"error": f"Lỗi không lường trước: {error}"})
            return

        manifest_kind = payload.get("manifest")
        item_id = payload.get("id")
        status = payload.get("status")
        if (
            not isinstance(manifest_kind, str)
            or manifest_kind not in _VALID_MANIFESTS
            or not isinstance(item_id, str)
            or not item_id
            or not isinstance(status, str)
            or status not in _VALID_REVIEW_STATUSES
        ):
            self._send_json(400, {"error": "Trường manifest, id hoặc status không hợp lệ"})
            return

        has_note = "ghi_chu" in payload
        note_val = payload.get("ghi_chu", "")
        if not isinstance(note_val, str):
            self._send_json(400, {"error": "Trường ghi_chu phải là chuỗi"})
            return

        manifest_path = self.server.manifests_dir / _VALID_MANIFESTS[manifest_kind]
        with self.server.lock:
            try:
                rows = load_rows(manifest_path)
            except ManifestError as e:
                self._send_json(400, {"error": str(e)})
                return
            target = next((row for row in rows if row.get("id") == item_id), None)
            if target is None:
                self._send_json(400, {"error": f"Không có mã {item_id} trong danh mục {manifest_kind}"})
                return
            if manifest_kind == "audio" and status == "dat":
                try:
                    target.update(approve(target, self.server.prev_dir))
                except (OSError, ValueError) as error:
                    self._send_json(400, {"error": str(error)})
                    return
            else:
                target["status"] = status
            if has_note:
                target["ghi_chu"] = nfc(note_val)
            else:
                target["ghi_chu"] = nfc(str(target.get("ghi_chu", "")))
            save_rows(manifest_path, rows)
            updated = dict(target)

        self._send_json(200, updated)

    def _get_tool(self, path):
        server = self.server
        if path == "/api/tts/job":
            return copy.deepcopy(server.job)
        if path == "/api/tts":
            settings = load_settings(server.settings_path)
            shown = server.shown()
            return dict(voice=settings["voice"], defaults=settings["defaults"],
                        voices=[dict(id=voice, label=label) for voice, label in VOICES.items()],
                        rows=[{**server.describe(row, settings), "hien_thi": shown.get(row["id"], [])}
                              for row in server.audio_rows()])
        if path == "/api/chain-notes":
            return server.chain_notes()
        if path == "/api/lessons":
            index = json.loads((server.lessons_dir / "index.json").read_text(encoding="utf-8"))
            return index["lessons"]
        for prefix in ("/api/lesson/", "/api/lesson-media/"):
            if not path.startswith(prefix):
                continue
            lesson_id = path[len(prefix):]
            if not re.fullmatch(r"[a-z0-9_]+", lesson_id) or lesson_id == "index":
                raise ValueError("Mã bài không hợp lệ")
            base = server.lessons_dir.resolve()
            lesson_path = (base / (lesson_id + ".json")).resolve()
            if lesson_path.parent != base:
                raise ValueError("Đường dẫn bài không hợp lệ")
            lesson = json.loads(lesson_path.read_text(encoding="utf-8"))
            if prefix == "/api/lesson/":
                return lesson
            manifests = server.manifests_dir
            videos = manifests / "video_manifest.json"
            return lesson_media(lesson, lesson_id, server.audio_rows(), load_rows(manifests / "image_manifest.json"),
                                load_rows(videos) if videos.exists() else [])
        raise LookupError(path)

    def _post_tool(self, path, payload):
        server = self.server
        if path == "/api/chain-notes":
            if set(payload) != {"lesson", "where", "chain", "note"} or any(
                    not isinstance(payload[k], str) for k in ("lesson", "where", "chain", "note")):
                raise ValueError("Cần lesson, where, chain, note dạng chữ")
            entry = {key: nfc(value).strip() for key, value in payload.items()}
            if any(not entry[k] for k in ("lesson", "where", "chain")):
                raise ValueError("Bài, vị trí và chuỗi không được rỗng")
            with server.lock:
                notes = [note for note in server.chain_notes() if any(
                    note.get(k) != entry[k] for k in ("lesson", "where", "chain"))]
                if entry["note"]:
                    notes.append(entry)
                save_rows(server.notes_path, notes)
            self._send_json(200, notes)
            return

        if path == "/api/tts/batch":
            if payload.keys() - {"lesson", "kind", "book", "include_approved"}:
                raise ValueError("Bộ lọc lô không hợp lệ")
            filters = dict(lesson=payload.get("lesson"), kind=payload.get("kind"),
                           include_approved=payload.get("include_approved", False))
            if type(filters["include_approved"]) is not bool or any(
                    key in payload and (not isinstance(payload[key], str) or not payload[key])
                    for key in ("lesson", "kind", "book")):
                raise ValueError("Bộ lọc lô không hợp lệ")
            book_lessons = server.book_lessons(payload["book"]) if "book" in payload else None
            with server.lock:
                if server.job["running"]:
                    self._send_json(409, {"error": "Đang tạo một lô khác"})
                    return
                settings = load_settings(server.settings_path)
                if filters["kind"] is not None and filters["kind"] not in settings["defaults"]:
                    raise ValueError("Loại âm thanh không hợp lệ")
                rows = [r for r in server.audio_rows() if selected(r, settings, **filters)
                        and (book_lessons is None or in_book(r, book_lessons))]
                server.job = dict(running=True, total=len(rows), done=0, current=None, failed={})
                server.batch_thread = threading.Thread(target=server.batch,
                    args=(rows, settings, filters), daemon=True)
                server.batch_thread.start()
                job = copy.deepcopy(server.job)
            self._send_json(200, job)
            return

        with server.lock:
            settings = load_settings(server.settings_path)
            rows = server.audio_rows()
            if path == "/api/tts/defaults":
                kind = payload.get("kind")
                if not isinstance(kind, str) or kind not in settings["defaults"] or set(payload) != {"kind", "rate", "pitch", "volume"}:
                    raise ValueError("Cần loại, tốc độ, cao độ và âm lượng hợp lệ")
                settings["defaults"][kind] = {k: payload[k] for k in ("rate", "pitch", "volume")}
                save_settings(server.settings_path, settings)
                result = {"needs_regen": sum(needs_regen(settings, r) for r in rows)}
            else:
                item_id = payload.get("id")
                if not isinstance(item_id, str) or not re.fullmatch(r"[a-z0-9_]+", item_id):
                    raise ValueError("Mã âm thanh không hợp lệ")
                row = next((r for r in rows if r["id"] == item_id), None)
                if row is None:
                    raise ValueError("Không có mã trong danh mục")
                allowed = {"id", "doc", "rate", "pitch", "volume", "voice"} if path == "/api/tts/row" else {"id"}
                if payload.keys() - allowed or any(v is None for v in payload.values()):
                    raise ValueError("Thông số không hợp lệ")
                if path == "/api/tts/row":
                    set_override(settings, row, **{k: v for k, v in payload.items() if k != "id"})
                    save_settings(server.settings_path, settings)
                    result = server.describe(row, settings)
                elif path == "/api/tts/restore":
                    updated = restore_previous(row, settings, server.res_dir / "audio", server.prev_dir)
                    rows[rows.index(row)] = updated
                    save_settings(server.settings_path, settings)
                    save_rows(server.manifests_dir / "audio_manifest.json", rows)
                    result = server.describe(updated, settings)
                else:
                    # Chụp thông số trước khi gọi bộ đọc, không giữ khoá khi chờ mạng.
                    params = effective_params(settings, row)
        if path == "/api/tts/generate":
            synthesized = server.engine_factory().synthesize(params)

            class ReadyEngine:
                def synthesize(self, unused):
                    return synthesized

            with server.lock:
                rows = server.audio_rows()
                row = next(r for r in rows if r["id"] == item_id)
                updated = generate_one(row, settings, ReadyEngine(), server.res_dir / "audio", server.prev_dir)
                rows[rows.index(row)] = updated
                save_rows(server.manifests_dir / "audio_manifest.json", rows)
                result = server.describe(updated, load_settings(server.settings_path))
        self._send_json(200, result)


def make_server(port: int, manifests_dir, res_dir, *, settings_path=None, prev_dir=None,
                lessons_dir=None, notes_path=None, clips_dir=None, scans_dir=None,
                engine_factory=None) -> ThreadingHTTPServer:
    """Tạo máy chủ HTTP chỉ nghe trên 127.0.0.1; đường dẫn phụ có thể thay trong test."""
    return _ReviewHTTPServer(("127.0.0.1", int(port)), Path(manifests_dir), Path(res_dir),
                             settings_path=settings_path, prev_dir=prev_dir,
                             lessons_dir=lessons_dir, notes_path=notes_path,
                             clips_dir=clips_dir, scans_dir=scans_dir, engine_factory=engine_factory)
