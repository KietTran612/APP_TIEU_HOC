"""Tuần 17 (mục 297–304), tr.115–121, ảnh 058–061."""
from l2lib import *

BAVI_IMG = "img_b298_trai_ba_vif"
BAVI_DESC = ("Nông trường Ba Vì: đàn bò sữa lông loang trắng đen gặm cỏ trên đồng cỏ xanh rộng, hàng rào gỗ chạy dài, "
             "mấy cây xanh, xa xa là dãy núi Ba Vì cao giữa trời")
POEM63 = ["Đầu năm, thăm trại Ba Vì", "Phởn phơ bò giống, xanh rì cỏ non.", "Bò to như chú voi con",
          "Lạ lùng quê mới, mắt tròn ngó quanh.", "Suối Hai hồ nước trong xanh", "Tản Viên, núi đẹp như tranh giữa trời."]
POEM64 = ["Một đường dây điện", "Từ phía chân trời", "Chạy đến xã tôi", "Cột cao, cao vút.",
          "Hàng cột như bước", "Từng bước qua đồng", "Cột vượt sang sông", "Lao xa nhanh nhẹn.",
          "Một đôi chim én", "Bay đậu trên dây", "Đậu rồi lại bay", "Bay xong lại ngắm.",
          "Trên cao thăm thẳm", "Đôi én reo vang:", "\"Đường dây qua làng", "Xưa đâu có thấy!\"."]
POEM65 = ["Đây là cây xà cừ", "Lá tròn và xanh biếc.", "Đây là cây bạch đàn", "Lá xanh thoa phấn bạc.",
          "Khắp ngả đường quê ta", "Cây xòe cho bóng mát", "Cây cùng ta về nhà", "Cây đưa ta đi học.",
          "Chúng em vâng lời Bác", "Trồng tiếp những hàng cây", "Cho mùa đông xanh tươi", "Cho mùa hè gió hát.",
          "Và hàng cây nhớ Bác", "Cứ vươn dài, vươn dài..."]

# 297 — Bài 62. Mùa xuân đến (tr.115–116)
lesson(297, [115, 116],
       [picture("img_b297_mua_xuaan_ddeens", "Mùa xuân đến, chim chóc bay nhảy trên cành hoa.", "mùa xuân"),
        title("Mùa xuân đến"),
        *prose("NGUYỄN KIÊN",
               ["Hoa mận vừa tàn thì mùa xuân đến.", "Bầu trời ngày thêm xanh.", "Nắng vàng ngày càng rực rỡ.",
                "Vườn cây lại đâm chồi, nảy lộc.", "Rồi vườn cây ra hoa.", "Hoa bưởi nồng nàn.", "Hoa nhãn ngọt.",
                "Hoa cau thoảng qua.", "Vườn cây lại đầy tiếng chim và bóng chim bay nhảy.",
                "Những thím chích chòe nhanh nhảu.", "Những chú khướu lắm điều.", "Những anh chào mào đỏm dáng.",
                "Những bác cu gáy trầm ngâm..."],
               ["Chú chim sâu vui cùng vườn cây và các loài chim bạn.",
                "Nhưng trong trí nhớ thơ ngây của chú còn mãi mãi sáng ngời hình ảnh",
                "một cành hoa mận trắng, biết nở cuối mùa đông để báo trước mùa xuân tới."]),
        *glossary("Mận: loài cây có hoa trắng, quả màu nâu hay xanh nhạt, ăn có vị ngọt chua.",
                 "Khướu: loài chim mình đen, hót rất hay.", "Trầm ngâm: có dáng lặng lẽ như đang suy nghĩ."),
        q("1. Một năm có mấy mùa? Hãy kể theo thứ tự. Cái gì báo trước mùa xuân sắp đến?", marker="?"),
        q("2. Khi mùa xuân đến, cảnh vật thay đổi như thế nào? (bầu trời, cây cỏ, loài vật)"),
        q("3. Em hãy tìm trong bài những từ chỉ người đem dùng chỉ loài chim. Dùng như thế rất hay, tại sao?"),
        q("4. Trong bài này, có hai thứ được tả nhiều nhất. Đó là thứ gì?")],
       listen(("hoa mận", "hoa bưởi", "hoa cau"), ("chích chòe", "chào mào", "cu gáy"), ("nồng nàn", "nhanh nhảu", "trầm ngâm"),
              ("đỏm dáng", "lắm điều", "thơ ngây"), ("đâm chồi", "nảy lộc", "ra hoa"), ("trầm ngâm", "rực rỡ", "đỏm dáng")),
       images={"img_b297_mua_xuaan_ddeens": "Vườn cây mùa xuân: cành mận nở hoa trắng, chim chích chòe, chào mào, khướu "
                                            "đậu và bay nhảy trên các cành, chim sâu nhỏ chuyền cành, trời xanh"},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 298 — Bài 63. Thăm trại Ba Vì (Học thuộc lòng, tr.116–117)
lesson(298, [116, 117],
       [picture(BAVI_IMG, "Đàn bò sữa gặm cỏ ở trại Ba Vì.", "trại Ba Vì"),
        title("Thăm trại Ba Vì", "Học thuộc lòng"),
        *sentences(*POEM63),
        passage("poem", "TỐ HỮU"),
        *glossary("Ba Vì: tên một ngọn núi cao thuộc tỉnh Hà Tây ở về phía tây Thủ đô Hà Nội, còn gọi là núi Tản Viên. "
                 "Nông trường Ba Vì ở sát dưới chân núi, chuyên chăn nuôi các giống trâu bò quý nhập của nước ngoài."),
        q("1. Ở trại Ba Vì, ta chăn nuôi gì?", marker="?"),
        q("2. Tác giả ví con bò to như con gì?"),
        q("3. Tại sao lại nói bò \"lạ lùng quê mới\"?"),
        q("4. Cảnh Ba Vì có gì đẹp?"),
        q("5. Đặt câu với mỗi từ: lạ lùng, ngó."),
        memorize()],
       listen(("bò giống", "cỏ non", "voi con"), ("phởn phơ", "xanh rì", "lạ lùng"), ("Tản Viên", "Ba Vì", "Suối Hai"),
              ("lạ lùng", "phởn phơ", "trong xanh"), ("cỏ non", "bò giống", "hồ nước"), ("hồ nước", "núi đẹp", "cỏ non")),
       images={BAVI_IMG: BAVI_DESC},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)])

# 299 — Bài 64. Đường dây điện (tr.118)
lesson(299, [118],
       [picture("img_b299_dduwowngf_daay_ddieenj", "Cột điện cao vút bước qua cánh đồng.", "cột điện"),
        title("Đường dây điện"),
        *sentences(*POEM64),
        passage("poem", "VÕ QUẢNG", breaks=[4, 8, 12]),
        q("1. Tác giả tưởng tượng hàng cột điện biết cử động như người qua những từ nào?", marker="?"),
        choose("2. Hàng cột ấy từ xa đi tới và còn đi rất xa. Tìm câu thơ nói lên điều đó (đọc kĩ khổ 1 và 2).",
               POEM64[:8], [1, 2, 6, 7]),
        q("3. Đường dây điện bắc qua làng đã lâu chưa? Vì sao em biết?"),
        q("4. Nỗi ngạc nhiên của chim én được bộc lộ ra trong những câu thơ nào?"),
        q("5. Đặt câu với mỗi từ sau đây: đậu, ngắm, cao vút, thăm thẳm.")],
       listen(("dây điện", "chân trời", "chim én"), ("cao vút", "thăm thẳm", "nhanh nhẹn"), ("hàng cột", "đường dây", "qua đồng"),
              ("nhanh nhẹn", "cao vút", "reo vang"), ("chim én", "dây điện", "hàng cột"), ("thăm thẳm", "nhanh nhẹn", "chân trời")),
       images={"img_b299_dduwowngf_daay_ddieenj": "Những cột điện cao vút bằng sắt nối dây điện bước qua cánh đồng và "
                                                  "vượt sang sông, một đôi chim én đậu trên dây, xa xa là núi"},
       notes=[("khac_sach", KS_ORAL)],
       review=[("part1[20]", "đáp án câu thơ do app soạn: Từ phía chân trời, Chạy đến xã tôi, Cột vượt sang sông, "
                             "Lao xa nhanh nhẹn")])

# 300 — Bài 65. Hàng cây trồng theo lời Bác (Bài đọc thêm, tr.119; sách không có tranh)
lesson(300, [119],
       [title("Hàng cây trồng theo lời Bác", "Bài đọc thêm"),
        *sentences(*POEM65),
        passage("poem", "NGUYỄN THANH TOÀN", breaks=[4, 8, 12])],
       listen(("xà cừ", "bạch đàn", "hàng cây"), ("xanh biếc", "phấn bạc", "bóng mát"), ("vâng lời", "trồng tiếp", "vươn dài"),
              ("bóng mát", "xanh tươi", "gió hát"), ("bạch đàn", "xà cừ", "đường quê"), ("vươn dài", "xanh biếc", "vâng lời")))

# 301 — Chính tả tuần 17 (tr.119–120)
lesson(301, [119, 120],
       [title("Chính tả: Mùa xuân đến", "Nghe đọc"),
        title("Bài viết: \"Hoa mận... trầm ngâm\".", "Phần này con nghe bố mẹ đọc rồi viết vào vở."),
        words("xuân", "thoảng", "chích chòe", "khướu", "đâm chồi", "tàn", "nảy lộc"),
        find("Tìm những chữ có uân trong các câu sau.", {"rime": ["uân"]},
             text=["Người đi như chẳng nhớ gì Tết xuân.", "Người đi quên hết gian truân.",
                   "Say mê như một dân quân trên đường."]),
        fill(["chồi", "trồi"], ("cây đâm chồi nảy lộc", "chồi", "chồi"), ("rễ cây trồi lên", "trồi", "trồi")),
        fill(["tàn", "tàng"], ("mùa đông đã tàn", "tàn", "tàn"), ("nhà bảo tàng", "tàng", "tàng"), ("hoa tàn", "tàn", "tàn")),
        title("Chính tả: Cây dừa", "Trí nhớ"),
        title("Bài viết: 6 câu đầu.", "Phần này con nhớ lại rồi viết vào vở."),
        words("tỏa", "bạc phếch", "lược", "chải", "trăng"),
        find("Gạch dưới chữ tỏa và chữ phếch trong các câu.", {"word": ["tỏa", "phếch"]},
             text=["Cây tỏa bóng mát.", "Khói tỏa mịt mù.", "Bức tường trắng phếch.", "Cây cau bạc phếch.",
                   "Cái áo trắng phếch."]),
        fill(["chải", "trải"], ("lược chải đầu", "chải", "chải"), ("dầu chải tóc", "chải", "chải"), ("trải chiếu", "trải", "trải"),
             ("trải thảm ra phơi", "trải", "trải")),
        fill(["trăng", "trăn"], ("vầng trăng sáng", "trăng", "trăng"), ("con trăn", "trăn", "trăn"))],
       listen(("mùa xuân", "chích chòe", "khướu"), ("đâm chồi", "nảy lộc", "rễ cây"), ("bảo tàng", "hoa tàn", "gian truân"),
              ("bạc phếch", "trắng phếch", "lược chải"), ("trải chiếu", "trải thảm", "vầng trăng"), ("con trăn", "dân quân", "mịt mù")),
       notes=[("khac_sach", KS_WRITE), ("khac_sach", "Tìm chữ, gạch dưới chữ, điền chỗ trống làm bằng chạm hoặc kéo thẻ.")],
       review=[("part1[4]", "đáp án chồi/trồi"), ("part1[5]", "đáp án tàn/tàng"), ("part1[10]", "đáp án chải/trải"),
               ("part1[11]", "đáp án trăng/trăn")])

# 302 — Từ ngữ: Ôn tập (tr.120–121)
lesson(302, [120, 121],
       [title("Từ ngữ: Ôn tập"),
        title("A – Trả lời câu hỏi"),
        q("1. Núi khác đồi thế nào?"),
        q("2. Kể tên ba phần khác nhau của một ngọn núi từ trên xuống dưới. Đèo ở đâu?"),
        q("3. Rừng có những gì nhiều và quý?"),
        q("4. Vịnh khác cảng như thế nào? Đảo nằm ở đâu?"),
        q("5. Ruộng khác nương thế nào? Rẫy là gì?"),
        title("B – Điền từ thích hợp vào chỗ trống", "thấp, bạc, rẫy, cảng, cao, vịnh, vàng, đèo"),
        fill_passage(["Núi [cao], đồi [thấp].", "Lên dốc xuống [đèo].", "Rừng [vàng] biển [bạc].",
                      "Phá [rẫy] làm nương.", "Tàu vào [vịnh] tránh bão.", "Tàu rời [cảng] ra khơi."],
                     bank=["thấp", "bạc", "rẫy", "cảng", "cao", "vịnh", "vàng", "đèo"])],
       listen(("núi", "đồi", "đèo"), ("vịnh", "cảng", "đảo"), ("ruộng", "nương", "rẫy"), ("rừng vàng", "biển bạc", "lên dốc"),
              ("tránh bão", "ra khơi", "phá rẫy"), ("đỉnh núi", "sườn núi", "chân núi")),
       notes=[("khac_sach", KS_ORAL), ("khac_sach", "Điền từ bằng chạm hoặc kéo thẻ; đáp án do app soạn.")],
       review=[("part1[8]", "đáp án điền từ do app soạn; \"Tàu vào ... tránh bão\" app chọn vịnh, \"Tàu rời ... ra khơi\" "
                            "app chọn cảng")])

# 303 — Ngữ pháp: Ôn: tiếng, từ, chữ, chữ cái (tr.121)
lesson(303, [121],
       [title("Ngữ pháp: Ôn: tiếng, từ, chữ, chữ cái"),
        q("1. Câu sau đây có mấy tiếng?", lines=["Nhân dân Việt Nam rất anh hùng."]),
        q("2. Câu trên gồm mấy từ?"),
        q("3. Tìm một từ gồm 2 tiếng ghép thành."),
        q("4. Chữ xương gồm mấy chữ cái? Chữ trường gồm mấy chữ cái?"),
        q("5. Tìm 1 chữ có 1 chữ cái (ví dụ: ô). Tìm 1 chữ có 2 chữ cái (ví dụ: ta), có 3 chữ cái (ví dụ: bàn), "
          "có 4 chữ cái (ví dụ: chân)."),
        q("6. Đọc thuộc lòng bảng chữ cái.")],
       listen(("nhân dân", "Việt Nam", "anh hùng"), ("anh hùng", "nhân dân", "chữ cái"), ("chữ cái", "bảng chữ", "tiếng"),
              ("xương", "trường", "chân"), ("bàn", "chân", "ta"), ("Việt Nam", "anh hùng", "bảng chữ")),
       notes=[("khac_sach", KS_ORAL)])

# 304 — Tập làm văn: Quan sát tranh và trả lời câu hỏi — Trại Ba Vì (tr.121)
lesson(304, [121],
       [title("Tập làm văn: Quan sát tranh và trả lời câu hỏi"),
        title("Đề bài: Trại Ba Vì.", "Xem tranh ở bài Thăm trại Ba Vì."),
        picture(BAVI_IMG, "Con nhìn kĩ tranh trại Ba Vì nhé.", "trại Ba Vì"),
        q("1. Trại bò giống Ba Vì nằm giữa những cảnh đẹp nào?"),
        q("2. Bò ở đây như thế nào?"),
        q("3. Đàn bò đang làm gì?"),
        q("4. Ở quê em có những trại chăn nuôi nào?")],
       listen(("trại bò", "đàn bò", "đồng cỏ"), ("đàn bò", "trại bò", "núi Ba Vì"), ("đồng cỏ", "đàn bò", "chăn nuôi"),
              ("chăn nuôi", "đồng cỏ", "trại bò"), ("núi Ba Vì", "chăn nuôi", "đàn bò"), ("bò giống", "núi Ba Vì", "đồng cỏ")),
       images={BAVI_IMG: BAVI_DESC},
       notes=[("khac_sach", "Tập làm văn quan sát tranh: app dùng lại tranh bài Thăm trại Ba Vì; bé trả lời miệng.")],
       review=[("part1[2]", "lời dẫn tranh do app soạn")])
