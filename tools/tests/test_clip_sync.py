"""Đồng bộ clip tranh động từ content/clips vào Resources/clips (chỉ clip dat, cho_duyet)."""

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import tapdoc.__main__ as cli
from tapdoc.clip_sync import apply_sync, describe, plan_sync


def _row(clip_id: str, status: str) -> dict:
    return {"id": clip_id, "file": f"clips/{clip_id}.mp4", "source": "flow_veo31_lite", "status": status, "ghi_chu": ""}


class ClipSyncTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        self.clips = root / "content" / "clips"
        self.res = root / "Resources" / "clips"
        self.clips.mkdir(parents=True)
        self.res.mkdir(parents=True)

    def src(self, clip_id: str, data: bytes) -> None:
        (self.clips / f"{clip_id}.mp4").write_bytes(data)

    def dst(self, clip_id: str, data: bytes, meta: bool = False) -> None:
        (self.res / f"{clip_id}.mp4").write_bytes(data)
        if meta:
            (self.res / f"{clip_id}.mp4.meta").write_text("guid: x", encoding="utf-8")

    def dst_index(self, hold: list[str]) -> None:
        (self.res / "index.json").write_text(json.dumps({"giu": hold}), encoding="utf-8")

    def test_plan_copies_dat_and_cho_duyet_skips_khong_dat(self):
        for clip_id in ("a", "b", "c"):
            self.src(clip_id, b"mp4-" + clip_id.encode())
        rows = [_row("a", "dat"), _row("b", "cho_duyet"), _row("c", "khong_dat")]
        plan = plan_sync(rows, self.clips, self.res)
        self.assertEqual(plan.new, ["a", "b"])
        for ids in (plan.changed, plan.remove, plan.unchanged, plan.missing_source):
            self.assertNotIn("c", ids)

    def test_plan_changed_when_content_differs_unchanged_when_same(self):
        self.src("a", b"x1")
        self.dst("a", b"x2")
        self.src("b", b"same")
        self.dst("b", b"same")
        plan = plan_sync([_row("a", "dat"), _row("b", "dat")], self.clips, self.res)
        self.assertEqual(plan.changed, ["a"])
        self.assertEqual(plan.unchanged, ["b"])
        self.assertEqual(plan.new, [])

    def test_plan_changed_when_same_size_but_different_bytes(self):
        self.src("a", b"abcd")
        self.dst("a", b"abce")
        plan = plan_sync([_row("a", "dat")], self.clips, self.res)
        self.assertEqual(plan.changed, ["a"])

    def test_plan_removes_stale_clip(self):
        self.src("c", b"c")
        self.dst("c", b"c")
        self.dst("z", b"z")
        plan = plan_sync([_row("c", "khong_dat")], self.clips, self.res)
        self.assertEqual(plan.remove, ["c", "z"])

    def test_plan_reports_missing_source(self):
        plan = plan_sync([_row("d", "dat")], self.clips, self.res)
        self.assertEqual(plan.missing_source, ["d"])
        self.assertEqual(plan.new, [])

    def test_plan_without_resources_dir_copies_everything(self):
        self.res.rmdir()
        self.src("a", b"a")
        plan = plan_sync([_row("a", "dat")], self.clips, self.res)
        self.assertEqual(plan.new, ["a"])

    def test_apply_copies_overwrites_and_deletes_meta(self):
        self.src("a", b"new-a")
        self.src("b", b"b2")
        self.dst("b", b"b1", meta=True)
        self.src("k", b"k")
        self.dst("k", b"k", meta=True)
        self.dst("c", b"c", meta=True)
        rows = [_row("a", "dat"), _row("b", "cho_duyet"), _row("k", "dat"), _row("c", "khong_dat")]
        apply_sync(plan_sync(rows, self.clips, self.res), self.clips, self.res)
        self.assertEqual((self.res / "a.mp4").read_bytes(), b"new-a")
        self.assertEqual((self.res / "b.mp4").read_bytes(), b"b2")
        self.assertTrue((self.res / "b.mp4.meta").is_file(), "chép đè giữ .meta (thiết lập nhập)")
        self.assertTrue((self.res / "k.mp4.meta").is_file())
        self.assertFalse((self.res / "c.mp4").exists())
        self.assertFalse((self.res / "c.mp4.meta").exists())
        self.assertEqual(sorted(p.name for p in self.res.iterdir() if p.suffix == ".tmp"), [])

    def test_apply_creates_resources_dir(self):
        self.res.rmdir()
        self.src("a", b"a")
        apply_sync(plan_sync([_row("a", "dat")], self.clips, self.res), self.clips, self.res)
        self.assertEqual((self.res / "a.mp4").read_bytes(), b"a")

    def test_describe_none_when_in_sync(self):
        self.src("a", b"a")
        self.dst("a", b"a")
        self.dst_index([])
        self.assertIsNone(describe(plan_sync([_row("a", "dat")], self.clips, self.res)))

    def test_describe_mentions_command_when_out_of_sync(self):
        self.src("a", b"a")
        text = describe(plan_sync([_row("a", "dat")], self.clips, self.res))
        self.assertIsNotNone(text)
        self.assertIn("run_unity_media.py clips", text)

    # --- clip "tiếp": "ket": "giu" — hết clip thì app giữ khung cuối; danh sách nằm ở Resources/clips/index.json ---

    def index(self) -> dict:
        return json.loads((self.res / "index.json").read_text(encoding="utf-8"))

    def test_apply_writes_index_with_playable_hold_clips_only(self):
        for clip_id in ("a", "b", "c", "d"):
            self.src(clip_id, clip_id.encode())
        rows = [{**_row("a", "dat"), "ket": "giu"}, {**_row("b", "cho_duyet"), "ket": "giu"},
                {**_row("c", "khong_dat"), "ket": "giu"}, _row("d", "dat")]
        apply_sync(plan_sync(rows, self.clips, self.res), self.clips, self.res)
        self.assertEqual(self.index(), {"giu": ["a", "b"]})

    def test_index_written_even_without_hold_clips(self):
        self.src("a", b"a")
        apply_sync(plan_sync([_row("a", "dat")], self.clips, self.res), self.clips, self.res)
        self.assertEqual(self.index(), {"giu": []})

    def test_plan_in_sync_only_when_index_matches(self):
        self.src("a", b"a")
        self.dst("a", b"a")
        rows = [{**_row("a", "dat"), "ket": "giu"}]
        plan = plan_sync(rows, self.clips, self.res)
        self.assertTrue(plan.index_changed, "chưa có index.json")
        self.assertIn("run_unity_media.py clips", describe(plan))
        apply_sync(plan, self.clips, self.res)
        again = plan_sync(rows, self.clips, self.res)
        self.assertFalse(again.index_changed)
        self.assertIsNone(describe(again))
        rows[0]["ket"] = "khac"  # giá trị lạ: như không đánh dấu
        self.assertTrue(plan_sync(rows, self.clips, self.res).index_changed)

    def test_index_json_is_not_treated_as_a_stale_clip(self):
        self.src("a", b"a")
        apply_sync(plan_sync([_row("a", "dat")], self.clips, self.res), self.clips, self.res)
        plan = plan_sync([_row("a", "dat")], self.clips, self.res)
        self.assertEqual(plan.remove, [])
        self.assertTrue((self.res / "index.json").is_file())

    # --- tapdoc validate: chỉ cảnh báo, không tính là lỗi ---

    def run_validate(self) -> str:
        manifest = self.clips.parent / "video_manifest.json"
        manifest.write_text(json.dumps([_row("a", "dat")]), encoding="utf-8")
        out = io.StringIO()
        with patch.object(cli, "validate_all", return_value=[]), \
                patch.object(cli, "MEDIA_LOCK", self.clips.parent / "khong_co_khoa.json"), \
                patch.object(cli, "CLIPS", self.clips), patch.object(cli, "VIDEO_MANIFEST", manifest), \
                patch.object(cli, "UNITY_RES_CLIPS", self.res), patch("sys.stdout", out):
            self.assertEqual(cli.main(["validate"]), 0)
        return out.getvalue()

    def test_validate_warns_when_resources_clips_out_of_sync(self):
        self.src("a", b"a")
        text = self.run_validate()
        self.assertIn("Cảnh báo: clip trong Resources lệch danh mục", text)
        self.assertTrue(text.rstrip().endswith("OK"))

    def test_validate_quiet_when_clips_in_sync(self):
        self.src("a", b"a")
        self.dst("a", b"a")
        self.dst_index([])
        self.assertNotIn("clip trong Resources", self.run_validate())


if __name__ == "__main__":
    unittest.main()
