"""Khoá media: mã kiểm tra của từng tranh và âm thanh đã đóng vào gói .unitypackage (không nằm trong git)."""

import hashlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import tapdoc.__main__ as cli

from tapdoc.media_lock import compare, describe, missing_meta, snapshot, write_lock


class MediaLockTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.res = Path(tmp.name) / "Resources"
        self.lock = Path(tmp.name) / "media_lock.json"
        for rel, data in (("images/img_a.png", b"png-a"), ("audio/am_b.mp3", b"mp3-b"), ("lessons/b01.json", b"{}")):
            path = self.res / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            (path.parent / (path.name + ".meta")).write_text("guid: x", encoding="utf-8")

    def test_snapshot_covers_only_media_files(self):
        self.assertEqual(snapshot(self.res), {
            "audio/am_b.mp3": hashlib.sha256(b"mp3-b").hexdigest(),
            "images/img_a.png": hashlib.sha256(b"png-a").hexdigest(),
        })

    def test_missing_meta_is_listed(self):
        self.assertEqual(missing_meta(self.res), [])
        (self.res / "audio/am_c.mp3").write_bytes(b"mp3-c")
        self.assertEqual(missing_meta(self.res), ["audio/am_c.mp3"])

    def test_no_lock_means_nothing_to_compare(self):
        self.assertIsNone(compare(self.res, self.lock))

    def test_fresh_lock_matches(self):
        write_lock(self.res, self.lock, "TapDoc-media-2026-11-02.unitypackage")
        diff = compare(self.res, self.lock)
        self.assertTrue(diff.ok)
        self.assertEqual(diff.package, "TapDoc-media-2026-11-02.unitypackage")
        self.assertIsNone(describe(diff))

    def test_changed_missing_and_new_files_are_reported(self):
        write_lock(self.res, self.lock, "TapDoc-media-2026-11-02.unitypackage")
        (self.res / "audio/am_b.mp3").write_bytes(b"mp3-b-moi")
        (self.res / "images/img_a.png").unlink()
        (self.res / "images/img_moi.png").write_bytes(b"png")
        diff = compare(self.res, self.lock)
        self.assertEqual((diff.changed, diff.missing, diff.extra),
                         (["audio/am_b.mp3"], ["images/img_a.png"], ["images/img_moi.png"]))
        message = describe(diff)
        self.assertIn("TapDoc-media-2026-11-02.unitypackage", message)
        self.assertIn("thiếu 1", message)
        self.assertIn("khác 1", message)
        self.assertIn("mới 1", message)

    def test_validate_warns_when_media_differs_from_package(self):
        write_lock(self.res, self.lock, "TapDoc-media-2026-11-02.unitypackage")
        (self.res / "audio/am_b.mp3").write_bytes(b"mp3-b-moi")
        out = io.StringIO()
        with patch.object(cli, "validate_all", return_value=[]), patch.object(cli, "UNITY_RES", self.res), \
                patch.object(cli, "MEDIA_LOCK", self.lock), patch("sys.stdout", out):
            self.assertEqual(cli.main(["validate"]), 0)  # chỉ cảnh báo, không tính là lỗi
        self.assertIn("Cảnh báo: media trên máy khác gói TapDoc-media-2026-11-02.unitypackage", out.getvalue())
        self.assertTrue(out.getvalue().rstrip().endswith("OK"))


if __name__ == "__main__":
    unittest.main()
