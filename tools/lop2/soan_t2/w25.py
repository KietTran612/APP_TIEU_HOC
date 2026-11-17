"""Tuần 25 (mục 363–370), tr.55–61, ảnh 028–031."""
from l2t2lib import *

# 363 — Bài 31. Đứng gác nơi biên giới (tr.55; sách không có tranh)
GAC_1 = ["Sớm nay đứng gác, anh Thái thấy Tổ quốc đẹp vô cùng.", "Mặt trời hé sáng, rừng núi như tỏa hào quang.",
         "Những tia nắng vàng hắt từ sau dãy núi lên nền trời ửng hồng.", "Mặt trời lên, sương tan dần.",
         "Từng cụm mây bạc vật vờ giữa lưng chừng núi, tan vào khe núi.", "Thác nước đổ ầm ầm hiện ra trắng xóa.",
         "Rừng cây xanh rung rinh.", "Chim chóc cất tiếng ca."]
lesson(363, [55],
       [title("Đứng gác nơi biên giới"),
        *prose("LÊ ĐÀO", GAC_1,
               ["Xa xa trong thung lũng, thấp thoáng bóng người lom khom trên ruộng lúa vàng."],
               ["Phong cảnh ở đây thật là hùng vĩ.", "Anh Thái nhìn đây đó, tình yêu đất nước rộn ràng trong lòng.",
                "Anh siết chặt thêm cây súng trong tay."]),
        *glossary("Hào quang: ánh sáng rực rỡ tỏa ra khắp bốn phía."),
        q("1. Em hãy tìm trong bài những từ ngữ nói lên vẻ đẹp của cảnh núi rừng buổi sớm.", marker="?"),
        q("2. Những từ nào tả âm thanh của núi rừng buổi sớm?"),
        q("*3. Anh Thái \"siết chặt thêm cây súng trong tay\" để làm gì?"),
        q("*4. Tìm một từ ghép trong đó có tiếng \"gác\". Đặt một câu với từ đó."),
        q("5. Tìm trong bài một danh từ chung chỉ loài vật và một danh từ chung chỉ đồ vật.")],
       listen(("hào quang", "thác nước", "mây bạc"), ("thác nước", "hào quang", "thung lũng"), ("thung lũng", "mây bạc", "khe núi"),
              ("rung rinh", "lom khom", "rộn ràng"), ("lom khom", "rung rinh", "thấp thoáng"), ("thấp thoáng", "rộn ràng", "lom khom")),
       notes=[("khac_sach", KS_ORAL)])

# 364 — Bài 32. Chú hải quân (Học thuộc lòng, tr.56–57)
lesson(364, [56, 57],
       [picture(img(364, "hải quân"), "Chú hải quân đứng gác ngoài hải đảo.", "hải quân"),
        title("Chú hải quân", "Học thuộc lòng"),
        *sentences("Đứng canh ngày, canh đêm", "Ngoài xa vời hải đảo", "Kìa! Bóng chú hải quân", "Dưới trời xanh trứng sáo.",
                   "Mặc nắng mưa gió bão", "Cây súng chú chắc tay", "Quân thù mà ló mặt", "Biển lớn sẽ vùi thây.",
                   "Em mong ngày khôn lớn", "Sẽ vượt sóng ra khơi", "Cũng cầm chắc tay súng", "Giữ lấy biển lấy trời."),
        passage("poem", "VĂN ĐÀI", breaks=[4, 8]),
        q("1. Trong bài, chú hải quân làm nhiệm vụ gì?", marker="?"),
        q("2. Những câu nào, từ ngữ nào cho biết nỗi vất vả, gian khổ của chú hải quân? (Tìm trong khổ 1 và khổ 2)."),
        q("3. Những hình ảnh nào nói lên niềm mong ước của em bé? (khổ 3)."),
        q("*4. Tìm trong bài hai từ ghép có tiếng hải. Đặt câu với mỗi từ đó."),
        memorize()],
       listen(("hải quân", "hải đảo", "biển lớn"), ("hải đảo", "hải quân", "trứng sáo"), ("trứng sáo", "gió bão", "hải đảo"),
              ("gió bão", "trứng sáo", "ra khơi"), ("ra khơi", "biển lớn", "gió bão"), ("biển lớn", "ra khơi", "hải quân")),
       images={img(364, "hải quân"): "Mỏm đá trên hòn đảo nhỏ có bụi cỏ: chú hải quân mặc áo thủy thủ kẻ sọc, đội mũ "
                                     "hải quân có dải băng, đứng gác, hai tay cầm ống nhòm nhìn ra biển xanh; bên cạnh "
                                     "là cột cờ cao có lá cờ bay trong gió; xa xa có con tàu, chim hải âu bay "
                                     "(không vẽ súng hay vũ khí nào)"},
       notes=[("khac_sach", "Sách vẽ chú hải quân cầm súng; app vẽ chú đứng gác cầm ống nhòm bên cột cờ "
                            "(tranh cho trẻ nhỏ không vẽ vũ khí)."),
              ("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)],
       review=[("part1[0]", "tranh thay súng bằng ống nhòm; lời dẫn tranh do app soạn")])

# 365 — Bài 33. Bộ đội đi trên Trường Sơn (tr.57–58)
TRUONG_SON = img(365, "Trường Sơn")
TRUONG_SON_DESC = ("Dốc núi rừng Trường Sơn trơn lầy: đoàn bộ đội đội mũ tai bèo, đeo ba lô to, nối nhau lom khom "
                   "leo lên dốc cao giữa những thân cây rừng, người đi trước kéo tay người đi sau")
lesson(365, [57, 58],
       [picture(TRUONG_SON, "Đoàn bộ đội nối nhau leo dốc Trường Sơn.", "bộ đội"),
        title("Bộ đội đi trên Trường Sơn"),
        *prose("DƯƠNG THỊ XUÂN QUÝ",
               ["Đường lên dốc trơn và lầy.", "Người nọ đi tiếp sau người kia.",
                "Đoàn quân nối thành vệt dài từ thung lũng tới đỉnh cao | như một sợi dây kéo thẳng đứng.",
                "Họ nhích từng bước.",
                "Nhìn lên chỉ thấy những chiếc ba lô lù lù nối nhau | trên những cái lưng cong cong.",
                "Nhìn xuống là những chiếc mũ tai bèo lúp xúp | trên những mái đầu đang cắm về phía trước.",
                "Những khuôn mặt đỏ bừng."],
               ["Đoàn quân đột ngột chuyển mạnh.", "Những dặm rừng đỏ lên vì bom Mĩ.",
                "Những rặng rừng xám đi vì chất độc hóa học Mĩ.",
                "Những dặm rừng đen, cây cháy thành than chọc lên nền trời đầy mây...",
                "Tất cả, tất cả lướt qua rất nhanh."]),
        q("1. Câu nào cho em biết bộ đội đang leo lên một cái dốc rất cao trên đỉnh Trường Sơn?", marker="?"),
        q("2. Tìm những từ ngữ diễn tả nỗi vất vả, gian khổ của đoàn quân đang leo dốc."),
        q("*3. Đỏ lên, xám đi, đen, cháy thành than... những từ ngữ đó nói lên tội ác gì của giặc Mĩ?"),
        q("4. Tìm trong bài những từ láy gồm 2 tiếng lặp lại. Đặt câu với mỗi từ đó."),
        q("5. \"Trường Sơn\" là danh từ riêng chỉ núi. Em có nhận xét gì về cách viết từ đó?")],
       listen(("ba lô", "mũ tai bèo", "thung lũng"), ("mũ tai bèo", "ba lô", "sợi dây"), ("lù lù", "cong cong", "lúp xúp"),
              ("cong cong", "lù lù", "đỏ bừng"), ("lúp xúp", "đỏ bừng", "lù lù"), ("thung lũng", "sợi dây", "ba lô")),
       images={TRUONG_SON: TRUONG_SON_DESC},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 366 — Bài 34. Những cái chân (Bài đọc thêm, tr.58–59; sách không có tranh)
lesson(366, [58, 59],
       [title("Những cái chân", "Bài đọc thêm"),
        *sentences("Cái gậy có một chân", "Biết giúp bà khỏi ngã.", "Chiếc com pa bố vẽ", "Có chân đứng, chân quay.",
                   "Cái kiềng đun hằng ngày", "Ba chân xòe trong lửa.", "Chẳng bao giờ đi cả", "Là chiếc bàn bốn chân.",
                   "Riêng cái võng Trường Sơn", "Không chân đi khắp nước."),
        passage("poem", "VŨ QUẦN PHƯƠNG")],
       listen(("cái gậy", "com pa", "cái kiềng"), ("com pa", "cái gậy", "cái võng"), ("cái kiềng", "cái bàn", "com pa"),
              ("cái bàn", "cái kiềng", "cái gậy"), ("cái võng", "cái bàn", "cái kiềng"), ("bốn chân", "ba chân", "một chân")))

# 367 — Chính tả tuần 25 (tr.59)
lesson(367, [59],
       [title("Chính tả: Đứng gác nơi biên giới", "Nghe đọc"),
        title("Bài viết: \"Sớm nay... hào quang\" và \"Xa xa... trong tay\".", "Phần này con viết vào vở cùng bố mẹ."),
        words("Thái", "Tổ quốc", "tỏa", "thoáng", "khom", "siết", "rừng", "súng", "gác", "quang", "vĩ"),
        q("a) Sắp xếp các chữ sau đây thành hai câu:", lines=["người, thấp thoáng, bóng", "rừng, hào quang, núi, tỏa."]),
        fill(["r", "d"], ("núi rừng", "rừng", "r"), ("đứng dừng lại", "dừng", "d")),
        fill(["n", "ng"], ("hào quang", "quang", "ng"), ("quan trọng", "quan", "n"), ("vinh quang", "quang", "ng")),
        fill(["vĩ", "vỉ"], ("hùng vĩ", "vĩ", "vĩ"), ("vỉ ruồi", "vỉ", "vỉ")),
        title("Chính tả: Người trong một nước", "Trí nhớ"),
        title("Bài viết: Cả bài.", "Phần này con viết vào vở cùng bố mẹ."),
        words("giá", "giống", "giàn", "chụm", "chung", "nhiễu điều", "phủ"),
        fill(["chung", "trung"], ("chung lòng", "chung", "chung"), ("chung sức", "chung", "chung"),
             ("trung thành", "trung", "trung"), ("trung thực", "trung", "trung")),
        fill(["phủ", "phũ"], ("bao phủ", "phủ", "phủ"), ("phũ phàng", "phũ", "phũ"), ("che phủ", "phủ", "phủ"))],
       listen(("núi rừng", "dừng lại", "hào quang"), ("quan trọng", "vinh quang", "hùng vĩ"), ("vỉ ruồi", "hùng vĩ", "quan trọng"),
              ("chung lòng", "trung thành", "chung sức"), ("trung thực", "chung sức", "bao phủ"), ("phũ phàng", "che phủ", "trung thực")),
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Sắp xếp chữ thành câu: bé nói cùng bố mẹ; điền chỗ trống, ghép đúng làm bằng chạm thẻ."),
              ("khac_sach", "Sách in \"Xa ra... trong tay\"; đoạn bài là \"Xa xa... trong tay\", app ghi theo bài.")],
       review=[("part1[1]", "sách in \"Xa ra\", app ghi \"Xa xa\" theo bài đọc"),
               ("@a) Sắp xếp", "câu gợi ý cho bố mẹ: \"Bóng người thấp thoáng.\", \"Rừng núi tỏa hào quang.\""),
               ("part1[4]", "đáp án r/d theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[5]", "đáp án n/ng theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[6]", "đáp án vĩ/vỉ theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[10]", "đáp án chung/trung theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[11]", "đáp án phủ/phũ theo chính tả chuẩn (sách không in đáp án)")])

# 368 — Từ ngữ: Quân đội (tr.60)
lesson(368, [60],
       [title("Từ ngữ: Quân đội"),
        title("Những từ ngữ cần ghi nhớ"),
        words("bộ đội", "bộ binh", "hải quân", "không quân", "biên giới"),
        words("tuần tiễu", "bảo vệ", "nắm chắc tay súng"),
        title("Bài tập: Điền từ ngữ thích hợp vào những chỗ trống"),
        fill_passage(["Gia đình bạn Đông có ba người anh đều đi [bộ đội|biên giới|tuần tiễu].",
                      "Anh Thu là bộ đội [bộ binh|tuần tiễu|bảo vệ] hiện đóng trên [biên giới|bộ đội|bảo vệ].",
                      "Anh Hạ là bộ đội [hải quân|biên giới|bảo vệ] chuyên đi [tuần tiễu|bộ binh|biên giới] trên mặt biển.",
                      "Còn anh Xuân lớn tuổi nhất là chiến sĩ [không quân|biên giới|tuần tiễu] ngày nào cũng cất cánh "
                      "làm nhiệm vụ canh gác bầu trời của Tổ quốc.",
                      "Các anh đều [nắm chắc tay súng|tuần tiễu|biên giới] sẵn sàng chiến đấu để "
                      "[bảo vệ|bộ binh|hải quân] đất nước quê hương."]),
        q("*2. Bài tập ở nhà: Đặt câu với mỗi từ: canh gác, canh phòng, canh giữ.")],
       listen(("bộ đội", "bộ binh", "hải quân"), ("hải quân", "không quân", "biên giới"), ("không quân", "hải quân", "bộ binh"),
              ("biên giới", "tuần tiễu", "bảo vệ"), ("tuần tiễu", "biên giới", "bộ đội"), ("bảo vệ", "bộ đội", "tuần tiễu")),
       notes=[("khac_sach", "Điền từ: mỗi chỗ trống 3 thẻ do app chọn trong các từ ngữ cần ghi nhớ, tránh hai từ cùng "
                            "đúng; đáp án do app soạn."),
              ("khac_sach", "Sách có tranh chú hải quân, chú bộ binh, chú không quân; app không vẽ (bài từ ngữ)."),
              ("khac_sach", KS_ORAL)],
       review=[("part1[5]", "đáp án và thẻ chọn do app soạn: bộ đội, bộ binh, biên giới, hải quân, tuần tiễu, không quân, "
                            "nắm chắc tay súng, bảo vệ")])

# 369 — Ngữ pháp: Danh từ riêng. Cách viết hoa tên người (tr.61)
lesson(369, [61],
       [title("Ngữ pháp: Danh từ riêng", "Cách viết hoa tên người"),
        *rule("Tên người gồm 2 tiếng: Lê Lợi, Trần Phú.", "Tên người gồm 3 tiếng: Hồ Chí Minh, Tôn Đức Thắng.",
              "Tên người gồm 4 tiếng: Nguyễn Thị Minh Khai, Lê Thị Hồng Gấm."),
        *rule("Tên người Việt Nam gồm 2 tiếng, 3 tiếng, 4 tiếng... đều phải viết hoa chữ cái ở đầu mỗi tiếng."),
        q("1. Hãy viết đúng họ tên 3 bạn ở tổ em."),
        q("2. Em hãy viết lại cho đúng chính tả tất cả các tên người sau đây:",
          lines=["nguyễn bá ngọc", "lê văn tám", "vừ a dính", "trần quốc toản", "võ thị sáu", "kim đồng"])],
       listen(("tên người", "viết hoa", "chữ cái"), ("viết hoa", "tên người", "họ tên"), ("chữ cái", "họ tên", "viết hoa"),
              ("họ tên", "chữ cái", "tên người"), ("Lê Lợi", "Trần Phú", "Kim Đồng"), ("Kim Đồng", "Lê Lợi", "Trần Phú")),
       notes=[("khac_sach", "Viết họ tên, viết lại tên người cho đúng: bé nói cách viết hoa cùng bố mẹ.")])

# 370 — Tập làm văn: Trả lời câu hỏi — Bộ đội đi trên Trường Sơn (tr.61)
lesson(370, [61],
       [title("Tập làm văn: Trả lời câu hỏi"),
        title("Đề bài: Bộ đội đi trên Trường Sơn.", "Xem tranh ở bài Bộ đội đi trên Trường Sơn."),
        picture(TRUONG_SON, "Con nhớ lại đoàn bộ đội leo dốc Trường Sơn nhé.", "bộ đội"),
        q("1. Đi trên đường Trường Sơn, các chú bộ đội gặp những khó khăn gì?"),
        q("2. Các chú phải đi như thế nào?"),
        q("3. Lên dốc cao như thế, nhìn lên ta thấy có gì lạ mắt?"),
        q("4. Nhìn xuống, ta thấy như thế nào?"),
        q("5. Tại sao khuôn mặt các chú lại đỏ bừng?")],
       listen(("bộ đội", "dốc cao", "ba lô"), ("dốc cao", "bộ đội", "khuôn mặt"), ("ba lô", "khuôn mặt", "dốc cao"),
              ("khuôn mặt", "ba lô", "Trường Sơn"), ("Trường Sơn", "bộ đội", "đỏ bừng"), ("đỏ bừng", "Trường Sơn", "ba lô")),
       images={TRUONG_SON: TRUONG_SON_DESC},
       notes=[("khac_sach", KS_TLC)],
       review=[("part1[2]", "lời dẫn tranh do app soạn")])
print("tuần 25 xong")
