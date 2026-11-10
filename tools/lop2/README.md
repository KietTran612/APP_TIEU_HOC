# Script làm Tiếng Việt 2 tập một (lớp 2, mục 172–304)

Chạy từ thư mục gốc repo.

| Script | Việc |
|---|---|
| `tts_lop2.py <số lượt> [bài đầu=172] [bài cuối=304] [--giu-may-thuc]` | Tạo âm thanh HoaiMy cho mã **chỉ thuộc bài lớp 2**, chưa `dat`, còn `chua_co` hoặc khác cấu hình. 1 tiến trình, mỗi mã tối đa 90 giây, mỗi lượt sau là lượt bù. Log: `.superpowers/tts_lop2.log`. `--giu-may-thuc` xin Windows không cho máy nghỉ khi script còn chạy |
| `tieng_doc_lop2.py [--ghi]` | Đặt cách đọc tiếng lẻ lớp 2: thanh nặng "X. X.", có ê thanh sắc "X, X, X.", còn lại "X, X." (đều giữ tiếng đầu). Không `--ghi` thì chỉ in |
| `stage_lop2.py <danh mục…>` | Stage chỉ phần lớp 2 của `content/manifests/*.json` (blob từ HEAD + dòng lớp 2), giữ nguyên chỉnh sửa duyệt chưa commit của chủ dự án |
| `soan/` | Script đã dùng để soạn `content/src/tv2_t1_*.json` (`l2lib.py`, `toc_l2.py`, `w1.py`…`w17.py` mỗi tuần một file). Chỉ để tham khảo/soạn lại: chạy `python wN.py` trong thư mục `soan/` sẽ **ghi đè** nguồn bài tuần đó |
