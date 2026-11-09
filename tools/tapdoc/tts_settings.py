"""Cấu hình giọng đọc và dấu nhận dạng thông số của mỗi lần tạo."""

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from .viet import nfc

VOICES = {"vi-VN-HoaiMyNeural": "HoaiMy (nữ)", "vi-VN-NamMinhNeural": "NamMinh (nam)"}

_LIMITS = {"rate": (-60, 30), "pitch": (-30, 30), "volume": (-50, 50)}


@dataclass(frozen=True)
class TtsParams:
    doc: str
    rate: int
    pitch: int
    volume: int
    voice: str
    # Đọc cả doc (ví dụ "dỗ, dỗ.") rồi chỉ giữ các tiếng đầu, bằng số tiếng của chữ trong danh mục.
    keep_first: bool = False
    # Ghép tiếng: nối file của các mã này (đã có, thường đã duyệt) theo thứ tự thay vì gọi bộ đọc.
    join: tuple = ()
    join_gap: float = 0.08  # nghỉ giữa hai tiếng ghép (giây); dấu "," trong join là nghỉ dài


def _number(key, value):
    low, high = _LIMITS[key]
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{key} phải là số nguyên từ {low} đến {high}")
    return value


def _validate(settings):
    if not isinstance(settings, dict) or not isinstance(settings.get("voice"), str) or settings["voice"] not in VOICES:
        raise ValueError("Giọng đọc voice không hợp lệ")
    defaults, overrides = settings.get("defaults"), settings.get("overrides")
    if not isinstance(defaults, dict) or not isinstance(overrides, dict):
        raise ValueError("defaults và overrides phải là đối tượng JSON")
    for kind in ("am", "van", "dau", "tieng", "tu", "cau", "huong_dan", "khen"):
        values = defaults.get(kind)
        if not isinstance(values, dict):
            raise ValueError(f"Thiếu mặc định của loại {kind}")
        for key in _LIMITS:
            _number(key, values.get(key))
    for audio_id, values in overrides.items():
        if not isinstance(values, dict) or values.keys() - {"doc", "voice", "keep_first", "join", "join_gap", *_LIMITS}:
            raise ValueError(f"Thông số chỉnh tay không hợp lệ: {audio_id}")
        if "doc" in values and not isinstance(values["doc"], str):
            raise ValueError(f"Cách đọc của {audio_id} phải là chữ")
        if "voice" in values and (not isinstance(values["voice"], str) or values["voice"] not in VOICES):
            raise ValueError(f"Giọng đọc của {audio_id} không hợp lệ")
        if "keep_first" in values and type(values["keep_first"]) is not bool:
            raise ValueError(f"keep_first của {audio_id} phải là true hoặc false")
        if "join" in values:
            _join(values["join"])
        if "join_gap" in values:
            _join_gap(values["join_gap"])
        for key in values.keys() & _LIMITS.keys():
            _number(key, values[key])


def load_settings(path) -> dict:
    with open(path, encoding="utf-8") as f:
        settings = json.load(f)
    _validate(settings)
    return settings


def save_settings(path, settings: dict) -> None:
    _validate(settings)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    try:
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


_JOIN_ID = re.compile(r"[a-z0-9_]+")


def _join(value) -> list:
    """Danh sách ghép: ít nhất hai mã âm thanh; "," (nghỉ dài) chỉ đứng giữa hai mã, không liền nhau."""
    ok = isinstance(value, list) and all(isinstance(v, str) and (v == "," or _JOIN_ID.fullmatch(v)) for v in value)
    if ok:
        ids = [v for v in value if v != ","]
        ok = (len(ids) >= 2 and value[0] != "," and value[-1] != ","
              and all(not (a == "," and b == ",") for a, b in zip(value, value[1:])))
    if not ok:
        raise ValueError("join phải là danh sách từ hai mã âm thanh trở lên, \",\" chỉ đứng giữa hai mã")
    return list(value)


def _join_gap(value) -> float:
    if type(value) not in (int, float) or not 0.03 <= value <= 0.3:
        raise ValueError("join_gap phải là số giây từ 0.03 đến 0.3")
    return float(value)


def effective_params(settings: dict, row: dict) -> TtsParams:
    values = {**settings["defaults"][row["kind"]], **settings["overrides"].get(row["id"], {})}
    doc = values.get("doc") or row["text"]
    if not isinstance(doc, str):
        raise ValueError("Cách đọc phải là chữ")
    own = settings["overrides"].get(row["id"], {})
    return TtsParams(nfc(doc), *(_number(key, values[key]) for key in _LIMITS),
                     own.get("voice", settings["voice"]), own.get("keep_first", False),
                     tuple(own.get("join", ())), own.get("join_gap", 0.08))


def signature(p: TtsParams) -> str:
    values = asdict(p)
    if not values["keep_first"]:
        del values["keep_first"]  # giữ nguyên dấu nhận dạng của mọi bản tạo trước khi có keep_first
    if not values["join"]:
        del values["join"], values["join_gap"]
    data = json.dumps(values, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha1(data).hexdigest()


def set_override(settings, row, *, doc=None, rate=None, pitch=None, volume=None, voice=None,
                 keep_first=None, join=None, join_gap=None) -> None:
    values = dict(settings["overrides"].get(row["id"], {}))
    for key, value in (("doc", doc), ("rate", rate), ("pitch", pitch), ("volume", volume), ("voice", voice),
                       ("keep_first", keep_first), ("join", join), ("join_gap", join_gap)):
        if value is None:
            continue
        if key == "doc":
            if not isinstance(value, str):
                raise ValueError("Cách đọc phải là chữ")
            value = nfc(value).strip()
        elif key == "voice":
            if not isinstance(value, str) or value not in VOICES:
                raise ValueError("Giọng đọc không hợp lệ")
        elif key == "keep_first":
            if type(value) is not bool:
                raise ValueError("keep_first phải là true hoặc false")
        elif key == "join":
            value = _join(list(value)) if value else []
        elif key == "join_gap":
            value = _join_gap(value)
        else:
            value = _number(key, value)
        values[key] = value
    defaults = {**settings["defaults"][row["kind"]], "doc": nfc(row["text"]), "voice": settings["voice"],
                "keep_first": False, "join": [], "join_gap": 0.08}
    values = {key: value for key, value in values.items()
              if value != defaults[key] and not (key == "doc" and not value)}
    if values:
        settings["overrides"][row["id"]] = values
    else:
        settings["overrides"].pop(row["id"], None)


def ensure_keep_first(settings, audio_id: str, text: str) -> bool:
    """Tiếng lẻ đọc trong câu đệm "X, X." rồi giữ tiếng đầu; mã đã có chỉnh riêng thì giữ nguyên. True nếu đã ghi."""
    if audio_id in settings["overrides"]:
        return False
    settings["overrides"][audio_id] = {"doc": f"{text}, {text}.", "keep_first": True}
    return True


def differs_from_settings(settings, row) -> bool:
    record = row.get("tts")
    return not isinstance(record, dict) or record.get("sig") != signature(effective_params(settings, row))


def needs_regen(settings, row) -> bool:
    return row.get("status") != "dat" and differs_from_settings(settings, row)
