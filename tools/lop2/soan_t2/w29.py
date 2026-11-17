"""Tuần 29 (mục 395–402), tr.83–91, ảnh 042–046."""
from l2t2lib import *

# 395 — Bài 47. Cánh tay khổng lồ (tr.83–84)
CAN_TRUC = img(395, "cần trục")
CAN_TRUC_DESC = ("Bến cảng đông vui: chiếc cần trục cao vươn cánh tay sắt nhấc một thùng hàng lớn từ con tàu biển lên; "
                 "dưới bến có xe tải chở hàng, những kiện hàng xếp đống, vài chú công nhân nhỏ xíu đứng xa, "
                 "trên trời có hải âu bay")
CAN_TRUC_2 = ["Cái cánh tay ấy vươn lên, sừng sững và chuyển động rất chậm, rất chậm.",
              "Tàu nào có hàng cần bốc lên là Cần trục vươn tới.", "Hòm nhỏ, hòm to, Cần trục xách một tay cứ như không.",
              "Cả những chiếc ô tô, những cỗ máy lớn, Cần trục cũng chỉ khẽ cúi xuống, | "
              "vươn tay ra, móc lấy sợi dây chằng rồi từ từ nhấc lên."]
lesson(395, [83, 84],
       [picture(CAN_TRUC, "Bác Cần trục nhấc thùng hàng từ tàu lên bến.", "cần trục"),
        title("Cánh tay khổng lồ"),
        *prose("PHONG THU",
               ["Bến cảng lúc nào cũng đông vui.", "Tàu mẹ, tàu con đậu đầy mặt nước.",
                "Xe anh, xe em tíu tít nhận hàng về và chở hàng ra.", "Tất cả đều bận rộn.",
                "Nhưng hăng hái nhất và khỏe nhất là bác Cần trục.",
                "Người bác không cao to, tiếng bác không ầm ĩ, chỉ có cái cánh tay của bác thì thật là đặc biệt."],
               CAN_TRUC_2,
               ["Cần trục đúng là cánh tay kì diệu của các chú công nhân."]),
        q("1. Ở bến cảng, em thấy có những gì đông vui?", marker="?"),
        q("2. Hăng hái nhất và khỏe nhất ở bến cảng là ai?"),
        q("3. Những câu nào, từ ngữ nào diễn tả sức khỏe kì lạ của bác Cần trục? (Đọc thong thả lại những câu đó)."),
        q("*4. Vì sao có thể nói: \"Cần trục đúng là cánh tay kì diệu của các chú công nhân\"?"),
        q("5. Tìm từ trái nghĩa với từ khổng lồ. Đặt một câu với từ vừa tìm được.")],
       listen(("cần trục", "bến cảng", "cánh tay"), ("bến cảng", "cần trục", "cỗ máy"), ("cánh tay", "cỗ máy", "sợi dây"),
              ("cỗ máy", "cánh tay", "bến cảng"), ("tíu tít", "sừng sững", "ầm ĩ"), ("sừng sững", "tíu tít", "kì diệu")),
       images={CAN_TRUC: CAN_TRUC_DESC},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 396 — Bài 48. Em muốn lái máy bay (Học thuộc lòng, tr.84–86)
lesson(396, [84, 85, 86],
       [picture(img(396, "máy bay"), "Em bé mơ được lái máy bay bay qua đám mây.", "máy bay"),
        title("Em muốn lái máy bay", "Học thuộc lòng"),
        *sentences("Em muốn lái máy bay", "Miễn dạy em cầm lái.", "Đổ xăng vào bình chứa,", "Nổ máy, cánh quạt quay.",
                   "\"Vù lên trời, máy ơi,", "Cùng với chim ca hót\".", "Chẳng sợ gió", "Sợ mưa gì hết.",
                   "Tôi bay qua đám mây,", "Lửng lơ lưng chừng trời", "Lượn như chim âu trắng,", "Tôi bay trên biển nắng.",
                   "Núi kia cao đến đâu,", "Cũng bay vượt trên đầu.", "\"Mây ơi, đưa ta đi", "lên tận trăng, sao",
                   "Dấu trăng, sao", "xa lơ xa lắc\"."),
        passage("poem", "V. MAI-A-CỐP-XKI (Nga)", breaks=[8]),
        q("1. Em bé tưởng tượng khi bay lên trời sẽ được làm bạn với ai?", marker="?"),
        q("2. Em bé cũng tưởng tượng sẽ được bay qua những đâu và bay tới những nơi nào?"),
        q("*3. Tìm trong bài những từ ngữ tả các cách bay khác nhau của em bé."),
        q("4. Tìm một số từ ghép có tiếng xa ở đầu. Ví dụ: (xa lắc)."),
        memorize()],
       listen(("máy bay", "cánh quạt", "bình chứa"), ("cánh quạt", "máy bay", "chim âu"), ("chim âu", "đám mây", "biển nắng"),
              ("đám mây", "chim âu", "cánh quạt"), ("lửng lơ", "xa lắc", "cầm lái"), ("xa lắc", "lửng lơ", "đám mây")),
       images={img(396, "máy bay"): "Trên trời xanh có vài đám mây: chiếc máy bay cánh quạt nhỏ xinh bay vút lên, "
                                    "em bé ngồi trong buồng lái vẫy khăn; bên dưới là rừng cây bạch dương, "
                                    "các bạn nhỏ đứng giơ tay vẫy theo"},
       notes=[("sach", "Bài thơ trích (sách in dấu \".....\" ở đầu bài)."),
              ("sach", "Sách in \"Dấu trăng, sao\" (nghĩa là \"Dẫu\"); app chép như sách."),
              ("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)],
       review=[("@Dấu trăng", "sách in \"Dấu\" (có thể là lỗi in của \"Dẫu\"): chủ dự án xem giữ hay sửa")])

# 397 — Bài 49. Mẹ Thủy (tr.86–87)
lesson(397, [86, 87],
       [picture(img(397, "công trường"), "Mẹ Thủy làm việc trên công trường cao.", "công trường"),
        title("Mẹ Thủy"),
        *prose("THÁI BÁ TÂN",
               ["Một lần, Thủy được một chú công nhân dẫn vào sâu trong công trường."],
               ["Ở tít trên cao, lại đội chiếc mũ hàn che kín mặt, thế mà mẹ vẫn nhìn thấy Thủy.", "Mẹ cởi mũ, cười.",
                "Còn Thủy thì đứng dưới, giơ bàn tay bé xíu vẫy chào mẹ.",
                "Rồi mẹ quay sang phía chiếc cần cẩu cao lêu đêu.", "Chiếc cần cẩu đang chìa bàn tay sắt tới chỗ mẹ.",
                "Một chốc sau, Thủy nhận được hai chiếc kẹo mẹ gói vội trong một tờ giấy nhỏ, gửi theo xuống."],
               ["Một cô công nhân rất trẻ vừa nhanh nhẹn móc dây vào tấm bê tông, vừa cười và nói:"],
               ["- Thủy có muốn lên với mẹ không, ngồi vào đây, cô bảo cần cẩu bế lên?"],
               ["Thủy bẽn lẽn đứng im, lắc đầu."]),
        q("1. Mẹ Thủy làm nghề gì và đang làm việc ở đâu?", marker="?"),
        q("2. Trông thấy nhau, hai mẹ con chào nhau như thế nào?"),
        q("3. Chiếc cần cẩu đưa vật liệu lên cho mẹ Thủy làm việc như thế nào? "
          "Khi \"bàn tay sắt\" trở xuống, mẹ Thủy gửi theo cho Thủy cái gì?"),
        q("4. Biết cô công nhân nói đùa, Thủy đã làm gì?"),
        q("*5. Tìm trong bài hai từ ghép có tiếng công ở đầu. Đặt câu với mỗi từ đó.")],
       listen(("công trường", "cần cẩu", "mũ hàn"), ("cần cẩu", "công trường", "bê tông"), ("mũ hàn", "bê tông", "chiếc kẹo"),
              ("bê tông", "mũ hàn", "cần cẩu"), ("lêu đêu", "bẽn lẽn", "nhanh nhẹn"), ("bẽn lẽn", "lêu đêu", "công nhân")),
       images={img(397, "công trường"): "Công trường xây dựng nhà cao tầng có cần cẩu tháp và khung thép: người mẹ đội "
                                        "mũ hàn đẩy lên trán, mặc quần áo bảo hộ, đứng trên giàn cao mỉm cười; dưới đất "
                                        "xa xa chú công nhân dắt tay bé gái Thủy đang giơ tay vẫy mẹ"},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 398 — Bài 50. Đoàn tàu chở hàng (Bài đọc thêm, tr.87–88; sách không có tranh)
lesson(398, [87, 88],
       [title("Đoàn tàu chở hàng", "Bài đọc thêm"),
        *prose("Theo Ê-ĐU-A PE-TI-ZKA (Đức), TRÚC MAI và NHỊ HÀ lược dịch",
               ["Một đoàn tàu chở hàng đang xình xịch chạy, phun khói trắng xóa.",
                "Phía trước là đầu máy rồi đến năm toa nối nhau.",
                "Toa cuối cùng là một toa bỏ không vừa chạy vừa hò hét to nhất."],
               ["Toa củi chạy trước nó liền hỏi:"], ["- Có gì mà cậu hò hét điếc cả tai thế?"],
               ["Chiếc toa không liền trả lời:"],
               ["- Tớ là một cái toa danh tiếng lừng lẫy. | Tuần trước tớ đã chở một con sư tử cho vườn bách thú đấy nhé!"],
               ["Toa củi nói:"], ["- Cậu thì có gì ghê gớm! | Nếu tôi không kéo cậu đi thì cậu phải đứng ì tại chỗ."],
               ["Toa khoai nghe nói vậy, lanh canh lên tiếng:"], ["- Thôi đi các cậu! Chính tôi kéo hai cậu chạy theo!"],
               ["Toa gạo mỉa mai nói:"], ["- Nói gì vậy? Cả ba cậu đều do tôi kéo hết!"],
               ["Toa sách báo nghe vậy liền cười:"], ["- Các cậu nhầm rồi! Chính tôi kéo cả bốn cậu."],
               ["Đầu máy thở phì phì và tức giận nói:"],
               ["- Sao các cậu kiêu căng đến thế! | Không có tớ thì tất cả các cậu đều chết dí tại chỗ!"],
               ["Bỗng đoàn tàu chạy chậm chậm dần rồi dừng lại..."], ["Toa sách báo liền hỏi:"],
               ["- Anh đầu máy! Tại sao anh không chạy? | Anh vừa bảo anh kéo tất cả chúng tôi cơ mà?"],
               ["Đầu máy trả lời:"], ["- Người lái tàu hãm tôi lại. | Và người ấy đã muốn thì tôi đành chịu!"])],
       listen(("đoàn tàu", "đầu máy", "toa củi"), ("đầu máy", "đoàn tàu", "toa gạo"), ("toa củi", "toa khoai", "sư tử"),
              ("toa khoai", "toa sách báo", "đầu máy"), ("xình xịch", "lanh canh", "phì phì"), ("phì phì", "xình xịch", "kiêu căng")),
       notes=[("khac_sach", KS_SPLIT)])

# 399 — Chính tả tuần 29 (tr.88–89)
lesson(399, [88, 89],
       [title("Chính tả: Cánh tay khổng lồ", "Nghe đọc"),
        title("Bài viết: \"Cái cánh tay ấy... nhấc lên\".", "Phần này con viết vào vở cùng bố mẹ."),
        words("sừng sững", "chuyển", "trục", "hòm", "xách", "vươn", "hàng", "cỗ", "khẽ"),
        q("a) Xếp các ô chữ sau đây cho thành câu:",
          lines=["vươn lên, Cần trục, sừng sững, và, rất chậm, chuyển động",
                 "ra, vươn tay, Cần trục, cỗ máy, lên, nhấc"]),
        fill(["chục", "trục"], ("cần trục", "trục", "trục"), ("chục trứng", "chục", "chục")),
        fill(["hàng", "hàn"], ("cửa hàng", "hàng", "hàng"), ("thợ hàn", "hàn", "hàn")),
        combine_mixed("khẽ", ("khe", "before"), ("nói", "before")),
        title("Chính tả: Trâu ơi", "Trí nhớ"),
        title("Bài viết: Cả bài.", "Phần này con viết vào vở cùng bố mẹ."),
        words("ngoài", "cấy cày", "nghiệp", "gia", "trâu", "nông", "quản", "bảo"),
        combine("ngoài", "sân", "biển"),
        combine("nghiệp", "nghề", "tội", at="before"),
        fill(["tr", "ch"], ("con trâu", "trâu", "tr"), ("con châu chấu", "châu", "ch")),
        fill(["n", "ng"], ("không quản công", "quản", "n"), ("quảng trường Ba Đình", "quảng", "ng")),
        fill(["bảo", "bão"], ("dạy bảo", "bảo", "bảo"), ("trận bão", "bão", "bão"))],
       listen(("cần trục", "chục trứng", "cửa hàng"), ("thợ hàn", "cửa hàng", "khe khẽ"), ("nói khẽ", "khe khẽ", "ngoài sân"),
              ("ngoài biển", "nghề nghiệp", "tội nghiệp"), ("con trâu", "châu chấu", "quảng trường"),
              ("dạy bảo", "trận bão", "quản công")),
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Xếp ô chữ thành câu: bé nói cùng bố mẹ; ghép chữ, điền chỗ trống làm bằng chạm thẻ.")],
       review=[("@a) Xếp các ô chữ", "câu gợi ý cho bố mẹ: \"Cần trục vươn lên sừng sững và chuyển động rất chậm.\", "
                                     "\"Cần trục vươn tay ra nhấc cỗ máy lên.\""),
               ("part1[4]", "đáp án chục/trục theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[5]", "đáp án hàng/hàn theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[6]", "ghép \"khe khẽ\", \"nói khẽ\" do app chọn"),
               ("part1[10]", "ghép \"ngoài sân\", \"ngoài biển\" do app chọn"),
               ("part1[11]", "ghép \"nghề nghiệp\", \"tội nghiệp\" do app chọn"),
               ("part1[12]", "đáp án tr/ch theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[13]", "đáp án n/ng theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[14]", "đáp án bảo/bão theo chính tả chuẩn (sách không in đáp án)")])

# 400 — Từ ngữ: Giao thông vận tải (tr.89–91)
lesson(400, [89, 90, 91],
       [title("Từ ngữ: Giao thông vận tải"),
        title("Những từ ngữ cần ghi nhớ"),
        words("ô tô", "tàu hỏa", "tàu thủy", "máy bay", "nhà ga", "bến cảng", "cần trục"),
        words("chuyên chở", "vận chuyển", "an toàn"),
        title("Bài tập: Điền từ ngữ thích hợp vào những chỗ trống"),
        fill_passage(["Chúng ta đi lại, chuyên chở trên đường bộ bằng [ô tô|máy bay|tàu thủy] "
                      "hoặc [tàu hỏa|máy bay|bến cảng].",
                      "Muốn đi lại bằng đường không chúng ta có [máy bay|tàu hỏa|nhà ga].",
                      "Ngoài ra, muốn [chuyên chở|an toàn|nhà ga] trên sông, trên biển, chúng ta có [tàu thủy|ô tô|cần trục].",
                      "Tàu thủy đậu ở [bến cảng|nhà ga|cần trục].", "Tàu hỏa đỗ ở [nhà ga|bến cảng|máy bay].",
                      "Ở các bến cảng thường có những chiếc [cần trục|tàu hỏa|ô tô] khổng lồ "
                      "để bốc dỡ hàng hóa từ tàu biển lên.",
                      "Chú Phong là một công nhân lái xe vận tải rất lành nghề.",
                      "Xe chú [vận chuyển|nhà ga|cần trục] hàng tấn hàng và chạy hàng nghìn cây số đường dài "
                      "mà vẫn [an toàn|bến cảng|máy bay]."]),
        title("*2. Điền các từ sau đây vào những chỗ trống thích hợp:", "nhổ neo, chuyển bánh, nổ máy, cất cánh."),
        fill_passage(["Ô tô [nổ máy].", "Tàu hỏa [chuyển bánh].", "Máy bay [cất cánh].", "Tàu thủy [nhổ neo]."],
                     bank=["nhổ neo", "chuyển bánh", "nổ máy", "cất cánh"])],
       listen(("ô tô", "tàu hỏa", "máy bay"), ("tàu thủy", "nhà ga", "bến cảng"), ("nhà ga", "bến cảng", "cần trục"),
              ("cần trục", "ô tô", "tàu thủy"), ("chuyên chở", "vận chuyển", "an toàn"), ("cất cánh", "nhổ neo", "nổ máy")),
       notes=[("khac_sach", "Điền từ: mỗi chỗ trống 3 thẻ do app chọn trong các từ ngữ cần ghi nhớ, tránh hai từ cùng "
                            "đúng; đáp án do app soạn."),
              ("khac_sach", "Sách có tranh máy bay, tàu hỏa, ô tô, tàu thủy; app không vẽ (bài từ ngữ).")],
       review=[("part1[5]", "đáp án và thẻ chọn do app soạn: ô tô, tàu hỏa, máy bay, chuyên chở, tàu thủy, bến cảng, "
                            "nhà ga, cần trục, vận chuyển, an toàn"),
               ("part1[7]", "đáp án do app soạn: Ô tô nổ máy, Tàu hỏa chuyển bánh, Máy bay cất cánh, Tàu thủy nhổ neo")])

# 401 — Ngữ pháp: Tập xếp tên người theo thứ tự bảng chữ cái (tiếp theo) (tr.91)
lesson(401, [91],
       [title("Ngữ pháp: Tập xếp tên người theo thứ tự bảng chữ cái", "Tiếp theo"),
        *rule("1. Nếu 2 người trùng tên thì căn cứ vào con chữ đầu của Họ để xếp thứ tự:",
              "Nguyễn Hữu Hưng xếp trước Trịnh Văn Hưng (vì n trước t)."),
        *rule("2. Nếu 2 người trùng tên, trùng họ thì căn cứ vào con chữ đầu của tên lót để xếp thứ tự.",
              "Trịnh Anh Hạnh xếp trên Trịnh Văn Hạnh (vì a trước v),",
              "hoặc: Đỗ Quang xếp trước Đỗ Văn Quang (tên người nào ít tiếng thì xếp trước)."),
        q("3. Có 5 bạn tên là: (Em hãy xếp tên 5 bạn đó theo thứ tự bảng chữ cái.)",
          lines=["Nguyễn Xuân Cảnh", "Trần Văn Cảnh", "Đỗ Thị Cảnh", "Trần Tấn Cảnh", "Đỗ Đức Cảnh"])],
       listen(("họ tên", "tên lót", "thứ tự"), ("tên lót", "họ tên", "chữ cái"), ("thứ tự", "chữ cái", "tên lót"),
              ("chữ cái", "thứ tự", "họ tên"), ("trùng tên", "trùng họ", "thứ tự"), ("trùng họ", "trùng tên", "chữ cái")),
       notes=[("khac_sach", KS_XEP_TEN)])

# 402 — Tập làm văn: Dùng từ – đặt câu (tr.91)
lesson(402, [91],
       [title("Tập làm văn: Dùng từ – đặt câu"),
        title("Đề bài: Em hãy dùng mỗi từ ngữ sau đây đặt thành một câu nói về chiếc cần trục."),
        words("cần trục", "sừng sững", "cao lêu đêu", "bàn tay sắt", "cánh tay kì diệu"),
        q("Em hãy đặt câu với mỗi từ ngữ trên.")],
       listen(("cần trục", "bàn tay sắt", "sừng sững"), ("sừng sững", "cao lêu đêu", "cần trục"),
              ("cao lêu đêu", "sừng sững", "bàn tay sắt"), ("bàn tay sắt", "cần trục", "cánh tay kì diệu"),
              ("cánh tay kì diệu", "bàn tay sắt", "cao lêu đêu"), ("bến cảng", "cần trục", "sừng sững")),
       notes=[("khac_sach", KS_DAT_CAU),
              ("khac_sach", "Câu \"Em hãy đặt câu với mỗi từ ngữ trên\" do app thêm để nhắc bé (trang chỉ in đề bài).")],
       review=[("part1[3]", "câu nhắc đặt câu do app thêm")])
print("tuần 29 xong")
