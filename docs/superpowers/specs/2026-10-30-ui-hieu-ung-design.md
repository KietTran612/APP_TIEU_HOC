# Thiết kế: Giao diện, hiệu ứng và Sổ bé ngoan cho app Tập đọc lớp 1

> **Ngày:** 30/10/2026 · **Trạng thái:** chủ dự án đã duyệt ngày 30/10/2026; khi làm giao diện sẽ thử và chỉnh thêm · Repo: https://github.com/KietTran612/APP_TIEU_HOC, chỉ dùng branch `main`, giữ nguyên lịch sử
> **Thiết kế gốc của app:** [2026-10-28-app-tap-doc-mvp-design.md](2026-10-28-app-tap-doc-mvp-design.md). Mọi điều ở đó vẫn giữ, trừ những chỗ tài liệu này nói rõ là thay.
> **Bản mẫu đã xem** (trang tạm, không nằm trong git): `.superpowers/brainstorm/1994-1793329432/content/`. Các file `phong-cach-man-hoc.html` (hướng A), `so-be-ngoan-v2.html` (Sổ bé ngoan; bố cục trang trong bản mẫu là 4 ô, đã đổi thành mỗi trang một bài, xem mục 8.3).
>
> Cách đánh dấu trong tài liệu:
> - **[Chốt]**: chủ dự án đã quyết.
> - **[Đề xuất]**: người viết tự quyết. Chủ dự án có thể đổi; builder không cần hỏi lại.
> - **[Builder]**: builder tự quyết.

---

## 1. Mục đích và lý do

Chủ dự án thấy giao diện hiện tại "đơn giản quá, không thu hút". Tình trạng hiện nay:
- toàn ô vuông phẳng một màu;
- nút chỉ có chữ ("Về", "Nghe lại", "Tiếp"), trong khi bé 6 tuổi chưa đọc được;
- không có chuyển động nào, không có tiếng động nào ngoài giọng đọc;
- học xong bài chỉ hiện ba ngôi sao đứng yên. Bài nào học xong cũng được đủ 3 sao, nên sao không mang ý nghĩa gì.

Việc này làm app **đẹp hơn, sinh động hơn** để bé thích ngồi học, mà **vẫn là app học tập**: chữ và tranh của bài luôn là thứ nổi nhất trên màn.

Chưa có bé nào thử app. Mọi điều về hành vi của bé trong tài liệu này là phán đoán, sẽ chỉnh sau khi có bé thử.

## 2. Mục tiêu, việc không làm, và điều coi là thất bại

### Mục tiêu
1. **Phong cách tranh SGK 1990 cho cả giao diện [Chốt]:** nét mực đen, màu phẳng xanh lam ngọc và cam nhạt, nền giấy ngà. Đây là hướng "A – Trang sách in" trong bản mẫu.
2. **Hiệu ứng chuyển động** cho các lúc: app đọc mẫu, bé chạm, bé làm đúng, bé làm sai, sang bước mới, học xong bài [Chốt: "cần thêm hiệu ứng cho sinh động"].
3. **Tiếng động khi tương tác**, làm cho hợp lý [Chốt]. Nguồn là bộ tiếng miễn phí trên mạng [Chốt: chủ dự án muốn tìm nguồn free có âm thanh đúng ý].
4. **Bạn gà con** đồng hành trong màn học, làm đơn giản trước [Chốt]. Sau này chủ dự án sẽ làm cho gà con sinh động và đa dạng hơn.
5. **Sổ bé ngoan [Chốt]:** một quyển sổ giống sổ bé ngoan của học sinh ngày xưa, **mỗi trang là một bài học**. Học xong bài thì được **3 bông hoa bé ngoan** (thay cho 3 ngôi sao), dán ở phía trên trang của bài đó. Phần dưới trang tạm để trống, sau này sẽ có nội dung mới. Bé mở lại xem sổ được.

### Không làm lần này
- Nền có cảnh vật (làng quê, mây, đồi cỏ), trang vở ô li, quyển sách mở làm khung [Chốt: chủ dự án chọn A, nền trơn].
- Gà con nhiều tư thế, biết nói, có hoạt hình riêng [Chốt: để sau].
- Nhiều loại hoa hay hình dán, nội dung phần dưới trang sổ, sự kiện mới trong sổ [Chốt: tạm chỉ 1 hình hoa, phần dưới để trống].
- Đổi nội dung bài, thứ tự bước, quy tắc đánh vần, giọng đọc.
- Bản build Windows/Android (vẫn chỉ commit, như quy tắc chung).

### Coi là thất bại, dù app vẫn chạy
- **Rối mắt, lấn át việc học:** nền hay hình trang trí giành sự chú ý với chữ và tranh của bài.
- **Hiệu ứng bắt bé chờ:** bé phải đợi hiệu ứng chạy xong mới chạm tiếp được, hoặc hiệu ứng làm chậm nhịp đánh vần.
- **Tiếng động át giọng đọc:** bé không nghe rõ "đờ – u – đu" vì có tiếng động chen vào.
- **Có cảm giác bị phạt khi sai:** màu đỏ, dấu X, tiếng "è è", gà con buồn hay lắc đầu.
- **Vỡ bố cục:** ở khung 2400×1080 hoặc 2048×1536, vùng chạm nhỏ hơn 160 hoặc chữ tràn (`LayoutProbe`).
- **Hình hay tiếng viết cứng trong code:** không thay được bằng cách ghi đè file có cùng mã.
- **Mất tiến độ cũ:** bé đã học xong bài nào trước bản này thì sau khi cập nhật vẫn thấy đủ 3 hoa của bài đó.

## 3. Ràng buộc

| Ràng buộc | Giá trị |
|---|---|
| Engine, cách dựng | Unity 6.6, giao diện dựng hoàn toàn bằng code (`UiKit`), không có prefab. Giữ cách này |
| Khung hình | Phải vừa 2400×1080 (điện thoại) và 2048×1536 (máy tính bảng). Vùng chạm ≥ 160 (đơn vị canvas 1920×1080), chữ không tràn; kiểm tra bằng `LayoutProbe` như hiện nay [Chốt] |
| Không cần mạng | Mọi hình và tiếng đóng gói sẵn trong app |
| Thay tài nguyên | Hình và tiếng mới đều có **mã riêng**, nạp qua `AssetCatalog`. Ghi đè file cùng mã là thay được, không sửa code |
| Gói ngoài | Ưu tiên gói có sẵn của Unity. Không mua gói trả phí |
| Tranh | Vẽ bằng ChatGPT dự án Kiet_1, qua Edge trên máy này. Hỏi chủ dự án trước khi tải mỗi lô |
| Tiếng động | Chỉ dùng file có giấy phép **CC0** (tự do, kể cả thương mại, không cần ghi công). Hỏi chủ dự án trước khi tải lô |
| Test | Claude viết và review mọi test. Codex/Antigravity chỉ viết code cho test của Claude chạy xanh |
| Ảnh scan | Không bao giờ vào repo hay bản build, kể cả ảnh sổ bé ngoan chủ dự án gửi làm mẫu |

## 4. Phong cách hình ảnh [Chốt: hướng A]

### 4.1 Bảng màu [Đề xuất]

| Tên | Màu | Dùng cho |
|---|---|---|
| Mực | `#2B2621` | Viền, nét, chữ |
| Giấy ngà | `#F6EEDB` | Nền màn |
| Giấy sáng | `#FBF6E9` | Nền thẻ, khung tranh, trang sổ |
| Lam ngọc | `#2F8C9B` | Nút chính, chấm tiến độ đã qua, phần vần/âm mới tô màu trong chữ |
| Lam ngọc nhạt | `#A9D4D6` | Viền ô hoa trong sổ, nền phụ |
| Cam | `#EF9D4F` | Nút "Tiếp", chấm tiến độ đang làm |
| Cam nhạt | `#F8D3A6` | Thẻ đang được đọc, bài đang học tới |
| Vàng gợi ý | `#F4C54A` | Thẻ gợi ý khi bé sai lần hai, sao giấy |
| Đỏ son | `#D0453B` | Chỉ dùng cho con dấu "Bé ngoan" |
| Khoá | nền `#E9E1CC`, viền và chữ `#B5AA93` | Bài chưa mở |

Màu tô phần vần mới trong chữ (hiện là lam ngọc) giữ nguyên.

Mọi màu khai báo một chỗ, ví dụ một lớp `Palette` [Builder: tên, chỗ đặt]. Code màn không viết mã màu trực tiếp.

### 4.2 Hình khối
- **Thẻ, khung tranh, ô hoa:** viền mực dày khoảng 3 đơn vị, góc bo khoảng 16, nền giấy sáng.
- **Bóng đổ bằng nét gạch chéo** (giống bóng trong tranh SGK), lệch xuống phải khoảng 10. Dùng cho khung tranh, quyển sổ, thẻ to. Thẻ nhỏ (ô bảng ghép, chip) không cần bóng [Đề xuất].
- **Nút của bé:** hình tròn, viền mực, nền lam ngọc (nút "Tiếp" nền cam), bên trong là **biểu tượng**, không có chữ:

  | Nút | Biểu tượng |
  |---|---|
  | Về danh sách | ngôi nhà |
  | Nghe lại | cái loa |
  | Tiếp | mũi tên sang phải |
  | Lật trang trước/sau (sổ) | mũi tên trái/phải |
  | Mở Sổ bé ngoan | quyển sổ có bông hoa |
  | Đổi bé | hình đại diện của bé đang học |
  | Ôn lại | mũi tên vòng tròn |
  | "Con đọc xong rồi" (bước câu) | dấu tích |
  | "Nghe cả câu" (bước câu) | cái loa, nút to đặt ngay dưới câu |
  | "Trang trước" / "Trang sau" trong một bước (`PageButtons` ở bảng chữ hoa, bảng ôn vần, bảng nhóm vần) | tờ giấy có góc gấp kèm mũi tên nhỏ, nền giấy sáng viền mực (không phải nền cam), giữ chỗ như hiện nay |

  Hai dòng cuối là quyết định của người viết [Đề xuất]:
  - "Nghe cả câu" giữ lại vì thiết kế gốc đã chốt nút này. Nút loa ở góc dưới trái vẫn có, cho đồng bộ với mọi bước.
  - Nút lật trang trong bước phải khác hẳn nút "Tiếp" (mũi tên trên nền cam), để bé không lẫn "sang trang" với "sang bước".

- **Nút của người lớn** (Phụ huynh, Ghi chú, Đóng, các nút trong màn Phụ huynh): hình chữ nhật bo góc, viền mực, **vẫn có chữ** [Đề xuất]. Người dùng là phụ huynh, cần đọc được.
- **Nền màn:** giấy ngà trơn, phủ hết màn, kể cả khoảng trống hai bên ở màn rộng [Chốt: không có cảnh vật].
- **Font:** giữ Andika như hiện nay.
- **Cách vẽ hình khối và biểu tượng:** [Builder]. Gợi ý:
  - khung bo góc có viền và nền gạch chéo có thể sinh bằng code thành sprite 9 mảnh (9-slice);
  - biểu tượng có thể là file SVG nạp bằng gói Vector Graphics của Unity, hoặc file PNG.

  Dù chọn cách nào, mỗi biểu tượng là **một file có mã riêng** (ví dụ `img_ui_nha`), thay được bằng cách ghi đè.

### 4.3 Chấm tiến độ trong bài [Đề xuất]
- Trên đầu màn học là một hàng chấm tròn, mỗi bước của bài (Phần 1 và Phần 2) là một chấm.
- Chấm của bước đã qua tô lam ngọc, chấm của bước đang làm tô cam, chấm của bước chưa tới để trống.
- Bài quá nhiều bước, hàng chấm không vừa chiều ngang thì đổi sang thanh tiến độ liền [Builder: ngưỡng].
- Chấm chỉ để xem, không bấm được.

## 5. Bạn gà con [Chốt: giữ như hướng C, làm đơn giản]

- **Hình:** mã riêng `img_chung_ga_con`. Tạm thời chép từ hình đại diện số 4 (`img_chung_avatar_04`) [Đề xuất]. Sau này thay hình chỉ cần ghi đè file.
- **Chỗ đứng:**
  - Màn học: góc dưới bên phải, cạnh nút "Tiếp". Không đè lên vùng học (Stage) và không đè lên nút.
  - Màn kết thúc bài: bên phải quyển sổ.
  - Danh sách bài: góc dưới bên phải.
- **Gà con không nhận chạm** [Đề xuất]. Lý do: tránh bé chạm nhầm thay vì làm bài.
- **Phản ứng:**

  | Lúc | Gà con |
  |---|---|
  | Bé làm đúng (mọi lượt có chấm đúng sai, và khi xong một bước đánh vần) | Nhảy lên 2 nhịp, hiện bong bóng "Đúng rồi!" khoảng 1,5 giây |
  | Bé chọn sai | Nghiêng đầu như đang nghĩ, khoảng 0,6 giây. Không có bong bóng |
  | Học xong bài | Nhảy lên, bong bóng "Bé ngoan quá!" |
  | Lúc khác | Đứng yên, thỉnh thoảng nhún rất nhẹ (thở) [Builder: có làm hay không] |

- **Chữ trong bong bóng** nằm ở `UiText`, không viết cứng. Bong bóng chỉ để trang trí; lời khen bé nghe vẫn là giọng đọc hiện có (`khen_01`, `khen_02`, `khen_hoan_thanh`).

## 6. Hiệu ứng chuyển động

### 6.1 Nguyên tắc
1. **Không bắt bé chờ.** Hiệu ứng phản hồi chạm chạy song song, không khoá chạm. Riêng cảnh học xong bài dài khoảng 3 giây; bé chạm vào màn thì cảnh chạy nhanh tới cuối.
2. **Ngắn.** Hiệu ứng phản hồi dưới 0,4 giây; hiệu ứng khen dưới 1,5 giây.
3. **Đi theo giọng đọc, không chạy trước giọng đọc.** Thẻ sáng lên đúng lúc mảnh âm thanh của nó phát, như hiện nay (`SequenceTimeline`).
4. **Không có hiệu ứng phạt** (mục 2).
5. **Tắt được trong test.** Có một chỗ chỉnh tốc độ hoặc tắt hiệu ứng, như `SpeechPlayer.WaitScale`, để test chạy trọn 80 bài không chậm đi [Builder: cách làm].

### 6.2 Danh sách hiệu ứng [Đề xuất, thời gian là mức gợi ý cho builder]

| Lúc | Hiệu ứng |
|---|---|
| Bé chạm thẻ hoặc nút | Lún xuống còn khoảng 92% rồi bật lại, khoảng 0,15 giây |
| App đọc tới một thẻ (đánh vần mẫu, đọc câu) | Thẻ chuyển nền cam nhạt và phồng lên khoảng 110% trong lúc mảnh âm phát, rồi trở lại |
| Các thẻ nhập thành tiếng (đánh vần) | Các thẻ trượt sát vào nhau rồi mờ đi, thẻ tiếng hiện ra, phồng 115% rồi về 100%, khoảng 0,4 giây |
| Bé làm đúng | Vài ngôi sao giấy (hình sao có viền mực) bung ra từ thẻ đúng rồi mờ đi. Tranh của bước (nếu có) lắc nhẹ. Gà con nhảy. Chấm tiến độ tô màu khi sang bước |
| Bé chọn sai | Thẻ bé chọn lắc ngang nhẹ 2–3 nhịp rồi về chỗ cũ, khoảng 0,3 giây. Không đổi màu. Gà con nghiêng đầu |
| Sai lần hai (gợi ý) | Thẻ đúng chuyển nền vàng gợi ý và nhún nhẹ lặp lại cho tới khi bé chạm |
| Kéo thả (dấu, âm, vần) | Thẻ đang kéo to lên khoảng 110% và có bóng. Thả trúng chỗ: thẻ hút vào chỗ trống. Thả trượt: thẻ bay về chỗ cũ |
| Nút "Nghe lại" | Nhún nhẹ theo nhịp trong lúc giọng đọc đang phát |
| Nút "Tiếp" hiện ra | Phóng từ nhỏ lên, nảy nhẹ, rồi nhún chậm lặp lại để mời bé bấm |
| Sang bước mới | **Lật trang sách** [Chốt 30/10/2026]: nội dung bước cũ như một trang giấy lật từ phải sang trái quanh mép trái, tối dần khi lật, để lộ bước mới nằm bên dưới. Khoảng 0,4 giây, kèm `sfx_lat_trang`. Nút "Tiếp" khi đó không phát thêm `sfx_cham`. Trong lúc lật, bé chạm được ngay vào bước mới |
| Chuyển giữa các màn (danh sách, bài, sổ…) | Mờ dần sang màn mới, khoảng 0,25 giây |
| Danh sách bài | Bài đang học tới có nền cam nhạt và nhún chậm lặp lại |

- **Thứ tự lúc bé làm đúng [Đề xuất]:**
  1. hiệu ứng khen và tiếng "ting" bắt đầu ngay;
  2. giọng khen phát như hiện nay;
  3. sang lượt hay bước sau theo luồng hiện có.

  Hiệu ứng không làm luồng chờ thêm.

### 6.3 Kéo thả và chạm cũ
Hiệu ứng là lớp trang trí. **Không đổi cách chấm đúng sai, thứ tự bước, hay luồng `LessonFlow` / `RoundFeedback`.** Test hiện có của các màn học vẫn phải xanh mà không sửa, trừ test kiểm tra màu, chữ trên nút hay ngôi sao (đổi theo thiết kế này).

## 7. Tiếng động khi tương tác

### 7.1 Danh sách tiếng [Đề xuất]

| Mã | Lúc phát | Kiểu tiếng |
|---|---|---|
| `sfx_cham` | Bé chạm thẻ hoặc nút | "tách" nhỏ, ngắn |
| `sfx_dung` | Bé làm đúng | "ting" trong, vui |
| `sfx_nhap` | Các thẻ nhập thành tiếng | "bụp" nhẹ |
| `sfx_hoa_bay` | Bông hoa bay vào sổ | "vút" nhẹ |
| `sfx_dong_dau` | Con dấu "Bé ngoan" đóng xuống | "cộp" |
| `sfx_lat_trang` | Lật trang sổ, sang bước mới trong bài | "sột" giấy |

- **Bé chọn sai: không có tiếng động riêng.** Chỉ giọng đọc mời thử lại như hiện nay [Chốt: giữ nhẹ nhàng].
- **Kéo thả** dùng `sfx_cham` khi nhấc thẻ lên. Thả trúng chỗ thì dùng `sfx_nhap` [Đề xuất].

### 7.2 Quy tắc phát [Đề xuất]
1. **Âm lượng tiếng động thấp hơn giọng đọc rõ rệt** (gợi ý khoảng 40–50% âm lượng giọng đọc) [Builder: mức cụ thể].
2. **Tiếng động có kênh phát riêng**, không dùng chung kênh với giọng đọc. Phát tiếng động không làm dừng hay cắt giọng đọc.
3. **Không chen vào chuỗi đánh vần:** trong lúc app đang phát chuỗi đánh vần hay đọc câu, `sfx_cham` và `sfx_nhap` không phát. Riêng `sfx_nhap` phát được ở khoảng nghỉ trước mảnh tiếng đã ghép [Builder: cách làm].
3b. **Chạm mà làm giọng đọc phát ngay thì không có `sfx_cham`** [Đề xuất]. Ví dụ: chạm thẻ để nghe đánh vần, chạm tiếng trong câu, chạm ô bảng ghép, nút loa. Lý do: tiếng "tách" sẽ đè lên âm đầu ("bờ"). Hiệu ứng lún thẻ vẫn chạy.
   - `sfx_cham` chỉ phát khi chạm không kèm giọng đọc tức thì: nút điều hướng (nhà, sổ, lật trang, đổi bé, mở bài), nhấc thẻ lên để kéo, thẻ ở màn chọn bé, ô trong sổ.
   - Luật này áp dụng theo từng chỗ chạm; builder đánh dấu chỗ nào phát tiếng [Builder: cách làm].
4. **Công tắc "Tiếng động" ở màn Phụ huynh**, mặc định bật. Lưu cho cả máy, không theo từng bé. Giọng đọc luôn bật.

### 7.3 Nguồn tiếng [Chốt: tìm nguồn free]

Chỉ dùng file **CC0**. Đã tìm ngày 30/10/2026:

| Nguồn | Giấy phép | Dùng cho | Đã kiểm |
|---|---|---|---|
| Kenney "Interface Sounds" (kenney.nl/assets/interface-sounds; danh sách file ở github.com/Calinou/kenney-interface-sounds) | CC0 | `sfx_cham` (các file `click_`, `tick_`, `select_`); `sfx_dung` (các file `confirmation_`, `glass_`, `pluck_`) | Đã xem tên file (99 file .wav) |
| Kenney "Impact Sounds" (kenney.nl/assets/impact-sounds) | CC0 | `sfx_dong_dau` | Trang ghi 130 file; chưa xem tên file |
| Kenney "RPG Audio" (kenney.nl/assets/rpg-audio) | CC0 | `sfx_lat_trang` (nếu có tiếng lật sách) | Trang ghi 50 file; chưa xem tên file |
| OpenGameArt "Pop sounds" (opengameart.org/content/pop-sounds) | CC0 | `sfx_nhap` (`pop1`–`pop10.ogg`) | Đã xem: 10 file ogg |
| Freesound (freesound.org), chỉ lấy file CC0 | CC0 | `sfx_hoa_bay`, và dự phòng cho tiếng nào các bộ trên không có | Chưa chọn file cụ thể |

- Trang hỗ trợ của Kenney ghi rõ mọi tài nguyên là CC0, dùng được trong dự án thương mại, không cần ghi công.
- **Cách chọn:**
  1. Claude hỏi chủ dự án một lần trước khi tải cả lô (tên gói, nguồn, dung lượng).
  2. Claude nghe, chọn mỗi mã một file, cắt hoặc chỉnh âm lượng nếu cần.
  3. Chủ dự án nghe duyệt.
- **Tách hẳn khỏi âm thanh phát âm [Chốt 30/10/2026: "âm thanh hiệu ứng không liên quan tới audio phát âm, phải phân biệt rõ ràng, tránh dùng sai dữ liệu"]:**
  - Thư mục riêng `Resources/sfx/`, không nằm trong `Resources/audio/`. Giữ định dạng gốc (ogg/wav).
  - Mã luôn bắt đầu bằng `sfx_`. Âm thanh phát âm không bao giờ có mã `sfx_`.
  - Không vào danh mục âm thanh phát âm (`audio_manifest.json`), không vào công cụ duyệt giọng đọc, không vào lệnh `tts`. Danh sách tiếng động, nguồn và giấy phép ghi riêng trong `SYSTEM_SFX` (công cụ Python).
  - Trong app: lớp phát riêng (`SfxPlayer`), hàm nạp riêng (`AssetCatalog.Sfx`). `SpeechPlayer` không phát được mã `sfx_`, `SfxPlayer` không phát được mã không có `sfx_`.
  - `validate` báo lỗi khi:
    - thư mục `audio/` có file `sfx_*`;
    - danh mục âm thanh có mã `sfx_*`;
    - thư mục `sfx/` có file không nằm trong `SYSTEM_SFX`;
    - tiếng động thiếu file hoặc giấy phép không phải CC0.
- Thêm một file ghi công trong repo (ví dụ `docs/credits-am-thanh.md`), dù CC0 không bắt buộc ghi công.
- **Nếu không tìm được file CC0 vừa ý** cho một mã: Claude báo chủ dự án. Phương án dự phòng là tự tạo tiếng đó bằng công cụ Python trong repo.

## 8. Sổ bé ngoan

### 8.1 Quy tắc [Chốt]
- **Mỗi trang sổ là một bài học.**
- **Mỗi bài có 3 bông hoa bé ngoan, thay cho 3 ngôi sao** ở màn kết thúc bài, ở danh sách bài và trong sổ.
- **3 bông hoa nằm phía trên trang. Phần bên dưới tạm để trống**, sau này sẽ có nội dung mới.
- **Tạm thời chỉ 1 hình hoa** cho mọi ô hoa.
- **Bé mở lại sổ để xem** được bất cứ lúc nào.
- **Số hoa của một bài theo đúng luật của sao hiện nay** [Đề xuất]: học xong bài là được đủ 3 hoa, không phụ thuộc số lần sai. Luật này có thể đổi sau mà không phải đổi giao diện, vì giao diện chỉ hiện "số hoa của bài" (0–3).

### 8.2 Dữ liệu [Đề xuất]
- **Số hoa của bài = số sao hiện lưu** (`ProgressStore.StarsFor`, tối đa `MaxStars` = 3). Không thêm trường mới. Nhờ vậy:
  - tiến độ cũ (bài đã học có `stars` = 3) tự hiện đủ 3 hoa, không phải chuyển đổi dữ liệu;
  - học lại bài cũ không thêm hoa (số sao chỉ giữ mức cao nhất, như hiện nay).
- Trong code và chữ giao diện, đổi cách gọi "sao" thành "hoa" ở những chỗ bé nhìn thấy. Đổi tên trường `stars` trong file tiến độ là **không** cần; giữ để đọc được file cũ [Builder: có đổi tên trong code hay không].
- **Để sau này có nhiều loại hoa/hình dán:** hình của mỗi ô hoa lấy qua một chỗ duy nhất (ví dụ hàm "hình hoa của bài X, ô thứ i"). Tạm thời hàm này luôn trả về `img_chung_hoa_be_ngoan`. Không thêm dữ liệu mới bây giờ [Builder: tên, chỗ đặt].
- **Phần dưới trang** chỉ là một vùng trống có tên riêng trong code (ví dụ "vùng nội dung của trang"), để sau này gắn nội dung mới vào mà không phải dựng lại trang [Builder: cách làm].
- **Phiên "Ôn lại" không phải một bài:** không có hoa, không có trang trong sổ. Kết thúc phiên ôn vẫn có lời khen và gà con nhảy, rồi về danh sách.

### 8.3 Trang sổ [Đề xuất]
- **Mỗi trang là một bài**, theo thứ tự bài trong danh sách bài (`lessons/index.json`). 80 bài là 80 trang.
- **Đầu trang:** "Bài N" và tên bài như ở danh sách bài (ví dụ "Bài 13 · u ư").
- **Phía trên trang: 3 ô hoa** xếp một hàng ngang, viền lam ngọc, giống ô trong sổ bé ngoan thật.
  - Ô có hoa: nền trắng, hình hoa.
  - Ô chưa có hoa: viền đứt nét nhạt, để trống.
- **Phía dưới trang:** để trống, nền giấy sáng [Chốt]. Có thể có vài đường kẻ rất nhạt như trang sổ [Builder].
- **Hai trang mở cạnh nhau** ở cả hai khung hình, tức 2 bài mỗi lần nhìn, 40 lần lật cho 80 bài. Trang trái là bài số lẻ trong thứ tự danh sách, trang phải là bài kế tiếp [Đề xuất].
- **Bài chưa mở** vẫn có trang, với 3 ô trống, để bé thấy còn bao nhiêu bài phía trước [Đề xuất].
- **Đầu sổ** (trên quyển sổ, ngoài trang) ghi "Sổ bé ngoan của <tên bé>". Chữ nằm ở `UiText`.
- Danh sách bài sau này dài thêm (Tập 2…) thì sổ tự thêm trang. Không viết cứng số 80.

### 8.4 Cảnh học xong bài (thay màn 3 ngôi sao) [Chốt: cách 1 trong bản mẫu]
Thứ tự, tổng khoảng 3 giây:
1. Màn kết thúc mở ra với quyển sổ (2 trang), **trang của bài vừa học** đang mở. 3 ô hoa của trang đó sáng viền cam.
2. **3 bông hoa lần lượt bay vào 3 ô**, cách nhau khoảng 0,3 giây. Mỗi bông có `sfx_hoa_bay`, nảy nhẹ khi chạm ô, vài cánh hoa rơi ra.
3. Con dấu đỏ "BÉ NGOAN" đóng xuống phần trống phía dưới trang (`sfx_dong_dau`), sổ rung nhẹ.
4. Gà con nhảy lên, bong bóng "Bé ngoan quá!". Giọng đọc `khen_hoan_thanh` như hiện nay.
5. Hiện nút "Về danh sách" (biểu tượng nhà) và "Học bài tiếp" (mũi tên, nền cam). Nút "Học bài tiếp" chỉ hiện khi có bài sau đã mở, như hiện nay.

Thêm:
- **Bé chạm màn khi cảnh đang chạy** thì nhảy tới cuối: hoa đã dán, dấu đã đóng, nút đã hiện.
- **Học lại một bài đã đủ 3 hoa:** sổ mở ở trang của bài đó, hoa đã có sẵn. Chỉ có dấu đóng, gà con và lời khen, không có cảnh hoa bay. (Nếu sau này luật cho số hoa ít hơn 3, thì chỉ những hoa mới được thêm mới bay vào.)
- Bài được ghi là đã học xong **ngay khi mở màn này**, như hiện nay. Thoát app giữa chừng vẫn giữ hoa.
- **Con dấu chỉ là một phần của cảnh này** [Đề xuất]. Nó mờ đi khi cảnh kết thúc (khi các nút hiện ra), không nằm lại trong sổ. Phần dưới trang vẫn trống để dành cho nội dung sau này.
- **Con dấu vẽ bằng code** (vòng tròn đôi màu đỏ son, chữ "BÉ NGOAN" bằng font của app) [Đề xuất]. Lý do: ChatGPT hay vẽ sai chữ tiếng Việt có dấu. Chữ trên dấu nằm ở `UiText`.

### 8.5 Màn Sổ bé ngoan [Chốt: có màn xem lại]
- **Mở từ nút quyển sổ** ở góc trên bên phải danh sách bài.
- **Mở ở trang có bài đứng sau cùng (theo thứ tự danh sách) trong số các bài bé đã học xong**. Chưa học bài nào thì mở trang đầu [Đề xuất]. File tiến độ không lưu thời điểm học, nên không dùng "bài học gần đây nhất".
- **Lật trang:**
  - bằng nút mũi tên hai bên, kèm `sfx_lat_trang`, hiệu ứng trang lật;
  - vuốt ngang cũng lật được [Đề xuất].
  - Hết trang thì nút mũi tên phía đó mờ đi.
- **Nút nhà** ở góc trên trái để về danh sách bài.
- Chạm vào ô hoa chỉ làm ô nhún nhẹ. Không mở bài từ sổ [Đề xuất: sổ là chỗ để xem, mở bài vẫn ở danh sách bài].
- Chưa có cách nhảy nhanh tới một trang xa (mục lục sổ). Để sau, khi chủ dự án thử thấy cần [Đề xuất].

### 8.6 Hình hoa [Chốt: vẽ cho đẹp và bắt mắt hơn]
- **Mã** `img_chung_hoa_be_ngoan`, vẽ bằng ChatGPT Kiet_1.
- **Được rực rỡ, bắt mắt hơn tranh bài học**, nhưng vẫn hợp với nét mực và màu phẳng của app. Gợi ý cho lời yêu cầu:
  - một bông hồng hồng tươi, có lá xanh và cuống;
  - viền mực đen rõ, có điểm sáng;
  - nền trong suốt hoặc giấy ngà, không chữ, không khung, tỉ lệ vuông.
- Ảnh sổ bé ngoan chủ dự án gửi chỉ để tham khảo ý tưởng, không đưa vào ChatGPT để chép, không vào repo.
- **Hình mặc định trước, hình chính thức sau [Chốt 30/10/2026]:** ChatGPT chưa tạo ảnh tiếp được, nên làm giao diện với hình mặc định. Hoa, gà con và các biểu tượng dùng file PNG mặc định do công cụ Python trong repo sinh ra (gà con chép từ hình đại diện số 4). Khi có hình chính thức thì ghi đè file cùng mã, không sửa code.

## 9. Các màn

### 9.1 Chọn bé
- Nền giấy ngà, tiêu đề "Tập đọc lớp 1".
- Mỗi bé là một thẻ to (viền mực, bóng gạch chéo) có hình đại diện và tên gọi ở nhà.
- Thẻ "+ Bé mới" cùng kiểu, có dấu cộng to.
- Chạm thẻ thì thẻ nhún, `sfx_cham`.

**Màn tạo bé:** ô nhập tên và 6 hình đại diện theo cùng kiểu thẻ. Hình đang chọn có viền cam dày và phồng nhẹ. Nút "Xong" là nút của người lớn (có chữ), vì phụ huynh thường là người nhập tên [Đề xuất].

### 9.2 Danh sách bài [Đề xuất, theo bản mẫu phần 3]
- **Thanh trên:**
  - trái: nút hình đại diện của bé (đổi bé);
  - giữa: tiêu đề;
  - phải: nút quyển sổ (Sổ bé ngoan) và nút "Phụ huynh" (nút của người lớn, có chữ).
- **Thẻ bài:** viền mực, bo góc, ghi "Bài N" và chữ của bài như hiện nay.
  - Đã học: có **hàng 3 bông hoa nhỏ** ở phía dưới thẻ, đúng chỗ hàng 3 ngôi sao hiện nay. Số hoa hiện theo số hoa của bài (mục 8.2).
  - Đang học tới (bài đầu tiên đã mở mà chưa học xong): nền cam nhạt, nhún chậm.
  - Chưa mở: nền và chữ nhạt, có ổ khoá, chạm không vào bài (giữ như hiện nay).
- **Chia phần** "Chữ cái và âm" / "Vần" và cuộn dọc như hiện nay. Mở màn thì cuộn sẵn tới bài đang học tới [Đề xuất].
- **Nút "Ôn lại":** nút tròn có biểu tượng mũi tên vòng, ở góc dưới bên trái. Chỉ bấm được khi có lượt nhầm, như hiện nay (khi không có lượt nhầm thì mờ đi).
- **Gà con** ở góc dưới bên phải.

### 9.3 Màn học bài
- Nút tròn có biểu tượng:
  - nhà (góc trên trái);
  - loa (góc dưới trái);
  - mũi tên "Tiếp" (góc dưới phải, chỉ hiện khi bước cho phép đi tiếp, như hiện nay).
- Hàng chấm tiến độ ở giữa phía trên. Gà con cạnh nút "Tiếp".
- **Nút "Ghi chú"** (chỉ có ở bài có ghi chú) là nút của người lớn ở góc trên phải, giữ như hiện nay nhưng đổi sang kiểu mới.
- Mọi bước học (đánh vần, bảng ghép, bảng dấu, câu, đọc thêm, bảng ôn vần…) và mọi bài luyện tập dùng thẻ kiểu mới (mục 4.2) và hiệu ứng mục 6.
- **Bố cục bên trong từng bước giữ như hiện nay**, chỉ đổi hình khối, màu, hiệu ứng. Riêng khung tranh có bóng gạch chéo.
- Nút "Con đọc xong rồi" ở bước câu: nút tròn to có dấu tích, nền cam.

### 9.4 Màn kết thúc bài
Theo mục 8.4.

### 9.5 Màn của người lớn: Phụ huynh, khóa phụ huynh, Ghi chú, Chú ý và Phụ lục [Đề xuất]
- Đổi sang cùng nền, viền mực, màu và kiểu nút của người lớn cho đồng bộ.
- Vẫn dùng chữ. Không có gà con, không có hiệu ứng vui, không có sao giấy.
- Màn Phụ huynh thêm **công tắc "Tiếng động"** (mục 7.2).
- Phép cộng khoá phụ huynh giữ nguyên cách làm.

## 10. Tài nguyên mới

| Mã | Loại | Nguồn |
|---|---|---|
| `img_chung_hoa_be_ngoan` | Tranh | ChatGPT Kiet_1 (mục 8.6) |
| `img_chung_ga_con` | Tranh | Tạm chép từ `img_chung_avatar_04` |
| `img_ui_*` (nhà, loa, mũi tên phải, mũi tên trái, sổ, vòng ôn lại, dấu tích, ổ khoá, sao giấy) | Biểu tượng | [Builder]: vẽ SVG trong repo hoặc PNG. Theo phong cách nét mực, mục 4.2 |
| `sfx_*` (6 mã, mục 7.1) | Tiếng động | Bộ CC0, mục 7.3 |

- Mã mới khai báo cùng chỗ với `SystemImages` / `SystemAudio`. Công cụ Python biết các mã này (danh mục, `validate`), giống tài nguyên hệ thống hiện có.
- **Thiếu file thì app vẫn chạy:**
  - thiếu hình: vẽ tạm bằng code;
  - thiếu tiếng: bỏ qua;
  - báo lỗi rõ trong chế độ phát triển, như hiện nay.
- `img_chung_sao` không còn dùng ở giao diện. Giữ file hay xoá là [Builder]; nếu xoá thì xoá cả khỏi danh mục và test.

## 11. Cách kiểm tra

**Test tự động (Claude viết, chạy bằng `python tools/run_unity_tests.py editmode|playmode` và test Python):**
- Toàn bộ test hiện có vẫn xanh. Test kiểm tra 3 ngôi sao, chữ trên nút đổi thành biểu tượng thì sửa theo thiết kế này.
- **Sổ bé ngoan:**
  - học xong bài thì trang của bài đó có đủ 3 hoa, và danh sách bài hiện 3 hoa nhỏ ở thẻ bài;
  - học lại không thêm hoa;
  - phiên ôn lại không thêm hoa, không có trang;
  - tiến độ cũ (file có `stars` = 3) hiện đủ 3 hoa;
  - số trang bằng số bài trong danh sách, không viết cứng;
  - mở sổ ở đúng trang (mục 8.5), lật trang tới đầu hoặc cuối thì nút phía đó mờ đi;
  - trang có vùng nội dung phía dưới để trống.
- **Tiếng động:**
  - tắt công tắc thì không phát `sfx_*`, giọng đọc vẫn phát;
  - trong lúc phát chuỗi đánh vần thì không phát `sfx_cham`;
  - thiếu file tiếng thì không lỗi.
- **Bố cục:** `LayoutProbe` ở 2400×1080 và 2048×1536 cho các màn mới và màn đã đổi (sổ, kết thúc bài, danh sách bài, chọn bé, màn học có gà con và chấm tiến độ). Vùng chạm ≥ 160, chữ không tràn, gà con không đè nút và không đè Stage.
- **Hiệu ứng không làm chậm test:** test chạy trọn 80 bài tắt hoặc tăng tốc hiệu ứng (mục 6.1). Có ít nhất một test chạy với hiệu ứng bật để chắc không lỗi.
- **Python:** `validate` biết loại `sfx` và mã tranh mới; `tts` không đụng tới `sfx`.

**Chủ dự án xem:** ảnh chụp màn hình do test sinh ra ở `TestOutput/screens/`. Không build bản thử, chỉ commit.

## 12. Thứ tự làm [Đề xuất]

1. **Nền móng:** bảng màu, hình khối (thẻ, nút tròn, bóng gạch chéo), biểu tượng, công cụ hiệu ứng nhỏ, kênh tiếng động. Đổi kiểu cho mọi màn, chưa có hiệu ứng mới.
2. **Hiệu ứng và tiếng động trong màn học**, gà con, chấm tiến độ. Tải và chọn tiếng (hỏi chủ dự án trước khi tải).
3. **Sổ bé ngoan:** cảnh học xong bài, màn sổ, hoa ở danh sách bài. Vẽ hình hoa bằng ChatGPT.
4. **Màn của người lớn** đổi kiểu, thêm công tắc tiếng động.

Mỗi bước một hoặc vài commit rõ ràng trên `main`.

## 13. Builder tự quyết
- Cách vẽ khung bo góc, bóng gạch chéo, biểu tượng (mục 4.2).
- Cách làm hiệu ứng: tự viết bộ chạy hiệu ứng nhỏ bằng code hay dùng gói có sẵn của Unity. Không mua gói trả phí.
- Định dạng file tiếng động, mức âm lượng cụ thể.
- Chỗ lưu công tắc tiếng động trong file tiến độ hay file cài đặt riêng.
- Tên lớp, chỗ đặt code mới.
- Ngưỡng đổi từ chấm tiến độ sang thanh tiến độ.

## 14. Việc để sau
- Gà con sinh động hơn: nhiều tư thế, biểu cảm, có thể biết nói [Chốt: để sau].
- Nhiều loại hoa, hình dán, nội dung cho phần dưới mỗi trang sổ, sự kiện mới trong Sổ bé ngoan [Chốt: để sau].
- Luật cho số hoa khác "học xong là đủ 3" (ví dụ theo số lần sai), nếu chủ dự án muốn.
- Chỉnh hiệu ứng và tiếng động sau khi có bé thử app thật.
