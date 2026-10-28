using System;
using System.Collections.Generic;
using UnityEngine;

namespace TapDoc
{
    public class AssetCatalog
    {
        private readonly Func<string, AudioClip> _audioLoader;
        private readonly Func<string, Sprite> _imageLoader;
        private readonly HashSet<string> _loggedMissingAudio = new();
        private readonly HashSet<string> _loggedMissingImages = new();

        public AssetCatalog(
            Func<string, AudioClip> audioLoader = null,
            Func<string, Sprite> imageLoader = null)
        {
            _audioLoader = audioLoader ?? (id => Resources.Load<AudioClip>($"audio/{id}"));
            _imageLoader = imageLoader ?? (id => Resources.Load<Sprite>($"images/{id}"));
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
