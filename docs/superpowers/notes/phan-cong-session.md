# Phân công session — dự án "Bờ A Ba"

Bảng này do session điều phối (root) giữ. Cập nhật mỗi khi tạo session mới, giao việc lớn, hoặc một mảng việc xong.
Cập nhật lần cuối: 10/11/2026 (tạm dừng, chuyển máy — xem CHUYEN-MAY-MOI.md). Lịch sử việc đã xong: [lich-su-cong-viec.md](lich-su-cong-viec.md). Quy trình chuẩn và cách giải vấn đề khó: [QUY-TRINH-LAM-VIEC.md](../../../QUY-TRINH-LAM-VIEC.md).

## Nguyên tắc

- **Root điều phối, không làm thay.** Việc thuộc mảng nào thì giao cho session của mảng đó. Root chỉ tự làm khi chưa có session phụ trách (ví dụ vẽ lại lẻ một tranh lớp 1).
- **Mỗi sách có bộ session riêng.** Không giao việc lớp 2 cho session lớp 1 và ngược lại. Việc dùng chung cho cả app (UI, kỹ thuật đọc dữ liệu) thuộc nhóm `[Chung]`.
- **Thứ tự theo đợt:**
  1. Session nội dung soạn bài và gửi danh sách tranh của đợt cho session vẽ tranh.
  2. Session vẽ tranh nhập tranh xong mới báo session tranh động.
  3. Âm thanh do session nội dung tạo.
  4. Cuối cùng session nội dung đóng gói media.
- **Không đẻ việc khi chưa có đầu vào.** Ví dụ: không làm clip khi tranh chưa nhập.
- **Lỗi từ duyệt:** root gom các mục `khong_dat` và ghi chú duyệt trong ba danh mục, chia theo mảng:
  - âm thanh → session nội dung (hoặc session đang giữ công cụ giọng đọc);
  - tranh → session vẽ tranh của sách đó (lớp 1: root);
  - clip → session tranh động của sách đó.
- **Chỉnh sửa duyệt** của chủ dự án nằm trong working copy của danh mục và không được commit lẫn. Các session chỉ stage dòng của mình.
- Tên session có tiền tố `[L1]`, `[L2]`, `[Chung]`. Thanh bên luôn xếp session con dưới session root, nên dùng tiền tố thay cho nhóm.
- Root báo chủ dự án ngắn gọn sau mỗi lần một session báo về, và kiểm tra lại kết quả (commit, file) trước khi báo "xong".

## Danh sách session

| Session | Id | Mảng | Tình trạng (11/11) |
|---|---|---|---|
| Điều phối dự án Bờ A Ba (root) | `local_0cefca18-12fb-4d82-a1d6-a65ff28a9bed` | Điều phối; tự vẽ lẻ tranh lớp 1 | Đang chạy |
| [L1] Làm SGK Tiếng Việt 1 tập 2 | `local_1af66fbb-4b38-439a-a40c-4b31d98db980` | Nội dung TV1 tập 2; giữ công cụ giọng đọc (tts) | Xong âm thanh lớp 1: thanh nặng, âm ê (68a4ed7), mụ (1619f07), 7 từ Em viết của bài Ôn tập (7461625, bb6c51f). Lớp 1 không còn mã `chua_co`; chờ chủ dự án nghe |
| [L1] Tranh động lớp 1 | `local_fdaead13-02aa-4c66-abfd-9eb7797cd628` | Clip Flow cho TV1 (cả hai tập) | Làm lại clip bị chê đợt 11/11: tập 1 xong 20/27 (17f2366, 15c77c9, 1a09bed). Còn 7 clip tập 1, 32 clip tập 2 và clip cái cuốc b101; làm tiếp từ 12/11 trên /u/4, gửi chậm |
| [L2] Làm SGK Tiếng Việt 2 tập 1 | `local_8c04ba54-8b7d-4491-97c5-f8b6526afa73` | Nội dung, âm thanh, màn mới, đóng gói TV2 tập 1 | Xong: nội dung 133 mục và âm thanh 3.321/3.321 mã, đã đo và sửa hỏi, ngã (b26949d, 379aeb7); chờ chủ dự án nghe (danh sách ở ghi chú tiếp tục mục 1b) |
| [L2] Vẽ tranh Tiếng Việt 2 tập 1 | `local_be5a6177-2125-4c96-8ac1-da797a8751f8` | Tranh ChatGPT cho TV2 tập 1 | Xong: đủ 4 đợt, 57 tranh và kí hiệu giải nghĩa (447cf3e, d239be1, d7bbff2, 957e711); chờ duyệt |
| [L2] Tranh động Tiếng Việt 2 tập 1 | `local_d1b0f2bf-9813-44de-8419-c1b19596eb10` | Clip Flow cho TV2 tập 1 | Xong 57/57 clip (28fe7be, a0662f8, d553b83); chờ duyệt |
| [Chung] UI và hiệu ứng | `local_98b994e9-1559-4920-b85d-4c3bcf3a5892` | Giao diện, hiệu ứng, màn mở đầu, Cài đặt, tỷ lệ màn hình | Tủ sách xong tới 916a3ca (chọn quyển, 3 bìa mới, tên "Bé tập đọc 1/2/3"); chờ duyệt bìa và "test all" |
| [Chung] Refactor đọc dữ liệu | `local_1590fb2c-d64a-4465-b148-58ea493f67a0` | Cách nạp dữ liệu, chuẩn bị Addressables | Xong 4/11; nghỉ |

Session cũ (chủ dự án tự tách ra hoặc đã xong), không giao việc mới: "Setup project", "Kiểm tra data bài học ôn tập", "Chuẩn bị startup dự án" (2 bản fork ngày 29/10), "Đoạn chat phụ", và bản "Thử ảnh động / sprite sheet" cũ ngày 30/10.

## Việc chờ chủ dự án

- Duyệt tranh, âm thanh, clip của cả hai tập lớp 1 trong tool duyệt (chọn ô "Sách").
- Tải bản cập nhật 11/11 lên Drive: các file trong `C:\Source\AURA\BoABa-chuyen-may-2026-11-10\upload-cap-nhat-2026-11-11\`.
- Bản đồ bài 97 (TV1 tập 2): đang dùng ảnh cắt tạm từ scan, phải vẽ lại trước khi phát hành.
- Nói "test all" khi muốn chạy toàn bộ test.
- Push.
- Trước khi đăng app: chọn mã gói; tra nhãn hiệu "Bờ A Ba".
