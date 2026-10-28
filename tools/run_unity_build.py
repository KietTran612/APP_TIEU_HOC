"""Build bản Windows của project Unity TapDoc hoặc mở bản build ở khung cửa sổ.

Cách dùng (chạy từ thư mục tools/):
    python run_unity_build.py
    python run_unity_build.py --launch 1600x720
    python run_unity_build.py --launch 1440x1080
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

from run_unity_tests import (
    BUSY_MARKER,
    BUSY_MESSAGE,
    OUTPUT,
    PROJECT,
    UNITY_EXE,
    print_log_errors,
    project_is_open,
    read_log,
)

EXE_PATH = PROJECT / "Builds" / "Windows" / "TapDoc.exe"


def launch_windowed(spec: str) -> int:
    match = re.fullmatch(r"(\d+)x(\d+)", spec.strip())
    if not match:
        print(f"Kích thước không hợp lệ: {spec!r} (cần dạng WxH, ví dụ 1600x720)")
        return 1
    if not EXE_PATH.exists():
        print(f"Chưa có file {EXE_PATH}. Hãy chạy `python run_unity_build.py` trước.")
        return 1

    width, height = match.group(1), match.group(2)
    cmd = [
        str(EXE_PATH),
        "-screen-fullscreen", "0",
        "-screen-width", width,
        "-screen-height", height,
    ]
    subprocess.Popen(cmd, cwd=str(EXE_PATH.parent))
    print(f"Đã mở {EXE_PATH} ở khung {width}x{height}")
    return 0


def build_windows() -> int:
    if project_is_open():
        print(BUSY_MESSAGE)
        return 2

    OUTPUT.mkdir(parents=True, exist_ok=True)
    log_path = OUTPUT / "build_windows.log"
    log_path.unlink(missing_ok=True)

    cmd = [
        str(UNITY_EXE),
        "-batchmode",
        "-projectPath", str(PROJECT),
        "-executeMethod", "TapDoc.EditorTools.BuildScript.BuildWindows",
        "-logFile", str(log_path),
    ]
    completed = subprocess.run(cmd)
    log_text = read_log(log_path)
    if BUSY_MARKER in log_text.lower():
        print(BUSY_MESSAGE)
        return 2

    if completed.returncode != 0 or not EXE_PATH.exists():
        print(f"Build Windows thất bại (mã thoát {completed.returncode}).")
        print_log_errors(log_text)
        print(f"  Log đầy đủ: {log_path}")
        return 1

    print(str(EXE_PATH))
    return 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Build hoặc mở bản Windows của TapDoc.")
    parser.add_argument("--launch", metavar="WxH", help="Mở TapDoc.exe ở khung cửa sổ WxH (ví dụ 1600x720)")
    args = parser.parse_args()

    if args.launch:
        return launch_windowed(args.launch)
    return build_windows()


if __name__ == "__main__":
    sys.exit(main())
