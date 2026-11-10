"""Tuần 4 (mục 196–202), tr.24–29, ảnh 013–015."""
from l2lib import *

# 196 — Bài 13. Cò và Vạc (tr.24–25)
lesson(196, [24, 25],
       [picture("img_b196_cof_vaj_vacj", "Cò đứng đọc sách, Vạc nằm ngủ trong bụi cây.", "Cò và Vạc"),
        title("Cò và Vạc"),
        *sentences("Cò và Vạc là hai anh em, nhưng tính nết rất khác nhau.",
                   "Cò thì ngoan ngoãn, chăm chỉ học tập,",
                   "sách vở sạch sẽ, luôn luôn được thầy yêu bạn mến.",
                   "Còn Vạc thì lười biếng, suốt ngày chỉ nằm ngủ.",
                   "Cò bảo mãi, Vạc chẳng nghe.",
                   "Nhờ chăm chỉ siêng năng nên Cò học giỏi nhất lớp.",
                   "Còn Vạc thì chịu ngu dốt.",
                   "Sợ chúng bạn chế nhạo, ban đêm Vạc mới bay đi kiếm ăn.",
                   "Ngày nay, chúng ta lật cánh Cò lên,",
                   "vẫn thấy một dúm lông màu vàng nhạt,",
                   "người ta bảo đó là quyển sách của Cò.",
                   "Cò rất chăm học nên lúc nào cũng mang sách theo.",
                   "Sau những buổi mò tôm bắt ốc,",
                   "Cò lại đậu trên ngọn tre giở sách ra học."),
        passage("prose", "Truyện cổ Việt Nam – LÊ NGÂN sưu tầm", breaks=[5, 8]),
        *glossary("Vạc: loài chim hình dáng gần giống Cò, ở đầu có một túm lông nhọn, chuyên đi ăn về đêm."),
        q("1. Em hãy nêu những tính tốt của Cò.", marker="?"),
        q("2. Vạc có tính xấu gì?"),
        q("3. Tìm từ trái nghĩa với lười biếng."),
        q("4. Em hãy kể lại chuyện Cò và Vạc bằng lời kể của mình.")],
       listen(("ngoan ngoãn", "chăm chỉ", "lười biếng"), ("lười biếng", "ngu dốt", "chế nhạo"),
              ("chăm chỉ", "siêng năng", "ngoan ngoãn"), ("mò tôm", "bắt ốc", "kiếm ăn"),
              ("ngọn tre", "dúm lông", "quyển sách"), ("vàng nhạt", "ngọn tre", "mò tôm")),
       images={"img_b196_cof_vaj_vacj": "Con cò trắng đứng trên cành tre cầm quyển sách nhỏ chăm chú đọc; bên dưới, "
                                        "con vạc lông xám nằm ngủ trong bụi cây rậm, trời mây xanh"},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 197 — Bài 14. Quyển vở của em (Học thuộc lòng, tr.25–26)
POEM14 = ["Quyển vở này mở ra", "Bao nhiêu trang giấy trắng", "Từng dòng kẻ ngay ngắn", "Như chúng em xếp hàng.",
          "Lật từng trang, từng trang", "Giấy trắng sờ mát rượi", "Thơm tho mùi giấy mới", "Nắn nót bàn tay xinh.",
          "Ơi quyển vở mới tinh", "Em viết cho sạch, đẹp", "Chữ đẹp là tính nết", "Của những người trò ngoan."]
lesson(197, [25, 26],
       [picture("img_b197_bes_vieets_bai", "Bé ngồi nắn nót viết vào quyển vở mới.", "quyển vở"),
        title("Quyển vở của em", "Học thuộc lòng"),
        *sentences(*POEM14),
        passage("poem", "QUANG HUY", breaks=[4, 8]),
        q("1. Quyển vở mới có gì đẹp khiến cho em yêu thích?", marker="?"),
        q("2. Muốn giữ cho vở đẹp, em phải làm gì?"),
        find("3. Tìm những tiếng có vần giống nhau (hoặc gần giống nhau) ở cuối các dòng thơ.",
             {"word": ["trắng", "ngắn", "hàng", "trang", "rượi", "mới", "xinh", "tinh"]}),
        choose("4. Trong khổ thơ thứ 2, câu thơ nào có hai tiếng được láy lại?", POEM14[4:8], [0]),
        memorize()],
       listen(("giấy trắng", "dòng kẻ", "xếp hàng"), ("ngay ngắn", "mát rượi", "nắn nót"),
              ("mát rượi", "thơm tho", "mới tinh"), ("nắn nót", "ngay ngắn", "thơm tho"),
              ("mới tinh", "giấy mới", "trò ngoan"), ("tính nết", "trò ngoan", "chữ đẹp")),
       images={"img_b197_bes_vieets_bai": "Cô bé tóc ngắn mặc áo chấm bi ngồi bên bàn, cầm bút nắn nót viết vào quyển "
                                          "vở mở, lọ mực nhỏ đặt cạnh; ngoài cửa sổ có tranh con cò"},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)],
       review=[("part1[17]", "tiếng cuối dòng cùng vần (hoặc gần giống) do app chọn: trắng–ngắn, hàng–trang, "
                             "rượi–mới, xinh–tinh"),
               ("part1[18]", "đáp án câu thơ có tiếng láy lại do app soạn: Lật từng trang, từng trang")])

# 198 — Bài 15. Câu đố: Đồ dùng của học sinh (Bài đọc thêm, tr.27; đáp án tr.122)
lesson(198, [27, 122],
       [title("Câu đố: Đồ dùng của học sinh", "Bài đọc thêm"),
        *sentences("Mình tròn, mũi nhọn", "Không phải bò, trâu", "Uống nước ao sâu", "Lên cày ruộng cạn.",
                   "(Là cái gì?)"),
        {"type": "riddle_answer", "answer": "Bút mực", "image": "img_b198_buts_muwcj",
         "options": [{"image": "img_b137_buts_chif", "text": "Bút chì"},
                     {"image": "img_b08_quyeenr_vowr", "text": "Quyển vở"}]},
        *sentences("Ruột dài từ mũi đến chân", "Mũi mòn, ruột cũng dần dần mòn theo", "(Là cái gì?)"),
        {"type": "riddle_answer", "answer": "Bút chì", "image": "img_b137_buts_chif",
         "options": [{"image": "img_b198_buts_muwcj", "text": "Bút mực"},
                     {"image": "img_b08_quyeenr_vowr", "text": "Quyển vở"}]},
        *sentences("Mình em thì trắng phau phau", "Áo em có đủ các màu đỏ xanh", "Gân em là sợi chỉ mành",
                   "Giúp cậu trò nhỏ học hành nên khôn.", "(Là cái gì?)"),
        {"type": "riddle_answer", "answer": "Quyển vở", "image": "img_b08_quyeenr_vowr",
         "options": [{"image": "img_b198_buts_muwcj", "text": "Bút mực"},
                     {"image": "img_b137_buts_chif", "text": "Bút chì"}]}],
       [{"kind": "listen_picture", "rounds": [
           {"word": "Bút mực", "prompt": "Mình tròn, mũi nhọn, không phải bò, trâu, uống nước ao sâu, lên cày ruộng cạn. "
                                         "Là cái gì?", "answer": "img_b198_buts_muwcj",
            "options": ["img_b198_buts_muwcj", "img_b137_buts_chif", "img_b08_quyeenr_vowr"]},
           {"word": "Bút chì", "prompt": "Ruột dài từ mũi đến chân, mũi mòn, ruột cũng dần dần mòn theo. Là cái gì?",
            "answer": "img_b137_buts_chif", "options": ["img_b08_quyeenr_vowr", "img_b137_buts_chif", "img_b198_buts_muwcj"]},
           {"word": "Quyển vở", "prompt": "Mình em thì trắng phau phau, áo em có đủ các màu đỏ xanh. Là cái gì?",
            "answer": "img_b08_quyeenr_vowr", "options": ["img_b137_buts_chif", "img_b198_buts_muwcj", "img_b08_quyeenr_vowr"]}]},
        *listen(("phau phau", "chỉ mành", "ao sâu"), ("ruộng cạn", "ao sâu", "mũi nhọn"),
                ("học hành", "nên khôn", "chỉ mành"))],
       images={"img_b198_buts_muwcj": "Chiếc bút mực (bút máy) thân tròn, ngòi nhọn, đặt cạnh lọ mực tím; không có chữ",
               "img_b137_buts_chif": "Cây bút chì gỗ vót nhọn, ruột chì đen",
               "img_b08_quyeenr_vowr": "Quyển vở mở nằm nghiêng trên bàn, bìa có hình vẽ em bé đang chạy và một ô nhãn"},
       notes=[("khac_sach", "Đáp án câu đố lấy ở tr.122 \"Giải đáp câu đố\" và hiện ngay sau mỗi câu đố. "
                            "Tranh đáp án vẽ mới hoặc dùng lại tranh đã có (bút chì, quyển vở).")],
       review=[("part1[6]", "tranh đáp án bút mực vẽ mới (sách không có tranh)")])

# 199 — Chính tả tuần 4 (tr.27–28)
lesson(199, [27, 28],
       [title("Tập chép: Cò và Vạc", "Nhìn bảng"),
        title("Bài chép: \"Ngày nay... ra học\".", "Phần này con chép vào vở cùng bố mẹ."),
        words("dúm lông", "quyển", "giở sách", "chăm", "nhạt", "cũng"),
        combine("dúm", "lông", "muối"),
        combine("quyển", "vở", "sách", "truyện", "sổ"),
        fill(["giở", "dở"], ("giở trang sách", "giở", "giở"), ("giở vở ra học", "giở", "giở"), ("dở dang", "dở", "dở")),
        fill(["ch", "tr"], ("chăm học", "chăm", "ch"), ("chăm làm", "chăm", "ch"), ("trăm công", "trăm", "tr")),
        title("Chính tả: Đi học", "Trí nhớ"),
        title("Bài viết: 8 câu thơ cuối.", "Phần này con nhớ lại rồi viết vào vở."),
        words("giữa", "dạy", "giáo", "xòe", "rừng", "lặng", "trẻ"),
        combine("giữa", "rừng", "lớp", "sân"),
        combine("dạy", "toán", "văn", "bảo", "dỗ"),
        fill(["r", "d"], ("cây rừng", "rừng", "r"), ("xe dừng lại", "dừng", "d")),
        fill(["n", "ng"], ("Mặt trời lặn", "lặn", "n"), ("cảnh vật im lặng", "lặng", "ng"))],
       listen(("dúm lông", "dúm muối", "quyển sổ"), ("quyển truyện", "quyển sách", "giở sách"),
              ("dở dang", "giở sách", "chăm làm"), ("giữa rừng", "giữa sân", "dạy toán"),
              ("dạy bảo", "dạy dỗ", "giữa lớp"), ("lặng", "rừng", "dạy")),
       notes=[("khac_sach", KS_WRITE), ("khac_sach", "Điền chỗ trống, ghép chữ làm bằng chạm hoặc kéo thẻ.")],
       review=[("part1[5]", "đáp án giở/dở theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[6]", "đáp án ch/tr: chăm học, chăm làm, trăm công nghìn việc"),
               ("part1[12]", "đáp án r/d: rừng, dừng"), ("part1[13]", "đáp án n/ng: lặn, lặng")])

# 200 — Từ ngữ: Đồ dùng của học sinh (tr.28)
lesson(200, [28],
       [title("Từ ngữ: Đồ dùng của học sinh"),
        title("Những từ ngữ cần ghi nhớ"),
        words("sách", "vở", "lọ mực", "bút mực", "bút chì", "thước kẻ", "giấy trắng"),
        words("sạch sẽ", "ngăn nắp", "gọn gàng", "nắn nót"),
        title("Bài tập"),
        q("1. Kể tiếp những đồ dùng của học sinh chưa nêu ở trên."),
        q("2. Sách và vở có gì khác nhau?"),
        title("3. Tìm từ thích hợp điền vào chỗ trống"),
        fill_passage(["Sạch sẽ là không [bẩn|mới|đẹp].",
                      "[Ngăn nắp|Nắn nót|Sạch sẽ] là không lộn xộn.",
                      "[Gọn gàng|Nắn nót|Giấy trắng] là không luộm thuộm.",
                      "Em tập viết [nắn nót|ngăn nắp|gọn gàng] từng chữ trên trang vở mới tinh."])],
       listen(("lọ mực", "bút mực", "bút chì"), ("thước kẻ", "giấy trắng", "lọ mực"),
              ("ngăn nắp", "gọn gàng", "nắn nót"), ("gọn gàng", "sạch sẽ", "ngăn nắp"),
              ("nắn nót", "ngăn nắp", "thước kẻ"), ("giấy trắng", "bút chì", "sạch sẽ")),
       notes=[("khac_sach", KS_ORAL),
              ("khac_sach", "Bài 3 sách để trống: app cho mỗi chỗ trống 3 thẻ để chọn; thẻ và đáp án do app soạn.")],
       review=[("part1[8]", "thẻ chọn và đáp án điền chỗ trống do app soạn (\"là không lộn xộn\": ngăn nắp)")])

# 201 — Ngữ pháp: Câu – Mở đầu và kết thúc (tiếp theo) (tr.29)
lesson(201, [29],
       [title("Ngữ pháp: Câu – Mở đầu và kết thúc", "Tiếp theo"),
        title("Nhìn vào hình vẽ và trả lời"),
        picture("img_b201_laam_hocj_baif", "Lâm đứng bên bàn học bài.", "học bài"),
        q("1. Lâm đang làm gì? (tranh bên trái)"),
        picture("img_b201_laam_vieets_baif", "Lâm ngồi ngay ngắn viết bài.", "viết bài"),
        q("2. Khi học thuộc bài rồi, Lâm làm gì? (tranh bên phải)"),
        q("3. Trên bàn học, đồ đạc được sắp xếp thế nào?"),
        q("Em hãy chép lại các câu trả lời vào vở. Đoạn văn em vừa chép có mấy câu? "
          "Chữ đầu câu viết như thế nào cho đúng? Có dấu gì ở cuối câu?")],
       listen(("học bài", "viết bài", "bàn học"), ("bàn học", "học bài", "đồ đạc"),
              ("đồ đạc", "sắp xếp", "viết bài"), ("sắp xếp", "đồ đạc", "học thuộc"),
              ("học thuộc", "học bài", "sắp xếp"), ("viết bài", "bàn học", "học thuộc")),
       images={"img_b201_laam_hocj_baif": "Cậu bé Lâm đứng bên bàn học gọn gàng, hai tay đặt trên trang sách, chăm chú "
                                          "đọc bài; trên bàn có chồng sách xếp ngay ngắn, lọ mực, đồng hồ nhỏ",
               "img_b201_laam_vieets_baif": "Cậu bé Lâm ngồi ngay ngắn trên ghế, cúi viết bài vào vở; trên bàn có lọ mực "
                                            "và chồng sách xếp gọn, đồng hồ nhỏ"},
       notes=[("khac_sach", "Sách in hai tranh cạnh nhau; app hiện từng tranh trước câu hỏi về tranh đó. "
                            "Bé trả lời miệng cùng bố mẹ; phần chép vào vở bé viết cùng bố mẹ.")],
       review=[("part1[2]", "lời dẫn tranh do app soạn"), ("part1[4]", "lời dẫn tranh do app soạn")])

# 202 — Tập làm văn: Điền từ — Đồ dùng của Lan (tr.29)
lesson(202, [29],
       [title("Tập làm văn: Điền từ"),
        title("Đề bài: Đồ dùng của Lan.",
              "Em hãy chọn những từ sau đây để điền vào chỗ trống: sách, vở, cặp, sạch sẽ, bút mực, gọn gàng."),
        fill_passage(["Lan cắp chiếc [cặp] mới đi học.",
                      "Trong cặp, Lan để [vở] và một hộp bút.",
                      "Hộp bút của Lan có đủ bút chì, [bút mực], thước kẻ và một cái tẩy.",
                      "Lan luôn luôn giữ gìn sách vở [sạch sẽ].",
                      "Đồ dùng của Lan lúc nào cũng được sắp xếp [gọn gàng].",
                      "Lan thường được cô giáo khen."],
                     bank=["sách", "vở", "cặp", "sạch sẽ", "bút mực", "gọn gàng"])],
       listen(("hộp bút", "bút chì", "cái tẩy"), ("cái tẩy", "thước kẻ", "hộp bút"),
              ("sạch sẽ", "gọn gàng", "sắp xếp"), ("gọn gàng", "giữ gìn", "sạch sẽ"),
              ("giữ gìn", "sắp xếp", "cô giáo"), ("sắp xếp", "giữ gìn", "hộp bút")),
       notes=[("khac_sach", "Điền từ bằng chạm hoặc kéo thẻ từ vào chỗ trống; đáp án do app soạn.")],
       review=[("part1[2]", "đáp án điền từ do app soạn; \"Lan để ... và một hộp bút\": sách hay vở đều được, "
                            "app chọn vở")])
