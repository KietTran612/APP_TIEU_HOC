# Ghi chú tiếp tục — TV2 tập hai ("Bé tập đọc 4"), 17/11/2026

Đọc file này trước khi làm tiếp cuốn thứ tư. Thiết kế: [2026-11-17-tv2-tap-2-design.md](../specs/2026-11-17-tv2-tap-2-design.md) (mục 15 Kết quả); kế hoạch: [2026-11-17-tv2-tap-2.md](../plans/2026-11-17-tv2-tap-2.md). Session nội dung `[L2T2]`, root `local_0cefca18-12fb-4d82-a1d6-a65ff28a9bed`.

## 1. Đang ở đâu

| Phần | Trạng thái |
|---|---|
| Kiểm kê | Xong: bảng ảnh → trang (BOOK_CATALOG 4.4), 130 dòng CSV `page_verified` |
| Công cụ | Xong: f285c84 (`books.json`, tuần 1–35, chủ điểm), f95f92b (`--t2`, `xuat_wav_lop2.py`) |
| Nội dung | Xong: 130 mục 305–434 (e9f837c, 005b828, f9b4fd5, 391c59f), `validate --allow-missing` OK |
| Tranh | 41 tranh `chua_co`, danh sách đã gửi root (`content/requests/images_tv2_t2_dot_1..4.md`, ngoài git). Bìa `img_bia_tv2_t2_2002` đã có (216e923, `[Chung]` UI) |
| Âm thanh | **Xong 18/11**, 4 đợt HoaiMy: 3147 mã chỉ của tập hai đều `cho_duyet`, không thiếu mp3. Đợt 1–2 (305–370) 2de90da, đợt 3 (371–402) 760e607, đợt 4 (403–434) 9dfe844. Root đã nhận dạng từng đợt và so với giọng NamMinh; 168 bản thử được cài; các mã "giữ cũ" và "nghe kỹ" nằm trong danh sách nghe của chủ dự án (root giữ, `TapDocSoat/danh_sach_chu_du_an.md`) |
| Media | Chưa đóng gói. Root chạy `bosung` một lần cho mọi session; session này **không** chạy `bosung` hay `pack` |
| Unity | **Xanh 18/11.** EditMode 37/37 (`DataTests`, `BookShelfTests`, `LessonRepositoryTests`); PlayMode 39/39 (`Grade2Tap2LessonSmokeTests` 4 đợt, `BookScreenTests`, `ParentScreenTests`, `LessonPathTests`, `LessonListPartsTests`). Mọi mp3 và tranh đã có `.meta` |

## 2. Làm tiếp

1. **Unity**, chạy lại khi nội dung đổi (chỉ khi root nhắn tới lượt; đóng Editor): `cd tools && python run_unity_tests.py playmode --filter "TapDoc.Tests.Grade2Tap2LessonSmokeTests;TapDoc.Tests.BookScreenTests;TapDoc.Tests.ParentScreenTests"`. Hỏng ở màn dùng chung thì báo root, không tự sửa.
2. Khi tranh về đủ: `python -m tapdoc validate` (không `--allow-missing`).
3. **Làm lại âm thanh một mã** (chỉ khi root giao lượt tts; cả máy chỉ một tiến trình đọc):
   - Tạo bản thử ngoài danh mục: `python tools/lop2/ban_thu_lop2.py tao <thư mục> MÃ:cham#25=25 MÃ:ghep`. Ghép theo phần cho sẵn: `MÃ:ghep#nhãn=doc:…|tieng_x|,|doc:…`. Chữ số được giữ thành phần `doc:` (75dab62).
   - Root nhận dạng rồi chọn bản.
   - Cài: `ban_thu_lop2.py cai <thư mục> MÃ__cách --ghi-chu "…"`. Lệnh cài kiểm file cài trùng từng byte với bản thử.
   - Commit qua chỉ mục tạm: `GIT_INDEX_FILE=<tạm>`, `git read-tree HEAD`, rồi `python tools/lop2/stage_lop2.py --t2 content/manifests/audio_manifest.json content/tts/settings.json`. Gửi root `git diff --cached --stat` để kiểm, rồi commit. Sau commit chạy `git reset -q --` hai file đó.
   - Trong bản làm việc còn 33 dòng và 4 override duyệt của chủ dự án (`tieng_hes`, `tieng_thowf`, `tieng_tror`, `tu_cas_roo`): không commit lẫn, không xoá.

## 3. Soạn lại một tuần

`cd tools/lop2/soan_t2 && python wNN.py` ghi đè nguồn bài tuần đó, rồi `python trybuild.py <đầu> <cuối>`, `cd tools && python -m tapdoc build && python -m tapdoc validate --allow-missing`, `python tools/lop2/soan_t2/csv_verify.py`. File `.meta` của file bài mới phải tạo (GUID mới) trước khi commit. Commit nguồn bài, file bài, `index.json`, CSV và dòng danh mục qua chỉ mục tạm như mục 2.

## 4. Bài học

- Ảnh scan đầu sách bị xáo: luôn lấy ảnh theo `toc_t2.image_of(trang)`, không theo công thức.
- `l2lib.split_long` tách câu không có dấu phẩy ở giữa, có khi ngang hai câu thoại: ghi chỗ ngắt tay " | " trong `wNN.py`; nhớ tách " | " khỏi `text` của `find_words`.
- Điền từ của Từ ngữ tập hai thường có hai từ cùng đúng: dùng thẻ riêng mỗi ô.
- `python -m tapdoc requests` xoá file tổng đợt: chạy `requests` rồi chạy lại `dot_list.py` cho mọi đợt.
- Mã `tu_*` dùng chung với lớp 1 mà lời đọc khác ("Sa Pa") làm `build` báo lỗi danh mục: bỏ từ đó khỏi phương án nghe.

Âm thanh (18/11), áp vào chữ đọc trước khi tạo giọng:
- Ngoặc kép giữa câu không đọc (kiểu a, `ngoac_kep_lop2.py --t2`).
- Thêm dấu phẩy trước "nhé" khi tiếng trước nó mang thanh sắc.
- "Chính tả: …" và câu có "tả" cuối cụm: đọc chậm −25% (rate −40).
- "..." giữa câu: viết chữ đọc riêng. Câu giao bài viết "đoạn từ … đến …"; chỗ khác đổi thành dấu phẩy hoặc bỏ.

Lỗi hay gặp của HoaiMy và cách xử lý:
- Đọc phụ âm đầu c/ch thành t/tr (cào → trào, cấp → tập, chen → trên). "khuya" thành "khuy". Cách xử lý: bản chậm −25%, hoặc ghép từng tiếng; thiếu file tiếng thì tách tại chữ khó.
- "ĩ" (`tieng_ix`) luôn ra thanh sắc ("Ý"), cả với "ĩ, ĩ, ĩ.", "ỹ, ỹ.", "Ĩ, Ĩ.". Root chốt giữ bản đang cài, để chủ dự án nghe.
- Máy nghe (Whisper) đôi khi ra câu ảo ("Hãy subscribe…"). Root đệm 0,5 s lặng ở hai đầu rồi nhận dạng lại.

Đo cao độ (`do_cao_do_lop2.py`): tiếng đứng ngay trước chữ số ("khổ 2)") không tính là cuối cụm (1fd37f9). `can_nghe_ky` đặt tay giữ được qua `build` từ d7f6842.
