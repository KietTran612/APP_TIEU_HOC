import copy
import tempfile
import unittest
from dataclasses import asdict
from pathlib import Path
from unittest import mock

from tapdoc.tts_settings import (
    differs_from_settings, effective_params, load_settings, needs_regen,
    save_settings, set_override, signature,
)

SETTINGS = Path(__file__).resolve().parents[2] / "content/tts/settings.json"


def settings():
    return load_settings(SETTINGS)


def row(audio_id="am_b", text="bờ", kind="am", status="cho_duyet"):
    return {"id": audio_id, "text": text, "kind": kind, "status": status,
            "source": "cu", "bai": ["tv1_t1_b01"], "file": f"audio/{audio_id}.mp3"}


class ParamsTest(unittest.TestCase):
    def test_defaults_by_kind(self):
        s = settings()
        for kind, rate in (("am", -30), ("van", -30), ("dau", -30), ("tieng", -25),
                           ("tu", -15), ("cau", -15), ("huong_dan", -15), ("khen", -15)):
            with self.subTest(kind=kind):
                p = effective_params(s, row(kind=kind))
                self.assertEqual((p.doc, p.rate, p.pitch, p.volume, p.voice),
                                 ("bờ", rate, 0, 0, "vi-VN-HoaiMyNeural"))

    def test_override_wins_and_only_diff_is_stored(self):
        s, r = settings(), row()
        set_override(s, r, doc="bo\u031b\u0300", rate=-40, pitch=0, volume=0)
        self.assertEqual(s["overrides"], {"am_b": {"rate": -40}})
        set_override(s, r, doc="cu", pitch=10)
        self.assertEqual(s["overrides"]["am_b"], {"doc": "cu", "rate": -40, "pitch": 10})
        self.assertEqual(effective_params(s, r).doc, "cu")
        self.assertEqual(effective_params(s, r).rate, -40)
        set_override(s, r, doc="", rate=-30, pitch=0)
        self.assertNotIn("am_b", s["overrides"])

    def test_limits_raise(self):
        for key, values in (("rate", (-61, 31, True, 1.5)), ("pitch", (-31, 31)),
                            ("volume", (-51, 51))):
            for value in values:
                s = settings()
                before = copy.deepcopy(s)
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    set_override(s, row(), **{key: value})
                self.assertEqual(s, before)

    def test_save_roundtrip_and_atomic_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "settings.json"
            s = settings()
            save_settings(path, s)
            self.assertEqual(load_settings(path), s)
            with mock.patch("tapdoc.tts_settings.os.replace", side_effect=OSError("đĩa đầy")):
                with self.assertRaises(OSError):
                    save_settings(path, {**s, "voice": "khác"})
            self.assertEqual(load_settings(path), s)
            self.assertEqual(list(Path(tmp).glob("*.tmp")), [])


class StaleTest(unittest.TestCase):
    def test_default_change_marks_only_unapproved(self):
        s = settings()
        rows = [row(), row("am_c", "cờ", status="dat"), row("cau_x", "bé đi", "cau")]
        for r in rows:
            p = effective_params(s, r)
            r["tts"] = {**asdict(p), "sig": signature(p), "trimmed": True}
        s["defaults"]["am"]["rate"] = -40
        self.assertEqual([needs_regen(s, r) for r in rows], [True, False, False])
        self.assertTrue(differs_from_settings(s, rows[1]))

    def test_missing_tts_record_needs_regen(self):
        self.assertTrue(needs_regen(settings(), row()))
        self.assertFalse(needs_regen(settings(), row(status="dat")))
