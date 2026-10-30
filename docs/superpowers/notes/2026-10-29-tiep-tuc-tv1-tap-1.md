# Ghi chú tiếp tục — TV1 Tập 1 (cập nhật 30/10/2026, chiều)

Đọc file này trước khi làm tiếp. Kế hoạch gốc: [2026-10-29-hoan-thanh-tv1-tap-1.md](../plans/2026-10-29-hoan-thanh-tv1-tap-1.md); giọng đọc: mục 17 của [bản thiết kế](../specs/2026-10-28-app-tap-doc-mvp-design.md).

## 1. Đang ở đâu

| Phần | Trạng thái |
|---|---|
| Đợt 1 (bài 1–41) | Đã phát hành: `fc4510c` |
| Đợt 2 (bài 42–64) | Xong nội dung, 154 tranh, giọng HoaiMy cho 1.317 mã, công cụ duyệt. **Chờ chủ dự án thử app rồi nói "phát hành"** |
| Đợt 3 (bài 65–80) | Xong code, nội dung 16 bài, 585 âm thanh, đủ 45 tranh (6 tranh cuối vẽ chiều 30/10, `7808597`). **Chờ chủ dự án thử app rồi nói "phát hành"** |
| Review code | 8 lỗi đã sửa ở `cc172f6` (test viết trước, đỏ rồi xanh) |
| Test | Python 653 đạt. EditMode 105/105 (30/10 chiều, gồm kiểm tra đủ tài nguyên). PlayMode trọn 80 bài chạy lần cuối sáng 30/10: 264/276, lỗi chỉ do thiếu 6 tranh nay đã có; chạy lại khi chủ dự án yêu cầu "test all" |

Giao diện và hiệu ứng (30/10): đang thảo luận với chủ dự án ở một session riêng ("Thảo luận UI và hiệu ứng cho app tập đọc"); bản thiết kế sẽ lưu ở `docs/superpowers/specs/…-ui-hieu-ung-design.md`.

Âm thanh và tranh đều ở trạng thái `cho_duyet` (tạo theo mặc định, chủ dự án duyệt sau).

## 1b. XONG — ghi chú cho phụ huynh (30/10/2026)

**Chủ dự án đã chốt:**
- Bài học giữ đúng cách dạy của sách: khi đánh vần đọc theo mục Chú ý tr.122 (k "ca", q "cu", gh "gờ kép", ngh "ngờ kép", gi "di", i "i ngắn", y "i dài"). Không đổi sang âm ở Phụ lục.
- Bài nào có ghi chú thì app hiện nút "Ghi chú" (góc trên phải), gồm 3 loại:
  1. `sach` (Sách ghi): chú thích, lời dặn in trên trang — rà đủ 80 trang, chỉ bài 11, 27, 42, 60, 66, 68. Lời dặn "theo mẫu" bài 39, 40, 80 và khung luật chính tả bài 40 là nội dung bài. Câu "Các bài ôn sau cũng vậy" (bài 11) chỉ hiện ở bài 11, đúng chỗ sách in;
  2. `ten_doc` (Cách đọc theo sách): tên đọc riêng theo tr.122, **công cụ tự sinh** cho bài dạy chữ đó (2, 5, 10, 14, 20, 25, 26, 28, 29, 35);
  3. `khac_sach` (App khác sách): bài 1, 3, 6, 18, 27, 38, 42, 43, 44, 49, 53, 66, 68, 76, 80.
- Màn Phụ huynh có mục "Chú ý và Phụ lục" (tr.120–122 và các điểm app khác sách); bài 80 tô phụ âm đầu; bảng nhóm vần bài 79 có số cột (1)–(7).

**Commit:** `02d86af` (công cụ, dữ liệu), `e9f1f90` (sửa cắt MP3, âm "tô"), `74ce1ef` (giao diện Unity — Codex viết theo test của Claude, Claude review và sửa), `ac71105` (chú thích bài 11, 27), `6b64a77` (.meta 39 tranh bài 65–80).
- Phụ lục đặt tên theo mã sách: `Resources/appendix/tv1_t1_1990.json`; `index.json` có trường `book` cho từng bài.
- Test: Python 653 đạt. Unity EditMode 83/84, PlayMode 264/276 — mọi lỗi còn lại chỉ do thiếu 6 tranh (mục 2).

**Âm "tô" (`tieng_too`) — đã sửa:** FMOD của Unity không nhập được file vì khung MP3 đầu của file đã cắt mượn dữ liệu (bit reservoir) của khung đã bị bỏ. `trim_mp3` giờ lùi điểm bắt đầu tới khung không mượn dữ liệu. Review độc lập (30/10 chiều) chỉ ra 1.236 file khác cùng lỗi: đã tạo lại hết với đúng thông số cũ (`269ebde`, không đụng `content/tts/prev`), test `ShippedAudioTest` kiểm mọi file. Giọng đọc edge-tts chỉ có khung 0 là không mượn dữ liệu, nên bước cắt giờ giữ nguyên phần lặng đầu (khoảng 1–2 khung), chỉ cắt phần lặng cuối.

**Review độc lập phần ghi chú cho phụ huynh (30/10 chiều):** không có lỗi nghiêm trọng. Đã sửa: âm thanh (ở trên), mở khung Ghi chú thì dừng giọng đọc (`6e503b8`). **Chờ chủ dự án quyết:** nút "Ghi chú" đang nằm ngay màn bài của bé, chữ không có biểu tượng; bé chạm vào sẽ gặp trang chữ. Có thể giữ nguyên, hoặc chỉ hiện ghi chú sau khoá phụ huynh. Lỗi nhỏ để sau: nút Ghi chú sát dãy chấm tiến độ ở màn 4:3; nút Phụ lục im lặng khi thiếu dữ liệu và chỉ theo một quyển; tên âm và số trang trong `lesson_notes.py` ghi cứng (nên lấy từ dữ liệu Phụ lục); test mp3trim chưa có mẫu MPEG-1 và CRC; chưa có test khung ghi chú chặn chạm xuống bài; loại ghi chú lạ bị bỏ qua; lượt Phần 2 tự chuyển có thể đóng khung đang mở; màu nền khung trùng `Palette.Paper`.

## 2. XONG — 6 tranh còn thiếu (vẽ bằng ChatGPT chiều 30/10; giữ lại các bước để lần sau vẽ tranh mới)

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

1. **Chỉ khi chủ dự án yêu cầu "test all"** mới chạy trọn Unity PlayMode (`python tools/run_unity_tests.py playmode`, khoảng 25–30 phút, MvpEndToEndTests đi hết 80 bài ở 2 khung hình). Bình thường chỉ chạy test liên quan (Python, EditMode, hoặc PlayMode có `--filter`).
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
- Chỉ chạy test liên quan tới thay đổi (unit test, EditMode, PlayMode có `--filter`). Không chạy trọn PlayMode ("test all") khi chủ dự án chưa yêu cầu (30/10).
- Trình duyệt: chỉ Edge trên máy này. Hỏi trước khi tải file (một lần cho mỗi lô).
- Âm thanh tạo theo mặc định (HoaiMy nữ); chủ dự án duyệt sau.
- Trả lời bằng tiếng Việt.
