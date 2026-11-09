# Thiết kế: Đưa SGK Tiếng Việt 2 – Tập một vào app (lớp 2, tuần 1–17)

> **Ngày:** 9/11/2026 · **Trạng thái:** chủ dự án giao Claude tự chọn hết ("Claude tự chọn hết", 9/11/2026). Spec và plan chờ chủ dự án duyệt trước khi làm.
> **Sách:** `tv2_t1_2001`, Tiếng Việt 2 – Tập một, Bộ GD&ĐT, Trịnh Mạnh – Đinh Tấn Ký – Đỗ Quang Lưu, tái bản lần thứ hai mươi (2001), 66 ảnh trang đôi.
> **Dựa trên:** [thiết kế TV1 tập 2](2026-11-05-tv1-tap-2-design.md) (đọc trước, spec này chỉ ghi phần khác), [thiết kế MVP](2026-10-28-app-tap-doc-mvp-design.md), [ghi chú tiếp tục tập 2](../notes/2026-11-05-tiep-tuc-tv1-tap-2.md).
>
> Cách đánh dấu:
> - **[Chốt]**: chủ dự án hoặc session gốc đã quyết.
> - **[Đề xuất]**: Claude chọn. Chủ dự án đổi được khi duyệt spec hay khi thử app; builder không hỏi lại.
> - **[Builder]**: builder tự quyết.

---

## 1. Mục đích

Lớp 1 (171 mục, hai quyển) đã có trong app. Lớp 2 là bước tiếp theo của cùng bé: bé đã đọc trơn, nay đọc bài dài hơn, hiểu nghĩa từ, làm quen với câu và tập nói thành đoạn. App vẫn là app tập đọc: giữ đúng trang sách, đổi cách tương tác để bé làm được trên màn hình mà không cần viết.

## 2. Sách thực tế (đã xem mục lục tr.122–128 và trang mẫu)

- **Chương trình cũ, không phải chương trình 2002.** Sách không có Kể chuyện, Tập viết, Luyện từ và câu. Mỗi tuần có: **Tập đọc**, **Học thuộc lòng**, **Bài đọc thêm** (bài "Đ.T"), **Chính tả**, **Từ ngữ**, **Ngữ pháp**, **Tập làm văn**.
- **17 tuần, 65 bài đọc** đánh số 1–65 trong sách (gồm Tập đọc, Học thuộc lòng, Bài đọc thêm). Mục lục tuần 16 để trống cột số bài; theo thứ tự thì đó là bài 59–61. Tuần 4, 9, 16 có 3 bài đọc, các tuần còn lại 4 bài.
- **Câu đố:** bài 15 "Câu đố: Đồ dùng của học sinh" (tr.27) và bài 46 "Câu đố: Quả gì?" (tr.84), cả hai in "(Bài đọc thêm)". Đáp án ở **tr.122 "Giải đáp câu đố"**.
- **Chủ điểm** in trong mục lục: "Nhà trường" (tuần 1–5), "Gia đình" (tuần 6–9), "Đất nước ta" (tuần 10–17). Kiểm lại khi chép tuần 13–17.
- **Trang:** nội dung tr.4–121; tr.122 giải đáp câu đố; tr.123–128 mục lục.
- **Ảnh:** ảnh `NNN` chứa tr.`2·NNN−2` và `2·NNN−1`, **trừ `029` và `030` bị đảo**: `030` là tr.56–57, `029` là tr.58–59 (lấy từ bản scan khác). Hai ảnh tên `Trang_29` không trùng nhau; đủ trang. Ảnh `065` là tr.128 và trang trắng.
- **Kí hiệu trên trang:** **[?]** câu hỏi (như TV1 tập 2), **[:]** giải nghĩa từ (mới), câu hỏi có dấu **\*** (câu dành cho bé khá, in như vậy).
- **Bài 1 "Bác Hồ khuyên học sinh"** in ảnh chụp chân dung Bác Hồ (người thật).

### Cấu trúc từng phân môn
| Phân môn | Trên trang |
|---|---|
| Tập đọc / Học thuộc lòng / Đọc thêm | số và tên bài, dòng "(Học thuộc lòng)"/"(Bài đọc thêm)", tranh, bài văn hoặc thơ, tác giả; [:] giải nghĩa 1–3 từ; [?] 2–5 câu hỏi (hiểu bài, tìm từ cùng nghĩa, đặt câu, tìm tiếng có vần giống nhau…). Bài đọc thêm không có câu hỏi |
| Chính tả | hai phần (Tập chép / Nghe đọc / Trí nhớ), mỗi phần: "1. Bài viết/Bài chép", "2. Viết đúng" (từ), "3. Luyện tập": ghép chữ rồi đọc lên, điền vào chỗ trống (*chao* hay *trao*…), gạch dưới chữ, viết tên riêng, tìm chữ có vần… |
| Từ ngữ | tên bài; "I – Những từ ngữ cần ghi nhớ" (các nhóm từ); "II – Bài tập": điền từ vào đoạn văn (có hoặc không có từ cho sẵn), trả lời câu hỏi về nghĩa từ |
| Ngữ pháp | tên bài; khung quy tắc; bài tập: dòng nào chưa thành câu, đặt câu hỏi tìm bộ phận chính, tìm bộ phận chính, đếm tiếng/từ/chữ cái… |
| Tập làm văn | "Điền từ" (đề bài + đoạn văn có chỗ trống + từ cho sẵn) hoặc "Quan sát tranh và trả lời câu hỏi" (xem tranh của một bài đọc trước đó + 3–4 câu hỏi) |

## 3. Mục tiêu, việc không làm, điều coi là thất bại

### Mục tiêu
1. Đưa vào app **133 mục** của tập một, đúng nội dung và thứ tự trang, mức `page_verified`: 65 bài đọc (gồm 2 trang câu đố) và mỗi tuần 4 mục Chính tả, Từ ngữ, Ngữ pháp, Tập làm văn (17 × 4 = 68).
2. Lớp 2 hiện trong app như **một lớp riêng**: bé lớp 2 vào thẳng lớp 2, không phải học hết 171 mục lớp 1.
3. Thêm các bước còn thiếu cho Từ ngữ, Ngữ pháp, Tập làm văn, Chính tả lớp 2 (mục 7).
4. Âm thanh HoaiMy cho mọi mã mới, `cho_duyet`.
5. Danh sách tranh cho mọi tranh mới, bàn giao session vẽ tranh (mục 10).
6. Gói media đóng sau đợt cuối.

### Không làm
- Phần viết: "Bài viết/Bài chép", "Viết tên riêng", "viết vào vở" [Chốt, giữ như TV1 tập 2]. Thay bằng dòng nhắc, ghi `khac_sach`.
- Micro, chấm câu trả lời nói. Câu hỏi hiểu bài và câu hỏi mở bé trả lời miệng với bố mẹ [Chốt, như tập 2].
- Tự vẽ tranh, dùng ChatGPT hay Google Flow [Chốt].
- Bản build Windows/Android [Chốt].
- Tiếng Việt 2 tập hai, Truyện đọc 2. Chọn lớp trong màn tạo hồ sơ bé (để sau).

### Coi là thất bại, dù app vẫn chạy
- Chữ khác trang sách, đổi thứ tự trang, thêm hoạt động không bắt nguồn từ trang.
- Bé lớp 1 đang học bị mất tiến độ, mất hoa, thấy danh sách lớp 1 đổi thứ tự; file bài lớp 1 dựng lại bị đổi.
- Bé lớp 2 phải học hết lớp 1 mới mở được bài lớp 2.
- Đáp án do app soạn mà không gắn `can_duyet`.
- Tranh vẽ người thật; ảnh scan lọt vào repo hay vào app.

## 4. Lớp 2 trong app

### 4.1 Số bài, mã bài [Đề xuất]
- **`lesson_no` chạy tiếp cả chương trình: 172–304**, theo thứ tự trang. Bé không thấy số này.
  - Lý do: công cụ đã dựa vào `lesson_no` cho thứ tự, mã âm thanh `cau_bNN_kk`/`hoi_bNN_kk`/`hd_bNN_*`, mã tranh `img_bNN_*` và "chữ đã học". Đánh lại từ 1 sẽ trùng mã với lớp 1 (khảo sát code 9/11/2026); chạy tiếp thì không phải đổi gì.
- Mã bài `tv2_t1_b172` … `tv2_t1_b304`; file nguồn `content/src/tv2_t1_bNNN.json`; mã tranh `img_b172_*`.
- **Nhãn** (`label`): bài đọc "Bài 1" … "Bài 65" theo số in (`td_no`); câu đố "Câu đố"; "Chính tả", "Từ ngữ", "Ngữ pháp", "Tập làm văn".
- **Tuần** (`week`): 1–17. **Chủ điểm** (`theme`, mới): "Nhà trường", "Gia đình", "Đất nước ta".
- Thứ tự trong tuần theo trang (cũng là thứ tự mục lục): các bài đọc, rồi Chính tả, Từ ngữ, Ngữ pháp, Tập làm văn.

### 4.2 Dữ liệu sách [Đề xuất]
- `content/books.json` thêm quyển `tv2_t1_2001` (title "Tiếng Việt 2 – Tập một", `appendix: "tv1_t1_1990"` vì sách lớp 2 không in Phụ lục, và app cần Phụ lục cho mọi quyển khi khởi động). Mọi quyển thêm trường **`grade`** (1 hoặc 2) và **`spell`** (true/false, mục 4.5).
- Loại bài mới: `tu_ngu`, `ngu_phap`, `tap_lam_van`. Bài đọc dùng lại `tap_doc`, `hoc_thuoc_long`, `doc_them`, `cau_do`; chính tả dùng lại `tap_chep_chinh_ta`.
- **Phần** (`part`) của bài lớp 2 là `lop2` cho mọi loại; `part` lớp 1 giữ nguyên. Dòng `index.json` thêm `grade` (lấy từ quyển) và `theme` (chỉ lớp 2). Trường cũ giữ nguyên.
- "Chữ đã học" (`curriculum`): bài 172 trở đi coi như đã học hết lớp 1. Không có quy tắc đánh vần mới.
- `LESSON_INDEX.csv` thêm 133 dòng `tv2_t1_2001`. Cột `bai_so` của lớp 2 không dùng số trần (công cụ báo lỗi số trùng giữa hai quyển), ví dụ "L2-B1" cho bài đọc 1, để trống cho Chính tả/Từ ngữ/Ngữ pháp/Tập làm văn [Builder: dạng chuỗi].
- Sửa `BOOK_CATALOG.md` mục 4.3: hai ảnh `Trang_29` là tr.56–57 và 58–59, bị đảo.

### 4.3 Danh sách bài [Đề xuất]
> **Đã thay (9/11/2026):** mục 4.3–4.4 (thẻ "Lớp 1/Lớp 2", mở khoá riêng mỗi lớp) được thay bằng thiết kế Tủ sách ([2026-11-09-tu-sach-design.md](2026-11-09-tu-sach-design.md)), chủ dự án đã duyệt: chọn quyển ở màn Tủ sách, học xong quyển trước mới mở quyển sau. Session UI làm phần này.

- Trên cùng màn danh sách có **hai thẻ chọn lớp: "Lớp 1" và "Lớp 2"**. Lớp 1 giữ đúng ba phần như hiện nay. Lớp 2 chia phần theo chủ điểm ("Nhà trường", "Gia đình", "Đất nước ta"), trong mỗi phần có dòng "Tuần 1" … "Tuần 17" như phần Tập đọc lớp 1.
- Thẻ bài: dòng trên là nhãn, dòng dưới là tên bài, như Tập đọc tập 2. Tên Tập làm văn dài ("Quan sát tranh và trả lời câu hỏi: Cánh đồng lúa chín") phải đọc được [Builder: cỡ chữ, cắt dòng].
- **Nhớ lớp đang xem theo từng bé** (lưu trong hồ sơ, mặc định "Lớp 1"). Mở màn thì vào lớp đã nhớ và cuộn tới bài đang học của lớp đó.
- Sửa chỗ bài có `part` lạ bị ẩn mà vẫn nằm trong chuỗi mở khoá (khảo sát: `LessonListScreen` chỉ biết ba phần).

### 4.4 Mở khoá [Đề xuất]
- **Mỗi lớp một chuỗi riêng:** bài đầu của mỗi lớp luôn mở; trong lớp, bài k mở khi bài k−1 xong. Lớp 1 không đổi gì.
- Công tắc "Mở mọi bài" giữ nguyên, áp cho cả hai lớp.
- Lý do: bé đã học lớp 1 ở trường vào thẳng lớp 2; không cần thêm công tắc mới.

### 4.5 Chạm tiếng: đọc trơn, không đánh vần [Đề xuất]
- Bé lớp 2 đã đọc trơn. Quyển có `spell: false` thì công cụ **không sinh chuỗi đánh vần** cho tiếng nào; chạm tiếng thì app đọc tiếng đó (Unity đã xử lý chuỗi rỗng như vậy). Lớp 1 `spell: true`, file bài không đổi (test hồi quy).
- Ích lợi phụ: không sinh mã `am_`/`van_` mới, ít âm thanh phải tạo hơn nhiều.
- Muốn bật lại đánh vần chỉ cần đổi cờ rồi dựng lại.

### 4.6 Màn Phụ huynh, Sổ bé ngoan [Đề xuất]
- Tiến độ tách theo lớp: "Lớp 1: x/171", "Lớp 2: y/133".
- Sổ bé ngoan ghi nhãn và tên bài (hiện đang ghi "Bài {lesson_no}", sẽ hiện "Bài 172"): đổi sang `label`. Sửa này cũng đúng cho lớp 1 (bài vần và chữ cái có nhãn "Bài N" trùng số cũ).
- Phụ lục: giữ một mục, lấy theo `books.json` như hiện nay.

## 5. Một bài đọc lớp 2 [Đề xuất, dựa trên Tập đọc TV1 tập 2]

Ví dụ "Cái trống trường em" (tr.6–7). Phần 1 đúng thứ tự trang:
1. **Tranh bài** (`picture`), chạm thì nghe lời dẫn ngắn (`can_duyet`).
2. **Tên bài** (`title`), dòng "(Học thuộc lòng)"/"(Bài đọc thêm)" nếu có.
3. **Đọc từng câu** (`sentence`): mỗi câu văn hoặc dòng thơ một bước, câu dài tách theo dấu phẩy như tập 2. Chạm tiếng thì nghe tiếng (mục 4.5).
4. **Đọc cả bài** (`passage`), chia trang theo đoạn/khổ khi dài. Bài lớp 2 dài tới khoảng 10 câu; chữ không nhỏ hơn mức tối thiểu tập 2.
5. **[:] Giải nghĩa từ**: bước `rule` có kí hiệu ":", mỗi dòng "Giá trống: cái khung bằng gỗ…" đọc liền; từ được giải nghĩa in đậm hoặc nghiêng như sách [Builder].
6. **[?] Câu hỏi**, mỗi câu một bước, đúng thứ tự, giữ dấu "\*":
   - Câu hỏi về chữ có đáp án trong bài ("Tìm những tiếng có vần giống nhau ở cuối các dòng thơ") → `find_words`. Khi đáp án không xác định được bằng vần/âm/dấu, dùng điều kiện mới **`word`** (danh sách tiếng đúng, Claude chọn, `can_duyet`).
   - Câu hỏi hiểu bài, tìm từ cùng nghĩa, đặt câu → `question` (trả lời miệng).
   - "Học thuộc lòng" (bài HTL) → `memorize`, như tập 2. Bài HTL lớp 2 không in câu "Học thuộc lòng cả bài" nhưng nhãn "(Học thuộc lòng)" có trên trang, nên vẫn có bước `memorize` ở cuối Phần 1 (`khac_sach`).
7. **Tranh người thật** (bài 1 và mọi trang có Bác Hồ hay nhân vật lịch sử): app vẽ cảnh không có người thật, ghi `khac_sach` như các bài 107, 115, 124, 130, 160, 168 của lớp 1 [Chốt theo cách đã làm].

Bài đọc thêm không có câu hỏi. Câu đố làm như tập 2 (`riddle_answer`, đáp án tr.122, tranh đáp án vẽ mới `can_duyet`).

## 6. Chính tả, Từ ngữ, Ngữ pháp, Tập làm văn [Đề xuất]

Mỗi mục là một bài trong danh sách, bắt đầu bằng `title` (tên phân môn và tên bài). Mỗi phần I/II hay "1. Đề bài", "2. Câu hỏi" là một `title` có dòng phụ.

| Trên trang | Bước trong app |
|---|---|
| "Bài viết/Bài chép", "Viết tên riêng…", "viết vào vở" | dòng nhắc "Phần này con viết vào vở cùng bố mẹ" (trong `title`), `khac_sach`. Chữ cần viết (tên riêng) vẫn hiện để bé đọc (`words`) |
| "Viết đúng", "Những từ ngữ cần ghi nhớ" | `words`: mỗi từ một thẻ, chạm thì nghe từ |
| "Ghép chữ *dúm* với các chữ: *lông, muối*", "Viết chữ *quạt* vào trước (hay sau) các chữ…" | **`combine_words`** (mới): thẻ chữ gốc và các thẻ chữ ghép; chạm thẻ ghép thì cụm từ hiện ra ("dúm lông") và app đọc. Chỗ sách để bé chọn trước/sau thì Claude chọn, `can_duyet` |
| "Điền vào chỗ trống: *chao* hay *trao*" | `fill_blank` sẵn có (lựa chọn là cả tiếng cũng chạy được với mode `letter`) |
| "Gạch dưới chữ *tỏa* và chữ *phếch*", "Tìm chữ có *ươi*" | `find_words` (điều kiện `word`, `rime`…), có thể dùng `text` riêng như tập 2 |
| Điền từ vào đoạn văn có từ cho sẵn (Từ ngữ, Tập làm văn "Điền từ") | **`fill_passage`** (mới): đoạn văn có các ô trống, hàng thẻ từ bên dưới. Bé chạm ô rồi chạm thẻ (hoặc kéo thẻ vào ô). Đúng thì ô điền chữ và app đọc câu đó; sai thì thẻ về chỗ, không chê; sai 2 lần liên tiếp ở một ô thì thẻ đúng nhấp nháy. Điền đủ thì khen. Đáp án Claude điền, `can_duyet` |
| Điền vào chỗ trống mà sách không cho từ ("Một năm có … tháng") | `fill_passage`, mỗi ô có 2–3 lựa chọn riêng do Claude soạn (đáp án + nhiễu), `can_duyet`, `khac_sach` |
| "Trong những dòng sau, dòng nào viết chưa thành câu?" và câu chọn tương tự | **`choose_line`** (mới): các dòng thành thẻ; chạm thì nghe; thẻ đúng được đánh dấu, thẻ sai chỉ đọc lại. Tìm đủ thì khen. Đáp án Claude, `can_duyet` |
| Khung quy tắc Ngữ pháp | `rule` sẵn có |
| Câu hỏi mở (đặt câu, kể tên, so sánh nghĩa, đếm tiếng/từ, đặt câu hỏi cho bộ phận câu) | `question`, thêm trường tuỳ chọn **`lines`**: các câu sách in kèm câu hỏi hiện bên dưới, chạm để nghe |
| Tập làm văn "Quan sát tranh và trả lời câu hỏi" | `picture` dùng **lại tranh của bài đọc được nhắc** (cùng mã, không vẽ thêm), rồi mỗi câu hỏi một `question` |

- Đáp án do app soạn được nêu một lần trong ghi chú "App khác sách" của mỗi bài có đáp án soạn.
- Không thêm hoạt động mà trang không có [Chốt].

### Phần 2 – Luyện tập
- Giữ luật hiện có cho mọi bài: 6–10 lượt, phương án chỉ dùng chữ đã học (lớp 2 = cả lớp 1), luật giọng miền Nam [Đề xuất: không đổi `validate`].
- Lấy từ chữ của chính bài: nghe và chọn từ (từ ngữ cần ghi nhớ, từ "Viết đúng", từ trong bài đọc), ghép tiếng (`compose`), nhìn dấu hỏi/ngã khi bài có cặp đó, nghe và chọn tranh (câu đố).
- Từ có âm chưa dạy ở lớp 1 (tên riêng như "Plây Cu") không dùng làm phương án.

## 7. Bước mới và bước sửa (công cụ + Unity)

| Bước | Thay đổi | Ghi chú |
|---|---|---|
| `combine_words` | mới | `base`, `partners`, vị trí `before`/`after` mỗi cụm; mỗi cụm có chữ và audio `tu_*` |
| `fill_passage` | mới | đoạn văn tách thành mảnh chữ và ô; mỗi ô: đáp án, lựa chọn (chung `bank` hoặc riêng); audio từng câu (`cau_bNNN_kk`) |
| `choose_line` | mới | câu hỏi + audio `hoi_`; các dòng có chữ, audio; danh sách dòng đúng |
| `find_words` | sửa | thêm điều kiện `word` (danh sách tiếng) |
| `question` | sửa | thêm `lines` tuỳ chọn |
| `rule` | sửa nhẹ | nhận kí hiệu ":"; `validate` cho phép kí hiệu ":" |
| mọi bước có tiếng | sửa | không sinh đánh vần khi quyển `spell: false` |

- Màn mới theo phong cách đã chốt (thẻ viền mực, bóng gạch, tiếng động chạm, gà con, chấm tiến độ). Giao diện Claude tự làm, không giao worker [Chốt].
- Chữ của `fill_passage` và `choose_line` đọc được ở cả hai khung thử (1600×720, 1440×1080); đoạn dài thì chia trang, không thu nhỏ thêm.
- Kí hiệu [:] cần biểu tượng tạm `img_chung_giai_nghia` vẽ bằng `ui_icons.py` như [?] [Builder: hình].

## 8. Ghi chú cho phụ huynh

- `sach`: chú thích in trên trang (các dòng [:] đã thành bước, không lặp lại ở ghi chú).
- `khac_sach`: phần viết bỏ; câu hỏi trả lời miệng; đáp án app soạn; tranh thay người thật; câu dài tách bước; bước học thuộc lòng thêm ở bài HTL; chạm tiếng chỉ đọc, không đánh vần (ghi một lần ở bài đầu lớp 2).
- Không có `ten_doc` mới.

## 9. Âm thanh [Chốt: HoaiMy]

- Mọi mã mới tạo bằng `python -m tapdoc tts`, giọng HoaiMy, `cho_duyet`. Không đụng mã lớp 1 đã có (dùng chung theo mã).
- Chạy **1 tiến trình**, mỗi mã tối đa 90 giây [Chốt].
- **Mọi tiếng lẻ (`tieng_*`) mới đọc trong câu đệm ngay từ đầu** [Chốt, root 9/11/2026]: HoaiMy hay đọc thanh hỏi, ngã của tiếng đứng một mình thành thanh huyền (chủ dự án đã chê nhiều ở lớp 1). Mỗi mã `tieng_*` mới có override `{"doc": "X, X.", "keep_first": true}` trong `content/tts/settings.json` trước lượt tạo đầu tiên. Công cụ `tts` thêm cờ `--tieng-keep-first` tự ghi override này cho mã chưa có override.
- **Từ và câu có thanh hỏi, ngã phải qua đo cao độ** trước khi coi là xong [Chốt, root 9/11/2026]: so đường cao độ của tiếng hỏi/ngã với mẫu (dip rồi lên). Mã đo không đạt thì làm lại theo cách session lớp 1 (`local_1af66fbb…`) báo sau khi rà soát xong; trong lúc chờ, thử `keep_first` với câu đệm. Cách đo: bộ nhớ `project-tts-keep-first` (MP3 → WAV bằng Media Foundation, YIN thuần Python, mẫu lấy từ tiếng đã duyệt `dat`). Dùng công cụ đo của session lớp 1 nếu đã có trong repo; chưa có thì đưa vào `tools/tapdoc/pitch_check.py`.
- Dịch vụ hay trả rỗng: sau lượt chính chạy **lượt bù** cho mã còn `chua_co`. Mã từ ngắn mà vẫn rỗng cũng đọc trong câu đệm như trên [Chốt].
- Âm thanh chạy nền, song song với việc chép bài; không chặn đợt sau.
- Commit `settings.json` chỉ các override mới của mình, bằng cách dựng blob từ HEAD (mục 11).

## 10. Tranh [Chốt]

- Session này không vẽ. Mỗi đợt, `python -m tapdoc requests` sinh phiếu `content/requests/images_tv2_t1_bNNN.md` (mã `img_bNNN_*` + mô tả cảnh); kèm một file tổng của đợt `content/requests/images_tv2_t1_dot_N.md` liệt kê mọi mã `chua_co` của đợt [Đề xuất].
- Nhắn session "Vẽ tranh SGK Tiếng Việt 2 tập 1" (`local_be5a6177-2125-4c96-8ac1-da797a8751f8`) đường dẫn file tổng và số mã. Session đó vẽ và nhập; session "Tranh động SGK Tiếng Việt 2 tập 1" (`local_d1b0f2bf-9813-44de-8419-c1b19596eb10`) làm clip sau khi tranh đã nhập (không nhắn trực tiếp trừ khi root bảo).
- Mỗi bài đọc thường 1 tranh lớn theo tranh sách; câu đố có tranh đáp án và tranh nhiễu nếu thiếu; Chính tả, Từ ngữ, Ngữ pháp không có tranh; Tập làm văn quan sát tranh dùng lại tranh bài đọc.
- Lúc chưa có tranh: `validate --allow-missing`.

## 11. Git, phối hợp, kiểm tra

- Chỉ `main`, `git add` theo đường dẫn, không squash, không force push; chủ dự án tự push [Chốt].
- `content/manifests/*.json`, `content/tts/settings.json`, `content/style/tranh_dong_kich_ban.json` có chỉnh sửa duyệt chưa commit của chủ dự án: chỉ stage dòng của mình (blob từ HEAD + dòng mới, `git hash-object -w`, `git update-index --cacheinfo`) [Chốt].
- Không mở công cụ duyệt, không đổi giao diện công cụ duyệt. Công cụ duyệt lọc theo `book` sẵn; chỉ thêm thư mục scan `tv2_t1_2001` vào `SCAN_BOOK_DIRS` (dữ liệu, không đổi giao diện) để chủ dự án đối chiếu trang [Đề xuất].
- **Test** [Chốt]: Claude viết và review mọi test, test trước rồi mới code; chỉ chạy test của phần đang làm; toàn bộ chỉ khi chủ dự án nói "test all"; đóng Unity Editor trước khi chạy test Unity.
  - Python: `books.json` có `grade`/`spell`; `part`/`grade`/`theme` trong `index.json`; tắt đánh vần theo quyển; ba bước mới và hai bước sửa; **test hồi quy: dựng lại 171 mục lớp 1 ra file y hệt bản đang commit**; test nội dung lớp 2 (đủ 133 mục, nhãn, tuần, chủ điểm).
  - Unity EditMode: đọc bước mới, chuỗi mở khoá theo lớp, thẻ lớp, nhãn Sổ bé ngoan.
  - Unity PlayMode chạy `--filter` theo lớp test của màn mới và một smoke test đi qua các bài lớp 2 của đợt.
- `validate` báo OK (`--allow-missing` khi tranh chưa về).
- Ảnh scan không vào repo, không vào app [Chốt].
- Tối đa 1 subagent [Chốt].

## 12. Chia đợt [Đề xuất]

| Đợt | Nội dung | Mục |
|---|---|---|
| **L2-1** | Lớp 2 trong app (mục 4), tắt đánh vần theo quyển, 3 bước mới + 2 bước sửa (mục 7); nội dung tuần 1–3 (đủ mọi phân môn, làm mẫu) | 172–195 (24) |
| **L2-2** | Tuần 4–8 (có câu đố bài 15) | 196–234 (39) |
| **L2-3** | Tuần 9–13 (có câu đố bài 46) | 235–273 (39) |
| **L2-4** | Tuần 14–17; cập nhật `BOOK_CATALOG.md`, `LESSON_TYPES.md`, ghi chú tiếp tục; lượt bù âm thanh cuối; đóng gói media | 274–304 (31) |

- Mỗi đợt kết thúc khi: các mục `page_verified`, `build` + `validate --allow-missing` OK, test liên quan xanh, commit, phiếu tranh đã gửi session vẽ tranh, báo root.
- Làm liền các đợt, không dừng chờ duyệt [Đề xuất, như tập 2]; chủ dự án góp ý lúc nào sửa lúc đó.
- **Xong khi:** đủ 133 mục trong app, `validate` không lỗi (không `--allow-missing`, sau khi tranh về đủ), âm thanh đủ, `python tools/run_unity_media.py pack` đã chạy và `media_lock.json` đã commit; chủ dự án tự tải gói lên Drive [Chốt].
- Tranh về chậm hơn nội dung thì đóng gói khi tranh của đợt L2-4 đã nhập; nếu chủ dự án muốn sớm hơn thì đóng gói theo lời chủ dự án.

## 13. Builder tự quyết
- Bố cục, cỡ chữ, hiệu ứng của `combine_words`, `fill_passage`, `choose_line` và thẻ chọn lớp, trong khuôn phong cách đã chốt.
- Dạng chuỗi `bai_so` lớp 2 trong CSV; cách chia trang đoạn dài.
- Số lượt và kiểu lượt Phần 2 mỗi bài trong khoảng 6–10.

## 14. Rủi ro và việc để sau
- **Âm thanh chậm:** 1 tiến trình, dịch vụ chập chờn; lớp 2 có nhiều câu dài. Có thể kéo dài nhiều ngày; chạy nền liên tục.
- **Bản quyền bài đọc:** chép nguyên văn như lớp 1; vẫn nằm trong danh sách rủi ro chính sách chủ dự án đang để ngỏ.
- **Đáp án app soạn** (điền từ, chọn dòng): chủ dự án duyệt qua ghi chú `can_duyet`.
- Để sau: chọn lớp ngay khi tạo hồ sơ bé; Tiếng Việt 2 tập hai; giọng người thật.

## 15. Kết quả (9/11/2026)

- **Nội dung:** đủ **133 mục** `page_verified` (mục 172–304, tuần 1–17), chép từ ảnh 003–061. Mục lục khớp trang; tuần 16 mục lục để trống số bài, trang in 59–61 (ghi `sach`). Trang 37, 65 là trang bìa chủ điểm, không thành bài.
- **Công cụ:** `books.json` có `grade`, `spell`; `index.json` có `grade`, `theme`, `part = lop2`; quyển `spell: false` không sinh đánh vần; bước mới `combine_words`, `fill_passage`, `choose_line`; `find_words` điều kiện `word`; `question.lines`; kí hiệu ":". Âm thanh: `tts --tieng-keep-first`, mốc từng tiếng (`content/tts/marks`, chỉ trên máy), `tapdoc pitch` đo hỏi/ngã.
- **Unity:** thẻ "Lớp 1"/"Lớp 2" ở mép dưới danh sách bài, lớp 2 chia theo chủ điểm và tuần, mỗi lớp một chuỗi mở khoá, nhớ lớp theo bé; Phụ huynh hiện tiến độ từng lớp; Sổ bé ngoan ghi nhãn bài.
- **Khác kế hoạch (đã ghi trong sổ theo dõi):**
  - Smoke test bắt thẻ nhỏ hơn cỡ chạm tối thiểu (160): ghép chữ hiện cụm ngay trên thẻ; chọn dòng và câu kèm câu hỏi xếp lưới 2×2, nhiều thì chia trang; **điền đoạn văn đi từng câu**, mỗi ô 3 thẻ (đáp án và hai từ khác của sách), bé không tự chọn ô.
  - Câu dài tự tách theo dấu phẩy (≤15 tiếng); màn quy tắc/giải nghĩa tối đa 3 dòng; dòng phụ liệt kê từ cho sẵn rút gọn (từ đã hiện thành thẻ); 10 cụm điền chỗ trống rút ngắn cho vừa khung.
  - "Sa Pa" không dùng làm phương án nghe (mã `tu_sa_pa` đã có ở lớp 1 với lời đọc khác).
  - Kí hiệu [:] có hình tạm vẽ bằng `ui_icons.py` (không bao giờ bị ghi đè); hình chính thức vẫn nhờ session vẽ tranh.
- **Test:** Python liên quan đạt, test hồi quy 171 mục lớp 1 dựng lại y hệt; Unity EditMode 158/159 (`AllReferencedAssetsExist` chờ tranh, âm thanh lớp 2); PlayMode lọc (màn mới, danh sách bài, Phụ huynh) đạt; smoke 133 mục ở hai khung hình đạt.
- **Còn lại:** âm thanh HoaiMy (khoảng 3.000 mã, 1 tiến trình, đang chạy nền) và đo cao độ; 57 tranh + kí hiệu [:] (session vẽ tranh, 4 phiếu `content/requests/images_tv2_t1_dot_1..4.md`); đóng gói media khi đủ.
