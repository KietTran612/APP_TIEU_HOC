import io
import tempfile
import unittest
import zipfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from tapdoc import __main__ as cli
from tapdoc import importer
from tapdoc.importer import ImportReport, import_audio_zip, import_image
from tapdoc.manifest import TEXT_CHANGED_NOTE, load_rows, save_rows

ID3 = b"ID3\x04\x00\x00\x00\x00\x00\x00"
PNG = b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\rIHDR" + b"\x00" * 20
JPEG = b"\xff\xd8\xff\xe0\x00\x10JFIF" + b"\x00" * 20


def arow(i, text="đờ", status="chua_co", source="", ghi_chu=""):
    return {"id": i, "text": text, "kind": "am", "file": f"audio/{i}.mp3", "source": source, "status": status,
            "can_nghe_ky": False, "ghi_chu": ghi_chu, "bai": ["tv1_t1_b13"]}


def irow(i, status="chua_co", source="", ghi_chu=""):
    return {"id": i, "mo_ta": "Bé gái ngồi đánh đu", "bai": ["tv1_t1_b13"], "file": f"images/{i}.png",
            "source": source, "status": status, "ghi_chu": ghi_chu}


def make_zip(path, members, compress=zipfile.ZIP_DEFLATED):
    """Ghi ZIP với đúng các tên mục đã cho (ZipInfo, không để zipfile chuẩn hóa tên)."""
    with zipfile.ZipFile(path, "w") as zf:
        for name, data in members:
            zf.writestr(zipfile.ZipInfo(name), data, compress_type=compress)
    return Path(path)


def field_of(manifest_path, row_id, field):
    return next(row[field] for row in load_rows(manifest_path) if row["id"] == row_id)


def listing(root):
    """Mọi file dưới root, theo đường dẫn tương đối."""
    return sorted(p.relative_to(root).as_posix() for p in Path(root).rglob("*") if p.is_file())


class TempDirCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)


class ImportAudioZipTest(TempDirCase):
    def setUp(self):
        super().setUp()
        self.audio_dir = self.root / "out" / "audio"
        self.manifest = self.root / "manifests" / "audio_manifest.json"
        self.zip = self.root / "tai_ve.zip"
        save_rows(self.manifest, [arow("am_dd"), arow("tieng_ddu"), arow("van_u")])

    def run_import(self, members, **kw):
        make_zip(self.zip, members, **kw)
        return import_audio_zip(self.zip, self.audio_dir, self.manifest)

    def test_brief_scenario(self):
        rep = self.run_import([
            ("am_dd.mp3", ID3 + b"1"),
            ("nested/tieng_ddu.mp3", ID3 + b"2"),
            ("../evil.mp3", ID3 + b"3"),
            ("notes.txt", b"ghi chu"),
            ("van_u.mp3", b"hello"),
        ])
        self.assertIsInstance(rep, ImportReport)
        self.assertEqual(sorted(rep.imported), ["am_dd", "tieng_ddu"])
        self.assertEqual(sorted(n for n, _ in rep.skipped), ["../evil.mp3", "notes.txt", "van_u.mp3"])
        self.assertEqual(sorted(p.name for p in self.audio_dir.iterdir()), ["am_dd.mp3", "tieng_ddu.mp3"])
        self.assertFalse((self.audio_dir.parent / "evil.mp3").exists())
        self.assertEqual(field_of(self.manifest, "am_dd", "status"), "cho_duyet")

    def test_files_have_the_member_bytes(self):
        self.run_import([("am_dd.mp3", ID3 + b"mot"), ("sub/tieng_ddu.mp3", ID3 + b"hai")])
        self.assertEqual((self.audio_dir / "am_dd.mp3").read_bytes(), ID3 + b"mot")
        self.assertEqual((self.audio_dir / "tieng_ddu.mp3").read_bytes(), ID3 + b"hai")

    def test_manifest_gets_cho_duyet_and_chatgpt_tam_for_imported_rows_only(self):
        before = {row["id"]: row for row in load_rows(self.manifest)}
        self.run_import([("am_dd.mp3", ID3), ("van_u.mp3", b"hello")])
        after = {row["id"]: row for row in load_rows(self.manifest)}
        self.assertEqual(after["am_dd"]["status"], "cho_duyet")
        self.assertEqual(after["am_dd"]["source"], "chatgpt_tam")
        self.assertEqual({k: v for k, v in after["am_dd"].items() if k not in ("status", "source")},
                         {k: v for k, v in before["am_dd"].items() if k not in ("status", "source")})
        self.assertEqual(after["van_u"], before["van_u"])  # bị bỏ qua nên không đổi
        self.assertEqual(after["tieng_ddu"], before["tieng_ddu"])

    def test_reimport_replaces_old_file_and_overrides_old_status(self):
        save_rows(self.manifest, [arow("am_dd", status="dat", source="tay")])
        self.audio_dir.mkdir(parents=True)
        (self.audio_dir / "am_dd.mp3").write_bytes(b"cu")
        self.run_import([("am_dd.mp3", ID3 + b"moi")])
        self.assertEqual((self.audio_dir / "am_dd.mp3").read_bytes(), ID3 + b"moi")
        self.assertEqual(field_of(self.manifest, "am_dd", "status"), "cho_duyet")
        self.assertEqual(field_of(self.manifest, "am_dd", "source"), "chatgpt_tam")

    def test_creates_missing_audio_dir_and_leaves_no_temp_files(self):
        self.assertFalse(self.audio_dir.exists())
        self.run_import([("am_dd.mp3", ID3)])
        self.assertEqual([p.name for p in self.audio_dir.iterdir()], ["am_dd.mp3"])

    def test_path_tricks_write_only_inside_audio_dir(self):
        rep = self.run_import([
            ("../am_dd.mp3", ID3 + b"1"),
            ("../../tieng_ddu.mp3", ID3 + b"2"),
            ("/tmp/abs/van_u.mp3", ID3 + b"3"),
            ("C:\\Windows\\evil.mp3", ID3 + b"4"),
            ("a\\..\\..\\x.mp3", ID3 + b"5"),
        ])
        self.assertEqual(sorted(rep.imported), ["am_dd", "tieng_ddu", "van_u"])
        # evil và x không có trong danh mục (tên mục có thể đã được đổi "\" thành "/" tùy hệ điều hành)
        self.assertEqual(len(rep.skipped), 2)
        self.assertTrue(all("danh mục" in reason for _, reason in rep.skipped))
        self.assertEqual(listing(self.root), [
            "manifests/audio_manifest.json", "out/audio/am_dd.mp3", "out/audio/tieng_ddu.mp3",
            "out/audio/van_u.mp3", "tai_ve.zip"])

    def test_backslash_separator_uses_last_component(self):
        rep = self.run_import([("thu_muc\\am_dd.mp3", ID3)])
        self.assertEqual(rep.imported, ["am_dd"])
        self.assertEqual(rep.skipped, [])

    def test_backslash_in_member_name_uses_last_component_on_any_platform(self):
        # Trên Windows zipfile tự đổi "\" thành "/" khi đọc; ép tên có "\" để kiểm cả trường hợp không đổi.
        make_zip(self.zip, [("x/am_dd.mp3", ID3), ("y/tieng_ddu.mp3", ID3)])
        real_infolist = zipfile.ZipFile.infolist

        def infolist_with_backslashes(zf):
            infos = real_infolist(zf)
            for info in infos:
                info.filename = "..\\thu_muc\\" + info.filename.split("/")[-1]
            return infos

        with mock.patch.object(zipfile.ZipFile, "infolist", infolist_with_backslashes):
            rep = import_audio_zip(self.zip, self.audio_dir, self.manifest)
        self.assertEqual(sorted(rep.imported), ["am_dd", "tieng_ddu"])
        self.assertEqual(rep.skipped, [])
        self.assertEqual(sorted(p.name for p in self.audio_dir.iterdir()), ["am_dd.mp3", "tieng_ddu.mp3"])

    def test_directory_entries_are_silently_ignored(self):
        rep = self.run_import([("nested/", b""), ("khac\\", b""), ("nested/sau/", b""), ("am_dd.mp3", ID3)])
        self.assertEqual(rep.imported, ["am_dd"])
        self.assertEqual(rep.skipped, [])

    def test_bad_names_are_skipped_with_reason(self):
        bad = ["Am_dd.mp3", "am-dd.mp3", "am_dd.MP3", "am_dd.mp3.exe", ".mp3", "am dd.mp3", "am_dd.wav",
               "am_dd.mp3\n", "ám_dd.mp3"]
        rep = self.run_import([(name, ID3) for name in bad])
        self.assertEqual(rep.imported, [])
        self.assertEqual(sorted(n for n, _ in rep.skipped), sorted(bad))
        for _, reason in rep.skipped:
            self.assertTrue(reason)
        self.assertFalse(self.audio_dir.exists() and any(self.audio_dir.iterdir()))
        self.assertEqual(field_of(self.manifest, "am_dd", "status"), "chua_co")

    def test_unknown_id_is_skipped_and_reason_names_it(self):
        rep = self.run_import([("khong_co.mp3", ID3)])
        self.assertEqual(rep.imported, [])
        (name, reason), = rep.skipped
        self.assertEqual(name, "khong_co.mp3")
        self.assertIn("khong_co", reason)
        self.assertIn("danh mục", reason)

    def test_oversize_member_is_skipped_by_declared_size(self):
        limit = importer.MAX_AUDIO_BYTES
        self.assertEqual(limit, 5 * 1024 * 1024)
        # Rất dễ nén: ZIP nhỏ nhưng nội dung 6 MB.
        rep = self.run_import([("am_dd.mp3", ID3 + b"\x00" * (6 * 1024 * 1024)), ("tieng_ddu.mp3", ID3)])
        self.assertEqual(rep.imported, ["tieng_ddu"])
        (name, reason), = rep.skipped
        self.assertEqual(name, "am_dd.mp3")
        self.assertIn("5 MB", reason)
        self.assertFalse((self.audio_dir / "am_dd.mp3").exists())
        self.assertLess(self.zip.stat().st_size, 1024 * 1024)

    def test_size_limit_is_inclusive(self):
        limit = importer.MAX_AUDIO_BYTES
        rep = self.run_import([("am_dd.mp3", ID3 + b"\x00" * (limit - len(ID3))),
                               ("tieng_ddu.mp3", ID3 + b"\x00" * (limit - len(ID3) + 1))])
        self.assertEqual(rep.imported, ["am_dd"])
        self.assertEqual([n for n, _ in rep.skipped], ["tieng_ddu.mp3"])
        self.assertEqual((self.audio_dir / "am_dd.mp3").stat().st_size, limit)

    def test_oversize_check_happens_before_reading_the_member(self):
        make_zip(self.zip, [("am_dd.mp3", ID3 + b"\x00" * 100)])
        with mock.patch.object(importer, "MAX_AUDIO_BYTES", 50), \
                mock.patch.object(zipfile.ZipFile, "read") as read, \
                mock.patch.object(zipfile.ZipFile, "open") as zopen:
            rep = import_audio_zip(self.zip, self.audio_dir, self.manifest)
        read.assert_not_called()
        zopen.assert_not_called()
        self.assertEqual(rep.imported, [])
        self.assertEqual([n for n, _ in rep.skipped], ["am_dd.mp3"])

    def test_lying_file_size_oversize_member_is_skipped_by_bounded_read(self):
        make_zip(self.zip, [("am_dd.mp3", ID3 + b"\x00" * (6 * 1024 * 1024)), ("tieng_ddu.mp3", ID3)])
        real_infolist = zipfile.ZipFile.infolist
        real_open = zipfile.ZipFile.open
        real_sizes = {}

        def lying_infolist(zf):
            infos = real_infolist(zf)
            for info in infos:
                if info.filename == "am_dd.mp3":
                    real_sizes[info.filename] = info.file_size
                    info.file_size = 10  # khai gian kích thước nhỏ để lọt qua bước kiểm tra đầu
            return infos

        def open_with_real_stream(zf, info, *args, **kwargs):
            if isinstance(info, zipfile.ZipInfo) and info.filename in real_sizes:
                info.file_size = real_sizes[info.filename]
            return real_open(zf, info, *args, **kwargs)

        with mock.patch.object(zipfile.ZipFile, "infolist", lying_infolist), \
                mock.patch.object(zipfile.ZipFile, "open", open_with_real_stream):
            rep = import_audio_zip(self.zip, self.audio_dir, self.manifest)
        self.assertEqual(rep.imported, ["tieng_ddu"])
        (name, reason), = rep.skipped
        self.assertEqual(name, "am_dd.mp3")
        self.assertIn("quá lớn", reason)
        self.assertIn("5 MB", reason)
        self.assertFalse((self.audio_dir / "am_dd.mp3").exists())

    def test_duplicate_id_first_wins(self):
        rep = self.run_import([("a/am_dd.mp3", ID3 + b"dau"), ("b/am_dd.mp3", ID3 + b"sau"),
                               ("am_dd.mp3", ID3 + b"cuoi")])
        self.assertEqual(rep.imported, ["am_dd"])
        self.assertEqual([n for n, _ in rep.skipped], ["b/am_dd.mp3", "am_dd.mp3"])
        for _, reason in rep.skipped:
            self.assertIn("am_dd", reason)
        self.assertEqual((self.audio_dir / "am_dd.mp3").read_bytes(), ID3 + b"dau")

    def test_duplicate_only_counts_after_a_successful_import(self):
        rep = self.run_import([("a/am_dd.mp3", b"hello"), ("b/am_dd.mp3", ID3 + b"tot")])
        self.assertEqual(rep.imported, ["am_dd"])
        self.assertEqual([n for n, _ in rep.skipped], ["a/am_dd.mp3"])
        self.assertEqual((self.audio_dir / "am_dd.mp3").read_bytes(), ID3 + b"tot")

    def test_mpeg_frame_sync_is_accepted(self):
        rep = self.run_import([("am_dd.mp3", b"\xff\xfb\x90\x00"), ("tieng_ddu.mp3", b"\xff\xe3"),
                               ("van_u.mp3", b"\xff\xf3\x00")])
        self.assertEqual(sorted(rep.imported), ["am_dd", "tieng_ddu", "van_u"])
        self.assertEqual(rep.skipped, [])
        for edge in (b"\xff\xe0", b"\xff\xff"):  # hai biên của 3 bit đồng bộ
            with self.subTest(edge=edge):
                self.assertEqual(self.run_import([("am_dd.mp3", edge)]).imported, ["am_dd"])
        for near in (b"\xff\xdf", b"\xff\xc0", b"\xff\x80", b"\xff\x00"):  # thiếu một trong 3 bit đồng bộ
            with self.subTest(near=near):
                self.assertEqual(self.run_import([("am_dd.mp3", near)]).imported, [])

    def test_not_mp3_content_is_skipped(self):
        for bad in (b"", b"\xff", b"ID", b"\xff\x1f", b"\xfe\xfb", b"\x00\xff\xfb", b"RIFF....WAVE", PNG, b"id3"):
            with self.subTest(content=bad[:6]):
                rep = self.run_import([("am_dd.mp3", bad)])
                self.assertEqual(rep.imported, [])
                (name, reason), = rep.skipped
                self.assertEqual(name, "am_dd.mp3")
                self.assertIn("MP3", reason)
        self.assertFalse((self.audio_dir / "am_dd.mp3").exists())
        self.assertEqual(field_of(self.manifest, "am_dd", "status"), "chua_co")

    def test_corrupt_member_is_skipped_and_others_still_import(self):
        make_zip(self.zip, [("am_dd.mp3", ID3 + b"xxxxxxxxxx"), ("tieng_ddu.mp3", ID3 + b"yyyyyyyyyy")],
                 compress=zipfile.ZIP_STORED)
        raw = self.zip.read_bytes()
        self.assertIn(b"xxxxxxxxxx", raw)
        self.zip.write_bytes(raw.replace(b"xxxxxxxxxx", b"xxxxzxxxxx"))  # hỏng CRC
        rep = import_audio_zip(self.zip, self.audio_dir, self.manifest)
        self.assertEqual(rep.imported, ["tieng_ddu"])
        self.assertEqual([n for n, _ in rep.skipped], ["am_dd.mp3"])
        self.assertFalse((self.audio_dir / "am_dd.mp3").exists())

    def test_manifest_saved_once_and_only_when_something_was_imported(self):
        with mock.patch.object(importer, "save_rows", wraps=importer.save_rows) as saver:
            self.run_import([("am_dd.mp3", ID3), ("tieng_ddu.mp3", ID3), ("van_u.mp3", b"hello")])
        self.assertEqual(saver.call_count, 1)
        before = self.manifest.read_bytes()
        with mock.patch.object(importer, "save_rows") as saver:
            rep = self.run_import([("van_u.mp3", b"hello"), ("notes.txt", b"x")])
        self.assertEqual(rep.imported, [])
        saver.assert_not_called()
        self.assertEqual(self.manifest.read_bytes(), before)

    def test_write_failure_skips_that_member_only(self):
        real_replace = importer.os.replace

        def flaky(src, dst):
            if Path(dst).name == "am_dd.mp3":
                raise PermissionError("đang bị khóa")
            return real_replace(src, dst)

        with mock.patch.object(importer.os, "replace", side_effect=flaky):
            rep = self.run_import([("am_dd.mp3", ID3), ("tieng_ddu.mp3", ID3)])
        self.assertEqual(rep.imported, ["tieng_ddu"])
        self.assertEqual([n for n, _ in rep.skipped], ["am_dd.mp3"])
        self.assertEqual([p.name for p in self.audio_dir.iterdir()], ["tieng_ddu.mp3"])  # không để lại file tạm
        self.assertEqual(field_of(self.manifest, "am_dd", "status"), "chua_co")
        self.assertEqual(field_of(self.manifest, "tieng_ddu", "status"), "cho_duyet")

    def test_not_a_zip_raises_value_error(self):
        self.zip.write_text("đây không phải ZIP", encoding="utf-8")
        with self.assertRaises(ValueError) as ctx:
            import_audio_zip(self.zip, self.audio_dir, self.manifest)
        self.assertIn("ZIP", str(ctx.exception))
        self.assertFalse(self.audio_dir.exists())

    def test_empty_and_missing_files_raise_value_error(self):
        self.zip.write_bytes(b"")
        with self.assertRaises(ValueError):
            import_audio_zip(self.zip, self.audio_dir, self.manifest)
        with self.assertRaises(ValueError) as ctx:
            import_audio_zip(self.root / "khong_co.zip", self.audio_dir, self.manifest)
        self.assertIn("khong_co.zip", str(ctx.exception))
        with self.assertRaises(ValueError):
            import_audio_zip(self.root, self.audio_dir, self.manifest)  # thư mục, không phải file

    def test_empty_zip_imports_nothing(self):
        rep = self.run_import([])
        self.assertEqual((rep.imported, rep.skipped), ([], []))

    def test_missing_manifest_skips_everything(self):
        self.manifest.unlink()
        rep = self.run_import([("am_dd.mp3", ID3)])
        self.assertEqual(rep.imported, [])
        self.assertEqual([n for n, _ in rep.skipped], ["am_dd.mp3"])
        self.assertFalse(self.manifest.exists())

    def test_not_implemented_and_unicode_errors_on_open_raise_value_error(self):
        make_zip(self.zip, [("am_dd.mp3", ID3)])
        errors = [
            NotImplementedError("compression type 99"),
            UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid start byte"),
        ]
        for err in errors:
            with self.subTest(err=type(err).__name__), \
                    mock.patch.object(importer.zipfile, "ZipFile", side_effect=err):
                with self.assertRaises(ValueError) as ctx:
                    import_audio_zip(self.zip, self.audio_dir, self.manifest)
                self.assertIn("không phải file ZIP hợp lệ", str(ctx.exception))

    def test_interrupt_mid_loop_still_saves_already_imported_rows(self):
        make_zip(self.zip, [("am_dd.mp3", ID3 + b"1"), ("tieng_ddu.mp3", ID3 + b"2")])
        real_write = importer._write_atomic

        def boom_on_second(dest, data):
            if dest.name == "tieng_ddu.mp3":
                raise RuntimeError("lỗi bất ngờ giữa chừng")
            return real_write(dest, data)

        with mock.patch.object(importer, "_write_atomic", side_effect=boom_on_second), \
                mock.patch.object(importer, "save_rows", wraps=importer.save_rows) as saver:
            with self.assertRaises(RuntimeError):
                import_audio_zip(self.zip, self.audio_dir, self.manifest)
        self.assertEqual(saver.call_count, 1)
        self.assertEqual(field_of(self.manifest, "am_dd", "status"), "cho_duyet")
        self.assertEqual(field_of(self.manifest, "am_dd", "source"), "chatgpt_tam")
        self.assertEqual(field_of(self.manifest, "tieng_ddu", "status"), "chua_co")

    def test_zip_handle_closed_when_load_rows_fails(self):
        make_zip(self.zip, [("am_dd.mp3", ID3)])
        self.manifest.write_text("{json hỏng", encoding="utf-8")
        with self.assertRaises(ValueError):
            import_audio_zip(self.zip, self.audio_dir, self.manifest)
        # Trên Windows, nếu ZipFile chưa đóng thì unlink sẽ báo PermissionError.
        self.zip.unlink()
        self.assertFalse(self.zip.exists())

    def test_strips_text_changed_note_and_preserves_user_note(self):
        save_rows(self.manifest, [
            arow("am_dd", status="khong_dat", ghi_chu=TEXT_CHANGED_NOTE),
            arow("tieng_ddu", status="khong_dat", ghi_chu=f"{TEXT_CHANGED_NOTE}; đọc hơi nhanh"),
            arow("van_u", status="khong_dat", ghi_chu=TEXT_CHANGED_NOTE),
        ])
        self.run_import([("am_dd.mp3", ID3 + b"1"), ("tieng_ddu.mp3", ID3 + b"2")])
        self.assertEqual(field_of(self.manifest, "am_dd", "ghi_chu"), "")
        self.assertEqual(field_of(self.manifest, "tieng_ddu", "ghi_chu"), "đọc hơi nhanh")
        self.assertEqual(field_of(self.manifest, "van_u", "ghi_chu"), TEXT_CHANGED_NOTE)  # chưa nhập thì giữ nguyên


class ImportImageTest(TempDirCase):
    def setUp(self):
        super().setUp()
        self.image_dir = self.root / "out" / "images"
        self.manifest = self.root / "manifests" / "image_manifest.json"
        save_rows(self.manifest, [irow("img_b13_cais_ddu"), irow("img_b13_cur_tuwf")])
        self.png = self.root / "tai_ve.png"
        self.png.write_bytes(PNG)
        self.jpeg = self.root / "tai_ve.jpg"
        self.jpeg.write_bytes(JPEG)

    def test_image(self):
        import_image(self.png, "img_b13_cais_ddu", self.image_dir, self.manifest)
        self.assertTrue((self.image_dir / "img_b13_cais_ddu.png").exists())
        with self.assertRaises(ValueError):
            import_image(self.jpeg, "img_b13_cais_ddu", self.image_dir, self.manifest)
        with self.assertRaises(ValueError):
            import_image(self.png, "img_khong_co", self.image_dir, self.manifest)

    def test_copies_bytes_and_marks_row(self):
        import_image(self.png, "img_b13_cais_ddu", self.image_dir, self.manifest)
        self.assertEqual((self.image_dir / "img_b13_cais_ddu.png").read_bytes(), PNG)
        self.assertEqual(field_of(self.manifest, "img_b13_cais_ddu", "status"), "cho_duyet")
        self.assertEqual(field_of(self.manifest, "img_b13_cais_ddu", "source"), "chatgpt_tam")
        self.assertEqual(field_of(self.manifest, "img_b13_cur_tuwf", "status"), "chua_co")  # dòng khác không đổi
        self.assertEqual(field_of(self.manifest, "img_b13_cur_tuwf", "source"), "")
        self.assertTrue(self.png.exists())  # file tải về vẫn còn
        self.assertEqual([p.name for p in self.image_dir.iterdir()], ["img_b13_cais_ddu.png"])  # không file tạm

    def test_replaces_existing_and_overrides_old_status(self):
        save_rows(self.manifest, [irow("img_b13_cais_ddu", status="dat", source="tay")])
        self.image_dir.mkdir(parents=True)
        (self.image_dir / "img_b13_cais_ddu.png").write_bytes(b"cu")
        import_image(self.png, "img_b13_cais_ddu", self.image_dir, self.manifest)
        self.assertEqual((self.image_dir / "img_b13_cais_ddu.png").read_bytes(), PNG)
        self.assertEqual(field_of(self.manifest, "img_b13_cais_ddu", "status"), "cho_duyet")

    def test_failures_leave_everything_untouched(self):
        before = self.manifest.read_bytes()
        cases = [(self.jpeg, "img_b13_cais_ddu"), (self.png, "img_khong_co"),
                 (self.root / "khong_co.png", "img_b13_cais_ddu")]
        for path, image_id in cases:
            with self.subTest(path=path.name, image_id=image_id):
                with self.assertRaises(ValueError):
                    import_image(path, image_id, self.image_dir, self.manifest)
        self.assertFalse(self.image_dir.exists())
        self.assertEqual(self.manifest.read_bytes(), before)

    def test_messages_are_vietnamese_and_name_the_problem(self):
        with self.assertRaises(ValueError) as ctx:
            import_image(self.jpeg, "img_b13_cais_ddu", self.image_dir, self.manifest)
        self.assertIn("PNG", str(ctx.exception))
        with self.assertRaises(ValueError) as ctx:
            import_image(self.png, "img_khong_co", self.image_dir, self.manifest)
        self.assertIn("img_khong_co", str(ctx.exception))
        self.assertIn("danh mục", str(ctx.exception))
        with self.assertRaises(ValueError) as ctx:
            import_image(self.root / "khong_co.png", "img_b13_cais_ddu", self.image_dir, self.manifest)
        self.assertIn("khong_co.png", str(ctx.exception))

    def test_signature_must_be_the_full_8_bytes(self):
        for name, data in (("ngan.png", b"\x89PNG"), ("rong.png", b""), ("sai.png", b"\x89PNG\r\n\x1a\x0b")):
            with self.subTest(name=name):
                path = self.root / name
                path.write_bytes(data)
                with self.assertRaises(ValueError):
                    import_image(path, "img_b13_cais_ddu", self.image_dir, self.manifest)
        bare = self.root / "chi_chu_ky.png"
        bare.write_bytes(b"\x89PNG\r\n\x1a\n")
        import_image(bare, "img_b13_cais_ddu", self.image_dir, self.manifest)  # chỉ kiểm chữ ký
        self.assertTrue((self.image_dir / "img_b13_cais_ddu.png").exists())

    def test_directory_instead_of_file_raises(self):
        with self.assertRaises(ValueError):
            import_image(self.root, "img_b13_cais_ddu", self.image_dir, self.manifest)

    def test_too_large_file_is_refused(self):
        self.assertEqual(importer.MAX_IMAGE_BYTES, 20 * 1024 * 1024)
        big = self.root / "to.png"
        big.write_bytes(PNG + b"\x00" * 100)
        with mock.patch.object(importer, "MAX_IMAGE_BYTES", len(PNG) + 99):
            with self.assertRaises(ValueError) as ctx:
                import_image(big, "img_b13_cais_ddu", self.image_dir, self.manifest)
        self.assertIn("quá lớn", str(ctx.exception))
        self.assertFalse(self.image_dir.exists())
        self.assertEqual(field_of(self.manifest, "img_b13_cais_ddu", "status"), "chua_co")
        with mock.patch.object(importer, "MAX_IMAGE_BYTES", len(PNG) + 100):  # đúng bằng giới hạn thì được
            import_image(big, "img_b13_cais_ddu", self.image_dir, self.manifest)
        self.assertEqual((self.image_dir / "img_b13_cais_ddu.png").stat().st_size, len(PNG) + 100)

    def test_id_cannot_escape_the_image_dir(self):
        save_rows(self.manifest, [irow("../evil"), irow("a/b"), irow("img_b13_cais_ddu")])  # kể cả danh mục có mã lạ
        for image_id in ("../evil", "a/b", "..\\evil", "img_b13_cais_ddu/../../x"):
            with self.subTest(image_id=image_id):
                with self.assertRaises(ValueError):
                    import_image(self.png, image_id, self.image_dir, self.manifest)
        self.assertFalse((self.root / "out" / "evil.png").exists())
        self.assertFalse(self.image_dir.exists())

    def test_write_failure_leaves_no_temp_file_and_manifest_unchanged(self):
        self.image_dir.mkdir(parents=True)
        before = self.manifest.read_bytes()
        with mock.patch.object(importer.os, "replace", side_effect=PermissionError("đang bị khóa")):
            with self.assertRaises(OSError):
                import_image(self.png, "img_b13_cais_ddu", self.image_dir, self.manifest)
        self.assertEqual(list(self.image_dir.iterdir()), [])
        self.assertEqual(self.manifest.read_bytes(), before)

    def test_strips_text_changed_note_and_preserves_user_note(self):
        save_rows(self.manifest, [
            irow("img_b13_cais_ddu", status="khong_dat", ghi_chu=TEXT_CHANGED_NOTE),
            irow("img_b13_cur_tuwf", status="khong_dat", ghi_chu=f"{TEXT_CHANGED_NOTE}; màu hơi tối"),
        ])
        import_image(self.png, "img_b13_cais_ddu", self.image_dir, self.manifest)
        self.assertEqual(field_of(self.manifest, "img_b13_cais_ddu", "ghi_chu"), "")
        self.assertEqual(field_of(self.manifest, "img_b13_cur_tuwf", "ghi_chu"), f"{TEXT_CHANGED_NOTE}; màu hơi tối")
        import_image(self.png, "img_b13_cur_tuwf", self.image_dir, self.manifest)
        self.assertEqual(field_of(self.manifest, "img_b13_cur_tuwf", "ghi_chu"), "màu hơi tối")


class ImportCliTest(TempDirCase):
    def setUp(self):
        super().setUp()
        self.manifests = self.root / "manifests"
        self.unity_res = self.root / "res"
        self.audio_manifest = self.manifests / "audio_manifest.json"
        self.image_manifest = self.manifests / "image_manifest.json"
        save_rows(self.audio_manifest, [arow("am_dd"), arow("tieng_ddu"), arow("van_u")])
        save_rows(self.image_manifest, [irow("img_b13_cais_ddu")])
        self.zip = self.root / "tai_ve.zip"
        self.png = self.root / "tranh.png"
        self.png.write_bytes(PNG)

    def run_cli(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(cli, "MANIFESTS", self.manifests), \
                mock.patch.object(cli, "UNITY_RES", self.unity_res), \
                redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_import_audio_lists_imported_and_skipped_with_reasons(self):
        make_zip(self.zip, [("am_dd.mp3", ID3), ("nested/tieng_ddu.mp3", ID3), ("../evil.mp3", ID3),
                            ("notes.txt", b"x"), ("van_u.mp3", b"hello")])
        code, out, err = self.run_cli(["import-audio", str(self.zip)])
        self.assertEqual(code, 0, err)
        for text in ("am_dd", "tieng_ddu", "../evil.mp3", "notes.txt", "van_u.mp3"):
            self.assertIn(text, out)
        evil_line = next(line for line in out.splitlines() if "../evil.mp3" in line)
        self.assertIn("danh mục", evil_line)  # kèm lý do
        notes_line = next(line for line in out.splitlines() if "notes.txt" in line)
        self.assertIn("tên", notes_line)
        self.assertEqual(sorted(p.name for p in (self.unity_res / "audio").iterdir()), ["am_dd.mp3", "tieng_ddu.mp3"])
        self.assertEqual(field_of(self.audio_manifest, "am_dd", "status"), "cho_duyet")
        self.assertEqual(field_of(self.audio_manifest, "am_dd", "source"), "chatgpt_tam")
        self.assertEqual(field_of(self.audio_manifest, "van_u", "status"), "chua_co")
        self.assertEqual(listing(self.root), [
            "manifests/audio_manifest.json", "manifests/image_manifest.json", "res/audio/am_dd.mp3",
            "res/audio/tieng_ddu.mp3", "tai_ve.zip", "tranh.png"])

    def test_import_audio_with_nothing_imported_still_exits_0(self):
        make_zip(self.zip, [("notes.txt", b"x")])
        code, out, err = self.run_cli(["import-audio", str(self.zip)])
        self.assertEqual(code, 0, err)
        self.assertIn("notes.txt", out)

    def test_import_audio_prints_member_names_safely(self):
        make_zip(self.zip, [("\x1b[31mdo\x07.mp3", ID3)])
        code, out, err = self.run_cli(["import-audio", str(self.zip)])
        self.assertEqual(code, 0, err)
        self.assertNotIn("\x1b", out + err)
        self.assertNotIn("\x07", out + err)

    def test_import_audio_invalid_zip_exits_1(self):
        self.zip.write_text("không phải ZIP", encoding="utf-8")
        code, out, err = self.run_cli(["import-audio", str(self.zip)])
        self.assertEqual(code, 1)
        self.assertIn("ZIP", out + err)
        self.assertFalse((self.unity_res / "audio").exists())

    def test_import_audio_missing_zip_exits_1(self):
        code, out, err = self.run_cli(["import-audio", str(self.root / "khong_co.zip")])
        self.assertEqual(code, 1)
        self.assertIn("khong_co.zip", out + err)

    def test_import_audio_without_manifest_exits_1_and_points_to_build(self):
        self.audio_manifest.unlink()
        make_zip(self.zip, [("am_dd.mp3", ID3)])
        code, out, err = self.run_cli(["import-audio", str(self.zip)])
        self.assertEqual(code, 1)
        self.assertIn("build", out + err)
        self.assertFalse((self.unity_res / "audio").exists())

    def test_import_image_success(self):
        code, out, err = self.run_cli(["import-image", str(self.png), "img_b13_cais_ddu"])
        self.assertEqual(code, 0, err)
        self.assertIn("img_b13_cais_ddu", out)
        self.assertEqual((self.unity_res / "images" / "img_b13_cais_ddu.png").read_bytes(), PNG)
        self.assertEqual(field_of(self.image_manifest, "img_b13_cais_ddu", "status"), "cho_duyet")
        self.assertEqual(field_of(self.image_manifest, "img_b13_cais_ddu", "source"), "chatgpt_tam")

    def test_import_image_not_png_exits_1(self):
        jpeg = self.root / "tranh.jpg"
        jpeg.write_bytes(JPEG)
        code, out, err = self.run_cli(["import-image", str(jpeg), "img_b13_cais_ddu"])
        self.assertEqual(code, 1)
        self.assertIn("PNG", out + err)
        self.assertFalse((self.unity_res / "images").exists())
        self.assertEqual(field_of(self.image_manifest, "img_b13_cais_ddu", "status"), "chua_co")

    def test_import_image_unknown_id_exits_1(self):
        code, out, err = self.run_cli(["import-image", str(self.png), "img_khong_co"])
        self.assertEqual(code, 1)
        self.assertIn("img_khong_co", out + err)
        self.assertFalse((self.unity_res / "images").exists())

    def test_import_image_without_manifest_exits_1_and_points_to_build(self):
        self.image_manifest.unlink()
        code, out, err = self.run_cli(["import-image", str(self.png), "img_b13_cais_ddu"])
        self.assertEqual(code, 1)
        self.assertIn("build", out + err)

    def test_import_image_write_error_exits_1_instead_of_traceback(self):
        with mock.patch.object(importer.os, "replace", side_effect=PermissionError("đang bị khóa")):
            code, out, err = self.run_cli(["import-image", str(self.png), "img_b13_cais_ddu"])
        self.assertEqual(code, 1)
        self.assertIn("img_b13_cais_ddu", out + err)


if __name__ == "__main__":
    unittest.main()
