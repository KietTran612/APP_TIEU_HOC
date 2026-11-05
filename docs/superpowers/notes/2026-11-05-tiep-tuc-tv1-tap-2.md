# Ghi chú tiếp tục — TV1 Tập 2 (cập nhật 5/11/2026)

Đọc file này trước khi làm tiếp tập 2. Thiết kế: [2026-11-05-tv1-tap-2-design.md](../specs/2026-11-05-tv1-tap-2-design.md); kế hoạch: [2026-11-05-tv1-tap-2.md](../plans/2026-11-05-tv1-tap-2.md).

## 1. Đang ở đâu

| Phần | Trạng thái |
|---|---|
| Hai quyển trong một app | Xong: `content/books.json`, `index.json` có `books`, `part`, `label`, `week`; danh sách bài ba phần, nhóm tuần; công tắc "Mở mọi bài" theo từng bé ở màn Phụ huynh; Phụ lục của tập 1 dùng cho tập 2 |
| Nội dung | Đủ **91 mục**, `page_verified`: bài vần 81–125, Tập đọc 126–171 (tuần 27–33). Tr.138 "Trả lời câu đố" không thành bài, đáp án nằm trong các trang Câu đố |
| Quy tắc đánh vần mới | iê/yê/uô/ươ là một mảnh đọc theo tr.121 ("iê – nờ – iên"); âm đệm theo sơ đồ bảng ôn tr.72, 82 ("oa – nờ – oan", "uyê – nờ – uyên"); "oo" một mảnh. Mọi chuỗi gắn "quy tắc tạm" để duyệt |
| Màn mới | tên bài, câu hỏi trả lời miệng, đọc cả bài, tìm tiếng theo câu hỏi, học thuộc lòng (ẩn bớt 3 mức), điền chữ/dấu, đoán đáp án câu đố; bảng vần ít dùng có cột câu |
| Âm thanh | Đang tạo HoaiMy cho khoảng 2.700 mã mới (dịch vụ edge-tts chập chờn, rất chậm). Chạy lại: xem mục 3 |
| Tranh | 155 mã tranh bài + `img_chung_cau_hoi` ở `chua_co`, đã bàn giao cho session gốc (phiếu vẽ `content/requests/images_tv1_t2_bNN.md`) |
| Gói media | **Chưa đóng gói** (chờ đủ âm thanh và tranh) |

## 2. Việc của chủ dự án

- Thử app: màn Phụ huynh → bật "Mở mọi bài" cho một bé → vào phần "Vần" (từ bài 81) và "Tập đọc".
- Nghe các chuỗi đánh vần gắn "quy tắc tạm" (công cụ duyệt, "Nghe theo bài"), nhất là bài 92 (iê), 100 (uô), 104 (ươ), 109–110 (âm đệm), 121 (oo).
- Duyệt các chỗ "App khác sách": tranh thay người thật (bài 107, 115, 124, 130, 160, 168), đáp án điền chỗ trống do app soạn (trang chính tả), câu hỏi hiểu bài trả lời miệng.
- Khi muốn chạy trọn: nói "test all".

## 3. Làm tiếp (Claude)

1. **Âm thanh:** tìm các mã tập 2 còn `chua_co` rồi chạy `tts` (có thể chia 3 tiến trình chạy song song, mỗi tiến trình một phần danh sách mã):
   ```
   cd tools
   python -m tapdoc tts --ma <các mã>
   ```
   Sau đó chạy `python -m tapdoc validate` (không `--allow-missing`) khi đã có đủ tranh.
2. **Tranh:** session gốc nhập tranh bằng `import-image`; nhập xong thì chạy `validate` lại.
3. **Đóng gói** khi đủ media: `python tools/run_unity_media.py pack`, commit `content/manifests/media_lock.json`, báo chủ dự án đưa gói lên Drive.
4. **Commit danh mục:** chỉ đưa dòng mới và trường `bai` (cách làm: dựng bản index từ HEAD cộng dòng mới, `git update-index --cacheinfo`), không lẫn kết quả duyệt của chủ dự án.

## 4. Bài học khi làm tập 2

- Bash trên máy này làm hỏng dấu gạch ngược trong heredoc Python: sửa file có dấu gạch ngược (C#, regex) bằng công cụ Edit, không dùng `python - <<EOF`.
- `edge-tts` lúc này hay trả "No audio was received" với nhiều câu; công cụ thử lại 4 lần mỗi mã nên chạy chậm (khoảng 3 file/phút mỗi tiến trình).
- Bộ tách tiếng nay bỏ qua ngoặc đơn và chữ số; "oo" có mã riêng (`van_ooong`), không trùng "ô".
- `validate` bắt buộc Phần 2 có 6–10 lượt cho mọi bài, kể cả bài tập đọc.
