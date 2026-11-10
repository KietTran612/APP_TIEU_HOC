"""Tuần 6 (mục 211–218), tr.38–43, ảnh 020–022."""
from l2lib import *

# 211 — Bài 20. Tình cảm gia đình (tr.38–39)
CADAO = ["Công cha như núi ngất trời", "Nghĩa mẹ như nước ngời ngời biển Đông",
         "Núi cao, biển rộng mênh mông", "Công cha nghĩa mẹ ghi lòng con ơi!",
         "Anh em như thể chân tay", "Rách lành đùm bọc, dở hay đỡ đần."]
lesson(211, [38, 39],
       [picture("img_b211_gia_ddinhf", "Cả nhà quây quần bên nhau buổi tối.", "gia đình"),
        title("Tình cảm gia đình"),
        *sentences(*CADAO),
        passage("poem", "Ca dao Việt Nam", breaks=[4]),
        *glossary("Đùm bọc: che chở, giúp đỡ nhau."),
        q("1. Câu ca dao 1 đã so sánh công cha mẹ với gì? Tại sao có thể so sánh như vậy?", marker="?"),
        q("2. Câu 2 so sánh tình anh em với cái gì? Em hiểu thế nào là đùm bọc và đỡ đần nhau?"),
        find("3. So sánh tiếng cuối của câu sáu tiếng và tiếng thứ 6 của câu tám tiếng xem có gì giống nhau.",
             {"word": ["trời", "ngời", "mông", "lòng", "tay", "hay"]})],
       listen(("núi", "biển", "trời"), ("ngất trời", "mênh mông", "ngời ngời"), ("đùm bọc", "đỡ đần", "chân tay"),
              ("đỡ đần", "đùm bọc", "rách lành"), ("biển Đông", "núi cao", "ngất trời"), ("chân tay", "anh em", "dở hay")),
       images={"img_b211_gia_ddinhf": "Buổi tối trong căn nhà ấm cúng: người bố và cậu con trai ngồi bên bàn, cậu bé "
                                      "đang viết bài; người mẹ ngồi trên giường ôm em bé, trăng khuyết ngoài cửa sổ"},
       notes=[("khac_sach", KS_ORAL)],
       review=[("part1[12]", "tiếng giống vần do app chọn: trời–ngời, mông–lòng, tay–hay")])

# 212 — Bài 21. Mẹ (Học thuộc lòng, tr.39)
POEM21 = ["Lặng rồi cả tiếng con ve", "Con ve cũng mệt vì hè nắng oi.", "Nhà em vẫn tiếng ạ ời",
          "Kẽo cà tiếng võng mẹ ngồi mẹ ru.", "Lời ru có gió mùa thu", "Bàn tay mẹ quạt mẹ đưa gió về.",
          "Những ngôi sao thức ngoài kia", "Chẳng bằng mẹ đã thức vì chúng con.", "Đêm nay con ngủ giấc tròn",
          "Mẹ là ngọn gió của con suốt đời."]
lesson(212, [39],
       [picture("img_b212_mej_ru_con", "Mẹ ngồi bên võng quạt cho con ngủ.", "mẹ"),
        title("Mẹ", "Học thuộc lòng"),
        *sentences(*POEM21),
        passage("poem", "TRẦN QUỐC MINH"),
        q("1. Đọc xong bài này, em thích nhất những câu nào? Tại sao?", marker="?"),
        q("2. Để con ngủ ngon giấc, mẹ đã làm gì?"),
        q("3. Câu nào nói lên nỗi vất vả của mẹ?"),
        find("4. Tìm những tiếng cùng vần ở câu sáu tiếng và câu tám tiếng (cặp câu đầu và cặp câu cuối của bài).",
             {"word": ["ve", "hè", "tròn", "con"]}, sentences_in=[0, 1, 8, 9]),
        memorize()],
       listen(("tiếng võng", "con ve", "lời ru"), ("nắng oi", "gió mùa thu", "giấc tròn"),
              ("ngọn gió", "ngôi sao", "tiếng võng"), ("giấc tròn", "suốt đời", "nắng oi"),
              ("lời ru", "ngọn gió", "con ve"), ("ngôi sao", "lời ru", "ngọn gió")),
       images={"img_b212_mej_ru_con": "Trưa hè trong nhà tranh, người mẹ ngồi bên chiếc võng vừa đưa võng vừa cầm quạt "
                                      "nan quạt cho em bé ngủ; ngoài hiên có cây và tiếng ve"},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)],
       review=[("part1[0]", "sách in tranh mờ sau bài thơ; tranh vẽ lại theo nội dung bài"),
               ("part1[16]", "tiếng cùng vần do app chọn: ve–hè, tròn–con")])

# 213 — Bài 22. Bố làm thợ mộc (tr.40–41)
lesson(213, [40, 41],
       [picture("img_b213_thowj_mocj", "Bố bào gỗ, Tuấn đứng xem.", "thợ mộc"),
        title("Bố làm thợ mộc"),
        *prose("NGÔ QUÂN MIỆN",
               ["Tuấn chăm chú ngắm nghía từng động tác của bố.",
                "Cái bào của bố lướt trên mặt tấm ván", "cứ y như con tàu lướt trên mặt biển,",
                "mà đám vỏ bào đùn lên cứ y như sóng biển cuộn trào.",
                "Cái con tàu hình khối vuông dài lao vút lên trước, rồi lùi lại sau.",
                "Những làn sóng, lúc thì cong vồng, lúc thì loăn xoăn,",
                "đợt thì màu vàng, đợt thì màu nâu, màu hồng,", "ùn lên phía trước mũi tàu..."],
               ["Gỗ của bố thường chỉ là những cái thùng cũ, những mảnh ván thừa,", "nhiều khi lấm lem đất cát.",
                "Nhưng khi lưỡi bào, lưỡi đục của bố", "đã gọt hết lượt da ngoài xấu xí đi,",
                "thì mặt gỗ nào hiện ra cũng đẹp."],
               ["Tuấn rất yêu cái mùi hương gỗ.", "Tối tối, Tuấn đi ngủ,",
                "hương gỗ như còn theo Tuấn vào trong cả giấc mơ."]),
        q("1. Nghề thợ mộc là nghề gì? Em hãy kể vài đồ dùng trong nhà em do các bác thợ mộc làm ra.", marker="?"),
        q("2. Tác giả so sánh cái bào lướt trên ván như vật gì? So sánh vỏ bào như vật gì?"),
        q("3. Câu nào nói lên bàn tay khéo léo của bố Tuấn?")],
       listen(("cái bào", "vỏ bào", "tấm ván"), ("vỏ bào", "sóng biển", "con tàu"), ("loăn xoăn", "cong vồng", "lấm lem"),
              ("lưỡi đục", "lưỡi bào", "mặt gỗ"), ("hương gỗ", "giấc mơ", "vỏ bào"), ("lấm lem", "xấu xí", "loăn xoăn")),
       images={"img_b213_thowj_mocj": "Dưới gốc cây, người bố mặc áo may ô đang đẩy cái bào trên tấm ván đặt trên giá gỗ, "
                                      "vỏ bào cuộn tròn rơi xuống; cậu bé Tuấn đứng bên chăm chú nhìn, sau lưng là "
                                      "chiếc tủ gỗ đóng dở"},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 214 — Bài 23. Lòng mẹ (Bài đọc thêm, tr.41; sách không có tranh)
lesson(214, [41],
       [title("Lòng mẹ", "Bài đọc thêm"),
        *prose("H.T.",
               ["Đêm đã khuya.", "Mẹ Thắng vẫn ngồi cặm cụi làm việc.", "Chiều nay, trời trở rét.",
                "Mẹ cố may cho xong tấm áo", "để ngày mai Thắng có thêm áo ấm đi học.",
                "Chốc chốc, Thắng trở mình,", "mẹ dừng mũi kim, đắp lại chăn cho Thắng ngủ ngon."],
               ["Nhìn khuôn mặt sáng sủa, bầu bĩnh của Thắng, mẹ thấy vui trong lòng.",
                "Tay mẹ đưa mũi kim nhanh hơn.", "Bên ngoài, tiếng gió bấc rào rào trong vườn chuối."])],
       listen(("mũi kim", "tấm áo", "áo ấm"), ("cặm cụi", "bầu bĩnh", "rào rào"), ("bầu bĩnh", "sáng sủa", "cặm cụi"),
              ("gió bấc", "vườn chuối", "trở rét"), ("trở mình", "trở rét", "mũi kim"), ("rào rào", "gió bấc", "chốc chốc")),
       notes=[("khac_sach", KS_SPLIT)])

# 215 — Chính tả tuần 6 (tr.41–42)
lesson(215, [41, 42],
       [title("Tập chép: Tình cảm gia đình", "Nhìn bảng"),
        title("Bài chép: 6 câu đầu.", "Phần này con chép vào vở cùng bố mẹ."),
        words("biển Đông", "mênh mông", "dở hay", "gia đình", "ngất trời", "nghĩa"),
        fill(["gia", "da"], ("gia đình", "gia", "gia"), ("da thịt", "da", "da"), ("tham gia", "gia", "gia"),
             ("áo da bò", "da", "da")),
        fill(["ngã", "ngả"], ("Chị ngã em nâng", "ngã", "ngã"), ("cùng về một ngả", "ngả", "ngả")),
        combine("nghĩa", "có", "trả", "ơn", "tình", at="before"),
        title("Chính tả: Quyển vở của em", "Trí nhớ"),
        title("Bài viết: 2 khổ thơ đầu.", "Phần này con nhớ lại rồi viết vào vở."),
        words("dòng", "giấy", "mát rượi", "chữ", "ngay ngắn", "nắn nót", "mở"),
        fill(["chúng", "trúng"], ("vở của chúng em", "chúng", "chúng"), ("bắn trúng đích", "trúng", "trúng")),
        fill(["n", "ng"], ("trời nắng", "nắng", "ng"), ("viết nắn nót", "nắn", "n"), ("uốn nắn", "nắn", "n"),
             ("ngồi ngay ngắn", "ngắn", "n"), ("dài hay ngắn", "ngắn", "n"))],
       listen(("gia đình", "da thịt", "tham gia"), ("mênh mông", "biển Đông", "ngất trời"), ("tình nghĩa", "ơn nghĩa", "trả nghĩa"),
              ("ngay ngắn", "nắn nót", "mát rượi"), ("trời nắng", "uốn nắn", "dòng"), ("bắn trúng", "chúng em", "giấy")),
       notes=[("khac_sach", KS_WRITE), ("khac_sach", "Điền chỗ trống, ghép chữ làm bằng chạm hoặc kéo thẻ.")],
       review=[("part1[3]", "đáp án gia/da theo chính tả chuẩn"), ("part1[4]", "đáp án ngã/ngả theo câu tục ngữ quen"),
               ("part1[5]", "cách ghép do app chọn: có nghĩa, trả nghĩa, ơn nghĩa, tình nghĩa"),
               ("part1[9]", "đáp án chúng/trúng theo chính tả chuẩn"),
               ("part1[10]", "đáp án n/ng: nắng, nắn nót, uốn nắn, ngay ngắn, ngắn")])

# 216 — Từ ngữ: Gia đình (tr.42)
lesson(216, [42],
       [title("Từ ngữ: Gia đình"),
        title("Những từ ngữ cần ghi nhớ"),
        words("gia đình", "ông bà", "cha mẹ", "anh", "chị", "em"),
        words("đùm bọc", "thương yêu", "đỡ đần", "hòa thuận"),
        words("Lá lành đùm lá rách."),
        title("Bài tập 1: Điền từ thích hợp vào chỗ trống"),
        fill_passage(["Cha còn gọi là [bố|bà|anh].", "Mẹ còn gọi là [má|chị|cô]."]),
        title("Bài tập 2: Điền thêm từ vào chỗ trống"),
        fill_passage(["Những lúc rỗi rãi, em thường [đỡ đần|đùm bọc|hòa thuận] bố mẹ.",
                      "Anh chị em trong một nhà phải [thương yêu|đỡ đần|hòa thuận] và [đùm bọc|ông bà|gia đình] nhau.",
                      "[Cha mẹ|Anh chị|Ông bà] rất thương con, [ông bà|cha mẹ|anh chị] rất thương cháu.",
                      "Mọi người trong gia đình em sống rất [hòa thuận|đỡ đần|đùm bọc] với nhau."])],
       listen(("ông bà", "cha mẹ", "anh chị"), ("đùm bọc", "đỡ đần", "thương yêu"), ("hòa thuận", "thương yêu", "gia đình"),
              ("thương yêu", "hòa thuận", "đùm bọc"), ("lá lành", "lá rách", "gia đình"), ("đỡ đần", "ông bà", "hòa thuận")),
       notes=[("khac_sach", "Sách để trống, không cho sẵn từ: app cho mỗi chỗ trống 3 thẻ để chọn; "
                            "thẻ và đáp án do app soạn.")],
       review=[("part1[6]", "đáp án do app soạn: cha còn gọi là bố, mẹ còn gọi là má (sách để trống)"),
               ("part1[8]", "thẻ chọn và đáp án điền chỗ trống do app soạn")])

# 217 — Ngữ pháp: Câu – Hai bộ phận chính (tr.43)
lesson(217, [43],
       [title("Ngữ pháp: Câu – Hai bộ phận chính"),
        *rule("Mẹ Thắng – chưa thành câu.", "Vá áo – chưa thành câu.", "Mẹ Thắng vá áo. – đã thành câu."),
        *rule("Câu thường phải có đủ hai bộ phận chính.",
             "Bộ phận chính thứ nhất đứng trước, bộ phận chính thứ hai đứng sau."),
        q("1. Điền thêm bộ phận thứ hai cho thành câu:", lines=["Bố Tuấn...", "Thắng..."]),
        q("2. Điền thêm bộ phận thứ nhất cho thành câu:", lines=["... đang ăn cơm.", "... may áo mặc rét cho Thắng."])],
       listen(("vá áo", "may áo", "ăn cơm"), ("bộ phận", "thành câu", "vá áo"), ("ăn cơm", "vá áo", "mặc rét"),
              ("mặc rét", "ăn cơm", "bộ phận"), ("thành câu", "bộ phận", "may áo"), ("may áo", "mặc rét", "thành câu")),
       notes=[("khac_sach", "Bé nói thêm bộ phận câu cùng bố mẹ (sách để bé tự điền, không có đáp án cố định).")])

# 218 — Tập làm văn: Điền từ — Gia đình Sơn (tr.43)
lesson(218, [43],
       [title("Tập làm văn: Điền từ"),
        title("Đề bài: Gia đình Sơn.", "Em tự tìm từ thích hợp để điền vào chỗ trống."),
        fill_passage(["Gia đình Sơn gồm có ông [bà|chú|anh] Sơn; [bố|ông|chị] mẹ Sơn; em Sơn và Sơn.",
                      "Em Sơn là em gái.", "Như vậy Sơn không có em [trai|gái|bé].",
                      "Ông nội Sơn tuy [già|trẻ|nhỏ] nhưng vẫn còn khỏe mạnh.",
                      "Ông thường [tưới|vẽ|ăn] cây cối trong vườn.",
                      "Bà nội thì [chăm sóc|tưới|bào] Sơn và em Sơn."])],
       listen(("ông bà", "bố mẹ", "em gái"), ("em gái", "em trai", "ông bà"), ("khỏe mạnh", "cây cối", "chăm sóc"),
              ("chăm sóc", "khỏe mạnh", "bà nội"), ("bà nội", "ông nội", "em trai"), ("cây cối", "chăm sóc", "bố mẹ")),
       notes=[("khac_sach", "Sách để bé tự tìm từ: app cho mỗi chỗ trống 3 thẻ để chọn; thẻ và đáp án do app soạn.")],
       review=[("part1[2]", "thẻ chọn và đáp án điền chỗ trống do app soạn")])
