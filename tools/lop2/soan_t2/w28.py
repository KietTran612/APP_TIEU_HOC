"""Tuần 28 (mục 387–394), tr.76–82, ảnh 039–042."""
from l2t2lib import *

ALPHABET = ["a", "ă", "â", "b", "c", "d", "đ", "e", "ê", "g", "h", "i", "k", "l", "m", "n", "o", "ô", "ơ", "p", "q", "r",
            "s", "t", "u", "ư", "v", "x", "y"]

# 387 — Bài 43. Anh thợ đốt lò (tr.76–77)
THO_LO = ["Cửa lò hé mở", "Than rơi, than rơi...", "Anh thợ lò ơi!", "Bàn tay nóng ấm", "Chuyền vào tay tôi",
          "Và màu lửa sáng", "Trong mắt anh cười.", "Anh thợ lò ơi!", "Cửa lò anh đứng", "Như cửa mặt trời",
          "Bóng anh trải rộng", "Như đám mây trôi.", "Lửa vàng làm nắng", "Bóng anh tỏa dài", "Nhịp tay đều đặn",
          "Than rơi, than rơi..."]
lesson(387, [76, 77],
       [picture(img(387, "thợ đốt lò"), "Các anh thợ đốt lò làm việc bên cửa lò.", "thợ đốt lò"),
        title("Anh thợ đốt lò"),
        *sentences(*THO_LO),
        passage("poem", "VÕ THANH AN", breaks=[7]),
        q("1. Anh thợ đốt lò đang đứng làm việc ở đâu? Tại sao tác giả lại ví cửa lò như \"cửa mặt trời\"?", marker="?"),
        q("2. Bàn tay anh thợ đốt lò ra sao? \"Màu lửa sáng\" làm cho mắt anh đẹp như thế nào?"),
        q("*3. Em hãy tìm những câu tả hình dáng, cử chỉ khỏe, đẹp của anh thợ đốt lò."),
        q("4. Tìm từ cùng nghĩa với từ thợ."),
        q("5. Em đọc lại thong thả 2 câu đầu và 2 câu cuối của bài thơ.")],
       listen(("cửa lò", "than rơi", "mặt trời"), ("than rơi", "cửa lò", "đám mây"), ("mặt trời", "đám mây", "lửa vàng"),
              ("lửa vàng", "mặt trời", "bàn tay"), ("nóng ấm", "đều đặn", "tỏa dài"), ("đều đặn", "nóng ấm", "trải rộng")),
       images={img(387, "thợ đốt lò"): "Sân nhà máy có ống khói và bồn chứa lớn: hai anh thợ đốt lò mặc áo xanh, đội mũ, "
                                       "cầm xẻng dài đứng trước cửa lò đang mở, ánh lửa vàng hắt ra; một anh thợ khác "
                                       "đứng phía sau đưa tay che mắt nhìn"},
       notes=[("khac_sach", KS_ORAL)])

# 388 — Bài 44. Lên cao (Học thuộc lòng, tr.77–78)
lesson(388, [77, 78],
       [picture(img(388, "thợ điện"), "Anh thợ điện trèo lên cột điện mắc dây.", "thợ điện"),
        title("Lên cao", "Học thuộc lòng"),
        *sentences("Kìa anh thợ điện lên cao!", "Chào anh, gió hát rì rào hàng dương.", "Líu lo, chim hót yêu thương",
                   "Từng đôi sà xuống, lượn vờn quanh anh.", "Trời xanh xanh, đất xanh xanh",
                   "Bóng anh đứng giữa mông mênh đất trời.", "Mắc muôn dòng điện sáng ngời",
                   "Về nơi xóm vắng, về nơi thị thành.", "Mai sau em lớn bằng anh", "Em đi mắc điện sáng quanh địa cầu."),
        passage("poem", "VÕ VĂN TRỰC", breaks=[2, 4, 6, 8]),
        q("1. Anh thợ điện trèo lên cột điện để làm gì?", marker="?"),
        q("2. Gió và chim rất mến anh thợ điện. Em hãy tìm những từ ngữ cho biết điều đó."),
        q("3. Bóng dáng anh thợ điện đứng trên cao trông rất đẹp. Những câu thơ nào tả vẻ đẹp ấy của anh?"),
        q("*4. Tìm một số từ láy tả tiếng động của gió (ví dụ: rì rào); tiếng hót của chim (ví dụ: líu lo)."),
        memorize()],
       listen(("thợ điện", "hàng dương", "dòng điện"), ("hàng dương", "thợ điện", "địa cầu"), ("rì rào", "líu lo", "mông mênh"),
              ("líu lo", "rì rào", "sáng ngời"), ("xóm vắng", "thị thành", "hàng dương"), ("địa cầu", "dòng điện", "xóm vắng")),
       images={img(388, "thợ điện"): "Cánh đồng làng có hàng cột điện chạy dài, xa xa máy cày và mái nhà: anh thợ điện "
                                     "đội mũ, đeo dây an toàn, trèo lên cột điện cao mắc dây; bên đường có hàng cây "
                                     "và mấy chú chim bay lượn quanh"},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)])

# 389 — Bài 45. Màu men cánh gián (tr.79–80)
lesson(389, [79, 80],
       [picture(img(389, "lọ mực"), "Chú Nguyên tặng Cương lọ mực màu men cánh gián.", "lọ mực"),
        title("Màu men cánh gián"),
        *prose("ĐỖ VĂN",
               ["Chú Nguyên ở bộ đội chuyển về, làm trong nhà máy sứ.", "Cương rất thân với chú.",
                "Một hôm, chú mang về hai gói: đất và đá.", "Cương múc nước giúp chú lọc đất.",
                "Cương giúp chú nghiền đá."],
               ["Mấy hôm sau, Cương lại đến chơi nhà chú.", "Vừa thấy Cương, chú đã reo to:"],
               ["- Vào đây, Cương! Chú đợi mãi!"],
               ["Chú cho Cương một lọ mực loe miệng màu men cánh gián mới nung | và nói hể hả:"],
               ["- Nước men này là do chú cháu mình chế ra hôm ấy đấy!"],
               ["Cương há mồm, ngạc nhiên.", "Cương ngắm mãi màu men.", "Thoạt nhìn, nước men màu nâu.",
                "Ngắm lâu, lại thấy phảng phất sắc tím pha đỏ trông thật thích mắt.",
                "Cương chợt ngước mắt nhìn chú Nguyên, một con người xương xương, | "
                "lúc nào cũng say mê ngẫm nghĩ để tìm ra những nước men đẹp."]),
        q("1. Chú Nguyên làm việc ở đâu? Cương giúp chú lọc đất, nghiền đá, để làm gì?", marker="?"),
        q("2. Chú Nguyên tặng Cương vật gì? Tại sao Cương lại há mồm ngạc nhiên?"),
        q("3. Màu men cánh gián của lọ mực mới nung đẹp như thế nào?"),
        q("4. Chú Nguyên say mê làm việc gì?"),
        q("*5. Tìm trong bài 2 danh từ riêng chỉ tên người và xếp 2 danh từ riêng đó theo thứ tự bảng chữ cái.")],
       listen(("lọ mực", "nhà máy sứ", "nước men"), ("nước men", "lọ mực", "cánh gián"), ("cánh gián", "nước men", "nghiền đá"),
              ("nghiền đá", "lọc đất", "lọ mực"), ("hể hả", "ngạc nhiên", "phảng phất"), ("phảng phất", "hể hả", "say mê")),
       images={img(389, "lọ mực"): "Trong gian nhà có tủ bát và bàn nước: chú bộ đội cũ đội mũ lưỡi trai ngồi trên ghế "
                                   "đẩu, trao cho cậu bé Cương một lọ mực sứ loe miệng màu men nâu tím; trên bàn có "
                                   "phích nước và ấm chén, chú mèo nằm dưới chân"},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 390 — Bài 46. Bác thợ xây vui tính (Bài đọc thêm, tr.80–81; sách không có tranh)
lesson(390, [80, 81],
       [title("Bác thợ xây vui tính", "Bài đọc thêm"),
        *prose("NGUYỄN NHO",
               ["Trời gần đứng bóng, Hòe đang rảo bước trên vỉa hè.", "Bỗng một tiếng gọi giật lại:"],
               ["- Này, cậu bé, lại đây!"],
               ["Hòe vội quay lại.", "Bác thợ xây quen thuộc đang tươi cười hồ hởi.",
                "Khuôn mặt tráng nắng còn đọng mấy vệt mồ hôi khô trắng."],
               ["- Đói chưa? Đây, ăn đi."],
               ["Bác thợ dúi vào tay Hòe một mẩu bánh xốp | còn nóng hổi lẫn cả mùi nồng của vôi.",
                "Hòe nhoẻn miệng cười hồn nhiên.", "Bác vỗ vỗ vào vai Hòe cười ha hả:"],
               ["- Cháu thích cái nghề vôi vữa này không đấy?"],
               ["- Cháu rất thích ạ."],
               ["- Khà khà... tốt lắm!"],
               ["Bác thợ vừa trò chuyện vừa xúc hồ trát thoăn thoắt.", "Chiếc bay trong tay bác loang loáng.",
                "Bức thành cao lên trông thấy.", "Hòe mải xem bác thợ làm, quên cả đói."])],
       listen(("thợ xây", "vỉa hè", "bánh xốp"), ("bánh xốp", "thợ xây", "vôi vữa"), ("vôi vữa", "bánh xốp", "chiếc bay"),
              ("chiếc bay", "vôi vữa", "vỉa hè"), ("hồ hởi", "thoăn thoắt", "loang loáng"),
              ("loang loáng", "hồ hởi", "nóng hổi")),
       notes=[("sach", "Sách in \"Khuôn mặt tráng nắng\" (có thể là lỗi in của \"rám nắng\"); app chép như sách.")],
       review=[("part1[6]", "sách in \"tráng nắng\" (có thể là \"rám nắng\"): chủ dự án xem giữ hay sửa")])

# 391 — Chính tả tuần 28 (tr.81)
lesson(391, [81],
       [title("Chính tả: Anh thợ đốt lò", "Nghe đọc"),
        title("Bài viết: Cả bài.", "Phần này con viết vào vở cùng bố mẹ."),
        words("chuyền", "tỏa", "màu", "trải", "cười", "đều đặn", "lửa"),
        combine_mixed("chuyền", ("dây", "before"), ("tay", "after")),
        combine("tỏa", "khói", "sáng"),
        fill(["màu", "mầu"], ("màu xanh", "màu", "màu"), ("pha màu", "màu", "màu"), ("bà tiên có phép mầu", "mầu", "mầu")),
        fill(["đều", "điều"], ("đều đặn", "đều", "đều"), ("đều tay", "đều", "đều"), ("điều tốt", "điều", "điều"),
             ("điều lệ", "điều", "điều")),
        find("c) Viết những chữ có dấu hỏi trong bài.", {"tone": ["hỏi"]}, text=THO_LO),
        title("Chính tả: Màu men cánh gián", "So sánh"),
        *sentences("Chú Nguyên cho Cương một lọ mực loe miệng mới nung.", "Cương ngạc nhiên ngắm mãi màu men.",
                   "Nước men màu nâu, phảng phất sắc tím pha đỏ như màu cánh gián."),
        title("Bài viết: ba câu trên.", "Phần này con viết vào vở cùng bố mẹ."),
        words("Nguyên", "loe", "ngắm", "gián", "chú", "lọ", "nung", "sắc", "miệng", "ngạc", "phảng phất", "mãi"),
        title("Phát âm phân biệt các cặp từ ngữ sau"),
        words("chú bác", "trú mưa", "màu sắc", "cái xắc"),
        words("phảng phất", "phản động", "mãi mãi", "mải miết"),
        words("con gián", "dán tem thư"),
        q("b) Thêm chữ thích hợp vào các cặp từ sau.", lines=["... loe, leo ...", "ngắm...., lửa... ngắm."])],
       listen(("dây chuyền", "chuyền tay", "tỏa khói"), ("tỏa sáng", "màu xanh", "phép mầu"), ("đều đặn", "điều tốt", "điều lệ"),
              ("chú bác", "trú mưa", "cái xắc"), ("mãi mãi", "mải miết", "phảng phất"), ("con gián", "dán tem", "màu sắc")),
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Ghép chữ, điền chỗ trống, tìm chữ có dấu hỏi làm bằng chạm thẻ, chạm chữ; thêm chữ: bé nói "
                            "cùng bố mẹ; cặp từ so sánh thành thẻ chạm để nghe. Dấu \"≠\" thay bằng dấu phẩy.")],
       review=[("part1[3]", "ghép \"dây chuyền\" (trước), \"chuyền tay\" (sau) do app chọn"),
               ("part1[4]", "ghép \"tỏa khói\", \"tỏa sáng\" do app chọn"),
               ("part1[5]", "đáp án màu/mầu theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[6]", "đáp án đều/điều theo chính tả chuẩn (sách in \"dều hay điều\", không in đáp án)")])

# 392 — Từ ngữ: Công nghiệp (tr.82)
lesson(392, [82],
       [title("Từ ngữ: Công nghiệp"),
        title("Những từ ngữ cần ghi nhớ"),
        words("thợ điện", "thợ đốt lò", "thợ xây", "nhà máy", "công trường", "công nhân", "kĩ sư"),
        words("kinh nghiệm", "sáng kiến"),
        title("Bài tập: Điền từ thích hợp vào các chỗ trống"),
        fill_passage(["Khu nhà tập thể nơi em ở có ba bác [công nhân|nhà máy|sáng kiến] ở cạnh nhà nhau.",
                      "Bác Trực là [thợ điện|kĩ sư|công trường] và bác An là [thợ đốt lò|kinh nghiệm|nhà máy] "
                      "cùng làm việc ở nhà máy điện thành phố.",
                      "Còn bác Nho là [thợ xây|nhà máy|sáng kiến] ở công trường xây dựng khu nam thành phố.",
                      "Tuy người thì làm việc ở [nhà máy|thợ xây|kĩ sư], người thì ở [công trường|thợ điện|sáng kiến], "
                      "nhưng các bác rất thân với nhau.",
                      "Cả ba bác đều là thợ giỏi có nhiều [sáng kiến|công trường|thợ xây] có giá trị.",
                      "Bố em tuy là [kĩ sư|thợ đốt lò|nhà máy] nhưng cũng học hỏi được ở các bác rất nhiều "
                      "[kinh nghiệm|công nhân|thợ điện]."]),
        q("2. Nêu một số nghề thợ khác nữa ở các nhà máy, công trường mà em biết.")],
       listen(("thợ điện", "thợ xây", "thợ đốt lò"), ("thợ xây", "thợ điện", "công nhân"), ("nhà máy", "công trường", "kĩ sư"),
              ("công trường", "nhà máy", "sáng kiến"), ("kĩ sư", "công nhân", "kinh nghiệm"), ("sáng kiến", "kinh nghiệm", "nhà máy")),
       notes=[("khac_sach", "Điền từ: mỗi chỗ trống 3 thẻ do app chọn trong các từ ngữ cần ghi nhớ, tránh hai từ cùng "
                            "đúng; đáp án do app soạn."),
              ("khac_sach", KS_ORAL)],
       review=[("part1[5]", "đáp án và thẻ chọn do app soạn: công nhân, thợ điện, thợ đốt lò, thợ xây, nhà máy, "
                            "công trường, sáng kiến, kĩ sư, kinh nghiệm (bác Trực, An, Nho là tên tác giả các bài đọc tuần 28)")])

# 393 — Ngữ pháp: Tập xếp tên người theo thứ tự bảng chữ cái (tr.82)
lesson(393, [82],
       [title("Ngữ pháp: Tập xếp tên người theo thứ tự bảng chữ cái"),
        {"type": "letter_pairs", "letters": ALPHABET},
        q("1. Đọc lại 29 chữ cái theo đúng thứ tự bảng chữ cái."),
        q("2. Xếp tên các bạn sau đây theo đúng thứ tự bảng chữ cái:", lines=["Hưng, Vượng, Thịnh, Minh, Lai"]),
        *rule("Nếu tên người có cùng chữ cái đầu thì căn cứ vào chữ thứ 2 để xếp thứ tự trước sau.",
              "Ví dụ: Hà, Hòa, Hùng.", "Chữ thứ 2 trong ba người trên là a, o, u."),
        *rule("Nếu tên người có 2 chữ cái đầu giống nhau thì căn cứ vào chữ thứ 3 để xếp thứ tự:",
              "Dục xếp trước Dung (vì chữ c trước chữ n)."),
        q("3. Xếp tên các bạn sau đây theo thứ tự bảng chữ cái:",
          lines=["Định, An, Khả, Phượng, Mạnh,", "Điện, Kính, Phụng, Gái, Minh."])],
       listen(("chữ cái", "thứ tự", "bảng chữ cái"), ("thứ tự", "chữ cái", "tên người"), ("tên người", "thứ tự", "chữ cái"),
              ("Hà", "Hòa", "Hùng"), ("Hòa", "Hùng", "Hà"), ("Hùng", "Hà", "Hòa")),
       notes=[("khac_sach", "Bảng chữ cái hiện lại để bé nhìn. " + KS_XEP_TEN)])

# 394 — Tập làm văn: Dùng từ – đặt câu (tr.82)
lesson(394, [82],
       [title("Tập làm văn: Dùng từ – đặt câu"),
        title("Đề bài: Em hãy dùng mỗi từ ngữ sau đây đặt thành một câu nói về chú công nhân điện:"),
        words("thợ điện", "yêu thương", "sáng ngời", "dây điện", "mắc điện"),
        q("Em hãy đặt câu với mỗi từ ngữ trên.")],
       listen(("thợ điện", "dây điện", "mắc điện"), ("yêu thương", "sáng ngời", "thợ điện"), ("sáng ngời", "yêu thương", "dây điện"),
              ("dây điện", "mắc điện", "sáng ngời"), ("mắc điện", "thợ điện", "yêu thương"), ("cột điện", "dây điện", "thợ điện")),
       notes=[("khac_sach", KS_DAT_CAU),
              ("khac_sach", "Câu \"Em hãy đặt câu với mỗi từ ngữ trên\" do app thêm để nhắc bé (trang chỉ in đề bài).")],
       review=[("part1[3]", "câu nhắc đặt câu do app thêm")])
print("tuần 28 xong")
