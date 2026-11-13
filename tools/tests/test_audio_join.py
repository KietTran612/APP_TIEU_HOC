import math
import unittest
from pathlib import Path

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


def frame_levels(samples, sr=SR):
    step = int(0.01 * sr)
    return [aj.rms(samples[i:i + step]) for i in range(0, len(samples) - step + 1, step)]


def loud_seconds(samples, ratio=0.5, sr=SR):
    levels = frame_levels(samples, sr)
    peak = max(levels)
    return sum(1 for v in levels if v > ratio * peak) * 0.01


class KeepFirstPcmTest(unittest.TestCase):
    """keep_first trên PCM (soát 13/11): giữ trọn tiếng đầu, kết thúc bằng giảm dần và lặng, không còn "tách"."""

    def assert_soft_tail(self, out):
        levels = frame_levels(out)
        peak = max(levels)
        self.assertTrue(all(v < 0.1 * peak for v in levels[-3:]), [round(v / peak, 2) for v in levels[-3:]])
        self.assertTrue(all(v == 0 for v in out[-int(aj.KEEP_TAIL * SR):]))

    def test_pause_after_keeps_whole_first_word_even_if_marks_are_wrong(self):
        # "ẹ. ẹ.": bộ đọc báo tiếng thứ hai bắt đầu ở 0,38 giây nhưng tiếng đầu thật kéo dài tới 0,63 giây.
        first, second = tone_burst(0.4), tone_burst(0.35)
        samples = silence(0.23) + first + silence(0.8) + second + silence(0.5)
        out, _ = aj.keep_first_pcm(samples, SR, word_start=0.17, next_word=(0.383, 0.767), pause=True)
        self.assertGreaterEqual(loud_seconds(out), 0.4 - aj.FADE)
        self.assertLessEqual(loud_seconds(out), 0.41)  # không lấy tiếng thứ hai
        self.assert_soft_tail(out)

    def test_read_on_stops_before_next_word_with_fade(self):
        # "nụ hoa.": đọc liền, không có chỗ lặng; PCM giải mã trễ hơn mốc bộ đọc 0,07 giây.
        samples = silence(0.22) + tone_burst(0.8) + silence(0.4)
        out, _ = aj.keep_first_pcm(samples, SR, word_start=0.15, next_word=(0.517, 1.033), pause=False)
        kept = loud_seconds(out, ratio=0.05)
        self.assertLessEqual(kept, 0.517 + 0.07 - 0.22)  # không lấn sang tiếng sau
        self.assertGreaterEqual(kept, 0.25)
        self.assert_soft_tail(out)

    def test_pause_without_gap_falls_back_to_next_word(self):
        # Có dấu câu nhưng bộ đọc không nghỉ: khoảng lặng đầu tiên nằm sau cả tiếng kế tiếp thì không dùng.
        samples = silence(0.2) + tone_burst(1.0) + silence(0.3)
        out, _ = aj.keep_first_pcm(samples, SR, word_start=0.2, next_word=(0.6, 1.0), pause=True)
        self.assertLessEqual(loud_seconds(out, ratio=0.05), 0.41)
        self.assert_soft_tail(out)

    def test_single_word_without_next_keeps_until_silence(self):
        samples = silence(0.2) + tone_burst(0.3) + silence(0.6)
        out, _ = aj.keep_first_pcm(samples, SR, word_start=0.2, next_word=None, pause=False)
        self.assertAlmostEqual(loud_seconds(out), 0.3, delta=0.06)
        self.assert_soft_tail(out)

    def test_offset_maps_marks_into_new_audio(self):
        samples = silence(0.23) + tone_burst(0.4) + silence(0.8) + tone_burst(0.35) + silence(0.5)
        out, offset = aj.keep_first_pcm(samples, SR, word_start=0.17, next_word=(0.383, 0.767), pause=True)
        onset = next(i for i, v in enumerate(out) if abs(v) > 100) / SR
        self.assertAlmostEqual(0.17 - offset, onset, delta=0.03)

    def test_silence_raises(self):
        with self.assertRaises(aj.JoinError):
            aj.keep_first_pcm(silence(1.0), SR, word_start=0.2, next_word=None, pause=True)


class EncodeTest(unittest.TestCase):
    def test_pads_silence_the_encoder_drops_at_the_end(self):
        # Media Foundation bỏ mất khoảng 0,1 giây cuối khi mã hoá (đo 13/11): đệm lặng để chỉ mất phần lặng.
        import wave
        from unittest import mock
        seen = {}

        def fake_run(script, folder, wav, mp3):
            with wave.open(str(wav), "rb") as w:
                seen["frames"] = w.getnframes()
            Path(mp3).write_bytes(b"ID3ok")

        samples = tone_burst(0.3)
        with mock.patch.object(aj, "_run_ps", side_effect=fake_run):
            self.assertEqual(aj.encode_mp3(samples, SR), b"ID3ok")
        self.assertEqual(seen["frames"], len(samples) + int(aj.ENCODER_FLUSH * SR))
        self.assertGreaterEqual(aj.ENCODER_FLUSH, 0.15)


if __name__ == "__main__":
    unittest.main()
