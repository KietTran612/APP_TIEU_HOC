"""Mục lục Tiếng Việt 2 tập hai (tr.122–124) → danh sách 130 mục (lesson_no 305–434) và dòng CSV.

Chạy: python toc_t2.py toc_t2.json <file dòng csv>
"""
import csv
import io
import json
import sys
from pathlib import Path

# (tuần, [(số bài, loại, tên, trang)], chính tả (tên1, tr1, tên2, tr2), từ ngữ (tên, tr), ngữ pháp (tên, tr), tlv (tên, tr))
# Tên theo đầu bài in trên trang. Bài 10 sách in "xú người" (nghĩa "xứ người"), xem spec TV2 tập 2.
# Mục lục in chung một dòng "12–13", "17–18", "22–23" (Bài đọc thêm): mỗi số là một bài riêng có đầu bài riêng.
TD, HTL, DT = "tap_doc", "hoc_thuoc_long", "doc_them"
TLC = "Trả lời câu hỏi: "
DT_CAU = "Dùng từ đặt câu"
WEEKS = [
    (18, [(1, TD, "Câu chuyện bó đũa", 4), (2, HTL, "Hòn đá to", 5), (3, TD, "Không sống riêng lẻ", 7),
          (4, DT, "Xe lu và xe ca", 8)],
     ("Câu chuyện bó đũa", 8, "Không sống riêng lẻ", 9), ("Thiếu nhi đoàn kết", 9), ("Danh từ", 10),
     (TLC + "Câu chuyện bó đũa", 10)),
    (19, [(5, TD, "Trên đường đến nhà lao", 11), (6, HTL, "Chú bé liên lạc", 12), (7, TD, "Ai can đảm", 14),
          (8, DT, "Làm cách nào dễ hơn", 15)],
     ("Trên đường đến nhà lao", 16, "Hòn đá to", 16), ("Thiếu nhi dũng cảm", 17), ("Danh từ (tiếp theo)", 18),
     (TLC + "Trên đường đến nhà lao", 18)),
    (20, [(9, TD, "Tủ sách của bạn Sắc", 19), (10, HTL, "Trăng sao cũng hóa xú người", 20), (11, TD, "Bóc lịch", 21),
          (12, DT, "Có một lần", 22), (13, DT, "Chiếc dao nóng nảy", 23)],
     ("Tủ sách của bạn Sắc", 24, "Ai can đảm", 24), ("Thiếu nhi chăm học", 25), ("Danh từ (tiếp theo)", 25),
     (TLC + "Tủ sách của bạn Sắc", 26)),
    (21, [(14, TD, "Làm việc thật là vui", 27), (15, HTL, "Tí Xíu", 28), (16, TD, "Sao Chổi", 29),
          (17, DT, "Chế giễu người lười", 31), (18, DT, "Chuyện bé Chăm", 32)],
     ("Làm việc thật là vui", 32, "Trăng sao cũng hóa xú người", 33), ("Thiếu nhi chăm làm", 33),
     ("Danh từ chung – Danh từ riêng", 34), (TLC + "Sao Chổi", 34)),
    (22, [(19, TD, "Hai con chim", 35), (20, HTL, "Tiếng ru", 36), (21, TD, "Con cáo và tổ ong", 38),
          (22, DT, "Cái ổ gà", 39), (23, DT, "Nhắn chú Phạm Tuân", 40)],
     ("Hai con chim", 41, "Con cáo và tổ ong", 41), ("Ôn tập chủ đề: Thiếu nhi", 42), ("Danh từ riêng", 42),
     (TLC + "Tí Xíu", 42)),
    (23, [(24, TD, "Phong cảnh đền Hùng", 44), (25, HTL, "Người trong một nước", 45), (26, TD, "Voi Bà Triệu ra trận", 46),
          (27, DT, "Gò Đống Đa", 47)],
     ("Phong cảnh đền Hùng", 48, "Tí Xíu", 48), ("Dân tộc Việt Nam", 49),
     ("Danh từ chung và danh từ riêng (tiếp theo)", 49), (TLC + "Phong cảnh đền Hùng", 49)),
    (24, [(28, TD, "Trần Quốc Toản ra quân", 50), (29, HTL, "Việt Nam có Bác", 51), (30, DT, "Một chiều hè lịch sử", 52)],
     ("Voi Bà Triệu ra trận", 53, "Trần Quốc Toản ra quân", 53), ("Dân tộc Việt Nam (tiếp theo)", 53),
     ("Ôn tập: Danh từ", 54), (TLC + "Trần Quốc Toản ra quân", 54)),
    (25, [(31, TD, "Đứng gác nơi biên giới", 55), (32, HTL, "Chú hải quân", 56), (33, TD, "Bộ đội đi trên Trường Sơn", 57),
          (34, DT, "Những cái chân", 58)],
     ("Đứng gác nơi biên giới", 59, "Người trong một nước", 59), ("Quân đội", 60),
     ("Danh từ riêng. Cách viết hoa tên người", 61), (TLC + "Bộ đội đi trên Trường Sơn", 61)),
    (26, [(35, TD, "Cái máy tuốt lúa", 62), (36, HTL, "Chăm việc cấy cày", 63), (37, TD, "Đánh cá đèn", 64),
          (38, DT, "Làm mưa", 65)],
     ("Cái máy tuốt lúa", 66, "Đánh cá đèn", 66), ("Nông nghiệp", 67), ("Cách viết hoa tên đất", 67), (DT_CAU, 68)),
    (27, [(39, TD, "Đàn bê của anh Hồ Giáo", 69), (40, HTL, "Trâu ơi", 70), (41, TD, "Phân xưởng gà con", 72),
          (42, DT, "Chị công nhân chăn bò", 73)],
     ("Đàn bê của anh Hồ Giáo", 74, "Chăm việc cấy cày", 74), ("Chăn nuôi", 75),
     ("Ôn cách viết hoa danh từ riêng", 75), (DT_CAU, 75)),
    (28, [(43, TD, "Anh thợ đốt lò", 76), (44, HTL, "Lên cao", 77), (45, TD, "Màu men cánh gián", 79),
          (46, DT, "Bác thợ xây vui tính", 80)],
     ("Anh thợ đốt lò", 81, "Màu men cánh gián", 81), ("Công nghiệp", 82),
     ("Tập xếp tên người theo thứ tự bảng chữ cái", 82), (DT_CAU, 82)),
    (29, [(47, TD, "Cánh tay khổng lồ", 83), (48, HTL, "Em muốn lái máy bay", 84), (49, TD, "Mẹ Thủy", 86),
          (50, DT, "Đoàn tàu chở hàng", 87)],
     ("Cánh tay khổng lồ", 88, "Trâu ơi", 88), ("Giao thông vận tải", 89),
     ("Tập xếp tên người theo thứ tự bảng chữ cái (tiếp theo)", 91), (DT_CAU, 91)),
    (30, [(51, TD, "Ông bác sĩ già", 92), (52, HTL, "Giọt mồ hôi", 93), (53, TD, "Một buổi đi thăm đoàn địa chất", 94),
          (54, DT, "Ai mạnh nhất trên đời", 96)],
     ("Ông bác sĩ già", 97, "Một buổi đi thăm đoàn địa chất", 98), ("Ôn tập chủ đề: Nhân dân ta", 98),
     ("Tập xếp tên người theo thứ tự bảng chữ cái (tiếp theo)", 99), (DT_CAU, 99)),
    (31, [(55, TD, "Có những mùa đông", 101), (56, HTL, "Nhớ ơn Bác Hồ", 102), (57, TD, "Bác Hồ ở chiến khu", 103),
          (58, DT, "Một que diêm", 104)],
     ("Có những mùa đông", 105, "Em muốn lái máy bay", 106), ("Ôn tập cuối năm: Nhà trường, gia đình", 106),
     ("Tóm tắt cách sắp tên người theo thứ tự bảng chữ cái", 107), (DT_CAU, 107)),
    (32, [(59, TD, "Thư của Chú Nguyễn", 108), (60, HTL, "Tổ nước ta", 109), (61, TD, "Quả táo của Bác Hồ", 110),
          (62, DT, "Bác rất thương loài vật", 112)],
     ("Thư của Chú Nguyễn", 112, "Bác Hồ ở chiến khu", 112), ("Ôn tập cuối năm: Đất nước, nhân dân", 113),
     ("Ôn tập: Tiếng – Từ – Câu", 114), (DT_CAU, 114)),
    (33, [(63, TD, "Phong cảnh quê hương Bác", 115), (64, HTL, "Nắng Ba Đình", 116),
          (65, TD, "Không có ngọn núi nào cao hơn", 117), (66, DT, "Hoa phượng", 119)],
     ("Phong cảnh quê hương Bác", 119, "Tổ nước ta", 119), ("Bác Hồ", 120), ("Ôn tập: Danh từ", 121), (DT_CAU, 121)),
]

FIRST, LAST = 305, 434


def theme(week):
    """Chủ điểm in trên trang bìa chủ điểm: tr.3 "Thiếu nhi", tr.43 "Nhân dân ta", tr.100 "Bác Hồ"."""
    return "Thiếu nhi" if week <= 22 else "Nhân dân ta" if week <= 30 else "Bác Hồ"


# Thứ tự ảnh scan bị xáo ở đầu sách (xem BOOK_CATALOG mục 4): bảng trang → ảnh.
_SPECIAL = {1: "005", 2: "008", 3: "008", 18: "001", 19: "001", 20: "004", 21: "004", 22: "007", 23: "007",
            24: "000", 25: "000", 26: "003", 27: "003", 28: "006", 29: "006"}


def image_of(page):
    if page in _SPECIAL:
        return _SPECIAL[page]
    if 4 <= page <= 17:
        return f"{10 + (page - 4) // 2 * 2:03d}"
    if 30 <= page <= 45:
        return f"{9 + (page - 30) // 2 * 2:03d}"
    if 46 <= page <= 125:
        return f"{page // 2 + 1:03d}"
    raise ValueError(page)


def items():
    out, no = [], FIRST
    for week, readings, ct, tn, np_, tlv in WEEKS:
        for td_no, kind, title, page in readings:
            out.append(dict(lesson_no=no, week=week, theme=theme(week), type=kind, title=title, td_no=td_no, page=page))
            no += 1
        out.append(dict(lesson_no=no, week=week, theme=theme(week), type="tap_chep_chinh_ta",
                        title=f"{ct[0]} – {ct[2]}", page=ct[1], page2=ct[3])); no += 1
        out.append(dict(lesson_no=no, week=week, theme=theme(week), type="tu_ngu", title=tn[0], page=tn[1])); no += 1
        out.append(dict(lesson_no=no, week=week, theme=theme(week), type="ngu_phap", title=np_[0], page=np_[1])); no += 1
        out.append(dict(lesson_no=no, week=week, theme=theme(week), type="tap_lam_van", title=tlv[0], page=tlv[1])); no += 1
    assert no == LAST + 1, no
    assert [r["td_no"] for r in out if "td_no" in r] == list(range(1, 67))
    return out


if __name__ == "__main__":
    rows = items()
    Path(sys.argv[1]).write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    for r in rows:
        bai = f"L2T2-B{r['td_no']}" if "td_no" in r else ""
        end = r.get("page2", r["page"])
        w.writerow(["tv2_t2_2002", r["theme"], r["week"], bai, r["title"], r["type"], r["page"], end, image_of(r["page"]),
                    r["title"], "metadata_verified", f"lesson_no {r['lesson_no']}"])
    Path(sys.argv[2]).write_text(buf.getvalue(), encoding="utf-8")
    print(len(rows))
