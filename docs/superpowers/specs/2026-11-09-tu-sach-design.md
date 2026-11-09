# Thiết kế: Tủ sách — chọn sách giáo khoa

> Ngày 09/11/2026. Bản mẫu đã xem (trang tạm, không nằm trong git): `.superpowers/brainstorm/10119-1794208659/content/tu-sach.html`.
>
> Ký hiệu:
> - **[Chốt]**: chủ dự án đã quyết.
> - **[Đề xuất]**: người viết đề xuất, chủ dự án đã nghe và đồng ý chung.
> - **[Builder]**: để người làm tự quyết.

## 1. Mục đích

App có ba quyển sách:

| Quyển | Mã | Số bài |
|---|---|---|
| Tiếng Việt 1 – Tập một | `tv1_t1_1990` | 80 bài |
| Tiếng Việt 1 – Tập hai | `tv1_t2_1996` | 91 bài |
| Tiếng Việt 2 – Tập một | `tv2_t1_2001` | 133 mục |

Hiện nay danh sách bài gộp chung các quyển, có thêm hai nút "Lớp 1 / Lớp 2". Chủ dự án muốn có chỗ chọn sách, để bài của các quyển không lẫn với nhau, và giao diện "hợp lý, đẹp, dễ chịu cho việc học" [Chốt].

## 2. Đã chốt

1. **Màn "Tủ sách"** theo bản mẫu: các quyển đứng trên kệ như sách thật; bé chạm bìa thì vào danh sách bài của quyển đó [Chốt].
2. **Mỗi quyển có ảnh bìa riêng** [Chốt].
3. **Bài học theo thứ tự:** học xong bài trước mới mở bài sau, như hiện nay [Chốt].
4. **Sách theo thứ tự:** học xong sách cấp thấp mới mở sách cấp cao hơn [Chốt]. Thứ tự sách là thứ tự trong `index.books`: TV1 tập một → TV1 tập hai → TV2 tập một.
5. **Ảnh bìa không có chữ.** Tên sách do app viết lên bìa bằng font Andika [Đề xuất, chủ dự án đồng ý chung]. Tranh vẽ mới theo phong cách app, không chép hay nhái bìa sách gốc, không có dấu hiệu của nhà xuất bản [Chốt, theo chính sách 05/11]. Làm hình tạm trước, vẽ bằng ChatGPT sau [Chốt, theo cách làm chung].

## 3. Mục tiêu, không làm, điều cấm

**Mục tiêu**
- Mỗi lần bé chỉ thấy bài của một quyển. Nhìn Tủ sách là biết đang học quyển nào, học tới đâu.
- Thêm quyển mới (ví dụ Tiếng Việt 2 tập hai) chỉ cần thêm vào `index.books` và có ảnh bìa, không sửa code.

**Không làm**
- Không đổi màn học, bài học, luật chấm, hiệu ứng trong bài.
- Không có chỗ để bé chọn lớp riêng ngoài Tủ sách.

**Điều cấm**
- Bé vào được bài của quyển còn khoá. Ngoại lệ: phụ huynh đã bật "Mở mọi bài".
- Chữ tràn, vùng chạm dưới 160, hay ra ngoài vùng an toàn ở 9 cỡ máy (`ScreenSizes.All`).
- Mất tiến độ đã có khi cập nhật app. Bài đã học xong vẫn là đã học xong, hoa vẫn còn.

## 4. Luồng

```
chọn bé → Tủ sách → (chạm bìa quyển đã mở) → danh sách bài của quyển → bài → cảnh học xong bài
```

- **Tủ sách** hiện sau khi chọn bé, và mỗi khi bé bấm nút về Tủ sách ở danh sách bài [Đề xuất].
- **Mở app các lần sau:** chọn bé xong vẫn qua Tủ sách; quyển đang học nhún sẵn để bé chạm [Đề xuất].
- **Học xong bài cuối của một quyển (không phải quyển cuối):** ở cảnh học xong bài, nút "Bài tiếp" đổi thành nút **Tủ sách**; nút "Về danh sách" giữ nguyên [Quyết định của người viết].
  - Bấm nút Tủ sách: quyển kế tiếp vừa mở khoá chạy hiệu ứng ổ khoá rơi, bìa sáng lên, kèm tiếng động [Đề xuất; hiệu ứng cụ thể là Builder].
  - Hiệu ứng chỉ chạy một lần, ngay khi đi từ nút đó; không lưu dấu "đã xem" vào file tiến độ.
  - Bài cuối của quyển cuối: không có nút "Bài tiếp", như hiện nay.

## 5. Màn Tủ sách

**Hàng trên**
- Trái: nút đổi bé (hình đại diện của bé), chuyển từ danh sách bài sang đây.
- Giữa: tiêu đề "Tủ sách của {tên bé}".
- Phải: nút bánh răng (Cài đặt).

**Kệ sách**
- Các quyển xếp một hàng theo thứ tự trong `index.books`, đặt trên một vạch kệ. Bìa đứng, tỷ lệ khoảng 3:4, viền mực, bóng gạch chéo.
- Trên điện thoại màn rộng thì bìa to hơn. Khi có nhiều quyển hơn chỗ trống thì kệ cuộn ngang [Builder: cỡ, số quyển trên một màn].
- Mỗi bìa gồm:
  - ảnh bìa;
  - tên quyển do app viết (`BookEntry.title`, tách hai dòng như "Tiếng Việt 1" và "Tập một") [Builder: cách tách];
  - "Đã học n/N bài" và thanh tiến độ.
- **Ba trạng thái của bìa:**
  - **Đang học** (quyển đầu tiên chưa học xong mà đã mở): viền cam, nhún nhẹ.
  - **Đã học xong:** có dấu "Đã học xong" và bông hoa bé ngoan nhỏ [Đề xuất].
  - **Chưa mở:** bìa mờ, có ổ khoá. Chạm vào thì bìa lắc nhẹ, không mở [Đề xuất].
- Gà con đứng ở góc dưới phải [Đề xuất].
- **Thiếu ảnh bìa:** dùng nền màu riêng của quyển (một bảng màu cố định theo thứ tự quyển) [Builder].

## 6. Danh sách bài của một quyển

- Như danh sách hiện nay (các phần, tuần, thẻ bài, hoa, ổ khoá, bài đang học nhún, số cột theo màn), nhưng **chỉ có bài của quyển đã chọn**.
- **Bỏ hai nút "Lớp 1 / Lớp 2"** (commit `39ead72` của session Lớp 2). Tủ sách thay cho việc chọn lớp.
- Tiêu đề là tên quyển.
- Góc trên trái là nút về Tủ sách, thay chỗ nút đổi bé. Biểu tượng là quyển sách hay kệ sách [Builder: dùng biểu tượng có sẵn hay thêm mã mới].
- Các nút Sổ bé ngoan, Phụ huynh, bánh răng và nút Ôn lại giữ chỗ như hiện nay.

## 7. Luật mở khoá

- **Quyển:**
  - Quyển đầu tiên luôn mở.
  - Quyển k mở khi **mọi bài** của quyển k−1 đã học xong.
  - Nếu "Mở mọi bài" bật cho bé này thì mọi quyển đều mở.
- **Bài trong một quyển:** đã mở quyển thì bài đầu mở; bài sau mở khi bài trước đã học xong; bài đã học xong luôn mở (như hiện nay).
- **Thay đổi so với hiện nay:**
  - Chuỗi mở khoá đang tách theo lớp: lớp 2 mở sẵn từ bài đầu. Giờ lớp 2 chỉ mở khi đã học xong lớp 1.
  - Hai tập lớp 1 trước đây là một chuỗi liền nhau; giờ tập hai mở khi xong hết tập một, kết quả tương đương.
  - Bé đã học ở trường thì phụ huynh dùng "Mở mọi bài".
- **Tiến độ cũ:** bài đã học xong giữ nguyên. Bé đã lỡ học vài bài lớp 2 (khi lớp 2 còn mở sẵn) mà lớp 1 chưa xong: quyển lớp 2 vẫn khoá hẳn, chưa vào được cho tới khi xong lớp 1; các bài đã học vẫn được ghi nhận [Quyết định của người viết: app chưa phát hành, trường hợp này chỉ có trên máy thử].

## 8. Các phần khác theo quyển

- **Sổ bé ngoan:** mở từ danh sách bài của một quyển thì chỉ có trang của các bài trong quyển đó [Đề xuất].
- **Cảnh học xong bài:** sổ hiện trang của bài vừa học, lấy theo quyển của bài đó.
- **Ôn lại:** chỉ ôn các lượt bé nhầm trong quyển đang mở. Nút Ôn lại chỉ bấm được khi quyển đó có lượt nhầm [Đề xuất].
- **Màn Phụ huynh:** mỗi bé có "Đã học n/N" cho từng quyển [Đề xuất]. Phần chữ hay nhầm giữ như hiện nay [Builder].
- **Phụ lục sách:** giữ như hiện nay, theo `BookEntry.appendix`.

## 9. Ảnh bìa

- **Mã ảnh:** `img_bia_<book_id>`, ví dụ `img_bia_tv1_t1_1990`. Lấy từ `index.books`, nên thêm quyển mới không phải sửa code [Đề xuất].
- **Tranh:**
  - nét mực, màu kiểu SGK xưa, nền giấy;
  - không chữ, không logo, không dấu hiệu của nhà xuất bản;
  - chừa khoảng trống phía trên để app viết tên quyển.
- **Chủ đề gợi ý** [Builder: câu lệnh vẽ cụ thể]:
  - TV1 tập một: bé tập đọc chữ cái, bảng chữ, phấn;
  - TV1 tập hai: bé đọc truyện dưới tán cây;
  - TV2 tập một: hai bạn cùng đến trường.
- **Hình tạm:** bìa màu có hình quyển sách, sinh bằng công cụ Python như các biểu tượng.
- **Hình chính thức:** vẽ bằng ChatGPT (project Kiet_1, trình duyệt Edge trên máy này); hỏi chủ dự án trước khi tải; trạng thái `cho_duyet`.
- **Đóng gói lên Drive:** cùng đợt Tập 2, như biểu tượng bánh răng [Chốt 05/11].

## 10. Ràng buộc

- Unity 6.6, uGUI dựng bằng code, TMP với font Andika. Màn của bé nằm trong `AppRoot.KidRoot`. Theo phong cách và bảng màu SGK.
- Dữ liệu đọc từ `index.json` (`books`, `lessons`). Không viết cứng số quyển hay mã quyển trong giao diện.
- Chỉ chạy test của phần đang làm; bộ đầy đủ chỉ khi chủ dự án nói "test all". Không test nội dung Tập 2 hay lớp 2 đang làm dở (test dùng tranh, âm thanh giả khi cần).
- Phối hợp với session Lớp 2 (`tv2-tap-1`): báo trước khi sửa `LessonListScreen`, `ParentScreen`, `ResultScreen` và `LessonIndex`, để hai bên không sửa cùng lúc.
- Chỉ nhánh `main`, commit từng phần, không push.

## 11. Kiểm tra

- **Luật mở quyển:**
  - quyển đầu luôn mở;
  - quyển sau mở đúng khi xong hết quyển trước;
  - "Mở mọi bài" mở hết;
  - tiến độ cũ không mất (gồm trường hợp bé đã học vài bài lớp 2).
- **Luật mở bài trong quyển:** như test hiện có, chạy theo từng quyển.
- **Tủ sách:**
  - đúng số quyển và thứ tự;
  - ba trạng thái bìa;
  - chạm quyển khoá thì không mở;
  - chạm quyển mở thì vào đúng danh sách.
- **Danh sách bài:** chỉ có bài của quyển đó; nút về Tủ sách đúng.
- **Theo quyển:** Sổ bé ngoan, Ôn lại, màn Phụ huynh.
- **Học xong quyển:** về Tủ sách, quyển sau vừa mở.
- **Bố cục** ở 9 cỡ máy, có ảnh chụp cho chủ dự án.

## 12. Để người làm quyết [Builder]

- Cỡ bìa, khoảng cách, cuộn ngang; cách tách tên quyển thành hai dòng.
- Hiệu ứng mở khoá quyển; biểu tượng nút về Tủ sách.
- Nơi lưu "quyển đang mở" của mỗi bé (nếu cần); bỏ hay giữ trường `GradeTab` cũ trong file tiến độ.
- Câu lệnh vẽ bìa; bảng màu dự phòng.
