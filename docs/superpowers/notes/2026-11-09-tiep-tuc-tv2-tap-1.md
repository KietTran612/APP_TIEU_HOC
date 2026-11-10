# Ghi chú tiếp tục — TV2 tập một (lớp 2), 9–10/11/2026

Đọc file này trước khi làm tiếp lớp 2. Thiết kế: [2026-11-09-tv2-tap-1-design.md](../specs/2026-11-09-tv2-tap-1-design.md) (mục 15 Kết quả); kế hoạch: [2026-11-09-tv2-tap-1.md](../plans/2026-11-09-tv2-tap-1.md).

## 1. Đang ở đâu

| Phần | Trạng thái |
|---|---|
| Nội dung | Đủ 133 mục (172–304) `page_verified`, `validate --allow-missing` OK |
| Công cụ, Unity | Xong; test liên quan đạt, smoke 133 mục đạt |
| Tranh | Đủ 57 tranh + `img_chung_giai_nghia` đã nhập (447cf3e, d239be1, d7bbff2, 957e711), `cho_duyet`; validate không còn lỗi tranh. Ghi chú duyệt: b190 cô bé mặc áo hoa (không phải áo bông), b268 chọn bản có thuyền chở cá, b274 hai cô gái không đội nón |
| Tranh động | 27 clip mục 172–230 (28fe7be) + 29 clip mục 235–298 (a0662f8), chờ duyệt; còn thiếu 1 clip img_b299_dduwowngf_daay_ddieenj (Flow hết credit 9/11) — đóng gói media sau khi có clip này và đủ âm thanh |
| Âm thanh | **Dừng 10/11 09:10 (chủ dự án chuyển máy).** Mã chỉ thuộc lớp 2: 3334; đã có file 1623 (`cho_duyet`), còn **1711 `chua_co`** (886 từ, 343 tiếng, 326 câu, 148 câu hỏi, 15 hướng dẫn) + 7 mã cần tạo lại vì đổi cách đọc → lượt tới chọn 1718 mã. Lượt 10/11 chỉ kịp 8 trong 1726 mã. Dòng danh mục và 140 cách đọc riêng của lớp 2 đã commit; **file mp3 chỉ có trên máy cũ** (`unity/TapDoc/Assets/Content/Resources/audio/`) — đi qua gói media root đóng |
| Gói media | Chưa đóng (chờ tranh và âm thanh) |

## 2. Làm tiếp (Claude)

1. **Âm thanh trên máy mới** (sau khi `run_unity_media.py unpack` gói root đóng, để có các mp3 đã tạo):
   ```
   python tools/lop2/tieng_doc_lop2.py --ghi      # cách đọc tiếng lẻ: nặng "X. X.", ê sắc "X, X, X.", còn lại "X, X."
   python tools/lop2/tts_lop2.py 4 172 304 --giu-may-thuc
   ```
   `tts_lop2.py` chỉ chọn mã **mọi bài đều là `tv2_t1_*`** (mã dùng chung với lớp 1 để L1 làm), chưa `dat`, còn `chua_co` hoặc khác cấu hình; 1 tiến trình, mỗi mã một lệnh `python -m tapdoc tts --tieng-keep-first --ma <mã>` giới hạn 90 giây; lượt 2–4 là lượt bù. Log `.superpowers/tts_lop2.log`. edge-tts trả rỗng khoảng 1 mã/phút, hôm 9/11 tạo được khoảng 4 mã/phút; 1718 mã cần chừng 7–8 giờ. Nếu L1 chạy tts song song mà lỗi tăng hẳn thì nhắn L1 chạy lần lượt.
2. **Đo cao độ** sau khi hết `chua_co`: `cd tools && python -m tapdoc pitch --bai tv2_t1_bNNN` cho từng bài 172–304 (tiếng lẻ, từ, câu có hỏi/ngã). Mã không đạt sửa theo `QUY-TRINH-LAM-VIEC.md` mục 6, **quyết định chủ dự án 9/11** (đọc đúng trên hết, ngữ điệu tự nhiên càng tốt): (1) đọc nguyên câu nếu đo đúng → (2) đọc chậm khoảng −20% hoặc ngắt nhẹ, không đổi chữ → (3) ghép mượt `overrides[mã] = {"join": ["tieng_a", "tieng_b", ",", "tieng_c"], "join_gap": 0.08}` (f6c01f1 của L1; `","` = nghỉ 0,25 s). Mỗi mã đổi về `cho_duyet` + ghi chú cách làm (giữ ghi chú cũ). Tạo lại một tiếng đã dùng để ghép thì tạo lại cả mã ghép. Báo root các mã vẫn không đạt.
   **Làm tới cuối, không chờ duyệt giữa chừng** (chủ dự án 9/11); chủ dự án duyệt sau bằng tool.
3. **Commit âm thanh:** `python tools/lop2/stage_lop2.py content/manifests/audio_manifest.json content/tts/settings.json` (chỉ dòng/cách đọc của mã lớp 2, giữ nguyên chỉnh sửa duyệt của chủ dự án), xem `git diff --cached --stat`, commit.
4. **Đóng gói chung hai lớp** — root làm (10/11): chờ clip `img_b299_dduwowngf_daay_ddieenj` (session tranh động) và L1 báo xong sửa âm thanh lớp 1; đóng Unity, `python tools/run_unity_media.py pack`, commit `media_lock.json`.
5. **Kết thúc:** `cd tools && python -m tapdoc validate` (không `--allow-missing`) phải OK; cập nhật ghi chú này, `QUY-TRINH-LAM-VIEC.md` mục 12 nếu có cách giải mới; báo root.

Script của lớp 2 nằm ở `tools/lop2/` (xem `tools/lop2/README.md`; `soan/` là script đã soạn nguồn bài, chỉ để tham khảo).

**Ngoài git, chỉ có trên máy cũ:** mp3 lớp 2 (đi qua gói media); `content/tts/marks/` (mốc từng tiếng — `pitch` cần, mất thì tạo lại mã đó sẽ sinh lại); `content/requests/images_tv2_t1_*.md` (phiếu tranh, tranh đã nhập đủ nên không cần nữa); log cũ `.superpowers/` và scratchpad của session.

## 3. Việc của chủ dự án

- Thử app: danh sách bài → thẻ "Lớp 2" ở mép dưới; hoặc Phụ huynh → "Mở mọi bài".
- Duyệt các chỗ `can_duyet`: đáp án điền chỗ trống, chọn dòng, ghép chữ do app soạn; lời dẫn tranh; tranh thay ảnh chụp Bác Hồ (mục 172).
- Quyết định: điền đoạn văn hiện đi từng câu với 3 thẻ mỗi ô (sách cho chọn trong cả danh sách từ).

## 4. Bài học

- Smoke test (`Grade2LessonSmokeTests`) bắt được thẻ nhỏ hơn 160 và chữ tràn mà test từng màn không bắt: chạy nó sau mỗi lần thêm dạng bài.
- Màn đọc từng câu chứa tối đa khoảng 16 tiếng; màn quy tắc tối đa 3 dòng; màn điền chữ (`fill_blank`) cụm ≤ khoảng 18 kí tự.
- Mã âm thanh từ (`tu_*`) dùng chung với lớp 1: cùng chữ mà lời đọc khác (ví dụ "Sa Pa" / "sa-pa") thì `build` báo lỗi danh mục.
- `python -m tapdoc requests` xoá mọi `content/requests/images_*.md` không còn khớp bài, kể cả file tổng `images_tv2_t1_dot_N.md`: file tổng chỉ để gửi một lần, session vẽ tranh làm theo phiếu từng bài `images_tv2_t1_bNNN.md`.
