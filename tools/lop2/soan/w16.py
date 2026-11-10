"""Tuần 16 (mục 290–296), tr.108–114, ảnh 055–058. Mục lục để trống số bài; trang in số 59, 60, 61."""
from l2lib import *

DUA_IMG = "img_b291_caay_duwaf"
DUA_DESC = ("Cây dừa cao vút bên bờ biển, tàu lá xanh xòe rộng như những bàn tay, chùm quả dừa tròn trên cao, trăng tròn "
            "trên trời và mây trắng")
POEM60 = ["Cây dừa xanh tỏa nhiều tàu", "Dang tay đón gió, gật đầu gọi trăng.", "Thân dừa bạc phếch tháng năm",
          "Quả dừa – đàn lợn con nằm trên cao.", "Đêm hè hoa nở cùng sao", "Tàu dừa – chiếc lược chải vào mây xanh.",
          "Ai mang nước ngọt, nước lành", "Ai đeo bao hũ rượu quanh cổ dừa.", "Tiếng dừa làm dịu nắng trưa",
          "Gọi đàn gió đến cùng dừa múa reo.", "Trời trong đầy tiếng rì rào", "Đàn cò đánh nhịp bay vào bay ra...",
          "Đứng canh trời đất bao la", "Mà dừa đủng đỉnh như là đứng chơi."]
KS_NO_NUMBER = "Mục lục sách để trống số bài của tuần 16; app ghi số bài theo số in trên trang (59, 60, 61)."

# 290 — Bài 59. Cây xoài của ông em (tr.108–109)
lesson(290, [108, 109],
       [picture("img_b290_caay_xoaif", "Cây xoài ông trồng trước sân trĩu quả.", "cây xoài"),
        title("Cây xoài của ông em"),
        *prose("ĐOÀN GIỎI",
               ["Ông em trồng cây xoài cát này trước sân, khi em còn đi lẫm chẫm.", "Cuối đông, hoa nở trắng cành.",
                "Trông từng chùm quả to, đu đưa theo gió đầu hè, em càng nhớ ông.",
                "Mùa xoài nào, mẹ em cũng chọn những quả chín mọng, vàng đẹp và to nhất, bày lên bàn thờ ông."],
               ["Xoài thanh ca, xoài voi, xoài tượng... đều ngon.", "Nhưng em thích xoài cát nhất.",
                "Mùi thơm dịu dàng, vị ngọt đậm đà, màu sắc đẹp, quả lại to."],
               ["Ăn quả xoài cát chín trẩy từ cây của ông em trồng,",
                "kèm với xôi nếp hương, thì đối với em không thứ quả gì ngon bằng."]),
        *glossary("Đi lẫm chẫm: đi chập chững.", "Trẩy: hái."),
        q("1. Cây xoài có quả chín vào mùa nào?", marker="?"),
        q("2. Tại sao mẹ lại chọn những quả xoài ngon nhất bày lên bàn thờ ông?"),
        q("3. Quả xoài chín có mùi, vị gì? Màu sắc như thế nào?"),
        q("4. Em đặt câu với mỗi từ: đu đưa, chín mọng, đậm đà.")],
       listen(("xoài cát", "xôi nếp", "bàn thờ"), ("lẫm chẫm", "đu đưa", "chín mọng"), ("đậm đà", "dịu dàng", "chín mọng"),
              ("chùm quả", "xoài voi", "nếp hương"), ("đu đưa", "đậm đà", "lẫm chẫm"), ("dịu dàng", "đu đưa", "xoài cát")),
       images={"img_b290_caay_xoaif": "Cây xoài cát to trước sân ngôi nhà ngói nhỏ, chùm quả vàng trĩu cành; người bố "
                                      "đeo giỏ chỉ lên cây cho bé gái xem, hàng rào tre và cây dừa phía sau"},
       notes=[("sach", KS_NO_NUMBER), ("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 291 — Bài 60. Cây dừa (Học thuộc lòng, tr.110–111)
lesson(291, [110, 111],
       [picture(DUA_IMG, "Cây dừa xanh dang tay đón gió.", "cây dừa"),
        title("Cây dừa", "Học thuộc lòng"),
        *sentences(*POEM60),
        passage("poem", "TRẦN ĐĂNG KHOA", breaks=[4, 8, 12]),
        q("1. Những từ ngữ nào tả cây dừa như người? (biết vui chơi, biết lo nhiệm vụ)", marker="?"),
        q("2. Tác giả so sánh quả dừa, tàu dừa với vật gì?"),
        find("3. Tìm những tiếng cùng vần với nhau trong bốn câu thơ đầu.",
             {"word": ["tàu", "đầu", "trăng", "năm", "cao"]}, sentences_in=[0, 1, 2, 3]),
        q("4. Ở nước ta, vùng nào có nhiều dừa?"),
        memorize()],
       listen(("tàu dừa", "quả dừa", "thân dừa"), ("bạc phếch", "rì rào", "đủng đỉnh"), ("đàn cò", "đàn gió", "đàn lợn"),
              ("rì rào", "đủng đỉnh", "bao la"), ("chiếc lược", "hũ rượu", "tàu dừa"), ("đủng đỉnh", "bạc phếch", "múa reo")),
       images={DUA_IMG: DUA_DESC},
       notes=[("sach", KS_NO_NUMBER), ("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)],
       review=[("part1[19]", "tiếng cùng vần do app chọn: tàu–đầu, trăng–năm (cao vần với \"tàu\" ở câu sau)")])

# 292 — Bài 61. Truyện vui về cây Thì là (Bài đọc thêm, tr.111–112; sách không có tranh)
lesson(292, [111, 112],
       [title("Truyện vui về cây Thì là", "Bài đọc thêm"),
        *prose("Văn học dân gian Việt Nam (TRỊNH MẠNH kể)",
               ["Ngày xưa, cây cối trên trái đất đều chưa có tên gọi.",
                "Trời bèn gọi các cây lên để đặt cho mỗi loại cây một cái tên.",
                "Nghe tin đó, đám cây cối mừng lắm và mỗi loại đều cử một cây lên trời để nhận tên."],
               ["Lên đến trời, trên một bãi rộng, các cây, to, nhỏ, cao, thấp đứng chen chúc nhau.",
                "Trời ngồi trên một gò cao, lần lượt đặt tên cho các cây to rồi đến các cây nhỏ.",
                "Trời trỏ tay vào từng cây và đặt tên:"],
               ["- Chú thì ta đặt tên cho là cây Dừa."], ["- Chú thì ta đặt tên cho là cây Cau."],
               ["- Chú thì ta đặt tên cho là cây Mít."], ["- Chú thì tên là cây Nhãn."], ["- Chú thì tên là cây Hồng..."],
               ["Trời nói mãi, mỏi cả mồm mà vẫn chưa hết.", "Vì vậy, lúc đầu trời còn nói câu dài.",
                "Về sau, trời chỉ nói vắn tắt:"],
               ["- Chú thì là cây Cải."], ["- Chú là cây Ớt."], ["- Chú là cây Tỏi."],
               ["Khi tất cả các cây đều đã có tên, trời tưởng hết,",
                "bỗng còn một cây tiến đến chỗ trời để xin đặt tên.",
                "Trời nhìn thấy một cây nhỏ xíu như que hương, thân mảnh khảnh, lá lăn tăn.", "Trời hỏi:"],
               ["- Chú bé tí xíu, có ích gì mà cũng xin đặt tên?"], ["Cây nhỏ liền thưa:"],
               ["- Thưa trời, con rất có ích.",
                "Khi nấu canh riêu cá hoặc làm các món ăn như chả cá, chả mực mà không có con thì mất cả ngon."],
               ["Trời liền bảo:"], ["- Ừ, ta sẽ nghĩ cho một cái tên.", "Tên chú thì... là..."],
               ["Trời còn đang suy nghĩ, chưa biết nên đặt tên là gì,", "khi nhìn xuống thì cây nhỏ đã chạy đi xa rồi.",
                "Nó mừng rỡ nói với bạn bè: Trời đặt cho tôi là cây \"Thì là\"!"])],
       listen(("cây Dừa", "cây Cau", "cây Mít"), ("cây Nhãn", "cây Hồng", "cây Cải"), ("cây Ớt", "cây Tỏi", "Thì là"),
              ("chen chúc", "mảnh khảnh", "lăn tăn"), ("canh riêu", "chả cá", "chả mực"), ("vắn tắt", "mừng rỡ", "suy nghĩ")),
       notes=[("sach", KS_NO_NUMBER), ("khac_sach", KS_SPLIT)])

# 293 — Chính tả tuần 16 (tr.112–113)
lesson(293, [112, 113],
       [title("Chính tả: Quê em vùng biển", "Nghe đọc"),
        title("Bài viết: Cả bài (10 câu).", "Phần này con nghe bố mẹ đọc rồi viết vào vở."),
        words("mênh mông", "đoàn thuyền", "đầy ắp", "tràn", "bãi"),
        combine("mênh mông", "rộng", "biển cả", at="before"),
        combine("thuyền", "đoàn", "con", "chiếc", at="before"),
        fill(["ắp", "ấp"], ("thuyền đầy ắp cá", "ắp", "ắp"), ("gà mái ấp trứng", "ấp", "ấp")),
        fill(["tràn", "tràng"], ("nước tràn", "tràn", "tràn"), ("đầy tràn", "tràn", "tràn"), ("tràng hạt", "tràng", "tràng"),
             ("tràng vỗ tay", "tràng", "tràng")),
        fill(["bãi", "bải"], ("bãi cát", "bãi", "bãi"), ("bãi biển", "bãi", "bãi"), ("bải hoải tay chân", "bải", "bải")),
        title("Chính tả: Sa Pa", "Trí nhớ"),
        title("Bài viết: 6 câu đầu.", "Phần này con nhớ lại rồi viết vào vở."),
        words("trĩu", "quanh", "bậc thang", "đỉnh"),
        title("Viết tên riêng các địa phương sau", "Phần viết con viết vào vở; ở đây con đọc các tên riêng."),
        *rule("Pác Bó", "Kon Tum", "Đà Lạt", "Plây Cu"),
        fill(["bậc", "bật"], ("bậc thang", "bậc", "bậc"), ("nổi bật", "bật", "bật"), ("vượt bậc", "bậc", "bậc"),
             ("bật đèn", "bật", "bật")),
        fill(["đỉnh", "đĩnh"], ("đỉnh núi", "đỉnh", "đỉnh"), ("đỉnh đầu", "đỉnh", "đỉnh"), ("đĩnh đạc", "đĩnh", "đĩnh"))],
       listen(("mênh mông", "biển cả", "đoàn thuyền"), ("con thuyền", "chiếc thuyền", "đầy ắp"), ("tràng hạt", "nước tràn", "bãi cát"),
              ("bãi biển", "bải hoải", "bậc thang"), ("đỉnh núi", "đĩnh đạc", "nổi bật"), ("Đà Lạt", "Kon Tum", "Pác Bó")),
       notes=[("khac_sach", KS_WRITE), ("khac_sach", "Ghép chữ, điền chỗ trống làm bằng chạm hoặc kéo thẻ; tên riêng "
                                                   "bé đọc trên thẻ rồi viết vào vở cùng bố mẹ.")],
       review=[("part1[3]", "cách ghép do app chọn: rộng mênh mông, biển cả mênh mông"),
               ("part1[5]", "đáp án ắp/ấp"), ("part1[6]", "đáp án tràn/tràng"), ("part1[7]", "đáp án bãi/bải"),
               ("part1[13]", "đáp án bậc/bật"), ("part1[14]", "đáp án đỉnh/đĩnh")])

# 294 — Từ ngữ: Ruộng vườn, cây cối (tr.113)
lesson(294, [113],
       [title("Từ ngữ: Ruộng vườn, cây cối"),
        title("Những từ ngữ cần ghi nhớ"),
        words("vườn rau", "ruộng lúa", "rẫy lúa", "vườn cây ăn quả", "nương ngô"),
        words("gốc cây", "thân cây", "cành cây", "vòm lá", "hoa", "quả"),
        words("vun xới", "xum xuê"),
        title("Bài tập: Điền từ thích hợp vào chỗ trống", "Cây xoan"),
        fill_passage(["Ở vườn nhà Liên có cây [xoan].", "Thân cây mọc thẳng vươn cao, cành lá [xum xuê].",
                      "Mùa này, [quả] xoan chín vàng, rụng đầy [gốc] cây.",
                      "Từng đàn chào mào, sáo đen kéo nhau về, ríu rít trong [vòm lá] xanh tìm ăn quả chín."],
                     bank=["xoan", "xum xuê", "quả", "gốc", "vòm lá", "vun xới"])],
       listen(("vườn rau", "ruộng lúa", "nương ngô"), ("gốc cây", "thân cây", "cành cây"), ("vòm lá", "xum xuê", "vun xới"),
              ("vun xới", "vòm lá", "rẫy lúa"), ("xum xuê", "vun xới", "gốc cây"), ("rẫy lúa", "vườn rau", "vòm lá")),
       notes=[("khac_sach", "Điền từ bằng chạm hoặc kéo thẻ; thẻ lấy từ các từ ngữ cần ghi nhớ, đáp án do app soạn.")],
       review=[("part1[6]", "đáp án điền từ do app soạn")])

# 295 — Ngữ pháp: Bảng chữ cái (tiếp theo) (tr.114)
lesson(295, [114],
       [title("Ngữ pháp: Bảng chữ cái", "Tiếp theo"),
        {"type": "letter_pairs", "letters": ["a", "ă", "â", "b", "c", "d", "đ", "e", "ê", "g", "h", "i", "k", "l", "m",
                                              "n", "o", "ô", "ơ", "p", "q", "r", "s", "t", "u", "ư", "v", "x", "y"]},
        q("1. Đọc thuộc lòng bảng chữ cái."),
        q("2. Trong các cặp chữ cái sau, theo thứ tự trong bảng chữ cái, chữ nào đứng trước, chữ nào đứng sau?",
          lines=["b và e", "n và h", "p và t", "v và r"]),
        q("3. Xếp những nhóm chữ cái sau đây theo đúng thứ tự trong bảng chữ cái:",
          lines=["a, d, g, c, e", "h, o, m, s, t", "b, c, p, v, y"])],
       listen(("chữ cái", "thứ tự", "bảng chữ"), ("đứng trước", "đứng sau", "thứ tự"), ("bảng chữ", "chữ cái", "đứng sau"),
              ("thuộc lòng", "đứng trước", "chữ cái"), ("đứng sau", "thuộc lòng", "bảng chữ"), ("thứ tự", "đứng trước", "thuộc lòng")),
       notes=[("khac_sach", "Bảng chữ cái hiện lại để bé nhìn; bé trả lời và sắp xếp bằng miệng cùng bố mẹ.")])

# 296 — Tập làm văn: Quan sát tranh và trả lời câu hỏi — Cây dừa (tr.114)
lesson(296, [114],
       [title("Tập làm văn: Quan sát tranh và trả lời câu hỏi"),
        title("Đề bài: Cây dừa.", "Xem tranh ở bài Cây dừa."),
        picture(DUA_IMG, "Con nhìn kĩ tranh cây dừa nhé.", "cây dừa"),
        q("1. Cây dừa mới nhìn giống cây gì?"),
        q("2. Cây dừa có những bộ phận nào? Trong tranh, bộ phận nào của cây dừa gợi lên hình ảnh đẹp dưới trăng?"),
        q("3. Cây dừa có dáng vẻ gì khác hẳn các cây khác? (Ví dụ: cây tre, cây xoan...)"),
        q("4. Em biết ở đâu có nhiều dừa?")],
       listen(("cây dừa", "tàu dừa", "quả dừa"), ("tàu dừa", "cây dừa", "thân dừa"), ("thân dừa", "quả dừa", "cây tre"),
              ("cây tre", "cây xoan", "cây dừa"), ("cây xoan", "cây tre", "tàu dừa"), ("quả dừa", "thân dừa", "cây xoan")),
       images={DUA_IMG: DUA_DESC},
       notes=[("khac_sach", "Tập làm văn quan sát tranh: app dùng lại tranh bài Cây dừa; bé trả lời miệng.")],
       review=[("part1[2]", "lời dẫn tranh do app soạn")])
