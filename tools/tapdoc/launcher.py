"""Phần hỗ trợ mở công cụ duyệt bằng một cú nhấp (MoCongCuDuyet.cmd ở gốc repo)."""

import importlib.util
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

REQUIREMENTS = Path(__file__).resolve().parents[1] / "requirements-tts.txt"


def tool_running(port: int, timeout: float = 1.0) -> bool:
    """Cổng này đang chạy đúng công cụ duyệt (không phải chương trình khác)?"""
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/tts/job", timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (OSError, ValueError):
        return False
    return isinstance(data, dict) and "running" in data


def ensure_edge_tts(*, find_spec=importlib.util.find_spec, run=subprocess.run) -> bool:
    """Cài edge-tts lần đầu; cài không được thì vẫn nghe và duyệt được, chỉ chưa tạo lại được."""
    if find_spec("edge_tts") is not None:
        return True
    print("Đang cài bộ đọc edge-tts (chỉ lần đầu)...", flush=True)
    command = [sys.executable, "-m", "pip", "install"]
    if sys.prefix == sys.base_prefix:
        command.append("--user")  # không ở môi trường ảo thì cài vào tài khoản, không cần quyền quản trị
    if run(command + ["-r", str(REQUIREMENTS)]).returncode == 0:
        return True
    print("Chưa cài được edge-tts. Vẫn nghe và duyệt được, nhưng chưa tạo lại âm thanh được.")
    return False
