import http.client
import io
import json
import re
import tempfile
import threading
import unicodedata
import unittest
import urllib.error
import urllib.request
from contextlib import redirect_stderr, redirect_stdout
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest import mock

from tapdoc import __main__ as cli
from tapdoc.manifest import load_rows, save_rows
from tapdoc.review_server import make_server


class ReviewServerTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.manifests_dir = self.root / "manifests"
        self.res_dir = self.root / "res"
        (self.res_dir / "audio").mkdir(parents=True)
        (self.res_dir / "images").mkdir(parents=True)

        self.audio_manifest = self.manifests_dir / "audio_manifest.json"
        self.image_manifest = self.manifests_dir / "image_manifest.json"
        save_rows(
            self.audio_manifest,
            [
                {
                    "id": "am_dd",
                    "text": "đờ",
                    "kind": "am",
                    "file": "audio/am_dd.mp3",
                    "source": "chatgpt_tam",
                    "status": "cho_duyet",
                    "can_nghe_ky": False,
                    "ghi_chu": "",
                    "bai": ["tv1_t1_b13"],
                }
            ],
        )
        save_rows(
            self.image_manifest,
            [
                {
                    "id": "img_b13_cais_ddu",
                    "mo_ta": "Bé gái ngồi trên ván đu",
                    "bai": ["tv1_t1_b13"],
                    "file": "images/img_b13_cais_ddu.png",
                    "source": "chatgpt_tam",
                    "status": "cho_duyet",
                    "ghi_chu": "",
                }
            ],
        )
        (self.res_dir / "audio" / "am_dd.mp3").write_bytes(b"ID3-fake-mp3")
        (self.res_dir / "images" / "img_b13_cais_ddu.png").write_bytes(b"\x89PNG\r\n\x1a\nfake")
        (self.res_dir / "secret.mp3").write_bytes(b"secret")

        self.server = make_server(0, self.manifests_dir, self.res_dir)
        self.addCleanup(self._stop_server)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        host, port = self.server.server_address
        self.base_url = f"http://{host}:{port}"

    def _stop_server(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def _get(self, path: str):
        req = urllib.request.Request(f"{self.base_url}{path}", method="GET")
        return urllib.request.urlopen(req, timeout=5)

    def _post(self, path: str, payload):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}{path}",
            data=data,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        return urllib.request.urlopen(req, timeout=5)

    def test_brief_core_scenarios(self):
        audio_manifest = self.audio_manifest

        def get_json(path: str):
            with self._get(path) as resp:
                return json.loads(resp.read().decode("utf-8"))

        def post_json(path: str, payload: dict):
            with self._post(path, payload) as resp:
                return json.loads(resp.read().decode("utf-8"))

        def post_status(path: str, payload: dict) -> int:
            try:
                with self._post(path, payload) as resp:
                    return resp.status
            except urllib.error.HTTPError as e:
                e.close()
                return e.code

        def get_status(path: str) -> int:
            try:
                with self._get(path) as resp:
                    return resp.status
            except urllib.error.HTTPError as e:
                e.close()
                return e.code

        self.assertEqual(len(get_json("/api/data")["audio"]), 1)
        row = post_json("/api/review", {"manifest": "audio", "id": "am_dd", "status": "dat", "ghi_chu": "rõ"})
        self.assertEqual(row["status"], "dat"); self.assertEqual(load_rows(audio_manifest)[0]["ghi_chu"], "rõ")
        self.assertEqual(post_status("/api/review", {"manifest": "audio", "id": "am_dd", "status": "tot"}), 400)
        self.assertEqual(get_status("/media/audio/am_dd.mp3"), 200)
        self.assertEqual(get_status("/media/audio/..%2Fsecret.mp3"), 404); self.assertEqual(get_status("/media/audio/am_dd.exe"), 404)

    def test_server_bound_to_localhost_and_is_threading_http_server(self):
        self.assertIsInstance(self.server, ThreadingHTTPServer)
        self.assertEqual(self.server.server_address[0], "127.0.0.1")

    def test_index_html_served_offline_with_tabs_filters_and_controls(self):
        with self._get("/") as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("text/html", resp.headers.get("Content-Type", ""))
            html = resp.read().decode("utf-8")
        self.assertIn("Âm thanh", html)
        self.assertIn("Tranh", html)
        self.assertIn("chỉ file cần nghe kỹ", html)
        self.assertIn("Đạt", html)
        self.assertIn("Không đạt", html)
        self.assertIn("160px", html)
        self.assertIn("/api/data", html)
        self.assertIn("/api/review", html)
        self.assertIn("/media/audio/", html)
        self.assertIn("/media/images/", html)
        self.assertIsNone(re.search(r"https?://", html, re.IGNORECASE))

    def test_media_images_and_invalid_media_paths(self):
        with self._get("/media/images/img_b13_cais_ddu.png") as resp:
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.headers.get("Content-Type"), "image/png")
            self.assertEqual(resp.read(), b"\x89PNG\r\n\x1a\nfake")

        for bad_path in (
            "/media/images/am_dd.mp3",
            "/media/audio/img_b13_cais_ddu.png",
            "/media/audio/khong_co.mp3",
            "/media/images/khong_co.png",
            "/media/audio/AM_DD.mp3",
            "/media/audio/am-dd.mp3",
            "/media/audio/..%5Csecret.mp3",
            "/media/images/..%2Fsecret.png",
            "/unknown",
        ):
            with self.subTest(bad_path=bad_path):
                with self.assertRaises(urllib.error.HTTPError) as cm:
                    self._get(bad_path)
                cm.exception.close()
                self.assertEqual(cm.exception.code, 404)

    def test_review_updates_image_manifest_and_normalizes_nfc(self):
        nfd_note = unicodedata.normalize("NFD", "màu hơi tối")
        with self._post(
            "/api/review",
            {"manifest": "images", "id": "img_b13_cais_ddu", "status": "khong_dat", "ghi_chu": nfd_note},
        ) as resp:
            self.assertEqual(resp.status, 200)
            row = json.loads(resp.read().decode("utf-8"))
        self.assertEqual(row["status"], "khong_dat")
        self.assertEqual(row["ghi_chu"], "màu hơi tối")
        self.assertTrue(unicodedata.is_normalized("NFC", row["ghi_chu"]))
        saved = load_rows(self.image_manifest)[0]
        self.assertEqual(saved["status"], "khong_dat")
        self.assertEqual(saved["ghi_chu"], "màu hơi tối")

    def test_review_rejects_bad_requests_with_400(self):
        bad_payloads = [
            {"manifest": "other", "id": "am_dd", "status": "dat", "ghi_chu": ""},
            {"manifest": "audio", "id": "khong_co", "status": "dat", "ghi_chu": ""},
            {"manifest": "audio", "id": 123, "status": "dat", "ghi_chu": ""},
            {"manifest": "audio", "id": "am_dd", "status": "chua_co", "ghi_chu": ""},
            {"manifest": "audio", "id": "am_dd", "status": "dat", "ghi_chu": 123},
            ["not", "a", "dict"],
        ]
        for payload in bad_payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(urllib.error.HTTPError) as cm:
                    self._post("/api/review", payload)
                cm.exception.close()
                self.assertEqual(cm.exception.code, 400)

        # Invalid JSON body
        host, port = self.server.server_address
        conn = http.client.HTTPConnection(host, port, timeout=5)
        self.addCleanup(conn.close)
        conn.request("POST", "/api/review", body=b"{not-json", headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        resp.read()
        self.assertEqual(resp.status, 400)

    def test_concurrent_reviews_do_not_clobber_rows(self):
        rows = [
            {
                "id": f"am_{i}",
                "text": "a",
                "kind": "am",
                "file": f"audio/am_{i}.mp3",
                "source": "chatgpt_tam",
                "status": "cho_duyet",
                "can_nghe_ky": False,
                "ghi_chu": "",
                "bai": ["tv1_t1_b13"],
            }
            for i in range(10)
        ]
        save_rows(self.audio_manifest, rows)
        errors = []

        def worker(i: int):
            try:
                with self._post(
                    "/api/review",
                    {"manifest": "audio", "id": f"am_{i}", "status": "dat", "ghi_chu": f"ok {i}"},
                ) as resp:
                    if resp.status != 200:
                        errors.append(resp.status)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=5)

        self.assertEqual(errors, [])
        saved = {r["id"]: r for r in load_rows(self.audio_manifest)}
        for i in range(10):
            self.assertEqual(saved[f"am_{i}"]["status"], "dat")
            self.assertEqual(saved[f"am_{i}"]["ghi_chu"], f"ok {i}")

    def test_cli_review_prints_url_and_stops_on_keyboard_interrupt(self):
        fake_server = mock.MagicMock()
        fake_server.server_address = ("127.0.0.1", 8765)  # server thật luôn có địa chỉ đã gắn
        fake_server.serve_forever.side_effect = KeyboardInterrupt
        out, err = io.StringIO(), io.StringIO()
        with mock.patch("tapdoc.__main__.make_server", return_value=fake_server) as mocked_make, \
                redirect_stdout(out), redirect_stderr(err):
            code = cli.main(["review", "--port", "8765"])
        self.assertEqual(code, 0, err.getvalue())
        self.assertIn("Mở http://127.0.0.1:8765/", out.getvalue())
        mocked_make.assert_called_once()
        fake_server.serve_forever.assert_called_once()
        fake_server.server_close.assert_called_once()

    def test_cli_review_prints_real_bound_port_when_port_is_zero(self):
        fake_server = mock.MagicMock()
        fake_server.server_address = ("127.0.0.1", 54321)
        fake_server.serve_forever.side_effect = KeyboardInterrupt
        fake_server.server_close.return_value = None
        out, err = io.StringIO(), io.StringIO()
        with mock.patch("tapdoc.__main__.make_server", return_value=fake_server) as mocked_make, \
                redirect_stdout(out), redirect_stderr(err):
            code = cli.main(["review", "--port", "0"])
        self.assertEqual(code, 0, err.getvalue())
        self.assertIn("127.0.0.1:54321", out.getvalue())
        mocked_make.assert_called_once()
        fake_server.serve_forever.assert_called_once()
        fake_server.server_close.assert_called_once()

    def test_save_review_does_not_call_render(self):
        with self._get("/") as resp:
            html = resp.read().decode("utf-8")
        match = re.search(
            r"(?:async\s+)?function\s+saveReview\b(.*?)(?=\r?\n\s*(?:async\s+)?function\s+\w+)",
            html,
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        self.assertNotIn("render(", match.group(1))


if __name__ == "__main__":
    unittest.main()
