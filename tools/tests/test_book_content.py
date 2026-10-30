"""Nội dung bài 18–80 của TV1 Tập 1: kiểm tra chung cho mọi bài và các điểm đối chiếu với trang sách."""

import unittest

from tapdoc.build import build_lesson, load_sources
from tapdoc.paths import CONTENT_SRC

L = {r.lesson["lesson_id"]: r.lesson for r in (build_lesson(s) for s in load_sources(CONTENT_SRC))}


def lid_of(no):
    return f"tv1_t1_b{no:02d}"


def types(no):
    return [s["type"] for s in L[lid_of(no)]["part1"]]


def steps(no, kind):
    return [s for s in L[lid_of(no)]["part1"] if s["type"] == kind]


def aud(spell):
    return [p["audio"] for p in spell["parts"]]


def notes(no):
    return [n["note"] for n in L[lid_of(no)]["review"]["can_duyet"]]


class BookTestCase(unittest.TestCase):
    def assert_lesson_basics(self, no):
        """Dựng được, đã đối chiếu trang, Phần 2 có 6–10 lượt, mọi đánh vần không rỗng."""
        lid = lid_of(no)
        self.assertIn(lid, L, f"chưa có bài {no}")
        lesson = L[lid]
        self.assertEqual(lesson["source"]["verification"], "page_verified", lid)
        self.assertTrue(6 <= len(lesson["part2"]) <= 10, f"{lid}: {len(lesson['part2'])} lượt")
        for i, st in enumerate(lesson["part1"]):
            spells = [st["spell"]] if "spell" in st else []
            spells += [sp for it in st.get("items", []) for sp in it.get("spells", [])]
            for sp in spells:
                self.assertTrue(sp["parts"], f"{lid} part1[{i}]: đánh vần rỗng")


class Lessons18To27Test(BookTestCase):
    def test_basics(self):
        for no in range(18, 28):
            with self.subTest(no=no):
                self.assert_lesson_basics(no)

    def test_b18_v(self):
        kw = steps(18, "keyword")[0]
        self.assertEqual(kw["text"], "tò vò")
        reading = steps(18, "reading")[0]
        rows = [i["row"] for i in reading["items"]]
        self.assertEqual(max(rows) + 1, 2)
        self.assertEqual(rows.count(0), 9)

    def test_b20_two_units(self):
        self.assertEqual([s["text"] for s in steps(20, "unit")], ["k", "kh"])
        self.assertEqual([s["text"] for s in steps(20, "keyword")], ["bó kê", "quả khế"])

    def test_b22_review_table(self):
        self.assertEqual(types(22)[:2], ["letter_grid", "combine_table"])
        table = steps(22, "combine_table")[0]
        k_row = next(i["row"] for i in table["items"] if i["role"] == "onset" and i["text"] == "k")
        self.assertEqual([i["text"] for i in table["items"] if i["role"] == "base" and i["row"] == k_row],
                         ["ke", "kê", "ki"])

    def test_b25_two_units(self):
        self.assertEqual([s["text"] for s in steps(25, "unit")], ["g", "gh"])

    def test_b26_gi_uses_temporary_name(self):
        spell = steps(26, "spell")[0]["spell"]
        self.assertEqual(spell["parts"][0]["audio"], "am_gi")
        self.assertTrue(any("'gi'" in n for n in notes(26)))

    def test_b26_two_sentence_lines(self):
        self.assertEqual([s["text"] for s in steps(26, "sentence")], ["dì giã gì đó?", "dì giã giò"])

    def test_b27_gi_row_has_gi(self):
        table = steps(27, "combine_table")[0]
        self.assertIn("gi", [i["text"] for i in table["items"] if i["role"] == "base"])

    def test_b24_no_s_x_listen_pair(self):
        for rd in L[lid_of(24)]["part2"]:
            texts = {o["text"] for o in rd["options"]}
            self.assertFalse({"s", "x"} <= texts, rd)



class Lessons28To36Test(BookTestCase):
    def test_basics(self):
        for no in range(28, 37):
            with self.subTest(no=no):
                self.assert_lesson_basics(no)

    def test_keywords(self):
        self.assertEqual([s["text"] for s in steps(28, "keyword")], ["bắp ngô"])
        self.assertEqual([s["text"] for s in steps(31, "keyword")], ["con thỏ"])
        self.assertEqual([s["text"] for s in steps(36, "keyword")], ["pí pa pí pô", "phố xá"])

    def test_temporary_names_flagged(self):
        self.assertTrue(any("'ngh'" in n for n in notes(29)))
        self.assertTrue(any("'qu'" in n for n in notes(35)))
        self.assertTrue(any("'q'" in n for n in notes(35)))

    def test_b32_review_table_and_sentence(self):
        self.assertEqual(types(32), ["letter_grid", "combine_table", "sentence"])
        self.assertEqual(steps(32, "sentence")[0]["marker"], "⌂")

    def test_b35_reading_has_quy(self):
        reading = steps(35, "reading")[0]
        self.assertIn("quy", [i["text"] for i in reading["items"]])

    def test_no_ch_tr_listen_pair(self):  # Review Focus 1
        for no in (33, 34):
            for rd in L[lid_of(no)]["part2"]:
                texts = {o["text"] for o in rd["options"]}
                self.assertFalse({"ch", "tr"} <= texts, (no, rd))



def bases(table, onset):
    row = next(i["row"] for i in table["items"] if i["role"] == "onset" and i["text"] == onset)
    return [i["text"] for i in table["items"] if i["role"] == "base" and i["row"] == row]


def blocked(table, onset):
    row = next(i["row"] for i in table["items"] if i["role"] == "onset" and i["text"] == onset)
    cols = {i["col"]: i["text"] for i in table["items"] if i["role"] == "vowel"}
    return [cols[i["col"]] for i in table["items"] if i["role"] == "blocked" and i["row"] == row]


class Lessons37To41Test(BookTestCase):
    def test_basics(self):
        for no in range(37, 42):
            with self.subTest(no=no):
                self.assert_lesson_basics(no)

    def test_b37_qu_row(self):
        self.assertEqual([i["text"] for i in steps(37, "letter_grid")[0]["items"]], ["ch", "tr", "qu", "p", "ph"])
        table = steps(37, "combine_table")[0]
        self.assertEqual(len({i["row"] for i in table["items"] if i["role"] == "onset"}), 5)
        self.assertEqual(bases(table, "qu"), ["qua", "quơ", "que", "quê", "qui", "quy"])

    def test_b38_vowels_and_labelled_reading(self):
        self.assertEqual([i["text"] for i in steps(38, "letter_grid")[0]["items"]],
                         ["a", "o", "ô", "ơ", "e", "ê", "i", "y", "u", "ư"])
        self.assertEqual(types(38)[1], "reading")
        readings = steps(38, "reading")
        labels = [lb for st in readings for lb in st["labels"]]
        self.assertEqual(len(labels), 12)
        self.assertEqual((labels[0], labels[-1]), ("a – a", "u – i"))
        first = readings[0]
        self.assertEqual([i["text"] for i in first["items"] if i["row"] == 0], ["ra rả", "khà khà"])
        self.assertEqual([i["text"] for i in readings[-1]["items"] if i["row"] == len(readings[-1]["labels"]) - 1],
                         ["xù xì", "rủ rỉ rù rì"])

    def test_b39_table_and_tone_tables(self):
        self.assertEqual(len(steps(39, "letter_grid")[0]["items"]), 17)
        self.assertEqual(types(39)[1], "combine_table")
        table = steps(39, "combine_table")[0]
        self.assertEqual(blocked(table, "c"), ["e", "ê", "i"])
        self.assertEqual(blocked(table, "k"), ["a", "o", "ô", "ơ", "u", "ư"])
        self.assertEqual(bases(table, "k"), ["ke", "kê", "ki"])
        self.assertEqual([s["text"] for s in steps(39, "tone_table")], ["ba", "ca", "ke"])

    def test_b40_table_tone_tables_rule(self):
        self.assertEqual(len(steps(40, "letter_grid")[0]["items"]), 11)
        table = steps(40, "combine_table")[0]
        self.assertEqual(blocked(table, "gh"), ["a", "o", "ô", "ơ", "u", "ư"])
        self.assertEqual(blocked(table, "ng"), ["e", "ê", "i"])
        self.assertEqual([s["text"] for s in steps(40, "tone_table")], ["cha", "ghe"])
        self.assertEqual([i["text"] for i in steps(40, "rule")[0]["items"]],
                         ["k chỉ ghép với e, ê, i", "gh chỉ ghép với e, ê, i", "ngh chỉ ghép với e, ê, i"])

    def test_b41_pairs_and_rounds(self):
        self.assertEqual(types(41)[0], "letter_pairs")
        pairs = steps(41, "letter_pairs")[0]["items"]
        self.assertEqual("".join(i["text"] for i in pairs), "aăâbcdđeêghiklmnoôơpqrstuưvxy")
        kinds = {r["kind"] for r in L[lid_of(41)]["part2"]}
        self.assertIn("match_case", kinds)
        listen = [r for r in L[lid_of(41)]["part2"] if r["kind"] == "listen_choose"]
        self.assertTrue(listen and all(o["text"].isupper() for r in listen for o in r["options"]))



def index_ids():
    import json
    from tapdoc.paths import UNITY_RES
    return [e["lesson_id"] for e in json.loads((UNITY_RES / "lessons" / "index.json").read_text("utf-8"))["lessons"]]


def run_types(no):
    """Loại bước liền nhau gộp lại: ["sentence", "sentence"] -> ("sentence", 2)."""
    out = []
    for t in types(no):
        if out and out[-1][0] == t:
            out[-1] = (t, out[-1][1] + 1)
        else:
            out.append((t, 1))
    return out


class Lessons42To47Test(BookTestCase):
    def test_basics(self):
        for no in range(42, 48):
            with self.subTest(no=no):
                self.assert_lesson_basics(no)

    def test_b42_in_app(self):
        self.assertIn("tv1_t1_b42", index_ids())
        self.assertTrue(L[lid_of(42)]["in_app"])

    def test_b43_b44_letter_then_rime(self):
        self.assertEqual([s["text"] for s in steps(43, "unit")], ["ă", "ăn"])
        self.assertEqual([s["text"] for s in steps(44, "keyword")], ["cân bàn"])

    def test_b45_three_rimes_three_sentences(self):
        self.assertEqual([s["text"] for s in steps(45, "keyword")], ["quả bồ hòn", "con chồn", "cá thờn bơn"])
        self.assertIn(("sentence", 3), run_types(45))
        self.assertEqual([s["text"] for s in steps(45, "sentence")],
                         ["Mẹ bế bé đi nhà trẻ.", "Cô ân cần đón bé.", "Cô hôn bé."])
        hon = steps(45, "sentence")[2]["items"][1]
        self.assertEqual(hon["hl"], [{"s": 1, "n": 2}])  # "hôn": tô vần ôn như sách

    def test_b46_keywords(self):
        self.assertEqual([s["text"] for s in steps(46, "keyword")], ["dế mèn", "con nhện"])

    def test_b47_poem_four_lines(self):
        self.assertIn(("sentence", 4), run_types(47))
        self.assertEqual(steps(47, "sentence")[0]["items"][0]["text"], "Ủn")



def table_rows(no):
    st = steps(no, "rime_table")[0]
    rimes = [i["text"] for i in st["items"] if i["role"] == "rime"]
    words = [i["text"] for i in st["items"] if i["role"] == "word"]
    return list(zip(rimes, words))


class Lessons48To54Test(BookTestCase):
    def test_basics(self):
        for no in range(48, 55):
            with self.subTest(no=no):
                self.assert_lesson_basics(no)

    def test_b48_rime_table(self):
        self.assertEqual(table_rows(48), [("an", "nhà sàn"), ("ăn", "củ sắn"), ("ân", "quả cân"), ("on", "cỏ non"),
                                          ("ôn", "con chồn"), ("ơn", "đàn lợn"), ("en", "mũ len"), ("ên", "ngọn nến"),
                                          ("in", "bản tin"), ("un", "con giun")])
        self.assertEqual([s["text"] for s in steps(48, "sentence")], ["Lan cho ngan ăn giun, bà khen Lan."])

    def test_b50_name_keyword(self):
        self.assertEqual([s["text"] for s in steps(50, "keyword")], ["con tằm", "cô Tấm"])

    def test_b51_three_rimes(self):
        self.assertEqual([s["text"] for s in steps(51, "keyword")], ["com pa", "quả chôm chôm", "bó rơm"])

    def test_b53_poem_three_lines(self):
        self.assertIn(("sentence", 3), run_types(53))

    def test_b54_rime_table(self):
        self.assertEqual(len(table_rows(54)), 10)
        self.assertEqual(table_rows(54)[-1], ("um", "um tùm"))



class Lessons55To64Test(BookTestCase):
    def test_basics(self):
        for no in range(55, 65):
            with self.subTest(no=no):
                self.assert_lesson_basics(no)

    def test_i_y_rimes_flagged(self):
        for no, word in ((55, "i ngắn"), (56, "i dài"), (57, "i ngắn"), (58, "i ngắn")):
            with self.subTest(no=no):
                self.assertTrue(any(word in n for n in notes(no)), notes(no))

    def test_b56_poem_four_lines(self):
        self.assertIn(("sentence", 4), run_types(56))
        self.assertEqual(steps(56, "sentence")[3]["text"], "Hay hay hay hay!")

    def test_b57_ha_noi(self):
        words = [i["text"] for s in steps(57, "words") for i in s["items"]]
        self.assertIn("Hà Nội", words)

    def test_b59_b64_rime_tables(self):
        self.assertEqual(len(table_rows(59)), 8)
        self.assertEqual(table_rows(59)[0], ("ai", "xóm chài"))
        self.assertEqual(table_rows(64), [("ao", "con cáo"), ("eo", "cái kéo"), ("au", "quả cau"), ("âu", "cần cẩu"),
                                          ("êu", "gối thêu"), ("iu", "cái rìu"), ("ưu", "cây lựu")])

    def test_b60_note_on_heo(self):
        heo = [i for s in steps(60, "words") for i in s["items"] if i["text"] == "heo nái"]
        self.assertEqual(heo[0]["note"], "heo nái: lợn nái.")


def keywords(no):
    return [s["text"] for s in steps(no, "keyword")]


def lines(no):
    return [s["text"] for s in steps(no, "sentence")]


class Lessons65To73Test(BookTestCase):
    """Đối chiếu ảnh scan 046–054 (tr.90–107)."""

    def test_basics(self):
        for no in range(65, 74):
            with self.subTest(no=no):
                self.assert_lesson_basics(no)

    def test_keywords(self):
        expected = {65: ["củ lạc", "con tắc kè", "quả gấc"], 66: ["con sóc", "vỏ ốc"], 67: ["máy xúc", "lọ mực"],
                    69: ["bãi cát", "chim cắt", "đôi tất"], 70: ["cái sọt", "củ cà rốt", "cái vợt"],
                    71: ["con vẹt", "bồ kết", "con vịt"], 72: ["bút bi", "mứt tết"]}
        for no, words in expected.items():
            with self.subTest(no=no):
                self.assertEqual(keywords(no), words)

    def test_b65_poem(self):
        self.assertEqual(lines(65), ["Mặc gió núi đèo cao", "Quân đi như thác chảy."])

    def test_b66_dialogue_keeps_dash_on_screen(self):
        # Sách ghi lời thoại có gạch đầu dòng; chữ trên màn giữ gạch, phần đọc thì bỏ.
        self.assertEqual(lines(66), ["Cốc, cốc, cốc!", "– Ai gọi đó?", "– Tôi là thỏ.", "– Nếu là thỏ", "Cho xem tai."])
        self.assertEqual([i["text"] for i in steps(66, "sentence")[1]["items"]], ["Ai", "gọi", "đó"])

    def test_b67_one_sentence(self):
        self.assertEqual(lines(67), ["Thu về cúc nở, sực nức mùi thơm."])

    def test_b68_rime_table_and_teacher_note(self):
        self.assertEqual(table_rows(68), [("ac", "con vạc"), ("ăc", "chè đặc"), ("âc", "xôi gấc"), ("oc", "con cóc"),
                                          ("ôc", "vỏ ốc"), ("uc", "cá nục"), ("ưc", "thơm phức")])
        self.assertEqual(lines(68), ["Nhớ lời Bác dạy:", "Chăm học, chăm làm", "Bố mẹ đều khen", "Thầy cô vui vẻ."])
        self.assertTrue(any("ec" in n for n in notes(68)), notes(68))

    def test_b71_tet_poem(self):
        self.assertEqual(lines(71), ["Trời ren rét", "Tết đến rồi", "Đào, mai nở", "Thật là vui..."])

    def test_b73_rime_table_eleven_rows(self):
        rows = table_rows(73)
        self.assertEqual(len(rows), 11)
        self.assertEqual((rows[0], rows[-1]), (("at", "bài hát"), ("ưt", "gói mứt")))
        self.assertIn(("sentence", 5), run_types(73))


class Lessons74To80Test(BookTestCase):
    """Đối chiếu ảnh scan 055–060 (tr.108–119)."""

    def test_basics(self):
        for no in range(74, 81):
            with self.subTest(no=no):
                self.assert_lesson_basics(no)

    def test_keywords(self):
        expected = {74: ["xe đạp", "cải bắp", "cá mập"], 75: ["con cọp", "tốp ca", "sấm chớp"],
                    76: ["cá chép", "đèn xếp"], 77: ["nhịp cầu", "búp sen"]}
        for no, words in expected.items():
            with self.subTest(no=no):
                self.assertEqual(keywords(no), words)

    def test_poems(self):
        self.assertEqual(lines(74)[0], "“Rầm rập rầm rầm rập!”")
        self.assertIn(("sentence", 4), run_types(74))
        self.assertIn(("sentence", 6), run_types(75))
        self.assertEqual(lines(76)[1], "“Đôi dép Bác Hồ”,")
        self.assertEqual(lines(77), ["Búp sen nhỏ", "Bên bờ ao", "Như tay bé", "Vẫy trời cao."])

    def test_b76_real_person_picture_replaced(self):
        self.assertTrue(any("Bác Hồ" in n for n in notes(76)), notes(76))

    def test_b78_rime_table_and_passage(self):
        rows = table_rows(78)
        self.assertEqual(len(rows), 10)
        self.assertEqual((rows[0], rows[-1]), (("ap", "xe đạp"), ("up", "chè búp")))
        self.assertEqual(len(lines(78)), 3)
        self.assertEqual(lines(78)[1], "Mấy bác đi xe đạp la: “Ếp ếp!”.")

    def test_b79_rime_grid_like_page(self):
        grid = steps(79, "rime_grid")[0]
        items = grid["items"]
        self.assertEqual([i["text"] for i in items if i["role"] == "final"], ["n", "m", "c", "t", "p", "i-y", "o-u"])
        self.assertEqual([i["text"] for i in items if i["role"] == "vowel"],
                         ["a", "ă", "â", "o", "ô", "ơ", "e", "ê", "i", "u", "ư"])
        cells = {(i["row"], i["col"]): i for i in items if i["role"] == "cell"}
        self.assertEqual(len(cells), 61)
        self.assertEqual(cells[(0, 5)]["text"], "ai - ay")
        self.assertEqual([aud(sp) for sp in cells[(0, 5)]["spells"]],
                         [["van_a", "van_i", "van_ai"], ["van_a", "van_y", "van_ay"]])
        self.assertEqual([c for (r, c) in cells if r == 10], [2, 3, 5, 6])  # ư: ưc ưt ưi ưu, ô trống như trang
        self.assertNotIn((5, 2), cells)  # không có "ơc"

    def test_b80_find_words_and_riddle(self):
        readings = steps(80, "reading")
        labels = [lb for st in readings for lb in st["labels"]]
        self.assertEqual(labels, ["(1)", "(2)", "(3)", "(4)", "(5)", "(6)", "(7)"])
        sixth = readings[1]["items"]
        self.assertEqual([i["text"] for i in sixth if i["row"] == 1], ["vải", "bay", "mây", "voi", "nôi"])
        self.assertEqual(lines(80), ["Con gì ăn no", "Má to mắt híp,", "Mồm kêu ụt ịt,", "Nằm thở phì phò?"])
        riddle = L[lid_of(80)]["part2"][0]
        self.assertEqual(riddle["kind"], "listen_picture")
        self.assertEqual(riddle["instruction_audio"], "hd_nghe_do_chon_tranh")
        self.assertTrue(riddle["prompt_audio"].startswith("cau_b80_"))
        self.assertEqual(riddle["options"][riddle["answer"]]["image"], "img_b80_con_lownj")



def notes_by_kind(no, kind):
    return [n["text"] for n in L[lid_of(no)]["notes"] if n["kind"] == kind]


class LessonNotesContentTest(unittest.TestCase):
    """Ghi chú cho phụ huynh: chú thích sách, tên đọc riêng (tr.122), chỗ app khác sách."""

    def test_book_footnotes(self):
        # Rà đủ 80 trang bài (30/10/2026): chỉ 6 bài có chú thích hay lời dặn cho người lớn. Lời dặn làm bài
        # của bài 39, 40, 80 ("theo mẫu") là nội dung bài, không phải ghi chú.
        with_notes = {no for no in range(1, 81) if notes_by_kind(no, "sach")}
        self.assertEqual(with_notes, {11, 27, 42, 60, 66, 68})
        self.assertIn("Bài ôn: Học sinh giỏi có thể ghép thêm dấu thanh. Các bài ôn sau cũng vậy.",
                      notes_by_kind(11, "sach"))
        self.assertIn("Ghép thêm dấu thanh để tạo tiếng mới ở nhà.", notes_by_kind(27, "sach"))
        self.assertTrue(any("vịt xiêm" in t for t in notes_by_kind(42, "sach")))
        self.assertIn("heo nái: lợn nái.", notes_by_kind(60, "sach"))
        self.assertIn("cá lóc: cá quả.", notes_by_kind(66, "sach"))
        self.assertTrue(any("Vần ec rất ít gặp" in t for t in notes_by_kind(68, "sach")))

    def test_reading_names_only_in_lessons_teaching_those_letters(self):
        with_names = {no for no in range(1, 81) if notes_by_kind(no, "ten_doc")}
        self.assertEqual(with_names, {2, 5, 10, 14, 20, 25, 26, 28, 29, 35})
        self.assertEqual(len(notes_by_kind(25, "ten_doc")), 2)  # g và gh
        self.assertTrue(any('"k" đọc là "ca"' in t for t in notes_by_kind(20, "ten_doc")))
        self.assertTrue(any('"qu" đọc là "quờ"' in t for t in notes_by_kind(35, "ten_doc")))

    def test_app_differences_noted(self):
        with_diff = {no for no in range(1, 81) if notes_by_kind(no, "khac_sach")}
        self.assertEqual(with_diff, {1, 3, 6, 18, 27, 38, 42, 43, 44, 49, 53, 66, 68, 76, 80})
        self.assertTrue(any("4 bước" in t for t in notes_by_kind(38, "khac_sach")))
        self.assertTrue(any("đôi dép" in t for t in notes_by_kind(76, "khac_sach")))

    def test_b80_onsets_coloured_like_page(self):
        first = steps(80, "reading")[0]["items"]
        self.assertEqual([(i["text"], i["hl"]) for i in first[:2]], [("sàn", [{"s": 0, "n": 1}]), ("sắn", [{"s": 0, "n": 1}])])
        oc = next(i for st in steps(80, "reading") for i in st["items"] if i["text"] == "ốc")
        self.assertEqual(oc["hl"], [])


if __name__ == "__main__":
    unittest.main()
