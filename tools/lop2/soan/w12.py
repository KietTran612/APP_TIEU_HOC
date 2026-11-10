"""Tuần 12 (mục 258–265), tr.80–86, ảnh 041–044. Đáp án câu đố tr.122."""
from l2lib import *

LUA_IMG = "img_b258_canhs_ddoongf_luas"
LUA_DESC = ("Cánh đồng lúa chín vàng óng trải rộng, các cô bác nông dân đội nón trắng dàn hàng ngang gặt lúa, "
            "bó lúa vàng xếp trên bờ ruộng; xa xa là lũy tre làng và con đường có xe chở lúa về sân phơi")
FRUITS = {
    "Quả nhãn": ("img_b261_quar_nhanx", "Chùm nhãn chín vỏ nâu vàng, một quả bóc dở thấy cùi trắng trong và hạt đen"),
    "Quả vải": ("img_b55_chumf_vair", "Chùm vải chín ba quả tròn, vỏ sần, có cuống"),
    "Quả mít": ("img_b261_quar_mits", "Quả mít to vỏ gai xanh vàng, bên cạnh có mấy múi mít vàng ươm"),
    "Quả bí": ("img_b261_quar_bis", "Quả bí đao dài vỏ xanh phủ phấn trắng, có lá và hoa bí vàng"),
    "Quả đu đủ": ("img_b13_ddu_ddur", "Một quả đu đủ chín, thuôn dài, có cuống nhỏ"),
}
RIDDLES = [
    (["Da cóc mà bọc bột lọc", "Bột lọc mà bọc hòn than."], "Quả nhãn", ["Quả vải", "Quả mít"]),
    (["Da cóc mà bọc bột lọc", "Bột lọc mà bọc hòn son."], "Quả vải", ["Quả nhãn", "Quả đu đủ"]),
    (["Da cóc mà bọc trứng gà", "Bổ ra thơm nức cả nhà muốn ăn."], "Quả mít", ["Quả bí", "Quả nhãn"]),
    (["Dùng làm mứt, hoặc nấu canh", "Đến khi mất sắc, theo anh học trò."], "Quả bí", ["Quả đu đủ", "Quả vải"]),
    (["Tên em không thiếu, chẳng thừa", "Chín vàng ngon ngọt rất vừa lòng anh."], "Quả đu đủ", ["Quả mít", "Quả bí"]),
]

# 258 — Bài 43. Cánh đồng lúa chín (tr.80–81)
lesson(258, [80, 81],
       [picture(LUA_IMG, "Cánh đồng lúa chín vàng, mọi người đang gặt lúa.", "cánh đồng"),
        title("Cánh đồng lúa chín"),
        *prose("TRÚC MAI",
               ["Ánh nắng ban mai trải xuống cánh đồng vàng óng, xua tan dần hơi lạnh mùa đông.",
                "Lúa nặng trĩu bông, ngả đầu vào nhau, thoang thoảng hương thơm.",
                "Từng cơn gió nhẹ làm cả biển vàng rung rinh như gợn sóng.",
                "Đàn chim gáy ở đâu bay về gù vang cánh đồng,", "như hòa nhịp với tiếng hát trên các thửa ruộng.",
                "Các tổ lao động đang thoăn thoắt đưa tay hái, xén ngang từng bụi lúa.",
                "Nón trắng nhấp nhô, mọi người dàn thành hàng ngang",
                "như một đoàn quân đang nhịp nhàng tiến bước."],
               ["Ngày mùa, cánh đồng lúa trông thật là đẹp mắt."]),
        q("1. Những từ ngữ nào cho em biết cánh đồng lúa rất tốt?", marker="?"),
        q("2. Tìm những từ tả màu sắc của cánh đồng lúa chín."),
        q("3. Ngoài màu sắc đẹp đẽ được nhìn thấy, đứng ở cánh đồng lúa chín, ta còn ngửi thấy mùi gì và nghe "
          "thấy âm thanh gì?"),
        q("4. Câu nào tả cảnh mọi người đang hăng say gặt lúa?"),
        q("5. Đặt câu với mỗi từ: thoăn thoắt, nhấp nhô.")],
       listen(("vàng óng", "trĩu bông", "rung rinh"), ("thoang thoảng", "thoăn thoắt", "nhấp nhô"), ("chim gáy", "nón trắng", "thửa ruộng"),
              ("nhấp nhô", "nhịp nhàng", "thoang thoảng"), ("ngày mùa", "ban mai", "mùa đông"), ("rung rinh", "vàng óng", "nhịp nhàng")),
       images={LUA_IMG: LUA_DESC},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)])

# 259 — Bài 44. Lũy tre (Học thuộc lòng, tr.82–83)
POEM44 = ["Mỗi sớm mai thức dậy", "Lũy tre xanh rì rào", "Ngọn tre cong gọng vó", "Kéo mặt trời lên cao.",
          "Những trưa đồng đầy nắng", "Trâu nằm nhai bóng râm", "Tre bần thần nhớ gió", "Chợt về đầy tiếng chim.",
          "Mặt trời xuống núi ngủ", "Tre nâng vầng trăng lên", "Sao, sao treo đầy cành", "Suốt đêm dài thắp sáng.",
          "Bỗng gà lên tiếng gáy", "Xôn xao ngoài lũy tre", "Đêm chuyển dần về sáng", "Mầm măng đợi nắng về."]
lesson(259, [82, 83],
       [picture("img_b259_luyx_tre", "Lũy tre xanh, chú trâu nằm dưới bóng râm.", "lũy tre"),
        title("Lũy tre", "Học thuộc lòng"),
        *sentences(*POEM44),
        passage("poem", "NGUYỄN CÔNG DƯƠNG", breaks=[4, 8, 12]),
        *glossary("Lũy tre: nhiều bụi tre trồng thành dãy dày bao quanh làng xóm."),
        q("1. Nhìn mặt trời nhô lên ở đầu bụi tre, tác giả tưởng tượng ngọn tre đang làm gì?", marker="?"),
        q("2. Buổi trưa thường có những loài vật nào đến với lũy tre và đến để làm gì?"),
        q("3. Vào đêm có trăng sao, tác giả thấy lũy tre như thế nào?"),
        q("4. Sắp xếp lại thứ tự các từ ngữ sau đây cho thành câu (mỗi câu xếp 2 cách):",
          lines=["khuất dần – sau lũy tre – mặt trời", "về tổ – lúc chiều tối – chim bay"]),
        memorize()],
       listen(("lũy tre", "gọng vó", "bóng râm"), ("rì rào", "bần thần", "xôn xao"), ("vầng trăng", "mặt trời", "mầm măng"),
              ("gọng vó", "lũy tre", "tiếng chim"), ("xôn xao", "rì rào", "thắp sáng"), ("mầm măng", "vầng trăng", "bóng râm")),
       images={"img_b259_luyx_tre": "Bụi tre xanh cao vút bên đường làng, ngọn tre cong như gọng vó, chim đậu trên cành; "
                                    "dưới bóng râm gốc tre chú trâu nằm nhai cỏ"},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL),
              ("khac_sach", "Câu 4 sắp xếp từ ngữ: bé nói thành câu cùng bố mẹ.")])

# 260 — Bài 45. Con đường làng (Bài đọc thêm, tr.83–84; sách không có tranh)
POEM45 = ["Con đường làng", "Vừa mới đắp", "Đã xanh ngắt", "Hàng phi lao", "Gió xôn xao", "Về đưa võng",
          "Chim vui sướng", "Đến chuyền cành", "Bướm từng đàn", "Bay rộn rã.",
          "Con đường làng", "Vừa mới đắp", "Xe chở thóc", "Đã hò reo", "Nối đuôi nhau", "Cười khúc khích.",
          "Con đường làng", "Vừa mới đắp", "Em đến lớp", "Mới tinh sương", "Trông thấy đường", "Sao đẹp thế!"]
lesson(260, [83, 84],
       [title("Con đường làng", "Bài đọc thêm"),
        *sentences(*POEM45),
        passage("poem", "NGUYỄN NGỌC KÍ", breaks=[10, 16])],
       listen(("phi lao", "đường làng", "chuyền cành"), ("xôn xao", "rộn rã", "khúc khích"), ("chở thóc", "nối đuôi", "đưa võng"),
              ("khúc khích", "hò reo", "xôn xao"), ("tinh sương", "xanh ngắt", "rộn rã"), ("đưa võng", "chở thóc", "phi lao")))

# 261 — Bài 46. Câu đố: Quả gì? (Bài đọc thêm, tr.84; đáp án tr.122)
part1 = [title("Câu đố: Quả gì?", "Bài đọc thêm")]
for lines, answer, others in RIDDLES:
    part1 += sentences(*lines, "(Là quả gì?)")
    part1.append({"type": "riddle_answer", "answer": answer, "image": FRUITS[answer][0],
                  "options": [{"image": FRUITS[o][0], "text": o} for o in others]})
rounds = []
for k, (lines, answer, others) in enumerate(RIDDLES):
    opts = [FRUITS[answer][0]] + [FRUITS[o][0] for o in others]
    opts = opts[k % 3:] + opts[:k % 3]
    rounds.append({"word": answer, "prompt": " ".join(lines) + " Là quả gì?", "answer": FRUITS[answer][0], "options": opts})
lesson(261, [84, 122], part1,
       [{"kind": "listen_picture", "rounds": rounds},
        *listen(("bột lọc", "hòn than", "hòn son"), ("thơm nức", "ngon ngọt", "mất sắc"))],
       images={img: desc for img, desc in FRUITS.values()},
       notes=[("khac_sach", "Sách in câu đố thành từng cặp câu, không ghi \"(là quả gì?)\"; app thêm dòng hỏi và "
                            "hiện đáp án lấy ở tr.122 \"Giải đáp câu đố\" ngay sau mỗi câu đố.")],
       review=[("part1[4]", "đáp án câu đố theo tr.122; tranh đáp án nhãn, mít, bí vẽ mới, vải và đu đủ dùng lại tranh "
                            "đã có")])

# 262 — Chính tả tuần 12 (tr.84–85)
lesson(262, [84, 85],
       [title("Chính tả: Bến cảng Hải Phòng", "Nghe đọc"),
        title("Bài viết: Cả bài.", "Phần này con nghe bố mẹ đọc rồi viết vào vở."),
        words("giữa", "mênh mông", "chuyển", "dãy", "nối đuôi", "hải quân"),
        combine("giữa", "sông", "chính"),
        combine("chuyển", "động", "lay"),
        fill(["dãy", "giãy"], ("dãy núi", "dãy", "dãy"), ("giãy đành đạch", "giãy", "giãy")),
        fill(["đuôi", "đui"], ("đuôi cá", "đuôi", "đuôi"), ("đui mù", "đui", "đui")),
        fill(["hải", "hãi"], ("hải quân", "hải", "hải"), ("sợ hãi", "hãi", "hãi")),
        title("Tập chép: Cánh đồng lúa chín", "Nhìn bảng"),
        title("Bài viết: \"Ánh nắng... thửa ruộng\".", "Phần này con chép vào vở cùng bố mẹ."),
        words("trĩu", "thoang thoảng", "gợn", "rung rinh", "tan", "trải"),
        choose("Trong các chữ nặng, sóng, bông, nước: chữ nào có thể ghép với chữ trĩu?",
               ["nặng", "sóng", "bông", "nước"], [0]),
        choose("Chữ nào có thể ghép với chữ gợn?", ["nặng", "sóng", "bông", "nước"], [1]),
        fill(["rung", "dung"], ("rung rinh", "rung", "rung"), ("gió rung cây", "rung", "rung"), ("dung dăng dung dẻ", "dung", "dung")),
        fill(["tan", "tang"], ("sương tan", "tan", "tan"), ("đám tang", "tang", "tang"), ("tan nát", "tan", "tan")),
        fill(["trải", "trại"], ("trải chiếu", "trải", "trải"), ("trại nuôi gà", "trại", "trại"))],
       listen(("giữa sông", "chính giữa", "chuyển động"), ("lay chuyển", "dãy núi", "đuôi cá"), ("hải quân", "sợ hãi", "đui mù"),
              ("nặng trĩu", "gợn sóng", "rung rinh"), ("sương tan", "đám tang", "trải chiếu"), ("trại nuôi gà", "dung dăng", "thoang thoảng")),
       notes=[("khac_sach", KS_WRITE), ("khac_sach", "Ghép chữ, đố chữ, điền chỗ trống làm bằng chạm hoặc kéo thẻ.")],
       review=[("part1[5]", "đáp án dãy/giãy"), ("part1[6]", "đáp án đuôi/đui"), ("part1[7]", "đáp án hải/hãi"),
               ("part1[11]", "đáp án do app soạn: nặng trĩu (trĩu bông cũng nói được)"),
               ("part1[12]", "đáp án do app soạn: gợn sóng"), ("part1[13]", "đáp án rung/dung"),
               ("part1[14]", "đáp án tan/tang"), ("part1[15]", "đáp án trải/trại")])

# 263 — Từ ngữ: Nông thôn (tr.85–86)
lesson(263, [85, 86],
       [title("Từ ngữ: Nông thôn"),
        title("Những từ ngữ cần ghi nhớ"),
        words("làng", "xóm", "hợp tác xã", "nông dân", "lũy tre", "đường làng", "cánh đồng", "thửa ruộng", "ngày mùa"),
        words("vàng óng", "rộn rã", "thoăn thoắt"),
        title("Bài tập: Chọn từ thích hợp để điền vào bài sau đây", "Ngày mùa chốn làng quê"),
        fill_passage(["Cánh đồng trước làng rộng mênh mông, lúa trĩu bông một màu [vàng óng].",
                      "Quang cảnh xóm làng [rộn rã] hẳn lên giữa mùa gặt hái.",
                      "Bà con xã viên tay liềm tay hái [thoăn thoắt] gặt hết [thửa ruộng] này đến thửa ruộng khác.",
                      "Trên con [đường làng], đoàn xe cải tiến chất đầy những bó lúa vàng đang nối đuôi nhau tiến về "
                      "sân phơi..."],
                     bank=["vàng óng", "rộn rã", "thoăn thoắt", "thửa ruộng", "đường làng", "cánh đồng", "lũy tre"])],
       listen(("hợp tác xã", "nông dân", "lũy tre"), ("đường làng", "cánh đồng", "thửa ruộng"), ("ngày mùa", "vàng óng", "rộn rã"),
              ("thoăn thoắt", "rộn rã", "vàng óng"), ("nông dân", "hợp tác xã", "ngày mùa"), ("thửa ruộng", "đường làng", "lũy tre")),
       notes=[("khac_sach", "Điền từ bằng chạm hoặc kéo thẻ; thẻ lấy từ các từ ngữ cần ghi nhớ, đáp án do app soạn.")],
       review=[("part1[5]", "đáp án điền từ do app soạn")])

# 264 — Ngữ pháp: Tiếng và chữ (tr.86)
lesson(264, [86],
       [title("Ngữ pháp: Tiếng và chữ"),
        *rule("Câu có thể tách ra thành nhiều tiếng.", "Khi nói, từng tiếng có thể ngắt ra rõ ràng.",
             "Khi viết, mỗi tiếng viết thành một chữ."),
        *rule("Ví dụ: Sài/Gòn/là/thành/phố/có/vinh/dự/được/mang/tên/Bác/."),
        q("1. Tìm số tiếng trong các câu sau:",
          lines=["Cảng Sài Gòn có nhiều bến.", "Bến Nhà Rồng là nơi Bác Hồ đã ra đi để tìm đường cứu nước."]),
        q("2. Em hãy đặt một câu với từ thành phố. Câu em đặt có mấy tiếng? Được viết thành mấy chữ?")],
       listen(("thành phố", "vinh dự", "bến cảng"), ("tiếng", "chữ", "câu"), ("vinh dự", "cứu nước", "thành phố"),
              ("cứu nước", "vinh dự", "rõ ràng"), ("rõ ràng", "thành phố", "cứu nước"), ("chữ", "câu", "tiếng")),
       notes=[("khac_sach", KS_ORAL)])

# 265 — Tập làm văn: Quan sát tranh và trả lời câu hỏi — Cánh đồng lúa chín (tr.86)
lesson(265, [86],
       [title("Tập làm văn: Quan sát tranh và trả lời câu hỏi"),
        title("Đề bài: Cánh đồng lúa chín.", "Xem tranh ở bài Cánh đồng lúa chín."),
        picture(LUA_IMG, "Con nhìn kĩ tranh cánh đồng lúa chín nhé.", "cánh đồng"),
        q("1. Bức tranh này vẽ cảnh gì? Tại sao em biết bức tranh vẽ cánh đồng lúa chín?"),
        q("2. Dưới ruộng, mọi người đang làm gì?"),
        q("3. Trên đường về thôn, xe cải tiến đang chở gì?"),
        q("4. Hình ảnh nào cho ta biết cánh đồng được mùa?"),
        q("5. Trong bức tranh này, em thích hình ảnh nào nhất?")],
       listen(("cánh đồng", "lúa chín", "gặt lúa"), ("gặt lúa", "cánh đồng", "được mùa"), ("được mùa", "gặt lúa", "nón trắng"),
              ("nón trắng", "được mùa", "lúa chín"), ("lúa chín", "nón trắng", "cánh đồng"), ("xe cải tiến", "bó lúa", "được mùa")),
       images={LUA_IMG: LUA_DESC},
       notes=[("khac_sach", "Tập làm văn quan sát tranh: app dùng lại tranh bài Cánh đồng lúa chín; bé trả lời miệng.")],
       review=[("part1[2]", "lời dẫn tranh do app soạn")])
