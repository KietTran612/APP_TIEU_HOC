"""Tuần 10 (mục 242–249), tr.66–72, ảnh 034–037."""
from l2lib import *

QH_IMG = "img_b242_vex_quee_huwowng"
QH_DESC = ("Tranh làng quê nhìn từ trên cao: cánh đồng lúa xanh, sông máng lượn quanh, lũy tre xanh, những mái nhà ngói "
           "đỏ, ngôi trường trên đồi, cây gạo đầu xóm nở hoa đỏ, mặt trời đỏ và lá cờ đỏ sao vàng bay trên nền trời xanh")

# 242 — Bài 35. Vẽ quê hương (tr.66–67)
POEM35 = ["Bút chì xanh đỏ", "Em gọt hai đầu", "Em thử hai màu", "Xanh tươi, đỏ thắm.",
          "Em vẽ làng xóm", "Tre xanh, lúa xanh", "Sông máng lượn quanh", "Một dòng xanh mát", "Trời mây bát ngát",
          "Xanh ngắt mùa thu", "Xanh màu ước mơ...", "Em quay đầu đỏ", "Vẽ nhà em ở", "Ngói mới đỏ tươi",
          "Trường học trên đồi", "Em tô đỏ thắm", "Cây gạo đầu xóm", "Hoa nở chói ngời", "A, nắng lên rồi!",
          "Mặt trời đỏ chót", "Lá cờ Tổ quốc", "Bay giữa trời xanh...",
          "Chị ơi bức tranh", "Quê ta đẹp quá!"]
lesson(242, [66, 67],
       [picture(QH_IMG, "Bức tranh vẽ quê hương thật đẹp.", "quê hương"),
        title("Vẽ quê hương"),
        *sentences(*POEM35),
        passage("poem", "ĐỊNH HẢI", breaks=[4, 22]),
        q("1. Nêu những cảnh vật có màu xanh được tả trong bài. Tìm thêm những cảnh vật có màu xanh ở quê em.",
          marker="?"),
        q("2. Những cảnh vật nào có màu đỏ đã được tả trong bài? Kể thêm những cảnh vật có màu đỏ ở quê em."),
        q("3. Nêu những từ chỉ màu xanh và màu đỏ có trong bài. Tìm thêm các từ chỉ màu xanh và màu đỏ mà em biết. "
          "Ví dụ: xanh tươi, xanh ngắt, đỏ thắm, đỏ tía,...")],
       listen(("xanh tươi", "đỏ thắm", "xanh ngắt"), ("đỏ chót", "đỏ tươi", "chói ngời"), ("bát ngát", "lượn quanh", "ước mơ"),
              ("cây gạo", "làng xóm", "sông máng"), ("xanh ngắt", "xanh mát", "đỏ chót"), ("làng xóm", "trường học", "cây gạo")),
       images={QH_IMG: QH_DESC},
       notes=[("khac_sach", KS_ORAL)])

# 243 — Bài 36. Ta yêu quê ta (Học thuộc lòng, tr.67–68)
POEM36 = ["Yêu từng bờ ruộng, lối mòn,", "Đỏ tươi bông gạo, biếc rờn ngàn dâu.", "Yêu con sông mặt sóng xao,",
          "Dòng sông tuổi nhỏ rì rào hát ca.", "Yêu hàng ớt đã ra hoa,", "Đám dưa trổ nụ, đám cà trổ bông.",
          "Yêu sao tiếng mẹ ru nồng,", "Tiếng thoi lách cách bên nong dâu tằm."]
lesson(243, [67, 68],
       [picture("img_b243_quee_ta", "Làng quê ven sông với hàng dừa xanh.", "quê ta"),
        title("Ta yêu quê ta", "Học thuộc lòng"),
        *sentences(*POEM36),
        passage("poem", "LÊ ANH XUÂN"),
        *glossary("Ngàn dâu: bãi trồng dâu rất rộng, thường ở ven các sông lớn.",
                 "Mặt sóng xao: mặt nước chuyển động nhẹ, lăn tăn gợn sóng.", "Trổ bông: nở hoa, ra hoa.",
                 "Tiếng mẹ ru nồng: tiếng mẹ ru ấm áp, đậm đà."),
        q("1. Đọc bài này, em thấy quê hương tác giả là thành phố hay nông thôn? Vì sao em biết?", marker="?"),
        q("2. Tác giả yêu những cảnh vật nào ở quê nhà?"),
        q("3. Kể những màu sắc và âm thanh trong bài."),
        q("4. Kể một vài cảnh đẹp ở quê em."),
        memorize()],
       listen(("bờ ruộng", "lối mòn", "ngàn dâu"), ("bông gạo", "hàng ớt", "đám dưa"), ("rì rào", "lách cách", "biếc rờn"),
              ("trổ bông", "trổ nụ", "ra hoa"), ("lách cách", "rì rào", "dâu tằm"), ("dâu tằm", "ngàn dâu", "bông gạo")),
       images={"img_b243_quee_ta": "Làng quê miền Nam ven sông: những mái nhà tranh dưới hàng dừa, con thuyền nhỏ neo bên "
                                   "bờ, cây cầu tre bắc ra mặt nước gợn sóng lăn tăn"},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)])

# 244 — Bài 37. Hồ Gươm (tr.68–69)
lesson(244, [68, 69],
       [picture("img_b244_hoof_guwowm", "Hồ Gươm có cầu Thê Húc và Tháp Rùa.", "Hồ Gươm"),
        title("Hồ Gươm"),
        *prose("NGÔ QUÂN MIỆN",
               ["Nhà tôi ở cách Hồ Gươm không xa.", "Từ trên gác cao nhìn xuống,",
                "hồ như một chiếc gương bầu dục lớn, sáng long lanh."],
               ["Cầu Thê Húc màu son, cong cong như con tôm, dẫn vào đền Ngọc Sơn.",
                "Mái đền lấp ló bên gốc đa già, rễ, lá xum xuê.", "Xa một chút là Tháp Rùa, tường rêu cổ kính,",
                "xây trên gò đất cỏ mọc xanh um.", "Có buổi, người ta thấy có con rùa lớn,",
                "đầu to như trái bưởi, nhô lên khỏi mặt nước.",
                "Nó như lắng nghe tiếng chuông đồng hồ trên tầng cao nhà bưu điện",
                "buông từng tiếng ngân nga trong gió.", "Tôi thầm nghĩ:",
                "Không biết có phải con rùa đã từng ngậm thanh kiếm", "của vua Lê thắng giặc đó không?"]),
        *glossary("Hồ Gươm: còn gọi là hồ Hoàn Kiếm ở thủ đô Hà Nội.", "Cổ kính: cổ và trang nghiêm."),
        q("1. Tác giả so sánh Hồ Gươm với vật gì?", marker="?"),
        q("2. Nhìn vào tranh, em chỉ cầu Thê Húc, đền Ngọc Sơn, Tháp Rùa."),
        q("3. Nêu những vẻ đẹp của Hồ Gươm được tác giả tả trong bài.")],
       listen(("Hồ Gươm", "Tháp Rùa", "đền Ngọc Sơn"), ("long lanh", "xum xuê", "ngân nga"), ("cổ kính", "xanh um", "long lanh"),
              ("Tháp Rùa", "cầu Thê Húc", "Hồ Gươm"), ("ngân nga", "cổ kính", "xum xuê"), ("bầu dục", "trái bưởi", "con tôm")),
       images={"img_b244_hoof_guwowm": "Phong cảnh Hồ Gươm: mặt hồ xanh phẳng lặng, cầu Thê Húc cong màu son dẫn vào đền "
                                       "Ngọc Sơn giữa hàng cây, Tháp Rùa trên gò đất xa xa, cây cối xum xuê ven hồ "
                                       "(không có người, không có chữ)"},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 245 — Bài 38. Rừng miền đông (Bài đọc thêm, tr.70; sách không có tranh)
lesson(245, [70],
       [title("Rừng miền đông", "Bài đọc thêm"),
        *prose("CHU LAI",
               ["Đang vào mùa rừng dầu trút lá.", "Tàu lá dầu liệng xuống như cánh diều, phủ vàng mặt đất.",
                "Mỗi khi có con hoẵng chạy qua,", "thảm lá khô vang động như có ai đang bẻ chiếc bánh đa.",
                "Những cây dầu con mới lớn,", "phiến lá đã to gần bằng lá già rụng xuống.",
                "Lá như cái quạt nan che lấp cả thân cây.", "Đang giữa trưa nắng, gặp rừng dầu non,",
                "mắt bỗng dịu lại như đang lạc vào một vùng rau xanh mát."],
               ["Hết rừng dầu lại đến rừng cao su.",
                "Màu xanh lá dầu chỉ có thể so sánh với màu cao su vừa thay lá.",
                "Những cánh rừng cao su thăm thẳm, như những cái hang động màu ngọc bích.",
                "Sắc lá càng xanh biếc trong màu đất đỏ tươi."])],
       listen(("rừng dầu", "cao su", "con hoẵng"), ("thăm thẳm", "ngọc bích", "xanh biếc"), ("bánh đa", "cánh diều", "quạt nan"),
              ("ngọc bích", "thăm thẳm", "đất đỏ"), ("cánh diều", "quạt nan", "rừng dầu"), ("xanh biếc", "đỏ tươi", "thăm thẳm")),
       notes=[("khac_sach", KS_SPLIT)])

# 246 — Chính tả tuần 10 (tr.70–71)
lesson(246, [70, 71],
       [title("Chính tả: Vẽ quê hương", "Nghe đọc"),
        title("Bài viết: 12 câu thơ đầu.", "Phần này con nghe bố mẹ đọc rồi viết vào vở."),
        words("lượn quanh", "dòng", "màu", "máng", "vẽ"),
        fill(["n", "ng"], ("dòng sông lượn", "lượn", "n"), ("bay lượn", "lượn", "n"), ("số lượng", "lượng", "ng")),
        fill(["vẽ", "vẻ"], ("Em vẽ tranh.", "vẽ", "vẽ"), ("Nó cười vui vẻ.", "vẻ", "vẻ")),
        combine("quanh", "lượn", "chung", at="before"),
        combine("quanh", "co"),
        combine("hòa", "thuận", "bình"),
        title("Tập chép: Nói với em", "Nhìn sách"),
        title("Bài viết: 2 khổ sau của bài thơ.", "Phần này con chép vào vở cùng bố mẹ."),
        words("nhắm", "chuyện", "khuya", "Tấm", "dặm", "nuôi", "vất vả"),
        combine("chuyện", "nói", "kể", at="before"),
        combine("khuya", "đêm", "thức", at="before"),
        fill(["dặm", "rậm"], ("đường xa muôn dặm", "dặm", "dặm"), ("rừng cây rậm rạp", "rậm", "rậm"))],
       listen(("lượn quanh", "quanh co", "chung quanh"), ("hòa thuận", "hòa bình", "vui vẻ"), ("số lượng", "bay lượn", "vẽ tranh"),
              ("nói chuyện", "kể chuyện", "thức khuya"), ("đêm khuya", "muôn dặm", "rậm rạp"), ("vất vả", "nuôi", "nhắm")),
       notes=[("khac_sach", KS_WRITE), ("khac_sach", "Điền chỗ trống, ghép chữ làm bằng chạm hoặc kéo thẻ.")],
       review=[("part1[3]", "đáp án n/ng"), ("part1[4]", "đáp án vẽ/vẻ"),
               ("part1[5]", "cách ghép do app chọn: lượn quanh, chung quanh, quanh co; hòa thuận, hòa bình"),
               ("part1[13]", "đáp án dặm/rậm; dòng \"vả hay vá: vất..., vật..., ăn...\" trong sách chưa rõ chữ nên app "
                             "chưa đưa vào")])

# 247 — Từ ngữ: Quê hương đất nước (tr.71)
lesson(247, [71],
       [title("Từ ngữ: Quê hương đất nước"),
        title("Những từ ngữ cần ghi nhớ"),
        words("quê hương", "làng xóm", "quê cha đất tổ", "Tổ quốc", "đất nước", "non sông", "thủ đô"),
        words("yêu nước thương nòi", "bảo vệ Tổ quốc", "xây dựng đất nước"),
        title("Bài tập: Điền từ ngữ thích hợp vào chỗ trống"),
        fill_passage(["Tổ quốc ta là nước [Việt Nam|làng xóm|thủ đô].",
                      "Hà Nội là thủ đô của [Tổ quốc|làng xóm|quê cha] chúng ta.",
                      "Nhân dân ta rất giàu lòng [yêu nước thương nòi|xây dựng đất nước|quê cha đất tổ],",
                      "luôn luôn sẵn sàng chiến đấu để [bảo vệ Tổ quốc|xây dựng đất nước|yêu nước thương nòi].",
                      "Nhân dân ta lại hăng hái thi đua lao động sản xuất để "
                      "[xây dựng đất nước|bảo vệ Tổ quốc|quê cha đất tổ]."])],
       listen(("quê hương", "làng xóm", "thủ đô"), ("Tổ quốc", "đất nước", "non sông"), ("non sông", "thủ đô", "quê hương"),
              ("thủ đô", "Tổ quốc", "làng xóm"), ("làng xóm", "non sông", "đất nước"), ("đất nước", "quê hương", "Tổ quốc")),
       notes=[("khac_sach", "Sách để trống: app cho mỗi chỗ trống 3 thẻ lấy từ các từ ngữ cần ghi nhớ; "
                            "thẻ và đáp án do app soạn.")],
       review=[("part1[5]", "thẻ chọn và đáp án điền chỗ trống do app soạn")])

# 248 — Ngữ pháp: Câu – Hai bộ phận chính (tiếp theo) (tr.71–72)
lesson(248, [71, 72],
       [title("Ngữ pháp: Câu – Hai bộ phận chính", "Tiếp theo"),
        q("1. Đặt câu hỏi để tìm bộ phận chính thứ nhất và bộ phận chính thứ hai trong hai câu sau:",
          lines=["Chúng em chăm học chăm làm.", "Đất nước ta vô cùng tươi đẹp."]),
        *rule("Bộ phận chính thứ hai của câu còn là bộ phận trả lời câu hỏi: \"... như thế nào?\""),
        title("2. Nhìn vào hình vẽ và đặt câu"),
        picture("img_b248_las_cowf", "Lá cờ đỏ sao vàng bay trên cột cờ.", "lá cờ"),
        q("Nhìn tranh lá cờ, em hãy đặt một câu."),
        picture("img_b248_lowps_hocj", "Cô giáo đứng giảng bài, cả lớp chăm chú nghe.", "lớp học"),
        q("Nhìn tranh lớp học, em hãy đặt một câu."),
        q("3. Em hãy viết vào vở những câu em vừa đặt. "
          "Phân biệt bộ phận chính thứ nhất và bộ phận chính thứ hai của câu.")],
       listen(("lá cờ", "lớp học", "cô giáo"), ("tươi đẹp", "chăm học", "chăm làm"), ("cô giáo", "lá cờ", "cột cờ"),
              ("lớp học", "cô giáo", "đất nước"), ("chăm làm", "tươi đẹp", "lá cờ"), ("đất nước", "lớp học", "tươi đẹp")),
       images={"img_b248_las_cowf": "Lá cờ đỏ sao vàng tung bay trên đỉnh cột cờ, nền trời xanh có mây trắng",
               "img_b248_lowps_hocj": "Lớp học: cô giáo đứng trước bảng đen cầm quyển sách giảng bài, các bạn học sinh "
                                      "ngồi ngay ngắn ở bàn chăm chú nghe (nhìn từ phía sau lớp)"},
       notes=[("khac_sach", "Sách in hai tranh cạnh nhau; app hiện từng tranh rồi hỏi. Bé đặt câu bằng miệng cùng "
                            "bố mẹ; phần viết vào vở bé viết cùng bố mẹ.")],
       review=[("part1[4]", "lời dẫn tranh do app soạn"), ("part1[6]", "lời dẫn tranh do app soạn")])

# 249 — Tập làm văn: Quan sát tranh và trả lời câu hỏi — Quê hương (tr.72)
lesson(249, [72],
       [title("Tập làm văn: Quan sát tranh và trả lời câu hỏi"),
        title("Đề bài: Quê hương.", "Xem tranh ở bài Vẽ quê hương."),
        picture(QH_IMG, "Con nhìn kĩ bức tranh quê hương nhé.", "quê hương"),
        q("1. Nhìn bức tranh quê hương, em thấy đây là cảnh nông thôn hay thành phố? Vì sao em biết?"),
        q("2. Tranh vẽ những cảnh gì? Em thích cảnh nào nhất?"),
        q("3. Dựa vào tranh, em nêu thêm hai câu hỏi và tự trả lời.")],
       listen(("nông thôn", "thành phố", "quê hương"), ("thành phố", "nông thôn", "cánh đồng"), ("cánh đồng", "lũy tre", "mái nhà"),
              ("lũy tre", "cánh đồng", "ngôi trường"), ("ngôi trường", "mái nhà", "nông thôn"), ("mái nhà", "ngôi trường", "lũy tre")),
       images={QH_IMG: QH_DESC},
       notes=[("khac_sach", "Tập làm văn quan sát tranh: app dùng lại tranh bài Vẽ quê hương; bé trả lời miệng.")],
       review=[("part1[2]", "lời dẫn tranh do app soạn")])
