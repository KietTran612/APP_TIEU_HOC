"""Ghép tiếng đã có thành từ/câu đọc trơn (quyết định của chủ dự án 09/11: đọc đúng là trên hết).

Mỗi tiếng: giải mã MP3 ra PCM, cắt lặng đầu và cuối, cân âm lượng (RMS) về mức trung vị; giữa các tiếng chèn
khoảng nghỉ ngắn và đều (mặc định 0,08 giây, dấu phẩy 0,25 giây); rồi mã hoá lại MP3. Không nối thẳng file MP3
được vì khung MP3 của bộ đọc mượn dữ liệu khung trước, nên không bỏ được khoảng lặng đầu mỗi tiếng.

Giải mã và mã hoá dùng Media Foundation của Windows qua PowerShell (không cần ffmpeg); phần xử lý là Python thuần.
"""

import math
import shutil
import struct
import subprocess
import tempfile
import wave
from pathlib import Path

SR = 24000  # tần số mẫu của bộ đọc
GAP = 0.08  # nghỉ giữa hai tiếng (giây)
COMMA_GAP = 0.25  # nghỉ ở dấu phẩy
LEAD, TAIL = 0.05, 0.12  # lặng đầu và cuối file
MARGIN = 0.02  # giữ thêm quanh phần có tiếng khi cắt lặng
THRESHOLD_DB = -40.0  # dưới mức này so với khung to nhất thì coi là lặng
_FRAME = 0.01
_TIMEOUT = 300


class JoinError(Exception):
    """Không ghép được (thiếu tiếng, tiếng câm, giải mã/mã hoá lỗi)."""


def rms(samples) -> float:
    return math.sqrt(sum(v * v for v in samples) / len(samples)) if samples else 0.0


def trim_silence(samples, sr: int = SR, threshold_db: float = THRESHOLD_DB, margin: float = MARGIN) -> list:
    """Bỏ lặng đầu và cuối: giữ từ khung đầu tới khung cuối to hơn ngưỡng (so với khung to nhất), cộng lề."""
    step = max(1, int(_FRAME * sr))
    levels = [rms(samples[i:i + step]) for i in range(0, len(samples), step)]
    peak = max(levels, default=0.0)
    if peak <= 0:
        return []
    limit = peak * 10 ** (threshold_db / 20)
    loud = [k for k, level in enumerate(levels) if level > limit]
    pad = int(margin * sr)
    start = max(0, loud[0] * step - pad)
    end = min(len(samples), (loud[-1] + 1) * step + pad)
    return list(samples[start:end])


def match_loudness(parts) -> list:
    """Đưa mọi tiếng về cùng RMS (trung vị các tiếng), không để vượt biên 16 bit."""
    levels = [rms(p) for p in parts]
    target = sorted(levels)[len(levels) // 2]
    out = []
    for part, level in zip(parts, levels):
        gain = target / level if level else 1.0
        peak = max((abs(v) for v in part), default=0)
        if peak and peak * gain > 32767:
            gain = 32767 / peak
        out.append([max(-32768, min(32767, int(round(v * gain)))) for v in part])
    return out


def assemble(parts, gaps, sr: int = SR, lead: float = LEAD, tail: float = TAIL) -> list:
    """lặng đầu + tiếng 1 + nghỉ + tiếng 2 + … + lặng cuối."""
    if len(gaps) != len(parts) - 1:
        raise ValueError("số khoảng nghỉ phải bằng số tiếng trừ một")
    out = [0] * int(lead * sr)
    for k, part in enumerate(parts):
        if k:
            out += [0] * int(gaps[k - 1] * sr)
        out += part
    return out + [0] * int(tail * sr)


def plan(join, gap: float = GAP) -> tuple[list, list]:
    """Danh sách join (mã và dấu "," ) → (mã theo thứ tự, khoảng nghỉ giữa từng cặp)."""
    ids, gaps, comma = [], [], False
    for item in join:
        if item == ",":
            comma = True
            continue
        if ids:
            gaps.append(COMMA_GAP if comma else gap)
        ids.append(item)
        comma = False
    return ids, gaps


def join_files(paths, gaps, decoder=None, encoder=None) -> bytes:
    """Ghép các file MP3 (theo thứ tự) thành một MP3 đọc trơn.

    decoder(paths) -> (tần số mẫu, {path: mẫu PCM mono}); encoder(mẫu, tần số) -> byte MP3.
    """
    paths = [str(p) for p in paths]
    sr, decoded = (decoder or decode_mp3)(paths)
    parts = []
    for path in paths:
        samples = decoded.get(path)
        if not samples:
            raise JoinError(f"không giải mã được {Path(path).name}")
        part = trim_silence(samples, sr)
        if not part:
            raise JoinError(f"{Path(path).name} không có tiếng")
        parts.append(part)
    data = (encoder or encode_mp3)(assemble(match_loudness(parts), gaps, sr), sr)
    if not data:
        raise JoinError("mã hoá MP3 không ra dữ liệu")
    return data


# ---- keep_first trên PCM (soát 13/11) ----

FADE = 0.05  # giảm dần ở cuối phần giữ (giây)
FADE_IN = 0.005
KEEP_LEAD = 0.05  # giữ thêm trước tiếng đầu (âm gốc, thường là lặng)
KEEP_TAIL = 0.1  # lặng thêm sau khi giảm dần
QUIET_DB = -30.0  # dưới mức này so với khung to nhất thì coi là đã tắt tiếng
GAP_MIN = 0.15  # khoảng lặng ngắn nhất coi là chỗ nghỉ (dấu phẩy ~0,2 giây, hết câu ~1 giây)
EDGE = 0.03  # đọc liền: dừng trước đầu tiếng kế tiếp chừng này


def keep_first_pcm(samples, sr: int, *, word_start: float, next_word, pause: bool) -> tuple[list, float]:
    """Giữ phần đọc đầu của câu đệm ("ẹ. ẹ.", "nụ hoa.") trên PCM, kết thúc bằng giảm dần và lặng.

    Mốc bộ đọc không đủ tin: với "X. X." mốc tiếng sau có thể rơi giữa tiếng đầu, và PCM giải mã trễ hơn mốc
    (độ trễ bộ giải mã, ước bằng chỗ bắt đầu có tiếng trừ `word_start`).
    `next_word`: (đầu, cuối) theo mốc của tiếng ngay sau phần giữ, hoặc None.
    - `pause` (sau phần giữ có dấu câu): cắt ở khoảng lặng đầu tiên dài từ GAP_MIN sau chỗ bắt đầu có tiếng, nếu nó
      bắt đầu trước lúc tiếng kế tiếp kết thúc (theo mốc); không có thì như đọc liền (bộ đọc không nghỉ ở dấu câu).
    - Đọc liền: cắt trước đầu tiếng kế tiếp (mốc cộng độ trễ, trừ EDGE); không có tiếng kế tiếp thì giữ tới chỗ
      tắt tiếng cuối.
    Trả (PCM mới, giây theo mốc bộ đọc ứng với mẫu đầu PCM mới) để dời mốc từ: mốc mới = mốc cũ - giá trị này.
    """
    step = max(1, int(_FRAME * sr))
    levels = [rms(samples[i:i + step]) for i in range(0, len(samples), step)]
    peak = max(levels, default=0.0)
    if peak <= 0:
        raise JoinError("câu đệm không có tiếng")
    quiet = peak * 10 ** (QUIET_DB / 20)
    loud = [k for k, level in enumerate(levels) if level > quiet]
    onset = loud[0] * step
    delay = onset / sr - word_start
    limit, gap_before = len(samples), len(samples)
    if next_word is not None:
        limit = max(onset + step, int((next_word[0] + delay - EDGE) * sr))
        gap_before = int((next_word[1] + delay) * sr)
    cut = None
    if pause:
        need = max(1, int(round(GAP_MIN / _FRAME)))
        run = 0
        for k in range(loud[0], len(levels)):
            run = run + 1 if levels[k] <= quiet else 0
            if run == need:
                if (k - need + 1) * step < gap_before:
                    cut = (k - need + 1) * step + int(MARGIN * sr)
                break
    if cut is None:
        last = max((k for k in loud if k * step < limit), default=loud[0])
        cut = min(limit, (last + 1) * step + int(MARGIN * sr))
    start = max(0, onset - int(KEEP_LEAD * sr))
    piece = list(samples[start:max(cut, start + step)])
    fade_in, fade = min(len(piece), int(FADE_IN * sr)), min(len(piece), int(FADE * sr))
    for i in range(fade_in):
        piece[i] = int(piece[i] * i / fade_in)
    for i in range(fade):
        k = len(piece) - fade + i
        piece[k] = int(piece[k] * 0.5 * (1 + math.cos(math.pi * (i + 1) / fade)))
    return piece + [0] * int(KEEP_TAIL * sr), start / sr - delay


def decode_bytes(data: bytes) -> tuple[int, list]:
    """Giải mã một MP3 (byte) ra (tần số mẫu, PCM mono)."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "doc.mp3"
        path.write_bytes(data)
        sr, decoded = decode_mp3([str(path)])
    samples = decoded.get(str(path))
    if not samples:
        raise JoinError("không giải mã được âm thanh của bộ đọc")
    return sr, samples


# ---- Media Foundation (PowerShell) ----

_PS_HEAD = r"""
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Storage.StorageFolder, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Media.Transcoding.MediaTranscoder, Windows.Media, ContentType = WindowsRuntime]
$null = [Windows.Media.MediaProperties.MediaEncodingProfile, Windows.Media, ContentType = WindowsRuntime]
$methods = [System.WindowsRuntimeSystemExtensions].GetMethods()
$asTaskOp = $methods | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' } | Select-Object -First 1
$asTaskProg = $methods | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncActionWithProgress`1' } | Select-Object -First 1
function AwaitOp($op, [Type]$t) { $task = $asTaskOp.MakeGenericMethod($t).Invoke($null, @($op)); $task.Wait(); $task.Result }
function Transcode($inPath, $outPath, $profile) {
  $src = AwaitOp ([Windows.Storage.StorageFile]::GetFileFromPathAsync($inPath)) ([Windows.Storage.StorageFile])
  $folder = AwaitOp ([Windows.Storage.StorageFolder]::GetFolderFromPathAsync([IO.Path]::GetDirectoryName($outPath))) ([Windows.Storage.StorageFolder])
  $dst = AwaitOp ($folder.CreateFileAsync([IO.Path]::GetFileName($outPath), [Windows.Storage.CreationCollisionOption]::ReplaceExisting)) ([Windows.Storage.StorageFile])
  $prep = AwaitOp ((New-Object Windows.Media.Transcoding.MediaTranscoder).PrepareFileTranscodeAsync($src, $dst, $profile)) ([Windows.Media.Transcoding.PrepareTranscodeResult])
  if (-not $prep.CanTranscode) { throw "không chuyển được $inPath" }
  $task = $asTaskProg.MakeGenericMethod([double]).Invoke($null, @($prep.TranscodeAsync())); $task.Wait()
}
"""

_DECODE_PS1 = _PS_HEAD + r"""
param()
$dir = $args[0]
# Đặt tần số/kênh riêng thì Media Foundation từ chối; để mặc định (thường 48 kHz stereo) rồi trộn kênh trong Python.
$profile = [Windows.Media.MediaProperties.MediaEncodingProfile]::CreateWav([Windows.Media.MediaProperties.AudioEncodingQuality]::High)
foreach ($f in Get-ChildItem $dir -Filter *.mp3) {
  try { Transcode $f.FullName ([IO.Path]::ChangeExtension($f.FullName, '.wav')) $profile } catch { }
}
"""

_ENCODE_PS1 = _PS_HEAD + r"""
$in = $args[0]; $out = $args[1]
$profile = [Windows.Media.MediaProperties.MediaEncodingProfile]::CreateMp3([Windows.Media.MediaProperties.AudioEncodingQuality]::Medium)
$profile.Audio.SampleRate = 24000; $profile.Audio.ChannelCount = 1; $profile.Audio.Bitrate = 48000
Transcode $in $out $profile
"""


def _run_ps(script_text: str, folder: Path, *args) -> None:
    script = folder / "media.ps1"
    script.write_text(script_text.replace("param()\n", ""), encoding="utf-8-sig")
    try:
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script), *map(str, args)],
                       check=True, capture_output=True, timeout=_TIMEOUT)
    except (OSError, subprocess.SubprocessError) as e:
        raise JoinError(f"Media Foundation lỗi: {e}") from e


def decode_mp3(paths) -> tuple[int, dict]:
    """(tần số mẫu, PCM 16 bit mono của mỗi file); bỏ qua file không giải mã được."""
    out, rates = {}, set()
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for k, path in enumerate(paths):
            shutil.copy(path, tmp / f"p{k}.mp3")
        _run_ps(_DECODE_PS1, tmp, tmp)
        for k, path in enumerate(paths):
            wav = tmp / f"p{k}.wav"
            if not wav.is_file() or wav.stat().st_size == 0:
                continue
            try:
                with wave.open(str(wav), "rb") as w:
                    rate, ch, width = w.getframerate(), w.getnchannels(), w.getsampwidth()
                    raw = w.readframes(w.getnframes())
            except (EOFError, wave.Error):
                continue
            if width != 2:
                raise JoinError(f"{Path(path).name}: giải mã ra định dạng lạ")
            data = struct.unpack("<%dh" % (len(raw) // 2), raw)
            out[path] = [int(sum(data[i:i + ch]) / ch) for i in range(0, len(data) - ch + 1, ch)]
            rates.add(rate)
    if len(rates) > 1:
        raise JoinError("các tiếng giải mã ra tần số mẫu khác nhau")
    return (rates.pop() if rates else SR), out


ENCODER_FLUSH = 0.2  # bộ mã hoá MP3 của Media Foundation bỏ mất khoảng 0,1 giây cuối (đo 13/11): đệm lặng bù


def encode_mp3(samples, sr: int = SR) -> bytes:
    samples = list(samples) + [0] * int(ENCODER_FLUSH * sr)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        wav, mp3 = tmp / "ghep.wav", tmp / "ghep.mp3"
        with wave.open(str(wav), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sr)
            w.writeframes(struct.pack("<%dh" % len(samples), *samples))
        _run_ps(_ENCODE_PS1, tmp, wav, mp3)
        return mp3.read_bytes() if mp3.is_file() else b""
