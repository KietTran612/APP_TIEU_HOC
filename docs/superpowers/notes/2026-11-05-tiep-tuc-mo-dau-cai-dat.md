# Ghi chú tiếp tục: màn mở đầu, popup cảnh báo, menu Cài đặt

- **Bản thiết kế:** `docs/superpowers/specs/2026-11-05-man-mo-dau-canh-bao-cai-dat-design.md`
- **Kế hoạch:** `docs/superpowers/plans/2026-11-05-man-mo-dau-canh-bao-cai-dat.md`
- **Sổ theo dõi:** `.superpowers/sdd/2026-11-05-man-mo-dau-canh-bao-cai-dat/progress.md` (không nằm trong git)

## Đã làm (trên main, chưa push)

| Task | Nội dung |
|---|---|
| 1 | `ProgressStore` thêm: `NoticeVersion` (phiên bản cảnh báo đã xem), đổi tên, đổi hình, xoá hồ sơ, xoá toàn bộ (kể cả file `.tmp`, `.bak`). |
| 2 | Popup "Gửi phụ huynh" gồm 5 lưu ý, đoạn dữ liệu của bé và đoạn lời khuyên. Chỉ hiện một lần sau khởi động; nút "Đã hiểu" không khoá. Khung rộng theo màn của bé, tối đa 1800 (chủ dự án muốn rộng hơn). |
| 3 | Màn mở đầu trong lúc nạp: nền giấy, gà con nhún, tên app, ba chấm. Nạp lỗi thì hiện một dòng báo. Đã tắt màn "Made with Unity". |
| 4 | Biểu tượng bánh răng `img_ui_cai_dat`, hình tạm vẽ bằng công cụ Python. |
| 5 | Menu Cài đặt: tiếng động (chuyển từ màn Phụ huynh sang), xem lại lưu ý, thông tin và ghi công. Có nút bánh răng ở danh sách bài và ở màn chọn bé. |
| 6 | Nhóm có khoá phụ huynh trong Cài đặt: đổi tên/hình, xoá hồ sơ (hỏi xác nhận), xoá toàn bộ (hỏi xác nhận hai lần, xong thì như lúc mới cài). Khoá phép tính tách ra thành `ParentGatePanel`, dùng chung với màn Phụ huynh. |
| 7 | Tắt sao lưu của hệ điều hành. Android: sửa manifest lúc build (`AndroidNoBackup`, chỉ chạy khi máy có cài module Android). iOS: đặt cờ không sao lưu cho file tiến độ. |

## Việc còn lại

1. ~~Đóng gói biểu tượng bánh răng~~ — xong: `img_ui_cai_dat` có trong gói media 746792b (09/11), dòng danh mục commit 916a3ca (10/11 kiểm lại).
2. **Vẽ biểu tượng bánh răng chính thức** bằng ChatGPT theo phong cách các biểu tượng khác.
3. **Tên app chính thức:** đổi `UiText.AppTitle` là màn mở đầu và Cài đặt đổi theo.
4. **Để tới lúc phát hành (đã ghi chú, chưa làm):**
   - trang web chính sách quyền riêng tư;
   - khai báo trên Google Play và App Store;
   - liên hệ, nhắc học.
5. **Khi build Android lần đầu:** kiểm tra manifest đã gộp có `android:allowBackup="false"`.
6. **"Test all"** khi chủ dự án yêu cầu.

## Lỗi có từ trước (do Tập 2 chưa xong, không thuộc việc này)

- Thiếu tranh `img_chung_cau_hoi`, nên test cũ báo lỗi khi khởi động app.
- `DataTests.AllReferencedAssetsExist`, `NotesDataTests.Index_EntriesNameTheirBook`, `AppFlowTests.MainScene_ListsIndexLessons`.
