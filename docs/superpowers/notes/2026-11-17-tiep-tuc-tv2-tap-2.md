# Ghi chú tiếp tục — TV2 tập hai ("Bé tập đọc 4"), 17/11/2026

Đọc file này trước khi làm tiếp cuốn thứ tư. Thiết kế: [2026-11-17-tv2-tap-2-design.md](../specs/2026-11-17-tv2-tap-2-design.md) (mục 15 Kết quả); kế hoạch: [2026-11-17-tv2-tap-2.md](../plans/2026-11-17-tv2-tap-2.md). Session nội dung `[L2T2]`, root `local_0cefca18-12fb-4d82-a1d6-a65ff28a9bed`.

## 1. Đang ở đâu

| Phần | Trạng thái |
|---|---|
| Kiểm kê | Xong: bảng ảnh → trang (BOOK_CATALOG 4.4), 130 dòng CSV `page_verified` |
| Công cụ | Xong: f285c84 (`books.json`, tuần 1–35, chủ điểm), f95f92b (`--t2`, `xuat_wav_lop2.py`) |
| Nội dung | Xong: 130 mục 305–434 (e9f837c, 005b828, f9b4fd5, 391c59f), `validate --allow-missing` OK |
| Tranh | 41 tranh `chua_co`, danh sách đã gửi root (`content/requests/images_tv2_t2_dot_1..4.md`, ngoài git). Bìa `img_bia_tv2_t2_2002` đã có (216e923, `[Chung]` UI) |
| Âm thanh | **Chưa chạy.** Khoảng 3.150 mã chỉ của tập hai `chua_co`; chờ root cho lượt (một tiến trình cả máy) |
| Unity | **Chưa chạy.** `BookScreenTests`, `ParentScreenTests` (4 quyển), smoke `Grade2Tap2LessonSmokeTests` (4 đợt); chờ root cho lượt |

## 2. Làm tiếp

1. **Âm thanh** (chỉ khi root nhắn được chạy):
   ```
   python tools/lop2/tieng_doc_lop2.py --t2 --ghi
   python tools/lop2/tts_lop2.py 4 305 434 --t2 --giu-may-thuc
   ```
   Log `.superpowers/tts_lop2t2.log`. Xong thì đo: `python tools/lop2/do_cao_do_lop2.py --t2 --json <ra.json>`, rồi xuất WAV cho root theo đợt:
   ```
   python tools/lop2/xuat_wav_lop2.py --t2 305 338 --ra "<side-session-notes>/local_0cefca18-…/L2T2-dot1"
   ```
   (đợt 2: 339–370, đợt 3: 371–402, đợt 4: 403–434). Root nhận dạng; mã sai làm bản thử ngoài danh mục (chậm −20%, ngắt nhẹ, ghép tiếng đã đạt), xuất WAV, root nhận dạng lại, rồi mới cài; kiểm file cài trùng byte với bản thử (QUY-TRINH §6, §12). `sua_hoi_nga_lop2.py` chưa có `--t2` và đang có chỉnh sửa chưa commit của chủ dự án: không sửa, viết script riêng nếu cần.
2. **Commit âm thanh:** chỉ mục tạm dựng từ HEAD (`GIT_INDEX_FILE`, `git read-tree HEAD`), `python tools/lop2/stage_lop2.py --t2 content/manifests/audio_manifest.json content/tts/settings.json`, xem `git diff --cached --stat`, commit.
3. **Unity** (đóng Editor, báo root trước): `python tools/run_unity_tests.py playmode --filter BookScreenTests`, `--filter ParentScreenTests`, `--filter Grade2Tap2LessonSmokeTests`. Hỏng ở màn dùng chung thì báo root, không tự sửa.
4. Khi tranh về đủ: `python -m tapdoc validate` (không `--allow-missing`).

## 3. Soạn lại một tuần

`cd tools/lop2/soan_t2 && python wNN.py` ghi đè nguồn bài tuần đó, rồi `python trybuild.py <đầu> <cuối>`, `cd tools && python -m tapdoc build && python -m tapdoc validate --allow-missing`, `python tools/lop2/soan_t2/csv_verify.py`. File `.meta` của file bài mới phải tạo (GUID mới) trước khi commit. Commit nguồn bài, file bài, `index.json`, CSV và dòng danh mục qua chỉ mục tạm như mục 2.

## 4. Bài học

- Ảnh scan đầu sách bị xáo: luôn lấy ảnh theo `toc_t2.image_of(trang)`, không theo công thức.
- `l2lib.split_long` tách câu không có dấu phẩy ở giữa, có khi ngang hai câu thoại: ghi chỗ ngắt tay " | " trong `wNN.py`; nhớ tách " | " khỏi `text` của `find_words`.
- Điền từ của Từ ngữ tập hai thường có hai từ cùng đúng: dùng thẻ riêng mỗi ô.
- `python -m tapdoc requests` xoá file tổng đợt: chạy `requests` rồi chạy lại `dot_list.py` cho mọi đợt.
- Mã `tu_*` dùng chung với lớp 1 mà lời đọc khác ("Sa Pa") làm `build` báo lỗi danh mục: bỏ từ đó khỏi phương án nghe.
