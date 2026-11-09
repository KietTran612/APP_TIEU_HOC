"""Đo cao độ thanh hỏi/ngã (thiết kế TV2 tập một, mục 9): YIN thuần Python, so với mẫu thanh điệu."""

import io
import json
import math
import os
import subprocess
from unittest import mock
import struct
import tempfile
import unittest
import wave
from pathlib import Path

from tapdoc import pitch_check as pc

N = pc.POINTS
FLAT = [0.0] * N
TEMPLATES = {
    "ngang": FLAT,
    "huyen": [-0.6 * i for i in range(N)],                                # đi xuống đều
    "sac": [0.7 * i for i in range(N)],                                   # đi lên đều
    "nang": [0.0] * (N - 3) + [-2.0, -4.0, -6.0],                         # rơi gắt ở cuối
    "hoi": [0.0, -1.0, -2.0, -3.0, -3.5, -3.0, -1.5, 0.0, 1.5, 2.5],      # võng xuống rồi lên
}


def write_tone(path: Path, freqs, sr=16000, seconds_each=0.05):
    """WAV 16 kHz mono: mỗi tần số kéo dài `seconds_each` giây (dựng đường cao độ giả)."""
    samples, phase = [], 0.0
    for f in freqs:
        for _ in range(int(sr * seconds_each)):
            phase += 2 * math.pi * f / sr
            samples.append(int(8000 * math.sin(phase)))
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(struct.pack("<%dh" % len(samples), *samples))


class ToneOfTest(unittest.TestCase):
    def test_tone_of(self):
        self.assertEqual(pc.tone_of("cử"), "hoi")
        self.assertEqual(pc.tone_of("ngã"), "nga")
        self.assertEqual(pc.tone_of("bé"), "sac")
        self.assertEqual(pc.tone_of("em"), "ngang")


class TrackTest(unittest.TestCase):
    def test_sine_frequency_measured(self):
        with tempfile.TemporaryDirectory() as tmp:
            wav = Path(tmp) / "a.wav"
            write_tone(wav, [220.0] * 6)
            values = pc.contour(wav)
        self.assertGreater(len(values), 10)
        self.assertTrue(all(abs(v) < 0.5 for v in values), values[:5])  # 220 Hz = 0 bán âm

    def test_window_limits_frames(self):
        with tempfile.TemporaryDirectory() as tmp:
            wav = Path(tmp) / "a.wav"
            write_tone(wav, [220.0] * 3 + [330.0] * 3)
            late = pc.contour(wav, start=0.18, end=0.28)
        self.assertTrue(late)
        self.assertTrue(all(v > 5 for v in late), late)  # 330 Hz ≈ +7 bán âm


class JudgeTest(unittest.TestCase):
    def test_pitch_rising_tail_passes(self):
        dip_rise = [0.0, -1.2, -2.0, -3.2, -3.4, -2.8, -1.6, 0.2, 1.4, 2.6]
        self.assertTrue(pc.judge(dip_rise, "hoi", TEMPLATES))
        self.assertTrue(pc.judge(dip_rise, "nga", TEMPLATES))  # giọng này đọc ngã như hỏi

    def test_pitch_falling_fails(self):
        falling = [-0.6 * i for i in range(N)]
        self.assertFalse(pc.judge(falling, "hoi", TEMPLATES))
        self.assertFalse(pc.judge(falling, "nga", TEMPLATES))

    def test_too_few_points_fails(self):
        self.assertFalse(pc.judge([0.0, 1.0], "hoi", TEMPLATES))

    def test_resample_length(self):
        self.assertEqual(len(pc.resample(list(range(37)))), N)

    def test_templates_merge_hoi_into_nga(self):
        built = pc.build_templates({"hoi": [[1.0] * N], "nga": [[3.0] * N], "sac": [[0.0] * N]})
        self.assertEqual(built["nga"], [2.0] * N)
        self.assertEqual(built["hoi"], [1.0] * N)


class CheckRowTest(unittest.TestCase):
    def test_words_to_check_only_hoi_nga(self):
        self.assertEqual(pc.words_to_check("Mùa hè cũng nghỉ."), [(2, "cũng", "nga"), (3, "nghỉ", "hoi")])

    def test_multiword_without_marks_unchecked(self):
        result = pc.check_row({"id": "tu_x", "text": "cũng nghỉ"}, wav=None, marks=None, templates=TEMPLATES)
        self.assertEqual([r["ok"] for r in result], [None, None])



class RobustnessTest(unittest.TestCase):
    """Review cuối: lệnh pitch không được sập, không đo bằng mốc cũ."""

    def test_decode_without_powershell_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            mp3 = Path(tmp) / "tieng_cuwr.mp3"
            mp3.write_bytes(b"x")
            with mock.patch("tapdoc.pitch_check.subprocess.run", side_effect=FileNotFoundError("powershell")):
                self.assertEqual(pc.decode([mp3], Path(tmp) / "cache"), {})
            with mock.patch("tapdoc.pitch_check.subprocess.run",
                            side_effect=subprocess.TimeoutExpired("powershell", 1)):
                self.assertEqual(pc.decode([mp3], Path(tmp) / "cache"), {})

    def test_undecoded_reason(self):
        result = pc.check_row({"id": "tieng_cuwr", "text": "cử"}, wav=None, marks=None, templates=TEMPLATES)
        self.assertEqual((result[0]["ok"], result[0]["why"]), (None, "không giải mã được âm thanh"))

    def test_stale_marks_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            audio, marks = Path(tmp) / "audio", Path(tmp) / "marks"
            audio.mkdir()
            marks.mkdir()
            (marks / "tu_x.json").write_text(json.dumps({"text": "cũng nghỉ", "words": [[0, 0.1], [0.1, 0.2]]}))
            mp3 = audio / "tu_x.mp3"
            mp3.write_bytes(b"x")
            old = mp3.stat().st_mtime - 100
            os.utime(marks / "tu_x.json", (old, old))
            wav = Path(tmp) / "a.wav"
            write_tone(wav, [220.0] * 6)
            with mock.patch("tapdoc.pitch_check.decode", return_value={mp3: wav}):
                rows = pc.check_rows([{"id": "tu_x", "text": "cũng nghỉ"}], audio, marks, Path(tmp), TEMPLATES)
        self.assertEqual([r["ok"] for r in rows], [None, None])

    def test_cli_without_templates_exits_2(self):
        from tapdoc import __main__ as cli
        out = io.StringIO()
        with mock.patch("tapdoc.pitch_check.reference_templates", return_value={}),                 mock.patch.object(cli, "load_rows", return_value=[]),                 mock.patch("sys.stdout", out):
            code = cli.main(["pitch"])
        self.assertEqual(code, 2)
        self.assertIn("mẫu", out.getvalue())


if __name__ == "__main__":
    unittest.main()
