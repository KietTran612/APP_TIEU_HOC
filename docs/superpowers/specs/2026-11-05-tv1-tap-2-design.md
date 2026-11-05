# Thiết kế: Đưa SGK Tiếng Việt 1 Tập hai vào app (bài 81–125 và phần Tập đọc)

> **Ngày:** 5/11/2026 · **Trạng thái:** Claude tự chốt theo yêu cầu của chủ dự án ("tạo lộ trình tốt, hợp lý; làm thành kết quả rồi mình test lại"). Chủ dự án duyệt bằng cách thử app sau mỗi đợt.
> **Sách:** `tv1_t2_1996`, Tiếng Việt 1 Tập hai (Vần – Tập đọc), NXB Giáo dục, chỉnh lí 1994, in lần 8 năm 1996, 72 ảnh trang đôi.
> **Dựa trên:** [thiết kế MVP](2026-10-28-app-tap-doc-mvp-design.md) (mục 5, 7, 8, 9, 16, 17), [giao diện và hiệu ứng](2026-10-30-ui-hieu-ung-design.md), [đọc dữ liệu](2026-11-04-doc-du-lieu-design.md), [ghi chú tập 1](../notes/2026-10-29-tiep-tuc-tv1-tap-1.md).
>
> Cách đánh dấu:
> - **[Chốt]**: chủ dự án đã quyết (ở dự án này hoặc khi làm tập 1).
> - **[Đề xuất]**: Claude chọn. Chủ dự án đổi được khi thử app; builder không cần hỏi lại.
> - **[Builder]**: builder tự quyết.

---

## 1. Mục đích

Tập 1 (80 bài) đã đủ nội dung, âm thanh, tranh và giao diện. Tập 2 nối tiếp đúng lộ trình của bộ sách: học nốt các vần khó (bài 81–125), rồi chuyển sang **Tập đọc** (tuần 27–33), nơi bé đọc trọn một bài văn hay bài thơ ngắn và trả lời câu hỏi.

Với phụ huynh, đây là lúc bé từ "đánh vần từng tiếng" chuyển sang "đọc trơn cả bài". App phải giữ đúng trang sách, nhưng cách tương tác phải giúp bé đọc được bài dài mà không nản.

## 2. Mục tiêu, việc không làm, điều coi là thất bại

### Mục tiêu
1. Đưa vào app **45 bài Vần** (81–125) và **46 mục Tập đọc** (36 bài tập đọc, 3 trang câu đố, 7 trang tập chép – chính tả), đúng nội dung và thứ tự trang sách, mức `page_verified`.
2. Một app, một danh sách bài chạy liền từ bài 1 tới hết Tập đọc. Tiến độ, hoa, Sổ bé ngoan, Ôn lại dùng chung cho cả hai quyển.
3. Thêm các màn còn thiếu cho Tập đọc: đọc cả bài, tìm tiếng theo câu hỏi, câu hỏi trả lời miệng, học thuộc lòng, điền chữ.
4. Âm thanh HoaiMy cho mọi mã mới, trạng thái `cho_duyet`.
5. Phiếu vẽ cho mọi tranh mới, bàn giao cho session gốc (mục 11).

### Không làm [Chốt, giữ như tập 1]
- Tập viết, tô chữ: mục ▨ "Em viết", phần "Bài viết / Bài chép" của trang Tập chép – Chính tả.
- Micro, chấm phát âm. Bé trả lời câu hỏi hiểu bài bằng miệng với bố mẹ; app không chấm.
- Tự vẽ tranh, dùng ChatGPT hay Google Flow trong session này (session gốc và session tranh động làm).
- Bản build Windows/Android. Chỉ commit.
- Lớp 2, Truyện đọc.

### Coi là thất bại, dù app vẫn chạy
- Chữ trong bài khác trang sách, hoặc đổi thứ tự trang, hoặc thêm hoạt động không bắt nguồn từ trang (mục 2 thiết kế MVP). Đổi cách tương tác thì được.
- Đánh vần sai quy ước sách ở tr.120–122 tập 1, hoặc sai quy tắc tạm ở mục 5 mà không gắn `can_duyet`.
- Bé tập 1 đang học dở bị mất tiến độ, mất hoa, hay thấy danh sách bài đổi thứ tự.
- Bài đọc dài làm chữ quá nhỏ, tràn khung, hoặc bé phải đọc cả trang chữ mà không có cách nghe từng câu.
- Ảnh scan lọt vào repo hay vào app.

## 3. Ràng buộc

Giữ mọi ràng buộc của tập 1: Unity 6.6, màn ngang, không cần mạng, tiến độ lưu trên máy, chuỗi đánh vần sinh sẵn trong dữ liệu, chữ chuẩn hoá NFC, tranh và âm thanh tách khỏi code, tranh và âm thanh ra khỏi git (gói media trên Drive, `media_lock.json`).

Thêm cho tập 2:
- **Chia việc [Chốt 5/11/2026]:** session này làm nội dung bài, dựng bài, âm thanh, màn mới. Tranh bài học do session gốc vẽ bằng ChatGPT; tranh động do session "Thử ảnh động / sprite sheet" làm bằng Google Flow.
- **Chủ dự án đang duyệt tập 1 song song.** Công cụ duyệt ghi vào `content/manifests/*.json` và `content/tts/settings.json`. Commit của Claude không được lẫn thay đổi duyệt của chủ dự án: chỉ đưa vào các dòng mới của mình (dựng bản index từ HEAD cộng dòng mới, `git update-index`), hoặc hỏi trước.
- **Sửa code dùng chung không được làm đổi dữ liệu tập 1** (trừ khi sửa lỗi có chủ ý). Mỗi thay đổi công cụ phải dựng lại 80 bài tập 1 và so: file bài tập 1 không đổi (test hồi quy, mục 12).

## 4. Hai quyển trong một app

### 4.1 Mã bài và số bài [Đề xuất]
- **Số bài chạy liền cả chương trình:** tập 1 là 1–80, Vần tập 2 là 81–125 (đúng số in trong sách), **Tập đọc đánh số tiếp 126–171** theo thứ tự trang. Số này chỉ dùng trong dữ liệu (sắp xếp, "đã học tới đâu", mã tranh); bé không thấy số 126.
  - Lý do: công cụ đang dựa vào `lesson_no` để biết chữ nào đã học, để sắp danh sách bài và để đặt mã tranh `img_bNN_*`. Đánh số liền thì giữ được hết, không phải làm hai hệ đếm.
- **Mã bài:** `tv1_t2_b81` … `tv1_t2_b125`, `tv1_t2_b126` … `tv1_t2_b171`. File nguồn `content/src/tv1_t2_bNN.json` (NN có thể là 3 chữ số). Mã tranh `img_b126_*`.
- **Nhãn hiển thị** (trường mới `label`, công cụ tự sinh, có trong `index.json`):
  - bài vần: "Bài 81";
  - tập đọc: "Bài 1" … "Bài 36" theo số in trong mục lục phần Tập đọc, kèm tên bài;
  - câu đố: "Câu đố"; tập chép – chính tả: "Chính tả".
- **Tuần** (trường mới `week`, chỉ có ở phần Tập đọc): 27–33, để danh sách bài chia nhóm theo tuần.

### 4.2 `index.json` và dữ liệu sách [Đề xuất]
- `index.json` giữ một danh sách bài chung. Mỗi dòng thêm `part` (`chu_cai` / `van` / `tap_doc`), `label`, `week` (nếu có). Mọi trường cũ giữ nguyên.
- **File `content/books.json`** (mới, trong git) mô tả các quyển: mã, tên ("Tiếng Việt 1 – Tập một"…), và **Phụ lục dùng cho quyển** (`appendix`). Tập 2 không có Phụ lục bảng chữ cái (tr.139–140 là mục lục), nên `tv1_t2_1996` dùng Phụ lục của `tv1_t1_1990`. Công cụ (`readings.py`, `lesson_notes.py`, `curriculum.py`) đọc file này thay vì ghi cứng `tv1_t1_1990`.
- **Chữ đã học (`curriculum`)** gộp cả hai quyển theo số bài liền: bài 81 coi như đã học mọi thứ của tập 1.
- `LESSON_INDEX.csv` cập nhật các dòng `tv1_t2_1996` (trang, ảnh, mức xác minh) sau khi xác minh từng trang.

### 4.3 Danh sách bài [Đề xuất]
- Ba phần cuộn dọc như hiện nay: **"Chữ cái và âm"** (1–41), **"Vần"** (42–125), **"Tập đọc"** (126–171). Chia phần theo trường `part` trong `index.json`, không theo số bài ghi cứng như `LessonListScreen` đang làm (`lesson_no >= 42`).
- Phần Tập đọc có dòng nhỏ "Tuần 27" … "Tuần 33" trước nhóm bài của tuần.
- Thẻ bài tập đọc: dòng trên là nhãn ("Bài 4", "Câu đố", "Chính tả"), dòng dưới là tên bài, tự xuống dòng; tên dài như "Người nông dân và con gấu" phải đọc được ở thẻ cạnh ≥ 160 [Builder: cỡ chữ, cắt dòng].
- Mở màn thì cuộn sẵn tới bài đang học tới, như hiện nay.

### 4.4 Mở khoá bài [Đề xuất]
- Giữ quy tắc hiện có: bài k mở khi bài k−1 học xong, danh sách liền cả hai quyển.
- **Thêm công tắc "Mở mọi bài" ở màn Phụ huynh, theo từng bé** (mặc định tắt). Bật thì mọi bài mở; tắt thì quay lại quy tắc cũ, không xoá tiến độ.
  - Lý do: bé đã học tập 1 ở trường cần vào thẳng tập 2; chủ dự án cũng cần thử tập 2 mà không phải học hết 80 bài.
  - Màn Phụ huynh có khoá phép tính nên bé không tự bật được.
- Tiến độ cũ không đổi: mã bài tập 1 giữ nguyên, nên hoa và lượt nhầm của bé vẫn còn.

### 4.5 Màn Phụ huynh, Phụ lục, Sổ bé ngoan [Đề xuất]
- **Phụ lục:** app nạp Phụ lục theo `books.json`. Mục "Chú ý và Phụ lục" vẫn là một mục (tr.120–122 tập 1), dùng cho cả hai quyển, vì tập 2 không in lại. Sửa chỗ `AppRoot` và `ParentScreen` đang lấy mã sách từ bài đầu tiên: lấy Phụ lục của quyển có Phụ lục (công cụ chép `books.json` vào trường `books` của `index.json`, nên không cần loại dữ liệu mới).
- **Tiến độ:** màn Phụ huynh liệt kê theo ba phần như danh sách bài. Danh sách "chữ hay nhầm" gom cả hai quyển.
- **Nạp chữ các bài** khi mở màn Phụ huynh: 171 file bài, vẫn qua màn chuyển gà con như hiện nay. Nếu đo thấy chậm rõ rệt thì chỉ nạp bài đã học [Builder].
- **Sổ bé ngoan:** các trang nối tiếp theo thứ tự bài; trang của bài tập đọc ghi nhãn và tên bài. Không đổi cách tính hoa.

## 5. Quy tắc đánh vần cho vần mới của tập 2 [Đề xuất; mọi chuỗi theo mục này gắn `can_duyet` lần đầu]

Tập 2 có ba kiểu vần chưa có ở tập 1. Sách giáo khoa không in cách đánh vần cho các kiểu này (tr.122 tập 1 chỉ nói ia và nguyên âm đôi "dạy như một vần"); sách giáo viên chưa tìm được. Claude chọn theo hai nguyên tắc đã chốt ở tập 1: đọc chữ ghép theo tr.121 ("iê đọc là i-ê"), và **phần đã học thì giữ nguyên một khối**. Riêng vần có âm đệm, **làm theo sơ đồ cấu trúc vần in ở bảng ôn bài 115 (tr.72) và bài 120 (tr.82)**: sách nối âm đệm với âm chính ("o–a", "u–â", "u–yê") rồi mới rẽ ra âm cuối (ghi nhận 5/11/2026 khi chép bài 115; thay cho cách "o – an – oan" đã viết lúc đầu).

| Kiểu vần | Bài | Cách đánh vần vần | Ví dụ |
|---|---|---|---|
| Âm chính + âm cuối hai chữ (ch, ng, nh) | 81–89 | như tập 1 | "a – nhờ – anh" |
| Nguyên âm đôi đứng một mình: ia, ua, ưa | 91 | theo tr.122 | "i – a – ia" |
| Nguyên âm đôi iê/yê, uô, ươ + âm cuối | 92–107 | mảnh đầu là chữ ghép đọc theo tr.121 ("i-ê", "u-ô", "ư-ơ"), rồi âm cuối | "iê – nờ – iên", "ươ – i – ươi" |
| Âm đệm o/u + một nguyên âm: oa, oe, uê, uy, uơ | 109, 116, 117 | âm đệm, rồi nguyên âm | "o – a – oa", "u – i dài – uy" |
| Âm đệm o/u + âm chính + âm cuối | 110–119, 121–122 | **khối âm đệm + âm chính**, rồi âm cuối — theo sơ đồ bảng ôn tr.72 ("o–a" rồi i, n, c, t…) và tr.82 ("u–â" rồi n, t, y; "u–yê" rồi n, t) | "oa – nờ – oan", "uâ – nờ – uân", "uyê – nờ – uyên", "oa – y – oay" |
| Vần có "oo": oong, ooc | 121 | "oo" là một mảnh, rồi âm cuối | "oo – ngờ – oong" |

- Đánh vần tiếng vẫn như tập 1: âm đầu, vần (một khối), tiếng không dấu, dấu, tiếng có dấu. Ví dụ "loa": "lờ – oa – loa"; "khoẻ": "khờ – oe – khoe – hỏi – khoẻ".
- **qu + vần:** giữ cách tập 1, "qu" là âm đầu "quờ": "quê" = "quờ – ê – quê". Khi phần còn lại bắt đầu bằng y ("quyển"), gắn `can_duyet`.
- **gi + vần bắt đầu bằng i/iê** ("giếng"): giữ ghi chú `can_duyet` như tập 1.
- Mỗi kiểu ở bảng trên được nêu một lần trong ghi chú "App khác sách" của bài đầu tiên dùng kiểu đó, để phụ huynh biết đây là cách app chọn.
- Chủ dự án nghe chuỗi đánh vần trong công cụ duyệt ("Nghe theo bài"); thấy sai thì ghi chú, Claude sửa quy tắc rồi dựng lại.

## 6. Phần Vần tập 2 (bài 81–125)

Phần lớn dùng lại đúng các bước của tập 1 (`unit`, `keyword`, `analyze`, `spell`, `words`, `picture`, `sentence`, `rime_table`). Nội dung chép từ trang; tranh cảnh không chữ thành bước tranh có lời dẫn gắn `can_duyet`, như tập 1.

| Loại | Bài | Trong app |
|---|---|---|
| `van_moi` | 32 bài | như tập 1 |
| `on_tap_van` | 85, 90, 95, 99, 103, 108, 115, 120 | bảng ôn vần `rime_table` như tập 1; kiểu bảng nào khác thì xem trang rồi chọn bước gần nhất, ghi `khac_sach` nếu đổi cách trình bày |
| `van_it_dung` | 121, 122 | **bảng vần và câu**: `rime_table` mở rộng, hàng có `sentence` thay cho `word`. Chạm vần thì đánh vần vần; chạm câu thì nghe cả câu, chạm tiếng trong câu thì đánh vần tiếng đó |
| `on_luyen` | 123, 124, 125 | tranh, tên bài thơ, mỗi dòng một bước `sentence` (như đoạn đọc ở tập 1) |

Phần 2 – Luyện tập giữ 4 kiểu của tập 1 và luật giọng miền Nam (mục 5.3 thiết kế MVP). Bài vần âm đệm có thêm cặp dễ nhầm khi **nhìn**: oăn/oan, oăt/oat, oăng/oang… (bài nhìn, không phải bài nghe).

## 7. Phần Tập đọc (tuần 27–33)

### 7.1 Những gì có trên trang (đã xem tr.91–103, 136–138)
- **Bài tập đọc / học thuộc lòng / đọc thêm:** số và tên bài, tranh lớn, bài văn (1–2 đoạn) hoặc bài thơ (2–3 khổ), tên tác giả ("Theo THANH MAI", "PHẠM HỔ"). Bài đọc thêm có dòng "(Bài đọc thêm)", bài học thuộc lòng có "(Học thuộc lòng)".
- **Mục [?] Câu hỏi** (kí hiệu mới, tr.2): 2–4 câu, gồm ba nhóm:
  1. câu hỏi **về chữ**: "Tìm và đọc những tiếng trong bài có vần ươn", "… có âm ch đứng đầu", "Đánh vần và đọc những tiếng có thanh ngã ở câu cuối bài";
  2. câu hỏi **hiểu bài**: "Vì sao cuối năm học, Chim non được thưởng…?";
  3. **"Học thuộc lòng cả bài"** (bài HTL).
  Bài đọc thêm không có câu hỏi.
- **Câu đố** (tr.102, 115, 128): 2–3 câu đố, mỗi câu vài dòng thơ, cuối có "(là cái gì ?)" hay "(là con gì ?)". Đáp án in ở **tr.138 "Trả lời câu đố"**.
- **Tập chép – Chính tả** (tr.96, 103, 109, 116, 122, 129, 137): hai phần, mỗi phần có tên bài (lấy từ bài tập đọc trước đó), "1. Bài viết / Bài chép", "2. Viết đúng" (một dòng từ), "3. Luyện tập": tìm tiếng có vần X trong bài, điền vào chỗ trống (l/n, oa/a, oa/ao…), thêm dấu thanh vào chữ in nghiêng.

### 7.2 Một bài tập đọc trong app [Đề xuất]
Lấy "Trường em" (tr.91) làm ví dụ. Phần 1, đúng thứ tự trang:

1. **Tranh bài** (`picture`): tranh lớn; chạm thì nghe một lời dẫn ngắn (`can_duyet`), như tranh cảnh ở tập 1.
2. **Tên bài** (`title`, bước mới, rất nhẹ): số và tên bài, dòng "(Học thuộc lòng)"/"(Bài đọc thêm)" nếu có. Chạm thì nghe tên bài.
3. **Đọc từng câu** (`sentence`, có sẵn): mỗi câu văn hoặc mỗi dòng thơ một bước. Chạm tiếng nào thì nghe đánh vần tiếng đó; "Nghe cả câu" đọc trơn, tiếng sáng theo giọng; "Con đọc xong rồi" để đi tiếp. Đây là chỗ bé luyện đọc chậm.
   - Câu văn quá dài cho một màn (ví dụ trên khoảng 16 tiếng) thì tách theo dấu phẩy thành nhiều bước, vẫn đúng thứ tự [Builder: ngưỡng].
4. **Đọc cả bài** (`passage`, bước mới): cả bài hiện trên một màn như trang sách (khổ thơ giữ xuống dòng, đoạn văn giữ đoạn), tên tác giả ở cuối. "Nghe cả bài" đọc lần lượt các câu (dùng lại âm thanh câu ở bước 3, không có file riêng), câu đang đọc được tô. Chạm tiếng thì nghe đánh vần. "Con đọc xong rồi" để đi tiếp.
   - Bài dài không vừa một màn thì chia trang theo đoạn hoặc khổ thơ, có nút trang dùng chung [Builder: cỡ chữ tối thiểu, cách chia].
5. **[?] Câu hỏi**, mỗi câu một bước, đúng thứ tự in:
   - **Câu hỏi về chữ → `find_words`** (bước mới): app đọc câu hỏi; bài (hoặc phần bài câu hỏi nói tới, ví dụ "hai câu đầu", "câu cuối bài") hiện bên dưới. Bé chạm các tiếng đúng yêu cầu: tiếng đúng sáng lên, tô phần vần/âm/dấu được hỏi, rồi app đọc (hoặc đánh vần, nếu câu hỏi nói "đánh vần") tiếng đó. Chạm tiếng không đúng thì app chỉ đọc tiếng ấy, không chê, không trừ. Tìm đủ thì khen và đi tiếp. Sai 2 lần liên tiếp thì một tiếng còn thiếu nhấp nháy gợi ý (giống luật gợi ý ở Phần 2).
     - Công cụ tự tìm đáp án từ chữ của bài theo điều kiện (`rime`, `onset`, `tone`, có thể nhiều giá trị: "vần uyên, uynh"). Một tiếng lặp nhiều lần trong bài thì chạm một lần là tính cả. Điều kiện không có tiếng nào khớp thì công cụ báo lỗi khi dựng.
     - Câu hỏi về chữ **ngoài bài** ("Tìm tiếng ngoài bài có vần…") không có đáp án cố định → làm như câu hỏi hiểu bài.
   - **Câu hỏi hiểu bài → `question`** (bước mới): câu hỏi hiện to, app đọc; dưới có dòng "Con trả lời cùng bố mẹ nhé" và nút "Con trả lời rồi". Không có đáp án, không chấm. Câu hỏi có nhắc lại một câu trong bài thì chạm được câu đó để nghe lại [Builder: có làm hay không].
   - **"Học thuộc lòng cả bài" → `memorize`** (bước mới): bài thơ hiện đủ; bé bấm "Ẩn bớt" thì một số tiếng thành ô trống (lần 1 ẩn khoảng một phần ba, lần 2 khoảng hai phần ba, lần 3 chỉ còn tiếng đầu mỗi dòng). Chạm ô trống thì hiện lại và nghe tiếng đó. "Nghe cả bài" luôn có. "Con thuộc rồi" để đi tiếp, bấm được ở bất cứ mức nào. Chọn tiếng ẩn cố định trong dữ liệu (công cụ sinh, không ngẫu nhiên) để bé lặp lại được.
6. **Phần 2 – Luyện tập** (5–8 lượt), lấy từ chữ của chính bài, theo 4 kiểu có sẵn:
   - nghe và chọn tiếng (ưu tiên các tiếng có vần/âm mà câu hỏi nhắc tới);
   - kéo vần hoặc âm để ghép tiếng của bài;
   - nhìn chữ mẫu rồi kéo đúng dấu hỏi/ngã (khi bài có cặp đó);
   - nghe và chọn tranh chỉ dùng khi có tranh phù hợp (câu đố).
   Luật giọng miền Nam và luật "phương án nhiễu chỉ lấy từ chữ đã học" giữ nguyên.

Bài học thuộc lòng và bài đọc thêm đi cùng đường, chỉ khác bước 5 (HTL có `memorize`; đọc thêm không có câu hỏi).

### 7.3 Trang câu đố [Đề xuất]
- Phần 1: tên trang "Câu đố"; mỗi câu đố là các bước `sentence` theo dòng, dòng "(là cái gì ?)" là một bước câu riêng. Sau mỗi câu đố có bước **`riddle_answer`** (bước mới, nhẹ): 3 tranh để bé đoán; chọn xong thì hiện đáp án đúng theo tr.138, tranh và chữ ("Cái tẩy"), app đọc đáp án. Chọn sai không chê, cho chọn lại; sai 2 lần thì gợi ý.
- Phương án nhiễu là các đáp án câu đố khác và tranh đã có của bài trước [Builder chọn, ưu tiên tranh đã có để bớt tranh vẽ mới].
- Tr.138 không thành bài riêng; đáp án ghi trong dữ liệu câu đố kèm nguồn "tr.138". Đáp án có hai cách ("Trâu (hoặc bò)", "Bút chì (viết chì)") thì tranh vẽ theo cách đầu, chữ hiện đúng như sách.
- Phần 2: nghe câu đố rồi chọn tranh đáp án, như bài 80.
- Tranh đáp án vẽ mới, gắn `can_duyet` (sách không có tranh này).

### 7.4 Trang Tập chép – Chính tả [Đề xuất]
Đặt tên trong danh sách bài là "Chính tả" (nhãn) với tên bài là hai tên bài trên trang, ví dụ "Chim non chăm học – Dưới ánh trăng". Mỗi phần (Tập chép, Chính tả) theo thứ tự trang:

1. **Tên phần và tên bài** (`title`): "Tập chép (Nhìn bảng): Chim non chăm học".
2. **"1. Bài viết"**: không làm (phần viết). Thay bằng một dòng nhắc "Phần này con viết vào vở cùng bố mẹ" và ghi chú `khac_sach` [Đề xuất: hiện dòng nhắc để trang vẫn đủ mục].
3. **"2. Viết đúng"**: các từ thành bước `words` (chạm để nghe đánh vần, đọc trơn). Bé không viết, nhưng đọc kĩ các chữ dễ sai.
4. **"3. Luyện tập"**, mỗi dòng một bước:
   - "Tìm hai tiếng có vần oc…" → `find_words` trên bài tập đọc gốc, điều kiện như câu hỏi về chữ. Sách nói "hai tiếng": bé tìm đủ số sách nói thì xong (không bắt tìm hết).
   - "Điền vào chỗ trống (l hoặc n)" → `fill_blank` (bước mới): mỗi chỗ trống là một thẻ tiếng có ô trống ("…on gạo"), bên dưới hai thẻ lựa chọn đúng như sách ("l", "n"). Bé kéo (hoặc chạm) thẻ vào ô; đúng thì tiếng hiện đủ và app đọc cả từ; sai thì thẻ trượt về, app đọc thử tiếng bé ghép nếu đó là tiếng có nghĩa, không thì chỉ trượt về [Builder]. Đáp án do Claude điền (sách không in đáp án) và gắn `can_duyet`.
   - "Thêm dấu thanh thích hợp vào những chữ in nghiêng" → `fill_blank` dạng dấu: chữ in nghiêng hiện có ô dấu, các thẻ dấu là 5 dấu; đáp án lấy từ bài gốc.
5. Phần 2: nghe và chọn tiếng từ các từ "Viết đúng", 4–6 lượt.

### 7.5 Ghi chú cho phụ huynh [Đề xuất, theo cách tập 1]
- `sach`: chú thích in trên trang (rà đủ 72 ảnh khi chép bài; chép đúng chỗ sách in).
- `ten_doc`: công cụ tự sinh cho bài dạy chữ ghép đọc theo tr.121 (iê, yê, uô, ươ) ở bài đầu tiên có chữ đó.
- `khac_sach`: mỗi chỗ app làm khác trang, ít nhất:
  - quy tắc đánh vần app tự chọn (mục 5), ở bài đầu tiên dùng mỗi kiểu;
  - câu hỏi hiểu bài trả lời miệng, app không chấm;
  - bước "Ẩn bớt" để học thuộc lòng;
  - phần Bài viết / Bài chép không có trong app; điền chỗ trống bằng kéo thẻ; đáp án điền chỗ trống do app soạn;
  - đáp án câu đố lấy từ tr.138 và hiện ngay sau câu đố;
  - câu dài tách thành nhiều bước theo dấu phẩy (bài nào có).

## 8. Màn và bước mới (Unity)

| Bước | Dữ liệu chính (công cụ sinh) | Ghi chú |
|---|---|---|
| `title` | chữ tên bài, dòng phụ, audio | rất nhẹ, dùng `SentenceView` cũng được nếu đủ [Builder] |
| `passage` | các đoạn/khổ, mỗi câu có chữ, audio, mốc tiếng; tác giả | dùng lại âm thanh câu của `sentence` |
| `find_words` | câu hỏi + audio; chữ phần bài hiện ra; danh sách vị trí tiếng đúng; vùng tô; số cần tìm (mặc định: tất cả) | mỗi tiếng có chuỗi đánh vần |
| `question` | câu hỏi + audio | không chấm |
| `memorize` | các dòng thơ; 3 mức ẩn (danh sách vị trí) | |
| `fill_blank` | các mục: chữ có ô trống, lựa chọn, đáp án, audio từ đủ | dạng chữ và dạng dấu |
| `riddle_answer` | 3 phương án tranh, đáp án, chữ đáp án, audio | |

- Kí hiệu **[?] Câu hỏi**: thêm biểu tượng tạm `img_chung_cau_hoi` vẽ bằng `ui_icons.py` như ● và ⌂; hình chính thức thay sau theo mã. `SystemAssets.ForMarker` nhận thêm kí hiệu này.
- Mọi màn mới theo phong cách đã chốt ở thiết kế giao diện: thẻ viền mực, bóng gạch, tiếng động chạm, gà con, chấm tiến độ. Bố cục chi tiết là [Builder]; giao diện do Claude tự làm, không giao worker [Chốt].
- Cỡ chữ của `passage`, `find_words`, `memorize` phải đọc được ở cả hai khung hình thử (1600×720, 1440×1080). Nếu chữ phải nhỏ hơn mức tối thiểu thì chia trang, không thu nhỏ thêm.

## 9. Âm thanh [Chốt: HoaiMy, như tập 1]
- Mọi mã mới tạo bằng `python -m tapdoc tts` giọng HoaiMy, `cho_duyet`.
- Loại mới trong danh mục: `hoi` (câu hỏi) dùng mặc định như `cau`; tên bài và tên tác giả là `cau`. Lời dẫn tranh, khen, hướng dẫn như cũ. Mã theo mục 7.4 thiết kế MVP: `hoi_b126_01`, `cau_b126_03`.
- Mảnh chữ ghép mới (`van_iee`… theo quy ước Telex của `ids.py`) đọc theo tr.121; chủ dự án chỉnh cách đọc trong công cụ duyệt nếu bộ đọc đọc chưa đúng.
- Không đụng các mã tập 1 đã có (dùng chung theo mã).

## 10. Tranh
- **Tranh in sẵn trong sách được vẽ trước [Chốt 5/11/2026]:** session gốc chốt mã và mô tả rồi vẽ trước khi có nội dung. Bài 81–90: 24 mã ở [2026-11-05-tranh-tap-2-dot-1.md](../notes/2026-11-05-tranh-tap-2-dot-1.md) (session gốc gọi là "tranh đợt 1"). Khi chép bài, `images` dùng **đúng các mã và mô tả đó**; không đặt mã khác cho cùng tranh. Nếu session gốc gửi thêm danh sách cho các bài sau thì làm như vậy.
- Tranh **vẽ thêm** (từ dùng trong lượt nghe chọn tranh mà sách không có tranh, tranh đáp án câu đố…) do session này đặt mã theo quy ước `img_bNN_<telex>` và báo session gốc.
- Session gốc giữ tranh tập 2 ngoài repo và chỉ nhập sau khi bài đã dựng. Session này không mở công cụ duyệt (chủ dự án đang dùng để duyệt tập 1) [Chốt 5/11/2026].
- Công cụ sinh phiếu vẽ như tập 1 (`content/requests/images_tv1_t2_bNN.md`). Mỗi bài vần thường 2–4 tranh; mỗi bài tập đọc 1 tranh lớn theo tranh sách; câu đố có tranh đáp án và tranh nhiễu nếu thiếu; tập chép – chính tả không có tranh.
- Lúc chưa có tranh, app dùng tranh tạm như hiện nay khi file thiếu (chạy `validate --allow-missing` trong lúc làm).

## 11. Bàn giao với các session khác [Chốt 5/11/2026]
Xong mỗi đợt (nội dung `page_verified`, `python -m tapdoc build` và `python -m tapdoc requests` đã chạy), nhắn session gốc: đợt nào, bài nào, bao nhiêu mã tranh `chua_co`, và **tách rõ** mã đã có trong danh sách vẽ trước với mã vẽ thêm. Session gốc vẽ và nhập tranh rồi báo lại; session này chạy lại `validate` không `--allow-missing` cho đợt đó.

## 12. Kiểm tra
- **Python:** test cho quy tắc đánh vần mới (mỗi dòng bảng mục 5), các bước mới của `build`, `books.json`, `curriculum` gộp hai quyển, `label`/`part`/`week` trong `index.json`, `find_words` báo lỗi khi không có đáp án. **Test hồi quy:** dựng lại 80 bài tập 1 cho ra file y hệt bản đang commit.
- **Unity EditMode:** đọc được các bước mới, `index.json` hai quyển, chia phần danh sách bài theo `part`, mở khoá với công tắc "Mở mọi bài", Phụ lục theo `books.json`.
- **Unity PlayMode** chỉ chạy `--filter` theo lớp test của từng màn mới. Không chạy `MvpEndToEndTests` hay toàn bộ PlayMode khi chủ dự án chưa nói "test all" [Chốt].
- `validate` báo `OK` (với `--allow-missing` khi tranh chưa về).
- Claude viết và review mọi test; nếu có giao worker thì worker chỉ viết code đơn giản cho test chạy xanh [Chốt].

## 13. Chia đợt [Đề xuất]

| Đợt | Nội dung | Kết thúc khi |
|---|---|---|
| **T2-1** | Hai quyển trong một app (mục 4), toàn bộ quy tắc đánh vần ở mục 5 (một chỗ, test một lần); nội dung bài 81–99 | 19 bài `page_verified`, âm thanh tạo xong, phiếu vẽ đã bàn giao, test liên quan xanh, commit |
| **T2-2** | Bảng vần và câu; nội dung bài 100–125 | 26 bài như trên |
| **T2-3** | Các bước Tập đọc mới (mục 7–8); nội dung tuần 27–30 (mục 126–151) | 26 mục như trên, màn mới có test PlayMode lọc riêng |
| **T2-4** | Nội dung tuần 31–33 (mục 152–171); trau chuốt màn mới theo bài dài nhất; cập nhật `BOOK_CATALOG.md`, `LESSON_TYPES.md`, ghi chú tiếp tục | 20 mục như trên; báo chủ dự án thử cả quyển |

Đợt đặt tên **T2-1 … T2-4** để không lẫn với đợt 1–3 của tập 1 và với "tranh đợt 1" của session gốc.

- **Làm liền các đợt, không dừng chờ duyệt** [Đề xuất, theo lời chủ dự án "làm thành kết quả rồi test lại sau"]. Chủ dự án góp ý lúc nào thì Claude sửa lúc đó; quy tắc đánh vần đổi thì dựng lại bài và chạy lại `tts` cho các mã bị ảnh hưởng (tự động, không tốn công tay).
- **Thử app trên máy này.** Chỉ đóng gói media (`run_unity_media.py pack`, commit `media_lock.json`) **một lần sau đợt T2-4**, hoặc sớm hơn khi chủ dự án yêu cầu; chủ dự án tự đưa gói lên Drive.
- **Claude tự làm**, không giao worker theo mặc định [Đề xuất, như dự án đọc dữ liệu]. Phần công cụ Python có phạm vi rõ và test sẵn thì hỏi chủ dự án trước khi giao.

Mỗi đợt một hoặc vài commit rõ ràng trên `main`, `git add` theo đường dẫn; chủ dự án tự push. Sau mỗi đợt chủ dự án có thể thử ngay bằng công tắc "Mở mọi bài".

## 14. Builder tự quyết
- Bố cục, cỡ chữ, hiệu ứng của các màn mới, trong khuôn phong cách đã chốt.
- Ngưỡng tách câu dài, cách chia trang `passage`.
- Thuật toán chọn tiếng ẩn của `memorize` (cố định, lặp lại được).
- Số lượt và kiểu lượt Phần 2 của từng bài, trong khoảng ở mục 7.2.

## 15. Việc để sau
- Giọng người thật, giọng miền Nam (như tập 1).
- Đọc to và chấm bằng micro cho câu hỏi hiểu bài.
- Tranh động cho tranh tập 2 (session tranh động làm theo lịch của nó).
- Truyện đọc 1, lớp 2.

## 16. Kết quả (5/11/2026)

- **Nội dung:** đủ 91 mục `page_verified` (45 bài vần, 46 mục Tập đọc), chép từ ảnh 003–069. Mục lục ghi "Chị Võ Thị Sáu" nhưng trang in "Võ Thị Sáu"; bài "Chim sâu" là bài học thuộc lòng (trang in "(Học thuộc lòng)", CSV ghi sai `tap_doc`, đã sửa).
- **Quy tắc vần có âm đệm** đổi theo sơ đồ của chính sách (mục 5): "oa – nờ – oan".
- **Khác kế hoạch:** Phần 2 của bài tập đọc có 6 lượt (không phải 5–8) để giữ một luật chung cho cả app; câu "tìm tiếng... và viết ra" mà bài không đủ tiếng thì thành câu hỏi trả lời miệng; bài sửa chữ viết sai (tr.122) thành các bước điền chỗ trống.
- **Test:** Python đều đạt, trừ 2 test CLI của `validate` (cảnh báo media khác gói do chủ dự án đang tạo lại âm thanh tập 1); test hồi quy: dựng lại 80 bài tập 1 ra file y hệt. Unity EditMode 129/129; PlayMode chạy lọc theo lớp của các màn mới (danh sách bài, Phụ huynh, các màn Tập đọc, bảng vần) đều đạt; chưa chạy trọn PlayMode.
- **Còn lại:** âm thanh HoaiMy đang tạo; tranh do session gốc vẽ; đóng gói media sau khi đủ.
