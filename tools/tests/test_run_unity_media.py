"""Đóng gói và nhập gói media (tranh, âm thanh kèm .meta; clip tranh động) bằng Unity chạy nền."""

import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import Mock, patch

import run_unity_media


class UnityMediaTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        self.unity = root / "Unity.exe"
        self.unity.touch()
        self.res = root / "Resources"
        (self.res / "audio").mkdir(parents=True)
        (self.res / "audio/am_b.mp3").write_bytes(b"mp3")
        (self.res / "audio/am_b.mp3.meta").write_text("guid: 1", encoding="utf-8")
        self.clips = root / "clips"
        self.clips.mkdir()
        (self.clips / "img_b01_bof.mp4").write_bytes(b"mp4")
        self.dist = root / "dist"
        self.lock = root / "media_lock.json"
        for name, value in (("UNITY_EXE", self.unity), ("OUTPUT", root / "out"), ("RES_DIR", self.res),
                            ("CLIPS_DIR", self.clips), ("DIST_DIR", self.dist), ("LOCK_PATH", self.lock),
                            ("project_is_open", Mock(return_value=False)), ("today", Mock(return_value="2026-11-02"))):
            patcher = patch.object(run_unity_media, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = patch("sys.stdout", io.StringIO())
        patcher.start()
        self.addCleanup(patcher.stop)
        self.package = self.dist / "TapDoc-media-2026-11-02.unitypackage"

    def fake_unity_export(self, cmd, **_):
        out = Path(cmd[cmd.index("-mediaOut") + 1])
        out.write_bytes(b"unitypackage")
        return Mock(returncode=0)

    def test_pack_exports_package_zips_clips_and_writes_lock(self):
        with patch("run_unity_media.subprocess.run", side_effect=self.fake_unity_export) as run:
            self.assertEqual(run_unity_media.pack(), 0)
        cmd = run.call_args.args[0]
        self.assertIn("-batchmode", cmd)
        self.assertEqual(cmd[cmd.index("-executeMethod") + 1], "TapDoc.EditorTools.MediaPackage.Export")
        self.assertEqual(Path(cmd[cmd.index("-mediaOut") + 1]), self.package)
        self.assertTrue(self.package.is_file())
        with zipfile.ZipFile(self.dist / "TapDoc-clips-2026-11-02.zip") as z:
            self.assertEqual(z.namelist(), ["img_b01_bof.mp4"])
        lock = json.loads(self.lock.read_text(encoding="utf-8"))
        self.assertEqual(lock["package"], self.package.name)
        self.assertEqual(sorted(lock["files"]), ["audio/am_b.mp3"])

    def test_pack_refuses_media_without_meta(self):
        (self.res / "audio/am_c.mp3").write_bytes(b"mp3")
        with patch("run_unity_media.subprocess.run") as run:
            self.assertEqual(run_unity_media.pack(), 1)
        run.assert_not_called()
        self.assertFalse(self.lock.exists())

    def test_pack_failure_keeps_old_lock(self):
        self.lock.write_text('{"package": "cu", "files": {}}', encoding="utf-8")
        with patch("run_unity_media.subprocess.run", return_value=Mock(returncode=1)):
            self.assertEqual(run_unity_media.pack(), 1)
        self.assertEqual(json.loads(self.lock.read_text(encoding="utf-8"))["package"], "cu")

    def test_pack_refuses_when_project_is_open(self):
        with patch.object(run_unity_media, "project_is_open", Mock(return_value=True)), \
                patch("run_unity_media.subprocess.run") as run:
            self.assertEqual(run_unity_media.pack(), 2)
        run.assert_not_called()

    def test_unpack_imports_package_and_extracts_clips(self):
        self.dist.mkdir()
        self.package.write_bytes(b"unitypackage")
        clips_zip = self.dist / "TapDoc-clips-2026-11-02.zip"
        with zipfile.ZipFile(clips_zip, "w") as z:
            z.writestr("img_b02_coj.mp4", b"mp4")
        with patch("run_unity_media.subprocess.run", return_value=Mock(returncode=0)) as run:
            self.assertEqual(run_unity_media.unpack(self.package, clips_zip), 0)
        cmd = run.call_args.args[0]
        self.assertEqual(Path(cmd[cmd.index("-importPackage") + 1]), self.package)
        self.assertIn("-quit", cmd)
        self.assertTrue((self.clips / "img_b02_coj.mp4").is_file())

    def test_unpack_missing_package(self):
        with patch("run_unity_media.subprocess.run") as run:
            self.assertEqual(run_unity_media.unpack(self.dist / "khong_co.unitypackage", None), 1)
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
