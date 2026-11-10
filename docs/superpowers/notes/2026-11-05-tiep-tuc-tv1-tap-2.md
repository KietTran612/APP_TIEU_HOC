# Ghi chú tiếp tục — TV1 Tập 2 và âm thanh lớp 1 (cập nhật 10/11/2026)

Đọc file này trước khi làm tiếp. Thiết kế: [2026-11-05-tv1-tap-2-design.md](../specs/2026-11-05-tv1-tap-2-design.md); kế hoạch: [2026-11-05-tv1-tap-2.md](../plans/2026-11-05-tv1-tap-2.md). Cách làm âm thanh chuẩn: `QUY-TRINH-LAM-VIEC.md` mục 6 và 12.

## 0. Đợt thanh nặng và âm ê lớp 1 — XONG (10/11, chạy tiếp trên máy cũ)

- Tạo lại đủ 390/390 mã (`tools/scripts/l1_nang_e_ids.txt`), ghép mượt 2 câu `cau_b97_02`, `cau_b160_04`. Mọi mã `cho_duyet`, ghi chú "Rà soát thanh nặng/âm ê 10/11 … Chờ nghe xác nhận".
- **Chỉ 120 file mp3 thật sự đổi** (danh sách `tools/scripts/l1_mp3_doi_1011.txt`, cần đóng gói bổ sung lên Drive). 272 mã đọc "X. X." + `keep_first` ra file **trùng từng byte** với bản cũ đọc "X" trần (edge-tts tạo từng câu riêng) — ghi chú nói rõ "âm thanh không đổi". Xem `QUY-TRINH-LAM-VIEC.md` mục 12.
- Đổi thật: mụ ("mụ già."), nụ ("nụ hoa."), đàn ("đàn, đàn."), câu b16_02 ("bé, bá cổ bà." −25%), các tiếng ê và hỏi/ngã đọc dấu phẩy. "một" không đổi (trùng bản cũ) nên 2 câu ghép dùng bản "một" hiện có.
- Đo lại: 4 mã đo lạ (ạch, ặp — không đo được cao độ; kịch, sạch — đo ra như ngang) đều trùng bản cũ, chỉ ghi chú. Câu b16_02 đạt tiêu chí trong câu; các tiếng thành phần của 2 câu ghép đo khớp thanh.
- Việc tiếp nếu chủ dự án nghe thấy tiếng nặng còn sai: đặt trong ngữ cảnh như "nụ hoa." rồi `keep_first` (không dùng dấu chấm).

## 0b. Đã làm trong đợt rà soát âm thanh 09/11 (chờ chủ dự án nghe trong tool duyệt)

- Tiếng lẻ hỏi/ngã: 233 mã `keep_first` ("X, X.", cứng đầu thì "X, X, X."); cải, phải giữ bản cũ.
- Câu/từ/lời dẫn hỏi/ngã: đọc chậm −20% (53 mã), ngắt nhẹ bằng dấu phẩy (83 mã), ghép mượt 3 từ (chỗ ở, gõ mõ, mũ len).
- Chủ dự án chọn bằng tai: bạ "bạ. bạ.", ế "ế, ế, ế.", tế "tế, tế." −40%, hờ "hờ. hờ.", tổ dế ghép tổ + dế, nụ "nụ hoa.", bé bá cổ bà "bé, bá cổ bà.".
- Code: `keep_first` (9a1171f), `join` + ghép mượt `audio_join.py` (929d023, f6c01f1), không cắt lấn tiếng sau (fe46139).
- Trang nghe thử (thư mục bị git bỏ qua, chỉ trên máy này): `.superpowers/nghe-thu/`, `.superpowers/nghe-thu-2/`.

## 1. Đang ở đâu (tập 2)

| Phần | Trạng thái |
|---|---|
| Hai quyển trong một app | Xong: `content/books.json`, `index.json` có `books`, `part`, `label`, `week`; danh sách bài ba phần, nhóm tuần; công tắc "Mở mọi bài" theo từng bé ở màn Phụ huynh; Phụ lục của tập 1 dùng cho tập 2 |
| Nội dung | Đủ **91 mục**, `page_verified`: bài vần 81–125, Tập đọc 126–171 (tuần 27–33). Tr.138 "Trả lời câu đố" không thành bài, đáp án nằm trong các trang Câu đố |
| Quy tắc đánh vần mới | iê/yê/uô/ươ là một mảnh đọc theo tr.121 ("iê – nờ – iên"); âm đệm theo sơ đồ bảng ôn tr.72, 82 ("oa – nờ – oan", "uyê – nờ – uyên"); "oo" một mảnh. Mọi chuỗi gắn "quy tắc tạm" để duyệt |
| Màn mới | tên bài, câu hỏi trả lời miệng, đọc cả bài, tìm tiếng theo câu hỏi, học thuộc lòng (ẩn bớt 3 mức), điền chữ/dấu, đoán đáp án câu đố; bảng vần ít dùng có cột câu |
| Âm thanh | Đủ (9/11, 8a6a7b4); đang sửa phát âm theo mục 0 |
| Tranh | Đủ 155/155 (8c43d12); bản đồ bài 97 vẫn `scan_tam` |
| Gói media | Gói 2026-11-09 (746792b); sẽ đóng gói lại chung hai lớp (session L2) |

## 2. Việc của chủ dự án

- Nghe và chấm trong tool duyệt các mã ghi "chờ nghe xác nhận" và các mã đợt rà soát 09/11.
- Duyệt các chỗ "App khác sách": tranh thay người thật (bài 107, 115, 124, 130, 160, 168), đáp án điền chỗ trống do app soạn (trang chính tả), câu hỏi hiểu bài trả lời miệng.
- Khi muốn chạy trọn: nói "test all".

## 3. Commit danh mục

Chỉ đưa dòng mới và trường `bai` (dựng bản index từ HEAD cộng dòng mới, `git update-index --cacheinfo`), không lẫn kết quả duyệt của chủ dự án. Commit theo đường dẫn file (`git commit -- <file>`) để không kéo theo phần người khác đã stage.

## 4. Bài học

- Bash trên máy này làm hỏng dấu gạch ngược trong heredoc Python: sửa file có dấu gạch ngược bằng công cụ Edit.
- `edge-tts` hay trả "No audio was received"; chỉ chạy 1 tiến trình, có lượt bù (xem `QUY-TRINH-LAM-VIEC.md` mục 6, 12).
- Media Foundation: giải mã MP3 đặt tần số mẫu thì bị từ chối — để mặc định rồi trộn kênh trong Python (`audio_join.py`).
- Bộ tách tiếng bỏ qua ngoặc đơn và chữ số; "oo" có mã riêng (`van_ooong`).
- `validate` bắt buộc Phần 2 có 6–10 lượt cho mọi bài, kể cả bài tập đọc.
