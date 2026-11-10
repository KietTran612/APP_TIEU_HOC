"""Tuần 9 (mục 235–241), tr.59–64, ảnh 029 (tr.58–59), 031–033. Tr.65 là trang bìa chủ điểm "Đất nước ta"."""
from l2lib import *

GA_IMG = "img_b236_ddanf_gaf_con"
GA_DESC = ("Gà mẹ lông trắng xòe cánh che đàn gà con lông vàng trên bãi cỏ, mấy chú gà con chạy líu ríu quanh chân mẹ; "
           "trên cành cây phía trên có con diều hâu đang rình")

# 235 — Bài 32. Đồ dùng để ở đâu (tr.59–60)
lesson(235, [59, 60],
       [picture("img_b235_minh_chayj", "Minh chạy vội đi học.", "đi học"),
        title("Đồ dùng để ở đâu"),
        *prose("NHỊ HÀ",
               ["Minh nhìn lên đồng hồ.", "Đã đến giờ đi học.", "Minh cuống cuồng tìm quần áo để mặc.",
                "Nhưng chú bé không thấy quần dài, không thấy áo, không thấy dép đâu cả."],
               ["Minh gắt lên:"], ["- Quần ta đâu rồi?"], ["Quần lên tiếng:"],
               ["- Tôi đây! Tôi đây! Tôi ở trong xó tủ.", "Tối qua anh nhét tôi vào đây cơ mà!"],
               ["- Áo ta đâu?"],
               ["- Tôi ở đây! Trên đình màn này.", "Tối qua anh vứt tôi lên đây cơ mà!",
                "- Chiếc áo nhăn nhúm, kêu lên như vậy."],
               ["- Dép của ta ở đâu?"],
               ["- Tôi đây! Dưới gầm tủ ấy! - Chiếc dép bên phải trả lời.", "Chiếc bên trái im thin thít.",
                "Nó không nghe thấy tiếng Minh hỏi.", "Nó nằm ngoài cửa."],
               ["Cuối cùng, Minh cũng mặc xong quần áo và tìm thấy dép.", "Nhưng trống vào học đã đánh rồi.",
                "Minh chạy bở hơi tai mà vẫn chậm."]),
        *glossary("Chạy bở hơi tai: chạy vội vã và mệt hết sức."),
        q("1. Đồ dùng của Minh để như thế nào? Để như vậy có đúng chỗ không? Nên để như thế nào cho đúng chỗ?",
          marker="?"),
        q("2. Đồ dùng để lộn xộn có hại gì?"),
        q("3. Đặt câu với mỗi từ ngữ: cuống cuồng, chạy bở hơi tai, im thin thít.")],
       listen(("cuống cuồng", "im thin thít", "nhăn nhúm"), ("đồng hồ", "xó tủ", "gầm tủ"), ("nhăn nhúm", "cuống cuồng", "đình màn"),
              ("gầm tủ", "đình màn", "xó tủ"), ("im thin thít", "nhăn nhúm", "bở hơi tai"), ("quần áo", "đôi dép", "đồng hồ")),
       images={"img_b235_minh_chayj": "Cậu bé Minh đeo cặp, quần áo xộc xệch, hớt hải chạy qua sân trường vắng về phía "
                                      "dãy lớp học; các bạn đã ngồi trong lớp, nhìn qua cửa sổ"},
       notes=[("khac_sach", KS_ORAL)])

# 236 — Bài 33. Đàn gà mới nở (Học thuộc lòng, tr.60–61)
POEM33 = ["Lông vàng mát dịu", "Mắt đẹp sáng ngời", "Ôi! Chú gà ơi!", "Ta yêu chú lắm!",
          "Mẹ dang đôi cánh", "Con biến vào trong", "Mẹ ngẩng đầu trông", "Bọn diều, bọn quạ.",
          "Bây giờ thong thả", "Mẹ đi lên đầu", "Đàn con bé tí", "Líu ríu chạy sau.",
          "Con mẹ đẹp sao", "Những hòn tơ nhỏ", "Chạy như lăn tròn", "Trên sân, trên cỏ.",
          "Vườn trưa gió mát", "Bướm bay dập dờn", "Quanh đôi chân mẹ", "Một rừng chân con."]
lesson(236, [60, 61],
       [picture(GA_IMG, "Gà mẹ dang cánh che đàn con.", "đàn gà"),
        title("Đàn gà mới nở", "Học thuộc lòng"),
        *sentences(*POEM33),
        passage("poem", "PHẠM HỔ", breaks=[4, 8, 12, 16]),
        q("1. Nêu những nét xinh đẹp của đàn gà con (ở khổ 1 và khổ 3–4).", marker="?"),
        q("2. Tìm những từ tả gà mẹ bảo vệ đàn con."),
        q("3. Những câu nào cho biết gà mẹ có nhiều con? (ở khổ 3 và 5)"),
        find("4. Tìm những tiếng cùng vần ở cuối mỗi dòng.",
             {"word": ["ngời", "ơi", "trong", "trông", "đầu", "sau", "nhỏ", "cỏ"]}),
        memorize()],
       listen(("mát dịu", "sáng ngời", "dập dờn"), ("líu ríu", "lăn tròn", "thong thả"), ("dập dờn", "líu ríu", "mát dịu"),
              ("hòn tơ", "lông vàng", "bọn quạ"), ("thong thả", "dập dờn", "sáng ngời"), ("bọn diều", "bọn quạ", "đàn con")),
       images={GA_IMG: GA_DESC},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)],
       review=[("part1[26]", "tiếng cùng vần do app chọn: ngời–ơi, trong–trông, đầu–sau, nhỏ–cỏ")])

# 237 — Bài 34. Cô Chổi Rơm (Bài đọc thêm, tr.62; sách không có tranh)
lesson(237, [62],
       [title("Cô Chổi Rơm", "Bài đọc thêm"),
        *prose("VŨ DUY THÔNG",
               ["Trong họ hàng nhà chổi thì cô bé Chổi Rơm vào loại xinh xắn nhất.",
                "Cô có chiếc váy vàng óng, không ai đẹp bằng.", "Áo của cô cũng bằng rơm thóc nếp vàng tươi,",
                "được tết săn lại, cuốn từng vòng quanh người, trông cứ như áo len vậy."],
               ["Tuy bé nhưng Chổi Rơm rất được việc.", "Ngày hai lần, chị Thùy Linh mang chổi ra quét nhà.",
                "Chỉ quét nhà thôi, còn sân, vườn đã có loại chổi khác cứng hơn."],
               ["Chị rất quý Chổi Rơm.", "Chị đã nhờ bà đóng cho chiếc đinh sau cánh cửa.",
                "Mỗi lần quét nhà xong, chị treo Chổi Rơm lên đấy", "vừa đỡ ẩm chổi, lại gọn nhà.",
                "Thế là sau những lần lao động mệt nhọc,", "Chổi Rơm được nằm yên ngủ một giấc ngon lành."])],
       listen(("chổi rơm", "áo len", "cánh cửa"), ("vàng óng", "xinh xắn", "ngon lành"), ("xinh xắn", "vàng óng", "mệt nhọc"),
              ("mệt nhọc", "lao động", "ngon lành"), ("quét nhà", "gọn nhà", "chổi rơm"), ("ngon lành", "mệt nhọc", "vàng tươi")),
       notes=[("khac_sach", KS_SPLIT)])

# 238 — Chính tả tuần 9 (tr.62–63)
lesson(238, [62, 63],
       [title("Chính tả: Đồ dùng để ở đâu", "Nghe đọc"),
        title("Bài viết: \"Minh nhìn lên... đâu cả\" và \"Cuối cùng... vẫn chậm\".",
              "Phần này con nghe bố mẹ đọc rồi viết vào vở."),
        words("quần", "dép", "cuống cuồng", "xong", "cuối", "đã"),
        fill(["xong", "song"], ("làm bài xong", "xong", "xong"), ("chấn song gỗ", "song", "song"),
             ("chấn song sắt", "song", "song")),
        fill(["cuối", "cúi"], ("cuối cùng", "cuối", "cuối"), ("cuối năm", "cuối", "cuối"), ("cúi đầu", "cúi", "cúi"),
             ("cúi cổ", "cúi", "cúi")),
        title("Tập chép: Đàn gà mới nở", "Nhìn bảng"),
        title("Bài chép: 3 khổ thơ đầu.", "Phần này con chép vào vở cùng bố mẹ."),
        words("dịu", "yêu", "ngẩng", "diều", "dang", "líu ríu"),
        fill(["d", "r"], ("dang tay", "dang", "d"), ("ngô rang", "rang", "r"), ("râm ran", "ran", "r")),
        fill(["n", "ng"], ("những con bò vàng", "vàng", "ng"), ("những buổi sáng", "sáng", "ng"), ("đàn bò", "đàn", "n"),
             ("ngẩng đầu lên", "ngẩng", "ng"))],
       listen(("cuống cuồng", "quần", "dép"), ("chấn song", "làm xong", "cuối cùng"), ("cúi đầu", "cuối năm", "ngẩng đầu"),
              ("líu ríu", "dang tay", "diều"), ("ngô rang", "râm ran", "dịu"), ("ngẩng", "dang", "líu ríu")),
       notes=[("khac_sach", KS_WRITE), ("khac_sach", "Điền chỗ trống làm bằng chạm hoặc kéo thẻ.")],
       review=[("part1[3]", "đáp án xong/song"), ("part1[4]", "đáp án cuối/cúi"), ("part1[8]", "đáp án d/r"),
               ("part1[9]", "đáp án n/ng do app soạn; hai chỗ \"bò cứ xá...\" và \"ngơ ngá...\" trong sách không rõ "
                            "nên app chưa đưa vào")])

# 239 — Từ ngữ: Ôn tập (tr.63)
lesson(239, [63],
       [title("Từ ngữ: Ôn tập"),
        q("1. Sắp xếp tên gọi những người trong gia đình theo thứ tự trên dưới."),
        q("2. Thế nào là ông nội, bà nội? Thế nào là ông ngoại, bà ngoại?"),
        q("3. Bên nội là gì? Bên ngoại là gì? Kể tên một số bà con bên nội, bên ngoại."),
        q("4. Bé Mai là con của chú tôi và thím tôi, nên là em họ tôi. Bé Hoa cũng là em họ tôi, vì là con của "
          "cậu tôi và mợ tôi."),
        choose("Vậy ai là em họ bên nội?", ["Bé Mai", "Bé Hoa"], [0]),
        choose("Ai là em họ bên ngoại?", ["Bé Mai", "Bé Hoa"], [1]),
        q("5. Em đã nhường nhịn các em ở nhà như thế nào? "
          "Trong một gia đình hòa thuận thì mọi người đối xử với nhau ra sao?")],
       listen(("ông nội", "bà ngoại", "em họ"), ("em họ", "bà con", "ông nội"), ("bà con", "em họ", "nhường nhịn"),
              ("nhường nhịn", "hòa thuận", "bà con"), ("hòa thuận", "nhường nhịn", "ông nội"), ("bà ngoại", "ông nội", "hòa thuận")),
       notes=[("khac_sach", KS_ORAL), ("khac_sach", "Câu 4: bé chạm để chọn em họ bên nội, bên ngoại.")],
       review=[("part1[5]", "đáp án: Bé Mai bên nội (con của chú)"), ("part1[6]", "đáp án: Bé Hoa bên ngoại (con của cậu)")])

# 240 — Ngữ pháp: Câu – Hai bộ phận chính (tiếp theo) (tr.63–64)
lesson(240, [63, 64],
       [title("Ngữ pháp: Câu – Hai bộ phận chính", "Tiếp theo"),
        *rule("Chị Thùy Linh quét nhà.", "Hỏi: Trong câu nói đến ai?", "Trả lời: Nói đến \"Chị Thùy Linh\".",
             "Vậy \"Chị Thùy Linh\" là bộ phận chính thứ nhất của câu.", "Hỏi: \"Chị Thùy Linh\" làm gì?",
             "Trả lời: \"Quét nhà\".", "Kết luận: \"Quét nhà\" là bộ phận chính thứ hai của câu."),
        *rule("Bộ phận chính thứ hai của câu là bộ phận trả lời câu hỏi \"... làm gì?\""),
        q("Đặt câu hỏi để tìm bộ phận chính thứ hai trong các câu sau:",
          lines=["Bà tôi kể nhiều truyện cổ tích.", "Gà mẹ che chở cho con.", "Bố bạn Tuấn đóng bàn ghế."])],
       listen(("truyện cổ tích", "bàn ghế", "quét nhà"), ("che chở", "kể chuyện", "đóng bàn"), ("quét nhà", "che chở", "cổ tích"),
              ("bàn ghế", "quét nhà", "che chở"), ("bộ phận", "kết luận", "trả lời"), ("kết luận", "bộ phận", "bàn ghế")),
       notes=[("khac_sach", KS_ORAL)])

# 241 — Tập làm văn: Quan sát tranh và trả lời câu hỏi — Đàn gà mới nở (tr.64)
lesson(241, [64],
       [title("Tập làm văn: Quan sát tranh và trả lời câu hỏi"),
        title("Đề bài: Đàn gà mới nở.", "Xem tranh ở bài Đàn gà mới nở."),
        picture(GA_IMG, "Con nhìn kĩ tranh đàn gà nhé.", "đàn gà"),
        q("1. Đàn gà con trong tranh có những nét gì đẹp?"),
        q("2. Gà mẹ và gà con đang làm gì? Ở đâu?"),
        q("3. Con gì đe dọa đàn gà con?"),
        q("4. Gà mẹ làm gì để bảo vệ đàn con?"),
        q("5. Nhìn tranh, em hãy đặt thêm một câu hỏi nữa và tự trả lời.")],
       listen(("gà mẹ", "gà con", "diều hâu"), ("gà con", "gà mẹ", "bãi cỏ"), ("diều hâu", "gà con", "đe dọa"),
              ("bảo vệ", "đe dọa", "gà mẹ"), ("đe dọa", "bảo vệ", "bãi cỏ"), ("bãi cỏ", "diều hâu", "bảo vệ")),
       images={GA_IMG: GA_DESC},
       notes=[("khac_sach", "Tập làm văn quan sát tranh: app dùng lại tranh bài Đàn gà mới nở; bé trả lời miệng.")],
       review=[("part1[2]", "lời dẫn tranh do app soạn")])
