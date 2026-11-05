# Thiết kế: tỷ lệ màn hình cho điện thoại và máy tính bảng

> Ngày 05/11/2026. Chủ dự án chọn **cách B** trong bản mẫu so sánh A/B/C (trang tạm, không nằm trong git: `.superpowers/brainstorm/3120-1793867285/content/ty-le-man-hinh.html`).
>
> Ký hiệu:
> - **[Chốt]**: chủ dự án đã quyết.
> - **[Đề xuất]**: người viết đề xuất, chủ dự án đã nghe phần mô tả và đồng ý chung.
> - **[Builder]**: để người làm tự quyết.

## 1. Mục đích

App "Tập đọc lớp 1" ra bản **Android (APK) và iOS trước**, chạy trên **điện thoại và máy tính bảng** [Chốt]. Mục tiêu của chủ dự án: **dễ nhìn, dễ học, dễ tương tác** [Chốt].

**Hiện nay:**
- App chỉ chạy màn ngang.
- Mọi màn dựng trong một khung rộng 1440 đơn vị (tỷ lệ 4:3 ở chiều cao 1080), đặt giữa màn hình.
- Trên điện thoại (màn 19,5:9 đến 20:9), khoảng 40% chiều ngang chỉ là giấy trống. Các nút nằm ở dải trên và dải dưới, lấy mất chỗ của tranh và thẻ chữ, nên thẻ chữ chỉ còn khoảng 1 cm.
- App chưa tránh tai thỏ, góc bo và thanh vuốt của máy.

## 2. Đã chốt

1. **Cách B: màn ngang, co giãn theo máy [Chốt].**
   - Máy tính bảng giữ bố cục như hiện nay.
   - Điện thoại: các nút của bé dạt ra hai mép màn, phần học ở giữa to lên.
   - Chỉ một bộ dựng, không có bố cục màn dọc riêng.
2. **Màn ngang** trên mọi máy. Xoay máy 180° thì app xoay theo [Chốt, như hiện nay].
3. **Không có màn dọc riêng cho điện thoại** (cách C bị loại) [Chốt].

## 3. Mục tiêu, không làm, điều cấm

**Mục tiêu**
- Trên điện thoại, tranh và thẻ chữ của màn học to hơn rõ rệt so với hiện nay.
  - Mức to thêm tuỳ máy: khoảng 15% (iPhone có tai thỏ) đến khoảng 35% (điện thoại Android 20:9 có lỗ camera nhỏ).
  - Bản mẫu ghi "khoảng 30%" là số tròn; con số thật do mục 5.2 quyết định.
- Trên máy tính bảng, bố cục không đổi so với hiện nay.
- Không nút, thẻ hay chữ nào nằm dưới tai thỏ, lỗ camera, góc bo hay thanh vuốt.
- Máy tính bảng bị xoay dọc, hoặc cửa sổ app bị thu nhỏ (chia đôi màn trên iPad và máy tính bảng Android), thì app vẫn dùng được, không mất chữ, không mất nút (mục 5.6).

**Không làm**
- Không có bố cục màn dọc riêng.
- Không đổi phong cách SGK, bảng màu, biểu tượng, hiệu ứng, tiếng động.
- Không đổi nội dung hay thứ tự bên trong từng bước học.
- Không build bản Android hay iOS, chỉ commit (như các việc trước).

**Điều cấm** (làm ra như vậy là hỏng, dù chạy được)
- Vùng chạm nhỏ hơn 160 đơn vị canvas, hoặc chữ bị tràn, trên bất kỳ cỡ màn nào trong mục 7.
- Nút nhảy chỗ hay phần học đổi cỡ giữa các bước của cùng một bài trên cùng một máy. Bé phải thấy nút ở chỗ quen.
- Đổi cỡ cửa sổ hay xoay máy làm bước học chạy lại từ đầu, phát lại giọng đọc, mất tiến độ hay mất thẻ đang kéo dở.
- Khoảng trống lớn chỉ dồn về một bên khiến màn trông lệch. Nội dung giữ cân giữa màn.

## 4. Các máy cần hỗ trợ

Đổi ra đơn vị canvas ở chiều cao 1080, màn ngang.

| Máy | Điểm ảnh (ngang) | Canvas | Ghi chú |
|---|---|---|---|
| Điện thoại Android 20:9 | 2400×1080 | 2400×1080 | lỗ camera ở một mép; thanh điều hướng có thể ở mép |
| iPhone có tai thỏ / Dynamic Island (19,5:9) | 2556×1179 | ≈2341×1080 | vùng an toàn: mỗi bên trái, phải khoảng 160 đơn vị; dưới khoảng 58 (thanh vuốt) |
| Điện thoại 16:9 (iPhone SE, Android cũ) | 1334×750 | ≈1921×1080 | không tai thỏ |
| iPad 10,9" / Air | 2360×1640 | ≈1554×1080 | dưới khoảng 26 (thanh vuốt) |
| iPad mini | 2266×1488 | ≈1645×1080 | |
| iPad 4:3 / iPad Pro 13" | 2048×1536, 2752×2064 | 1440×1080 | |
| Máy tính bảng Android 16:10 | 2560×1600 | 1728×1080 | |
| Màn trong của máy gập | ≈2208×1840 | xem mục 5.6 | gần vuông |
| Máy tính bảng xoay dọc / cửa sổ hẹp | ví dụ 1536×2048 | xem mục 5.6 | xảy ra vì quy định mới của Android 16 và iPadOS 26 (mục 6) |

## 5. Cách hoạt động

### 5.1 Khung chung
- **Nền giấy** phủ hết màn, kể cả phần dưới tai thỏ và thanh vuốt (như hiện nay).
- **Vùng an toàn của máy** (vùng không bị tai thỏ, góc bo, thanh vuốt che) lấy từ hệ điều hành.
  - Mọi thứ bé nhìn hay chạm đều nằm trong vùng này.
  - Phần lề hai bên **lấy đối xứng** theo bên lớn hơn, để nội dung luôn cân giữa màn. Lề không đổi khi bé xoay máy 180° (tai thỏ đổi bên).
- **Khung 1440 hiện nay** (`UiKit.SafeWidth`) vẫn là khung chuẩn của máy tính bảng. Các màn không nói gì ở mục 5.4 thì giữ khung này, đặt giữa vùng an toàn.

### 5.2 Màn học: hai kiểu đặt nút
**Kiểu góc** (như hiện nay), dùng khi màn hẹp:
- Nút Về nhà ở góc trên trái, nút Loa ở góc dưới trái, nút Tiếp ở góc dưới phải, tất cả trong khung 1440.
- Dải trên và dải dưới (mỗi dải 200) dành cho nút. Phần học (`Stage`) là 1400×680 ở giữa.

**Kiểu mép**, dùng khi màn đủ rộng:
- Nút Về nhà và nút Loa ở **dải mép trái**: Về nhà ở trên, Loa ở dưới.
- Nút Tiếp ở **dải mép phải**, phía dưới.
- Mỗi dải mép rộng vừa một nút tròn 160 cộng lề, nằm trong vùng an toàn của máy.
- Hàng chấm tiến độ vẫn ở trên, giữa màn.
- Phần học chiếm phần còn lại ở giữa, gần hết chiều cao. Nó được **phóng to đều** từ 1400×680 lên vừa chỗ trống:
  - giữ nguyên tỷ lệ;
  - mọi thứ bên trong bước học (thẻ, tranh, ô thả, chữ) to lên cùng một mức;
  - bố cục bên trong không đổi.
- Gà con ở dải mép phải, phía trên nút Tiếp [Đề xuất; chỗ cụ thể là Builder].
- Nút "Ghi chú" (nút của người lớn, có chữ) ở góc trên phải [Builder: chỗ đặt sao cho không che phần học, không dưới tai thỏ].

**Chọn kiểu:** dùng kiểu mép khi kiểu đó cho phần học **to hơn** kiểu góc. Ngược lại dùng kiểu góc.
- Theo bảng mục 4: điện thoại 19,5:9 và 20:9 dùng kiểu mép.
- iPad và máy tính bảng 16:10 dùng kiểu góc.
- Màn 16:9 nằm gần ngưỡng [Builder: ngưỡng và cách tính].
- Ngay ở ngưỡng, hai kiểu cho phần học gần bằng nhau, nên không có cú nhảy cỡ lớn.

**Không đổi kiểu giữa chừng:** kiểu và mức phóng to chỉ tính lại khi kích thước màn hay vùng an toàn thật sự đổi (xoay dọc trên máy tính bảng, đổi cỡ cửa sổ). Không tính lại khi sang bước.

**Hiệu ứng vẫn đúng chỗ ở cả hai kiểu:** lật trang, sao giấy bung ra, thẻ bay về chỗ, kéo thả, thẻ sáng theo giọng đọc. Ví dụ: kéo thẻ trong phần học đã phóng to thì thẻ vẫn bám ngón tay.

### 5.3 Ví dụ cỡ thật (ước lượng)

| Máy | Kiểu | Thẻ chữ 160 đơn vị trên màn thật |
|---|---|---|
| Điện thoại 6,7" (hiện nay) | góc | ≈ 1,0 cm |
| Điện thoại Android 20:9, theo thiết kế này | mép | ≈ 1,3–1,4 cm |
| iPhone 6,1–6,7" có tai thỏ, theo thiết kế này | mép | ≈ 1,1–1,2 cm |
| iPad 10,9" | góc | ≈ 2,3 cm |

### 5.4 Các màn khác

| Màn | Trên điện thoại (màn rộng) | Trên máy tính bảng |
|---|---|---|
| **Danh sách bài** | Lưới thẻ bài dùng thêm chiều ngang: **thêm cột** thay vì phóng to thẻ (hiện 6 cột × 216). Nút Sổ bé ngoan, Phụ huynh, tiêu đề ra theo mép vùng an toàn [Đề xuất; số cột là Builder] | như hiện nay |
| **Sổ bé ngoan** | Hai trang sổ **to lên** vừa chỗ trống. Nút lật trước/sau ra hai dải mép. Nút Về nhà ở dải mép trái [Đề xuất] | như hiện nay |
| **Cảnh học xong bài** | Trang sổ, con dấu, gà con ở giữa, to lên theo chỗ trống. Các nút (Về danh sách, Học lại, Bài tiếp…) ra hai dải mép như màn học [Đề xuất; chia nút trái/phải là Builder] | như hiện nay |
| **Màn chọn bé / tạo bé** | Thẻ bé và hình đại diện ở giữa. Nút ra mép. Hàng thẻ bé có thể dài thêm [Builder] | như hiện nay |
| **Màn Phụ huynh, cổng phụ huynh, khung Ghi chú, màn chuẩn bị (tải dữ liệu)** | **giữ khung 1440**, đặt giữa vùng an toàn [Đề xuất: người lớn dùng, không cần to thêm] | như hiện nay |

Yêu cầu chung cho mọi màn ở mọi cỡ trong mục 7:
- vùng chạm ≥ 160;
- chữ không tràn;
- không gì nằm ngoài vùng an toàn.

### 5.5 Tai thỏ, góc bo, thanh vuốt
- Lấy vùng an toàn của hệ điều hành lúc mở app, và lấy lại khi nó đổi.
- Các nút ở dải mép trên điện thoại có tai thỏ nằm **bên trong** lề an toàn: không nằm cạnh tai thỏ, kể cả ở góc trên và góc dưới (góc bo).
- Code đọc vùng an toàn qua **một chỗ duy nhất có thể thay khi test** (ví dụ một hàm trả về vùng an toàn, test gán vùng giả lập tai thỏ). Lý do: test chạy trong Unity Editor, nơi không có tai thỏ thật [Builder: cách làm].

### 5.6 Máy tính bảng xoay dọc, cửa sổ hẹp, máy gập
Trường hợp này không chọn được nhưng phải chạy được, vì hai quy định mới (mục 6):
- máy tính bảng Android có thể bỏ qua khoá màn ngang;
- iPad có thể cho đổi cỡ cửa sổ tự do.

Khi màn **hẹp hơn 4:3** (xoay dọc, cửa sổ chia đôi, màn gập gần vuông):
- **Giữ nguyên bố cục ngang kiểu góc**, thu nhỏ đều cho vừa chiều ngang, đặt giữa màn.
- Phần thừa trên và dưới là nền giấy.
- Không có bố cục dọc riêng (đúng mục 2).

Ví dụ: iPad xoay dọc 1536×2048 thì khung ngang 1440×1080 nằm giữa, rộng hết màn, trên dưới là giấy. Thẻ chữ 160 trên iPad dọc còn khoảng 1,7 cm, vẫn to hơn điện thoại hiện nay.

[Builder: cách làm. Gợi ý: đổi `CanvasScaler` sang kiểu mở rộng (Expand) với cỡ chuẩn 1440×1080. Màn rộng thì canvas cao 1080 và rộng theo màn; màn hẹp thì canvas rộng 1440 và cao theo màn. Nhờ vậy khung 1440×1080 luôn vừa.]

**Đổi cỡ khi đang chạy:** xoay máy hay đổi cỡ cửa sổ giữa lúc học thì bố cục dựng lại theo cỡ mới. Bước học **không chạy lại**, giọng đọc không phát lại, tiến độ không mất. Nếu bé đang kéo dở một thẻ thì thẻ về chỗ cũ là được [Builder: cách làm].

Ở các màn khác, khi đổi cỡ thì **được dựng lại màn**, nhưng giữ những gì bé hay phụ huynh đang làm dở [Quyết định của người viết]:
- Danh sách bài giữ chỗ đang cuộn tới.
- Sổ bé ngoan giữ trang đang mở.
- Màn tạo bé giữ tên đang gõ và hình đại diện đang chọn.
- Cổng phụ huynh giữ câu hỏi và phần đã nhập. Nếu khó giữ phần đã nhập thì ra câu hỏi mới là chấp nhận được.
- Cảnh học xong bài **nhảy tới cuối** (hoa đã dán, dấu đã đóng, nút đã hiện) như khi bé chạm màn. Không chạy lại cảnh, không phát lại lời khen.
- Màn Phụ huynh, khung Ghi chú, màn chuẩn bị: dựng lại theo cỡ mới.

Tiếng hay giọng đọc đang phát thì không bị phát lại.

### 5.7 Cài đặt nền tảng
- **Android:**
  - Khoá màn ngang (trái và phải) như hiện nay.
  - Target API theo yêu cầu Google Play hiện hành (mục 6).
  - Không cần tắt hành vi mới của Android 16 trên máy tính bảng, vì mục 5.6 đã xử lý [Đề xuất].
- **iOS:**
  - Khoá màn ngang như hiện nay. Giữ `UIRequiresFullScreen` đang bật trong ProjectSettings cho các bản iPadOS cũ.
  - Không dựa vào nó trên iPadOS 26 trở đi (mục 6); mục 5.6 xử lý trường hợp cửa sổ đổi cỡ [Đề xuất].

## 6. Ràng buộc bên ngoài (đã tra ngày 05/11/2026)

- **Google Play:** từ 31/08/2026, app mới và bản cập nhật phải nhắm Android 16 (API 36).
  - Với API 36, máy có cạnh ngắn ≥ 600dp (máy tính bảng, màn gập) **bỏ qua khoá hướng màn và tỷ lệ**; app có thể bị chia cửa sổ.
  - Hiện còn cách tắt tạm (`PROPERTY_COMPAT_ALLOW_RESTRICTED_RESIZABILITY`). Theo nguồn thứ cấp, Android 17 sẽ bỏ cách tắt này.
  - Trò chơi (`android:appCategory="game"`) được miễn; app học đọc không nên khai là trò chơi.
- **iPadOS 26:** `UIRequiresFullScreen` bị bỏ dần. Apple cảnh báo sắp bắt buộc app hỗ trợ mọi hướng xoay và cỡ cửa sổ.
- **Unity 6.6:** uGUI dựng hoàn toàn bằng code (không prefab), TMP với font Andika. Canvas hiện là `ScaleWithScreenSize` 1920×1080, khớp theo chiều cao. `AndroidTargetSdkVersion` đang để tự động.

Nguồn:
- https://developer.android.com/develop/adaptive-apps/guides/app-orientation-aspect-ratio-resizability
- https://developer.android.com/google/play/requirements/target-sdk
- https://developer.apple.com/forums/thread/793406

## 7. Kiểm tra

**Test bố cục (`LayoutProbe`)** chạy ở các cỡ:
- 2400×1080 không tai thỏ;
- 2400×1080 có lỗ camera một bên;
- 2556×1179 có vùng an toàn kiểu iPhone (trái, phải, dưới);
- 1334×750;
- 2360×1640 có thanh vuốt;
- 2048×1536;
- 2560×1600;
- 1536×2048 (máy tính bảng dọc);
- 2208×1840 (màn gập).

Mỗi cỡ kiểm:
- vùng chạm ≥ 160;
- chữ không tràn;
- **mọi vùng chạm và chữ nằm trong vùng an toàn**;
- nội dung cân giữa màn.

**Test hành vi:**
- Chọn đúng kiểu góc/mép theo cỡ màn.
- Kiểu và cỡ phần học không đổi khi sang bước.
- Đổi cỡ màn giữa bước thì bước không chạy lại, giọng đọc không phát lại.
- Kéo thả và hiệu ứng đúng chỗ khi phần học đang phóng to.

**Chạy test:** trong lúc làm, chỉ chạy test của phần đang làm. Việc này đổi canvas và khung chung của mọi màn, nên **khi làm xong, người làm xin chủ dự án lệnh "test all"** rồi mới báo xong. Không tự chạy bộ đầy đủ khi chưa được nói [Quyết định của người viết, theo quy tắc của dự án].

Test cũ có giá trị mong đợi gắn với canvas 1920 hay khung 1440 (ví dụ `ScreenProbe` mặc định 1920×1080, các test so độ rộng theo `SafeWidth`) thì được sửa theo thiết kế mới. Không được nới các kiểm tra vùng chạm ≥ 160 và chữ không tràn.

**Chủ dự án xem:** ảnh chụp màn hình do test sinh ra ở `TestOutput/screens/`, mỗi màn chính ở điện thoại 20:9, iPhone tai thỏ, iPad, máy tính bảng dọc. Không build bản thử.

## 8. Để người làm quyết [Builder]
- Công thức chọn kiểu góc/mép và ngưỡng; độ rộng dải mép; lề.
- Cách phóng to phần học: phóng to đều cả khối, hay đổi cỡ thật rồi để các bước tự dựng. Gợi ý phóng to đều, vì các bước đang dựng theo 1400×680.
- Số cột của danh sách bài trên màn rộng; cách chia nút trái/phải ở cảnh học xong bài và màn chọn bé.
- Chỗ đặt nút Ghi chú và gà con ở kiểu mép.
- Cách lấy và giả lập vùng an toàn; cách dựng lại bố cục khi đổi cỡ.
- Có tắt tạm hành vi mới của Android 16 hay không (đề xuất là không).

## 9. Ngoài phạm vi
- Bố cục màn dọc riêng; chế độ cho máy tính để bàn và web.
- Build và thử trên máy thật (sau này chủ dự án tự làm).
- Đổi giao diện, hình, tiếng.
