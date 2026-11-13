# Tiếp tục tranh động lớp 1 (ghi chú chuyển máy, 10/11/2026)

Session tranh động lớp 1 dừng ngày 10/11 vì chủ dự án chuyển sang máy mới. Ghi chú này gom những gì trước đây chỉ nằm ngoài repo (ghi chú side-session, bộ nhớ của session) để session sau làm tiếp.

Cách làm chi tiết vẫn ở [content/style/tranh_dong_huong_dan.md](../../../content/style/tranh_dong_huong_dan.md). Kịch bản từng tranh ở [content/style/tranh_dong_kich_ban.json](../../../content/style/tranh_dong_kich_ban.json).

## 1. Tình trạng clip lớp 1 (343 clip)

Số liệu đọc từ `content/manifests/video_manifest.json` ở working copy ngày 10/11. Working copy có các lượt duyệt của chủ dự án chưa commit; chủ dự án tự commit phần này.

| Sách | Clip | Đạt | Chờ duyệt | Không đạt |
|---|---|---|---|---|
| Tiếng Việt 1 tập 1 (`tv1_t1_1990`) | 190 | 54 | 136 | 0 |
| Tiếng Việt 1 tập 2 (`tv1_t2_1996`) | 153 | 0 | 153 | 0 |

- **Tập 1:** đủ 190/190 tranh có clip.
- **Tập 2:** mọi tranh đều có clip, trừ hai tranh cố ý không làm:
  - `img_b97_banr_ddoof_vieetj_nam`: bản đồ tạm cắt từ scan;
  - `img_chung_cau_hoi`: kí hiệu câu hỏi.
- **Kịch bản:** đủ cho cả 343 clip trong `tranh_dong_kich_ban.json`, đã commit. Kịch bản cuối là 5a12fdb.
- **Lớp 2** (`tv2_t1_2001`, 56 clip): do session khác làm, không thuộc ghi chú này.

### Các clip đã làm lại

Đợt 05/11 làm lại 2 clip tập 1:

| Tranh | Chủ dự án chê | Đã sửa thành |
|---|---|---|
| `img_b05_dee` (con dê) | chưa có tiếng dê kêu | tiếng dê kêu thật, không giọng người |
| `img_b06_coj` (cây cọ) | lớn sai cách | lá quạt mọc thành bụi sát đất trước, rồi thân nhô lên đẩy tán, tán luôn đầy |

Đợt 09/11 làm lại 12 clip tập 1 bị chấm "không đạt":

| Tranh | Chủ dự án chê | Đã sửa thành |
|---|---|---|
| `img_b08_quyeenr_vowr` (quyển vở) | chưa hợp lý | vở gấp tự mở ra |
| `img_b10_ddi_ddof` (đi đò) | chuyển động chưa hay | đẩy sào, đò rẽ nước, cá nhảy |
| `img_b10_oo_too` (ô tô) | em bé không được lái xe | xe đỗ yên, không ai lái; đèn nháy, hai bạn vẫy tay |
| `img_b12_nuj_hoa` (nụ hoa) | nở rồi lại thu về nụ | chỉ đung đưa, có ong bay quanh, nụ không nở |
| `img_b12_quar_mow` (quả mơ) | hoa mọc trên lá | hoa trên cành, kết quả, quả chín rụng xuống lá |
| `img_b13_ddu_ddur` (đu đủ) | chưa tốt | quả xanh nằm yên, chín dần |
| `img_b13_cuwr_taj` (cử tạ) | tranh vẽ lại thành vận động viên người lớn | đặt tạ ngang vai, đẩy lên quá đầu rồi giữ |
| `img_b15_cais_loj` (cái lọ) | chưa hay | lọ trơn được cọ vẽ hoa văn lên |
| `img_b15_xe_lu` (xe lu) | chưa hay | trục lu nghiền lớp đá sỏi thành mặt đường |
| `img_b18_quar_var` (quả vả) | chưa hay | quả xanh lớn dần, ửng cam |
| `img_b20_ker_vowr` (kẻ vở) | chưa thấy bé dùng thước kẻ | tay giữ thước, tay kéo bút chì dọc mép thước |
| `img_b20_quar_khees` (quả khế) | chưa hay | chim lớn sà xuống mổ khế (gợi truyện Ăn khế trả vàng) |

Tình trạng duyệt của 14 clip này:
- Ngày 10/11 cả 14 clip đều đang **"đạt"** ở working copy, nghĩa là chủ dự án đã duyệt lại sau khi làm lại.
- Ghi chú của từng dòng có dạng "Đã tạo lại <ngày> (…). Lần trước: <lời chê cũ>".

## 2. Gói clip: cần đóng gói lại trước khi dùng ở máy mới

`content/clips/` nằm ngoài git và chỉ đi theo gói Drive.

**Gói `dist/TapDoc-clips-2026-11-09.zip` đã cũ.** Kiểm tra ngày 10/11 cho thấy:
- 12 clip làm lại đợt 09/11 trong gói vẫn là **bản cũ bị chê**: kích thước file khác với `content/clips`;
- gói thiếu 56 clip lớp 2.

Hai clip dê và cọ làm lại đợt 05/11 thì đã có trong gói.

Vì vậy cần đóng gói lại ở máy cũ trước khi chuyển:
1. Đóng Unity.
2. Chạy `cd tools && python run_unity_media.py pack`.
3. Commit `content/manifests/media_lock.json`.
4. Đưa hai file mới trong `dist/` lên Drive.

Nếu không đóng gói lại thì máy mới sẽ nhận clip cũ. Nếu máy cũ không còn dùng được, có thể tạo lại các clip này theo kịch bản trong `tranh_dong_kich_ban.json`.

`media_lock.json` chỉ khoá tranh và âm thanh, không khoá clip. Muốn biết gói clip có khớp không thì phải so file trong zip với `content/clips`.

## 3. Tài khoản Google Flow và credit

Quy tắc dùng tài khoản:
- Chỉ dùng các tài khoản đã đăng nhập sẵn trên trình duyệt của chủ dự án.
- Chủ dự án cho phép tự chuyển giữa các tài khoản đó.
- Không tự đăng nhập, không nhập mật khẩu, không tạo tài khoản.

Máy mới có thể đăng nhập theo thứ tự khác, nên số `/u/N` có thể đổi. Hãy nhận tài khoản theo tên hiển thị trong menu tài khoản.

Tình trạng từng tài khoản (ước lượng ngày 10/11):

| Đường dẫn ở máy cũ | Tài khoản | Credit còn lại | Ghi chú |
|---|---|---|---|
| `/u/6` | Arjunz Fullery | khoảng 310 | Gói 1.050 credit, đặt lại ngày 1/12. Dự án Flow "Tháng 11 05 - 14:12" (3f06579e…) chứa tranh và clip tập 2 cùng các clip làm lại. Đây là tài khoản chính hiện nay. |
| `/u/4` | Đặng Huỳnh Đức | khoảng 0 | Đặt lại ngày 29 hằng tháng, cộng 50 credit mỗi ngày. |
| `/u/1`, `/u/2`, `/u/3` | — | khoảng 50 mỗi ngày | `/u/3` là chatgpt.hytek. |
| `/u/0` | tài khoản công ty | — | Bắt buộc hình mờ: **không dùng**. |

- Mỗi clip Veo 3.1 Lite 720p dài 8 giây tốn 10 credit.
- Ảnh khung đầu tạo bằng Nano Banana Pro tốn 0 credit.
- Hộp thoại "Quyền sử dụng hình ảnh này" cần chủ dự án đồng ý cho từng tài khoản. Đã đồng ý cho `/u/1`, `/u/3` và `/u/4`.
- **Tải clip về:** ngày 05/11 chủ dự án dặn thẳng là tạo xong cứ tải về, không cần hỏi. Có lúc root lại dặn "hỏi trước khi tải"; nếu không chắc thì hỏi lại chủ dự án.

## 4. Cách làm

### Kịch bản

Mỗi tranh có một kịch bản riêng, sáng tạo theo đúng nội dung tranh. Có hai kiểu:
- **loop:** khung đầu và khung cuối đều là tranh gốc. Nhân vật làm một hành động có ý nghĩa rồi về đúng tư thế cũ.
- **build:** khung cuối là tranh gốc. Khung đầu là một ảnh "trạng thái trước", ví dụ cây còn nhỏ, quả còn xanh, vở còn gấp, lọ còn trơn hay tạ còn ngang vai. Ảnh này tạo bằng Nano Banana Pro, sửa từ chính tranh gốc.

### Điều chủ dự án muốn, rút từ các lượt chê

- Tăng trưởng chỉ đi **một chiều**: nụ không được nở rồi thu về.
- Tăng trưởng phải **đúng cách cây thật**: hoa mơ nở trên cành rồi mới kết quả, hoa không mọc trên lá; cây cọ ra bụi lá sát đất trước rồi thân mới lên.
- Trẻ em không lái xe.
- "Chưa hay" nghĩa là cần một hành động có ý nghĩa với tranh, không phải lắc nhẹ.
- Tiếng phải đúng tiếng thật, ví dụ dê kêu như dê.
- Veo hay làm quá tay: nụ nở bung rồi thu lại, vả chín thành tím, đu đủ dựng đứng, tạ hạ xuống rồi nâng lại. Cách chữa:
  - ghi rõ trạng thái cuối và những gì **không bao giờ** được xảy ra, kiểu "the bud never opens", "never turn purple", "stays completely still";
  - nếu vẫn hỏng thì đổi build sang loop.

### Quy trình trên Flow

1. **Chuẩn bị tranh:** đệm tranh vuông thành 1280×720. Lấy màu giấy ở điểm (8,8) làm nền, đặt tranh ở x = 280. Máy cũ dùng một script PowerShell System.Drawing; script nằm ở scratchpad nên sẽ mất, cần viết lại.
2. **Tải tranh lên Flow:**
   - Chặn `HTMLInputElement.prototype.click` và `showPicker` để bắt input file, gắn nhãn cho nó, rồi dùng công cụ file_upload, mỗi lần dưới 10 MB (khoảng 6 tranh).
   - Sau đó tìm từng mã trong ô "Tìm kiếm thành phần" để chắc đã lên đủ.
3. **Cài đặt:** Video, "Khung hình", 16:9, x1, Veo 3.1 - Lite.
   - Mỗi lần chuyển qua lại giữa chế độ ảnh và video, Flow có thể tự đổi về "Thành phần". Phải chọn lại "Khung hình" rồi mới gửi.
4. **Tạo khung đầu (chế độ Hình ảnh, Nano Banana Pro):**
   - Thêm tranh gốc làm tham chiếu và viết lệnh "Edit the attached illustration and change ONLY …".
   - Gửi bằng phím **Enter** trong ô lệnh. Click bằng JS hay bằng ref thì không ăn.
   - Flow tự đặt tên ảnh mới, ví dụ "Closed notebook on table". Tìm ảnh theo tên đó khi chọn khung Bắt đầu.
5. **Gửi video:** chọn khung Bắt đầu và Kết thúc trong bộ chọn, dán lời lệnh tiếng Anh kèm câu phong cách:
   > "Hand-drawn style throughout, exactly like the illustration: black ink outlines, hatched shading, flat colors, plain ivory paper background. Camera completely static: no zoom, no pan, no cut. No text, no letters."
6. **Tải clip về:**
   - Mở trang chi tiết của clip, đi qua từng clip bằng nút `arrow_right`, chọn tải → "720p".
   - Nhận ra clip nào bằng đoạn đầu lời lệnh hiện trên trang.
   - Tên file Flow trả về kết thúc bằng 8 kí tự hex. Dùng 8 kí tự này để chép đúng file từ thư mục Downloads sang `content/clips/<mã tranh>.mp4`.
7. **Kiểm tra clip:**
   - Phát clip thật và chụp khung theo thời gian thực. Tua (seek) rồi vẽ lên canvas thì trả về khung cũ, không tin được.
   - Xem đủ: có chuyển động, không quá tay, khung cuối khớp tranh.
   - Không nghe được tiếng, nên phần âm thanh để chủ dự án nghe.
8. **Ghi kết quả:**
   - Clip mới: thêm dòng vào `video_manifest.json` với `status: cho_duyet`, xếp theo `id`.
   - Clip làm lại: đưa dòng về `cho_duyet` và ghi chú "Đã tạo lại <ngày> (…). Lần trước: <lời chê cũ>".
   - **Chỉ commit dòng mới và kịch bản.** Không commit các lượt duyệt của chủ dự án đang nằm ở working copy. Cách commit: dựng nội dung file từ HEAD cộng các dòng mới, rồi chạy `git hash-object -w` và `git update-index --cacheinfo`.

### Lỗi đã gặp

- **Flow báo "Không thành công: hoạt động bất thường"** hai lần khi gửi liên tiếp nhiều ảnh khung đầu (09/11). Thử lại chậm từng cái thì được. Nếu còn lặp lại thì dừng và báo chủ dự án, không tìm cách lách.
- **Flow báo "Không tạo được âm thanh" hoặc "Đã hết thời gian tạo":** Flow hoàn credit, gửi lại là được.
- **Chụp màn hình Chrome treo** (06/11 và 09/11): làm qua JavaScript và find/ref, còn xem ảnh thì tải bản 1K về máy để mở.
- **Lệnh dừng server bằng bộ lọc CommandLine `*http.server 87xx*`** dừng luôn chính lệnh bash đang chạy nó, trả về mã 255. Phải chạy lệnh dừng riêng.

## 5. Việc còn lại

- Đóng gói clip lại trước khi chuyển máy (mục 2). Việc này do root hoặc chủ dự án quyết.
- Chủ dự án duyệt 136 clip tập 1 và 153 clip tập 2 đang chờ duyệt. Clip nào bị chê thì làm lại theo mục 4.
- Chưa có clip nào được đưa vào app Unity. Trước khi làm phần đó cần viết tài liệu thiết kế tranh động.

## 6. Đợt làm lại 11/11: 27 clip tập 1 bị chê (bài 21–80)

Ngày 11/11 chủ dự án chấm 76 clip bài 21–80: 49 đạt, 27 không đạt. Bốn lỗi lặp lại đã ghi vào mục 1 của `content/style/tranh_dong_huong_dan.md`: không tua ngược ở cuối clip, đi hoặc bay phải dời chỗ thật, con vật có tiếng kêu vui, phát triển đúng thực tế.

Cách sửa chính: clip có hành động đổi từ `loop` sang `build`. Khung đầu là lúc trước đó (bé còn đứng xa, đàn sếu còn ở bên trái, sen còn là nụ, lạc còn trong đất), clip diễn tiếp tới tranh gốc nên không có đoạn chạy ngược.

**Đã xong 15 clip**, đều đã xem khung hình và dạng sóng tiếng, dòng danh mục đã về `cho_duyet`:
- commit 17f2366, trên `/u/1`: `b28_ngaf_voi`, `b33_chos_xuf`, `b61_con_traau`, `b80_con_lownj`, `b80_con_meof`;
- commit 15c77c9, trên `/u/6`: `b23_quar_xoaif`, `b26_gaf_giof`, `b31_con_thor`, `b33_ddi_chowj`, `b46_con_nheenj`, `b49_ddons_baf`, `b49_xe_lam`, `b50_ddanf_gaf_con`, `b51_thoon_xoms`, `b52_que_kem`.

**Còn 12 clip** (dòng danh mục vẫn `khong_dat` với lời chê của chủ dự án; kịch bản mới đã có trong `tranh_dong_kich_ban.json`):

| Tranh | Kiểu | Khung đầu |
|---|---|---|
| `img_b61_quar_cau` | build | quả cau non bé xíu trong tai cau |
| `img_b62_ddanf_seeus` | build | đàn sếu lùi sang trái |
| `img_b63_cais_riuf` | build | thêm khúc gỗ dưới lưỡi rìu |
| `img_b65_booj_ddooij` | build | đoàn quân lùi xa trên đường núi |
| `img_b65_cur_lacj` | build | cây lạc có hoa, lớp đất cắt ngang, chưa có quả |
| `img_b67_hoa_cucs` | build | cây cúc con |
| `img_b68_coo_giaos_tawngj_quaf` | build | cô ôm hộp quà, bé buông tay |
| `img_b69_baix_cats` | build | thuyền buồm lùi sang trái |
| `img_b77_ddaamf_sen` | build | hai bông sen còn là nụ |
| `img_b77_nhipj_caauf` | build | chỉ có trụ cầu |
| `img_b78_xe_qua_caauf` | build | cả dòng xe lùi sang trái |
| `img_b50_coo_taams` | loop | không cần (tranh gốc ở cả hai đầu) |

Khung đầu và tranh đệm:
- 11 khung đầu đã tạo trên `/u/1` (dự án 84955ab1 "Tháng 10 30 - 17:03"), tên Flow dạng "Edit illustration…". Bản tải về ở scratchpad của session cũ, `r3/start/start_<mã>.jpg`; tranh đệm 16:9 ở `r3/pad/`. Nếu mất, tạo lại theo trường `start` trong kịch bản (Nano Banana Pro, 0 credit).
- Trên `/u/2` (dự án eb1940c8, giao diện tiếng Anh) đã có sẵn `start_` và `img_` của 5 tranh: cau, sếu, rìu, bộ đội, lạc.

**Lỗi 11/11:** trên `/u/2` cả 5 lần gửi đều báo "Failed — We noticed some unusual activity", không mất credit (còn 53). Root cho dừng cả ngày, không bấm Retry.

**Kế hoạch 12/11 (theo root):**
1. Thử 1 clip trên `/u/4` (còn 50 credit, cộng 50 mỗi ngày). Được thì gửi tiếp từng clip, **mỗi clip cách nhau ít nhất 1 phút**.
2. Nếu clip đầu trên `/u/4` lại bị "unusual activity" thì dừng hẳn và báo root.
3. `/u/2` và `/u/3` để sau cùng. Không dùng `/u/0`.

**Mẹo giao diện:** cửa sổ trình duyệt đổi cỡ sẽ làm lệch toạ độ. Chọn khung bằng mã trong trang thay cho toạ độ:
- bấm nút có chữ "Bắt đầu" hoặc "Start", chờ ô tìm kiếm hiện rồi focus nó;
- gõ tên tệp, bấm `[role=option]` khớp tên, rồi bấm "Thêm vào câu lệnh" hoặc "Add to prompt" nếu có;
- focus ô lệnh `[aria-label^="Bạn muốn tạo"]`, gõ lệnh, rồi bấm `[aria-label="Bắt đầu tạo"]` (tiếng Anh: "Start generation").

## 7. Hàng đợi tập 2: 32 clip làm lại (giao 11/11, làm sau 12 clip tập 1 ở mục 6)

Chủ dự án duyệt tập 2 ngày 11/11. Gồm 30 dòng `khong_dat` và 2 dòng có lời chê nhưng vẫn để `cho_duyet` (`b112_bes_loawts_choawts`, `b98_quar_saauf_rieeng`); root bảo coi 2 dòng này là không đạt.

Ba quy tắc mới ở mục 1 của hướng dẫn (5–7): tiếng nói và tiếng hát chỉ tiếng Việt, không có tiếng Anh; máy quay và vật không xoay, lia tùm lum, xe chạy đúng đường; người không biến thành con vật.

Kịch bản mới cho cả 32 clip đã có trong `tranh_dong_kich_ban.json` (24 build, 8 loop). Chưa tạo khung đầu nào. Khung đầu tạo bằng Nano Banana Pro theo trường `start`, 0 credit, ở cùng tài khoản sẽ làm video.

| Tranh | Lời chê | Kiểu | Cách sửa |
|---|---|---|---|
| `b81_quar_chanh` | chưa hay | build | hoa chanh trắng → quả lớn, một quả tách đôi |
| `b82_con_keenh_caauf_xinh` | đi mà đứng yên | build | hai bạn đi thật qua cầu |
| `b82_hocj_sinh` | đi mà đứng yên | build | cậu bé đi thật từ trái sang |
| `b83_capj_sachs` | chưa hay | build | cặp đổ, sách vương vãi → tự dọn gọn |
| `b83_lof_gachj` | chưa hay | build | thợ xếp gạch, chồng gạch cao dần |
| `b84_towf_lichj` | lật sai hướng | loop | tờ lịch lật ngược lên qua gáy phía trên rồi bị xé, bay đi |
| `b86_vaaps_phair_ddas` | chưa hay | build | bé chạy, vấp đá ngã, mẹ chạy tới đỡ |
| `b87_bups_mawng` | chưa hay | build | mưa xong, măng đội đất nhú lên |
| `b101_meof_dduoir_chuootj` | trẻ biến thành thú có đuôi | build | vòng tròn bắt đầu chơi; trẻ không có tai, đuôi |
| `b102_cais_chuoong` | chưa hay | loop | khúc gỗ treo dây thỉnh chuông "boong" |
| `b102_con_vitj` | chưa hay | build | vịt bơi thật tới, vỗ cánh kêu "cạp cạp" |
| `b105_caauf_truwowtj` | tua ngược ở cuối | build | bé ngồi trên đỉnh rồi trượt xuống |
| `b105_ruwowcs_ddenf` | đi mà đứng yên | build | đoàn rước đèn đi thật từ trái sang |
| `b106_con_buwowms` | chưa hay | build | nhộng nứt, bướm chui ra, cánh duỗi rộng |
| `b109_cais_loa` | không la làng, đọc "Loa loa loa" | loop | nói vào loa tiếng Việt "Loa! Loa! Loa!" |
| `b109_ddenf_trawng` | đèn cháy không đúng | build | ngọn lửa nhỏ sáng dần trong bóng đèn; mây trôi lộ trăng |
| `b110_mays_ddieenj_thoaij` | cần chuông reo, không quay | loop | chuông reo, ống nghe rung nhẹ, máy đứng yên |
| `b110_muix_khoan` | quay sai | loop | chỉ tay quay quay quanh trục khoan |
| `b110_quee_ngoaij` | đi mà đứng tại chỗ | build | má và bé đi thật dọc đường |
| `b111_con_nghes` | tiếng phải là nghé con | build | nghé bước tới, kêu giọng nghé non; cò bay ngang |
| `b112_choox_ngoawtj` | xe chạy tùm lum | build | xe khách chạy đúng đường, khuất sau vách núi |
| `b113_thu_hoachj_luas` | cần tiếng cô gái hát | loop | cô hát dịu dàng dân ca tiếng Việt |
| `b114_khai_hoang` | cần tiếng ca | loop | hai người vừa làm vừa hò tiếng Việt |
| `b116_hoa_hueej` | chưa hay | build | từ khóm lá, cành hoa vươn lên rồi nở |
| `b136_con_quaj` | thả đá thì nước phải dâng | build | nước thấp, quạ thả sỏi, nước dâng dần |
| `b137_cais_thuwowcs` | chưa hay | build | thanh gỗ trơn, vạch chia khắc dần |
| `b141_bacs_dduwa_thuw` | chưa hay | build | bác đạp xe tới, bấm chuông, đón cốc nước |
| `b142_cais_boongs` | có tiếng Anh | build | hai mẹ con đi thật trong mưa; không lời |
| `b145_baf_vaf_chaus` | có tiếng Anh | loop | bé đọc tiếng Việt "Ngày xửa ngày xưa..." |
| `b148_mej_ddax_veef` | chưa hay | build | bé quạt cho mẹ, bé gái mời nước, mẹ lau mồ hôi |
| `b112_bes_loawts_choawts` | chạy mà đứng tại chỗ | build | chú bé đi thật dọc đường đồi |
| `b98_quar_saauf_rieeng` | chưa hay | build | hoa sầu riêng → quả lớn, rụng, một quả nứt múi |

`b101_cais_cuoocs` chưa làm: root vẽ lại tranh trước rồi mới báo.

Credit: mỗi ngày khoảng 150 credit trên `/u/2`, `/u/3`, `/u/4`, tức khoảng 15 clip, nên tổng 44 clip (12 tập 1 + 32 tập 2) mất khoảng 3 ngày. Làm theo kế hoạch ở mục 6: mỗi clip cách nhau ít nhất 1 phút; gặp "unusual activity" là dừng và báo root.

## 8. Hàng đợi thêm: `b101_cais_cuoocs` (đứng sau 44 clip ở mục 6–7)

Root vẽ lại tranh cái cuốc ngày 11/11 (commit 60ef3a9): lưỡi sắt hình thang có khâu tra vào cán, vuông góc với cán, cắm xuống đất, bên cạnh có đất vụn và cỏ. Clip cũ làm từ tranh sai nên phải bỏ; dòng danh mục vẫn là `khong_dat` cho tới khi làm clip mới.

Kịch bản mới (build) đã có trong `tranh_dong_kich_ban.json`:
- khung đầu: cùng cái cuốc nhưng giơ lên cao, đất bên dưới phẳng, chưa có cục đất;
- clip: cuốc bổ xuống, lưỡi cắm vào đất, kéo về làm đất vỡ tơi;
- lưỡi luôn vuông góc với cán, không tua ngược.

Nhớ đệm lại tranh 16:9 từ bản mới trong `Resources/images`, đừng dùng bản cũ đã tải lên Flow.

## 9. Cập nhật tối 11/11

- Chủ dự án cho làm lại sau 1 giờ nghỉ. Trên `/u/4` (dự án bc8e3e5b "Tháng 11 02 - 09:37") đã làm 5 clip: `b61_quar_cau`, `b62_ddanf_seeus`, `b63_cais_riuf`, `b65_booj_ddooij`, `b65_cur_lacj`.
  - Gửi từng clip, chờ xong rồi đợi thêm 2–3 phút mới gửi clip sau; không gặp "unusual activity".
  - Cả 5 đã xem và đạt; commit 1a09bed. Tập 1 đợt này xong 20/27.
- **Còn lại:**
  - 7 clip tập 1: `b67_hoa_cucs`, `b68_coo_giaos_tawngj_quaf`, `b69_baix_cats`, `b77_ddaamf_sen`, `b77_nhipj_caauf`, `b78_xe_qua_caauf`, `b50_coo_taams`;
  - 32 clip tập 2 (mục 7);
  - cái cuốc (mục 8).
- **Credit tối 11/11:** `/u/2` 53, `/u/3` 50, `/u/4` 0 (cộng 50 mỗi ngày), `/u/1` và `/u/6` hết.
- **Chủ dự án chốt "để mai" (12/11).** Mai bắt đầu lại trên `/u/4`, cũng gửi chậm như trên. `/u/2` và `/u/3` để sau cùng.

## 10. Cập nhật 12/11

Nhịp làm theo chủ dự án: mỗi lần tạo (video hay ảnh khung đầu) cách nhau ít nhất 6 phút, khung đầu và video của cùng một clip cách nhau khoảng 3 phút, đổi tài khoản nghỉ 20 phút. Cả ngày không gặp "unusual activity", kể cả `/u/2` và `/u/3`.

**Đã nhận và commit (cho_duyet), xếp theo tài khoản:**
- `/u/6`: b67 hoa cúc, b69 bãi cát, b77 đầm sen, b77 nhịp cầu (commit 268e869; root đã xem, đạt).
- `/u/1`: b78 xe qua cầu, b50 cô Tấm (commit 124f0b6; root đã xem, đạt).
- `/u/3`: b84 tờ lịch, b83 cặp sách, b83 lò gạch (commit a98edb8; root đã xem, đạt).
- `/u/2`: b102 cái chuông, b101 mèo đuổi chuột, b102 đàn vịt (commit 302e6bc; chờ root xem). Ở clip chuông, khúc gỗ đi vào từ bên phải; cần xem có vướng quy tắc 9 không.

**Hỏng hoặc root trả lại, xếp làm lại** (kịch bản đã sửa):
- b68 cô giáo tặng quà: hỏng 2 lần, Veo vẽ thêm trẻ em ở hai bên rồi cho biến mất. Lần tới thử thêm câu "hai dải giấy hai bên luôn để trống"; nếu vẫn hỏng thì ghi chú cho chủ dự án.
- b81 quả chanh, b82 cầu kênh: root trả lại (commit e356984).
- b82 học sinh, b86 vấp đá: root trả lại (commit cbc8687).
- b87 búp măng: khóm tre mờ đi kiểu chuyển cảnh.
- b105 cầu trượt: bé xuống chân cầu rồi lại hiện trên đỉnh.

**Hàng đợi còn lại:**
1. Làm lại: b68, b81, b82_con_keenh, b82_hocj_sinh, b86, b87, b105_caauf.
2. Tập 2 chưa làm: b105_ruwowcs_ddenf, b106, b109 ×2, b110 ×3, b111, b112 ×2, b113, b114, b116, b136, b137, b141, b142, b145, b148, b98.
3. Cái cuốc b101_cais_cuoocs.
4. 16 clip mới root giao 12/11: 3 clip làm lại lần 2 (b26 gà gáy, b28 voi, b31 thỏ) và 13 clip mới chê (b42, b43, b57, b58, b69_mays_cayf, b73, b74, b91, b117, b163 ×2, b165, b166). Chưa viết kịch bản cho 16 clip này.

**Mẹo kỹ thuật 12/11:**
- Khung đầu tập 2 tạo trên chính tài khoản làm video. Khi chọn khung Bắt đầu, lấy mục mới nhất trong danh sách không bắt đầu bằng `img_` hay `start_`, rồi xem ảnh xem trước cho chắc.
- Tài khoản giao diện tiếng Anh: nút `Start`/`End`, `Add to prompt`, `Add ingredients to the prompt box`, `Start generation`, `Settings trigger`, chế độ `Frames`/`Image`.
- Ở giao diện tiếng Anh, phím Escape trong trang chi tiết sẽ thoát ra lưới. Muốn tải clip thì bấm vào ảnh nhỏ của clip trên dải phía trên (nhận theo tên), rồi Download → 720p.
- Sau khi gõ lệnh ảnh, phải đặt lại con trỏ vào ô lệnh rồi mới bấm Enter, nếu không đôi khi lệnh không được gửi.
- Gọi upd.py hai lần liền với hai tệp kịch bản khác nhau thì lần sau ghi đè phần stage của lần trước. upd.py nay nhận nhiều tệp kịch bản, cách nhau dấu phẩy.

**Chia tài khoản Flow (root chốt 12/11, áp dụng từ 13/11):**
- `/u/1` dành riêng cho [L2] tranh động.
- [L1] dùng theo thứ tự `/u/4`, `/u/6`, `/u/3`, rồi `/u/2` sau cùng. Không dùng `/u/0`.
- Chiều 12/11 [L2] có thể dùng phần credit còn lại, nên [L1] không mở Flow cho tới ngày 13/11.
- Sau đợt root trả lại 3 clip của 302e6bc (commit 7a83ad6), danh sách làm lại thêm b101 (mèo đuổi chuột, đổi lời lệnh bỏ chữ mèo/chuột), b102 vịt (loop) và b102 chuông (loop).
- Khi xem clip: lấy ít nhất 10 khung lớn và soi từng nhân vật (đuôi, tai, chồng hình, số lượng).
- **Root chốt lại (12/11 chiều), thay cho thứ tự ở trên:**
  - Chiều 12/11 [L2] dùng `/u/3` (sau 13:44); [L1] nghỉ.
  - Ngày 13/11 [L2] dùng `/u/1`; [L1] dùng `/u/6`, rồi `/u/3` (sau 13:44), cuối cùng `/u/2` nếu đã có credit lại.
  - `/u/4` không thấy được cộng lượt ngày. Sáng 13/11 xem lại; nếu có credit thì [L1] dùng.

**Chủ dự án duyệt 9 clip làm lại ngày 12/11** (kết quả nằm ở working copy, chưa commit; chủ dự án hoặc root sẽ commit):
- 7 đạt: b67 hoa cúc, b69 bãi cát, b77 đầm sen, b77 nhịp cầu, b78 xe qua cầu, b83 cặp sách, b84 tờ lịch.
- 2 không đạt, đã sửa kịch bản và xếp vào hàng làm lại:
  - b50 cô Tấm: chủ dự án muốn có tiếng đọc bài "bống bống bang bang". Kịch bản mới cho cô Tấm đọc tiếng Việt "Bống bống bang bang, lên ăn cơm vàng cơm bạc nhà ta".
  - b83 lò gạch: hành động xếp gạch chưa hay. Kịch bản mới: lúc đầu chưa có chồng gạch; thợ lấy gạch từ đống bên miệng lò, xếp hai chồng cao dần từng lớp.

## 11. Hàng đợi lớn ngày 13/11: 91 clip "đạt" bị root soát lại

Chủ dự án nhờ root soát lại 347 clip đã chấm đạt. Root tìm thấy 104 clip lỗi nặng, trong đó 91 clip lớp 1 thuộc [L1]: tập 1 có 43, tập 2 có 48. Danh sách lỗi theo từng giây ở `docs/superpowers/notes/2026-11-13-soat-lai-clip-dat.md`. Các dòng này đã về `khong_dat` (commit 2744d08); ghi chú mở đầu bằng "Root soát lại 13/11 (bản đã đạt)".

**Kịch bản đã viết xong:**
- tập 1: e52dddf;
- tập 2: c10a0ad (kể cả b98 sầu riêng, thay kịch bản cũ).

Mỗi lần commit chỉ stage các dòng của [L1] lấy từ HEAD, bằng script `scratchpad/r6/apply.py`.

Cách viết theo quy tắc 9–17 và QUY-TRINH §12 (f1b88d8):
- Cảnh không cần lớn lên hay lắp ráp thì dùng loop, chuyển động nhỏ trong tranh.
- Nhân vật đang ở giữa bước chạy hay bay thì cho chạy hoặc bay một vòng nhỏ rồi về đúng chỗ: b95 cò, b114 hoẵng, b92 khỉ.
- Build chỉ một việc: chín màu, lớn lên, đậy nắp, khép cửa, đặt sách hoặc gạch, mở ngăn.
- Khung đầu ghi số đo cụ thể, ví dụ thu nhỏ còn 75%, dời 1/10 hoặc 1/12 bề ngang.
- Dừng đúng khoảnh khắc trong tranh: b49 đón cam, b58 bỏ thư, b60 chim bay, b170 tung mũ.
- Ghi rõ số lượng: b02, b43, b44, b48, b55, b58 gà, b106 mướp.

**Thứ tự hàng đợi theo root:**
1. Các clip làm lại cũ: b68, b81, b82 ×2, b86, b87, b105 ×2, b101 ×2, b102 ×2, b50, b83 lò gạch, và các clip tập 2 ở mục 7 chưa làm.
2. 16 clip giao ngày 12/11 (mục 10).
3. 91 clip này, bắt đầu từ tập 1.

Tính đến 13/11, lớp 1 còn 137 dòng `khong_dat`. Với khoảng 20 clip mỗi ngày thì cần khoảng 7 ngày.

**Nhịp làm:** mỗi lần tạo cách nhau ít nhất 6 phút; đổi tài khoản nghỉ ít nhất 20 phút. [L1] dùng `/u/6`, `/u/3` (sau 13:44), `/u/2`, và `/u/4` nếu có credit. [L1] chỉ bắt đầu khi root báo, sau khi [L2] xong trên `/u/1`. Mỗi clip nhận xong đều báo root xem trước.
