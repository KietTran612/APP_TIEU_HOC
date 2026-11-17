"""Tuần 23 (mục 348–355), tr.44–49, ảnh 023–025 (tr.43 là trang chủ điểm "Nhân dân ta")."""
from l2t2lib import *

# 348 — Bài 24. Phong cảnh đền Hùng (tr.44–45)
DEN_HUNG = img(348, "đền Hùng")
DEN_HUNG_DESC = ("Đền Thượng trên đỉnh núi giữa rừng cây xanh: cổng đền mái cong, bậc đá dẫn lên, trước sân khóm hải "
                 "đường hoa đỏ rực, nhiều bướm màu bay rập rờn; xa xa dãy núi và sông nước mờ (không có người)")
DEN_HUNG_1 = ["Đền Thượng nằm chót vót trên đỉnh núi Nghĩa Cương.",
              "Trước đền, những khóm hải đường đâm bông rực đỏ, "
              "những cánh bướm nhiều màu sắc bay rập rờn | như đang múa quạt xòe hoa trước sân.",
              "Lăng của các vua Hùng ẩn trong rừng cây xanh gần đền Thượng."]
lesson(348, [44, 45],
       [picture(DEN_HUNG, "Đền Thượng trên đỉnh núi Nghĩa Cương.", "đền Hùng"),
        title("Phong cảnh đền Hùng"),
        *prose("ĐOÀN MINH TUẤN", DEN_HUNG_1,
               ["Đứng ở đây, nhìn ra xa, phong cảnh thật là đẹp.",
                "Bên phải là đỉnh Ba Vì vòi vọi, bên trái là dãy Tam Đảo như bức tường đá sừng sững.",
                "Trước mặt, ngã ba Hạc như một hồ lớn."],
               ["Mùa thu năm 1954, Bác Hồ tới thăm đền Hùng và đã căn dặn chúng ta: | "
                "\"Các vua Hùng đã có công dựng nước, Bác cháu ta phải cùng nhau giữ lấy nước\"."]),
        *glossary("Đền Hùng: đền thờ vua Hùng thuộc tỉnh Phú Thọ. Ở núi Nghĩa Cương có đền Thượng, đền Trung, đền Hạ.",
                  "Ngã ba Hạc: nơi sông Lô, sông Đà chảy vào sông Hồng."),
        q("1. Đền Hùng thờ ai? Đền Thượng nằm ở đâu? Trước đền có gì đẹp?", marker="?"),
        q("2. Đứng ở đền Thượng, nhìn ra phía xa, người ta thấy những gì?"),
        q("3. Bác Hồ căn dặn chúng ta điều gì?"),
        q("4. Trong bài này có những từ nào viết hoa? Tại sao phải viết hoa?")],
       listen(("hải đường", "cánh bướm", "rừng cây"), ("cánh bướm", "hải đường", "bức tường"), ("chót vót", "vòi vọi", "sừng sững"),
              ("vòi vọi", "chót vót", "rập rờn"), ("sừng sững", "rập rờn", "chót vót"), ("dựng nước", "giữ nước", "hải đường")),
       images={DEN_HUNG: DEN_HUNG_DESC},
       notes=[("khac_sach", "Tranh sách có khách đi lễ; app vẽ cảnh đền, không có người."),
              ("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 349 — Bài 25. Người trong một nước (Học thuộc lòng, tr.45–46; sách không có tranh riêng)
lesson(349, [45, 46],
       [title("Người trong một nước", "Học thuộc lòng"),
        *sentences("- Nhiễu điều phủ lấy giá gương", "Người trong một nước thì thương nhau cùng.",
                   "- Bầu ơi thương lấy bí cùng", "Tuy rằng khác giống nhưng chung một giàn.",
                   "- Một cây làm chẳng nên non", "Ba cây chụm lại nên hòn núi cao."),
        passage("poem", "Ca dao", breaks=[2, 4]),
        *glossary("Giá gương: ngày trước, chiếc gương để trên bàn thờ, thường đặt vào giá và phủ nhiễu điều cho đẹp, "
                  "che cho khỏi bụi."),
        q("1. Câu ca dao đầu khuyên ta điều gì?", marker="?"),
        q("2. Trong câu 2, những vật nào được ngụ ý chỉ những người cùng chung sống trên một đất nước? "
          "\"Chung một giàn\" ý nói cùng chung gì?"),
        q("3. Em hãy tìm một từ trong câu 3 nói lên sự đoàn kết giữa những người trong một nước."),
        q("4. Tìm từ gần nghĩa với non (trong câu 3)."),
        memorize()],
       listen(("nhiễu điều", "giá gương", "bầu bí"), ("giá gương", "nhiễu điều", "chụm lại"), ("bầu bí", "một giàn", "giá gương"),
              ("một giàn", "bầu bí", "núi cao"), ("chụm lại", "núi cao", "nhiễu điều"), ("núi cao", "chụm lại", "một giàn")),
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)])

# 350 — Bài 26. Voi Bà Triệu ra trận (tr.46–47)
VOI = img(350, "voi trắng")
VOI_DESC = ("Thung lũng núi Nưa giữa rừng: một con voi trắng khổng lồ mang bành phủ vải đỏ viền vàng đứng giơ vòi, "
            "hai bên là rừng cây và lau sậy, phía sau là dãy núi xanh (không có người, không có cảnh đánh nhau)")
VOI_CT = ["Từ trên đầu voi, Triệu Thị Trinh quát lớn, giục voi xông thẳng tới tên tướng Ngô.",
          "Vừa thấy con voi huỳnh huỵch xông tới, con ngựa chiến của tên tướng Ngô đã chồm dựng, | "
          "hí lên những tiếng kinh hoàng, rồi quay đầu chạy.",
          "Viên tướng Ngô bị hất tung từ trên ngựa xuống đất."]
lesson(350, [46, 47],
       [picture(VOI, "Con voi trắng khổng lồ ở thung lũng núi Nưa.", "con voi"),
        title("Voi Bà Triệu ra trận"),
        *prose("Theo Những vì sao đất nước",
               ["Đoàn quân Ngô vừa kéo đến cửa thung lũng núi Nưa, bỗng nghe dậy lên những tiếng cồng, tiếng lệnh dồn dập.",
                "Từ phía trước mặt, xộc ra một con voi trắng khổng lồ.", "Ngồi trên đầu voi là một nữ tướng.",
                "Quân ta từ các ngả trong rừng ùn ùn đổ ra, giáo mác, gươm đao vung lên sáng lóa.",
                "Quân Ngô đã bị bao vây ba mặt."],
               VOI_CT + ["Hắn định nhổm dậy chạy trốn.",
                         "Nhưng con voi khổng lồ đã đuổi kịp, lấy vòi quật ngã và lấy chân giẫm nát người hắn.",
                         "Đám quân Ngô tháo chạy khắp ngả như ong vỡ tổ.", "Thung lũng núi Nưa ngổn ngang xác giặc."]),
        *glossary("Núi Nưa: thuộc tỉnh Thanh Hóa, nơi Bà Triệu đã đóng quân trong các năm đầu của cuộc khởi nghĩa."),
        q("1. Câu nào và từ ngữ nào cho biết quân ta đông và mạnh?", marker="?"),
        q("2. Tìm những chi tiết nói lên sức mạnh ghê gớm của con voi Bà Triệu?"),
        q("3. Quân Ngô thua to và bị chết nhiều. Những từ ngữ nào cho em biết điều đó?"),
        q("4. Vì sao những từ Nưa, Ngô, Triệu Thị Trinh lại viết hoa?")],
       listen(("con voi", "thung lũng", "tiếng cồng"), ("thung lũng", "con voi", "nữ tướng"), ("nữ tướng", "tiếng cồng", "ngựa chiến"),
              ("ngựa chiến", "nữ tướng", "giáo mác"), ("huỳnh huỵch", "dồn dập", "ùn ùn"), ("dồn dập", "huỳnh huỵch", "kinh hoàng")),
       images={VOI: VOI_DESC},
       notes=[("khac_sach", KS_REAL.format(who="Bà Triệu cưỡi voi ra trận", what="con voi trắng ở thung lũng núi Nưa")),
              ("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)],
       review=[("part1[0]", "tranh thay cảnh Bà Triệu cưỡi voi đánh giặc; lời dẫn tranh do app soạn")])

# 351 — Bài 27. Gò Đống Đa (Bài đọc thêm, tr.47–48; sách không có tranh)
lesson(351, [47, 48],
       [title("Gò Đống Đa", "Bài đọc thêm"),
        *sentences("Đống Đa xưa bãi chiến trường", "Ngổn ngang xác giặc vùi xương thành gò.",
                   "Mồng năm Tết, trận thắng to", "Gió reo còn vẳng tiếng hò ba quân.",
                   "Hàng năm giỗ trận tưng bừng", "Nhớ ngày chiến thắng vang lừng núi sông.",
                   "Noi gương chiến đấu anh hùng", "Quang Trung sống mãi trong lòng chúng ta..."),
        passage("poem", "HẰNG PHƯƠNG", breaks=[2, 4, 6])],
       listen(("chiến trường", "chiến thắng", "giỗ trận"), ("giỗ trận", "chiến trường", "anh hùng"),
              ("anh hùng", "giỗ trận", "núi sông"), ("tưng bừng", "vang lừng", "ngổn ngang"),
              ("vang lừng", "tưng bừng", "anh hùng"), ("núi sông", "anh hùng", "chiến thắng")))

# 352 — Chính tả tuần 23 (tr.48)
lesson(352, [48],
       [title("Chính tả: Phong cảnh đền Hùng", "Nghe đọc"),
        title("Bài viết: \"Đền Thượng... gần đền Thượng\".", "Phần này con viết vào vở cùng bố mẹ."),
        words("Thượng", "Nghĩa Cương", "Hùng", "chót vót", "rập rờn", "màu sắc", "lăng", "ẩn"),
        q("a) Viết tên thôn, xã, huyện (hoặc phố, phường, quận) em đang ở."),
        combine_mixed("rập rờn", ("bay", "before"), ("cánh", "before")),
        combine_mixed("màu sắc", ("nhiều", "before"), ("đẹp", "after")),
        fill(["chót", "trót"], ("cao chót vót", "chót", "chót"), ("việc làm trót lọt", "trót", "trót")),
        fill(["lăng", "lăn"], ("viếng lăng Bác", "lăng", "lăng"), ("xe lăn bánh", "lăn", "lăn")),
        title("Chính tả: Tí Xíu", "Trí nhớ"),
        title("Bài viết: Cả bài.", "Phần này con viết vào vở cùng bố mẹ."),
        words("Tí Xíu", "nướng", "cật", "gửi", "rau", "biên", "cướp", "bữa"),
        combine_mixed("nướng", ("nấu", "before"), ("chả", "before"), ("bánh", "before")),
        combine_mixed("cật", ("tre", "before"), ("quả", "before")),
        fill(["gửi", "giữ"], ("giữ trật tự", "giữ", "giữ"), ("gửi thư", "gửi", "gửi")),
        fill(["biên", "biêng"], ("biên giới", "biên", "biên"), ("xanh biêng biếc", "biêng", "biêng")),
        fill(["bữa", "bửa"], ("một bữa ăn", "bữa", "bữa"), ("dao bửa củi", "bửa", "bửa"))],
       listen(("chót vót", "trót lọt", "rập rờn"), ("viếng lăng", "lăn bánh", "màu sắc"), ("nấu nướng", "bánh nướng", "tre cật"),
              ("giữ trật tự", "gửi thư", "biên giới"), ("xanh biêng biếc", "biên giới", "bữa ăn"),
              ("bữa ăn", "bửa củi", "gửi thư")),
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Viết tên nơi ở: bé nói cùng bố mẹ. Ghép chữ, điền chỗ trống làm bằng chạm thẻ.")],
       review=[("part1[4]", "ghép \"bay rập rờn\", \"cánh rập rờn\" (đứng trước) do app chọn"),
               ("part1[5]", "ghép \"nhiều màu sắc\", \"màu sắc đẹp\" do app chọn"),
               ("part1[6]", "đáp án chót/trót theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[7]", "đáp án lăng/lăn theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[11]", "ghép \"nấu nướng\", \"chả nướng\", \"bánh nướng\" do app chọn"),
               ("part1[12]", "ghép \"tre cật\" (như bài Tí Xíu), \"quả cật\" do app chọn"),
               ("part1[13]", "đáp án gửi/giữ theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[14]", "đáp án biên/biêng theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[15]", "đáp án bữa/bửa theo chính tả chuẩn (sách không in đáp án)")])

# 353 — Từ ngữ: Dân tộc Việt Nam (tr.49)
lesson(353, [49],
       [title("Từ ngữ: Dân tộc Việt Nam"),
        title("Những từ ngữ cần ghi nhớ"),
        words("dân tộc", "giống nòi", "đồng bào", "Tổ quốc", "non sông"),
        words("dựng nước", "giữ nước", "yêu nước thương nòi"),
        title("Bài tập: Điền từ ngữ thích hợp vào những chỗ trống"),
        fill_passage(["[Dân tộc|Dựng nước|Giữ nước] Việt Nam ta vốn là một dân tộc giàu lòng "
                      "[yêu nước thương nòi|dựng nước|giống nòi].",
                      "Trải qua hơn bốn nghìn năm lịch sử, ông cha ta đã ra sức [dựng nước|đồng bào|non sông] "
                      "và [giữ nước|Tổ quốc|giống nòi].",
                      "Ngày nay [đồng bào|non sông|dựng nước] cả nước ta cũng đang hăng hái xây dựng và bảo vệ "
                      "[Tổ quốc|giống nòi|dựng nước].",
                      "Nhờ đó, [non sông|đồng bào|giữ nước] chúng ta càng thêm tươi đẹp, hùng vĩ; "
                      "[giống nòi|dựng nước|giữ nước] ta càng thêm vẻ vang như điều Bác Hồ mong muốn."]),
        q("2. Đặt câu với mỗi từ: đồng bào, Tổ quốc.")],
       listen(("dân tộc", "giống nòi", "đồng bào"), ("đồng bào", "Tổ quốc", "non sông"), ("Tổ quốc", "dân tộc", "dựng nước"),
              ("non sông", "giữ nước", "giống nòi"), ("dựng nước", "giữ nước", "đồng bào"), ("giữ nước", "dựng nước", "Tổ quốc")),
       notes=[("khac_sach", "Điền từ: mỗi chỗ trống 3 thẻ do app chọn trong các từ ngữ cần ghi nhớ, tránh hai từ cùng "
                            "đúng; đáp án do app soạn."),
              ("khac_sach", KS_ORAL)],
       review=[("part1[5]", "đáp án và thẻ chọn do app soạn: Dân tộc, yêu nước thương nòi, dựng nước, giữ nước, "
                            "đồng bào, Tổ quốc, non sông, giống nòi")])

# 354 — Ngữ pháp: Danh từ chung và danh từ riêng (tiếp theo) (tr.49)
lesson(354, [49],
       [title("Ngữ pháp: Danh từ chung và danh từ riêng", "Tiếp theo"),
        q("1. Em tìm 3 danh từ riêng ở lớp em. Em tìm 3 danh từ chung chỉ tên các đồ đạc trong lớp."),
        choose("2. Hãy xếp các từ sau đây thành 2 cột (cột danh từ chung và cột danh từ riêng). "
               "Con chạm vào các danh từ riêng.",
               ["con đường", "Triệu Thị Trinh", "con sông", "cây táo", "Quang Trung", "bộ đội", "ngọn núi", "cơn mưa",
                "Võ Thị Sáu", "tàu hỏa", "Hà Nội", "Đống Đa"], [1, 4, 8, 10, 11]),
        find("3. Trong bài \"Phong cảnh đền Hùng\" có những từ nào là danh từ riêng?",
             {"word": ["thượng", "nghĩa", "cương", "hùng", "ba", "vì", "tam", "đảo"]},
             text=["Đền Thượng nằm chót vót trên đỉnh núi Nghĩa Cương.",
                   "Lăng của các vua Hùng ẩn trong rừng cây xanh gần đền Thượng.",
                   "Bên phải là đỉnh Ba Vì vòi vọi, bên trái là dãy Tam Đảo như bức tường đá sừng sững."])],
       listen(("con đường", "con sông", "ngọn núi"), ("cây táo", "cơn mưa", "tàu hỏa"), ("bộ đội", "con sông", "cây táo"),
              ("Hà Nội", "Đống Đa", "Quang Trung"), ("Đống Đa", "Hà Nội", "con đường"), ("tàu hỏa", "bộ đội", "cơn mưa")),
       notes=[("khac_sach", "Xếp 2 cột thành chạm vào các danh từ riêng; câu 3 app hiện ba câu của bài để bé chạm."),
              ("khac_sach", KS_ORAL)],
       review=[("part1[2]", "danh từ riêng do app chọn: Triệu Thị Trinh, Quang Trung, Võ Thị Sáu, Hà Nội, Đống Đa"),
               ("part1[3]", "danh từ riêng do app chọn trên ba câu của bài: Thượng, Nghĩa Cương, Hùng, Ba Vì, Tam Đảo")])

# 355 — Tập làm văn: Trả lời câu hỏi — Phong cảnh đền Hùng (tr.49)
lesson(355, [49],
       [title("Tập làm văn: Trả lời câu hỏi"),
        title("Đề bài: Phong cảnh đền Hùng.", "Xem tranh ở bài Phong cảnh đền Hùng."),
        picture(DEN_HUNG, "Con nhớ lại cảnh đền Hùng nhé.", "đền Hùng"),
        q("1. Đền Thượng nằm ở đâu? Lăng các vua Hùng ở đâu?"),
        q("2. Trước đền có gì đẹp?"),
        q("3. Đứng trên đỉnh Nghĩa Cương nhìn các phía, ta thấy những gì?"),
        q("4. Đến thăm đền Hùng, Bác Hồ đã căn dặn ta điều gì?")],
       listen(("đền Thượng", "lăng", "Nghĩa Cương"), ("Nghĩa Cương", "đền Thượng", "Ba Vì"), ("Ba Vì", "Tam Đảo", "đền Thượng"),
              ("Tam Đảo", "Ba Vì", "hải đường"), ("hải đường", "cánh bướm", "Tam Đảo"), ("cánh bướm", "hải đường", "Nghĩa Cương")),
       images={DEN_HUNG: DEN_HUNG_DESC},
       notes=[("khac_sach", KS_TLC)],
       review=[("part1[2]", "lời dẫn tranh do app soạn")])
print("tuần 23 xong")
