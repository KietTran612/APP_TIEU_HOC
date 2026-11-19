using UnityEngine;
using UnityEngine.Video;

namespace TapDoc
{
    /// <summary>
    /// Phần phát clip thật: một <see cref="VideoPlayer"/> vẽ vào một <see cref="RenderTexture"/> theo cỡ clip, tiếng qua
    /// một <see cref="AudioSource"/> riêng. Tạo khi phát lần đầu, trên GameObject của <see cref="ClipPlayer"/>.
    /// </summary>
    public sealed class VideoPlayerBackend : IClipBackend
    {
        private readonly GameObject _host;
        private VideoPlayer _player;
        private AudioSource _audio;
        private RenderTexture _texture;

        public VideoPlayerBackend(GameObject host)
        {
            _host = host;
        }

        public bool FirstFrameReady { get; private set; }
        public bool Finished { get; private set; }
        public bool Failed { get; private set; }
        public Texture Texture => _texture;
        public int Width { get; private set; }
        public int Height { get; private set; }

        public void Begin(Object clip)
        {
            FirstFrameReady = false;
            Finished = false;
            Failed = false;
            var video = clip as VideoClip;
            if (video == null || _host == null)
            {
                Failed = true;
                return;
            }

            EnsurePlayer();
            Width = (int)video.width;
            Height = (int)video.height;
            EnsureTexture(Width, Height);
            _player.targetTexture = _texture;
            _player.clip = video;
            _player.controlledAudioTrackCount = 1;
            _player.EnableAudioTrack(0, true);
            _player.SetTargetAudioSource(0, _audio);
            _player.sendFrameReadyEvents = true;
            _player.Prepare();
        }

        public void Stop()
        {
            FirstFrameReady = false;
            Finished = false;
            if (_player == null) return;
            _player.sendFrameReadyEvents = false;
            _player.Stop();
            _player.clip = null;
        }

        public void Release()
        {
            Stop();
            if (_player != null) _player.targetTexture = null;
            if (_texture == null) return;
            _texture.Release();
            Object.Destroy(_texture);
            _texture = null;
        }

        private void EnsurePlayer()
        {
            if (_player != null) return;
            _audio = _host.AddComponent<AudioSource>();
            _audio.playOnAwake = false;
            _audio.volume = ClipPlayer.Volume;
            _player = _host.AddComponent<VideoPlayer>();
            _player.playOnAwake = false;
            _player.isLooping = false;
            _player.waitForFirstFrame = true;
            _player.skipOnDrop = true;
            _player.source = VideoSource.VideoClip;
            _player.renderMode = VideoRenderMode.RenderTexture;
            _player.audioOutputMode = VideoAudioOutputMode.AudioSource;
            _player.prepareCompleted += source =>
            {
                if (source.clip != null) source.Play(); // đã bị dừng trong lúc chuẩn bị thì thôi
            };
            _player.frameReady += OnFrameReady;
            _player.loopPointReached += _ => Finished = true;
            _player.errorReceived += (_, _) => Failed = true;
        }

        /// <summary>Khung đầu đã có: bỏ nghe sự kiện từng khung (tốn), lớp phủ được hiện từ khung sau.</summary>
        private void OnFrameReady(VideoPlayer source, long frameIndex)
        {
            FirstFrameReady = true;
            source.sendFrameReadyEvents = false;
        }

        /// <summary>RenderTexture theo cỡ clip, xoá trong suốt trước mỗi clip để không hiện khung của clip trước.</summary>
        private void EnsureTexture(int width, int height)
        {
            if (_texture == null || _texture.width != width || _texture.height != height)
            {
                if (_texture != null)
                {
                    _texture.Release();
                    Object.Destroy(_texture);
                }
                _texture = new RenderTexture(width, height, 0, RenderTextureFormat.ARGB32) { name = "ClipTexture" };
                _texture.Create();
            }
            var active = RenderTexture.active;
            RenderTexture.active = _texture;
            GL.Clear(false, true, Color.clear);
            RenderTexture.active = active;
        }
    }
}
