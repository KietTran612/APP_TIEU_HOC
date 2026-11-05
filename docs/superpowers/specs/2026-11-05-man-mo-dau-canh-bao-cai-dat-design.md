# Thiết kế: màn mở đầu, màn cảnh báo và menu Cài đặt

> Ngày 05/11/2026. Bản mẫu đã xem (trang tạm, không nằm trong git): `.superpowers/brainstorm/4100-1793873337/content/splash-thong-bao.html`.
>
> Ký hiệu:
> - **[Chốt]**: chủ dự án đã quyết.
> - **[Đề xuất]**: người viết đề xuất, chủ dự án đã nghe và đồng ý chung.
> - **[Builder]**: để người làm tự quyết.

## 1. Mục đích

App sắp ra bản Android và iOS cho trẻ em. Trước khi bé học, phụ huynh cần đọc các lưu ý của app: app chỉ để tham khảo, nguồn nội dung, hình ảnh, âm thanh, dữ liệu của bé. Như vậy app minh bạch và tránh rủi ro khi phát hành [Chốt].

**Hiện nay:**
- Khi mở app, Unity hiện logo "Made with Unity" trên nền tối, sau đó là một màn giấy trống trong lúc nạp dữ liệu, rồi vào thẳng màn chọn bé.
- App chưa có lời cảnh báo nào, chưa có menu Cài đặt.
- Phụ huynh chưa đổi tên, chưa xoá được hồ sơ bé.

## 2. Đã chốt

1. **Màn mở đầu (splash)** hiện tên app [Chốt]. Tên app chưa chốt, nên tạm dùng tên hiện có (`UiText.AppTitle` = "Tập đọc lớp 1"); đổi tên sau chỉ sửa một chỗ [Chốt].
2. **Màn cảnh báo "Gửi phụ huynh"** hiện ngay sau màn mở đầu, **chỉ một lần** ở lần đầu mở app sau khi cài [Chốt].
3. **Menu Cài đặt** mở bằng **nút bánh răng** ở danh sách bài, bé cũng bấm được [Chốt]. Menu có mục mở lại popup cảnh báo [Chốt].
4. Nội dung của Cài đặt và cách chia việc với màn Phụ huynh theo mục 5.3 [Chốt].
5. Phong cách SGK như các màn khác: giấy ngà, viền mực, bóng gạch chéo, gà con [Chốt, theo bản thiết kế giao diện 30/10].

## 3. Mục tiêu, không làm, điều cấm

**Mục tiêu**
- Phụ huynh đọc đủ các lưu ý trước lần học đầu tiên, và xem lại được bất cứ lúc nào.
- Phụ huynh tự quản lý được dữ liệu của bé: đổi tên, đổi hình, xoá một hồ sơ, xoá toàn bộ.
- Mở app không chậm hơn hiện nay: màn mở đầu chỉ hiện trong lúc app nạp dữ liệu.

**Không làm lúc này** [Chốt, chủ dự án đã ghi chú để sau]
- Trang web chính sách quyền riêng tư và đường link tới nó.
- Các mục khai báo trên Google Play và App Store.
- Thông báo nhắc học gửi lên điện thoại.
- Liên hệ, góp ý qua email.
- Câu "app không có quảng cáo": không viết, vì sau này có thể có quảng cáo.

**Điều cấm**
- Màn cảnh báo che mất màn chọn bé mà không có cách đóng, hoặc hiện lại mỗi lần mở app.
- Bé lỡ tay xoá hồ sơ hay xoá dữ liệu. Mọi thao tác xoá phải qua khoá phụ huynh **và** hỏi xác nhận.
- Chữ tràn hay vùng chạm dưới 160, ở bất kỳ cỡ máy nào trong `ScreenSizes.All` (bản thiết kế tỷ lệ màn hình).
- Nhắc tên cụ thể một bộ sách hay một nhà xuất bản trong lời cảnh báo [Chốt].

## 4. Luồng mở app

1. **Màn mở đầu:**
   - Hiện ngay khi app bắt đầu, trong lúc `AppRoot.BootAsync` nạp bộ chung, danh sách bài và Phụ lục.
   - Nạp xong thì màn mở đầu mờ đi.
   - Hiện tối thiểu khoảng 1 giây để không chớp qua [Đề xuất; con số là Builder]. Thời gian tối thiểu nhân với `Motion.Scale`, nên trong test là 0.
2. **Lần đầu sau khi cài:** màn chọn bé hiện bên dưới, popup cảnh báo hiện đè lên trên. Bấm "Đã hiểu" thì đóng popup và app ghi nhớ đã xem.
3. **Các lần sau:** vào thẳng màn chọn bé, như hiện nay.
4. **Nạp dữ liệu lỗi** (hiện nay chỉ ghi log rồi đứng yên): màn mở đầu ở lại và hiện một dòng báo lỗi ngắn cho người lớn, ví dụ "Không mở được dữ liệu của ứng dụng. Hãy cài lại ứng dụng." [Đề xuất; câu chữ là Builder].
5. **Màn tối "Made with Unity" của Unity:** tắt trong Player Settings [Đề xuất]. Unity 6 cho tắt màn này ở mọi gói giấy phép; người làm kiểm tra lại giấy phép đang dùng trước khi tắt [Builder].

## 5. Các màn

### 5.1 Màn mở đầu
- Nền giấy ngà phủ kín màn.
- Ở giữa: gà con (`img_chung_ga_con`) nhún nhẹ, tên app chữ to, ba chấm chạy chậm bên dưới.
- Không có nút bấm.
- Nằm trên cùng, chặn chạm.
- Vừa mọi cỡ máy: đặt giữa vùng an toàn, dùng khung chuẩn 1440 như màn chuẩn bị.

### 5.2 Popup cảnh báo "Gửi phụ huynh"

**Hình thức:** một khung giấy rộng 1440 ở giữa màn. Nền phía sau phủ kín màn và chặn chạm, như khung Ghi chú.

**Bố cục:** tiêu đề ở trên, nội dung cuộn được ở giữa, một nút người lớn (có chữ) "Đã hiểu" ở dưới, gà con nhỏ đứng ở góc.

**Mở từ menu Cài đặt:** cùng popup đó, nút đổi thành "Đóng". Mở từ đây không làm đổi trạng thái đã xem.

**Không khoá:** bé hay phụ huynh bấm "Đã hiểu" đều đóng được popup; phụ huynh xem lại trong Cài đặt [Chốt].

**Không có giọng đọc** [Đề xuất]: popup dành cho người lớn, nên không phát âm thanh và không có tiếng động khi hiện.

**Nội dung** (bản nháp; chủ dự án sửa câu chữ, người làm đặt trong `UiText` để sửa một chỗ):

> **Gửi phụ huynh**
>
> **Lưu ý về ứng dụng**
> 1. Ứng dụng chỉ mang tính chất tham khảo, hỗ trợ bé tập đọc; không thay thế việc học ở trường và hướng dẫn của thầy cô.
> 2. Ứng dụng tham khảo cách dạy tập đọc từ các sách giáo khoa cũ, không dựa hoàn toàn vào một nguồn sách nào, và không liên kết với nhà xuất bản hay cơ quan quản lý giáo dục nào.
> 3. Ứng dụng không chứa và không cổ xúy bất kỳ hành vi vi phạm pháp luật nào.
> 4. Hình ảnh trong ứng dụng được vẽ để minh họa học tập, không liên quan đến bất kỳ cá nhân, tổ chức nào và có thể không giống thực tế.
> 5. Âm thanh và cách phát âm trong ứng dụng có thể chưa chuẩn. Nếu thấy chưa chuẩn, phụ huynh hãy đọc lại hoặc phát âm lại cho bé.
>
> **Dữ liệu của bé**
> Tên gọi, hình đại diện và tiến độ học của bé chỉ được lưu trên máy này; ứng dụng không gửi các thông tin này đi đâu. Xin chỉ nhập tên gọi ở nhà của bé. Phụ huynh có thể đổi hoặc xoá hồ sơ của bé trong phần Cài đặt.
>
> **Lời khuyên**
> Phụ huynh nên ngồi cùng bé khi học, mỗi lần học ngắn, để âm lượng vừa phải và giữ khoảng cách mắt với màn hình.

Ý 1–4 và ý 5 là của chủ dự án [Chốt]. Đoạn "Dữ liệu của bé" và "Lời khuyên" là [Đề xuất], chủ dự án đã đồng ý chung. **Sao lưu:** Android (Auto Backup) và iOS (iCloud) mặc định tự sao lưu dữ liệu của app. Chủ dự án cho biết app offline, không làm sao lưu [Chốt], nên người làm **tắt sao lưu của hệ điều hành** cho file tiến độ, để câu "chỉ được lưu trên máy này" đúng hoàn toàn. Android: `android:allowBackup="false"` (manifest riêng của dự án). iOS: cờ không sao lưu trên file tiến độ (`UnityEngine.iOS.Device.SetNoBackupFlag`) [Quyết định của người viết; cách làm là Builder]. Hệ quả: đổi sang máy mới thì tiến độ không tự chuyển theo.

**Ghi nhớ đã xem:**
- Lưu cho cả máy, không theo từng bé, trong file tiến độ, cạnh `sfx_off`: số `notice_version` = phiên bản nội dung cảnh báo đã xem, so với một hằng số trong `UiText` [Quyết định của người viết]. Sửa nội dung cảnh báo mà muốn mọi người đọc lại thì tăng hằng số.
- File cũ không có trường này (đọc ra 0) thì coi như **chưa xem**, nên máy đang dùng bản cũ sẽ thấy popup một lần sau khi cập nhật [Đề xuất].
- "Xoá toàn bộ dữ liệu" (mục 5.3) xoá luôn cờ này.

### 5.3 Menu Cài đặt

**Mở ra từ:**
- nút bánh răng ở danh sách bài, đặt ở hàng nút trên cùng cạnh nút Sổ bé ngoan và nút Phụ huynh [Đề xuất; chỗ đặt chính xác là Builder];
- nút bánh răng ở màn chọn bé, cả phần chọn lẫn phần tạo bé [Quyết định của người viết]. Lý do: lúc mới cài, sau "Xoá toàn bộ", hay khi đã đủ 7 hồ sơ, phụ huynh vẫn vào được Cài đặt để đọc lại lưu ý và quản lý hồ sơ. Nút Về của Cài đặt quay lại màn đã mở nó. Cài đặt phải chạy được khi chưa chọn bé nào (`current` trống).
- Biểu tượng mới có mã riêng `img_ui_cai_dat`.
- Làm hình tạm trước, vẽ bằng ChatGPT sau, theo quy trình biểu tượng cũ [Chốt].

**Hình thức:** một màn của bé, cùng kiểu với các màn khác (nằm trong `KidRoot`), có nút Về [Builder: màn riêng hay khung đè lên danh sách bài].

**Nhóm 1: ai cũng dùng được, không khoá**
- **Tiếng động:** công tắc bật/tắt tiếng động.
  - Chuyển từ màn Phụ huynh sang đây; màn Phụ huynh bỏ công tắc này [Chốt].
  - Dùng chung cờ `sfx_off` như hiện nay.
- **Xem lại lưu ý:** mở popup "Gửi phụ huynh" (mục 5.2).
- **Thông tin ứng dụng:**
  - tên app và số phiên bản (lấy từ `Application.version`);
  - ghi công: font Andika (giấy phép SIL Open Font License), tiếng động CC0 của Kenney và OpenGameArt (theo `docs/credits-am-thanh.md`).
  - Chưa nhắc nguồn giọng đọc hay công cụ vẽ tranh [Chốt].

**Nhóm 2: phải mở khoá phụ huynh trước**
- Dùng lại đúng khoá phép tính của màn Phụ huynh (`ParentGate`).
- Mở khoá một lần cho tới khi rời menu Cài đặt.
- **Quản lý hồ sơ bé:** danh sách các bé (hình và tên). Với mỗi bé:
  - **đổi tên gọi**, cùng luật như lúc tạo: tối đa `ProgressStore.MaxNameLength` ký tự, làm sạch bằng `CleanName`;
  - **đổi hình đại diện**;
  - **xoá hồ sơ:** hỏi xác nhận ("Xoá hồ sơ của bé X? Tiến độ của bé sẽ mất."); xoá bé đang học thì `current` về trống.
- **Xoá toàn bộ dữ liệu:**
  - hỏi xác nhận hai lần;
  - xoá mọi hồ sơ, tiến độ, cờ đã xem cảnh báo, và đưa công tắc tiếng động về bật; xoá cả các file phụ của file tiến độ (`.bak`, `.tmp`), vì `.bak` có thể còn tên bé [Quyết định của người viết];
  - sau đó app quay về luồng như lúc mới cài: popup cảnh báo, rồi màn tạo bé.

**Chia việc với màn Phụ huynh** [Chốt]:
- Màn Phụ huynh giữ phần học tập: Phụ lục sách, tiến độ từng bé, "Mở mọi bài", chữ hay nhầm.
- Cài đặt lo phần app: tiếng động, lưu ý, thông tin, dữ liệu.

**Sau khi xoá:**
- Không còn hồ sơ nào thì vào màn tạo bé.
- Còn hồ sơ nhưng bé đang học vừa bị xoá thì vào màn chọn bé.

**Để sau** [Chốt]: chính sách quyền riêng tư, liên hệ, nhắc học. Không làm chỗ trống hay nút mờ cho các mục này.

## 6. Ràng buộc
- Unity 6.6, uGUI dựng bằng code, không prefab, TMP với font Andika.
- Chữ đặt trong `UiText`. Hình đặt theo mã trong `SystemIcons` / `SystemImages` và danh mục Python `SYSTEM_IMAGES`.
- Màn của bé nằm trong `AppRoot.KidRoot`; popup, màn mở đầu và khung người lớn nằm trong khung chuẩn 1440 hoặc phủ kín canvas, theo bản thiết kế tỷ lệ màn hình.
- Vùng chạm ≥ 160, chữ không tràn, mọi thứ trong vùng an toàn, ở cả 9 cỡ máy.
- Hiệu ứng nhân với `Motion.Scale`; tiếng động qua `SfxPlayer`, tách khỏi giọng đọc.
- **Tranh và âm thanh không còn nằm trong git** (từ 02/11): hình mới phải đóng gói bằng `tools/run_unity_media.py pack`, commit `media_lock.json`, rồi báo chủ dự án đưa gói lên Drive. Biểu tượng `img_ui_cai_dat` đi theo quy trình này.
- Không build bản Android/iOS, chỉ commit. Chỉ nhánh `main`; chủ dự án tự push.

## 7. Kiểm tra
- Chỉ chạy test của phần đang làm. Bộ đầy đủ chỉ khi chủ dự án nói "test all".
- Không test nội dung Tập 2 (chưa làm xong).
- **Test cũ:** test cũ khởi động app với file tiến độ mới, nên sẽ thấy popup cảnh báo. Lớp test chung đặt sẵn "đã xem" để test cũ chạy như trước; test của popup thì đặt "chưa xem" [Builder: cách làm].
- **Cần có test cho:**
  - màn mở đầu hiện trong lúc nạp và tắt khi nạp xong;
  - lần đầu hiện popup, bấm "Đã hiểu" thì lần sau không hiện;
  - file cũ không có cờ thì hiện popup;
  - mở lại popup từ Cài đặt không đổi cờ;
  - công tắc tiếng động trong Cài đặt dùng chung cờ với `SfxPlayer`, và màn Phụ huynh không còn công tắc;
  - nhóm có khoá: chưa mở khoá thì không thấy nút đổi, xoá;
  - đổi tên, đổi hình, xoá một bé (bé đang học và bé khác);
  - xoá toàn bộ đưa app về như mới cài;
  - bố cục ở 9 cỡ máy, có ảnh chụp cho chủ dự án (`TestOutput/screens/<cỡ>/`).

## 8. Để người làm quyết [Builder]
- Thời gian tối thiểu của màn mở đầu; cách nối màn mở đầu với màn chuẩn bị đang có (`PrepareCurtain`).
- Menu Cài đặt là màn riêng hay khung đè; bố cục từng hàng.
- Cách đặt cờ "đã xem" trong lớp test chung.
- Câu báo lỗi khi nạp dữ liệu hỏng.
- Có tắt màn "Made with Unity" hay không, sau khi kiểm tra giấy phép.
