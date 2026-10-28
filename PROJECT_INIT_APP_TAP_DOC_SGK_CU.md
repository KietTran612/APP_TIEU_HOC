# TÀI LIỆU KHỞI TẠO DỰ ÁN — ỨNG DỤNG HỌC TIẾNG VIỆT & TẬP ĐỌC THEO SGK CŨ

> **Trạng thái:** Tài liệu định hướng ban đầu (Draft v0.1)  
> **Ngày lập:** 28/10/2026  
> **Mục tiêu:** Thống nhất phạm vi, nguồn tham chiếu, phương pháp biên soạn và kế hoạch triển khai trước khi viết ứng dụng.

## 1. Tầm nhìn dự án

Phát triển **ứng dụng học tiếng Việt và tập đọc dành cho trẻ em**, lấy **lộ trình dạy học của sách giáo khoa (SGK) Tiếng Việt tiểu học chương trình cũ trước đợt đổi sách từ năm 2002** làm tài liệu tham chiếu. Ứng dụng chuyển kiến thức và phương pháp thành các bài học số ngắn gọn, hấp dẫn, có hình minh họa mới, âm thanh phát âm và thao tác tương tác trực quan.

- **Giai đoạn đầu:** chức năng tập đọc là trọng tâm; chưa phát triển thành game khám phá thế giới / nông trại.
- **Phạm vi chương trình nghiên cứu:** lớp 1, 2, 3, 4, 5.
- **Đối tượng ban đầu được nhắc tới:** trẻ 3–8 tuổi. Cần phân biệt với độ khó của chương trình lớp 4–5 (thường dành cho trẻ lớn hơn); vì vậy nên thiết kế cấp độ theo **năng lực đọc** và bổ sung nội dung lớp 4–5 khi thích hợp.
- **Định hướng nền tảng:** ưu tiên ứng dụng di động; công nghệ triển khai chưa được chốt. Unity 2D là một phương án có thể cân nhắc, không phải quyết định đã phê duyệt.

### 1.1 Điều dự án **không** nhằm làm

- Không chỉ đưa PDF hoặc trang scan sách lên màn hình để bé lật trang.
- Không chỉ thay hình bìa hoặc tái bản y nguyên trang SGK.
- Không mặc định đưa nguyên văn bài đọc hay tranh trong SGK vào sản phẩm phát hành nếu chưa có quyền sử dụng.
- Không ưu tiên cơ chế cày cấp, chiến đấu, hoặc trang trí ngôi làng ở MVP.

## 2. Nguồn dữ liệu tham chiếu đã chọn

**Nguồn chính do chủ dự án lựa chọn:**

- GitHub: https://github.com/giangtv134/sach-giao-khoa-viet-nam
- Vai trò của kho: **nguồn tài liệu gốc để kiểm kê và đối chiếu** thứ tự bài, chữ, âm, vần, từ, câu, bài tập đọc và cách phân tầng kiến thức.
- Trạng thái kiểm chứng: **chưa có bản kiểm kê chi tiết tất cả file / trang / mục lục trong repository ở thời điểm lập tài liệu này**. Không được xem bất kỳ tên bài hay thứ tự bài suy đoán nào là đã xác thực.

**Nguồn đối chiếu bổ sung (không thay thế repo chính):**

- Kho sách cũ: https://thuongmaitruongxua.vn/ds-chuyen-muc/ban-scan-sgk-cac-thoi-ky/giai-doan-1990-2003/
- Trang tham khảo học Tiếng Việt cũ: https://vietlayers.com/tieng-viet/hoc-tieng-viet

### 2.1 Các sách cần khảo sát

| Lớp | Quyển cần khảo sát | Bản năm từng được nêu trong quá trình trao đổi* | Trạng thái |
|---|---|---|---|
| 1 | Tiếng Việt 1 — Tập 1 | 1990 | Cần kiểm kê trang & mục lục |
| 1 | Tiếng Việt 1 — Tập 2 | 1996 | Cần kiểm kê |
| 2 | Tiếng Việt 2 — Tập 1 | 2001 | Cần kiểm kê |
| 2 | Tiếng Việt 2 — Tập 2 | 2002 | Cần xác minh thuộc hệ sách cũ |
| 3 | Tiếng Việt 3 — Tập 1 | 1997 | Cần kiểm kê |
| 3 | Tiếng Việt 3 — Tập 2 | 2002 | Cần xác minh thuộc hệ sách cũ |
| 4 | Tiếng Việt 4 — Tập 1 | 2002 | Cần xác minh thuộc hệ sách cũ |
| 4 | Tiếng Việt 4 — Tập 2 | 2003 | Cần xác minh thuộc hệ sách cũ |
| 5 | Tiếng Việt 5 — Tập 1 | 1998 | Cần kiểm kê |
| 5 | Tiếng Việt 5 — Tập 2 | 2004 | Cần xác minh thuộc hệ sách cũ |

\* **Chú ý:** Năm nêu ở đây là năm của các *bản được nhắc đến*, không chứng minh 10 quyển thuộc cùng một lần in hay cùng một bộ đồng nhất. Các lần tái bản sau năm 2001 vẫn có thể thuộc chương trình cũ; phải kiểm tra trang thông tin xuất bản và nội dung thực tế. Không trộn mục lục của bộ chương trình thay sách 2002–2006 vào bộ đã chọn.

**Tài liệu bổ sung tùy chọn:** Truyện đọc 1, Truyện đọc 2, Truyện đọc 3 thuộc hệ sách cũ; chỉ tích hợp sau khi kiểm tra nguồn và tính phù hợp.

### 2.2 Cách xác minh tài liệu nguồn

Với **mỗi quyển**, cần ghi nhận:

1. Tên chính xác, lớp, tập, NXB, tác giả/chủ biên nếu hiển thị.
2. Năm xuất bản / tái bản, lần in, nhãn chương trình nếu có.
3. Link repository, nhánh/commit, đường dẫn file và loại file.
4. Số trang, mức đầy đủ, chất lượng trang scan, trang bị thiếu.
5. Mục lục nguyên bản, tên bài, trang bắt đầu và kết thúc, chủ đề / phân môn.
6. Mức xác minh: `unverified` / `metadata_verified` / `toc_verified` / `page_verified`.

**Không tự điền tên bài, lời bài tập đọc hay số trang khi chưa xem được nguồn gốc.**

## 3. Nguyên tắc chuyển hóa SGK thành bài học trong app

Giữ **lộ trình kiến thức và độ khó tiến triển** của SGK làm tham chiếu, nhưng **biên soạn trải nghiệm học tập mới**:

`SGK nguồn → Kiểm kê & xác minh → Trích xuất dữ liệu làm việc → Phân tích mục tiêu bài → Biên soạn bài học cho app → Thiết kế minh họa mới → Ghi âm / TTS → Tương tác → Kiểm tra chất lượng → Phát hành`

Các đối tượng kiến thức cần quản lý:

- **Chữ cái, âm, dấu thanh.**
- **Vần, tiếng, từ** và quan hệ chữ viết–âm đọc.
- **Câu, đoạn văn, bài tập đọc**, hướng đến đọc rõ, đọc trôi chảy và đọc hiểu.
- **Minh họa / đối tượng hình ảnh** gắn với từng từ hoặc tình huống.
- **Giọng đọc chuẩn, phản hồi khi chọn đáp án, luyện tập và ôn tập.**

### 3.1 Khác biệt giữa SGK tham chiếu và sản phẩm app

| Thành phần | Vai trò SGK | Bản app dự kiến |
|---|---|---|
| Lộ trình | Thứ tự và mục tiêu dạy học | Cấu trúc level / bài tương ứng, có thể chia nhỏ |
| Từ vựng | Ví dụ và bối cảnh | Từ/câu được biên soạn, phân loại và gắn âm thanh |
| Tranh | Tư liệu nhận diện nội dung | **Tranh mới hoàn toàn**, cùng phong cách và độ rõ cao |
| Bài đọc | Nguồn tham chiếu | Bài đọc có quyền sử dụng hoặc được biên soạn mới |
| Học tập | Đọc trên giấy và dạy trên lớp | Nghe, chạm, kéo thả, đọc theo, nhận phản hồi |
| Đánh giá | Hoạt động theo sách | Lưu tiến độ, nhận diện nội dung cần ôn |

## 4. Chức năng chính: Tập đọc (ưu tiên MVP)

### 4.1 Phân tầng hoạt động

1. **Nghe và nhận diện:** nghe âm/từ, chạm đúng chữ hoặc hình.
2. **Nhận diện chữ và dấu:** nhìn chữ, phân biệt ký tự / dấu thanh.
3. **Ghép âm, ghép vần, tạo tiếng:** kéo thả thẻ; hiển thị và phát âm sau khi ghép.
4. **Đọc từ:** hiện từ rõ ràng, nghe mẫu, nhận biết từ gắn với hình.
5. **Đọc câu:** làm nổi bật từ theo nhịp nghe, luyện đọc câu ngắn.
6. **Đọc đoạn / bài:** chia văn bản theo câu, nghe mẫu, câu hỏi hiểu nội dung đơn giản.
7. **Ôn tập:** quay lại những nội dung trẻ còn nhầm lẫn.

Không phải mọi bài học đều cần đủ cả bảy hoạt động. Chọn hoạt động theo mục tiêu của bài.

### 4.2 Ví dụ bản mẫu (minh họa cơ chế, KHÔNG khẳng định là chép từ mục lục SGK)

**Bài chữ “o”:**

- Màn 1: hiện chữ `o` lớn; chạm để nghe âm.
- Màn 2: nghe yêu cầu, chọn chữ `o` giữa một số chữ khác.
- Màn 3: xem hình gà trống, nghe tiếng gáy và liên hệ âm (nếu phù hợp mục tiêu bài).
- Màn 4: tô đường nét chữ bằng thao tác chạm/vuốt (có thể để sau MVP).
- Hoàn thành: phản hồi tích cực, cập nhật trạng thái đã học.

### 4.3 Thiết kế phù hợp khả năng học

| Nhóm tham chiếu | Trọng tâm | Giao diện |
|---|---|---|
| 3–4 tuổi, tiền đọc | Nghe và nhận biết hình | Hình to, ít nút, không bắt buộc biết chữ |
| 4–6 tuổi | Nhận diện chữ, âm, dấu cơ bản | Một yêu cầu mỗi màn, có giọng hướng dẫn |
| 6–8 tuổi | Học vần, đọc tiếng, từ, câu | Ghép chữ, luyện đọc tăng dần |
| Học sinh lớp 3–5 / người học trình độ tương ứng | Đọc đoạn, đọc lưu loát, hiểu bài | Văn bản dài hơn, câu hỏi nội dung |

Ứng dụng cần cân bằng tính dễ dùng cho trẻ nhỏ với độ khó thực tế của bài học lớp 4–5. Phân tuyến theo **trình độ đọc thực tế**, không chỉ theo tuổi.

## 5. Định hướng hình ảnh và trải nghiệm

- Tạo hình minh họa **mới**, phong cách 2D thân thiện, dễ thương, tươi sáng, đường nét rõ, chủ thể dễ nhận diện.
- Thể hiện các bối cảnh quen thuộc với trẻ Việt Nam: gia đình, lớp học, con vật, rau củ, làng quê, vật dụng sinh hoạt.
- Mỗi bài học ưu tiên **một mục tiêu chính**, tránh quá nhiều tương tác gây xao nhãng.
- Font tiếng Việt rõ, dấu thanh dễ nhìn; màu sắc vừa phải, độ tương phản tốt; nút chạm lớn.
- Hiệu ứng và phần thưởng nhẹ nhàng, không gây áp lực, không dùng cơ chế trừng phạt khi trả lời sai.
- Xây dựng **style guide** cho hình ảnh để đảm bảo tất cả bài học cùng một phong cách.
- Chưa chốt tỷ lệ ảnh, kích thước sprite, layout màn hình, nhân vật dẫn chuyện hay hệ thống trang trí. Cần xác định sau bản prototype.

## 6. Âm thanh và luyện đọc

**Giai đoạn đầu:**

- Phát âm từng chữ/tiếng/từ/câu, nút phát lại.
- Có thể có giọng đọc hướng dẫn ngắn cho trẻ chưa đọc tốt.
- Phân biệt rõ **cách gọi tên chữ** và **âm được dạy khi học vần** trong kịch bản nội dung.
- Soát lỗi phát âm, dấu thanh, ngắt câu và tốc độ đọc; tránh phụ thuộc vào TTS chưa kiểm duyệt.

**Giai đoạn sau (chưa thuộc MVP):**

- Thu âm bằng micro và nhận diện lời đọc / đánh giá phát âm.
- Nếu làm với trẻ em: cần thiết kế quyền riêng tư, xin phép phụ huynh phù hợp, hạn chế lưu âm thanh và kiểm tra sai số nhận diện tiếng Việt trẻ nhỏ.

## 7. Kiến trúc dữ liệu bài học (đề xuất ban đầu)

Cấu trúc nội dung:

`Curriculum → Grade → Book/Volume → Unit/Section → Lesson → Activity → Item → Asset`

Ví dụ JSON **minh họa schema, không phải dữ liệu đã trích xuất từ SGK**:

```json
{
  "lessonId": "tv1_t1_demo_001",
  "curriculumId": "tieng_viet_cu_pre2002",
  "grade": 1,
  "volume": 1,
  "source": {
    "repository": "https://github.com/giangtv134/sach-giao-khoa-viet-nam",
    "editionYear": 1990,
    "filePath": null,
    "pageStart": null,
    "pageEnd": null,
    "verificationStatus": "unverified"
  },
  "title": "Bài mẫu: chữ o",
  "learningObjectives": ["Nhận diện chữ o", "Nghe âm mẫu"],
  "activities": [
    {
      "type": "listen_and_choose_letter",
      "promptAudioId": "audio_o_instruction",
      "choices": ["o", "a", "e"],
      "correctAnswer": "o"
    }
  ],
  "assets": ["image_rooster_original", "audio_o_sample"],
  "contentRightsStatus": "needs_review",
  "status": "prototype"
}
```

**Mỗi nội dung / asset nên có:** ID ổn định, nguồn gốc, bản quyền/quyền sử dụng, người biên soạn, ngày cập nhật, trạng thái duyệt và liên kết đến bài sử dụng.

## 8. Quy trình sản xuất dữ liệu

### Pha A — Kiểm kê repo

- Lấy danh sách thư mục, file, metadata cho tất cả lớp 1–5.
- Lập bảng mapping `Lớp / Tập / Năm / File / Trang / Mức đầy đủ`.
- Chỉ ra quyển còn thiếu, phiên bản trùng lặp hoặc chưa chắc thuộc chương trình cũ.

### Pha B — Số hóa và rà soát

- Trích xuất nội dung làm việc từ scan khi có quyền và phương tiện phù hợp.
- Đối chiếu trực quan với trang gốc, nhất là dấu tiếng Việt và tên bài.
- Chuyển sang bảng bài học có liên kết đến trang nguồn.
- Gắn trạng thái kiểm chứng; tránh công bố nội dung chưa duyệt.

### Pha C — Chuyển hóa sư phạm

- Xác định mỗi bài dạy kỹ năng gì; phân nhỏ các bước học.
- Viết mới văn bản, câu hỏi và hướng dẫn trong phạm vi được phép.
- Thiết lập mức độ khó và điều kiện hoàn thành.
- Giáo viên/chuyên gia tiếng Việt tiểu học rà soát trước khi đưa vào app.

### Pha D — Asset và tích hợp

- Lên danh sách minh họa, viết brief cho từng hình.
- Tạo/duyệt hình mới và audio; thống nhất tên file.
- Ánh xạ asset ID với lesson data.
- Test trên thiết bị thật và kiểm thử với nhóm tuổi mục tiêu, có sự đồng ý phù hợp của phụ huynh.

## 9. MVP đề xuất (cần chốt lại sau kiểm kê)

- **Nguồn nội dung trước mắt:** Tiếng Việt 1 — Tập 1 (bản dự kiến 1990, chỉ chốt khi kiểm chứng repo).
- **Phạm vi thử nghiệm:** khoảng 10–20 bài nhỏ được xác minh/biên soạn; chưa cần nhập toàn bộ SGK lớp 1–5 cùng lúc.
- **3 cơ chế đầu:** (1) nghe và chọn chữ/hình, (2) ghép chữ/vần, (3) nghe–đọc từ hoặc câu.
- **Giao diện cốt lõi:** trang chọn bài, màn học, màn kết quả, màn theo dõi tiến độ cơ bản.
- **Âm thanh:** nghe mẫu và phát lại; **chưa cần** chấm phát âm tự động.
- **Kho nội dung:** bài và asset tách khỏi mã ứng dụng để mở rộng nhiều lớp về sau.

### 9.1 Tiêu chí chấp nhận MVP

- Mỗi bài nêu được mục tiêu học và có nguồn tham chiếu rõ.
- Người học có thể hoàn thành toàn bộ luồng bằng chạm hoặc kéo thả.
- Âm thanh tiếng Việt đúng, dễ nghe, phát lại nhanh.
- Nội dung hiển thị đúng dấu và thứ tự bài đã duyệt.
- Ghi nhớ bài đã hoàn thành và hỗ trợ ôn tập cơ bản.
- Hình ảnh là sản phẩm mới, nhất quán phong cách và được kiểm tra quyền sử dụng.

## 10. Phân kỳ phát triển

| Giai đoạn | Kết quả bàn giao |
|---|---|
| 0 — Nghiên cứu nguồn | Danh sách repo, ấn bản, mục lục đã đối chiếu, khoảng trống nguồn |
| 1 — Mô hình dữ liệu | Schema + bảng lessons/assets/source + bộ dữ liệu mẫu |
| 2 — Thiết kế trải nghiệm | Luồng tập đọc, wireframe, style guide, mẫu hình/audio |
| 3 — MVP | App chạy được với một phần bài Tiếng Việt 1 Tập 1 |
| 4 — Hoàn thiện lớp 1 | Đầy đủ bài được chọn và đã duyệt của lớp 1 |
| 5 — Mở rộng | Lớp 2–5, đọc hiểu và luyện đọc nâng cao |
| 6 — Nâng cao | Micro, nhận diện giọng đọc, gợi ý ôn tập thông minh (nếu phù hợp) |

## 11. Rủi ro và lưu ý

1. **Bản quyền:** repo chứa scan không đồng nghĩa với cấp phép tái sử dụng nội dung và tranh. Kiểm tra giấy phép repo, quyền tác giả/quyền nhà xuất bản và phạm vi sử dụng; ưu tiên biên soạn câu chữ mới và minh họa mới. Tham vấn pháp lý nếu phát hành thương mại.
2. **Sai ấn bản:** một số năm tái bản sau 2001 vẫn có thể thuộc bộ cũ; cần xác thực qua trang sách, không chỉ qua tên file.
3. **Nhận dạng chữ:** bản quét cũ dễ sai dấu khi OCR; phải duyệt thủ công.
4. **Lứa tuổi:** nội dung lớp 4–5 không mặc nhiên phù hợp trẻ 3–8 tuổi; thiết kế phân cấp theo trình độ.
5. **Chất lượng học liệu:** hình đẹp nhưng không làm sai nghĩa từ hoặc phân tán sự chú ý khỏi mục tiêu học đọc.
6. **Quyền riêng tư trẻ em:** nếu sau này lưu dữ liệu định danh, audio, tài khoản hoặc có quảng cáo, cần thiết kế phù hợp đối tượng trẻ nhỏ ngay từ đầu.

## 12. Việc đã thống nhất và việc còn mở

### Đã thống nhất

- Làm **app học Tiếng Việt**, **tập đọc trước**.
- Dựa trên **SGK Tiếng Việt tiểu học cũ trước đợt thay sách 2002**, xét chương trình lớp 1–5.
- Lấy **GitHub `giangtv134/sach-giao-khoa-viet-nam`** làm nguồn tài liệu chính để nghiên cứu và chuyển hóa.
- Giữ **lộ trình kiến thức** làm tham chiếu, không chỉ nhúng PDF vào app.
- Tạo **hình ảnh mới** đẹp, hiện đại và đồng nhất; kết hợp âm thanh và tương tác đọc.
- Bắt đầu nhỏ từ lớp 1, sau đó mở rộng hệ thống dữ liệu cho các lớp khác.

### Còn cần quyết định / xác minh

- Repo có đủ file và mục lục những quyển nào? Phiên bản chính xác của từng file?
- Những bài nào sẽ được chọn đưa vào app và quyền sử dụng văn bản ra sao?
- Dùng Unity 2D hay nền tảng phát triển app khác?
- Thiết bị ưu tiên (Android, iOS, tablet) và chính sách offline?
- Phong cách mỹ thuật cụ thể, nhân vật hướng dẫn, thư viện âm thanh.
- Có cần tài khoản phụ huynh / đồng bộ tiến độ hay chỉ lưu trên máy?
- Bộ tiêu chí kiểm thử học đọc và kế hoạch rà soát sư phạm.

## 13. Hành động tiếp theo ưu tiên

**Nhiệm vụ đầu tiên:** kiểm kê thực tế repository GitHub đã chọn, tạo `BOOK_CATALOG.md` cho lớp 1–5 và `LESSON_INDEX.csv` theo những trang có thể xác minh. Sau đó lấy **Tiếng Việt 1 — Tập 1** để tạo **1–3 bài prototype có dữ liệu, hình minh họa, âm thanh và tương tác hoàn chỉnh**.

---

**Nguyên tắc xuyên suốt:** *Bám sát lộ trình học của SGK cũ, nhưng tạo nội dung và trải nghiệm ứng dụng hiện đại, rõ nguồn, phù hợp trẻ nhỏ và có thể mở rộng bền vững.*
