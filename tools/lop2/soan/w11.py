"""Tuần 11 (mục 250–257), tr.73–79, ảnh 037–040."""
from l2lib import *

GACH_IMG = "img_b251_nhaf_mays_gachj"
GACH_DESC = ("Nhà máy gạch: lò nung cao có ống khói bốc khói nghi ngút, các chú công nhân xếp những chồng gạch đỏ, "
             "bốc gạch lên chiếc xe vận tải đậu trên bãi, một xe tải khác đang chạy ra cổng")
POEM36 = ["Yêu từng bờ ruộng, lối mòn,", "Đỏ tươi bông gạo, biếc rờn ngàn dâu.", "Yêu con sông mặt sóng xao,",
          "Dòng sông tuổi nhỏ rì rào hát ca.", "Yêu hàng ớt đã ra hoa,", "Đám dưa trổ nụ, đám cà trổ bông.",
          "Yêu sao tiếng mẹ ru nồng,", "Tiếng thoi lách cách bên nong dâu tằm."]

# 250 — Bài 39. Bến Nhà Rồng (tr.73–74)
lesson(250, [73, 74],
       [picture("img_b250_beens_nhaf_roongf", "Bến cảng bên sông lúc sáng sớm.", "bến cảng"),
        title("Bến Nhà Rồng"),
        *prose("ĐOÀN GIỎI",
               ["Nền trời rực hồng.", "Từng đàn chim én chao lượn, bay ra phía biển.",
                "Những con tàu sơn trắng đậu san sát,", "tung bay cờ đủ màu của các nước.",
                "Trông chúng như những tòa lâu đài nổi,", "ẩn hiện giữa sương mù và làn khói nước",
                "nhè nhẹ cuốn lên trong gió ban mai."],
               ["Một hồi còi rền mặt sông.", "Hùng hỏi ông:"],
               ["- Cháu nghe nói mấy chú hoa tiêu biết hết những chỗ sâu, cạn,",
                "những chỗ có đá ngầm trên sông này phải không ông?"],
               ["- Đúng!"], ["- Giỏi quá ông nhỉ!"],
               ["- Nhưng Bác Hồ mới là người hoa tiêu tài giỏi nhất.", "Cách đây bảy mươi năm, từ bến cảng này,",
                "Bác đã ra đi tìm đường cứu nước.",
                "Bác đã lái con thuyền Tổ quốc Việt Nam vượt muôn trùng sóng gió,",
                "đến bến bờ Độc lập, Thống nhất ngày nay đấy, cháu ạ!"]),
        *glossary("Bến Nhà Rồng: một trong 16 bến của cảng Sài Gòn, nằm trên sông Sài Gòn.",
                 "Hoa tiêu: người dẫn đường cho tàu thủy (hoặc máy bay)."),
        q("1. Cảnh bến Nhà Rồng được tả vào lúc nào? Từ nào cho em biết điều đó?", marker="?"),
        q("2. Cảnh bến có những nét gì đẹp?"),
        q("3. Tác giả so sánh những con tàu với vật gì?"),
        q("4. Bến Nhà Rồng còn giữ được kỉ niệm gì đáng quý?")],
       listen(("hoa tiêu", "bến cảng", "con tàu"), ("chao lượn", "san sát", "nhè nhẹ"), ("lâu đài", "sương mù", "khói nước"),
              ("san sát", "chao lượn", "ẩn hiện"), ("sóng gió", "đá ngầm", "bến bờ"), ("ẩn hiện", "nhè nhẹ", "lâu đài")),
       images={"img_b250_beens_nhaf_roongf": "Bến cảng bên sông lúc bình minh: tòa nhà cổ mái cong hai tầng bên bờ sông, "
                                             "những con tàu trắng đậu san sát, xuồng nhỏ trên mặt sông, đàn chim én bay "
                                             "về phía biển (không có người, không có chữ)"},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 251 — Bài 40. Gạch đỏ (Học thuộc lòng, tr.75–76)
POEM40 = ["Gạch vào lò", "Lửa bùng to,", "Khói ngùn ngụt", "Than đỏ rực", "Suốt đêm ngày.", "Gạch kề vai",
          "Đứng chịu nóng,", "Hơi lửa bỏng", "Quấn quanh người.",
          "A! Gạch chín rồi", "Áo hồng sắc lửa", "Lanh canh tiếng cười.", "Gạch ơi! Gạch ơi!", "Gạch rắn, gạch khỏe,",
          "Áo thắm, áo tươi,", "Gạch chào đất mẹ", "Đi xây cuộc đời.", "Kìa, xe đã đến,", "Còi reo đón mời,",
          "Từng chuyến, từng chuyến", "Gạch đi đỏ trời."]
lesson(251, [75, 76],
       [picture(GACH_IMG, "Nhà máy gạch đang làm việc.", "nhà máy gạch"),
        title("Gạch đỏ", "Học thuộc lòng"),
        *sentences(*POEM40),
        passage("poem", "NGUYỄN BIỂU", breaks=[9]),
        q("1. Những câu thơ nào cho em biết viên gạch ở đây được ví như con người?", marker="?"),
        q("2. Những viên gạch đã nung chín trông tươi đẹp và cứng rắn như thế nào?"),
        q("3. Em hiểu gạch \"đi xây cuộc đời\" ý nói gạch dùng để làm gì?"),
        q("4. Phân biệt nghĩa của từ chín: cơm chín, chuối chín, gạch chín, chín tuổi."),
        q("5. Đoạn 1 là thơ mấy tiếng, đoạn 2 là thơ mấy tiếng?"),
        memorize()],
       listen(("ngùn ngụt", "đỏ rực", "lanh canh"), ("lò gạch", "than đỏ", "hơi lửa"), ("lanh canh", "ngùn ngụt", "kề vai"),
              ("rắn chắc", "đỏ trời", "sắc lửa"), ("kề vai", "quấn quanh", "đón mời"), ("đỏ rực", "đỏ trời", "lanh canh")),
       images={GACH_IMG: GACH_DESC},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)])

# 252 — Bài 41. Bến cảng Hải Phòng (tr.76–77)
POEM41 = ["Em ra thăm bến cảng", "Thăm chú ở hải quân", "Lúc trời vừa hửng sáng", "Sương sớm đang tan dần.",
          "Giữa mặt nước mênh mông", "Tàu hải quân ta đó", "Xếp hàng nối đuôi nhau", "Trông như từng dãy phố.",
          "Khi mặt trời lên tỏ", "Nước xanh chuyển màu hồng", "Cờ trên tàu như lửa", "Sáng bừng cả mặt sông."]
lesson(252, [76, 77],
       [picture("img_b252_tauf_hair_quaan", "Những con tàu hải quân trên biển.", "tàu hải quân"),
        title("Bến cảng Hải Phòng"),
        *sentences(*POEM41),
        passage("poem", "NGUYỄN HỒNG KIÊN", breaks=[4, 8]),
        *glossary("Cảng: nơi tàu, thuyền đậu để chuyển hàng.", "Hải quân: quân đội bảo vệ vùng biển."),
        q("1. Trời hửng sáng là vào khoảng mấy giờ sáng?", marker="?"),
        q("2. Em hiểu thế nào là tàu xếp hàng nối đuôi nhau?"),
        q("3. Trong bài, đoàn tàu hải quân được so sánh với cái gì?"),
        q("4. Khi trời sáng rõ, bến cảng trông đẹp như thế nào?")],
       listen(("bến cảng", "hải quân", "dãy phố"), ("hửng sáng", "sương sớm", "mênh mông"), ("mênh mông", "hửng sáng", "sáng bừng"),
              ("dãy phố", "bến cảng", "mặt sông"), ("sáng bừng", "màu hồng", "tan dần"), ("hải quân", "dãy phố", "sương sớm")),
       images={"img_b252_tauf_hair_quaan": "Mặt biển xanh lúc sáng sớm, đoàn tàu hải quân xếp hàng nối đuôi nhau, cờ đỏ "
                                           "bay trên tàu, chim hải âu bay trên trời"},
       notes=[("khac_sach", KS_ORAL)])

# 253 — Bài 42. Bốn mùa hoa thắm (Bài đọc thêm, tr.77; sách không có tranh)
lesson(253, [77],
       [title("Bốn mùa hoa thắm", "Bài đọc thêm"),
        *sentences("Cây bầu hoa trắng,", "Cây mướp hoa vàng,", "Tím tím hoa xoan,", "Đỏ tươi râm bụt.",
                   "Mào gà đỏ chót,", "Hồng ửng hoa đào,", "Cao tít hoa cau,", "Mà thơm ngan ngát.",
                   "Hoa sen trên nước,", "Hoa dừa trên mây,", "Đất nước em đây,", "Bốn mùa hoa thắm."),
        passage("poem", "Tập đọc lớp Hai – 1980")],
       listen(("hoa xoan", "râm bụt", "hoa cau"), ("hoa sen", "hoa đào", "hoa dừa"), ("ngan ngát", "cao tít", "hồng ửng"),
              ("mào gà", "cây bầu", "cây mướp"), ("cao tít", "ngan ngát", "tím tím"), ("hoa đào", "hoa sen", "mào gà")))

# 254 — Chính tả tuần 11 (tr.77–78)
lesson(254, [77, 78],
       [title("Chính tả: Bến Nhà Rồng", "Nghe đọc"),
        title("Bài viết: \"Nền trời... ban mai\".", "Phần này con nghe bố mẹ đọc rồi viết vào vở."),
        words("Nhà Rồng", "chao lượn", "tòa", "cuốn", "san sát", "nổi"),
        choose("Đố em: Trong các chữ lượn, đổi, cánh, trả, chữ nào có thể ghép với chữ chao?",
               ["lượn", "đổi", "cánh", "trả"], [0, 2]),
        choose("Chữ nào có thể ghép với chữ trao?", ["lượn", "đổi", "cánh", "trả"], [1, 3]),
        fill(["sát", "xát"], ("san sát", "sát", "sát"), ("cọ xát", "xát", "xát"), ("nằm sát đất", "sát", "sát"),
             ("xát xà phòng", "xát", "xát")),
        fill(["san", "sang"], ("san bằng", "san", "san"), ("san phẳng", "san", "san"), ("giàu sang", "sang", "sang"),
             ("sang sông", "sang", "sang")),
        title("Chính tả: Ta yêu quê ta", "Trí nhớ"),
        title("Bài viết: Cả bài.", "Phần này con nhớ lại rồi viết vào vở."),
        words("yêu", "biếc rờn", "dòng", "dâu", "tươi", "tuổi", "trổ"),
        find("Gạch dưới những chữ yêu trong bài chính tả.", {"word": ["yêu"]}, text=POEM36),
        fill(["ưi", "ươi"], ("đỏ tươi", "tươi", "ươi"), ("tốt tươi", "tươi", "ươi"), ("cưỡi ngựa", "cưỡi", "ươi"),
             ("khung cửi", "cửi", "ưi"), ("gửi thư", "gửi", "ưi")),
        fill(["ui", "uôi"], ("nhỏ tuổi", "tuổi", "uôi"), ("tủi thân", "tủi", "ui"), ("lên bảy tuổi", "tuổi", "uôi"))],
       listen(("chao lượn", "trao đổi", "trao trả"), ("cọ xát", "san sát", "giàu sang"), ("san phẳng", "sang sông", "cọ xát"),
              ("biếc rờn", "trổ bông", "dâu tằm"), ("khung cửi", "cưỡi ngựa", "gửi thư"), ("tủi thân", "nhỏ tuổi", "đỏ tươi")),
       notes=[("khac_sach", KS_WRITE), ("khac_sach", "Đố chữ ghép làm bằng chạm chọn; điền chỗ trống bằng chạm hoặc "
                                                   "kéo thẻ; gạch dưới chữ làm bằng chạm vào chữ.")],
       review=[("part1[3]", "đáp án do app soạn: chao lượn, chao cánh"), ("part1[4]", "đáp án do app soạn: trao đổi, trao trả"),
               ("part1[5]", "đáp án sát/xát"), ("part1[6]", "đáp án san/sang"), ("part1[11]", "đáp án ưi/ươi"),
               ("part1[12]", "đáp án ui/uôi")])

# 255 — Từ ngữ: Thành phố (tr.78)
lesson(255, [78],
       [title("Từ ngữ: Thành phố"),
        title("Những từ ngữ cần ghi nhớ"),
        words("thành phố", "đường phố", "cửa hàng", "nhà máy", "xe cộ", "mặt đường", "vỉa hè"),
        words("san sát", "tấp nập", "nhộn nhịp"),
        title("Bài tập: Điền từ thích hợp vào chỗ trống"),
        fill_passage(["Ở các thành phố thường có nhiều nhà cửa [san sát].",
                      "Trên đường phố, suốt ngày [xe cộ] qua lại nhộn nhịp.",
                      "Hai bên [vỉa hè] người đi bộ cũng đi lại [tấp nập].",
                      "Thủ đô Hà Nội và thành phố Hồ Chí Minh là những [thành phố] lớn nhất ở nước ta."],
                     bank=["thành phố", "đường phố", "cửa hàng", "nhà máy", "xe cộ", "mặt đường", "vỉa hè", "san sát",
                           "tấp nập", "nhộn nhịp"])],
       listen(("đường phố", "thành phố", "cửa hàng"), ("vỉa hè", "mặt đường", "xe cộ"), ("tấp nập", "nhộn nhịp", "san sát"),
              ("nhà máy", "cửa hàng", "vỉa hè"), ("nhộn nhịp", "tấp nập", "đường phố"), ("xe cộ", "nhà máy", "mặt đường")),
       notes=[("khac_sach", "Điền từ bằng chạm hoặc kéo thẻ; thẻ lấy từ các từ ngữ cần ghi nhớ, đáp án do app soạn.")],
       review=[("part1[5]", "đáp án điền từ do app soạn")])

# 256 — Ngữ pháp: Ôn tập câu (tr.79)
lesson(256, [79],
       [title("Ngữ pháp: Ôn tập câu"),
        q("1. Tại sao nói và viết phải thành câu?"),
        q("2. Khi viết, hết câu ta phải làm gì? Chữ đầu câu phải viết như thế nào?"),
        q("3. Đoạn văn sau đây có mấy câu? Viết lại, chấm câu cho đúng.",
          lines=["Nhân dân ta rất anh hùng đất nước ta vô cùng tươi đẹp chúng em cố gắng học giỏi "
                 "chúng ta xây dựng Tổ quốc giàu mạnh"]),
        q("4. Câu có mấy bộ phận chính?"),
        q("5. Bộ phận chính thứ nhất trả lời câu hỏi nào?"),
        q("6. Tìm bộ phận chính thứ nhất trong mấy câu sau:",
          lines=["Chúng em yêu quý Tổ quốc Việt Nam.", "Con rùa nhô đầu lên khỏi mặt nước.", "Dòng sông rì rào hát ca."]),
        q("7. Bộ phận chính thứ hai trả lời câu hỏi nào?"),
        q("8. Tìm bộ phận chính thứ hai trong mấy câu sau:",
          lines=["Em ra thăm bến cảng.", "Nền trời rực hồng.", "Đồng ruộng quê hương đẹp như một bức tranh."])],
       listen(("thành câu", "bộ phận", "dấu chấm"), ("dấu chấm", "viết hoa", "thành câu"), ("anh hùng", "tươi đẹp", "giàu mạnh"),
              ("tươi đẹp", "giàu mạnh", "rì rào"), ("bức tranh", "bến cảng", "con rùa"), ("rực hồng", "rì rào", "anh hùng")),
       notes=[("khac_sach", KS_ORAL)])

# 257 — Tập làm văn: Quan sát tranh và trả lời câu hỏi — Nhà máy gạch (tr.79)
lesson(257, [79],
       [title("Tập làm văn: Quan sát tranh và trả lời câu hỏi"),
        title("Đề bài: Nhà máy gạch.", "Xem tranh ở bài Gạch đỏ."),
        picture(GACH_IMG, "Con nhìn kĩ tranh nhà máy gạch nhé.", "nhà máy gạch"),
        q("1. Nhìn tranh, em có thể biết đây là nhà máy gì không? Vì sao em biết?"),
        q("2. Các chú công nhân đang làm gì?"),
        q("3. Trên bãi nhà máy, nhiều người đang làm gì bên chiếc xe vận tải?"),
        q("4. Xe vận tải chở gạch đi những đâu? Để làm gì?"),
        q("5. Em hãy kể những nhà máy khác ở quê em.")],
       listen(("nhà máy", "công nhân", "xe vận tải"), ("công nhân", "nhà máy", "lò gạch"), ("xe vận tải", "lò gạch", "công nhân"),
              ("lò gạch", "ống khói", "xe vận tải"), ("ống khói", "lò gạch", "nhà máy"), ("chở gạch", "xếp gạch", "ống khói")),
       images={GACH_IMG: GACH_DESC},
       notes=[("khac_sach", "Tập làm văn quan sát tranh: app dùng lại tranh bài Gạch đỏ; bé trả lời miệng.")],
       review=[("part1[2]", "lời dẫn tranh do app soạn")])
