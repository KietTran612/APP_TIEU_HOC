"""Tuần 19 (mục 313–320), tr.11–18, ảnh 016–022, 001."""
from l2t2lib import *

# 313 — Bài 5. Trên đường đến nhà lao (tr.11–12)
CON_DAO = img(313, "Côn Đảo")
CON_DAO_DESC = ("Con đường ven biển Côn Đảo lúc bình minh: đường đất uốn quanh bờ biển, men theo triền núi; "
                "bên trên cây dừa, cây cối um tùm, chim đậu hót trên cành, một con bướm bay; bên dưới sóng trắng "
                "vỗ vào bờ đá dựng; bầu trời hồng nhạt (không có người)")
TRIEN = ["Bầu trời Côn Đảo trong buổi bình minh rất đẹp.",
         "Con đường từ Bến Đầm đến nhà lao uốn quanh bờ biển, men theo triền núi, "
         "bên trên là cây cối um tùm, bên dưới là sóng trắng vỗ bờ đá dựng.",
         "Trên cành cây, chim kêu ríu rít.", "Chị Sáu như say sưa với cảnh tự nhiên."]
lesson(313, [11, 12],
       [picture(CON_DAO, "Con đường ven biển Côn Đảo lúc bình minh.", "bờ biển"),
        title("Trên đường đến nhà lao"),
        *prose("LÊ QUANG VỊNH",
               TRIEN + ["Chị hát theo một con chim hót.", "Chị rướn đôi tay bị còng chụp một con bướm bay qua.",
                        "Chị chẳng để ý gì đến bọn lính | với súng gươm tua tủa ở xung quanh mình."]),
        *glossary("Triền núi: dải đất ở lưng chừng núi.", "Tua tủa: đâm ra mọi phía."),
        q("1. Côn Đảo trong buổi bình minh đẹp như thế nào? (con đường, cây cối, sóng, chim?)", marker="?"),
        q("2. Những câu nào ở cuối bài cho em biết chị Sáu chẳng sợ sệt gì cả? "
          "*Điều đó chứng tỏ chị Sáu có đức tính gì đáng quý?"),
        q("3. Tìm một từ gần nghĩa với từ \"nhà lao\"."),
        q("4. Tìm trong bài một từ chỉ người, một từ chỉ loài vật và một từ chỉ cây cỏ.")],
       listen(("bình minh", "bờ biển", "triền núi"), ("triền núi", "bình minh", "cây cối"),
              ("bờ biển", "con bướm", "bình minh"), ("ríu rít", "um tùm", "say sưa"),
              ("con bướm", "con chim", "cây cối"), ("say sưa", "ríu rít", "tua tủa")),
       images={CON_DAO: CON_DAO_DESC},
       notes=[("khac_sach", KS_REAL.format(who="chị Võ Thị Sáu bị lính giải đi",
                                           what="con đường ven biển Côn Đảo lúc bình minh")),
              ("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)],
       review=[("part1[0]", "tranh thay cảnh chị Võ Thị Sáu bị giải đi; lời dẫn tranh do app soạn")])

# 314 — Bài 6. Chú bé liên lạc (Học thuộc lòng, tr.12–13)
LIEN_LAC = ["Chú bé loắt choắt", "Cái xắc xinh xinh", "Cái chân thoăn thoắt", "Cái đầu nghênh nghênh.",
            "Ca lô đội lệch", "Mồm huýt sáo vang", "Như con chim chích", "Nhảy trên đường vàng...",
            "Vụt qua mặt trận", "Đạn bay vèo vèo", "Thư đề \"Thượng khẩn\"", "Sợ chi hiểm nghèo?",
            "Đường quê vắng vẻ", "Lúa trổ đòng đòng", "Ca lô chú bé", "Nhấp nhô trên đồng..."]
lesson(314, [12, 13],
       [picture(img(314, "đường quê"), "Đường quê vàng nắng giữa đồng lúa trổ đòng đòng.", "đường quê"),
        title("Chú bé liên lạc", "Học thuộc lòng"),
        *sentences(*LIEN_LAC),
        passage("poem", "TỐ HỮU", breaks=[4, 8, 12]),
        *glossary("Ca lô: một loại mũ vải không vành có hai đầu nhọn.", "Loắt choắt: bé nhỏ.",
                  "Thượng khẩn: rất cần kíp, rất gấp."),
        q("1. Hình dáng chú bé liên lạc có gì đáng yêu? (Khổ 1 và 2)", marker="?"),
        q("2. Chú bé rất gan dạ. Những từ nào nói lên điều đó?"),
        q("3. Chú bé liên lạc thường làm những công việc gì?"),
        find("4. Tìm những từ láy trong bài. (Ví dụ: loắt choắt, xinh xinh).",
             {"word": ["loắt", "choắt", "xinh", "thoăn", "thoắt", "nghênh", "vèo", "đòng", "vắng", "vẻ", "nhấp", "nhô"]}),
        q("*5. \"Xắc\" là từ chỉ đồ vật. Em hãy tìm các từ chỉ đồ vật khác trong bài."),
        memorize()],
       listen(("loắt choắt", "xinh xinh", "thoăn thoắt"), ("thoăn thoắt", "nghênh nghênh", "loắt choắt"),
              ("ca lô", "cái xắc", "chim chích"), ("chim chích", "ca lô", "đòng đòng"),
              ("đòng đòng", "vắng vẻ", "nhấp nhô"), ("nhấp nhô", "vèo vèo", "xinh xinh")),
       images={img(314, "đường quê"): "Con đường quê vàng nắng chạy giữa cánh đồng lúa đang trổ đòng đòng; "
                                      "một chú chim chích nhảy trên đường; xa xa có lũy tre và dãy núi thấp "
                                      "(không có người)"},
       notes=[("khac_sach", KS_REAL.format(who="chú bé liên lạc", what="con đường quê giữa đồng lúa có chim chích")),
              ("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)],
       review=[("part1[0]", "tranh thay hình chú bé liên lạc (người thật); lời dẫn tranh do app soạn"),
               ("@4. Tìm những từ láy", "từ láy do app chọn: loắt choắt, xinh xinh, thoăn thoắt, nghênh nghênh, vèo vèo, "
                             "vắng vẻ, đòng đòng, nhấp nhô")])

# 315 — Bài 7. Ai can đảm (tr.14–15)
NGONG = img(315, "đàn ngỗng")
NGONG_DESC = ("Sân nhà quê có túp nhà tranh và bụi tre: đàn ngỗng trắng vươn dài cổ, kêu quàng quạc; cậu bé Tiến "
              "cầm cành xoan xua đàn ngỗng, cậu bé Thắng cầm thanh kiếm gỗ nấp sau lưng Tiến, xa xa cậu bé Hùng "
              "đang chạy biến")
lesson(315, [14, 15],
       [picture(NGONG, "Tiến cầm cành xoan xua đàn ngỗng.", "đàn ngỗng"),
        title("Ai can đảm"),
        *prose("NHỊ HÀ phỏng dịch",
               ["- Bây giờ thì mình không sợ gì hết! | Hùng vừa nói vừa giơ khẩu súng lục bằng nhựa ra khoe."],
               ["- Mình cũng vậy, mình không sợ gì hết! - Thắng vừa nói vừa vung thanh kiếm gỗ lên."],
               ["Tiến chưa kịp nói gì thì một đàn ngỗng đi vào sân.",
                "Chúng vươn dài cổ, kêu quàng quạc, chúi mỏ về phía trước, định đớp bọn trẻ."],
               ["Hùng đút vội khẩu súng vào túi quần và chạy biến.",
                "Thắng tưởng đàn ngỗng đến giật kiếm của mình, mồm mếu máo, nấp vào sau lưng Tiến."],
               ["Tiến không có súng, cũng chẳng có kiếm.", "Em liền nhặt một cành xoan, xua đàn ngỗng ra xa.",
                "Đàn ngỗng kêu quàng quạc, cổ vươn dài, chạy miết."]),
        *glossary("Đớp: há miệng (mỏ) ngoạm thật nhanh."),
        q("1. Vì sao Hùng và Thắng thoạt đầu đều tỏ ý không sợ sệt gì cả?", marker="?"),
        q("2. Khi thấy đàn ngỗng chúi mỏ về phía trước, định đớp bọn trẻ, hai bạn ấy làm gì?"),
        q("3. Ai mới thật sự là người can đảm ở đây? Vì sao em biết?"),
        q("*4. Tìm từ trái nghĩa với từ \"can đảm\"."),
        q("5. Tìm một từ chỉ loài vật, một từ chỉ cây cối và hai từ chỉ đồ vật trong bài.")],
       listen(("đàn ngỗng", "cành xoan", "kiếm gỗ"), ("cành xoan", "đàn ngỗng", "túi quần"),
              ("kiếm gỗ", "cành xoan", "quàng quạc"), ("quàng quạc", "mếu máo", "chạy miết"),
              ("mếu máo", "quàng quạc", "can đảm"), ("can đảm", "chạy miết", "đàn ngỗng")),
       images={NGONG: NGONG_DESC},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 316 — Bài 8. Làm cách nào dễ hơn (Bài đọc thêm, tr.15–16; sách không có tranh)
lesson(316, [15, 16],
       [title("Làm cách nào dễ hơn", "Bài đọc thêm"),
        *prose("TRẦN CAO THỤY phỏng dịch",
               ["Ba cậu bé rủ nhau vào rừng.", "Trong rừng có nấm, có quả rừng, lại có đủ các thứ chim.",
                "Ba cậu mải chơi nên không để ý là trời đã về chiều, sắp tối.", "Về bây giờ thì sợ lắm!"],
               ["Cả ba cố nghĩ ngợi tìm xem cách nào dễ hơn: | nói dối hay là thú thật?"],
               ["Cậu thứ nhất nói:"],
               ["- Tớ sẽ nói dối là bị chó sói đuổi ở trong rừng.",
                "Bố tớ phát hoảng lên và thế là thôi không mắng nữa."],
               ["Cậu thứ hai nói:"],
               ["- Tớ sẽ nói là đang đi đường thì gặp ông ngoại.", "Mẹ tớ sẽ vui và cũng không mắng tớ."],
               ["Cậu thứ ba nói:"],
               ["- Còn mình thì mình sẽ nói thật, vì nói thật thì chẳng cần phải nghĩ tìm cách này hay cách khác."],
               ["Thế rồi ba cậu bé chia tay nhau về nhà.",
                "Cậu thứ nhất vừa nói với bố xong thì đúng lúc bác coi rừng đến chơi.", "Bác nói:"],
               ["- Không, trong rừng này làm gì có chó sói."],
               ["Người cha bực tức vô cùng.",
                "Vì tội đi chơi về muộn cũng đủ tức lắm rồi, vậy mà lại còn nói dối nữa nên tức lên gấp đôi."],
               ["Cậu thứ hai đang nói với mẹ là đi đường gặp ông ngoại | thì vừa lúc ông ngoại bước vào."],
               ["Bà mẹ cũng bực tức vô cùng.",
                "Vì tội đi chơi về muộn cũng đủ tức lắm rồi, vậy mà lại còn nói dối nữa nên tức lên gấp đôi."],
               ["Còn cậu thứ ba, vừa về đến nhà, đã nhận lỗi ngay từ cửa.",
                "Bố cậu chỉ căn dặn một câu và hoàn toàn tha thứ cho cậu."])],
       listen(("nói dối", "thú thật", "nói thật"), ("thú thật", "nói dối", "nhận lỗi"), ("chó sói", "quả rừng", "ông ngoại"),
              ("nhận lỗi", "tha thứ", "bực tức"), ("tha thứ", "nhận lỗi", "chó sói"), ("bực tức", "thú thật", "tha thứ")),
       notes=[("khac_sach", KS_SPLIT)])

# 317 — Chính tả tuần 19 (tr.16–17)
HON_DA = ["Hòn đá to", "Hòn đá nặng", "Chỉ một người", "Nhấc không đặng."]
lesson(317, [16, 17],
       [title("Chính tả: Trên đường đến nhà lao", "Nghe đọc"),
        title("Bài viết: \"Bầu trời... tự nhiên\".", "Phần này con viết vào vở cùng bố mẹ."),
        words("Côn Đảo", "Bến Đầm", "chị Sáu", "triền", "say sưa", "uốn", "ríu rít", "vỗ"),
        title("Viết lại các từ chỉ tên riêng trong bài: Côn Đảo, Bến Đầm, Sáu.",
              "Phần này con viết vào vở cùng bố mẹ."),
        fill(["triền", "chiền"], ("triền núi", "triền", "triền"), ("chiền chiện", "chiền", "chiền")),
        fill(["say", "xay"], ("xay thóc", "xay", "xay"), ("say mê", "say", "say")),
        fill(["uốn", "uống"], ("uốn éo", "uốn", "uốn"), ("uốn cong", "uốn", "uốn"), ("uống nước", "uống", "uống")),
        fill(["vỗ", "vổ"], ("vỗ tay", "vỗ", "vỗ"), ("sóng vỗ", "vỗ", "vỗ"), ("răng vổ", "vổ", "vổ")),
        title("Chính tả: Hòn đá to", "Trí nhớ"),
        title("Bài viết: Cả bài.", "Phần này con viết vào vở cùng bố mẹ."),
        words("nhấc", "người", "nhiều", "nặng", "lên", "đặng", "việc", "chỉ"),
        fill(["nhấc", "nhắc"], ("nhấc hòn đá lên", "nhấc", "nhấc"), ("nhắc nhở", "nhắc", "nhắc")),
        fill(["nặng", "lặng"], ("hòn đá nặng", "nặng", "nặng"), ("im lặng", "lặng", "lặng"),
             ("việc nặng nhọc", "nặng", "nặng")),
        q("Viết câu ngắn: câu có chữ nhấc, câu có chữ nhắc.", lines=["Câu có chữ nhấc.", "Câu có chữ nhắc."])],
       listen(("triền núi", "chiền chiện", "say mê"), ("xay thóc", "say mê", "uốn cong"), ("uống nước", "uốn éo", "vỗ tay"),
              ("răng vổ", "vỗ tay", "sóng vỗ"), ("nhắc nhở", "nhấc lên", "im lặng"), ("im lặng", "nặng nhọc", "nhắc nhở")),
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Điền chỗ trống làm bằng chạm thẻ; viết câu ngắn thì bé nói câu cùng bố mẹ."),
              ("khac_sach", "Cụm \"... nhở em học bài\" rút ngắn thành \"nhắc nhở\" cho vừa khung.")],
       review=[("part1[4]", "đáp án triền/chiền theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[5]", "đáp án say/xay theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[6]", "đáp án uốn/uống theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[7]", "đáp án vỗ/vổ theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[11]", "đáp án nhấc/nhắc theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[12]", "đáp án nặng/lặng theo chính tả chuẩn (sách không in đáp án)")])

# 318 — Từ ngữ: Thiếu nhi dũng cảm (tr.17–18)
lesson(318, [17, 18],
       [title("Từ ngữ: Thiếu nhi dũng cảm"),
        title("Những từ ngữ cần ghi nhớ"),
        words("chú bé liên lạc", "mặt trận", "súng đạn", "nhà lao"),
        words("gian khổ", "hiểm nghèo", "can đảm"),
        title("Bài tập: Tìm từ ngữ thích hợp điền vào những chỗ trống"),
        fill_passage(["Anh Kim Đồng là một [chú bé liên lạc|nhà lao|súng đạn] rất [can đảm|mặt trận|nhà lao].",
                      "Tuy không chiến đấu ở [mặt trận|chú bé liên lạc|can đảm], nhưng nhiều khi đi liên lạc, "
                      "anh cũng gặp những giây phút hết sức [hiểm nghèo|nhà lao|mặt trận].",
                      "Năm 15 tuổi, anh đã ngã xuống vì [súng đạn|can đảm|mặt trận] của giặc "
                      "nhưng tấm gương sáng của anh vẫn còn mãi mãi.",
                      "Năm 14 tuổi, chị Võ Thị Sáu đã là một chiến sĩ công an rất gan dạ.",
                      "Hoạt động trong hoàn cảnh vô cùng [gian khổ|súng đạn|mặt trận], chị vẫn luôn miệng ca hát.",
                      "Giặc bắt được chị, nhưng [nhà lao|can đảm|hiểm nghèo] và còng xích của kẻ thù "
                      "cũng không làm cho chị khiếp sợ."]),
        q("2. Tìm một số từ gần nghĩa với từ: can đảm.")],
       listen(("mặt trận", "nhà lao", "súng đạn"), ("nhà lao", "mặt trận", "gian khổ"), ("gian khổ", "hiểm nghèo", "can đảm"),
              ("hiểm nghèo", "gian khổ", "mặt trận"), ("can đảm", "gan dạ", "nhà lao"), ("gan dạ", "can đảm", "hiểm nghèo")),
       notes=[("khac_sach", "Điền từ: mỗi chỗ trống 3 thẻ do app chọn trong các từ ngữ cần ghi nhớ, tránh hai từ cùng "
                            "đúng; đáp án do app soạn."),
              ("khac_sach", KS_ORAL)],
       review=[("part1[5]", "đáp án điền từ do app soạn: chú bé liên lạc, can đảm, mặt trận, hiểm nghèo, súng đạn, "
                            "gian khổ, nhà lao")])

# 319 — Ngữ pháp: Danh từ (tiếp theo) (tr.18)
lesson(319, [18],
       [title("Ngữ pháp: Danh từ", "Tiếp theo"),
        q("1. Em tìm những từ chỉ cây cối trong các bài \"Trên đường đến nhà lao\" và \"Chú bé liên lạc\"."),
        q("2. Em kể một số từ chỉ cây cối, hoa quả mà em biết."),
        find("3. Trong bài \"Chú bé liên lạc\", những từ nào chỉ đồ vật?",
             {"word": ["xắc", "ca", "lô", "đạn", "thư"]}, text=LIEN_LAC),
        q("4. Em hãy kể một số từ chỉ đồ vật dùng trong nhà (ví dụ: bàn, ghế, giường...)."),
        *rule("Những từ chỉ cây cối, hoa quả, đồ vật cũng gọi là danh từ.")],
       listen(("cây cối", "hoa quả", "đồ vật"), ("hoa quả", "cây cối", "danh từ"), ("cái xắc", "ca lô", "cái bàn"),
              ("cái bàn", "cái ghế", "cái xắc"), ("cái giường", "cái bàn", "ca lô"), ("danh từ", "đồ vật", "hoa quả")),
       notes=[("khac_sach", KS_ORAL)],
       review=[("part1[3]", "từ chỉ đồ vật trong bài Chú bé liên lạc do app chọn: xắc, ca lô, đạn, thư")])

# 320 — Tập làm văn: Trả lời câu hỏi — Trên đường đến nhà lao (tr.18)
lesson(320, [18],
       [title("Tập làm văn: Trả lời câu hỏi"),
        title("Đề bài: Trên đường đến nhà lao.", "Xem tranh ở bài Trên đường đến nhà lao."),
        picture(CON_DAO, "Con nhớ lại con đường ven biển Côn Đảo nhé.", "bờ biển"),
        q("1. Bầu trời trong buổi bình minh ở Côn Đảo như thế nào?"),
        q("2. Con đường từ Bến Đầm đến nhà lao có gì đẹp?"),
        q("3. Trên cành cây có tiếng gì vui?"),
        q("4. Trước cảnh đẹp tự nhiên, chị Sáu đã làm gì?")],
       listen(("bình minh", "bầu trời", "con đường"), ("con đường", "cành cây", "bình minh"),
              ("cành cây", "bầu trời", "tự nhiên"), ("bầu trời", "bình minh", "cành cây"),
              ("tự nhiên", "con đường", "bầu trời"), ("bờ biển", "tự nhiên", "cành cây")),
       images={CON_DAO: CON_DAO_DESC},
       notes=[("khac_sach", KS_TLC)],
       review=[("part1[2]", "lời dẫn tranh do app soạn")])
print("tuần 19 xong")
