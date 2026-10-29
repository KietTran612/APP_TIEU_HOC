"""Cấu hình giọng đọc và dấu nhận dạng thông số của mỗi lần tạo."""

import hashlib
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

from .viet import nfc

_LIMITS = {"rate": (-60, 30), "pitch": (-30, 30), "volume": (-50, 50)}


@dataclass(frozen=True)
class TtsParams:
    doc: str
    rate: int
    pitch: int
    volume: int
    voice: str


def _number(key, value):
    low, high = _LIMITS[key]
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{key} phải là số nguyên từ {low} đến {high}")
    return value


def _validate(settings):
    if not isinstance(settings, dict) or not isinstance(settings.get("voice"), str) or not settings["voice"].strip():
        raise ValueError("Cấu hình phải có giọng đọc voice")
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
        if not isinstance(values, dict) or values.keys() - {"doc", *_LIMITS}:
            raise ValueError(f"Thông số chỉnh tay không hợp lệ: {audio_id}")
        if "doc" in values and not isinstance(values["doc"], str):
            raise ValueError(f"Cách đọc của {audio_id} phải là chữ")
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


def effective_params(settings: dict, row: dict) -> TtsParams:
    values = {**settings["defaults"][row["kind"]], **settings["overrides"].get(row["id"], {})}
    doc = values.get("doc") or row["text"]
    if not isinstance(doc, str):
        raise ValueError("Cách đọc phải là chữ")
    return TtsParams(nfc(doc), *(_number(key, values[key]) for key in _LIMITS), settings["voice"])


def signature(p: TtsParams) -> str:
    data = json.dumps(asdict(p), ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha1(data).hexdigest()


def set_override(settings, row, *, doc=None, rate=None, pitch=None, volume=None) -> None:
    values = dict(settings["overrides"].get(row["id"], {}))
    for key, value in (("doc", doc), ("rate", rate), ("pitch", pitch), ("volume", volume)):
        if value is None:
            continue
        if key == "doc":
            if not isinstance(value, str):
                raise ValueError("Cách đọc phải là chữ")
            value = nfc(value).strip()
        else:
            value = _number(key, value)
        values[key] = value
    defaults = {**settings["defaults"][row["kind"]], "doc": nfc(row["text"])}
    values = {key: value for key, value in values.items()
              if value != defaults[key] and not (key == "doc" and not value)}
    if values:
        settings["overrides"][row["id"]] = values
    else:
        settings["overrides"].pop(row["id"], None)


def differs_from_settings(settings, row) -> bool:
    record = row.get("tts")
    return not isinstance(record, dict) or record.get("sig") != signature(effective_params(settings, row))


def needs_regen(settings, row) -> bool:
    return row.get("status") != "dat" and differs_from_settings(settings, row)
