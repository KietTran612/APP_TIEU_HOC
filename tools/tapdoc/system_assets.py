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
    "hd_nhin_chon_chu_hoa": "Con nhìn chữ thường rồi chọn chữ hoa đúng nhé.",
    "hd_nghe_do_chon_tranh": "Con nghe câu đố rồi chọn tranh đúng nhé.",
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
    # Sổ bé ngoan và bạn đồng hành. Hiện là hình mặc định (`python -m tapdoc ui-icons`); tranh chính thức
    # vẽ sau bằng ChatGPT rồi ghi đè file cùng mã.
    "img_chung_hoa_be_ngoan": "Bông hoa bé ngoan: một bông hồng hồng tươi có lá xanh và cuống, viền mực đen rõ, "
                              "có điểm sáng, rực rỡ bắt mắt, nền trong suốt",
    "img_chung_ga_con": "Bạn gà con đồng hành: chú gà con lông vàng tròn xoe, đứng nhìn thẳng, vui vẻ",
    # Biểu tượng trên nút của bé: nét mực đen, tô giấy sáng, nền trong suốt, nằm giữa khung.
    "img_ui_nha": "Biểu tượng về danh sách: ngôi nhà nhỏ mái nhọn, cửa đen",
    "img_ui_loa": "Biểu tượng nghe lại: cái loa với hai làn sóng âm",
    "img_ui_tiep": "Biểu tượng đi tiếp: mũi tên to chỉ sang phải",
    "img_ui_lui": "Biểu tượng quay lại: mũi tên to chỉ sang trái",
    "img_ui_so": "Biểu tượng Sổ bé ngoan: quyển sổ mở, có bông hoa nhỏ ở trang trái",
    "img_ui_on_lai": "Biểu tượng ôn lại: mũi tên vòng tròn",
    "img_ui_xong": "Biểu tượng con đọc xong rồi: dấu tích",
    "img_ui_khoa": "Biểu tượng bài chưa mở: ổ khoá nhỏ màu nhạt",
    "img_ui_lat_truoc": "Biểu tượng trang trước: tờ giấy gấp góc, mũi tên nhỏ chỉ sang trái",
    "img_ui_lat_sau": "Biểu tượng trang sau: tờ giấy gấp góc, mũi tên nhỏ chỉ sang phải",
    "img_ui_sao_giay": "Ngôi sao giấy màu vàng viền mực, bung ra khi bé làm đúng",
    "img_ui_canh_hoa": "Cánh hoa hồng hình giọt nước viền mực, rơi ra khi dán hoa vào sổ",
}

# Tiếng động khi tương tác: tách hẳn khỏi âm thanh phát âm (`SYSTEM_AUDIO`). Mã luôn bắt đầu bằng `sfx_`,
# file nằm ở `Resources/sfx/` (không phải `audio/`), không vào danh mục âm thanh hay lệnh `tts`.
# Chỉ dùng file CC0 (chủ dự án nghe chọn ngày 30/10/2026; ghi công ở docs/credits-am-thanh.md). Mã chưa có file
# CC0 dùng tiếng mặc định tự tạo (`python -m tapdoc sfx-default`).
DEFAULT_SFX_SOURCE = "mặc định tự tạo: python -m tapdoc sfx-default"
SYSTEM_SFX: dict[str, dict] = {
    "sfx_cham": {"mo_ta": "\"tách\" nhỏ, ngắn khi chạm nút hoặc nhấc thẻ",
                 "nguon": DEFAULT_SFX_SOURCE, "giay_phep": "CC0"},
    "sfx_dung": {"mo_ta": "\"ting\" trong, vui khi bé làm đúng",
                 "nguon": "Kenney Interface Sounds 1.0: confirmation_001.ogg (opengameart.org/content/interface-sounds)",
                 "giay_phep": "CC0"},
    "sfx_nhap": {"mo_ta": "\"bụp\" nhẹ khi các thẻ nhập thành tiếng",
                 "nguon": "OpenGameArt \"Pop sounds\" (cogitollc): pop1.ogg (opengameart.org/content/pop-sounds)",
                 "giay_phep": "CC0"},
    "sfx_hoa_bay": {"mo_ta": "\"vút\" nhẹ khi bông hoa bay vào sổ",
                    "nguon": "Kenney Interface Sounds 1.0: maximize_008.ogg (opengameart.org/content/interface-sounds)",
                    "giay_phep": "CC0"},
    "sfx_dong_dau": {"mo_ta": "\"cộp\" khi đóng dấu Bé ngoan",
                     "nguon": "Kenney RPG Audio: bookPlace1.ogg (opengameart.org/content/50-rpg-sound-effects)",
                     "giay_phep": "CC0"},
    "sfx_lat_trang": {"mo_ta": "\"sột\" giấy khi lật trang sổ hoặc sang bước mới",
                      "nguon": "Kenney RPG Audio: bookFlip2.ogg (opengameart.org/content/50-rpg-sound-effects)",
                      "giay_phep": "CC0"},
}
