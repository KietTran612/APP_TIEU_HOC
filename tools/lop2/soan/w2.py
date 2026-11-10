"""Tuần 2 (mục 180–187), tr.12–17, ảnh 007–009."""
from l2lib import *

# 180 — Bài 5. Ngôi trường mới (tr.12–13)
lesson(180, [12, 13],
       [picture("img_b180_ngoi_truwowngf_mowis", "Đây là ngôi trường mới.", "ngôi trường"),
        title("Ngôi trường mới"),
        *sentences("Trường mới xây trên nền ngôi trường lợp lá cũ.",
                   "Nhìn từ xa, những mảng tường vàng,",
                   "ngói đỏ như những cánh hoa lấp ló trong cây.",
                   "Em bước vào lớp vừa bỡ ngỡ vừa thấy quen thân.",
                   "Tường vôi trắng, cánh cửa xanh,",
                   "bàn ghế gỗ xoan đào nổi vân như lụa.",
                   "Em thấy tất cả đều sáng lên và thơm trong nắng mùa thu.",
                   "Dưới mái trường mới, sao tiếng trống rung động kéo dài!",
                   "Tiếng cô giáo trang nghiêm mà ấm áp.",
                   "Tiếng đọc bài của em cũng vang vang đến lạ!",
                   "Em nhìn ai cũng thấy thân thương.",
                   "Cả đến chiếc thước kẻ, chiếc bút chì,",
                   "sao cũng đáng yêu đến thế!"),
        passage("prose", "NGÔ QUÂN MIỆN", breaks=[3, 7]),
        q("1. Ngôi trường tả trong bài có gì đẹp?", marker="?"),
        q("2. Câu nào trong bài tả rõ những nét đẹp của lớp học?"),
        q("3. Những điều gì đã làm cho em học sinh cảm động dưới mái trường mới?"),
        q("4. Em đã làm những gì để trường lớp của em thêm sạch đẹp?")],
       listen(("ngói đỏ", "tường vàng", "cánh hoa"), ("bỡ ngỡ", "quen thân", "ấm áp"),
              ("gỗ xoan", "bàn ghế", "thước kẻ"), ("trang nghiêm", "thân thương", "vang vang"),
              ("thước kẻ", "bút chì", "gỗ xoan"), ("ấm áp", "bỡ ngỡ", "nắng mùa thu")),
       images={"img_b180_ngoi_truwowngf_mowis": "Ngôi trường mới tường vàng ngói đỏ, sân rộng có cây bàng lớn, cột cờ "
                                                "có lá cờ đỏ sao vàng, vài bạn học sinh đứng trước cửa lớp (không có chữ)"},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 181 — Bài 6. Đi học (Học thuộc lòng, tr.13–14)
POEM6 = ["Hôm qua em tới trường", "Mẹ dắt tay từng bước.", "Hôm nay mẹ lên nương", "Một mình em tới lớp.",
         "Trường của em be bé", "Nằm lặng giữa rừng cây", "Cô giáo em tre trẻ", "Dạy em hát rất hay.",
         "Hương rừng thơm đồi vắng,", "Nước suối trong thầm thì...", "Cọ xòe ô che nắng", "Râm mát đường em đi."]
lesson(181, [13, 14],
       [picture("img_b181_ddi_hocj", "Các bạn nhỏ miền núi đi học.", "đi học"),
        title("Đi học", "Học thuộc lòng"),
        *sentences(*POEM6),
        passage("poem", "MINH CHÍNH", breaks=[4, 8]),
        q("1. Bạn học sinh nói trong bài ở miền xuôi hay miền núi? Những từ nào cho em biết điều đó?", marker="?"),
        q("2. Bạn rất quý cô giáo. Những câu thơ nào nói lên ý đó?"),
        q("3. Con đường đi đến trường có gì đẹp?"),
        find("4. Tìm những tiếng cùng vần ở cuối các dòng thơ.",
             {"word": ["trường", "nương", "bé", "trẻ", "vắng", "nắng", "thì", "đi"]}),
        memorize()],
       listen(("lên nương", "rừng cây", "suối trong"), ("rừng cây", "đồi vắng", "lên nương"),
              ("tre trẻ", "be bé", "thầm thì"), ("thầm thì", "râm mát", "tre trẻ"),
              ("râm mát", "hương rừng", "be bé"), ("suối trong", "đồi vắng", "râm mát")),
       images={"img_b181_ddi_hocj": "Con đường mòn ven suối dưới tán cọ xòe ô, ba bạn nhỏ miền núi mặc áo thổ cẩm, "
                                    "đeo túi vải đi học; xa xa là ngôi trường nhỏ giữa rừng cây"},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)],
       review=[("part1[18]", "tiếng cùng vần cuối dòng do app chọn: trường–nương, bé–trẻ, vắng–nắng, thì–đi")])

# 182 — Bài 7. Đẹp mà không đẹp (tr.14–15)
lesson(182, [14, 15],
       [picture("img_b182_vex_nguwaj", "Hùng vẽ con ngựa lên tường.", "con ngựa"),
        title("Đẹp mà không đẹp"),
        *sentences("Thấy bác Thành đi qua, Hùng liền gọi:",
                   "- Bác Thành ơi, bác xem con ngựa của cháu vẽ có đẹp không?",
                   "Trên bức tường trắng, hiện ra những nét than đen",
                   "vẽ hình một con ngựa đang leo núi.",
                   "Bác Thành nhìn bức vẽ rồi trả lời:",
                   "- Cháu vẽ đẹp đấy, nhưng còn có cái không đẹp!",
                   "Hùng vội hỏi:",
                   "- Cái nào không đẹp, hở bác?",
                   "Bác Thành bảo:",
                   "- Cái không đẹp là bức tường của nhà trường đã bị vẽ bẩn, cháu ạ!"),
        passage("prose", "LỤC VĂN VẬN", breaks=[1, 2, 4, 5, 6, 7, 8, 9]),
        q("1. Hùng vẽ gì trên tường?", marker="?"),
        q("2. Tại sao bác Thành vừa khen lại vừa chê? Khen gì? Chê gì?"),
        q("3. Em hãy tìm từ trái nghĩa với từ: đẹp, bẩn, trắng.")],
       listen(("con ngựa", "bức tường", "nét than"), ("bức tường", "con ngựa", "leo núi"),
              ("leo núi", "vẽ bẩn", "trả lời"), ("nét than", "bức vẽ", "con ngựa"),
              ("vẽ bẩn", "leo núi", "bức tường"), ("trả lời", "vội hỏi", "nét than")),
       images={"img_b182_vex_nguwaj": "Hành lang lớp học: trên bức tường trắng có hình con ngựa vẽ bằng nét than đen, "
                                      "cậu bé Hùng đứng cạnh tường, một bác trung niên mặc áo xanh đứng nhìn bức vẽ, "
                                      "chiếc cặp sách để dưới đất"},
       notes=[("khac_sach", KS_ORAL)])

# 183 — Bài 8. Cô giáo với mùa thu (Bài đọc thêm, tr.16; sách không có tranh)
lesson(183, [16],
       [title("Cô giáo với mùa thu", "Bài đọc thêm"),
        *sentences("Cô giáo em", "Hiền như cô Tấm", "Giọng cô đầm ấm", "Như lời mẹ ru.",
                   "Cô giáo đưa mùa thu", "Đến với những quả vàng chín mọng.", "Một mùa thu hi vọng",
                   "Tiếng chim ca ríu rít sân trường."),
        passage("poem", "VŨ HẠNH THẮM", breaks=[4])],
       listen(("cô Tấm", "lời mẹ", "mùa thu"), ("đầm ấm", "ríu rít", "chín mọng"),
              ("chín mọng", "hi vọng", "đầm ấm"), ("hi vọng", "chín mọng", "sân trường"),
              ("ríu rít", "đầm ấm", "hi vọng"), ("sân trường", "mùa thu", "lời mẹ")))

# 184 — Chính tả tuần 2 (tr.16–17)
NGOI_TRUONG = ["Trường mới xây trên nền ngôi trường lợp lá cũ.",
               "Nhìn từ xa, những mảng tường vàng, ngói đỏ như những cánh hoa lấp ló trong cây.",
               "Em bước vào lớp vừa bỡ ngỡ vừa thấy quen thân.",
               "Tường vôi trắng, cánh cửa xanh, bàn ghế gỗ xoan đào nổi vân như lụa.",
               "Em thấy tất cả đều sáng lên và thơm trong nắng mùa thu."]
lesson(184, [16, 17],
       [title("Chính tả: Ngôi trường mới", "Nghe đọc"),
        title("Bài viết: \"Trường mới xây... nắng mùa thu\".", "Phần này con nghe bố mẹ đọc rồi viết vào vở."),
        words("ngôi trường", "xây", "mảng tường", "lấp ló", "gỗ xoan", "bỡ ngỡ"),
        fill(["s", "x"], ("xây trường", "xây", "x"), ("lát sân", "sân", "s"), ("thôn xã", "xã", "x"),
             ("hợp tác xã", "xã", "x"), ("lăn xả vào", "xả", "x")),
        find("Tìm trong bài chính tả những chữ có tr ở đầu.", {"onset": ["tr"]}, text=NGOI_TRUONG),
        find("Tìm trong bài chính tả những chữ có ng ở cuối.",
             {"word": ["trường", "những", "mảng", "tường", "vàng", "trong", "trắng", "sáng", "nắng"]}, text=NGOI_TRUONG),
        title("Chính tả: Cái trống trường em", "Trí nhớ"),
        title("Bài viết: 8 câu thơ cuối.", "Phần này con nhớ lại rồi viết vào vở."),
        words("lặng im", "giá", "giọng", "trống", "chúng", "nghiêng", "vang"),
        combine("giá", "trống", "gương"),
        combine("lặng", "im", "lẽ", "ngắt"),
        fill(["nghỉ", "nghĩ"], ("nghỉ ngơi", "nghỉ", "nghỉ"), ("nghĩ ngợi", "nghĩ", "nghĩ"),
             ("suy nghĩ", "nghĩ", "nghĩ"), ("nghỉ hè", "nghỉ", "nghỉ"))],
       listen(("ngôi trường", "mảng tường", "gỗ xoan"), ("lấp ló", "bỡ ngỡ", "lặng im"),
              ("giá trống", "giá gương", "lặng lẽ"), ("lặng ngắt", "lặng im", "nghiêng"),
              ("nghỉ ngơi", "suy nghĩ", "lấp ló"), ("bỡ ngỡ", "gỗ xoan", "giọng")),
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Điền chỗ trống, ghép chữ, tìm chữ trong bài làm bằng chạm hoặc kéo thẻ.")],
       review=[("part1[3]", "đáp án s/x theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[5]", "chữ có ng ở cuối do app chọn trong đoạn bài viết"),
               ("part1[11]", "đáp án nghỉ/nghĩ theo chính tả chuẩn (sách không in đáp án)")])

# 185 — Từ ngữ: Trường học (tr.17)
lesson(185, [17],
       [title("Từ ngữ: Trường học"),
        title("Những từ ngữ cần ghi nhớ"),
        words("ngôi trường", "ngói đỏ", "tường vàng", "lớp học", "bàn ghế", "sân trường", "vườn trường"),
        words("thân thương", "đầm ấm", "bảo vệ của công"),
        title("Bài tập"),
        q("Đặt câu với từ: ngôi trường, lớp học, thân thương, đầm ấm."),
        q("Tìm thêm những tiếng có thể ghép với các từ đỏ, thân.", lines=["Đỏ: đỏ thắm, ...", "Thân: thân thương, ..."])],
       listen(("sân trường", "vườn trường", "ngôi trường"), ("bàn ghế", "lớp học", "ngói đỏ"),
              ("đầm ấm", "thân thương", "tường vàng"), ("tường vàng", "ngói đỏ", "bàn ghế"),
              ("thân thương", "đầm ấm", "sân trường"), ("lớp học", "bàn ghế", "vườn trường")),
       notes=[("khac_sach", KS_ORAL)])

# 186 — Ngữ pháp: Câu (tiếp theo) (tr.17)
lesson(186, [17],
       [title("Ngữ pháp: Câu", "Tiếp theo"),
        choose("1. Dòng nào dưới đây viết đã thành câu?",
               ["Trường của em", "Lớp học của chúng em rất sáng sủa, sạch sẽ.", "Cô giáo em"], [1]),
        q("2. Em hãy viết tiếp vào vở những dòng chưa thành câu ở trên cho thành câu.",
          lines=["Trường của em", "Cô giáo em"]),
        q("3. Nói và viết không thành câu thì người khác có hiểu được không? "
          "Vậy muốn người khác hiểu thì nói và viết phải như thế nào?")],
       listen(("sáng sủa", "sạch sẽ", "lớp học"), ("sạch sẽ", "sáng sủa", "cô giáo"),
              ("lớp học", "trường", "cô giáo"), ("cô giáo", "lớp học", "sáng sủa"),
              ("trường", "lớp học", "sạch sẽ"), ("thành câu", "hiểu được", "sáng sủa")),
       notes=[("khac_sach", "Bé chạm vào dòng đã thành câu; đáp án do app soạn. Phần viết tiếp vào vở: "
                            "bé nói tiếp cho thành câu cùng bố mẹ.")],
       review=[("part1[1]", "đáp án dòng đã thành câu do app soạn: Lớp học của chúng em rất sáng sủa, sạch sẽ.")])

# 187 — Tập làm văn: Điền từ — Ngôi trường mới (tr.17)
lesson(187, [17],
       [title("Tập làm văn: Điền từ"),
        title("Đề bài: Ngôi trường mới.",
              "Em hãy chọn những từ ngữ sau đây để điền vào chỗ trống: lớp học, bàn ghế, ngôi trường, bảo vệ của công."),
        fill_passage(["Xã em vừa xây xong một [ngôi trường].",
                      "Trường của em có mười [lớp học].",
                      "Chúng em giữ gìn [bàn ghế] trong lớp.",
                      "Giữ gìn bàn ghế, không vẽ bẩn lên tường là [bảo vệ của công]."],
                     bank=["lớp học", "bàn ghế", "ngôi trường", "bảo vệ của công"])],
       listen(("ngôi trường", "lớp học", "bàn ghế"), ("lớp học", "ngôi trường", "giữ gìn"),
              ("bàn ghế", "bức tường", "lớp học"), ("giữ gìn", "vẽ bẩn", "xây xong"),
              ("vẽ bẩn", "giữ gìn", "bàn ghế"), ("xây xong", "ngôi trường", "vẽ bẩn")),
       notes=[("khac_sach", "Điền từ bằng chạm hoặc kéo thẻ từ vào chỗ trống; đáp án do app soạn.")],
       review=[("part1[2]", "đáp án điền từ do app soạn")])
