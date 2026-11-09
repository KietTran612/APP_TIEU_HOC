# Phân công session — dự án "Bờ A Ba"

Bảng này do session điều phối (root) giữ. Cập nhật mỗi khi tạo session mới, giao việc lớn, hoặc một mảng việc xong.
Cập nhật lần cuối: 09/11/2026.

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

| Session | Id | Mảng | Tình trạng (09/11) |
|---|---|---|---|
| Điều phối dự án Bờ A Ba (root) | `local_0cefca18-12fb-4d82-a1d6-a65ff28a9bed` | Điều phối; tự vẽ lẻ tranh lớp 1 | Đang chạy |
| [L1] Làm SGK Tiếng Việt 1 tập 2 | `local_1af66fbb-4b38-439a-a40c-4b31d98db980` | Nội dung TV1 tập 2; giữ công cụ giọng đọc (tts) | Tập 2 đã chốt và đóng gói 9/11. Đang tạo lại các âm thanh bị chấm không đạt bằng `keep_first` |
| [L1] Tranh động lớp 1 | `local_fdaead13-02aa-4c66-abfd-9eb7797cd628` | Clip Flow cho TV1 (cả hai tập) | 343 clip; 12 clip bị chê đã làm lại, chờ duyệt |
| [L2] Làm SGK Tiếng Việt 2 tập 1 | `local_8c04ba54-8b7d-4491-97c5-f8b6526afa73` | Nội dung, âm thanh, màn mới, đóng gói TV2 tập 1 | Mới tạo; đang lập kế hoạch cùng chủ dự án |
| [L2] Vẽ tranh Tiếng Việt 2 tập 1 | `local_be5a6177-2125-4c96-8ac1-da797a8751f8` | Tranh ChatGPT cho TV2 tập 1 | Chờ danh sách tranh đợt 1 |
| [L2] Tranh động Tiếng Việt 2 tập 1 | `local_d1b0f2bf-9813-44de-8419-c1b19596eb10` | Clip Flow cho TV2 tập 1 | Chờ tranh đợt 1 |
| [Chung] UI và hiệu ứng | `local_98b994e9-1559-4920-b85d-4c3bcf3a5892` | Giao diện, hiệu ứng, màn mở đầu, Cài đặt, tỷ lệ màn hình | Xong tới f8a607e; chờ "test all" |
| [Chung] Refactor đọc dữ liệu | `local_1590fb2c-d64a-4465-b148-58ea493f67a0` | Cách nạp dữ liệu, chuẩn bị Addressables | Xong 4/11; nghỉ |

Session cũ (chủ dự án tự tách ra hoặc đã xong), không giao việc mới: "Setup project", "Kiểm tra data bài học ôn tập", "Chuẩn bị startup dự án" (2 bản fork ngày 29/10), "Đoạn chat phụ", và bản "Thử ảnh động / sprite sheet" cũ ngày 30/10.

## Việc chờ chủ dự án

- Duyệt tranh, âm thanh, clip của cả hai tập lớp 1 trong tool duyệt (chọn ô "Sách").
- Tải gói `dist/TapDoc-media-2026-11-09.unitypackage` và `dist/TapDoc-clips-2026-11-09.zip` lên Drive.
- Bản đồ bài 97 (TV1 tập 2): đang dùng ảnh cắt tạm từ scan, phải vẽ lại trước khi phát hành.
- Nói "test all" khi muốn chạy toàn bộ test.
- Push.
- Trước khi đăng app: chọn mã gói; tra nhãn hiệu "Bờ A Ba".
