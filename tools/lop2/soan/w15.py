"""Tuần 15 (mục 282–289), tr.101–107, ảnh 051–054."""
from l2lib import *

BIEN_IMG = "img_b282_bieenr_ddepj"
BIEN_DESC = ("Bãi biển buổi sáng: mặt biển xanh sáng trong, những cánh buồm trắng ở xa như đàn bướm, mấy ngư dân kéo "
             "thuyền lên bãi cát, xa xa là dãy núi; sóng nhẹ tung bọt trắng")
POEM56 = ["Con chim chiền chiện", "Bay vút, vút cao", "Lòng đầy yêu mến", "Khúc hát ngọt ngào.",
          "Chim bay chim sà", "Lúa tròn bụng sữa", "Đồng quê chan chứa", "Những lời chim ca.",
          "Bay cao, cao vút", "Chim biến mất rồi", "Chỉ còn tiếng hót", "Làm xanh da trời."]

# 282 — Bài 55. Biển đẹp (tr.101–102)
BIEN_TEXT = [["Biển rất đẹp!", "Buổi sáng, nắng sớm tràn trên mặt biển.",
              "Mặt biển sáng trong như tấm thảm khổng lồ bằng ngọc thạch.",
              "Những cánh buồm trắng trên biển được nắng sớm chiếu vào sáng rực lên,",
              "ở xa trông như đàn bướm trắng lượn giữa trời xanh."],
             ["Buổi chiều nắng tàn, mát dịu, biển trong xanh như màu mảnh chai.",
              "Xa xa, về phía bắc, mấy ngọn núi màu tím pha hồng.",
              "Những đợt sóng nhè nhẹ liếm lên bãi cát, tung bọt trắng xóa."]]
lesson(282, [101, 102],
       [picture(BIEN_IMG, "Biển buổi sáng thật đẹp.", "biển"),
        title("Biển đẹp"),
        *prose("VŨ TÚ NAM", *BIEN_TEXT),
        *glossary("Ngọc thạch: một loại đá quý màu xanh nhạt."),
        q("1. Tìm những từ chỉ màu sắc đẹp trên mặt biển vào buổi sáng.", marker="?"),
        q("2. Buổi chiều, biển có những màu sắc gì đẹp?"),
        q("3. Tác giả so sánh những cánh buồm trắng với vật gì?"),
        q("4. Tìm từ trái nghĩa với \"khổng lồ\". Đặt một câu với từ \"khổng lồ\" và một câu với từ trái nghĩa của từ đó."),
        find("5. Tìm những chữ có 5 chữ cái trong bài trên.",
             {"word": ["chiếu", "chiều", "khổng", "những", "thạch", "trong", "trông", "trắng"]}, sentences_in=None)],
       listen(("ngọc thạch", "mảnh chai", "bãi cát"), ("khổng lồ", "nhè nhẹ", "trắng xóa"), ("cánh buồm", "đàn bướm", "mặt biển"),
              ("tím pha hồng", "trong xanh", "sáng rực"), ("nắng sớm", "nắng tàn", "mát dịu"), ("bãi cát", "bọt trắng", "ngọn núi")),
       images={BIEN_IMG: BIEN_DESC},
       notes=[("khac_sach", KS_SPLIT), ("khac_sach", KS_ORAL)],
       review=[("part1[16]", "đáp án chữ có 5 chữ cái do app đếm (ch, tr, ng, nh, kh, th tính là 2 chữ cái): chiếu, chiều, khổng, những, thạch, trong, trông, trắng")])

# 283 — Bài 56. Con chim chiền chiện (Học thuộc lòng, tr.102–103)
lesson(283, [102, 103],
       [picture("img_b283_chim_chieefn_chieenj", "Chim chiền chiện bay vút trên cánh đồng lúa.", "chim chiền chiện"),
        title("Con chim chiền chiện", "Học thuộc lòng"),
        *sentences(*POEM56),
        passage("poem", "HUY CẬN", breaks=[4, 8]),
        *glossary("Chiền chiện: còn gọi là chim sơn ca."),
        q("1. Chim bay vút và chim sà khác nhau thế nào?", marker="?"),
        q("2. Tác giả dùng những từ nào để tả chim chiền chiện bay rất cao?"),
        q("3. Câu thơ nào tả tiếng chim hót rất hay?"),
        q("4. Cánh đồng lúa có gì đẹp?"),
        choose("5. Trong 3 dòng dưới đây, dòng nào là câu, dòng nào chưa phải là câu? Chạm vào dòng là câu.",
               ["Con chim chiền chiện", "Chim bay chim sà", "Chim biến mất rồi"], [1, 2]),
        memorize()],
       listen(("chiền chiện", "sơn ca", "da trời"), ("vút cao", "ngọt ngào", "chan chứa"), ("bụng sữa", "đồng quê", "lời chim"),
              ("ngọt ngào", "yêu mến", "biến mất"), ("chan chứa", "ngọt ngào", "bay vút"), ("tiếng hót", "khúc hát", "lời chim")),
       images={"img_b283_chim_chieefn_chieenj": "Cánh đồng lúa xanh trổ bông bao la, mấy con chim chiền chiện bay vút "
                                                "lên trời cao, con đường nhỏ và hàng cây ven đồng"},
       notes=[("khac_sach", KS_HTL), ("khac_sach", KS_ORAL)],
       review=[("part1[20]", "đáp án dòng là câu do app soạn: Chim bay chim sà, Chim biến mất rồi")])

# 284 — Bài 57. Quê em vùng biển (tr.103–104)
POEM57 = ["Quê em ở vùng biển", "Phong cảnh đẹp vô cùng", "Nước biển xanh mênh mông", "Sóng xô tràn bãi cát.",
          "Sớm ngày vang tiếng hát", "Từng đoàn thuyền ra khơi", "Chiều ngả bóng mặt trời", "Thuyền về đầy ắp cá.",
          "Quê em giàu đẹp quá!", "Em tha thiết yêu quê."]
lesson(284, [103, 104],
       [picture("img_b284_beens_thuyeefn", "Thuyền đánh cá cập bến đầy ắp cá.", "thuyền"),
        title("Quê em vùng biển"),
        *sentences(*POEM57),
        passage("poem", "Tập đọc 1 – 1980", breaks=[4, 8]),
        q("1. Đứng ở bờ biển, ta thấy có gì đẹp? Từ \"mênh mông\" gợi lên ý gì?", marker="?"),
        q("2. Buổi sáng, cảnh bờ biển vui như thế nào?"),
        q("3. Em hiểu thế nào là đầy ắp? Đặt một câu với từ đầy ắp."),
        q("4. Tìm ba từ ở trong bài do 2 tiếng hợp thành."),
        q("5. \"Chiều ngả bóng mặt trời\", em hãy thay bằng cách nói khác có ý nghĩa giống như thế.")],
       listen(("vùng biển", "bãi cát", "ra khơi"), ("mênh mông", "đầy ắp", "tha thiết"), ("đầy ắp", "mênh mông", "phong cảnh"),
              ("phong cảnh", "vùng biển", "mặt trời"), ("ra khơi", "tiếng hát", "bãi cát"), ("tha thiết", "giàu đẹp", "đầy ắp")),
       images={"img_b284_beens_thuyeefn": "Bến thuyền làng biển: những con thuyền buồm cập bến dưới hàng dừa, ngư dân "
                                          "khiêng thúng cá đầy ắp lên bờ, phía xa là núi và mái nhà"},
       notes=[("khac_sach", KS_ORAL)])

# 285 — Bài 58. Mùa sương ở Hạ Long (Bài đọc thêm, tr.105; sách không có tranh)
lesson(285, [105],
       [title("Mùa sương ở Hạ Long", "Bài đọc thêm"),
        *prose("THI SẢNH",
               ["Đi giữa Hạ Long vào mùa sương,", "ta cảm thấy những hòn đảo vừa xa lạ, vừa quen thuộc, mờ mờ, ảo ảo.",
                "Chung quanh ta, sương buông trắng xóa.", "Con thuyền bơi trong sương như bơi trong mây.",
                "Tiếng sóng vỗ long bong bên mạn thuyền.", "Tiếng gõ thuyền lộc cộc của bạn chài săn cá,",
                "âm vang mặt vịnh.", "Thỉnh thoảng mấy con hải âu đột ngột hiện ra trong màn sương.",
                "Chúng dang cánh sà xuống mặt nước, rồi vội vã bay vọt lên, vô ý đập vào lá buồm."],
               ["Vào mùa sương, ngày ở Hạ Long như ngắn lại.",
                "Buổi sớm, mặt trời lên ngang cột buồm, sương tan, trời mới quang.",
                "Buổi chiều, nắng vừa nhạt, sương đã buông nhanh xuống mặt biển."]),
        *glossary("Vịnh: chỗ biển ăn sâu vào đất liền.",
                 "Hạ Long: tên một cảnh đẹp ở vịnh Bắc Bộ, thuộc bờ biển tỉnh Quảng Ninh.")],
       listen(("hòn đảo", "hải âu", "cột buồm"), ("mờ mờ", "ảo ảo", "trắng xóa"), ("long bong", "lộc cộc", "âm vang"),
              ("hải âu", "lá buồm", "mạn thuyền"), ("đột ngột", "vội vã", "quen thuộc"), ("cột buồm", "mặt vịnh", "hòn đảo")),
       notes=[("khac_sach", KS_SPLIT)])

# 286 — Chính tả tuần 15 (tr.105–106)
lesson(286, [105, 106],
       [title("Chính tả: Biển đẹp", "Nghe đọc"),
        title("Bài viết: \"Biển rất đẹp... giữa trời xanh\".", "Phần này con nghe bố mẹ đọc rồi viết vào vở."),
        words("bướm", "lượn", "buồm", "xa", "nắng", "biển"),
        find("Gạch dưới những chữ có vần ươm và ươn trong câu.", {"rime": ["ươm", "ươn"]}, text=["Hoa thơm bướm lượn."]),
        find("Gạch dưới những chữ có vần uôm trong câu.", {"rime": ["uôm"]}, text=["Ếch kêu uôm uôm, ao chuôm đầy nước."]),
        fill(["xa", "sa"], ("gần xa", "xa", "xa"), ("sao sa", "sa", "sa"), ("xa xỉ", "xa", "xa")),
        fill(["nắng", "nắn"], ("mưa nắng", "nắng", "nắng"), ("uốn nắn", "nắn", "nắn"), ("ánh nắng", "nắng", "nắng"),
             ("nắn nót", "nắn", "nắn")),
        title("Tập chép: Con chim chiền chiện", "Nhìn bảng"),
        title("Bài chép: Cả bài.", "Phần này con chép vào vở cùng bố mẹ."),
        words("chiền chiện", "ngọt ngào", "sà", "chan chứa", "biến", "sữa"),
        combine("chiền chiện", "hót", "bay"),
        combine("ngọt ngào", "tiếng nói", "lời ru", at="before"),
        fill(["chan", "chang"], ("chan chứa", "chan", "chan"), ("chan canh", "chan", "chan"), ("nắng chang chang", "chang", "chang")),
        fill(["sữa", "sửa"], ("sữa bò", "sữa", "sữa"), ("sửa lỗi", "sửa", "sửa"), ("sữa đậu nành", "sữa", "sữa"),
             ("sửa soạn", "sửa", "sửa"))],
       listen(("bướm lượn", "cánh buồm", "ao chuôm"), ("sao sa", "gần xa", "xa xỉ"), ("uốn nắn", "ánh nắng", "nắn nót"),
              ("chiền chiện hót", "tiếng nói", "lời ru"), ("chan canh", "nắng chang chang", "chan chứa"), ("sửa soạn", "sữa bò", "sửa lỗi")),
       notes=[("khac_sach", KS_WRITE), ("khac_sach", "Gạch dưới chữ, ghép chữ, điền chỗ trống làm bằng chạm hoặc kéo thẻ.")],
       review=[("part1[5]", "đáp án xa/sa"), ("part1[6]", "đáp án nắng/nắn"), ("part1[12]", "đáp án chan/chang"),
               ("part1[13]", "đáp án sữa/sửa")])

# 287 — Từ ngữ: Biển (tr.106)
lesson(287, [106],
       [title("Từ ngữ: Biển"),
        title("Những từ ngữ cần ghi nhớ"),
        words("biển (bể)", "vịnh", "bờ biển", "cảng", "bãi biển", "đảo"),
        words("mênh mông", "thoai thoải", "lộng gió", "ra khơi"),
        title("Bài tập 1: Điền ba từ dưới đây vào chỗ trống", "hải quân, hải đảo, hải sản"),
        fill_passage(["Biển cho ta rất nhiều [hải sản] quý.",
                      "Ở ngoài [hải đảo], các anh bộ đội phải canh phòng ngày đêm.",
                      "Trên mặt biển, tàu [hải quân] của ta đi tuần."],
                     bank=["hải quân", "hải đảo", "hải sản"]),
        title("Bài tập 2: Điền các từ ngữ sau đây vào chỗ trống", "thoai thoải, ra khơi, mênh mông, lộng gió"),
        fill_passage(["Biển rộng [mênh mông].", "Bãi biển [thoai thoải].", "Bờ biển luôn luôn [lộng gió].",
                      "Sáng sớm, đoàn thuyền đánh cá [ra khơi]."],
                     bank=["thoai thoải", "ra khơi", "mênh mông", "lộng gió"])],
       listen(("bãi biển", "bờ biển", "hải đảo"), ("hải quân", "hải sản", "hải đảo"), ("thoai thoải", "mênh mông", "lộng gió"),
              ("ra khơi", "lộng gió", "thoai thoải"), ("vịnh", "cảng", "đảo"), ("hải sản", "hải quân", "bãi biển")),
       notes=[("khac_sach", "Điền từ bằng chạm hoặc kéo thẻ; đáp án do app soạn.")],
       review=[("part1[5]", "đáp án điền từ do app soạn"), ("part1[7]", "đáp án điền từ do app soạn")])

# 288 — Ngữ pháp: Bảng chữ cái (tr.107)
lesson(288, [107],
       [title("Ngữ pháp: Bảng chữ cái"),
        *rule("Chữ Việt có 29 chữ cái."),
        {"type": "letter_pairs", "letters": ["a", "ă", "â", "b", "c", "d", "đ", "e", "ê", "g", "h", "i", "k", "l", "m",
                                              "n", "o", "ô", "ơ", "p", "q", "r", "s", "t", "u", "ư", "v", "x", "y"]},
        q("Em hãy học thuộc bảng chữ cái trên theo đúng thứ tự.")],
       listen(("chữ cái", "bảng chữ", "thứ tự"), ("thứ tự", "chữ cái", "học thuộc"), ("học thuộc", "thứ tự", "bảng chữ"),
              ("bảng chữ", "học thuộc", "chữ cái"), ("chữ Việt", "chữ cái", "thứ tự"), ("chữ cái", "chữ Việt", "học thuộc")),
       notes=[("khac_sach", "Bảng chữ cái thành các thẻ chữ thường – chữ hoa chạm để nghe (như bài 41 lớp 1). "
                            "Bé học thuộc cùng bố mẹ.")])

# 289 — Tập làm văn: Quan sát tranh và trả lời câu hỏi — Cảnh biển buổi sáng (tr.107)
lesson(289, [107],
       [title("Tập làm văn: Quan sát tranh và trả lời câu hỏi"),
        title("Đề bài: Cảnh biển buổi sáng.", "Xem tranh ở bài Biển đẹp."),
        picture(BIEN_IMG, "Con nhìn kĩ tranh biển buổi sáng nhé.", "biển"),
        q("1. Mặt biển buổi sáng ra sao?"),
        q("2. Những cánh buồm trắng trên biển trông đẹp như thế nào?"),
        q("3. Những chiếc thuyền đang làm gì?"),
        q("4. Trong tranh còn có hình ảnh nào đẹp?"),
        q("Dựa vào tranh, em hãy tự nghĩ ra 2 câu hỏi.")],
       listen(("mặt biển", "cánh buồm", "chiếc thuyền"), ("cánh buồm", "mặt biển", "bãi cát"), ("chiếc thuyền", "bãi cát", "cánh buồm"),
              ("bãi cát", "chiếc thuyền", "buổi sáng"), ("buổi sáng", "bãi cát", "mặt biển"), ("hình ảnh", "buổi sáng", "chiếc thuyền")),
       images={BIEN_IMG: BIEN_DESC},
       notes=[("khac_sach", "Tập làm văn quan sát tranh: app dùng lại tranh bài Biển đẹp; bé trả lời miệng.")],
       review=[("part1[2]", "lời dẫn tranh do app soạn")])
