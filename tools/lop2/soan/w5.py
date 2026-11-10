"""Tuần 5 (mục 203–210), tr.30–36, ảnh 016–019. Tr.37 là trang bìa chủ điểm "Gia đình" (không thành bài)."""
from l2lib import *

# 203 — Bài 16. Có chí thì nên (tr.30–31)
lesson(203, [30, 31],
       [picture("img_b203_phaafn_thuwowngr", "Thầy giáo trao phần thưởng cho bạn Bắc.", "phần thưởng"),
        title("Có chí thì nên"),
        *prose("A-MI-XI (\"Những tấm lòng cao cả\")",
               ["Đầu năm học, Bắc được bố đưa đến trường.", "Bố cậu nói với thầy giáo:",
                "\"Xin thầy kiên nhẫn, thật kiên nhẫn, vì con tôi tối dạ lắm\"."],
               ["Từ đó, có người gọi cậu là \"Tối dạ\".", "Bắc không giận và quyết trả lời bằng việc làm.",
                "Cậu học thật chăm, khó khăn không nản.", "Ở lớp, điều gì chưa hiểu, cậu xin thầy giảng lại.",
                "Ở nhà, cậu học bài thật thuộc và làm bài đầy đủ.",
                "Chỉ ba tháng sau, nhờ siêng năng, cần cù, cậu vượt lên đầu lớp.",
                "Trước đây, cậu không biết tí gì về phép tính,", "bài chép mắc nhiều lỗi chính tả.",
                "Thế mà giờ đây, cậu giải được các bài tính đố,",
                "viết đúng chính tả và hiểu cặn kẽ các bài học."],
               ["Cuối năm, khi trao phần thưởng cho cậu, thầy giáo phải thốt lên:", "\"Hoan hô em Bắc!",
                "Em đã nêu một gương sáng về tính cần cù và kiên nhẫn.", "Thật là có chí thì nên!\"."]),
        *glossary("Tối dạ: chậm hiểu, chậm nhớ.",
                 "Có chí thì nên: định làm việc gì mà cố gắng làm bằng được thì sẽ thành công."),
        q("1. Bạn bè gọi Bắc là gì? Thái độ của Bắc ra sao?", marker="?"),
        q("2. Ở lớp và ở nhà, Bắc chăm học như thế nào? Bắc đã có những tiến bộ gì?"),
        q("3. Tại sao Bắc được phần thưởng cuối năm học?"),
        q("4. Em đặt câu với mỗi từ: cần cù, kiên nhẫn.")],
       listen(("kiên nhẫn", "cần cù", "siêng năng"), ("tối dạ", "khó khăn", "kiên nhẫn"),
              ("cần cù", "gương sáng", "tối dạ"), ("phần thưởng", "phép tính", "chính tả"),
              ("gương sáng", "phần thưởng", "cặn kẽ"), ("cặn kẽ", "đầy đủ", "giảng lại")),
       images={"img_b203_phaafn_thuwowngr": "Trong lớp học, thầy giáo đeo kính đứng trước bảng đen trao phần thưởng cho "
                                            "cậu học trò nhỏ; các bạn ngồi ở bàn vỗ tay, lọ hoa trên bàn thầy"},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 204 — Bài 17. Khuyên chăm học (Học thuộc lòng, tr.31–32; sách không có tranh)
PROVERBS = ["Có học mới hay, có cày mới biết.", "Dốt đến đâu, học lâu cũng biết.",
            "Muốn biết phải hỏi, muốn giỏi phải học.", "Không cày không có thóc, không học không biết chữ.",
            "Đi một ngày đàng, học một sàng khôn."]
lesson(204, [31, 32],
       [title("Khuyên chăm học", "Học thuộc lòng"),
        *sentences(*PROVERBS),
        passage("poem", "Tục ngữ Việt Nam"),
        *glossary("Đàng: đường.", "Sàng: vật đan bằng nan tre thưa, to bằng cái mâm, dùng để sàng cho gạo rời khỏi trấu.",
                 "Một sàng khôn: nhiều điều khôn."),
        find("1. Trong năm câu trên, mỗi câu đều có hai tiếng cùng vần với nhau. Em hãy tìm các tiếng cùng vần đó.",
             {"word": ["hay", "cày", "đâu", "lâu", "hỏi", "giỏi", "thóc", "học", "đàng", "sàng"]}, marker="?"),
        q("2. Bốn câu đầu khuyên chúng ta những điều gì?"),
        q("3. Khi đi nhiều nơi, ta cũng có thể hiểu biết thêm những điều có ích. Em hãy kể một ví dụ."),
        memorize()],
       listen(("cày", "thóc", "chữ"), ("hỏi", "giỏi", "học"), ("sàng", "đàng", "khôn"),
              ("thóc", "chữ", "sàng"), ("lâu", "đâu", "dốt"), ("khôn", "giỏi", "hay")),
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)],
       review=[("part1[8]", "tiếng cùng vần do app chọn: hay–cày, đâu–lâu, hỏi–giỏi, thóc–học, đàng–sàng")])

# 205 — Bài 18. Chú gà trống ưa dậy sớm (tr.32–33)
lesson(205, [32, 33],
       [picture("img_b205_gaf_troongs", "Chú gà trống dậy sớm chạy ra giữa sân.", "gà trống"),
        title("Chú gà trống ưa dậy sớm"),
        *prose("Tập đọc 1 – 1980",
               ["Mấy hôm nay trời rét cóng tay.", "Càng về sáng, tiết trời càng lạnh giá.",
                "Trong bếp, bác mèo mướp vẫn nằm lì bên đống tro ấm.",
                "Bác lim dim đôi mắt, luôn miệng gừ gừ kêu: \"Eo ôi! Rét! Rét!\"."],
               ["Thế nhưng mới sớm tinh mơ, chú gà trống đã chạy tót ra giữa sân.",
                "Chú vươn mình, dang đôi cánh to, khỏe như hai chiếc quạt,", "vỗ phành phạch.",
                "Cái mào đỏ rực.", "Chú rướn cổ lên gáy \"o... o!\" vang cả xóm.",
                "Bộ lông màu tía trông thật đẹp mắt.",
                "Chú chạy đi chạy lại quanh sân, đôi đùi mập mạp, chắc nịch."]),
        q("1. Tìm những từ cho em biết trời rất rét.", marker="?"),
        q("2. Tìm những từ tả dáng điệu khỏe khoắn của chú gà trống."),
        q("3. Chú gà trống này rất đáng khen? Tại sao?"),
        q("4. Đặt một câu với từ mập mạp.")],
       listen(("rét cóng", "lạnh giá", "tro ấm"), ("lim dim", "gừ gừ", "phành phạch"),
              ("phành phạch", "đỏ rực", "chắc nịch"), ("mập mạp", "chắc nịch", "lim dim"),
              ("sớm tinh mơ", "lạnh giá", "đẹp mắt"), ("đỏ rực", "màu tía", "mập mạp")),
       images={"img_b205_gaf_troongs": "Sáng sớm, chú gà trống mào đỏ, lông đuôi cong đứng giữa sân lát gạch; trong "
                                       "khung cửa bếp, con mèo mướp nằm cuộn tròn lim dim ngủ; cây hoa đại ở góc sân"},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 206 — Bài 19. Vượt bậc (Bài đọc thêm, tr.33–34; sách không có tranh)
lesson(206, [33, 34],
       [title("Vượt bậc", "Bài đọc thêm"),
        *prose("TRẦN NINH HỒ",
               ["Hôm chủ nhật, bố và Nam đến nhà bác chơi.", "Nam có một chuyện rất thú.",
                "Nam sẽ kể cho các chị nghe.", "Tháng này, Nam vượt từ thứ hai mươi lên thứ tám trong lớp.",
                "Nam được cô giáo khen là học khá."],
               ["Vừa xuống xe, Nam chạy ngay đến chỗ chị Bích, chị Diệp."],
               ["- Chị Bích, chị Diệp ơi!", "Tháng này xếp thứ, em vượt được những mười hai bậc đấy nhé!"],
               ["- Thế cơ à! - Bích và Diệp cùng reo lên."],
               ["Nhìn hai chị tròn xoe mắt, Nam càng thích chí."],
               ["- Thế còn chị Diệp vượt được mấy bậc?"],
               ["- Được... - Diệp bối rối - được một bậc thôi!"],
               ["- Thế chị Bích?"],
               ["- Chị thì... - Bích càng tỏ ra bối rối hơn - chị thì chả vượt được bậc nào."],
               ["- Thế các chị có được cô giáo khen là khá không?"],
               ["- Không."],
               ["- Thế cô giáo khen thế nào?"],
               ["- Cô giáo khen là... giỏi!"],
               ["Ô! Nam ngẩn người ra và chớp mắt lia lịa.", "Giỏi thì hơn khá đứt đuôi đi rồi.",
                "Nhưng sao các chị ấy vượt được ít bậc như thế mà lại được khen là giỏi nhỉ?", "Lạ quá."],
               ["Chợt bố Nam đứng bên cạnh cười rất to:"],
               ["- Vì chị Diệp tháng trước xếp thứ nhì, tháng này lên thứ nhất, vượt được một bậc.",
                "Còn chị Bích thì toàn xếp thứ nhất thôi.", "Con hiểu chưa?"],
               ["À, bây giờ thì Nam hiểu.", "Các chị ấy giỏi thật.", "Thế mà chả ai nói trước cho Nam biết!"])],
       listen(("vượt bậc", "xếp thứ", "học khá"), ("bối rối", "thích chí", "lia lịa"),
              ("tròn xoe", "chớp mắt", "đứt đuôi"), ("thứ nhất", "thứ nhì", "thứ tám"),
              ("thích chí", "bối rối", "tròn xoe"), ("chớp mắt", "ngẩn người", "vượt bậc")),
       notes=[("khac_sach", KS_SPLIT)])

# 207 — Chính tả tuần 5 (tr.34–35)
lesson(207, [34, 35],
       [title("Tập chép: Có chí thì nên", "Nhìn sách"),
        title("Bài viết: \"Có người gọi cậu là... vượt lên đầu lớp\".", "Phần này con chép vào vở cùng bố mẹ."),
        words("Bắc", "Tối dạ", "quyết", "giảng", "vượt", "đầy đủ"),
        fill(["vượt", "vược"], ("vượt qua sông", "vượt", "vượt"), ("con cá vược", "vược", "vược"),
             ("vượt bậc", "vượt", "vượt")),
        fill(["dạ", "rạ"], ("mát lòng mát dạ", "dạ", "dạ"), ("mái lợp bằng rạ", "rạ", "rạ")),
        q("Đố em: Chữ gì có thể ghép với chữ quyết? (thí dụ cương, tâm,...)"),
        title("Chính tả: Chú gà trống ưa dậy sớm", "Nghe đọc"),
        title("Bài viết: \"Mới sớm tinh mơ... chắc nịch\".", "Phần này con nghe bố mẹ đọc rồi viết vào vở."),
        words("tót", "phành phạch", "o... o", "dang", "rướn", "vươn", "vỗ"),
        fill(["d", "r"], ("dang tay", "dang", "d"), ("lạc rang", "rang", "r")),
        fill(["n", "ng"], ("vươn vai", "vươn", "n"), ("vương vãi khắp nơi", "vương", "ng"),
             ("vươn lên hàng đầu", "vươn", "n"), ("vương vấn", "vương", "ng"))],
       listen(("quyết", "giảng", "vượt"), ("đầy đủ", "tối dạ", "vượt bậc"), ("cá vược", "vượt qua", "mái rạ"),
              ("phành phạch", "dang tay", "rướn cổ"), ("vươn vai", "lạc rang", "vỗ cánh"),
              ("vương vấn", "dang tay", "phành phạch")),
       notes=[("khac_sach", KS_WRITE), ("khac_sach", "Điền chỗ trống làm bằng chạm hoặc kéo thẻ; "
                                                   "câu đố ghép chữ bé trả lời miệng.")],
       review=[("part1[3]", "đáp án vượt/vược theo chính tả chuẩn"), ("part1[4]", "đáp án dạ/rạ theo chính tả chuẩn"),
               ("part1[9]", "đáp án d/r: dang tay, lạc rang"),
               ("part1[10]", "đáp án n/ng: vươn vai, vương vãi, vươn lên, vương vấn")])

# 208 — Từ ngữ: Ôn tập (tr.35)
lesson(208, [35],
       [title("Từ ngữ: Ôn tập"),
        q("1. Ngày khai trường là ngày gì? Ta còn gọi là ngày gì?"),
        q("2. Năm học có mấy tháng? Bắt đầu từ tháng nào? Năm thường có mấy tháng? Bắt đầu từ tháng nào? "
          "Tại sao lại gọi là năm học 1999 – 2000?"),
        q("3. Trong nhà trường, học sinh làm gì? Thầy, cô giáo làm việc gì? Thầy (cô) hiệu trưởng làm công việc gì?"),
        q("4. Tìm một số từ nói về những tính tốt của học sinh."),
        q("5. Đặt câu với mỗi từ: khai giảng, chăm học, dạy bảo, sạch sẽ, gọn gàng.")],
       listen(("khai giảng", "khai trường", "năm học"), ("chăm học", "dạy bảo", "gọn gàng"),
              ("dạy bảo", "chăm học", "sạch sẽ"), ("sạch sẽ", "gọn gàng", "khai giảng"),
              ("gọn gàng", "sạch sẽ", "hiệu trưởng"), ("hiệu trưởng", "học sinh", "cô giáo")),
       notes=[("khac_sach", KS_ORAL)])

# 209 — Ngữ pháp: Câu (tr.36)
lesson(209, [36],
       [title("Ngữ pháp: Câu"),
        picture("img_b209_laam_vaf_mej", "Lâm cầm quyển vở chạy đến nói với mẹ.", "quyển vở"),
        q("1. Trong tranh vẽ, Lâm đang nói gì với mẹ? Nói như vậy đã thành câu chưa?",
          lines=["Mẹ ơi! Quyển vở này..."]),
        q("Mẹ Lâm có hiểu ý Lâm muốn nói gì không? Tại sao?"),
        q("Nói và viết phải như thế nào để người khác hiểu được?"),
        q("Em thử nói tiếp hộ Lâm cho thành câu."),
        q("2. Một bạn viết thư cho bố như sau. Bạn này viết như trên đã thành câu chưa? Còn thiếu sót gì? "
          "Ở đây, có thể tách ra thành mấy câu?",
          lines=["Bố ạ.", "Tuần này, em Mai học rất tiến bộ bài tập viết em được sáu điểm, bài tập đọc em được "
                          "tám điểm cô giáo khen em khi nào bố về, nhớ mua cho em một cái cặp sách."]),
        q("3. Em hãy chép lại vào vở bức thư trên cho đúng.")],
       listen(("quyển vở", "cặp sách", "bức thư"), ("tiến bộ", "tập viết", "tập đọc"),
              ("tập viết", "tập đọc", "quyển vở"), ("cặp sách", "quyển vở", "tiến bộ"),
              ("bức thư", "cặp sách", "tập viết"), ("tập đọc", "tiến bộ", "bức thư")),
       images={"img_b209_laam_vaf_mej": "Cô bé Lâm buộc tóc đuôi gà, hai tay cầm quyển vở giơ lên khoe mẹ; người mẹ "
                                        "mặc áo hoa đứng cúi nhìn bé, bên cạnh là chiếc bàn (không có chữ, không có "
                                        "khung lời thoại)"},
       notes=[("khac_sach", "Lời Lâm nói trong tranh của sách hiện thành dòng chữ dưới câu hỏi, chạm để nghe. "
                            "Bé trả lời miệng cùng bố mẹ; phần chép thư vào vở bé viết cùng bố mẹ.")],
       review=[("part1[1]", "tranh vẽ lại không có khung lời thoại; lời dẫn tranh do app soạn")])

# 210 — Tập làm văn: Điền từ — Có chí thì nên (tr.36)
lesson(210, [36],
       [title("Tập làm văn: Điền từ"),
        title("Đề bài: Có chí thì nên.", "Em hãy tìm từ thích hợp để điền vào chỗ trống."),
        fill_passage(["Bắc học rất [chăm|lười|chậm].",
                      "Cậu học ở lớp và ở nhà rất [siêng năng|lười biếng|tối dạ].",
                      "Bài nào chưa hiểu kĩ, cậu xin thầy [giảng|khen|thưởng] thêm.",
                      "Cuối năm, Bắc được trao [phần thưởng|quyển vở|bài tập].",
                      "Thầy giáo nói: \"Hoan hô em Bắc! Em đã nêu một [gương sáng|bài học|lời khuyên] về học tập\"."])],
       listen(("phần thưởng", "gương sáng", "siêng năng"), ("siêng năng", "lười biếng", "kiên nhẫn"),
              ("gương sáng", "phần thưởng", "học tập"), ("học tập", "siêng năng", "giảng"),
              ("giảng", "chăm", "khen"), ("chăm", "giảng", "phần thưởng")),
       notes=[("khac_sach", "Sách để trống, không cho sẵn từ: app cho mỗi chỗ trống 3 thẻ để chọn; "
                            "thẻ và đáp án do app soạn theo bài Có chí thì nên.")],
       review=[("part1[2]", "thẻ chọn và đáp án điền chỗ trống do app soạn")])
