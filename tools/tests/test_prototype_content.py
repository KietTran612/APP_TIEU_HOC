import json
import unittest

from tapdoc.build import build_lesson, load_sources
from tapdoc.curriculum import learned_until, load_curriculum
from tapdoc.manifest import load_rows
from tapdoc.paths import CONTENT_SRC, LESSON_INDEX, MANIFESTS, STYLE_FILE, UNITY_RES
from tapdoc.validate import check_nfc, check_part1, check_part2, validate_all
from tapdoc.viet import is_nfc


L = {r.lesson["lesson_id"]: r.lesson for r in (build_lesson(s) for s in load_sources(CONTENT_SRC))}


def aud(spell):
    return [p["audio"] for p in spell["parts"]]


class PrototypeContentTest(unittest.TestCase):
    def test_b13(self):
        p1 = L["tv1_t1_b13"]["part1"]
        self.assertEqual(
            [s["type"] for s in p1],
            ["unit", "keyword", "analyze", "spell", "unit", "keyword", "analyze", "spell", "words", "sentence", "reading"],
        )
        self.assertEqual(aud(p1[7]["spell"]), ["am_c", "van_uw", "tieng_cuw", "dau_hoi", "tieng_cuwr"])
        self.assertTrue(p1[7]["spell"]["drag_tone"])
        self.assertEqual(p1[9]["text"], "má có củ từ")
        self.assertEqual([i["text"] for i in p1[10]["items"]], ["cù", "cừ", "dù", "tư", "nụ", "mụ", "từ từ", "tù mù"])

    def test_b42(self):
        p1 = L["tv1_t1_b42"]["part1"]
        self.assertEqual(aud(p1[3]["spell"]), ["van_a", "am_n", "van_an"])
        self.assertEqual(aud(p1[4]["spell"]), ["am_s", "van_an", "tieng_san", "dau_huyen", "tieng_sanf"])
        self.assertEqual(p1[4]["then_text"], "nhà sàn")
        self.assertEqual(p1[5]["items"][1]["note"], "ngan: ở phía Nam gọi là vịt xiêm.")
        self.assertEqual([s["target"] for s in p1[5]["items"][2]["spells"]], ["bàn"])

    def test_b04(self):
        p1 = L["tv1_t1_b04"]["part1"]
        self.assertEqual(
            [s["type"] for s in p1],
            ["keyword", "spell", "tone_intro", "tone_attach", "tone_intro", "tone_attach", "picture", "words"],
        )
        self.assertEqual([p["text"] for p in p1[3]["spell"]["parts"]], ["ca", "ˋ", "cà"])
        self.assertEqual((p1[6]["image"], p1[6]["audio"]), ("img_b04_mua", "hd_b04_tranh_01"))
        self.assertTrue(any(n["where"] == "part1[6]" for n in L["tv1_t1_b04"]["review"]["can_duyet"]))

    def test_round_counts(self):
        for lid, l in L.items():
            self.assertTrue(6 <= len(l["part2"]) <= 10, lid)

    def test_sources_pass_nfc_part1_and_part2_checks(self):
        cur = load_curriculum(LESSON_INDEX)
        self.assertLessEqual({"tv1_t1_b04", "tv1_t1_b13", "tv1_t1_b42"}, set(L.keys()))  # bản đầu tiên thêm bài 1–17
        for lid, lesson in L.items():
            with self.subTest(lesson=lid):
                self.assertEqual(check_nfc(lesson), [])
                self.assertEqual(check_part1(lesson), [])
                learned = learned_until(cur, lesson["lesson_no"])
                self.assertEqual(check_part2(lesson, learned), [])

    def test_style_file_exists_and_is_nfc(self):
        self.assertTrue(STYLE_FILE.is_file())
        text = STYLE_FILE.read_text(encoding="utf-8").strip()
        self.assertTrue(is_nfc(text))
        self.assertIn("Tranh minh họa sách giáo khoa Việt Nam năm 1990", text)
        self.assertIn("tỉ lệ vuông 1:1", text)

    def test_built_outputs_and_manifests_are_valid(self):
        index_path = UNITY_RES / "lessons" / "index.json"
        self.assertTrue(index_path.is_file())
        index_data = json.loads(index_path.read_text(encoding="utf-8"))
        index_ids = [item["lesson_id"] for item in index_data["lessons"]]
        self.assertLessEqual({"tv1_t1_b04", "tv1_t1_b13"}, set(index_ids))
        self.assertIn("tv1_t1_b42", index_ids)  # từ đợt 2 bài 42 vào danh sách
        self.assertTrue((UNITY_RES / "lessons" / "tv1_t1_b42.json").is_file())
        audio_rows = load_rows(MANIFESTS / "audio_manifest.json")
        image_rows = load_rows(MANIFESTS / "image_manifest.json")
        self.assertGreater(len(audio_rows), 0)
        self.assertGreater(len(image_rows), 0)
        self.assertEqual(validate_all(allow_missing=True), [])


if __name__ == "__main__":
    unittest.main()
