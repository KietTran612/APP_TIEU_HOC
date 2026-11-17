"""Tuần 33 (mục 427–434), tr.115–121, ảnh 058–061."""
from l2t2lib import *
from w32 import TO_NUOC

# 427 — Bài 63. Phong cảnh quê hương Bác (tr.115; sách không có tranh)
QUE_BAC = img(427, "quê Bác")
QUE_BAC_DESC = ("Đứng trên núi nhìn xuống: bên trái dòng sông Lam uốn khúc theo dãy núi, mặt sông lấp lánh nắng chiều "
                "thành đường quanh co trắng xóa; bên phải dãy núi nối liền xa xa; giữa hai dãy núi là cánh đồng nhiều "
                "màu xanh (mía, lúa chiêm, tre, phi lao), làng nối làng, mái nhà nhỏ (không có người)")
QUE_BAC_CT = ["Hôm chúng tôi đứng trên núi Chung, | nhìn sang bên trái là dòng sông Lam uốn khúc theo dãy núi Thiên Nhẫn.",
              "Mặt sông hắt ánh nắng chiếu thành một đường quanh co trắng xóa.",
              "Nhìn sang bên phải là dãy núi Trác nối liền với dãy núi Đại Huệ xa xa.",
              "Trước mặt chúng tôi, giữa hai dãy núi, là nhà Bác với cánh đồng quê Bác."]
lesson(427, [115],
       [picture(QUE_BAC, "Dòng sông Lam và cánh đồng quê Bác.", "quê Bác"),
        title("Phong cảnh quê hương Bác"),
        *prose("HOÀI THANH và THANH TỊNH", ["Phong cảnh vùng này quả thật là đẹp."], QUE_BAC_CT,
               ["Nhìn xuống cánh đồng, có đủ các màu xanh: | xanh pha vàng của ruộng mía, "
                "xanh rất mượt mà của lúa chiêm đương thời con gái, xanh đậm của những rặng tre, | "
                "đây đó một vài cây phi lao xanh biếc và rất nhiều màu xanh khác nữa."],
               ["Cả cánh đồng thu gọn trong tầm mắt, làng nối làng, ruộng tiếp ruộng.",
                "Cuộc sống ở đây có một cái gì mặn mà, ấm áp."]),
        q("1. Nhà Bác và cánh đồng quê Bác nằm giữa hai dãy núi đẹp. Đó là những dãy núi nào? (Bên trái? Bên phải?).",
          marker="?"),
        q("2. Dòng sông Lam đẹp như thế nào? (Hình dáng? Ánh sáng? Màu sắc?)."),
        q("3. Kể những màu xanh khác nhau trên cánh đồng quê Bác."),
        q("4. Đặt câu với mỗi từ: xanh biếc, ấm áp."),
        q("*5. Tìm các danh từ riêng trong bài. Xếp các từ đó theo thứ tự trong bảng chữ cái.")],
       listen(("sông Lam", "cánh đồng", "dãy núi"), ("cánh đồng", "sông Lam", "ruộng mía"), ("ruộng mía", "lúa chiêm", "rặng tre"),
              ("rặng tre", "phi lao", "ruộng mía"), ("xanh biếc", "ấm áp", "mặn mà"), ("ấm áp", "xanh biếc", "quanh co")),
       images={QUE_BAC: QUE_BAC_DESC},
       notes=[("khac_sach", "Sách không có tranh; app vẽ cảnh sông Lam và cánh đồng quê Bác để bài Tập làm văn tuần 33 "
                            "dùng lại."),
              ("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)],
       review=[("part1[0]", "tranh và lời dẫn tranh do app thêm (sách không có tranh)")])

# 428 — Bài 64. Nắng Ba Đình (Học thuộc lòng, tr.116–117)
lesson(428, [116, 117],
       [picture(img(428, "Ba Đình"), "Quảng trường Ba Đình và lăng Bác trong nắng thu.", "Ba Đình"),
        title("Nắng Ba Đình", "Học thuộc lòng"),
        *sentences("Nắng Ba Đình mùa thu", "Thắm vàng trên lăng Bác", "Vẫn trong vắt bầu trời", "Ngày Tuyên ngôn độc lập.",
                   "Ta đi trên quảng trường", "Bâng khuâng như vẫn thấy", "Nắng reo trên lễ đài", "Có bàn tay Bác vẫy.",
                   "Ấm lòng ta biết mấy", "Ánh mắt Bác nheo cười", "Lồng lộng một vòm trời", "Sau mái đầu của Bác..."),
        passage("poem", "NGUYỄN PHAN HÁCH", breaks=[4, 8]),
        q("1. Cảnh lăng Bác về mùa thu có gì đẹp?", marker="?"),
        q("2. Đi trên quảng trường Ba Đình, tác giả tưởng tượng như vẫn trông thấy Bác đứng trên lễ đài "
          "với những nét rất cụ thể. Những câu thơ nào cho em biết điều đó?"),
        q("3. \"Bàn tay Bác vẫy\", \"ánh mắt Bác nheo cười\", những hình ảnh này cho em biết tình cảm gì "
          "của Bác đối với nhân dân ta?"),
        q("4. Đặt câu với mỗi từ: trong vắt, vẫy."),
        memorize()],
       listen(("Ba Đình", "quảng trường", "lễ đài"), ("quảng trường", "Ba Đình", "vòm trời"), ("lễ đài", "vòm trời", "bàn tay"),
              ("vòm trời", "lễ đài", "quảng trường"), ("bâng khuâng", "lồng lộng", "trong vắt"),
              ("lồng lộng", "bâng khuâng", "Tuyên ngôn")),
       images={img(428, "Ba Đình"): "Quảng trường Ba Đình mùa thu nắng vàng: lăng Bác bằng đá xám ở giữa, cột cờ cao "
                                    "có lá cờ đỏ sao vàng bay, thảm cỏ xanh kẻ ô vuông phía trước, hàng cây hai bên, "
                                    "trời trong vắt có vài đám mây (không có chữ, không có người)"},
       notes=[("khac_sach", "Tranh sách có hàng người vào lăng nhỏ xíu; app vẽ quảng trường không có người, không có chữ."),
              ("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)])

# 429 — Bài 65. Không có ngọn núi nào cao hơn (tr.117–118)
NUI_NGUA = img(429, "núi đá")
lesson(429, [117, 118],
       [picture(NUI_NGUA, "Dãy núi đá giống hình con ngựa, mây trắng bay quanh.", "núi đá"),
        title("Không có ngọn núi nào cao hơn"),
        *prose("HỒNG TRANG",
               ["Trước nhà Ún Xinh có dãy núi đá trông giống hình con ngựa.", "Núi rất cao.",
                "Chỉ có đám mây trắng buổi sáng, mây hồng buổi chiều là cưỡi ngựa được thôi."],
               ["Có lần Ún Xinh hỏi Ún Hảo:"], ["- Có ai cưỡi được con ngựa kia không?"], ["Ún Hảo gật đầu và nói:"],
               ["- Có Bác Hồ."],
               ["Thế rồi, Ún Hảo kể lại câu chuyện đã được nghe ông kể: | \"Khắp bản mường ta, Bác Hồ đã đi qua cả.",
                "Cái gậy Bác chống đã mòn gần hết nhưng đôi chân Bác vẫn khỏe.", "Bác đã leo qua dãy núi đó\"."],
               ["Ún Xinh nhớ mãi câu chuyện ấy.", "Không có ngọn núi nào cao hơn Bác được đâu."]),
        *glossary("Bản mường: làng mạc (của đồng bào miền núi)."),
        q("1. Trước nhà Ún Xinh có dãy núi giống hình con gì?", marker="?"),
        q("2. Tại sao lại nói: chỉ có mây cưỡi ngựa được thôi?"),
        q("3. Câu \"Cái gậy Bác chống đã mòn gần hết\" ý nói gì?"),
        q("4. Vì sao Ún Xinh lại nghĩ: \"Không có ngọn núi nào cao hơn Bác\"?"),
        q("5. Tìm từ gần nghĩa với từ leo. Đặt câu với từ đó.")],
       listen(("núi đá", "con ngựa", "đám mây"), ("con ngựa", "núi đá", "bản mường"), ("đám mây", "mây hồng", "cái gậy"),
              ("bản mường", "cái gậy", "con ngựa"), ("cái gậy", "bản mường", "núi đá"), ("mây hồng", "đám mây", "bản mường")),
       images={NUI_NGUA: "Vùng núi phía Bắc: dãy núi đá cao trông giống hình con ngựa đang phi, mây trắng quấn quanh "
                         "lưng núi, bụi cây rậm phía dưới; hai bạn nhỏ người dân tộc đứng nhìn, một bạn giơ tay chỉ "
                         "lên đỉnh núi"},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 430 — Bài 66. Hoa phượng (Bài đọc thêm, tr.119; sách không có tranh)
lesson(430, [119],
       [title("Hoa phượng", "Bài đọc thêm"),
        *sentences("Hôm qua còn lấm tấm", "Chen lẫn màu lá xanh", "Sáng nay bừng lửa thẫm", "Rừng rực cháy trên cành.",
                   "- \"Bà ơi! Sao mà nhanh", "Phượng mở nghìn mắt lửa", "Cả dãy phố nhà mình", "Một trời hoa phượng đỏ.",
                   "Hay đêm qua không ngủ", "Chị gió quạt cho cây", "Hay mặt trời ủ lửa", "Cho hoa bừng hôm nay\"."),
        passage("poem", "LÊ HUY HÒA", breaks=[4, 8])],
       listen(("hoa phượng", "dãy phố", "mặt trời"), ("dãy phố", "hoa phượng", "chị gió"), ("lấm tấm", "rừng rực", "lửa thẫm"),
              ("rừng rực", "lấm tấm", "mắt lửa"), ("mắt lửa", "lửa thẫm", "dãy phố"), ("chị gió", "mặt trời", "hoa phượng")))

# 431 — Chính tả tuần 33 (tr.119–120)
lesson(431, [119, 120],
       [title("Chính tả: Phong cảnh quê hương Bác", "Nghe đọc"),
        title("Bài viết: \"Hôm chúng tôi... quê Bác\".", "Phần này con viết vào vở cùng bố mẹ."),
        words("Chung", "Lam", "Thiên Nhẫn", "Trác", "Đại Huệ", "dòng", "xóa", "uốn", "hắt", "dãy"),
        find("a) Viết những tên riêng có hai tiếng trong bài chính tả.",
             {"word": ["thiên", "nhẫn", "đại", "huệ"]}, text=[x for t in QUE_BAC_CT for x in t.split(" | ")]),
        fill(["xóa", "xáo"], ("tẩy xóa", "xóa", "xóa"), ("ăn bát xáo măng", "xáo", "xáo"), ("trắng xóa", "xóa", "xóa")),
        fill(["uốn", "uống"], ("uốn cong", "uốn", "uốn"), ("uống nước", "uống", "uống"), ("uốn éo", "uốn", "uốn"),
             ("uống thuốc", "uống", "uống")),
        fill(["dãy", "giải", "dải"], ("dãy núi", "dãy", "dãy"), ("dãy phố", "dãy", "dãy"), ("giải thưởng", "giải", "giải"),
             ("dải yếm", "dải", "dải"), ("đoạt giải", "giải", "giải")),
        title("Chính tả: Tổ nước ta", "Trí nhớ"),
        title("Bài viết: Cả bài.", "Phần này con viết vào vở cùng bố mẹ."),
        words("Hồng Bàng", "Văn Lang", "Phù Đổng", "chưa", "cứu", "tuổi", "mười", "vẻ"),
        q("a) Viết lại những địa danh trong bài theo thứ tự bảng chữ cái.", lines=TO_NUOC[:2]),
        fill(["cứu", "kíu"], ("cứu nước", "cứu", "cứu"), ("cứu nhà", "cứu", "cứu"), ("ngỗng kêu kíu kíu", "kíu", "kíu")),
        fill(["tuổi", "tủi"], ("em lên bảy tuổi", "tuổi", "tuổi"), ("đừng làm nó tủi thân", "tủi", "tủi")),
        fill(["vẻ", "vẽ"], ("vẻ vang", "vẻ", "vẻ"), ("vui vẻ", "vẻ", "vẻ"), ("tranh vẽ", "vẽ", "vẽ"), ("ong vò vẽ", "vẽ", "vẽ"))],
       listen(("tẩy xóa", "xáo măng", "trắng xóa"), ("uốn cong", "uống nước", "uống thuốc"), ("dãy núi", "giải thưởng", "dải yếm"),
              ("cứu nước", "kíu kíu", "tuổi"), ("tủi thân", "bảy tuổi", "vẻ vang"), ("tranh vẽ", "vui vẻ", "ong vò vẽ")),
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Tìm tên riêng hai tiếng làm bằng chạm chữ; viết địa danh theo thứ tự: bé nói cùng bố mẹ; "
                            "điền chỗ trống làm bằng chạm thẻ.")],
       review=[("part1[3]", "tên riêng hai tiếng do app chọn: Thiên Nhẫn, Đại Huệ"),
               ("part1[4]", "đáp án xóa/xáo theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[5]", "đáp án uốn/uống theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[6]", "đáp án dãy/giải/dải theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[11]", "đáp án cứu/kíu theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[12]", "đáp án tuổi/tủi theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[13]", "đáp án vẻ/vẽ theo chính tả chuẩn (sách không in đáp án)")])

# 432 — Từ ngữ: Bác Hồ (tr.120)
lesson(432, [120],
       [title("Từ ngữ: Bác Hồ"),
        title("Những từ ngữ cần ghi nhớ"),
        words("chiến khu", "nhà sàn", "vườn cây", "ao cá", "quảng trường", "lễ đài", "Tuyên ngôn độc lập"),
        words("đơn sơ", "giản dị", "thương yêu", "ân cần", "quyến luyến"),
        title("Bài tập: Điền từ ngữ thích hợp vào những chỗ trống"),
        fill_passage(["Bác Hồ sống rất [giản dị|chiến khu|lễ đài].",
                      "Hồi còn lãnh đạo cách mạng và kháng chiến ở [chiến khu|nhà sàn|ao cá] Việt Bắc, "
                      "Bác sống và làm việc trên một căn [nhà sàn|quảng trường|lễ đài] mái tranh vách nứa.",
                      "Kháng chiến thắng lợi. Bác về Thủ đô cũng chỉ sống và làm việc ở một ngôi nhà sàn "
                      "[đơn sơ|quyến luyến|thương yêu].",
                      "Xung quanh nhà có [vườn cây|lễ đài|quảng trường], [ao cá|chiến khu|lễ đài] "
                      "do chính tay Bác chăm nom, vun trồng.",
                      "Bác Hồ rất [thương yêu|quyến luyến|đơn sơ] các cháu thiếu nhi.",
                      "Bác thường gửi thư thăm hỏi các cháu.",
                      "Được đến thăm Bác, cháu nào cũng [quyến luyến|giản dị|ân cần] không muốn rời Bác.",
                      "Hằng năm cứ đến ngày mồng 2 tháng 9, nhân dân cả nước ta lại nhớ đến hình ảnh Bác Hồ đứng đọc "
                      "[Tuyên ngôn độc lập|chiến khu|vườn cây] trên [lễ đài|nhà sàn|ao cá] ở "
                      "[quảng trường|chiến khu|vườn cây] Ba Đình chói chang ánh nắng mùa thu."])],
       listen(("chiến khu", "nhà sàn", "vườn cây"), ("ao cá", "quảng trường", "lễ đài"), ("nhà sàn", "chiến khu", "ao cá"),
              ("lễ đài", "quảng trường", "vườn cây"), ("đơn sơ", "giản dị", "ân cần"), ("quyến luyến", "thương yêu", "đơn sơ")),
       notes=[("khac_sach", "Điền từ: mỗi chỗ trống 3 thẻ do app chọn trong các từ ngữ cần ghi nhớ, tránh hai từ cùng "
                            "đúng; đáp án do app soạn.")],
       review=[("part1[5]", "đáp án và thẻ chọn do app soạn: giản dị, chiến khu, nhà sàn, đơn sơ, vườn cây, ao cá, "
                            "thương yêu, quyến luyến, Tuyên ngôn độc lập, lễ đài, quảng trường")])

# 433 — Ngữ pháp: Ôn tập: Danh từ (tr.121)
lesson(433, [121],
       [title("Ngữ pháp: Ôn tập: Danh từ"),
        q("1. Tìm 2 danh từ chung chỉ người,",
          lines=["2 danh từ chung chỉ loài vật,", "2 danh từ chung chỉ đồ vật,", "2 danh từ chung chỉ cây cối,",
                 "2 danh từ chung chỉ hoa quả."], marker="?"),
        q("2. Danh từ riêng chỉ tên người phải viết như thế nào? Ví dụ."),
        q("3. Danh từ riêng chỉ địa danh (núi, sông, xã, huyện, tỉnh...) phải viết như thế nào? Ví dụ."),
        q("4. Tìm và viết: 1 danh từ riêng chỉ tên người, 1 danh từ riêng chỉ tên sông, 1 danh từ riêng chỉ tên núi,",
          lines=["1 danh từ riêng chỉ tên huyện (hoặc quận),", "1 danh từ riêng chỉ tên tỉnh (hoặc thành phố),",
                 "1 danh từ riêng chỉ tên một nước bạn."])],
       listen(("danh từ chung", "danh từ riêng", "địa danh"), ("danh từ riêng", "danh từ chung", "hoa quả"),
              ("địa danh", "hoa quả", "cây cối"), ("hoa quả", "cây cối", "đồ vật"), ("cây cối", "đồ vật", "loài vật"),
              ("đồ vật", "loài vật", "địa danh")),
       notes=[("khac_sach", "Bảng \"2 – loài vật, 2 – đồ vật...\" trong sách viết thành dòng đọc được. " + KS_ORAL)])

# 434 — Tập làm văn: Dùng từ – đặt câu (tr.121)
lesson(434, [121],
       [title("Tập làm văn: Dùng từ – đặt câu"),
        title("Đề bài: Dựa vào bài \"Phong cảnh quê hương Bác\", em hãy dùng mỗi từ ngữ sau đây "
              "đặt thành hai câu nói về quê hương Bác Hồ:"),
        picture(QUE_BAC, "Con nhớ lại cảnh quê hương Bác nhé.", "quê Bác"),
        words("Quê Bác", "xanh", "phong cảnh"),
        q("Em hãy đặt hai câu với mỗi từ ngữ trên.")],
       listen(("quê Bác", "phong cảnh", "sông Lam"), ("phong cảnh", "quê Bác", "cánh đồng"), ("sông Lam", "cánh đồng", "quê Bác"),
              ("cánh đồng", "sông Lam", "phong cảnh"), ("màu xanh", "phong cảnh", "sông Lam"), ("dãy núi", "màu xanh", "cánh đồng")),
       images={QUE_BAC: QUE_BAC_DESC},
       notes=[("khac_sach", KS_DAT_CAU),
              ("khac_sach", "App hiện lại tranh bài Phong cảnh quê hương Bác và thêm câu nhắc đặt câu (trang chỉ in đề bài).")],
       review=[("part1[2]", "lời dẫn tranh do app soạn"), ("part1[4]", "câu nhắc đặt câu do app thêm")])
print("tuần 33 xong")
