# Cài đặt dự án trên máy mới (dành cho AI đọc và làm theo)

File này dành cho trợ lý AI (Claude Code hoặc tương tự) khi chủ dự án chuyển sang máy mới. Làm lần lượt từng bước. Mỗi bước có lệnh kiểm tra; chỉ sang bước sau khi kết quả đúng như ghi. Gặp bước cần chủ dự án (đăng nhập, chép file từ máy cũ, cài phần mềm có giấy phép) thì dừng lại và hỏi.

Dự án: app **"Tập đọc lớp 1"** theo SGK Tiếng Việt 1 tập 1 (1990), làm bằng Unity, kèm bộ công cụ Python để dựng bài, tạo giọng đọc và duyệt âm thanh, tranh.

---

## 1. Phần mềm cần có

| Phần mềm | Phiên bản đang dùng | Ghi chú |
|---|---|---|
| Windows | 11 | Các lệnh và file `.cmd` viết cho Windows |
| Git | 2.55 | |
| Python | 3.14 | Cài bản python.org, có trong PATH (bản giả của Microsoft Store không chạy được) |
| Unity Hub + Unity Editor | **6000.6.5f1** | Cài đúng chỗ mặc định `C:\Program Files\Unity\Hub\Editor\6000.6.5f1\`: `tools/run_unity_tests.py` và `run_unity_build.py` gọi đúng đường dẫn này |
| Node.js | 24 | Cho hook `rule-keeper` trong `.agents/` và bộ giao việc cho Codex/Antigravity (tùy chọn) |
| Microsoft Edge | mới nhất | Trình duyệt duy nhất được dùng (xem mục 8) |

Kiểm tra:

```bash
git --version
python --version
node --version
ls "/c/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe"
```

Phần mềm nào thiếu thì báo chủ dự án cài. Unity cần đăng nhập tài khoản Unity: AI không tự đăng nhập.

## 2. Lấy mã nguồn

Nên đặt đúng đường dẫn cũ, để ghi nhớ của Claude và các đường dẫn trong ghi chú vẫn khớp:

```bash
git clone https://github.com/KietTran612/APP_TIEU_HOC.git /c/Source/AURA/APP_TIEU_HOC
cd /c/Source/AURA/APP_TIEU_HOC
git log --oneline -3
```

Chỉ dùng branch `main`.

## 3. Ảnh scan sách (tài liệu tham chiếu, không bao giờ vào repo)

Ảnh scan SGK nằm trong thư mục `sach-giao-khoa-viet-nam/`. Thư mục này đã có trong `.gitignore`, phải lấy riêng:

```bash
cd /c/Source/AURA/APP_TIEU_HOC
git clone https://github.com/giangtv134/sach-giao-khoa-viet-nam.git sach-giao-khoa-viet-nam
ls "sach-giao-khoa-viet-nam/Tiếng Việt 1 (tập 1 1990)" | head -3
```

Quy tắc: ảnh scan chỉ để đọc đối chiếu. Không chép vào repo, không đưa vào app, không gửi lên dịch vụ nào.

## 4. Gói media: tranh, âm thanh, clip tranh động (không nằm trong git)

Tranh (`Resources/images`) và âm thanh (`Resources/audio`) của bài học, **cùng file `.meta` của chúng**, không nằm trong git để repo không phình. Chúng nằm trong gói trên Google Drive của dự án: https://drive.google.com/drive/u/1/folders/1cw5FYmXGkWIwQRS3-BNPbvGfbJzrmT3m

| File trên Drive | Nội dung |
|---|---|
| `TapDoc-media-<ngày>.unitypackage` (~520 MB) | 213 tranh + 1.926 âm thanh, kèm `.meta` (GUID giữ nguyên) |
| `TapDoc-clips-<ngày>.zip` (~510 MB) | Clip tranh động, giải nén vào `content/clips/` |

Dùng **bản có ngày trùng với tên gói ghi trong `content/manifests/media_lock.json`** (khoá media trong git ghi tên gói và mã kiểm tra từng file).

1. Nhờ chủ dự án tải hai file trên về thư mục `dist/` ở gốc repo (AI không tự đăng nhập Google).
2. Đóng Unity Editor rồi nhập gói (Unity chạy nền, giữ đúng `.meta` và GUID):

```bash
cd /c/Source/AURA/APP_TIEU_HOC/tools
python run_unity_media.py unpack ../dist/TapDoc-media-<ngày>.unitypackage --clips ../dist/TapDoc-clips-<ngày>.zip
```

   Hoặc làm tay: mở project trong Unity, chọn **Assets → Import Package → Custom Package…**, chọn file `.unitypackage`, bấm Import tất cả; rồi giải nén file zip vào `content/clips/`.
3. Kết quả đúng: lệnh in "Đã nhập gói media." (không có dòng "Cảnh báo: media…"); có 213 file `.png` trong `Resources/images` và 1.926 file `.mp3` trong `Resources/audio`.

**Khi sửa media** (duyệt hay tạo lại âm thanh, vẽ lại tranh, thêm clip): đóng Unity, chạy `python run_unity_media.py pack` (trong `tools/`). Lệnh xuất gói mới có ngày vào `dist/` và ghi lại `media_lock.json`. Sau đó commit `media_lock.json`, rồi nhờ chủ dự án kéo thả hai file mới vào thư mục Drive. Lệnh `python -m tapdoc validate` sẽ cảnh báo khi media trên máy khác gói đã ghi.

## 5. Bộ công cụ Python

Làm sau mục 4: một số test và lệnh `validate` đọc tranh, âm thanh trong `Resources`.

```bash
cd /c/Source/AURA/APP_TIEU_HOC/tools
python -m pip install -r requirements-tts.txt
PYTHONIOENCODING=utf-8 python -m unittest discover -s tests -t .
```

Kết quả đúng: khoảng 700 test, dòng cuối `OK`. Trên Windows nhớ đặt `PYTHONIOENCODING=utf-8` (hoặc `PYTHONUTF8=1`), nếu không, chữ tiếng Việt in ra sẽ lỗi.

Các lệnh hay dùng (chạy trong `tools/`):

- `python -m tapdoc build`: dựng bài từ `content/src/` ra `unity/TapDoc/Assets/Content/Resources/lessons/` và cập nhật danh mục.
- `python -m tapdoc validate`: kiểm tra dữ liệu; phải ra `OK`.
- `python -m tapdoc requests`: tạo lại lời yêu cầu vẽ tranh trong `content/requests/` (thư mục này không có trong git).
- `python -m tapdoc tts --ma <mã>`: tạo giọng đọc edge-tts (cần mạng). Thêm `--thu` để chỉ liệt kê mã sẽ tạo.

## 6. Unity

1. Mở Unity Hub, chọn **Add project from disk**, chọn `C:\Source\AURA\APP_TIEU_HOC\unity\TapDoc`.
2. Lần mở đầu tiên Unity nhập toàn bộ tài nguyên (khoảng 2.000 file âm thanh, hơn 200 tranh từ gói media ở mục 4), mất khá lâu. TextMesh Pro và scene `Assets/Scenes/Main.unity` đã có sẵn trong git.
3. Đóng Unity Editor trước khi chạy test bằng dòng lệnh (Unity không cho hai tiến trình mở cùng một project).

Kiểm tra bằng một nhóm test nhỏ:

```bash
cd /c/Source/AURA/APP_TIEU_HOC
python tools/run_unity_tests.py editmode --filter "TapDoc.Tests.DataTests"
```

Kết quả đúng: `EditMode: N passed, 0 failed`. Nếu test báo "Thiếu âm thanh" mà file vẫn có, xem mục "Âm tô" trong ghi chú tiếp tục (tạo lại riêng mã đó).

Chỉ khi scene hay TextMesh Pro bị thiếu mới chạy thiết lập: `Unity.exe -batchmode -projectPath unity/TapDoc -executeMethod TapDoc.EditorTools.ProjectSetup.Run` (không kèm `-quit`).

## 7. File chỉ có trên máy cũ (không có trong git, không có trong gói media)

Các thứ dưới đây phải **chép từ máy cũ** (hỏi chủ dự án cách chép: ổ USB, ổ mạng…). Thiếu thì app vẫn chạy, nhưng mất phần việc tương ứng.

| Đường dẫn | Dung lượng | Dùng để | Thiếu thì sao |
|---|---|---|---|
| `content/tts/prev/` | ~11 MB | Bản âm thanh trước của các mã đã chỉnh, để nút "dùng lại bản trước" trong công cụ duyệt | Không quay lại được bản cũ |
| `.superpowers/scripts/` | nhỏ | `chatgpt_tranh.js` (dán, thu, tải tranh ChatGPT), `sheet.ps1` (bảng xem nhanh tranh) và kịch bản dựng trang sách | Phải viết lại khi cần vẽ tranh |
| `C:\Users\<tên máy>\.claude\projects\C--Source-AURA-APP-TIEU-HOC\memory\` | nhỏ | Ghi nhớ của Claude về dự án | Mất các ghi nhớ; quy tắc chính đã chép ở mục 8 |
| `C:\Users\<tên máy>\.claude\delegate\` | nhỏ | Bộ giao việc cho Codex/Antigravity (`delegate.mjs`) | Không giao việc cho worker được; Claude tự làm |

Thư mục ghi nhớ của Claude đặt tên theo đường dẫn dự án: clone đúng `C:\Source\AURA\APP_TIEU_HOC` thì tên thư mục giữ nguyên `C--Source-AURA-APP-TIEU-HOC`.

## 8. Quy tắc làm việc chủ dự án đã chốt (bắt buộc)

Ghi nhớ của Claude không tự đi theo sang máy mới, nên các quy tắc được chép lại ở đây:

- **Ngôn ngữ:** mọi tin nhắn cho chủ dự án viết bằng tiếng Việt.
- **Git:** chỉ dùng branch `main`, không tạo branch khác. Giữ nguyên lịch sử: không squash, không force push. **Chủ dự án tự push**; AI chỉ commit khi được bảo hoặc khi xong một việc rõ ràng, mỗi việc một commit, `git add` từng đường dẫn (không `git add -A`). Thay đổi chủ dự án đang làm dở (ví dụ đang duyệt âm thanh) thì không commit lẫn vào.
- **Media:** tranh và âm thanh trong `Resources/images`, `Resources/audio` (cùng `.meta`) không commit vào git. Sửa media xong thì đóng gói lại (mục 4), commit `media_lock.json`, nhờ chủ dự án đưa gói mới lên Drive.
- **Test:**
  - Claude viết và review mọi test; Codex/Antigravity chỉ viết code cho test của Claude chạy xanh.
  - **Chỉ chạy unit test của phần vừa sửa** (Python, EditMode, hoặc PlayMode có `--filter` đúng lớp test đó). Không chạy test đi hết bài (`MvpEndToEndTests`) hay toàn bộ PlayMode khi chủ dự án chưa nói **"test all"**.
- **Code:** review kỹ, tránh code rác và hard-code. Phần giao diện, hiệu ứng thì Claude tự làm, không giao cho worker. Tiếng động tách riêng khỏi âm thanh phát âm.
- **Trình duyệt:** chỉ dùng Edge trên chính máy này. Trên máy mới, mã thiết bị Claude in Chrome sẽ khác mã cũ: kiểm tra bằng `list_connected_browsers` (phải là trình duyệt của máy này) và hỏi chủ dự án xác nhận trước lần dùng đầu. Không bao giờ điều khiển trình duyệt của máy khác.
- **Tải file:** hỏi trước mỗi lô tải về (nói rõ tên, nguồn, dung lượng).
- **Tài khoản:** không nhập mật khẩu, không tạo tài khoản. Trang đăng nhập (ChatGPT, Google Flow, Unity) để chủ dự án tự làm.
- **Không làm bản build** Windows/Android; chỉ commit.
- **Trợ lý phụ (subagent):** tối đa một. Việc trên trình duyệt (ChatGPT, Google Flow) luôn do Claude chính làm.
- **Tranh bài học** vẽ bằng ChatGPT (dự án ChatGPT "Kiet_1"), theo phong cách tranh SGK 1990 trong `content/style/image_style.txt`. **Tranh động** làm bằng Google Flow, theo `content/style/tranh_dong_huong_dan.md`.
- **Giọng đọc:** edge-tts giọng HoaiMy (nữ) mặc định; chủ dự án duyệt bằng công cụ duyệt.

## 9. Đọc gì để biết dự án đang tới đâu

Đọc theo thứ tự:

1. `docs/superpowers/notes/2026-10-29-tiep-tuc-tv1-tap-1.md`: trạng thái nội dung 80 bài, âm thanh, tranh, việc còn chờ.
2. `docs/superpowers/notes/2026-10-30-tiep-tuc-ui.md`: trạng thái giao diện, hiệu ứng, Sổ bé ngoan.
3. Bản thiết kế: `docs/superpowers/specs/2026-10-28-app-tap-doc-mvp-design.md` (app, giọng đọc ở mục 17) và `docs/superpowers/specs/2026-10-30-ui-hieu-ung-design.md` (giao diện).
4. `git status` và `git log origin/main..main`: thay đổi chưa commit và commit chưa push.

## 10. Công cụ duyệt cho chủ dự án

Bấm đúp `MoCongCuDuyet.cmd` ở thư mục gốc: file tự tìm Python và mở trang duyệt trên trình duyệt. Trang có các tab "Âm thanh", "Tranh", "Tranh động" (cần `content/clips/` từ gói ở mục 4) và "Nghe theo bài".

## 11. Kiểm tra cuối

Coi như cài xong khi đủ các ý sau:

- [ ] `git log` thấy lịch sử dự án, đang ở `main`.
- [ ] Có `sach-giao-khoa-viet-nam/Tiếng Việt 1 (tập 1 1990)/`.
- [ ] Đã nhập gói media mới nhất (mục 4): 213 tranh, 1.926 âm thanh, clip trong `content/clips/`.
- [ ] Test Python ra `OK`.
- [ ] `python -m tapdoc validate` ra `OK`, không có "Cảnh báo: media…".
- [ ] `run_unity_tests.py editmode --filter "TapDoc.Tests.DataTests"` không có test lỗi.
- [ ] `MoCongCuDuyet.cmd` mở được trang duyệt.
- [ ] Đã hỏi chủ dự án về các file ở mục 7 và chép những gì cần.
- [ ] Đã xác nhận với chủ dự án trình duyệt Edge của máy này (mục 8).

Báo lại chủ dự án (bằng tiếng Việt): bước nào xong, bước nào còn thiếu và cần họ làm gì.
