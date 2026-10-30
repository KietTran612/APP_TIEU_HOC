using System.Collections.Generic;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Phát tiếng động khi tương tác (<see cref="SystemSfx"/>), trên kênh riêng, tách hẳn khỏi giọng đọc
    /// (<see cref="SpeechPlayer"/>): không dừng hay cắt giọng đọc, nhỏ hơn giọng đọc, tắt được ở màn phụ huynh.
    /// Chỉ nhận mã <c>sfx_*</c>; thiếu file thì <see cref="AssetCatalog.Sfx"/> chỉ cảnh báo.
    /// </summary>
    public class SfxPlayer : MonoBehaviour
    {
        public const float DefaultVolume = .45f;
        private const int MaxHistory = 50;

        private AssetCatalog _catalog;
        private SpeechPlayer _speech;
        private AudioSource _source;
        private readonly List<string> _history = new();

        /// <summary>Kênh tiếng động của app (do <see cref="AppRoot"/> tạo); <c>null</c> trong test màn không có app.</summary>
        public static SfxPlayer Instance { get; private set; }

        /// <summary>Phụ huynh có bật tiếng động không.</summary>
        public bool Enabled { get; set; } = true;

        /// <summary>Các mã đã được phép phát (kể cả khi thiếu file), mới nhất ở cuối.</summary>
        public IReadOnlyList<string> History => _history;

        public void Init(AssetCatalog catalog, SpeechPlayer speech)
        {
            _catalog = catalog ?? new AssetCatalog();
            _speech = speech;
            if (_source == null)
            {
                _source = gameObject.AddComponent<AudioSource>();
                _source.playOnAwake = false;
                _source.volume = DefaultVolume;
            }
            Instance = this;
        }

        /// <summary>Phát tiếng động <paramref name="id"/>; bỏ qua khi phụ huynh đã tắt.</summary>
        public void Play(string id)
        {
            if (!SystemSfx.IsSfx(id))
            {
                Debug.LogError($"[TapDoc] Không phải mã tiếng động: {id}");
                return;
            }
            if (!Enabled) return;
            Record(id);
            var clip = _catalog?.Sfx(id);
            if (clip != null && _source != null) _source.PlayOneShot(clip);
        }

        /// <summary>Như <see cref="Play"/>, nhưng bỏ qua khi giọng đọc đang phát (để không chen vào lời đánh vần).</summary>
        public void PlayUnlessSpeaking(string id)
        {
            if (_speech != null && _speech.IsBusy) return;
            Play(id);
        }

        private void Record(string id)
        {
            if (_history.Count >= MaxHistory) _history.RemoveAt(0);
            _history.Add(id);
        }

        private void OnDestroy()
        {
            if (Instance == this) Instance = null;
        }
    }
}
