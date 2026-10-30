"""Biểu tượng giao diện, hoa bé ngoan tạm và gà con tạm (hình mặc định cho tới khi có tranh chính thức).

Mỗi hình là một danh sách nét vẽ trong khung 24×24, vẽ ra PNG RGBA chỉ bằng thư viện chuẩn. Ba loại nét:

- ``("fill", points, color)``: đa giác tô kín;
- ``("stroke", points, width, color, closed)``: đường gấp khúc có độ dày;
- ``("circle", cx, cy, r, fill, stroke_width)``: hình tròn, ``fill`` là ``None`` thì chỉ có viền mực.

Màu theo bảng màu của bản thiết kế giao diện (mục 4.1). Hình chính thức sau này ghi đè file cùng mã.
"""

import math
import shutil
import struct
import zlib
from pathlib import Path

INK = (43, 38, 33)
PAPER = (251, 246, 233)
TEAL = (47, 140, 155)
STAR_YELLOW = (244, 197, 74)
PETAL_PINK = (239, 138, 165)
ROSE_DARK = (184, 64, 95)
LEAF_GREEN = (111, 179, 106)
LOCKED_FILL = (216, 206, 182)
LOCKED_INK = (166, 156, 134)

ICON_SIZE = 192
FLOWER_SIZE = 256
VIEW = 24.0
SAMPLES = 4  # lấy mẫu 4×4 trong mỗi điểm ảnh để viền mịn

FLOWER_ID = "img_chung_hoa_be_ngoan"
MASCOT_ID = "img_chung_ga_con"
MASCOT_SOURCE_ID = "img_chung_avatar_04"


def _arc(cx, cy, r, start_deg, end_deg, steps=24):
    """Các điểm trên cung tròn, góc tính theo độ, 0° chỉ sang phải, chiều kim đồng hồ trên màn hình."""
    return [(cx + r * math.cos(math.radians(start_deg + (end_deg - start_deg) * i / steps)),
             cy + r * math.sin(math.radians(start_deg + (end_deg - start_deg) * i / steps)))
            for i in range(steps + 1)]


def _outlined(points, width, color=PAPER, closed=False):
    """Nét màu ``color`` có viền mực, như mũi tên trên nút tròn."""
    return [("stroke", points, width + 1.6, INK, closed), ("stroke", points, width, color, closed)]


def _star(cx, cy, outer, inner):
    return [(cx + (outer if i % 2 == 0 else inner) * math.cos(math.radians(-90 + 36 * i)),
             cy + (outer if i % 2 == 0 else inner) * math.sin(math.radians(-90 + 36 * i)))
            for i in range(10)]


def _mirror(shapes):
    """Lật ngang một hình (mũi tên phải thành mũi tên trái)."""
    out = []
    for shape in shapes:
        if shape[0] == "circle":
            out.append((shape[0], VIEW - shape[1]) + tuple(shape[2:]))
        else:
            out.append((shape[0], [(VIEW - x, y) for x, y in shape[1]]) + tuple(shape[2:]))
    return out


_ARROW = _outlined([(5, 12), (17.5, 12)], 3.2) + _outlined([(12, 6.5), (17.8, 12), (12, 17.5)], 3.2)
# Cánh hoa hình giọt nước, đầu nhọn ở trên.
_PETAL = [(12 + 5.5 * math.sin(math.radians(a)) * (1 - 0.35 * math.cos(math.radians(a))),
           12 - 8 * math.cos(math.radians(a))) for a in range(0, 360, 15)]
_PAGE = [("fill", [(6, 3.5), (15, 3.5), (19, 7.5), (19, 20.5), (6, 20.5)], PAPER),
         ("stroke", [(6, 3.5), (15, 3.5), (19, 7.5), (19, 20.5), (6, 20.5)], 1.5, INK, True),
         ("stroke", [(15, 3.5), (15, 7.5), (19, 7.5)], 1.3, INK, False)]
_PAGE_NEXT = _PAGE + [("stroke", [(8.8, 14), (15.6, 14)], 1.8, TEAL, False),
                      ("stroke", [(12.8, 11.2), (15.6, 14), (12.8, 16.8)], 1.8, TEAL, False)]
_PAGE_PREV = _PAGE + [("stroke", [(16.2, 14), (9.4, 14)], 1.8, TEAL, False),
                      ("stroke", [(12.2, 11.2), (9.4, 14), (12.2, 16.8)], 1.8, TEAL, False)]

ICONS: dict[str, list] = {
    "img_ui_nha": [
        ("fill", [(5.5, 10.5), (12, 5), (18.5, 10.5), (18.5, 19.5), (5.5, 19.5)], PAPER),
        ("stroke", [(5.5, 10.5), (5.5, 19.5), (18.5, 19.5), (18.5, 10.5)], 1.6, INK, False),
        ("stroke", [(3, 12), (12, 4.2), (21, 12)], 2.0, INK, False),
        ("fill", [(10.3, 14), (13.7, 14), (13.7, 19.5), (10.3, 19.5)], INK),
    ],
    "img_ui_loa": [
        ("fill", [(4, 9.5), (7.5, 9.5), (12.5, 5), (12.5, 19), (7.5, 14.5), (4, 14.5)], PAPER),
        ("stroke", [(4, 9.5), (7.5, 9.5), (12.5, 5), (12.5, 19), (7.5, 14.5), (4, 14.5)], 1.6, INK, True),
    ] + _outlined(_arc(12.5, 12, 3.6, -50, 50, 12), 1.4) + _outlined(_arc(12.5, 12, 6.8, -55, 55, 16), 1.4),
    "img_ui_tiep": _ARROW,
    "img_ui_lui": _mirror(_ARROW),
    "img_ui_so": [
        ("fill", [(2.5, 6), (12, 7.6), (12, 19.5), (2.5, 18)], PAPER),
        ("fill", [(12, 7.6), (21.5, 6), (21.5, 18), (12, 19.5)], PAPER),
        ("stroke", [(2.5, 6), (12, 7.6), (21.5, 6), (21.5, 18), (12, 19.5), (2.5, 18)], 1.5, INK, True),
        ("stroke", [(12, 7.6), (12, 19.5)], 1.3, INK, False),
        ("circle", 7.3, 12.6, 2.2, PETAL_PINK, 0.9),
        ("stroke", [(15, 11), (19, 10.4)], 0.9, INK, False),
        ("stroke", [(15, 14), (19, 13.4)], 0.9, INK, False),
    ],
    "img_ui_on_lai": _outlined(_arc(12, 12.5, 6.5, 200, 480, 30), 2.4) + [
        ("fill", [(15.6, 3.6), (20.8, 7.4), (14.6, 9.4)], PAPER),
        ("stroke", [(15.6, 3.6), (20.8, 7.4), (14.6, 9.4)], 1.2, INK, True),
    ],
    "img_ui_xong": _outlined([(5.5, 12.5), (10, 17), (18.5, 7.5)], 3.2),
    "img_ui_khoa": [
        ("stroke", _arc(12, 10.5, 4, 180, 360, 16), 2.0, LOCKED_INK, False),
        ("fill", [(6, 10.5), (18, 10.5), (18, 20), (6, 20)], LOCKED_FILL),
        ("stroke", [(6, 10.5), (18, 10.5), (18, 20), (6, 20)], 1.6, LOCKED_INK, True),
        ("circle", 12, 14.8, 1.3, LOCKED_INK, 0),
    ],
    "img_ui_lat_truoc": _PAGE_PREV,
    "img_ui_lat_sau": _PAGE_NEXT,
    "img_ui_sao_giay": [("fill", _star(12, 12.6, 9.5, 4), STAR_YELLOW),
                        ("stroke", _star(12, 12.6, 9.5, 4), 1.4, INK, True)],
    "img_ui_canh_hoa": [("fill", _PETAL, PETAL_PINK), ("stroke", _PETAL, 1.3, INK, True)],
}

FLOWER: list = [
    ("stroke", [(12, 14), (12.4, 18), (12, 23)], 1.3, INK, False),
    ("fill", [(12, 19), (8, 16.2), (4.5, 17.4), (8, 20.2)], LEAF_GREEN),
    ("stroke", [(12, 19), (8, 16.2), (4.5, 17.4), (8, 20.2)], 1.0, INK, True),
    ("fill", [(12, 17.2), (16, 14.6), (19.5, 15.8), (16, 18.4)], LEAF_GREEN),
    ("stroke", [(12, 17.2), (16, 14.6), (19.5, 15.8), (16, 18.4)], 1.0, INK, True),
    ("circle", 12, 8.6, 7, PETAL_PINK, 1.2),
    ("stroke", _arc(12, 8.6, 4.4, 150, 470, 30), 1.0, ROSE_DARK, False),
    ("stroke", _arc(12.4, 8.4, 2.2, 200, 520, 20), 1.0, ROSE_DARK, False),
    ("stroke", _arc(12, 8.6, 5.6, 200, 250, 8), 1.0, PAPER, False),
]


def _dist2_to_segment(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    length2 = dx * dx + dy * dy
    t = 0.0 if length2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / length2))
    qx, qy = ax + t * dx - px, ay + t * dy - py
    return qx * qx + qy * qy


def _inside(points, x, y):
    inside = False
    j = len(points) - 1
    for i, (xi, yi) in enumerate(points):
        xj, yj = points[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def _edge_dist(points, x, y, closed=True):
    segs = zip(points, points[1:] + (points[:1] if closed else []))
    return math.sqrt(min(_dist2_to_segment(x, y, a[0], a[1], b[0], b[1]) for a, b in segs))


def _layers(shape):
    """Tách một nét thành các lớp ``(hit, edge, color, bbox)`` trong toạ độ khung 24×24.

    ``hit(x, y)``: điểm có thuộc nét không; ``edge(x, y)``: khoảng cách tới mép nét, để chỉ lấy mẫu dày
    ở những điểm ảnh nằm sát mép.
    """
    kind = shape[0]
    if kind == "fill":
        _, pts, color = shape
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        return [(lambda x, y: _inside(pts, x, y), lambda x, y: _edge_dist(pts, x, y), color,
                 (min(xs), min(ys), max(xs), max(ys)))]
    if kind == "stroke":
        _, pts, width, color, closed = shape
        half = width / 2
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        return [(lambda x, y: _edge_dist(pts, x, y, closed) <= half,
                 lambda x, y: abs(_edge_dist(pts, x, y, closed) - half), color,
                 (min(xs) - half, min(ys) - half, max(xs) + half, max(ys) + half))]
    if kind == "circle":
        _, cx, cy, r, fill, stroke_width = shape
        layers = []
        if fill is not None:
            layers.append((lambda x, y: math.hypot(x - cx, y - cy) <= r,
                           lambda x, y: abs(math.hypot(x - cx, y - cy) - r), fill,
                           (cx - r, cy - r, cx + r, cy + r)))
        if stroke_width > 0:
            half = stroke_width / 2
            layers.append((lambda x, y: abs(math.hypot(x - cx, y - cy) - r) <= half,
                           lambda x, y: abs(abs(math.hypot(x - cx, y - cy) - r) - half), INK,
                           (cx - r - half, cy - r - half, cx + r + half, cy + r + half)))
        return layers
    raise ValueError(f"nét lạ: {kind!r}")


def render(shapes, size: int) -> bytes:
    """Vẽ các nét lên nền trong suốt cỡ ``size``×``size``, trả về PNG RGBA."""
    scale = VIEW / size
    near = 0.75 * scale  # điểm ảnh có tâm xa mép hơn mức này thì phủ kín hoặc trống hẳn
    canvas = [[0.0, 0.0, 0.0, 0.0] for _ in range(size * size)]  # màu đã nhân alpha
    offsets = [((sx + 0.5) / SAMPLES, (sy + 0.5) / SAMPLES) for sy in range(SAMPLES) for sx in range(SAMPLES)]
    for shape in shapes:
        for hit, edge, color, (x0, y0, x1, y1) in _layers(shape):
            px0, py0 = max(0, int(x0 / scale) - 1), max(0, int(y0 / scale) - 1)
            px1, py1 = min(size, int(x1 / scale) + 2), min(size, int(y1 / scale) + 2)
            for py in range(py0, py1):
                for px in range(px0, px1):
                    cx, cy = (px + .5) * scale, (py + .5) * scale
                    if edge(cx, cy) > near:
                        a = 1.0 if hit(cx, cy) else 0.0
                    else:
                        a = sum(1 for ox, oy in offsets if hit((px + ox) * scale, (py + oy) * scale)) / len(offsets)
                    if a <= 0:
                        continue
                    cell = canvas[py * size + px]
                    for k in range(3):
                        cell[k] = color[k] / 255 * a + cell[k] * (1 - a)
                    cell[3] = a + cell[3] * (1 - a)
    raw = bytearray()
    for y in range(size):
        raw.append(0)
        for x in range(size):
            r, g, b, a = canvas[y * size + x]
            raw += bytes((0, 0, 0, 0)) if a <= 0 else bytes(
                (round(r / a * 255), round(g / a * 255), round(b / a * 255), round(a * 255)))
    return _png(size, size, bytes(raw))


def _png(width: int, height: int, raw: bytes) -> bytes:
    def chunk(kind: bytes, body: bytes) -> bytes:
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))
    header = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def write_all(image_dir: Path, force: bool = False) -> list[str]:
    """Ghi các hình mặc định còn thiếu vào ``image_dir``, trả về các mã đã ghi.

    ``force`` vẽ lại mọi biểu tượng; hoa và gà con thì không bao giờ ghi đè, vì đó là chỗ
    tranh chính thức sẽ thay vào.
    """
    image_dir = Path(image_dir)
    written = []
    for icon_id, shapes in ICONS.items():
        path = image_dir / f"{icon_id}.png"
        if force or not path.exists():
            path.write_bytes(render(shapes, ICON_SIZE))
            written.append(icon_id)
    flower = image_dir / f"{FLOWER_ID}.png"
    if not flower.exists():
        flower.write_bytes(render(FLOWER, FLOWER_SIZE))
        written.append(FLOWER_ID)
    mascot, source = image_dir / f"{MASCOT_ID}.png", image_dir / f"{MASCOT_SOURCE_ID}.png"
    if not mascot.exists() and source.exists():
        shutil.copyfile(source, mascot)
        written.append(MASCOT_ID)
    return written
