"""Tuần 24 (mục 356–362), tr.50–54, ảnh 026–028."""
from l2t2lib import *

# 356 — Bài 28. Trần Quốc Toản ra quân (tr.50–51)
NGUA = img(356, "ngựa trắng")
NGUA_DESC = ("Sân trước cổng thành cổ lúc trời vừa rạng sáng: một con ngựa trắng phau thắng yên cương đứng chờ, "
             "lá cờ đỏ viền vàng cắm cạnh cổng bay phần phật trong gió, xa xa dãy núi (không có người, không có chữ)")
lesson(356, [50, 51],
       [picture(NGUA, "Con ngựa trắng phau và lá cờ đỏ bay trong gió.", "con ngựa"),
        title("Trần Quốc Toản ra quân"),
        *prose("NGUYỄN HUY TƯỞNG",
               ["Sáng hôm ấy, Trần Quốc Toản dậy sớm từ biệt mẹ già:"],
               ["- Con đi phen này thề sống chết với giặc. | Bao giờ đất nước được yên, con mới trở về..."],
               ["Bà mẹ nói:"],
               ["- Con đi vì nước nên mẹ chẳng giữ. | Mẹ chỉ có một mình con. | "
                "Mẹ mong con chóng thắng giặc trở về, để mẹ con ta sớm được sum họp."],
               ["Quốc Toản lạy mẹ rồi bước ra sân.", "Trời vừa rạng sáng.",
                "Mình mặc áo bào đỏ, vai mang cung tên, lưng đeo thanh gươm báu, Quốc Toản ngồi trên con ngựa trắng phau.",
                "Theo sau Quốc Toản là người tướng già và sáu trăm dũng sĩ, nón nhọn, giáo dài.",
                "Đoàn quân hăm hở ra đi trong tiếng chiêng trống rập rình."],
               ["Đoàn quân đã đi xa.",
                "Bà con ra tiễn vẫn còn trông thấy | lá cờ đỏ thêu sáu chữ vàng căng lên trong gió."]),
        q("1. Quốc Toản từ biệt mẹ đi đâu? Bà mẹ có giữ con ở nhà không?", marker="?"),
        q("2. Hình ảnh Trần Quốc Toản lúc ra quân đẹp đẽ và oai hùng như thế nào? "
          "(Đọc lại hai câu văn miêu tả hình ảnh đó)."),
        q("3. Những từ ngữ nào cho em biết đoàn quân của Quốc Toản đã ra đi rất hùng dũng?"),
        q("4. Đặt một câu với từ hăm hở."),
        q("5. Tìm trong bài: 1 danh từ riêng chỉ tên người, 1 danh từ chung chỉ người, "
          "1 danh từ chung chỉ loài vật, 1 danh từ chung chỉ đồ vật.")],
       listen(("áo bào", "cung tên", "thanh gươm"), ("cung tên", "áo bào", "con ngựa"), ("thanh gươm", "con ngựa", "lá cờ"),
              ("lá cờ", "chiêng trống", "cung tên"), ("hăm hở", "rập rình", "sum họp"), ("sum họp", "hăm hở", "dũng sĩ")),
       images={NGUA: NGUA_DESC},
       notes=[("khac_sach", KS_REAL.format(who="Trần Quốc Toản cưỡi ngựa, cầm cờ ra quân",
                                           what="con ngựa trắng và lá cờ đỏ trước cổng thành")),
              ("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)],
       review=[("part1[0]", "tranh thay hình Trần Quốc Toản (nhân vật lịch sử); lời dẫn tranh do app soạn")])

# 357 — Bài 29. Việt Nam có Bác (Học thuộc lòng, tr.51–52; sách không có tranh)
VN_CO_BAC = ["Bác là non nước, trời mây", "Việt Nam có Bác mỗi ngày đẹp hơn.", "Còn cao hơn đỉnh Trường Sơn",
             "Nghìn năm chung đúc tâm hồn ông cha.", "Điệu lục bát, khúc dân ca,", "Việt Nam là Bác, Bác là Việt Nam."]
lesson(357, [51, 52],
       [title("Việt Nam có Bác", "Học thuộc lòng"),
        *sentences(*VN_CO_BAC),
        passage("poem", "LÊ ANH XUÂN", breaks=[2, 4]),
        *glossary("Chung đúc...: ý nói tâm hồn (tình cảm và ý nghĩ) của Bác là kết quả của tất cả những gì tốt đẹp "
                  "mà ông cha ta hàng nghìn năm đã để lại."),
        q("1. \"Non nước, trời mây\" ở đây chỉ đất nước. Đó là đất nước nào?", marker="?"),
        q("2. Câu \"Việt Nam có Bác mỗi ngày đẹp hơn\" nói lên ý gì?"),
        q("3. Những câu thơ nào cho em biết Bác Hồ tiêu biểu cho tất cả những gì tốt đẹp của dân tộc Việt Nam?"),
        q("4. Bác Hồ đã có công ơn gì đối với đất nước và nhân dân ta?"),
        q("*5. Tìm một vài từ gần nghĩa với từ non nước."),
        memorize()],
       listen(("non nước", "trời mây", "dân ca"), ("trời mây", "non nước", "ông cha"), ("dân ca", "lục bát", "tâm hồn"),
              ("lục bát", "dân ca", "non nước"), ("tâm hồn", "ông cha", "trời mây"), ("ông cha", "tâm hồn", "lục bát")),
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)])

# 358 — Bài 30. Một chiều hè lịch sử (Bài đọc thêm, tr.52; sách không có tranh)
lesson(358, [52],
       [title("Một chiều hè lịch sử", "Bài đọc thêm"),
        *sentences("Bố kể chuyện Điện Biên", "Bộ đội mình chiến thắng", "Lũ Tây bị bắt sống", "Ta giải đi từng đàn.",
                   "Tướng Đờ Cát xin hàng", "Bốt đồn đều san phẳng", "Cờ quyết chiến quyết thắng",
                   "Tung bay trên nóc hầm.", "Chiều mùng bảy tháng năm", "Một chiều hè lịch sử."),
        passage("poem", "HOÀNG VƯỢNG"),
        *glossary("Chiến thắng Điện Biên Phủ: ngày 7 - 5 - 1954, quân dân ta đã thắng lớn ở Điện Biên Phủ "
                  "buộc giặc Pháp phải rút khỏi miền Bắc nước ta.")],
       listen(("bộ đội", "chiến thắng", "nóc hầm"), ("chiến thắng", "bộ đội", "bốt đồn"), ("bốt đồn", "nóc hầm", "lịch sử"),
              ("nóc hầm", "bốt đồn", "chiều hè"), ("chiều hè", "lịch sử", "bộ đội"), ("lịch sử", "chiều hè", "chiến thắng")))

# 359 — Chính tả tuần 24 (tr.53)
lesson(359, [53],
       [title("Chính tả: Voi Bà Triệu ra trận", "Nghe đọc"),
        title("Bài viết: \"Từ trên đầu voi... xuống đất\".", "Phần này con viết vào vở cùng bố mẹ."),
        words("Triệu Thị Trinh", "giục", "huỳnh huỵch", "quay", "xông", "chồm dựng", "kinh hoàng", "những"),
        q("a) Viết họ tên các bạn cùng bàn."),
        fill(["giục", "dục"], ("thúc giục", "giục", "giục"), ("hình bầu dục", "dục", "dục"), ("giục giã", "giục", "giục")),
        fill(["xông", "sông"], ("giục voi xông lên", "xông", "xông"), ("bơi qua sông", "sông", "sông")),
        q("c) Ghép từ thích hợp với: huỳnh huỵch, quay.", lines=["Ví dụ: chạy huỳnh huỵch; quay sang trái..."]),
        title("Chính tả: Trần Quốc Toản ra quân", "So sánh"),
        *sentences("Trần Quốc Toản dậy sớm từ biệt mẹ già.", "Trời vừa rạng sáng.",
                   "Đoàn quân hăm hở ra đi trong tiếng chiêng trống rập rình."),
        title("Bài viết: ba câu trên.", "Phần này con viết vào vở cùng bố mẹ."),
        words("dậy", "già", "rạng", "chiêng", "trống", "sáng", "tiếng", "hăm hở"),
        title("Phát âm phân biệt các cặp từ ngữ sau"),
        words("rạng đông", "hình dạng", "cái trống", "chống gậy"),
        words("cái chiêng", "con chiên", "rạng sáng", "rạn nứt"),
        q("b) Thêm chữ thích hợp vào các cặp từ sau đây.",
          lines=["... trong, chong...", "đoàn ..., ... đoàng", "hăm..., hăm...", "... sáng, ... sán"])],
       listen(("thúc giục", "bầu dục", "giục giã"), ("xông lên", "qua sông", "chồm dựng"), ("rạng đông", "hình dạng", "cái trống"),
              ("chống gậy", "cái trống", "con chiên"), ("cái chiêng", "con chiên", "rạn nứt"), ("rạn nứt", "rạng sáng", "chống gậy")),
       notes=[("khac_sach", KS_WRITE),
              ("khac_sach", "Viết họ tên, ghép từ, thêm chữ: bé nói cùng bố mẹ; cặp từ so sánh thành thẻ chạm để nghe. "
                            "Dấu \"≠\" giữa hai từ trong sách thay bằng dấu phẩy.")],
       review=[("part1[4]", "đáp án giục/dục theo chính tả chuẩn (sách không in đáp án)"),
               ("part1[5]", "đáp án xông/sông theo chính tả chuẩn (sách không in đáp án)")])

# 360 — Từ ngữ: Dân tộc Việt Nam (tiếp theo) (tr.53–54)
lesson(360, [53, 54],
       [title("Từ ngữ: Dân tộc Việt Nam", "Tiếp theo"),
        title("Những từ ngữ cần ghi nhớ"),
        words("quê hương", "đất nước", "quân dân", "chiến trường", "chiến sĩ", "anh hùng"),
        words("quyết chiến quyết thắng", "vì nước quên mình"),
        title("Bài tập: Điền từ ngữ thích hợp vào các chỗ trống"),
        fill_passage(["Dân tộc Việt Nam ta còn là một dân tộc có tinh thần "
                      "[quyết chiến quyết thắng|chiến trường|quê hương] bất kì kẻ thù xâm lược nào.",
                      "Trải qua hơn bốn nghìn năm lịch sử, [quân dân|chiến trường|vì nước quên mình] cả nước ta "
                      "luôn luôn đoàn kết một lòng",
                      "quyết tâm đánh đuổi bọn cướp nước để bảo vệ [quê hương|quân dân|chiến trường] thân yêu.",
                      "Biết bao [anh hùng|quê hương|đất nước], đã ngã xuống trên [chiến trường|quân dân|vì nước quên mình].",
                      "Họ đã nêu cao tấm gương [vì nước quên mình|quân dân|đất nước] cho chúng ta noi theo."])],
       listen(("quê hương", "đất nước", "quân dân"), ("chiến trường", "chiến sĩ", "anh hùng"), ("chiến sĩ", "chiến trường", "quê hương"),
              ("anh hùng", "quân dân", "đất nước"), ("quân dân", "anh hùng", "chiến trường"),
              ("vì nước quên mình", "quyết chiến quyết thắng", "quê hương")),
       notes=[("khac_sach", "Điền từ: mỗi chỗ trống 3 thẻ do app chọn trong các từ ngữ cần ghi nhớ, tránh hai từ cùng "
                            "đúng; đáp án do app soạn. Câu dài thứ hai tách làm hai dòng.")],
       review=[("part1[5]", "đáp án và thẻ chọn do app soạn: quyết chiến quyết thắng, quân dân, quê hương, anh hùng, "
                            "chiến trường, vì nước quên mình")])

# 361 — Ngữ pháp: Ôn tập: Danh từ (tr.54)
lesson(361, [54],
       [title("Ngữ pháp: Ôn tập: Danh từ"),
        q("1. Kể 2 danh từ riêng chỉ sông (hoặc núi).",
          lines=["Kể 2 danh từ riêng chỉ người.", "Kể 2 danh từ riêng chỉ huyện, tỉnh."]),
        q("2. Kể 2 danh từ chung chỉ người.",
          lines=["Kể 2 danh từ chung chỉ loài vật.", "Kể 2 danh từ chung chỉ cây cối.", "Kể 2 danh từ chung chỉ đồ vật."]),
        find("3. Tìm các danh từ riêng trong bài \"Việt Nam có Bác\".",
             {"word": ["việt", "nam", "bác", "trường", "sơn"]}, text=VN_CO_BAC)],
       listen(("danh từ riêng", "danh từ chung", "loài vật"), ("danh từ chung", "danh từ riêng", "cây cối"),
              ("loài vật", "cây cối", "đồ vật"), ("cây cối", "đồ vật", "loài vật"), ("đồ vật", "loài vật", "danh từ riêng"),
              ("Trường Sơn", "Việt Nam", "non nước")),
       notes=[("khac_sach", KS_ORAL)],
       review=[("@3. Tìm các danh từ riêng", "danh từ riêng do app chọn: Việt Nam, Bác (chỉ Bác Hồ), Trường Sơn")])

# 362 — Tập làm văn: Trả lời câu hỏi — Trần Quốc Toản ra quân (tr.54)
lesson(362, [54],
       [title("Tập làm văn: Trả lời câu hỏi"),
        title("Đề bài: Trần Quốc Toản ra quân.", "Xem tranh ở bài Trần Quốc Toản ra quân."),
        picture(NGUA, "Con nhớ lại buổi sáng Trần Quốc Toản ra quân nhé.", "con ngựa"),
        q("1. Quốc Toản làm gì trước lúc ra đi?"),
        q("2. Hình ảnh Trần Quốc Toản lúc ra quân trông đẹp và hùng dũng như thế nào?"),
        q("3. Theo sau Trần Quốc Toản có những ai?"),
        q("4. Đoàn quân lên đường ra sao?"),
        q("5. Khi đoàn quân đã đi xa, ta vẫn còn trông thấy gì?")],
       listen(("đoàn quân", "lá cờ", "con ngựa"), ("lá cờ", "đoàn quân", "tướng già"), ("con ngựa", "tướng già", "lá cờ"),
              ("tướng già", "con ngựa", "dũng sĩ"), ("dũng sĩ", "lá cờ", "đoàn quân"), ("hùng dũng", "hăm hở", "con ngựa")),
       images={NGUA: NGUA_DESC},
       notes=[("khac_sach", KS_TLC)],
       review=[("part1[2]", "lời dẫn tranh do app soạn")])
print("tuần 24 xong")
