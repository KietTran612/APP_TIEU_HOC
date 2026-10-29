"""Cắt khoảng lặng theo mốc lời đọc, giữ nguyên dữ liệu nén của các khung MP3."""

import math

_BITRATES_1 = (0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320)
_BITRATES_2 = (0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160)


def _frames(data):
    """Đọc toàn bộ khung; không đoán lại vị trí khi gặp dữ liệu hỏng."""
    pos = 0
    if data.startswith(b"ID3"):
        if len(data) < 10 or any(b & 0x80 for b in data[6:10]):
            raise ValueError("Thẻ ID3 không hợp lệ")
        size = 0
        for byte in data[6:10]:
            size = (size << 7) | byte
        pos = 10 + size
        if data[3] == 4 and data[5] & 0x10:
            pos += 10  # chân thẻ ID3v2.4
    frames = []
    elapsed = 0.0
    while pos < len(data):
        if len(data) - pos == 128 and data[pos:pos + 3] == b"TAG":
            break  # thẻ ID3v1 ở cuối không phải khung âm thanh
        if pos + 4 > len(data):
            raise ValueError("Khung MP3 bị cụt")
        h = int.from_bytes(data[pos:pos + 4], "big")
        version, layer = (h >> 19) & 3, (h >> 17) & 3
        bitrate_index, sample_index = (h >> 12) & 15, (h >> 10) & 3
        if (h >> 21 != 0x7ff or version == 1 or layer != 1
                or bitrate_index in (0, 15) or sample_index == 3):
            raise ValueError("Đầu khung MP3 không hợp lệ")
        divisor = {3: 1, 2: 2, 0: 4}[version]
        sample_rate = (44100, 48000, 32000)[sample_index] // divisor
        bitrate = (_BITRATES_1 if version == 3 else _BITRATES_2)[bitrate_index] * 1000
        length = (144 if version == 3 else 72) * bitrate // sample_rate + ((h >> 9) & 1)
        if pos + length > len(data):
            raise ValueError("Khung MP3 thiếu dữ liệu")
        duration = (1152 if version == 3 else 576) / sample_rate
        frames.append((pos, pos + length, elapsed, elapsed + duration))
        elapsed += duration
        pos += length
    if not frames:
        raise ValueError("Không có khung MP3")
    return frames


def trim_mp3(data: bytes, speech_start: float, speech_end: float,
             pad: float = 0.1) -> tuple[bytes, bool]:
    """Giữ các khung giao vùng lời đọc và một khung trước đó cho bit reservoir.

    Mốc không hợp lệ hoặc file không đọc được thì giữ nguyên và trả cờ False.
    """
    try:
        if (not all(math.isfinite(v) for v in (speech_start, speech_end, pad))
                or speech_start < 0 or speech_end <= speech_start or pad < 0):
            return data, False
        frames = _frames(data)
        if speech_start >= frames[-1][3]:
            return data, False
        start, end = max(0, speech_start - pad), min(frames[-1][3], speech_end + pad)
        kept = [i for i, (_, _, a, b) in enumerate(frames) if b > start and a < end]
        if not kept:
            return data, False
        first, last = max(0, kept[0] - 1), kept[-1]
        return data[frames[first][0]:frames[last][1]], True
    except (ValueError, TypeError, OverflowError):
        return data, False
