"""Tuần 1 (mục 172–179), tr.4–11, ảnh 003–006."""
from l2lib import *

# 172 — Bài 1. Bác Hồ khuyên học sinh (tr.4–5)
lesson(172, [4, 5],
       [picture("img_b172_hocj_sinh", "Các bạn nhỏ siêng học, siêng làm.", "học sinh"),
        title("Bác Hồ khuyên học sinh"),
        *sentences("Bác rất vui lòng biết rằng:",
                   "cháu nào cũng biết siêng học, siêng làm,",
                   "biết ăn ở sạch sẽ, biết giữ kỉ luật, lễ phép,",
                   "thế là tốt lắm.",
                   "Bác khuyên các cháu gắng sức thêm.",
                   "Việc gì có ích cho Tổ quốc thì các cháu nên gắng sức làm.",
                   "Tuổi các cháu còn nhỏ thì các cháu làm những công việc nhỏ.",
                   "Nhiều công việc nhỏ cộng lại thành công việc to.",
                   "Bác mong các cháu làm việc và học hành",
                   "cho xứng đáng là nhi đồng của nước Việt Nam...",
                   "Bác hôn tất cả các cháu."),
        passage("prose", "BÁC HỒ", breaks=[4, 10]),
        *glossary("Kỉ luật: những điều nhà trường đề ra cho học sinh phải tuân theo như: đi học đúng giờ, "
                 "trong lớp giữ gìn trật tự, nghỉ học phải xin phép...",
                 "Tổ quốc: đất nước mình."),
        q("1. Bác Hồ khen các cháu đã làm tốt được những điều gì?", marker="?"),
        q("2. Bác khuyên tuổi nhỏ làm việc nhỏ. Em hãy kể một số việc nhỏ có ích mà em đã làm được."),
        q("3. Em hãy thay những từ siêng học, siêng làm bằng những từ khác cùng nghĩa."),
        q("4. Em đặt một câu với từ gắng sức.")],
       listen(("siêng học", "sạch sẽ", "lễ phép"), ("kỉ luật", "Tổ quốc", "công việc"),
              ("gắng sức", "học hành", "nhi đồng"), ("Tổ quốc", "kỉ luật", "tốt lắm"),
              ("nhi đồng", "gắng sức", "sạch sẽ"), ("lễ phép", "siêng làm", "học hành")),
       images={"img_b172_hocj_sinh": "Các bạn học sinh tiểu học quàng khăn đỏ trong lớp học: một bạn chăm chú viết bài, "
                                     "một bạn lau bảng, một bạn tưới chậu hoa cửa sổ (không vẽ người thật, không có chữ)"},
       notes=[("khac_sach", "Sách in ảnh chụp Bác Hồ; app vẽ các bạn học sinh siêng học, siêng làm (không vẽ người thật)."),
              ("khac_sach", KS_NO_SPELL), ("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)],
       review=[("part1[0]", "tranh thay ảnh chụp Bác Hồ; lời dẫn tranh do app soạn")])

# 173 — Bài 2. Cái trống trường em (Học thuộc lòng, tr.6–7)
POEM2 = ["Cái trống trường em", "Mùa hè cũng nghỉ.", "Suốt ba tháng liền", "Trống nằm ngẫm nghĩ.",
         "Buồn không hả trống", "Trong những ngày hè", "Bọn mình đi vắng", "Chỉ còn tiếng ve?",
         "Cái trống lặng im", "Nghiêng đầu trên giá.", "Chắc thấy chúng em", "Nó mừng vui quá!",
         "Kìa trống đang gọi:", "Tùng! Tùng! Tùng! Tùng!", "Vào năm học mới", "Giọng vang tưng bừng."]
lesson(173, [6, 7],
       [picture("img_b173_cais_troongs_truwowngf", "Đây là cái trống trường.", "cái trống"),
        title("Cái trống trường em", "Học thuộc lòng"),
        *sentences(*POEM2),
        passage("poem", "THANH HÀO", breaks=[4, 8, 12]),
        *glossary("Giá trống: cái khung bằng gỗ để đặt (hoặc treo) cái trống."),
        q("1. Câu thơ nào trong khổ thơ đầu cho em biết cái trống buồn?", marker="?"),
        q("2. Tại sao trong mùa hè, cái trống lại buồn?"),
        q("3. Tìm một câu trong khổ thơ cuối bài tả cái trống vui."),
        q("4. Tại sao cái trống lại vui?"),
        memorize()],
       listen(("cái trống", "tiếng ve", "năm học"), ("ngẫm nghĩ", "lặng im", "mừng vui"),
              ("tiếng ve", "cái trống", "tưng bừng"), ("tưng bừng", "ngẫm nghĩ", "đi vắng"),
              ("lặng im", "mừng vui", "giọng vang"), ("năm học", "ngày hè", "tiếng ve")),
       images={"img_b173_cais_troongs_truwowngf": "Sân trường dưới gốc cây lớn: bác bảo vệ cầm dùi đánh chiếc trống to "
                                                  "đặt trên giá gỗ, các bạn học sinh đeo cặp vui vẻ chạy vào trường"},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)])

# 174 — Bài 3. Niềm vui ngày khai trường (tr.7–8)
lesson(174, [7, 8],
       [picture("img_b174_khai_truwowngf", "Hôm nay là ngày khai trường.", "khai trường"),
        title("Niềm vui ngày khai trường"),
        *sentences("Món quà của bố gửi về cho Lan thật đúng dịp.",
                   "Một chiếc cặp màu đen có quai xách.",
                   "Trong cặp có bốn quyển vở bìa xanh biếc,",
                   "một cái bút chì màu và một phong thư.",
                   "Chao ôi! Sắp đến ngày khai trường,",
                   "nhận được quà của bố, Lan càng thêm náo nức.",
                   "Trong thư bố dặn:",
                   "\"Con được lên lớp hai, bố vội gửi quà về cho con.",
                   "Trong năm học này, con hứa gì với bố thì viết thư cho bố nhé!\"",
                   "Các bạn ơi! Hôm nay đã vào năm học mới.",
                   "Lan vui vui khi cắp chiếc cặp mới đi học.",
                   "Nhưng Lan chưa viết thư cho bố.",
                   "Hứa gì với bố trong năm học này,",
                   "Lan còn suy nghĩ thật kĩ rồi mới viết."),
        passage("prose", "TRÚC MAI", breaks=[4, 9]),
        *glossary("Ngày khai trường: ngày bắt đầu năm học mới, còn gọi là ngày khai giảng."),
        q("1. Sắp đến ngày khai trường, bố gửi về cho Lan những quà gì? "
          "Câu nào cho em biết Lan rất vui khi nhận được quà của bố?", marker="?"),
        q("2. Trong thư, bố dặn Lan điều gì?"),
        q("3. Tại sao Lan chưa viết thư cho bố?"),
        q("4. Em thử đoán xem Lan sẽ hứa với bố điều gì?")],
       listen(("chiếc cặp", "phong thư", "quyển vở"), ("phong thư", "bút chì", "quai xách"),
              ("náo nức", "suy nghĩ", "khai trường"), ("khai trường", "năm học", "náo nức"),
              ("xanh biếc", "màu đen", "đúng dịp"), ("suy nghĩ", "náo nức", "xanh biếc")),
       images={"img_b174_khai_truwowngf": "Trước cổng trường ngày khai trường: cô bé Lan mặc áo chấm bi, ôm chiếc cặp đen "
                                          "mới, đi cùng một bạn gái; các bạn học sinh tụm lại vui vẻ trước cổng (không có chữ)"},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 175 — Bài 4. Mùa thu đẹp (Bài đọc thêm, tr.9; sách không có tranh)
lesson(175, [9],
       [title("Mùa thu đẹp", "Bài đọc thêm"),
        *sentences("Cứ mỗi độ thu sang,", "Hoa cúc lại nở vàng.", "Ngoài vườn, hương thơm ngát,",
                   "Ong, bướm bay rộn ràng.", "Em cắp sách tới trường,", "Nắng tươi trải trên đường,",
                   "Trời cao xanh, gió mát,", "Đẹp thay lúc thu sang!"),
        passage("poem", "Tập đọc lớp 1 – 1980")],
       listen(("hoa cúc", "ong bướm", "gió mát"), ("rộn ràng", "thơm ngát", "nở vàng"),
              ("thu sang", "tới trường", "trên đường"), ("gió mát", "hoa cúc", "nắng tươi"),
              ("thơm ngát", "rộn ràng", "cao xanh"), ("nắng tươi", "thu sang", "hoa cúc")))

# 176 — Chính tả tuần 1 (tr.9–10)
lesson(176, [9, 10],
       [title("Tập chép: Bác Hồ khuyên học sinh", "Nhìn sách"),
        title("Bài chép: \"Bác rất vui lòng... gắng sức thêm\".", "Phần này con chép vào vở cùng bố mẹ."),
        words("Bác khuyên", "giữ", "kỉ luật", "siêng", "sạch sẽ", "gắng sức", "lễ phép"),
        fill(["s", "x"], ("siêng học", "siêng", "s"), ("siêng làm", "siêng", "s"), ("sạch sẽ", "sạch", "s"),
             ("sạch sẽ", "sẽ", "s"), ("xứng đáng", "xứng", "x")),
        fill(["gắng", "gắn"], ("cố gắng học tập", "gắng", "gắng"), ("gắn bó", "gắn", "gắn")),
        q("Câu bắt đầu bằng một chữ cái viết hoa và kết thúc bằng một dấu chấm. Em hãy đếm xem bài chép có mấy câu?"),
        title("Tập chép: Niềm vui ngày khai trường", "Nhìn bảng"),
        title("Bài chép: \"Chao ôi!... bố nhé\".", "Phần này con chép vào vở cùng bố mẹ."),
        words("Lan", "gửi", "niềm", "chao ôi", "dặn", "của"),
        combine("gửi", "thư", "quà"),
        fill(["chao", "trao"], ("chao ôi", "chao", "chao"), ("trao giải thưởng", "trao", "trao"))],
       listen(("siêng", "xứng", "sạch"), ("kỉ luật", "lễ phép", "gắng sức"), ("gắn bó", "gắng sức", "đoàn kết"),
              ("gửi thư", "gửi quà", "chao ôi"), ("trao", "dặn", "gửi"), ("niềm", "dặn", "gửi")),
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Điền chỗ trống và ghép chữ làm bằng chạm hoặc kéo thẻ.")],
       review=[("part1[3]", "đáp án s/x theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[4]", "đáp án gắng/gắn theo chính tả chuẩn (sách không in đáp án)")])

# 177 — Từ ngữ: Ngày khai trường (tr.10)
lesson(177, [10],
       [title("Từ ngữ: Ngày khai trường"),
        title("Những từ ngữ cần ghi nhớ"),
        words("mùa hè", "mùa thu", "ngày khai trường", "năm học mới"),
        words("nghỉ hè", "khai giảng", "siêng học", "siêng làm", "lễ phép", "náo nức", "tưng bừng"),
        title("Bài tập: Điền từ thích hợp vào chỗ trống"),
        fill_passage(["Một năm có [mười hai|mười|chín] tháng, bắt đầu từ tháng [một|hai|chín] "
                      "đến tháng [mười hai|mười|tám].",
                      "Nhưng năm học của chúng em chỉ có [chín|mười hai|sáu] tháng, bắt đầu từ tháng [chín|một|sáu] "
                      "năm trước đến tháng [năm|tám|mười hai] năm sau.",
                      "Từ tháng sáu đến tháng tám, chúng em được [nghỉ hè|khai giảng|lễ phép].",
                      "Ngày [khai trường|nghỉ hè|mùa thu] là ngày mở đầu năm học.",
                      "Chúng em [náo nức|lễ phép|nghỉ hè] bước vào năm học mới."])],
       listen(("mùa thu", "mùa hè", "năm học"), ("khai giảng", "khai trường", "nghỉ hè"),
              ("náo nức", "tưng bừng", "lễ phép"), ("nghỉ hè", "mùa hè", "năm học"),
              ("tưng bừng", "náo nức", "siêng làm"), ("lễ phép", "siêng học", "khai giảng")),
       notes=[("khac_sach", "Sách để trống, không cho sẵn từ: app cho mỗi chỗ trống 3 thẻ để chọn; "
                            "thẻ và đáp án do app soạn.")],
       review=[("part1[5]", "thẻ chọn và đáp án điền chỗ trống do app soạn (năm học 9 tháng, tháng 9 đến tháng 5)")])

# 178 — Ngữ pháp: Câu (tr.10–11)
lesson(178, [10, 11],
       [title("Ngữ pháp: Câu"),
        *rule("Nói, viết phải thành câu.", "Nếu nói, viết không thành câu thì người khác không hiểu được."),
        choose("Trong những dòng sau đây, dòng nào viết chưa thành câu?",
               ["Ngày khai trường", "Bác rất vui lòng.", "Cái trống trường em", "Trong cặp có bốn quyển vở.",
                "Lan chưa"], [0, 2, 4])],
       listen(("thành câu", "hiểu được", "người khác"), ("quyển vở", "cái trống", "vui lòng"),
              ("cái trống", "khai trường", "quyển vở"), ("vui lòng", "người khác", "thành câu"),
              ("khai trường", "quyển vở", "hiểu được"), ("hiểu được", "vui lòng", "cái trống")),
       notes=[("khac_sach", "Bé chạm vào dòng chưa thành câu; đáp án do app soạn.")],
       review=[("part1[2]", "đáp án dòng chưa thành câu do app soạn: Ngày khai trường, Cái trống trường em, Lan chưa")])

# 179 — Tập làm văn: Điền từ — Niềm vui ngày khai trường (tr.11)
lesson(179, [11],
       [title("Tập làm văn: Điền từ"),
        title("Đề bài: Niềm vui ngày khai trường.",
              "Em hãy chọn những từ sau đây để điền vào chỗ trống: vui sướng, khai trường, năm học, siêng học."),
        fill_passage(["Sắp đến ngày [khai trường], nhận được quà của bố, Lan càng thêm náo nức.",
                      "Hôm nay đã bắt đầu [năm học] mới: Lan [vui sướng] khi cắp chiếc cặp mới đi học.",
                      "Lan hứa với bố sẽ [siêng học], siêng làm như lời Bác Hồ khuyên."],
                     bank=["vui sướng", "khai trường", "năm học", "siêng học"])],
       listen(("vui sướng", "náo nức", "siêng học"), ("chiếc cặp", "năm học", "khai trường"),
              ("siêng học", "siêng làm", "vui sướng"), ("náo nức", "vui sướng", "năm học"),
              ("khai trường", "chiếc cặp", "siêng làm"), ("năm học", "khai trường", "chiếc cặp")),
       notes=[("khac_sach", "Điền từ bằng chạm hoặc kéo thẻ từ vào chỗ trống; đáp án do app soạn.")],
       review=[("part1[2]", "đáp án điền từ do app soạn theo bài Niềm vui ngày khai trường")])
print("tuần 1 xong")
