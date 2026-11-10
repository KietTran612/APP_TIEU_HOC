# Chuyển dự án "Bờ A Ba" sang máy mới — hướng dẫn từng bước

Ngày 10/11/2026 mọi session trên máy cũ đã tạm dừng ở điểm sạch, toàn bộ dữ liệu đã được đóng gói. File này hướng dẫn khôi phục **từng bước** trên máy mới, theo hai phần:

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
2. Tải 4 file "Bắt buộc" ở mục 0.1 về `C:\Source\AURA\chuyen-may\`.
3. Giải nén hai file `BoABa-…zip` ngay tại thư mục đó: chuột phải → **Extract All** (Giải nén tất cả). Sau khi giải nén phải có:
   ```
   C:\Source\AURA\chuyen-may\repo\
   C:\Source\AURA\chuyen-may\ngoai-repo\
   C:\Source\AURA\chuyen-may\claude\
   C:\Source\AURA\chuyen-may\TapDoc-media-2026-11-10.unitypackage
   C:\Source\AURA\chuyen-may\TapDoc-clips-2026-11-10.zip
   ```
   **Không** giải nén file `TapDoc-clips-…zip`; lệnh ở bước B4 tự xử lý.

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

Bundle lỗi (báo "not a bundle", "missing") thì clone từ GitHub: `git clone https://github.com/KietTran612/APP_TIEU_HOC.git /c/Source/AURA/APP_TIEU_HOC`. Sau đó so với `COMMIT.txt`. Nếu thiếu commit, nghĩa là chủ dự án chưa push trên máy cũ: báo chủ dự án.

Sau khi clone: `git fetch origin`, rồi `git status` phải ghi "Your branch is ahead of 'origin/main' by N commits" hoặc "up to date". **Không** push; chủ dự án tự push.

### B3. Đặt lại chỉnh sửa duyệt

Bốn file `audio_manifest.json`, `image_manifest.json`, `video_manifest.json` và `content/tts/settings.json` chứa trạng thái, ghi chú duyệt của chủ dự án và cấu hình giọng đọc của các đợt sửa âm thanh.

Ngày 10/11 chủ dự án đã cho commit cả bốn file vào git (commit `230a2ef`, "bản chụp kết quả duyệt và cấu hình giọng đọc đến 10/11/2026").
- **Clone từ GitHub** và `git log` có `230a2ef`: **bỏ qua bước này**, bốn file đã đúng.
- **Clone từ bundle trong gói** (bundle được tạo trước commit đó): chạy các lệnh dưới đây. Sau đó `git pull` từ GitHub sẽ ra cùng nội dung.

```bash
cd /c/Source/AURA/APP_TIEU_HOC
cp "<goi>/repo/chinh-sua-duyet/content/manifests/audio_manifest.json" content/manifests/
cp "<goi>/repo/chinh-sua-duyet/content/manifests/image_manifest.json" content/manifests/
cp "<goi>/repo/chinh-sua-duyet/content/manifests/video_manifest.json" content/manifests/
cp "<goi>/repo/chinh-sua-duyet/content/tts/settings.json" content/tts/
git status --short
```

Kết quả đúng: `git status --short` chỉ có đúng 4 dòng `M` của 4 file trên. Nếu đã kéo được `230a2ef` từ GitHub thì `git status` sạch.

Từ nay về sau, chỉnh sửa duyệt **mới** của chủ dự án vẫn theo quy tắc cũ: không commit lẫn vào, trừ khi chủ dự án cho phép (QUY-TRINH-LAM-VIEC.md mục 1 và mục 10).

### B4. Nhập gói media

**Đóng Unity Editor** nếu đang mở, rồi chạy:

```bash
cd /c/Source/AURA/APP_TIEU_HOC/tools
python run_unity_media.py --timeout 7200 unpack "<goi>/TapDoc-media-2026-11-10.unitypackage" --clips "<goi>/TapDoc-clips-2026-11-10.zip"
```

Lần đầu mất khoảng 10–30 phút, vì Unity chạy nền để nhập.

Kiểm tra:

```bash
cd /c/Source/AURA/APP_TIEU_HOC
ls unity/TapDoc/Assets/Content/Resources/audio/*.mp3 | wc -l     # đúng: 6395
ls unity/TapDoc/Assets/Content/Resources/images/*.png | wc -l    # đúng: 431
ls content/clips/*.mp4 | wc -l                                   # đúng: 399
ls unity/TapDoc/Assets/Content/Resources/images/img_bia_*.png    # đúng: 3 bìa
grep '"package"' content/manifests/media_lock.json               # đúng: TapDoc-media-2026-11-10.unitypackage
```

Sai số lượng thì chạy lại lệnh unpack. Vẫn sai thì báo chủ dự án.

### B5. Chép các thư mục ngoài git

```bash
cd /c/Source/AURA/APP_TIEU_HOC
cp -r "<goi>/ngoai-repo/content/requests" content/
mkdir -p content/tts
cp -r "<goi>/ngoai-repo/content/tts/prev" "<goi>/ngoai-repo/content/tts/marks" "<goi>/ngoai-repo/content/tts/pitch_cache" content/tts/
cp -r "<goi>/ngoai-repo/.superpowers" .
ls content/tts/prev | wc -l          # đúng: khoảng 1.700
ls content/tts/marks | wc -l         # đúng: khoảng 2.750
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
PYTHONIOENCODING=utf-8 python -m tapdoc validate --allow-missing
```

Kết quả đúng:
- `validate --allow-missing` báo OK, không có dòng "Cảnh báo: media khác gói".
- Dùng `--allow-missing` vì còn khoảng 1.700 âm thanh lớp 2 và 274 âm thanh lớp 1 chưa tạo (việc dở, xem mục B11).

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
ls ~/.claude/projects/C--Source-AURA-APP-TIEU-HOC/memory/MEMORY.md
ls ~/.claude/projects/C--Source-AURA-APP-TIEU-HOC/*.jsonl | wc -l     # đúng: khoảng 22
# tùy chọn: bộ giao việc cho Codex và Antigravity
cp -r "<goi>/claude/claude-config/delegate" "<goi>/claude/claude-config/skills" ~/.claude/
```

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
2. Đọc `<goi>/claude/khoi-dong-lai.md`. File có 7 khối lời giao việc: Root và 6 session con.
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

| # | Việc | Session | Lệnh hoặc chỗ bắt đầu |
|---|---|---|---|
| 1 | Âm thanh lớp 1: còn 274 tiếng thanh nặng và âm ê (có mụ, nụ, đàn, một), câu "bé, bá cổ bà.", rồi ghép 2 câu khó `cau_b97_02`, `cau_b160_04` | [L1] | Ghi chú TV1 tập 2 mục 0; script `tools/scripts/regen_runner.py`, `l1_ghep_2_cau.py`; cấu hình đã có trong `content/tts/settings.json` |
| 2 | Âm thanh lớp 2: còn 1.711 mã | [L2] nội dung | `python tools/lop2/tieng_doc_lop2.py --ghi`, rồi `python tools/lop2/tts_lop2.py 4 172 304 --giu-may-thuc`. Sau đó đo cao độ, sửa, `stage_lop2.py`, commit |
| 3 | Clip b299 (đường dây điện): đã tạo trên Flow `/u/1`, dự án "Tháng 11 09 - 15:14", chưa tải | [L2] tranh động | Hỏi chủ dự án trước khi tải; thêm 1 dòng vào `video_manifest` |
| 4 | Đóng gói media lần cuối cho cả hai lớp, khi 1–3 xong | [L2] nội dung | Đóng Unity; `python tools/run_unity_media.py pack`; commit `media_lock.json`; chủ dự án tải lên Drive |

Quy tắc khi chạy âm thanh:
- chỉ **1 tiến trình** tạo giọng tại một thời điểm, nên việc 1 và 2 chạy lần lượt;
- mỗi mã đổi giữ bản cũ trong `prev`, trạng thái về `cho_duyet`, ghi chú "chờ nghe xác nhận".

### B12. Kiểm tra cuối và báo chủ dự án

- [ ] `git log` có commit `230a2ef` (hoặc đã chép 4 file ở bước B3); `git status` sạch hoặc chỉ có 4 file đó.
- [ ] Media: 6.395 âm thanh, 431 tranh, 399 clip; `media_lock.json` ghi gói `2026-11-10`.
- [ ] `content/tts/prev`, `marks`, `.superpowers`, `content/requests` đã có.
- [ ] `validate --allow-missing` OK, không có cảnh báo media.
- [ ] Bộ nhớ Claude đã chép (thấy `MEMORY.md`).
- [ ] Trình duyệt đã xác nhận, mã thiết bị mới đã ghi vào bộ nhớ.
- [ ] Đã mở lại đủ 6 session con; bảng phân công có id mới.
- [ ] `MoCongCuDuyet.cmd` mở được tool duyệt; ô "Sách" có 3 quyển.

Báo chủ dự án bằng tiếng Việt: bước nào xong, bước nào thiếu, chủ dự án cần làm gì.

---

## Phụ lục 1. Tình trạng lúc dừng (10/11/2026)

| Mảng | Đã xong | Còn lại |
|---|---|---|
| [L1] Nội dung, âm thanh TV1 | Tập 1 và tập 2 đủ bài, tranh, clip. Rà soát hỏi, ngã: 231 mã đã sửa. Thanh nặng và âm ê: 116/390 mã | 274 mã thanh nặng và âm ê, 2 câu khó |
| [L1] Tranh động lớp 1 | 343 clip; các clip làm lại chờ duyệt | Chờ chủ dự án duyệt |
| [L2] Nội dung TV2 tập một | 133 mục (172–304), màn mới; âm thanh 1.623/3.334 mã | 1.711 mã âm thanh, đo và sửa, đóng gói chung |
| [L2] Vẽ tranh TV2 | 57 tranh và kí hiệu giải nghĩa | Chờ duyệt (để ý b190, b268, b274) |
| [L2] Tranh động TV2 | 56/57 clip | Clip b299 |
| [Chung] UI | Tủ sách, 3 bìa, tên quyển "Bé tập đọc 1/2/3" | Chờ duyệt bìa, "test all" |

## Phụ lục 2. Việc chờ chủ dự án

1. Duyệt trong tool duyệt (`MoCongCuDuyet.cmd`), chọn ô "Sách" theo quyển:
   - âm thanh lớp 1 đã sửa (ghi chú "chờ nghe xác nhận"), nhất là 83 câu chèn dấu phẩy;
   - tranh và clip lớp 2;
   - các clip lớp 1 làm lại;
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
| `validate` báo "media khác gói" | Chưa unpack đúng gói `2026-11-10`; làm lại bước B4 |
| Chữ tiếng Việt in ra bị lỗi | Đặt `PYTHONIOENCODING=utf-8` trước lệnh python |
| edge-tts báo "No audio was received" | Dịch vụ chập chờn; chỉ chạy 1 tiến trình, chạy lượt bù (QUY-TRINH mục 12) |
| Không thấy bộ nhớ Claude trong session mới | Kiểm tra repo đặt đúng `C:\Source\AURA\APP_TIEU_HOC` và đã chép vào `~/.claude/projects/C--Source-AURA-APP-TIEU-HOC/` |
| Session con biến mất khỏi thanh bên | Không ghim session root; mục "Đã ghim" thu gọn sẽ giấu cả session con |
