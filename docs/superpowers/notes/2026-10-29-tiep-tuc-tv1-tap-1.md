# Ghi chú tiếp tục — TV1 Tập 1 (cập nhật 29/10/2026, tối)

Đọc file này trước khi làm tiếp. Kế hoạch gốc: [2026-10-29-hoan-thanh-tv1-tap-1.md](../plans/2026-10-29-hoan-thanh-tv1-tap-1.md); giọng đọc: mục 17 của [bản thiết kế](../specs/2026-10-28-app-tap-doc-mvp-design.md).

## 1. Đang ở đâu

| Phần | Trạng thái |
|---|---|
| Đợt 1 (bài 1–41) | Đã phát hành: `fc4510c` |
| Đợt 2 (bài 42–64) | Xong nội dung, 154 tranh, giọng HoaiMy cho 1.317 mã, công cụ duyệt. **Chờ chủ dự án thử app rồi nói "phát hành"** |
| Đợt 3 (bài 65–80) | Xong code, nội dung 16 bài, 585 âm thanh, **39/45 tranh**. Còn 6 tranh (mục 2) |
| Review code | 8 lỗi đã sửa ở `cc172f6` (test viết trước, đỏ rồi xanh) |
| Test | Python 631 đạt. Unity: chạy riêng các màn mới đạt (31/31); **chưa chạy trọn 80 bài** |

Âm thanh và tranh đều ở trạng thái `cho_duyet` (tạo theo mặc định, chủ dự án duyệt sau).

## 1b. ĐANG LÀM DỞ — ghi chú cho phụ huynh (dừng theo yêu cầu, 30/10/2026)

**Chủ dự án đã chốt:**
- Bài học giữ đúng cách dạy của sách: khi đánh vần đọc theo mục Chú ý tr.122 (k "ca", q "cu", gh "gờ kép", ngh "ngờ kép", gi "di", i "i ngắn", y "i dài"). Không đổi sang âm ở Phụ lục.
- Bài nào có ghi chú thì app hiện ghi chú cho người dùng, gồm cả 3 loại:
  1. `sach`: chú thích sách in trên trang (dấu \*, ngoặc đơn), ví dụ bài 42 ngan/vịt xiêm, 60 heo nái, 66 cá lóc, 68 vần ec;
  2. `ten_doc`: tên đọc riêng theo tr.122, **công cụ tự sinh** cho bài dạy chữ đó (2, 5, 10, 14, 20, 25, 26, 28, 29, 35);
  3. `khac_sach`: chỗ app khác sách (bài 1, 3, 6, 18, 27, 38, 42, 43, 44, 49, 53, 66, 68, 76, 80).
- Thêm mục "Chú ý và Phụ lục" ở màn Phụ huynh (chép đúng tr.120–122, kèm danh sách điểm app khác sách nói chung); tô phụ âm đầu bài 80; số cột (1)–(7) ở bài 79.

**Đã xong, commit `02d86af`:**
- Công cụ: `tools/tapdoc/lesson_notes.py`, trường `notes` khi dựng bài, tuỳ chọn `"colour": "onset"` cho bước reading.
- Dữ liệu: ghi chú trong `content/src` (15 bài), dữ liệu Phụ lục `unity/TapDoc/Assets/Content/Resources/appendix/tv1_t1.json`, 80 bài đã dựng lại.
- Test Python (Claude viết) đều xanh: 640+ test.

**Chưa commit (cố ý, vì phần giao diện chưa có nên chưa biên dịch được):**
- Test Unity do Claude viết: `Tests/EditMode/NotesDataTests.cs`, `Tests/PlayMode/LessonNotesTests.cs`, cùng test thêm trong `ParentScreenTests.cs`, `ItemsViewTests.cs`, `RimeGridViewTests.cs`.
- Phần kết quả Đợt 2 trong mục 15 của bản thiết kế.

**Việc tiếp theo:**
1. Giao Codex phần giao diện Unity: yêu cầu đã viết sẵn ở `~/.claude/delegate/orders/parent-notes-ui.md`. Chạy `node ~/.claude/delegate/bin/delegate.mjs start --task parent-notes-ui --worker codex --order ~/.claude/delegate/orders/parent-notes-ui.md --repo /c/Source/AURA/APP_TIEU_HOC --write`, **sau khi** commit hoặc chép các file test Unity ở trên vào worktree của Codex. Codex không được sửa test.
2. Review kỹ code Codex (tránh code rác, hard-code), chạy Unity EditMode và PlayMode, sửa nếu cần, rồi commit.
3. Chú thích sách (loại 1): một trợ lý đã được giao rà đủ 80 trang bài tìm mọi chú thích có dấu \* hoặc ngoặc đơn. Nếu kết quả chưa được ghi ở đây thì rà lại: ảnh `sach-giao-khoa-viet-nam/Tiếng Việt 1 (tập 1 1990)/004…061`. Thêm chú thích còn thiếu vào `notes` (kind `sach`) của bài tương ứng và vào test `LessonNotesContentTest`.

## 2. Việc khi ChatGPT mở lại lượt tạo ảnh (sau 14:30 ngày 30/10/2026)

Ngày 29/10 gói Plus báo hết lượt tạo ảnh sau 39 tranh. Còn 6 tranh `chua_co`:

| Mã | Vẽ |
|---|---|
| `img_b75_saams_chowps` | Đám mây đen có tia chớp sáng loé, mưa gió làm cành cây nghiêng |
| `img_b77_nhipj_caauf` | Cây cầu sắt nhiều nhịp vòm bắc qua sông |
| `img_b78_xe_qua_caauf` | Xe cộ đi qua cầu: xe buýt, xe tải, xe máy, xe đạp, người gánh hàng |
| `img_b80_con_lownj` | Con lợn mũm mĩm, má to, mắt híp, nằm thở trên ổ rơm |
| `img_b80_con_meof` | Con mèo mướp ngồi liếm chân |
| `img_b80_con_gaf` | Con gà trống mào đỏ đứng gáy |

Lời yêu cầu đầy đủ nằm trong `content/requests/images_tv1_t1_b75.md`, `…b77.md`, `…b78.md`, `…b80.md` (tạo lại bằng `cd tools && python -m tapdoc requests` nếu đã bị xoá).

Các bước:
1. Dùng **Edge trên máy này** (Claude in Chrome, thiết bị `407cb8a9-…`, kiểm tra trình duyệt là "Microsoft Edge"), dự án ChatGPT **Kiet_1**. Có thể gửi tiếp trong 3 cuộc trò chuyện cũ ("Tạo tranh minh họa", "Tạo tranh tắc kè", "Tạo tranh củ lạc") để giữ cùng phong cách.
2. Kịch bản dán/thu/tải: `.superpowers/scripts/chatgpt_tranh.js` (đọc chú thích đầu file: `RUN()`, `HARVEST()`, `DOWNLOAD()`).
   - Bài học 29/10: phải chờ nút Gửi xuất hiện rồi mới bấm; không xoá khung soạn khi nó đang trống; trang chỉ dựng phần đang thấy nên phải cuộn lên đầu khi thu tranh.
3. Chủ dự án đã đồng ý tải lô 45 tranh này (29/10). Tải về Downloads, chuyển vào thư mục tạm riêng.
4. Soát bằng bảng xem nhanh: `.superpowers/scripts/sheet.ps1` (đúng mã, đúng nội dung, không chữ, không khung).
5. Nhập: `cd tools && python -m tapdoc import-image <file.png> <mã>` cho từng tranh, rồi `python -m tapdoc validate` phải ra `OK` (không còn `--allow-missing`).

## 3. Sau khi đủ 45 tranh

1. Chạy trọn Unity: `python tools/run_unity_tests.py editmode` và `python tools/run_unity_tests.py playmode` (MvpEndToEndTests đi hết 80 bài ở 2 khung hình, bố cục, bảng nhóm vần bài 79, câu đố bài 80).
2. Commit các file `.meta` Unity tạo cho tranh mới.
3. Điền số liệu test vào mục 15 của bản thiết kế (phần "Đợt 2" đã viết sẵn, **chưa commit**, dòng Unity để trống); viết phần "Đợt 3" và nghiệm thu cả quyển (mục 15, 16).
4. Review cả kế hoạch bằng một người review mới (1 subagent), sửa phát hiện quan trọng (test trước).
5. Dọn worktree Codex/Antigravity còn lại (`node ~/.claude/delegate/bin/delegate.mjs status`).

## 4. Phát hành

Lúc 17:42 ngày 29/10, chủ dự án tự push `main` lên GitHub tới `d5d8488` (22 commit lẻ). Sau đó chủ dự án chọn **giữ nguyên lịch sử**:
- không gộp commit theo đợt nữa, không ghi đè lịch sử trên GitHub (không force push);
- mỗi việc một commit rõ ràng; push bình thường khi chủ dự án phát hành hoặc yêu cầu.

Chủ dự án push tiếp lúc 18:05 tới `a277098`. Xem phần chưa push bằng `git log origin/main..main`.

## 5. Việc của chủ dự án (làm lúc nào cũng được)

- Duyệt âm thanh: bấm đúp `MoCongCuDuyet.cmd`, nghe từng mã (1.902 mã `cho_duyet`), sửa cách đọc rồi **Tạo lại** mới nghe được bản mới.
- Duyệt tranh: 193 tranh `cho_duyet` (thêm 6 khi vẽ xong). Lưu ý: `img_b72_muwts_teets` (gói mứt Tết) trông giống cái kẹo.
- Xem các mục "cần duyệt" trong từng bài (`review.can_duyet`), nhất là tranh vẽ thay người thật (bài 68, 76).
- Thử app bài 42–64 (và 65–80 khi đủ tranh), rồi báo "phát hành".

## 6. Quy tắc làm việc đã thống nhất

- Chỉ branch `main`; không build bản thử, chỉ commit.
- Claude viết và review mọi test; Codex/Antigravity chỉ viết code cho test của Claude chạy xanh. Review kỹ, tránh code rác và hard-code.
- Trình duyệt: chỉ Edge trên máy này. Hỏi trước khi tải file (một lần cho mỗi lô).
- Âm thanh tạo theo mặc định (HoaiMy nữ); chủ dự án duyệt sau.
- Trả lời bằng tiếng Việt.
