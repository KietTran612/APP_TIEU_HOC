using NUnit.Framework;
using UnityEngine;

namespace TapDoc.Tests
{
    /// <summary>
    /// Tắt tiếng loa trong lúc chạy test PlayMode (chủ dự án thấy ồn khi chạy nhiều test). Âm thanh vẫn được phát như
    /// thường (<c>AudioSource.isPlaying</c>, độ dài clip không đổi), chỉ âm lượng tổng về 0; chạy xong trả lại như cũ.
    /// </summary>
    [SetUpFixture]
    public class MuteAudioDuringTests
    {
        private float _volume;

        [OneTimeSetUp]
        public void Mute()
        {
            _volume = AudioListener.volume;
            AudioListener.volume = 0f;
        }

        [OneTimeTearDown]
        public void Restore() => AudioListener.volume = _volume;
    }
}
