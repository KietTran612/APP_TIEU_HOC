"""Chép clip tranh động phát được từ `content/clips/` vào `Resources/clips/` của Unity.

`Resources/clips/` chỉ là bản chép ra (ngoài git, không ghi khoá media, không vào gói media): nguồn vẫn là
`content/clips/` cùng trạng thái trong `video_manifest.json`. Clip phát được là clip có trạng thái `dat` hoặc
`cho_duyet` (root chốt 18/11); clip `khong_dat` hay đã bỏ thì xoá khỏi Resources để app dùng tranh tĩnh.
"""

import hashlib
import os
from dataclasses import dataclass, field
from pathlib import Path

PLAYABLE_STATUSES = ("dat", "cho_duyet")
COMMAND_HINT = "python tools/run_unity_media.py clips"


@dataclass
class ClipSyncPlan:
    """Việc cần làm, theo mã tranh (đã sắp xếp)."""

    new: list[str] = field(default_factory=list)
    changed: list[str] = field(default_factory=list)
    remove: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    missing_source: list[str] = field(default_factory=list)

    @property
    def in_sync(self) -> bool:
        return not (self.new or self.changed or self.remove)


def _source(clips_dir: Path, clip_id: str) -> Path:
    """File nguồn của một mã: `content/clips/<mã>.mp4` (cách `importer.import_clips` đặt tên)."""
    return Path(clips_dir) / f"{clip_id}.mp4"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _same(a: Path, b: Path) -> bool:
    return a.stat().st_size == b.stat().st_size and _sha256(a) == _sha256(b)


def plan_sync(rows: list[dict], clips_dir, res_clips_dir) -> ClipSyncPlan:
    """So danh mục clip với `Resources/clips/` và trả việc cần làm; không đụng file nào."""
    clips_dir, res = Path(clips_dir), Path(res_clips_dir)
    plan = ClipSyncPlan()
    playable = {}
    for row in rows:
        if row.get("status") in PLAYABLE_STATUSES and row.get("id"):
            playable[row["id"]] = _source(clips_dir, row["id"])
    for clip_id, src in sorted(playable.items()):
        dst = res / f"{clip_id}.mp4"
        if not src.is_file():
            plan.missing_source.append(clip_id)
        elif not dst.is_file():
            plan.new.append(clip_id)
        elif _same(src, dst):
            plan.unchanged.append(clip_id)
        else:
            plan.changed.append(clip_id)
    if res.is_dir():
        plan.remove = sorted(p.stem for p in res.glob("*.mp4") if p.stem not in playable)
    return plan


def apply_sync(plan: ClipSyncPlan, clips_dir, res_clips_dir) -> None:
    """Làm theo `plan`: chép mới, chép đè (giữ `.meta`), xoá clip không còn phát (kèm `.meta`)."""
    clips_dir, res = Path(clips_dir), Path(res_clips_dir)
    res.mkdir(parents=True, exist_ok=True)
    for clip_id in [*plan.new, *plan.changed]:
        dst = res / f"{clip_id}.mp4"
        tmp = dst.with_name(dst.name + ".tmp")
        tmp.write_bytes(_source(clips_dir, clip_id).read_bytes())
        os.replace(tmp, dst)
    for clip_id in plan.remove:
        (res / f"{clip_id}.mp4").unlink(missing_ok=True)
        (res / f"{clip_id}.mp4.meta").unlink(missing_ok=True)


def describe(plan: ClipSyncPlan) -> str | None:
    """Câu cảnh báo khi `Resources/clips/` lệch tập clip phát được; khớp thì `None`."""
    if plan.in_sync:
        return None
    return (f"clip trong Resources lệch danh mục (mới {len(plan.new)}, đổi {len(plan.changed)}, "
            f"thừa {len(plan.remove)}): chạy {COMMAND_HINT} khi Unity đóng")
