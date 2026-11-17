# Nâng cấp UI toàn app theo nghiên cứu — thiết kế (17/11/2026)

Trạng thái: **root duyệt 17/11 (thay chủ dự án), kèm 7 chỉnh sửa đã ghi vào spec** (đánh dấu "Root 17/11"). Làm theo đợt, root kiểm từng đợt.

Ảnh mẫu (khung 2400×1080, vẽ bằng HTML với tranh, phông, màu thật của app): thư mục [2026-11-17-nang-cap-ui/](2026-11-17-nang-cap-ui/). Số đỏ trên ảnh khớp số mục trong spec. Chụp lại ảnh mẫu: `sh 2026-11-17-nang-cap-ui/render.sh <tên>` (Edge chạy ngầm, hồ sơ riêng).

Hiện trạng: ảnh chụp 17/11 trong `unity/TapDoc/TestOutput/screens/phone_20x9/` (2400×1080) và `ipad_43/` (2048×1536), tên `app_*.png`. Ảnh các bước bài học (`tv1_t1_b*_*.png`) chụp 5/11, giao diện bước học không đổi từ đó.

## 1. Mục đích

Lời chủ dự án (17/11):

> "về UI mình muốn bạn improve, sáng tạo cho thật hay, với tiêu chí phù hợp cho việc học của trẻ em, phù hợp cho phụ huynh quản lý, tạo cảm giác học tập, thu hút sự tập trung của bé để bé tập trung học, cảm thấy thích thú."

Chủ dự án muốn dựa trên nghiên cứu. Bốn mục tiêu:
- bé tập trung vào chữ;
- bé biết mình đang ở đâu và làm gì tiếp;
- bé thấy vui vì tiến bộ thật;
- phụ huynh biết con học gì và biết làm gì cùng con.

## 2. Nguyên tắc rút từ nghiên cứu

| # | Nguyên tắc | Nguồn | Áp dụng ở |
|---|---|---|---|
| N1 | Mọi thứ động và có tiếng phải phục vụ việc đọc. Đồ trang trí chạm được, trò phụ không gắn bài làm trẻ hiểu bài kém hơn. Hình động và tiếng khớp nội dung thì giúp. | Takacs, Swart, Bus 2015, meta-analysis 43 nghiên cứu ([PMC4647204](https://pmc.ncbi.nlm.nih.gov/articles/PMC4647204)); Bus, Takacs, Kegel 2015 | Cảnh nền không chạm được và nhạt. Gà con chỉ vào chữ đang đọc. Tem thưởng là tranh của bài. |
| N2 | Vùng chạm cho trẻ phải to: khoảng 2 cm. Trẻ chạm trượt nhiều hơn người lớn (46% so với 32% ở trẻ 7–11 tuổi). Chạm dễ hơn kéo thả. | NN/g [children-ux-physical-development](https://www.nngroup.com/articles/children-ux-physical-development/); Brown & Anthony CHI 2012 | Nút của bé to hơn trên điện thoại, vùng nhận chạm rộng hơn hình. |
| N3 | Phản hồi ngay, to, rõ, cả tiếng lẫn hình. Trẻ dưới 6 tuổi không để ý phản hồi tinh tế. | NN/g [kids-cognition](https://www.nngroup.com/articles/kids-cognition/) | Hạt tiến độ to, gà con đi theo, nút Tiếp phát sáng. |
| N4 | Lời dẫn bằng giọng nói. Có nhân vật chào bé. Bé ngồi im lâu thì nhắc bước tiếp. Sai thì khích lệ, gợi ý từng bước, không phạt. | Sesame Workshop / Joan Ganz Cooney Center ([bài](https://joanganzcooneycenter.org/?p=19607)) | Lời chào. Nhắc khi ngồi im. Bàn tay gợi ý. Giữ cách gợi ý từng bước khi sai (đã có). |
| N5 | Bốn trụ cột của app học tốt: chủ động, tập trung, có nghĩa, có tương tác xã hội. App miễn phí thường điểm thấp vì nhiều thứ gây phân tâm. | Hirsh-Pasek và cộng sự 2015 ([APS](https://www.psychologicalscience.org/publications/educational-apps.html)) | Không thêm trò phụ. Gợi ý chơi cùng bố mẹ gắn với bài. |
| N6 | Thưởng cho tiến bộ thật, không dùng điểm số hay bảng xếp hạng. Khen cách làm (chịu khó, tự sửa), không khen "thông minh". | Mueller & Dweck 1998; Dweck | Tem bài học. Câu khen theo cách bé đã làm. Không thêm điểm. |
| N7 | Ẩn dụ quen thuộc ngoài đời giúp trẻ hiểu nhanh. | NN/g | Con đường đến trường, quyển sổ dán tem, tủ sách. |
| N8 | Bố mẹ học cùng con (joint media engagement) giúp con học tốt hơn. Phụ huynh cần gợi ý cụ thể để làm cùng con, không cần bảng số liệu. | Digital Promise ([JME](https://digitalpromise.dspacedirect.org/handle/20.500.12265/121)); Kidaptive Learner Mosaic | Mục "Chơi cùng con". |
| N9 | Rời màn hình dễ hơn khi dừng ở điểm dừng tự nhiên và có thói quen. Cảnh báo "còn 2 phút" lại làm trẻ khó chịu hơn. AAP: gia đình tự đặt giới hạn đều đặn. | Hiniker và cộng sự, Đại học Washington 2016 ([tin](https://www.washington.edu/news/2016/05/05/two-minute-warnings-make-kids-screen-time-tantrums-worse/)); AAP | Nghỉ mắt chỉ sau khi xong bài, không đếm ngược, không khoá cứng. Phụ huynh đặt số bài. |
| N10 | Thấy rõ mình gần tới đích thì cố gắng hơn (goal gradient). Đây là lý thuyết chung, ít bằng chứng riêng cho trẻ nhỏ, nên chỉ dùng ở mức hiện tiến độ. | Hull 1932; Kivetz và cộng sự 2006 | Con đường bài học, hạt tiến độ có đích là bông hoa. Không dùng chuỗi ngày (streak). |

## 3. Rà hiện trạng

| Màn | Thấy gì (ảnh 17/11) | Chưa đạt nguyên tắc |
|---|---|---|
| Chọn bé `app_profiles` | Tiêu đề "Bờ A Ba". Thẻ bé 250×265 giữa nền trống. Có nút bánh răng. | N4: chưa có ai chào bé, không có tiếng. N7: chưa có cảm giác bước vào lớp học. |
| Tủ sách `app_shelf` | 4 bìa trên kệ, quyển đang học viền cam và nhấp nháy, gà con đứng yên ở góc. | Khá ổn. Gà con chưa gắn với quyển đang học. Muốn học tiếp phải chạm bìa rồi chạm bài: 2 lần chạm. |
| Danh sách bài `app_lesson_list_*` | Lưới thẻ 6–10 cột, mỗi thẻ "Bài n" + chữ + 3 hoa. Quyển 3 có 133 thẻ, cuộn dọc dài. | N3, N7, N10: bé khó thấy mình đang ở đâu và đã đi được bao xa. Thẻ trông giống nhau. Gà con đứng yên ở góc. |
| Màn học `app_lesson_chrome`, `tv1_*` | Thẻ chữ hoặc tranh giữa nền trống rộng. Chấm tiến độ 26 đơn vị ở mép trên, tới 20 chấm. Gà con ở góc phải dưới. Loa và nhà 160. | N2: trên điện thoại 2400×1080, 160 đơn vị chỉ khoảng 1 cm. N3: chấm tiến độ nhỏ. N4: không có nhắc khi bé ngồi im (code không có bộ đếm). Khoảng trống chưa dùng cho nội dung. |
| Xong bài `app_result` | Sổ hai trang: 3 ô hoa, nửa dưới trang trống. Gà con nói "Bé ngoan quá!". | N6: khen chung chung. Phần thưởng chưa gắn nội dung bài. Trang trống. |
| Sổ bé ngoan `app_book` | Mỗi trang một bài: 3 ô hoa. | Như trên. Không có gì gợi lại bài đã học. |
| Phụ huynh `app_parent` | Khoá phép tính, rồi mỗi bé: tiến độ theo quyển, "Mở mọi bài", chữ hay nhầm. | N8: chưa có gợi ý làm cùng con. Chưa thấy theo thời gian (tuần này). Chưa đặt được thời lượng (N9). Chữ hay nhầm không nghe được. |
| Mở đầu, thông báo, cài đặt | Ổn, mới làm 9/11. | Không đổi trong đợt này. |

Đo vùng chạm: canvas tham chiếu 1440×1080, chế độ Expand.
- **Điện thoại 2400×1080** (6,5", khoảng 400 ppi): 1 đơn vị bằng 1 điểm ảnh, nên 160 đơn vị khoảng 10 mm.
- **iPad 2048×1536** (264 ppi): 1 đơn vị bằng 1,42 điểm ảnh, nên 160 đơn vị khoảng 22 mm.
- **Kết luận:** điện thoại mới là chỗ thiếu.

## 4. Đề xuất theo màn

### 4.1 Màn học (ảnh mẫu `m1_man_hoc.png`)

**Nguyên tắc chỗ đứng:** kích thước nội dung thắng. Mọi thứ thêm vào chỉ dùng dải trên, dải bên và dải dưới đã có của `ScreenLayout`, không thu nhỏ khung bước học. Ảnh mẫu `m1` minh hoạ cách nhìn, không phải toạ độ.

1. **Con đường bài học thay chấm tiến độ.**
   - Các hạt to (40 đơn vị, hạt đang học 56) xếp trên đường nét đứt hơi lượn, nằm gọn trong dải trên (70 ở khung rộng, rộng hơn ở 4:3). Hạt đã qua xanh, hạt đang học cam, hạt chưa tới giấy sáng.
   - Hạt đang học là hạt cam to hơn (56), nhún nhẹ; qua bước thì hạt cam chuyển sang hạt sau. **Không có gà con trên đường**: màn học chỉ có một gà con, ở dải bên (Root 17/11, N1). Cuối đường là bông hoa của Sổ bé ngoan.
   - Bài quá 20 bước thì bỏ hạt, chỉ còn đường và gà con đi trên đó (thay thanh tiến độ hiện nay).
   - Không chạm được, không làm bé chờ: gà con nhảy song song với lật trang.
   - Lý do: N3, N7, N10.
2. **Gà con làm bạn học.**
   - Gà con giữ chỗ hiện nay (dải bên, trên nút Tiếp ở khung rộng; góc ở 4:3), to bằng hết bề rộng dải (khoảng 180), không vào khung bước học.
   - Khi giọng đọc chạy, gà con "nói": nhún, bong bóng chỉ có hình loa, **không có chữ** (manifest giữ cách đọc như "bờ", không phải chữ viết; lời dẫn, bài đọc dài cũng không hợp bong bóng). Móc vào bộ phát tiếng, không phải sửa từng loại bước.
   - Mũi tên chỉ vào thẻ đang đọc: không làm ở đợt 1 (cần mỗi loại bước báo thẻ đang đọc); để sau, thêm dần cho bước từ khoá, tranh.
   - Đúng hay sai vẫn giữ phản ứng hiện có (Cheer, Ponder).
   - Lý do: N1, N4.
3. **Nhắc khi bé ngồi im.** Bộ đếm theo bước, tính từ lần chạm cuối hoặc từ lúc giọng đọc dừng. Hai loại bước (Root 17/11):
   - **Bước bấm chọn và mọi lượt Phần 2** (bước cần chạm, chọn, kéo vào nội dung mới xong):
     - sau **12 giây**: gà con nhún và đọc lại lời dẫn của bước;
     - sau **24 giây**: bàn tay gợi ý. Phần 1 chỉ vào nội dung cần chạm (hoặc nút Tiếp nếu bước đã xong); Phần 2 chỉ nút Nghe lại, **không** chỉ đáp án, để không làm hộ bé.
   - **Bước bé tự đọc** (câu, đọc cả bài, đọc thêm, học thuộc lòng, bài đọc dài lớp 2; nói chung là bước chỉ đọc rồi bấm Tiếp): **không** đọc lại lời dẫn, để không cắt ngang lúc bé đang đọc; chỉ hiện bàn tay chỉ nút Tiếp (hoặc dấu tích) sau **30 giây**.
   - Mọi ngưỡng là hằng số ở một chỗ, có test. Bước tự khai báo loại của mình (mặc định: bước tự đọc nếu không cần chạm nội dung).
   - Mỗi bước nhắc tối đa 2 lần, rồi thôi.
   - Bất kỳ lần chạm nào cũng xoá nhắc. Không nhắc khi giọng đọc đang chạy.
   - Lý do: N4.
4. **Nội dung to hơn.** Nâng mức phóng to tối đa của khung bước học (FitBox) khi còn chỗ, để tranh và chữ chiếm phần lớn khung. Rà từng loại bước bằng ảnh chụp, loại nào không đẹp thì giữ mức cũ. Lý do: N1, chữ và tranh luôn nổi nhất.
5. **Nút của bé to hơn trên điện thoại.**
   - "Điện thoại" là khung rộng có tỉ lệ ≥ 1,9 (20:9, 19,5:9). Máy tính bảng 16:10 và 4:3 giữ như cũ (đã khoảng 2 cm).
   - Nút Tiếp, Nghe lại hiện to 180–220 (theo chỗ trong dải bên), vùng nhận chạm rộng hơn hình nút nhưng **chừa ít nhất 48 đơn vị tới mép dưới và mép bên** (bé hay tì cổ tay lên mép máy, Sesame; Root 17/11), không chồng vùng chạm nút khác, không vào khung bước học. Quy tắc 48 áp dụng cả nút "Học tiếp" ở con đường bài học.
   - Thẻ đáp án nằm trong khung bước học đã phóng (khoảng ×1,4 trên điện thoại, thẻ 220×180 thành khoảng 310×250), nên đã đủ; chỉ thêm test đo kích thước sau phóng ≥ 220.
   - Lý do: N2.
6. **Tiếng động nhỏ lại khi có giọng đọc.** Âm lượng tiếng động 0,45 hạ xuống 0,2 khi giọng đọc đang chạy. Giọng đọc không bao giờ bị át (ràng buộc của root).

### 4.2 Danh sách bài thành con đường (ảnh mẫu `m2_con_duong.png`)

1. **Đường lượn ngang theo từng quyển.**
   - Mỗi bài là một trạm tròn 200 đơn vị: chữ của bài to, "Bài n" nhỏ.
   - Bài ôn tập dùng ngôi sao `img_chung_sao`.
   - Bài đã học có hoa theo số sao đã được. Bài khoá màu nhạt có ổ khoá nhỏ.
   - **Gà con đứng ở bài đang học**, bài này to hơn và có quầng cam.
   - Lý do: N3, N7, N10.
2. **Biển chặng** cắm ở đầu mỗi nhóm:
   - lớp 1 theo phần ("Chữ cái và âm", "Vần");
   - lớp 2 theo tuần và chủ điểm.
   Thay cho tiêu đề nhóm của lưới hiện nay.
3. **Nút "Học tiếp" to** ở góc phải dưới: vào thẳng bài đang học bằng một lần chạm. Nút Ôn lại giữ ở góc trái dưới.
4. **Cuộn ngang và tự cuộn tới bài đang học**, thêm **hai nút mũi tên to (≥ 160) ở hai bên để nhảy một chặng** vì trẻ nhỏ khó cuộn, kéo (NN/g; Root 17/11). Khi mở màn, gà con và mũi tên nhẹ gợi ý hướng vuốt (một lần). Quyển 133 bài vẫn một đường, có biển chặng để định hướng.
5. **Trạm của lớp 2** (tên bài dài, Root 17/11): trong hình tròn là nhãn ngắn ("Bài 10", hoặc loại bài "Chính tả", "Từ ngữ", "Ngữ pháp", "Tập làm văn") kèm biểu tượng nhỏ theo loại bài; dưới hình tròn là tên bài chữ nhỏ, tối đa 2 dòng, cắt bằng "…". Lớp 1 giữ chữ của bài trong hình tròn. Test LayoutProbe với quyển 133 mục và quyển 130 mục.
6. **Nền:** cỏ, cây nét mực nhạt 35%, không chạm được (N1). Thanh trên giữ nguyên: Tủ sách, tên quyển, bánh răng, Sổ, Phụ huynh.
7. **Tủ sách:** gà con đứng cạnh quyển đang học thay vì đứng ở góc.

### 4.3 Xong bài và Sổ bé ngoan (ảnh mẫu `m4_xong_bai.png`)

1. **Tem bài học.**
   - Nửa dưới trang trái của Sổ dán tem là tranh từ khoá của bài, kèm chữ: tranh đầu tiên của bước `keyword`/`picture` trong phần 1.
   - Tem có viền giấy trắng, nghiêng nhẹ, có băng dính giấy.
   - Chọn tranh theo thứ tự: tranh của bước `keyword`/`picture`; nếu không có thì tranh đầu tiên ở bất kỳ bước phần 1 nào; rồi tranh đầu tiên ở phần 2. Lớp 2 nhiều bài không có bước từ khoá (khoảng 150/263), nên bước này cần.
   - Bài không có tranh nào: tem là tên bài viết to, tự co, tối đa 2 dòng, cắt bằng "…".
   - Lật Sổ bé ngoan thấy lại tem từng bài.
   - Trang phải hé lộ ô tem của bài sau, để mờ.
   - Lý do: N1, N6, N7. Thưởng gắn với nội dung bài, gợi lại bài đã học.
2. **Khen theo cách bé đã làm.** Có 4 câu khen mới, chọn theo những gì bé đã làm trong bài:

   | Bé đã làm gì trong bài | Câu khen | Mã tiếng |
   |---|---|---|
   | Nhầm rồi tự làm đúng | "Bé tự sửa được rồi, giỏi quá!" | `khen_tu_sua` |
   | Bấm nghe lại | "Bé chịu khó nghe lại, tốt lắm!" | `khen_nghe_lai` |
   | Làm đúng hết ngay từ đầu | "Bé nghe kĩ, làm đúng hết rồi!" | `khen_nghe_ki` |
   | Mặc định | "Bé học chăm quá!" | `khen_cham` |

   Cách chọn (ghi trong lúc học bài, chỉ trong bộ nhớ):
   - "Tự sửa": có ít nhất một lượt phần 2 bé nhầm đúng một lần rồi làm đúng **trước khi** gợi ý hiện (gợi ý hiện từ lần nhầm thứ hai). Lượt có gợi ý thì không tính tự sửa.
   - "Nghe lại": bé chạm nút Nghe lại ở phần 1 hoặc phần 2 ít nhất một lần.
   - "Nghe kĩ": không nhầm lượt nào. (Không khen "đọc to, rõ" vì app không có micro, không biết bé đọc thế nào; Root 17/11.)
   - Nhiều điều đúng thì lấy theo thứ tự trên: tự sửa, nghe lại, nghe kĩ; còn lại "chăm".
   Câu khen hiện cả bong bóng chữ lẫn tiếng. Không có câu khen "thông minh". Lý do: N6.

### 4.4 Chào bé (ảnh mẫu `m3_chao_be.png`)

1. **Gà con chào bằng tiếng.**
   - Gà con to (380 đơn vị) đứng bên trái.
   - Vào màn chọn bé thì đọc `hd_chao_be`: "Chào bé! Bé nào học hôm nay nào?".
   - Chọn bé xong thì đọc `hd_cung_hoc`: "Mình cùng học nhé!".
   - Không đọc tên bé (tên do phụ huynh gõ, không có tiếng sẵn).
   - Lý do: N4.
2. **Thẻ bé to hơn.**
   - Thẻ 420×500, ảnh đại diện 300.
   - Bé vừa học gần nhất đứng đầu và có quầng cam.
   - Cảnh sân trường nét mực rất nhạt phía sau: tranh mới `img_ui_canh_chao` vẽ bằng ChatGPT, không chạm được.
   - Lý do: N2, N7.

### 4.5 Nghỉ mắt (ảnh mẫu `m5_nghi_mat.png`)

Hiện **sau màn Xong bài** khi bé đã học đủ số bài phụ huynh đặt trong một lần học. Một lần học tính từ lúc chọn bé; mở lại app hoặc rời app quá 30 phút thì tính lần mới. Tính mọi bài học xong qua màn học, kể cả học lại bài cũ; không tính Ôn lại.

1. **Gà con nghỉ mắt.** Tranh mới `img_ui_nghi_mat` vẽ bằng ChatGPT: gà con duỗi cánh bên cửa sổ. Tiếng `hd_nghi_mat`: "Bé học giỏi lắm! Mình nghỉ mắt chút nhé."
2. **Hôm nay bé học mấy bài**, kèm hoa của từng bài.
3. **Một việc làm cùng bố mẹ ngoài màn hình**, gắn với bài vừa học (cùng nguồn với 4.6 mục 3). Dòng này cho bố mẹ đọc, **không có loa** (câu sinh theo bài nên không có tiếng sẵn).
4. **Nút "Tạm biệt" to** về màn chọn bé.
   - Dòng chữ nhỏ "Phụ huynh: học thêm" mở khoá phép tính; mở được thì bắt đầu lần học mới và đi tiếp như nút Tiếp của màn Xong bài (bài sau, hoặc Tủ sách nếu hết quyển).
   - Không đếm ngược, không khoá cứng (N9).
   - Mặc định **3 bài**; phụ huynh đổi hoặc tắt ở mục Thời lượng (Root 17/11).

### 4.6 Phụ huynh (ảnh mẫu `m6_phu_huynh.png`)

Sau khoá phép tính, chọn bé rồi xem từng mục. Cột trái có các mục: Tuần này, Chơi cùng con, Thời lượng, Chú ý và Phụ lục. Dòng tiến độ theo quyển và nút "Mở mọi bài" (đã có) chuyển vào mục Tuần này.

1. **Tuần này:**
   - số bài và số phút bé học, cột theo từng ngày (7 ngày gần nhất);
   - các dòng tiến độ theo quyển.
   Số phút chỉ tính lúc ở màn học, bỏ quãng ngồi im quá 60 giây.
2. **Chữ hay nhầm, chạm để nghe:** dùng tiếng của đáp án trong lượt bé nhầm. Lượt không có tiếng thì không có loa.
3. **Chơi cùng con hôm nay:** 2–3 gợi ý sinh từ bài bé vừa học, theo mẫu câu trong `UiText`:
   - bài âm, vần: "Tìm trong nhà đồ vật có tiếng chứa …";
   - từ khoá: "Con đọc '…', bố mẹ làm động tác";
   - viết: "Viết chữ … lên khay muối, đố nhau";
   - lớp 2: "Con đọc lại bài … cho bố mẹ nghe, rồi hỏi con một câu".
   Lý do: N5, N8.
4. **Thời lượng:** "Mỗi lần học: Không nhắc / 2 / 3 / 5 bài rồi gà con rủ nghỉ mắt". Có ghi chú "Nghỉ sau khi xong bài, không cắt ngang bài đang học". Lý do: N9.

## 5. Chia đợt

Mỗi đợt:
- viết test trước;
- chụp `phone_20x9`, `ipad_43`, `tab_16x10`, `tab_portrait`;
- LayoutProbe và kiểm chồng lấn bằng `WorldRect` khi có chữ cạnh nút;
- commit;
- gửi root ảnh chụp và kết quả test.

| Đợt | Nội dung | Cần ảnh, tiếng mới | Test chính |
|---|---|---|---|
| **1** | Màn học: con đường hạt (4.1.1); gà con bạn học (4.1.2); nhắc khi ngồi im + bàn tay (4.1.3); nút to trên điện thoại (4.1.5); tiếng động nhỏ lại (4.1.6) | Bàn tay `img_ui_tay_chi`: vẽ tạm trước, ChatGPT sau | ProgressPath (số hạt, chế độ đường dài, hạt đang học, nằm trong dải trên, không có gà con trên đường); IdleNudge (bước bấm chọn và Phần 2: 12 s, 24 s; bước tự đọc: chỉ bàn tay sau 30 s; tối đa 2 lần, chạm thì xoá, phần 2 không chỉ đáp án; dùng thời gian giả); khung bước học không nhỏ hơn trước ở mọi khung; vùng chạm Tiếp/Nghe lại ở khung ≥ 1,9 và thẻ đáp án sau phóng ≥ 220, không chồng nhau, chừa ≥ 48 tới mép; âm lượng tiếng động khi có giọng đọc; LayoutProbe mọi khung; smoke một bài lớp 1 và một bài lớp 2 |
| **2** | Con đường bài học (4.2) + nút Học tiếp + nút lật chặng + trạm lớp 2 + gà con ở Tủ sách | Không (dùng sao, hoa, khoá có sẵn) | Thứ tự trạm, trạng thái mở/khoá giống luật cũ (`BookShelf`), Học tiếp mở đúng bài, tự cuộn tới bài đang học, biển chặng theo phần/tuần, nút lật nhảy đúng một chặng, trạm lớp 2 có nhãn ngắn và tên dưới tối đa 2 dòng, quyển 133 và 130 mục vừa khung (LayoutProbe) và cuộn được, nút chừa ≥ 48 tới mép |
| **3** | Tem bài học + khen theo cách làm (4.3) | 4 mã tiếng `khen_*` (edge-tts như các mã khác) | Chọn tem đúng tranh từ khoá; bài không tranh thì tem chữ; chọn câu khen theo lượt nhầm hoặc nghe lại; Sổ bé ngoan có tem; tiến độ cũ vẫn mở được |
| **4** | Chào bé (4.4) | `img_ui_canh_chao` (ChatGPT); `hd_chao_be`, `hd_cung_hoc` | Tiếng chào phát một lần mỗi lần vào màn; thẻ to vừa 7 bé; cảnh nền không nhận chạm |
| **5** | Phụ huynh (4.6) + Nghỉ mắt (4.5) + ghi thời gian học | `img_ui_nghi_mat` (ChatGPT); `hd_nghi_mat` | Ghi ngày, số bài, số giây (bỏ quãng ngồi im); giữ 14 ngày; nghỉ mắt chỉ sau màn Xong bài, đúng số bài, mặc định 3 bài, file cũ lấy 3; học thêm qua khoá phép tính; gợi ý sinh đúng theo loại bài; chữ hay nhầm có loa khi có tiếng; file tiến độ cũ đọc được |

Thứ tự 1 → 5:
- **Đợt 1** chạm vào mọi lần học và không cần ảnh mới.
- **Đợt 2** đổi màn bé thấy nhiều thứ hai.
- **Đợt 3 và 4** cần tiếng và tranh mới.
- **Đợt 5** cần thêm dữ liệu.
Mỗi đợt dùng được ngay khi xong, không chờ đợt sau.

## 6. Ràng buộc và điều không làm

- Giữ bản sắc tranh SGK 1990: nét mực, màu phẳng, giấy ngà. Chữ và tranh bài học luôn nổi nhất. Cảnh nền nhạt và không chạm được.
- Không đổi nội dung bài, thứ tự bước, cách đánh vần. Không mất tiến độ cũ. Không quảng cáo, không mua hàng.
- Không phạt khi sai: giữ cách hiện có (rung, gợi ý dần, thử lại không giới hạn).
- Không điểm số, không bảng xếp hạng, không chuỗi ngày, không đếm ngược.
- Hiệu ứng không bắt bé chờ: chạy song song, chạm là bỏ qua như hiện nay. Tiếng động không át giọng đọc.
- Không thêm đồ trang trí chạm được, không thêm trò phụ (N1, N5).
- Vừa mọi khung đang chụp. Vùng chạm ≥ 160 ở mọi khung, ≥ 220 cho nút của bé ở khung rộng. LayoutProbe.
- Chữ trong `UiText`. Ảnh, tiếng có mã riêng, thay file cùng mã là ghi đè.
- Test chỉ cho phần đổi hoặc bị ảnh hưởng. Full suite khi đụng code dùng chung (đợt 1 đụng `LessonScreen`, `ProgressDots`, `Mascot`, nên chạy các test màn học). Test phải im lặng.

## 7. Dữ liệu tiến độ (đợt 5)

Thêm vào `Profile`; file cũ thiếu trường thì lấy mặc định:
- `session_lessons`: số nguyên, 0 = không nhắc; mặc định 3. File cũ không có trường thì lấy 3 (cần phân biệt "thiếu" với "0": dùng -1 hoặc cờ khi đọc).
- `days`: danh sách `{date: "yyyy-MM-dd", lessons, seconds}`, giữ 14 ngày gần nhất.
- `last_lesson_id`: bài học xong gần nhất (nguồn cho "Chơi cùng con").

Đợt 4 thêm `last_played` (ticks) vào `Profile` để xếp bé học gần nhất lên đầu; file cũ thiếu thì giữ thứ tự cũ.

Không đổi `schema` nếu chỉ thêm trường. Nếu bộ đọc JSON cần thì tăng `schema` kèm chuyển đổi, có test đọc file cũ.

## 8. Quyết định của mình (chủ dự án xem lại)

1. Nhắc ngồi im: bước bấm chọn và Phần 2 là 12 s và 24 s; bước tự đọc chỉ có bàn tay sau 30 s; tối đa 2 lần mỗi bước. Phần 2 chỉ chỉ nút Nghe lại, không chỉ đáp án. (Root 17/11)
2. Nghỉ mắt mặc định **3 bài**, phụ huynh đổi hoặc tắt. (Root 17/11)
3. Nút của bé to hơn chỉ ở khung rộng (điện thoại). Máy tính bảng đã đủ 2 cm nên giữ. Vùng chạm chừa 48 tới mép. (Root 17/11)
4. Không đọc tên bé trong lời chào, vì tên tự gõ không có tiếng sẵn.
5. Danh sách bài cuộn ngang một đường dài thay vì chia trang theo chặng.
6. Tem là tranh từ khoá của bài (thứ tự dự phòng ở 4.3), không cho bé chọn tem, để giữ bé tập trung.
7. Bong bóng của gà con chỉ có hình loa, không có chữ; mũi tên chỉ thẻ đang đọc để sau đợt 1. Màn học chỉ có một gà con (ở dải bên). (Root 17/11)
8. Thêm thứ vào màn học không được thu nhỏ khung bước học; nút to hơn chỉ trong dải bên.
9. Gợi ý "Chơi cùng con" không có tiếng (phụ huynh đọc), cả ở Phụ huynh lẫn Nghỉ mắt.

## 9. Việc ngoài phạm vi, ghi lại

- Tên app vẫn chưa chốt (`UiText.AppTitle`).
- Tranh `img_ui_tay_chi`, `img_ui_canh_chao`, `img_ui_nghi_mat` cần vẽ bằng ChatGPT (Kiet_1). Bàn tay vẽ tạm trước để đợt 1 không phải chờ.
- 7 mã tiếng mới: `hd_chao_be`, `hd_cung_hoc`, `hd_nghi_mat`, `khen_tu_sua`, `khen_nghe_lai`, `khen_nghe_ki`, `khen_cham`. Gom danh sách gửi root; root xếp lượt tạo giọng, nhận dạng và soát.
- Tranh ChatGPT: báo root trước khi mở trình duyệt (Edge dùng chung với Flow và [L2T2]); root xếp lượt.
