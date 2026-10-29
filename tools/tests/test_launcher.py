import _thread
import contextlib
import io
import socket
import sys
import tempfile
import threading
import unittest
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

from tapdoc import __main__ as cli
from tapdoc.launcher import REQUIREMENTS, ensure_edge_tts, tool_running
from tapdoc.manifest import save_rows
from tapdoc.review_server import make_server


def _serve(test, server):
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    def stop():
        server.shutdown()
        server.server_close()
        thread.join(3)
    test.addCleanup(stop)
    return server.server_address[1]


def _free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class LauncherTest(unittest.TestCase):
    def setUp(self):
        # Lệnh in tiếng Việt; gom lại để chạy được cả khi đầu ra là ống mã cp1252.
        self.out = io.StringIO()
        quiet = contextlib.redirect_stdout(self.out)
        quiet.__enter__()
        self.addCleanup(quiet.__exit__, None, None, None)
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.manifests = self.root / "manifests"
        save_rows(self.manifests / "audio_manifest.json", [])
        save_rows(self.manifests / "image_manifest.json", [])
        self.res = self.root / "res"
        (self.res / "audio").mkdir(parents=True)

    def test_tool_running_true_for_review_server(self):
        port = _serve(self, make_server(0, self.manifests, self.res))
        self.assertTrue(tool_running(port))

    def test_tool_running_false_when_nothing_listens(self):
        self.assertFalse(tool_running(_free_port(), timeout=0.5))

    def test_tool_running_false_for_other_program(self):
        class Other(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"<html>khac</html>")

            def log_message(self, *args):
                return
        port = _serve(self, ThreadingHTTPServer(("127.0.0.1", 0), Other))
        self.assertFalse(tool_running(port))

    def test_ensure_edge_tts_does_nothing_when_installed(self):
        run = mock.Mock()
        self.assertTrue(ensure_edge_tts(find_spec=lambda name: object(), run=run))
        run.assert_not_called()

    def test_ensure_edge_tts_installs_requirements_when_missing(self):
        run = mock.Mock(return_value=mock.Mock(returncode=0))
        self.assertTrue(ensure_edge_tts(find_spec=lambda name: None, run=run))
        command = run.call_args.args[0]
        self.assertEqual(command[:4], [sys.executable, "-m", "pip", "install"])
        self.assertEqual(command[-2:], ["-r", str(REQUIREMENTS)])
        self.assertTrue(REQUIREMENTS.is_file())

    def test_ensure_edge_tts_reports_failed_install(self):
        run = mock.Mock(return_value=mock.Mock(returncode=1))
        self.assertFalse(ensure_edge_tts(find_spec=lambda name: None, run=run))

    def test_open_only_opens_page_when_tool_already_running(self):
        port = _serve(self, make_server(0, self.manifests, self.res))
        with mock.patch("webbrowser.open") as opener, mock.patch.object(cli, "ensure_edge_tts") as ensure, \
                mock.patch.object(cli, "make_server") as new_server:
            self.assertEqual(cli.main(["mo", "--port", str(port)]), 0)
        opener.assert_called_once_with(f"http://127.0.0.1:{port}/")
        ensure.assert_not_called()
        new_server.assert_not_called()

    def test_open_starts_tool_then_opens_page(self):
        opened = []

        def opener(url):
            # Trang phải trả lời được ngay lúc mở trình duyệt; xong thì dừng máy chủ như khi đóng cửa sổ.
            with urllib.request.urlopen(url, timeout=3) as resp:
                opened.append((url, resp.status))
            _thread.interrupt_main()
        port = _free_port()
        with mock.patch("webbrowser.open", side_effect=opener), \
                mock.patch.object(cli, "ensure_edge_tts", return_value=True) as ensure, \
                mock.patch.object(cli, "MANIFESTS", self.manifests), mock.patch.object(cli, "UNITY_RES", self.res):
            self.assertEqual(cli.main(["mo", "--port", str(port)]), 0)
        ensure.assert_called_once()
        self.assertEqual(opened, [(f"http://127.0.0.1:{port}/", 200)])

    def test_open_moves_to_free_port_when_other_program_holds_it(self):
        opened = []

        def opener(url):
            with urllib.request.urlopen(url, timeout=3) as resp:
                opened.append((url, resp.status))
            _thread.interrupt_main()
        with socket.socket() as other:
            other.bind(("127.0.0.1", 0))
            other.listen()
            port = other.getsockname()[1]
            with mock.patch("webbrowser.open", side_effect=opener), \
                    mock.patch.object(cli, "ensure_edge_tts", return_value=True), \
                    mock.patch.object(cli, "MANIFESTS", self.manifests), mock.patch.object(cli, "UNITY_RES", self.res):
                self.assertEqual(cli.main(["mo", "--port", str(port)]), 0)
        self.assertEqual(len(opened), 1)
        self.assertNotEqual(opened[0][0], f"http://127.0.0.1:{port}/")
        self.assertEqual(opened[0][1], 200)


if __name__ == "__main__":
    unittest.main()
