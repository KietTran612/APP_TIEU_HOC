"""Tuần 7 (mục 219–226), tr.44–51, ảnh 023–026."""
from l2lib import *

# 219 — Bài 24. Làm anh (tr.44–45)
POEM24 = ["Làm anh khó đấy", "Phải đâu chuyện đùa", "Với em gái bé", "Phải \"người lớn\" cơ.",
          "Khi em bé khóc", "Anh phải dỗ dành", "Nếu em bé ngã", "Anh nâng dịu dàng.",
          "Mẹ cho quà bánh", "Chia em phần hơn", "Có đồ chơi đẹp", "Cũng nhường em luôn.",
          "Làm anh thật khó", "Nhưng mà thật vui", "Ai yêu em bé", "Thì làm được thôi."]
lesson(219, [44, 45],
       [picture("img_b219_lamf_anh", "Anh kéo xe đồ chơi cho em bé.", "làm anh"),
        title("Làm anh"),
        *sentences(*POEM24),
        passage("poem", "PHAN THỊ THANH NHÀN", breaks=[4, 8, 12]),
        q("1. Khổ thơ thứ 2 khuyên làm anh phải biết chăm sóc em như thế nào?", marker="?"),
        q("2. Khổ thơ thứ 3 còn khuyên làm anh phải làm gì đối với em?"),
        q("3. Tại sao \"Ai yêu em bé\" mới làm anh (hoặc làm chị) được?"),
        q("4. Em hãy tìm một từ có nghĩa như từ nâng trong câu \"Anh nâng dịu dàng\".")],
       listen(("dỗ dành", "dịu dàng", "quà bánh"), ("dịu dàng", "dỗ dành", "đồ chơi"), ("quà bánh", "đồ chơi", "em bé"),
              ("đồ chơi", "quà bánh", "phần hơn"), ("nhường em", "chia em", "làm anh"), ("chuyện đùa", "người lớn", "dỗ dành")),
       images={"img_b219_lamf_anh": "Trên sân dưới gốc cây, cậu anh mặc áo len vừa đi vừa kéo dây chiếc ô tô đồ chơi; "
                                    "em bé chập chững bám xe tập đi, cười giơ tay theo anh"},
       notes=[("khac_sach", KS_ORAL)])

# 220 — Bài 25. Ngôi nhà (Học thuộc lòng, tr.46–47)
POEM25 = ["Em yêu nhà em", "Hàng xoan trước ngõ", "Hoa xao xuyến nở", "Như mây từng chùm.",
          "Em yêu tiếng chim", "Đầu hồi lảnh lót", "Mái vàng thơm phức", "Rạ đầy sân phơi.",
          "Em yêu ngôi nhà", "Gỗ tre mộc mạc", "Như yêu đất nước", "Bốn mùa chim ca."]
lesson(220, [46, 47],
       [picture("img_b220_ngoi_nhaf", "Ngôi nhà nhỏ có hàng xoan trước ngõ.", "ngôi nhà"),
        title("Ngôi nhà", "Học thuộc lòng"),
        *sentences(*POEM25),
        passage("poem", "TÔ HÀ", breaks=[4, 8]),
        *glossary("Đầu hồi: hai bên đầu nhà.", "Mộc mạc: đơn sơ, giản dị.",
                 "Xoan: tên một loại cây (có vùng gọi là cây sầu đông)."),
        q("1. Trước ngõ ngôi nhà có gì đẹp và đáng yêu?", marker="?"),
        q("2. Đầu hồi có tiếng gì vui?"),
        q("3. Ngôi nhà này làm bằng gì? Lợp bằng gì?"),
        q("4. Tại sao ngôi nhà mộc mạc nhưng đáng yêu?"),
        q("5. Tìm thêm các từ chỉ mùi thơm như: thơm phức."),
        memorize()],
       listen(("hàng xoan", "đầu hồi", "sân phơi"), ("xao xuyến", "lảnh lót", "mộc mạc"), ("thơm phức", "mộc mạc", "lảnh lót"),
              ("mộc mạc", "xao xuyến", "thơm phức"), ("sân phơi", "hàng xoan", "đất nước"), ("đầu hồi", "ngôi nhà", "từng chùm")),
       images={"img_b220_ngoi_nhaf": "Ngôi nhà mái rạ vàng ở làng quê, sân phơi trước nhà, hàng cây xoan trổ hoa tím "
                                     "từng chùm trước ngõ; hai bạn nhỏ khoác vai nhau đứng ở ngõ"},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)])

# 221 — Bài 26. Bé Hoa (tr.47–48)
lesson(221, [47, 48],
       [picture("img_b221_bes_hoa", "Hoa đưa võng ru em Nụ ngủ.", "đưa võng"),
        title("Bé Hoa"),
        *prose("VIỆT TÂM",
               ["Bây giờ Hoa đã là chị rồi.", "Mẹ có thêm em Nụ.", "Em Nụ da đỏ hồng đẹp thật.",
                "Em Nụ cũng đã lớn lên nhiều.", "Em ngủ ít hơn trước,",
                "có lúc mắt em mở to, vừa đen vừa tròn, cứ nhìn Hoa mãi.", "Hoa yêu em lắm.",
                "Hoa thích đưa võng ru cho em ngủ."],
               ["Đêm nay, Hoa hát hết cả bài hát mà mẹ vẫn chưa về.", "Từ ngày bố đi bộ đội, mẹ bận việc nhiều hơn.",
                "Em Nụ đã ngủ.", "Bây giờ Hoa phải viết thư cho bố.",
                "Vặn to đèn, Hoa ngồi trên ghế, nắn nót viết từng chữ:"],
               ["Bố ạ,"],
               ["Em Nụ ở nhà ngoan lắm.", "Nó ngủ cũng ngoan nữa.", "Con hết cả bài hát ru em rồi.",
                "Bao giờ bố về, bố dạy thêm bài khác cho con.", "Dạy bài thật hay ấy, bố nhé!"]),
        q("1. Bé Nụ rất xinh. Em hãy tìm những nét đáng yêu của bé Nụ.", marker="?"),
        q("2. Hoa đã giúp mẹ làm gì?"),
        q("3. Lúc bố của Hoa nhận được thư, em tưởng tượng bố Hoa có vui không? Tại sao?"),
        q("4. Tìm trong bài những từ chỉ người trong gia đình. "
          "Em kể thêm một vài từ khác dùng để chỉ người thân trong gia đình."),
        q("5. Đoạn thư Hoa viết cho bố gồm mấy câu?")],
       listen(("đưa võng", "bài hát", "viết thư"), ("bộ đội", "bận việc", "đỏ hồng"), ("đỏ hồng", "nắn nót", "bộ đội"),
              ("viết thư", "đưa võng", "vặn đèn"), ("nắn nót", "đỏ hồng", "bận việc"), ("bài hát", "viết thư", "nắn nót")),
       images={"img_b221_bes_hoa": "Buổi tối, cô bé Hoa ngồi bên chiếc võng lưới đưa võng ru em bé ngủ; đèn dầu sáng "
                                   "trên bàn, chú mèo nằm ngủ dưới gầm bàn, cửa sổ tối"},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 222 — Bài 27. Ông tôi (Bài đọc thêm, tr.48–49; sách không có tranh)
lesson(222, [48, 49],
       [title("Ông tôi", "Bài đọc thêm"),
        *prose("PHONG THU",
               ["Ông tôi năm nay đã già lắm.", "Tóc ông bạc phơ và ông không thể ăn mía như tôi được.",
                "Thế mà hôm nọ, ông lại trồng một cây ổi,", "giống ổi Bo, quả to, thơm ngọt."],
               ["Tôi liền hỏi:"], ["- Ông ơi, ông ăn ổi làm sao được nữa ạ?"],
               ["Ông tôi nhìn tôi, móm mém cười:"], ["- Ông không ăn được thì đã có cháu ông ăn!"],
               ["Ông tôi đã già, thế mà không một ngày nào ông quên ra vườn.",
                "Tôi vẫn thường tha thẩn theo ông, khi xới gốc, lúc tưới nước giúp ông.",
                "Tôi thầm mong sao cho ông tôi đừng già thêm nữa."])],
       listen(("cây ổi", "ăn mía", "quả to"), ("bạc phơ", "móm mém", "tha thẩn"), ("móm mém", "bạc phơ", "thơm ngọt"),
              ("xới gốc", "tưới nước", "ra vườn"), ("tha thẩn", "móm mém", "xới gốc"), ("thơm ngọt", "quả to", "bạc phơ")),
       notes=[("khac_sach", KS_SPLIT)])

# 223 — Chính tả tuần 7 (tr.49)
lesson(223, [49],
       [title("Tập chép: Làm anh", "Nhìn sách"),
        title("Bài chép: 3 khổ thơ đầu.", "Phần này con chép vào vở cùng bố mẹ."),
        words("chuyện", "người lớn", "dỗ dành", "dịu dàng", "nâng", "ngã"),
        combine("chuyện", "câu", "trò", "kể", at="before"),
        fill(["dỗ", "giỗ"], ("dỗ em", "dỗ", "dỗ"), ("dạy dỗ", "dỗ", "dỗ"), ("ngày giỗ", "giỗ", "giỗ")),
        fill(["dàng", "ràng"], ("dịu dàng", "dàng", "dàng"), ("rõ ràng", "ràng", "ràng"), ("dễ dàng", "dàng", "dàng"),
             ("rộn ràng", "ràng", "ràng")),
        fill(["ngã", "ngả"], ("Chị ngã em nâng", "ngã", "ngã"), ("Mỗi người đi một ngả", "ngả", "ngả")),
        title("Đố em điền đúng"),
        fill_passage(["Nâng như [nâng|hứng|ngã] trứng, hứng như [hứng|nâng|ngả] hoa."]),
        title("Chính tả: Bé Hoa", "Nghe đọc"),
        title("Bài viết: \"Bây giờ... em ngủ\".", "Phần này con nghe bố mẹ đọc rồi viết vào vở."),
        words("Hoa", "Nụ", "yêu", "da", "ru", "mắt", "ngủ", "võng"),
        {"type": "combine_words", "base": "yêu",
         "items": [{"with": "mến", "at": "after"}, {"with": "thương", "at": "after"}, {"with": "thân", "at": "before"},
                   {"with": "quý", "at": "after"}]},
        fill(["da", "ra", "gia"], ("da thịt", "da", "da"), ("ra vào", "ra", "ra"), ("gia đình", "gia", "gia"),
             ("giày bằng da", "da", "da")),
        fill(["mắt", "mắc"], ("hai con mắt", "mắt", "mắt"), ("mắc lỗi chính tả", "mắc", "mắc"), ("có tai có mắt", "mắt", "mắt"),
             ("thắc mắc", "mắc", "mắc"))],
       listen(("câu chuyện", "trò chuyện", "kể chuyện"), ("dỗ dành", "dịu dàng", "rõ ràng"), ("ngày giỗ", "dạy dỗ", "rộn ràng"),
              ("yêu mến", "thân yêu", "yêu quý"), ("thắc mắc", "con mắt", "gia đình"), ("võng", "ru", "ngủ")),
       notes=[("khac_sach", KS_WRITE), ("khac_sach", "Điền chỗ trống, ghép chữ làm bằng chạm hoặc kéo thẻ.")],
       review=[("part1[3]", "cách ghép do app chọn: câu chuyện, trò chuyện, kể chuyện"),
               ("part1[4]", "đáp án dỗ/giỗ"), ("part1[5]", "đáp án dàng/ràng"), ("part1[6]", "đáp án ngã/ngả"),
               ("part1[8]", "thành ngữ do app điền: nâng như nâng trứng, hứng như hứng hoa"),
               ("part1[12]", "cách ghép do app chọn: yêu mến, yêu thương, thân yêu, yêu quý"),
               ("part1[13]", "đáp án da/ra/gia"), ("part1[14]", "đáp án mắt/mắc")])

# 224 — Từ ngữ: Ông bà (tr.50)
lesson(224, [50],
       [title("Từ ngữ: Ông bà"),
        title("Những từ ngữ cần ghi nhớ"),
        words("ông", "bà", "ông nội", "bà nội", "ông ngoại", "bà ngoại"),
        words("yêu quý", "kính mến", "vâng lời", "giúp đỡ"),
        title("Bài tập 1: Chọn từ ở mục I điền vào chỗ trống cho thích hợp"),
        fill_passage(["Cha của cha em thì em gọi là [ông nội].", "Mẹ của cha em thì em gọi là [bà nội].",
                      "Cha của mẹ em thì em gọi là [ông ngoại].", "Mẹ của mẹ em thì em gọi là [bà ngoại]."],
                     bank=["ông", "bà", "ông nội", "bà nội", "ông ngoại", "bà ngoại"]),
        title("Bài tập 2: Điền vào chỗ trống"),
        fill_passage(["Bé Tâm ở với bà ngoại.", "Thường ngày, Tâm vẫn [giúp đỡ] bà, xâu kim cho bà may vá.",
                      "Tâm hay trèo cây.", "Bà bảo không nên trèo cây và không nên ăn quả xanh.", "Tâm [vâng lời] bà.",
                      "Bé Tâm hết lòng [kính mến] bà ngoại.", "Bà cũng rất [yêu quý] bé Tâm."],
                     bank=["yêu quý", "kính mến", "vâng lời", "giúp đỡ"])],
       listen(("ông nội", "bà nội", "ông ngoại"), ("bà ngoại", "ông ngoại", "bà nội"), ("kính mến", "yêu quý", "giúp đỡ"),
              ("vâng lời", "giúp đỡ", "kính mến"), ("giúp đỡ", "vâng lời", "yêu quý"), ("may vá", "xâu kim", "trèo cây")),
       notes=[("khac_sach", "Điền từ bằng chạm hoặc kéo thẻ từ vào chỗ trống; đáp án do app soạn.")],
       review=[("part1[5]", "đáp án điền từ do app soạn"),
               ("part1[7]", "đáp án điền từ do app soạn; \"hết lòng ... bà ngoại\" và \"rất ... bé Tâm\" có thể đổi chỗ "
                            "kính mến / yêu quý")])

# 225 — Ngữ pháp: Câu – Hai bộ phận chính (tiếp theo) (tr.50–51)
lesson(225, [50, 51],
       [title("Ngữ pháp: Câu – Hai bộ phận chính", "Tiếp theo"),
        *rule("Em Nụ đang ngủ.", "Hỏi: Trong câu, nói đến ai?", "Trả lời: Nói đến \"Em Nụ\".",
             "Kết luận: \"Em Nụ\" là bộ phận chính thứ nhất của câu."),
        *rule("Bộ phận chính thứ nhất của câu là bộ phận trả lời câu hỏi: Trong câu, nói đến ai?"),
        q("Đặt câu hỏi để tìm bộ phận chính thứ nhất bằng cách dùng từ \"ai\":",
          lines=["Mẹ cho quà bánh.", "Bé Hoa đã lớn rồi.", "Hai chị em về nhà."])],
       listen(("quà bánh", "về nhà", "lớn rồi"), ("bộ phận", "câu hỏi", "trả lời"), ("câu hỏi", "kết luận", "bộ phận"),
              ("về nhà", "quà bánh", "đang ngủ"), ("đang ngủ", "về nhà", "kết luận"), ("kết luận", "trả lời", "quà bánh")),
       notes=[("khac_sach", KS_ORAL)])

# 226 — Tập làm văn: Điền từ — Chị và em (tr.51)
lesson(226, [51],
       [title("Tập làm văn: Điền từ"),
        title("Đề bài: Chị và em.", "Em tự tìm lấy từ thích hợp điền vào chỗ trống."),
        fill_passage(["Bé Hoa là [chị|em|bà] của em Nụ.", "Bé Sơn là [em|chị|ông] của chị Lan.",
                      "Hoa rất [yêu|ghét|sợ] em Nụ còn Sơn thì rất [vâng lời|ghét|trêu] chị Lan.",
                      "Có đồ chơi đẹp, Hoa [nhường|giấu|giành] cho em Nụ.",
                      "Có quà bánh ngon, chị Lan đều [để phần|giấu|ăn hết] cho Sơn.",
                      "Vì thế, chị và em sống với nhau rất [hòa thuận|buồn|xa cách]."])],
       listen(("hòa thuận", "nhường", "để phần"), ("nhường", "hòa thuận", "vâng lời"), ("để phần", "đồ chơi", "quà bánh"),
              ("đồ chơi", "quà bánh", "hòa thuận"), ("quà bánh", "để phần", "đồ chơi"), ("vâng lời", "nhường", "để phần")),
       notes=[("khac_sach", "Sách để bé tự tìm từ: app cho mỗi chỗ trống 3 thẻ để chọn; thẻ và đáp án do app soạn.")],
       review=[("part1[2]", "thẻ chọn và đáp án điền chỗ trống do app soạn")])
