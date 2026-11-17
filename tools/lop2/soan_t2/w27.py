"""Tuần 27 (mục 379–386), tr.69–75, ảnh 035–038."""
from l2t2lib import *

# 379 — Bài 39. Đàn bê của anh Hồ Giáo (tr.69–70)
DAN_BE = img(379, "đàn bê")
DAN_BE_DESC = ("Đồng cỏ xanh dưới chân núi Ba Vì, trời cao vút có mây trắng: đàn bê sữa lông đen trắng ăn cỏ, "
               "mấy con bê đực nhảy quẩng đuổi nhau, hai con bê cái đứng rụt rè bên bụi hoa (không có người)")
DAN_BE_CT = ["Giống như những đứa trẻ quấn quýt bên cạnh mẹ, đàn bê cứ quẩn vào chân anh.",
             "Chúng vừa ăn vừa đùa nghịch.",
             "Những con bê đực, y hệt những em bé trai khỏe mạnh, | chốc chốc lại ngừng ăn, nhảy quẩng lên "
             "rồi chạy đuổi nhau thành một vòng tròn chung quanh Giáo..."]
lesson(379, [69, 70],
       [picture(DAN_BE, "Đàn bê ăn cỏ, chạy nhảy trên đồng cỏ Ba Vì.", "đàn bê"),
        title("Đàn bê của anh Hồ Giáo"),
        *prose("PHƯỢNG VŨ",
               ["Bây giờ đã sang tháng ba.", "Đồng cỏ Ba Vì vẫn giữ nguyên vẻ đẹp như hồi đầu xuân.",
                "Không khí trong lành và rất ngọt ngào.", "Bầu trời cao vút, trập trùng những đám mây trắng..."],
               ["Giáo đứng trên đồng cỏ đã lâu lắm.", "Đàn bê ăn quanh quẩn ở bên anh."],
               DAN_BE_CT + ["Những con bê cái thì khác hẳn.",
                            "Chúng rụt rè chẳng khác nào những em bé gái được bà chiều, | lúc nào cũng chăm bẵm "
                            "không dám cho chạy đi chơi xa....",
                            "Chúng ăn nhỏ nhẹ, từ tốn.",
                            "Thỉnh thoảng một con, chừng như nhớ mẹ, chạy lại chỗ Giáo, dụi mõm vào người anh nũng nịu.",
                            "Con khó tính hay vòi cứ sán vào lòng Giáo | rồi quơ quơ đôi chân lên như là đòi bế."]),
        *glossary("Hồ Giáo: anh hùng lao động ngành chăn nuôi.", "Chăm bẵm: chăm chút (trẻ nhỏ) từng li từng tí."),
        q("1. Đồng cỏ Ba Vì đẹp như thế nào? (không khí, bầu trời).", marker="?"),
        q("2. Những từ quanh quẩn, quấn quýt, quẩn cho em biết tình cảm của đàn bê đối với anh Hồ Giáo ra sao? "
          "Em đặt câu với mỗi từ đó."),
        q("3. Những con bê đực vừa ăn, vừa đùa nghịch như thế nào?"),
        q("4. Những con bê cái khác hẳn chúng. Em hãy tìm những từ ngữ cho biết điều đó."),
        q("5. Tìm trong bài một danh từ riêng chỉ họ và tên người, một danh từ riêng chỉ tên đất. "
          "*Em hãy cho biết cách viết những danh từ riêng đó.")],
       listen(("đàn bê", "đồng cỏ", "bê đực"), ("đồng cỏ", "đàn bê", "bê cái"), ("quấn quýt", "quanh quẩn", "nũng nịu"),
              ("nũng nịu", "rụt rè", "quấn quýt"), ("rụt rè", "từ tốn", "nhảy quẩng"), ("trập trùng", "ngọt ngào", "rụt rè")),
       images={DAN_BE: DAN_BE_DESC},
       notes=[("khac_sach", KS_REAL.format(who="anh hùng lao động Hồ Giáo vuốt ve đàn bê",
                                           what="đàn bê trên đồng cỏ Ba Vì")),
              ("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)],
       review=[("part1[0]", "tranh thay hình anh Hồ Giáo (người thật); lời dẫn tranh do app soạn")])

# 380 — Bài 40. Trâu ơi (Học thuộc lòng, tr.70–72)
lesson(380, [70, 71, 72],
       [picture(img(380, "con trâu"), "Bác nông dân vuốt ve con trâu bên ruộng lúa.", "con trâu"),
        title("Trâu ơi", "Học thuộc lòng"),
        *sentences("Trâu ơi, ta bảo trâu này,", "Trâu ra ngoài ruộng, trâu cày với ta.", "Cấy cày vốn nghiệp nông gia,",
                   "Ta đây trâu đấy, ai mà quản công!", "Bao giờ cây lúa còn bông,",
                   "Thời còn ngọn cỏ ngoài đồng trâu ăn."),
        passage("poem", "Ca dao"),
        *glossary("Nghiệp: nghề nghiệp.", "Nông gia: nhà nông, người làm nghề cày cấy.",
                  "Quản công: ngại khó nhọc, vất vả (ngại tốn công sức)."),
        q("1. Người nông dân gọi \"trâu ơi\" và tự xưng là \"ta\". "
          "Cách xưng hô đó cho biết tình cảm của họ đối với con trâu ra sao?", marker="?"),
        q("2. Người nông dân nhắn nhủ, động viên trâu cùng chịu khó vất vả trong nghề cày cấy với mình qua hai câu nào? "
          "\"Ai mà quản công\" ý nói gì? (dựa vào mục chú thích để trả lời)"),
        q("3. Qua hai câu cuối, người nông dân hứa với trâu điều gì?"),
        q("4. Đặt câu với mỗi từ: công sức, công lao."),
        memorize()],
       listen(("con trâu", "ngoài ruộng", "cây lúa"), ("ngoài ruộng", "con trâu", "ngọn cỏ"), ("cây lúa", "ngọn cỏ", "nông gia"),
              ("ngọn cỏ", "cây lúa", "cấy cày"), ("nông gia", "cấy cày", "quản công"), ("quản công", "nông gia", "con trâu")),
       images={img(380, "con trâu"): "Bờ ruộng lúa quê có cây chuối, xa xa lũy tre và chim bay: bác nông dân mặc áo nâu, "
                                     "vấn khăn, một tay cầm thừng, một tay vuốt ve con trâu đang gặm cỏ"},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)])

# 381 — Bài 41. Phân xưởng gà con (tr.72–73)
lesson(381, [72, 73],
       [picture(img(381, "gà con"), "Cô công nhân điều chỉnh lồng sưởi cho đàn gà con.", "gà con"),
        title("Phân xưởng gà con"),
        *prose("DUY LẬP",
               ["Vừa bước vào khu nhà nuôi gà con, chúng tôi đã thấy một cuộc sum vầy đông đúc của hàng nghìn gà con."],
               ["Những tiếng chiêm chiếp non nớt quấn quýt rất dễ thương.", "Có lúc chúng lại rộ lên, ríu rít thật vui.",
                "Chúng ở tập trung từng cụm, dưới những lồng sưởi dòng từ trần nhà xuống.",
                "Những lồng sưởi điện này hình sáu cạnh, múi xanh, múi trắng.",
                "Chúng có đường kính rộng hai mét, treo úp.",
                "Lồng sưởi tỏa nhiệt xuống đàn gà con đứng dưới, cách xa gần một mét."],
               ["Một cô công nhân rón rén đến bên lồng sưởi điều chỉnh độ nhiệt.",
                "Lũ gà, con đứng, con nằm thoải mái."]),
        *glossary("Phân xưởng: một bộ phận sản xuất của nhà máy. Trong nhà máy nuôi gà có nhiều phân xưởng "
                  "như phân xưởng gà con, phân xưởng gà choai, phân xưởng gà đẻ...",
                  "Ở đây gà đẻ không ấp trứng và nuôi con (trứng gà được ấp bằng điện để nở thành gà con)."),
        q("1. Ở nhà em, gà con thường đi với gà mẹ, ở đây tại sao không có gà mẹ?", marker="?"),
        q("2. Tìm các từ tả những nét đáng yêu của đàn gà con."),
        q("3. Tại sao gà con lại thích ở tập trung từng cụm dưới lồng sưởi điện?"),
        q("4. Tìm một từ ghép có tiếng \"sum\" ở đầu và cùng nghĩa với từ \"sum vầy\". Đặt một câu với từ đó."),
        q("5. Tìm trong bài 3 danh từ chung (chỉ người, loài vật, đồ vật).")],
       listen(("gà con", "lồng sưởi", "phân xưởng"), ("lồng sưởi", "gà con", "công nhân"), ("chiêm chiếp", "ríu rít", "non nớt"),
              ("ríu rít", "chiêm chiếp", "rón rén"), ("sum vầy", "đông đúc", "thoải mái"), ("rón rén", "thoải mái", "sum vầy")),
       images={img(381, "gà con"): "Trong nhà nuôi gà sáng sủa có cửa sổ lớn: cô công nhân đội khăn, mặc áo kẻ sọc, "
                                   "đeo tạp dề, đi ủng, đang điều chỉnh chiếc lồng sưởi điện hình sáu cạnh múi xanh "
                                   "múi trắng treo úp; bên dưới hàng chục chú gà con lông vàng tụ thành cụm"},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 382 — Bài 42. Chị công nhân chăn bò (Bài đọc thêm, tr.73–74; sách không có tranh)
lesson(382, [73, 74],
       [title("Chị công nhân chăn bò", "Bài đọc thêm"),
        *sentences("Chị là con gái miền xuôi,", "Lên chăn bò sữa núi đồi Sa Pa.", "Đồi bát ngát, núi bao la,",
                   "Đây là Thác Bạc, kia là Cầu Mây.", "Cỏ hương, cỏ sữa mọc đầy,", "Đường đi, con suối lượn ngay chân đèo.",
                   "Hàng sa mu đứng nhìn theo,", "Đêm khuya, một mảnh trăng treo trên ngàn.",
                   "Nhìn đàn bò sữa nông trường", "Trắng, đen, lang, đốm trong sương hiện dần.",
                   "Càng yêu mến chị công nhân,", "Đẹp như một đóa hoa xuân núi rừng."),
        passage("poem", "TẾ HANH"),
        *glossary("Sa mu: một loại cây giống cây thông.")],
       listen(("bò sữa", "đồi núi", "Thác Bạc"), ("Thác Bạc", "Cầu Mây", "bò sữa"), ("bát ngát", "bao la", "con suối"),
              ("bao la", "bát ngát", "sa mu"), ("sa mu", "con suối", "nông trường"), ("nông trường", "sa mu", "Cầu Mây")),
       notes=[("khac_sach", "\"Sa Pa\" không dùng làm phương án nghe (mã tu_sa_pa đã có ở lớp 1 với lời đọc khác).")])

# 383 — Chính tả tuần 27 (tr.74)
lesson(383, [74],
       [title("Chính tả: Đàn bê của anh Hồ Giáo", "Nghe đọc"),
        title("Bài viết: \"Giống như... chung quanh Giáo\".", "Phần này con viết vào vở cùng bố mẹ."),
        words("giống", "quấn quýt", "nghịch", "quẩng", "trẻ", "chốc", "đuổi", "những", "nhảy"),
        combine_mixed("giống", ("nhau", "after"), ("hệt", "after")),
        combine_mixed("quẩng", ("nhảy", "before"), ("lên", "after")),
        q("b) Đặt câu với mỗi từ: quấn quýt, nghịch."),
        fill(["chốc", "trốc"], ("một chốc", "chốc", "chốc"), ("cây bị trốc rễ", "trốc", "trốc")),
        fill(["đuổi", "dũi"], ("theo đuổi", "đuổi", "đuổi"), ("đánh đuổi", "đuổi", "đuổi"),
             ("bộ quần áo bằng vải dũi", "dũi", "dũi")),
        title("Chính tả: Chăm việc cấy cày", "Trí nhớ"),
        title("Bài viết: 3 cặp câu đầu.", "Phần này con viết vào vở cùng bố mẹ."),
        words("ruộng", "hoang", "bao nhiêu", "rủ", "lưu", "tấc đất", "bỏ"),
        q("a) Đặt câu với mỗi từ: hoang, bao nhiêu."),
        fill(["rủ", "dủ"], ("rủ nhau đi học", "rủ", "rủ"), ("dủ lòng thương", "dủ", "dủ")),
        fill(["tấc", "tất"], ("một tấc đất", "tấc", "tấc"), ("tất cả mọi người", "tất", "tất")),
        fill(["bỏ", "bõ"], ("bỏ dở công việc", "bỏ", "bỏ"), ("chẳng bõ công làm", "bõ", "bõ"))],
       listen(("giống nhau", "giống hệt", "nhảy quẩng"), ("một chốc", "trốc rễ", "theo đuổi"), ("đánh đuổi", "vải dũi", "một chốc"),
              ("rủ nhau", "dủ lòng", "tấc đất"), ("tất cả", "tấc đất", "bỏ dở"), ("chẳng bõ", "bỏ dở", "rủ nhau")),
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Đặt câu: bé nói cùng bố mẹ; ghép chữ, điền chỗ trống làm bằng chạm thẻ.")],
       review=[("part1[3]", "ghép \"giống nhau\", \"giống hệt\" do app chọn (sách in \"nhau, hệt\")"),
               ("part1[4]", "ghép \"nhảy quẩng\", \"quẩng lên\" do app chọn"),
               ("part1[6]", "đáp án chốc/trốc theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[7]", "đáp án đuổi/dũi theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[12]", "đáp án rủ/dủ theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[13]", "đáp án tấc/tất theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[14]", "đáp án bỏ/bõ theo chính tả chuẩn (sách không in đáp án)")])

# 384 — Từ ngữ: Chăn nuôi (tr.75)
lesson(384, [75],
       [title("Từ ngữ: Chăn nuôi"),
        title("Những từ ngữ cần ghi nhớ"),
        words("nông trường chăn nuôi", "đồng cỏ", "bò", "bê"),
        words("bao la", "bát ngát", "quấn quýt", "chăm bẵm"),
        title("Bài tập: Điền từ thích hợp vào những chỗ trống"),
        fill_passage(["Chị Vân là công nhân chăn bò ở [nông trường chăn nuôi|đồng cỏ|bao la] Cẩm Thủy.",
                      "Nông trường có khu [đồng cỏ|chăm bẵm|quấn quýt] rộng [bao la|bò|bê].",
                      "Hằng ngày, hàng trăm con [bò|chăm bẵm|bao la] và [bê|quấn quýt|đồng cỏ] béo tốt "
                      "mang đủ màu lông, được thả cho ăn cỏ ở đây trông rất thích mắt.",
                      "Mấy chú [bê|bao la|chăm bẵm] con chẳng chịu đi ăn xa cứ [quấn quýt|bát ngát|đồng cỏ] bên chị Vân.",
                      "Chị [chăm bẵm|bát ngát|đồng cỏ] chúng chẳng khác gì các con nhỏ của chị ở nhà.",
                      "Mỗi buổi sáng, chỉ có đứng ở đây cùng với đàn bê, chị Vân mới ngắm nhìn được toàn cảnh "
                      "nông trường xanh tươi [bát ngát|quấn quýt|chăm bẵm] vô cùng thân thiết."]),
        q("*2. Tìm một số từ gần nghĩa với các từ: bát ngát, chăm bẵm.")],
       listen(("đồng cỏ", "bò", "bê"), ("bao la", "bát ngát", "quấn quýt"), ("quấn quýt", "chăm bẵm", "bao la"),
              ("chăm bẵm", "quấn quýt", "đồng cỏ"), ("bát ngát", "bao la", "chăm bẵm"), ("nông trường chăn nuôi", "đồng cỏ", "bê")),
       notes=[("khac_sach", "Điền từ: mỗi chỗ trống 3 thẻ do app chọn trong các từ ngữ cần ghi nhớ, tránh hai từ cùng "
                            "đúng; đáp án do app soạn."),
              ("khac_sach", KS_ORAL)],
       review=[("part1[5]", "đáp án và thẻ chọn do app soạn: nông trường chăn nuôi, đồng cỏ, bao la, bò, bê, bê, "
                            "quấn quýt, chăm bẵm, bát ngát")])

# 385 — Ngữ pháp: Ôn cách viết hoa danh từ riêng (tr.75)
lesson(385, [75],
       [title("Ngữ pháp: Ôn cách viết hoa danh từ riêng"),
        q("1. Viết lại cho đúng các danh từ riêng sau đây:",
          lines=["nguyễn văn trỗi, nguyễn thị minh khai, hải phòng,", "hà nội, trần quốc toản, kim đồng,",
                 "ba vì, tản viên, nha trang, cửu long."]),
        choose("2. Xếp các danh từ riêng ở trên thành 2 cột: một cột chỉ tên người, một cột chỉ địa danh. "
               "Con chạm vào các tên người.",
               ["Nguyễn Văn Trỗi", "Nguyễn Thị Minh Khai", "Hải Phòng", "Hà Nội", "Trần Quốc Toản", "Kim Đồng",
                "Ba Vì", "Tản Viên", "Nha Trang", "Cửu Long"], [0, 1, 4, 5]),
        q("3. Viết tên trường em học và tên 5 bạn trong lớp (viết cả họ và tên).")],
       listen(("Hải Phòng", "Hà Nội", "Nha Trang"), ("Hà Nội", "Hải Phòng", "Cửu Long"), ("Ba Vì", "Tản Viên", "Kim Đồng"),
              ("Kim Đồng", "Ba Vì", "Hà Nội"), ("Cửu Long", "Nha Trang", "Tản Viên"), ("Nha Trang", "Cửu Long", "Ba Vì")),
       notes=[("khac_sach", "Viết lại tên riêng, viết tên trường và tên bạn: bé nói cách viết hoa cùng bố mẹ; "
                            "xếp 2 cột thành chạm vào các tên người (app hiện tên đã viết hoa).")],
       review=[("part1[2]", "đáp án tên người do app chọn: Nguyễn Văn Trỗi, Nguyễn Thị Minh Khai, Trần Quốc Toản, "
                            "Kim Đồng")])

# 386 — Tập làm văn: Dùng từ – đặt câu (tr.75)
lesson(386, [75],
       [title("Tập làm văn: Dùng từ – đặt câu"),
        title("Đề bài: Em hãy dùng mỗi từ ngữ sau đây đặt thành một câu nói về đàn bê của anh Hồ Giáo:"),
        words("đàn bê", "đồng cỏ", "quấn quýt", "bê đực", "nũng nịu"),
        title("Suy nghĩ trước khi đặt câu"),
        q("1. Anh Hồ Giáo đang làm gì?"),
        q("2. Anh cho đàn bê ăn ở đâu?"),
        q("3. Đàn bê mến anh như thế nào?"),
        q("4. Những con bê đực vừa ăn cỏ vừa làm gì?"),
        q("5. Trái lại, những con bê cái vừa ăn cỏ vừa làm gì?")],
       listen(("đàn bê", "đồng cỏ", "bê đực"), ("đồng cỏ", "đàn bê", "nũng nịu"), ("quấn quýt", "nũng nịu", "đàn bê"),
              ("bê đực", "bê cái", "quấn quýt"), ("nũng nịu", "quấn quýt", "đồng cỏ"), ("bê cái", "bê đực", "đồng cỏ")),
       notes=[("khac_sach", KS_DAT_CAU)])
print("tuần 27 xong")
