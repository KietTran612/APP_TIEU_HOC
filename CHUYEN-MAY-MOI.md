# Chuyển dự án "Bờ A Ba" sang máy mới — hướng dẫn từng bước

Ngày 10/11/2026 mọi session trên máy cũ đã tạm dừng ở điểm sạch, toàn bộ dữ liệu đã được đóng gói.

**Cập nhật 11/11/2026.** Chủ dự án cho làm tiếp trên máy cũ thêm một ngày. Phần mới nằm trong **2 file cập nhật** trên Drive: gói media bổ sung và gói cập nhật. Máy mới vẫn dùng 4 file của ngày 10/11, rồi áp thêm 2 file này. Các bước bên dưới đã ghi rõ chỗ áp.

File này hướng dẫn khôi phục **từng bước** trên máy mới, theo hai phần:

- **Phần A: chủ dự án làm tay.** Gồm các việc AI không được làm: cài phần mềm có tài khoản, đăng nhập, tải file từ Drive.
- **Phần B: AI (Claude Code) làm theo**, sau khi phần A xong. Mỗi bước có lệnh, kết quả đúng phải thấy, và cách xử lý khi sai.

Không bỏ bước. Bước nào ra kết quả khác với ghi ở đây thì dừng, báo chủ dự án.

Tài liệu liên quan trong repo:
- [SETUP-MAY-MOI.md](SETUP-MAY-MOI.md): cài đặt chung;
- [QUY-TRINH-LAM-VIEC.md](QUY-TRINH-LAM-VIEC.md): quy trình chuẩn và bảng vấn đề khó;
- [docs/superpowers/notes/phan-cong-session.md](docs/superpowers/notes/phan-cong-session.md): các session;
- [docs/superpowers/notes/lich-su-cong-viec.md](docs/superpowers/notes/lich-su-cong-viec.md): việc đã xong.

---

## 0. Các file chuyển máy

### 0.1. Trên Google Drive (thư mục DATA)

Link: https://drive.google.com/drive/u/1/folders/1cw5FYmXGkWIwQRS3-BNPbvGfbJzrmT3m

| File | Dung lượng | Nội dung | Bắt buộc? |
|---|---|---|---|
| `TapDoc-media-2026-11-10.unitypackage` | khoảng 1,2 GB | 6.395 âm thanh và 431 tranh (cả lớp 1, lớp 2, 3 bìa, biểu tượng), kèm file `.meta` | **Có** |
| `TapDoc-clips-2026-11-10.zip` | khoảng 1,2 GB | 399 clip tranh động | **Có** |
| `BoABa-repo-va-ngoai-git-2026-11-10.zip` | khoảng 590 MB | Bản sao lịch sử git, chỉnh sửa duyệt chưa commit, các thư mục ngoài git | **Có** |
| `BoABa-du-lieu-session-2026-11-10.zip` | vài GB | Toàn bộ dữ liệu Claude: bộ nhớ, hội thoại gốc của mọi session, thư mục tạm, lời giao việc để mở lại session | **Có** (để AI làm tiếp đúng mạch) |
| `TapDoc-bosung-2026-11-11.zip` | khoảng 95 MB | **Cập nhật 11/11.** Media đổi sau gói 10/11: 1.704 âm thanh mới (hết lớp 2, 7 từ Em viết lớp 1), 152 file đổi (âm thanh sửa, tranh cái cuốc b101), 21 clip (b299 và 20 clip làm lại) | **Có** |
| `BoABa-cap-nhat-2026-11-11.zip` | xem mục 0.3 | **Cập nhật 11/11.** Commit mới (bundle tăng dần), chỉnh sửa duyệt mới, file ngoài git và dữ liệu Claude đổi sau 10/11, lời giao việc mới | **Có** |
| `CHUYEN-MAY-MOI.md` | | File này, bản 11/11; thay bản 10/11 | **Có** |
| `TapDoc-media-2026-11-02…`, `TapDoc-clips-2026-11-02…` | | Gói cũ | Không dùng nữa |

### 0.2. Trên máy cũ (bản gốc của gói)

Thư mục `C:\Source\AURA\BoABa-chuyen-may-2026-11-10\` có cùng nội dung đã giải nén. Có thể chép thẳng bằng USB thay cho việc tải từ Drive.

### 0.3. Nội dung hai file zip chuyển máy

`BoABa-repo-va-ngoai-git-2026-11-10.zip`:
```
repo/APP_TIEU_HOC.bundle          toàn bộ lịch sử git, có cả commit chưa push
repo/COMMIT.txt                   commit cuối và số commit chưa push lúc đóng gói
repo/chinh-sua-duyet/             4 file có chỉnh sửa duyệt chưa commit, kèm chinh-sua-duyet.patch
   content/manifests/audio_manifest.json
   content/manifests/image_manifest.json
   content/manifests/video_manifest.json
   content/tts/settings.json
ngoai-repo/content/requests/      phiếu vẽ tranh từng bài
ngoai-repo/content/tts/prev/      bản âm thanh cũ, để nghe so trong tool duyệt
ngoai-repo/content/tts/marks/     mốc thời gian từng tiếng (lệnh tapdoc pitch cần)
ngoai-repo/content/tts/pitch_cache/
ngoai-repo/.superpowers/          trang nghe thử, sổ kế hoạch, script cũ
CHUYEN-MAY-MOI.md
```

`BoABa-du-lieu-session-2026-11-10.zip`:
```
claude/memory/                                  bộ nhớ dự án của Claude (32 file .md)
claude/claude-projects/C--Source-AURA-APP-TIEU-HOC/   toàn bộ dữ liệu Claude Code của dự án:
                                                hội thoại gốc *.jsonl của mọi session, kèm memory/
claude/scratchpads/                             thư mục tạm của từng session (script, log, dữ liệu đo)
claude/ghi-chu-session/                         ghi chú các session để ngoài repo
claude/claude-config/delegate, skills           bộ giao việc cho Codex và Antigravity
claude/khoi-dong-lai.md                         lời giao việc để mở lại từng session
CHUYEN-MAY-MOI.md
```

`BoABa-cap-nhat-2026-11-11.zip` (giải nén ra thư mục `cap-nhat/`; chỉ gồm file đổi sau 10/11 09:00):
```
cap-nhat/repo/APP_TIEU_HOC-cap-nhat.bundle     các commit mới sau 5fd08c5 (cần bundle 10/11 trước)
cap-nhat/repo/COMMIT.txt                       commit cuối lúc đóng gói 11/11
cap-nhat/repo/chinh-sua-duyet/                 4 file có chỉnh sửa duyệt mới chưa commit, kèm .patch
cap-nhat/ngoai-repo/                           file đổi trong content/tts/prev, marks, pitch_cache, content/requests, .superpowers
cap-nhat/claude/memory/                        bộ nhớ dự án bản mới nhất (đủ cả thư mục)
cap-nhat/claude/claude-projects/…              hội thoại *.jsonl và file đổi của các session
cap-nhat/claude/scratchpads/, ghi-chu-session/, claude-config/   file đổi
cap-nhat/claude/khoi-dong-lai.md               lời giao việc bản 11/11 (thay bản 10/11)
```

---

## Phần A — Chủ dự án làm tay

### A1. Cài phần mềm

Cài theo bảng ở SETUP-MAY-MOI.md mục 1:

| Phần mềm | Phiên bản | Lưu ý |
|---|---|---|
| Git | mới nhất | Có Git Bash |
| Python | 3.14 | Bản python.org; lúc cài nhớ tích "Add python.exe to PATH" |
| Unity Hub và Unity Editor | **6000.6.5f1** | Cài vào chỗ mặc định `C:\Program Files\Unity\Hub\Editor\6000.6.5f1\`; đăng nhập tài khoản Unity |
| Node.js | 24 | Tùy chọn |
| Microsoft Edge | mới nhất | Cài tiện ích **Claude** (Claude in Chrome) và đăng nhập Claude |
| Claude Code | app máy tính hoặc dòng lệnh | Đăng nhập tài khoản Claude sẽ dùng |

### A2. Đăng nhập các dịch vụ trên Edge

AI không đăng nhập hộ, nên chủ dự án tự đăng nhập:
- **ChatGPT**: tài khoản có dự án **Kiet_1** (dùng để vẽ tranh).
- **Google Flow**: các tài khoản đang dùng để làm tranh động. Danh sách và credit xem `docs/superpowers/notes/2026-11-10-tiep-tuc-tranh-dong-tv2-t1.md` và `content/style/tranh_dong_huong_dan.md` mục 5. Không dùng tài khoản công ty `/u/0`.
- **Google Drive**: tài khoản có thư mục DATA (link ở mục 0.1).

### A3. Tải file từ Drive

1. Tạo thư mục `C:\Source\AURA\`.
2. Tải mọi file "Bắt buộc" ở mục 0.1 (7 file) về `C:\Source\AURA\chuyen-may\`. `CHUYEN-MAY-MOI.md` lấy bản 11/11.
3. Giải nén ba file `BoABa-…zip` ngay tại thư mục đó: chuột phải → **Extract All** (Giải nén tất cả), bỏ tên thư mục con Windows tự thêm. Sau khi giải nén phải có:
   ```
   C:\Source\AURA\chuyen-may\repo\
   C:\Source\AURA\chuyen-may\ngoai-repo\
   C:\Source\AURA\chuyen-may\claude\
   C:\Source\AURA\chuyen-may\cap-nhat\repo\   (và cap-nhat\ngoai-repo\, cap-nhat\claude\)
   C:\Source\AURA\chuyen-may\TapDoc-media-2026-11-10.unitypackage
   C:\Source\AURA\chuyen-may\TapDoc-clips-2026-11-10.zip
   C:\Source\AURA\chuyen-may\TapDoc-bosung-2026-11-11.zip
   ```
   **Không** giải nén `TapDoc-clips-…zip` và `TapDoc-bosung-…zip`; lệnh ở bước B4 tự xử lý.

### A4. Mở Claude Code và giao việc cho AI

1. Mở Claude Code tại thư mục `C:\Source\AURA\`. Repo chưa có nên mở thư mục cha.
2. Dán câu sau:
   > Đọc file `C:\Source\AURA\chuyen-may\CHUYEN-MAY-MOI.md` và làm Phần B từng bước. Gói chuyển máy ở `C:\Source\AURA\chuyen-may\`. Trả lời bằng tiếng Việt.
3. Khi AI hỏi xác nhận trình duyệt (bước B9), kiểm tra đúng là Edge của máy mới rồi trả lời.

---

## Phần B — AI làm theo

Quy ước:
- `<goi>` = `C:/Source/AURA/chuyen-may` (dùng `/` trong Git Bash).
- Repo đặt **đúng** ở `C:/Source/AURA/APP_TIEU_HOC`. Bộ nhớ Claude được đặt tên theo đường dẫn này (`C--Source-AURA-APP-TIEU-HOC`); đặt chỗ khác sẽ không khớp.

### B1. Kiểm tra phần mềm

```bash
git --version
python --version
ls "/c/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe"
ls "<goi>/repo/APP_TIEU_HOC.bundle" "<goi>/TapDoc-media-2026-11-10.unitypackage" "<goi>/TapDoc-clips-2026-11-10.zip" "<goi>/claude/khoi-dong-lai.md"
ls "<goi>/TapDoc-bosung-2026-11-11.zip" "<goi>/cap-nhat/repo/APP_TIEU_HOC-cap-nhat.bundle" "<goi>/cap-nhat/claude/khoi-dong-lai.md"
```

Kết quả đúng: in ra phiên bản Git và Python 3.14, không có dòng "No such file". Thiếu thứ gì thì dừng, báo chủ dự án làm lại Phần A.

### B2. Lấy mã nguồn

Ưu tiên lấy từ bundle, vì bundle có cả các commit chưa push:

```bash
git clone "<goi>/repo/APP_TIEU_HOC.bundle" /c/Source/AURA/APP_TIEU_HOC
cd /c/Source/AURA/APP_TIEU_HOC
git checkout main
git remote set-url origin https://github.com/KietTran612/APP_TIEU_HOC.git
git log -1 --format="%H %s"
cat "<goi>/repo/COMMIT.txt"
```

Kết quả đúng: mã commit in ra từ `git log` **trùng** dòng đầu của `COMMIT.txt`.

**Áp bản cập nhật 11/11** (bundle tăng dần, cần commit `5fd08c5` đã có từ bước trên):

```bash
cd /c/Source/AURA/APP_TIEU_HOC
git bundle verify "<goi>/cap-nhat/repo/APP_TIEU_HOC-cap-nhat.bundle"
git pull --ff-only "<goi>/cap-nhat/repo/APP_TIEU_HOC-cap-nhat.bundle" main
git log -1 --format="%H %s"
head -1 "<goi>/cap-nhat/repo/COMMIT.txt"
```

Kết quả đúng: `verify` báo "is okay"; hai dòng cuối in **cùng** mã commit. Nếu chủ dự án đã push hết lên GitHub thì `git pull origin main` cũng ra cùng kết quả.

Bundle lỗi (báo "not a bundle", "missing") thì clone từ GitHub: `git clone https://github.com/KietTran612/APP_TIEU_HOC.git /c/Source/AURA/APP_TIEU_HOC`. Sau đó so với `COMMIT.txt`. Nếu thiếu commit, nghĩa là chủ dự án chưa push trên máy cũ: báo chủ dự án.

Sau khi clone: `git fetch origin`, rồi `git status` phải ghi "Your branch is ahead of 'origin/main' by N commits" hoặc "up to date". **Không** push; chủ dự án tự push.

### B3. Đặt lại chỉnh sửa duyệt

Bốn file `audio_manifest.json`, `image_manifest.json`, `video_manifest.json` và `content/tts/settings.json` chứa trạng thái, ghi chú duyệt của chủ dự án và cấu hình giọng đọc của các đợt sửa âm thanh.

Ngày 10/11 chủ dự án đã cho commit cả bốn file vào git (commit `230a2ef`). Ngày 11/11 chủ dự án duyệt thêm (clip tập 1 bài 21–80, clip tập 2 bài 81–148, tranh cái cuốc, một số âm thanh). Các chỉnh sửa duyệt mới này **chưa commit**, nằm trong gói cập nhật. Sau bước B2 (đã áp bundle cập nhật), chép bản 11/11:

```bash
cd /c/Source/AURA/APP_TIEU_HOC
cp "<goi>/cap-nhat/repo/chinh-sua-duyet/content/manifests/audio_manifest.json" content/manifests/
cp "<goi>/cap-nhat/repo/chinh-sua-duyet/content/manifests/image_manifest.json" content/manifests/
cp "<goi>/cap-nhat/repo/chinh-sua-duyet/content/manifests/video_manifest.json" content/manifests/
cp "<goi>/cap-nhat/repo/chinh-sua-duyet/content/tts/settings.json" content/tts/
git status --short
git diff --stat
```

Kết quả đúng: `git status --short` chỉ có 4 dòng `M` của 4 file trên; `git diff --stat` khớp với `chinh-sua-duyet.patch` (khoảng 350 dòng thêm, 300 dòng bớt). **Không** dùng thư mục `chinh-sua-duyet` cũ của ngày 10/11.

Từ nay về sau, chỉnh sửa duyệt **mới** của chủ dự án vẫn theo quy tắc cũ: không commit lẫn vào, trừ khi chủ dự án cho phép (QUY-TRINH-LAM-VIEC.md mục 1 và mục 10).

### B4. Nhập gói media

**Đóng Unity Editor** nếu đang mở, rồi chạy:

```bash
cd /c/Source/AURA/APP_TIEU_HOC/tools
python run_unity_media.py --timeout 7200 unpack "<goi>/TapDoc-media-2026-11-10.unitypackage" --clips "<goi>/TapDoc-clips-2026-11-10.zip" --bosung "<goi>/TapDoc-bosung-2026-11-11.zip"
```

Lần đầu mất khoảng 10–30 phút, vì Unity chạy nền để nhập. Lệnh nhập gói chính trước, rồi áp gói bổ sung 11/11 (chép đè file đổi, thêm file mới, kèm `.meta`), rồi so với khoá media.

Kiểm tra:

```bash
cd /c/Source/AURA/APP_TIEU_HOC
ls unity/TapDoc/Assets/Content/Resources/audio/*.mp3 | wc -l     # đúng: 8099
ls unity/TapDoc/Assets/Content/Resources/images/*.png | wc -l    # đúng: 431
ls content/clips/*.mp4 | wc -l                                   # đúng: 400
ls unity/TapDoc/Assets/Content/Resources/clips/*.mp4 | wc -l     # clip dat + cho_duyet (unpack tự chép; chép lại: python tools/run_unity_media.py clips)
ls unity/TapDoc/Assets/Content/Resources/images/img_bia_*.png    # đúng: 3 bìa
grep -A2 '"package"' content/manifests/media_lock.json           # đúng: gói 2026-11-10 và "bosung": ["TapDoc-bosung-2026-11-11.zip"]
```

Lệnh unpack in "media khác gói" nghĩa là thiếu gói bổ sung hoặc áp sai thứ tự: chạy lại đúng lệnh trên.

Sai số lượng thì chạy lại lệnh unpack. Vẫn sai thì báo chủ dự án.

### B5. Chép các thư mục ngoài git

```bash
cd /c/Source/AURA/APP_TIEU_HOC
cp -r "<goi>/ngoai-repo/content/requests" content/
mkdir -p content/tts
cp -r "<goi>/ngoai-repo/content/tts/prev" "<goi>/ngoai-repo/content/tts/marks" "<goi>/ngoai-repo/content/tts/pitch_cache" content/tts/
cp -r "<goi>/ngoai-repo/.superpowers" .
# áp bản cập nhật 11/11 (chép đè lên)
cp -r "<goi>/cap-nhat/ngoai-repo/." .
ls content/tts/prev | wc -l          # đúng: khoảng 2.200
ls content/tts/marks | wc -l         # đúng: khoảng 4.700
ls .superpowers/nghe-thu-2/index.html
git status --short                   # vẫn chỉ 4 dòng M: các thư mục trên bị git bỏ qua
```

Ảnh scan sách gốc thì clone riêng, theo SETUP-MAY-MOI.md mục 3:
```bash
git clone https://github.com/giangtv134/sach-giao-khoa-viet-nam.git /c/Source/AURA/APP_TIEU_HOC/sach-giao-khoa-viet-nam
```

### B6. Công cụ Python và kiểm tra dữ liệu

```bash
cd /c/Source/AURA/APP_TIEU_HOC/tools
python -m pip install -r requirements-tts.txt
PYTHONIOENCODING=utf-8 python -m tapdoc validate
```

Kết quả đúng: `validate` báo OK, không có dòng "Cảnh báo: media khác gói". Từ 11/11 mọi âm thanh đã có file, nên **không** cần `--allow-missing`.

Chỉ chạy unit test liên quan khi sửa code. Không chạy toàn bộ khi chủ dự án chưa nói "test all".

### B7. Mở project Unity một lần

1. Mở Unity Hub, chọn **Add project from disk**, rồi chọn `C:\Source\AURA\APP_TIEU_HOC\unity\TapDoc`.
2. Mở project, chờ nhập xong rồi đóng.
3. Kiểm tra nhanh:

```bash
cd /c/Source/AURA/APP_TIEU_HOC
python tools/run_unity_tests.py editmode --filter "TapDoc.Tests.SetupTests"
```

Kết quả đúng: `EditMode: N passed, 0 failed`.

### B8. Khôi phục dữ liệu Claude (bộ nhớ và hội thoại)

Thư mục dữ liệu Claude Code của dự án nằm ở `C:\Users\<tên người dùng>\.claude\projects\C--Source-AURA-APP-TIEU-HOC\`. Nếu chưa có, mở Claude Code một lần trong `C:\Source\AURA\APP_TIEU_HOC` để nó tự tạo.

```bash
mkdir -p ~/.claude/projects
cp -r "<goi>/claude/claude-projects/C--Source-AURA-APP-TIEU-HOC" ~/.claude/projects/
# áp bản cập nhật 11/11: hội thoại mới, rồi bộ nhớ bản mới nhất
cp -r "<goi>/cap-nhat/claude/claude-projects/C--Source-AURA-APP-TIEU-HOC/." ~/.claude/projects/C--Source-AURA-APP-TIEU-HOC/
rm -rf ~/.claude/projects/C--Source-AURA-APP-TIEU-HOC/memory
cp -r "<goi>/cap-nhat/claude/memory" ~/.claude/projects/C--Source-AURA-APP-TIEU-HOC/memory
ls ~/.claude/projects/C--Source-AURA-APP-TIEU-HOC/memory/MEMORY.md
grep -c "3321/3321" ~/.claude/projects/C--Source-AURA-APP-TIEU-HOC/memory/MEMORY.md   # đúng: 1 (bộ nhớ bản 11/11)
ls ~/.claude/projects/C--Source-AURA-APP-TIEU-HOC/*.jsonl | wc -l     # đúng: khoảng 22
# tùy chọn: bộ giao việc cho Codex và Antigravity
cp -r "<goi>/claude/claude-config/delegate" "<goi>/claude/claude-config/skills" ~/.claude/
cp -r "<goi>/cap-nhat/claude/claude-config/." ~/.claude/ 2>/dev/null || true
```

Thư mục tạm và ghi chú session: bản 11/11 nằm trong `<goi>/cap-nhat/claude/scratchpads/` và `<goi>/cap-nhat/claude/ghi-chu-session/`, chỉ để tra cứu, không cần chép.

Sau bước này:
- **Bộ nhớ** tự được nạp ở mọi session mới của dự án: các quy tắc chủ dự án đã chốt, quyết định, tình trạng.
- **Hội thoại cũ:** với Claude Code dòng lệnh, chạy `claude --resume` trong thư mục repo để liệt kê và mở lại. App máy tính không hiện các session cũ trên thanh bên; khi đó mở session mới bằng lời giao việc (bước B10). Hội thoại cũ vẫn tra cứu được trong các file `.jsonl`.
- **Ghi nhớ gắn với máy cũ, phải sửa lại:**
  - mã thiết bị trình duyệt `407cb8a9…` trong bộ nhớ `feedback-local-edge-only` là của máy cũ: cập nhật sau bước B9;
  - các đường dẫn `C:\Users\trant\…` của máy cũ.

### B9. Xác nhận trình duyệt

Gọi `list_connected_browsers`. Chỉ được dùng trình duyệt có `onThisComputer: true` (Edge của máy mới).

Hỏi chủ dự án xác nhận trước lần dùng đầu, rồi ghi mã thiết bị mới vào bộ nhớ `feedback-local-edge-only.md`, thay mã cũ. Không bao giờ điều khiển trình duyệt của máy khác.

### B10. Mở lại các session

1. Session hiện tại trở thành session **điều phối** (root). Đổi tên thành "Điều phối dự án Bờ A Ba" và **không ghim** nó.
2. Đọc `<goi>/cap-nhat/claude/khoi-dong-lai.md` (bản 11/11; **không** dùng bản 10/11). File có 7 khối lời giao việc: Root và 6 session con.
3. Mở 6 session con, mỗi session dán đúng một khối, tên có tiền tố như cũ:

   | Session | Ghi chú tiếp tục phải đọc trước |
   |---|---|
   | [L1] Làm SGK Tiếng Việt 1 (nội dung, giọng đọc) | `docs/superpowers/notes/2026-11-05-tiep-tuc-tv1-tap-2.md` (mục 0) |
   | [L1] Tranh động lớp 1 | `docs/superpowers/notes/2026-11-10-tiep-tuc-tranh-dong-lop-1.md` |
   | [L2] Làm SGK Tiếng Việt 2 tập 1 | `docs/superpowers/notes/2026-11-09-tiep-tuc-tv2-tap-1.md` |
   | [L2] Vẽ tranh Tiếng Việt 2 tập 1 | `docs/superpowers/notes/2026-11-10-tiep-tuc-tranh-tv2-t1.md` |
   | [L2] Tranh động Tiếng Việt 2 tập 1 | `docs/superpowers/notes/2026-11-10-tiep-tuc-tranh-dong-tv2-t1.md` |
   | [Chung] UI và hiệu ứng | `docs/superpowers/notes/2026-11-09-tiep-tuc-tu-sach.md` |

4. Ghi id mới của các session vào `docs/superpowers/notes/phan-cong-session.md`, rồi commit.
5. Gửi id của nhau cho các session [L2], để chúng nhắn trực tiếp được.

### B11. Việc dở cần chạy tiếp (theo thứ tự)

Đến 11/11 các việc âm thanh lớp 1, âm thanh lớp 2 và clip b299 trong bảng 10/11 đều đã xong. Việc còn lại:

| # | Việc | Session | Lệnh hoặc chỗ bắt đầu |
|---|---|---|---|
| 1 | Làm lại clip bị chê đợt 11/11: 7 clip tập 1 (hoa cúc, cô giáo, bãi cát, đầm sen, nhịp cầu, xe qua cầu, cô Tấm), 32 clip tập 2, clip cái cuốc b101 (tranh đã vẽ lại) | [L1] tranh động | Ghi chú `2026-11-10-tiep-tuc-tranh-dong-lop-1.md` mục 6–9; kịch bản đã có. Gửi **chậm**, từng clip cách nhau vài phút; thử 1 clip trên `/u/4` trước, `/u/2` và `/u/3` để sau cùng. Gặp "unusual activity" hoặc CAPTCHA thì dừng, báo root |
| 2 | Khi có thêm media mới (clip làm lại, âm thanh sửa theo duyệt): đóng gói bổ sung | Root | Đóng Unity; chạy Unity nền một lần để tạo `.meta` (Phụ lục 3); `python tools/run_unity_media.py bosung`; commit `media_lock.json`; chủ dự án tải `dist/TapDoc-bosung-<ngày>.zip` lên Drive |

Quy tắc:
- **Không** chạy `run_unity_media.py pack` nữa, trừ khi chủ dự án muốn làm lại gói lớn: `pack` đổi gói gốc, các máy khác phải tải lại toàn bộ. Dùng `bosung`.
- Âm thanh: chỉ **1 tiến trình** tạo giọng tại một thời điểm; mỗi mã đổi giữ bản cũ trong `prev`, trạng thái về `cho_duyet`, ghi chú "chờ nghe xác nhận".

### B12. Kiểm tra cuối và báo chủ dự án

- [ ] `git log -1` trùng dòng đầu `cap-nhat/repo/COMMIT.txt`; `git status` chỉ có 4 file chỉnh sửa duyệt 11/11.
- [ ] Media: 8.099 âm thanh, 431 tranh, 400 clip; `media_lock.json` ghi gói `2026-11-10` và bổ sung `TapDoc-bosung-2026-11-11.zip`.
- [ ] `content/tts/prev`, `marks`, `.superpowers`, `content/requests` đã có, đã chép đè bản cập nhật.
- [ ] `validate` (không `--allow-missing`) OK, không có cảnh báo media.
- [ ] Bộ nhớ Claude đã chép (thấy `MEMORY.md`).
- [ ] Trình duyệt đã xác nhận, mã thiết bị mới đã ghi vào bộ nhớ.
- [ ] Đã mở lại đủ 6 session con; bảng phân công có id mới.
- [ ] `MoCongCuDuyet.cmd` mở được tool duyệt; ô "Sách" có 3 quyển.

Báo chủ dự án bằng tiếng Việt: bước nào xong, bước nào thiếu, chủ dự án cần làm gì.

---

## Phụ lục 1. Tình trạng lúc dừng (11/11/2026)

| Mảng | Đã xong | Còn lại |
|---|---|---|
| [L1] Nội dung, âm thanh TV1 | Tập 1 và tập 2 đủ bài, tranh, clip, âm thanh (không còn mã `chua_co`). Thanh nặng, âm ê, mụ, 2 câu khó; thêm từ ▨ Em viết của 7 bài Ôn tập (b07, b11, b17, b22, b27, b32, b37) | Chờ chủ dự án nghe |
| [L1] Tranh động lớp 1 | Làm lại 20/27 clip tập 1 bị chê ngày 11/11; kịch bản mới cho 32 clip tập 2 bị chê và clip cái cuốc | 7 clip tập 1, 32 clip tập 2, clip cái cuốc (B11 việc 1) |
| [L2] Nội dung TV2 tập một | 133 mục (172–304), màn mới; âm thanh 3.321/3.321 mã, đã đo và sửa hỏi, ngã | Chờ chủ dự án nghe (ghi chú tiếp tục mục 1b) |
| [L2] Vẽ tranh TV2 | 57 tranh và kí hiệu giải nghĩa | Chờ duyệt (để ý b190, b268, b274) |
| [L2] Tranh động TV2 | 57/57 clip | Chờ duyệt |
| [Chung] UI | Tủ sách, 3 bìa, tên quyển "Bé tập đọc 1/2/3" | Chờ duyệt bìa, "test all" |

## Phụ lục 2. Việc chờ chủ dự án

1. Duyệt trong tool duyệt (`MoCongCuDuyet.cmd`), chọn ô "Sách" theo quyển:
   - âm thanh lớp 1 đã sửa (ghi chú "chờ nghe xác nhận"), nhất là mụ, 4 tiếng khó ạch, ặp, kịch, sạch, và 7 từ Em viết (câu "Dì ghi gì đó?" giọng gần như câu kể);
   - âm thanh lớp 2: các mã nêu ở ghi chú `2026-11-09-tiep-tuc-tv2-tap-1.md` mục 1b;
   - tranh và clip lớp 2;
   - các clip lớp 1 làm lại, và tranh cái cuốc b101 vẽ lại;
   - 3 bìa mới;
   - lời dẫn tranh bài 18 (chữ "quả").
2. Bản đồ bài 97 (TV1 tập 2) đang là ảnh tạm cắt từ scan, phải vẽ lại trước khi phát hành.
3. Nói "test all" khi muốn chạy toàn bộ test.
4. Push các commit chưa push.
5. Trước khi đăng app: chọn mã gói, tra nhãn hiệu "Bờ A Ba".

## Phụ lục 3. Gặp lỗi thì làm gì

| Triệu chứng | Cách xử lý |
|---|---|
| `run_unity_media.py` báo "Không tìm thấy Unity" | Cài Unity đúng bản 6000.6.5f1 vào chỗ mặc định |
| Unpack báo project đang mở | Đóng Unity Editor rồi chạy lại |
| `pack` báo "N file chưa có .meta" | Chạy Unity nền một lần: `"C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe" -batchmode -nographics -projectPath C:/Source/AURA/APP_TIEU_HOC/unity/TapDoc -quit`, rồi chạy lại `pack` |
| `validate` báo "media khác gói" | Chưa unpack đúng gói `2026-11-10` kèm `--bosung` gói `2026-11-11`; làm lại bước B4 |
| `git pull` bundle cập nhật báo thiếu commit cần có trước | Chưa clone bundle 10/11 (bước B2 phần đầu); làm lại từ B2 |
| Chữ tiếng Việt in ra bị lỗi | Đặt `PYTHONIOENCODING=utf-8` trước lệnh python |
| edge-tts báo "No audio was received" | Dịch vụ chập chờn; chỉ chạy 1 tiến trình, chạy lượt bù (QUY-TRINH mục 12) |
| Không thấy bộ nhớ Claude trong session mới | Kiểm tra repo đặt đúng `C:\Source\AURA\APP_TIEU_HOC` và đã chép vào `~/.claude/projects/C--Source-AURA-APP-TIEU-HOC/` |
| Session con biến mất khỏi thanh bên | Không ghim session root; mục "Đã ghim" thu gọn sẽ giấu cả session con |
