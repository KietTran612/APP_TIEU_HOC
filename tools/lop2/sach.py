"""Chọn tập cho các script lớp 2: mặc định Tiếng Việt 2 tập một (tv2_t1_, bài 172–304); cờ --t2 chọn tập hai
(tv2_t2_, bài 305–434). Chỉ lấy mã mà mọi bài đều thuộc tập đã chọn: mã dùng chung với cuốn khác do session của
cuốn đó giữ (thiết kế TV2 tập hai mục 7)."""

FLAG = "--t2"
RANGES = {"tv2_t1_": (172, 304), "tv2_t2_": (305, 434)}


def prefix(argv: list) -> str:
    """Tiền tố mã bài của tập đã chọn; bỏ cờ --t2 khỏi `argv` để các tham số vị trí giữ nguyên chỗ."""
    if FLAG in argv:
        argv.remove(FLAG)
        return "tv2_t2_"
    return "tv2_t1_"


def only_book_ids(rows: list, pre: str) -> list:
    """Dòng danh mục có `bai` không rỗng và mọi mã bài bắt đầu bằng `pre`."""
    return [r for r in rows if r.get("bai") and all(b.startswith(pre) for b in r["bai"])]
