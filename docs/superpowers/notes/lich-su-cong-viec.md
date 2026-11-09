# Lịch sử công việc — dự án "Bờ A Ba"

Ghi lại những gì đã làm xong, theo ngày, mới nhất ở trên cùng. Session điều phối (root) cập nhật file này mỗi khi một session báo xong một phần việc, sau khi đã kiểm tra commit và file thật. Mỗi mục ghi:
- ai làm, làm gì;
- commit;
- test đã chạy;
- việc còn dở.

Phân công hiện tại xem ở [phan-cong-session.md](phan-cong-session.md). Chi tiết từng mảng xem các ghi chú `*-tiep-tuc-*.md` cùng thư mục.

---

## 09/11/2026

**Root — điều phối**
- Gom kết quả duyệt của chủ dự án và giao sửa theo mảng: 32 âm thanh và 12 clip tập 1 bị chấm "không đạt".
- Tự vẽ lại tranh cử tạ bài 13 thành vận động viên người lớn (7f13b2a).
- Lập 3 session mới cho Tiếng Việt 2 tập 1; đặt tiền tố [L1]/[L2]/[Chung] cho tên session.
- Viết bảng phân công session: d5a1a01, 6d226aa, e109ade, bf60ae0, 7e99565.

**[L1] Làm SGK Tiếng Việt 1 tập 2** (`local_1af66fbb…`)
- Chốt tập 2:
  - 2 âm thanh cuối (8a6a7b4); bài 97 build lại với ghi chú bản đồ tạm (210cc1c);
  - `validate` không lỗi;
  - gói media `TapDoc-media-2026-11-09` và `TapDoc-clips-2026-11-09` (746792b), chờ chủ dự án tải lên Drive.
- Sửa âm thanh:
  - thêm cách đọc lặp "X, X." rồi giữ tiếng đầu (`keep_first`) cho tiếng lẻ (1b3623c, 9a1171f);
  - tạo lại 30/32 mã bị chê. Chủ dự án nghe lại: 21/30 đạt, toàn bộ 18 tiếng thanh hỏi, ngã đều đạt.
- Rà soát toàn bộ thanh hỏi, ngã, phần tiếng lẻ:
  - đo 268 tiếng, 92 nghi sai, đã sửa đạt mẫu 92/92;
  - áp `keep_first` cho 138/142 tiếng hỏi, ngã còn lại.
  - Bản cũ để trong `prev`, danh mục chưa commit (chờ chủ dự án duyệt).
- Làm trang nghe thử 8 mã khó (thanh nặng, ê mang thanh sắc, "hờ", "bé bá cổ bà", "tổ dế"): `.superpowers/nghe-thu/index.html`, chờ chủ dự án chọn.
- Sửa dữ liệu tập 2: danh mục âm thanh dùng lại 87 mã có sẵn (98880eb); test `Index_EntriesNameTheirBook` (3effd2c).
- **Còn dở:**
  - rà hỏi, ngã trong từ, câu, lời dẫn (775 mã; đang thử đọc chậm 20%);
  - rà âm ê (879 mã; máy không đo được lỗi nguyên âm, chờ chủ dự án chọn trên trang nghe thử);
  - thanh nặng (288 tiếng lẻ).

**[L1] Tranh động lớp 1** (`local_fdaead13…`)
- Làm lại 12 clip tập 1 bị chê, cả clip cử tạ theo tranh mới. Kịch bản: b4d5ed4, 5a12fdb. Clip ở trạng thái chờ duyệt, chưa đóng gói Drive.

**[L2] Làm SGK Tiếng Việt 2 tập 1** (`local_8c04ba54…`)
- Spec và plan được duyệt: 23311a1, 9478423.
- Công cụ:
  - quyển lớp 2, tắt đánh vần (4099a87, 8df282f);
  - lệnh `tapdoc pitch` và cờ `tts --tieng-keep-first` (753004a, sửa 90fbf81, 9678b22);
  - 3 bước mới (ff7519e, 38d19d1).
- Unity:
  - thẻ Lớp 1/Lớp 2, mở khoá theo lớp (39ead72);
  - màn ghép chữ, điền đoạn, chọn dòng (f1ae593);
  - sửa cỡ chạm tối thiểu (a9c22b8), xáo thẻ điền đoạn (eeac040).
- Nội dung: đủ 133 mục 172–304, tuần 1–17 (081c868, 089718c, 92f6df4, f92809b, edbb6e4, 0b810e9, 6859d2c).
- Test:
  - Python liên quan đạt; test hồi quy 171 mục lớp 1 đạt;
  - smoke test 133 mục 4/4 đạt; PlayMode lọc đạt;
  - EditMode 158/159 (còn `AllReferencedAssetsExist`, chờ tranh và âm thanh).
- **Còn dở:** âm thanh khoảng 3.300 mã (đang tạo, khoảng 8 mã/phút); review code độc lập; đóng gói media.

**[L2] Vẽ tranh Tiếng Việt 2 tập 1** (`local_be5a6177…`)
- Đợt L2-1: 9 tranh và kí hiệu giải nghĩa (447cf3e).
- Đợt L2-2: 18 tranh (d239be1).
- **Còn dở:** đợt L2-3 (18 tranh), đợt L2-4 (12 tranh).

**[L2] Tranh động Tiếng Việt 2 tập 1** (`local_d1b0f2bf…`)
- Đã tạo trên Flow 27 clip (đợt L2-1 và L2-2), chờ chủ dự án cho phép tải về.

**[Chung] UI và hiệu ứng** (`local_98b994e9…`)
- Viết bản thiết kế "Tủ sách" (`docs/superpowers/specs/2026-11-09-tu-sach-design.md`), đang qua người đọc độc lập, chưa duyệt.

## 06/11/2026

- **Root:**
  - vẽ 25 tranh tập 2 còn thiếu bằng ChatGPT (8c43d12), tập 2 đủ 155/155 tranh;
  - tìm ra cách lấy ảnh qua dữ liệu cuộc trò chuyện khi trang ChatGPT bị treo.
- **[L1] Tranh động:**
  - ghi 129 clip tập 2 bài 81–150 vào danh mục (04cb04b);
  - làm 24 clip đợt cuối (56fdd22); tập 2 có 153 clip.
- **[L1] Tập 2:** âm thanh HoaiMy 2249 mã (9201f56) và 27 mã lượt bù (f591cd6).

## 05/11/2026

- **[L1] Tập 2:** đưa Tiếng Việt 1 tập 2 vào app.
  - Bài 81–125 (Vần) và Tập đọc tuần 27–33: 7b2ad34 … b42061f.
  - Các bước Tập đọc, bảng vần có cột câu; danh sách bài ba phần.
  - Test đi hết 91 mục (a71a5ee).
  - Tranh cắt tạm từ scan cho bản đồ bài 97 (c31e355); bản phát hành bị chặn cho tới khi vẽ lại.
- **Root:**
  - danh sách tranh tập 2 (93486a3, e2bffd8, 08dc42c);
  - nhập 130 tranh tập 2 (b50bb9d);
  - thêm ô chọn Sách vào tool duyệt (5dcc4ed);
  - đặt tên app "Bờ A Ba" (8b8a2f0).
- **[Chung] UI:**
  - tỷ lệ màn hình cách B, co giãn cho điện thoại và máy tính bảng (5b8bd2f … 128728c);
  - màn mở đầu, popup Gửi phụ huynh, menu Cài đặt, đổi/xoá hồ sơ, tắt sao lưu (aed2f50 … 5e26e1d).

## 04/11/2026

- **[Chung] Refactor đọc dữ liệu:** dọn cách app đọc dữ liệu, chuẩn bị Addressables. Gồm nguồn dữ liệu theo loại và mã, AssetCatalog, kho bài có bộ nhớ đệm, màn chuyển gà con khi chuẩn bị bài (574727f … a8ce5bf).
- **Root:**
  - tool duyệt thêm tab "Duyệt theo bài", hiện trang sách gốc cạnh bảng (a24174f … 3bd8daf);
  - lưu các mã âm thanh chủ dự án đã duyệt (a120f18, 951d7f4).

## 02/11/2026

- **Root:**
  - các cách đọc của chữ (đọc khi học, âm chuẩn, tên chữ cái) theo Phụ lục tr.120–122, kèm 24 âm thanh mới và nút trong bài (980255b … 4dd084c);
  - tranh và âm thanh ra khỏi git, chuyển sang gói media trên Google Drive (a34bb21, c373d68, 66da49b);
  - hướng dẫn cài máy mới (0974c2b).
- **[L1] Tranh động:** đủ 190/190 clip tập 1 (092f6e0).

## 30/10/2026

- **Root:**
  - ghi chú cho phụ huynh, mục "Chú ý và Phụ lục" (74ce1ef);
  - sửa cắt MP3 và tạo lại 1.236 âm thanh (e9f1f90, 269ebde);
  - 6 tranh còn thiếu, đủ 199 tranh tập 1 (7808597);
  - vẽ lại tranh cá thờn bơn (f9f0203);
  - duyệt clip trong tool (c1ae6f8).
- **[Chung] UI:** giao diện, hiệu ứng, tiếng động, Sổ bé ngoan, hình giao diện chính thức (24d89a3 … 7c9fbb7); test all đạt.
- **[L1] Tranh động:** hướng dẫn kiểu sáng tạo, kịch bản 190 tranh, 52 clip đầu (2674eb5).

## 29/10/2026

- **Root:** hoàn thành Tiếng Việt 1 tập 1.
  - Bài 1–17 (f792778), 18–41 (fc4510c), 42–64, 65–80.
  - Bảng ôn vần, bảng nhóm vần, câu đố.
  - Công cụ giọng đọc edge-tts HoaiMy và trang duyệt âm thanh.
  - Âm thanh HoaiMy cho bài 1–80; tranh bài 42–80.

## 28/10/2026

- Bản mẫu đầu tiên: bài 4, 13, 42 của Tiếng Việt 1 tập 1 (fc0c75d).
