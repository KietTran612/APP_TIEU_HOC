# Lịch sử công việc — dự án "Bờ A Ba"

Ghi lại những gì đã làm xong, theo ngày, mới nhất ở trên cùng. Session điều phối (root) cập nhật file này mỗi khi một session báo xong một phần việc, sau khi đã kiểm tra commit và file thật. Mỗi mục ghi:
- ai làm, làm gì;
- commit;
- test đã chạy;
- việc còn dở.

Phân công hiện tại xem ở [phan-cong-session.md](phan-cong-session.md). Chi tiết từng mảng xem các ghi chú `*-tiep-tuc-*.md` cùng thư mục.

---

## 25/11/2026

- **Root soát clip kiểu cũ loop (6dd12cb).** Chủ dự án 25/11: ảnh tĩnh chỉ cần là khung đầu hoặc khung cuối để clip không giật; ảnh động phải hợp lý, đúng nội dung.
  - Lọc 239 clip loop đang phát (197 dat, 42 cho_duyet), còn 44 clip có lời nhắc di chuyển. Root xem tờ khung 8 nhịp của cả 44 (loop_soat_01…11.jpg).
  - 22 KHÔNG NHẬN, chuyển khong_dat: đi tại chỗ, bị kéo về chỗ cũ, hoặc đổi nét vẽ giữa chừng. Lý do và cách làm lại (A/B) ghi trong ghi_chu.
  - 18 mã lớp 1 giao L1; 4 mã lớp 2 (b181, b235, b268, b282) giao L2.
  - 22 clip giữ lại: chuyển động tại chỗ tự nhiên, hoặc tàu thuyền lớn có sóng như máy quay chạy theo (b56, b93, b252).
  - Quy tắc mới ghi QUY-TRINH §12: kiểu loop chỉ cho chuyển động tại chỗ; vật di chuyển thì tranh chỉ trùng một đầu clip.
- **Kịch bản làm lại các clip loop, root duyệt từng khung đầu và lời nhắc:**
  - **[L1] (c1c18ed), 18 mã lớp 1:** 14 cách A, 3 cách B "tiếp", b89 giữ loop nhưng sửa câu trăng.
    - Bốn tranh nền trơn (b01, b19, b21, b36) dời chính tranh gốc sang lề làm khung đầu, không qua ChatGPT.
    - Root kiểm commit: đúng 18 dòng, đúng mode, cách B có câu "ở trong ô, không mờ chồng".
    - Lịch: Flow /u/3 từ 26 tới 30/11, mỗi ngày 3 mã cùng 2 mã nhóm 1–3; cách B trên Vids ngày 28/11.
  - **[L2] (a5d988d), b181 và b282:** chuyển sang cách A, làm trên Flow từ 29/11.
    - b235 và b268 làm cách B trên Vids ngày 27/11. Lời nhắc b235 root sửa để Minh vẫn hớt hải chạy vào lớp (đúng bài "Đồ dùng để ở đâu").
- **[L2] tranh động — Vids /u/3 cách B "tiếp", lần 2 cho 4 mã lớp 2 (f2af12b):** Root xem từng tờ khung. Cả 4 KHÔNG NHẬN, vẫn khong_dat:
  - b219: ô tô chui vào gầm xe tập đi;
  - b284: người gánh bước tại chỗ;
  - b250: én to gấp đôi từ 1 s, số con đổi;
  - b173: từ 5 s mọc thêm một bạn ở cửa lớp.
  - Lần 3 (cuối) đặt ngày 27/11 trên Vids /u/4, mỗi clip 5 s, root đã duyệt lời nhắc. Hỏng nữa thì giữ tranh tĩnh.
  - /u/3 còn 4 giây Vids trong tháng 11.
  - Bài học: clip Vids chưa Insert sẽ mất nếu tab rời nhóm; từ nay Insert ngay.
- **Root duyệt 7 mã TV2 tập hai làm cách B:** b340, b341, b395, b364, b332, b404, b405, trên Vids 6 s ngày 26/11, tài khoản /u/4 và /u/6. Root sửa 4 lời nhắc:
  - b405, b364: bỏ chữ số;
  - b404: cá bơi vòng trong ao;
  - b332: sao chổi chỉ đi một đoạn ngắn.
  - Các mã còn lại của TV2 tập hai giữ cách A.
- **Root duyệt 14 mã lớp 1 làm cách B (L1):**
  - Lịch Vids 26/11: /u/1 b60, b62, b69, b88; /u/2 b94, b95, b106.
  - 7 mã còn lại làm ngày 27/11.

## 20/11/2026

- **[L2] tranh động — lượt /u/3 ngày 20/11 (cff3b64, 87cf9dc):** lùi giờ sang 14:35 cho qua lúc usage 5 giờ reset.
  - b274 NHẬN (cho_duyet): root xem tờ khung, hai cô gái đi thật xuống lối mòn, khung cuối lệch tranh 8,2.
  - KHÔNG NHẬN: b284 mọc thêm người gánh (root xem tờ khung); b219, b250, b173 theo mô tả và số đo của L2.
  - Bốn mã hỏng làm lại theo cách B sau khi usage tuần reset (25/11).
- **Root:** cập nhật bảng phân công session theo ngày 20/11 (884ba72).

## 19/11/2026

- **[Chung] Phát tranh động trong app (dc8da76, 12d448c, e7be8e9, e8351af, 8653586, 672bce3, 26a43da, 30916c9):** clip phát ở 4 màn Phần 1 sau khi đọc chữ của tranh, giọng đọc luôn ưu tiên, máy yếu dùng tranh tĩnh, cài đặt "Tranh động", lệnh `run_unity_media.py clips` chép clip dat+cho_duyet vào Resources/clips (ngoài git), cắt thêm 4 điểm ảnh mỗi mép. Soát độc lập: 0 Critical, 3 Important đã sửa có test (52/52 lớp clip), 5 Minor ghi sổ. Root duyệt spec và xem ảnh phone_20x9, ipad_43: đạt. Bản Windows lớn thêm ~0,9 GB.
- **[Chung] UI — 25c81f2:** bảng đọc bài 80 tràn đáy trên iPhone (LessonNotesTests.Notes_PanelFitsAllSizes đỏ từ đợt UI 1): hàng dư thì thu cột nhãn và thẻ dài về vừa chữ. ItemsViewTests 8/8, LessonNotesTests 7/7. Root kiểm: đạt.
- **Tranh động 19/11:** b274 lượt cuối (L2, e82013c) và b115 (L1, 1d57ae6, f372d7d) root nhận; b58 gửi thư lần 2, b119 lần 1 không đạt (0c1cfdf).
- **[L1] tranh động — lượt /u/3 chiều 19/11 (ef2269e, bfe3980, 681f180, 043de45, dddac1a):** đây là lượt cách A đầu tiên.
  - Root xem tờ khung từng clip. b110 quê ngoại NHẬN (cho_duyet): hai bà cháu đi thật từ xa, tới đúng chỗ ở cuối. Điểm trừ: vải của người giặt đổi màu.
  - KHÔNG NHẬN b112 (đá chân, bước tại chỗ), b82 (đứng nghiêm rồi giật về dáng), b105 và b33 (khung đầu chỉ lùi khoảng 10%, đi tại chỗ).
  - Bài học ghi QUY-TRINH §12 (5b305ff, a233711): khung đầu lùi xa; người đang bước thì đi liên tục tới khung cuối. L1 vẽ lại khung lùi xa b105, b33, b112 (root duyệt); bốn mã làm lần 2 ở đầu lượt 21/11.
- **[Chung] Phát tranh động trong app — clip "tiếp" giữ khung cuối (d6a3e65):** chủ dự án cho chọn cách làm clip theo từng tranh (QUY-TRINH §12, f9f6872).
  - Clip có `"ket": "giu"` trong video_manifest thì hết clip giữ khung cuối, không mờ về tranh tĩnh. Danh sách cho app nằm ở Resources/clips/index.json (lệnh `run_unity_media.py clips`).
  - Root tự chạy lại test: Python 39/39, EditMode 17/17, PlayMode 78/78 (ClipPlayer, AssetCatalog, ClipApp, ClipRealVideo, ClipInViews, SettingsScreen).
  - Root đọc diff. Clip không đánh dấu chạy như cũ. Khung giữ nằm trên RenderTexture riêng và được giải phóng khi lớp phủ bị huỷ; bản sao lúc lật trang không chép theo khung đang giữ. Hiện chưa clip nào đánh dấu.
- **Soát lại theo bài học cách A (chiều 19/11):** root duyệt từng tờ khung.
  - **L1:** kịch bản 19 mã nhóm 1–3 cùng 4 mã lần 2 (e80c38e). b65 và b57 vẽ lại cho to khoảng 50–60% (dd79d13, 826b3b4).
  - **L2, 5 mã lớp 2 cho ngày 20/11:** 7fc0e96 và 23d4b0c. b219 vẽ lại vì người anh phải bước sang phải. b250 vẽ lại vì khung đầu có 6 én, tranh gốc 5.
  - **L2, 41 mã TV2 tập hai:** 054d1f0 và fd1dea4. Vẽ lại 8 khung; b315 và b330 vẽ lại lần nữa cho to ít nhất khoảng 55%. Root nhận giữ khung cũ b340, b341, b395, b404.
  - **Ngưỡng cỡ khung đầu ít nhất khoảng 55%:** ghi QUY-TRINH §12 (3cf952f).
- **Root — thử Google Vids lần 2 (chủ dự án chọn "Thử thêm Vids"):** b82 con kênh, clip bắt đầu từ chính tranh gốc. Khung đầu trùng tranh (lệch 14,7). Hai bạn đi thật hết cầu và ở trong tranh, nền giữ ổn. Khung cuối khác tranh (lệch khoảng 22), nên chỉ dùng được nếu app giữ khung cuối của clip; việc này chờ chủ dự án quyết. /u/3 còn 44 giây Vids trong tháng 11.
- **Root — thử Google Vids (chủ dự án cho thử 1 clip):** b112 trên /u/3, Animate 8 giây.
  - Tốt: đi tự nhiên hơn Flow.
  - Không đạt: Vids không có khung cuối, nên clip đi quá ra ngoài tranh, nền tự thêm nhà và cây, khung cuối lệch tranh, góc có dấu ✦.
  - Hạn mức tài khoản cá nhân 60 giây mỗi tháng. Kết luận: clip build vẫn làm bằng Flow. Tờ so sánh ở Downloads/vids_thu/.
- **[L2] tranh động TV2 tập hai — kịch bản và khung đầu đủ 41/41 (d519217, c4450f9, 0c1b485, 4d58e04, 7fe511b, dfc9872, 1641cac):** cách A, hướng di chuyển thật. Root soát tờ so sánh từng nhóm. Đợt vẽ lại 7 khung cho quãng đi đủ dài (b364 hải âu bay vào từ lề phải). b307 thêm câu giữ cỡ cào cào. b397 vẽ lại lần hai: thanh thép từ sát đống cát lên khoảng 1/4–1/3 chiều cao. Chưa gửi Flow; chờ credit /u/1, /u/4 (29/11).
- **Chủ dự án sửa hướng tranh động:** lỗi cần sửa là "cử động mà không di chuyển" → nhân vật phải DI CHUYỂN THẬT (cách A: khung đầu lùi một quãng, tới đúng chỗ tranh ở cuối; được sáng tạo). Cinemagraph giữ người đứng yên là sai; 14 clip như vậy chuyển về khong_dat để làm lại. Quy trình sửa ở ba1536c.

## 18/11/2026

- **[L1] tranh động — ngày 18/11 (57b8d07 … b9d6e0d, df93c0c §15):** 30 clip root xem trước và nhận (b12, b13, b105 rước đèn, b68, b101, b82 con kênh, b15, b20, b24, b25, b26, b28, b31, b33, b34, b35, b36, b43 củ sắn, b43 khăn, b44, b47, b49, b52, b54, b55, b57 chim non, b58 gà mẹ, b58 cái túi, b65 tranh mới, b110 quê ngoại). Tranh tĩnh: b57 con dơi. Hết credit /u/2, /u/3, /u/4, /u/6. Hàng 19/11: cinemagraph lượt cuối cho các mã dừng, b58 gửi thư lượt 2, b115/b119 tranh mới.
- **[L2] tranh động — ngày 18/11 (d2ec938, 36b765f, 013f635, 3fa0398):** b219, b284, b267, b261 (bản lần 2), b198, b250, b173 lượt cuối → cho_duyet; b274 lượt cuối gửi /u/1 18:47.
- **Root — quyết định 18/11:** chủ dự án giao root kiểm tra và duyệt luôn tới khi app hoàn chỉnh; root tự chốt các mục trước để chủ dự án chọn (clip dừng: một lượt cinemagraph cuối rồi tranh tĩnh). Tranh vũ khí: vẽ lại b65 (efbada3), b119, b115 (84a49b5); b252 tàu hải quân chủ dự án chốt giữ nguyên. Đề xuất và duyệt spec phát tranh động trong app (dc8da76, kế hoạch 12d448c, Task 1 e7be8e9).

- **[L2T2] — TV2 tập hai hoàn tất phía nội dung (74d08dc ghi chú resume):** smoke Unity EditMode 37/37 (DataTests, BookShelfTests, LessonRepositoryTests), PlayMode 39/39 (Grade2Tap2LessonSmokeTests 4 tuần-khối, BookScreenTests, ParentScreenTests 12/12, LessonPathTests, LessonListPartsTests); batchmode tạo .meta cho 11253 mp3 + 476 tranh; `tapdoc validate` (không --allow-missing) OK. Root đọc TestOutput và chạy lại validate: đạt. Chỉ còn bosung media cuối ngày.

- **[L2T2] nội dung — âm thanh TV2 tập hai mục 403–434 (đợt 4), 9dfe844:** 710 mã cho_duyet; 37 mã cài bản thử root chọn (30 khớp hẳn gồm 4 mã cao độ tả/xã/Hảo/vả, 7 nghe kỹ); 37 mã giữ bản cũ nghe kỹ. Toàn TV2 tập hai 3147 mã cho_duyet. Root kiểm: đúng tập dot4, 116 override không xoá, 37 mp3 khớp từng byte, phần chủ dự án nằm ngoài.
- **Root — soát âm đợt 4:** nghi 238, NamMinh 166 mã → làm lại 68, nghe kỹ 33, do máy nghe 67, tiếng lẻ 70 (không hỏi/ngã nào ra huyền). Bản thử 149 bản nhận dạng; đệm lặng gỡ câu ảo cau_b406_22. tieng_ix chốt giữ bản cũ (mọi cách đều ra sắc).
- **Root — d7f6842:** update_audio_manifest giữ dấu can_nghe_ky đặt tay khi chữ không đổi ([L2T2] phát hiện); 2 test mới, 991 test Python OK.

- **[L2T2] vẽ tranh — 11 tranh còn lại (b397, b403–b429), c9c0903:** đủ 41/41 tranh TV2 tập hai, cho_duyet/chatgpt_tam. Root soát tờ kiểm tra: đúng nội dung, không vũ khí, không chữ; đủ 11 file; commit chỉ 11 dòng. Chi tiết để chủ dự án xem: b403 vạch nắp lọ mực, b421 Khải Hoàn Môn, b429 đỉnh núi hình đầu ngựa.
- **Root — 3 tranh giao diện bằng ChatGPT (e18c029):** bàn tay chỉ (nền trong suốt, thêm lề để đầu ngón trùng pivot HintHand), cảnh chào sân trường 16:9, cửa sổ nghỉ mắt 4:3 (không vẽ gà con vì mascot đứng trước).
- **[Chung] UI — lắp 3 tranh (e5236ca):** chóp ngón chạm viền elip nội tiếp của đích (nút tròn trước hở ~30 px trên iPad), hướng ngón 138°; cảnh chào phủ kín màn (EnvelopeParent), có tranh thì ẩn nét đất. Test: Hand_FitsAllSizes + Nudge_* 4/4, WelcomeTests 4/4 (1 mới), ProfileScreenTests 9/9, RestAndParentTests 9/9, ParentScreenTests 12/12, IdleNudgeTests 8/8. Root xem ảnh phone_20x9 và ipad_43: đạt.
- **[Chung] UI — 7 mã tiếng mới phát đúng chỗ (3df36c0):** GuideVoiceTests 3/3 (hd_chao_be một lần mỗi lần vào màn, mở tạo bé rồi Về không chào lại; hd_cung_hoc khi chọn bé; hd_nghi_mat; 4 khen_* theo cách làm, sau cảnh hoa bay). WelcomeTests 4/4, ProfileScreenTests 9/9, LessonStickerTests 6/6, RestAndParentTests 9/9, PraiseAndStickerTests 9/9. Root kiểm diff: đạt. Nâng cấp UI chỉ còn chờ chủ dự án duyệt.
- **[L1] tranh động — b12 quả me (57b8d07):** khung đầu ChatGPT, một quả chín xanh → nâu; root xem trước: đạt, cho_duyet. b219 lần 3 (L2) gửi trên /u/2 lúc 09:41 theo lời chủ dự án "Cho chạy ／u/2".
- **[L2] tranh động — b173 lần 3 không đạt (3edbea4):** chuyển cảnh mờ 4,5–5,4 s; hết 3 lượt, chờ chủ dự án chọn tranh tĩnh hay loop đứng yên.

- **Ngoặc kép giữa câu — sửa 36 mã (root điều phối, 08:30–09:10):**
  - [L2] nội dung: 30 mã TV2 tập 1, chữ đọc bỏ ngoặc kép bằng ngoac_kep_lop2.py kiểu a (4990a01).
  - [L1] nội dung: 6 mã lớp 1 (696c375), gồm 2 mã ngoặc cong cau_b78_02 và cau_b78_03. Trước đây máy nghe mất hẳn phần trong ngoặc.
  - Root nhận dạng lại cả 36 mã: không còn tiếng chèn. Thêm nghe kỹ 2 mã: cau_b176_04 ("nhé" nghe "nha", có từ trước) và cau_b146_13 ("Vểnh" nghe "Vỉnh").
  - Root kiểm cả hai commit: đúng bộ mã dòng/override, phần còn lại của settings giữ nguyên, phần chủ dự án sửa dở nằm ngoài. 36 mp3 đi theo gói bosung.
- **[L2] nội dung — 7514730:** van_thay trong sua_hoi_nga_lop2.py. Khi ghép thiếu tieng_X thì dùng van_X; đây là thay đổi 16/11 trước đó chưa commit. Root chạy lại 4 test mới: đạt.

- **[L2T2] nội dung — âm thanh TV2 tập 2 mục 371–402 (đợt 3):**
  - 791 mã cho_duyet (760e607), 43 mã cài bản thử root chọn:
    - 28 mã bản thử khớp hẳn, gồm 2 mã cao độ: cau_b376_06 ghép "cả" từ tieng_car, cau_b373_04 chậm −25%;
    - 11 mã cài kèm "nghe kỹ";
    - 4 mã vòng 2: 3 câu hỏi ghép lại có số đầu câu, cau_b395_07.
  - Giữ bản cũ 60 mã, nghe kỹ 53 mã: đưa vào danh sách chủ dự án nghe.
  - tieng_ix ("ĩ") nghe như sắc, 2 bản thử không đỡ; đợt 4 thử thêm "ỹ".
  - Công cụ: ghép từng tiếng giữ chữ số "2." (75dab62). Test: 16 test lớp 2 (bản thử + đo cao độ) đạt.
  - Root kiểm trước commit:
    - dựng lại index tạm, stat trùng;
    - 791 mã đúng bằng danh sách đợt 3, không mp3 rỗng;
    - 33 dòng và 4 cách đọc riêng của chủ dự án nằm ngoài commit;
    - 43 mp3 khớp từng byte.
- **Root — soát âm đợt 3:**
  - Nhận dạng 791 mã, nghi 317. So NamMinh 237 mã, chia làm lại 101, nghe kỹ 53, do máy nghe 83, tiếng lẻ 75.
  - Chấm thanh 90 tiếng lẻ bằng mẫu đã duyệt: không tiếng hỏi/ngã nào ra huyền.
  - Ghi thêm 3 cách vào quy trình chuẩn §12:
    - đệm 0,5 s lặng để Whisper hết nghe ra câu ảo;
    - chấm thanh tiếng lẻ;
    - ghép phải giữ số đầu câu.

- **[L2T2] nội dung — âm thanh TV2 tập 2 mục 305–370 (đợt 1–2):**
  - Đủ 1646 mã cho_duyet (2de90da); không còn mã nào chờ tạo lại.
  - Có 88 mã cài bản thử root chọn:
    - 14 mã sửa cao độ hỏi/ngã ("tả", "bão", "ngã", "hải", "bảo", "ngủ"; bản chậm −25% hoặc ghép);
    - 74 mã nhóm "làm lại".
  - Root kiểm trước khi commit:
    - dựng lại index tạm, bảng thay đổi trùng nhau;
    - 33 dòng và 4 cách đọc riêng chủ dự án sửa dở vẫn nằm ngoài commit;
    - 74 mp3 khớp từng byte.
  - Công cụ:
    - đo cao độ không còn coi "(khổ 2)" là cuối cụm (1fd37f9);
    - bản thử "cham=N" và ghép theo danh sách phần (b059273).
  - Test: 15 test lớp 2 đạt.
- **Root — soát âm TV2 tập 2:**
  - Nhận dạng đợt 2 (766 mã): 24 mã ngoặc kép tạo lại hết tiếng chèn.
  - So giọng NamMinh cho 256 + 181 mã nghi. Chia nhóm: làm lại 193, nghe kỹ 82.
  - Nhận dạng 364 bản thử: chọn được 74 mã. 119 mã vẫn bị nghe sai ở mọi bản → giữ bản cũ, đưa vào danh sách chủ dự án nghe theo cặp chữ.
  - Cách làm ghi ở QUY-TRINH §12 (2f5aacb).
- **Còn dở:**
  - TV2 tập 2 đợt 3 (371–402) đang tạo giọng; còn đợt 4.
  - Sửa ngoặc kép cho TV2 tập 1 (~27 mã) và lớp 1 (~4 mã).

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
