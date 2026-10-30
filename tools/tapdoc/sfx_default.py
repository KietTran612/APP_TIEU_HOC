"""Tiếng động mặc định tự tạo (chỉ thư viện chuẩn), dùng tạm cho tới khi có file CC0 chính thức cùng mã.

Mỗi tiếng là một công thức ngắn: sóng sin có đường bao tắt dần, hoặc tiếng ồn đã lọc. Âm lượng đỉnh 0,8 để
không rè; hai đầu tắt hẳn để không có tiếng lách cách. Kết quả ổn định (cùng hạt giống ngẫu nhiên).
File ghi ra `Resources/sfx/<mã>.wav`; mã đã có file (bất kỳ định dạng) thì không đụng tới.
"""

import math
import random
import struct
import wave
from pathlib import Path

from .system_assets import SYSTEM_SFX

RATE = 22050
PEAK = 0.8
SFX_EXTENSIONS = (".ogg", ".wav", ".mp3")


def _env_decay(n: int, tau: float, attack: float = 0.004) -> list[float]:
    """Đường bao lên nhanh rồi tắt dần theo hàm mũ, về đúng 0 ở mẫu cuối."""
    a = max(1, int(attack * RATE))
    out = []
    for i in range(n):
        t = i / RATE
        rise = min(1.0, i / a)
        fade = 1.0 - i / (n - 1) if n > 1 else 0.0  # ép về 0 ở cuối
        out.append(rise * math.exp(-t / tau) * fade)
    return out


def _bell(n: int) -> list[float]:
    """Đường bao hình chuông (sin), 0 ở hai đầu."""
    return [math.sin(math.pi * i / (n - 1)) ** 2 for i in range(n)]


def _noise(n: int, seed: int, smooth: int) -> list[float]:
    """Tiếng ồn trắng làm mềm bằng trung bình trượt `smooth` mẫu (lọc thông thấp đơn giản)."""
    rng = random.Random(seed)
    raw = [rng.uniform(-1, 1) for _ in range(n + smooth)]
    acc, out = sum(raw[:smooth]), []
    for i in range(n):
        out.append(acc / smooth)
        acc += raw[i + smooth] - raw[i]
    return out


def _normalize(samples: list[float]) -> list[float]:
    peak = max(abs(s) for s in samples) or 1.0
    return [s / peak * PEAK for s in samples]


def _tap() -> list[float]:
    n = int(0.035 * RATE)
    env = _env_decay(n, 0.008, attack=0.001)
    noise = _noise(n, 1, 2)
    return [e * (0.6 * math.sin(2 * math.pi * 1900 * i / RATE) + 0.4 * noise[i]) for i, e in enumerate(env)]


def _ting() -> list[float]:
    # Hai nốt ngân (Đô 6 rồi Sol 6), mỗi nốt có hoạ âm bậc 2 nhẹ.
    n = int(0.42 * RATE)
    out = [0.0] * n
    for start, freq in ((0.0, 1046.5), (0.09, 1568.0)):
        s0 = int(start * RATE)
        env = _env_decay(n - s0, 0.11, attack=0.003)
        for i, e in enumerate(env):
            t = i / RATE
            out[s0 + i] += e * (math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(4 * math.pi * freq * t))
    return out


def _pop() -> list[float]:
    n = int(0.09 * RATE)
    env = _env_decay(n, 0.025, attack=0.002)
    out, phase = [], 0.0
    for i, e in enumerate(env):
        freq = 620 - 420 * i / n  # trượt từ cao xuống thấp
        phase += 2 * math.pi * freq / RATE
        out.append(e * math.sin(phase))
    return out


def _whoosh() -> list[float]:
    n = int(0.38 * RATE)
    env = _bell(n)
    noise = _noise(n, 2, 6)
    return [e * s for e, s in zip(env, noise)]


def _thud() -> list[float]:
    n = int(0.16 * RATE)
    env = _env_decay(n, 0.035, attack=0.001)
    noise = _noise(n, 3, 10)
    return [e * (0.75 * math.sin(2 * math.pi * 105 * i / RATE) + 0.5 * noise[i]) for i, e in enumerate(env)]


def _paper() -> list[float]:
    # Hai lần sột giấy: tiếng ồn cao (hiệu hai mẫu liền nhau) với hai nhịp đường bao.
    n = int(0.28 * RATE)
    noise = _noise(n + 1, 4, 2)
    hiss = [noise[i + 1] - noise[i] for i in range(n)]
    half = n // 2
    env = _bell(half) + [0.6 * e for e in _bell(n - half)]
    return [e * s for e, s in zip(env, hiss)]


RECIPES = {
    "sfx_cham": _tap,
    "sfx_dung": _ting,
    "sfx_nhap": _pop,
    "sfx_hoa_bay": _whoosh,
    "sfx_dong_dau": _thud,
    "sfx_lat_trang": _paper,
}


def synth(sfx_id: str) -> list[float]:
    """Các mẫu (-1..1) của tiếng mặc định `sfx_id`, đã chuẩn hoá về đỉnh `PEAK`."""
    return _normalize(RECIPES[sfx_id]())


def _write_wav(path: Path, samples: list[float]) -> None:
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", round(max(-1.0, min(1.0, s)) * 32767)) for s in samples))


def write_missing(sfx_dir: Path) -> list[str]:
    """Ghi `<mã>.wav` cho mỗi mã trong `SYSTEM_SFX` chưa có file nào (ogg/wav/mp3); trả về các mã đã ghi."""
    sfx_dir = Path(sfx_dir)
    sfx_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for sfx_id in SYSTEM_SFX:
        if any((sfx_dir / f"{sfx_id}{ext}").exists() for ext in SFX_EXTENSIONS):
            continue
        _write_wav(sfx_dir / f"{sfx_id}.wav", synth(sfx_id))
        written.append(sfx_id)
    return written
