import tempfile
import unittest
import wave
from pathlib import Path

from tapdoc import sfx_default
from tapdoc.system_assets import SYSTEM_SFX


def read_wav(path: Path) -> tuple[int, list[int]]:
    with wave.open(str(path), "rb") as w:
        assert (w.getnchannels(), w.getsampwidth()) == (1, 2), "mono 16 bit"
        raw = w.readframes(w.getnframes())
        rate = w.getframerate()
    samples = [int.from_bytes(raw[i:i + 2], "little", signed=True) for i in range(0, len(raw), 2)]
    return rate, samples


class SynthTest(unittest.TestCase):
    def test_every_sfx_has_a_recipe(self):
        self.assertEqual(set(sfx_default.RECIPES), set(SYSTEM_SFX))

    def test_short_audible_not_clipping(self):
        for sfx_id in sfx_default.RECIPES:
            samples = sfx_default.synth(sfx_id)
            seconds = len(samples) / sfx_default.RATE
            self.assertGreater(seconds, 0.02, sfx_id)
            self.assertLess(seconds, 0.8, sfx_id)  # tiếng động ngắn, không bắt bé chờ
            peak = max(abs(s) for s in samples)
            self.assertGreater(peak, 0.2, sfx_id)
            self.assertLessEqual(peak, 0.9, sfx_id)

    def test_starts_and_ends_quiet(self):
        """Không có tiếng lách cách ở hai đầu: mẫu đầu và cuối gần 0."""
        for sfx_id in sfx_default.RECIPES:
            samples = sfx_default.synth(sfx_id)
            self.assertLess(abs(samples[0]), 0.05, sfx_id)
            self.assertLess(abs(samples[-1]), 0.05, sfx_id)

    def test_deterministic(self):
        for sfx_id in sfx_default.RECIPES:
            self.assertEqual(sfx_default.synth(sfx_id), sfx_default.synth(sfx_id), sfx_id)


class WriteMissingTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name) / "sfx"

    def tearDown(self):
        self._tmp.cleanup()

    def test_writes_wav_for_each_missing_id(self):
        written = sfx_default.write_missing(self.dir)
        self.assertEqual(set(written), set(SYSTEM_SFX))
        for sfx_id in SYSTEM_SFX:
            rate, samples = read_wav(self.dir / f"{sfx_id}.wav")
            self.assertEqual(rate, sfx_default.RATE)
            self.assertGreater(len(samples), 0)

    def test_never_overwrites_existing_file_of_any_format(self):
        self.dir.mkdir(parents=True)
        (self.dir / "sfx_dung.ogg").write_bytes(b"real")
        (self.dir / "sfx_cham.wav").write_bytes(b"real")
        written = sfx_default.write_missing(self.dir)
        self.assertNotIn("sfx_dung", written)
        self.assertNotIn("sfx_cham", written)
        self.assertFalse((self.dir / "sfx_dung.wav").exists(), "Đã có file thật thì không thêm bản mặc định")
        self.assertEqual((self.dir / "sfx_cham.wav").read_bytes(), b"real")


if __name__ == "__main__":
    unittest.main()
