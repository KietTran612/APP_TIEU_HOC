"""Tuần 22 (mục 339–347), tr.35–42, ảnh 013–021."""
from l2t2lib import *

# 339 — Bài 19. Hai con chim (tr.35–36)
HAI_CHIM_1 = ["Mưa rồi, trời mưa to quá!", "Gió ném rào rào từng vốc nước xuống mặt đường.",
              "Gió lay cây rồi giật ra từng nắm lá tung lên trời."]
HAI_CHIM_2 = ["Giữa cảnh ấy, trên cây sấu già kia có hai con chim.", "Con chim bé run rẩy kêu:"]
lesson(339, [35, 36],
       [picture(img(339, "hai con chim"), "Chim lớn che chở cho chim bé dưới trời mưa gió.", "hai con chim"),
        title("Hai con chim"),
        *prose("PHONG THU", HAI_CHIM_1, HAI_CHIM_2, ["- Chíp! Chíp!"], ["Chim lớn dỗ dành:"], ["- Ti ri... ti ri..."],
               ["Không ai biết trên cây sấu ấy có con chim lớn đang che chở cho con chim bé dưới trời mưa gió."],
               ["Sáng hôm sau, khi tia nắng óng ánh vừa rơi xuống chỗ ẩn nấp, con chim lớn mở choàng mắt.",
                "Nó giũ giũ lông cánh cho khô rồi khẽ nhích ra ngoài.",
                "Tia nắng ấm vừa vặn rơi xuống đúng chỗ con chim non đang ngái ngủ, lông cánh vẫn khô nguyên."]),
        q("1. Cảnh mưa to, gió lớn trong bài được tả ở những câu nào, bằng những từ ngữ nào?", marker="?"),
        q("2. Từ nào cho em biết con chim bé bị rét lạnh và sợ hãi? "
          "Từ nào cho em biết con chim lớn rất yêu thương con chim bé?"),
        q("3. Nó giũ giũ lông cánh cho khô. \"Giũ giũ\" khác với \"giũ\" như thế nào?"),
        q("4. Đặt câu với mỗi từ: dỗ dành, che chở.")],
       listen(("cây sấu", "lông cánh", "tia nắng"), ("run rẩy", "dỗ dành", "che chở"), ("dỗ dành", "che chở", "run rẩy"),
              ("che chở", "run rẩy", "ngái ngủ"), ("ngái ngủ", "óng ánh", "rào rào"), ("tia nắng", "cây sấu", "lông cánh")),
       images={img(339, "hai con chim"): "Trời mưa gió: cây sấu già nghiêng ngả, lá bay tung, hạt mưa xiên chéo; trong "
                                         "hốc cây có tổ, con chim lớn xòe cánh che cho con chim bé đang co ro"},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 340 — Bài 20. Tiếng ru (Học thuộc lòng, tr.36–37)
lesson(340, [36, 37],
       [picture(img(340, "tiếng ru"), "Các bạn nhỏ nắm tay nhau thành vòng tròn.", "nắm tay"),
        title("Tiếng ru", "Học thuộc lòng"),
        *sentences("Con ong làm mật yêu hoa", "Con cá bơi, yêu nước; con chim ca, yêu trời.",
                   "Con người muốn sống, con ơi", "Phải yêu đồng chí, yêu người anh em.",
                   "Một ngôi sao chẳng sáng đêm", "Một thân lúa chín, chẳng nên mùa vàng.",
                   "Một người - đâu phải nhân gian,", "Sống chăng, một đốm lửa tàn mà thôi!"),
        passage("poem", "TỐ HỮU", breaks=[4]),
        *glossary("Nhân gian: chỉ tất cả mọi người sống trên trái đất."),
        q("1. Tại sao con ong yêu hoa? Tại sao con cá yêu nước, con chim yêu trời?", marker="?"),
        q("2. Con người muốn sống phải yêu đồng chí, yêu anh em. Vì sao như vậy?"),
        q("*3. Vì sao \"một ngôi sao\" chẳng làm \"sáng đêm\" được? "
          "Vì sao \"một thân lúa chín\" chẳng làm nên \"mùa vàng\" được?"),
        q("4. Con người nếu chỉ có một mình có sống được không? "
          "Em hãy kể những thứ cần thiết hằng ngày mà phải nhờ người khác mới có được."),
        q("5. Bài này khuyên em điều gì?"),
        memorize()],
       listen(("con ong", "con cá", "con chim"), ("làm mật", "mùa vàng", "ngôi sao"), ("ngôi sao", "lúa chín", "con ong"),
              ("lúa chín", "ngôi sao", "nhân gian"), ("nhân gian", "anh em", "mùa vàng"), ("anh em", "đồng chí", "làm mật")),
       images={img(340, "tiếng ru"): "Bãi cỏ dưới gốc cây lớn bên bờ ao, xa xa lũy tre và chim bay: năm bạn nhỏ nắm "
                                     "tay nhau thành vòng tròn, vui vẻ nhảy múa; bên bụi hoa có bướm và ong bay"},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)])

# 341 — Bài 21. Con cáo và tổ ong (tr.38–39)
CAO_ONG = ["Tổ ong lủng lẳng trên cành", "Trong đầy mật nhộng, ngon lành lắm thay!", "Cáo già nhè nhẹ lên cây",
           "Định rằng lấy được ăn ngay cho giòn.", "Ong thấy cáo muốn cướp con", "Kéo nhau xúm lại vây tròn cáo ta.",
           "Châm đầu, châm mắt cáo già", "Cáo già đau quá phải sa xuống rồi.", "Ong kia yêu giống, yêu nòi",
           "Đồng tâm hợp lực đuổi loài cáo đi."]
lesson(341, [38, 39],
       [picture(img(341, "tổ ong"), "Đàn ong xúm lại đuổi con cáo già.", "tổ ong"),
        title("Con cáo và tổ ong"),
        *sentences(*CAO_ONG),
        passage("poem", "BÁC HỒ"),
        q("1. Em kể những nhân vật trong bài thơ này. Nhân vật nào tốt? Nhân vật nào xấu?", marker="?"),
        q("2. Thấy tổ ong, cáo định làm gì? Tại sao nó lại \"nhè nhẹ lên cây\"?"),
        q("3. Ong tuy bé hơn cáo nhưng đã làm thế nào để thắng cáo?"),
        q("4. Em còn nhớ bài thơ nào của Bác Hồ cũng ngụ ý khuyên ta đoàn kết mới có sức mạnh? "
          "(Bài học thuộc lòng tuần 18)"),
        q("5. Em hãy tìm ở bài đó một từ ngữ gần nghĩa với đồng tâm hợp lực.")],
       listen(("tổ ong", "cáo già", "mật nhộng"), ("cáo già", "tổ ong", "lủng lẳng"), ("mật nhộng", "lủng lẳng", "vây tròn"),
              ("lủng lẳng", "nhè nhẹ", "cáo già"), ("nhè nhẹ", "vây tròn", "đồng tâm"), ("đồng tâm", "mật nhộng", "nhè nhẹ")),
       images={img(341, "tổ ong"): "Bên gốc cây to có tổ ong treo lủng lẳng trên cành: con cáo già đang ngã từ trên cây "
                                   "xuống, mấy con ong xúm lại bay quanh đầu cáo; dưới đất có nấm và hoa cỏ"},
       notes=[("sach", "Bài thơ của Bác Hồ; tranh sách vẽ cáo và đàn ong, không vẽ Bác."), ("khac_sach", KS_ORAL)])

# 342 — Bài 22. Cái ổ gà (Bài đọc thêm, tr.39–40; sách không có tranh)
lesson(342, [39, 40],
       [title("Cái ổ gà", "Bài đọc thêm"),
        *prose("HOÀNG ANH ĐƯỜNG",
               ["Chiều nay, Dũng đứng chơi trước cửa chờ đón bố về.", "Dũng nhìn xe cộ và mọi người qua đường.",
                "Một bác chở một bó củi sau xe đạp, | định tránh ổ gà thì một chiếc xe khác ở phía trước xô tới.",
                "Bác luống cuống đưa luôn xe xuống ổ gà.", "Bó củi lọc xọc, đứt dây, rơi vung vãi.",
                "Bác suýt ngã, vội vàng xuống xe, lúng túng nhặt từng que củi.", "Bọn trẻ cứ đứng mà cười."],
               ["Lát sau, một chiếc xe khác lại gặp phải ổ gà; sau xe có một em bé.",
                "Xe xóc mạnh, em bé suýt ngã.", "Bà mẹ tay lái loạng choạng, cũng suýt ngã.",
                "Rồi đường vắng dần, xe qua lại thưa thớt đi."],
               ["Bố về.", "Hết chuyện này đến chuyện khác, cuối cùng Dũng kể cho bố nghe về cái ổ gà.",
                "Dũng chưa kể hết, bố đã hỏi ngay:"],
               ["- Thế con cứ đứng mà xem à? Sao con không lấp nó đi?"],
               ["Dũng đỏ ra!", "Có thế mà cũng không nghĩ đến!", "Dũng ấp úng:"],
               ["- Con quên mất!"],
               ["Dũng vội đi lấy cái xô và cái xẻng con vẫn xúc cát chơi.",
                "Hai bố con ra đến đường thì cái ổ gà tai ác đã được lấp phẳng.",
                "Chắc là một bạn nào đã kể cho bố bạn ấy nghe trước Dũng.", "Dũng thấy tiếc quá!"]),
        *glossary("Ổ gà: chỗ trũng nhỏ trên đường cái.")],
       listen(("ổ gà", "bó củi", "xe đạp"), ("bó củi", "ổ gà", "cái xẻng"), ("cái xẻng", "cái xô", "bó củi"),
              ("luống cuống", "lúng túng", "loạng choạng"), ("lúng túng", "luống cuống", "ấp úng"),
              ("ấp úng", "loạng choạng", "lúng túng")),
       notes=[("khac_sach", KS_SPLIT)])

# 343 — Bài 23. Nhắn chú Phạm Tuân (Bài đọc thêm, tr.40–41; sách không có tranh)
lesson(343, [40, 41],
       [title("Nhắn chú Phạm Tuân", "Bài đọc thêm"),
        *sentences("Cháu chào chú Phạm Tuân", "Chú bay vào vũ trụ", "Có qua bờ sông Ngân", "Mượn sao Gàu về nhé",
                   "Đồng ta lúa đương cần!", "Nếu chú gặp Thần Nông", "Nhớ nói giùm: bà cháu", "Vẫn kể chuyện về ông.",
                   "Khom lưng, ông đương cấy", "Ruộng trên trời... phải không?", "À, chú ơi! Quên mất",
                   "Đàn vịt vàng sông Ngân", "Bắt về mấy con nhé", "Làm giống cho cháu chăn."),
        passage("poem", "TRẦN HỒNG", breaks=[5, 10]),
        *glossary("Chú Phạm Tuân là chiến sĩ lái máy bay, anh hùng quân đội. Chú đã hạ được máy bay B52 của giặc Mĩ. "
                  "Năm 1980 chú đã bay vào vũ trụ cùng với một nhà du hành vũ trụ Liên Xô.",
                  "Sao Gàu: chòm sao giống hình chiếc gàu.",
                  "Vịt: sao Vịt, chòm sao giống hình con vịt ở giữa dải sông Ngân Hà.",
                  "Thần Nông: chòm sao ở về phương Nam, giống hình người đội nón, cúi lom khom như đang cấy.")],
       listen(("vũ trụ", "sông Ngân", "sao Gàu"), ("sông Ngân", "vũ trụ", "đàn vịt"), ("sao Gàu", "Thần Nông", "vũ trụ"),
              ("Thần Nông", "sao Gàu", "ruộng"), ("đàn vịt", "làm giống", "sông Ngân"), ("làm giống", "đàn vịt", "Thần Nông")))

# 344 — Chính tả tuần 22 (tr.41)
lesson(344, [41],
       [title("Chính tả: Hai con chim", "Nghe đọc"),
        title("Bài viết: \"Mưa rồi... Ti ri... ti ri...\".", "Phần này con viết vào vở cùng bố mẹ."),
        words("vốc", "giật", "run rẩy", "chíp", "dỗ dành", "rào rào", "sấu", "ném", "giữa"),
        q("a) Xếp chữ thành câu (bé nói câu cùng bố mẹ):",
          lines=["giật, to, mưa, gió: thành 2 câu, mỗi câu 2 chữ.",
                 "run, rẩy, dỗ, dành, con, mẹ: thành 2 câu, mỗi câu 3 chữ."]),
        fill(["s", "x"], ("cây sấu", "sấu", "s"), ("con cá sấu", "sấu", "s"), ("không nói xấu", "xấu", "x")),
        fill(["ném", "nếm"], ("ném hòn đá", "ném", "ném"), ("nếm thức ăn", "nếm", "nếm")),
        title("Chính tả: Con cáo và tổ ong", "So sánh"),
        *sentences(*CAO_ONG[2:7]),
        title("Bài viết: năm dòng thơ trên.", "Phần này con viết vào vở cùng bố mẹ."),
        words("già", "giòn", "cướp", "xúm", "rằng", "lấy", "châm", "muốn", "mắt"),
        title("Phát âm phân biệt các cặp từ ngữ sau"),
        words("nói rằng", "giằng co", "châm kim", "trâm cài đầu"),
        words("ý muốn", "rau muống", "con mắt", "vướng mắc"),
        q("b) Thêm chữ thích hợp vào các cặp từ so sánh sau đây.", lines=["... vây, vay...", "xúm ..., xóm..."])],
       listen(("cây sấu", "nói xấu", "cá sấu"), ("ném", "nếm", "mưa"), ("nói rằng", "giằng co", "châm kim"),
              ("trâm cài đầu", "châm kim", "ý muốn"), ("rau muống", "ý muốn", "vướng mắc"), ("vướng mắc", "con mắt", "giằng co")),
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Xếp chữ thành câu, thêm chữ: bé nói cùng bố mẹ; cặp từ so sánh thành thẻ chạm để nghe. "
                            "Dấu \"≠\" giữa hai từ trong sách thay bằng dấu phẩy.")],
       review=[("@a) Xếp chữ", "câu gợi ý cho bố mẹ: \"Mưa to. Gió giật.\", \"Con run rẩy. Mẹ dỗ dành.\""),
               ("part1[4]", "đáp án s/x theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[5]", "đáp án ném/nếm theo chính tả chuẩn (sách không in đáp án)")])

# 345 — Từ ngữ: Ôn tập chủ đề Thiếu nhi (tr.42)
lesson(345, [42],
       [title("Từ ngữ: Ôn tập chủ đề Thiếu nhi"),
        q("1. Em hãy tìm những từ ngữ cùng nghĩa hoặc gần nghĩa với các từ:",
          lines=["Đoàn kết, ...", "Dũng cảm, ...", "Chăm chỉ, ..."]),
        q("2. Tìm một số từ ngữ nói lên những nét tốt của thiếu nhi."),
        words("can đảm", "dũng cảm", "gan góc"),
        q("3. Đặt câu với mỗi từ: can đảm, dũng cảm, gan góc."),
        q("*4. Tìm từ trái nghĩa với 3 từ trên.")],
       listen(("đoàn kết", "dũng cảm", "chăm chỉ"), ("dũng cảm", "đoàn kết", "gan góc"), ("chăm chỉ", "can đảm", "thiếu nhi"),
              ("can đảm", "chăm chỉ", "đoàn kết"), ("gan góc", "thiếu nhi", "can đảm"), ("thiếu nhi", "gan góc", "dũng cảm")),
       notes=[("khac_sach", KS_ORAL),
              ("khac_sach", "Ba từ của câu 3 hiện thành thẻ chạm để nghe trước khi đặt câu.")])

# 346 — Ngữ pháp: Danh từ riêng (tr.42)
lesson(346, [42],
       [title("Ngữ pháp: Danh từ riêng"),
        q("1. Em hãy kể tên xã, huyện, tỉnh em đang ở (nếu ở thành phố thì kể tên phường, quận, thành phố)."),
        q("2. Ở nước ta có hai con sông lớn tên là sông Hồng và sông Cửu Long. Em hãy kể tên một con sông khác mà em biết."),
        q("3. Dãy núi dài nhất nước ta tên là Trường Sơn. Kể tên một ngọn núi khác mà em biết."),
        *rule("Tên riêng của đất, núi, sông... cũng gọi là danh từ riêng và phải viết hoa."),
        find("4. Em hãy tìm những danh từ riêng trong bài \"Trên đường đến nhà lao\".",
             {"word": ["côn", "đảo", "bến", "đầm", "sáu"]},
             text=["Bầu trời Côn Đảo trong buổi bình minh rất đẹp.",
                   "Con đường từ Bến Đầm đến nhà lao uốn quanh bờ biển.", "Chị Sáu như say sưa với cảnh tự nhiên."])],
       listen(("sông Hồng", "Cửu Long", "Trường Sơn"), ("Cửu Long", "sông Hồng", "Côn Đảo"), ("Trường Sơn", "Côn Đảo", "Bến Đầm"),
              ("Côn Đảo", "Trường Sơn", "sông Hồng"), ("Bến Đầm", "Cửu Long", "Trường Sơn"), ("danh từ riêng", "viết hoa", "Bến Đầm")),
       notes=[("khac_sach", KS_ORAL),
              ("khac_sach", "Câu 4: app hiện ba câu của bài Trên đường đến nhà lao (câu thứ hai rút ngắn) để bé chạm "
                            "vào danh từ riêng.")],
       review=[("@4. Em hãy tìm", "danh từ riêng do app chọn: Côn Đảo, Bến Đầm, Sáu; câu thứ hai rút ngắn")])

# 347 — Tập làm văn: Trả lời câu hỏi — Tí Xíu (tr.42)
TI_XIU, TI_XIU_DESC = picture_of(331)
lesson(347, [42],
       [title("Tập làm văn: Trả lời câu hỏi"),
        title("Đề bài: Tí Xíu.", "Xem tranh ở bài Tí Xíu."),
        picture(TI_XIU, "Con nhớ lại bạn Tí Xíu chăm làm nhé.", "Tí Xíu"),
        q("1. Tí Xíu đã biết làm những việc gì để giúp gia đình?"),
        q("2. Tí Xíu còn biết làm gì để góp phần giữ nước?"),
        q("3. Như vậy Tí Xíu có còn bé nữa không? Tại sao?"),
        q("4. Em đã làm được những việc gì để giúp nhà và giúp nước?")],
       listen(("Tí Xíu", "gia đình", "giữ nước"), ("gia đình", "Tí Xíu", "giúp nhà"), ("giữ nước", "giúp nhà", "Tí Xíu"),
              ("giúp nhà", "giữ nước", "gia đình"), ("nấu nướng", "gia đình", "giữ nước"), ("cây chông", "nấu nướng", "giúp nhà")),
       images={TI_XIU: TI_XIU_DESC},
       notes=[("khac_sach", KS_TLC)],
       review=[("part1[2]", "lời dẫn tranh do app soạn")])
print("tuần 22 xong")
