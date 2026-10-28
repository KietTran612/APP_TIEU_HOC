"""Âm thanh và tranh dùng chung cho mọi bài (không thuộc riêng bài nào).

Danh mục âm thanh/tranh (Task 6) lấy các mã này từ đây; file bài học chỉ tham chiếu mã
`instruction_audio`, không liệt kê lại trong `BuildResult.audio`.
"""

# mã -> lời đọc
SYSTEM_AUDIO: dict[str, str] = {
    "hd_nghe_chon_chu": "Con nghe rồi chọn chữ đúng nhé.",
    "hd_nghe_chon_tranh": "Con nghe rồi chọn tranh đúng nhé.",
    "hd_nhin_keo_dau": "Con nhìn chữ mẫu rồi kéo dấu vào cho đúng nhé.",
    "hd_keo_vao_cho_trong": "Con kéo chữ vào chỗ trống nhé.",
    "hd_danh_van_theo": "Con đánh vần theo nhé.",
    "hd_keo_dau_vao_chu": "Con kéo dấu vào chữ nhé.",
    "hd_thu_lai": "Con thử lại nhé.",
    "khen_01": "Đúng rồi!",
    "khen_02": "Giỏi lắm!",
    "khen_hoan_thanh": "Con học xong bài rồi. Giỏi lắm!",
}

# mã -> mô tả tranh
SYSTEM_IMAGES: dict[str, str] = {
    "img_chung_sao": "Ngôi sao vàng năm cánh, viền mực đen, kiểu hình dán cho bé",
    "img_chung_em_doc": "Kí hiệu 'Em đọc' của sách: một chấm tròn đặc màu đen, bên trong có hoa văn nhỏ",
    "img_chung_luyen_tap": "Kí hiệu 'Luyện tập ở lớp và ở nhà' của sách: ngôi nhà nhỏ mái nhọn, nét mực đen, "
                           "thân nhà tô hoa văn ô nhỏ",
}
