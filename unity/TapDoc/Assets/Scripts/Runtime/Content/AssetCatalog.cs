using System;
using System.Collections.Generic;
using UnityEngine;

namespace TapDoc
{
    public class AssetCatalog
    {
        private readonly Func<string, AudioClip> _audioLoader;
        private readonly Func<string, Sprite> _imageLoader;
        private readonly Func<string, AudioClip> _sfxLoader;
        private readonly HashSet<string> _loggedMissingAudio = new();
        private readonly HashSet<string> _loggedMissingImages = new();
        private readonly HashSet<string> _loggedMissingSfx = new();

        /// <param name="sfxLoader">
        /// Nạp tiếng động (<c>sfx_*</c>) từ thư mục riêng <c>sfx/</c>, tách hẳn khỏi âm thanh phát âm ở <c>audio/</c>.
        /// </param>
        public AssetCatalog(
            Func<string, AudioClip> audioLoader = null,
            Func<string, Sprite> imageLoader = null,
            Func<string, AudioClip> sfxLoader = null)
        {
            _audioLoader = audioLoader ?? (id => Resources.Load<AudioClip>($"audio/{id}"));
            _imageLoader = imageLoader ?? (id => Resources.Load<Sprite>($"images/{id}"));
            _sfxLoader = sfxLoader ?? (id => Resources.Load<AudioClip>($"sfx/{id}"));
        }

        public AudioClip Audio(string id)
        {
            if (string.IsNullOrEmpty(id)) return null;
            var clip = _audioLoader(id);
            if (clip == null && _loggedMissingAudio.Add(id))
            {
                Debug.LogError($"[TapDoc] Thiếu âm thanh: {id}");
            }
            return clip;
        }

        /// <summary>
        /// Tiếng động khi tương tác. Thiếu file thì chỉ cảnh báo một lần (app vẫn chạy, chỉ không có tiếng), khác với
        /// âm thanh phát âm và tranh là báo lỗi.
        /// </summary>
        public AudioClip Sfx(string id)
        {
            if (string.IsNullOrEmpty(id)) return null;
            var clip = _sfxLoader(id);
            if (clip == null && _loggedMissingSfx.Add(id))
            {
                Debug.LogWarning($"[TapDoc] Thiếu tiếng động: {id}");
            }
            return clip;
        }

        public Sprite Image(string id)
        {
            if (string.IsNullOrEmpty(id)) return null;
            var sprite = _imageLoader(id);
            if (sprite == null && _loggedMissingImages.Add(id))
            {
                Debug.LogError($"[TapDoc] Thiếu tranh: {id}");
            }
            return sprite;
        }
    }
}
