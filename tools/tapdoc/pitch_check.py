"""Đo cao độ thanh hỏi/ngã trong âm thanh HoaiMy (thiết kế TV2 tập một, mục 9).

HoaiMy hay đọc tiếng hỏi/ngã thành thanh huyền (đường cao độ đi xuống thay vì võng xuống rồi lên).
Cách đo: giải mã MP3 ra WAV bằng Media Foundation của Windows (qua PowerShell, không cần ffmpeg), dò cao độ bằng
YIN thuần Python, rồi so với mẫu thanh điệu dựng từ các tiếng đã duyệt `dat`. Giọng này đọc ngã như hỏi, nên hai
thanh coi là một nhóm. Tiếng trong từ/câu được cắt theo mốc từ ghi lúc tạo (`content/tts/marks/<mã>.json`).
"""

import json
import math
import shutil
import struct
import subprocess
import tempfile
import unicodedata
import wave
from pathlib import Path

from .viet import tokens

POINTS = 10  # số điểm của đường cao độ sau khi lấy mẫu lại
_SR = 8000  # hạ mẫu còn 8 kHz cho nhanh
_FMIN, _FMAX = 110.0, 480.0
_WIN, _HOP = 240, 80  # cửa sổ 30 ms, bước 10 ms
_MIN_POINTS = 5
_TONE_MARKS = {"̀": "huyen", "́": "sac", "̉": "hoi", "̃": "nga", "̣": "nang"}
_DIP_RISE = ("hoi", "nga")

_DECODE_PS1 = r"""
param([string]$Dir)
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Storage.StorageFolder, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Media.Transcoding.MediaTranscoder, Windows.Media, ContentType = WindowsRuntime]
$null = [Windows.Media.MediaProperties.MediaEncodingProfile, Windows.Media, ContentType = WindowsRuntime]
$methods = [System.WindowsRuntimeSystemExtensions].GetMethods()
$asTaskOp = $methods | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' } | Select-Object -First 1
$asTaskProg = $methods | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncActionWithProgress`1' } | Select-Object -First 1
function AwaitOp($op, [Type]$t) { $task = $asTaskOp.MakeGenericMethod($t).Invoke($null, @($op)); $task.Wait(); $task.Result }
$folder = AwaitOp ([Windows.Storage.StorageFolder]::GetFolderFromPathAsync($Dir)) ([Windows.Storage.StorageFolder])
$tr = New-Object Windows.Media.Transcoding.MediaTranscoder
$profile = [Windows.Media.MediaProperties.MediaEncodingProfile]::CreateWav([Windows.Media.MediaProperties.AudioEncodingQuality]::Low)
$profile.Audio.SampleRate = 16000
$profile.Audio.ChannelCount = 1
$profile.Audio.BitsPerSample = 16
foreach ($f in Get-ChildItem $Dir -Filter *.mp3) {
  $wavName = [IO.Path]::ChangeExtension($f.Name, '.wav')
  try {
    $in = AwaitOp ([Windows.Storage.StorageFile]::GetFileFromPathAsync($f.FullName)) ([Windows.Storage.StorageFile])
    $out = AwaitOp ($folder.CreateFileAsync($wavName, [Windows.Storage.CreationCollisionOption]::ReplaceExisting)) ([Windows.Storage.StorageFile])
    $prep = AwaitOp ($tr.PrepareFileTranscodeAsync($in, $out, $profile)) ([Windows.Media.Transcoding.PrepareTranscodeResult])
    if (-not $prep.CanTranscode) { "skip $($f.Name)"; continue }
    $task = $asTaskProg.MakeGenericMethod([double]).Invoke($null, @($prep.TranscodeAsync())); $task.Wait()
  } catch { "fail $($f.Name)" }
}
"""


def tone_of(word: str) -> str:
    for ch in unicodedata.normalize("NFD", word):
        if ch in _TONE_MARKS:
            return _TONE_MARKS[ch]
    return "ngang"


def words_to_check(text: str) -> list[tuple[int, str, str]]:
    """(vị trí, tiếng, thanh) của các tiếng mang thanh hỏi hoặc ngã."""
    return [(k, tok, tone_of(tok)) for k, (tok, _) in enumerate(tokens(text)) if tone_of(tok) in _DIP_RISE]


# ---- giải mã ----

def decode(mp3s, cache_dir) -> dict[Path, Path]:
    """WAV 16 kHz mono cho mỗi MP3 (giữ trong `cache_dir`, giải mã lại khi MP3 mới hơn). MP3 hỏng thì bỏ qua."""
    cache = Path(cache_dir)
    cache.mkdir(parents=True, exist_ok=True)
    out, todo = {}, []
    for mp3 in map(Path, mp3s):
        wav = cache / f"{mp3.stem}.wav"
        out[mp3] = wav
        if not wav.is_file() or wav.stat().st_mtime < mp3.stat().st_mtime:
            todo.append(mp3)
    if todo:
        with tempfile.TemporaryDirectory(dir=cache) as tmp:
            for mp3 in todo:
                shutil.copy(mp3, Path(tmp) / mp3.name)
            script = Path(tmp) / "decode.ps1"
            script.write_text(_DECODE_PS1, encoding="utf-8-sig")
            subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script),
                            "-Dir", tmp], check=True, capture_output=True)
            for mp3 in todo:
                made = Path(tmp) / f"{mp3.stem}.wav"
                if made.is_file():
                    shutil.move(made, cache / made.name)
    return {mp3: wav for mp3, wav in out.items() if wav.is_file()}


# ---- dò cao độ ----

def _read_wav(path) -> list[float]:
    with wave.open(str(path), "rb") as w:
        n, sr, ch, sw = w.getnframes(), w.getframerate(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
    if sw != 2:
        raise ValueError(f"{path}: chỉ đọc WAV 16 bit")
    data = struct.unpack("<%dh" % (len(raw) // 2), raw)[::ch]
    step = max(1, sr // _SR)
    return [sum(data[i:i + step]) / step for i in range(0, len(data) - step + 1, step)]


def _track(samples) -> list[tuple[float, float | None]]:
    """(giây, Hz hoặc None) mỗi bước 10 ms — YIN với ngưỡng 0,2."""
    lo, hi = int(_SR / _FMAX), int(_SR / _FMIN)
    out = []
    for start in range(0, len(samples) - _WIN - hi, _HOP):
        x = samples[start:start + _WIN + hi]
        energy = math.sqrt(sum(v * v for v in x[:_WIN]) / _WIN)
        cm, run = [1.0] * (hi + 1), 0.0
        for tau in range(1, hi + 1):
            d = 0.0
            for j in range(_WIN):
                diff = x[j] - x[j + tau]
                d += diff * diff
            run += d
            cm[tau] = d * tau / run if run else 1.0
        best = next((tau for tau in range(lo, hi) if cm[tau] < 0.2 and cm[tau] <= cm[tau + 1]), None)
        f = None
        if best is not None and energy > 300:
            a, b, c = cm[best - 1], cm[best], cm[best + 1]
            den = a - 2 * b + c
            f = _SR / (best + (0.5 * (a - c) / den if den else 0.0))
        out.append(((start + _WIN / 2) / _SR, f))
    return out


def contour(wav, start: float | None = None, end: float | None = None) -> list[float]:
    """Cao độ (bán âm so với 220 Hz) các khung hữu thanh trong khoảng [start, end] giây."""
    return [12 * math.log2(f / 220.0) for t, f in _track(_read_wav(wav))
            if f and (start is None or t >= start) and (end is None or t <= end)]


def resample(values, n: int = POINTS) -> list[float]:
    k = len(values)
    return [values[min(k - 1, round(i * (k - 1) / (n - 1)))] for i in range(n)]


def build_templates(groups: dict[str, list[list[float]]]) -> dict[str, list[float]]:
    """Mẫu mỗi thanh = trung bình các đường đã lấy mẫu lại; mẫu ngã gộp cả hỏi (giọng này đọc ngã như hỏi)."""
    groups = {tone: list(curves) for tone, curves in groups.items() if curves}
    if "hoi" in groups:
        groups["nga"] = groups.get("nga", []) + groups["hoi"]
    return {tone: [sum(c[i] for c in curves) / len(curves) for i in range(POINTS)] for tone, curves in groups.items()}


def nearest(values, templates) -> str:
    v = resample(values)
    return min(templates, key=lambda t: sum((a - b) ** 2 for a, b in zip(v, templates[t])))


def judge(values, tone: str, templates) -> bool:
    """Tiếng hỏi/ngã đạt khi đường cao độ gần mẫu hỏi hoặc ngã nhất. Quá ít điểm hữu thanh thì không đạt."""
    if len(values) < _MIN_POINTS:
        return False
    if tone not in _DIP_RISE:
        return True
    return nearest(values, templates) in _DIP_RISE


def check_row(row: dict, wav, marks: dict | None, templates) -> list[dict]:
    """Kết quả từng tiếng hỏi/ngã của một mã: ok True/False, hoặc None khi không cắt được tiếng (thiếu mốc)."""
    words = words_to_check(row["text"])
    count = len(tokens(row["text"]))
    spans = (marks or {}).get("words") or []
    results = []
    for k, word, tone in words:
        res = {"id": row["id"], "word": word, "tone": tone}
        if wav is None or (count > 1 and len(spans) != count):
            results.append({**res, "ok": None, "why": "không có mốc từng tiếng"})
            continue
        start, end = (None, None) if count == 1 else spans[k]
        values = contour(wav, start, end)
        ok = judge(values, tone, templates)
        results.append({**res, "ok": ok, "best": nearest(values, templates) if len(values) >= _MIN_POINTS else "?"})
    return results


def reference_templates(rows, audio_dir, cache_dir, per_tone: int = 14) -> dict[str, list[float]]:
    """Mẫu thanh điệu từ tối đa `per_tone` tiếng lẻ đã duyệt `dat` mỗi thanh."""
    picked: dict[str, list[Path]] = {}
    for r in rows:
        mp3 = Path(audio_dir) / f"{r['id']}.mp3"
        if r.get("kind") == "tieng" and r.get("status") == "dat" and len(tokens(r["text"])) == 1 and mp3.is_file():
            bucket = picked.setdefault(tone_of(r["text"]), [])
            if len(bucket) < per_tone:
                bucket.append(mp3)
    wavs = decode([m for ms in picked.values() for m in ms], cache_dir)
    groups = {}
    for tone, mp3s in picked.items():
        curves = [contour(wavs[m]) for m in mp3s if m in wavs]
        groups[tone] = [resample(c) for c in curves if len(c) >= _MIN_POINTS]
    return build_templates(groups)


def check_rows(rows, audio_dir, marks_dir, cache_dir, templates) -> list[dict]:
    """Đo mọi tiếng hỏi/ngã của các mã đã có file."""
    targets = [r for r in rows if words_to_check(r["text"]) and (Path(audio_dir) / f"{r['id']}.mp3").is_file()]
    wavs = decode([Path(audio_dir) / f"{r['id']}.mp3" for r in targets], cache_dir)
    results = []
    for r in targets:
        marks_path = Path(marks_dir) / f"{r['id']}.json"
        marks = json.loads(marks_path.read_text(encoding="utf-8")) if marks_path.is_file() else None
        results += check_row(r, wavs.get(Path(audio_dir) / f"{r['id']}.mp3"), marks, templates)
    return results
