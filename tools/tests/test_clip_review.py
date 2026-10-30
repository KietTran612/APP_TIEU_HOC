"""Duyệt clip tranh động: danh mục video, phục vụ file mp4, lệnh nhập clip."""

import io
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from tapdoc import __main__ as cli
from tapdoc.importer import import_clips
from tapdoc.manifest import load_rows, save_rows
from tapdoc.review_server import make_server

# Đủ để giống một file MP4: hộp đầu tiên là ftyp.
FAKE_MP4 = b"\x00\x00\x00\x18ftypmp42" + bytes(range(40))


def _image_row(image_id):
    return {"id": image_id, "mo_ta": "Con bò", "bai": ["tv1_t1_b01"], "file": f"images/{image_id}.png",
            "source": "chatgpt_tam", "status": "dat", "ghi_chu": ""}


class ClipReviewServerTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        self.manifests_dir = root / "content" / "manifests"
        self.clips_dir = root / "content" / "clips"
        self.clips_dir.mkdir(parents=True)
        res_dir = root / "res"
        (res_dir / "images").mkdir(parents=True)
        save_rows(self.manifests_dir / "image_manifest.json", [_image_row("img_b01_bof")])
        self.video_manifest = self.manifests_dir / "video_manifest.json"
        save_rows(self.video_manifest, [{
            "id": "img_b01_bof", "file": "clips/img_b01_bof.mp4", "source": "flow_veo31_lite",
            "status": "cho_duyet", "ghi_chu": "",
        }])
        (self.clips_dir / "img_b01_bof.mp4").write_bytes(FAKE_MP4)
        (root / "content" / "secret.mp4").write_bytes(FAKE_MP4)

        self.server = make_server(0, self.manifests_dir, res_dir)
        thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(lambda: (self.server.shutdown(), self.server.server_close(), thread.join(timeout=2)))
        host, port = self.server.server_address
        self.base_url = f"http://{host}:{port}"

    def _get(self, path, headers=None):
        return urllib.request.urlopen(urllib.request.Request(self.base_url + path, headers=headers or {}), timeout=5)

    def _get_code(self, path):
        try:
            with self._get(path) as resp:
                return resp.status
        except urllib.error.HTTPError as e:
            e.close()
            return e.code

    def test_data_lists_video_rows(self):
        with self._get("/api/data") as resp:
            data = json.loads(resp.read().decode("utf-8"))
        self.assertEqual([row["id"] for row in data["videos"]], ["img_b01_bof"])

    def test_data_has_empty_video_list_when_manifest_missing(self):
        self.video_manifest.unlink()
        with self._get("/api/data") as resp:
            data = json.loads(resp.read().decode("utf-8"))
        self.assertEqual(data["videos"], [])

    def test_clip_served_as_mp4_from_content_clips(self):
        with self._get("/media/clips/img_b01_bof.mp4") as resp:
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.headers.get("Content-Type"), "video/mp4")
            self.assertEqual(resp.headers.get("Accept-Ranges"), "bytes")
            self.assertEqual(resp.read(), FAKE_MP4)

    def test_clip_byte_range_for_seeking_and_looping(self):
        with self._get("/media/clips/img_b01_bof.mp4", {"Range": "bytes=4-11"}) as resp:
            self.assertEqual(resp.status, 206)
            self.assertEqual(resp.headers.get("Content-Range"), f"bytes 4-11/{len(FAKE_MP4)}")
            self.assertEqual(resp.read(), FAKE_MP4[4:12])
        with self._get("/media/clips/img_b01_bof.mp4", {"Range": "bytes=20-"}) as resp:
            self.assertEqual(resp.status, 206)
            self.assertEqual(resp.read(), FAKE_MP4[20:])

    def test_clip_range_past_end_is_rejected(self):
        with self.assertRaises(urllib.error.HTTPError) as cm:
            self._get("/media/clips/img_b01_bof.mp4", {"Range": f"bytes={len(FAKE_MP4)}-"})
        cm.exception.close()
        self.assertEqual(cm.exception.code, 416)

    def test_bad_clip_paths_are_404(self):
        for path in ("/media/clips/khong_co.mp4", "/media/clips/..%2Fsecret.mp4",
                     "/media/clips/img_b01_bof.png", "/media/images/img_b01_bof.mp4"):
            with self.subTest(path=path):
                self.assertEqual(self._get_code(path), 404)

    def test_review_writes_video_manifest(self):
        body = json.dumps({"manifest": "videos", "id": "img_b01_bof", "status": "khong_dat",
                           "ghi_chu": "méo chân"}).encode("utf-8")
        req = urllib.request.Request(self.base_url + "/api/review", data=body, method="POST",
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
        saved = load_rows(self.video_manifest)[0]
        self.assertEqual((saved["status"], saved["ghi_chu"]), ("khong_dat", "méo chân"))

    def test_page_has_clip_tab(self):
        with self._get("/") as resp:
            html = resp.read().decode("utf-8")
        self.assertIn("Tranh động", html)
        self.assertIn("/media/clips/", html)


class ImportClipsTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        self.src = root / "tai_ve"
        self.src.mkdir()
        self.clips_dir = root / "clips"
        self.video_manifest = root / "video_manifest.json"
        self.image_manifest = root / "image_manifest.json"
        save_rows(self.image_manifest, [_image_row("img_b01_bof"), _image_row("img_b02_cof")])

    def _import(self):
        return import_clips(self.src, self.clips_dir, self.video_manifest, self.image_manifest)

    def test_imports_clips_named_by_picture_id_as_pending(self):
        (self.src / "img_b02_cof.mp4").write_bytes(FAKE_MP4)
        (self.src / "img_b01_bof.mp4").write_bytes(FAKE_MP4)
        report = self._import()
        self.assertEqual(sorted(report.imported), ["img_b01_bof", "img_b02_cof"])
        self.assertEqual((self.clips_dir / "img_b01_bof.mp4").read_bytes(), FAKE_MP4)
        rows = load_rows(self.video_manifest)
        self.assertEqual([r["id"] for r in rows], ["img_b01_bof", "img_b02_cof"])
        self.assertEqual(rows[0], {"id": "img_b01_bof", "file": "clips/img_b01_bof.mp4",
                                   "source": "flow_veo31_lite", "status": "cho_duyet", "ghi_chu": ""})

    def test_skips_unknown_ids_and_files_that_are_not_mp4(self):
        (self.src / "img_b99_khong_co.mp4").write_bytes(FAKE_MP4)
        (self.src / "img_b01_bof.mp4").write_bytes(b"not a video at all")
        (self.src / "Animated_cow_da3e4237.mp4").write_bytes(FAKE_MP4)
        (self.src / "ghi_chu.txt").write_text("x")
        report = self._import()
        self.assertEqual(report.imported, [])
        self.assertEqual(sorted(name for name, _ in report.skipped),
                         ["Animated_cow_da3e4237.mp4", "img_b01_bof.mp4", "img_b99_khong_co.mp4"])
        self.assertEqual(load_rows(self.video_manifest), [])

    def test_reimport_sends_clip_back_to_review_and_keeps_note(self):
        save_rows(self.video_manifest, [{"id": "img_b01_bof", "file": "clips/img_b01_bof.mp4",
                                         "source": "flow_veo31_lite", "status": "khong_dat",
                                         "ghi_chu": "méo chân"}])
        (self.src / "img_b01_bof.mp4").write_bytes(FAKE_MP4)
        self._import()
        row = load_rows(self.video_manifest)[0]
        self.assertEqual((row["status"], row["ghi_chu"]), ("cho_duyet", "méo chân"))

    def test_cli_import_clips_reports_count(self):
        (self.src / "img_b01_bof.mp4").write_bytes(FAKE_MP4)
        out = io.StringIO()
        with mock.patch.object(cli, "CLIPS", self.clips_dir), \
             mock.patch.object(cli, "MANIFESTS", self.video_manifest.parent), \
             redirect_stdout(out), redirect_stderr(io.StringIO()):
            code = cli.main(["import-clips", str(self.src)])
        self.assertEqual(code, 0)
        self.assertIn("1 clip", out.getvalue())
        self.assertTrue((self.clips_dir / "img_b01_bof.mp4").is_file())


if __name__ == "__main__":
    unittest.main()
