"""Tuần 18 (mục 305–312), tr.4–10, ảnh 010–016."""
from l2t2lib import *

# 305 — Bài 1. Câu chuyện bó đũa (tr.4–5)
BO_DUA = img(305, "bó đũa")
BO_DUA_DESC = ("Trong gian nhà xưa: ông già râu tóc bạc mặc áo the ngồi trên ghế gỗ, tay giơ bó đũa; "
               "bốn người con trai đứng quanh chiếc bàn gỗ, trên bàn có một túi tiền buộc dây")
lesson(305, [4, 5],
       [picture(BO_DUA, "Ông già cầm bó đũa, bốn người con đứng quanh.", "bó đũa"),
        title("Câu chuyện bó đũa"),
        *prose("Truyện ngụ ngôn Việt Nam",
               ["Ngày xưa có một ông già sinh được bốn người con.",
                "Một hôm, ông để một bó đũa và một túi tiền trên bàn | rồi gọi các con lại và bảo:"],
               ["- Trong các con, ai bẻ gãy được bó đũa này thì cha thưởng cho túi tiền."],
               ["Các người con lần lượt bẻ, ai cũng cố hết sức mà không sao bẻ gãy được bó đũa."],
               ["Ông già bèn cởi bó đũa ra, rồi bẻ gãy từng chiếc một cách dễ dàng."],
               ["Bốn người con cùng nói:"],
               ["- Thưa cha, lấy từng chiếc mà bẻ thì có khó gì!"],
               ["Ông già liền bảo:"],
               ["- Đúng! Như thế là các con đều thấy rằng chia lẻ ra thì yếu, hợp lại thì mạnh.",
                "Vậy các con phải biết hợp quần và đùm bọc lấy nhau, có hợp quần thì mới có sức mạnh."]),
        *glossary("Hợp quần: hợp lại với nhau thành một khối vững chắc, đoàn kết chặt chẽ với nhau."),
        q("1. Một chiếc đũa, một đôi đũa, một bó đũa có gì khác nhau?", marker="?"),
        q("2. Tại sao bốn người con không ai bẻ gãy được bó đũa?"),
        q("3. Ông già bẻ gãy bó đũa bằng cách nào?"),
        q("4. Bài này khuyên ta điều gì?"),
        q("5. \"Ông già\" là một từ chỉ người. Em hãy tìm một số từ khác cũng chỉ người.")],
       listen(("bó đũa", "túi tiền", "người con"), ("túi tiền", "bó đũa", "sức mạnh"),
              ("hợp quần", "đùm bọc", "dễ dàng"), ("đùm bọc", "hợp quần", "lần lượt"),
              ("lần lượt", "dễ dàng", "túi tiền"), ("sức mạnh", "người con", "đùm bọc")),
       images={BO_DUA: BO_DUA_DESC},
       notes=[("khac_sach", KS_NO_SPELL), ("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 306 — Bài 2. Hòn đá to (Học thuộc lòng, tr.5–6)
lesson(306, [5, 6],
       [picture(img(306, "hòn đá"), "Nhiều người cùng khiêng hòn đá to.", "hòn đá"),
        title("Hòn đá to", "Học thuộc lòng"),
        *sentences("Hòn đá to", "Hòn đá nặng", "Chỉ một người", "Nhấc không đặng.",
                   "Hòn đá nặng", "Hòn đá bền", "Chỉ ít người", "Nhấc không lên.",
                   "Hòn đá to", "Hòn đá nặng", "Nhiều người nhấc", "Nhấc lên đặng.",
                   "Biết đồng sức", "Biết đồng lòng,", "Việc gì khó", "Làm cũng xong."),
        passage("poem", "HỒ CHÍ MINH", breaks=[4, 8, 12]),
        *glossary("Đặng: được."),
        q("1. Bài thơ nói: \"Chỉ một người\", \"Chỉ ít người\", và \"Nhiều người\". "
          "Cách nói như thế có gì khác nhau? (Cho ví dụ)", marker="?"),
        q("2. Số người như thế nào thì nhấc được hòn đá to lên? Tại sao nhấc được?"),
        q("3. Em hiểu thế nào là đồng sức, đồng lòng? "
          "Cho ví dụ một công việc cần phải có nhiều người đồng sức, đồng lòng mới làm được."),
        q("4. Trong bài này, Bác Hồ khuyên chúng ta điều gì?"),
        q("*5. Hòn đá là từ chỉ vật. Em hãy tìm một số từ khác cũng chỉ vật."),
        memorize()],
       listen(("hòn đá", "đồng sức", "nhấc lên"), ("đồng sức", "hòn đá", "việc khó"),
              ("đồng lòng", "nhấc lên", "hòn đá"), ("nhấc lên", "đồng lòng", "làm xong"),
              ("làm xong", "đồng sức", "nhấc lên"), ("việc khó", "làm xong", "đồng lòng")),
       images={img(306, "hòn đá"): "Bãi đất có bụi cỏ và cành cây: bốn người đàn ông mặc áo lao động cùng nhau "
                                   "khiêng một hòn đá to, ai cũng gắng sức; bên cạnh một người đứng cúi xuống "
                                   "cố nhấc một hòn đá khác mà không lên (không có chữ)"},
       notes=[("sach", "Bài thơ của Bác Hồ; tranh sách vẽ những người cùng khiêng đá, không vẽ Bác."),
              ("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)])

# 307 — Bài 3. Không sống riêng lẻ (tr.7–8)
KIEN = ["Hễ kiếm được mồi", "Kiến tha về tổ", "Xếp cùng một chỗ", "Làm của cải chung", "Tới khi đói lòng",
        "Cùng ăn vui sướng.", "Từ quân đến tướng", "Một dạ như nhau", "Chẳng thấy ở đâu", "Kiến sống riêng lẻ."]
lesson(307, [7, 8],
       [picture(img(307, "đàn kiến"), "Đàn kiến cùng nhau tha mồi về tổ.", "đàn kiến"),
        title("Không sống riêng lẻ"),
        *sentences(*KIEN),
        passage("poem", "NAM HƯƠNG"),
        q("1. Khi kiếm được mồi, kiến làm gì?", marker="?"),
        q("2. Đàn kiến có tính tốt gì?"),
        q("3. Em hãy tìm một từ khác thay cho từ dạ trong câu \"Một dạ như nhau\"."),
        q("4. Trái nghĩa với riêng lẻ là gì?"),
        q("5. \"Kiến\" là một từ chỉ loài vật. Em hãy tìm một số từ khác cũng chỉ loài vật.")],
       listen(("con kiến", "tổ kiến", "kiếm mồi"), ("riêng lẻ", "vui sướng", "của cải"),
              ("của cải", "riêng lẻ", "đói lòng"), ("đói lòng", "của cải", "như nhau"),
              ("vui sướng", "đói lòng", "tổ kiến"), ("như nhau", "vui sướng", "riêng lẻ")),
       images={img(307, "đàn kiến"): "Trên bãi cỏ dưới chân đồi: một đàn kiến đen xếp hàng cùng nhau tha một con "
                                     "cào cào to về tổ, vài con kiến khác khiêng hạt thóc theo sau; xa xa có dãy "
                                     "núi thấp và vài đám mây"},
       notes=[("khac_sach", KS_ORAL)])

# 308 — Bài 4. Xe lu và xe ca (Bài đọc thêm, tr.8; sách không có tranh)
lesson(308, [8],
       [title("Xe lu và xe ca", "Bài đọc thêm"),
        *prose("PHONG THU",
               ["Xe lu và xe ca cùng đi trên đường với nhau.", "Thấy xe lu đi chậm, xe ca chế:"],
               ["- Cậu đi như con rùa ấy! Xem tớ đây này!"],
               ["Nói rồi, xe ca phóng vụt lên, bỏ xe lu ở tít đằng sau.", "Xe ca tưởng mình thế là giỏi lắm."],
               ["Tới một quãng đường bị hỏng, xe ca phải đỗ lại vì lầy lội quá.", "Bấy giờ xe lu mới tiến lên.",
                "Khi đám đá hộc và đá cuội ngổn ngang đổ xuống, xe lu liền lăn qua lăn lại cho phẳng lì.",
                "Nhờ vậy mà xe ca mới tiếp tục lên đường."],
               ["Từ đấy, xe ca không chế giễu xe lu nữa.", "Xe ca đã hiểu rằng: công việc của xe lu là như vậy."])],
       listen(("xe lu", "xe ca", "con rùa"), ("xe ca", "xe lu", "đá cuội"), ("con rùa", "đá hộc", "xe ca"),
              ("đá cuội", "con rùa", "phẳng lì"), ("phẳng lì", "lầy lội", "đá hộc"), ("lầy lội", "phẳng lì", "xe lu")))

# 309 — Chính tả tuần 18 (tr.8–9)
BO_DUA_CT = ["Một hôm, ông để một bó đũa và một túi tiền trên bàn rồi gọi các con lại và bảo:",
             "- Trong các con, ai bẻ gãy được bó đũa này thì cha thưởng cho túi tiền.",
             "Các người con lần lượt bẻ, ai cũng cố hết sức mà không sao bẻ gãy được bó đũa."]
lesson(309, [8, 9],
       [title("Chính tả: Câu chuyện bó đũa", "Nghe đọc"),
        title("Bài viết: \"Một hôm, ông để... gãy được bó đũa\".", "Phần này con viết vào vở cùng bố mẹ."),
        words("chuyện", "túi", "gãy", "rồi", "này", "lần lượt", "đũa", "bẻ"),
        combine("túi", "áo", "quần", "gạo"),
        combine_mixed("gãy", ("bẻ", "before"), ("gọn", "after")),
        fill(["xưa", "sưa"], ("chuyện đời xưa", "xưa", "xưa"), ("say sưa", "sưa", "sưa")),
        fill(["lượt", "lược"], ("năm lần bảy lượt", "lượt", "lượt"), ("cái lược chải đầu", "lược", "lược")),
        find("Gạch dưới những chữ có dấu ngã trong bài chính tả.", {"tone": ["ngã"]}, text=BO_DUA_CT),
        title("Tập chép: Không sống riêng lẻ", "Nhìn bảng"),
        title("Bài chép: Cả bài.", "Phần này con chép vào vở cùng bố mẹ."),
        words("riêng", "kiếm", "sướng", "xếp", "chung", "vui", "hễ", "lẻ"),
        fill(["sướng", "xướng"], ("vui sướng", "sướng", "sướng"), ("sung sướng", "sướng", "sướng"),
             ("xướng ca", "xướng", "xướng"), ("xướng âm", "xướng", "xướng")),
        fill(["hễ", "hể"], ("hể hả", "hể", "hể"), ("hễ ăn là nhớ đến em", "hễ", "hễ")),
        find("Tìm trong bài chính tả những chữ có iê.", {"word": ["kiếm", "kiến", "riêng"]}, text=KIEN),
        find("Tìm trong bài chính tả những chữ có ươ.", {"word": ["được", "sướng", "tướng"]}, text=KIEN)],
       listen(("túi áo", "túi quần", "túi gạo"), ("bẻ gãy", "gãy gọn", "lần lượt"), ("chuyện đời xưa", "say sưa", "cái lược"),
              ("năm lần bảy lượt", "chuyện đời xưa", "say sưa"), ("riêng lẻ", "vui sướng", "xướng ca"),
              ("hể hả", "riêng lẻ", "lần lượt")),
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Ghép chữ, điền chỗ trống, gạch dưới chữ làm bằng chạm vào thẻ hoặc vào chữ."),
              ("khac_sach", "Cụm \"say ... nghe chuyện\" rút ngắn thành \"say sưa\" cho vừa khung.")],
       review=[("part1[4]", "ghép \"bẻ gãy\" (bẻ đứng trước), \"gãy gọn\" (gọn đứng sau) do app chọn"),
               ("part1[5]", "đáp án xưa/sưa theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[6]", "đáp án lượt/lược theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[11]", "đáp án sướng/xướng theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[12]", "sách in \"hễ hay hể\": hể hả, hễ ăn là nhớ đến em (sách không in đáp án)"),
               ("part1[13]", "chữ có iê trong bài chép do app chọn: kiếm, Kiến, riêng"),
               ("part1[14]", "chữ có ươ trong bài chép do app chọn: được, sướng, tướng")])

# 310 — Từ ngữ: Thiếu nhi đoàn kết (tr.9–10)
lesson(310, [9, 10],
       [title("Từ ngữ: Thiếu nhi đoàn kết"),
        title("Những từ ngữ cần ghi nhớ"),
        words("bạn học", "tình bạn", "tập thể", "đoàn kết", "gắn bó"),
        words("đồng sức đồng lòng", marker=""),
        title("Bài tập: Chọn từ ngữ thích hợp ở trên để điền vào những chỗ trống"),
        fill_passage(["Các bạn Xuân, Phong, Thụ, Hải và em cùng học với nhau một lớp, "
                      "nên chúng em đều là [bạn học|tập thể|đồng sức đồng lòng] của nhau.",
                      "Ở lớp cũng như ở nhà, chúng em luôn luôn [đoàn kết|bạn học|tình bạn] với nhau, "
                      "cùng giúp đỡ nhau tiến bộ.",
                      "[Tình bạn|Bạn học|Tập thể] giữa chúng em ngày càng thêm [gắn bó|tập thể|bạn học]."]),
        fill_passage(["Bác Hồ dạy: Việc gì khó mà biết [đồng sức đồng lòng|bạn học|tình bạn] "
                      "thì việc khó mấy cũng làm xong.",
                      "Trong một [tập thể|bạn học|gắn bó] mà mọi người không [đoàn kết|bạn học|tập thể] "
                      "thì dù việc dễ cũng không làm được đến nơi đến chốn."])],
       listen(("bạn học", "tình bạn", "tập thể"), ("tình bạn", "bạn học", "gắn bó"), ("tập thể", "đoàn kết", "bạn học"),
              ("đoàn kết", "gắn bó", "tình bạn"), ("gắn bó", "tập thể", "đoàn kết"),
              ("đồng sức đồng lòng", "đoàn kết", "tập thể")),
       notes=[("sach", "\"Đồng sức đồng lòng\" là thành ngữ (sách in trong mục từ ngữ cần ghi nhớ)."),
              ("khac_sach", "Điền từ: mỗi chỗ trống 3 thẻ do app chọn trong các từ ngữ cần ghi nhớ, tránh hai từ cùng "
                            "đúng; đáp án do app soạn.")],
       review=[("part1[5]", "đáp án điền từ do app soạn: bạn học, đoàn kết, Tình bạn, gắn bó"),
               ("part1[6]", "đáp án điền từ do app soạn: đồng sức đồng lòng, tập thể, đoàn kết")])

# 311 — Ngữ pháp: Danh từ (tr.10)
lesson(311, [10],
       [title("Ngữ pháp: Danh từ"),
        q("1. Tìm những từ chỉ người trong bài Câu chuyện bó đũa."),
        q("2. Em hãy kể thêm những từ khác chỉ người mà em biết. Ví dụ: em bé, cô giáo..."),
        find("3. Trong bài Không sống riêng lẻ, từ nào chỉ loài vật?", {"word": ["kiến"]}, text=KIEN),
        q("4. Em hãy kể tên một số con vật nuôi trong nhà."),
        *rule("Những từ chỉ người, chỉ loài vật gọi là danh từ.")],
       listen(("danh từ", "loài vật", "con vật"), ("cô giáo", "em bé", "ông già"), ("em bé", "cô giáo", "con kiến"),
              ("ông già", "người con", "em bé"), ("con kiến", "con vật", "cô giáo"), ("loài vật", "danh từ", "ông già")),
       notes=[("khac_sach", KS_ORAL)],
       review=[("part1[3]", "từ chỉ loài vật trong bài Không sống riêng lẻ do app chọn: kiến")])

# 312 — Tập làm văn: Trả lời câu hỏi — Câu chuyện bó đũa (tr.10)
lesson(312, [10],
       [title("Tập làm văn: Trả lời câu hỏi"),
        title("Đề bài: Câu chuyện bó đũa.", "Xem tranh ở bài Câu chuyện bó đũa."),
        picture(BO_DUA, "Con nhớ lại câu chuyện bó đũa nhé.", "bó đũa"),
        q("1. Ông già bảo các con thế nào?"),
        q("2. Bốn người con làm gì? Kết quả ra sao?"),
        q("3. Ông già dùng cách gì để bẻ gãy bó đũa một cách dễ dàng?"),
        q("4. Chuyện này khuyên ta điều gì?")],
       listen(("bó đũa", "túi tiền", "ông già"), ("ông già", "người con", "bó đũa"), ("người con", "ông già", "dễ dàng"),
              ("dễ dàng", "kết quả", "túi tiền"), ("kết quả", "dễ dàng", "người con"), ("túi tiền", "bó đũa", "kết quả")),
       images={BO_DUA: BO_DUA_DESC},
       notes=[("khac_sach", KS_TLC)],
       review=[("part1[2]", "lời dẫn tranh do app soạn")])
print("tuần 18 xong")
