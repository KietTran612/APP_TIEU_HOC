"""Tuần 13 (mục 266–273), tr.87–93, ảnh 044–047."""
from l2lib import *

MO_IMG = "img_b268_vungf_mor"
MO_DESC = ("Vịnh biển vùng mỏ: núi đá cao sừng sững bên bờ, những chiếc thuyền buồm căng gió chở đầy cá, tàu chở than "
           "đậu ngoài khơi, xa xa là bến cảng và nhà cửa san sát dưới chân núi")

# 266 — Bài 47. Hoa mai vàng (tr.87–88)
lesson(266, [87, 88],
       [picture("img_b266_hoa_mai_vangf", "Cành hoa mai vàng nở rộ.", "hoa mai"),
        title("Hoa mai vàng"),
        *prose("Theo \"Mùa xuân và phong tục Việt Nam\"",
               ["Hoa mai cũng có năm cánh như hoa đào, nhưng cánh hoa mai to hơn cánh hoa đào một chút.",
                "Những nụ mai không phô hồng mà ngời xanh màu ngọc bích.", "Sắp nở, nụ mai mới phô vàng.",
                "Khi nở, cánh hoa mai xòe ra mịn màng như lụa.", "Những cánh hoa ánh lên một sắc vàng muốt, mượt mà.",
                "Một mùi thơm lựng như nếp hương phảng phất bay ra.",
                "Hoa mai trổ từng chùm thưa thớt, không đơm đặc như hoa đào.",
                "Nhưng cành mai uyển chuyển hơn cành đào.", "Vì thế, khi cành mai rung rinh cười với gió xuân,",
                "ta liên tưởng đến hình ảnh một đàn bướm vàng rập rờn bay lượn."]),
        *glossary("Ngọc bích: một loại đá quý màu xanh biếc, rất đẹp."),
        q("1. Hoa mai khác hoa đào như thế nào?", marker="?"),
        q("2. Hoa mai khi nở đẹp như thế nào?"),
        q("3. Ngoài màu sắc đẹp, hoa mai còn có gì khiến mọi người ưa thích?"),
        q("4. Tác giả ví những đóa hoa mai rung rinh trước gió với hình ảnh gì?"),
        q("5. Đặt câu với mỗi từ sau đây: rung rinh, rập rờn.")],
       listen(("hoa mai", "hoa đào", "ngọc bích"), ("mịn màng", "mượt mà", "phảng phất"), ("uyển chuyển", "rung rinh", "rập rờn"),
              ("thưa thớt", "đơm đặc", "phảng phất"), ("rập rờn", "rung rinh", "thơm lựng"), ("vàng muốt", "ngọc bích", "mịn màng")),
       images={"img_b266_hoa_mai_vangf": "Cành mai vàng uyển chuyển vươn lên, những bông hoa năm cánh vàng muốt xòe nở, "
                                         "nụ xanh xen giữa lá non, nền trời xuân nhạt"},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 267 — Bài 48. Một vài cảnh đẹp (Học thuộc lòng, tr.88–90)
lesson(267, [88, 89, 90],
       [picture("img_b267_mua_xuaan", "Cảnh mùa xuân: cỏ non xanh và cành lê trắng.", "mùa xuân"),
        title("Một vài cảnh đẹp", "Học thuộc lòng"),
        *sentences("Cảnh mùa xuân:", "Cỏ non xanh rợn chân trời", "Cành lê trắng điểm một vài bông hoa.",
                   "Cảnh mùa hè:", "Dưới trăng quyên đã gọi hè", "Đầu tường lửa lựu lập lòe đâm bông.",
                   "Cảnh mùa thu:", "Long lanh đáy nước in trời", "Thành xây khói biếc, non phơi bóng vàng."),
        passage("poem", "Truyện Kiều", breaks=[3, 6]),
        *glossary("Quyên: chim cuốc.", "Lửa lựu: hoa lựu đỏ như màu lửa."),
        q("1. Thơ lục bát gồm hai câu đi liền nhau từng đôi một. Em đếm xem câu trên có mấy tiếng, câu dưới có mấy "
          "tiếng. Tiếng thứ 6 của câu trên vần với tiếng thứ mấy của câu dưới?", marker="?"),
        q("2. Em hãy tìm những nét đẹp của cảnh mùa xuân được tả trong hai câu đầu."),
        q("3. Cảnh mùa hè có gì nổi bật? (âm thanh, màu sắc)"),
        q("4. Câu \"Long lanh đáy nước in trời\" cho em biết bầu trời và mặt nước (sông, hồ...) về mùa thu như thế nào?"),
        memorize()],
       listen(("cỏ non", "cành lê", "lửa lựu"), ("long lanh", "lập lòe", "chân trời"), ("chim quyên", "hoa lựu", "cành lê"),
              ("khói biếc", "bóng vàng", "đáy nước"), ("lập lòe", "long lanh", "đâm bông"), ("mùa thu", "mùa hè", "mùa xuân")),
       images={"img_b267_mua_xuaan": "Cảnh mùa xuân: bãi cỏ non xanh trải tới chân trời, cành lê khẳng khiu điểm vài bông "
                                     "hoa trắng, núi xa mờ"},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL),
              ("khac_sach", "Sách in ba tranh (xuân, hè, thu); app dùng một tranh cảnh mùa xuân.")])

# 268 — Bài 49. Vùng mỏ (tr.90–91)
POEM49 = ["Quê em vàng đen quý", "Nơi vịnh Hạ Long xanh", "Núi Bài Thơ như tranh", "Nghiêng nghiêng nhìn sóng biếc.",
          "Suối than ngày chảy miết", "Còi tàu vang khơi xa", "Buồm căng, thuyền nặng cá", "Ấm no theo về nhà."]
lesson(268, [90, 91],
       [picture(MO_IMG, "Thuyền buồm chở cá về bên vùng mỏ.", "vùng mỏ"),
        title("Vùng mỏ"),
        *sentences(*POEM49),
        passage("poem", "PHẠM THỊ LIÊN", breaks=[4]),
        *glossary("Vàng đen: ý nói than mỏ quý như vàng.",
                 "Núi Bài Thơ: một hòn núi đẹp ở sát cảng Hòn Gai thuộc tỉnh Quảng Ninh."),
        q("1. Tại sao tác giả ví than với vàng?", marker="?"),
        q("2. Nêu những vẻ đẹp của vùng mỏ (khổ thơ 1)."),
        q("3. Núi Bài Thơ được ví như \"bức tranh\" ý nói gì?"),
        choose("4. Tìm những câu thơ nói lên cảnh giàu có của vùng mỏ (khổ thơ 2).", POEM49[4:], [0, 2, 3]),
        q("5. Cảnh hoạt động náo nhiệt ở vùng mỏ được tả bằng những từ ngữ nào?")],
       listen(("vàng đen", "suối than", "còi tàu"), ("vịnh Hạ Long", "núi Bài Thơ", "sóng biếc"), ("chảy miết", "nghiêng nghiêng", "ấm no"),
              ("buồm căng", "nặng cá", "khơi xa"), ("ấm no", "chảy miết", "vàng đen"), ("sóng biếc", "suối than", "buồm căng")),
       images={MO_IMG: MO_DESC},
       notes=[("khac_sach", KS_ORAL)],
       review=[("part1[15]", "đáp án câu thơ nói cảnh giàu có do app soạn")])

# 269 — Bài 50. Chim én tìm tổ (Bài đọc thêm, tr.91–92; sách không có tranh)
lesson(269, [91, 92],
       [title("Chim én tìm tổ", "Bài đọc thêm"),
        *sentences("Chim én ngày nào", "Trên mái tranh nhà ta xây tổ", "Sáng nay trở về bâng khuâng cánh vỗ",
                   "Vù sang cây sấu", "Vút lên cây mai", "Bay rồi lại đậu", "Đậu rồi lại bay", "Nghĩ gì chim hỡi?",
                   "Chim bay lên mái ngói", "Xanh cửa, trắng tường", "Ríu rít bên nhau xây tổ mới."),
        passage("poem", "NÔNG QUỐC CHẤN", breaks=[8])],
       listen(("chim én", "mái tranh", "mái ngói"), ("bâng khuâng", "ríu rít", "xây tổ"), ("cây sấu", "cây mai", "mái tranh"),
              ("ríu rít", "bâng khuâng", "cánh vỗ"), ("xây tổ", "tổ mới", "trắng tường"), ("mái ngói", "chim én", "cây sấu")))

# 270 — Chính tả tuần 13 (tr.92)
lesson(270, [92],
       [title("Chính tả: Hoa mai vàng", "Nghe đọc"),
        title("Bài viết: \"Hoa mai... bay ra\".", "Phần này con nghe bố mẹ đọc rồi viết vào vở."),
        words("muốt", "mượt mà", "phảng phất", "nở", "ánh"),
        combine("mượt", "chải", "bóng", at="before"),
        fill(["màng", "màn"], ("mịn màng", "màng", "màng"), ("mơ màng", "màng", "màng"), ("vải màn", "màn", "màn")),
        fill(["phảng", "phản"], ("phảng phất", "phảng", "phảng"), ("tấm phản gỗ", "phản", "phản")),
        title("Tập chép: Lũy tre", "Nhìn sách"),
        title("Bài chép: 3 khổ thơ đầu.", "Phần này con chép vào vở cùng bố mẹ."),
        words("lũy", "suốt", "râm", "sao", "bần thần", "mỗi"),
        choose("Trong các chữ tre, đêm, thép, ngày: chữ nào có thể ghép với chữ lũy?", ["tre", "đêm", "thép", "ngày"], [0]),
        choose("Chữ nào có thể ghép với chữ suốt?", ["tre", "đêm", "thép", "ngày"], [1, 3]),
        fill(["sao", "xao"], ("ngôi sao", "sao", "sao"), ("xôn xao", "xao", "xao"), ("vì sao", "sao", "sao"),
             ("lao xao", "xao", "xao")),
        fill(["ân", "âng"], ("cái cân", "cân", "ân"), ("vâng lời", "vâng", "âng"))],
       listen(("chải mượt", "bóng mượt", "mịn màng"), ("phảng phất", "tấm phản", "vải màn"), ("lũy tre", "suốt đêm", "suốt ngày"),
              ("xôn xao", "ngôi sao", "lao xao"), ("vâng lời", "bần thần", "râm"), ("mơ màng", "mượt mà", "vàng muốt")),
       notes=[("khac_sach", KS_WRITE), ("khac_sach", "Ghép chữ, đố chữ, điền chỗ trống làm bằng chạm hoặc kéo thẻ.")],
       review=[("part1[3]", "cách ghép do app chọn: chải mượt, bóng mượt"), ("part1[4]", "đáp án màng/màn"),
               ("part1[5]", "đáp án phảng/phản"), ("part1[9]", "đáp án do app soạn: lũy tre"),
               ("part1[10]", "đáp án do app soạn: suốt đêm, suốt ngày"), ("part1[11]", "đáp án sao/xao"),
               ("part1[12]", "đáp án ân/âng: cái cân, vâng lời")])

# 271 — Từ ngữ: Ôn tập (tr.92–93)
lesson(271, [92, 93],
       [title("Từ ngữ: Ôn tập"),
        q("1. Tổ quốc là gì? Tổ quốc ta tên là gì?"),
        q("2. Thành phố lớn là trung tâm văn hóa chính trị của một nước được gọi là gì? Thủ đô của nước ta tên là gì?"),
        q("3. Đặt câu với các từ: thành phố, nông thôn, đường phố, đường làng, cánh đồng, thửa ruộng."),
        title("4. Điền từ (quê hương, quê quán) vào câu sau đây"),
        fill_passage(["Hai anh bộ đội ấy [quê quán] khác nhau, nhưng cả hai đều yêu [quê hương] tha thiết."],
                     bank=["quê hương", "quê quán"])],
       listen(("Tổ quốc", "thủ đô", "thành phố"), ("nông thôn", "thành phố", "đường phố"), ("quê hương", "quê quán", "đường làng"),
              ("quê quán", "quê hương", "cánh đồng"), ("cánh đồng", "thửa ruộng", "nông thôn"), ("thủ đô", "Tổ quốc", "đường làng")),
       notes=[("khac_sach", KS_ORAL)],
       review=[("part1[5]", "đáp án điền từ do app soạn")])

# 272 — Ngữ pháp: Tiếng và từ (tr.93)
lesson(272, [93],
       [title("Ngữ pháp: Tiếng và từ"),
        *rule("Từ thì phải có nghĩa.", "Tiếng có lúc không có nghĩa.", "Có từ chỉ có một tiếng.",
             "Lại có từ gồm hai, ba tiếng."),
        *rule("Ví dụ: Long lanh đáy nước in trời.", "Long lanh là từ hai tiếng.",
             "đáy, nước, in và trời là những từ một tiếng."),
        q("1. Tìm từ trong ba câu sau:",
          lines=["Nụ hoa xanh màu ngọc bích.", "Đồng lúa rộng mênh mông.", "Tổ quốc ta vô cùng tươi đẹp."]),
        q("2. Tìm một từ hai tiếng và dùng từ đó đặt câu.")],
       listen(("long lanh", "mênh mông", "ngọc bích"), ("ngọc bích", "tươi đẹp", "đồng lúa"), ("mênh mông", "vô cùng", "long lanh"),
              ("tươi đẹp", "ngọc bích", "Tổ quốc"), ("vô cùng", "mênh mông", "tươi đẹp"), ("đồng lúa", "nụ hoa", "Tổ quốc")),
       notes=[("khac_sach", KS_ORAL)])

# 273 — Tập làm văn: Quan sát tranh và trả lời câu hỏi — Vùng mỏ (tr.93)
lesson(273, [93],
       [title("Tập làm văn: Quan sát tranh và trả lời câu hỏi"),
        title("Đề bài: Vùng mỏ.", "Xem tranh ở bài Vùng mỏ."),
        picture(MO_IMG, "Con nhìn kĩ tranh vùng mỏ nhé.", "vùng mỏ"),
        q("1. Đây là bức tranh vẽ vùng mỏ Hòn Gai, em thấy trong tranh có những gì?"),
        q("2. Trên mặt biển, những chiếc tàu và thuyền đang làm gì?"),
        q("3. Ở vùng mỏ, công nhân khai thác những gì để làm giàu cho Tổ quốc?"),
        q("4. Nhìn vào tranh, em hãy đặt thêm một câu hỏi và trả lời.")],
       listen(("vùng mỏ", "mặt biển", "thuyền buồm"), ("thuyền buồm", "vùng mỏ", "núi đá"), ("núi đá", "thuyền buồm", "công nhân"),
              ("công nhân", "núi đá", "khai thác"), ("khai thác", "công nhân", "mặt biển"), ("mặt biển", "khai thác", "vùng mỏ")),
       images={MO_IMG: MO_DESC},
       notes=[("khac_sach", "Tập làm văn quan sát tranh: app dùng lại tranh bài Vùng mỏ; bé trả lời miệng.")],
       review=[("part1[2]", "lời dẫn tranh do app soạn")])
