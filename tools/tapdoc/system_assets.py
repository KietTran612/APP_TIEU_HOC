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
    # Hình đại diện để bé chọn khi tạo hồ sơ: con vật quen thuộc, vẽ mặt trước, nền trơn.
    "img_chung_avatar_01": "Hình đại diện: mặt con mèo con tươi cười, tai nhọn, có ria, vẽ chính diện",
    "img_chung_avatar_02": "Hình đại diện: mặt con chó con tươi cười, tai cụp, lưỡi thè nhẹ, vẽ chính diện",
    "img_chung_avatar_03": "Hình đại diện: mặt con thỏ trắng tươi cười, hai tai dài dựng đứng, vẽ chính diện",
    "img_chung_avatar_04": "Hình đại diện: chú gà con lông vàng tròn xoe, mỏ nhỏ, đứng nhìn thẳng",
    "img_chung_avatar_05": "Hình đại diện: con cá vàng tròn trịa, vây đuôi xòe, bơi nghiêng mỉm cười",
    "img_chung_avatar_06": "Hình đại diện: mặt con voi con tươi cười, tai to, vòi cong lên",
}
