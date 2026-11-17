"""Tuần 30 (mục 403–410), tr.92–99, ảnh 047–050."""
from l2t2lib import *

# 403 — Bài 51. Ông bác sĩ già (tr.92–93)
BAC_SI_2 = ["Đêm ấy, Vân thức dậy mấy lần.",
            "Lần nào Vân cũng thấy cái bóng áo trắng | và những bước chân vội vã của ông đi qua.",
            "Mẹ bảo: \"Đêm nay, có bốn, năm ca cấp cứu. Bác sĩ làm việc suốt đêm!\""]
BAC_SI_3 = ["Đến bây giờ, Vân vẫn không quên được khuôn mặt hiền từ, mái tóc sợi đen sợi trắng, "
            "đôi mắt đầy yêu thương và lo lắng của ông."]
lesson(403, [92, 93],
       [picture(img(403, "bác sĩ"), "Ông bác sĩ già khám bệnh cho bé Vân.", "bác sĩ"),
        title("Ông bác sĩ già"),
        *prose("NGÔ QUÂN MIỆN",
               ["Đêm ấy, bé Vân sốt cao, phải vào bệnh viện.",
                "Em lo lắng nhìn ông bác sĩ già đeo kính trắng, cổ đeo cái ống nghe như chiếc vòng bạc.",
                "Khi khám cho Vân, đôi mày ông cứ nhíu lại như nghĩ ngợi điều gì.",
                "Cuối cùng, đôi mắt ông sáng lên làm mẹ và Vân thấy nhẹ cả người: | \"Cháu bị cảm thôi! Chị cứ yên tâm\"."],
               BAC_SI_2, BAC_SI_3),
        q("1. Khi bác sĩ khám bệnh cho bé Vân, tại sao đôi mày ông lúc đầu \"cứ nhíu lại\", "
          "sau đôi mắt ông lại \"sáng lên\"?", marker="?"),
        q("2. Đêm ấy, mỗi lần Vân thức dậy lại thấy \"những bước chân vội vã\" của ông bác sĩ đi qua. "
          "Em có biết vì sao không?"),
        q("3. Vân không quên được đôi mắt ông \"đầy yêu thương và lo lắng\". Ông yêu thương ai và lo lắng cho ai?"),
        q("*4. Tìm một số từ chỉ những người làm các nghề khác nhau. (Ví dụ: bác sĩ,...).")],
       listen(("bác sĩ", "bệnh viện", "ống nghe"), ("bệnh viện", "bác sĩ", "cấp cứu"), ("ống nghe", "vòng bạc", "bệnh viện"),
              ("cấp cứu", "ống nghe", "bác sĩ"), ("hiền từ", "lo lắng", "vội vã"), ("vội vã", "hiền từ", "yêu thương")),
       images={img(403, "bác sĩ"): "Phòng khám bệnh viện có cửa sổ và lọ hoa: ông bác sĩ già đeo kính trắng, đội mũ "
                                   "trắng, cổ đeo ống nghe, ngồi bên bàn khám cho bé gái Vân; người mẹ ngồi cạnh ôm vai "
                                   "con; trên bàn có lọ mực và đồng hồ"},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 404 — Bài 52. Giọt mồ hôi (Học thuộc lòng, tr.93–94)
lesson(404, [93, 94],
       [picture(img(404, "mồ hôi"), "Bác nông dân lau mồ hôi bên ruộng lúa.", "mồ hôi"),
        title("Giọt mồ hôi", "Học thuộc lòng"),
        *sentences("Mồ hôi mà đổ xuống đồng,", "Lúa mọc trùng trùng sáng cả đồi nương", "Mồ hôi mà đổ xuống vườn,",
                   "Dâu xanh lá tốt vấn vương tơ tằm.", "Mồ hôi mà đổ xuống đầm,", "Cá lội phía dưới, rau nằm phía trên.",
                   "Mồ hôi xuống, cây mọc lên,", "Ăn no, đánh thắng, dân yên, nước giàu."),
        passage("poem", "THANH TỊNH"),
        q("1. \"Giọt mồ hôi\" ở đây ý nói công việc của người nông dân như thế nào?", marker="?"),
        q("2. Sáu câu đầu cho biết mồ hôi của người nông dân đổ xuống những đâu?"),
        q("3. Công việc lao động vất vả đó của họ đã đem lại những kết quả cụ thể gì?"),
        q("*4. Qua hai câu cuối, tác giả cho biết sức lao động của người nông dân đã có tác dụng gì?"),
        q("5. Tìm từ gần nghĩa với các từ: đồng, đầm."),
        memorize()],
       listen(("mồ hôi", "đồi nương", "tơ tằm"), ("đồi nương", "mồ hôi", "dâu xanh"), ("dâu xanh", "tơ tằm", "cá lội"),
              ("tơ tằm", "dâu xanh", "mồ hôi"), ("trùng trùng", "vấn vương", "đồi nương"), ("vấn vương", "trùng trùng", "cá lội")),
       images={img(404, "mồ hôi"): "Buổi trưa nắng gắt, mặt trời chói chang: bác nông dân trẻ mặc áo cộc, quần đùi, "
                                   "tay chống cuốc, đưa tay lau mồ hôi trán; bên cạnh là ruộng lúa trĩu bông, dưới "
                                   "đầm nước có rau bèo nổi phía trên và mấy con cá lội phía dưới"},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)])

# 405 — Bài 53. Một buổi đi thăm đoàn địa chất (tr.94–96)
DIA_CHAT_CT = ["Đèo cao, rừng thẳm.", "Có quãng phải vượt qua rừng song thân lởm chởm gai nhọn.", "Song đan chằng chịt.",
               "Con chó trắng khi leo tới đỉnh núi, toàn thân nó ướt đẫm."]
lesson(405, [94, 95, 96],
       [picture(img(405, "leo núi"), "Đoàn địa chất leo qua đèo cao rừng thẳm.", "leo núi"),
        title("Một buổi đi thăm đoàn địa chất"),
        *prose("ĐINH PHONG NHÃ",
               ["Mới sáng, trời đã bức.", "Rừng bạc thếch, đứng im.", "Trên trời không gợn một bóng mây...",
                "Hôm nay, tôi đi thăm các bộ phận lò, giếng..."],
               ["Đây! Đèo cao, rừng thẳm!", "Con đường đến các bộ phận toàn là rừng với núi.",
                "Có quãng phải vượt qua rừng song, thân lởm chởm gai nhọn.",
                "Song đan chằng chịt như một cái giàn mướp khổng lồ, | muốn vượt qua phải bò cả \"bốn chân\", "
                "hoặc ngồi chồm chỗm xuống, đi như vịt.",
                "Tính cả đi lẫn về, phải vượt qua mười bốn quả núi....",
                "Con chó trắng đi theo chúng tôi, khi leo lên tới đỉnh núi, toàn thân nó ướt đẫm, | "
                "bộ lông xù ướt mèm bết xuống tận da.",
                "Còn tôi, trước khi đi có chặt một cây nhỏ làm gậy, vì biết phải leo qua nhiều núi.",
                "Nhưng leo đến quả núi thứ hai | thì tôi đã cảm thấy cây gậy to và nặng quá.",
                "Để được nhẹ hơn, tôi bóc dần vỏ tươi của cây gậy, | đến lúc sạch nhẵn vẫn thấy nó nặng quá sức mình.",
                "Tôi cởi áo ngoài, quấn ngang bụng.", "Mồ hôi như tắm, chảy vào mồm, vào mắt, mặn đắng, cay xè..."]),
        *glossary("Lò, giếng: các bộ phận thăm dò địa chất dưới lòng đất sâu để tìm quặng.",
                  "Lò: đào xuyên ngang quả núi. Giếng: đào sâu dưới lòng đất."),
        q("1. Trên con đường dẫn đến các bộ phận lò, giếng của đoàn địa chất, tác giả gặp những gì?", marker="?"),
        q("2. Muốn vượt qua một quãng rừng song, tác giả phải đi như thế nào?"),
        q("3. Cả đi lẫn về phải vượt qua bao nhiêu quả núi? Những chi tiết nào chứng tỏ việc leo núi cực kì vất vả, "
          "khó nhọc? (Chú ý chi tiết: con chó trắng, cây gậy nhỏ)."),
        q("4. Câu văn cuối cùng diễn tả sâu sắc nỗi mệt nhọc ghê gớm mà tác giả đã phải chịu đựng. "
          "Em hãy đọc thong thả lại câu đó."),
        q("*5. Đặt câu với mỗi từ: ướt đẫm, ướt sũng.")],
       listen(("địa chất", "rừng song", "đèo cao"), ("rừng song", "địa chất", "giàn mướp"), ("đèo cao", "rừng thẳm", "cây gậy"),
              ("cây gậy", "đèo cao", "rừng song"), ("lởm chởm", "chằng chịt", "chồm chỗm"), ("chằng chịt", "lởm chởm", "ướt đẫm")),
       images={img(405, "leo núi"): "Sườn núi dốc giữa rừng rậm, gốc cây lớn và bụi song gai: hai người đoàn địa chất "
                                    "đội mũ, đeo ba lô, chống gậy leo lên dốc đá, người đi trước giơ tay kéo người đi "
                                    "sau; con chó trắng chạy lên phía trước"},
       notes=[("khac_sach", "Chú thích \"Lò, giếng\" tách làm hai dòng cho vừa màn."),
              ("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 406 — Bài 54. Ai mạnh nhất trên đời (Bài đọc thêm, tr.96–97; sách không có tranh)
lesson(406, [96, 97],
       [title("Ai mạnh nhất trên đời", "Bài đọc thêm"),
        *prose("Theo Truyện cổ Kiếc-ghi, VŨ PHƯỢNG NGỌC lược dịch",
               ["Chú gà rừng đến bờ sông để tìm nước uống cho đỡ khát.",
                "Chú ta tìm được một chỗ nước chưa đóng băng tròn như cái đĩa.",
                "Chú uống cho đến lúc đôi cánh cũng bị băng đóng cứng đờ."],
               ["- Ô! Băng! Anh thật mạnh biết bao!"],
               ["- Không đâu gà rừng ạ! Mưa còn mạnh hơn mình nhiều. | Hắn làm mình tan ra thành nước đấy."],
               ["Mưa nói:"], ["- Không, đất mạnh hơn chứ! Mình vừa rơi xuống, hắn đã nuốt chửng."],
               ["- Cây mạnh hơn tôi nhiều. - Đất phân trần - | Hắn đứng ở trên người tôi và hút hết sức mạnh của tôi."],
               ["Cây lắc đầu:"],
               ["- Không! Lửa mới có sức mạnh ghê gớm. | Hắn thở những lưỡi lửa dài và thiêu tớ thành tro."],
               ["- Đúng, nhưng chàng Gió lại có thể dập tắt được tớ. - Lửa khiêm tốn đáp lại."],
               ["Gió chậm rãi nói:"],
               ["- Mình có thể dập tắt lửa, nhưng các bạn xem, | chàng Cỏ nhóc vẫn đứng hiên ngang trong gió bão.",
                "Cỏ mới xứng đáng là kẻ mạnh nhất."],
               ["Cỏ xua tay từ chối:"], ["- Tôi mà mạnh à? Bác Cừu đến chén tôi ngon ơ, các bạn ạ!"],
               ["Cừu kêu to:"],
               ["- Không! Không! | Người có thể bắt gà rừng, làm tan băng, tắm trong mưa, cày đất, cưa đổ cây, "
                "dập tắt lửa, bắt gió làm việc cho họ, | cắt cỏ và ăn thịt cả tôi nữa đấy!",
                "Người đúng là mạnh nhất trên đời."])],
       listen(("gà rừng", "đóng băng", "cái đĩa"), ("đóng băng", "gà rừng", "gió bão"), ("cái đĩa", "lưỡi lửa", "đóng băng"),
              ("lưỡi lửa", "cái đĩa", "gà rừng"), ("hiên ngang", "khiêm tốn", "chậm rãi"), ("khiêm tốn", "hiên ngang", "phân trần")),
       notes=[("khac_sach", KS_SPLIT)])

# 407 — Chính tả tuần 30 (tr.97–98)
lesson(407, [97, 98],
       [title("Chính tả: Ông bác sĩ già", "Nghe đọc"),
        title("Bài viết: \"Đêm ấy... của ông\".", "Phần này con viết vào vở cùng bố mẹ."),
        words("dậy", "suốt", "khuôn", "Vân", "trắng", "cứu", "mặt", "vội vã"),
        combine_mixed("suốt", ("đêm", "after"), ("trong", "before")),
        combine("khuôn mặt", "trái xoan"),
        fill(["cứu", "kíu"], ("cấp cứu", "cứu", "cứu"), ("nghiên cứu", "cứu", "cứu"), ("ngỗng kêu kíu kíu", "kíu", "kíu")),
        fill(["mặt", "mặc"], ("rửa mặt", "mặt", "mặt"), ("ăn mặc gọn gàng", "mặc", "mặc")),
        title("Chính tả: Một buổi đi thăm đoàn địa chất", "So sánh"),
        *sentences(*DIA_CHAT_CT),
        title("Bài viết: các câu trên.", "Phần này con viết vào vở cùng bố mẹ."),
        words("quãng", "chằng chịt", "lởm chởm", "toàn", "đẫm", "rừng", "song", "đan", "ướt", "đỉnh"),
        title("Phát âm phân biệt các cặp từ ngữ sau"),
        words("rừng núi", "dừng lại", "cây song", "làm xong bài"),
        words("đan áo len", "đang làm việc", "ướt đẫm", "ước mơ"),
        words("quãng đường đi", "quảng trường", "đỉnh núi", "đĩnh đạc"),
        q("b) Thêm chữ thích hợp vào cặp từ sau đây.", lines=["... chằng chịt, ... chăn len."])],
       listen(("suốt đêm", "trong suốt", "trái xoan"), ("cấp cứu", "nghiên cứu", "kíu kíu"), ("rửa mặt", "ăn mặc", "cấp cứu"),
              ("rừng núi", "dừng lại", "cây song"), ("đan áo", "đang làm", "ướt đẫm"), ("quãng đường", "quảng trường", "đỉnh núi")),
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Ghép chữ, điền chỗ trống làm bằng chạm thẻ; thêm chữ: bé nói cùng bố mẹ; cặp từ so sánh "
                            "thành thẻ chạm để nghe. Dấu \"≠\" thay bằng dấu phẩy.")],
       review=[("part1[3]", "ghép \"suốt đêm\", \"trong suốt\" do app chọn"),
               ("part1[4]", "ghép \"khuôn mặt trái xoan\" do app chọn"),
               ("part1[5]", "đáp án cứu/kíu theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[6]", "đáp án mặt/mặc theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[17]", "chữ in mờ: app đọc là \"đĩnh đạc\" (cặp hỏi/ngã)")])

# 408 — Từ ngữ: Ôn tập chủ đề Nhân dân ta (tr.98)
lesson(408, [98],
       [title("Từ ngữ: Ôn tập chủ đề Nhân dân ta"),
        q("1. Em hãy kể tên một số nghề của người công nhân. Ví dụ: công nhân điện, công nhân xây dựng, v.v..."),
        q("2. Qua bài từ ngữ về công nghiệp đã học, em hiểu người thợ giỏi là người như thế nào? "
          "Tìm trong bài từ ngữ về giao thông vận tải một từ gần nghĩa với từ \"thợ giỏi\"."),
        q("3. Hãy kể một số công việc đồng áng mà các bác nông dân thường làm."),
        q("*4. Tìm một thành ngữ (trong bài từ ngữ về nông nghiệp đã học) nói lên nỗi vất vả, khó nhọc của người "
          "nông dân trong việc làm ra hạt thóc hạt gạo. Nêu thêm một vài thành ngữ khác, nếu em biết."),
        words("yêu nước thương dân", "dũng cảm", "nắm chắc tay súng"),
        q("5. Đặt câu với mỗi từ ngữ sau đây nói về anh bộ đội: yêu nước thương dân, dũng cảm, nắm chắc tay súng.")],
       listen(("công nhân", "nông dân", "bộ đội"), ("nông dân", "công nhân", "thợ giỏi"), ("thợ giỏi", "lành nghề", "bộ đội"),
              ("lành nghề", "thợ giỏi", "nông dân"), ("dũng cảm", "yêu nước thương dân", "nắm chắc tay súng"),
              ("đồng áng", "dũng cảm", "lành nghề")),
       notes=[("khac_sach", KS_ORAL),
              ("khac_sach", "Các từ ngữ của câu 5 hiện thành thẻ chạm để nghe trước khi đặt câu.")])

# 409 — Ngữ pháp: Tập xếp tên người theo thứ tự bảng chữ cái (tiếp theo) (tr.99)
lesson(409, [99],
       [title("Ngữ pháp: Tập xếp tên người theo thứ tự bảng chữ cái", "Tiếp theo"),
        *rule("1. Những trường hợp không thể dựa vào chữ cái, không thể dựa vào họ hoặc chữ lót "
             "để xếp thứ tự thì làm thế nào?",
             "Ví dụ: Nguyễn Văn Hàn, Nguyễn Văn Hán, Nguyễn Văn Hãn."),
        *rule("Trong trường hợp này, người ta dựa vào dấu thanh để xếp theo thứ tự:",
              "Thanh ngang (không dấu), thanh huyền, thanh hỏi,", "thanh ngã, thanh sắc, thanh nặng."),
        *rule("Vì vậy, ta xếp 3 tên trên theo thứ tự Hàn, Hãn, Hán."),
        q("2. Em hãy xếp tên các bạn sau đây theo thứ tự bảng chữ cái:",
          lines=["Minh, Phùng, Kha, Định, Mạnh,", "Khả, Đính, Phụng, Phương, Đinh."])],
       listen(("thanh ngang", "thanh huyền", "thanh hỏi"), ("thanh ngã", "thanh sắc", "thanh nặng"),
              ("thanh hỏi", "thanh ngã", "thanh ngang"), ("dấu thanh", "chữ cái", "thứ tự"), ("Hàn", "Hãn", "Hán"),
              ("Hán", "Hàn", "Hãn")),
       notes=[("khac_sach", "Danh sách sáu thanh (sách in mỗi thanh một dòng kèm dấu) gộp thành hai dòng. " + KS_XEP_TEN)])

# 410 — Tập làm văn: Dùng từ – đặt câu (tr.99)
lesson(410, [99],
       [title("Tập làm văn: Dùng từ – đặt câu"),
        title("Đề bài: Em hãy dùng mỗi từ ngữ sau đây đặt thành 2 câu nói về người thầy thuốc:"),
        words("bác sĩ", "yêu thương", "cấp cứu"),
        title("Suy nghĩ trước khi đặt câu"),
        q("1. Ở bệnh viện, ai khám bệnh cho các em?"),
        q("2. Các bác sĩ thường dùng vật gì để khám bệnh?"),
        q("3. Vì sao các bác sĩ hết lòng chăm sóc người bệnh?"),
        q("4. Nêu một ví dụ cho thấy tấm lòng đầy yêu thương của các bác sĩ?"),
        q("5. Khi nào các bác sĩ phải làm việc suốt đêm?"),
        q("6. Vì sao gặp những ca cấp cứu, các bác sĩ phải làm việc vất vả?")],
       listen(("bác sĩ", "yêu thương", "cấp cứu"), ("yêu thương", "bác sĩ", "bệnh viện"), ("cấp cứu", "bệnh viện", "bác sĩ"),
              ("bệnh viện", "cấp cứu", "ống nghe"), ("ống nghe", "bác sĩ", "người bệnh"), ("người bệnh", "ống nghe", "yêu thương")),
       notes=[("khac_sach", KS_DAT_CAU)])
print("tuần 30 xong")
