# Thiết kế: Đưa SGK Tiếng Việt 2 – Tập hai vào app ("Bé tập đọc 4", tuần 18–33)

> **Ngày:** 17/11/2026 · **Trạng thái:** chủ dự án để Claude tự chọn như tập một (17/11). Root soát spec và plan trước khi làm.
> **Sách:** `tv2_t2_2002`, Tiếng Việt 2 – Tập hai, Bộ GD&ĐT, Trịnh Mạnh – Đinh Tấn Ký – Đỗ Quang Lưu, tái bản lần thứ hai mươi, in xong tháng 1/2002, 65 ảnh.
> **Dựa trên:** [thiết kế TV2 tập một](2026-11-09-tv2-tap-1-design.md) (đọc trước; spec này chỉ ghi phần khác), [kế hoạch hoàn thiện 4 cuốn](../plans/2026-11-17-hoan-thien-4-cuon.md), `QUY-TRINH-LAM-VIEC.md`.
>
> Cách đánh dấu như tập một: **[Chốt]** chủ dự án/root đã quyết; **[Đề xuất]** Claude chọn, root/chủ dự án đổi được; **[Builder]** builder tự quyết.

---

## 1. Mục đích

App đã có 304 mục của ba cuốn. Cuốn thứ tư là phần tiếp theo của lớp 2, cùng bé, cùng cách học. Làm đúng như tập một: giữ trang sách, đổi cách tương tác để bé làm trên màn hình mà không cần viết. Mục tiêu 17/11 là một sản phẩm hoàn chỉnh có đủ 4 cuốn.

## 2. Sách thực tế (đã xem mục lục tr.122–124 và trang mẫu, 17/11)

Chi tiết ở [BOOK_CATALOG.md](../../source-inventory/BOOK_CATALOG.md) mục 4.4.

- **Cùng chương trình cũ với tập một.** Mỗi tuần: Tập đọc, Học thuộc lòng, Bài đọc thêm, Chính tả, Từ ngữ, Ngữ pháp, Tập làm văn. Không có câu đố, Kể chuyện, Tập viết.
- **Tuần 18–33** (16 tuần, không phải 19–35 như ghi tạm lúc giao việc). **66 bài đọc**, sách đánh số lại từ 1.
  - Tuần 20, 21, 22 có 5 bài đọc; tuần 24 có 3; các tuần khác có 4.
  - Mục lục in chung một dòng "12–13", "17–18", "22–23" cho hai Bài đọc thêm. Trên trang mỗi số là một bài riêng, có đầu bài riêng.
- **Chủ điểm** in trên trang bìa chủ điểm (trang tranh, không thành bài): tr.3 "Thiếu nhi" (tuần 18–22), tr.43 "Nhân dân ta" (tuần 23–30), tr.100 "Bác Hồ" (tuần 31–33).
- **Trang:** tr.1 tên sách; tr.2 kí hiệu ([:] chú thích và giải nghĩa, [?] câu hỏi và bài tập, \* dành cho học sinh khá và giỏi); nội dung tr.4–121; mục lục tr.122–124.
- **Ảnh:** đầu sách bị xáo (đến ảnh `023`), từ ảnh `024` theo công thức ảnh `NNN` = tr.`2·NNN−2`, `2·NNN−1`. Đủ trang 1–125, không thiếu, không trùng. Bảng ảnh → trang ở BOOK_CATALOG; hàm `image_of` trong `tools/lop2/soan_t2/toc_t2.py`.
- **Dạng bài mới so với tập một** (cùng khuôn trang):
  - Ngữ pháp: danh từ, danh từ chung và riêng, viết hoa tên người và tên đất, xếp tên người theo thứ tự bảng chữ cái.
  - Tập làm văn: "Trả lời câu hỏi" (đề bài là một bài đọc đã học, 4 câu hỏi); "Dùng từ – đặt câu" (đề bài + các từ cho sẵn).
- **Nhiều bài về người thật:** Bác Hồ, chị Võ Thị Sáu, Bà Triệu, Trần Quốc Toản, Quang Trung (Gò Đống Đa), anh Phạm Tuân, các anh hùng nhỏ tuổi. Tranh sách vẽ các nhân vật này.
- **Lỗi in, bài 10 (Huy Cận):** sách in "Trăng sao cũng hóa **xú** người" ở cả đầu bài, câu thơ, câu hỏi 1 và mục lục; nghĩa đúng là "xứ người" (xem mục 5.3).

## 3. Mục tiêu, việc không làm, điều coi là thất bại

### Mục tiêu
1. Đưa vào app **130 mục** của tập hai, đúng nội dung và thứ tự trang, mức `page_verified`: 66 bài đọc và mỗi tuần 4 mục Chính tả, Từ ngữ, Ngữ pháp, Tập làm văn (16 × 4 = 64).
2. Cuốn hiện ở Tủ sách với tên **"Bé tập đọc 4"**, mở khi học xong "Bé tập đọc 3" (luật Tủ sách sẵn có).
3. **Dùng lại các bước của tập một, không thêm bước mới, không sửa Unity** [Đề xuất]. Trang nào cần bước mới thì hỏi root trước.
4. Âm thanh HoaiMy đủ mã mới, root đã nhận dạng giọng nói; `cho_duyet`.
5. Danh sách tranh mỗi đợt gửi root (root chuyển session vẽ tranh `[L2T2]`).
6. Test của phần mới xanh.

### Không làm
- Như tập một: phần viết (thay bằng dòng nhắc, `khac_sach`), micro, chấm câu trả lời nói.
- Vẽ tranh, dùng ChatGPT, Google Flow, trình duyệt [Chốt].
- Bìa sách: session `[Chung]` UI làm [Chốt].
- Sửa màn hình dùng chung (LessonListScreen, ResultScreen, ParentScreen, BookScreen, ReviewSession, ProgressStore, LessonData) [Chốt]. Sửa file của cuốn khác.
- `run_unity_media.py pack`; build Windows [Chốt]. Root đóng gói `bosung`.

### Coi là thất bại, dù app vẫn chạy
- Như tập một: chữ khác trang sách, đổi thứ tự trang, thêm hoạt động không có trên trang, đáp án app soạn mà không `can_duyet`, tranh vẽ người thật, ảnh scan lọt vào repo hay app.
- File bài của ba cuốn kia dựng lại bị đổi (test hồi quy).
- Bé đang học dở ba cuốn kia mất tiến độ hay thấy danh sách đổi.

## 4. Cuốn thứ tư trong app

### 4.1 Số bài, mã [Chốt theo kế hoạch 17/11]
- `lesson_no` **305–434** theo thứ tự trang. Mã bài `tv2_t2_b305` … `tv2_t2_b434`; nguồn `content/src/tv2_t2_bNNN.json`; tranh `img_bNNN_*`; âm thanh `cau_bNNN_kk`, `hoi_bNNN_kk`, `hd_bNNN_*` (số bài không trùng cuốn nào nên không đụng mã cũ).
- `book` = `tv2_t2_2002`, grade 2, `spell: false`, `part` = `lop2` như tập một.
- **Nhãn** (`label`): "Bài 1" … "Bài 66" theo số in (`td_no`); "Chính tả", "Từ ngữ", "Ngữ pháp", "Tập làm văn". "Bài 1" trùng nhãn với tập một nhưng mỗi cuốn có danh sách riêng ở Tủ sách nên không lẫn [Đề xuất].
- **Tuần** 18–33 như sách in [Đề xuất: giữ số tuần in, không đánh lại 1–16]. **Chủ điểm** (`theme`): "Thiếu nhi", "Nhân dân ta", "Bác Hồ".
- Thứ tự trong tuần như tập một: các bài đọc theo số, rồi Chính tả, Từ ngữ, Ngữ pháp, Tập làm văn.
- Danh sách 130 mục: `tools/lop2/soan_t2/toc_t2.json` (sinh từ `toc_t2.py`) và 130 dòng `tv2_t2_2002` trong `LESSON_INDEX.csv` (`bai_so` dạng "L2T2-B1").

### 4.2 Dữ liệu sách
- `content/books.json` thêm `{"book_id": "tv2_t2_2002", "title": "Bé tập đọc 4", "appendix": "tv1_t1_1990", "grade": 2, "spell": false}` [Chốt].
- `tools/tapdoc/build.py`: lớp 2 đang chặn tuần ngoài 1–17 và chủ điểm ngoài ba chủ điểm tập một. Sửa: **tuần lớp 2 hợp lệ 1–35; chủ điểm thêm "Thiếu nhi", "Nhân dân ta", "Bác Hồ"** [Đề xuất]. Sửa nhỏ, có test trước, commit sớm (mã dùng chung).
- `review_server.SCAN_BOOK_DIRS` thêm `tv2_t2_2002` (dữ liệu, không đổi giao diện), như tập một. Trang sách gốc trong tool duyệt lấy theo `source.scan_file`, nên ảnh xáo vẫn đúng.
- Unity không đổi: danh sách bài lớp 2 đã nhóm theo `theme` rồi `week` bất kỳ; Tủ sách đọc `books.json`; bìa `img_bia_tv2_t2_2002` có ảnh tạm cho đến khi `[Chung]` UI làm bìa.
- Thêm quyển có thể làm đổi bố cục Tủ sách, Sổ bé ngoan, Phụ huynh (4 quyển thay vì 3). Builder chạy test các màn đó sau khi thêm. Hỏng thì báo root, không tự sửa màn dùng chung.

## 5. Bài đọc [như tập một mục 5]

### 5.1 Khuôn
Tranh bài (`picture`, lời dẫn `can_duyet`) → tên bài → đọc từng câu (câu dài tách theo dấu phẩy, ≤ 15 tiếng) → đọc cả bài (chia trang theo đoạn/khổ) → [:] giải nghĩa (`rule` kí hiệu ":") → [?] câu hỏi (`question`, giữ dấu "\*"; câu tìm chữ có đáp án trong bài → `find_words`) → bài HTL thêm `memorize`. Bài đọc thêm: không có câu hỏi trên trang thì không thêm. Phần 2: 6–10 lượt nghe và chọn từ của bài.

### 5.2 Người thật [Chốt theo cách đã làm ở tập một]
Tranh của bài nói về người thật (Bác Hồ, nhân vật lịch sử, anh hùng, anh Phạm Tuân…) vẽ **cảnh không có người thật**: nơi chốn, đồ vật, thiên nhiên, hay các bạn nhỏ không tên. Mỗi bài ghi `khac_sach` "Sách vẽ …; app vẽ … (không vẽ người thật)" và `can_duyet` lời dẫn tranh.
- Bộ đội, công nhân, nông dân không tên trong tranh sách (đứng gác, hải quân, thợ đốt lò…) là người chung chung, vẽ được [Đề xuất]. Không vẽ súng chĩa vào người, không cảnh đánh nhau [Đề xuất].
- Bài về chiến tranh (chị Võ Thị Sáu bị giải ra nhà lao, voi Bà Triệu ra trận, Gò Đống Đa): tranh tả cảnh thiên nhiên và nơi chốn trong bài (đường ven biển Côn Đảo lúc bình minh, gò đất, rừng núi). Chữ bài đọc giữ nguyên như sách.

### 5.3 Bài 10 "xú người" [Đề xuất, cần root/chủ dự án chọn]
Sách in sai "xú người" ở 4 chỗ (đầu bài, câu thơ, câu hỏi 1, mục lục); "xú" nghĩa là hôi, không có nghĩa trong câu thơ.
- **Đề xuất:** app ghi **"xứ người"** ở mọi chỗ (bài 10 và tên bài Chính tả tuần 21), ghi `khac_sach` "Sách in 'xú người', app sửa thành 'xứ người' theo nghĩa câu thơ" và `can_duyet`. Lý do: bé học đọc và học nghĩa từ app, chép lỗi in thì dạy sai chữ, máy đọc cũng đọc sai.
- Cách khác: chép đúng "xú" như sách, ghi `sach` "sách in xú, nghĩa là xứ".

## 6. Chính tả, Từ ngữ, Ngữ pháp, Tập làm văn [như tập một mục 6, thêm dưới đây]

| Trên trang | Bước trong app |
|---|---|
| "Thêm chữ thích hợp vào các cặp từ so sánh: … vây ≠ vay…" | `fill_blank` (mỗi cặp một mục, lựa chọn là hai tiếng của cặp) |
| "Gạch dưới những chữ có dấu ngã trong bài chính tả", "Tìm trong bài chính tả những chữ có iê, ươ" | `find_words` trên đoạn bài chính tả (`text`), điều kiện dấu/vần; đáp án do điều kiện xác định |
| Ngữ pháp "Tìm những từ chỉ người/loài vật/cây cối/đồ vật trong bài …", "Tìm danh từ riêng trong bài" | `find_words` điều kiện `word` (Claude chọn, `can_duyet`) khi bài được nhắc là bài đọc ngắn có thể hiện lại; bài dài thì `question` (trả lời miệng) |
| Ngữ pháp "Kể thêm…", "Viết hoa…", "Tìm từ cùng nghĩa…" | `question` (có `lines` khi sách in kèm ví dụ) |
| Khung quy tắc ("Những từ chỉ … gọi là danh từ", "Tên riêng … phải viết hoa") | `rule` |
| "Đọc lại 29 chữ cái theo đúng thứ tự" | `letter_pairs` (bảng chữ cái, như tập một mục 295) |
| "Xếp tên các bạn sau theo thứ tự bảng chữ cái", "Em hãy xếp tên 5 bạn đó…" | `question` có `lines` là các tên in trên trang; bé xếp miệng cùng bố mẹ (như tập một mục 295), `khac_sach`. Ví dụ quy tắc in trên trang ("Duc xếp trước Dung (vì chữ c trước chữ n)") → `rule` |
| Tập làm văn "Trả lời câu hỏi", đề bài là bài đọc X | `title` (đề bài) → `picture` **dùng lại tranh của bài X** (cùng mã, không vẽ thêm) → mỗi câu hỏi một `question` |
| Tập làm văn "Dùng từ – đặt câu" | `title` (đề bài) → `words` (các từ cho sẵn, chạm nghe) → `question` "Em hãy đặt câu với mỗi từ" (trả lời miệng) |
| Từ ngữ "Điền từ thích hợp vào chỗ trống" có hoặc không có từ cho sẵn | `fill_passage` như tập một (đáp án Claude điền, `can_duyet`; không có từ cho sẵn thì mỗi ô 3 lựa chọn, `khac_sach`) |

- Chính tả, Từ ngữ, Ngữ pháp không có tranh; trang có hình minh hoạ (ví dụ xe cộ ở Từ ngữ "Giao thông vận tải") vẫn không vẽ, trừ khi bài tập dựa vào hình [Builder, ghi trong ghi chú].
- Không thêm hoạt động mà trang không có [Chốt].

## 7. Bước, công cụ, Unity

- Không bước mới. Công cụ sửa đúng hai chỗ ở mục 4.2 (tuần, chủ điểm).
- Script soạn bài của tập hai ở `tools/lop2/soan_t2/`: `toc_t2.py` (mục lục), `l2t2lib.py` (dùng lại khuôn `tools/lop2/soan/l2lib.py`, đổi mã bài, quyển, ảnh scan), mỗi tuần một file `wNN.py` [Builder].
- Script âm thanh `tools/lop2/` (tts, cách đọc tiếng lẻ, đo cao độ, kiểm tiếng lẻ, stage) đang lọc cứng `tv2_t1_`: thêm cờ `--t2` để lọc `tv2_t2_`, mặc định giữ nguyên tập một. **Không sửa `sua_hoi_nga_lop2.py`** (có chỉnh sửa chưa commit của chủ dự án); cần sửa hỏi/ngã cho tập hai thì viết script riêng [Đề xuất].

## 8. Ghi chú cho phụ huynh
Như tập một mục 8. Mục đầu cuốn (305) ghi `khac_sach` "chạm tiếng chỉ đọc, không đánh vần".

## 9. Âm thanh [Chốt: HoaiMy, cách của tập một và QUY-TRINH §6, §12]

- Mã mới tạo bằng `python -m tapdoc tts`, giọng HoaiMy, **1 tiến trình cả máy, hỏi root trước mỗi lần chạy** [Chốt 17/11]. Mỗi mã tối đa 90 giây, lượt bù cho mã rỗng.
- Tiếng lẻ mới: cách đọc của `tieng_doc_lop2.py` (nặng "X. X.", ê sắc "X, X, X.", còn lại "X, X.", giữ tiếng đầu) ghi trước khi tạo; `--tieng-keep-first`.
- Đo hỏi/ngã sau khi tạo (`do_cao_do_lop2.py --t2`, chỉ chấm tiếng lẻ và tiếng cuối cụm).
- **Nhận dạng giọng nói** [Đề xuất, root chọn]:
  1. Lượt chính tạo thẳng vào danh mục (`cho_duyet`), như tập một.
  2. Xuất WAV 16 kHz của cả đợt bằng `tapdoc.pitch_check.decode`, kèm `chi_muc.json` (mã, chữ, chữ đọc, file), vào thư mục root chỉ. Root nhận dạng và đối chiếu ở mức từ.
  3. Mã bị nghe sai hoặc đo sai: làm bản thử ngoài danh mục theo thứ tự §6 (đọc chậm, ngắt nhẹ, ghép tiếng đã đạt), xuất WAV cho root nhận dạng lại, rồi mới cài. Kiểm file cài trùng từng byte với bản thử.
  - Cách khác (nếu root muốn chặt hơn): mọi mã làm ngoài danh mục trước, root nhận dạng xong mới cài cả đợt.
- Commit danh mục âm thanh và `settings.json` chỉ dòng của mình, bằng `stage_lop2.py --t2` (blob từ HEAD).
- Âm thanh chạy nền theo đợt, không chặn chép bài.

## 10. Tranh [Chốt]
- Mỗi đợt: `python -m tapdoc build`, `python -m tapdoc requests`, rồi file tổng `content/requests/images_tv2_t2_dot_N.md` (mã, bài, mô tả). Nhắn root đường dẫn và số mã; root chuyển session vẽ tranh `[L2T2]`. Chạy `requests` trước, ghi file tổng sau (QUY-TRINH §12).
- Mỗi bài đọc thường một tranh theo tranh sách (người thật thay theo mục 5.2). Tập làm văn "Trả lời câu hỏi" dùng lại tranh bài đọc. Bài đọc thêm không có tranh in thì không vẽ.
- Lúc chưa có tranh: `validate --allow-missing`.

## 11. Git, test [như tập một mục 11]

- Chỉ `main`, `git add` theo đường dẫn; danh mục và `settings.json` qua chỉ mục tạm dựng từ HEAD; không đụng chỉnh sửa duyệt chưa commit của chủ dự án; không push [Chốt].
- **Test** [Chốt]: Claude viết test trước, chỉ chạy test phần mình làm.
  - Python: `test_grade2_build` thêm tuần 18–33, chủ điểm mới, tuần 36 bị chặn; `test_tap1_regression` (dựng lại lớp 1 y hệt) và kiểm 133 file `tv2_t1_*` dựng lại y hệt; mới `test_lop2t2_content.py` (đủ mục theo đợt, nhãn, tuần 18–33, chủ điểm theo tuần, `td_no` 1–66 liền, `page_verified`, không đánh vần).
  - Unity: không đổi code nên không chạy EditMode. PlayMode: mới `Grade2Tap2LessonSmokeTests` (đi hết các mục tập hai theo đợt ở 1600×720 và 1440×1080, như `Grade2LessonSmokeTests`); `BookScreenTests`, `ParentScreenTests` sau khi thêm quyển. Đóng Unity Editor trước khi chạy.
- Ảnh scan không vào repo, không vào app [Chốt].

## 12. Chia đợt [Đề xuất]

| Đợt | Nội dung | Mục |
|---|---|---|
| **T2-1** | `books.json`, công cụ (tuần, chủ điểm), script `--t2`; tuần 18–21 | 305–338 (34) |
| **T2-2** | Tuần 22–25 | 339–370 (32) |
| **T2-3** | Tuần 26–29 | 371–402 (32) |
| **T2-4** | Tuần 30–33; cập nhật `BOOK_CATALOG.md`, `LESSON_TYPES.md`, ghi chú tiếp tục | 403–434 (32) |

- Mỗi đợt xong khi: mục `page_verified`, `build` + `validate --allow-missing` OK, test liên quan xanh, commit, danh sách tranh đã gửi root, báo root.
- Âm thanh mỗi đợt chạy khi root cho phép (một tiến trình cả máy); xong thì xuất WAV cho root nhận dạng.
- Làm liền các đợt, không dừng chờ duyệt.
- **Xong khi:** đủ 130 mục, `index.json` dựng được, `validate --allow-missing` OK; danh sách tranh đã gửi; âm thanh đủ mã và root đã soát; test phần mới xanh; mọi thứ commit trên `main`. Root đóng gói `bosung` khi đủ media.

## 13. Builder tự quyết
- Cách chia trang đoạn dài, số lượt Phần 2 (6–10), đáp án điền chỗ trống (`can_duyet`).
- Mô tả tranh (đúng câu chữ trong bài, không người thật).

## 14. Rủi ro
- **Âm thanh chậm:** khoảng 3.000 mã mới, 1 tiến trình dùng chung cả máy với các session khác.
- **Bài về chiến tranh và người thật nhiều:** tranh thay thế phải vẫn gợi đúng bài; root và chủ dự án xem lời dẫn `can_duyet`.
- **Bản quyền bài đọc, lỗi in:** như tập một; lỗi in khác (nếu gặp) ghi `can_duyet`, xử lý như mục 5.3.
