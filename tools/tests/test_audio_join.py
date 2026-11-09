import math
import unittest

from tapdoc import audio_join as aj

SR = aj.SR


def tone_burst(seconds, amp=8000, freq=220.0):
    n = int(seconds * SR)
    return [int(amp * math.sin(2 * math.pi * freq * i / SR)) for i in range(n)]


def silence(seconds):
    return [0] * int(seconds * SR)


class TrimSilenceTest(unittest.TestCase):
    def test_cuts_leading_and_trailing_silence_with_small_margin(self):
        speech = tone_burst(0.3)
        out = aj.trim_silence(silence(0.2) + speech + silence(0.4))
        self.assertLessEqual(abs(len(out) - len(speech)), int(2 * aj.MARGIN * SR) + int(0.02 * SR))
        self.assertGreaterEqual(len(out), len(speech))

    def test_keeps_soft_onset_above_threshold(self):
        # Phụ âm đầu nhỏ (khoảng -30 dB so với nguyên âm) không được bị cắt mất.
        soft, loud = tone_burst(0.08, amp=250), tone_burst(0.3, amp=8000)
        out = aj.trim_silence(silence(0.2) + soft + loud + silence(0.2))
        self.assertGreaterEqual(len(out), len(soft) + len(loud))

    def test_all_silence_returns_empty(self):
        self.assertEqual(aj.trim_silence(silence(0.3)), [])


class LoudnessTest(unittest.TestCase):
    def test_parts_match_the_median_rms(self):
        a, b, c = tone_burst(0.2, 2000), tone_burst(0.2, 8000), tone_burst(0.2, 4000)
        out = aj.match_loudness([a, b, c])
        levels = [aj.rms(x) for x in out]
        for level in levels:
            self.assertAlmostEqual(level / aj.rms(c), 1.0, delta=0.02)

    def test_never_clips(self):
        out = aj.match_loudness([tone_burst(0.2, 30000), tone_burst(0.2, 300)])
        self.assertTrue(all(-32768 <= v <= 32767 for part in out for v in part))


class AssembleTest(unittest.TestCase):
    def test_gaps_lead_and_tail(self):
        a, b, c = tone_burst(0.1), tone_burst(0.2), tone_burst(0.1)
        out = aj.assemble([a, b, c], [0.08, 0.25])
        expect = (int(aj.LEAD * SR) + len(a) + int(0.08 * SR) + len(b) + int(0.25 * SR) + len(c)
                  + int(aj.TAIL * SR))
        self.assertEqual(len(out), expect)
        self.assertEqual(out[:int(aj.LEAD * SR)], [0] * int(aj.LEAD * SR))

    def test_gap_count_must_match(self):
        with self.assertRaises(ValueError):
            aj.assemble([tone_burst(0.1), tone_burst(0.1)], [])


class PlanTest(unittest.TestCase):
    def test_commas_become_long_gaps(self):
        ids, gaps = aj.plan(["tieng_bes", "tieng_bas", ",", "tieng_baf"], 0.08)
        self.assertEqual(ids, ["tieng_bes", "tieng_bas", "tieng_baf"])
        self.assertEqual(gaps, [0.08, aj.COMMA_GAP])


class JoinFilesTest(unittest.TestCase):
    def test_decodes_processes_and_encodes_in_order(self):
        parts = {"a.mp3": silence(0.1) + tone_burst(0.2, 2000) + silence(0.1),
                 "b.mp3": silence(0.1) + tone_burst(0.3, 8000) + silence(0.2)}
        seen = {}

        def decoder(paths):
            seen["paths"] = list(paths)
            return SR, {p: parts[p] for p in paths}

        def encoder(samples, sr):
            seen["samples"], seen["sr"] = samples, sr
            return b"ID3fake"

        out = aj.join_files(["a.mp3", "b.mp3"], [0.08], decoder=decoder, encoder=encoder)
        self.assertEqual(out, b"ID3fake")
        self.assertEqual(seen["paths"], ["a.mp3", "b.mp3"])
        self.assertEqual(seen["sr"], SR)
        total = len(seen["samples"]) / SR
        # 0.05 lead + ~0.2 + 0.08 + ~0.3 + 0.12 tail, cộng lề cắt lặng
        self.assertAlmostEqual(total, 0.75, delta=0.15)

    def test_part_that_cannot_be_decoded_raises(self):
        with self.assertRaises(aj.JoinError):
            aj.join_files(["a.mp3", "b.mp3"], [0.08], decoder=lambda paths: (SR, {"a.mp3": tone_burst(0.2)}),
                          encoder=lambda s, sr: b"ID3")

    def test_silent_part_raises(self):
        with self.assertRaises(aj.JoinError):
            aj.join_files(["a.mp3", "b.mp3"], [0.08],
                          decoder=lambda paths: (SR, {"a.mp3": tone_burst(0.2), "b.mp3": silence(0.3)}),
                          encoder=lambda s, sr: b"ID3")


if __name__ == "__main__":
    unittest.main()
