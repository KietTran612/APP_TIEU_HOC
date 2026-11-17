# Lịch sử công việc — dự án "Bờ A Ba"

Ghi lại những gì đã làm xong, theo ngày, mới nhất ở trên cùng. Session điều phối (root) cập nhật file này mỗi khi một session báo xong một phần việc, sau khi đã kiểm tra commit và file thật. Mỗi mục ghi:
- ai làm, làm gì;
- commit;
- test đã chạy;
- việc còn dở.

Phân công hiện tại xem ở [phan-cong-session.md](phan-cong-session.md). Chi tiết từng mảng xem các ghi chú `*-tiep-tuc-*.md` cùng thư mục.

---

## 17/11/2026

Chủ dự án giao mục tiêu: sản phẩm hoàn chỉnh đủ 4 quyển (TV1 tập 1–2, TV2 tập 1–2), bản Windows, chưa phát hành. Kế hoạch điều phối: [2026-11-17-hoan-thien-4-cuon.md](../plans/2026-11-17-hoan-thien-4-cuon.md) (0b09025, ef43c53, ac88bae, c5e8370).

- **[L2T2] nội dung, mở mới:** đủ 130 mục 305–434, tuần 18–33, quyển 4 "Bé tập đọc 4".
  - Dữ liệu và trang sách: f285c84, e9f837c, 005b828, f9b4fd5, 391c59f, 7734544, 2dce7fa.
  - Công cụ âm thanh lớp 2: chọn tập bằng `--t2` (f95f92b); bản thử ngoài danh mục (9e6c06f); bỏ ngoặc kép giữa câu trong chữ đọc (b375f3e).
  - Giọng đọc đợt 1 (305–338): đủ 904 mã. Root nhận dạng xong: 445 khớp, 381 nghi sai, chờ so giọng NamMinh. Đợt 2 đang chạy.
  - Test build đủ 4 quyển (a9ebed8).
- **[L2T2] vẽ tranh, mở mới:** 30/41 tranh ChatGPT qua ba đợt, root duyệt đạt (c43837b, 1a2b65b, f7cb4e8). Còn 11 tranh làm 18/11. Bìa Bé tập đọc 4 (216e923).
- **[Chung] UI, nâng cấp 5 đợt theo nghiên cứu:**
  - Spec: bd6dc1d, ba2f1f3.
  - Các đợt: đợt 1 8b2b988; đợt 2 3d95ef7; đợt 3 9a3d2a3, 50ba2e0, f18a00b; đợt 4 a28adcb; đợt 5 4adb92d, aa92c7d.
  - Root chạy lại test từng đợt, đều đạt, và xem ảnh 4 khung màn hình. Không chạy MvpEndToEndTests (đi hết 434 bài, quá 40 phút).
  - Còn chờ 3 tranh ChatGPT (root vẽ 18/11).
- **[L1] nội dung:**
  - Âm thanh đợt 3: 19 câu "âm X" (ce277f0), 34 câu "vần X" ghép van_* (377670f, 97ca7a3). Join nhận phần "doc:" (c89b1cc).
  - 7 mã tiếng UI (48930be). hd_nghi_mat đọc "chút, nhé" vì "nhé" sau tiếng sắc cao lên quá yếu.
  - CliTest không phụ thuộc media (7d083e4).
- **[L1] tranh động (Flow /u/2):** 33 video. Sau khi root soát còn 14 clip chờ duyệt.
  - Root trả lại 6 clip: b105 rước đèn, b110 quê ngoại, b112 (đi quá tư thế tranh); b101, b68, b141 (a190791, de78c18).
  - Dừng chờ chủ dự án chọn: b82 ×2, b105 cầu trượt, b136, b110 mũi khoan, b114.
  - Commit: e44e2eb, fff836d, b67b2f8, 319542e, f46c9fd.
- **[L2] tranh động (/u/1, /u/3):**
  - Chờ duyệt: b203, b209, b279, b227, b236, b188.
  - b219 trả lại, b198 dừng.
  - Commit: 7e59ac2, b8d0508, 7da8ffa, e374c83.
- **Root:**
  - Vẽ lại bản đồ b97 bằng ChatGPT (35e538f). Clip b97 lần 3 chỉ cho sao Hà Nội sáng, các đảo đủ ở mọi khung.
  - Quy tắc tranh động mục 11 (6609b60, 22cf55c, 71e73f1, c5ee273, 53fa7cc): người đi tới nơi ở giây thứ sáu, hai giây cuối đứng yên; khung đầu chỉ lùi 80–85%; đồ vật nhỏ chỉ cho ánh sáng chuyển động.
  - Tìm ra lỗi ngoặc kép giữa câu làm HoaiMy chèn tiếng, ở cả 3 sách, khoảng 95 mã (QUY-TRINH §12, 79bf5cb).
  - Nguyên tắc tạm ngưng khi usage 5 giờ từ 97% trở lên (7797a7d, 2c74b23).
- **Còn dở:**
  - TV2 tập 2: âm thanh đợt 2–4, tranh còn 11, clip chưa làm.
  - Tạo lại các mã có ngoặc kép giữa câu ở TV2 tập 1 và lớp 1.
  - 3 tranh UI.
  - Gói media bổ sung.
  - Bản Windows.
  - Danh sách duyệt cuối cho chủ dự án.

## 16/11/2026

- **Root:** nhận dạng giọng nói hai vòng cho âm thanh đợt 2 (250563c).
  - [L1] sửa 18/46 mã (dba3d26), trả bản gốc 2 mã đồng âm gì/dì (cd546fa).
  - [L2] sửa 26/49 mã (6b8a563, adc78a0).
- **[L1] tranh động:** đợt /u/6 và /u/2 (7ac1fae, e44e2eb).
- **[L2] tranh động:** bỏ chữ "lề giấy", "mép tranh" khỏi lời lệnh (9a33ca1, 69dffcb).
- 14–15/11 không có commit.

## 13/11/2026

- **Root soát lại 347 clip đã đạt:** 104 nặng, 154 nhẹ, 89 ổn.
  - Báo cáo ở 2eafe3b.
  - Chủ dự án duyệt chuyển 104 clip nặng về khong_dat (2744d08): [L1] 91 clip (kịch bản e52dddf, c10a0ad), [L2] 13 clip (adcf409).
  - Lỗi công cụ xem clip (máy chủ không hỗ trợ Range): 33 bảng dính khung 0s, đã tạo lại. Ghi ở QUY-TRINH §12 (bb4718a).
- **Tranh động, tối đa 3 lần mỗi clip.** Root xem trước từng clip, phóng to chỗ dễ lỗi.
  - [L2], tài khoản /u/1: nhận b220 ngôi nhà, b235 Minh chạy kiểu chạy vòng (d72779c); b198 hỏng 2 lần.
  - [L1], các tài khoản /u/6, /u/2, /u/3, /u/4: nhận 9 clip (b50 cô Tấm, b102 chuông, b102 vịt, b83 lò gạch, b86 vấp đá, b81 quả chanh, b87 búp măng, b105 lướt ván…; 54f5b4e, 3fecb77, 94d37a7, 7d7ccdf, 5bf38a1).
  - [L1] dừng 6 clip chờ chủ dự án chọn hướng: b82 con kênh, b82 học sinh, b105 cầu trượt, b101 mèo, b105 rước đèn, b68.
  - Bài học ghi ở QUY-TRINH §12 (f1b88d8): Nano Banana cần số đo cụ thể; tranh vẽ giữa bước chạy thì cho chạy vòng; một clip một việc lắp.
- **Root soát âm thanh 8.099 mã** (de92601, 0816ac2): kỹ thuật, chữ đọc, thanh điệu, ngữ điệu.
  - [L1] nội dung sửa:
    - 6 mã lỗi chắc chắn; sửa keep_first cắt trên PCM và lỗi Media Foundation cắt mất đuôi (98b6fa0, test 63/63);
    - 7 mã ghép tiếng (4443454);
    - đợt 1, 71 mã: 49 đổi, 22 giữ bản cũ chờ nghe (ac68c8d).
  - [L2] nội dung sửa cau_b264_05 (nằm trong df3f07d) và 21 câu có "..." (ea993b0).
  - Root đo lại độc lập sau mỗi đợt, khớp báo cáo.
  - Cài faster-whisper large-v3 vào môi trường riêng trong scratchpad để nhận dạng giọng nói. Bỏ qua tiếng lẻ (máy nghe không đáng tin).
- **Chủ dự án quyết:** clip chỉ làm bằng Flow (không ffmpeg, không ghép giọng); cho tải mọi clip làm lại; root là người quản lý, tự kiểm hết rồi mới báo.
- **Việc còn dở:**
  - Nhận dạng 4.914 mã nhiều tiếng xong 2.767, chạy tiếp 16/11, rồi giao sửa đợt 2.
  - Gói bosung cho khoảng 85 mp3 mới và các clip mới.
  - Chưa push.

## 12/11/2026

- **Chủ dự án:** dặn gửi clip chậm (≥6 phút mỗi lần tạo, đổi tài khoản nghỉ ≥20 phút). Root xem trước mọi clip mới, clip nào lỗi thì trả lại session làm lại trước khi tới tay chủ dự án.
- **Chủ dự án duyệt:**
  - 286 đạt, 60 không đạt (root commit 0b1f947);
  - 9 clip làm lại trong ngày: 7 đạt, cô Tấm và lò gạch không đạt (8cd592b).
- **Chủ dự án quyết:** clip chỉ làm bằng Google Flow, không ghép tiếng bằng ffmpeg hay HoaiMy, không dùng công cụ chưa được cho phép. Kịch bản cô Tấm để Veo tự đọc bài thơ (d0c1347).
- **[L1] tranh động:** làm lại 12 clip trên /u/6, /u/1, /u/3, /u/2 (268e869, 124f0b6, a98edb8, 302e6bc). Cả ngày không gặp "unusual activity".
  - Root xem trước và trả lại 7 clip vì: hoa ra thành chùm như nho, đi quá chỗ, máy quay chạy theo nhân vật, mẹ biến mất, trẻ mọc đuôi mèo, vịt chồng hình, khúc gỗ đi vào từ vùng đệm.
  - [L1] đưa 7 clip đó về không đạt (e356984, cbc8687, 7a83ad6) và thêm quy tắc 9–10 vào hướng dẫn.
- **[L2] tranh động:** trên /u/3 nhận b299 én đậu dây điện và b283 chim chiền chiện. Root xem trước: đạt (ad4c3f9). Bản b283 lúc 14:13 bị root trả vì vệt trắng. [L2] tự bỏ b235 (Minh đổi quần áo) và b220 (khói, cánh hoa).
- **Root:**
  - soát 43 clip không đạt, ghi lỗi bất hợp lý và cách làm lại từng clip, đề xuất quy tắc 11–16 (5116b8d, 4cb5275);
  - ghi 2 bài học vào QUY-TRINH §12 (de9e167): nhắc tên vật trong lời lệnh, kể cả câu cấm, làm Veo vẽ chính vật đó; so màu lề giấy của khung đầu với tranh gốc.
- **[L1] tranh động:** thêm quy tắc 11–17 vào hướng dẫn, sửa 41 kịch bản theo báo cáo soát (55bf4f0, 40aab10, 1fc949e, a42a128).
- **Credit cuối ngày:** /u/1, /u/3, /u/4, /u/6 hết; /u/2 còn 3.
- **Ngày 13/11:** [L2] chạy trước trên /u/1 (b235, b220, b198). Sau đó nghỉ 20 phút, [L1] làm hàng đợi khoảng 49 clip trên /u/6, /u/3 (sau 13:44), /u/2.
- **Việc còn dở:**
  - Hơn 20 commit chưa push.
  - Chỉnh sửa duyệt âm thanh và tranh chưa commit.
  - Gói bosung cho clip mới làm sau.

## 11/11/2026

- **[L1] nội dung:**
  - tạo lại `tieng_muj` bằng "mụ, già." + keep_first, vì bản cũ bị cụt (1619f07). Chờ chủ dự án nghe lại.
  - Đưa từ trong ▨ Em viết của 7 bài Ôn tập (b07, b11, b17, b22, b27, b32, b37) vào thành mục đọc (7461625). 7 mã âm thanh mới đang `chua_co`, tạo sau khi [L2] tạo giọng xong.
- **[L2] nội dung:** tạo giọng lớp 2 (c887a8d, còn chạy nền). Đo thanh hỏi, ngã 1.008 mã: 17 mã đọc sai (phần lớn chữ "tả"), 4 mã có thể sai. Sẽ sửa sau khi tạo xong.
- **Chủ dự án duyệt clip tập 1 (bài 21–80):** 49 đạt, 27 không đạt. Root giao [L1] tranh động làm lại.
- **[L1] tranh động:** làm lại 15/27 clip.
  - 17f2366 (/u/1): voi, chó xù, trâu, lợn, mèo. Thêm 4 quy tắc vào `tranh_dong_huong_dan.md`: không tua ngược ở cuối; đi hoặc bay phải rời chỗ thật; con vật có tiếng kêu; cây lớn đúng thực tế.
  - 15c77c9 (/u/6): 10 clip.
  - 1265676: ghi chú tiếp tục, kịch bản 12 clip còn lại.
  - Root đã kiểm: đúng 15 dòng `video_manifest` đổi, về `cho_duyet`, ghi chú giữ lý do cũ.
  - /u/2 báo "unusual activity" cả 5 clip (không mất credit). Root cho dừng gửi trong ngày. Ngày 12/11 thử 1 clip trên /u/4, mỗi clip cách nhau ít nhất 1 phút.
- **[L2] nội dung:** âm thanh lớp 2 xong 3.321/3.321 mã (b26949d, ghi chú 379aeb7). Đo hỏi/ngã 1.511 mã: 18 sai, sửa 17 (đọc chậm 20%, ghép mượt, "X, X." giữ tiếng đầu); còn vài mã chờ chủ dự án nghe. Root đã kiểm: commit chỉ đổi 1.631 dòng và 268 override của lớp 2.
- **[L1] nội dung:** tạo giọng 7 từ Em viết (bb6c51f), đọc nguyên cụm −15%. Validate không còn `chua_co`.
- **[L1] tranh động:** thêm 5 clip trên /u/4, gửi cách nhau khoảng 3 phút, không bị chặn (1a09bed); tập 1 xong 20/27. Kịch bản 32 clip tập 2 (a3deb34) và cái cuốc (843d9a9).
- **Root:** vẽ lại tranh cái cuốc b101 (60ef3a9). Chạy Unity nền tạo 1.704 file `.meta`, rồi `run_unity_media.py bosung`: `dist/TapDoc-bosung-2026-11-11.zip` 95 MB (1.704 mới, 152 đổi, 21 clip), khoá media 0d6084d. `validate` (không `--allow-missing`) OK. Gói bản cập nhật chuyển máy 11/11 (xem CHUYEN-MAY-MOI.md mục 0).
- **Chủ dự án duyệt thêm clip tập 2 (bài 81–148):** 32 clip cần làm lại, giao [L1] tranh động sau 12 clip tập 1 còn lại. Thêm hai quy tắc: lời trong clip chỉ tiếng Việt; máy quay không lia lung tung. Tranh `img_b101_cais_cuoocs` bị chê, phải vẽ lại tranh trước rồi mới làm clip.

## 10/11/2026 (chiều) — làm tiếp trên máy cũ

Chủ dự án cho làm tiếp các việc dở trong bảng B11 trước khi chuyển máy. Phần mới sẽ đưa lên Drive bằng gói bổ sung.
- **Root:** thêm lệnh `run_unity_media.py bosung` (ca1edeb). Lệnh chỉ gói tranh, âm thanh (kèm `.meta`) và clip đổi so với khoá. `unpack --bosung` nhập gói bổ sung sau gói chính. Test `test_run_unity_media`, `test_media_lock`: 20/20 đạt.
- **[L2] tranh động:** chủ dự án cho tải. Clip b299 (đường dây điện) đã vào `content/clips`, 1280×720, 7,9 giây (d553b83). TV2 tập một đủ 57/57 clip, tổng 400 clip. Chờ duyệt.
- **[L1] nội dung:** xong đợt thanh nặng, âm ê và 2 câu khó (68a4ed7). Root đã kiểm: đúng 392 dòng `audio_manifest` đổi, đều `cho_duyet`.
  - Có 120 mp3 thật sự đổi, danh sách ở `tools/scripts/l1_mp3_doi_1011.txt`.
  - 272 mã đọc "X. X." + keep_first ra file trùng từng byte với bản cũ, vì edge-tts tạo từng câu riêng. Đã ghi vào QUY-TRINH mục 12.
  - Còn khó: ạch, ặp, kịch, sạch (máy không đo được thanh nặng ở tiếng lẻ). Nếu nghe vẫn sai thì đặt vào ngữ cảnh (ví dụ "nụ hoa.") rồi keep_first.
- **[L2] nội dung:** chuẩn bị 1.718 mã; bắt đầu tạo giọng sau khi [L1] xong.

## 10/11/2026

**Root:** chủ dự án cho tạm dừng mọi session để chuyển sang máy mới.
- Mọi session dừng ở điểm sạch: không còn tiến trình tạo âm thanh, không file ghi dở.
- Mỗi session commit ghi chú tiếp tục và chép script từ scratchpad vào repo.
- Root viết `CHUYEN-MAY-MOI.md` và đóng gói `BoABa-chuyen-may-2026-11-10/`, gồm: bundle git, chỉnh sửa duyệt chưa commit, gói media mới, thư mục ngoài git, toàn bộ dữ liệu Claude (bộ nhớ, hội thoại, scratchpad).

Commit cuối của từng session:
- [L2] vẽ tranh: 7b2bd98;
- [Chung] UI: eca64b8 (4 ảnh bìa và biểu tượng chỉ có trên máy cũ, vào gói media mới);
- [L2] tranh động: 6a1c5dc (b299 đã tạo trên Flow, chưa tải);
- [L1] tranh động: dc16bb1;
- [L2] nội dung: 00d77f4 (1.623 mã âm thanh lớp 2), e41051a (script `tools/lop2/`);
- [L1] nội dung: 9286c56 (thanh nặng và ê 116/390, script `tools/scripts/`).

## 09/11/2026

**Root — điều phối**
- Gom kết quả duyệt của chủ dự án và giao sửa theo mảng: 32 âm thanh và 12 clip tập 1 bị chấm "không đạt".
- Tự vẽ lại tranh cử tạ bài 13 thành vận động viên người lớn (7f13b2a).
- Lập 3 session mới cho Tiếng Việt 2 tập 1; đặt tiền tố [L1]/[L2]/[Chung] cho tên session.
- Viết bảng phân công session: d5a1a01, 6d226aa, e109ade, bf60ae0, 7e99565.

**[L1] Làm SGK Tiếng Việt 1 tập 2** (`local_1af66fbb…`)
- Chốt tập 2:
  - 2 âm thanh cuối (8a6a7b4); bài 97 build lại với ghi chú bản đồ tạm (210cc1c);
  - `validate` không lỗi;
  - gói media `TapDoc-media-2026-11-09` và `TapDoc-clips-2026-11-09` (746792b), chờ chủ dự án tải lên Drive.
- Sửa âm thanh:
  - thêm cách đọc lặp "X, X." rồi giữ tiếng đầu (`keep_first`) cho tiếng lẻ (1b3623c, 9a1171f);
  - tạo lại 30/32 mã bị chê. Chủ dự án nghe lại: 21/30 đạt, toàn bộ 18 tiếng thanh hỏi, ngã đều đạt.
- Rà soát toàn bộ thanh hỏi, ngã, phần tiếng lẻ:
  - đo 268 tiếng, 92 nghi sai, đã sửa đạt mẫu 92/92;
  - áp `keep_first` cho 138/142 tiếng hỏi, ngã còn lại.
  - Bản cũ để trong `prev`, danh mục chưa commit (chờ chủ dự án duyệt).
- Làm trang nghe thử 8 mã khó (thanh nặng, ê mang thanh sắc, "hờ", "bé bá cổ bà", "tổ dế"): `.superpowers/nghe-thu/index.html`, chờ chủ dự án chọn.
- Sửa dữ liệu tập 2: danh mục âm thanh dùng lại 87 mã có sẵn (98880eb); test `Index_EntriesNameTheirBook` (3effd2c).
- Rà soát hỏi, ngã trong từ, câu, lời dẫn:
  - Cách đo: tạo lại với thông số cũ để lấy mốc từng tiếng (`content/tts/marks/`), chấm theo tiêu chí hiệu chỉnh trên các mã `dat`.
  - Cách sửa: chỉ đọc chậm hơn 20%, không đổi chữ.
  - Kết quả (số mã / nghi sai / đã sửa đạt / còn khó): câu 447 / 98 / 35 / 63; từ 251 / 28 / 12 / 16; lời dẫn 73 / 15 / 5 / 9; lời khen 2 / 1 / 1 / 0.
  - Mã `dat` bị nghi: `hd_b18_tranh_01` ("quả"), không đụng.
  - Tiếng lẻ hỏi, ngã: đã cài `keep_first` cho 233 mã; riêng "cải", "phải" giữ bản cũ.
  - Danh sách 88 mã cụm còn khó: `side-session-notes/…/hoi-nga-cum-con-nghi-2026-11-09.tsv`, chờ chủ dự án chọn cách đọc trên trang nghe thử.
- Cài theo lựa chọn của chủ dự án ở trang nghe thử vòng 1 (cả 5 mã ở `cho_duyet`):
  - bạ: "bạ. bạ.";
  - ế: "ế, ế, ế.";
  - tế: "tế, tế." đọc chậm −40%;
  - hờ: "hờ. hờ.";
  - tổ dế: ghép hai tiếng đã đạt.
- Ghép mượt (f6c01f1, có unit test): cắt lặng, cân âm lượng, nghỉ 0,08 giây, dấu phẩy 0,25 giây, mã hoá lại MP3. Mục 6 và 12 của quy trình đã cập nhật.
- Trang nghe thử vòng 2 (`.superpowers/nghe-thu-2/`): mụ, nụ, "bé bá cổ bà."; chờ chủ dự án chọn.
- **Còn dở:**
  - 88 mã cụm hỏi, ngã còn khó đã xử lý: 83 mã dùng ngắt nhẹ (thêm dấu phẩy sau tiếng bị nghi, đo đạt), 3 mã ghép (`tu_choox_owr`, `tu_gox_mox`, `tu_mux_len`). Root kiểm tra thì thấy dấu phẩy có chỗ đặt giữa cụm từ ("ngoài đảo, xa", "giữa, trời xanh"), cần chủ dự án nghe xác nhận. Còn 2 câu (`cau_b97_02`, `cau_b160_04`) chờ kết quả thanh nặng.
  - Tổng kết hỏi, ngã (số mã / nghi sai / đã sửa): tiếng 268 / 92 / 92; câu 447 / 98 / 96; từ 251 / 28 / 28; lời dẫn 73 / 15 / 14; lời khen 2 / 1 / 1;
  - rà âm ê (879 mã; máy không đo được lỗi nguyên âm, chờ chủ dự án chọn trên trang nghe thử);
  - thanh nặng (288 tiếng lẻ).

**[L1] Tranh động lớp 1** (`local_fdaead13…`)
- Làm lại 12 clip tập 1 bị chê, cả clip cử tạ theo tranh mới. Kịch bản: b4d5ed4, 5a12fdb. Clip ở trạng thái chờ duyệt, chưa đóng gói Drive.

**[L2] Làm SGK Tiếng Việt 2 tập 1** (`local_8c04ba54…`)
- Spec và plan được duyệt: 23311a1, 9478423.
- Công cụ:
  - quyển lớp 2, tắt đánh vần (4099a87, 8df282f);
  - lệnh `tapdoc pitch` và cờ `tts --tieng-keep-first` (753004a, sửa 90fbf81, 9678b22);
  - 3 bước mới (ff7519e, 38d19d1).
- Unity:
  - thẻ Lớp 1/Lớp 2, mở khoá theo lớp (39ead72);
  - màn ghép chữ, điền đoạn, chọn dòng (f1ae593);
  - sửa cỡ chạm tối thiểu (a9c22b8), xáo thẻ điền đoạn (eeac040).
- Nội dung: đủ 133 mục 172–304, tuần 1–17 (081c868, 089718c, 92f6df4, f92809b, edbb6e4, 0b810e9, 6859d2c).
- Test:
  - Python liên quan đạt; test hồi quy 171 mục lớp 1 đạt;
  - smoke test 133 mục 4/4 đạt; PlayMode lọc đạt;
  - EditMode 158/159 (còn `AllReferencedAssetsExist`, chờ tranh và âm thanh).
- **Còn dở:** âm thanh khoảng 3.300 mã (đang tạo, khoảng 8 mã/phút); review code độc lập; đóng gói media.

**[L2] Vẽ tranh Tiếng Việt 2 tập 1** (`local_be5a6177…`)
- Đợt L2-1: 9 tranh và kí hiệu giải nghĩa (447cf3e).
- Đợt L2-2: 18 tranh (d239be1).
- Đợt L2-3: 18 tranh (d7bbff2).
- Đợt L2-4: 12 tranh (957e711).
- Lớp 2 tập một đủ 57 tranh và kí hiệu giải nghĩa. Root đã kiểm tra: 61 dòng tranh lớp 2 trong danh mục, không dòng nào còn `chua_co`.

**[L2] Tranh động Tiếng Việt 2 tập 1** (`local_d1b0f2bf…`)
- Đợt L2-1 và L2-2 xong: 27 clip (bài 172–230), 1280×720, khoảng 8 giây, có tiếng. Tạo trên Flow /u/6.
- Commit 28fe7be: thêm 27 dòng `cho_duyet` vào `video_manifest.json` và 27 kịch bản. Root đã kiểm tra: đủ 27 file clip, các dòng tập 1 không bị đổi.
- Chủ dự án để ý khi duyệt:
  - b173: vệt mờ ở khung cuối;
  - b189: cánh hoa bay;
  - b209: vật đen nhỏ thoáng hiện.
- Đợt L2-3 và L2-4: 29 clip (a0662f8). Root đã kiểm tra: đủ 29 dòng mới có file clip.
- Lớp 2 tập một có 56/57 clip.
- Chủ dự án để ý thêm khi duyệt:
  - b242: Veo tự thêm bàn tay em bé cầm sáp;
  - b267: cảnh xuân tràn ra ngoài khung vuông;
  - b259: có một khoảnh khắc nhòe.
- Tài khoản Flow /u/3 bị báo "unusual activity" 3 lần.
- Chưa đóng gói Drive.
- **Còn dở:** clip `img_b299_dduwowngf_daay_ddieenj`, chờ credit ngày mai.

**[Chung] UI và hiệu ứng** (`local_98b994e9…`)
- Tủ sách:
  - bản thiết kế `docs/superpowers/specs/2026-11-09-tu-sach-design.md`;
  - luật mở quyển và bài theo quyển, quyển đang mở của mỗi bé (c71d0bb);
  - bìa tạm từng quyển và biểu tượng Tủ sách (992eb8c);
  - màn Tủ sách: chọn quyển, danh sách bài theo quyển (445e91b);
  - học xong quyển thì về Tủ sách, quyển mới mở có hiệu ứng (fedd386);
  - Sổ bé ngoan, Ôn lại và tiến độ Phụ huynh theo quyển (9b7bc49);
  - sửa theo review (30b6622, 04d6e43);
  - 3 bìa vẽ lại theo ý chủ dự án đã vào app, chờ duyệt; ba quyển đổi tên thành "Bé tập đọc 1/2/3"; thêm danh mục ảnh bìa và biểu tượng (916a3ca). Test liên quan 57/57. Ảnh bìa đóng gói cùng lớp 2.
- [L2] rút gọn tên bài Tập làm văn cho vừa thẻ (761444a).

## 06/11/2026

- **Root:**
  - vẽ 25 tranh tập 2 còn thiếu bằng ChatGPT (8c43d12), tập 2 đủ 155/155 tranh;
  - tìm ra cách lấy ảnh qua dữ liệu cuộc trò chuyện khi trang ChatGPT bị treo.
- **[L1] Tranh động:**
  - ghi 129 clip tập 2 bài 81–150 vào danh mục (04cb04b);
  - làm 24 clip đợt cuối (56fdd22); tập 2 có 153 clip.
- **[L1] Tập 2:** âm thanh HoaiMy 2249 mã (9201f56) và 27 mã lượt bù (f591cd6).

## 05/11/2026

- **[L1] Tập 2:** đưa Tiếng Việt 1 tập 2 vào app.
  - Bài 81–125 (Vần) và Tập đọc tuần 27–33: 7b2ad34 … b42061f.
  - Các bước Tập đọc, bảng vần có cột câu; danh sách bài ba phần.
  - Test đi hết 91 mục (a71a5ee).
  - Tranh cắt tạm từ scan cho bản đồ bài 97 (c31e355); bản phát hành bị chặn cho tới khi vẽ lại.
- **Root:**
  - danh sách tranh tập 2 (93486a3, e2bffd8, 08dc42c);
  - nhập 130 tranh tập 2 (b50bb9d);
  - thêm ô chọn Sách vào tool duyệt (5dcc4ed);
  - đặt tên app "Bờ A Ba" (8b8a2f0).
- **[Chung] UI:**
  - tỷ lệ màn hình cách B, co giãn cho điện thoại và máy tính bảng (5b8bd2f … 128728c);
  - màn mở đầu, popup Gửi phụ huynh, menu Cài đặt, đổi/xoá hồ sơ, tắt sao lưu (aed2f50 … 5e26e1d).

## 04/11/2026

- **[Chung] Refactor đọc dữ liệu:** dọn cách app đọc dữ liệu, chuẩn bị Addressables. Gồm nguồn dữ liệu theo loại và mã, AssetCatalog, kho bài có bộ nhớ đệm, màn chuyển gà con khi chuẩn bị bài (574727f … a8ce5bf).
- **Root:**
  - tool duyệt thêm tab "Duyệt theo bài", hiện trang sách gốc cạnh bảng (a24174f … 3bd8daf);
  - lưu các mã âm thanh chủ dự án đã duyệt (a120f18, 951d7f4).

## 02/11/2026

- **Root:**
  - các cách đọc của chữ (đọc khi học, âm chuẩn, tên chữ cái) theo Phụ lục tr.120–122, kèm 24 âm thanh mới và nút trong bài (980255b … 4dd084c);
  - tranh và âm thanh ra khỏi git, chuyển sang gói media trên Google Drive (a34bb21, c373d68, 66da49b);
  - hướng dẫn cài máy mới (0974c2b).
- **[L1] Tranh động:** đủ 190/190 clip tập 1 (092f6e0).

## 30/10/2026

- **Root:**
  - ghi chú cho phụ huynh, mục "Chú ý và Phụ lục" (74ce1ef);
  - sửa cắt MP3 và tạo lại 1.236 âm thanh (e9f1f90, 269ebde);
  - 6 tranh còn thiếu, đủ 199 tranh tập 1 (7808597);
  - vẽ lại tranh cá thờn bơn (f9f0203);
  - duyệt clip trong tool (c1ae6f8).
- **[Chung] UI:** giao diện, hiệu ứng, tiếng động, Sổ bé ngoan, hình giao diện chính thức (24d89a3 … 7c9fbb7); test all đạt.
- **[L1] Tranh động:** hướng dẫn kiểu sáng tạo, kịch bản 190 tranh, 52 clip đầu (2674eb5).

## 29/10/2026

- **Root:** hoàn thành Tiếng Việt 1 tập 1.
  - Bài 1–17 (f792778), 18–41 (fc4510c), 42–64, 65–80.
  - Bảng ôn vần, bảng nhóm vần, câu đố.
  - Công cụ giọng đọc edge-tts HoaiMy và trang duyệt âm thanh.
  - Âm thanh HoaiMy cho bài 1–80; tranh bài 42–80.

## 28/10/2026

- Bản mẫu đầu tiên: bài 4, 13, 42 của Tiếng Việt 1 tập 1 (fc0c75d).
