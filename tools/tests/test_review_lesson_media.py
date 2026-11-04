"""Trang duyệt theo bài: âm thanh, tranh, tranh động của một bài theo đúng thứ tự bé gặp trong bài."""

import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

from tapdoc.manifest import save_rows
from tapdoc.review_server import lesson_media, make_server

LESSON = {
    "lesson_id": "tv1_t1_b13",
    "part1": [
        {"type": "unit", "text": "k", "audio": "am_k",
         "readings": [{"kinds": ["hoc"], "text": "ca", "audio": "am_k"},
                      {"kinds": ["chuan"], "text": "cờ", "audio": "ghiam_k"}]},
        {"type": "picture", "image": "img_b13_ke", "text": "kẻ", "audio": "tu_ke"},
        {"type": "picture", "image": "img_b13_ki", "text": "kì", "audio": "tu_ki"},
    ],
    "part2": [
        {"type": "pick", "prompt_audio": "hd_chon", "items": [
            {"image": "img_b13_ke", "audio": "tu_ke"},
            {"image": "img_khong_co", "audio": "tu_khong_co"},
        ], "then_audio": "khen_gioi"},
    ],
}

AUDIO = ["am_k", "ghiam_k", "tu_ke", "tu_ki", "hd_chon", "khen_gioi", "tieng_ke", "tu_khac"]
IMAGES = ["img_b13_ke", "img_b13_ki", "img_b13_le"]


def _audio_rows():
    bai = {"tieng_ke": ["tv1_t1_b13"], "tu_khac": ["tv1_t1_b14"]}
    return [{"id": i, "bai": bai.get(i, ["tv1_t1_b13"])} for i in AUDIO]


def _image_rows():
    return [{"id": i, "bai": ["tv1_t1_b13"]} for i in IMAGES]


class LessonMediaOrderTest(unittest.TestCase):
    def test_items_follow_lesson_order_with_clip_after_its_picture(self):
        items = lesson_media(LESSON, "tv1_t1_b13", _audio_rows(), _image_rows(), [{"id": "img_b13_ke"}])
        self.assertEqual(items, [
            {"manifest": "audio", "id": "am_k"},
            {"manifest": "audio", "id": "ghiam_k"},
            {"manifest": "images", "id": "img_b13_ke"},
            {"manifest": "videos", "id": "img_b13_ke"},
            {"manifest": "audio", "id": "tu_ke"},
            {"manifest": "images", "id": "img_b13_ki"},
            {"manifest": "audio", "id": "tu_ki"},
            {"manifest": "audio", "id": "hd_chon"},
            {"manifest": "audio", "id": "khen_gioi"},
            # Có trong danh mục, ghi dùng ở bài này nhưng không thấy trong file bài: xếp cuối.
            {"manifest": "audio", "id": "tieng_ke"},
            {"manifest": "images", "id": "img_b13_le"},
        ])

    def test_each_item_listed_once_and_unknown_ids_skipped(self):
        items = lesson_media(LESSON, "tv1_t1_b13", _audio_rows(), _image_rows(), [])
        keys = [(i["manifest"], i["id"]) for i in items]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertNotIn(("images", "img_khong_co"), keys)
        self.assertNotIn(("audio", "tu_khong_co"), keys)
        self.assertNotIn(("audio", "tu_khac"), keys)  # thuộc bài khác
        self.assertNotIn("videos", {i["manifest"] for i in items})


class LessonMediaEndpointTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        manifests = root / "manifests"
        res = root / "res"
        (res / "lessons").mkdir(parents=True)
        (res / "lessons" / "tv1_t1_b13.json").write_text(json.dumps(LESSON, ensure_ascii=False), encoding="utf-8")
        save_rows(manifests / "audio_manifest.json", _audio_rows())
        save_rows(manifests / "image_manifest.json", _image_rows())
        save_rows(manifests / "video_manifest.json", [{"id": "img_b13_ki"}])
        self.server = make_server(0, manifests, res)
        thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        thread.start()

        def stop():
            self.server.shutdown()
            self.server.server_close()
            thread.join(timeout=2)
        self.addCleanup(stop)
        host, port = self.server.server_address
        self.base = f"http://{host}:{port}"

    def _get(self, path):
        with urllib.request.urlopen(self.base + path, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))

    def test_returns_lesson_items(self):
        status, data = self._get("/api/lesson-media/tv1_t1_b13")
        self.assertEqual(status, 200)
        keys = [(i["manifest"], i["id"]) for i in data]
        self.assertEqual(keys[:2], [("audio", "am_k"), ("audio", "ghiam_k")])
        self.assertLess(keys.index(("images", "img_b13_ki")), keys.index(("videos", "img_b13_ki")))

    def test_page_has_by_lesson_tab_using_endpoint(self):
        with urllib.request.urlopen(self.base + "/", timeout=5) as resp:
            html = resp.read().decode("utf-8")
        self.assertIn("Duyệt theo bài", html)
        self.assertIn("/api/lesson-media/", html)
        self.assertIn('let currentTab = "bylesson"', html)

    def test_rejects_bad_or_missing_lesson(self):
        for path in ("/api/lesson-media/..%2Fsecret", "/api/lesson-media/index", "/api/lesson-media/tv1_t1_b99"):
            with self.subTest(path=path):
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    self._get(path)
                caught.exception.close()
                self.assertEqual(caught.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
