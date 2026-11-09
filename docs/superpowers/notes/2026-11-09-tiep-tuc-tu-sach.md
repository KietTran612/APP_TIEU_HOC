# Ghi chú tiếp tục — Tủ sách, 9/11/2026

Đọc file này trước khi làm tiếp Tủ sách. Thiết kế: [2026-11-09-tu-sach-design.md](../specs/2026-11-09-tu-sach-design.md); kế hoạch: [2026-11-09-tu-sach.md](../plans/2026-11-09-tu-sach.md); sổ theo dõi: `.superpowers/sdd/2026-11-09-tu-sach/progress.md`.

## 1. Đang ở đâu

| Phần | Trạng thái |
|---|---|
| Luật quyển, bài (`BookShelf`) | Xong (c71d0bb) |
| Biểu tượng Tủ sách, bìa tạm `img_bia_<book_id>` | Xong (992eb8c). PNG chỉ có trên máy này, đóng gói cùng Tập 2 |
| Màn Tủ sách, danh sách theo quyển, bỏ tab Lớp 1/Lớp 2 | Xong (445e91b) |
| Học xong quyển → về Tủ sách, quyển mới có hiệu ứng mở khoá | Xong (fedd386) |
| Sổ bé ngoan, Ôn lại, tiến độ Phụ huynh theo quyển | Xong (9b7bc49) |
| Review độc lập | Không có lỗi nghiêm trọng/quan trọng; đã sửa các mục nhỏ đáng làm (30b6622); vạch kệ đè dòng "Đã học" — đã hạ dòng chữ |
| Ảnh bìa chính thức (ChatGPT) | Xong 9/11: 3 bìa 600×800 đã nhập, `cho_duyet`; dòng danh mục đã commit, PNG đóng gói cùng Tập 2 |
| Tên quyển | Chủ dự án đổi 9/11: "Bé tập đọc 1/2/3" (không dùng tên sách gốc) — `content/books.json`, `index.json` |
| Test all | Chưa chạy (chờ chủ dự án nói "test all") |

## 2. Cách hoạt động (tóm tắt)

- Chọn bé → **Tủ sách**: các quyển xếp theo `index.json` → `books`. Quyển đầu luôn mở; quyển sau mở khi học xong mọi bài quyển trước, hoặc khi phụ huynh bật "Mở mọi bài".
- Chạm bìa → danh sách bài của quyển đó (bài mở theo chuỗi trong quyển). Nút góc trên trái về Tủ sách. Quyển đang mở nhớ theo từng bé (`Profile.open_book`).
- Học xong bài cuối của một quyển: màn kết quả thay "Bài tiếp" bằng nút Tủ sách; về Tủ sách thì khoá quyển sau rơi xuống (không chạy lại nếu quyển đó đã học xong).
- Sổ bé ngoan và Ôn lại chỉ tính quyển đang mở; lượt nhầm lỗi thời của mọi quyển vẫn được dọn. Màn Phụ huynh: mỗi quyển một dòng tiến độ dưới tên bé.
- Thêm quyển mới: thêm vào `books.json` + bài trong index, chạy `python -m tapdoc ui-icons` (không `--force`) để có bìa tạm; không cần sửa code.

## 3. Làm tiếp (Claude)

1. **Bìa (Task 7) đã xong.** Chủ dự án duyệt qua nhiều lần vẽ lại (chat "Tạo tranh bìa sách", project Kiet_1):
   - bìa 1: cậu bé viết "a ă â b c" bằng **tay phải** (bảng bên trái tranh, bé bên phải);
   - bìa 2: bé gái đọc truyện dưới cây bàng;
   - bìa 3: hai bạn đi đến trường, **không nắm tay** (bạn trai nắm quai cặp, bạn gái ôm sách).
   Ảnh gốc 1086×1448 thu nhỏ 600×800 bằng System.Drawing (máy không có Pillow) rồi `import-image`.
2. **Khi nhập bìa thật:** giữ kích thước nhập ≤ 600×800 (bìa giữ trong bộ nhớ suốt phiên — `AppRoot._coverSet`), hoặc chuyển sang chuẩn bị bìa ở `ShowShelf` và nhả cùng bộ màn.
3. **Khi thêm quyển thứ 4 (TV2 tập hai):** hàng bìa đang căn giữa, vạch kệ rộng cố định. Ở màn hẹp nhất (1440) bốn quyển vừa sát mép, từ 5 quyển trở lên quyển đầu/quyển đang học nằm ngoài màn. Sửa: khi hàng bìa rộng hơn vùng nhìn thì căn trái và cuộn tới quyển đang học; vạch kệ theo bề rộng hàng bìa.
4. Quyển có 0 bài trong `books` không bao giờ "học xong" → chặn mọi quyển sau (trừ khi bật Mở mọi bài). Hiện không có quyển nào như vậy.

## 4. Việc của chủ dự án

- Thử app: chọn bé → Tủ sách → chạm quyển; bật/tắt "Mở mọi bài" ở Phụ huynh để thấy quyển mở/khoá.
- Duyệt ảnh bìa khi Task 7 xong.
- Đóng gói biểu tượng Tủ sách, bánh răng và bìa cùng Tập 2 (đã chốt).
- Tên app vẫn chưa chốt (`UiText.AppTitle`).
- Push.

## 5. Bài học

- `LayoutProbe` không kiểm chồng lấn giữa các phần tử: dòng tiến độ Phụ huynh từng bị nút "Mở mọi bài" che, vạch kệ từng đè dòng "Đã học x/y bài", mà test vẫn xanh. Màn có chữ cạnh nút thì thêm assert không chồng lấn (xem `Parent_ProgressPerBook`) và luôn xem ảnh chụp.
- Danh sách bài: tính trạng thái mở khoá một lần cho cả quyển, không gọi `BookShelf.IsLessonUnlocked` cho từng thẻ (mỗi lần gọi duyệt lại cả quyển trước).
- Test cần nguồn ảnh giả riêng thì bọc `AppRoot.SourceFactory` sau `UseStubsForMissingAssets()` để TearDown dọn.
