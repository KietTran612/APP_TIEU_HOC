"""Tuần 21 (mục 330–338), tr.27–34, ảnh 003, 006, 009, 011, 013."""
from l2t2lib import *

# 330 — Bài 14. Làm việc thật là vui (tr.27–28)
LAM_VIEC = [["Quanh ta, mọi vật, mọi người đều làm việc."],
            ["Cái đồng hồ tích tắc, tích tắc báo phút, báo giờ."],
            ["Con gà trống gáy vang ò ó o... báo cho mọi người biết trời sắp sáng, mau mau thức dậy."],
            ["Con tu hú kêu: tu hú, tu hú.", "Thế là sắp đến mùa vải chín."]]
lesson(330, [27, 28],
       [picture(img(330, "làm việc"), "Mọi người, mọi vật đều làm việc.", "làm việc"),
        title("Làm việc thật là vui"),
        *prose("TÔ HOÀI", *LAM_VIEC,
               ["Chim bắt sâu bảo vệ mùa màng."],
               ["Cỏ xanh nuôi thỏ, nuôi bò."],
               ["Cành đào nở hoa cho sắc xuân thêm rực rỡ, ngày xuân thêm tưng bừng."],
               ["Cô chim cú mèo có hai mắt hau háu, | chặp tối đứng trong hốc cây rúc \"cú cú\" nghe rợn người | "
                "cũng làm việc có ích cho đồng ruộng."],
               ["Như mọi vật, mọi người, bé cũng làm việc.", "Bé làm bài, bé đi học.",
                "Học xong, bé quét nhà, nhặt rau, chơi với em đỡ mẹ.",
                "Bé cũng luôn luôn bận rộn, mà công việc lúc nào cũng nhộn nhịp, cũng vui!..."]),
        q("1. Em tìm trong bài xem những vật gì đang làm việc? "
          "Những loài vật nào và những cây cối nào đang làm việc?", marker="?"),
        q("2. Bé làm những việc gì và làm như thế nào?"),
        q("3. Em hãy tìm trong bài những danh từ chỉ loài vật."),
        q("4. Đặt câu với mỗi từ: làm việc, vui.")],
       listen(("đồng hồ", "gà trống", "tu hú"), ("tu hú", "cú mèo", "đồng hồ"), ("mùa màng", "đồng ruộng", "mùa vải"),
              ("cành đào", "cỏ xanh", "gà trống"), ("bận rộn", "nhộn nhịp", "tưng bừng"), ("nhộn nhịp", "bận rộn", "rực rỡ")),
       images={img(330, "làm việc"): "Cảnh làng quê buổi sớm: mặt trời mọc sau cánh đồng, chiếc máy cày đang cày ruộng, "
                                     "mấy cô bác cúi cấy lúa; trên đường làng một em bé đeo cặp đi học cùng mẹ; "
                                     "cành đào nở hoa phía trước, gà trống đứng gáy, chim bay trên trời"},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 331 — Bài 15. Tí Xíu (Học thuộc lòng, tr.28–29)
TI_XIU = img(331, "Tí Xíu")
TI_XIU_DESC = ("Sân nhà quê bên bụi tre, xa xa dãy núi: ông cụ râu bạc ngồi vót thanh tre cật, cạnh đó cậu bé Tí Xíu "
               "đổ rau vào máng cho chú lợn ăn, mấy con gà đứng bên")
lesson(331, [28, 29],
       [picture(TI_XIU, "Tí Xíu mang rau về cho lợn ăn.", "Tí Xíu"),
        title("Tí Xíu", "Học thuộc lòng"),
        *sentences("Gọi là Tí Xíu", "Mà chẳng bé đâu!", "Tí biết lấy rau", "Mang về cho lợn", "Tí biết nấu nướng",
                   "Hai bữa cơm canh.", "Tí còn nhờ ông", "Pha thanh tre cật", "Tí ngồi Tí vót", "Được mười cây chông",
                   "Gửi đồn biên phòng", "Đánh quân cướp nước."),
        passage("poem", "NGÔ VĂN PHÚ", breaks=[6]),
        *glossary("Đồn biên phòng: nơi bộ đội đóng để canh phòng biên giới."),
        q("1. Bé tí xíu có nghĩa là bé lắm. Nhưng trong bài em bé có tên là Tí Xíu lại không bé. Tại sao? "
          "(Đọc kĩ cả hai khổ thơ để trả lời)", marker="?"),
        q("2. Tí Xíu làm được nhiều việc như thế để giúp đỡ những ai?"),
        q("3. \"Tí Xíu\" là danh từ chỉ tên chung của nhiều người hay tên riêng của một người? "
          "Em có nhận xét gì về cách viết từ đó?"),
        q("4. Em tìm một vài từ cùng nghĩa hoặc gần nghĩa với từ nấu nướng."),
        memorize()],
       listen(("nấu nướng", "cơm canh", "tre cật"), ("cơm canh", "nấu nướng", "cây chông"), ("tre cật", "cây chông", "biên phòng"),
              ("cây chông", "tre cật", "lấy rau"), ("biên phòng", "cướp nước", "cơm canh"), ("lấy rau", "nấu nướng", "biên phòng")),
       images={TI_XIU: TI_XIU_DESC},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)])

# 332 — Bài 16. Sao Chổi (tr.29–31)
SAO_CHOI = img(332, "sao Chổi")
SAO_CHOI_DESC = ("Sân thượng lát gạch hoa ban đêm, bầu trời đen chi chít sao, có một ngôi sao chổi kéo vệt sáng dài: "
                 "anh trai đứng giơ tay chỉ lên trời, em gái ngồi trên ghế băng tay cầm chổi, chú mèo đen đứng cạnh, "
                 "phía sau là hàng cây và cây dừa")
lesson(332, [29, 30, 31],
       [picture(SAO_CHOI, "Anh Tuấn chỉ cho bé Hà ngôi sao Chổi.", "sao Chổi"),
        title("Sao Chổi"),
        *prose("PHẠM ĐÌNH ÂN",
               ["Bé Hà quét sân xong thì trời vừa nhá nhem tối.", "Hai anh em mang ghế ra ngồi hóng mát.",
                "Không gian thoáng đãng.", "Đêm không trăng.", "Bầu trời chi chít sao sáng lấp lánh."],
               ["Bỗng nhiên, anh Tuấn reo lên:"],
               ["- Sao Chổi kìa!"],
               ["Bé Hà nhìn nhanh về phía tay anh Tuấn chỉ.",
                "Ngôi sao Chổi như một vệt quét sáng dài trên sân trời mênh mông."],
               ["Bé Hà thắc mắc:"],
               ["- Thế trời cũng quét sân hả anh?"],
               ["- Trời bắt chước em đấy. | Trên trời cũng phải đưa vài nhát chổi chứ! - Anh Tuấn cười hóm hỉnh."],
               ["- Bao nhiêu đêm, em có thấy sao Chổi đâu. | Bắt chước gì mà kém thế! - Bé Hà sôi nổi - | "
                "Hôm nào em cũng quét, còn trời thì lâu lắm mới đụng đến chổi."]),
        *glossary("Sao Chổi: sao tua, kéo theo một dải ánh sáng dài, giống hình cái chổi.",
                  "Không gian thoáng đãng: bầu trời trong trẻo, không có mây mù."),
        q("1. Những câu nào, từ ngữ nào tả bầu trời về đêm rất đẹp?", marker="?"),
        q("2. Câu nào tả ngôi sao Chổi? Trong câu đó, những từ \"chổi\", \"quét\", \"sân\" có ý so sánh "
          "ngôi sao Chổi với công việc gì hằng ngày của bé Hà?"),
        q("3. Vì sao bé Hà cho rằng mình còn chăm làm hơn cả trời?"),
        q("4. Đặt câu với mỗi từ: chi chít, lấp lánh."),
        find("5. Tìm những danh từ riêng trong bài này.", {"word": ["Hà", "Tuấn", "Chổi"]},
             text=["Bé Hà quét sân xong thì trời vừa nhá nhem tối.", "Bỗng nhiên, anh Tuấn reo lên:",
                   "- Sao Chổi kìa!", "Bé Hà nhìn nhanh về phía tay anh Tuấn chỉ."])],
       listen(("sao Chổi", "bầu trời", "cái chổi"), ("cái chổi", "sao Chổi", "quét sân"), ("chi chít", "lấp lánh", "nhá nhem"),
              ("lấp lánh", "chi chít", "thoáng đãng"), ("thoáng đãng", "mênh mông", "hóm hỉnh"),
              ("hóm hỉnh", "sôi nổi", "mênh mông")),
       images={SAO_CHOI: SAO_CHOI_DESC},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)],
       review=[("@5. Tìm những danh từ riêng", "danh từ riêng do app chọn trên bốn câu của bài: Hà, Tuấn, Sao Chổi")])

# 333 — Bài 17. Chế giễu người lười (Bài đọc thêm, tr.31)
lesson(333, [31],
       [title("Chế giễu người lười", "Bài đọc thêm"),
        *sentences("- Ăn no rồi lại nằm khoèo", "Nghe giục trống chèo bế bụng đi xem.",
                   "- Có làm thì mới có ăn", "Không dưng ai dễ đem phần đến cho.",
                   "- Vốn tôi có máu đau hàm", "Cơm ăn thì đỡ, việc làm thì đau.",
                   "- Ăn thì chọn những miếng ngon", "Làm thì chọn việc cỏn con mà làm.",
                   "- Làm trai cho đáng sức trai", "Khom lưng cố sức gánh hai hạt vừng."),
        passage("poem", "Tục ngữ Việt Nam", breaks=[2, 4, 6, 8])],
       listen(("trống chèo", "nằm khoèo", "hạt vừng"), ("hạt vừng", "miếng ngon", "trống chèo"),
              ("miếng ngon", "cỏn con", "đau hàm"), ("cỏn con", "miếng ngon", "khom lưng"),
              ("khom lưng", "đau hàm", "nằm khoèo"), ("nằm khoèo", "khom lưng", "cỏn con")),
       notes=[("sach", "Năm câu tục ngữ, ca dao chế giễu người lười (sách ghi \"Tục ngữ Việt Nam\").")])

# 334 — Bài 18. Chuyện bé Chăm (Bài đọc thêm, tr.32; sách không có tranh)
lesson(334, [32],
       [title("Chuyện bé Chăm", "Bài đọc thêm"),
        *prose("TRÚC MAI kể",
               ["Bé Chăm rất chăm làm nhưng cũng mau chán việc.",
                "Làm việc này chưa xong, em lại bỏ dở để làm việc khác."],
               ["Mới quét xong nửa cái sân, em lại lấy sách ra đọc.",
                "Bài học thuộc lòng mới thuộc nửa chừng, em lại lấy vở ra để tập chép."],
               ["Bố em thường khuyên răn em, nhưng bé Chăm vẫn chưa sửa chữa được."],
               ["Một hôm, bố dẫn Chăm đến bác thợ may ở trong làng | để may một bộ quần áo mới.",
                "Chăm thích quá vì sắp có bộ quần áo đẹp để mặc Tết.",
                "Một ngày, hai ngày và ngày thứ ba, Chăm đến lấy quần áo mới.",
                "Nhưng bác thợ may chỉ may xong nửa cái áo và nửa cái quần.", "Bác bảo Chăm cứ thế mặc vào xem sao."],
               ["Chăm mặc thử bộ quần áo làm cho mọi người bò lăn ra cười.", "Chăm bực tức nói:"],
               ["- Thế bác hãy may xong cái áo cho cháu đã có được không?",
                "Bác làm thế thành ra chẳng cái nào xong hẳn cả!"],
               ["Bác thợ nghiêm trang bảo: \"Cháu nói đúng, làm việc gì cũng phải làm đến nơi đến chốn "
                "mới khỏi phí công vô ích\"."])],
       listen(("thợ may", "quần áo", "nửa chừng"), ("quần áo", "thợ may", "bỏ dở"), ("bỏ dở", "nửa chừng", "khuyên răn"),
              ("khuyên răn", "bỏ dở", "nghiêm trang"), ("nghiêm trang", "khuyên răn", "quần áo"),
              ("nửa chừng", "nghiêm trang", "thợ may")),
       notes=[("khac_sach", KS_SPLIT)])

# 335 — Chính tả tuần 21 (tr.32–33)
lesson(335, [32, 33],
       [title("Chính tả: Làm việc thật là vui", "Nghe đọc"),
        title("Bài viết: \"Quanh ta... mùa vải chín\".", "Phần này con viết vào vở cùng bố mẹ."),
        words("quanh", "tích tắc", "gáy", "giờ", "dậy", "vang", "kêu", "vải"),
        q("Đồng hồ chạy kêu như thế nào?"),
        choose("Có thể ghép chữ gáy với những chữ nào trong các chữ sau?", ["gà", "mèo", "vịt", "cu"], [0, 3]),
        fill(["dạy", "dậy"], ("thầy dạy học", "dạy", "dạy"), ("em dậy sớm", "dậy", "dậy")),
        fill(["vang", "van"], ("gà gáy vang", "vang", "vang"), ("van nài", "van", "van"), ("van xin", "van", "van")),
        fill(["vải", "vãi"], ("quả vải", "vải", "vải"), ("áo vải", "vải", "vải"), ("rơi vãi", "vãi", "vãi"),
             ("vãi thóc", "vãi", "vãi")),
        title("Chính tả: Trăng sao cũng hóa xứ người", "Trí nhớ"),
        title("Bài viết: Cả bài.", "Phần này con viết vào vở cùng bố mẹ."),
        words("hóa", "người", "ngời", "trạm", "xinh", "đặt", "lượn", "vũ trụ"),
        combine_mixed("ngời", ("sáng", "before"), ("chói", "before")),
        combine_mixed("người", ("con", "before"), ("xứ", "before"), ("ta", "after"))],
       listen(("tích tắc", "đồng hồ", "gà gáy"), ("thầy dạy", "dậy sớm", "van xin"), ("van nài", "vang xa", "quả vải"),
              ("rơi vãi", "áo vải", "vãi thóc"), ("sáng ngời", "con người", "người ta"), ("vũ trụ", "lượn vòng", "sáng ngời")),
       title="Làm việc thật là vui – Trăng sao cũng hóa xứ người",
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Trả lời câu hỏi bằng miệng; chọn chữ ghép được với \"gáy\", điền chỗ trống, ghép chữ "
                            "làm bằng chạm thẻ.")],
       review=[("part1[4]", "đáp án do app chọn: gà gáy, cu gáy"),
               ("part1[5]", "đáp án dạy/dậy theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[6]", "đáp án vang/van theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[7]", "đáp án vải/vãi theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[11]", "ghép \"sáng ngời\", \"chói ngời\" (đứng trước) do app chọn"),
               ("part1[12]", "ghép \"con người\", \"xứ người\", \"người ta\" do app chọn")])

# 336 — Từ ngữ: Thiếu nhi chăm làm (tr.33–34)
TU_336 = ["lao động", "nhà cửa", "lợn gà", "cơm nước", "đỡ đần", "bận rộn", "đến nơi đến chốn"]
lesson(336, [33, 34],
       [title("Từ ngữ: Thiếu nhi chăm làm"),
        title("Những từ ngữ cần ghi nhớ"),
        words("lao động", "nhà cửa", "lợn gà", "cơm nước"),
        words("đỡ đần", "bận rộn", "đến nơi đến chốn"),
        title("Bài tập: Điền từ ngữ thích hợp vào những chỗ trống"),
        fill_passage(["Không những chăm học, bạn Hải còn chăm [lao động] ở trường cũng như ở nhà.",
                      "Buổi sáng đi học về, Hải lại [đỡ đần] bố mẹ mọi việc trong gia đình.",
                      "Bạn thái rau, băm bèo cho [lợn gà].",
                      "Sau đó Hải dọn dẹp [nhà cửa] cho ngăn nắp, gọn gàng.",
                      "Buổi chiều, học bài và làm bài xong, Hải lại lo việc nấu bữa cơm chiều.",
                      "Bố mẹ đi làm đồng về thì [cơm nước] đã sẵn sàng.",
                      "Tuy [bận rộn] suốt ngày, Hải vẫn vui.",
                      "Công việc nào bạn ấy cũng làm [đến nơi đến chốn]."],
                     bank=TU_336),
        q("2. Tìm từ trái nghĩa với bận rộn. Đặt một câu với từ tìm được.")],
       listen(("lao động", "nhà cửa", "lợn gà"), ("nhà cửa", "cơm nước", "đỡ đần"), ("lợn gà", "lao động", "bận rộn"),
              ("cơm nước", "lợn gà", "nhà cửa"), ("đỡ đần", "bận rộn", "cơm nước"), ("bận rộn", "đỡ đần", "lao động")),
       notes=[("khac_sach", "Điền từ bằng chạm hoặc kéo thẻ; thẻ lấy từ các từ ngữ cần ghi nhớ, đáp án do app soạn."),
              ("khac_sach", KS_ORAL)],
       review=[("part1[5]", "đáp án điền từ do app soạn: lao động, đỡ đần, lợn gà, nhà cửa, cơm nước, bận rộn, "
                            "đến nơi đến chốn")])

# 337 — Ngữ pháp: Danh từ chung – Danh từ riêng (tr.34)
lesson(337, [34],
       [title("Ngữ pháp: Danh từ chung – Danh từ riêng"),
        *rule("Nếu cô giáo gọi:", "- Học sinh lên bảng làm toán!",
              "Cả lớp không ai lên bảng cả vì không biết cô giáo gọi ai."),
        *rule("Học sinh là danh từ chỉ người nhưng không chỉ cụ thể người nào nên là danh từ chung."),
        *rule("Nếu cô giáo gọi:", "- Em Nguyễn Văn Hùng lên bảng làm toán.", "Em Hùng liền đi lên bảng."),
        *rule("Nguyễn Văn Hùng là tên riêng của một học sinh."),
        *rule("Những danh từ dùng để chỉ tên riêng của một người gọi là danh từ riêng.",
              "Danh từ riêng phải viết hoa."),
        q("Tìm những danh từ chung và danh từ riêng trong bài \"Ai can đảm\" "
          "(xếp thành 2 cột: một cột danh từ chung, một cột danh từ riêng).")],
       listen(("danh từ chung", "danh từ riêng", "học sinh"), ("danh từ riêng", "danh từ chung", "tên riêng"),
              ("học sinh", "cô giáo", "lên bảng"), ("cô giáo", "học sinh", "làm toán"), ("tên riêng", "viết hoa", "cô giáo"),
              ("viết hoa", "tên riêng", "lên bảng")),
       notes=[("khac_sach", "Bé tìm và xếp danh từ chung, danh từ riêng bằng miệng cùng bố mẹ.")])

# 338 — Tập làm văn: Trả lời câu hỏi — Sao Chổi (tr.34)
lesson(338, [34],
       [title("Tập làm văn: Trả lời câu hỏi"),
        title("Đề bài: Sao Chổi.", "Xem tranh ở bài Sao Chổi."),
        picture(SAO_CHOI, "Con nhớ lại đêm hai anh em ngắm sao Chổi nhé.", "sao Chổi"),
        q("1. Hai anh em Tuấn và Hà làm gì, vào lúc nào?"),
        q("2. Cảnh trời đêm lúc ấy ra sao?"),
        q("3. Sao Chổi hiện ra như thế nào?"),
        q("4. Thấy sao Chổi, bé Hà có ý nghĩ gì?")],
       listen(("sao Chổi", "trời đêm", "hai anh em"), ("trời đêm", "sao Chổi", "ý nghĩ"), ("hai anh em", "ý nghĩ", "trời đêm"),
              ("ý nghĩ", "hai anh em", "sao Chổi"), ("bầu trời", "trời đêm", "ý nghĩ"), ("quét sân", "bầu trời", "hai anh em")),
       images={SAO_CHOI: SAO_CHOI_DESC},
       notes=[("khac_sach", KS_TLC)],
       review=[("part1[2]", "lời dẫn tranh do app soạn")])
print("tuần 21 xong")
