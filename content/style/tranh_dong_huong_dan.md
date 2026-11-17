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
  7. **Người không biến thành con vật.** Trò chơi đóng vai (mèo đuổi chuột) vẫn là trẻ em bình thường, không có tai, đuôi hay lông thú. Ghi rõ bằng câu tả cái đang có: `the children look exactly as in the picture, ordinary schoolchildren in their school clothes`. Bỏ hẳn các chữ "mèo", "chuột", "đuổi" khỏi lời lệnh (xem quy tắc 17).
  8. **Tiếng con vật phải là tiếng thật của đúng con đó** (đợt duyệt 12/11: gà trống kêu như quạ, voi kêu như kèn).
     - Lời lệnh gọi đúng tên tiếng thật, ví dụ `one long, loud, real rooster crowing "cock-a-doodle-doo" (a domestic farm rooster)`, `a real wild elephant trumpeting call recorded in nature, deep and animal`. Không nhắc tên tiếng không muốn có (quy tắc 17).
     - Nếu Flow vẫn ra tiếng sai: làm lại clip chỉ có tiếng động nhẹ (gió, bước chân, lá xào xạc), không có tiếng kêu, và ghi vào `ghi_chu` để chủ dự án biết.
  9. **Người hay vật không đi vào từ vùng đệm ngoài tranh** (đợt xem trước 12/11: người mẹ đi vào từ mép phải bị cắt thẳng một đường dọc). Tranh đệm 16:9 có hai dải giấy trống hai bên; khi đưa vào app chỉ giữ phần vuông ở giữa, nên ai đi ra vào dải đó sẽ bị cắt thẳng. Khung đầu đặt mọi nhân vật nằm trọn trong phần tranh vuông. Lời lệnh **không nhắc tới lề giấy, mép tranh hay "inside the picture"**. Ngày 13/11, câu "the paper margins stay empty" làm Veo vẽ mép giấy cuộn lên và thêm trẻ em tràn ra lề (b68); xem quy tắc 17. Thay vào đó tả cái đang có: `nobody new appears`, `each one stays in its place`, `the camera and background stay still`. Máy quay và nền đứng yên, không kiểu máy quay chạy theo nhân vật.
  10. **Clip dừng đúng tư thế trong tranh, không diễn quá rồi giật về** (bé đã đứng dậy rồi khung cuối ngồi bệt lại; hai bạn đi quá chỗ rồi giật về giữa cầu). Lời lệnh tả hành động chỉ tới đúng tư thế trong tranh và nói rõ điều không được xảy ra, ví dụ `the clip ends with the boy still sitting on the ground`, `that spot in the middle of the bridge is where their walk ends`.
  11. **Đi, chạy, bay, xe chạy phải tiến thật** (root soát 12/11). Khung đầu đặt nhân vật lùi lại vài bước trên chính con đường hay khoảng trời TRONG tranh, hơi nhỏ hơn và xa hơn. Nhân vật tự đi tới đúng chỗ trong tranh; nền và máy quay đứng yên; không đi vào từ vùng đệm. **Chỉ lùi vài bước, giữ nhân vật gần như cùng cỡ, cho quãng đi ngắn.** Lùi xa quá thì Veo vẽ lại thành người khác. Bài học b235 ngày 12/11: khung đầu để Minh quá nhỏ, quá xa, nên Veo đổi quần áo, đổi mặt, rồi chồng hình ở cuối clip.
      - **Tới nơi ở giây thứ bảy, giây cuối đứng yên** (17/11, b110 quê ngoại, b112). Clip người đi mà kết thúc "khi đang bước" thì Veo gò khung cuối về tranh trong 0,1–0,2 giây cuối, nên nhân vật bị giật nhỏ lại hay lệch chỗ. Lời lệnh: `… arrives at the place in the picture by the sixth second; the last two seconds hold completely still exactly as in the final illustration`, kèm End frame là tranh gốc. Cuối ngày 17/11 đổi từ "giây thứ bảy, giây cuối" sang "giây thứ sáu, hai giây cuối", vì với câu cũ b105 rước đèn, b110 quê ngoại, b112 vẫn đi qua đúng tư thế tranh ở 7,7 s rồi bước tiếp (khung cuối lệch tranh 25–38). Kiểm bằng `picDiff` ở 7,0 / 7,5 / 7,7 s và khung cuối, tất cả dưới khoảng 16–18, chỉ đo ở 7,7 s là chưa đủ; và `endDiff` (các khung cuối lệch nhau dưới khoảng 3).
      - **Xem nhân vật đi về phía nào trước khi chọn to hay nhỏ** (17/11, b173). Nhân vật đi lại gần người xem thì khung đầu vẽ nhỏ hơn, xa hơn. Nhân vật đi ra xa người xem (như hai bạn chạy vào trường) thì khung đầu phải vẽ **to hơn, gần hơn**. Vẽ ngược thì clip thành chạy lùi.
      - **Khung đầu chỉ lùi vừa phải** (17/11, b82 học sinh, b82 con kênh, b142). Nếu khung đầu vẽ nhân vật nhỏ hơn hẳn hay ở xa hẳn so với tranh, Veo không cho đi tới mà làm chuyển cảnh mờ ở giây 5–7: cây cối, nền nhạt rồi mất, nhân vật chồng hình hoặc đổi dáng, rồi nền hiện lại. Hai clip đạt hôm đó (b110 quê ngoại, b112) chỉ lùi vừa phải. Giữ nhân vật ở khung đầu cỡ khoảng 80–85% so với tranh, đứng không quá xa chỗ cuối. Khi soát, xem kỹ các khung 4,5–7,5 s: nền phải còn nguyên suốt clip.
      - **Đồ vật nhỏ: chỉ cho ánh sáng chuyển động** (17/11, b05 cặp da, b08 ba lô). Hễ cho một bộ phận của đồ vật cử động (nắp gập, khoá bật, quai đung đưa, dây đai), Veo vẽ thêm hoặc làm méo: mọc khoá kéo, khoá thành cần gạt, dây đai vung ra mép. Với tranh một đồ vật, làm loop: vật đứng yên tuyệt đối, chỉ một vệt sáng lướt qua hay chỗ kim loại lóe sáng một lần.
  12. **Tranh là khoảnh khắc giữa động tác thì clip dựng tới đúng khoảnh khắc đó rồi dừng.** Không làm hết động tác rồi quay về (đó là "tua ngược"). Vật trao tay (quà, cốc, bát) chỉ đi một chiều.
  13. **Không biến mất, không chồng hình, không đổi hình.** Người, con vật, đồ vật không biến mất rồi hiện lại; không đổi màu, hoa văn hay kiểu dáng; nền giấy giữ một màu suốt clip.
  14. **Vật nào ra vật nấy.** Đồ gỗ, đồ sắt không tự chạy như máy; kim loại không cong mềm; bánh xe chỉ quay khi xe lăn; không có phoi gỗ khi không có gỗ; gấp, lắp, lớn, xếp chỉ đi một chiều, không tháo ngược lại.
  15. **Không thêm thứ phá tranh.** Không khói phồng to, không lửa trùm ra ngoài đèn, không tia nắng trên mặt trăng, không mây trên bảng đen, không vệt trắng vắt ngang cảnh; con vật không mọc tay, người không mọc đuôi hay tai thú.
  16. **Soát ảnh khung đầu trước khi gửi.** Mở ảnh xem trước trong hộp chọn khung, đối chiếu với tranh của clip (b58 cái túi từng bị lấy nhầm tranh chôm chôm của bài khác).
  17. **Không nhắc tên thứ không muốn có, kể cả để cấm** (QUY-TRINH §12, root 12/11). Hễ lời lệnh có tên một thứ, dù trong câu "không có…" hay "chỉ một chút…", Veo vẫn hay vẽ đúng thứ đó. Đã gặp: b220 có cục khói phồng dù dặn "khói mỏng"; b283 có vệt gió vì lời lệnh có chữ "gió"; b101 các bạn mọc đuôi vì lời lệnh có chữ "mèo".
     - Thay câu cấm bằng câu tả cái đang có, ví dụ `the drill and the bit lie still; only the crank turns`, `the moon stays a pale round moon`, `the background paper keeps exactly the same warm beige colour`.
     - Câu cấm chung không gọi tên vật cụ thể thì vẫn được: `no rewind`, `nothing enters from outside the picture`, `no new people`, `no speech, no words`.
     - Khi tạo khung đầu bằng Nano Banana, so màu lề giấy với tranh gốc. Lệch màu thì sửa thêm: `keep exactly the same warm beige paper colour as the original`.
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
