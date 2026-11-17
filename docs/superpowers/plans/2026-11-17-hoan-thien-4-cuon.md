# Hoàn thiện 4 cuốn SGK — kế hoạch điều phối (17/11/2026)

Root (session điều phối) giữ kế hoạch này và cập nhật khi xong từng mảng.

## Mục tiêu

Ngày 17/11 chủ dự án giao: làm ra một sản phẩm hoàn chỉnh (chưa đăng lên chợ ứng dụng) để chính chủ dự án dùng thử như người dùng.

Sản phẩm có đủ 4 cuốn:
- Tiếng Việt 1 tập 1 (`tv1_t1_1990`, "Bé tập đọc 1");
- Tiếng Việt 1 tập 2 (`tv1_t2_1996`, "Bé tập đọc 2");
- Tiếng Việt 2 tập 1 (`tv2_t1_2001`, "Bé tập đọc 3");
- Tiếng Việt 2 tập 2 (`tv2_t2_2002`, "Bé tập đọc 4", chưa làm).

## Quyết định của chủ dự án (17/11)

- **Bản dùng thử:** bản build Windows.
- **Thứ tự:** làm xong ba cuốn đang làm, rồi mới tới cuốn tiếp theo. Mọi thứ phải hoàn chỉnh, kể cả tranh động.
- **TV2 tập 2:** được chạy song song ngay (chép bài, vẽ tranh, âm thanh). Clip làm khi đã có tranh.
- **ChatGPT:** được dùng vẽ bất kỳ ảnh nào khi cần, kể cả khung đầu clip có người đứng xa hơn. Video vẫn chỉ làm bằng Google Flow.
- **Test:** chức năng hay thiết lập của cuốn nào đã chốt xong thì không test lại. Chỉ test phần có thay đổi hoặc bị ảnh hưởng, kể cả trước bản build giao chủ dự án (chủ dự án nói 17/11).
  - "Test all" chỉ chạy khi thay đổi chạm mã dùng chung.
  - Test phải im lặng. PlayMode đã tắt tiếng sẵn bằng `MuteAudioDuringTests`.

## Hiện trạng (17/11 sáng)

- **Bài:** 304 bài trong 3 cuốn.
- **Âm thanh:** 8.099 mã, đủ file; 371 `dat`, còn lại `cho_duyet`.
- **Tranh:** 431 tranh; 57 `dat`, 374 `cho_duyet`.
- **Clip:** 400 dòng; 243 `dat`, 15 `cho_duyet`, 142 `khong_dat`.
  - 142 clip `khong_dat`: TV1 T1 54, TV1 T2 74, TV2 T1 14.
  - Còn các clip L1 làm ngày 16/11 đang chờ ghi vào danh mục.

## A. Ba cuốn đang làm

### A1. Clip làm lại

**L1 tranh động** (`local_fdaead13…`) — TV1 tập 1 và tập 2:
- Các clip `khong_dat`.
- 6 clip đã dừng sau 3 lần: b82 con kênh, b82 học sinh, b105 cầu trượt, b105 rước đèn, b101 mèo đuổi chuột, b68. Mỗi clip được thêm 3 lượt; khung đầu có thể vẽ bằng ChatGPT.
- Hàng đợi tập 2 mục 7: b111, b110 quê ngoại, b112 bé loắt choắt, b142.
- Làm lại b114, b137, b141, b136.

**L2 tranh động** (`local_d1b0f2bf…`) — TV2 tập 1:
- 14 clip `khong_dat`;
- hàng đợi b198, b173, b188, b203, b209…

**Quy tắc clip:**
- Theo `content/style/tranh_dong_huong_dan.md`, quy tắc 9–17.
- Soi từng khung trong 0,25 s cuối của mỗi clip.
- Root xem trước mọi clip trước khi ghi danh mục.

### A2. Âm thanh đợt 3 — L1 nội dung (`local_1af66fbb…`)

Khoảng 35 câu hỏi TV1 tập 2 đọc tên âm, tên vần theo chữ cái (ví dụ "âm r" thành "e-rờ", "âm ch" thành "cờ hờ").
- Chữ đọc phải theo quy ước của mã `am_*`: "âm rờ", "âm chờ"… Tên vần ghép từ file `van_*`.
- Làm bản thử, root nhận dạng giọng nói, rồi mới cài.

### A3. Tranh — root

Bản đồ bài 97 (`img_b97_banr_ddoof_vieetj_nam`) đang dùng ảnh cắt từ scan. Root vẽ lại bằng ChatGPT, vì scan không được đưa vào app.

### A4. Giao bản ba cuốn

Thứ tự:
1. Media bổ sung (`run_unity_media.py bosung`).
2. Test phần có thay đổi (không test lại phần đã chốt).
3. Build Windows.
4. Gửi chủ dự án kèm danh sách cần nghe, xem.

## B. Tiếng Việt 2 tập 2 (song song)

Theo quy tắc mỗi cuốn có bộ session riêng, cuốn này có 3 session mới:

| Session | Việc |
|---|---|
| `[L2T2] Làm SGK Tiếng Việt 2 tập 2` | Sắp lại trang scan (thứ tự ảnh bị xáo, xem `docs/source-inventory/BOOK_CATALOG.md` mục 4), lập mục lục, viết spec và plan theo mẫu TV2 tập 1 (`docs/superpowers/specs/2026-11-09-tv2-tap-1-design.md`, `tools/lop2`), chép bài theo đợt, âm thanh HoaiMy, đóng gói |
| `[L2T2] Vẽ tranh Tiếng Việt 2 tập 2` | Tranh ChatGPT (Kiet_1), nhận danh sách theo đợt từ session nội dung |
| `[L2T2] Tranh động Tiếng Việt 2 tập 2` | Clip Flow; mở khi đã có tranh và có lượt trình duyệt |

- **Số bài, mã:** tiếp nối sau bài 304, mã `tv2_t2_bNNN`, `book` là `tv2_t2_2002`. Bìa mới "Bé tập đọc 4" do [Chung] UI làm.
- **Âm thanh:**
  - giữ `keep_first` cho tiếng lẻ;
  - đo hỏi, ngã;
  - root nhận dạng giọng nói, đối chiếu ở mức từ;
  - chỉ một tiến trình tạo giọng trên máy tại một thời điểm.

## Trình duyệt và Flow

- Chỉ dùng Edge trên máy này: `407cb8a9-94ae-4bdc-a1d0-2f0c6c933a58`. Không dùng máy khác, không dùng `switch_browser`. Xong việc thì đóng tab.
- Tại một thời điểm chỉ một session chạy Flow. Root xếp lượt.
- Nhịp Flow:
  - mỗi lần tạo cách nhau ít nhất 6 phút;
  - đổi tài khoản thì nghỉ ít nhất 20 phút;
  - không dùng `/u/0`;
  - gặp "unusual activity" hay CAPTCHA thì dừng.
- Session vẽ ChatGPT được chạy cùng lúc với một session Flow, mỗi bên tab riêng. Nếu thấy trục trặc thì chạy lần lượt.
- **Credit:** một video Veo 3.1 Lite tốn 10 credit; `/u/1` còn 50 credit (16/11). Số liệu ngày 17/11:

| Tài khoản | Credit | Nạp lại | Session dùng |
|---|---|---|---|
| /u/2 | 810 | 15/12 | L1 |
| /u/3 | 50 | mỗi ngày 13:44 | L2 |
| /u/4 | 50 | 29/11 | L1 |
| /u/6 | 50 | 1/12 | L1 |
| /u/1 | 50 | — | L2 |

Cần khoảng 380 video nên credit thiếu. Chủ dự án chọn **chờ nạp lại**, không mua thêm.
- Ưu tiên clip của 3 cuốn đang làm; clip TV2 tập 2 làm khi có credit.
- /u/3 phải dùng hết trước 13:44 mỗi ngày.

## C. Giao bản cuối

Khi TV2 tập 2 xong:
1. Media bổ sung.
2. Test phần có thay đổi (không test lại phần đã chốt).
3. Build Windows có đủ 4 cuốn.
4. Danh sách duyệt cuối gom một lần.
