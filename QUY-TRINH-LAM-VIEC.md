# Quy trình làm việc chuẩn — app "Bờ A Ba"

Đây là cách làm chung cho mọi session (người hay AI) khi đưa sách vào app: soạn bài, vẽ tranh, làm tranh động, tạo âm thanh, duyệt, đóng gói. Quy trình rút ra từ việc đã làm với Tiếng Việt 1 tập 1, tập 2 và Tiếng Việt 2 tập 1.

Đọc kèm:
- [SETUP-MAY-MOI.md](SETUP-MAY-MOI.md): cài dự án trên máy mới;
- [docs/superpowers/notes/phan-cong-session.md](docs/superpowers/notes/phan-cong-session.md): ai đang làm gì;
- [docs/superpowers/notes/lich-su-cong-viec.md](docs/superpowers/notes/lich-su-cong-viec.md): việc đã xong;
- `content/style/tranh_dong_huong_dan.md`: chi tiết làm tranh động;
- `docs/source-inventory/`: kiểm kê sách nguồn và các loại bài.

Khi quy trình thay đổi (chủ dự án quyết điều mới, hoặc tìm ra cách làm tốt hơn), cập nhật file này trong cùng commit.

---

## 1. Nguyên tắc chung (bắt buộc)

| Mảng | Quy tắc |
|---|---|
| Ngôn ngữ | Mọi trao đổi với chủ dự án, ghi chú, commit đều bằng tiếng Việt |
| Git | - Chỉ dùng branch `main`, không tạo branch hay worktree, không squash, không force push.<br>- Chủ dự án tự push.<br>- `git add` theo đường dẫn cụ thể, không dùng `git add -A`. |
| Commit | - Dạng `loại(phạm vi): mô tả tiếng Việt`, ví dụ `content: …`, `feat(tapdoc): …`, `fix(ui): …`, `docs: …`.<br>- Kết thúc bằng dòng `Co-Authored-By`.<br>- Mỗi việc một commit. |
| Media | - Tranh, âm thanh, clip và file `.meta` của chúng **không vào git**.<br>- Chúng đi trong gói media trên Google Drive (mục 8).<br>- Git chỉ giữ danh mục, nguồn bài, code và `media_lock.json`. |
| Chỉnh sửa duyệt | Working copy của `content/manifests/*.json`, `content/tts/settings.json` và `content/style/tranh_dong_kich_ban.json` có trạng thái và ghi chú chủ dự án vừa duyệt. **Không commit lẫn vào.** Chỉ stage các dòng của mình (mục 10). |
| Ảnh scan | Không bao giờ vào repo hay bản build. Ngoại lệ duy nhất phải được chủ dự án cho phép: dùng `import-image --scan-tam`; nó tự chặn bản phát hành. |
| Nội dung | - Chép đúng như sách in.<br>- Chỗ app làm khác sách thì ghi ghi chú loại `khac_sach`; chú thích in trong sách thì ghi loại `sach`.<br>- Chỗ không chắc thì đánh dấu `can_duyet`. |
| Test | - Claude tự viết và review test.<br>- Chỉ chạy test của phần đang làm.<br>- Chạy toàn bộ chỉ khi chủ dự án nói **"test all"**. |
| Build | Không build Windows hay Android khi chủ dự án chưa yêu cầu. |
| Trình duyệt | - Chỉ dùng Claude in Chrome trên **Edge của máy này** (thiết bị `407cb8a9…`). Không điều khiển thiết bị khác.<br>- Không nhập mật khẩu, không tạo hay đổi tài khoản.<br>- Gặp CAPTCHA hoặc bị đòi xác minh thì dừng và hỏi chủ dự án. |
| Tải file | Hỏi chủ dự án trước lần tải đầu tiên của mỗi loại (tranh, clip, bìa). Chủ dự án đồng ý cho cả loại thì các đợt sau không cần hỏi lại. |
| Tool duyệt | Không đổi giao diện tool duyệt khi chủ dự án đang duyệt, trừ khi được yêu cầu. |

---

## 2. Tổ chức session

- **Root ("Điều phối dự án Bờ A Ba")** điều phối:
  - tạo session, giao việc, kiểm tra kết quả thật (commit, file) rồi mới báo chủ dự án;
  - ghi lịch sử công việc, giữ bảng phân công.
- **Mỗi quyển sách có bộ session riêng**, tên có tiền tố theo lớp (`[L1]`, `[L2]`…):
  - **Nội dung:** soạn bài, build, màn mới trong Unity, âm thanh, đóng gói media;
  - **Vẽ tranh:** ChatGPT;
  - **Tranh động:** Google Flow.
- **Việc chung cho cả app** thuộc session `[Chung]` (UI, hiệu ứng, kỹ thuật nạp dữ liệu).
- **Không giao việc của quyển này cho session của quyển khác.**
- **Thứ tự theo đợt:**
  1. Nội dung soạn bài đợt N và gửi danh sách tranh.
  2. Vẽ tranh nhập xong đợt N thì báo tranh động.
  3. Tranh động làm clip đợt N.
  4. Âm thanh chạy song song.
  5. Đủ hết thì đóng gói media.
  Không làm bước sau khi chưa có đầu vào của bước trước.
- **Session nhắn trực tiếp cho nhau** bằng id ghi trong bảng phân công. Việc lớn, hoặc phần dùng chung giữa các quyển, thì báo root.
- **Code dùng chung** (`tools/tapdoc`, Unity): trước khi sửa xem `git log` của file, sửa nhỏ và commit sớm. Thay đổi lớn thì báo trước cho session cùng dùng phần đó.
- **Mỗi mảng có một ghi chú tiếp tục** `docs/superpowers/notes/<ngày>-tiep-tuc-<mảng>.md`: tình trạng, việc còn lại, cách làm tiếp. Ghi chú này để session mới (hoặc session sau khi rút gọn hội thoại) làm tiếp được.

---

## 3. Đưa một quyển sách mới vào app

1. **Kiểm kê nguồn.**
   - Scan nằm ở `sach-giao-khoa-viet-nam/<tên sách>/`, ngoài git.
   - Ghi thông tin vào `docs/source-inventory/BOOK_CATALOG.md` và `LESSON_INDEX.csv`.
   - Chú ý ảnh trùng hoặc xáo thứ tự trang.
2. **Thiết kế và kế hoạch.**
   - Dùng skill `superpowers:brainstorming` để hỏi chủ dự án:
     - lấy những phân môn nào;
     - đánh số bài: số bài chạy liền cả chương trình, lớp 1 là 1–171, lớp 2 tập một là 172–304;
     - các dạng bước mới.
   - Viết spec ở `docs/superpowers/specs/<ngày>-<tên>-design.md`, rồi plan bằng `superpowers:writing-plans`.
   - **Chủ dự án duyệt rồi mới làm.**
3. **Khai báo quyển** trong `content/books.json`: `book_id`, `title` (tên hiện trong app, hiện là "Bé tập đọc N"), `appendix`, `grade`, `spell` (lớp 2 trở lên là `false`, không sinh đánh vần).
4. **Soạn nguồn bài** trong `content/src/<book>_bNN.json`. Cấu trúc theo file mẫu đã có, ví dụ `tv1_t1_b13.json`:
   - `source.pages`, `source.scan_file`, `verification: page_verified`;
   - `images`: mã tranh kèm mô tả cảnh. Mô tả này là đề bài cho người vẽ, phải đúng với câu chữ trong bài;
   - `part1`: các bước học theo đúng thứ tự trong sách;
   - `part2`: luyện tập, 6–10 lượt;
   - `review.notes`: các ghi chú `can_duyet`, `khac_sach`, `sach`.
   - Đánh vần theo mục Chú ý tr.122 sách Tiếng Việt 1 tập 1. Quy tắc tạm phải ghi rõ "quy tắc tạm" và đánh dấu `can_duyet`.
5. **Dựng bài.** Chạy `cd tools && python -m tapdoc build`. Lệnh này:
   - sinh `unity/TapDoc/Assets/Content/Resources/lessons/*.json` và `index.json`;
   - thêm dòng mới, trạng thái `chua_co`, vào ba danh mục `content/manifests/{audio,image,video}_manifest.json`.
6. **Kiểm tra.**
   - Trong lúc làm: `python -m tapdoc validate --allow-missing`.
   - Khi đủ media: `python -m tapdoc validate`.
   - Trước khi phát hành: `python -m tapdoc validate --release`. Lệnh này đòi bài đã duyệt, media đã duyệt và không còn ảnh tạm từ scan.
7. **Màn hoặc bước mới trong Unity.**
   - Viết test trước. Chạy thử đi hết mọi bước của quyển ở nhiều cỡ máy.
   - Thẻ bấm phải đủ cỡ chạm tối thiểu, chữ không tràn.
   - Không làm thay đổi file bài lớp trước: có test hồi quy so từng byte.

---

## 4. Tranh bài học (ChatGPT)

- **Mã tranh:** `img_b<số bài>_<tiếng không dấu kiểu telex>`, do `tapdoc.ids.telex()` sinh từ nguồn bài, ví dụ `img_b13_cuwr_taj`. Ảnh dùng chung có dạng `img_chung_<tên>`.
- **Danh sách cần vẽ:** session nội dung ghi vào `content/requests/images_<book>_*.md` (thư mục này bị gitignore, chỉ có trên máy).
- **Phong cách** (`content/style/image_style.txt`) dán nguyên văn vào mọi lời nhắc:
  > Tranh minh họa sách giáo khoa Việt Nam năm 1990: nét mực đen viền rõ, tô 2–3 màu phẳng (xanh lam ngọc, cam nhạt), bóng đổ bằng nét gạch, nền trơn màu giấy ngà, không có chữ, không có khung viền; chủ thể ở giữa, chừa khoảng trống; tỉ lệ vuông 1:1; tranh vẽ mới hoàn toàn.
- **Lời nhắc từng tranh:**
  ```
  Tạo một tranh mới (ảnh PNG), cùng phong cách với tranh trước.

  <PHONG CÁCH>
  Vẽ: <mô tả cảnh>
  (Mã tranh: <mã>. Không viết mã này lên tranh.)
  ```
  Tranh đầu tiên của một cuộc trò chuyện thì mở bằng `Tạo một tranh (ảnh PNG).`
  Với kí hiệu (như dấu chấm hỏi, giải nghĩa), viết lời nhắc riêng cho phép có khung và kí hiệu.
- **Nơi vẽ:**
  - Dự án Kiet_1 trên ChatGPT.
  - **Mỗi đợt khoảng 30 tranh thì mở một cuộc trò chuyện mới**, vì trò chuyện quá dài thì trang bị treo.
  - Chỉ gửi tranh kế tiếp khi tranh trước đã vẽ xong. Lúc đang vẽ, nút gửi đổi thành `aria-label="Ngừng"`. Gửi chồng thì ChatGPT bỏ qua tranh.
  - Hết lượt vẽ thì ChatGPT báo "giới hạn" hoặc "hạn mức"; lượt tự mở lại sau khoảng một ngày.
- **Lấy ảnh về:** đọc thẳng dữ liệu cuộc trò chuyện, không cuộn trang.
  1. Lấy accessToken từ `/api/auth/session`. Chỉ giữ trong biến của trang, **không bao giờ in ra**.
  2. Đọc `/backend-api/conversation/<id>`, ghép tin "Mã tranh: X" với các `image_asset_pointer` trong câu trả lời phía sau.
  3. Gọi `/backend-api/files/download/<file_id>?conversation_id=<id>&inline=false`, lấy `download_url`, tải blob rồi lưu `<mã>.png`.
- **Mỗi đợt:**
  1. Tải vào `C:\Users\trant\Downloads\tranh_<book>\`. Kiểm tra trùng tên trước khi tải.
  2. Làm tờ kiểm tra: `powershell -File tools/sheet.ps1 -Dir <thư mục> -Ids <mã…> -Out <file> -Cols 5 -Thumb 300`. Xem **từng tranh** so với mô tả: đúng cảnh, đúng số lượng, không có chữ, không vô lý (ví dụ cá thờn bơn phải có hai mắt cùng một bên). Sai thì vẽ lại.
  3. Hai ảnh cho cùng một mã thì so mã băm; giống nhau thì giữ một.
  4. Nhập: `cd tools && python -m tapdoc import-image <file> <mã>`. Trạng thái chuyển thành `cho_duyet`, nguồn ghi `chatgpt_tam`.
  5. Commit chỉ các dòng tranh của mình trong `image_manifest.json` (mục 10).
  6. Chuyển file đã nhập trong Downloads vào **Thùng rác**.
  7. Nhắn session tranh động danh sách mã vừa nhập (bỏ kí hiệu và ảnh tạm), và báo session nội dung.
- **Vẽ lại theo duyệt:**
  - Sửa mô tả trong `content/src` nếu chủ dự án đổi ý (ví dụ tranh cử tạ thành người lớn).
  - Nhập tranh mới rồi ghi chú: `Đã vẽ lại <ngày> … Lần trước: <ghi chú cũ>`.
  - Báo session tranh động làm lại clip theo tranh mới.

---

## 5. Tranh động (Google Flow)

Chi tiết đầy đủ ở `content/style/tranh_dong_huong_dan.md`: tài khoản, thông số, cách tải, các lỗi đã gặp. Những điểm chính:

- Chỉ làm clip khi tranh đã nhập. **Không làm clip** cho kí hiệu và ảnh tạm cắt từ scan.
- Thông số: Veo 3.1 Lite, chế độ Khung hình, 16:9, 720p, 8 giây, có tiếng, 10 credit mỗi clip. Tranh vuông được đệm thành 1280×720; vào app thì cắt lại hình vuông.
- **Mỗi tranh một kịch bản sáng tạo** trong `content/style/tranh_dong_kich_ban.json`:
  - chuyển động có ý nghĩa, đúng nội dung tranh, có âm thanh hợp lý (ví dụ con dê phải kêu đúng tiếng dê);
  - chủ dự án duyệt clip chứ không duyệt kịch bản.
- **Những gì chủ dự án đã chê, phải tránh:**
  - chuyển động nhạt, chỉ lắc nhẹ;
  - sai đời thực: em bé lái ô tô, hoa đã nở rồi quay về nụ, hoa mọc trên lá;
  - không làm đúng việc trong tranh: bé kẻ vở thì phải thật sự dùng thước.
- **Tài khoản:**
  - Chỉ chuyển giữa các tài khoản đã đăng nhập sẵn. Không dùng `/u/0`, vì đó là tài khoản công ty, có hình mờ.
  - Tài khoản bị báo "unusual activity" thì dùng sau cùng và đi chậm. Bị đòi xác minh thì dừng, hỏi chủ dự án.
- **Đưa vào app:**
  1. Hỏi chủ dự án trước khi tải.
  2. Đặt tên `<mã tranh>.mp4`, chạy `python -m tapdoc import-clips <thư mục>`. Clip nằm ở `content/clips/`.
  3. Thêm dòng `cho_duyet` vào `video_manifest.json`, commit chỉ các dòng mới và kịch bản mới.
- **Làm lại theo duyệt:** trạng thái về `cho_duyet`, ghi chú `Đã tạo lại <ngày> (…). Lần trước: <ghi chú cũ>`.

---

## 6. Âm thanh (edge-tts, giọng HoaiMy)

- **Giọng:** `vi-VN-HoaiMyNeural`, nữ miền Nam, chủ dự án đã chọn. Không đổi giọng khi chưa được phép.
- **Loại mã:** `am`, `van`, `dau`, `tieng`, `tu`, `cau`, `huong_dan`, `khen`, cùng các mã cách đọc `ghiam_`, `tenchu_`. Thông số mặc định theo loại và chỉnh riêng từng mã nằm trong `content/tts/settings.json` (`defaults`, `overrides`).
- **Tạo:** `cd tools && python -m tapdoc tts [--bai …] [--loai …] [--ma …] [--tieng-keep-first] [--thu]`.
  - **Chỉ chạy 1 tiến trình.** Chạy nhiều tiến trình thì dịch vụ treo hoặc trả rỗng nhiều hơn.
  - Mỗi mã tối đa 90 giây. Dịch vụ hay trả rỗng ("No audio was received"), nên sau mỗi lượt phải chạy **lượt bù** cho các mã lỗi.
  - Không tạo lại mã đã `dat`, trừ khi chủ dự án cho phép (`--gom-da-duyet`).
- **Điểm yếu của HoaiMy và cách sửa đã được chủ dự án xác nhận:**

  | Lỗi | Cách sửa |
  |---|---|
  | Tiếng lẻ thanh hỏi, ngã bị đọc thành thanh huyền | Đọc "X, X." rồi chỉ giữ tiếng đầu (`keep_first`, cờ `--tieng-keep-first`). Vẫn sai thì đọc 3 lần "X, X, X.". Áp cho mọi tiếng lẻ mới ngay từ đầu |
  | Tiếng lẻ thanh nặng, âm ê | Máy chưa đo được lỗi. Tạo nhiều bản, để chủ dự án chọn bằng tai trên trang nghe thử (`.superpowers/nghe-thu/`), rồi áp cách thắng cho cả nhóm |
  | Hỏi, ngã nằm trong từ hoặc câu | Theo thứ tự ở dưới |

- **Thứ tự sửa từ và câu** (chủ dự án quyết 09/11: **đọc đúng là trên hết**):
  1. Đọc nguyên câu, nếu đo thấy đúng thanh. Cách này giữ ngữ điệu tự nhiên nhất.
  2. Đọc chậm hơn, khoảng −20%, hoặc ngắt nhẹ; không đổi chữ.
  3. Ghép từ các tiếng đã `dat` hoặc đã đo đúng, bằng `overrides[mã].join`:
     - khoảng nghỉ ngắn và đều, khoảng 0,05–0,12 giây;
     - ngắt nhẹ ở dấu phẩy;
     - âm lượng đều nhau;
     - ghi chú rõ ghép từ mã nào.
- **Đo trước khi thay:** `python -m tapdoc pitch --ma …|--bai …` đo cao độ thanh hỏi, ngã, so với các tiếng đã `dat`. Mốc từng tiếng lưu ở `content/tts/marks/`.
  - Tiếng ở cuối cụm thì đo tin được.
  - Tiếng ở giữa cụm thì tiêu chí yếu hơn; còn nghi thì để chủ dự án nghe.
- **Mỗi lần thay:**
  - bản cũ lưu trong `content/tts/prev/` để nghe so trong tool;
  - trạng thái về `cho_duyet`;
  - ghi chú thêm cách đã làm, giữ ghi chú cũ;
  - mã `dat` bị nghi sai thì chỉ báo lại, không tự thay.

---

## 7. Duyệt

- **Mở tool:** chạy `MoCongCuDuyet.cmd`, hoặc `cd tools && python -m tapdoc mo` (cổng 8765).
  - Tab **Duyệt theo bài**: âm thanh, tranh, clip theo thứ tự bé gặp trong bài, có trang sách gốc đặt cạnh.
  - Các tab Âm thanh, Tranh, Tranh động và **Nghe theo bài**.
  - Ô **Sách** lọc theo quyển. Mã dùng chung nhiều quyển hiện ở cả hai.
- **Trạng thái:**
  - `chua_co`: chưa có file;
  - `cho_duyet`: đã có, chờ nghe hoặc xem;
  - `dat`: đạt;
  - `khong_dat`: kèm ghi chú lý do.
- **Sau mỗi lần chủ dự án duyệt**, root:
  1. gom các mục `khong_dat` và ghi chú trong ba danh mục;
  2. chia theo mảng: âm thanh cho session đang giữ công cụ giọng đọc, tranh cho session vẽ của quyển đó, clip cho session tranh động của quyển đó;
  3. giao sửa kèm nguyên văn ghi chú của chủ dự án;
  4. trả lời luôn những câu chủ dự án hỏi trong ghi chú (ví dụ "từ này có trong bài không?");
  5. sửa xong thì kiểm tra lại rồi báo chủ dự án.

---

## 8. Đóng gói media và máy mới

- **Đóng gói** một lần khi quyển đã đủ tranh, âm thanh và clip:
  1. Đóng Unity Editor.
  2. Chạy `python tools/run_unity_media.py pack`. Lệnh xuất `dist/TapDoc-media-<ngày>.unitypackage` (tranh, âm thanh, kèm `.meta`) và `dist/TapDoc-clips-<ngày>.zip`.
  3. Commit `content/manifests/media_lock.json`.
  4. Báo chủ dự án tên và dung lượng hai file để chủ dự án **tự tải lên Drive**.
- **Hình mới khác** (bìa, biểu tượng): nhập vào app và đóng gói chung đợt với quyển đang làm.
- **Máy mới:** làm theo [SETUP-MAY-MOI.md](SETUP-MAY-MOI.md), dùng `run_unity_media.py unpack`. `validate` sẽ cảnh báo khi media trên máy khác với gói.

---

## 9. Test

- **Python:** `cd tools && python -m unittest tests.<module>`, chỉ các module liên quan.
- **Unity:**
  - Đóng Editor trước.
  - Chạy `cd tools && python run_unity_tests.py editmode|playmode --filter <Lớp test>`.
  - Kết quả và ảnh chụp nằm ở `unity/TapDoc/TestOutput/`.
- **Test bố cục** chạy nhiều cỡ máy (điện thoại, iPad). Xem ảnh chụp ở `TestOutput/screens/<cỡ>/` khi đổi giao diện.
- **Toàn bộ test** chỉ chạy khi chủ dự án nói "test all".
- **Test lỗi do phần khác hoặc do media chưa đủ:** ghi rõ trong báo cáo, không sửa lấn sang phần của session khác.

---

## 10. Commit dòng danh mục mà không lẫn chỉnh sửa duyệt

Danh mục trong working copy có cả chỉnh sửa duyệt của chủ dự án. Để chỉ commit dòng của mình:

1. Đọc bản HEAD: `git show HEAD:content/manifests/<x>_manifest.json`.
2. Thay hoặc thêm đúng các dòng của mình, lấy từ working copy. Ghi ra file tạm bằng `tapdoc.manifest.save_rows`, để giữ đúng định dạng.
3. Chạy `git hash-object -w <file tạm>`, rồi `git update-index --cacheinfo 100644,<blob>,content/manifests/<x>_manifest.json`.
4. Xem lại `git diff --cached`: chỉ có các dòng của mình. Rồi commit.

---

## 11. Danh sách kiểm tra mỗi đợt

- [ ] Nội dung: nguồn `page_verified`, `build`, `validate --allow-missing`, test liên quan, commit, gửi danh sách tranh.
- [ ] Tranh: vẽ, tải, tờ kiểm tra, xem từng tranh, `import-image`, commit dòng, dọn Downloads, báo tranh động.
- [ ] Tranh động: kịch bản, Flow, hỏi rồi mới tải, `import-clips`, dòng `video_manifest`, commit, báo.
- [ ] Âm thanh: `tts` 1 tiến trình, lượt bù, `keep_first` cho tiếng lẻ, đo `pitch`, sửa theo thứ tự, ghi chú.
- [ ] Đủ quyển: `validate`, đóng gói media, commit `media_lock.json`, báo chủ dự án tải lên Drive.
- [ ] Ghi chú tiếp tục, bảng phân công, lịch sử công việc đã cập nhật.

---

## 12. Vấn đề khó đã gặp và cách giải

Gặp vấn đề mới mà đã tìm ra cách giải (nhất là cách được chủ dự án xác nhận) thì ghi thêm vào bảng này, kèm ngày và commit nếu có.

### Âm thanh

| Vấn đề | Cách giải | Ngày / commit |
|---|---|---|
| Tiếng lẻ thanh hỏi, ngã bị HoaiMy đọc thành thanh huyền; chỉnh pitch hay tốc độ không sửa được | Đọc lặp "X, X." rồi cắt giữ tiếng đầu (`keep_first`). Một số tiếng cứng đầu (rỡ, xã, nở) phải đọc 3 lần "X, X, X.". Chủ dự án nghe xác nhận 18/18 đạt | 09/11, 1b3623c, 9a1171f |
| Không cắt được tiếng cuối hay tiếng giữa của một lần đọc | Khung MP3 của dịch vụ mượn dữ liệu của khung trước, nên chỉ cắt được phần sau. Luôn đặt tiếng cần lấy ở đầu | 09/11 |
| Cắt khoảng lặng đầu file làm hỏng tiếng đầu | Cắt ở khung không mượn dữ liệu (bit reservoir); tạo lại các file đã bị cắt hỏng | 30/10, e9f1f90, 269ebde |
| Tiếng trong câu hoặc từ đọc sai thanh | Theo thứ tự: đọc nguyên câu nếu đúng, rồi đọc chậm −20% hay ngắt nhẹ, rồi ghép từ các tiếng đã đạt (`join`). Chủ dự án chấp nhận câu ghép: đọc đúng là trên hết, ngữ điệu tự nhiên càng tốt | 09/11, 929d023 |
| Thêm dấu phẩy vào câu để sửa thanh thì lại làm câu nghe sai ("bé bá cổ, bà.") | Với cụm, không đổi chữ; dùng cách đọc chậm hoặc ghép | 09/11 |
| Máy không đo được lỗi nguyên âm (ê) và thanh nặng; đo formant chỉ đúng khoảng 85%, Whisper hay tự sửa thành đúng chữ | Tạo 4–6 bản cho mỗi mã, đặt lên một trang HTML nghe thử riêng để chủ dự án chọn bằng tai; áp cách thắng cho cả nhóm | 09/11, `.superpowers/nghe-thu/` |
| Đo cao độ cho tiếng ở giữa cụm không tin được | Hiệu chỉnh ngưỡng trên các mã đã `dat`. Tiếng cuối cụm thì tách rõ (đạt khi lên ≥ 7 bán âm, sai khi ≤ 1); tiếng giữa cụm chỉ coi là "có thể sai" và để tai người nghe | 09/11 |
| edge-tts trả rỗng ngẫu nhiên; chạy 4 tiến trình thì treo hàng giờ | Chỉ 1 tiến trình, mỗi mã tối đa 90 giây, nghỉ vài giây giữa các mã, rồi chạy lượt bù. Kiểm tra định kỳ xem file mp3 mới còn được ghi không | 05–06/11 |
| `tts --tieng-keep-first` báo "Đã tạo 0" với tiếng đã có file | Ghi cách đọc trước rồi mới chọn mã cần tạo | 09/11, 9678b22 |

### Tranh (ChatGPT)

| Vấn đề | Cách giải | Ngày / commit |
|---|---|---|
| Trang trò chuyện dài bị treo, ảnh không hiện, cuộn trang lấy ảnh không được | Đọc thẳng dữ liệu cuộc trò chuyện qua `/backend-api/conversation/<id>` và tải ảnh qua `/backend-api/files/download/…` (mục 4). Mỗi đợt khoảng 30 tranh thì mở một cuộc trò chuyện mới | 06/11 |
| Gửi lời nhắc kế tiếp khi tranh trước chưa vẽ xong làm ChatGPT bỏ qua tranh | Chờ hết trạng thái "Ngừng" mới gửi tiếp; tranh bị bỏ qua thì vẽ lại riêng | 06/11 |
| Một mã có hai ảnh | So mã băm; giống nhau thì giữ một, khác thì xem cả hai rồi chọn | 06/11 |
| Tranh vô lý (cá thờn bơn hai mắt hai bên, trẻ con giơ tạ) | Xem từng tranh trên tờ kiểm tra; sửa mô tả cho rõ rồi vẽ lại | 30/10, f9f0203; 09/11, 7f13b2a |
| Tranh bản đồ chưa vẽ lại được | Chủ dự án cho dùng tạm ảnh cắt từ scan (`import-image --scan-tam`), bản phát hành tự bị chặn | 05/11, c31e355 |
| Tải về bị trùng tên "(1)" | Kiểm tra trùng tên trong Downloads trước khi tải; nhập xong thì chuyển file vào Thùng rác | 05/11 |
| Lệnh JS tải cả đợt (khoảng 18 ảnh) chạy quá 45 giây, công cụ trình duyệt báo hết giờ; trang vẫn tải tiếp nhưng không trả kết quả | Gọi hàm tải mà không `await`; hàm ghi kết quả vào `window.__dlres`, đọc lại sau ít giây. Đếm file trong Downloads để xác nhận đủ | 09/11 |
| Một lô chờ trình duyệt dài quá khoảng 2 phút thì mất kết nối | Mỗi lô chờ tối đa khoảng 110 giây, rồi đọc tiến độ trong `window.__prog`. Mất kết nối thì chỉ đọc lại trạng thái một lần, không gửi lại thao tác | 09/11 |

### Tranh động (Flow)

| Vấn đề | Cách giải | Ngày / commit |
|---|---|---|
| Tải nhanh liên tiếp bị rơi file | Bắt `URL.createObjectURL` để giữ khối dữ liệu Flow đã nạp, rồi tự lưu ra máy | 30/10 |
| Flow chặn `eval` hay `new Function`, vòng lặp dừng mà không báo | Dùng hàm viết sẵn, không tạo hàm từ chuỗi | 30/10 |
| Khung cuối của lần trước còn sót làm sai clip, mất credit | Trước khi gửi, kiểm tra ô soạn có đúng 2 ảnh và đúng mã tranh | 30/10 |
| Hết credit; tài khoản bị báo "unusual activity" | Chia việc theo ngày (khoảng 5 clip mỗi tài khoản mỗi ngày). Tài khoản bị cảnh báo thì dùng sau cùng, đi chậm; bị đòi xác minh thì dừng, hỏi chủ dự án | 09/11 |
| Clip vô lý (hoa nở rồi quay về nụ, em bé lái ô tô) | Viết kịch bản theo đúng logic đời thực, một chiều thời gian; xem lại clip trước khi nhập | 09/11 |
| Thẻ clip báo "unusual activity" ngay sau khi gửi (3 clip liền trên `/u/3`) | Không gửi lại bằng mã. Bấm nút làm lại (Retry) trên từng thẻ bằng cú nhấp thật, mỗi lần cách nhau vài chục giây; cả 3 đều chạy được, credit lần hỏng được hoàn. Các tài khoản sau gửi cách nhau 12 giây thì không bị lại | 09/11, a0662f8 |
| Sửa ảnh "điểm bắt đầu" trong trang chi tiết ảnh làm bản sửa đè lên tên tranh gốc, mất khung cuối | Tải thêm tranh gốc với tên `<mã>_cuoi.png` để làm khung cuối; khung đầu chọn theo `<mã>.png` (giờ là bản sửa) | 09/11, 28fe7be, a0662f8 |
| Lệnh sửa ảnh gõ vào ô nhập không ăn (ô nhập đổi vị trí theo cỡ cửa sổ), ảnh vẫn là bản gốc | Nhập bằng `document.execCommand('insertText')` vào ô nhập rồi bấm phím Enter thật; kiểm tra lại: ảnh sửa của Nano Banana rộng 1376 px, ảnh gốc 1280 px | 09/11 |
| Ảnh "điểm bắt đầu" bị Nano Banana vẽ tràn cả khung 16:9, mất lề giấy hai bên | Sửa thêm một lần: "đưa cả cảnh vào ô vuông giữa khung, lề giấy trống hai bên như tranh gốc". Clip vẫn có thể lan ra ngoài ô vuông giữa chừng, nên nhắc chủ dự án xem kỹ | 09/11 |
| Tải nhiều ảnh lên một lần (khoảng 9 MB trở lên) làm rớt kết nối Claude in Chrome | Bắt ô chọn file bằng cách ghi đè `HTMLInputElement.prototype.click` khi bấm nút tải lên, rồi `file_upload` mỗi lần 3 ảnh. Khi công cụ báo lỗi, kiểm tra danh sách thành phần trước khi tải lại: ảnh thường vẫn lên | 09/11 |
| Trang chi tiết clip ở `/u/1`–`/u/4` không có nút mũi tên sang clip kế | Lọc lưới theo Video, mở từng thẻ theo thứ tự, xong thì quay về lưới | 09/11 |
| Ô soạn có thêm biểu tượng nhỏ (ảnh `gstatic`), làm bộ đếm "đúng 2 ảnh" sai | Khi đếm ảnh trong ô soạn, bỏ ảnh có `src` thuộc `gstatic.com` | 09/11 |
| Trình phát clip của Flow là canvas, không lấy được thẻ `video` để xem | Bấm phát rồi `drawImage` từ canvas theo thời gian để chụp khung; khung đen là do chưa nạp kịp. Chắc nhất là tải về rồi phát thật qua `python -m http.server` cục bộ | 09/11 |

### Dữ liệu, git, điều phối

| Vấn đề | Cách giải | Ngày / commit |
|---|---|---|
| Commit lẫn chỉnh sửa duyệt của chủ dự án | Chỉ stage dòng của mình bằng `hash-object` và `update-index` (mục 10) | 05/11 |
| Hai session cùng sửa `tools/tapdoc` | Xem `git log` file trước khi sửa, sửa nhỏ, commit sớm, báo nhau trước khi thay đổi lớn | 09/11 |
| `tapdoc build` tự thêm mã bài vào trường `bai` của danh mục | Kiểm tra đó là dữ liệu đúng rồi commit riêng các dòng đó | 09/11, 98880eb |
| `tapdoc requests` xoá luôn các file tổng hợp `content/requests/images_<book>_dot_N.md` | Chạy `requests` trước, rồi mới ghi file danh sách tranh từng đợt; hoặc sinh lại file đợt sau khi chạy | 09/11 |
| `validate` báo câu nhiễu nghe gần giống đáp án theo giọng miền Nam (trao/chao, lặng/lặn) | Đổi sang từ nhiễu khác hẳn âm; không tắt kiểm tra | 09/11 |
| Bài lớp 2 câu dài: thẻ, dòng câu hỏi, tên bài tràn chữ trên máy nhỏ | Test đi hết mọi bước ở 1600×720 và 1440×1080 và test mọi thẻ không tràn; màn có nhiều dòng thì chia trang; tên bài trên thẻ rút gọn (ví dụ "Quan sát tranh: …"), bước tên bài trong bài giữ đủ như sách | 09/11, 761444a |
| Session con biến mất khỏi thanh bên | Không ghim session root: mục "Đã ghim" đang thu gọn sẽ giấu luôn mọi session con | 09/11 |
| Thanh bên không chia nhóm được session con | Dùng tiền tố tên `[L1]`, `[L2]`, `[Chung]` | 09/11 |
