# Ghi chú tiếp tục: tỷ lệ màn hình (cách B)

- **Bản thiết kế:** `docs/superpowers/specs/2026-11-05-ty-le-man-hinh-design.md`
- **Kế hoạch:** `docs/superpowers/plans/2026-11-05-ty-le-man-hinh.md`
- **Sổ theo dõi:** `.superpowers/sdd/2026-11-05-ty-le-man-hinh/progress.md`, không nằm trong git.

## Đã làm (trên main, chưa push)

| Task | Nội dung |
|---|---|
| 1 | `ScreenLayout.Compute`: từ cỡ điểm ảnh và lề an toàn của máy tính ra cỡ canvas, vùng an toàn, khung của bé, khung chuẩn 1440, và chọn kiểu mép hay kiểu góc. Lề an toàn đọc qua `DeviceSafeArea`; test gán `Override` để giả lập máy. |
| 2 | Canvas mở rộng (Expand) quanh 1440×1080. `AppRoot` có hai gốc: `KidRoot` cho màn của bé, `SafeRoot` (1440) cho màn người lớn và màn chuẩn bị. Hai gốc được tính lại mỗi khung hình, chỉ đặt lại khi cỡ đổi. |
| 3 | `FitBox` phóng to đều một khối cỡ thiết kế; `FrameWatcher` báo khi cỡ màn đổi. `UiKit.CreateStage` trả `Stage` 1400×680 nằm trong `StageArea`. `DragTile` đổi quãng ngón tay ra toạ độ của cha, nên thẻ bám ngón tay cả khi phần học phóng to. |
| 4 | Màn học có kiểu góc (như máy tính bảng) và kiểu mép (điện thoại: nút ở hai dải mép, phần học to lên). Đổi cỡ thì chỉnh tại chỗ, không dựng lại bước. Khung Ghi chú: nền phủ kín, nội dung rộng 1440 ở giữa. |
| 5 | Danh sách bài thêm cột trên màn rộng (2400: 10 cột, iPhone: 8 cột), giữ chỗ cuộn khi đổi cỡ. Chữ thẻ bài tự co tới 22. |
| 6 | Sổ bé ngoan và cảnh học xong bài to lên trên màn rộng. Đổi cỡ giữa cảnh thì cảnh nhảy tới cuối, lời khen chỉ phát một lần. Hoa bay hạ đúng cỡ ô. |
| 7 | Mọi test bố cục chạy đủ 9 cỡ trong `ScreenSizes.All`. Test đi hết mọi bài chạy 5 cỡ tiêu biểu (`ScreenSizes.LessonWalk`). Thêm test: màn dọc; đổi cỡ vẫn giữ tên đang gõ và cổng phụ huynh. |

## Quyết định của người làm

1. **Phóng to phần học ở kiểu mép theo nội dung thật của từng bước.**
   - Mức tối đa bằng mức của kiểu mép, tối thiểu bằng 1 (máy tính bảng), nên vùng chạm luôn ≥ 160.
   - Chỉ đo bước đang hiện, kể cả phần đang ẩn sẽ hiện sau. Chữ đo theo từng ký tự vẽ ra.
   - Lý do: vài bước (bảng đọc nhiều hàng như bài 80) cao hơn khung 680. Nếu phóng to theo khung, thẻ sẽ ra khỏi màn.
   - Hệ quả: các bước này to ít hơn các bước khác.
   - Chủ dự án đã chốt ngày 05/11/2026: "mỗi bước có thể tùy chỉnh to khác nhau nhưng cần hợp lý và thích hợp để học tập". Bản thiết kế đã sửa theo.
2. **Gốc khung Ghi chú phủ kín màn**, để các nút ở hai mép không bấm được khi khung đang mở.
3. **Chữ thẻ bài tự co tới 22 (trước là 26)**, vì tên bài chính tả tập 2 bài 138 tràn.
4. **Test đi hết mọi bài chỉ chạy 5 cỡ.** Ba cỡ còn lại (16:10, xoay dọc, gập) có cùng khung 1440×1080 như iPad 4:3.
5. **Kiểm tra "chữ trong vùng an toàn" đo theo từng ký tự vẽ ra.** `textBounds` của TMP sai với dấu "˜" đứng riêng.
6. **Cài đặt nền tảng giữ nguyên** theo bản thiết kế mục 5.7:
   - Android khoá màn ngang, target API để tự động;
   - iOS khoá màn ngang, `UIRequiresFullScreen` bật.
   Khi build lần đầu, nhớ thử trên máy thật: điện thoại có tai thỏ, máy tính bảng Android 16 xoay dọc, iPad chia đôi màn.

## Sửa sau review độc lập

- **Màn chuẩn bị (gà con chờ tải bài) phủ kín màn.** Trước đây trên điện thoại nó chỉ che khung 1440 ở giữa, nên các nút ở hai mép vẫn bấm được trong lúc tải.
- **Phần học trên điện thoại không còn bị thu dưới mức 1.** Trước đây bước cũ chờ huỷ và khung cao của nhãn dấu thanh làm thẻ ở bài đánh vần còn 146.
- Hai test mới cho hai lỗi này đều hỏng trước khi sửa. Sau khi sửa, 141/142 test liên quan đạt, gồm 22 bài đi hết từng bước. Test hỏng còn lại là do thiếu tranh tập 2 (mục dưới).

## Lỗi có từ trước, không thuộc việc này

1. **Thiếu tranh hệ thống `img_chung_cau_hoi` của tập 2:** mọi test khởi động app báo lỗi. Test của việc này dùng `UseStubsForMissingAssets()`. Khi có tranh thì các test cũ tự hết lỗi.
2. **`AppFlowTests.MainScene_ListsIndexLessons`** cho rằng mọi thẻ đều bắt đầu bằng "Bài N". Các bài tập 2 có nhãn riêng (ví dụ "Chính tả").

## Còn lại

- Chủ dự án xem ảnh chụp ở `unity/TapDoc/TestOutput/screens/<tên cỡ>/` (`phone_20x9`, `iphone`, `ipad_43`, `tab_portrait`…).
- "Test all" khi chủ dự án yêu cầu.
- Push do chủ dự án làm.
