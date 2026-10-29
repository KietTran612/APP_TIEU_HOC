# Thiết kế: App tập đọc theo SGK Tiếng Việt 1 (sách cũ) — 3 bài mẫu và bản đầu tiên

> **Ngày:** 28/10/2026 · **Trạng thái:** đã qua vòng đọc kiểm tra, chờ chủ dự án duyệt · Repo: https://github.com/KietTran612/APP_TIEU_HOC, chỉ dùng branch `main`, gom thành 1 commit khi push
> **Tài liệu gốc:** [PROJECT_INIT_APP_TAP_DOC_SGK_CU.md](../../../PROJECT_INIT_APP_TAP_DOC_SGK_CU.md)
> **Kiểm kê nguồn:** [BOOK_CATALOG.md](../../source-inventory/BOOK_CATALOG.md) · [LESSON_INDEX.csv](../../source-inventory/LESSON_INDEX.csv) · [LESSON_TYPES.md](../../source-inventory/LESSON_TYPES.md)
>
> Cách đánh dấu trong tài liệu:
> - **[Chốt]**: chủ dự án đã quyết.
> - **[Đề xuất]**: người viết tự quyết. Chủ dự án có thể đổi; builder không cần hỏi lại.
> - **[Builder]**: builder tự quyết.

---

## 1. Mục đích và lý do

Đây là app giúp bé **tập đọc tiếng Việt** theo đúng lộ trình học vần của **SGK Tiếng Việt 1 bản cũ** (Tập 1 NXB Giáo dục 1990, Tập 2 chỉnh lí 1994). Trục của mỗi bài là **đánh vần theo quy ước của chính bộ sách**: âm → vần → tiếng → từ → câu.

App không đưa trang scan vào. Mỗi bài được soạn lại thành các màn có tranh mới, giọng đọc mẫu, và thao tác chạm hoặc kéo thả.

- **Người học:** bé tự học ở nhà, có bố mẹ ngồi cạnh. Độ tuổi từ lúc chuẩn bị vào lớp 1 đến lớp 1–2. Người tải app là phụ huynh. *(Người viết đoán; chủ dự án không sửa.)*
- **Lý do chọn sách cũ:** phụ huynh tin cách học vần chậm mà chắc của sách cũ giúp bé đọc vững. *(Người viết đoán; chủ dự án không sửa.)*
- **Bối cảnh:** dự án cá nhân theo hướng startup nhỏ. Chủ dự án làm một mình và đã từng làm một app học tiếng Nhật bằng Unity. App này **làm mới hoàn toàn**, không dùng lại code hay asset của app tiếng Nhật [Chốt].

## 2. Mục tiêu, việc không làm, và điều coi là thất bại

### Mục tiêu
1. **3 bài mẫu [Chốt]:** TV1 T1 bài 4 (dấu thanh), bài 13 (âm mới u, ư), bài 42 (vần mới an). Mỗi bài thuộc một loại, để thử đủ các cách dạy khác nhau.
2. **Bản đầu tiên [Chốt]:** **TV1 T1 bài 1–17** chạy hoàn chỉnh. Giai đoạn này làm và thử trên máy tính, trong Unity Editor. Chỉ build Android khi chủ dự án yêu cầu [Chốt].
3. Bé hoàn thành mỗi bài chỉ bằng chạm và kéo thả. Lời đánh vần đúng quy ước sách ở tr.120–122.
4. Nội dung bài, hình và âm thanh **tách khỏi code**. Thay một file âm thanh hay hình bằng bản tốt hơn mà **không phải sửa code** [Chốt — vì âm thanh hiện chỉ là bản tạm]. Cách thay: ghi đè file có cùng `id` trong project rồi chạy lại (hoặc build lại, khi đã có bản build). Không cần thay file ngay trên điện thoại [Đề xuất].
5. Cấu trúc dữ liệu chạy được cho cả phần Vần ngay từ đầu. Bài 42 nằm trong nhóm bài mẫu để kiểm chứng điều này.

### Không làm trong bản đầu tiên [Chốt]
- Tập viết, tô chữ (các mục ▨ "Em viết", Tập chép – Chính tả).
- Micro, chấm phát âm.
- Tài khoản, đồng bộ, thu phí, quảng cáo.
- Game khám phá, nông trại, cày cấp, chiến đấu.
- iOS (để sau, khi có máy Mac hoặc dịch vụ build trên mây).
- Phần Vần: bài 42 chỉ có trong bản mẫu, không nằm trong bản đầu tiên [Chốt].
- Lớp 2–5 và phần Tập đọc của TV1 Tập 2.
- Ảnh động (chỉ có hiệu ứng nhẹ do Unity làm).
- Phát hành: lên Google Play, chính sách quyền riêng tư, khai báo cho app trẻ em, ảnh cửa hàng, khóa ký phát hành. Chủ dự án sẽ tính khi app hoàn thành [Chốt].
- Build Android (APK) khi chủ dự án chưa yêu cầu [Chốt].

### Coi là thất bại, dù app vẫn chạy
- **Phần Tập đọc lệch khỏi trang SGK:** có thêm hoạt động không có trên trang, hoặc đổi thứ tự trang. Được đổi cách tương tác, không được đổi nội dung và thứ tự.
- **Đánh vần sai quy ước sách.** Ví dụ đọc tên chữ "bê" thay cho âm "bờ", hoặc tách vần khi đánh vần tiếng ("sờ – a – nờ – san" thay vì "sờ – an – san"). Điều này nói về **chữ và thứ tự đánh vần ghi trong dữ liệu**. Chất lượng giọng đọc tạm của ChatGPT thì chấp nhận được cho tới khi thay bằng bản tốt hơn [Chốt: dùng âm thanh tạm].
- **Ảnh scan gốc lọt vào app** hoặc vào gói phát hành.
- **Bé bị phạt hay bị áp lực khi sai:** trừ điểm, đếm giờ, âm thanh chê.
- **Nội dung bài viết cứng trong code.**

## 3. Ràng buộc

| Ràng buộc | Giá trị |
|---|---|
| Engine | **Unity 6.6 (`6000.6.5f1`), 2D**, bản đã cài sẵn trên máy làm việc [Chốt]. Kiểm tra ngày 28/10/2026: bản cài này mới có module **WebGL** và **Windows**, **chưa có Android Build Support**. Giai đoạn này chưa cần module đó. Khi chủ dự án yêu cầu build, cài thêm module này (kèm OpenJDK, Android SDK & NDK) qua Unity Hub |
| Nền tảng | App nhắm tới **Android trước** [Chốt]; chạy cả điện thoại lẫn máy tính bảng. Máy làm việc là Windows |
| Cách thử | **Hiện tại làm và thử trên máy tính** [Chốt]. Test tự động chạy trong Unity Editor. Đến bước chủ dự án thử, Claude **build bản Windows và mở lên** cho chủ dự án, ở khung ngang cỡ điện thoại (1600×720) và cỡ máy tính bảng (1440×1080) [Chốt]. Thao tác phải chạy được với cả chuột lẫn cảm ứng, để khi build Android không phải làm lại [Đề xuất] |
| Hướng màn hình | **Ngang** [Chốt] |
| Mạng | **Không cần mạng.** Toàn bộ nội dung bài 1–17 đóng gói sẵn trong app [Chốt] |
| Lưu trữ | Tiến độ lưu trên máy, **không có tài khoản** [Chốt]. Không lưu thông tin định danh trẻ: chỉ tên gọi ở nhà và hình đại diện do bé chọn |
| Chữ tiếng Việt | Font có đủ dấu. Mọi chuỗi chuẩn hóa **Unicode NFC** trước khi hiển thị hoặc so sánh |
| Hình | Tạo bằng **ChatGPT trong dự án "Kiet_1"** của chủ dự án [Chốt], phong cách **giống tranh SGK 1990** [Chốt] |
| Âm thanh | **Giọng nữ miền Nam** [Chốt]. **Tạm dùng âm thanh do ChatGPT tạo** [Chốt]; sau này thay bằng bản tốt hơn |
| Người tạo asset | **Claude tạo toàn bộ tranh và âm thanh** trong ChatGPT [Chốt], chủ dự án duyệt. Cách làm ở mục 8 |
| Code | Viết mới, không dùng lại app tiếng Nhật [Chốt]. Ưu tiên các gói có sẵn của Unity; dùng gói ngoài miễn phí hay không là [Builder]; không mua gói trả phí [Đề xuất] |

## 4. Nguồn nội dung và quy tắc dùng nguồn

- **Nguồn chính:** TV1 T1 (1990) trong repo `giangtv134/sach-giao-khoa-viet-nam`, commit `7fadf3e`. Danh sách bài, trang và ảnh scan tương ứng có trong `LESSON_INDEX.csv`.
- **Ảnh scan chỉ để tham chiếu nội bộ**, dùng để chép nội dung bài và để biết tranh cần vẽ gì. Ảnh scan không được nằm trong project Unity.
- **Chữ trong bài** (từ khóa, từ ứng dụng, câu, đọc thêm) chép đúng như trang sách và ghi trang nguồn [Chốt — chủ dự án chấp nhận rủi ro bản quyền của văn bản và của tranh vẽ lại].
- **Tranh vẽ mới bằng ChatGPT** theo nội dung tranh gốc [Chốt].

## 5. Cấu trúc một bài học [Chốt]

Mỗi bài có 3 phần, theo thứ tự cố định:

1. **Phần 1 – Tập đọc:** bám sát trang SGK, đúng thứ tự trên trang. Đánh vần là trục chính.
2. **Phần 2 – Luyện tập:** vài bài tập cơ bản, chỉ dùng nội dung của bài này và các bài trước.
3. **Kết thúc:** sao hoặc hình dán, mở khóa bài sau, ghi lại chỗ bé nhầm để ôn.

Bé đọc xong Phần 1 thì mới sang Phần 2.

### 5.1 Quy tắc đọc và đánh vần

Nguồn: [LESSON_TYPES.md](../../source-inventory/LESSON_TYPES.md), các mục "Bảng âm" và "Chú ý tr.122".

- **Âm** đọc theo cột "ghi âm" ở tr.120–121: b "bờ", c "cờ", d "dờ", đ "đờ", nh "nhờ"…
- **Âm có nhiều cách ghi** đọc theo tên riêng ở tr.122 **[Chốt tạm; cần duyệt]**:
  - k "ca", q "cu", gh "gờ kép", g "gờ đơn", ng "ngờ đơn", ngh "ngờ kép", gi "di", i "i ngắn", y "i dài".
  - Tổ hợp qu đọc là "quờ".
- **Đánh vần vần trước, đánh vần tiếng sau** [Chốt]. Ví dụ: "a – nờ – an" → "an"; rồi "sờ – an – san – huyền – sàn" → "sàn".
- **Khi đánh vần tiếng, vần giữ nguyên một khối,** không tách ra lại [Chốt].
- **Dấu thanh** đọc theo thứ tự: tiếng không dấu → tên dấu → tiếng có dấu. Ví dụ "cư – hỏi – cử".
- **Ở bài 1–41,** vần chỉ là một nguyên âm, nên bước đánh vần vần chỉ là đọc nguyên âm đó.
- **Thứ tự các bước [Chốt tạm; cần duyệt]:** phân tích từ trên xuống theo cột in trên trang (từ khóa → tiếng khóa → âm/vần), rồi đánh vần từ dưới lên (âm/vần → tiếng → từ khóa).
- **Tiếng không đánh vần thẳng được** theo quy tắc chung (ví dụ "gì") thì gắn nhãn `can_duyet` trong dữ liệu **[Chốt tạm]**. Chủ dự án sẽ duyệt lại từng bài.

### 5.2 Phần 1 theo từng loại bài

Bản đầu tiên (bài 1–17) có 3 loại bài: `am_moi`, `dau_thanh`, `on_tap_am`. Bài mẫu 42 thuộc loại `van_moi`.

Hai kí hiệu dùng trong sách và trong tài liệu này: **●** là "Em đọc", **⌂** là "Luyện tập ở lớp và ở nhà". Trong app, hai kí hiệu này hiện thành hình nhỏ đặt trước mục tương ứng, giống trong sách [Chốt].

**Mọi thứ in trên trang, trừ phần viết, đều đưa vào bài** [Chốt]. Kể cả tranh không có chữ: app hiện tranh, bé chạm thì nghe một lời dẫn ngắn. Lời dẫn do người soạn đề xuất và gắn nhãn `can_duyet`.

#### `am_moi` — bài âm mới

Gồm bài 1–3, 5, 8–10, 12–16. Các bước dưới đây lấy Bài 13 (u, ư) làm ví dụ:

1. **Chữ mới:** chữ "u" hiện to; bé chạm vào để nghe âm "u".
2. **Tranh và từ khóa:** tranh bé đánh đu; bé chạm tranh thì nghe "cái đu".
3. **Phân tích:** ba dòng "cái đu", "đu", "u" xếp dọc như trong sách; bé chạm dòng nào thì nghe dòng đó.
4. **Đánh vần:**
   - App đánh vần mẫu "đờ – u – đu": thẻ **đ** và thẻ **u** sáng lên, rồi nhập lại thành **đu**.
   - Bé tự chạm các thẻ theo đúng thứ tự.
   - App đọc từ khóa "cái đu".
5. **Âm thứ hai (nếu bài có):** lặp lại bước 1–4 với "ư" và từ khóa "cử tạ". Khi đánh vần, bé **kéo dấu hỏi** đặt lên "cư" để thành "cử".
6. **Từ ứng dụng** (có tranh): "đu đủ", "củ từ". Bé đánh vần từng tiếng, rồi đọc trơn cả từ.
7. **● Câu ứng dụng:** "má có củ từ".
   - Bé chạm vào tiếng nào thì nghe đánh vần tiếng đó.
   - Nút "Nghe cả câu" đọc trơn cả câu; từng tiếng sáng lên theo giọng đọc.
   - Bé bấm "Con đọc xong rồi" để đi tiếp.
8. **⌂ Đọc thêm:** dãy tiếng và từ trên trang. Bé chạm từng thẻ để nghe đánh vần và đọc trơn.

Mục nào trang sách không có thì bỏ qua. Ba bài đầu có biến thể riêng:

- **Bài 1 (o):** chưa có chữ để đọc. Chỉ có chữ o, âm "o", tranh gà gáy "ò ó o" và các tranh có âm o.
- **Bài 2 (c):** lần đầu ghép tiếng, đánh vần "cờ – o – co", từ khóa "kéo co".
- **Bài 3 (a):** đánh vần "cờ – a – ca", từ khóa "cái ca".

#### `dau_thanh` — bài dấu thanh (bài 4, 6)

1. **Tiếng gốc:** bé đánh vần và đọc tiếng gốc (ví dụ "ca").
2. **Giới thiệu dấu:** từng dấu hiện ra với hình dấu và tên dấu.
3. **Ghép dấu:** bé kéo dấu đặt lên tiếng gốc; app đọc "ca – huyền – cà", và tranh tương ứng hiện ra (quả cà, con cá).
4. **Bảng 5 dấu (riêng bài 6):** có tiếng gốc "đo" và 5 ô trống. Bé kéo từng dấu vào ô; app đọc kết quả: đò, đó, đỏ, đõ, đọ.
5. **Tranh không có chữ** (bài 4: tranh 5 bạn gái múa): hiện tranh, bé chạm thì nghe lời dẫn.
6. **Phần đọc của mục ●▨ và ⌂:** "có cà, có cá"; "đo, đò, đó, đỏ, đõ, đọ / đo đỏ, dạ".

#### `on_tap_am` — ôn tập âm (bài 7, 11, 17) [Đề xuất]

1. **Khung chữ và dấu:** khung các chữ và dấu đã học, giống trang sách. Bé chạm từng chữ để nghe âm.
2. **Bảng ghép theo trang sách** (phụ âm → nguyên âm → các tiếng có dấu):
   - Bé chọn phụ âm rồi chọn nguyên âm; app đánh vần "cờ – o – co".
   - Bé kéo dấu vào; app đọc "co – sắc – có".
3. **Đọc các tiếng** in trên trang, theo đúng thứ tự.

Bài 11 và 17 chưa được xem tận trang. Builder (hoặc người soạn dữ liệu) cần xem trang gốc và giữ đúng nội dung.

#### `van_moi` — vần mới (bài mẫu 42)

1. **Vần mới "an":** đánh vần "a – nờ – an" (thẻ **a** và **n** nhập thành khối **an**), rồi đọc trơn "an".
2. **Tiếng khóa "sàn":** đánh vần "sờ – an – san"; bé kéo dấu huyền đặt lên; app đọc "huyền – sàn".
3. **Từ khóa:** tranh nhà sàn và tiếng "nhà sàn". Cột "nhà sàn / sàn / an" hiện giống như trong sách.
4. **● Từ ứng dụng:** "lan can, đàn ngan, bàn ghế". Bé đánh vần các tiếng có vần an, rồi đọc trơn cả từ.
5. **Chú thích phương ngữ:** khi bé chạm tranh con ngan, hiện chú thích "ngan: ở phía Nam gọi là vịt xiêm".

### 5.3 Phần 2 – Luyện tập [Chốt]

Có 4 kiểu bài tập. Mỗi bài chọn những kiểu hợp với nội dung, tổng cộng khoảng 6–10 lượt.

| Kiểu | Cách làm | Ví dụ ở Bài 13 |
|---|---|---|
| Nghe và chọn chữ | App đọc một âm; bé chạm đúng thẻ trong 3 thẻ | Nghe "u" → chọn u |
| Phân biệt chữ dễ nhầm | 5–6 lượt nhanh với cặp chữ trông giống nhau, hoặc cặp dấu | u và ư. Ở bài dấu thanh: nhìn chữ mẫu rồi kéo đúng dấu hỏi hay dấu ngã |
| Kéo thả để ghép tiếng | Kéo âm, vần hoặc dấu vào chỗ trống; ghép đúng thì app đọc cả tiếng | "củ t_" ← "ừ" |
| Nghe và chọn tranh | App đọc một từ; bé chọn đúng tranh trong 2–3 tranh | "củ từ" |

- **Phương án nhiễu** chỉ lấy từ chữ và từ **đã học tới bài này**, theo thứ tự trong `LESSON_INDEX.csv`.
- **Cặp âm mà giọng miền Nam đọc giống nhau không làm phương án nhiễu của nhau trong bài nghe** [Đề xuất]. Đó là hỏi/ngã, và về sau d/gi/v, s/x, ch/tr, vần cuối n/ng và t/c. Lý do: bé có thể chọn đúng mà vẫn bị chấm sai. Các cặp này được luyện bằng bài **nhìn**, ví dụ nhìn chữ mẫu "đõ" rồi kéo đúng dấu ngã vào "đo".
- **Khi bé sai:** không trừ điểm. Cho nghe lại và thử lại; sai 2 lần thì app gợi ý đáp án đúng.

### 5.4 Kết thúc bài và ôn tập

- **Phần thưởng:** sao hoặc hình dán, nhẹ nhàng, không xếp hạng.
- **Mở khóa:** bài mở theo thứ tự.
- **Ghi lỗi:** app ghi lại các lượt bé nhầm, ví dụ nhầm u với ư.
- **Ôn lại:** trang chủ có mục "Ôn lại", lấy đúng những lượt bé đã nhầm cho làm lại theo các kiểu ở 5.3 [Chốt: "ghi lại chỗ bé nhầm để ôn"].

## 6. Các màn hình của app [Chốt]

| Màn | Nội dung |
|---|---|
| Chọn bé | Một máy có nhiều hồ sơ bé (tên gọi ở nhà và hình đại diện) |
| Danh sách bài | Bài 1–17 (bản mẫu: bài 4, 13, 42), có khóa và số sao; có mục "Ôn lại" |
| Học bài | Phần 1 → Phần 2 → Kết thúc; luôn có nút nghe lại |
| Kết quả | Sao hoặc hình dán; nút "Học bài tiếp" |
| Phụ huynh | Khóa bằng một phép tính đơn giản; xem tiến độ và những chữ bé hay nhầm |

- **[Builder]:** bố cục chi tiết, màu sắc, kích thước nút và hiệu ứng.
- **Bắt buộc:** nút và thẻ phải to, vừa ngón tay trẻ 5–6 tuổi; mỗi màn chỉ có một việc.
- **Nhân vật dẫn dắt:** bản mẫu chưa có, chỉ có giọng hướng dẫn [Đề xuất]. Sẽ quyết sau khi thử bản mẫu.

## 7. Âm thanh

### 7.1 Ghép lời đánh vần từ các mảnh [Đề xuất]

App **không thu cả câu đánh vần**. App phát lần lượt từng mảnh và làm sáng chữ tương ứng. Ví dụ "đờ – u – đu" là ba file: "đờ", "u", "đu", cách nhau khoảng nửa giây. Mỗi mảnh chỉ có một file và dùng chung cho mọi bài.

| Loại (`kind`) | Ví dụ | Ghi chú |
|---|---|---|
| `am` | "đờ", "cờ", "ca" (k) | Đọc theo tr.120–122 |
| `van` | "u", "an" | Gồm cả nguyên âm đứng một mình |
| `dau` | "huyền", "sắc", "hỏi", "ngã", "nặng" | |
| `tieng` | "đu", "cư", "cử" | Gồm cả tiếng không dấu đứng giữa hai bước đánh vần |
| `tu`, `cau` | "cái đu", "má có củ từ" | |
| `huong_dan`, `khen` | "Con hãy chọn chữ u", "Đúng rồi!" | |

### 7.2 Nguồn âm thanh

- **Hiện tại [Chốt]:** âm thanh do ChatGPT tạo trong dự án Kiet_1. Claude là người tạo (xem cách làm ở mục 8).
  - Ngày 28/10/2026 đã thử: ChatGPT tạo được file MP3 bằng bộ đọc máy giọng miền Nam. File phát được nhưng **phát âm chưa chuẩn**; chủ dự án vẫn chọn dùng tạm.
  - **Tạo theo lô [Đề xuất]:** đưa ChatGPT một danh sách `id,text` và nhờ xuất một file ZIP gồm các file `<id>.mp3`.
  - **File `can_nghe_ky`:** yêu cầu gửi ChatGPT ghi rõ "đọc rõ theo chính tả, phân biệt dấu hỏi và dấu ngã". Khi duyệt, "đạt" nghĩa là nghe ra được sự khác biệt. Nếu bản tạm không làm được thì để `khong_dat` và vẫn dùng tạm [Đề xuất; đã nêu với chủ dự án, chủ dự án không phản đối].
- **Sau này:**
  - Mảnh `am`, `van`, `dau` thay bằng giọng người thật; phần còn lại thay bằng giọng đọc máy tốt hơn.
  - Các lựa chọn đã tìm hiểu: FPT.AI (giọng lannhi, linhsan), Viettel AI (giọng Diễm My), Zalo AI, VieNeu-TTS (mã nguồn mở).
  - Việc thay chỉ cần **ghi đè file có cùng `id`** và cập nhật trạng thái trong danh mục.

### 7.3 Danh mục âm thanh và trang duyệt [Chốt: chủ dự án duyệt từng file]

**Danh mục âm thanh** là một file dữ liệu (ví dụ `audio_manifest.json`). Mỗi dòng có các trường:

| Trường | Ý nghĩa |
|---|---|
| `id` | Mã file |
| `text` | Đúng chữ cần đọc |
| `kind` | Loại mảnh (xem 7.1) |
| `file` | Đường dẫn file |
| `source` | `chatgpt_tam`, `tts_<nhà cung cấp>` hoặc `giong_that` |
| `status` | `chua_co`, `cho_duyet`, `dat` hoặc `khong_dat` |
| `can_nghe_ky` | Đánh dấu file có dấu hỏi hoặc ngã, hay cặp âm dễ lẫn khi đọc giọng miền Nam |
| `ghi_chu` | Ghi chú |

Danh mục được **sinh tự động** từ dữ liệu các bài. Mỗi `id` chỉ có một dòng, kể cả khi nhiều bài cùng dùng.

**Trang duyệt** chạy trên máy:
- Mỗi dòng có nút nghe, nút đạt / không đạt và ô ghi chú.
- Lọc được theo trạng thái, theo bài và theo `can_nghe_ky`.
- Kết quả duyệt ghi lại vào danh mục.
- Làm trang bằng gì và ghi kết quả ra sao là **[Builder]**.

**Khi app chạy:**
- File ở trạng thái `khong_dat` hoặc `chua_co` vẫn được phát, như bản tạm.
- Nếu thiếu hẳn file, app báo lỗi rõ ràng trong chế độ phát triển.

### 7.4 Quy ước mã âm thanh [Đề xuất]

Mã viết theo **kiểu gõ Telex, chỉ dùng chữ ASCII**, để không bị trùng và nhìn là đọc được.

| Nhóm | Ví dụ mã |
|---|---|
| Mảnh đánh vần | `am_dd` (đờ), `am_k` (ca), `van_u`, `van_an`, `dau_huyen` |
| Tiếng | `tieng_ddu` (đu), `tieng_cuw` (cư), `tieng_cuwr` (cử) |
| Từ | `tu_cais_ddu` (cái đu) |
| Câu, hướng dẫn, khen | Đặt mã theo bài: `cau_b13_01`, `hd_chon_chu`, `khen_01` |

## 8. Hình ảnh

- **Công cụ và người làm [Chốt]:** ChatGPT trong dự án Kiet_1 (đường link chủ dự án đã đưa). **Claude tạo toàn bộ tranh và âm thanh**, điều khiển trình duyệt thật của chủ dự án (Edge có cài extension Claude). Chủ dự án tự đăng nhập ChatGPT; Claude không nhập mật khẩu.
- **Duyệt tải file theo lô [Đề xuất]:** Claude không tải file về máy khi chưa hỏi. Mỗi lần hỏi gom thành một lô và nêu rõ tên file, nguồn, dung lượng:
  - tranh: mỗi bài một lần
  - âm thanh: một file ZIP cho nhiều bài
- **Sau khi tải:** Claude chuyển file từ thư mục Downloads vào đúng chỗ trong project, đặt tên theo `id`, cập nhật trạng thái `cho_duyet` trong danh mục. Chủ dự án duyệt trên trang duyệt (mục 7.3).
- **Phong cách [Chốt]:** giống tranh SGK 1990. Đoạn mô tả dưới đây đã thử và cho kết quả tốt:

  > *"nét mực đen viền rõ, tô 2–3 màu phẳng (xanh lam ngọc, cam nhạt), bóng đổ bằng nét gạch, nền trơn màu giấy ngà, không có chữ, không có khung viền; chủ thể ở giữa, chừa khoảng trống; tỉ lệ vuông 1:1; tranh vẽ mới hoàn toàn"*

  Đoạn này lưu thành một file mô tả phong cách chung và dán kèm mỗi lần tạo tranh.
- **Phiếu vẽ** sinh từ dữ liệu bài. Mỗi tranh một dòng, gồm:
  - `id`, ví dụ `img_b13_cais_ddu`
  - bài
  - vẽ gì (dựa trên tranh gốc)
  - ghi chú
  - trạng thái duyệt

  Bài 1–17 cần khoảng 80 tranh.
- **Danh mục hình** làm giống danh mục âm thanh. Thay hình bằng cách ghi đè file có cùng `id`.
- **[Builder]:** nền trong suốt hay nền giấy ngà.

## 9. Dữ liệu bài học

- **Mỗi bài một file dữ liệu** (ví dụ `lessons/tv1_t1_b13.json`), không nằm trong code [Chốt]. File gồm:
  - mã bài; quyển, phần, số bài; loại bài
  - nguồn: trang, ảnh scan, mức xác minh
  - các âm hoặc vần mới
  - các bước Phần 1 và các bài tập Phần 2
  - danh sách nhãn `can_duyet` và trạng thái duyệt của bài
- **Mỗi bước Phần 1** tham chiếu chữ, mã tranh và mã âm thanh.
- **Mỗi bước đánh vần** ghi rõ chuỗi mảnh âm thanh, ví dụ:

  ```json
  {
    "step": "spell",
    "target": "cử",
    "sequence": [
      { "text": "c",  "audio": "am_c" },
      { "text": "ư",  "audio": "van_uw" },
      { "join": "cư", "audio": "tieng_cuw" },
      { "tone": "hỏi", "audio": "dau_hoi" },
      { "join": "cử", "audio": "tieng_cuwr" }
    ]
  }
  ```

- **Chuỗi đánh vần ghi sẵn trong dữ liệu, app không tự tính lúc chạy [Đề xuất].**
  - Công cụ soạn nội dung sinh sẵn chuỗi theo quy tắc ở 5.1.
  - Người duyệt sửa tay các trường hợp gắn nhãn `can_duyet`.
  - Lý do: các ngoại lệ (gi, qu, ngh…) dễ kiểm soát hơn khi nằm trong dữ liệu.
- **[Builder]:** dạng dữ liệu (JSON, ScriptableObject hay cả hai) và cách nạp trong Unity (StreamingAssets, Addressables…). Miễn là:
  - chạy không cần mạng
  - thay asset không phải sửa code
  - một mô hình dữ liệu dùng chung cho mọi loại bài

## 10. Hiển thị chữ

- **Font:** đọc rõ, đủ dấu tiếng Việt, có **chữ a và g kiểu một tầng** (ɑ, ɡ) giống chữ in trong SGK và chữ bé tập viết.
  - **[Đề xuất]:** Andika (SIL, giấy phép OFL), font làm riêng cho việc học đọc. Builder cần kiểm tra lại font có đủ dấu tiếng Việt.
- **Trong Unity:** dùng TextMeshPro với font asset chứa đủ ký tự tiếng Việt, và chuẩn hóa mọi chuỗi về NFC. Phải thử trong Unity Editor ngay từ bài mẫu đầu tiên. Khi có bản build Android thì thử lại trên máy thật.
- **Màu chữ:** theo cách sách tô màu phần âm hoặc vần mới (phần "u" trong "đu" có màu khác). **[Builder]:** bảng màu.

## 11. Công cụ phụ trợ cần có

1. **Công cụ soạn bài:** nhận thông tin trang sách do người soạn chép vào, rồi tạo file dữ liệu bài kèm chuỗi đánh vần sinh sẵn.
2. **Sinh danh mục:** từ dữ liệu các bài, sinh danh mục âm thanh, danh mục hình và phiếu vẽ.
3. **Gói yêu cầu cho ChatGPT:** xuất danh sách `id,text` cho âm thanh còn thiếu, và phiếu vẽ cho tranh còn thiếu.
4. **Trang duyệt âm thanh** (xem 7.3), cùng một trang tương tự để duyệt hình. Hai trang có thể gộp làm một.
5. **Kiểm tra dữ liệu:**
   - mọi mã âm thanh và mã tranh mà bài dùng đều có trong danh mục
   - không còn chuỗi chưa chuẩn hóa NFC
   - phương án nhiễu chỉ lấy từ chữ đã học
   - không có ảnh scan trong project Unity

## 12. Thứ tự làm

1. **3 bài mẫu (bài 4, 13, 42)** dùng asset tạm từ ChatGPT, chạy trên máy tính. Chủ dự án thử trên bản build Windows do Claude build và mở lên.
   - Chủ dự án thử từ đầu đến cuối và duyệt cảm giác học.
   - Kiểm tra chữ tiếng Việt hiển thị đúng, và kiểm tra thay asset theo `id` được.
   - Quyết thêm chuyện nhân vật dẫn dắt.
   - Trong bản mẫu, cả 3 bài mở sẵn, không khóa. Phương án nhiễu của bài 42 lấy từ các chữ đã học ở bài 1–41 theo thứ tự sách [Đề xuất].
2. **Bản đầu tiên, bài 1–17:** soạn dữ liệu; Claude tạo tranh và âm thanh tạm trong ChatGPT; chủ dự án duyệt từng bài.
3. **Sau bản đầu tiên:** thay âm thanh tốt hơn, làm phần Vần (bài 42–80), rồi TV1 Tập 2.

## 13. Tiêu chí chấp nhận

**Bản mẫu (3 bài):**
- [ ] Đi hết Phần 1 → Phần 2 → Kết thúc của bài 4, 13, 42 chỉ bằng chạm (hoặc bấm chuột) và kéo thả, trên bản build Windows, không cần mạng. Thử ở cả khung hình cỡ điện thoại và cỡ máy tính bảng.
- [ ] Mọi chuỗi đánh vần đúng quy tắc ở 5.1, kể cả bài 42: vần trước, tiếng sau, vần giữ nguyên một khối.
- [ ] Nội dung Phần 1 khớp với trang sách và đúng thứ tự.
- [ ] Chữ tiếng Việt hiển thị đúng dấu, không bị xén hay lệch.
- [ ] Ghi đè một file âm thanh và một tranh có cùng `id` trong project, chạy lại thì app dùng bản mới mà không phải sửa code.
- [ ] Khi chủ dự án yêu cầu build: bản APK cài được và đạt các tiêu chí trên trên máy Android thật.

**Bản đầu tiên (bài 1–17):** đạt mọi tiêu chí trên, và thêm:
- [ ] Mỗi bài ghi trang nguồn và mức xác minh; mọi nhãn `can_duyet` đã được chủ dự án xử lý.
- [ ] Mọi file âm thanh đã qua trang duyệt; danh mục không còn file nào ở trạng thái `chua_co` (file `khong_dat` vẫn được dùng tạm).
- [ ] Tiến độ, sao và lỗi nhầm được lưu riêng cho từng hồ sơ bé; mục "Ôn lại" lấy đúng các lượt bé đã nhầm.
- [ ] Màn phụ huynh có khóa và hiển thị đúng tiến độ.
- [ ] Không có ảnh scan nào trong project Unity, và trong gói build khi có.

## 14. Builder tự quyết

- Cấu trúc project Unity: các scene, cách chia module, cách lưu tiến độ (ví dụ file JSON trong `persistentDataPath`).
- Bố cục, màu sắc, hiệu ứng nhẹ và kích thước nút, trong giới hạn ở mục 6.
- Dạng dữ liệu và cách nạp nội dung (mục 9).
- Công nghệ làm công cụ phụ trợ và trang duyệt (mục 11).
- Cách kiểm thử.

## 15. Việc còn mở (không chặn bản mẫu)

- **Nhân vật dẫn dắt và phần thưởng chi tiết:** quyết sau khi thử bản mẫu.
- **Phát hành:** kênh phát hành và các thủ tục cho app trẻ em. Chủ dự án tính khi app hoàn thành.
- **Nguồn âm thanh chính thức:** giọng người thật hay giọng đọc máy nào. Quyết khi chủ dự án thay bản tạm.
- **Ba điểm đánh vần "cần duyệt"** ở 5.1: chủ dự án duyệt khi kiểm tra từng bài. Vẫn đang tìm sách giáo viên bản cũ.

### Kết quả thử bản mẫu (29/10/2026)

- Chủ dự án đã thử bản build Windows của 3 bài mẫu, cả khung 1600×720 lẫn 1440×1080, và đánh giá **"Ổn"**.
- Kiểm tra dữ liệu bản đầy đủ (không bỏ qua file thiếu) báo `OK`.
- Kết quả test:
  - EditMode 23 đạt, trong đó có test kiểm tra đủ tài nguyên thật;
  - PlayMode 46 đạt, gồm chạy trọn 3 bài và kiểm tra bố cục ở hai khung hình;
  - Python 377 đạt.
- **Tài nguyên tạm:** 82 âm thanh (giọng máy vi-sgn) và 15 tranh, tạo trong ChatGPT Kiet_1. Tất cả đang ở trạng thái `cho_duyet`, chủ dự án duyệt dần bằng `python -m tapdoc review`.
- **Nhân vật dẫn dắt và phần thưởng chi tiết:** chưa quyết. Bản mẫu chỉ dùng 3 ngôi sao cùng lời khen. Quyết khi viết kế hoạch bản đầu tiên (bài 1–17).
- **Ba điểm chủ dự án cần duyệt nội dung** (`can_duyet`):
  - lời dẫn tranh 5 bạn múa ở bài 4;
  - các tranh lan can, đàn ngan, bàn ghế vẽ thêm ở bài 42;
  - tên đọc riêng "ngờ đơn" cho "ng" trong "ngan".
- **Việc trau chuốt để sau:**
  - kí hiệu dấu trong thẻ còn nhỏ và nằm hơi cao;
  - màn rộng còn nhiều khoảng trống hai bên;
  - thiếu tranh ngôi sao thì hiện ô vàng.

### Bản đầu tiên bài 1–17: đã làm (29/10/2026)

Kế hoạch: [2026-10-29-ban-dau-tien-bai-1-17.md](../plans/2026-10-29-ban-dau-tien-bai-1-17.md).

- **Phần thưởng [Đề xuất, đã làm]:** học xong một bài được 3 sao, không phụ thuộc số lần sai. Chưa có nhân vật dẫn dắt.
- **Nội dung:**
  - 17 bài chép từ trang sách (ảnh 004–012). Mức xác minh của cả 17 bài là `page_verified`.
  - Bài 42 vẫn được dựng nhưng không hiện trong danh sách bài (`in_app: false`).
- **Màn mới:**
  - bảng dấu (bài 6), khung chữ và bảng ghép (bài ôn tập 7, 11, 17);
  - dòng chữ dài tự xuống dòng;
  - thẻ kí hiệu dấu to và nằm giữa thẻ.
- **App:**
  - hồ sơ bé (tên gọi ở nhà và 6 hình đại diện);
  - tiến độ lưu riêng từng bé, qua file tạm, nên file không bị ghi dở;
  - bài mở theo thứ tự, có sao;
  - mục "Ôn lại" lấy các lượt bé đã nhầm;
  - màn phụ huynh khóa bằng một phép cộng.
- **Tài nguyên tạm** (ChatGPT Kiet_1, đều ở trạng thái `cho_duyet`):
  - 278 âm thanh, giọng máy vi-sgn+f3;
  - 58 tranh, gồm 6 hình đại diện.
- **Kết quả test:**
  - EditMode 79 đạt, trong đó có test kiểm tra đủ tài nguyên thật;
  - PlayMode 108 đạt, gồm chạy trọn 17 bài và bài 42, kiểm tra bố cục ở khung 2400×1080 và 2048×1536;
  - Python đều đạt.
  - Kiểm tra dữ liệu bản đầy đủ báo `OK`.
- **Việc trau chuốt để sau:**
  - câu dài xuống dòng có thể để một chữ đứng riêng ở dòng hai (bài 14 "tá");
  - tên bài dài (bài 4, bài 6) bị thu chữ khá nhỏ trên thẻ danh sách bài;
  - màn rộng vẫn còn khoảng trống hai bên.

### Đợt 1 bài 18–41: đã làm (29/10/2026)

Kế hoạch: [2026-10-29-hoan-thanh-tv1-tap-1.md](../plans/2026-10-29-hoan-thanh-tv1-tap-1.md), Task 1.1–1.8.

- **Nội dung:** 24 bài chép từ trang sách (ảnh 012–024), đều `page_verified`.
  - 16 bài âm mới (v … p ph), 7 bài ôn tập (22, 27, 32, 37–40) và bài 41 giới thiệu chữ hoa.
  - Bài 38: 12 hàng đọc có nhãn của trang được chia thành 4 bước, mỗi bước 3 hàng, cho vừa màn hình.
- **Màn mới:**
  - cặp chữ thường/chữ hoa 4 cột, 2 trang (bài 41) và lượt chọn chữ hoa;
  - luật chính tả (bài 40), nhãn đầu hàng đọc thêm (bài 38);
  - ô gạch chéo trong bảng ghép (k + a, gh + o…), chạm vào không đọc, không tính;
  - bảng ghép 5 âm đầu xếp 2 cột cho vừa màn;
  - danh sách bài cuộn dọc, chia phần "Chữ cái và âm" / "Vần".
- **Kiểm tra dữ liệu:** luật giọng miền Nam áp dụng cả cho phụ âm đứng riêng (s/x, d/gi/v, ch/tr); chữ hoa đọc và tính "đã học" như chữ thường; gạch nối trong từ mượn (ra-đi-ô) tách âm tiết.
- **Tài nguyên tạm** (ChatGPT Kiet_1, `cho_duyet`): thêm 467 âm thanh (tổng 745) và 38 tranh (tổng 96).
  - ChatGPT báo bộ đọc trong máy của nó là eSpeak 1.48 (cùng mã giọng vi-sgn+f3), giống lô "legacy" của bản đầu tiên.
- **Kết quả test:** Python đều đạt; EditMode 79 đạt; PlayMode 176 đạt, gồm chạy trọn 41 bài và kiểm tra bố cục ở 2 khung hình; `validate` bản đầy đủ báo `OK`.
- **Việc trau chuốt để sau:** như bản đầu tiên, cộng thêm: tranh từ khoá vẽ thêm cho các từ không có tranh trong sách đều gắn `can_duyet`.

## 16. Hoàn thành TV1 Tập 1: bài 18–80 [Đề xuất, chờ chủ dự án duyệt]

Đây là bước 3 ở mục 12, phần còn lại của quyển. Mọi điều ở mục 2–11 vẫn giữ nguyên. Riêng mục 2 có một thay đổi: phần Vần (bài 42–80) nay nằm trong phạm vi.

**Phạm vi.** Gồm 63 bài:
- 24 bài phần "Chữ cái và âm": 18 bài âm mới, 5 bài ôn tập, bài 41 giới thiệu chữ hoa;
- 37 bài phần "Vần": 30 bài vần mới, 7 bài ôn tập vần;
- 2 bài ôn tập cuối học kì I.

Bài 42 thôi là bài ẩn và hiện trong danh sách bài.

Không đưa vào app: tranh mở đầu, trang kí hiệu, phụ lục bảng chữ cái, trang "Chú ý" và mục lục. Đó không phải bài học. Phần ▨ "Em viết" vẫn bỏ qua như cũ.

**Ba đợt phát hành.** Mỗi đợt kết thúc như bản đầu tiên: bản build Windows cho chủ dự án thử, chủ dự án duyệt, gom 1 commit trên `main` rồi push.

| Đợt | Bài | Nội dung |
|---|---|---|
| 1 | 18–41 | âm mới (v … ph), ôn tập âm, chữ hoa |
| 2 | 42–64 | vần có âm cuối n, m, i/y, o/u, và các bài ôn tập vần |
| 3 | 65–80 | vần có âm cuối c, t, p, và ôn tập cuối học kì I |

**Cách thể hiện các kiểu trang mới.** Nội dung và thứ tự giữ đúng như trang sách; chỉ cách tương tác là mới.

| Trang sách | Trong app |
|---|---|
| Bảng chữ in thường – chữ in hoa (bài 41) | bước `letter_pairs`: mỗi cặp một thẻ, chạm để nghe |
| Bảng ghép có ô gạch chéo (bài 39–40: "k", "gh", "ngh" không ghép với a, o…) | `combine_table` có ô bị chặn: hiện gạch chéo, chạm không đọc |
| "Luật chính tả cần nhớ kĩ" (bài 40) | bước `rule`: mỗi dòng một thẻ, chạm để nghe cả dòng |
| Hàng có nhãn "a – a: ra rả, khà khà" (bài 38) | bước `reading` có nhãn đầu hàng |
| Bảng thay dấu nhiều tiếng gốc (bài 39–40) | mỗi tiếng gốc một bước `tone_table`, theo thứ tự hàng |
| Bảng ôn vần: vần = nguyên âm + âm cuối, kèm tiếng/từ ví dụ | bước `rime_table`: chạm hàng thì đánh vần vần rồi đọc từ |
| Bảng nhóm vần đã học (bài 79) | bước `rime_grid`: chạm ô thì đánh vần vần |
| Đoạn đọc nhiều câu hoặc bài thơ (từ bài 45) | mỗi câu (hoặc dòng thơ) một bước `sentence`, đúng thứ tự |
| Câu đố "Đố em" (bài 80) | Phần 1 đọc bài thơ. Phần 2 có lượt nghe câu đố rồi chọn tranh đáp án. Tranh là vẽ thêm, gắn `can_duyet`. |

**Phần 2 có thêm kiểu `match_case`** (từ bài 41): nhìn chữ thường, chọn đúng chữ hoa trong 3 thẻ. Đây là bài nhìn, không có đề bằng âm thanh.

**Giọng miền Nam.** Quy tắc "không làm nhiễu của nhau trong bài nghe" áp dụng cả khi phương án là phụ âm đứng riêng: s/x, d/gi/v, ch/tr.

**Danh sách bài.** Chia hai phần "Chữ cái và âm" và "Vần" (kèm 2 bài ôn tập cuối kì), cuộn dọc. Mọi thẻ vẫn giữ cạnh ≥ 160.

**Âm thanh.** Tiếp tục giọng tạm vi-sgn+f3 cho cả quyển. Sau này thay giọng tốt hơn theo mã, không phải sửa code (mục 2, mục tiêu 4).

## 17. Giọng đọc mới bằng edge-tts và công cụ chỉnh âm thanh [Đề xuất 29/10/2026, chờ chủ dự án duyệt bản viết]

**Vì sao.** Chủ dự án nghe các file tạm (ChatGPT, bộ đọc eSpeak vi-sgn+f3) và thấy không file nào dùng được:
- đọc quá nhanh, khó nghe;
- chữ cái và vần quá ngắn, không nghe ra;
- chưa chắc cách đọc từng mảnh đã đúng.

Bản nghe thử ngày 29/10 dùng gói Python `edge-tts` (giọng `vi-VN-HoaiMyNeural`, nữ, giọng Bắc). Chủ dự án thấy "ok hơn rất nhiều", nhưng cần một công cụ để tự nghe và chỉnh từng từ.

**Mục tiêu**
1. Thay toàn bộ âm thanh (1.317 mã tới bài 64, sau đó cả quyển) bằng file do `edge-tts` tạo.
   - **Tên file và mã giữ nguyên** như mục 7.4 (`am_b.mp3`, `tu_nhaf_sanf.mp3`…). Công cụ chỉ ghi đè nội dung file. Code, bài học và danh mục không đổi.
   - File mp3 đóng gói vào app như hiện nay. **App không cần mạng và không gọi bộ đọc khi chạy**; bản build vẫn phát âm đủ.
2. **Công cụ chỉnh âm thanh**, chạy trên máy cùng lệnh `python -m tapdoc review`:
   - **Lọc:** theo bài, theo loại (mục 7.1), theo trạng thái (`chua_co`, `cho_duyet`, `dat`, `khong_dat`) và theo "đã chỉnh tay".
   - **Mỗi dòng là một mã:**
     - chữ hiển thị trong app;
     - **cách đọc**: chữ đưa cho bộ đọc, mặc định bằng `text`, sửa tay được;
     - tốc độ, cao độ, âm lượng;
     - nút **Tạo lại**, **Nghe**, **Nghe bản trước**, **Đạt** / **Không đạt**, ô ghi chú.
   - **Tạo lại** gọi `edge-tts` ngay trên máy và ghi đè đúng file mà app dùng. Nghe trong công cụ thế nào thì app phát y như vậy.
   - Bản trước được giữ lại để nghe so sánh, đến khi chủ dự án bấm Đạt. Bản trước lưu ở thư mục không đưa vào git và không vào bản build.
   - **Nghe theo bài:** mở một bài, nghe từng chuỗi đánh vần và câu đúng như bé nghe trong app (cùng khoảng nghỉ giữa các mảnh). Bấm vào một mảnh thì nhảy tới dòng của mảnh đó.
3. **File cấu hình giọng đọc** nằm trong dự án và có trong git:
   - giọng;
   - thông số mặc định theo loại;
   - các mã đã chỉnh tay (chỉ lưu những gì khác mặc định).
4. **Lệnh tạo hàng loạt**, ví dụ `python -m tapdoc tts`:
   - tạo file cho các mã còn thiếu, hoặc mã có cách đọc/thông số đã đổi kể từ lần tạo trước;
   - lọc được theo bài hoặc theo loại;
   - không tạo lại file đã `dat` trừ khi chủ dự án yêu cầu rõ.

   Sau khi tạo, mã về trạng thái `cho_duyet` và `source` ghi `tts_edge_hoaimy`.

**Mặc định ban đầu [Claude chọn; chỉnh được trong công cụ]**

| Loại | Tốc độ |
|---|---|
| `am`, `van`, `dau` | −30% |
| `tieng` | −25% |
| `tu`, `cau`, `huong_dan`, `khen` | −15% |

- Cao độ và âm lượng giữ nguyên.
- Khoảng nghỉ giữa các mảnh đánh vần trong app vẫn là 0,5 giây (`SequenceTimeline.DefaultGap`). Nếu chủ dự án muốn đổi thì đổi ở đó, không tạo lại file.

**Cách đọc và cách đánh vần**
- "Cách đọc" chỉ đổi lời đọc của **một mã** (ví dụ viết lại "cu" cho bộ đọc đọc rõ hơn). Nó không đổi chữ hiển thị, không đổi mã, không đổi cấu trúc chuỗi đánh vần.
- Nếu một chuỗi đánh vần sai (thiếu hay thừa mảnh, sai quy tắc tr.122), chủ dự án ghi chú trong công cụ. Claude sửa quy tắc trong bộ công cụ, rồi dựng lại bài.

**Không làm lúc này**
- giọng miền Nam;
- giọng người thật;
- bộ đọc chạy trong app;
- sửa quy tắc đánh vần ngay trong công cụ;
- đổi tên file.

**Ràng buộc**
- Phần dựng bài và kiểm tra vẫn chỉ dùng thư viện chuẩn của Python. `edge-tts` là phụ thuộc riêng của phần tạo âm thanh, cài theo một file yêu cầu riêng. Thiếu gói thì lệnh báo rõ cách cài.
- Tạo âm thanh cần mạng (dịch vụ đọc của Microsoft). Lỗi mạng, hoặc dịch vụ trả về rỗng (đã gặp với chữ "cu"), thì thử lại vài lần rồi báo đúng mã bị lỗi; không ghi đè file cũ bằng file hỏng.
- Test không gọi mạng: phần gọi bộ đọc thay được bằng bộ đọc giả trong test.

**Rủi ro cần chủ dự án biết**
- `edge-tts` dùng dịch vụ đọc của trình duyệt Edge một cách **không chính thức**, có thể ngừng hoạt động bất cứ lúc nào.
- Quyền dùng file tạo ra trong một app phát hành công khai chưa rõ. Trước khi phát hành, nên chuyển sang dịch vụ chính thức của Microsoft (Azure, cùng giọng HoaiMy, có phí, điều khoản rõ) hoặc một nhà cung cấp khác.
- Thiết kế giữ phần "bộ đọc" thay được, để việc chuyển chỉ là đổi cấu hình rồi tạo lại.

**Builder tự quyết**
- định dạng file cấu hình;
- giao diện cụ thể của công cụ;
- cách lưu bản trước;
- cách nhận biết "thông số đã đổi" (ví dụ băm cách đọc và thông số).

**Quyết định thêm sau khi soát bản viết [Claude chọn; chủ dự án đổi được]**
1. **Mặc định theo loại sửa được ngay trong công cụ.**
   - Đổi một mặc định thì các mã chưa `dat` theo mặc định đó được đánh dấu "cần tạo lại". Công cụ có nút tạo lại hàng loạt, có thanh tiến độ; lệnh `tts` cũng làm được việc này.
   - Mã đã `dat` **giữ nguyên file và giữ nguyên thông số lúc được duyệt.** Công cụ chỉ báo "khác mặc định mới", không tự tạo lại.
   - Vì vậy file cấu hình lưu, cho mỗi mã đã tạo: cách đọc, các thông số thực dùng và dấu nhận dạng của lần tạo.
2. **Bản trước** là bản ngay trước lần Tạo lại gần nhất, chỉ giữ một bản.
   - Có nút **Dùng lại bản trước**: trả lại cả file lẫn cách đọc và thông số của bản đó, để cấu hình luôn khớp với file.
   - Bấm Đạt thì xoá bản trước.
3. **Khoảng lặng hai đầu file:** cắt về một mức đều, khoảng 0,1 giây mỗi đầu.
   - Mục đích: khoảng nghỉ giữa các mảnh trong app chỉ còn do `SequenceTimeline.DefaultGap` quyết định, và chữ sáng lên đúng lúc có tiếng.
   - Dùng mốc thời gian do `edge-tts` trả về và cắt theo khung mp3, không thêm thư viện xử lý âm thanh.
   - Nếu cắt không được thì giữ nguyên file và ghi chú lại.
4. **Ghi chú cho cả một chuỗi đánh vần**, ở chế độ "Nghe theo bài", lưu riêng cho từng bài và từng bước.
   - Mỗi ghi chú gồm bài, vị trí bước và chữ của chuỗi, để vẫn tìm lại được sau khi dựng lại bài.
   - Claude đọc các ghi chú này để sửa quy tắc đánh vần.
5. **Chỉ có edge-tts.** Phần bộ đọc làm thành một chỗ thay được, chưa làm Azure (chủ dự án chọn "dùng free trước").
   - `validate --release` chỉ **cảnh báo** khi file có nguồn `tts_edge_*`, không chặn, vì chưa phát hành công khai.
6. **Danh mục âm thanh được thêm trường.** Chỉ mã và tên file là cố định.
