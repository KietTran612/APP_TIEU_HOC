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


if __name__ == "__main__":
    unittest.main()
