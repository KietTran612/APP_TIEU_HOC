"""Lõi tạo, khôi phục, duyệt và tạo hàng loạt âm thanh dùng chung cho CLI và trang duyệt."""

import copy
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .importer import _ID_RE, _looks_like_mp3, _without_changed_note, _write_atomic
from .mp3trim import trim_mp3
from .tts_engine import TtsError, TtsUnavailable
from .tts_settings import effective_params, needs_regen, set_override, signature


@dataclass
class BatchReport:
    done: list[str] = field(default_factory=list)
    failed: dict[str, str] = field(default_factory=dict)
    skipped: int = 0


def _paths(row, audio_dir, prev_dir):
    audio_id = row["id"]
    if not isinstance(audio_id, str) or not _ID_RE.fullmatch(audio_id):
        raise ValueError(f"Mã âm thanh không hợp lệ: {audio_id!r}")
    return (Path(audio_dir) / f"{audio_id}.mp3", Path(prev_dir) / f"{audio_id}.mp3",
            Path(prev_dir) / f"{audio_id}.json")


def _json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def generate_one(row, settings, engine, audio_dir, prev_dir) -> dict:
    """Chỉ thay file sau khi bộ đọc trả âm thanh; lỗi bộ đọc không chạm bản cũ."""
    dest, previous, metadata = _paths(row, audio_dir, prev_dir)
    p = effective_params(settings, row)
    result = engine.synthesize(p)
    if not result.audio or not _looks_like_mp3(result.audio):
        raise TtsError(f"{row['id']}: bộ đọc trả dữ liệu rỗng hoặc không phải MP3")
    audio, trimmed = trim_mp3(result.audio, result.speech_start, result.speech_end)
    updated = copy.deepcopy(row)
    updated.update(status="cho_duyet", source="tts_edge_hoaimy",
                   tts={**asdict(p), "sig": signature(p), "trimmed": trimmed})
    updated["ghi_chu"] = _without_changed_note(row.get("ghi_chu", ""))
    old_audio = dest.read_bytes() if dest.is_file() else None
    if old_audio is not None:
        # Mỗi lần tạo thành công đều thay bản trước bằng chính bản đang nghe.
        old = {key: copy.deepcopy(row[key]) for key in ("tts", "status", "source") if key in row}
        old["override"] = copy.deepcopy(settings["overrides"].get(row["id"]))
        backups = {path: path.read_bytes() if path.is_file() else None for path in (previous, metadata)}
        try:
            _write_atomic(previous, old_audio)
            _write_atomic(metadata, _json_bytes(old))
            _write_atomic(dest, audio)
        except OSError:
            # File đích ghi nguyên tử nên vẫn nguyên vẹn; trả cả cặp bản trước về như cũ.
            for path, content in backups.items():
                if content is None:
                    path.unlink(missing_ok=True)
                else:
                    _write_atomic(path, content)
            raise
    else:
        _write_atomic(dest, audio)
        previous.unlink(missing_ok=True)
        metadata.unlink(missing_ok=True)
    return updated


def restore_previous(row, settings, audio_dir, prev_dir) -> dict:
    """Trả file cùng thông số về bản trước; tiêu thụ bản trước sau khi khôi phục."""
    dest, previous, metadata = _paths(row, audio_dir, prev_dir)
    with open(metadata, encoding="utf-8") as f:
        old = json.load(f)
    data = previous.read_bytes()
    restored = copy.deepcopy(row)
    for key in ("tts", "status", "source"):
        restored.pop(key, None)
        if key in old:
            restored[key] = copy.deepcopy(old[key])
    config = copy.deepcopy(settings)
    record = old.get("tts")
    if record:
        if record["voice"] != config["voice"]:
            raise ValueError("Giọng đọc bản trước khác giọng hiện tại; cần khôi phục giọng trong cấu hình trước")
        set_override(config, restored, **{key: record[key] for key in ("doc", "rate", "pitch", "volume")})
    elif old.get("override"):
        config["overrides"][row["id"]] = old["override"]
    else:
        config["overrides"].pop(row["id"], None)
    _write_atomic(dest, data)
    settings["overrides"] = config["overrides"]
    previous.unlink()
    metadata.unlink()
    return restored


def approve(row, prev_dir) -> dict:
    """Duyệt bản hiện tại rồi bỏ bản trước."""
    _, previous, metadata = _paths(row, Path(), prev_dir)
    previous.unlink(missing_ok=True)
    metadata.unlink(missing_ok=True)
    return {**copy.deepcopy(row), "status": "dat"}


def selected(row, settings, *, lesson=None, kind=None, ids=None, include_approved=False):
    """Cùng một phép chọn cho chế độ thử và tạo thật."""
    return ((lesson is None or lesson in row.get("bai", []))
            and (kind is None or row.get("kind") == kind)
            and (ids is None or row["id"] in ids)
            and (include_approved or needs_regen(settings, row)))


def run_batch(rows, settings, engine, audio_dir, prev_dir, *, lesson=None, kind=None,
              ids=None, include_approved=False, on_progress=None, save=None) -> BatchReport:
    report = BatchReport()
    for index, row in enumerate(rows):
        if not selected(row, settings, lesson=lesson, kind=kind, ids=ids,
                        include_approved=include_approved):
            report.skipped += 1
            continue
        try:
            updated = generate_one(row, settings, engine, audio_dir, prev_dir)
        except TtsUnavailable:
            raise
        except (TtsError, OSError, ValueError) as e:
            report.failed[row["id"]] = str(e)
        else:
            rows[index] = updated
            report.done.append(row["id"])
        if save is not None:
            save(rows)
        if on_progress is not None:
            on_progress(row["id"], report)
    return report
