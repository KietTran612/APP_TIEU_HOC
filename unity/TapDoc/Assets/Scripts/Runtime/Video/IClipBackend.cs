using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Phần phát clip thật sự (giải mã hình, tiếng) mà <see cref="ClipPlayer"/> điều khiển. Bản thật là
    /// <see cref="VideoPlayerBackend"/>; test dùng bản giả để điều khiển từng khung mà không giải mã video.
    /// </summary>
    public interface IClipBackend
    {
        /// <summary>Chuẩn bị và phát <paramref name="clip"/> từ đầu (bản thật cần <c>VideoClip</c>, vật khác là hỏng).</summary>
        void Begin(Object clip);

        /// <summary>Dừng, tắt tiếng và bỏ tham chiếu clip.</summary>
        void Stop();

        /// <summary>Nhả bộ nhớ hình (RenderTexture); lần <see cref="Begin"/> sau tự tạo lại.</summary>
        void Release();

        /// <summary>Đã vẽ xong khung đầu tiên vào <see cref="Texture"/> sau lần <see cref="Begin"/> gần nhất.</summary>
        bool FirstFrameReady { get; }

        /// <summary>Clip đã chạy hết.</summary>
        bool Finished { get; }

        /// <summary>Không phát được (lỗi giải mã, clip không hợp lệ).</summary>
        bool Failed { get; }

        Texture Texture { get; }
        int Width { get; }
        int Height { get; }
    }
}
