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
