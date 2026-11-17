"""Tuần 32 (mục 419–426), tr.108–114, ảnh 055–058."""
from l2t2lib import *
from w31 import CHIEN_KHU_POEM

# 419 — Bài 59. Thư của Chú Nguyễn (tr.108–109)
THU_CT = ["Các cháu ngoan.", "Học thuộc bài.", "Vâng lời cha mẹ.", "Đừng đánh con chó nhỏ Ma-ri-uýt của các cháu.",
          "Khi các cháu lớn lên, các cháu sẽ đấu tranh cho Tổ quốc của các cháu | "
          "cũng như ba má, chú Nguyễn và những chú khác."]
lesson(419, [108, 109],
       [picture(img(419, "lá thư"), "Hai bạn nhỏ đọc lá thư của Chú Nguyễn.", "lá thư"),
        title("Thư của Chú Nguyễn"),
        *prose("Trích Thư Chú Nguyễn",
               ["... Có lẽ rất lâu, các cháu sẽ không được thấy chú Nguyễn, "
                "không được leo lên đùi, lên lưng chú như các cháu thường làm.",
                "Và cũng rất lâu, chú sẽ không thấy cháu gái A-lit-xơ và cháu trai Pôn của chú.",
                "Khi chú cháu mình gặp nhau, có lẽ chú đã già, các cháu đã lớn bằng ba và má.", "Điều đó không ngại gì.",
                "Chú sẽ luôn luôn nhớ đến các cháu.",
                "Các cháu luôn luôn vẫn là | cô bé A-lit-xơ và cậu bé Pôn thân yêu của chú."],
               THU_CT,
               ["Các cháu nhỏ thân yêu của chú, chú hôn các cháu rất kêu..."]),
        *glossary("Chú Nguyễn: tên gọi Bác Hồ hồi Bác hoạt động cách mạng ở Pháp.",
                  "A-lit-xơ, Pôn: tên của cháu gái 8 tuổi và cháu trai 4 tuổi, con một đồng chí người Trung Mĩ, "
                  "cùng hoạt động với Bác Hồ ở Pháp trước khi Bác rời Pa-ri về hoạt động trong nước."),
        q("1. Trong thư, Chú Nguyễn nhắc lại kỉ niệm gì giữa Chú và các cháu A-lit-xơ, Pôn?", marker="?"),
        q("2. Tuy xa các cháu nhưng tình cảm của Chú Nguyễn đối với các cháu vẫn không thay đổi. "
          "Câu nào trong thư cho em biết điều đó?"),
        q("3. Chú Nguyễn khuyên các cháu A-lit-xơ và Pôn những điều gì? "
          "*Chú ước mong mai sau lớn lên các cháu sẽ làm gì?"),
        q("4. Tìm những từ trái nghĩa với các từ yêu, nhớ, ngoan.")],
       listen(("lá thư", "con chó", "Tổ quốc"), ("con chó", "lá thư", "cô bé"), ("cô bé", "cậu bé", "lá thư"),
              ("cậu bé", "cô bé", "Tổ quốc"), ("thân yêu", "kỉ niệm", "đấu tranh"), ("đấu tranh", "thân yêu", "con chó")),
       images={img(419, "lá thư"): "Phòng khách nhỏ ở nước Pháp có rèm cửa xanh, nhìn ra mái nhà cổ: cô bé tóc ngắn "
                                   "ngồi ghế bành cầm lá thư đọc, cậu em trai ngồi ghế bên cạnh vuốt ve chú chó nhỏ; "
                                   "giữa phòng có bàn tròn đặt lọ hoa (không vẽ Bác)"},
       notes=[("khac_sach", "Tranh sách vẽ hai cháu A-lit-xơ, Pôn với chú chó; app vẽ hai bạn nhỏ không rõ mặt người "
                            "thật, không vẽ Bác."),
              ("sach", "Bài trích thư (sách in \"...\" ở đầu bài)."),
              ("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)],
       review=[("part1[0]", "lời dẫn tranh do app soạn")])

# 420 — Bài 60. Tổ nước ta (Học thuộc lòng, tr.109–110; sách không có tranh)
TO_NUOC = ["Hồng Bàng là tổ nước ta", "Nước ta lúc ấy gọi là Văn Lang.", "Thiếu nhi ta rất vẻ vang",
           "Trẻ em Phù Đổng tiếng vang muôn đời", "Tuổi tuy chưa đến chín mười", "Ra tay cứu nước diệt loài vô lương..."]
lesson(420, [109, 110],
       [title("Tổ nước ta", "Học thuộc lòng"),
        *sentences(*TO_NUOC),
        passage("poem", "HỒ CHÍ MINH", breaks=[2]),
        q("1. Tổ nước ta tên là gì?", marker="?"),
        q("2. Tên đầu tiên của nước ta là gì?"),
        q("3. Em bé đầu tiên ở nước ta có chiến công giết giặc giữ nước rất vẻ vang là ai?"),
        q("*4. Tìm một từ ghép gồm 2 tiếng cùng nghĩa với từ tổ ở trong bài."),
        find("5. Tìm các danh từ riêng trong bài. *Xếp các từ đó theo thứ tự trong bảng chữ cái "
             "(căn cứ vào tiếng đầu của mỗi từ).",
             {"word": ["hồng", "bàng", "văn", "lang", "phù", "đổng"]}),
        memorize()],
       listen(("Hồng Bàng", "Văn Lang", "Phù Đổng"), ("Văn Lang", "Hồng Bàng", "thiếu nhi"), ("Phù Đổng", "Văn Lang", "vẻ vang"),
              ("thiếu nhi", "vẻ vang", "cứu nước"), ("vẻ vang", "thiếu nhi", "muôn đời"), ("cứu nước", "muôn đời", "Hồng Bàng")),
       notes=[("sach", "Bài thơ trích (sách in \"...\" ở cuối)."), ("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)],
       review=[("@5. Tìm các danh từ riêng", "danh từ riêng do app chọn: Hồng Bàng, Văn Lang, Phù Đổng")])

# 421 — Bài 61. Quả táo của Bác Hồ (tr.110–111)
lesson(421, [110, 111],
       [picture(img(421, "quả táo"), "Em bé gái giữ khư khư quả táo, các bạn đứng quanh.", "quả táo"),
        title("Quả táo của Bác Hồ"),
        *prose("Theo cuốn BÁC HỒ KÍNH YÊU",
               ["Hôm ấy, tòa Thị chính Pa-ri mở tiệc lớn đón mừng Bác.",
                "Tiệc tan, mọi người mời Bác ra phòng lớn uống nước và nói chuyện.",
                "Bác vui vẻ đứng dậy và cầm một quả táo đem theo.", "Nhiều người ngạc nhiên, nhiều con mắt tò mò chú ý."],
               ["Bác ra đến ngoài thì có một đám thiếu nhi ríu rít chạy tới chào.",
                "Bác tươi cười bế một em gái nhỏ nhất lên và cho em quả táo.",
                "Mọi người bấy giờ mới vỡ lẽ | và rất cảm động trước cử chỉ thương yêu của Người."],
               ["Ngày hôm sau, câu chuyện \"Quả táo của Bác Hồ\" | đều được các báo Pháp đăng lên đầu trang nhất.",
                "Các báo còn kể lại rằng | em bé gái khi nhận được quả táo đó thì giữ khư khư trong tay, "
                "ai xin cũng không cho.",
                "Lúc về nhà, em để quả táo trên bàn học.",
                "Cha mẹ em bảo: \"Con ăn đi, kẻo để lâu sẽ hỏng không ăn được\".",
                "Nhưng em nhất định không ăn.",
                "Em nói: \"Đó là táo của Bác Hồ cho con, | con sẽ giữ thật lâu để làm kỉ niệm\"."]),
        *glossary("Năm 1946, Bác Hồ sang thăm nước Pháp theo lời mời của tổng thống Pháp.",
                  "Tòa Thị chính: nơi làm việc của chính quyền thành phố."),
        q("1. Trong phòng tiệc đón mừng Bác Hồ, mọi người ngạc nhiên vì điều gì?", marker="?"),
        q("2. Câu nào cho em biết cử chỉ thương yêu rất mực của Bác Hồ đối với thiếu nhi?"),
        q("3. Em bé gái trong bài rất kính yêu Bác Hồ. Những sự việc gì chứng tỏ điều đó?"),
        q("4. Đặt câu với mỗi từ: khư khư, kỉ niệm.")],
       listen(("quả táo", "bàn học", "thiếu nhi"), ("bàn học", "quả táo", "tòa Thị chính"), ("thiếu nhi", "trang nhất", "quả táo"),
              ("kỉ niệm", "khư khư", "ríu rít"), ("khư khư", "kỉ niệm", "ngạc nhiên"), ("ríu rít", "ngạc nhiên", "kỉ niệm")),
       images={img(421, "quả táo"): "Trước cửa vòm của một tòa nhà lớn ở Pa-ri: một bé gái nhỏ mặc váy hoa hai tay "
                                    "giữ khư khư quả táo đỏ, bốn bạn thiếu nhi đứng quanh tươi cười nhìn quả táo "
                                    "(không vẽ Bác)"},
       notes=[("khac_sach", KS_REAL.format(who="các bạn thiếu nhi và em bé gái nhận quả táo",
                                           what="em bé gái cầm quả táo giữa các bạn (không vẽ Bác)")),
              ("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)],
       review=[("part1[0]", "lời dẫn tranh do app soạn")])

# 422 — Bài 62. Bác rất thương loài vật (Bài đọc thêm, tr.112; sách không có tranh)
lesson(422, [112],
       [title("Bác rất thương loài vật", "Bài đọc thêm"),
        *prose("DIỆP MINH CHÂU kể, ĐOÀN GIỎI ghi",
               ["Lúc ở chiến khu, Bác Hồ nuôi một con chó, một con mèo và một con khỉ.",
                "Thông thường thì ba loài đó vốn chẳng ưa nhau.",
                "Không biết Bác dạy thế nào mà chúng lại quấn quýt nhau, | "
                "thường đùa giỡn, không hề trêu chọc hay cắn nhau bao giờ."],
               ["Mỗi lần dời nhà đi, có khi phải hai ngày mới tới chỗ mới, | "
                "bao giờ con khỉ cũng nhảy phốc lên ngồi trên lưng con chó to.",
                "Hễ con chó đi chậm, con khỉ cấu hai tai chó giật giật.",
                "Con chó chạy sải thì khỉ gò lưng như người phi ngựa.",
                "Chó chạy thong thả, khỉ buông thõng hai tay, ngồi ngúc nga ngúc ngắc.", "Ai trông thấy cũng phải cười.",
                "Con mèo đen có đốm trắng thì ngao ngao, lững thững chạy theo."],
               ["Con khỉ này rất nghịch nên các anh bảo vệ thường phải cột dây.",
                "Khi Bác ăn cơm, Bác mở dây và cho nó ăn.",
                "Bữa nọ, Bác vừa quay lưng ngó ra sân, | nó bèn rón rén bốc trộm cơm của Bác | "
                "và ngồi yên, giấu nắm cơm trong tay vờ như không có gì xảy ra.",
                "Tôi vội kêu: \"Sao mày bốc cơm của Bác?\"",
                "Con khỉ vội lom khom chạy đi, vừa chạy vừa quay lại nhìn như sợ Bác giận.",
                "Bác mỉm cười, nụ cười rất hiền lành."])],
       listen(("con khỉ", "con chó", "con mèo"), ("con chó", "con khỉ", "nắm cơm"), ("con mèo", "nắm cơm", "con khỉ"),
              ("nắm cơm", "con mèo", "con chó"), ("quấn quýt", "lững thững", "rón rén"), ("lững thững", "quấn quýt", "lom khom")),
       notes=[("khac_sach", KS_SPLIT)])

# 423 — Chính tả tuần 32 (tr.112–113)
lesson(423, [112, 113],
       [title("Chính tả: Thư của Chú Nguyễn", "Nghe đọc"),
        title("Bài viết: \"Các cháu ngoan... rất kêu\".", "Phần này con viết vào vở cùng bố mẹ."),
        words("Ma-ri-uýt", "Tổ quốc", "Nguyễn", "tranh", "lên", "vâng", "kêu", "sẽ", "những"),
        q("a) Viết các tên riêng trong bài chính tả theo thứ tự bảng chữ cái."),
        fill(["tranh", "chanh"], ("bức tranh", "tranh", "tranh"), ("quả chanh", "chanh", "chanh"),
             ("đấu tranh", "tranh", "tranh"), ("nước chanh", "chanh", "chanh")),
        fill(["kêu", "kiêu"], ("tiếng kêu", "kêu", "kêu"), ("kiêu căng", "kiêu", "kiêu"), ("kêu ca", "kêu", "kêu")),
        fill(["vâng", "vân"], ("vâng lời", "vâng", "vâng"), ("gỗ có vân đẹp", "vân", "vân")),
        title("Chính tả: Bác Hồ ở chiến khu", "So sánh"),
        *sentences(*CHIEN_KHU_POEM[:4]),
        title("Bài viết: bốn câu thơ trên.", "Phần này con viết vào vở cùng bố mẹ."),
        words("khuya", "suối", "sơ", "chảy", "nứa", "đêm", "cháy", "sáng", "lửa"),
        title("Phát âm phân biệt tiếng in nghiêng ở mỗi cặp từ ngữ sau"),
        words("đơn sơ", "xơ mướp", "nước chảy", "trảy quả"),
        words("đêm ngày", "đem đi", "bếp lửa", "củi nổ lép bép"),
        words("đèn sáng", "sán đến gần", "ngọn lửa", "lần lữa")],
       listen(("bức tranh", "quả chanh", "đấu tranh"), ("tiếng kêu", "kiêu căng", "kêu ca"), ("vâng lời", "vân gỗ", "nước chanh"),
              ("đơn sơ", "xơ mướp", "nước chảy"), ("đêm ngày", "đem đi", "bếp lửa"), ("đèn sáng", "lần lữa", "ngọn lửa")),
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Viết tên riêng theo thứ tự: bé nói cùng bố mẹ; điền chỗ trống làm bằng chạm thẻ; cặp từ so "
                            "sánh thành thẻ chạm để nghe (dấu \"≠\" thay bằng dấu phẩy).")],
       review=[("part1[4]", "đáp án tranh/chanh theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[5]", "đáp án kêu/kiêu theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[6]", "đáp án vâng/vân theo chính tả chuẩn (sách không in đáp án)")])

# 424 — Từ ngữ: Ôn tập cuối năm: Đất nước, nhân dân (tr.113)
lesson(424, [113],
       [title("Từ ngữ: Ôn tập cuối năm: Đất nước, nhân dân"),
        q("1. Tổ quốc là gì? Em hãy tìm những danh từ cùng nghĩa hoặc gần nghĩa với từ Tổ quốc."),
        words("đồng bằng", "rừng núi", "vùng biển"),
        q("2. Đặt câu với mỗi từ sau đây: đồng bằng, rừng núi, vùng biển."),
        q("3. Nông thôn và thành phố có gì khác nhau?"),
        q("4. Nông dân làm gì? Công nhân làm gì? Bộ đội làm nhiệm vụ gì?"),
        words("cần cù", "anh dũng", "đoàn kết"),
        q("5. Đặt câu với mỗi từ sau đây nói về nhân dân ta: cần cù, anh dũng, đoàn kết.")],
       listen(("Tổ quốc", "đất nước", "non sông"), ("đồng bằng", "rừng núi", "vùng biển"), ("rừng núi", "vùng biển", "đồng bằng"),
              ("nông thôn", "thành phố", "Tổ quốc"), ("cần cù", "anh dũng", "đoàn kết"), ("anh dũng", "đoàn kết", "cần cù")),
       notes=[("khac_sach", KS_ORAL), ("khac_sach", "Các từ để đặt câu hiện thành thẻ chạm để nghe.")])

# 425 — Ngữ pháp: Ôn tập: Tiếng – Từ – Câu (tr.114)
lesson(425, [114],
       [title("Ngữ pháp: Ôn tập: Tiếng – Từ – Câu"),
        q("1. Tìm 1 từ do 1 tiếng tạo nên (Ví dụ: ăn).",
          lines=["1 từ do 2 tiếng tạo nên (Ví dụ: học sinh, xe đạp).", "1 từ do 3 tiếng tạo nên (Ví dụ: hợp tác xã)."]),
        q("2. Câu thường có 2 bộ phận chính: Bộ phận thứ nhất trả lời câu hỏi gì? Bộ phận thứ hai trả lời câu hỏi gì?"),
        q("Khi viết chữ đầu câu phải viết như thế nào? Cuối câu thường có dấu gì?"),
        q("*3. Đoạn văn sau đây chưa chấm câu. Em hãy chấm câu và viết hoa chữ đầu câu:",
          lines=["thầy giáo bước vào lớp cả lớp đứng dậy chào giờ học bắt đầu thầy gọi tên hai bạn lên đọc bài",
                 "thầy khen các bạn thuộc bài và cho điểm tốt sau đó thầy bắt đầu giảng bài mới cả lớp chăm chú lắng nghe"])],
       listen(("tiếng", "từ", "câu"), ("học sinh", "xe đạp", "hợp tác xã"), ("hợp tác xã", "học sinh", "thầy giáo"),
              ("thầy giáo", "giờ học", "bài mới"), ("giờ học", "thầy giáo", "điểm tốt"), ("điểm tốt", "bài mới", "giờ học")),
       notes=[("khac_sach", "Bé chấm câu bằng miệng cùng bố mẹ; đoạn văn chưa chấm câu chia làm hai dòng cho vừa màn."),
              ("khac_sach", KS_ORAL)],
       review=[("@*3. Đoạn văn", "đoạn văn chưa chấm câu: app đọc liền một mạch như sách in, chữ đầu viết thường; "
                                 "chủ dự án nghe xem có ổn")])

# 426 — Tập làm văn: Dùng từ – đặt câu (tr.114)
lesson(426, [114],
       [title("Tập làm văn: Dùng từ – đặt câu"),
        title("Đề bài: Em hãy dùng mỗi từ ngữ sau đây đặt thành hai câu nói về tình cảm của Bác Hồ "
              "đối với các cháu thiếu nhi:"),
        words("thiếu nhi", "Bác Hồ", "thương yêu"),
        q("Em hãy đặt hai câu với mỗi từ ngữ trên.")],
       listen(("thiếu nhi", "Bác Hồ", "thương yêu"), ("Bác Hồ", "thương yêu", "thiếu nhi"), ("thương yêu", "thiếu nhi", "Bác Hồ"),
              ("quả táo", "lá thư", "thiếu nhi"), ("lá thư", "quả táo", "thương yêu"), ("kỉ niệm", "lá thư", "quả táo")),
       notes=[("khac_sach", KS_DAT_CAU),
              ("khac_sach", "Câu \"Em hãy đặt hai câu với mỗi từ ngữ trên\" do app thêm để nhắc bé (trang chỉ in đề bài).")],
       review=[("part1[3]", "câu nhắc đặt câu do app thêm")])
print("tuần 32 xong")
