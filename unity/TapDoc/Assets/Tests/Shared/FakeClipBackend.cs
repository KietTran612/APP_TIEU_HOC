using UnityEngine;

namespace TapDoc.Tests
{
    /// <summary>
    /// Phần phát clip giả cho test: không giải mã video; test tự bật "có khung đầu", "hết clip", "hỏng". Đếm số lần
    /// bắt đầu, dừng, nhả để test kiểm việc <see cref="ClipPlayer"/> làm với phần phát.
    /// </summary>
    public sealed class FakeClipBackend : IClipBackend
    {
        private readonly Texture2D _texture = new(4, 4, TextureFormat.RGBA32, false);

        public int BeginCount { get; private set; }
        public int StopCount { get; private set; }
        public int ReleaseCount { get; private set; }

        /// <summary>Clip đang giữ (bỏ khi <see cref="Stop"/>).</summary>
        public Object LastClip { get; private set; }

        /// <summary>Lần <see cref="Begin"/> sau báo hỏng ngay.</summary>
        public bool FailOnBegin { get; set; }

        public bool FirstFrameReady { get; set; }
        public bool Finished { get; set; }
        public bool Failed { get; set; }
        public Texture Texture => _texture;
        public int Width => 1280;
        public int Height => 720;

        public void Begin(Object clip)
        {
            BeginCount++;
            LastClip = clip;
            FirstFrameReady = false;
            Finished = false;
            Failed = FailOnBegin;
        }

        public void Stop()
        {
            StopCount++;
            LastClip = null;
        }

        public void Release() => ReleaseCount++;
    }
}
