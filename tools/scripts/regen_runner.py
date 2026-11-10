"""Tạo lại âm thanh các mã còn khác cấu hình: 1 tiến trình, mỗi mã tối đa 150 giây, có lượt bù.

Đầu mỗi lượt hỏi `tapdoc tts --thu` xem mã nào còn thiếu, nên bị tắt giữa chừng thì chạy lại là tiếp từ chỗ dở.
Mỗi mã một dòng log, ghi ngay.

Chạy (từ thư mục tools):
    python scripts/regen_runner.py scripts/l1_nang_e_ids.txt ../.superpowers/regen.log 4
"""
import os
import subprocess
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def main(id_file: str, log_file: str, passes: int = 4) -> None:
    ids = Path(id_file).read_text(encoding="utf-8").split()
    log = open(log_file, "a", encoding="utf-8", buffering=1)

    def say(msg):
        log.write(time.strftime("%m-%d %H:%M:%S ") + msg + "\n")

    def remaining():
        p = subprocess.run([sys.executable, "-m", "tapdoc", "tts", "--ma", *ids, "--thu"], cwd=TOOLS, env=ENV,
                           capture_output=True, text=True, encoding="utf-8")
        return [l.strip() for l in p.stdout.splitlines() if l.strip() and not l.startswith("Sẽ tạo")]

    for n in range(1, passes + 1):
        todo = remaining()
        say(f"LƯỢT {n}: còn {len(todo)} mã")
        if not todo:
            break
        ok = fail = 0
        for k, audio_id in enumerate(todo, 1):
            try:
                p = subprocess.run([sys.executable, "-m", "tapdoc", "tts", "--ma", audio_id], cwd=TOOLS, env=ENV,
                                   capture_output=True, text=True, encoding="utf-8", timeout=150)
                good = "Đã tạo 1" in p.stdout
                why = "" if good else (p.stderr.strip().splitlines() or [p.stdout.strip()])[-1][:160]
            except subprocess.TimeoutExpired:
                good, why = False, "quá 150 giây"
            ok += good
            fail += not good
            say(f"{'ok ' if good else 'LỖI'} {audio_id} {why}")
            if k % 50 == 0:
                say(f"  {k}/{len(todo)}: tạo {ok}, lỗi {fail}")
            time.sleep(2 if good else 6)
        say(f"HẾT LƯỢT {n}: tạo {ok}, lỗi {fail}")
        time.sleep(20)
    say(f"XONG: còn {len(remaining())} mã")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 4)
