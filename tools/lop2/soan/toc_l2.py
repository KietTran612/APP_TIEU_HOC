"""Mục lục Tiếng Việt 2 tập một (tr.123–128) → danh sách 133 mục lớp 2 (lesson_no 172–304) và dòng CSV."""
import csv
import io
import json
import sys
from pathlib import Path

# (tuần, [(số bài, loại, tên, trang)], chính tả (tên1, tr1, tên2, tr2), từ ngữ (tên, tr), ngữ pháp (tên, tr), tlv (tên, tr))
TD, HTL, DT, CD = "tap_doc", "hoc_thuoc_long", "doc_them", "cau_do"
QS = "Quan sát tranh: "  # tên ngắn cho thẻ bài; trang in "Quan sát tranh và trả lời câu hỏi"
WEEKS = [
    (1, [(1, TD, "Bác Hồ khuyên học sinh", 4), (2, HTL, "Cái trống trường em", 6), (3, TD, "Niềm vui ngày khai trường", 7),
         (4, DT, "Mùa thu đẹp", 9)],
     ("Bác Hồ khuyên học sinh", 9, "Niềm vui ngày khai trường", 9), ("Ngày khai trường", 10), ("Câu", 10),
     ("Điền từ: Niềm vui ngày khai trường", 11)),
    (2, [(5, TD, "Ngôi trường mới", 12), (6, HTL, "Đi học", 13), (7, TD, "Đẹp mà không đẹp", 14),
         (8, DT, "Cô giáo với mùa thu", 16)],
     ("Ngôi trường mới", 16, "Cái trống trường em", 16), ("Trường học", 17), ("Câu (tiếp theo)", 17),
     ("Điền từ: Ngôi trường mới", 17)),
    (3, [(9, TD, "Đàn kiến nó đi", 18), (10, HTL, "Cô giáo lớp em", 19), (11, TD, "Bé và chim chích bông", 20),
         (12, DT, "Chú bộ đội lái máy bay", 21)],
     ("Đàn kiến nó đi", 22, "Đẹp mà không đẹp", 22), ("Thầy trò", 23), ("Câu – Mở đầu và kết thúc", 23),
     ("Điền từ: Cô giáo, thầy giáo của chúng em", 23)),
    (4, [(13, TD, "Cò và Vạc", 24), (14, HTL, "Quyển vở của em", 25), (15, CD, "Câu đố: Đồ dùng của học sinh", 27)],
     ("Cò và Vạc", 27, "Đi học", 28), ("Đồ dùng của học sinh", 28), ("Câu – Mở đầu và kết thúc (tiếp theo)", 29),
     ("Điền từ: Đồ dùng của Lan", 29)),
    (5, [(16, TD, "Có chí thì nên", 30), (17, HTL, "Khuyên chăm học", 31), (18, TD, "Chú gà trống ưa dậy sớm", 32),
         (19, DT, "Vượt bậc", 33)],
     ("Có chí thì nên", 34, "Chú gà trống ưa dậy sớm", 35), ("Ôn tập", 35), ("Câu", 36), ("Điền từ: Có chí thì nên", 36)),
    (6, [(20, TD, "Tình cảm gia đình", 38), (21, HTL, "Mẹ", 39), (22, TD, "Bố làm thợ mộc", 40), (23, DT, "Lòng mẹ", 41)],
     ("Tình cảm gia đình", 41, "Quyển vở của em", 42), ("Gia đình", 42), ("Câu – Hai bộ phận chính", 43),
     ("Điền từ: Gia đình Sơn", 43)),
    (7, [(24, TD, "Làm anh", 44), (25, HTL, "Ngôi nhà", 46), (26, TD, "Bé Hoa", 47), (27, DT, "Ông tôi", 48)],
     ("Làm anh", 49, "Bé Hoa", 49), ("Ông bà", 50), ("Câu – Hai bộ phận chính (tiếp theo)", 50), ("Điền từ: Chị và em", 51)),
    (8, [(28, TD, "Bé Mai trở thành người lớn như thế nào", 52), (29, HTL, "Nói với em", 53), (30, TD, "Giàn mướp", 55),
         (31, DT, "Quạt cho bà ngủ", 56)],
     ("Bé Mai trở thành người lớn như thế nào", 56, "Mẹ", 57), ("Họ hàng nội ngoại", 57),
     ("Câu – Hai bộ phận chính (tiếp theo)", 58), (QS + "Giàn mướp", 58)),
    (9, [(32, TD, "Đồ dùng để ở đâu", 59), (33, HTL, "Đàn gà mới nở", 60), (34, DT, "Cô Chổi Rơm", 62)],
     ("Đồ dùng để ở đâu", 62, "Đàn gà mới nở", 62), ("Ôn tập", 63), ("Câu – Hai bộ phận chính (tiếp theo)", 63),
     (QS + "Đàn gà mới nở", 64)),
    (10, [(35, TD, "Vẽ quê hương", 66), (36, HTL, "Ta yêu quê ta", 67), (37, TD, "Hồ Gươm", 68), (38, DT, "Rừng miền đông", 70)],
     ("Vẽ quê hương", 70, "Nói với em", 71), ("Quê hương đất nước", 71), ("Câu – Hai bộ phận chính (tiếp theo)", 71),
     (QS + "Quê hương", 72)),
    (11, [(39, TD, "Bến Nhà Rồng", 73), (40, HTL, "Gạch đỏ", 75), (41, TD, "Bến cảng Hải Phòng", 76),
          (42, DT, "Bốn mùa hoa thắm", 77)],
     ("Bến Nhà Rồng", 77, "Ta yêu quê ta", 78), ("Thành phố", 78), ("Ôn tập câu", 79), (QS + "Nhà máy gạch", 79)),
    (12, [(43, TD, "Cánh đồng lúa chín", 80), (44, HTL, "Lũy tre", 82), (45, TD, "Con đường làng", 83),
          (46, CD, "Câu đố: Quả gì?", 84)],
     ("Bến cảng Hải Phòng", 84, "Cánh đồng lúa chín", 85), ("Nông thôn", 85), ("Tiếng và chữ", 86),
     (QS + "Cánh đồng lúa chín", 88)),
    (13, [(47, TD, "Hoa mai vàng", 87), (48, HTL, "Một vài cảnh đẹp", 88), (49, TD, "Vùng mỏ", 90),
          (50, DT, "Chim én tìm tổ", 91)],
     ("Hoa mai vàng", 92, "Lũy tre", 92), ("Ôn tập", 92), ("Tiếng và từ", 93), (QS + "Vùng mỏ", 93)),
    (14, [(51, TD, "Nhớ Việt Bắc", 94), (52, HTL, "Sa Pa", 95), (53, TD, "Nhà Gấu ở trong rừng", 97),
          (54, DT, "Câu chuyện đàn ong mật", 98)],
     ("Một vài cảnh đẹp", 99, "Nhà Gấu ở trong rừng", 99), ("Rừng núi", 99), ("Chữ và chữ cái", 100),
     (QS + "Nhà Gấu ở trong rừng", 100)),
    (15, [(55, TD, "Biển đẹp", 101), (56, HTL, "Con chim chiền chiện", 102), (57, TD, "Quê em vùng biển", 103),
          (58, DT, "Mùa sương ở Hạ Long", 105)],
     ("Biển đẹp", 105, "Con chim chiền chiện", 106), ("Biển", 106), ("Bảng chữ cái", 107), (QS + "Cảnh biển buổi sáng", 107)),
    (16, [(59, TD, "Cây xoài của ông em", 108), (60, HTL, "Cây dừa", 110), (61, DT, "Truyện vui về cây Thì là", 111)],
     ("Quê em vùng biển", 112, "Sa Pa", 113), ("Ruộng vườn, cây cối", 113), ("Bảng chữ cái (tiếp theo)", 114),
     (QS + "Cây dừa", 114)),
    (17, [(62, TD, "Mùa xuân đến", 115), (63, HTL, "Thăm Trại Ba Vì", 116), (64, TD, "Đường dây điện", 118),
          (65, DT, "Hàng cây trồng theo lời Bác", 119)],
     ("Mùa xuân đến", 119, "Cây dừa", 120), ("Ôn tập", 120), ("Ôn: tiếng, từ, chữ, chữ cái", 121),
     (QS + "Thăm trại Ba Vì", 121)),
]


def theme(week):
    return "Nhà trường" if week <= 5 else "Gia đình" if week <= 9 else "Đất nước ta"


def image_of(page):
    if page in (56, 57):
        return "030"
    if page in (58, 59):
        return "029"
    return f"{page // 2 + 1:03d}"


def items():
    out, no = [], 172
    for week, readings, ct, tn, np_, tlv in WEEKS:
        for td_no, kind, title, page in readings:
            out.append(dict(lesson_no=no, week=week, theme=theme(week), type=kind, title=title, td_no=td_no, page=page))
            no += 1
        out.append(dict(lesson_no=no, week=week, theme=theme(week), type="tap_chep_chinh_ta",
                        title=f"{ct[0]} – {ct[2]}", page=ct[1], page2=ct[3])); no += 1
        out.append(dict(lesson_no=no, week=week, theme=theme(week), type="tu_ngu", title=tn[0], page=tn[1])); no += 1
        out.append(dict(lesson_no=no, week=week, theme=theme(week), type="ngu_phap", title=np_[0], page=np_[1])); no += 1
        out.append(dict(lesson_no=no, week=week, theme=theme(week), type="tap_lam_van", title=tlv[0], page=tlv[1])); no += 1
    assert no == 305, no
    return out


if __name__ == "__main__":
    rows = items()
    Path(sys.argv[1]).write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    for r in rows:
        bai = f"L2-B{r['td_no']}" if "td_no" in r else ""
        end = r.get("page2", r["page"])
        w.writerow(["tv2_t1_2001", r["theme"], r["week"], bai, r["title"], r["type"], r["page"], end, image_of(r["page"]),
                    r["title"], "metadata_verified", f"lesson_no {r['lesson_no']}"])
    Path(sys.argv[2]).write_text(buf.getvalue(), encoding="utf-8")
    print(len(rows))
