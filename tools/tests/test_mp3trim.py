import math
import unittest

from tapdoc.mp3trim import trim_mp3
from tests.tts_fakes import fake_mp3


class TrimTest(unittest.TestCase):
    def test_trims_to_speech_plus_pad(self):
        data = fake_mp3(1.2)
        trimmed, ok = trim_mp3(data, 0.5, 0.7)
        self.assertTrue(ok)
        self.assertEqual(trimmed, data[(math.floor(0.4 / 0.024) - 1) * 144:
                                      math.ceil(0.8 / 0.024) * 144])

    def test_not_mp3_returned_unchanged(self):
        for data in (b"", b"broken", fake_mp3(1.2)[:-1]):
            self.assertEqual(trim_mp3(data, 0.5, 0.7), (data, False))

    def test_id3_header_skipped(self):
        data = fake_mp3(1.2)
        tagged = b"ID3\x04\x00\x00\x00\x00\x00\x03abc" + data
        self.assertEqual(trim_mp3(tagged, 0.5, 0.7), trim_mp3(data, 0.5, 0.7))

    def test_pad_clamped_at_edges(self):
        data = fake_mp3(1.2)
        self.assertEqual(trim_mp3(data, 0, 1.2)[0], data)

    def test_invalid_boundaries_keep_original(self):
        data = fake_mp3(1.2)
        for start, end in ((None, None), (0.8, 0.2), (float("nan"), 1), (2, 3)):
            self.assertEqual(trim_mp3(data, start, end), (data, False))

    def test_mpeg_versions_and_padding(self):
        for header, length in ((b"\xff\xfb\x90\x00", 417),
                               (b"\xff\xfb\x92\x00", 418),
                               (b"\xff\xe3\x64\x00", 288)):
            data = (header + bytes(length - 4)) * 100
            result, ok = trim_mp3(data, 0.5, 0.7)
            self.assertTrue(ok)
            self.assertLess(len(result), len(data))
            self.assertEqual(len(result) % length, 0)
