import io
import tempfile
import unicodedata
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from tapdoc import __main__ as cli
from tapdoc.chatgpt_requests import AUDIO_HEADER, audio_requests, image_requests, write_request_files
from tapdoc.manifest import save_rows

# Nội dung cố định theo bản yêu cầu (Task 6, Step 3).
HEADER = (
    "Hãy tạo file âm thanh tiếng Việt, giọng nữ miền Nam, đọc chậm và rõ, mỗi dòng một file.\n"
    "- Tên file: đúng cột id, đuôi .mp3 (ví dụ am_dd.mp3).\n"
    "- Chỉ đọc đúng chữ ở cột text, không thêm lời nào khác.\n"
    "- Dòng có doc_ky = x: đọc rõ theo chính tả, phân biệt dấu hỏi và dấu ngã.\n"
    "- Gom tất cả vào một file ZIP để tải về.\n"
    "\n"
    "id,text,doc_ky\n"
)


def arow(i, text="đờ", status="chua_co", ky=False):
    return {"id": i, "text": text, "status": status, "can_nghe_ky": ky}


def irow(i, mo_ta="Một con cá", bai=("tv1_t1_b04",), status="chua_co"):
    return {"id": i, "mo_ta": mo_ta, "bai": list(bai), "status": status}


class AudioRequestTest(unittest.TestCase):
    def test_audio_request(self):
        text = audio_requests([{"id": "tieng_cuwr", "text": "cử", "status": "chua_co", "can_nghe_ky": True},
                               {"id": "am_dd", "text": "đờ", "status": "dat", "can_nghe_ky": False}])[0]
        self.assertIn("giọng nữ miền Nam", text)
        self.assertIn("đọc rõ theo chính tả, phân biệt dấu hỏi và dấu ngã", text)
        self.assertIn("id,text,doc_ky", text)
        self.assertIn("tieng_cuwr,cử,x", text)
        self.assertNotIn("am_dd,", text)  # (phần mở đầu có "ví dụ am_dd.mp3" nên chỉ xét dòng dữ liệu)

    def test_exact_header_then_one_line_per_row(self):
        (prompt,) = audio_requests([arow("am_dd", "đờ"), arow("tieng_cuwr", "cử", ky=True)])
        self.assertEqual(prompt, HEADER + "am_dd,đờ,\ntieng_cuwr,cử,x\n")
        self.assertEqual(AUDIO_HEADER, HEADER)

    def test_header_is_nfc(self):
        self.assertTrue(unicodedata.is_normalized("NFC", AUDIO_HEADER))

    def test_missing_can_nghe_ky_is_blank(self):
        (prompt,) = audio_requests([{"id": "am_dd", "text": "đờ", "status": "chua_co"}])
        self.assertTrue(prompt.endswith("am_dd,đờ,\n"))

    def test_comma_in_text_is_quoted(self):
        (prompt,) = audio_requests([arow("cau_b13_01", "má có cá, bé có cá", ky=True), arow("am_dd", "đờ")])
        self.assertIn('cau_b13_01,"má có cá, bé có cá",x\n', prompt)
        self.assertIn("am_dd,đờ,\n", prompt)  # không dấu phẩy thì không bọc

    def test_quote_inside_quoted_text_is_doubled(self):
        (prompt,) = audio_requests([arow("c", 'Bé nói "a", rồi đi')])
        self.assertIn('c,"Bé nói ""a"", rồi đi",\n', prompt)

    def test_newlines_are_stripped(self):
        (prompt,) = audio_requests([arow("tu_cais_ddu", "cái\nđu"), arow("tu_x", "a\r\nb\r"), arow("am_dd", "đờ")])
        self.assertIn("tu_cais_ddu,cái đu,\n", prompt)
        self.assertIn("tu_x,a b,\n", prompt)
        body = prompt[len(HEADER):]
        self.assertEqual(len(body.splitlines()), 3)

    def test_only_chua_co_by_default(self):
        rows = [arow("a_1", status="chua_co"), arow("a_2", status="dat"), arow("a_3", status="cho_duyet"),
                arow("a_4", status="khong_dat")]
        (prompt,) = audio_requests(rows)
        body = prompt[len(HEADER):]
        self.assertEqual(body, "a_1,đờ,\n")

    def test_include_khong_dat(self):
        rows = [arow("a_1", status="chua_co"), arow("a_2", status="dat"), arow("a_3", status="khong_dat")]
        (prompt,) = audio_requests(rows, include_khong_dat=True)
        self.assertEqual(prompt[len(HEADER):], "a_1,đờ,\na_3,đờ,\n")

    def test_nothing_to_request(self):
        self.assertEqual(audio_requests([]), [])
        self.assertEqual(audio_requests([arow("a_1", status="dat")]), [])

    def test_batches_of_60_keep_order_and_repeat_header(self):
        rows = [arow(f"a_{i:03d}", f"t{i}") for i in range(130)]
        prompts = audio_requests(rows)
        self.assertEqual(len(prompts), 3)
        sizes = [len(p[len(HEADER):].splitlines()) for p in prompts]
        self.assertEqual(sizes, [60, 60, 10])
        for p in prompts:
            self.assertTrue(p.startswith(HEADER))
        ids = [line.split(",")[0] for p in prompts for line in p[len(HEADER):].splitlines()]
        self.assertEqual(ids, [r["id"] for r in rows])

    def test_exactly_one_batch_when_equal_to_batch_size(self):
        self.assertEqual(len(audio_requests([arow(f"a_{i}") for i in range(60)])), 1)
        self.assertEqual(len(audio_requests([arow(f"a_{i}") for i in range(61)])), 2)

    def test_custom_batch_size(self):
        prompts = audio_requests([arow(f"a_{i}") for i in range(5)], batch_size=2)
        self.assertEqual([len(p[len(HEADER):].splitlines()) for p in prompts], [2, 2, 1])

    def test_batch_size_must_be_positive(self):
        with self.assertRaises(ValueError):
            audio_requests([arow("a_1")], batch_size=0)


class ImageRequestTest(unittest.TestCase):
    def test_image_request(self):
        reqs = image_requests([{"id": "img_b13_cais_ddu", "mo_ta": "Bé gái ngồi đánh đu", "bai": ["tv1_t1_b13"],
                                "status": "chua_co"}], "STYLE")
        ((iid, prompt),) = reqs["tv1_t1_b13"]
        self.assertEqual(iid, "img_b13_cais_ddu")
        self.assertIn("STYLE", prompt)
        self.assertIn("Bé gái ngồi đánh đu", prompt)

    def test_exact_prompt(self):
        reqs = image_requests([irow("img_b04_cas", "Con cá có vảy")], "Phong cách: nét mực đen.")
        self.assertEqual(reqs["tv1_t1_b04"], [(
            "img_b04_cas",
            "Phong cách: nét mực đen.\nVẽ: Con cá có vảy\n(Mã tranh: img_b04_cas. Không viết mã này lên tranh.)")])

    def test_grouped_by_first_lesson_and_system_under_chung(self):
        rows = [irow("img_b04_a", bai=["tv1_t1_b04", "tv1_t1_b05"]), irow("img_b05_b", bai=["tv1_t1_b05"]),
                irow("img_b04_c", bai=["tv1_t1_b04"]), irow("img_chung_sao", "Ngôi sao", bai=["chung"])]
        reqs = image_requests(rows, "S")
        self.assertEqual(list(reqs), ["tv1_t1_b04", "tv1_t1_b05", "chung"])
        self.assertEqual([i for i, _ in reqs["tv1_t1_b04"]], ["img_b04_a", "img_b04_c"])
        self.assertEqual([i for i, _ in reqs["tv1_t1_b05"]], ["img_b05_b"])
        self.assertEqual([i for i, _ in reqs["chung"]], ["img_chung_sao"])

    def test_only_chua_co_by_default(self):
        rows = [irow("i1", status="chua_co"), irow("i2", status="dat"), irow("i3", status="cho_duyet"),
                irow("i4", status="khong_dat")]
        reqs = image_requests(rows, "S")
        self.assertEqual([i for i, _ in reqs["tv1_t1_b04"]], ["i1"])

    def test_include_khong_dat(self):
        rows = [irow("i1", status="chua_co"), irow("i2", status="dat"), irow("i4", status="khong_dat")]
        reqs = image_requests(rows, "S", include_khong_dat=True)
        self.assertEqual([i for i, _ in reqs["tv1_t1_b04"]], ["i1", "i4"])

    def test_no_group_without_requests(self):
        self.assertEqual(image_requests([], "S"), {})
        self.assertEqual(image_requests([irow("i2", status="dat")], "S"), {})


class TempDirCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)


class WriteRequestFilesTest(TempDirCase):
    def test_writes_audio_batches_and_image_files(self):
        out = self.root / "requests"
        audio = [arow(f"a_{i:03d}", f"t{i}") for i in range(61)]
        images = [irow("img_b04_cas", "Con cá có vảy"), irow("img_chung_sao", "Ngôi sao", bai=["chung"])]
        written = write_request_files(audio, images, "STYLE", out)
        names = [p.name for p in written]
        self.assertEqual(names, ["audio_01.txt", "audio_02.txt", "images_chung.md", "images_tv1_t1_b04.md"])
        self.assertTrue(all(p.parent == out for p in written))
        first = (out / "audio_01.txt").read_bytes().decode("utf-8")
        self.assertTrue(first.startswith(HEADER))
        self.assertEqual(len(first[len(HEADER):].splitlines()), 60)
        self.assertEqual((out / "audio_02.txt").read_text(encoding="utf-8"), HEADER + "a_060,t60,\n")
        md = (out / "images_tv1_t1_b04.md").read_text(encoding="utf-8")
        self.assertEqual(md, "## img_b04_cas\n\nSTYLE\nVẽ: Con cá có vảy\n"
                             "(Mã tranh: img_b04_cas. Không viết mã này lên tranh.)\n\n")
        self.assertNotIn(b"\r", (out / "images_tv1_t1_b04.md").read_bytes())

    def test_several_entries_in_an_image_file(self):
        out = self.root / "requests"
        write_request_files([], [irow("i1", "Một"), irow("i2", "Hai")], "S", out)
        md = (out / "images_tv1_t1_b04.md").read_text(encoding="utf-8")
        self.assertEqual(md, "## i1\n\nS\nVẽ: Một\n(Mã tranh: i1. Không viết mã này lên tranh.)\n\n"
                             "## i2\n\nS\nVẽ: Hai\n(Mã tranh: i2. Không viết mã này lên tranh.)\n\n")

    def test_deletes_old_request_files_only(self):
        out = self.root / "requests"
        out.mkdir()
        for name in ("audio_01.txt", "audio_07.txt", "images_tv1_t1_b13.md", "ghi_chu.txt", "audio_zip.md"):
            (out / name).write_text("cu", encoding="utf-8")
        (out / "con").mkdir()
        write_request_files([arow("a_1")], [], "S", out)
        self.assertEqual(sorted(p.name for p in out.iterdir()), ["audio_01.txt", "audio_zip.md", "con", "ghi_chu.txt"])
        self.assertTrue((out / "audio_01.txt").read_text(encoding="utf-8").startswith(HEADER))

    def test_nothing_to_write_still_clears_old_files(self):
        out = self.root / "requests"
        out.mkdir()
        (out / "audio_01.txt").write_text("cu", encoding="utf-8")
        self.assertEqual(write_request_files([arow("a_1", status="dat")], [], "S", out), [])
        self.assertFalse((out / "audio_01.txt").exists())

    def test_include_khong_dat(self):
        out = self.root / "requests"
        written = write_request_files([arow("a_1", status="khong_dat")], [irow("i1", status="khong_dat")], "S", out,
                                      include_khong_dat=True)
        self.assertEqual([p.name for p in written], ["audio_01.txt", "images_tv1_t1_b04.md"])
        self.assertEqual(write_request_files([arow("a_1", status="khong_dat")], [], "S", out), [])


class RequestsCliTest(TempDirCase):
    def setUp(self):
        super().setUp()
        self.manifests = self.root / "manifests"
        self.requests = self.root / "requests"
        self.style = self.root / "style" / "image_style.txt"
        self.style.parent.mkdir()
        self.style.write_text("PHONG CÁCH\n", encoding="utf-8")
        save_rows(self.manifests / "audio_manifest.json", [
            {**arow("am_dd", "đờ"), "kind": "am"},
            {**arow("tieng_cuwr", "cử", ky=True), "kind": "tieng"},
            {**arow("van_u", "u", status="dat"), "kind": "van"},
            {**arow("am_c", "cờ", status="khong_dat"), "kind": "am"},
        ])
        save_rows(self.manifests / "image_manifest.json", [
            irow("img_b13_cais_ddu", "Bé gái ngồi đánh đu", ["tv1_t1_b13"]),
            irow("img_b13_cur_tuwf", "Củ từ", ["tv1_t1_b13"], status="khong_dat"),
            irow("img_chung_sao", "Ngôi sao", ["chung"]),
        ])

    def run_cli(self, argv, style=None):
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(cli, "MANIFESTS", self.manifests), \
                mock.patch.object(cli, "REQUESTS_DIR", self.requests), \
                mock.patch.object(cli, "STYLE_FILE", style or self.style), \
                redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_requests_writes_files_and_lists_them(self):
        code, out, err = self.run_cli(["requests"])
        self.assertEqual(code, 0, err)
        self.assertEqual(sorted(p.name for p in self.requests.iterdir()),
                         ["audio_01.txt", "images_chung.md", "images_tv1_t1_b13.md"])
        audio = (self.requests / "audio_01.txt").read_text(encoding="utf-8")
        self.assertIn("am_dd,đờ,\n", audio)
        self.assertIn("tieng_cuwr,cử,x\n", audio)
        self.assertNotIn("van_u,", audio)
        self.assertNotIn("am_c,", audio)  # khong_dat chỉ vào khi --redo
        md = (self.requests / "images_tv1_t1_b13.md").read_text(encoding="utf-8")
        self.assertIn("## img_b13_cais_ddu\n\nPHONG CÁCH\nVẽ: Bé gái ngồi đánh đu\n", md)
        self.assertNotIn("img_b13_cur_tuwf", md)
        for name in ("audio_01.txt", "images_chung.md", "images_tv1_t1_b13.md"):
            self.assertIn(name, out)

    def test_style_trailing_newline_does_not_add_blank_line(self):
        self.run_cli(["requests"])
        md = (self.requests / "images_chung.md").read_text(encoding="utf-8")
        self.assertEqual(md, "## img_chung_sao\n\nPHONG CÁCH\nVẽ: Ngôi sao\n"
                             "(Mã tranh: img_chung_sao. Không viết mã này lên tranh.)\n\n")

    def test_redo_includes_khong_dat(self):
        code, out, err = self.run_cli(["requests", "--redo"])
        self.assertEqual(code, 0, err)
        audio = (self.requests / "audio_01.txt").read_text(encoding="utf-8")
        self.assertIn("am_c,cờ,\n", audio)
        self.assertNotIn("van_u,", audio)
        md = (self.requests / "images_tv1_t1_b13.md").read_text(encoding="utf-8")
        self.assertIn("## img_b13_cur_tuwf", md)

    def test_batches_into_audio_files(self):
        save_rows(self.manifests / "audio_manifest.json", [arow(f"a_{i:03d}", f"t{i}") for i in range(61)])
        code, out, err = self.run_cli(["requests"])
        self.assertEqual(code, 0, err)
        self.assertTrue((self.requests / "audio_01.txt").is_file())
        self.assertTrue((self.requests / "audio_02.txt").is_file())
        self.assertFalse((self.requests / "audio_03.txt").exists())

    def test_deletes_old_files_before_writing(self):
        self.requests.mkdir()
        (self.requests / "audio_09.txt").write_text("cu", encoding="utf-8")
        (self.requests / "images_tv1_t1_b99.md").write_text("cu", encoding="utf-8")
        self.run_cli(["requests"])
        self.assertFalse((self.requests / "audio_09.txt").exists())
        self.assertFalse((self.requests / "images_tv1_t1_b99.md").exists())

    def test_missing_style_file_exits_1_and_keeps_old_files(self):
        self.requests.mkdir()
        (self.requests / "audio_01.txt").write_text("cu", encoding="utf-8")
        code, out, err = self.run_cli(["requests"], style=self.root / "khong_co.txt")
        self.assertEqual(code, 1)
        self.assertIn("khong_co.txt", out + err)
        self.assertEqual((self.requests / "audio_01.txt").read_text(encoding="utf-8"), "cu")

    def test_missing_manifests_exits_1(self):
        for name in ("audio_manifest.json", "image_manifest.json"):
            (self.manifests / name).unlink()
        code, out, err = self.run_cli(["requests"])
        self.assertEqual(code, 1)
        self.assertIn("build", out + err)
        self.assertFalse(self.requests.exists())


if __name__ == "__main__":
    unittest.main()
