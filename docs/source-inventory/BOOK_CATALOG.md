# BOOK_CATALOG — Kiểm kê sách nguồn

> Khảo sát ngày 28/10/2026 qua GitHub API. Danh sách bài chi tiết: [LESSON_INDEX.csv](LESSON_INDEX.csv). Cấu trúc từng loại bài: [LESSON_TYPES.md](LESSON_TYPES.md).

## 1. Repository nguồn

| Mục | Giá trị |
|---|---|
| Repo | https://github.com/giangtv134/sach-giao-khoa-viet-nam |
| Nhánh / commit | `main` @ `7fadf3e8570085ba193e4abf92a2570fcbae7cc0` (06/11/2025, 7 commit) |
| Dung lượng | ~230 MB |
| Giấy phép | **Không có** file LICENSE |
| Nguồn gốc ảnh | README ghi nguồn https://thuongmaitruongxua.vn/ds-chuyen-muc/ban-scan-sgk-cac-thoi-ky; mọi trang có watermark "thuongmaitruongxua.vn" |
| Trạng thái | README ghi "Updating" |

**Cách dùng trong dự án:** chỉ là tài liệu tham chiếu nội bộ. Không đưa ảnh scan vào app.

## 2. Quy ước file

- Mỗi thư mục là một quyển, gồm các ảnh JPG **trang đôi** (khoảng 1400 px chiều ngang) và một file PDF ghép từ các ảnh đó (`converter.js` cắt đôi ảnh ngang thành hai trang PDF).
- Tiền tố `NNN_` cho biết thứ tự ảnh. **Chữ `Trang_N` trong tên file không phải số trang in.**
- Với TV1 T1 và TV1 T2, ảnh `NNN` chứa trang in `2·NNN−2` và `2·NNN−1`, ví dụ ảnh `010` chứa trang 18–19. Ngoại lệ được ghi ở mục 4.

## 3. Danh sách quyển trong repo

| book_id | Quyển | Ảnh | Thông tin in (đọc từ trang sách) | Mục lục | Thuộc hệ sách cũ? | Mức xác minh |
|---|---|---|---|---|---|---|
| `tv1_t1_1990` | Tiếng Việt 1 – Tập một (Chữ cái và Vần) | 64 | Vụ Giáo dục phổ thông – Bộ Giáo dục; NXB Giáo dục 1990, in lần thứ hai. Biên tập: Phạm Bích Hợp; minh họa: Hồng Kỳ – Phạm Ngọc Tới | Có, tr.123–124 (80 bài) | Có | `toc_verified`; 22 bài và các trang phụ `page_verified` |
| `tv1_t2_1996` | Tiếng Việt 1 – Tập hai (Vần – Tập đọc) | 72 | Bộ GD&ĐT; NXB Giáo dục; in lần thứ 8, chỉnh lí năm 1994; ghi chú tay "1996" | Có, tr.139–140 | Có | `toc_verified` |
| `tv2_t1_2001` | Tiếng Việt 2 – Tập một | 66 | Bộ GD&ĐT; Trịnh Mạnh – Đinh Tấn Ký – Đỗ Quang Lưu; tái bản lần thứ hai mươi | Có, khoảng tr.125–127 (theo tuần, phân môn) | Có | `metadata_verified` |
| `tv2_t2_2002` | Tiếng Việt 2 – Tập hai | 65 | Mã số 1H202T2; in xong và nộp lưu chiểu tháng 1/2002; bìa sau ghi "Tái bản" | Chưa tìm | Có: in 01/2002 dưới dạng tái bản, trong khi sách lớp 2 mới đến năm 2003 mới dùng | `metadata_verified` |
| `truyen_doc_1_2000` | Truyện đọc 1 | 44 | Chưa xem | — | Chưa xác minh | `unverified` |
| `truyen_doc_2_2001` | Truyện đọc 2 | 61 | Chưa xem | — | Chưa xác minh | `unverified` |

## 4. Vấn đề đã phát hiện

1. **Repo không có lớp 3, 4, 5.** thuongmaitruongxua.vn (mục "Giai đoạn 1990 – 2003") vẫn có các quyển này, cùng năm in với danh sách trong tài liệu khởi tạo:
   - Tiếng Việt 3: tập 1 (1997), tập 2 (2002).
   - Tiếng Việt 4: tập 1 (2002), tập 2 (2003).
   - Tiếng Việt 5: tập 1 (1998), tập 2 (2004).
   - Truyện đọc 3 (2001), Truyện đọc 4 (1992), Truyện đọc 5 (2001).

   Mục "Giai đoạn 1980 – 1989" của trang này còn có bản đầu tiên của chương trình: Học vần lớp 1 tập 1 (1981), tập 2 (1986) và Tập đọc lớp 1 (1985).
2. **TV1 T1:** ảnh `041` và `042` bị đảo thứ tự. Ảnh `041` chứa tr.82–83 (bài 61) và lấy từ một bản scan khác (màu giấy, màu mực khác); ảnh `042` chứa tr.80–81 (bài 60). Tính cả hai ảnh này thì đủ trang 0–124.
3. **TV2 T1:** có hai ảnh cùng tên `Trang_29` (`029`, `030`). Chưa kiểm xem có trùng trang hay không.
4. **TV2 T2:** thứ tự ảnh bị xáo trộn, mỗi tên `Trang_N` lặp lại 2–3 lần (ví dụ ảnh `001` chứa tr.18–19). Phải sắp lại theo số trang in trên sách.
5. **TV1 T1 (1990) và TV1 T2 (chỉnh lí 1994)** thuộc hai lần in khác nhau. Số bài nối tiếp nhau (80 → 81), nhưng chưa kiểm xem bản chỉnh lí 1994 có sửa nội dung Tập 1 hay không.

## 5. Trang tham chiếu quan trọng (TV1 T1)

| Trang | Ảnh | Nội dung | Dùng cho |
|---|---|---|---|
| 4 | `003` | Các kí hiệu dùng trong sách: ● Em đọc, ▨ Em viết, ●▨ Em đọc và viết, ⌂ Luyện tập ở lớp và ở nhà | Đọc hiểu bố cục trang |
| 120 | `061` | Bảng chữ cái: thứ tự, tên chữ cái, cách ghi âm của 29 chữ | Kịch bản âm thanh |
| 121 | `061` | Bảng gọi tên chữ ghép: iê, yê, uô, ươ, ch, kh, nh, th, ph, gh, ng, ngh, tr, gi | Kịch bản âm thanh |
| 122 | `062` | Chú ý: dạy bằng tên âm; cách đọc riêng của c, k, q, d, gi, i, y, g, gh, ng, ngh, qu; cách đánh vần vần rồi đến tiếng | Quy tắc đánh vần |
