"""Chỗ gọi bộ đọc thay được; chỉ nạp edge-tts khi thật sự cần tạo âm thanh."""

import asyncio
from dataclasses import dataclass

from .tts_settings import TtsParams


@dataclass(frozen=True)
class SynthResult:
    audio: bytes
    speech_start: float | None
    speech_end: float | None


class TtsError(Exception):
    """Bộ đọc không tạo được âm thanh dùng được."""


class TtsUnavailable(TtsError):
    def __init__(self):
        super().__init__("Chưa có edge-tts. Cài bằng: python -m pip install -r tools/requirements-tts.txt")


class EdgeEngine:
    def __init__(self):
        try:
            import edge_tts
        except ImportError as e:
            raise TtsUnavailable() from e
        self._edge_tts = edge_tts

    def synthesize(self, p: TtsParams) -> SynthResult:
        return asyncio.run(self._synthesize(p))

    async def _synthesize(self, p):
        for attempt in range(4):
            try:
                c = self._edge_tts.Communicate(
                    p.doc, p.voice, rate=f"{p.rate:+d}%", pitch=f"{p.pitch:+d}Hz",
                    volume=f"{p.volume:+d}%", boundary="WordBoundary")
                audio = bytearray()
                starts, ends = [], []
                async for ch in c.stream():
                    if ch["type"] == "audio":
                        audio.extend(ch["data"])
                    elif ch["type"] == "WordBoundary":
                        starts.append(ch["offset"] / 10_000_000)
                        ends.append((ch["offset"] + ch["duration"]) / 10_000_000)
                if not audio:
                    raise TtsError("Dịch vụ không trả âm thanh")
                return SynthResult(bytes(audio), min(starts) if starts else None,
                                   max(ends) if ends else None)
            except (ValueError, TypeError) as e:
                # Sai giọng hay thông số: thử lại cũng hỏng y như cũ.
                raise TtsError(f"Thông số đọc không hợp lệ: {e}") from e
            except Exception as e:
                if attempt == 3:
                    raise TtsError(f"Không tạo được âm thanh sau 4 lần thử: {e}") from e
                await asyncio.sleep(2 ** attempt)
