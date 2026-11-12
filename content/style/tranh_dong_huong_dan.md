# Hướng dẫn làm tranh động (clip) cho tranh bài học

Tài liệu để nhớ cách làm clip cho tranh bài học, dùng lại cho các tranh và các tập sách sau. Kịch bản riêng của từng tranh nằm ở `tranh_dong_kich_ban.json` cùng thư mục.

## 1. Chủ dự án muốn gì

- **Clip phải sáng tạo, có ý tưởng riêng cho từng tranh.** Không làm kiểu "tranh rung nhẹ" chung chung, cũng không áp một khuôn cứng cho mọi tranh. Xem kỹ từng tranh rồi chọn chuyển động và âm thanh hay nhất, hợp lý nhất cho tranh đó.
- **Bốn hướng gợi ý.** Đây là gợi ý, không bắt buộc; một tranh không cần có đủ mọi hành động, chọn cái hợp nhất:
  - **Cây, hoa, quả, củ:** kiểu phát triển. Mầm nhú, cây vươn, ra hoa, kết quả, quả lớn và chín, kết thúc đúng bằng tranh gốc. Hoa có thể nở từ nụ; củ có thể lớn dưới đất rồi lộ ra.
  - **Đồ vật:** kiểu lắp ghép thành thành phẩm. Ví dụ ghế đẩu: bốn chân bật đứng dậy, mặt ghế bay vào gắn lên. Đồ đan (sọt, ghế mây) thì tự đan; đồ gấp (khăn) thì tự gấp; nhà, cầu thì dựng lên từng phần.
  - **Vật phát ra âm thanh:** cho vật đang hoạt động và phát tiếng của nó: đài phát nhạc (có nốt nhạc bay ra), xe nổ máy, chuông xe đạp kêu, sấm chớp.
  - **Con vật, người:** có hành động rõ (bay, chạy, nhảy, bơi, vỗ cánh, mổ thóc…); con vật có tiếng kêu đặc trưng (gà gáy, bò "ò", dê "be be", ếch "ộp ộp").
- **Bốn lỗi chủ dự án chê nhiều lần (đợt duyệt 11/11, áp dụng cho mọi lớp):**
  1. **Không tua ngược ở cuối clip.** Clip `loop` hay bị Veo diễn xong rồi chạy ngược lại về tư thế đầu (kiểu boomerang); chủ dự án không chấp nhận, kể cả khi clip cần lặp. Cách tránh:
     - hành động có hướng (đi, chạy, bay, trao quà, xe chạy) thì làm kiểu `build`: khung đầu là lúc trước đó, rồi diễn tiếp tới tranh gốc;
     - nếu vẫn dùng `loop` thì nhân vật về tư thế cũ bằng một động tác mới, tự nhiên (mèo kêu xong cúi xuống liếm chân tiếp), và lời lệnh ghi rõ `Time only moves forward: the motion never plays backward, never rewinds and never reverses.`
  2. **Đi hay bay thì phải dời chỗ thật**, không bước tại chỗ hay vỗ cánh đứng yên. Khung đầu đặt nhân vật lùi lại phía sau trên đường đi (hoặc lệch sang một bên), clip cho nhân vật đi hoặc bay tới đúng chỗ trong tranh.
  3. **Con vật nên có tiếng kêu vui, rõ:** gà trống gáy, chó sủa "gâu gâu", mèo "meo", lợn "ụt ịt", trâu "nghé ọ", voi rống. Lời lệnh tả cả động tác mở miệng kêu và ghi tiếng kêu là tiếng thật, to, rõ.
  4. **Quá trình phát triển phải đúng thực tế:** củ lạc lớn dưới đất (hoa lạc đâm tia xuống đất, quả lớn trong đất rồi mới lộ ra); hoa mọc từ cây (cây con lớn lên, ra nụ, nụ nở thành hoa), không mọc từ lá hay từ không trung; quả lớn từ hoa trên cành.
- **Hai quy tắc thêm sau đợt duyệt tập 2 (11/11):**
  5. **Tiếng nói, tiếng hát chỉ được là tiếng Việt, không bao giờ có tiếng Anh.** Veo hay tự chèn lời tiếng Anh. Lời lệnh phải ghi rõ một trong hai cách:
     - không lời: `No speech, no words, no English`;
     - có lời thì ghi đúng câu tiếng Việt, ví dụ `the boy calls out in Vietnamese "Loa loa loa!"`, hoặc `a young woman softly sings a gentle Vietnamese folk melody (Vietnamese lyrics, never English)`.
  6. **Máy quay không xoay, không lia; vật không quay tùm lum; xe chạy đúng theo đường.**
     - Ghi rõ vật chỉ chuyển động đúng kiểu thật của nó, ví dụ mũi khoan quay quanh trục của nó, ống nghe điện thoại nảy nhẹ trên giá, xe đi theo mặt đường và không bao giờ ra khỏi đường.
     - Câu phong cách đã có `Camera completely static`. Với vật dễ bị xoay, thêm `The object itself stays in place and does not spin or tumble`.
  7. **Người không biến thành con vật.** Trò chơi đóng vai (mèo đuổi chuột) vẫn là trẻ em bình thường, không có tai, đuôi hay lông thú. Ghi rõ `they stay ordinary children: no animal ears, no tails, no fur`.
  8. **Tiếng con vật phải là tiếng thật của đúng con đó** (đợt duyệt 12/11: gà trống kêu như quạ, voi kêu như kèn).
     - Lời lệnh gọi đúng tên tiếng và nói rõ không được thành tiếng gì, ví dụ `a real rooster crowing "cock-a-doodle-doo", never a crow's caw`, `a real elephant trumpeting from its trunk, an animal call, not a brass trumpet or horn instrument`.
     - Nếu Flow vẫn ra tiếng sai: làm lại clip chỉ có tiếng động nhẹ (gió, bước chân, lá xào xạc), không có tiếng kêu, và ghi vào `ghi_chu` để chủ dự án biết.
- **Không cần chủ dự án duyệt kịch bản trước.** Cứ làm clip. Chủ dự án xem thành phẩm trong công cụ duyệt (tab "Tranh động") và yêu cầu làm lại nếu cần.

## 2. Phong cách hình và tiếng

- **Hình:** giữ đúng nét tranh SGK 1990: nét mực đen, gạch bóng, màu phẳng, nền giấy ngà. Máy quay đứng yên, không zoom, không lia, không cắt cảnh. Không có chữ trên hình; trừ tranh chữ số như `img_b47_soos_chins`, khi đó bỏ câu cấm chữ (trường `no_text_rule: false`).
- **Tiếng:**
  - Tiếng tự nhiên hợp cảnh: tiếng kêu của con vật, nước, gió, máy, bước chân.
  - Không lời nói, không hát có lời.
  - Không nhạc nền; chỉ có nhạc khi chính vật trong tranh phát ra nhạc (đài, tốp ca ngân nga không lời).
  - Trẻ con cười hay reo thì ghi rõ "(no words)".

## 3. Hai kiểu clip

| Kiểu | Trường `mode` | Khung đầu | Khung cuối | Dùng cho |
|---|---|---|---|---|
| Diễn rồi về | `loop` | tranh gốc | tranh gốc | hành động tại chỗ: con vật kêu, vật phát tiếng, cảnh gió nước; hành động ở giữa rồi về dáng cũ bằng động tác mới, không tua ngược |
| Dựng lên thành tranh | `build` | ảnh "điểm bắt đầu" tạo bằng sửa ảnh | tranh gốc | cây quả (mọc lên), đồ vật (lắp ghép, đan, gấp), công trình (dựng lên), chữ số (tự vẽ); người, con vật, xe đi tới chỗ trong tranh (khung đầu lùi lại phía sau) |

- **Flow bắt buộc phải có khung đầu.** Nếu chỉ đặt khung cuối thì nút tạo bị khoá. Vì vậy kiểu `build` phải tạo trước ảnh "điểm bắt đầu".
- **Ảnh "điểm bắt đầu":**
  - Tạo bằng chế độ Hình ảnh của Flow (Nano Banana Pro, 16:9, không tốn credit), gắn tranh gốc đệm 16:9 làm tham chiếu.
  - Lời yêu cầu: `Edit the attached illustration into the STARTING frame of a … animation: keep exactly the same … but <trường start>. Same 16:9 framing, no text.`
  - Mỗi lần chỉ gửi một yêu cầu ảnh, bấm nút gửi bằng cú nhấp thật (gửi bằng mã đôi khi không đi).

## 4. Cách viết lời yêu cầu video

- **Câu mở và nội dung:**
  - `loop`: "…comes alive / The X does A, B, C …, then settles back into the exact original pose."
  - `build`: "… animation from the first frame to the last: … until it matches the final illustration exactly."
- **Hành động:** tả hành động cụ thể theo thứ tự (2–4 việc), có chi tiết nhỏ làm cảnh sống động (lá rơi, bong bóng, bụi, mây trôi).
- **Tiếng:** câu `Sound: …` ghi rõ tiếng chính và tiếng phụ.
- **Câu phong cách luôn thêm ở cuối:** `Hand-drawn style throughout, exactly like the illustration: black ink outlines, hatched shading, flat colors, plain ivory paper background. Camera completely static: no zoom, no pan, no cut. No text, no letters.` Bỏ "No text, no letters" khi `no_text_rule` là `false`.
- **Lời tả trong kịch bản** là tiếng Anh (Veo hiểu tốt hơn); trường `vi` là tóm tắt tiếng Việt để người đọc nắm ý.

## 5. Làm trên Google Flow

- **Thông số:** Veo 3.1 Lite, chế độ "Khung hình" (Frames), 16:9, x1, 720p, 8 giây, **10 credit mỗi clip**.
- **Chuẩn bị tranh:** tranh gốc vuông được đệm thành 1280×720 bằng màu giấy lấy ở góc tranh, đặt giữa khung. Khi đưa vào app thì cắt lại hình vuông ở giữa.
- **Kiểm tra trước khi gửi:** ô soạn phải đúng 2 ảnh và đúng mã tranh. Lỗi đã gặp: khung cuối của lần trước còn sót lại, làm clip đài ra-đi-ô thành "đài → búp sen", mất 10 credit.
- **Tài khoản** (chủ dự án cho phép tự chuyển giữa các tài khoản đã đăng nhập sẵn; không đăng nhập hay tạo tài khoản mới):
  - Tài khoản 1 (`/u/2`): đặt lại credit ngày 15 hằng tháng, tắt được hình mờ.
  - Tài khoản 2 (`/u/1`): đặt lại ngày 29 hằng tháng. Khu vực bắt buộc "hình mờ nhìn thấy", nhưng file 720p tải về đã kiểm tra không thấy hình mờ ở cả bốn góc.
  - Ngày 2/11 cả hai tài khoản trên đều có thêm khoảng 50 credit, tức 5 clip mỗi tài khoản.
  - `/u/3` (chatgpt.hytek): 50 credit, nạp lại mỗi ngày lúc 9:36.
  - `/u/4` (Đặng Huỳnh Đức): 1.050 credit, đặt lại ngày 29. Dự án "Tháng 11 02 - 09:37".
  - `/u/0` là tài khoản công ty, bắt buộc hình mờ: không dùng.
  - Mỗi tài khoản mới phải tải tranh đệm lên và tạo lại ảnh "điểm bắt đầu" (miễn phí). Lần đầu tải ảnh lên có hộp "Quyền sử dụng hình ảnh này"; hỏi chủ dự án trước khi bấm đồng ý.
  - Dự án mới có thể mở sẵn bảng "Tác nhân" và nút Tác nhân đang bật: tắt cả hai trước khi làm.
  - Ảnh tạo bằng Nano Banana có một dấu lấp lánh nhỏ ở góc phải dưới, nằm ngoài vùng cắt vuông.
- **Giao diện tiếng Việt** (tài khoản 2): Bắt đầu / Kết thúc / Tìm kiếm thành phần / Thêm vào câu lệnh / Tải nội dung nghe nhìn lên / Bắt đầu tạo. Lần đầu tải ảnh có hộp "Quyền sử dụng hình ảnh này", cần chủ dự án đồng ý.
- **Lỗi "Audio generation failed":** bấm nút thử lại trên thẻ; Flow hoàn credit cho lần hỏng.
- **Tự động hoá bằng mã trong trang:**
  - Flow chặn tạo hàm từ chuỗi (`new Function`, `eval`), nên vòng lặp sẽ dừng mà không báo lỗi. Dùng hàm so khớp viết sẵn.
  - Ảnh "điểm bắt đầu" thường có tên chung chung (ví dụ "Edit illustration into animation…"). Nếu hai ảnh trùng tên, chọn theo thứ tự: hộp chọn xếp ảnh mới nhất trước.
  - Hết credit thì Flow hiện dải "Bạn đã dùng hết tín dụng Google Flow". Lệnh gửi sau đó không chạy, nên cần kiểm tra lại số thẻ đã tạo.

## 6. Tải về và đưa vào công cụ duyệt

- **Tải từ Flow:**
  - Dùng nút Tải xuống → 720p của Flow.
  - Nút này nạp video vào bộ nhớ rồi xoá ngay link tạm, nên tải nhanh liên tiếp sẽ bị rơi file. Cách đã dùng: giữ lại khối dữ liệu Flow đã nạp (bắt `URL.createObjectURL`) rồi tự lưu ra máy.
  - Tên file Flow có đuôi 8 ký tự là đầu mã media; ghép mã media với lời yêu cầu để biết tranh nào.
- **Đặt tên** `<mã tranh>.mp4`, rồi nhập vào kho clip:

```bash
python -m tapdoc import-clips <thư mục chứa clip>
```

  Clip được chép vào `content/clips/` (ngoài git) và ghi vào `content/manifests/video_manifest.json` với trạng thái `cho_duyet`. Nhập lại một clip thì clip quay về chờ duyệt, giữ ghi chú cũ.
- **Duyệt:**

```bash
python -m tapdoc review
```

  Mở tab "Tranh động": tranh gốc cạnh clip, Đạt / Không đạt, ghi chú. Clip "Không đạt" kèm ghi chú là danh sách cần làm lại.
