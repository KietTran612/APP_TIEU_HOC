# Ghi chú tiếp tục — Giao diện, hiệu ứng, Sổ bé ngoan (30/10/2026)

Bản thiết kế: [2026-10-30-ui-hieu-ung-design.md](../specs/2026-10-30-ui-hieu-ung-design.md) · Kế hoạch: [2026-10-30-ui-hieu-ung.md](../plans/2026-10-30-ui-hieu-ung.md) · Sổ tiến độ (không trong git): `.superpowers/sdd/2026-10-30-ui-hieu-ung/progress.md`.

## Đã xong (commit `8da7285` … `82e05bb` trên `main`, chưa push)

| Task | Nội dung |
|---|---|
| 1 | Lệnh `ui-icons`: 12 biểu tượng, hoa bé ngoan tạm, gà con (chép hình đại diện 4); `SYSTEM_SFX`; `validate` chặn tiếng động lẫn với âm thanh phát âm |
| 2 | `Palette`, khung viền mực bo góc, bóng gạch chéo, nút biểu tượng, thẻ to; `AssetCatalog.Sfx` |
| 3 | `Motion` (có `PageTurn`), `Pulse`, `TapFeedback` |
| 4 | `SfxPlayer` kênh riêng, công tắc `SfxEnabled` lưu trong tiến độ, `onGap` của chuỗi đọc; lệnh `sfx-default` |
| 5–6 | Màn học: nút biểu tượng, chấm tiến độ, gà con, chuyển bước lật trang; hiệu ứng đúng/sai/gợi ý/nhập thẻ/kéo thả |
| 7–10 | Sổ bé ngoan (mỗi trang một bài, 3 hoa), cảnh hoa bay khi học xong bài, danh sách bài có hoa |
| 11 | Màn chọn bé, màn Phụ huynh có công tắc tiếng động |
| Review | Review độc lập toàn bộ; đã sửa lật trang lệch chỗ, bước cũ chen lời đọc, tiếng chạm đè giọng đọc, thẻ lệch khi chạm dồn (`ae22591`) |
| 12 | Tiếng động CC0 chủ dự án nghe chọn; ghi công ở `docs/credits-am-thanh.md` |

## Còn lại

1. **Test all** khi chủ dự án yêu cầu (quy tắc: chỉ chạy test của phần đang làm; bộ đầy đủ chỉ khi chủ dự án nói "test all"):
   - `python tools/run_unity_tests.py editmode` và `playmode`.
   - Lần chạy đầy đủ gần nhất (sau Task 3) chỉ hỏng 8 test do 6 tranh bài 75–80 chưa vẽ (có từ trước). Từ Task 5 trở đi chưa chạy lại bộ đầy đủ.
2. **Hình chính thức** (Task 13): đã vẽ bằng ChatGPT Kiet_1 ngày 30/10 (cuộc trò chuyện "Tạo tranh hoa bé ngoan") và nhập cả 14 hình (hoa, gà con, 12 biểu tượng), trạng thái `cho_duyet`. Muốn vẽ lại hình nào: vẽ, hỏi chủ dự án trước khi tải, `python -m tapdoc import-image <file> <mã>`. **Không chạy `python -m tapdoc ui-icons --force`** (sẽ ghi đè biểu tượng chính thức bằng hình mặc định).
3. **Tiếng chạm** `sfx_cham` vẫn là tiếng mặc định tự tạo (chủ dự án chọn giữ).
4. **Lỗi nhỏ từ review:** đã sửa ở `ffe8e37` (nhún trả đúng cỡ, ô hoa giữ viền cam, hình đại diện giữ phóng to, tiếng bụp khi thả đúng chỗ, lớp đánh vần của từ ứng dụng có hiệu ứng, bóng gạch chéo không dùng Mask, màu về bảng màu). Hai điểm không tái hiện được thành lỗi (gà con khen hai lần, con dấu khi bỏ qua cảnh) giữ nguyên. Màu dự phòng của hình đại diện (khi thiếu file) vẫn là danh sách riêng trong `ProfileScreen`.
5. **Chủ dự án duyệt:** 14 hình giao diện (`cho_duyet`), 6 tiếng động (đã nghe chọn).
