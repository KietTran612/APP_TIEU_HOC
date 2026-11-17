"""Tuần 26 (mục 371–378), tr.62–68, ảnh 032–035."""
from l2t2lib import *

# 371 — Bài 35. Cái máy tuốt lúa (tr.62–63)
MAY_TUOT = img(371, "máy tuốt lúa")
MAY_TUOT_DESC = ("Sân phơi hợp tác xã bên lũy tre và mái kho: mấy bác nông dân đội nón đứng quanh cái máy tuốt lúa, "
                 "ôm từng bó lúa đưa vào máy; thóc vàng tuôn ra thành đống cao như núi, một em bé cầm cào san thóc")
MAY_TUOT_POEM = ["Trông kìa, máy tuốt", "Rung triệu vì sao", "Đầy sân hợp tác", "Thóc vàng xôn xao.",
                 "Máy tròn quay tít", "Núi thóc dần cao", "Máy không biết mệt", "Cười reo rào rào.",
                 "Chú công nhân ơi", "Máy ngoan thật nhỉ", "Suốt cả mùa vui", "Máy thành dũng sĩ."]
lesson(371, [62, 63],
       [picture(MAY_TUOT, "Cái máy tuốt lúa quay tít, thóc vàng đầy sân.", "máy tuốt lúa"),
        title("Cái máy tuốt lúa"),
        *sentences(*MAY_TUOT_POEM),
        passage("poem", "ĐỊNH HẢI", breaks=[4, 8]),
        q("1. Thóc vàng từ chiếc máy tuốt lúa tuôn ra được ví như gì? (khổ 1).", marker="?"),
        q("2. Những câu thơ nào cho em biết máy tuốt lúa cũng được ví như một con người vừa vui tính, vừa chăm làm? "
          "(khổ 2 và 3)."),
        q("3. Ví cái máy tuốt lúa như một con người vui tính và chăm làm chính là muốn nói tới ai ở đây? (khổ 3)."),
        find("4. Tìm hai từ láy diễn tả âm thanh trong bài. Đặt câu với mỗi từ đó.",
             {"word": ["xôn", "xao", "rào"]})],
       listen(("máy tuốt", "thóc vàng", "núi thóc"), ("thóc vàng", "máy tuốt", "hợp tác"), ("xôn xao", "rào rào", "quay tít"),
              ("rào rào", "xôn xao", "dũng sĩ"), ("dũng sĩ", "công nhân", "núi thóc"), ("công nhân", "dũng sĩ", "thóc vàng")),
       images={MAY_TUOT: MAY_TUOT_DESC},
       notes=[("khac_sach", KS_ORAL)],
       review=[("@4. Tìm hai từ láy", "từ láy tả âm thanh do app chọn: xôn xao, rào rào")])

# 372 — Bài 36. Chăm việc cấy cày (Học thuộc lòng, tr.63–64; sách không có tranh)
CAY_CAY = ["- Rủ nhau đi cấy đi cày", "Bây giờ khó nhọc, có ngày phong lưu.",
           "- Ai ơi đừng bỏ ruộng hoang", "Bao nhiêu tấc đất, tấc vàng bấy nhiêu.",
           "- Muốn no thì phải chăm làm", "Một hạt lúa vàng, chín giọt mồ hôi.",
           "- Quanh năm cấy hái cày bừa", "Vụ chiêm tiết hạ, vụ mùa tiết đông.",
           "Ai về nhắn chị em cùng", "Muốn cho no ấm nghề nông chuyên cần."]
lesson(372, [63, 64],
       [title("Chăm việc cấy cày", "Học thuộc lòng"),
        *sentences(*CAY_CAY),
        passage("poem", "Ca dao cổ", breaks=[2, 4, 6]),
        *glossary("Phong lưu: ý nói sống no đủ, sung sướng."),
        q("1. Tại sao \"đi cấy, đi cày\" vất vả, khó nhọc lại \"có ngày phong lưu\"?", marker="?"),
        q("2. Tại sao tấc đất lại quý như tấc vàng?"),
        q("3. Câu \"Một hạt lúa vàng chín giọt mồ hôi\" ý nói gì?"),
        q("4. Muốn cho no ấm quanh năm, nhà nông phải làm lụng như thế nào?"),
        q("5. Một hạt lúa vàng: Thay từ lúa bằng một từ cùng nghĩa."),
        memorize()],
       listen(("ruộng hoang", "tấc đất", "hạt lúa"), ("tấc đất", "ruộng hoang", "mồ hôi"), ("mồ hôi", "hạt lúa", "vụ chiêm"),
              ("vụ chiêm", "vụ mùa", "tấc đất"), ("phong lưu", "khó nhọc", "chuyên cần"), ("chuyên cần", "phong lưu", "nghề nông")),
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)])

# 373 — Bài 37. Đánh cá đèn (tr.64–65)
CA_DEN = img(373, "đánh cá đèn")
CA_DEN_DESC = ("Biển đêm: nhiều thuyền gắn cột đèn điện sáng rực, mặt biển lấp lánh ánh đèn; một con thuyền đang kéo "
               "lưới đầy cá lóc nhóc, phao lưới nổi thành vòng tròn trên sóng")
CA_DEN_CT = ["Thuyền nổ máy ran ran, trườn nhanh qua vùng sóng lừng.", "Nắng chiều tỏa ánh vàng hoe.",
             "Mặt trời lặn.", "Màn đêm buông xuống.", "Đèn điện trên các thuyền bật sáng rực rỡ."]
lesson(373, [64, 65],
       [picture(CA_DEN, "Thuyền đánh cá đèn sáng rực trên biển đêm.", "đánh cá"),
        title("Đánh cá đèn"),
        *prose("BÙI NGUYÊN KHIẾT",
               ["Chiều hôm ấy, bãi biển tấp nập hẳn lên.", "Ai cũng muốn xem các đội thuyền ra khơi đánh cá đèn.",
                "Lũ trẻ cũng theo ra bãi."],
               ["Các thuyền nổ máy ran ran rồi vọt ra khơi, trườn nhanh qua vùng sóng lừng.",
                "Nắng chiều tỏa ánh vàng hoe.", "Màu cầu vồng hiện lên trên bụi nước đầu sóng.", "Mặt trời lặn.",
                "Màn đêm buông xuống.", "Đèn điện trên các thuyền bật sáng rực rỡ.",
                "Vài tiếng đồng hồ sau, thấy ánh đèn, cá kéo về đen đặc.",
                "Những con mối, con nục, nổi lên cuốn vào nhau lúc nhúc.",
                "Dưới ánh điện, mắt chúng sáng rực cả một vùng như trận mưa tàn lửa...",
                "Mỗi thuyền chỉ đánh bốn mẻ lưới mà chở không hết cá, | phải đùn vào lưới thả xuống nước kéo về.",
                "Thuyền nào cũng no, lặc lè trên sóng."]),
        *glossary("Đánh cá đèn: đánh cá về đêm, dùng đèn điện thật sáng để nhử cá tới mà kéo lưới."),
        q("1. Đoàn thuyền máy ra khơi đánh cá trông đẹp mắt. Những từ ngữ nào cho thấy hình ảnh đẹp mắt đó?", marker="?"),
        q("2. Vì sao ánh sáng trên mặt biển lúc đánh cá rực rỡ lên?"),
        q("3. Những từ ngữ nào cho em biết đàn cá rất đông?"),
        q("4. Những từ nào chứng tỏ các thuyền chở cá về rất nặng?"),
        q("5. Đặt câu với mỗi từ: vọt, trườn.")],
       listen(("bãi biển", "cầu vồng", "mẻ lưới"), ("cầu vồng", "bãi biển", "con nục"), ("ran ran", "lúc nhúc", "lặc lè"),
              ("lúc nhúc", "ran ran", "tấp nập"), ("lặc lè", "tấp nập", "lúc nhúc"), ("mẻ lưới", "con nục", "bãi biển")),
       images={CA_DEN: CA_DEN_DESC},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 374 — Bài 38. Làm mưa (Bài đọc thêm, tr.65–66; sách không có tranh)
lesson(374, [65, 66],
       [title("Làm mưa", "Bài đọc thêm"),
        *sentences("Bước lên đồng trên", "Thấy con sông mới.", "Bước xuống đồng dưới", "Thấy con kênh đào.",
                   "Bước ra đồng sau", "Thấy máy bơm nước.", "Bước ra đồng trước", "Thấy guồng đang quay.",
                   "Chẳng mưa từ chín tầng mây,", "Thì mưa từ những bàn tay con người."),
        passage("poem", "BÚT NGỮ", breaks=[8])],
       listen(("con sông", "kênh đào", "máy bơm"), ("kênh đào", "con sông", "guồng quay"), ("máy bơm", "guồng quay", "tầng mây"),
              ("guồng quay", "máy bơm", "bàn tay"), ("tầng mây", "bàn tay", "kênh đào"), ("bàn tay", "tầng mây", "con sông")))

# 375 — Chính tả tuần 26 (tr.66–67)
lesson(375, [66, 67],
       [title("Chính tả: Cái máy tuốt lúa", "Nghe đọc"),
        title("Bài viết: Cả bài.", "Phần này con viết vào vở cùng bố mẹ."),
        words("triệu", "tuốt", "quay", "ngoan", "rung", "rào rào", "suốt", "dũng sĩ"),
        combine_mixed("triệu", ("một", "before"), ("lúa", "after")),
        combine_mixed("tuốt", ("máy", "before"), ("lúa", "after")),
        q("b) Đặt câu với mỗi từ: rung, dũng sĩ, suốt."),
        fill(["quay", "quai"], ("tròn quay", "quay", "quay"), ("quai búa", "quai", "quai"), ("lăn quay", "quay", "quay")),
        fill(["rào", "dào"], ("mưa rào", "rào", "rào"), ("hàng rào", "rào", "rào"), ("dạt dào", "dào", "dào"),
             ("dồi dào", "dào", "dào")),
        title("Chính tả: Đánh cá đèn", "So sánh"),
        *sentences(*CA_DEN_CT),
        title("Bài viết: các câu trên.", "Phần này con viết vào vở cùng bố mẹ."),
        words("ran ran", "trườn", "tỏa", "hoe", "lặn", "rực rỡ", "màn", "buông", "bật", "nổ"),
        title("Phát âm phân biệt các cặp từ ngữ sau"),
        words("nổ ran", "gian nhà", "rực rỡ", "dỡ nhà"),
        words("tỏa ánh sáng", "tần tảo", "đỏ hoe", "con heo"),
        words("trườn lên", "nhà trường", "nổ máy", "nỗ lực"),
        q("b) Thêm chữ thích hợp vào các cặp từ sau.", lines=["lặn..., nặn...", "... bật, ... bậc"])],
       listen(("một triệu", "máy tuốt", "tuốt lúa"), ("tròn quay", "quai búa", "mưa rào"), ("dạt dào", "hàng rào", "dồi dào"),
              ("nổ ran", "gian nhà", "rực rỡ"), ("đỏ hoe", "con heo", "tần tảo"), ("nỗ lực", "nổ máy", "nhà trường")),
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Đặt câu, thêm chữ: bé nói cùng bố mẹ; ghép chữ, điền chỗ trống làm bằng chạm thẻ; cặp từ "
                            "so sánh thành thẻ chạm để nghe. Dấu \"≠\" giữa hai từ trong sách thay bằng dấu phẩy.")],
       review=[("part1[3]", "ghép \"một triệu\", \"triệu lúa\" do app chọn (sách: ghép chữ một, lúa với triệu, tuốt)"),
               ("part1[4]", "ghép \"máy tuốt\", \"tuốt lúa\" do app chọn"),
               ("part1[6]", "đáp án quay/quai theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[7]", "đáp án rào/dào theo chính tả chuẩn (sách không in đáp án)")])

# 376 — Từ ngữ: Nông nghiệp (tr.67)
lesson(376, [67],
       [title("Từ ngữ: Nông nghiệp"),
        title("Những từ ngữ cần ghi nhớ"),
        words("nông dân", "việc cày cấy", "máy cày", "máy bơm nước", "vụ chiêm", "vụ mùa"),
        words("chống úng", "chống hạn", "cày sâu cuốc bẫm", "chân lấm tay bùn"),
        title("Bài tập: Điền từ ngữ thích hợp vào những chỗ trống"),
        fill_passage(["Bà con [nông dân|máy cày|vụ mùa] quanh năm [chân lấm tay bùn|máy bơm nước|vụ chiêm] "
                      "làm ăn vất vả, khó nhọc mới làm ra được hạt thóc hạt gạo.",
                      "Chưa kể một năm hai vụ hết lo [chống úng|máy cày|nông dân] lại lo [chống hạn|vụ mùa|máy cày].",
                      "Nhưng nhờ chịu khó [cày sâu cuốc bẫm|chống úng|máy cày] và ra công chăm bón nên "
                      "cả hai [vụ chiêm|chống hạn|nông dân] và [vụ mùa|máy bơm nước|chống úng] lúa đều tốt cả.",
                      "Nhiều nơi bà con lại sắm được cả [máy cày|vụ chiêm|chống hạn] và [máy bơm nước|vụ mùa|nông dân] "
                      "nên [việc cày cấy|chống úng|vụ mùa] cũng đỡ vất vả hơn."]),
        q("*2. Hãy điền từ cho câu đủ ý:",
          lines=["Vụ... là vụ lúa tháng năm ta.", "Vụ... là vụ lúa tháng mười ta.",
                 "Thành ngữ: \"Tấc đất...\" (Nói như thế nghĩa là thế nào?)",
                 "Gợi ý: dựa vào bài \"Chăm việc cấy cày\" để điền cho đúng."])],
       listen(("nông dân", "máy cày", "vụ chiêm"), ("máy cày", "máy bơm nước", "vụ mùa"), ("vụ chiêm", "vụ mùa", "chống úng"),
              ("chống úng", "chống hạn", "nông dân"), ("chống hạn", "chống úng", "máy cày"), ("vụ mùa", "vụ chiêm", "chống hạn")),
       notes=[("khac_sach", "Điền từ: mỗi chỗ trống 3 thẻ do app chọn trong các từ ngữ cần ghi nhớ, tránh hai từ cùng "
                            "đúng; đáp án do app soạn."),
              ("khac_sach", KS_ORAL)],
       review=[("part1[5]", "đáp án và thẻ chọn do app soạn: nông dân, chân lấm tay bùn, chống úng, chống hạn, "
                            "cày sâu cuốc bẫm, vụ chiêm, vụ mùa, máy cày, máy bơm nước, việc cày cấy")])

# 377 — Ngữ pháp: Cách viết hoa tên đất (tr.67–68)
lesson(377, [67, 68],
       [title("Ngữ pháp: Cách viết hoa tên đất"),
        *rule("Ở sách Tiếng Việt 2, tập một, các em đã gặp các từ chỉ tên riêng như: "
             "Hải Phòng, Ba Vì, Tản Viên, Hồ Gươm."),
        *rule("Hải Phòng là tên một thành phố.", "Ba Vì là tên một huyện.", "Tản Viên là tên một ngọn núi.",
              "Hồ Gươm là tên một cái hồ."),
        *rule("Các danh từ riêng chỉ tên đất đều phải viết hoa chữ cái đầu mỗi tiếng."),
        q("Kể và viết tên riêng của xã, huyện, tỉnh em ở (nếu ở thành phố kể tên phường, quận, thành phố).")],
       listen(("Hải Phòng", "Ba Vì", "Hồ Gươm"), ("Ba Vì", "Tản Viên", "Hải Phòng"), ("Tản Viên", "Hồ Gươm", "Ba Vì"),
              ("Hồ Gươm", "Hải Phòng", "Tản Viên"), ("thành phố", "ngọn núi", "cái hồ"), ("ngọn núi", "thành phố", "Hải Phòng")),
       notes=[("khac_sach", "Kể và viết tên nơi ở: bé nói cùng bố mẹ, viết vào vở.")])

# 378 — Tập làm văn: Dùng từ – đặt câu (tr.68)
lesson(378, [68],
       [title("Tập làm văn: Dùng từ – đặt câu"),
        title("Đề bài: Em hãy dùng mỗi từ ngữ sau đây đặt thành một câu nói về máy tuốt lúa:"),
        words("máy tuốt lúa", "quay tít", "thóc vàng", "cười reo", "ngoan"),
        title("Suy nghĩ trước khi đặt câu"),
        q("1. Ngày nay, nông dân đã dùng máy gì thay việc đập lúa?"),
        q("2. Máy tuốt lúa chạy nhanh như thế nào?"),
        q("3. Máy làm việc khỏe và vui ra sao?"),
        q("4. Khi máy làm việc, em thấy có gì đẹp?"),
        q("5. Tại sao máy được khen là ngoan?")],
       listen(("máy tuốt lúa", "thóc vàng", "quay tít"), ("quay tít", "cười reo", "máy tuốt lúa"),
              ("thóc vàng", "máy tuốt lúa", "ngoan"), ("cười reo", "ngoan", "thóc vàng"), ("ngoan", "quay tít", "cười reo"),
              ("đập lúa", "thóc vàng", "quay tít")),
       notes=[("khac_sach", KS_DAT_CAU)])
print("tuần 26 xong")
