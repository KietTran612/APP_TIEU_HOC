# Script làm Tiếng Việt 2 (lớp 2): tập một mục 172–304, tập hai mục 305–434

Chạy từ thư mục gốc repo. Mặc định là tập một; thêm cờ **`--t2`** cho tập hai (`sach.py`: chỉ lấy mã mà mọi bài đều thuộc tập đã chọn, mã dùng chung với cuốn khác không đụng). `sua_hoi_nga_lop2.py` chưa có `--t2`.

| Script | Việc |
|---|---|
| `tts_lop2.py <số lượt> [bài đầu=172] [bài cuối=304] [--giu-may-thuc]` | Tạo âm thanh HoaiMy cho mã **chỉ thuộc bài lớp 2**, chưa `dat`, còn `chua_co` hoặc khác cấu hình. 1 tiến trình, mỗi mã tối đa 90 giây, mỗi lượt sau là lượt bù. Log: `.superpowers/tts_lop2.log`. `--giu-may-thuc` xin Windows không cho máy nghỉ khi script còn chạy |
| `tieng_doc_lop2.py [--ghi]` | Đặt cách đọc tiếng lẻ lớp 2: thanh nặng "X. X.", có ê thanh sắc "X, X, X.", còn lại "X, X." (đều giữ tiếng đầu). Không `--ghi` thì chỉ in |
| `do_cao_do_lop2.py [--ma MÃ…] [--json ra.json]` | Đo hỏi/ngã mọi mã lớp 2 có file; chỉ chấm tiếng lẻ và tiếng cuối cụm (sai / có thể sai / đạt), tiếng giữa cụm không chấm |
| `kiem_tieng_le_lop2.py [--json ra.json]` | Kiểm tiếng lẻ lớp 2 theo cách của L1: nặng dài > 0,45 s hoặc cao độ ra thanh khác → lạ |
| `sua_hoi_nga_lop2.py cham\|ghep\|ghi-chu …` | Đặt đọc chậm hơn 20% hoặc ghép mượt cho mã sai, rồi ghi chú sau khi tạo lại và đo lại |
| `stage_lop2.py <danh mục…>` | Stage chỉ phần lớp 2 của `content/manifests/*.json` (blob từ HEAD + dòng lớp 2), giữ nguyên chỉnh sửa duyệt chưa commit của chủ dự án |
| `xuat_wav_lop2.py [--t2] <bài đầu> <bài cuối> --ra <thư mục> [--ma MÃ…]` | Xuất WAV 16 kHz mono (`wav/<mã>.wav`) và `chi_muc.json` (chữ hiển thị, chữ đọc) của các mã trong khoảng bài để root nhận dạng giọng nói |
| `sach.py` | Chọn tập theo cờ `--t2`, khoảng bài mặc định của từng tập |
| `soan/`, `soan_t2/` | Script soạn nguồn bài: `soan/` cho `content/src/tv2_t1_*.json` (`l2lib.py`, `toc_l2.py`, `w1.py`…`w17.py` mỗi tuần một file). Chỉ để tham khảo/soạn lại: chạy `python wN.py` trong thư mục `soan/` sẽ **ghi đè** nguồn bài tuần đó |

`soan_t2/` (tập hai): `toc_t2.py` (mục lục tr.122–124, `image_of` vì ảnh scan đầu sách bị xáo), `l2t2lib.py`, `w18.py` … `w33.py`. Chạy `python wNN.py` trong `soan_t2/` sẽ **ghi đè** nguồn bài tuần đó.
