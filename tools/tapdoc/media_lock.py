"""Khoá media: mã kiểm tra (sha256) của từng tranh và âm thanh đã đóng vào gói .unitypackage.

Tranh và âm thanh (cùng file .meta) không nằm trong git mà nằm trong gói đưa lên Google Drive. Khoá ghi tên gói
và mã kiểm tra từng file, nằm trong git (`content/manifests/media_lock.json`), để máy nào cũng biết file media
đang có có đúng với gói đã đóng hay không.
"""

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

MEDIA_DIRS = ("images", "audio")


def media_files(res_dir) -> list[Path]:
    """File tranh và âm thanh (không gồm .meta) trong Resources, sắp theo đường dẫn."""
    res = Path(res_dir)
    return sorted(p for d in MEDIA_DIRS if (res / d).is_dir() for p in (res / d).iterdir()
                  if p.is_file() and p.suffix != ".meta")


def _rel(res_dir, path: Path) -> str:
    return path.relative_to(res_dir).as_posix()


def snapshot(res_dir) -> dict[str, str]:
    return {_rel(res_dir, p): hashlib.sha256(p.read_bytes()).hexdigest() for p in media_files(res_dir)}


def missing_meta(res_dir) -> list[str]:
    """File chưa có .meta (Unity chưa nhập): đóng gói lúc này sẽ thiếu file đó hoặc đổi GUID."""
    return [_rel(res_dir, p) for p in media_files(res_dir) if not p.with_name(p.name + ".meta").is_file()]


def write_lock(res_dir, lock_path, package: str) -> dict:
    lock = {"package": package, "files": snapshot(res_dir)}
    Path(lock_path).write_text(json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return lock


@dataclass
class MediaDiff:
    package: str
    missing: list[str] = field(default_factory=list)
    changed: list[str] = field(default_factory=list)
    extra: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not (self.missing or self.changed or self.extra)


def compare(res_dir, lock_path) -> MediaDiff | None:
    """So file media trên máy với khoá; chưa có khoá thì None."""
    path = Path(lock_path)
    if not path.is_file():
        return None
    lock = json.loads(path.read_text(encoding="utf-8"))
    locked, current = lock["files"], snapshot(res_dir)
    return MediaDiff(package=lock["package"],
                     missing=sorted(set(locked) - set(current)),
                     changed=sorted(k for k in locked.keys() & current.keys() if locked[k] != current[k]),
                     extra=sorted(set(current) - set(locked)))


def describe(diff: MediaDiff | None) -> str | None:
    """Một dòng cảnh báo khi media trên máy khác gói đã ghi trong khoá; khớp hoặc chưa có khoá thì None."""
    if diff is None or diff.ok:
        return None
    return (f"media trên máy khác gói {diff.package}: thiếu {len(diff.missing)}, khác {len(diff.changed)}, "
            f"mới {len(diff.extra)} (thiếu thì nhập gói mới nhất; khác hoặc mới thì đóng gói lại: "
            f"python run_unity_media.py pack)")
