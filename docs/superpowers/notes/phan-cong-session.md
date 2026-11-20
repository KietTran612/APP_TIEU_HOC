# Phân công session — dự án "Bờ A Ba"

Bảng này do session điều phối (root) giữ. Cập nhật mỗi khi tạo session mới, giao việc lớn, hoặc một mảng việc xong.
Cập nhật lần cuối: 17/11/2026 (16:15). Từ 17/11 các session làm theo kế hoạch hoàn thiện 4 cuốn: [2026-11-17-hoan-thien-4-cuon.md](../plans/2026-11-17-hoan-thien-4-cuon.md). Lịch sử việc đã xong: [lich-su-cong-viec.md](lich-su-cong-viec.md). Quy trình chuẩn và cách giải vấn đề khó: [QUY-TRINH-LAM-VIEC.md](../../../QUY-TRINH-LAM-VIEC.md).

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
- **Sắp hết usage thì tạm ngưng** (chủ dự án 17/11). Usage 5 giờ và usage tuần dùng chung cho mọi session. Khi usage 5 giờ từ 97% trở lên (xem `get_usage`; chủ dự án đặt ngưỡng 97%), hoặc app báo giới hạn: dừng ở chỗ an toàn. Xong bước nhỏ đang làm; không để file viết dở, commit dở, hay lượt Unity sắp quá giờ. Ghi một dòng đã dừng ở đâu. Việc nền không tốn usage cứ chạy tiếp: tts, nhận dạng giọng nói, clip Flow đã gửi. Không gửi clip Flow mới. Root đặt lịch sau giờ reset để kiểm usage rồi báo các session làm tiếp.

## Danh sách session

| Session | Id | Mảng | Tình trạng (20/11) |
|---|---|---|---|
| Điều phối dự án Bờ A Ba (root) | `local_0cefca18-12fb-4d82-a1d6-a65ff28a9bed` | Điều phối, kiểm tra và duyệt mọi việc tới khi app hoàn chỉnh (chủ dự án 18/11) | Đang chạy |
| [L1] Làm SGK Tiếng Việt 1 tập 2 | `local_1af66fbb-4b38-439a-a40c-4b31d98db980` | Nội dung TV1 tập 2; giữ công cụ giọng đọc (tts) | Xong nội dung và âm thanh lớp 1; nghỉ từ 18/11 |
| [L1] Tranh động lớp 1 | `local_fdaead13-02aa-4c66-abfd-9eb7797cd628` | Clip cho TV1 (cả hai tập) | Lượt cách A /u/3 ngày 19/11: nhận b110, làm lại b112, b82 học sinh, b105 rước đèn, b33. Đã soát nhóm 1–3 theo bài học mới (e80c38e, dd79d13, 826b3b4). Lượt kế: 21/11 trên /u/3 |
| [L2] Làm SGK Tiếng Việt 2 tập 1 | `local_8c04ba54-8b7d-4491-97c5-f8b6526afa73` | Nội dung, âm thanh, màn mới, đóng gói TV2 tập 1 | Xong; nghỉ |
| [L2] Vẽ tranh Tiếng Việt 2 tập 1 | `local_be5a6177-2125-4c96-8ac1-da797a8751f8` | Tranh ChatGPT cho TV2 tập 1 | Xong; nghỉ |
| [L2] Tranh động Tiếng Việt 2 tập 1 | `local_d1b0f2bf-9813-44de-8419-c1b19596eb10` | Clip cho TV2 tập 1 và TV2 tập 2 | 20/11: 5 mã lớp 2 trên /u/3 từ 14:05 (7fc0e96, 23d4b0c). TV2 tập hai: 41/41 kịch bản và khung đầu đã duyệt (054d1f0, fd1dea4), chờ credit /u/1, /u/4 ngày 29/11 |
| [L2T2] Làm SGK Tiếng Việt 2 tập 2 | `local_7211e4a4-03f2-4c19-92c6-70263649b8cb` | Nội dung, âm thanh, đóng gói TV2 tập 2 (`tv2_t2_2002`, "Bé tập đọc 4") | Xong 130 mục và âm thanh 4 đợt (18/11); nghỉ |
| [L2T2] Vẽ tranh Tiếng Việt 2 tập 2 | `local_fb53b89b-8fc5-4226-8e5b-dcad52bf4290` | Tranh ChatGPT cho TV2 tập 2 | Xong 41/41 tranh (c9c0903); nghỉ |
| [Chung] UI và hiệu ứng | `local_98b994e9-1559-4920-b85d-4c3bcf3a5892` | Giao diện, hiệu ứng, màn mở đầu, Cài đặt, tỷ lệ màn hình | Nâng cấp UI 5 đợt, 3 tranh ChatGPT, 7 tiếng mới (tới 3df36c0) và sửa bảng đọc bài 80 (25c81f2); nghỉ |
| [Chung] Phát tranh động trong app | `local_cd9755d6-6fed-4a90-9ad3-707ee8949c86` | Phát clip trong app (spec 2026-11-18-tranh-dong-trong-app-design.md) | Clip phát ở 4 màn Phần 1 (tới 30916c9); clip cách B "tiếp" giữ khung cuối (d6a3e65, root chạy lại test xanh 19/11); nghỉ |
| [Chung] Refactor đọc dữ liệu | `local_1590fb2c-d64a-4465-b148-58ea493f67a0` | Cách nạp dữ liệu, chuẩn bị Addressables | Xong 4/11; nghỉ |

Clip TV2 tập 2 do [L2] Tranh động làm, không mở session riêng.

Session cũ (chủ dự án tự tách ra hoặc đã xong), không giao việc mới: "Setup project", "Kiểm tra data bài học ôn tập", "Chuẩn bị startup dự án" (2 bản fork ngày 29/10), "Đoạn chat phụ", và bản "Thử ảnh động / sprite sheet" cũ ngày 30/10.

## Việc chờ chủ dự án

Root kiểm tra và duyệt mọi việc tới khi app hoàn chỉnh. Khi xong, root gửi một danh sách tổng để chủ dự án xem một lần:
- những gì cần tai người nghe;
- các clip;
- các quyết định root đã chốt;
- rủi ro điều khoản Google Vids ("chỉ dùng trong Vids").

Các việc chỉ chủ dự án làm:
- Nói "test all" khi muốn chạy toàn bộ test.
- Push.
- Trước khi đăng app: chọn mã gói; tra nhãn hiệu "Bờ A Ba".
- Drive và các gói bổ sung: tạm dừng theo lời chủ dự án 19/11 ("chưa cần quan tâm đến drive").

Đã xong: bản đồ bài 97 vẽ lại bằng ChatGPT (17/11). App không còn tranh cắt từ scan.
