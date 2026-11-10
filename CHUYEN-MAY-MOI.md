# Chuyển dự án sang máy mới (tạm dừng ngày 10/11/2026)

Ngày 10/11/2026 chủ dự án cho tạm dừng mọi session trên máy cũ và đóng gói, để làm tiếp trên một máy hoặc tài khoản khác. File này hướng dẫn khôi phục. Việc cài phần mềm theo [SETUP-MAY-MOI.md](SETUP-MAY-MOI.md); file này chỉ ghi phần riêng của lần chuyển này.

Đọc kèm:
- [QUY-TRINH-LAM-VIEC.md](QUY-TRINH-LAM-VIEC.md): quy trình chuẩn và bảng vấn đề khó đã giải;
- [docs/superpowers/notes/phan-cong-session.md](docs/superpowers/notes/phan-cong-session.md): các session và việc của từng session lúc dừng;
- [docs/superpowers/notes/lich-su-cong-viec.md](docs/superpowers/notes/lich-su-cong-viec.md): việc đã xong.

---

## 1. Gói chuyển máy

Gói nằm ở thư mục `BoABa-chuyen-may-2026-11-10/`, cạnh repo trên máy cũ (`C:\Source\AURA\`). Chủ dự án chép cả thư mục sang máy mới bằng USB hoặc Drive.

| Trong gói | Nội dung | Dùng ở bước |
|---|---|---|
| `repo/APP_TIEU_HOC.bundle` | Toàn bộ lịch sử git (`git bundle --all`), để khôi phục không cần mạng | 2 |
| `repo/chinh-sua-duyet/` | 4 file danh mục và cấu hình đang có chỉnh sửa duyệt của chủ dự án **chưa commit**, kèm `chinh-sua-duyet.patch` | 3 |
| `media/TapDoc-media-2026-11-10.unitypackage` (khoảng 1,2 GB), `media/TapDoc-clips-2026-11-10.zip` (khoảng 1,2 GB) | Gói media mới nhất: tranh, âm thanh, clip của cả lớp 1 và lớp 2. Mới hơn gói trên Drive | 4 |
| `ngoai-repo/` | Các thư mục bị git bỏ qua mà vẫn cần: `content/requests/`, `content/tts/prev/`, `content/tts/marks/`, `.superpowers/` (trang nghe thử, sổ kế hoạch) | 5 |
| `claude/memory/` | Bộ nhớ dự án của Claude (các quy tắc chủ dự án đã chốt) | 6 |
| `claude/claude-projects/C--Source-AURA-APP-TIEU-HOC/` | **Toàn bộ** dữ liệu Claude Code của dự án: bộ nhớ và hội thoại gốc (`*.jsonl`) của mọi session (root, các session con, các session cũ), kèm kết quả công cụ | 6 |
| `claude/scratchpads/` | Thư mục tạm của từng session: script, log, dữ liệu đo | tra cứu |
| `claude/ghi-chu-session/` | Ghi chú các session để ngoài repo (`side-session-notes`) | 6 |
| `claude/claude-config/` | `~/.claude/delegate` (giao việc cho Codex, Antigravity) và `~/.claude/skills` | 6 |
| `claude/khoi-dong-lai.md` | Lời giao việc để mở lại các session trên máy mới | 7 |

## 2. Lấy mã nguồn

Nên đặt đúng đường dẫn cũ `C:\Source\AURA\APP_TIEU_HOC`, để ghi chú và bộ nhớ khớp đường dẫn.

- **Có mạng:** `git clone https://github.com/KietTran612/APP_TIEU_HOC.git C:\Source\AURA\APP_TIEU_HOC`. Lúc đóng gói còn 9 commit chưa push: chủ dự án push trên máy cũ trước khi rời, hoặc dùng bundle bên dưới (bundle có đủ mọi commit).
- **Không có mạng hoặc muốn chắc chắn:** `git clone <gói>/repo/APP_TIEU_HOC.bundle C:\Source\AURA\APP_TIEU_HOC`, rồi `git remote set-url origin https://github.com/KietTran612/APP_TIEU_HOC.git`.
- Kiểm tra: `git log --oneline -1` phải trùng commit ghi trong `<gói>/repo/COMMIT.txt`.

## 3. Đặt lại chỉnh sửa duyệt chưa commit

Chủ dự án đang duyệt dở: trạng thái và ghi chú nằm trong 4 file chưa commit, gồm `content/manifests/audio_manifest.json`, `image_manifest.json`, `video_manifest.json` và `content/tts/settings.json`. Chép đè 4 file trong `<gói>/repo/chinh-sua-duyet/` vào đúng chỗ trong repo, hoặc chạy `git apply <gói>/repo/chinh-sua-duyet/chinh-sua-duyet.patch`.

**Không commit các file này.** Chúng vẫn là chỉnh sửa duyệt của chủ dự án (xem quy tắc ở QUY-TRINH mục 1 và mục 10).

## 4. Media

Đóng Unity Editor, rồi chạy:

```bash
cd C:/Source/AURA/APP_TIEU_HOC/tools
python run_unity_media.py unpack "<gói>/media/TapDoc-media-2026-11-10.unitypackage" --clips "<gói>/media/TapDoc-clips-2026-11-10.zip"
```

Kết quả đúng: lệnh in "Đã nhập gói media." và không có cảnh báo media khác gói. Tên gói phải trùng với `content/manifests/media_lock.json`. Chủ dự án nên tải hai file này lên thư mục Drive của dự án, vì chúng mới hơn gói trên Drive.

## 5. Các thư mục ngoài git

Chép từ `<gói>/ngoai-repo/` vào repo, giữ nguyên đường dẫn:

| Thư mục | Dùng để |
|---|---|
| `content/requests/` | Phiếu vẽ tranh từng bài (lớp 1, lớp 2) |
| `content/tts/prev/` | Bản âm thanh cũ để nghe so trong tool duyệt |
| `content/tts/marks/` | Mốc thời gian từng tiếng, dùng cho lệnh `tapdoc pitch` |
| `.superpowers/` | Trang nghe thử `nghe-thu/`, `nghe-thu-2/`; sổ kế hoạch `sdd/`; script cũ |

Ảnh scan sách thì clone lại theo SETUP mục 3.

## 6. Bộ nhớ Claude

Trên máy mới, sau khi mở dự án bằng Claude Code một lần:
- Chép `<gói>/claude/claude-projects/C--Source-AURA-APP-TIEU-HOC/` vào `C:\Users\<tên>\.claude\projects\`. Thư mục được đặt tên theo đường dẫn dự án, nên phải clone repo đúng `C:\Source\AURA\APP_TIEU_HOC`.
  - Bước này mang theo bộ nhớ (`memory/`) và hội thoại gốc của mọi session.
  - Với Claude Code dạng dòng lệnh, `claude --resume` trong thư mục repo sẽ liệt kê các hội thoại cũ để mở lại.
  - App máy tính không tự hiện các session cũ trên thanh bên. Khi đó dùng lời giao việc ở mục 7; hội thoại gốc vẫn tra cứu được trong các file `.jsonl`.
- Nếu chỉ cần bộ nhớ: chép `<gói>/claude/memory/*.md` vào `C:\Users\<tên>\.claude\projects\C--Source-AURA-APP-TIEU-HOC\memory\`.
- Nếu muốn dùng lại bộ giao việc cho Codex, Antigravity: chép `<gói>/claude/claude-config/delegate` và `skills` vào `C:\Users\<tên>\.claude\`.

Một số ghi nhớ gắn với máy cũ, cần đọc lại cho đúng trên máy mới:
- **Mã thiết bị trình duyệt** `407cb8a9…` là của máy cũ. Trên máy mới, kiểm tra bằng `list_connected_browsers`, và hỏi chủ dự án xác nhận trình duyệt của máy mới trước lần dùng đầu.
- **Thư mục ghi chú session** (`side-session-notes`): nội dung đã chép vào `<gói>/claude/ghi-chu-session/`; phần quan trọng đã được các session chép vào `docs/superpowers/notes/`.
- **Tài khoản ChatGPT** (dự án Kiet_1) **và Google Flow:** chủ dự án tự đăng nhập trên Edge của máy mới. AI không đăng nhập, không tạo tài khoản.

## 7. Mở lại các session

Mở Claude Code trong thư mục repo. Session đầu tiên là session **điều phối**: dán lời giao việc "Root" trong `<gói>/claude/khoi-dong-lai.md`. Session điều phối đọc bảng phân công rồi mở lại các session con bằng các lời giao việc còn lại trong file đó, mỗi mảng một session, giữ tiền tố `[L1]`, `[L2]`, `[Chung]`.

Mỗi session con bắt đầu bằng việc đọc ghi chú tiếp tục của mảng mình (danh sách ở mục 8) và `git log`, rồi làm tiếp từ chỗ đã dừng.

## 8. Tình trạng lúc dừng (10/11/2026)

| Mảng | Đã xong | Còn lại | Ghi chú tiếp tục |
|---|---|---|---|
| [L1] Nội dung và âm thanh TV1 | - Tập 1 và tập 2 đủ bài, tranh, clip.<br>- Rà soát thanh hỏi, ngã: 231 mã đã sửa.<br>- Thanh nặng và âm ê: 116/390 mã đã có bản mới. | - Còn 274 mã thanh nặng và âm ê, trong đó có mụ, nụ, đàn, một, câu "bé, bá cổ bà." Cấu hình sẵn trong `content/tts/settings.json`, script ở `tools/scripts/regen_runner.py`.<br>- 2 câu khó: ghép sau khi có "một", "đàn". | `docs/superpowers/notes/2026-11-05-tiep-tuc-tv1-tap-2.md` (mục 0) |
| [L1] Tranh động lớp 1 | 343 clip; 12 clip làm lại | Chờ duyệt | `docs/superpowers/notes/2026-11-10-tiep-tuc-tranh-dong-lop-1.md` |
| [L2] Nội dung TV2 tập một | - 133 mục, màn mới.<br>- Âm thanh 1.623/3.334 mã riêng lớp 2 (00d77f4). | - 1.711 mã âm thanh: chạy `python tools/lop2/tieng_doc_lop2.py --ghi`, rồi `python tools/lop2/tts_lop2.py 4 172 304 --giu-may-thuc`.<br>- Đo và sửa hỏi, ngã.<br>- Đóng gói chung. | `docs/superpowers/notes/2026-11-09-tiep-tuc-tv2-tap-1.md` |
| [L2] Vẽ tranh TV2 | 57 tranh và kí hiệu | Chờ duyệt | `docs/superpowers/notes/2026-11-10-tiep-tuc-tranh-tv2-t1.md` |
| [L2] Tranh động TV2 | 56/57 clip | Clip b299 đã tạo trên Flow (`/u/1`, dự án "Tháng 11 09 - 15:14"), chưa tải. Tải về, thêm 1 dòng `video_manifest` | `docs/superpowers/notes/2026-11-10-tiep-tuc-tranh-dong-tv2-t1.md` |
| [Chung] UI | Tủ sách, 3 bìa mới, tên "Bé tập đọc 1/2/3" | Chờ duyệt bìa, "test all" | `docs/superpowers/notes/2026-11-09-tiep-tuc-tu-sach.md` |

Số liệu chính xác lúc dừng xem trong từng ghi chú tiếp tục và mục cuối của lịch sử công việc.

## 9. Việc chờ chủ dự án

1. Duyệt trong tool duyệt (`MoCongCuDuyet.cmd`), chọn ô "Sách" theo từng quyển:
   - âm thanh lớp 1 đã sửa: các mã ghi chú "chờ nghe xác nhận", nhất là 83 câu chèn dấu phẩy;
   - tranh và clip lớp 2;
   - 12 clip lớp 1 làm lại;
   - 3 bìa mới.
2. Tải gói media mới lên Drive.
3. Bản đồ bài 97 (TV1 tập 2) đang là ảnh tạm cắt từ scan, phải vẽ lại trước khi phát hành.
4. Nói "test all" khi muốn chạy toàn bộ test.
5. Trước khi đăng app: chọn mã gói và tra nhãn hiệu "Bờ A Ba".
