"""Tuần 14 (mục 274–281), tr.94–100, ảnh 048–051."""
from l2lib import *

GAU_IMG = "img_b276_nhaf_gaaus"
GAU_DESC = ("Trong rừng già, gia đình nhà Gấu: gấu bố béo đứng lên hai chân bên gốc cây, gấu mẹ đi lặc lè, hai gấu con "
            "chạy theo, một gấu con trèo trên cành cây cao")

# 274 — Bài 51. Nhớ Việt Bắc (tr.94–95)
POEM51 = ["Ta về mình có nhớ ta", "Ta về, ta nhớ những hoa cùng người.", "Rừng xanh hoa chuối đỏ tươi",
          "Đèo cao nắng ánh dao gài thắt lưng.", "Ngày xuân mơ nở trắng rừng", "Nhớ người đan nón chuốt từng sợi dang.",
          "Ve kêu rừng phách đổ vàng", "Nhớ cô em gái hái măng một mình.", "Rừng thu trăng rọi hòa bình",
          "Nhớ ai tiếng hát ân tình thủy chung."]
lesson(274, [94, 95],
       [picture("img_b274_vieetj_bawcs", "Rừng núi Việt Bắc với hoa chuối đỏ tươi.", "Việt Bắc"),
        title("Nhớ Việt Bắc"),
        *sentences(*POEM51),
        passage("poem", "TỐ HỮU"),
        *glossary("Việt Bắc: chỉ một số tỉnh miền núi phía bắc nước ta, trước kia được xây dựng thành căn cứ lãnh đạo "
                 "cách mạng và kháng chiến chống thực dân Pháp.", "Phách: một loại tre rừng.",
                 "Dang: một loại cây giống cây nứa, rất dẻo, dùng để chẻ làm lạt buộc.",
                 "Ân tình thủy chung: có ơn có nghĩa, trước sau không thay đổi."),
        q("1. Bài này tả cảnh rừng núi hay đồng bằng? Tại sao em biết?", marker="?"),
        q("2. Em hãy tìm những từ chỉ màu sắc trong bài."),
        q("3. Trong bài còn có những âm thanh gì?"),
        q("4. Tác giả nhớ những cảnh gì, nhớ những người nào?")],
       listen(("hoa chuối", "rừng phách", "đèo cao"), ("đỏ tươi", "trắng rừng", "đổ vàng"), ("đan nón", "hái măng", "tiếng hát"),
              ("thủy chung", "ân tình", "hòa bình"), ("rừng phách", "hoa chuối", "sợi dang"), ("hái măng", "đan nón", "rừng thu")),
       images={"img_b274_vieetj_bawcs": "Rừng núi Việt Bắc: cây chuối rừng trổ hoa đỏ tươi, rừng mơ nở trắng, hai cô gái "
                                        "miền núi đội nón đeo gùi đi trên lối mòn giữa những tảng đá lớn"},
       notes=[("khac_sach", KS_ORAL)])

# 275 — Bài 52. Sa Pa (Học thuộc lòng, tr.95–96)
POEM52 = ["Đường lên đỉnh núi Sa Pa", "Hoa chen thắm lá, mây là là bay.", "Hương đào thoang thoảng đâu đây",
          "Nhà ai mận chín, trái cây trĩu cành.", "Đường vòng sườn núi quanh quanh",
          "Bậc thang nương rẫy, nhà tranh ven rừng.", "Chào anh bộ đội biên phòng",
          "Cầu Mây, Thác Bạc, trập trùng núi cao."]
lesson(275, [95, 96],
       [picture("img_b275_sa_pa", "Núi đồi Sa Pa với ruộng bậc thang.", "Sa Pa"),
        title("Sa Pa", "Học thuộc lòng"),
        *sentences(*POEM52),
        passage("poem", "LÊ NHƯ SÂM"),
        *glossary("Sa Pa: một nơi nghỉ mát nổi tiếng, thuộc tỉnh Lào Cai.",
                 "Cầu Mây: tên một cái cầu treo, bắc giữa hai sườn núi.",
                 "Thác Bạc: tên một ngọn thác chảy từ sườn núi xuống, trông như tấm lụa trắng xóa.",
                 "Bộ đội biên phòng: bộ đội canh phòng vùng đất của nước ta giáp với một nước khác."),
        q("1. Câu thứ 2 tả những cảnh đẹp gì?", marker="?"),
        q("2. Ở câu 3 và 4, ta thấy Sa Pa về mùa hè có những thứ quả gì?"),
        q("3. Đi men theo sườn núi, ta thấy những gì?"),
        find("4. Tìm trong bài những từ láy (ví dụ: quanh quanh).",
             {"word": ["là", "thoang", "thoảng", "quanh", "trập", "trùng"]}),
        memorize()],
       listen(("bậc thang", "nương rẫy", "nhà tranh"), ("thoang thoảng", "là là", "quanh quanh"), ("trập trùng", "trĩu cành", "thoang thoảng"),
              ("hương đào", "mận chín", "trái cây"), ("biên phòng", "bộ đội", "Thác Bạc"), ("Cầu Mây", "Thác Bạc", "nương rẫy")),
       images={"img_b275_sa_pa": "Núi đồi Sa Pa trập trùng trong mây, ruộng bậc thang uốn quanh sườn núi, mấy nếp nhà "
                                 "tranh ven rừng thông, đào nở hồng bên đường"},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)],
       review=[("part1[15]", "từ láy do app chọn: là là, thoang thoảng, quanh quanh, trập trùng")])

# 276 — Bài 53. Nhà Gấu ở trong rừng (tr.97–98)
lesson(276, [97, 98],
       [picture(GAU_IMG, "Cả nhà Gấu đi trong rừng.", "nhà Gấu"),
        title("Nhà Gấu ở trong rừng"),
        *prose("TÔ HOÀI",
               ["Cả nhà Gấu ở trong rừng.", "Mùa xuân, cả nhà Gấu kéo nhau đi bẻ măng và uống mật ong.",
                "Mùa thu, Gấu đi nhặt quả hạt dẻ.", "Gấu bố, gấu mẹ, gấu con cùng béo rung rinh,",
                "bước đi lặc lè, lặc lè.", "Béo đến nỗi khi mùa đông tới, suốt ba tháng rét,",
                "cả nhà Gấu đứng tránh gió trong gốc cây, không cần đi kiếm ăn,",
                "chỉ mút hai bàn chân mỡ cũng đủ no.", "Sang xuân ấm áp, cả nhà Gấu đi bẻ măng, tìm uống mật ong",
                "và đến mùa thu lại nhặt quả hạt dẻ.", "Gấu bố, gấu mẹ, gấu con lại béo rung rinh,",
                "chân lại nặng những mỡ, bước đi lặc lè, lặc lè..."]),
        q("1. Mùa xuân, Gấu đi kiếm thức ăn gì?", marker="?"),
        q("2. Mùa thu, Gấu đi kiếm thức ăn gì?"),
        q("3. Tìm những từ tả đàn gấu rất béo."),
        q("4. Đặt một câu với từ: lặc lè.")],
       listen(("bẻ măng", "mật ong", "hạt dẻ"), ("lặc lè", "rung rinh", "ấm áp"), ("gốc cây", "bàn chân", "mùa đông"),
              ("rung rinh", "lặc lè", "tránh gió"), ("hạt dẻ", "mật ong", "bẻ măng"), ("tránh gió", "ấm áp", "gốc cây")),
       images={GAU_IMG: GAU_DESC},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 277 — Bài 54. Câu chuyện đàn ong mật (Bài đọc thêm, tr.98–99; sách không có tranh)
lesson(277, [98, 99],
       [title("Câu chuyện đàn ong mật", "Bài đọc thêm"),
        *prose("VŨ HÙNG",
               ["Ngày xưa có một người đàn bà tên là nàng Ong.",
                "Nàng Ong làm việc chăm chỉ nhưng vẫn nghèo túng vì nhà đông miệng ăn.",
                "Nàng Ong mong các con khôn lớn để đỡ đần mình.", "Nhưng lũ con nàng, đứa nào cũng lười.",
                "Nàng thường khuyên các con:"],
               ["Muốn no thì phải chăm làm", "Một hạt thóc vàng, chín giọt mồ hôi."],
               ["Nhưng không đứa nào nghe.", "Lũ con gái nói: \"Chúng con sẽ đi tìm cái khung cửi thần.",
                "Cái khung cửi ấy, cứ gõ vào là ra vải, không cần khó nhọc ngồi dệt\".",
                "Lũ con trai nói: \"Chúng con sẽ vào rừng tìm cái rìu vàng của thần núi.",
                "Người ta bảo cái rìu ấy có thể tự ngả cây, người không phải mó tay vào\"."],
               ["Thế rồi một hôm, chúng bỏ nhà ra đi để nàng Ong ở nhà vò võ một mình.",
                "Nàng buồn phiền mà chết."],
               ["Mấy năm sau, lũ con nàng Ong trở về.", "Đứa nào cũng rách rưới, xanh xao, vàng vọt.",
                "Chúng đã đi khắp núi cao, rừng sâu nhưng không tìm được vật quý.",
                "Hổ thẹn vì không nghe lời mẹ dạy, chúng bảo nhau chăm chỉ làm ăn."],
               ["Khi chết, chúng gặp nàng Ong.", "Mẹ con biến thành loài ong bây giờ.",
                "Mẹ biến thành Ong Chúa, các con biến thành Ong Thợ.", "Ong Thợ làm việc suốt ngày.",
                "Chúng làm ra mật ngọt lịm mà mọi người ưa thích."])],
       listen(("khung cửi", "rìu vàng", "mật ngọt"), ("nghèo túng", "vò võ", "hổ thẹn"), ("rách rưới", "xanh xao", "vàng vọt"),
              ("Ong Chúa", "Ong Thợ", "nàng Ong"), ("mồ hôi", "hạt thóc", "khung cửi"), ("hổ thẹn", "buồn phiền", "chăm chỉ")),
       notes=[("khac_sach", KS_SPLIT)])

# 278 — Chính tả tuần 14 (tr.99)
lesson(278, [99],
       [title("Chính tả: Một vài cảnh đẹp", "Trí nhớ"),
        title("Bài viết: Cả bài.", "Phần này con nhớ lại rồi viết vào vở."),
        words("quyên", "lập lòe", "lựu", "xanh rợn", "cỏ"),
        combine("quyên", "chim", "gọi", "hè"),
        combine("lòe", "lập", "sáng", "loẹt", at="before"),
        fill_passage(["Đầu tường [lửa lựu|cỏ non|cành lê] lập lòe đâm bông.",
                      "[Cỏ non|Lửa lựu|Cành lê] xanh [rợn|đỏ|trắng] chân trời."]),
        title("Chính tả: Nhà Gấu ở trong rừng", "Nghe đọc"),
        title("Bài viết: \"Mùa thu... cũng no\".", "Phần này con nghe bố mẹ đọc rồi viết vào vở."),
        words("hạt dẻ", "lặc lè", "suốt", "mút", "đến nỗi"),
        fill(["dẻ", "giẻ"], ("Hạt dẻ rất bùi.", "dẻ", "dẻ"), ("Cây gỗ giẻ", "giẻ", "giẻ")),
        fill(["dẻ", "dễ"], ("Gấu ăn hạt dẻ.", "dẻ", "dẻ"), ("Chim dễ ăn giun.", "dễ", "dễ")),
        find("Tìm trong bài chính tả những chữ có dấu hỏi và dấu ngã.", {"tone": ["hỏi", "ngã"]},
             text=["Mùa thu, Gấu đi nhặt quả hạt dẻ.", "Gấu bố, gấu mẹ, gấu con cùng béo rung rinh,",
                   "bước đi lặc lè, lặc lè.", "Béo đến nỗi khi mùa đông tới, suốt ba tháng rét,",
                   "cả nhà Gấu đứng tránh gió trong gốc cây, không cần đi kiếm ăn,",
                   "chỉ mút hai bàn chân mỡ cũng đủ no."])],
       listen(("chim quyên", "gọi hè", "quyên hè"), ("lập lòe", "sáng lòe", "lòe loẹt"), ("lửa lựu", "cỏ non", "xanh rợn"),
              ("hạt dẻ", "lặc lè", "đến nỗi"), ("cây gỗ", "hạt dẻ", "ăn giun"), ("mút", "suốt", "nỗi")),
       notes=[("khac_sach", KS_WRITE), ("khac_sach", "Ghép chữ, điền chỗ trống, tìm chữ làm bằng chạm hoặc kéo thẻ.")],
       review=[("part1[3]", "cách ghép do app chọn: chim quyên, quyên gọi hè"),
               ("part1[4]", "cách ghép do app chọn: lập lòe, sáng lòe, lòe loẹt"),
               ("part1[5]", "đáp án điền từ do app soạn theo bài Một vài cảnh đẹp"),
               ("part1[9]", "đáp án dẻ/giẻ do app soạn"), ("part1[10]", "đáp án dẻ/dễ do app soạn")])

# 279 — Từ ngữ: Rừng núi (tr.99–100)
lesson(279, [99, 100],
       [title("Từ ngữ: Rừng núi"),
        title("Những từ ngữ cần ghi nhớ"),
        words("rừng", "núi", "đồi", "suối", "đèo", "lâm sản", "thú rừng", "chim rừng", "gỗ quý"),
        words("trập trùng", "rậm rạp", "trèo đèo lội suối"),
        title("Bài tập"),
        picture("img_b279_nuis_rungf", "Đây là cảnh núi rừng.", "núi rừng"),
        q("Nhìn vào hình vẽ, em chỉ rõ: đỉnh núi, sườn núi, chân núi, đèo."),
        q("Kể vài sản vật ở rừng nước ta mà em biết."),
        fill_passage(["Ở miền rừng núi thường có cây cối [rậm rạp].", "Núi non [trập trùng].",
                      "Có nơi, học sinh đi học phải [trèo đèo lội suối] mới tới lớp học."],
                     bank=["trập trùng", "rậm rạp", "trèo đèo lội suối"])],
       listen(("lâm sản", "thú rừng", "gỗ quý"), ("trập trùng", "rậm rạp", "trèo đèo"), ("chim rừng", "thú rừng", "lâm sản"),
              ("rậm rạp", "trập trùng", "gỗ quý"), ("gỗ quý", "chim rừng", "suối"), ("đèo", "đồi", "núi")),
       images={"img_b279_nuis_rungf": "Núi đá cao có đỉnh nhọn, sườn núi phủ cây rừng, con đèo uốn quanh sườn núi, dưới "
                                      "chân núi có tảng đá lớn và dòng suối nhỏ"},
       notes=[("khac_sach", KS_ORAL), ("khac_sach", "Điền từ bằng chạm hoặc kéo thẻ; đáp án do app soạn.")],
       review=[("part1[5]", "lời dẫn tranh do app soạn"), ("part1[8]", "đáp án điền từ do app soạn")])

# 280 — Ngữ pháp: Chữ và chữ cái (tr.100)
lesson(280, [100],
       [title("Ngữ pháp: Chữ và chữ cái"),
        *rule("Chữ do một hoặc nhiều chữ cái tạo nên.", "Ví dụ: Đàn chim gáy ở đâu bay về gù vang cánh đồng.",
             "Chữ gáy gồm 3 chữ cái g, a, y.", "Chữ ở gồm 1 chữ cái ơ."),
        find("1. Tìm những chữ có 3 chữ cái trong 2 câu sau đây.",
             {"word": ["mặt", "núi", "ngủ", "tre", "lên"]}, text=["Mặt trời xuống núi ngủ.", "Tre nâng vầng trăng lên."]),
        find("Tìm những chữ có 4 chữ cái trong 2 câu sau đây.", {"word": ["trời", "nâng", "vầng"]},
             text=["Mặt trời xuống núi ngủ.", "Tre nâng vầng trăng lên."]),
        q("2. Em hãy đặt một câu với từ đồng lúa. Trong câu em đặt có mấy chữ? Chữ đầu câu có mấy chữ cái? "
          "Chữ cuối câu có mấy chữ cái? Trong câu, chữ cái nào phải viết hoa?")],
       listen(("chữ cái", "đồng lúa", "chim gáy"), ("mặt trời", "vầng trăng", "đồng lúa"), ("vầng trăng", "mặt trời", "cánh đồng"),
              ("cánh đồng", "đồng lúa", "chữ cái"), ("chim gáy", "cánh đồng", "vầng trăng"), ("đồng lúa", "chim gáy", "mặt trời")),
       notes=[("khac_sach", "Bé tìm chữ bằng cách chạm; đáp án do app đếm chữ cái (ch, tr, ng... tính là 2 chữ cái).")],
       review=[("part1[2]", "đáp án chữ có 3 chữ cái do app đếm: Mặt, núi, ngủ, tre, lên"),
               ("part1[3]", "đáp án chữ có 4 chữ cái do app đếm: trời, nâng, vầng")])

# 281 — Tập làm văn: Quan sát tranh và trả lời câu hỏi — Nhà Gấu ở trong rừng (tr.100)
lesson(281, [100],
       [title("Tập làm văn: Quan sát tranh và trả lời câu hỏi"),
        title("Đề bài: Nhà Gấu ở trong rừng.", "Xem tranh ở bài Nhà Gấu ở trong rừng."),
        picture(GAU_IMG, "Con nhìn kĩ tranh nhà Gấu nhé.", "nhà Gấu"),
        q("1. Bức tranh này vẽ cảnh gì?"),
        q("2. Gia đình nhà Gấu có những ai?"),
        q("3. Chúng đang làm gì trong rừng?"),
        q("4. Hình dáng Gấu bố, Gấu mẹ và cả lũ con trông như thế nào?"),
        q("5. Ở miền rừng núi nước ta, ngoài gấu ra còn có những loài vật gì quý?")],
       listen(("gấu bố", "gấu mẹ", "gấu con"), ("gấu con", "gấu bố", "rừng"), ("rừng", "gốc cây", "gấu mẹ"),
              ("gốc cây", "rừng", "hình dáng"), ("hình dáng", "gốc cây", "loài vật"), ("loài vật", "hình dáng", "gấu bố")),
       images={GAU_IMG: GAU_DESC},
       notes=[("khac_sach", "Tập làm văn quan sát tranh: app dùng lại tranh bài Nhà Gấu ở trong rừng; bé trả lời miệng.")],
       review=[("part1[2]", "lời dẫn tranh do app soạn")])
