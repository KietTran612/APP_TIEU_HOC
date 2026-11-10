"""Tuần 3 (mục 188–195), tr.18–23, ảnh 010–012."""
from l2lib import *

# 188 — Bài 9. Đàn kiến nó đi (tr.18)
POEM9 = ["Một đàn kiến nhỏ", "Chạy ngược chạy xuôi,", "Chẳng ra hàng một,", "Chẳng thành hàng đôi.",
         "Đang chạy bên này", "Lại sang bên nọ", "Cắm cổ cắm đầu", "Kìa trông, xấu quá!",
         "Chúng em vào lớp", "Sóng bước hai hàng.", "Chẳng như kiến nọ", "Rối tinh cả đàn."]
lesson(188, [18],
       [picture("img_b188_sawps_hangf", "Các bạn xếp hàng đôi vào lớp.", "xếp hàng"),
        title("Đàn kiến nó đi"),
        *sentences(*POEM9),
        passage("poem", "ĐỊNH HẢI", breaks=[4, 8]),
        q("1. Tám câu đầu tả cảnh gì? Tại sao đàn kiến đi trông rất xấu?", marker="?"),
        q("2. Khổ thơ cuối tả cảnh gì? Cảnh đó khác cảnh trên như thế nào?"),
        q("3. Đi sóng bước hai hàng là đi như thế nào?"),
        find("4. Tìm hai từ có nghĩa trái ngược nhau ở khổ thơ đầu.", {"word": ["ngược", "xuôi"]},
             sentences_in=[0, 1, 2, 3])],
       listen(("đàn kiến", "hàng đôi", "bên này"), ("hàng một", "hàng đôi", "hai hàng"),
              ("sóng bước", "cắm cổ", "rối tinh"), ("rối tinh", "sóng bước", "xấu quá"),
              ("cắm cổ", "đàn kiến", "bên nọ"), ("hàng đôi", "hàng một", "vào lớp")),
       images={"img_b188_sawps_hangf": "Các bạn học sinh tiểu học đeo cặp xếp thành hai hàng thẳng, đi đều bước vào "
                                       "cửa lớp; dưới chân cột hiên có một đàn kiến nhỏ bò lộn xộn"},
       notes=[("khac_sach", KS_ORAL)],
       review=[("part1[18]", "hai từ trái nghĩa do app chọn: ngược – xuôi")])

# 189 — Bài 10. Cô giáo lớp em (Học thuộc lòng, tr.19–20)
POEM10 = ["Sáng nào em đến lớp", "Cũng thấy cô đến rồi", "Đáp lời \"chào cô ạ!\"", "Cô mỉm cười thật tươi.",
          "Cô dạy em tập viết", "Gió đưa thoảng hương nhài", "Nắng ghé vào cửa lớp", "Xem chúng em học bài.",
          "Những lời cô giáo giảng", "Ấm trang vở thơm tho", "Yêu thương em ngắm mãi", "Những điểm mười cô cho."]
lesson(189, [19, 20],
       [picture("img_b189_coo_giaos_lowps_em", "Cô giáo đứng đón các em ở cửa lớp.", "cô giáo"),
        title("Cô giáo lớp em", "Học thuộc lòng"),
        *sentences(*POEM10),
        passage("poem", "NGUYỄN XUÂN SANH", breaks=[4, 8]),
        q("1. Trong khổ thơ đầu, câu nào cho em biết cô giáo yêu quý các em học sinh?", marker="?"),
        q("2. Trong khổ thơ cuối, những từ ấm, ngắm mãi nói lên tình cảm gì của em học sinh đối với cô giáo?"),
        find("3. Em tìm những tiếng cuối dòng có vần giống nhau trong khổ thơ thứ 2 và thứ 3.",
             {"word": ["nhài", "bài", "tho", "cho"]}, sentences_in=range(4, 12)),
        memorize()],
       listen(("tập viết", "học bài", "điểm mười"), ("hương nhài", "cửa lớp", "thơm tho"),
              ("điểm mười", "tập viết", "mỉm cười"), ("mỉm cười", "đến lớp", "hương nhài"),
              ("thơm tho", "ngắm mãi", "học bài"), ("ngắm mãi", "thơm tho", "đáp lời")),
       images={"img_b189_coo_giaos_lowps_em": "Cô giáo trẻ mặc áo dài đứng ở cửa lớp mỉm cười, hai bạn học sinh "
                                              "khoanh tay chào cô, trong lớp một bạn ngồi đọc sách bên cửa sổ"},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)],
       review=[("part1[17]", "tiếng cuối dòng cùng vần do app chọn: nhài – bài, tho – cho")])

# 190 — Bài 11. Bé và chim chích bông (tr.20–21)
lesson(190, [20, 21],
       [picture("img_b190_bes_hocj_baif", "Bé dậy sớm ngồi học bài.", "học bài"),
        title("Bé và chim chích bông"),
        *sentences("Buổi sáng, Bé dậy sớm, ngồi học bài.",
                   "Dậy sớm học bài là một thói quen tốt.",
                   "Nhưng phải cố gắng lắm mới có được thói quen ấy.",
                   "Rét ghê.",
                   "Thế mà Bé vùng dậy, chui ra được khỏi cái chăn ấm.",
                   "Bé ngồi học bài.",
                   "Rồi trời ấm dần.",
                   "Phải rồi, khi chim sâu ra ăn đàn, thế là trời nắng ấm.",
                   "Chim sâu nhiều thế.",
                   "Nó bay tràn qua vườn cải.",
                   "Cả đàn ùa xuống, líu tíu trên những luống rau trồng muộn.",
                   "Bé hỏi:",
                   "- Chích bông ơi chích bông, làm gì thế?",
                   "Chim trả lời:",
                   "- Chúng em bắt sâu.",
                   "Chim hỏi lại Bé:",
                   "- Chị Bé làm gì thế?",
                   "Bé ngẩn ra, rồi nói:",
                   "- À... Bé học bài."),
        passage("prose", "TÔ HOÀI", breaks=[6, 8, 11, 12, 13, 14, 15, 16, 17, 18]),
        *glossary("Chim chích bông: loại chim nhỏ, còn gọi là chim sâu, thường ở các vườn cây, vườn rau để tìm bắt sâu."),
        q("1. Bé dậy sớm để làm gì?", marker="?"),
        q("2. Những câu nào, từ nào cho ta biết Bé phải cố gắng lắm mới dậy sớm được? Em đã làm được như Bé chưa?"),
        q("3. Chim sâu xuống vườn cải để làm gì? Những từ nào tả cảnh chim sâu xuống vườn cải đông lắm?"),
        q("4. Trong bài này, những ai đáng khen?")],
       listen(("chim sâu", "vườn cải", "chăn ấm"), ("vườn cải", "luống rau", "chim sâu"),
              ("thói quen", "cố gắng", "học bài"), ("líu tíu", "ùa xuống", "ngẩn ra"),
              ("chăn ấm", "nắng ấm", "thói quen"), ("bắt sâu", "học bài", "líu tíu")),
       images={"img_b190_bes_hocj_baif": "Buổi sáng sớm, cô bé mặc áo bông ngồi trên ghế đẩu chăm chú học bài bên bàn "
                                         "cạnh cửa sổ; ngoài cửa sổ đàn chim sâu nhỏ bay xuống vườn rau"},
       notes=[("khac_sach", KS_ORAL)])

# 191 — Bài 12. Chú bộ đội lái máy bay (Bài đọc thêm, tr.21–22; sách không có tranh)
lesson(191, [21, 22],
       [title("Chú bộ đội lái máy bay", "Bài đọc thêm"),
        *sentences("Trước giờ vào lớp, chúng em đang chơi thì có một chú bộ đội đến.",
                   "Chú đội chiếc mũ có ông sao trên nền xanh da trời.",
                   "Chú hỏi thăm cô giáo.",
                   "Một bạn vào thưa với cô.",
                   "Cô vội vàng bước ra.",
                   "Chú bộ đội cũng bước nhanh tới, vội ngả chiếc mũ xuống:",
                   "- Em chào cô ạ!",
                   "Cô giáo bỗng đứng sững lại.",
                   "Chúng em cũng nín lặng vây quanh.",
                   "- Thưa cô, em về thăm sức khỏe của cô!",
                   "Cô giáo như chợt nhớ ra:",
                   "- À! Em Thanh! Em lái máy bay à?...",
                   "Em còn nhớ cô ư?",
                   "- Thưa cô, dù bao nhiêu năm nữa, dù đi đâu rất xa,",
                   "em vẫn là học sinh cũ của cô,",
                   "đã từng được cô dìu dắt, dạy bảo."),
        passage("prose", "PHONG THU", breaks=[6, 7, 9, 10, 11, 13])],
       listen(("bộ đội", "máy bay", "cô giáo"), ("máy bay", "chiếc mũ", "ông sao"),
              ("dìu dắt", "dạy bảo", "nín lặng"), ("nín lặng", "đứng sững", "vây quanh"),
              ("ông sao", "chiếc mũ", "máy bay"), ("hỏi thăm", "vội vàng", "dìu dắt")),
       notes=[("khac_sach", KS_SPLIT)])

# 192 — Chính tả tuần 3 (tr.22)
lesson(192, [22],
       [title("Tập chép: Đàn kiến nó đi", "Nhìn sách"),
        title("Bài chép: 2 khổ thơ đầu.", "Phần này con chép vào vở cùng bố mẹ."),
        words("ngược", "cắm", "xuôi", "xấu", "đàn kiến", "cổ"),
        q("Đặt câu với mỗi từ: hàng, hòn, đoàn, dàn."),
        title("Chính tả: Đẹp mà không đẹp", "Nghe đọc"),
        title("Bài viết: \"Trên bức tường trắng... cháu ạ!\".", "Phần này con nghe bố mẹ đọc rồi viết vào vở."),
        words("Hùng", "bác Thành", "trên", "than", "vẽ"),
        q("Viết tên các bạn cùng bàn (nhớ viết hoa)."),
        fill(["tr", "ch"], ("trên trời", "trên", "tr"), ("trên trời", "trời", "tr"), ("mây trắng", "trắng", "tr"),
             ("chung quanh", "chung", "ch")),
        fill(["n", "ng"], ("cái bàn", "bàn", "n"), ("cây bàng", "bàng", "ng"), ("bàn ghế", "bàn", "n"))],
       listen(("đàn kiến", "xấu", "cổ"), ("ngược", "xuôi", "cắm"), ("bác Thành", "Hùng", "than"),
              ("cây bàng", "bàn ghế", "mây vàng"), ("mây trắng", "mây vàng", "mây xanh"), ("vẽ", "than", "trên")),
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Câu \"Viết tên các bạn cùng bàn\": bé nói tên các bạn cùng bố mẹ."),
              ("khac_sach", "Điền chỗ trống làm bằng chạm hoặc kéo thẻ.")],
       review=[("part1[8]", "đáp án tr/ch theo bài thơ quen (trên trời có đám mây xanh, chung quanh mây vàng)"),
               ("part1[9]", "đáp án n/ng theo chính tả chuẩn (cái bàn, cây bàng, bàn ghế)")])

# 193 — Từ ngữ: Thầy trò (tr.23)
lesson(193, [23],
       [title("Từ ngữ: Thầy trò"),
        title("Những từ ngữ cần ghi nhớ"),
        words("thầy giáo", "cô giáo", "giáo viên", "học sinh", "hiệu trưởng"),
        words("dạy bảo", "dìu dắt", "yêu thương", "kính trọng", "biết ơn"),
        title("Bài tập: Tìm từ thích hợp điền vào những chỗ trống"),
        fill_passage(["Trường em có năm thầy giáo và sáu cô giáo, tất cả là mười một "
                      "[giáo viên|học sinh|hiệu trưởng].",
                      "Nhưng trường em chỉ có một cô [hiệu trưởng|giáo viên|học sinh] trông nom chung mọi việc "
                      "trong trường.",
                      "Các thầy giáo, cô giáo chăm lo [dạy bảo|kính trọng|biết ơn] học sinh.",
                      "Chúng em rất [kính trọng|dạy bảo|dìu dắt] các thầy giáo, cô giáo."])],
       listen(("hiệu trưởng", "giáo viên", "học sinh"), ("giáo viên", "hiệu trưởng", "thầy giáo"),
              ("dìu dắt", "dạy bảo", "biết ơn"), ("kính trọng", "yêu thương", "dìu dắt"),
              ("biết ơn", "kính trọng", "dạy bảo"), ("thầy giáo", "cô giáo", "học sinh")),
       notes=[("khac_sach", "Sách để trống, không cho sẵn từ: app cho mỗi chỗ trống 3 thẻ lấy từ các từ ngữ cần "
                            "ghi nhớ; thẻ và đáp án do app soạn.")],
       review=[("part1[5]", "thẻ chọn và đáp án điền chỗ trống do app soạn")])

# 194 — Ngữ pháp: Câu – Mở đầu và kết thúc (tr.23)
lesson(194, [23],
       [title("Ngữ pháp: Câu – Mở đầu và kết thúc"),
        *rule("Khi nói hết câu phải nghỉ hơi.", "Khi viết hết câu phải ghi dấu chấm.", "Chữ cái đầu câu phải viết hoa."),
        q("Đoạn văn dưới đây có thể cắt thành mấy câu? Em hãy chép lại đoạn văn này vào vở, "
          "ghi dấu chấm câu và viết hoa cho đúng.",
          lines=["trống trường đã điểm chúng em vào lớp cô giáo từ ngoài bước vào "
                 "chúng em ngồi xuống giờ học bắt đầu"])],
       listen(("nghỉ hơi", "dấu chấm", "viết hoa"), ("dấu chấm", "viết hoa", "nghỉ hơi"),
              ("viết hoa", "nghỉ hơi", "dấu chấm"), ("trống trường", "giờ học", "cô giáo"),
              ("giờ học", "vào lớp", "trống trường"), ("ngồi xuống", "bước vào", "giờ học")),
       notes=[("khac_sach", "Bé đếm câu và nói cùng bố mẹ; phần chép lại đoạn văn bé viết vào vở.")])

# 195 — Tập làm văn: Điền từ — Cô giáo, thầy giáo của chúng em (tr.23)
lesson(195, [23],
       [title("Tập làm văn: Điền từ"),
        title("Đề bài: Cô giáo, thầy giáo của chúng em.",
              "Em hãy chọn những từ sau đây để điền vào chỗ trống: dạy bảo, cô giáo, kính trọng, thầy giáo, yêu quý."),
        fill_passage(["Mẹ của em ở trường là [cô giáo] mến thương.",
                      "Nghe lời cô [dạy bảo], em cố gắng chăm chỉ học tập.",
                      "Trong trường em, ngoài các cô giáo còn có các [thầy giáo] và thầy hiệu trưởng.",
                      "Em rất [kính trọng] và [yêu quý] các thầy giáo, cô giáo trong trường."],
                     bank=["dạy bảo", "cô giáo", "kính trọng", "thầy giáo", "yêu quý"])],
       listen(("cô giáo", "thầy giáo", "dạy bảo"), ("dạy bảo", "yêu quý", "cô giáo"),
              ("kính trọng", "dạy bảo", "chăm chỉ"), ("yêu quý", "kính trọng", "thầy giáo"),
              ("chăm chỉ", "mến thương", "học tập"), ("mến thương", "chăm chỉ", "yêu quý")),
       notes=[("khac_sach", "Điền từ bằng chạm hoặc kéo thẻ từ vào chỗ trống; đáp án do app soạn "
                            "(câu cuối: \"kính trọng và yêu quý\").")],
       review=[("part1[2]", "đáp án điền từ do app soạn; câu cuối đổi chỗ \"kính trọng\" và \"yêu quý\" cũng đúng")])
