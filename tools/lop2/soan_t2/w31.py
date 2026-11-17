"""Tuần 31 (mục 411–418), tr.101–107, ảnh 051–054 (tr.100 là trang chủ điểm "Bác Hồ")."""
from l2t2lib import *

# 411 — Bài 55. Có những mùa đông (tr.101; sách không có tranh)
MUA_DONG_2 = ["Lại có những mùa đông, Bác Hồ sống ở Pa-ri, thủ đô nước Pháp, | "
              "Bác trọ trong một khách sạn rẻ tiền ở xóm lao động.",
              "Buổi sáng, trước khi đi làm, Bác để một viên gạch vào bếp lò.",
              "Tối về Bác lấy viên gạch ra, bọc nó vào một tờ giấy báo cũ, để xuống dưới nệm nằm cho đỡ lạnh."]
lesson(411, [101],
       [title("Có những mùa đông"),
        *prose("TRẦN DÂN TIÊN",
               ["Có một mùa đông, Bác Hồ sống bên nước Anh.", "Lúc ấy Bác còn trẻ.",
                "Bác làm việc cào tuyết trong một trường học để có tiền sinh sống.", "Công việc này rất mệt nhọc.",
                "Mình Bác đẫm mồ hôi, nhưng tay chân thì lạnh cóng.", "Sau tám giờ làm việc, Bác vừa mệt, vừa đói."],
               MUA_DONG_2),
        *glossary("Tuyết: ở những xứ lạnh, khi trời rét quá, hơi nước đông lại và rơi xuống mặt đất, xốp và trắng.",
                  "Tuyết rơi xuống làm cho đường sá rất trơn và khó đi lại. "
                  "Người ta phải cào tuyết thành từng đống để lấy lối đi.",
                  "Khách sạn: ngôi nhà lớn để cho khách nghỉ trọ và ăn uống."),
        q("1. Lúc ở nước Anh, Bác Hồ phải làm nghề gì để sinh sống?", marker="?"),
        q("2. Câu văn nào diễn tả nỗi vất vả, mệt nhọc của Bác khi cào tuyết?"),
        q("3. Lúc ở Pa-ri (nước Pháp), Bác phải làm gì để chống rét?"),
        q("4. Tìm những từ gần nghĩa với lạnh."),
        q("*5. Bác Hồ đi các nước để làm gì?")],
       listen(("mùa đông", "cào tuyết", "khách sạn"), ("cào tuyết", "mùa đông", "viên gạch"), ("khách sạn", "viên gạch", "bếp lò"),
              ("viên gạch", "bếp lò", "giấy báo"), ("lạnh cóng", "mệt nhọc", "mồ hôi"), ("mệt nhọc", "lạnh cóng", "mùa đông")),
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 412 — Bài 56. Nhớ ơn Bác Hồ (Học thuộc lòng, tr.102–103)
lesson(412, [102, 103],
       [picture(img(412, "bầu trời sao"), "Bầu trời đêm đầy sao trên rặng cây.", "vì sao"),
        title("Nhớ ơn Bác Hồ", "Học thuộc lòng"),
        *sentences("Đố ai đếm được lá rừng", "Đố ai đếm được mấy từng trời cao", "Đố ai đếm đủ vì sao",
                   "Đố ai đếm được công lao Bác Hồ.", "Bác Hồ là vị Cha chung", "Là sao Bắc Đẩu, là vừng thái dương."),
        passage("poem", "Ca dao", breaks=[4]),
        *glossary("Sao Bắc Đẩu: tên một chòm sao trong đó có sao Bắc Cực ở đúng phương bắc, "
                  "giúp cho người ta tìm được phương hướng về ban đêm.",
                  "Ở đây ý nói Bác Hồ là người vạch ra phương hướng cho cách mạng Việt Nam đi đến thắng lợi.",
                  "Thái dương: mặt trời."),
        q("1. Trong bốn câu thơ đầu, \"đố ai\" được nhắc lại 4 lần nhằm nhấn mạnh ý. "
          "Em hãy đọc lại và nhấn giọng ở những từ đó.", marker="?"),
        q("2. Tác giả ví công lao không kể xiết của Bác Hồ đối với nhân dân ta với những gì?"),
        q("3. Tại sao lại ví Bác Hồ với sao Bắc Đẩu, với vừng thái dương?"),
        q("4. Đặt câu với mỗi từ: công lao, công ơn."),
        memorize()],
       listen(("lá rừng", "vì sao", "trời cao"), ("vì sao", "lá rừng", "thái dương"), ("công lao", "công ơn", "vì sao"),
              ("công ơn", "công lao", "lá rừng"), ("thái dương", "Bắc Đẩu", "công lao"), ("trời cao", "thái dương", "công ơn")),
       images={img(412, "bầu trời sao"): "Bầu trời đêm đen thẫm đầy những vì sao lấp lánh, một chòm sao sáng rõ; "
                                         "bên phải là mấy cây cọ, cây dừa in bóng (không có người)"},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)])

# 413 — Bài 57. Bác Hồ ở chiến khu (tr.103–104)
CHIEN_KHU = img(413, "nhà sàn")
CHIEN_KHU_DESC = ("Chiến khu Việt Bắc: một ngôi nhà sàn đơn sơ vách nứa, mái lá, nép giữa rừng cọ, tre và đá; "
                  "bên cạnh có dòng suối chảy, cá bơi; trong nhà có ánh lửa hồng hắt ra (không có người)")
CHIEN_KHU_POEM = ["Một nhà sàn đơn sơ vách nứa,", "Bốn bên suối chảy cá bơi vui.", "Đêm đêm cháy hồng bên bếp lửa,",
                  "Ánh đèn khuya còn sáng trên đồi.", "Nơi đây sống một người tóc bạc,", "Người không con mà có triệu con.",
                  "Nhân dân ta gọi Người là Bác,", "Cả đời Người là của nước non."]
lesson(413, [103, 104],
       [picture(CHIEN_KHU, "Ngôi nhà sàn đơn sơ bên suối ở chiến khu.", "nhà sàn"),
        title("Bác Hồ ở chiến khu"),
        *sentences(*CHIEN_KHU_POEM),
        passage("poem", "NGUYỄN ĐÌNH THI", breaks=[4]),
        *glossary("Chiến khu: khu căn cứ của ta trong cuộc kháng chiến chống bọn xâm lược Pháp.",
                  "Đây là chiến khu Việt Bắc, nơi Bác Hồ và Trung ương đã ở từ năm 1947 đến 1954.",
                  "Nhà sàn: một kiểu nhà của đồng bào miền núi có sàn cao cho người ở để tránh ẩm thấp và thú dữ."),
        q("1. Hình ảnh nào cho em biết, ở chiến khu, Bác sống rất giản dị?", marker="?"),
        q("2. Bác đã làm việc suốt ngày đêm không biết mệt mỏi. Những câu thơ nào cho em biết điều đó?"),
        q("3. \"Người không con mà có triệu con\". Triệu con đây là ai?"),
        q("*4. Em hiểu câu \"Cả đời Người là của nước non\" ý nói gì?"),
        q("5. Từ đêm và đêm đêm có nghĩa khác nhau như thế nào? Tìm một vài từ láy giống như thế.")],
       listen(("nhà sàn", "vách nứa", "bếp lửa"), ("vách nứa", "nhà sàn", "suối chảy"), ("bếp lửa", "đèn khuya", "vách nứa"),
              ("đèn khuya", "bếp lửa", "nước non"), ("chiến khu", "nước non", "nhà sàn"), ("nước non", "chiến khu", "suối chảy")),
       images={CHIEN_KHU: CHIEN_KHU_DESC},
       notes=[("khac_sach", "Tranh sách vẽ nhà sàn ở chiến khu, không có người; app vẽ lại cảnh đó."),
              ("khac_sach", KS_ORAL)])

# 414 — Bài 58. Một que diêm (Bài đọc thêm, tr.104–105; sách không có tranh)
lesson(414, [104, 105],
       [title("Một que diêm", "Bài đọc thêm"),
        *prose("VŨ TRỌNG TÂM",
               ["Sau khi đến thăm nhà câu lạc bộ, nhà ăn và ra xem chuồng lợn, Bác đi vào nhà bếp.",
                "Thấy đồng chí Hào, tổ trưởng anh nuôi của đơn vị | đang bê một nồi cơm to từ trên bếp lò xuống, "
                "Bác vui vẻ hỏi:"],
               ["- Mỗi bữa chú ăn được mấy bát?"], ["- Thưa Bác, cháu ăn được ba bát ạ!"], ["Bác thân mật nói tiếp:"],
               ["- Chú ăn được như vậy là tốt!"], ["Nói xong, Bác mở hộp thuốc lá lấy một điếu đưa cho Hào:"],
               ["- Bác biếu chú, hút đi!"], ["Rồi Bác lấy một điếu khác ra để hút."],
               ["Thấy Bác đang tìm đóm để châm lửa, Hào nhanh nhẹn rút bao diêm trong túi áo mình ra, | "
                "lấy một que định quẹt lửa mời Bác.", "Bác liền giơ tay ngăn lại:"],
               ["- Chú để dành diêm mà nhóm bếp. Bác châm lửa ở trong lò cũng được."], ["Ngừng một lát, Bác hỏi Hào:"],
               ["- Chú có biết phải qua tay bao nhiêu người mới làm ra một que diêm không?"], ["- Thưa Bác có ạ!"],
               ["Bác ân cần nhắc nhở:"],
               ["- Vì vậy mỗi khi dùng một que diêm, | chúng ta cũng phải nghĩ tới công sức của bao nhiêu người!"])],
       listen(("que diêm", "bao diêm", "nhà bếp"), ("bao diêm", "que diêm", "nồi cơm"), ("nồi cơm", "nhà bếp", "bếp lò"),
              ("bếp lò", "nồi cơm", "que diêm"), ("ân cần", "thân mật", "nhanh nhẹn"), ("thân mật", "ân cần", "công sức")),
       notes=[("khac_sach", KS_SPLIT)],
       review=[("part1[0]", "bài có chi tiết mời nhau hút thuốc lá (đúng sách): chủ dự án xem có giữ bài đọc thêm này")])

# 415 — Chính tả tuần 31 (tr.105–106)
lesson(415, [105, 106],
       [title("Chính tả: Có những mùa đông", "Nghe đọc"),
        title("Bài viết: \"Lại có những... đỡ lạnh\".", "Phần này con viết vào vở cùng bố mẹ."),
        words("trọ", "khách sạn", "bếp", "rẻ", "cũ", "Bác Hồ", "Pa-ri", "Pháp", "nệm"),
        q("a) Viết các tên riêng trong bài theo thứ tự bảng chữ cái."),
        fill(["nệm", "niệm"], ("tấm nệm", "nệm", "nệm"), ("giường trải nệm", "nệm", "nệm"), ("kỉ niệm", "niệm", "niệm")),
        fill(["bếp", "bép"], ("củi nổ lép bép", "bép", "bép"), ("bắc nồi lên bếp", "bếp", "bếp")),
        fill(["cũ", "củ"], ("tờ báo cũ", "cũ", "cũ"), ("cây cải củ", "củ", "củ")),
        title("Chính tả: Em muốn lái máy bay", "Trí nhớ"),
        title("Bài viết: \"Em muốn... biển nắng\".", "Phần này con viết vào vở cùng bố mẹ."),
        words("máy", "miễn", "xăng", "quay", "chứa", "chừng", "muốn", "hót", "nổ", "đổ"),
        fill(["máy", "mấy"], ("máy bay", "máy", "máy"), ("mấy phút", "mấy", "mấy"), ("máy cày", "máy", "máy"),
             ("mấy giờ", "mấy", "mấy")),
        fill(["quay", "quai"], ("tròn quay", "quay", "quay"), ("quai nón", "quai", "quai"), ("quay phim", "quay", "quay"),
             ("quai dép", "quai", "quai")),
        fill(["ch", "tr"], ("lưng chừng trời", "chừng", "ch"), ("bị trừng phạt", "trừng", "tr")),
        fill(["n", "ng"], ("muốn ăn rau", "muốn", "n"), ("rau muống", "muống", "ng"))],
       listen(("tấm nệm", "kỉ niệm", "lép bép"), ("bắc nồi", "tờ báo cũ", "cải củ"), ("máy bay", "mấy phút", "máy cày"),
              ("mấy giờ", "máy cày", "quai nón"), ("quay phim", "quai dép", "tròn quay"), ("lưng chừng", "trừng phạt", "rau muống")),
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Viết tên riêng theo thứ tự: bé nói cùng bố mẹ; chọn chữ, điền chỗ trống làm bằng chạm thẻ. "
                            "Câu \"muốn ăn rau muống phải lội xuống ao\" tách thành hai thẻ ngắn.")],
       review=[("part1[4]", "đáp án nệm/niệm theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[5]", "đáp án bếp/bép do app chọn: củi nổ lép bép, bắc nồi lên bếp"),
               ("part1[6]", "đáp án cũ/củ do app chọn: tờ báo cũ, cây cải củ"),
               ("part1[10]", "ghép máy/mấy do app chọn: máy bay, mấy phút, máy cày, mấy giờ"),
               ("part1[11]", "ghép quay/quai do app chọn: tròn quay, quai nón, quay phim, quai dép"),
               ("part1[12]", "đáp án ch/tr theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[13]", "đáp án n/ng theo chính tả chuẩn (sách không in đáp án)")])

# 416 — Từ ngữ: Ôn tập cuối năm: Nhà trường, gia đình (tr.106)
lesson(416, [106],
       [title("Từ ngữ: Ôn tập cuối năm: Nhà trường, gia đình"),
        q("1. Em hãy tìm những danh từ chỉ tên các phòng và các khu vực dành cho việc học tập, lao động "
          "và giải trí trong trường học của em."),
        words("chuyên cần", "chăm chỉ", "lễ phép", "khiêm tốn"),
        q("2. Tìm một số từ ngữ nói về các nết tốt của một học sinh ngoan. "
          "Đặt câu với mỗi từ sau đây: chuyên cần, chăm chỉ, lễ phép, khiêm tốn."),
        q("3. Hãy kể những người trong gia đình, họ hàng có quan hệ thân thiết, ruột thịt với nhau."),
        words("đùm bọc", "hòa thuận"),
        q("4. Người trong một gia đình phải sống với nhau như thế nào? Đặt câu với mỗi từ sau đây: đùm bọc, hòa thuận."),
        q("*5. Nhắc lại một thành ngữ đã học về mối tình cảm thương yêu, đùm bọc lẫn nhau trong một gia đình "
          "(hoặc trong một tập thể)? (Bài từ ngữ về Gia đình, tuần 6)")],
       listen(("chuyên cần", "chăm chỉ", "lễ phép"), ("lễ phép", "khiêm tốn", "chuyên cần"), ("khiêm tốn", "lễ phép", "đùm bọc"),
              ("đùm bọc", "hòa thuận", "chăm chỉ"), ("hòa thuận", "đùm bọc", "khiêm tốn"), ("chăm chỉ", "chuyên cần", "hòa thuận")),
       notes=[("khac_sach", KS_ORAL),
              ("khac_sach", "Các từ để đặt câu của câu 2 và câu 4 hiện thành thẻ chạm để nghe."),
              ("sach", "Câu 5 nhắc bài Từ ngữ \"Gia đình\" tuần 6 (Tiếng Việt 2 tập một).")])

# 417 — Ngữ pháp: Tóm tắt cách xếp tên người theo thứ tự bảng chữ cái (tr.107)
lesson(417, [107],
       [title("Ngữ pháp: Tóm tắt cách xếp tên người theo thứ tự bảng chữ cái"),
        *rule("1. Căn cứ vào chữ đầu, chữ thứ 2, chữ thứ 3 của tên người để xếp thứ tự (xem bài tuần 28).",
              "2. Trường hợp trùng tên thì căn cứ vào họ và chữ lót để xếp thứ tự (xem bài tuần 29).",
              "3. Ngoài ra, người ta còn dựa vào thứ tự dấu thanh để xếp thứ tự trước sau (xem bài tuần 30)."),
        q("4. Học sinh chia làm 2 nhóm, mỗi nhóm tập xếp thứ tự họ tên các bạn trong nhóm của mình theo các bài đã học "
          "(mỗi nhóm có thể gồm 2 tổ).")],
       listen(("chữ đầu", "chữ lót", "dấu thanh"), ("chữ lót", "chữ đầu", "họ tên"), ("dấu thanh", "họ tên", "chữ đầu"),
              ("họ tên", "dấu thanh", "chữ lót"), ("thứ tự", "chữ cái", "dấu thanh"), ("chữ cái", "thứ tự", "họ tên")),
       notes=[("khac_sach", "Phần tập xếp tên theo nhóm: bé làm cùng bố mẹ, anh chị (sách cho cả lớp chia nhóm).")])

# 418 — Tập làm văn: Dùng từ – đặt câu (tr.107)
lesson(418, [107],
       [title("Tập làm văn: Dùng từ – đặt câu"),
        title("Đề bài: Dựa vào bài tập đọc \"Có những mùa đông\", em hãy dùng mỗi từ ngữ sau đây "
              "đặt thành hai câu nói về Bác Hồ kính yêu:"),
        words("cào tuyết", "viên gạch", "công lao"),
        title("Suy nghĩ trước khi đặt câu"),
        q("1. Hồi còn trẻ ở nước Anh, Bác sống bằng nghề gì?"),
        q("2. Nghề cào tuyết nặng nhọc như thế nào?"),
        q("3. Hồi ở Pháp, mùa đông Bác làm cách nào để nằm cho ấm?"),
        q("4. Bác đặt viên gạch ở đâu?"),
        q("5. Vì sao nhân dân ta vô cùng biết ơn Bác?"),
        q("6. Câu ca dao nào em đã học nói lên công lao to lớn của Bác?")],
       listen(("cào tuyết", "viên gạch", "công lao"), ("viên gạch", "cào tuyết", "mùa đông"), ("công lao", "mùa đông", "cào tuyết"),
              ("mùa đông", "công lao", "viên gạch"), ("bếp lò", "giấy báo", "công lao"), ("giấy báo", "bếp lò", "mùa đông")),
       notes=[("khac_sach", KS_DAT_CAU)])
print("tuần 31 xong")
