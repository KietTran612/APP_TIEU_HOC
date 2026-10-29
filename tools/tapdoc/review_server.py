"""Máy chủ HTTP nội bộ để chủ dự án nghe duyệt âm thanh và xem duyệt tranh."""

import copy
import json
import re
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

_MEDIA_NAME_RE = re.compile(r"^[a-z0-9_]+\.(mp3|png)$")
_VALID_MANIFESTS = {"audio": "audio_manifest.json", "images": "image_manifest.json"}
_VALID_REVIEW_STATUSES = frozenset({"dat", "khong_dat", "cho_duyet"})
_MAX_BODY_BYTES = 1_000_000


class _ReviewHTTPServer(ThreadingHTTPServer):
    def __init__(self, server_address: tuple[str, int], manifests_dir: Path, res_dir: Path,
                 *, settings_path=None, prev_dir=None, lessons_dir=None, notes_path=None,
                 engine_factory=None):
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
        self.engine_factory = engine_factory or EdgeEngine
        self.job = dict(running=False, total=0, done=0, current=None, failed={})
        self.batch_thread = None

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
            self._send_json(200, {"audio": audio, "images": images})
            return

        if path.startswith("/api/tts") or path in ("/api/lessons", "/api/chain-notes") or path.startswith("/api/lesson/"):
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
        base_dir = (self.server.prev_dir if folder == "prev" else self.server.res_dir / folder).resolve()
        file_path = (base_dir / name).resolve()
        if file_path.parent != base_dir or not file_path.is_file():
            self._send_json(404, {"error": "Chưa có file"})
            return
        try:
            body = file_path.read_bytes()
        except OSError:
            self._send_json(404, {"error": "Không đọc được file"})
            return
        self._send_bytes(200, content_type, body)

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
            return dict(voice=settings["voice"], defaults=settings["defaults"],
                        voices=[dict(id=voice, label=label) for voice, label in VOICES.items()],
                        rows=[server.describe(row, settings) for row in server.audio_rows()])
        if path == "/api/chain-notes":
            return server.chain_notes()
        if path == "/api/lessons":
            index = json.loads((server.lessons_dir / "index.json").read_text(encoding="utf-8"))
            return index["lessons"]
        if path.startswith("/api/lesson/"):
            lesson_id = path[len("/api/lesson/"):]
            if not re.fullmatch(r"[a-z0-9_]+", lesson_id) or lesson_id == "index":
                raise ValueError("Mã bài không hợp lệ")
            base = server.lessons_dir.resolve()
            lesson_path = (base / (lesson_id + ".json")).resolve()
            if lesson_path.parent != base:
                raise ValueError("Đường dẫn bài không hợp lệ")
            return json.loads(lesson_path.read_text(encoding="utf-8"))
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
            if payload.keys() - {"lesson", "kind", "include_approved"}:
                raise ValueError("Bộ lọc lô không hợp lệ")
            filters = dict(lesson=payload.get("lesson"), kind=payload.get("kind"),
                           include_approved=payload.get("include_approved", False))
            if type(filters["include_approved"]) is not bool or any(
                    key in payload and (not isinstance(payload[key], str) or not payload[key])
                    for key in ("lesson", "kind")):
                raise ValueError("Bộ lọc lô không hợp lệ")
            with server.lock:
                if server.job["running"]:
                    self._send_json(409, {"error": "Đang tạo một lô khác"})
                    return
                settings = load_settings(server.settings_path)
                if filters["kind"] is not None and filters["kind"] not in settings["defaults"]:
                    raise ValueError("Loại âm thanh không hợp lệ")
                rows = [r for r in server.audio_rows() if selected(r, settings, **filters)]
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
                lessons_dir=None, notes_path=None, engine_factory=None) -> ThreadingHTTPServer:
    """Tạo máy chủ HTTP chỉ nghe trên 127.0.0.1; đường dẫn phụ có thể thay trong test."""
    return _ReviewHTTPServer(("127.0.0.1", int(port)), Path(manifests_dir), Path(res_dir),
                             settings_path=settings_path, prev_dir=prev_dir,
                             lessons_dir=lessons_dir, notes_path=notes_path,
                             engine_factory=engine_factory)
