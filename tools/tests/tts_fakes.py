"""Bộ đọc và khung MP3 giả, không dùng mạng hay gói ngoài."""

import math

from tapdoc.tts_engine import SynthResult, TtsError


def fake_mp3(seconds: float) -> bytes:
    return (b"\xff\xf3\x64\xc0" + bytes(140)) * math.ceil(seconds / 0.024)


class FakeEngine:
    def __init__(self, *, failures=(), rows=(), audio=None, speech_start=0.5, speech_end=0.7):
        self.calls = []
        self.failures = set(failures)
        self.ids_by_doc = {r["text"]: r["id"] for r in rows}
        self.audio = fake_mp3(1.2) if audio is None else audio
        self.speech_start = speech_start
        self.speech_end = speech_end

    def synthesize(self, p):
        self.calls.append(p)
        if p.doc in self.failures or self.ids_by_doc.get(p.doc) in self.failures:
            raise TtsError(f"không đọc được {p.doc}")
        return SynthResult(self.audio, self.speech_start, self.speech_end)
