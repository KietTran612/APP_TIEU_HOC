"""Tuần 20 (mục 321–329), tr.19–26, ảnh 001, 004, 007, 000, 003."""
from l2t2lib import *

# 321 — Bài 9. Tủ sách của bạn Sắc (tr.19; sách không có tranh)
TU_SACH = img(321, "giá sách")
TU_SACH_DESC = ("Góc phòng nhỏ: cái giá sách nhiều tầng bằng gỗ thông, rèm xanh kéo lên một bên, ba hàng sách xếp "
                "ngay ngắn có thứ tự (truyện, sách khoa học, tập thơ, gáy sách không có chữ); bên cạnh là bàn học "
                "có một quyển sách đang mở (không có người)")
SAC = ["Sắc rất mê sách.", "Những món tiền cậu dành dụm được đều đi vào cửa hàng bán sách.",
       "Bố cậu mua cho cậu một cái giá nhiều tầng bằng gỗ thông, có rèm xanh.",
       "Khi kéo rèm lên, tôi thấy ba hàng sách hiện ra rất có thứ tự.",
       "Sách gồm nhiều loại: truyện thiếu nhi, truyện khoa học, thơ..."]
lesson(321, [19],
       [picture(TU_SACH, "Đây là cái giá sách nhiều tầng của bạn Sắc.", "giá sách"),
        title("Tủ sách của bạn Sắc"),
        *prose("Theo A-MI-XI", SAC,
               ["Sắc rất chăm đọc sách.",
                "Có nhìn cậu giở sách với những ngón tay rất nhẹ nhàng, mới thấy cậu yêu sách như thế nào.",
                "Mỗi quyển sách mua được đem lại cho cậu một niềm vui thích.",
                "Đọc xong cậu còn vuốt ve, ngắm nghía quyển sách rồi mới xếp vào giá như cất đi một của báu."]),
        *glossary("Của báu: của quý, đồ quý."),
        q("1. Sắc thường dùng tiền của mình để làm gì?", marker="?"),
        q("2. Giá sách của Sắc có những nét gì đặc biệt?"),
        q("3. Những câu nào, từ nào cho biết bạn Sắc yêu quý sách của mình?"),
        q("4. Vì sao bạn Sắc lại yêu quý sách như vậy?"),
        q("5. Đặt câu với mỗi từ: dành dụm, tranh giành.")],
       listen(("giá sách", "cửa hàng", "gỗ thông"), ("dành dụm", "vuốt ve", "ngắm nghía"),
              ("vuốt ve", "dành dụm", "nhẹ nhàng"), ("ngắm nghía", "vui thích", "giá sách"),
              ("của báu", "rèm xanh", "gỗ thông"), ("rèm xanh", "của báu", "cửa hàng")),
       images={TU_SACH: TU_SACH_DESC},
       notes=[("khac_sach", "Sách không có tranh; app vẽ giá sách của bạn Sắc để bài Tập làm văn tuần 20 dùng lại."),
              ("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)],
       review=[("part1[0]", "tranh và lời dẫn tranh do app thêm (sách không có tranh)")])

# 322 — Bài 10. Trăng sao cũng hóa xứ người (Học thuộc lòng, tr.20–21)
TRANG_SAO = ["Anh em ơi! Ta tới trăng rồi!", "Trăng sao cũng hóa xứ người từ đây.", "Trạm đầu vũ trụ xinh thay",
             "Nửa quen nửa lạ đặt ngay cờ hồng.", "Mẹ ơi! Mua cốm, mua hồng", "Mua con cá chép lượn vòng con chơi.",
             "Trăng cao, trăng đẹp, trăng ngời", "Mua tàu vũ trụ con ngồi lên trăng."]
lesson(322, [20, 21],
       [picture(img(322, "tàu vũ trụ"), "Em bé ngồi tàu vũ trụ bay lên mặt trăng.", "tàu vũ trụ"),
        title("Trăng sao cũng hóa xứ người", "Học thuộc lòng"),
        *sentences(*TRANG_SAO),
        passage("poem", "HUY CẬN", breaks=[4]),
        *glossary("Bài này nói về việc Liên Xô (trước đây) lần đầu tiên đã phóng con tàu vũ trụ và đặt quốc huy "
                  "có cờ đỏ búa liềm xuống mặt trăng.",
                  "Vũ trụ: chỉ bầu trời và toàn bộ trăng, sao."),
        q("1. Tại sao lại nói \"Trăng sao cũng hóa xứ người từ đây\"?", marker="?"),
        q("*2. Vì sao mặt trăng được coi là \"trạm đầu vũ trụ\"? (xem chú giải)"),
        q("3. Các em nhỏ thường được mẹ mua cốm, mua hồng, mua đèn \"cá chép\" vào dịp nào trong năm? Để làm gì?"),
        q("4. Em bé trong bài còn đòi mẹ mua thêm đồ chơi gì nữa?"),
        q("5. Tìm một từ ghép trong đó có tiếng người."),
        memorize()],
       listen(("mặt trăng", "vũ trụ", "cá chép"), ("vũ trụ", "mặt trăng", "cờ hồng"), ("cá chép", "cốm", "tàu vũ trụ"),
              ("cờ hồng", "cá chép", "mặt trăng"), ("tàu vũ trụ", "cờ hồng", "vũ trụ"), ("cốm", "hồng", "cờ hồng")),
       images={img(322, "tàu vũ trụ"): "Trời đêm có vầng trăng lưỡi liềm: em bé mặc bộ đồ vũ trụ, đội mũ có ăng-ten, "
                                       "vẫy tay, ngồi trên con tàu vũ trụ sơn xanh trắng đang phóng lên, khói trắng "
                                       "phía sau; bên dưới là mái nhà, hàng cây và vài đám mây (không có cờ, không có chữ)"},
       title="Trăng sao cũng hóa xứ người",
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)])

# 323 — Bài 11. Bóc lịch (tr.21–22)
BOC_LICH = ["Em cầm tờ lịch cũ", "- Ngày hôm qua đâu rồi?", "Ra ngoài sân hỏi bố", "Xoa đầu em, bố cười:",
            "- Ngày hôm qua ở lại", "Trên cành hoa trong vườn", "Nụ hồng lớn thêm mãi", "Đợi đến ngày tỏa hương.",
            "- Ngày hôm qua ở lại", "Trong hạt lúa mẹ trồng", "Cánh đồng chờ gặt hái", "Chín vàng màu ước mong.",
            "- Ngày hôm qua ở lại", "Trong vở hồng của con", "Con học hành chăm chỉ", "Là ngày qua vẫn còn..."]
lesson(323, [21, 22],
       [picture(img(323, "tờ lịch"), "Bố xoa đầu em, em cầm tờ lịch cũ.", "tờ lịch"),
        title("Bóc lịch"),
        *sentences(*BOC_LICH),
        passage("poem", "BẾ KIẾN QUỐC", breaks=[4, 8, 12]),
        q("1. Vì sao bố nói: \"Ngày hôm qua ở lại trên cành hoa trong vườn\"? (dựa vào 2 câu tiếp để trả lời)",
          marker="?"),
        q("*2. Vì sao bố nói: \"Ngày hôm qua ở lại, trong hạt lúa mẹ trồng\"? (dựa vào 2 câu tiếp để trả lời)"),
        q("3. Tại sao có thể nói: Em \"học hành chăm chỉ\" là \"ngày qua vẫn còn\"?"),
        q("4. Hãy tìm một số từ ghép chỉ thời gian. Ví dụ: hôm qua..."),
        q("5. Tìm những danh từ chỉ người, cây cối và đồ vật trong bài.")],
       listen(("tờ lịch", "hôm qua", "nụ hồng"), ("hôm qua", "tờ lịch", "cánh đồng"), ("nụ hồng", "hạt lúa", "tờ lịch"),
              ("hạt lúa", "nụ hồng", "vở hồng"), ("vở hồng", "cánh đồng", "hôm qua"), ("cánh đồng", "vở hồng", "hạt lúa")),
       images={img(323, "tờ lịch"): "Trong gian phòng có cửa sổ rèm hoa, chậu hoa hồng có nụ: người bố mặc áo sơ mi "
                                    "trắng cúi xoa đầu cậu con trai; cậu bé cầm một tờ lịch cũ vừa bóc; trên tường "
                                    "treo cuốn lịch bloc, góc phòng có bàn học (tờ lịch không có chữ số)"},
       notes=[("khac_sach", KS_ORAL)])

# 324 — Bài 12. Có một lần (Bài đọc thêm, tr.22–23; sách không có tranh)
lesson(324, [22, 23],
       [title("Có một lần", "Bài đọc thêm"),
        *prose("GÔ-LI-AN-KIN",
               ["Tôi chẳng muốn kể chuyện này vì tôi thấy ngượng quá.",
                "Nhưng dù sao, tôi cũng xin kể để các bạn nghe.",
                "Mọi người đều tưởng là tôi bị đau thật, nhưng có phải là tôi bị sưng bộng răng đâu.",
                "Tôi nhét tờ giấy thấm vào mồm, thế là má sưng phồng lên đấy.",
                "Tôi lại nhăn nhó mặt mũi nữa: ôi, đau răng quá!", "Rồi tôi khẽ rên.",
                "Đấy là tôi cố tình làm thế để không bị gọi đọc bài.", "Cô giáo tin tôi, các bạn cũng tin.",
                "Ai cũng thương tôi và lo lắng.", "Còn tôi thì làm ra vẻ đau lắm.", "Cô giáo nói:"],
               ["- Em đi về nhà đi! Răng đau thế cơ mà!"],
               ["Nhưng tôi không muốn về nhà.",
                "Tôi lấy lưỡi đẩy đi đẩy lại cục giấy thấm trong mồm và nghĩ: | "
                "\"Mình đánh lừa được tất cả mọi người, tài thật!\"."],
               ["Bỗng một cậu bạn hét ầm lên:"],
               ["- Ôi, nhìn kìa, bộng răng sưng của bạn ấy bây giờ chuyển chỗ sang má bên kia rồi."])],
       listen(("giấy thấm", "đau răng", "cô giáo"), ("đau răng", "giấy thấm", "nhăn nhó"), ("nhăn nhó", "lo lắng", "ngượng"),
              ("lo lắng", "nhăn nhó", "đánh lừa"), ("đánh lừa", "lo lắng", "giấy thấm"), ("cô giáo", "cậu bạn", "đau răng")),
       notes=[("khac_sach", KS_SPLIT)])

# 325 — Bài 13. Chiếc dao nóng nảy (Bài đọc thêm, tr.23–24; sách không có tranh)
lesson(325, [23, 24],
       [title("Chiếc dao nóng nảy", "Bài đọc thêm"),
        *prose("F. PÉC-MI-AC (Nga), THÁI BÁ TÂN (dịch)",
               ["Mi-chi-a cầm dao gọt một chiếc gậy, nhưng gọt một chốc, cậu quẳng gậy xuống đất.",
                "Chiếc gậy cong queo, sần sùi, trông thật xấu."],
               ["- Sao con quẳng gậy đi? - Bố hỏi."],
               ["- Tại dao xấu quá, gọt thế nào cũng không trơn - Mi-chi-a đáp."],
               ["- Không! - Bố nói - Dao rất tốt, có điều tính nó nóng nảy.", "Con phải dạy cho nó tập kiên nhẫn."],
               ["- Dạy thế nào ạ? - Mi-chi-a hỏi."],
               ["- Dạy thế này... - bố nói rồi nhặt chiếc gậy lên, cầm dao bắt đầu gọt cẩn thận, nhẹ nhàng, từng tí một."],
               ["Bây giờ Mi-chi-a hiểu phải dạy dao tập kiên nhẫn như thế nào, "
                "và cậu bắt chước bố gọt một cách cẩn thận, nhẹ nhàng, từng tí một."],
               ["Một hồi lâu, chiếc dao nóng nảy không chịu làm theo ý Mi-chi-a.",
                "Bao giờ nó cũng nóng nảy, vội vàng, tìm cách tuột bên này, xén lẹm bên kia, nhưng không được.",
                "Mi-chi-a bắt nó phải kiên nhẫn."],
               ["Dần dần chiếc dao gọt tốt hơn.", "Trơn.", "Đều.", "Đẹp."])],
       listen(("chiếc dao", "chiếc gậy", "kiên nhẫn"), ("kiên nhẫn", "nóng nảy", "cẩn thận"),
              ("nóng nảy", "kiên nhẫn", "cong queo"), ("cẩn thận", "nhẹ nhàng", "sần sùi"),
              ("cong queo", "sần sùi", "chiếc dao"), ("sần sùi", "cong queo", "nhẹ nhàng")),
       notes=[("khac_sach", KS_SPLIT)])

# 326 — Chính tả tuần 20 (tr.24–25)
AI_CAN_DAM_CT = ["Hùng giơ khẩu súng lục ra khoe.", "Thắng vung thanh kiếm lên.",
                 "Đàn ngỗng vươn dài cổ kêu quàng quạc, chúi mỏ định đớp bọn trẻ.",
                 "Hùng chạy biến.", "Thắng mếu máo.", "Tiến nhặt một cành xoan, xua đàn ngỗng ra xa."]
lesson(326, [24, 25],
       [title("Chính tả: Tủ sách của bạn Sắc", "Nghe đọc"),
        title("Bài viết: \"Sắc rất mê sách... truyện khoa học, thơ...\".", "Phần này con viết vào vở cùng bố mẹ."),
        words("dành dụm", "truyện", "loại", "rèm", "tầng", "hàng", "gỗ"),
        fill(["rành", "dành", "giành"], ("để dành tiền", "dành", "dành"), ("đọc rành mạch", "rành", "rành"),
             ("tranh giành", "giành", "giành")),
        fill(["tầng", "tần"], ("nhà hai tầng", "tầng", "tầng"), ("cây cúc tần", "tần", "tần")),
        find("Viết lại những chữ có dấu ngã trong bài.", {"tone": ["ngã"]}, text=SAC),
        title("Chính tả: Ai can đảm", "So sánh"),
        *sentences(*AI_CAN_DAM_CT),
        title("Bài viết: các câu trên.", "Phần này con viết vào vở cùng bố mẹ."),
        words("giơ", "khoe", "quàng quạc", "chúi", "mếu máo", "lên", "trẻ", "xa", "vươn", "biến", "cổ", "mỏ"),
        title("Đọc phân biệt các tiếng in nghiêng trong các cặp từ ngữ sau"),
        words("giơ tay", "dơ bẩn", "trẻ em", "chẻ lạt"),
        words("quàng quạc", "cái quạt", "chúi mỏ", "cây chuối"),
        words("chạy biến", "lười biếng", "mỏ vịt", "gõ mõ")],
       listen(("dành dụm", "rành mạch", "tranh giành"), ("nhà hai tầng", "cây cúc tần", "dành dụm"),
              ("giơ tay", "dơ bẩn", "trẻ em"), ("cái quạt", "quàng quạc", "cây chuối"),
              ("lười biếng", "chạy biến", "gõ mõ"), ("mỏ vịt", "gõ mõ", "chẻ lạt")),
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Điền chỗ trống, tìm chữ có dấu ngã làm bằng chạm thẻ, chạm chữ; cặp từ so sánh thành "
                            "thẻ chạm để nghe và đọc phân biệt.")],
       review=[("part1[3]", "đáp án rành/dành/giành theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[4]", "đáp án tầng/tần theo chính tả chuẩn (sách không in đáp án)")])

# 327 — Từ ngữ: Thiếu nhi chăm học (tr.25)
lesson(327, [25],
       [title("Từ ngữ: Thiếu nhi chăm học"),
        title("Những từ ngữ cần ghi nhớ"),
        words("góc học tập", "bàn học", "giá sách", "sách vở", "truyện thiếu nhi", "truyện khoa học"),
        words("chuyên cần", "chăm chỉ", "chăm chú"),
        title("Bài tập: Điền từ ngữ thích hợp vào những chỗ trống"),
        fill_passage(["Bạn Hải là học sinh giỏi nhất lớp em.", "Bạn ấy đi học rất [chuyên cần|giá sách|bàn học].",
                      "Ở lớp bạn ấy luôn luôn [chăm chú|sách vở|góc học tập] nghe cô giáo giảng bài.",
                      "Ở nhà, Hải cũng [chăm chỉ|giá sách|truyện thiếu nhi] học tập.",
                      "Hải thường ngồi học nghiêm chỉnh ở [góc học tập|chăm chú|truyện khoa học] của mình.",
                      "Trên [bàn học|chuyên cần|chăm chỉ] của bạn ấy, [sách vở|chăm chú|chuyên cần] "
                      "luôn luôn được xếp đặt rất ngăn nắp.",
                      "Ngoài việc học bài, làm bài, Hải còn rất ham đọc sách.",
                      "Trên [giá sách|chăm chỉ|chuyên cần] của bạn ấy có rất nhiều truyện hay.",
                      "Nhiều nhất là hai loại [truyện thiếu nhi|chăm chú|góc học tập] "
                      "và [truyện khoa học|bàn học|chuyên cần]."]),
        q("2. Tìm những từ trái nghĩa với các từ chăm chỉ, chăm học.")],
       listen(("góc học tập", "bàn học", "giá sách"), ("chuyên cần", "chăm chú", "chăm chỉ"),
              ("chăm chú", "chăm chỉ", "chuyên cần"), ("sách vở", "giá sách", "bàn học"),
              ("truyện thiếu nhi", "truyện khoa học", "sách vở"), ("ngăn nắp", "chuyên cần", "góc học tập")),
       notes=[("khac_sach", "Điền từ: mỗi chỗ trống 3 thẻ do app chọn trong các từ ngữ cần ghi nhớ, tránh hai từ cùng "
                            "đúng; đáp án do app soạn."),
              ("khac_sach", KS_ORAL)],
       review=[("part1[5]", "đáp án điền từ do app soạn: chuyên cần, chăm chú, chăm chỉ, góc học tập, bàn học, sách vở, "
                            "giá sách, truyện thiếu nhi, truyện khoa học")])

# 328 — Ngữ pháp: Danh từ (tiếp theo) (tr.25–26)
lesson(328, [25, 26],
       [title("Ngữ pháp: Danh từ", "Tiếp theo"),
        *rule("Cụ già, em bé, bộ đội: chỉ người.", "Mèo, chó, gà, bồ câu: chỉ loài vật.",
              "Cam, ổi, mít, dừa: chỉ cây cối.", "Bàn, ghế, bút chì, sách: chỉ đồ vật."),
        *rule("Từ chỉ người, loài vật, cây cối, đồ vật... gọi là danh từ."),
        q("1. Em hãy tìm những danh từ chỉ người và đồ vật trong bài \"Tủ sách của bạn Sắc\"."),
        q("2. Tìm 1 danh từ chỉ người, 1 danh từ chỉ loài vật, 1 danh từ chỉ đồ vật trong bài "
          "\"Trăng sao cũng hóa xứ người\" (khổ thứ 2).", lines=TRANG_SAO[4:])],
       listen(("cụ già", "em bé", "bộ đội"), ("bồ câu", "con mèo", "con gà"), ("quả cam", "quả mít", "quả ổi"),
              ("bút chì", "cái bàn", "cái ghế"), ("bộ đội", "cụ già", "bồ câu"), ("cây dừa", "bút chì", "em bé")),
       notes=[("khac_sach", "Bảng phân loại danh từ trong sách (có hình cụ già, cây dừa, chim bồ câu, quyển sách) "
                            "thành bốn dòng đọc được; app không vẽ hình."),
              ("khac_sach", KS_ORAL)],
       review=[("part1[1]", "bảng phân loại viết thành dòng \"…: chỉ người\" do app soạn")])

# 329 — Tập làm văn: Trả lời câu hỏi — Tủ sách của bạn Sắc (tr.26)
lesson(329, [26],
       [title("Tập làm văn: Trả lời câu hỏi"),
        title("Đề bài: Tủ sách của bạn Sắc.", "Xem tranh ở bài Tủ sách của bạn Sắc."),
        picture(TU_SACH, "Con nhớ lại giá sách của bạn Sắc nhé.", "giá sách"),
        q("1. Giá sách của bạn Sắc như thế nào?"),
        q("2. Khi kéo rèm lên, em thấy những gì?"),
        q("3. Sách gồm có những loại nào?"),
        q("4. Sắc giữ gìn sách như thế nào? Tại sao như vậy?")],
       listen(("giá sách", "rèm xanh", "quyển sách"), ("rèm xanh", "giá sách", "giữ gìn"), ("quyển sách", "giữ gìn", "rèm xanh"),
              ("giữ gìn", "quyển sách", "giá sách"), ("truyện thiếu nhi", "giữ gìn", "rèm xanh"),
              ("truyện khoa học", "truyện thiếu nhi", "quyển sách")),
       images={TU_SACH: TU_SACH_DESC},
       notes=[("khac_sach", KS_TLC)],
       review=[("part1[2]", "lời dẫn tranh do app soạn")])
print("tuần 20 xong")
