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
    "book": "tv1_t1_1990",
    "source": {"pages": [18], "scan_file": "010"},
    "part1": [
        {"type": "unit", "text": "k", "audio": "am_k",
         "readings": [{"kinds": ["hoc"], "text": "ca", "audio": "am_k"},
                      {"kinds": ["chuan"], "text": "cờ", "audio": "ghiam_k"}]},
        {"type": "picture", "image": "img_b13_ke", "text": "kẻ", "audio": "tu_ke"},
        {"type": "picture", "image": "img_b13_ki", "text": "kì", "audio": "tu_ki"},
    ],
    "part2": [
        {"kind": "listen_picture", "prompt_audio": "hd_chon", "items": [
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
        self.assertEqual([(i["manifest"], i["id"]) for i in items], [
            ("audio", "am_k"),
            ("audio", "ghiam_k"),
            ("images", "img_b13_ke"),
            ("videos", "img_b13_ke"),
            ("audio", "tu_ke"),
            ("images", "img_b13_ki"),
            ("audio", "tu_ki"),
            ("audio", "hd_chon"),
            ("audio", "khen_gioi"),
            # Có trong danh mục, ghi dùng ở bài này nhưng không thấy trong file bài: xếp cuối.
            ("audio", "tieng_ke"),
            ("images", "img_b13_le"),
        ])

    def test_items_carry_the_step_they_first_appear_in(self):
        items = lesson_media(LESSON, "tv1_t1_b13", _audio_rows(), _image_rows(), [{"id": "img_b13_ke"}])
        group = {(i["manifest"], i["id"]): (i["part"], i["step"], i["label"]) for i in items}
        self.assertEqual(group[("audio", "am_k")], ("part1", 1, "Âm, vần mới: k"))
        self.assertEqual(group[("audio", "ghiam_k")], ("part1", 1, "Âm, vần mới: k"))
        self.assertEqual(group[("images", "img_b13_ke")], ("part1", 2, "Tranh: kẻ"))
        self.assertEqual(group[("videos", "img_b13_ke")], ("part1", 2, "Tranh: kẻ"))
        self.assertEqual(group[("audio", "tu_ki")], ("part1", 3, "Tranh: kì"))
        # tu_ke đã có ở bước 2 nên không lặp lại ở câu luyện tập.
        self.assertEqual(group[("audio", "hd_chon")], ("part2", 1, "Nghe chọn tranh"))
        self.assertEqual(group[("audio", "khen_gioi")], ("part2", 1, "Nghe chọn tranh"))
        self.assertEqual(group[("audio", "tieng_ke")], ("khac", 0, "Danh mục ghi dùng ở bài này nhưng file bài không dùng"))

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
        no_source = {k: v for k, v in LESSON.items() if k != "source"}
        (res / "lessons" / "tv1_t1_b14.json").write_text(json.dumps(no_source), encoding="utf-8")
        (res / "lessons" / "tv1_t1_b15.json").write_text(
            json.dumps({**LESSON, "source": {"pages": [20], "scan_file": "011"}}), encoding="utf-8")
        book_dir = root / "scans" / "Tiếng Việt 1 (tập 1 1990)"
        book_dir.mkdir(parents=True)
        self.scan_bytes = bytes([0xFF, 0xD8, 0xFF]) + b"-fake-jpeg"
        (book_dir / "010_Tiếng_Việt_1_(tập_1_1990)_-_Trang_10.jpg").write_bytes(self.scan_bytes)
        (book_dir / "100_Tiếng_Việt_1_(tập_1_1990)_-_Trang_100.jpg").write_bytes(b"other")
        self.server = make_server(0, manifests, res, scans_dir=root / "scans")
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
        self.assertIn("/media/scan/", html)
        self.assertIn("Trang sách gốc", html)

    def test_serves_book_scan_of_lesson(self):
        with urllib.request.urlopen(self.base + "/media/scan/tv1_t1_b13.jpg", timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.headers["Content-Type"], "image/jpeg")
            self.assertEqual(resp.read(), self.scan_bytes)

    def test_scan_missing_or_invalid_is_404(self):
        # b14 không ghi trang sách, b15 ghi ảnh 011 mà máy chưa có, còn lại là tên không hợp lệ.
        for name in ("tv1_t1_b14.jpg", "tv1_t1_b15.jpg", "tv1_t1_b99.jpg", "index.jpg", "..%2Fsecret.jpg", "tv1_t1_b13.png"):
            with self.subTest(name=name):
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    urllib.request.urlopen(self.base + "/media/scan/" + name, timeout=5)
                caught.exception.close()
                self.assertEqual(caught.exception.code, 404)

    def test_rejects_bad_or_missing_lesson(self):
        for path in ("/api/lesson-media/..%2Fsecret", "/api/lesson-media/index", "/api/lesson-media/tv1_t1_b99"):
            with self.subTest(path=path):
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    self._get(path)
                caught.exception.close()
                self.assertEqual(caught.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
