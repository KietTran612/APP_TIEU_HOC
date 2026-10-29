"""Chạy test của project Unity TapDoc ở chế độ batchmode và in kết quả gọn.

Cách dùng (chạy từ thư mục tools/):
    python run_unity_tests.py editmode
    python run_unity_tests.py editmode --filter TapDoc.Tests.SetupTests

Kết quả XML ghi vào unity/TapDoc/TestOutput/<platform>.xml, log ghi vào
unity/TapDoc/TestOutput/<platform>.log. Dòng tóm tắt có dạng
"EditMode: 20 passed, 0 failed, 1 ignored" (thêm "skipped"/"inconclusive" khi có), kèm tên
và lý do của từng test bị bỏ qua. Exit 0 khi không có test lỗi.
"""
import argparse
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

UNITY_EXE = Path("C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe")
PROJECT = Path(__file__).resolve().parent.parent / "unity" / "TapDoc"
OUTPUT = PROJECT / "TestOutput"

PLATFORMS = {"editmode": "EditMode", "playmode": "PlayMode"}
BUSY_MARKER = "another unity instance is running"
BUSY_MESSAGE = "Hãy đóng Unity Editor đang mở project TapDoc"
LOCKFILE = PROJECT / "Temp" / "UnityLockfile"
MAX_LOG_ERRORS = 20


def project_is_open():
    """Unity giữ khoá độc quyền trên Temp/UnityLockfile khi project đang mở (Windows)."""
    if not LOCKFILE.exists():
        return False
    try:
        with open(LOCKFILE, "r+b"):
            return False
    except PermissionError:
        return True
    except OSError:
        return False


def read_log(log_path):
    if not log_path.exists():
        return ""
    return log_path.read_text(encoding="utf-8", errors="replace")


def print_log_errors(log_text):
    """In các dòng lỗi biên dịch / lỗi chung trong log để biết vì sao không có kết quả."""
    pattern = re.compile(r"error CS\d+|Scripts have compiler errors|Compilation failed", re.I)
    lines = [ln.strip() for ln in log_text.splitlines() if pattern.search(ln)]
    seen = []
    for ln in lines:
        if ln not in seen:
            seen.append(ln)
    for ln in seen[:MAX_LOG_ERRORS]:
        print("  " + ln)
    if len(seen) > MAX_LOG_ERRORS:
        print(f"  ... và {len(seen) - MAX_LOG_ERRORS} dòng lỗi nữa (xem log)")


def failure_text(element):
    failure = element.find("failure")
    if failure is None:
        return ""
    message = (failure.findtext("message") or "").strip()
    return message


def reason_text(element):
    """Lý do bỏ qua (Assert.Ignore, Inconclusive...) nằm ở <reason><message>."""
    for tag in ("reason", "failure"):
        node = element.find(tag)
        if node is not None:
            message = (node.findtext("message") or "").strip()
            if message:
                return message
    return ""


def summarize(xml_path, label):
    try:
        root = ET.parse(xml_path).getroot()
    except (OSError, ET.ParseError):
        print(f"Không đọc được kết quả test: {xml_path}")
        return 2
    cases = list(root.iter("test-case"))
    passed = [c for c in cases if c.get("result") == "Passed"]
    failed = [c for c in cases if c.get("result") == "Failed"]
    skipped_all = [c for c in cases if c.get("result") == "Skipped"]
    ignored = [c for c in skipped_all if c.get("label") == "Ignored"]
    skipped = [c for c in skipped_all if c.get("label") != "Ignored"]
    inconclusive = [c for c in cases if c.get("result") == "Inconclusive"]

    counts = [f"{len(passed)} passed", f"{len(failed)} failed", f"{len(ignored)} ignored"]
    if skipped:
        counts.append(f"{len(skipped)} skipped")
    if inconclusive:
        counts.append(f"{len(inconclusive)} inconclusive")
    print(f"{label}: " + ", ".join(counts))
    for case in failed:
        print(f"  FAIL {case.get('fullname')}")
        message = failure_text(case)
        if message:
            for line in message.splitlines():
                print("    " + line)
    for tag, group in (("IGNORED", ignored), ("SKIPPED", skipped), ("INCONCLUSIVE", inconclusive)):
        for case in group:
            reason = reason_text(case)
            print(f"  {tag} {case.get('fullname')}" + (f": {reason}" if reason else ""))

    if not cases:
        print("  Không có test nào được chạy (kiểm tra --filter hoặc asmdef).")
        return 1
    if failed:
        return 1
    if root.get("result", "").startswith("Failed"):
        # Suite lỗi mà không có test-case nào lỗi (ví dụ OneTimeSetUp ném exception).
        print("  Lượt chạy báo lỗi ở mức suite:")
        for suite in root.iter("test-suite"):
            message = failure_text(suite)
            if suite.get("result", "").startswith("Failed") and message:
                print(f"    {suite.get('fullname')}: {message}")
        return 1
    return 0


def main():
    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Chạy test Unity của project TapDoc.")
    parser.add_argument("platform", choices=sorted(PLATFORMS))
    parser.add_argument("--filter", dest="test_filter", help="Tên (hoặc nhiều tên cách nhau bằng ;) test cần chạy")
    parser.add_argument("--timeout", type=int, default=1800, metavar="SECONDS", help="Thời gian chờ Unity tối đa (giây)")
    args = parser.parse_args()

    if not UNITY_EXE.exists():
        print(f"Không tìm thấy Unity: {UNITY_EXE}", file=sys.stderr)
        return 2

    label = PLATFORMS[args.platform]
    if project_is_open():
        # Unity batchmode thoát im lặng (mã 1, không thông điệp trong log) khi project đang mở nơi khác.
        print(BUSY_MESSAGE)
        return 2

    OUTPUT.mkdir(parents=True, exist_ok=True)
    xml_path = OUTPUT / f"{args.platform}.xml"
    log_path = OUTPUT / f"{args.platform}.log"
    xml_path.unlink(missing_ok=True)  # tránh đọc nhầm kết quả của lần chạy trước
    log_path.unlink(missing_ok=True)

    command = [
        str(UNITY_EXE),
        "-batchmode",
        "-projectPath", str(PROJECT),
        "-runTests",
        "-testPlatform", label,
        "-testResults", str(xml_path),
        "-logFile", str(log_path),
    ]
    if args.test_filter:
        command += ["-testFilter", args.test_filter]

    try:
        completed = subprocess.run(command, timeout=args.timeout)
    except subprocess.TimeoutExpired:
        print(f"Unity chạy quá {args.timeout} giây, đã dừng.", file=sys.stderr)
        return 2

    log_text = read_log(log_path)
    if BUSY_MARKER in log_text.lower():
        print(BUSY_MESSAGE)
        return 2

    if not xml_path.exists():
        print(f"{label}: Unity thoát với mã {completed.returncode} và không tạo file kết quả {xml_path}")
        print_log_errors(log_text)
        print(f"  Log đầy đủ: {log_path}")
        return 2

    return summarize(xml_path, label)


if __name__ == "__main__":
    sys.exit(main())
