"""Tuần 8 (mục 227–234), tr.52–58, ảnh 027, 028, 030 (tr.56–57), 029 (tr.58–59)."""
from l2lib import *

GIAN_MUOP_IMG = "img_b229_giafn_muwowps"
GIAN_MUOP_DESC = ("Giàn mướp xanh bắc trên mặt ao nở đầy hoa vàng, quả mướp dài thõng xuống; người bà đứng hái mướp, "
                  "cô bé ngồi bên bờ ao ôm mấy quả mướp, cá rô lội dưới nước, xa xa có mái nhà")

# 227 — Bài 28. Bé Mai trở thành người lớn như thế nào (tr.52–53)
lesson(227, [52, 53],
       [picture("img_b227_bes_mai_quets_nhaf", "Bé Mai cầm chổi quét nhà như mẹ.", "quét nhà"),
        title("Bé Mai trở thành người lớn như thế nào"),
        *prose("",
               ["Bé Mai rất thích làm người lớn.", "Bé thử đủ mọi cách:",
                "bé đi dép của mẹ, bé cài trâm lên mái tóc theo kiểu của cô.", "Bé lại còn đeo đồng hồ tay nữa."],
               ["Nhưng chẳng có kết quả.", "Mọi người chỉ nhìn bé, cười chế giễu."],
               ["Một lần, bé Mai thử quét nhà như mẹ.", "Bé quét sạch đến nỗi mẹ phải ngạc nhiên:"],
               ["- Bé Mai của mẹ, phải chăng con đã trở thành người lớn rồi?"],
               ["Và khi bé Mai rửa bát đũa thật sạch, lau thật khô,", "thì cả bố mẹ đều lấy làm lạ.",
                "Lúc ngồi ăn cơm, bố nói:"],
               ["- Lạ thật, bé Mai nhà ta đã lớn từ lúc nào mà chúng ta không thấy!"],
               ["Mai cũng cảm thấy mình đã lớn thật.", "Bé không đi dép của mẹ, không cài trâm, không đeo đồng hồ.",
                "Rõ ràng những thứ ấy không làm cho trẻ con thành người lớn được."]),
        q("1. Lúc đầu, bé Mai muốn làm người lớn bằng cách nào?", marker="?"),
        q("2. Do đâu mà bé Mai được cả nhà coi như người lớn?"),
        q("3. Em đã trở thành người lớn như bé Mai chưa? Hãy kể vài việc em đã làm ở nhà để giúp đỡ bố mẹ.")],
       listen(("quét nhà", "rửa bát", "ăn cơm"), ("đồng hồ", "cài trâm", "đi dép"), ("ngạc nhiên", "chế giễu", "kết quả"),
              ("bát đũa", "đồng hồ", "mái tóc"), ("chế giễu", "ngạc nhiên", "lấy làm lạ"), ("người lớn", "trẻ con", "bố mẹ")),
       images={"img_b227_bes_mai_quets_nhaf": "Cô bé Mai mặc bộ quần áo hoa cầm chổi quét sạch sân trước nhà, lá rụng "
                                              "gom thành đống; trong cửa, người mẹ ngồi rửa nồi bên bếp, cây cau ở góc sân"},
       notes=[("khac_sach", KS_ORAL)])

# 228 — Bài 29. Nói với em (Học thuộc lòng, tr.53–54)
POEM29 = ["Nếu nhắm mắt trong vườn lộng gió", "Sẽ được nghe nhiều tiếng chim hay", "Tiếng lích rích chim sâu trong lá",
          "Con chìa vôi vừa hót vừa bay.",
          "Nếu nhắm mắt nghe bà kể chuyện", "Sẽ được nhìn thấy các bà tiên", "Thấy chú bé đi hài bảy dặm",
          "Quả thị thơm, cô Tấm rất hiền.",
          "Nếu nhắm mắt nghĩ về cha mẹ", "Đã nuôi em khôn lớn từng ngày", "Tay bồng bế, sớm khuya vất vả",
          "Mắt nhắm rồi, lại mở ra ngay."]
lesson(228, [53, 54],
       [picture("img_b228_baf_ker_chuyeenj", "Bà bế em bé, các bạn nhỏ ngồi nghe.", "kể chuyện"),
        title("Nói với em", "Học thuộc lòng"),
        *sentences(*POEM29),
        passage("poem", "VŨ QUẦN PHƯƠNG", breaks=[4, 8]),
        q("1. Đứng trong vườn, nếu nhắm mắt lại, em sẽ được nghe những tiếng gì?", marker="?"),
        q("2. Khi nghe bà kể chuyện, nếu nhắm mắt lại, em tưởng tượng thấy những gì?"),
        q("3. Nếu nghĩ về công ơn cha mẹ, em hiểu được điều gì?"),
        find("4. Mỗi câu thơ có mấy tiếng? Tìm vần giống nhau ở cuối các câu.",
             {"word": ["hay", "bay", "tiên", "hiền", "ngày", "ngay"]}),
        memorize()],
       listen(("lộng gió", "lích rích", "chìa vôi"), ("bà tiên", "cô Tấm", "quả thị"), ("bồng bế", "vất vả", "khôn lớn"),
              ("chìa vôi", "chim sâu", "bà tiên"), ("vất vả", "bồng bế", "lộng gió"), ("quả thị", "hài bảy dặm", "chim sâu")),
       images={"img_b228_baf_ker_chuyeenj": "Dưới tán cây dừa bên bờ sông, người bà ngồi ghế bế em bé, hai cô cháu gái "
                                            "đứng và ngồi tựa bàn tròn chăm chú nghe bà kể chuyện"},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)],
       review=[("part1[18]", "vần cuối câu do app chọn: hay–bay, tiên–hiền, ngày–ngay; câu \"mấy tiếng\" bé trả lời miệng")])

# 229 — Bài 30. Giàn mướp (tr.55–56)
lesson(229, [55, 56],
       [picture(GIAN_MUOP_IMG, "Giàn mướp nở hoa vàng trên mặt ao.", "giàn mướp"),
        title("Giàn mướp"),
        *prose("VŨ TÚ NAM",
               ["Thật là tuyệt!", "Mấy bông hoa vàng tươi, như những đốm nắng,",
                "đã nở sáng trưng trên giàn mướp xanh mát.",
                "Cái giàn trên mặt ao soi bóng xuống làn nước lấp lánh hoa vàng.",
                "Mấy chú cá rô cứ lội quanh lội quẩn ở đó chẳng muốn đi đâu.", "Cứ thế, hoa nở tiếp hoa.",
                "Rồi quả thi nhau chòi ra... bằng ngón tay... bằng con chuột.", "Rồi bằng con cá chuối to.",
                "Có hôm chị em tôi hái không xuể.",
                "Bà tôi sai mang đi biếu cô tôi, dì tôi, cậu tôi, chú tôi, bác tôi,", "mỗi người một quả."]),
        *glossary("Cá chuối: còn gọi là cá quả hay cá tràu.", "Không xuể: không hết được."),
        q("1. Kể những nét đẹp của giàn mướp khi có hoa.", marker="?"),
        q("2. Tác giả đã ví quả mướp từ lúc bé đến lúc lớn với những vật gì?"),
        q("3. Đặt một câu với mỗi từ: sáng trưng, lấp lánh."),
        q("4. \"Chú\" khác với \"cậu\" như thế nào? \"Cô\" khác với \"dì\" như thế nào?")],
       listen(("giàn mướp", "cá rô", "cá chuối"), ("sáng trưng", "lấp lánh", "xanh mát"), ("lấp lánh", "sáng trưng", "đốm nắng"),
              ("cá chuối", "cá rô", "con chuột"), ("đốm nắng", "ngón tay", "giàn mướp"), ("không xuể", "lội quẩn", "lấp lánh")),
       images={GIAN_MUOP_IMG: GIAN_MUOP_DESC},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 230 — Bài 31. Quạt cho bà ngủ (Bài đọc thêm, tr.56)
POEM31 = ["Ơi chích chòe ơi!", "Chim đừng hót nữa", "Bà em ốm rồi", "Lặng cho bà ngủ.",
          "Bàn tay bé nhỏ", "Vẫy quạt thật đều", "Ngấn nắng thiu thiu", "Đậu trên tường trắng.",
          "Căn nhà đã vắng", "Cốc chén nằm im", "Đôi mắt lim dim", "Ngủ ngon bà nhé.",
          "Hoa cam, hoa khế", "Chín lặng trong vườn", "Bà mơ tay cháu", "Quạt đầy hương thơm."]
lesson(230, [56],
       [picture("img_b230_quatj_cho_baf", "Cháu ngồi quạt cho bà ngủ.", "quạt"),
        title("Quạt cho bà ngủ", "Bài đọc thêm"),
        *sentences(*POEM31),
        passage("poem", "THẠCH QUỲ", breaks=[4, 8, 12])],
       listen(("chích chòe", "hoa cam", "hoa khế"), ("thiu thiu", "lim dim", "nằm im"), ("lim dim", "thiu thiu", "cốc chén"),
              ("hoa khế", "hoa cam", "hương thơm"), ("cốc chén", "căn nhà", "tường trắng"), ("vẫy quạt", "bàn tay", "chích chòe")),
       images={"img_b230_quatj_cho_baf": "Trong gian nhà vắng buổi trưa, bà nằm ngủ trên giường, cô cháu nhỏ ngồi bên cầm "
                                         "quạt nan quạt đều cho bà; ngoài cửa sổ có cây cam, cây khế trong vườn"},
       review=[("part1[0]", "sách in tranh mờ sau bài thơ; tranh vẽ lại theo nội dung bài")])

# 231 — Chính tả tuần 8 (tr.56–57)
lesson(231, [56, 57],
       [title("Chính tả: Bé Mai trở thành người lớn như thế nào", "Nghe đọc"),
        title("Bài viết: \"Một lần... lấy làm lạ\".", "Phần này con nghe bố mẹ đọc rồi viết vào vở."),
        words("người", "quét", "trở", "ngạc nhiên", "bát đũa"),
        find("Tìm những chữ có ươi trong câu sau.", {"rime": ["ươi"]},
             text=["Cười người hôm trước, hôm sau người cười."]),
        q("Em tìm thêm ba từ có ươi."),
        fill(["chở", "trở"], ("thuyền chở thóc", "chở", "chở"), ("em trở về nhà", "trở", "trở")),
        fill(["ngạc", "ngạt"], ("ngạc nhiên", "ngạc", "ngạc"), ("ngạt thở", "ngạt", "ngạt"), ("kinh ngạc", "ngạc", "ngạc"),
             ("ngào ngạt", "ngạt", "ngạt")),
        fill(["bát", "bác"], ("bát đũa", "bát", "bát"), ("chú bác", "bác", "bác")),
        title("Chính tả: Mẹ", "Trí nhớ"),
        title("Bài viết: 6 câu đầu.", "Phần này con nhớ lại rồi viết vào vở."),
        words("quạt", "lặng", "nắng oi", "tiếng"),
        {"type": "combine_words", "base": "quạt",
         "items": [{"with": "cái", "at": "before"}, {"with": "nan", "at": "after"}, {"with": "giấy", "at": "after"},
                   {"with": "máy", "at": "after"}, {"with": "em", "at": "before"}]},
        fill(["l", "n"], ("im lặng", "lặng", "l"), ("gánh nặng", "nặng", "n"), ("lắng tai", "lắng", "l"),
             ("trời nắng", "nắng", "n")),
        fill(["n", "ng"], ("tiếng ve ran", "tiếng", "ng"), ("tiến lên", "tiến", "n"), ("tiếng ru", "tiếng", "ng"),
             ("tiến bộ", "tiến", "n")),
        fill(["vẫn", "vẩn"], ("em vẫn đi học", "vẫn", "vẫn"), ("chơi vơ vẩn", "vẩn", "vẩn"))],
       listen(("ngạc nhiên", "bát đũa", "quét nhà"), ("người", "cười", "tươi"), ("ngào ngạt", "ngạt thở", "kinh ngạc"),
              ("quạt nan", "quạt giấy", "quạt máy"), ("tiến bộ", "tiếng ru", "gánh nặng"), ("vơ vẩn", "lắng tai", "im lặng")),
       notes=[("khac_sach", KS_WRITE), ("khac_sach", "Điền chỗ trống, ghép chữ, tìm chữ làm bằng chạm hoặc kéo thẻ.")],
       review=[("part1[5]", "đáp án chở/trở"), ("part1[6]", "đáp án ngạc/ngạt"), ("part1[7]", "đáp án bát/bác"),
               ("part1[11]", "cách ghép do app chọn: cái quạt, quạt nan, quạt giấy, quạt máy, em quạt"),
               ("part1[12]", "đáp án l/n"), ("part1[13]", "đáp án n/ng"), ("part1[14]", "đáp án vẫn/vẩn")])

# 232 — Từ ngữ: Họ hàng nội ngoại (tr.57–58)
lesson(232, [57, 58],
       [title("Từ ngữ: Họ hàng nội ngoại"),
        title("Những từ ngữ cần ghi nhớ"),
        words("họ hàng", "họ nội", "họ ngoại"),
        words("chú", "bác", "cô", "dì", "cậu"),
        words("thân thiết", "ruột thịt"),
        title("Bài tập 1: Điền từ thích hợp vào các chỗ trống"),
        fill_passage(["Bố mẹ Lan quê ở Hà Nội.", "Họ hàng bên [nội] và bên [ngoại] Lan cũng ở Hà Nội.",
                      "Lan gọi các anh, các chị của bố và mẹ đều bằng [bác].",
                      "Các em trai và em gái của bố thì Lan gọi bằng [chú] và [cô].",
                      "Nhưng các em trai, em gái của mẹ, Lan gọi bằng [cậu] và [dì]."],
                     bank=["nội", "ngoại", "bác", "chú", "cô", "cậu", "dì"]),
        q("2. Ai bên nội, ai bên ngoại?",
          lines=["Giàn mướp ở nhà rất sai quả.", "Có hôm chị em tôi hái không xuể.",
                 "Bà tôi sai mang đi biếu cô tôi, dì tôi, cậu tôi, chú tôi, bác tôi mỗi người một quả.",
                 "Như vậy, tôi đã biếu những ai bên nội, bên ngoại?"])],
       listen(("họ nội", "họ ngoại", "họ hàng"), ("ruột thịt", "thân thiết", "họ hàng"), ("cậu", "chú", "bác"),
              ("dì", "cô", "cậu"), ("thân thiết", "ruột thịt", "họ nội"), ("bác", "dì", "chú")),
       notes=[("khac_sach", "Điền từ bằng chạm hoặc kéo thẻ; thẻ lấy từ các từ ngữ cần ghi nhớ, đáp án do app soạn.")],
       review=[("part1[6]", "đáp án điền từ do app soạn; \"chú và cô\", \"cậu và dì\" đổi chỗ cũng đúng")])

# 233 — Ngữ pháp: Câu – Hai bộ phận chính (tiếp theo) (tr.58)
lesson(233, [58],
       [title("Ngữ pháp: Câu – Hai bộ phận chính", "Tiếp theo"),
        *rule("Bộ phận chính thứ nhất của câu còn là bộ phận trả lời câu hỏi: "
             "Trong câu nói đến con gì? Nói đến cái gì?"),
        q("1. Đặt câu hỏi để tìm bộ phận chính thứ nhất trong hai câu sau:",
          lines=["Con chìa vôi vừa hót vừa bay.", "Hoa mướp nở vàng rực."]),
        q("2. Tìm bộ phận chính thứ nhất trong các câu sau:",
          lines=["Bé Hoa đang viết thư cho bố.", "Em nắn nót viết từng chữ.", "Bức thư đã viết xong.",
                 "Con mèo đang lim dim ngủ trên bàn."])],
       listen(("chìa vôi", "hoa mướp", "con mèo"), ("hoa mướp", "chìa vôi", "bức thư"), ("bức thư", "con mèo", "nắn nót"),
              ("con mèo", "bức thư", "vàng rực"), ("vàng rực", "lim dim", "nắn nót"), ("lim dim", "vàng rực", "chìa vôi")),
       notes=[("khac_sach", KS_ORAL)])

# 234 — Tập làm văn: Quan sát tranh và trả lời câu hỏi — Giàn mướp (tr.58)
lesson(234, [58],
       [title("Tập làm văn: Quan sát tranh và trả lời câu hỏi"),
        title("Đề bài: Giàn mướp.", "Xem tranh ở bài Giàn mướp."),
        picture(GIAN_MUOP_IMG, "Con nhìn kĩ tranh giàn mướp nhé.", "giàn mướp"),
        q("1. Giàn mướp (trong tranh) bắc ở đâu?"),
        q("2. Trên giàn mướp, em thấy những gì?"),
        q("3. Hình thù những quả mướp khác nhau như thế nào?"),
        q("4. Em hãy nhìn vào tranh đặt thêm một câu hỏi và tự trả lời.")],
       listen(("giàn mướp", "mặt ao", "quả mướp"), ("quả mướp", "hoa mướp", "giàn mướp"), ("hoa vàng", "lá xanh", "mặt ao"),
              ("mặt ao", "giàn mướp", "hoa vàng"), ("hình thù", "câu hỏi", "quả mướp"), ("câu hỏi", "trả lời", "hình thù")),
       images={GIAN_MUOP_IMG: GIAN_MUOP_DESC},
       notes=[("khac_sach", "Tập làm văn quan sát tranh: app dùng lại tranh bài Giàn mướp; bé trả lời miệng cùng bố mẹ.")],
       review=[("part1[2]", "lời dẫn tranh do app soạn")])
