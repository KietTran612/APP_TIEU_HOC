"""Lõi tạo, khôi phục, duyệt và tạo hàng loạt âm thanh dùng chung cho CLI và trang duyệt."""

import copy
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from . import audio_join
from .importer import _ID_RE, _looks_like_mp3, _without_changed_note, _write_atomic
from .mp3trim import trim_mp3_span
from .tts_engine import TtsError, TtsUnavailable
from .tts_settings import VOICES, differs_from_settings, effective_params, set_override, signature
from .viet import tokens


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


KEEP_PAD = 0.1  # phần đệm trim_mp3_span giữ thêm sau lời (mặc định của nó)


def _speech_span(row, p, result):
    """Khoảng lời cần giữ: cả lời đọc, hoặc với keep_first chỉ các tiếng đầu (bằng số tiếng của chữ).

    Chỉ cắt được phần sau: khung MP3 của bộ đọc mượn dữ liệu khung trước nên đầu đoạn giữ luôn lùi về đầu file.
    """
    if not p.keep_first:
        return result.speech_start, result.speech_end
    count = len(tokens(row["text"]))
    if count == 0 or len(result.words) < count:
        raise TtsError(f"{row['id']}: không đủ mốc từ để cắt lấy tiếng đầu")
    start, end = result.words[0][0], result.words[count - 1][1]
    if len(result.words) > count:
        # Tiếng kế tiếp đọc liền ("mụ già."): phần đệm cuối (KEEP_PAD) không được lấn sang tiếng đó.
        end = max(start + 0.05, min(end, result.words[count][0] - KEEP_PAD))
    return start, end


def _write_marks(marks_dir, row, p, result, offset) -> None:
    """Mốc (giây, tính từ đầu file đã cắt) của các tiếng còn trong file, để đo cao độ từng tiếng."""
    words = result.words[:len(tokens(row["text"]))] if p.keep_first else result.words
    data = {"text": row["text"], "words": [[round(a - offset, 4), round(b - offset, 4)] for a, b in words]}
    Path(marks_dir).mkdir(parents=True, exist_ok=True)
    _write_atomic(Path(marks_dir) / f"{row['id']}.json", _json_bytes(data))


def _joined(row, p, audio_dir) -> bytes:
    """Ghép các tiếng trong p.join (cắt lặng, cân âm lượng, nghỉ p.join_gap; "," là nghỉ dài) thành một MP3."""
    ids, gaps = audio_join.plan(p.join, p.join_gap)
    paths = []
    for audio_id in ids:
        path = Path(audio_dir) / f"{audio_id}.mp3"
        data = path.read_bytes() if path.is_file() else b""
        if not data or not _looks_like_mp3(data):
            raise TtsError(f"{row['id']}: thiếu file ghép {audio_id}.mp3 hoặc file không phải MP3")
        paths.append(path)
    try:
        audio = audio_join.join_files(paths, gaps)
    except audio_join.JoinError as e:
        raise TtsError(f"{row['id']}: ghép tiếng lỗi: {e}") from e
    if not _looks_like_mp3(audio):
        raise TtsError(f"{row['id']}: ghép tiếng không ra MP3")
    return audio


def generate_one(row, settings, engine, audio_dir, prev_dir, marks_dir=None) -> dict:
    """Chỉ thay file sau khi bộ đọc trả âm thanh; lỗi bộ đọc không chạm bản cũ."""
    dest, previous, metadata = _paths(row, audio_dir, prev_dir)
    p = effective_params(settings, row)
    if p.join:
        audio, trimmed, source, result = _joined(row, p, audio_dir), False, "ghep_tieng", None
    else:
        result = engine.synthesize(p)
        if not result.audio or not _looks_like_mp3(result.audio):
            raise TtsError(f"{row['id']}: bộ đọc trả dữ liệu rỗng hoặc không phải MP3")
        audio, trimmed, offset = trim_mp3_span(result.audio, *_speech_span(row, p, result))
        if p.keep_first and not trimmed:
            raise TtsError(f"{row['id']}: không cắt được phần đọc lặp phía sau")
        source = "tts_edge_" + p.voice.removeprefix("vi-VN-").removesuffix("Neural").lower()
    updated = copy.deepcopy(row)
    updated.update(status="cho_duyet", source=source,
                   tts={**asdict(p), "join": list(p.join), "sig": signature(p), "trimmed": trimmed})
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
    if marks_dir is not None:
        if result is not None and result.words:
            _write_marks(marks_dir, row, p, result, offset)
        else:
            (Path(marks_dir) / f"{row['id']}.json").unlink(missing_ok=True)  # mốc cũ không còn khớp file mới
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
        if not isinstance(record.get("voice"), str) or record["voice"] not in VOICES:
            raise ValueError("Giọng đọc bản trước không hợp lệ")
        set_override(config, restored, **{key: record[key] for key in ("doc", "rate", "pitch", "volume", "voice")},
                     keep_first=record.get("keep_first", False), join=record.get("join", []),
                     join_gap=record.get("join_gap", 0.08))
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
    """Cùng một phép chọn cho chế độ thử và tạo thật: chỉ mã khác cấu hình; mã đã duyệt chỉ khi include_approved."""
    return ((lesson is None or lesson in row.get("bai", []))
            and (kind is None or row.get("kind") == kind)
            and (ids is None or row["id"] in ids)
            and differs_from_settings(settings, row)
            and (include_approved or row.get("status") != "dat"))


def run_batch(rows, settings, engine, audio_dir, prev_dir, *, lesson=None, kind=None,
              ids=None, include_approved=False, on_progress=None, save=None, marks_dir=None) -> BatchReport:
    report = BatchReport()
    for index, row in enumerate(rows):
        if not selected(row, settings, lesson=lesson, kind=kind, ids=ids,
                        include_approved=include_approved):
            report.skipped += 1
            continue
        try:
            updated = generate_one(row, settings, engine, audio_dir, prev_dir, marks_dir)
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
