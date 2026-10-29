"""Danh mục âm thanh và tranh: mỗi mã một dòng, kèm trạng thái duyệt.

Danh mục là file JSON (danh sách dòng) do công cụ ghi và chủ dự án xem. Mỗi lần dựng lại, dòng
được lấy từ các bài vừa dựng cộng âm thanh/tranh dùng chung (`system_assets`); riêng `status`,
`source` và `ghi_chu` được giữ từ danh mục cũ, trừ khi file hoặc chữ đã thay đổi.
"""

import json
import os
import threading
import time
from pathlib import Path

from .build import BuildResult
from .system_assets import SYSTEM_AUDIO, SYSTEM_IMAGES
from .viet import nfc, split_syllable, tokens

CHUNG = "chung"

STATUS_NONE = "chua_co"  # chưa có file
STATUS_PENDING = "cho_duyet"  # có file, chờ chủ dự án nghe/xem
STATUS_OK = "dat"
STATUS_BAD = "khong_dat"
_KEPT_STATUSES = frozenset({STATUS_OK, STATUS_BAD, STATUS_PENDING})

TEXT_CHANGED_NOTE = "chữ đã đổi, cần tạo lại"

_CAREFUL_TONES = frozenset({"hoi", "nga"})
_CAREFUL_ONSETS = frozenset({"d", "gi", "v", "s", "x", "ch", "tr"})
_CAREFUL_CODAS = ("n", "ng", "t", "c")


class ManifestError(ValueError):
    """Danh mục không dựng được hoặc không đọc được (thông điệp nói rõ mã và nguyên nhân)."""


def careful_listen(text: str) -> bool:
    """Chữ có tiếng dễ nghe nhầm (hỏi/ngã, d/gi/v, s/x, ch/tr, vần cuối n/ng/t/c) cần đọc kỹ."""
    for token, _ in tokens(text):
        try:
            syllable = split_syllable(token)
        except ValueError:
            continue
        if (syllable.tone in _CAREFUL_TONES or syllable.onset in _CAREFUL_ONSETS
                or syllable.rime.endswith(_CAREFUL_CODAS)):
            return True
    return False


def load_rows(path) -> list[dict]:
    """Đọc danh mục; file chưa có thì trả về danh sách rỗng."""
    path = Path(path)
    try:
        with open(path, encoding="utf-8") as f:
            rows = json.load(f)
    except FileNotFoundError:
        return []
    except (OSError, ValueError) as e:
        raise ManifestError(f"{path}: không đọc được danh mục: {e}") from e
    if not isinstance(rows, list) or not all(isinstance(row, dict) and "id" in row for row in rows):
        raise ManifestError(f"{path}: danh mục phải là danh sách các dòng (đối tượng JSON có trường id)")
    return rows


_REPLACE_TRIES = 40  # tối đa khoảng 2 giây


def save_rows(path, rows: list[dict]) -> None:
    """Ghi danh mục qua file tạm rồi thay file cũ, để lần ghi dở không làm hỏng danh mục."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Trang duyệt và lệnh tts có thể cùng ghi: mỗi tiến trình, mỗi luồng một file tạm riêng.
    tmp = path.with_name(f"{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    try:
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
            f.write("\n")
        for attempt in range(_REPLACE_TRIES):
            try:
                os.replace(tmp, path)
                break
            except PermissionError:
                # Windows không cho thay file khi tiến trình khác đang mở đọc; chờ một chút rồi thử lại.
                if attempt == _REPLACE_TRIES - 1:
                    raise
                time.sleep(0.05)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


def _same_text_key(text: str) -> str:
    """Khóa so sánh lời đọc: chữ thường, NFC, bỏ mọi ký tự không phải chữ hay khoảng trắng."""
    kept = "".join(ch if ch.isalpha() else " " if ch.isspace() else "" for ch in nfc(nfc(text).lower()))
    return " ".join(kept.split())


def _status(file_exists: bool, old_status: str | None) -> str:
    if not file_exists:
        return STATUS_NONE
    return old_status if old_status in _KEPT_STATUSES else STATUS_PENDING


def _with_changed_note(old_note: str) -> str:
    if TEXT_CHANGED_NOTE in old_note:
        return old_note
    return f"{TEXT_CHANGED_NOTE}; {old_note}" if old_note else TEXT_CHANGED_NOTE


def _system_audio_kind(audio_id: str) -> str:
    return "huong_dan" if audio_id.startswith("hd_") else "khen"


def update_audio_manifest(results: list[BuildResult], old_rows: list[dict], audio_dir) -> list[dict]:
    """Danh mục âm thanh mới: mã của các bài vừa dựng và `SYSTEM_AUDIO`, xếp theo `id`.

    Một mã chỉ có một lời đọc. Hai bài (hoặc một bài và `SYSTEM_AUDIO`) cho cùng mã mà lời đọc
    khác nhau (sau khi bỏ khác biệt hoa/thường, dấu câu, khoảng trắng) thì báo `ManifestError`.
    """
    audio_dir = Path(audio_dir)
    old_by_id = {row["id"]: row for row in old_rows}
    # mã -> [lời đọc gặp đầu tiên, loại, bài đã gặp đầu tiên, tập mã bài]
    wanted: dict[str, list] = {}

    def want(audio_id: str, text: str, kind: str, lesson_id: str) -> None:
        entry = wanted.get(audio_id)
        if entry is None:
            wanted[audio_id] = [nfc(text), kind, lesson_id, {lesson_id}]
            return
        if _same_text_key(entry[0]) != _same_text_key(text):
            raise ManifestError(
                f"mã âm thanh {audio_id} có hai lời đọc khác nhau: {entry[0]!r} (bài {entry[2]}) "
                f"và {text!r} (bài {lesson_id})")
        entry[3].add(lesson_id)

    for audio_id, text in SYSTEM_AUDIO.items():
        want(audio_id, text, _system_audio_kind(audio_id), CHUNG)
    for result in results:
        lesson_id = result.lesson["lesson_id"]
        for audio_id, (text, kind) in result.audio.items():
            want(audio_id, text, kind, lesson_id)

    rows = []
    for audio_id in sorted(wanted):
        text, kind, _, lessons = wanted[audio_id]
        old = old_by_id.get(audio_id, {})
        file_exists = (audio_dir / f"{audio_id}.mp3").is_file()
        status = _status(file_exists, old.get("status"))
        note = old.get("ghi_chu", "")
        old_text = old.get("text")
        if file_exists and old_text is not None and _same_text_key(old_text) != _same_text_key(text):
            status = STATUS_BAD
            note = _with_changed_note(note)
        rows.append({
            "id": audio_id,
            "text": text,
            "kind": kind,
            "file": f"audio/{audio_id}.mp3",
            "source": old.get("source", ""),
            "status": status,
            "can_nghe_ky": careful_listen(text),
            "ghi_chu": note,
            "bai": sorted(lessons),
        })
        if "tts" in old:
            rows[-1]["tts"] = dict(old["tts"])
    return rows


def update_image_manifest(results: list[BuildResult], old_rows: list[dict], image_dir) -> list[dict]:
    """Danh mục tranh mới: mã của các bài vừa dựng và `SYSTEM_IMAGES`, xếp theo `id`."""
    image_dir = Path(image_dir)
    old_by_id = {row["id"]: row for row in old_rows}
    wanted: dict[str, list] = {}  # mã -> [mô tả gặp đầu tiên, tập mã bài]

    def want(image_id: str, description: str, lesson_id: str) -> None:
        entry = wanted.setdefault(image_id, [nfc(description), set()])
        entry[1].add(lesson_id)

    for image_id, description in SYSTEM_IMAGES.items():
        want(image_id, description, CHUNG)
    for result in results:
        lesson_id = result.lesson["lesson_id"]
        for image_id, description in result.images.items():
            want(image_id, description, lesson_id)

    rows = []
    for image_id in sorted(wanted):
        description, lessons = wanted[image_id]
        old = old_by_id.get(image_id, {})
        file_exists = (image_dir / f"{image_id}.png").is_file()
        rows.append({
            "id": image_id,
            "mo_ta": description,
            "bai": sorted(lessons),
            "file": f"images/{image_id}.png",
            "source": old.get("source", ""),
            "status": _status(file_exists, old.get("status")),
            "ghi_chu": old.get("ghi_chu", ""),
        })
    return rows
