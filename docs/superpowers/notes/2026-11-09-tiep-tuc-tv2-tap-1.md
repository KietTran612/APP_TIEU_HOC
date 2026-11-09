# Ghi chú tiếp tục — TV2 tập một (lớp 2), 9/11/2026

Đọc file này trước khi làm tiếp lớp 2. Thiết kế: [2026-11-09-tv2-tap-1-design.md](../specs/2026-11-09-tv2-tap-1-design.md) (mục 15 Kết quả); kế hoạch: [2026-11-09-tv2-tap-1.md](../plans/2026-11-09-tv2-tap-1.md).

## 1. Đang ở đâu

| Phần | Trạng thái |
|---|---|
| Nội dung | Đủ 133 mục (172–304) `page_verified`, `validate --allow-missing` OK |
| Công cụ, Unity | Xong; test liên quan đạt, smoke 133 mục đạt |
| Tranh | Đủ 57 tranh + `img_chung_giai_nghia` đã nhập (447cf3e, d239be1, d7bbff2, 957e711), `cho_duyet`; validate không còn lỗi tranh. Ghi chú duyệt: b190 cô bé mặc áo hoa (không phải áo bông), b268 chọn bản có thuyền chở cá, b274 hai cô gái không đội nón |
| Tranh động | 27 clip mục 172–230 (28fe7be) + 29 clip mục 235–298 (a0662f8), chờ duyệt; còn thiếu 1 clip img_b299_dduwowngf_daay_ddieenj (Flow hết credit 9/11) — đóng gói media sau khi có clip này và đủ âm thanh |
| Âm thanh | Đang tạo HoaiMy, 1 tiến trình, mỗi mã ≤ 90 giây, tiếng lẻ `keep_first` |
| Gói media | Chưa đóng (chờ tranh và âm thanh) |

## 2. Làm tiếp (Claude)

1. **Âm thanh:** chạy lại cho mã lớp 2 còn `chua_co` (1 tiến trình), mỗi mã một lệnh để giới hạn 90 giây:
   ```
   cd tools
   python -m tapdoc tts --tieng-keep-first --ma <mã>
   ```
   Lượt bù đến khi hết `chua_co`. Rồi `python -m tapdoc pitch --bai tv2_t1_bNNN` cho mọi câu, từ có hỏi/ngã; mã không đạt sửa theo **quyết định chủ dự án 9/11** (đọc đúng trên hết, ngữ điệu tự nhiên càng tốt), theo thứ tự: (1) đọc nguyên câu nếu đo đúng thanh → (2) đọc chậm, ngắt nhẹ → (3) ghép từ các tiếng đã đạt/đo đúng bằng `overrides[id].join` (929d023 của L1). Khi ghép: nghỉ ngắn đều 0,05–0,12 s, ngắt nhẹ ở dấu phẩy, âm lượng đều, cắt lặng đầu/cuối mỗi tiếng, ghi rõ ghép từ mã nào. Tham số ghép dùng chung với L1 (local_1af66fbb, đã hỏi 9/11 về `join_gap`/cân âm lượng). Báo chủ dự án các mã vẫn không đạt.
2. **Tranh:** khi session vẽ tranh báo đã nhập, chạy `python -m tapdoc validate` (không `--allow-missing`).
3. **Đóng gói** (đóng Unity trước): `python tools/run_unity_media.py pack`, commit `content/manifests/media_lock.json` (blob từ HEAD nếu file có chỉnh sửa của chủ dự án), báo chủ dự án tải hai file trong `dist/` lên Drive.
4. **Commit danh mục:** chỉ dòng lớp 2 (blob từ HEAD + dòng có `bai` toàn `tv2_t1_*`, thêm mã bài lớp 2 vào dòng cũ), `git update-index --cacheinfo`.

## 3. Việc của chủ dự án

- Thử app: danh sách bài → thẻ "Lớp 2" ở mép dưới; hoặc Phụ huynh → "Mở mọi bài".
- Duyệt các chỗ `can_duyet`: đáp án điền chỗ trống, chọn dòng, ghép chữ do app soạn; lời dẫn tranh; tranh thay ảnh chụp Bác Hồ (mục 172).
- Quyết định: điền đoạn văn hiện đi từng câu với 3 thẻ mỗi ô (sách cho chọn trong cả danh sách từ).

## 4. Bài học

- Smoke test (`Grade2LessonSmokeTests`) bắt được thẻ nhỏ hơn 160 và chữ tràn mà test từng màn không bắt: chạy nó sau mỗi lần thêm dạng bài.
- Màn đọc từng câu chứa tối đa khoảng 16 tiếng; màn quy tắc tối đa 3 dòng; màn điền chữ (`fill_blank`) cụm ≤ khoảng 18 kí tự.
- Mã âm thanh từ (`tu_*`) dùng chung với lớp 1: cùng chữ mà lời đọc khác (ví dụ "Sa Pa" / "sa-pa") thì `build` báo lỗi danh mục.
- `python -m tapdoc requests` xoá mọi `content/requests/images_*.md` không còn khớp bài, kể cả file tổng `images_tv2_t1_dot_N.md`: file tổng chỉ để gửi một lần, session vẽ tranh làm theo phiếu từng bài `images_tv2_t1_bNNN.md`.
