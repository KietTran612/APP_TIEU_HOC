"""Lớp 1: ghép mượt 2 câu còn khó sau khi "một" (tieng_mootj) và "đàn" (tieng_ddanf) đã có bản mới.

Chạy (từ thư mục tools), SAU khi regen_runner đã tạo xong mọi mã trong scripts/l1_nang_e_ids.txt:
    python scripts/l1_ghep_2_cau.py
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tapdoc.manifest import load_rows, save_rows  # noqa: E402
from tapdoc.paths import ROOT  # noqa: E402
from tapdoc.tts_settings import effective_params, load_settings, save_settings, signature  # noqa: E402

JOINS = {
    # Biển Đông một dải xanh lam cõi bờ.
    "cau_b97_02": ["tieng_bieenr", "tieng_ddoong", "tieng_mootj", "tieng_dair", "tieng_xanh", "tieng_lam",
                   "tieng_coix", "tieng_bowf"],
    # Một lát sau, ông Ké dắt theo sau một đàn cháu nhỏ.
    "cau_b160_04": ["tieng_mootj", "tieng_lats", "tieng_sau", ",", "van_oong", "tieng_kes", "tieng_dawts",
                    "tieng_theo", "tieng_sau", "tieng_mootj", "tieng_ddanf", "tieng_chaus", "tieng_nhor"],
}
NEED_NEW = ("tieng_mootj", "tieng_ddanf")


def main() -> int:
    path = ROOT / "content/manifests/audio_manifest.json"
    settings_path = ROOT / "content/tts/settings.json"
    rows = {r["id"]: r for r in load_rows(path)}
    s = load_settings(settings_path)
    for i in NEED_NEW:
        if (rows[i].get("tts") or {}).get("sig") != signature(effective_params(s, rows[i])):
            print(f"{i} chưa có bản mới: chạy regen_runner trước")
            return 1
    for i, join in JOINS.items():
        s["overrides"][i] = {"join": join}
    save_settings(settings_path, s)
    code = subprocess.run([sys.executable, "-m", "tapdoc", "tts", "--ma", *JOINS], cwd=ROOT / "tools").returncode
    rows_list = load_rows(path)
    for r in rows_list:
        if r["id"] in JOINS and r.get("source") == "ghep_tieng" and "ghép mượt" not in (r.get("ghi_chu") or ""):
            parts = " + ".join(x for x in JOINS[r["id"]] if x != ",")
            note = (f"Rà soát hỏi/ngã 10/11: đọc nguyên câu, đọc chậm, ngắt nhẹ đều chưa đạt → ghép mượt {parts}. "
                    "Chờ nghe xác nhận. Bản cũ ở prev.")
            r["ghi_chu"] = f"{r['ghi_chu']} | {note}" if r.get("ghi_chu") else note
    save_rows(path, rows_list)
    return code


if __name__ == "__main__":
    sys.exit(main())
