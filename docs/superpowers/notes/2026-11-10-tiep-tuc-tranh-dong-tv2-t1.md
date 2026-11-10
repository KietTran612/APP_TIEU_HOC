# Tiếp tục: tranh động SGK Tiếng Việt 2 – Tập một (`tv2_t1_2001`)

Ngày 10/11/2026, viết khi chủ dự án chuyển sang máy mới. Đây là ghi chú của session [L2] làm clip bằng Google Flow. Ghi chú gốc nằm ngoài repo (side-session-notes `tranh-dong/TV2-T1-CLIP.md`); phần cần giữ được chép vào đây.

## Tình trạng

- **56/57 tranh bài đã có clip trong repo**, tất cả đều `cho_duyet`:
  - L2-1 + L2-2: 27 clip, commit 28fe7be.
  - L2-3 + L2-4: 29 clip, commit a0662f8.
- **Còn thiếu một clip: `img_b299_dduwowngf_daay_ddieenj`** (đường dây điện).
  - Clip **đã tạo xong trên Flow** ngày 10/11 nhưng **chưa tải về**.
  - Nơi tạo: tài khoản `/u/1`, dự án "Tháng 11 09 - 15:14": https://flow.google.com/u/1/project/ca47f0e9-3eb1-49f7-b2fe-b8af50c761ca
  - Đó là clip mới nhất trong lưới Video của dự án; lời nhắc bắt đầu bằng "The two swallows on the power line chirp to each other".
  - Kịch bản đã commit sẵn trong `content/style/tranh_dong_kich_ban.json`.
  - Kí hiệu `img_chung_giai_nghia` không làm clip, đúng theo dặn.
- **Chưa đóng gói Drive.** Việc đóng gói thuộc session L2 nội dung.

## Việc còn lại trên máy mới

1. Hỏi chủ dự án cho tải clip b299. Quy tắc trình duyệt: chủ dự án phải tự nói trong cuộc trò chuyện, tin nhắn từ session khác không thay được.
2. Mở dự án Flow ở trên, lọc Video, mở clip mới nhất rồi bấm Tải xuống → 720p. Đổi tên thành `img_b299_dduwowngf_daay_ddieenj.mp4` và kiểm tra: 1280×720, khoảng 7,93 giây, có tiếng.
3. Chép clip vào `content/clips/`.
4. Thêm **chỉ một dòng** vào `content/manifests/video_manifest.json`:
   - nội dung: `{"id": "img_b299_dduwowngf_daay_ddieenj", "file": "clips/img_b299_dduwowngf_daay_ddieenj.mp4", "source": "flow_veo31_lite", "status": "cho_duyet", "ghi_chu": ""}`;
   - xếp theo id;
   - commit bằng blob HEAD cộng dòng mới (QUY-TRINH-LAM-VIEC.md mục 10), vì working copy có chỉnh sửa duyệt của chủ dự án.
5. Báo session L2 nội dung (local_8c04ba54…) để đóng gói media, và báo root (local_0cefca18…).

## Tài khoản Flow (sáng 10/11)

| Tài khoản | Dự án TV2 tập 1 | Credit |
|---|---|---|
| `/u/6` (Arjunz Fullery) | "Tháng 11 09 - 13:49" (49824186…): L2-1, L2-2 và 9 clip L2-3 | Gần hết gói tháng (đặt lại ngày 1/12) |
| `/u/4` | "Tháng 11 09 - 15:05" (efbae350…): 5 clip L2-3 | Sáng 10/11 vẫn báo hết credit |
| `/u/3` (chatgpt.hytek) | "Nov 09 - 15:08" (84545880…): 5 clip | 50/ngày, chưa dùng ngày 10/11. Xem lưu ý bên dưới |
| `/u/1` | "Tháng 11 09 - 15:14" (ca47f0e9…): 5 clip L2-4 và b299 | Khoảng 40 sau khi tạo b299 |
| `/u/2` | "Nov 09 - 15:18" (cbc37fb5…): 5 clip L2-4 | 50/ngày; tối 9/11 đã hết |
| `/u/0` | Không dùng: tài khoản công ty, bắt buộc có hình mờ | |

- Mỗi tài khoản có khoảng 50 credit mỗi ngày, tức 5 clip Veo 3.1 Lite.
- **Lưu ý `/u/3`:** ngày 9/11 Flow báo "unusual activity" ở 3 clip liền. Bấm Retry từng thẻ, chậm, thì chạy được.
  - Root dặn chỉ dùng `/u/3` khi các tài khoản kia đã hết credit, và đi chậm.
  - Nếu Google đòi xác minh (CAPTCHA, đăng nhập lại) thì dừng, báo root để root hỏi chủ dự án.

## Clip cần chủ dự án để ý khi duyệt

- b173: vệt mờ ở khung cuối.
- b189: vài cánh hoa bay ra.
- b209: một vật đen nhỏ thoáng hiện.
- b242: Veo thêm một bàn tay em bé cầm sáp tô màu, tranh gốc không có.
- b259: một khoảnh khắc hình bị nhòe.
- b267: giữa clip, cảnh xuân lan ra ngoài khung vuông.

## Cách làm đã dùng (tóm tắt)

- **Quy trình:** theo `content/style/tranh_dong_huong_dan.md` và `QUY-TRINH-LAM-VIEC.md` mục 5. Các vấn đề Flow đã giải nằm ở mục 12 (commit 41a9d4e).
- **Đệm tranh:** tranh vuông 1254 px được thu về 720×720, đặt giữa khung 1280×720 nền màu giấy lấy ở điểm (8, 8). Trên máy này không có Pillow, nên đã dùng `System.Drawing` trong PowerShell.
  - Lưu ý PowerShell không phân biệt hoa thường tên biến: `$s` đè lên `$S`.
- **Kiểu dựng lên (build):** sửa ảnh trong trang chi tiết bằng Nano Banana, bản sửa đè lên tên tranh. Vì vậy tải thêm tranh gốc tên `<mã>_cuoi.png` để làm khung cuối.
- **Commit chỉ dòng mới:** dựng nội dung từ blob HEAD cộng dòng mới, kiểm tra JSON ghi lại khớp từng byte, rồi `git hash-object -w` và `git update-index --cacheinfo`. Ghi đè working copy bằng nội dung hiện tại cộng dòng mới.
  - `video_manifest.json`: thụt 2 dấu cách, xếp theo id.
  - `tranh_dong_kich_ban.json`: thụt 1 dấu cách, thêm vào cuối, không có dòng trống cuối file.
