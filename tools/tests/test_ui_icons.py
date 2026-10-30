import struct
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest import mock

from tapdoc import ui_icons
from tapdoc.system_assets import SYSTEM_IMAGES

FLOWER = "img_chung_hoa_be_ngoan"
MASCOT = "img_chung_ga_con"
AVATAR = "img_chung_avatar_04"


def decode_rgba(png: bytes) -> list[list[tuple[int, int, int, int]]]:
    """Giải nén PNG RGBA 8 bit (bộ lọc 0–4), trả về lưới [y][x] = (r, g, b, a)."""
    pos, width, height, data = 8, 0, 0, b""
    while pos < len(png):
        length, kind = struct.unpack(">I4s", png[pos:pos + 8])
        body = png[pos + 8:pos + 8 + length]
        if kind == b"IHDR":
            width, height, depth, color = struct.unpack(">IIBB", body[:10])
            assert (depth, color) == (8, 6), "chỉ đọc PNG RGBA 8 bit"
        elif kind == b"IDAT":
            data += body
        pos += 12 + length
    raw = zlib.decompress(data)
    stride, bpp = width * 4, 4
    rows, prev = [], bytearray(stride)
    for y in range(height):
        f = raw[y * (stride + 1)]
        line = bytearray(raw[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        for i in range(stride):
            a = line[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if f == 1:
                line[i] = (line[i] + a) & 255
            elif f == 2:
                line[i] = (line[i] + b) & 255
            elif f == 3:
                line[i] = (line[i] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pred = a if pa <= pb and pa <= pc else (b if pb <= pc else c)
                line[i] = (line[i] + pred) & 255
        rows.append([tuple(line[x * 4:x * 4 + 4]) for x in range(width)])
        prev = line
    return rows


class RenderTest(unittest.TestCase):
    def test_png_signature_and_size(self):
        png = ui_icons.render(ui_icons.ICONS["img_ui_nha"], 64)
        self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
        w, h = struct.unpack(">II", png[16:24])
        self.assertEqual((w, h), (64, 64))

    def test_every_icon_has_ink_and_transparent_corner(self):
        for icon_id, shapes in ui_icons.ICONS.items():
            px = decode_rgba(ui_icons.render(shapes, 48))
            self.assertEqual(px[0][0][3], 0, icon_id)
            self.assertTrue(any(a > 200 for row in px for (*_, a) in row), icon_id)

    def test_ink_is_centered(self):
        """Nét vẽ không lệch hẳn về một phía: tâm khối nét nằm trong 1/4 giữa khung."""
        for icon_id, shapes in ui_icons.ICONS.items():
            px = decode_rgba(ui_icons.render(shapes, 48))
            pts = [(x, y) for y, row in enumerate(px) for x, (*_, a) in enumerate(row) if a > 128]
            cx = sum(x for x, _ in pts) / len(pts)
            cy = sum(y for _, y in pts) / len(pts)
            self.assertLess(abs(cx - 24), 12, icon_id)
            self.assertLess(abs(cy - 24), 12, icon_id)

    def test_ids_match_system_images(self):
        self.assertTrue(set(ui_icons.ICONS) <= set(SYSTEM_IMAGES))
        self.assertEqual(len(ui_icons.ICONS), 12)
        self.assertIn(FLOWER, SYSTEM_IMAGES)
        self.assertIn(MASCOT, SYSTEM_IMAGES)


class WriteAllTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        (self.dir / f"{AVATAR}.png").write_bytes(b"avatar-bytes")
        # Cỡ nhỏ cho nhanh: ở đây chỉ kiểm tra file nào được ghi, không kiểm tra nét vẽ.
        for name in ("ICON_SIZE", "FLOWER_SIZE"):
            patcher = mock.patch.object(ui_icons, name, 16)
            patcher.start()
            self.addCleanup(patcher.stop)

    def tearDown(self):
        self._tmp.cleanup()

    def test_writes_missing_copies_mascot(self):
        written = ui_icons.write_all(self.dir)
        self.assertEqual(set(written), set(ui_icons.ICONS) | {FLOWER, MASCOT})
        for icon_id in ui_icons.ICONS:
            self.assertEqual((self.dir / f"{icon_id}.png").read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual((self.dir / f"{FLOWER}.png").read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual((self.dir / f"{MASCOT}.png").read_bytes(), b"avatar-bytes")

    def test_force_never_overwrites_flower_or_mascot(self):
        (self.dir / f"{FLOWER}.png").write_bytes(b"x")
        (self.dir / f"{MASCOT}.png").write_bytes(b"x")
        written = ui_icons.write_all(self.dir, force=True)
        self.assertEqual((self.dir / f"{FLOWER}.png").read_bytes(), b"x")
        self.assertEqual((self.dir / f"{MASCOT}.png").read_bytes(), b"x")
        self.assertEqual(set(written), set(ui_icons.ICONS))

    def test_keeps_existing_icon_without_force(self):
        (self.dir / "img_ui_nha.png").write_bytes(b"x")
        written = ui_icons.write_all(self.dir)
        self.assertNotIn("img_ui_nha", written)
        self.assertEqual((self.dir / "img_ui_nha.png").read_bytes(), b"x")

    def test_missing_avatar_skips_mascot(self):
        (self.dir / f"{AVATAR}.png").unlink()
        written = ui_icons.write_all(self.dir)
        self.assertNotIn(MASCOT, written)
        self.assertFalse((self.dir / f"{MASCOT}.png").exists())


if __name__ == "__main__":
    unittest.main()
