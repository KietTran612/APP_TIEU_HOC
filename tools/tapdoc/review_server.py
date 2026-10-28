"""Máy chủ HTTP nội bộ để chủ dự án nghe duyệt âm thanh và xem duyệt tranh."""

import json
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from .manifest import ManifestError, load_rows, save_rows
from .viet import nfc

INDEX_HTML_PATH = Path(__file__).resolve().parent / "review" / "index.html"

_MEDIA_NAME_RE = re.compile(r"^[a-z0-9_]+\.(mp3|png)$")
_VALID_MANIFESTS = {"audio": "audio_manifest.json", "images": "image_manifest.json"}
_VALID_REVIEW_STATUSES = frozenset({"dat", "khong_dat", "cho_duyet"})
_MAX_BODY_BYTES = 1_000_000


class _ReviewHTTPServer(ThreadingHTTPServer):
    def __init__(self, server_address: tuple[str, int], manifests_dir: Path, res_dir: Path):
        super().__init__(server_address, _ReviewRequestHandler)
        self.manifests_dir = Path(manifests_dir)
        self.res_dir = Path(res_dir)
        self.lock = threading.Lock()


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
        self._send_bytes(200, content_type, body)

    def do_POST(self) -> None:
        path = urlsplit(self.path).path
        if path != "/api/review":
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
            target["status"] = status
            if has_note:
                target["ghi_chu"] = nfc(note_val)
            else:
                target["ghi_chu"] = nfc(str(target.get("ghi_chu", "")))
            save_rows(manifest_path, rows)
            updated = dict(target)

        self._send_json(200, updated)


def make_server(port: int, manifests_dir, res_dir) -> ThreadingHTTPServer:
    """Tạo máy chủ HTTP chỉ nghe trên `127.0.0.1`."""
    return _ReviewHTTPServer(("127.0.0.1", int(port)), Path(manifests_dir), Path(res_dir))

