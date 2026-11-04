using System;
using System.Collections.Generic;
using UnityEngine;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// Nguồn dữ liệu giả trong bộ nhớ cho test: có thể giả lập nạp chậm (<see cref="DelayFrames"/>) và thiếu file
    /// (mã chưa <see cref="Put"/>, không có <see cref="Fallback"/>). Đếm số lần nạp và nhả từng mã.
    /// </summary>
    public sealed class FakeContentSource : IContentSource
    {
        private readonly Dictionary<(ContentKind, string), Object> _assets = new();
        private readonly Dictionary<(ContentKind, string), int> _loads = new();
        private readonly Dictionary<(ContentKind, string), int> _releases = new();

        /// <summary>Số khung <see cref="LoadAsync"/> chờ trước khi trả kết quả.</summary>
        public int DelayFrames { get; set; }

        /// <summary>Dùng cho mã chưa <see cref="Put"/>; trả <c>null</c> là thiếu file.</summary>
        public Func<ContentKind, string, Object> Fallback { get; set; }

        public void Put(ContentKind kind, string id, Object asset) => _assets[(kind, id)] = asset;

        public int LoadCount(ContentKind kind, string id) => _loads.TryGetValue((kind, id), out var n) ? n : 0;

        public int ReleaseCount(ContentKind kind, string id) => _releases.TryGetValue((kind, id), out var n) ? n : 0;

        public async Awaitable<Object> LoadAsync(ContentKind kind, string id)
        {
            for (var i = 0; i < DelayFrames; i++) await Awaitable.NextFrameAsync();
            return Load(kind, id);
        }

        public Object Load(ContentKind kind, string id)
        {
            var key = (kind, id);
            _loads[key] = LoadCount(kind, id) + 1;
            if (_assets.TryGetValue(key, out var asset)) return asset;
            return Fallback?.Invoke(kind, id);
        }

        public void Release(ContentKind kind, string id, Object asset)
        {
            _releases[(kind, id)] = ReleaseCount(kind, id) + 1;
        }

        /// <summary>Số lần được nhờ dọn (<see cref="IContentSource.ReleaseUnused"/>).</summary>
        public int ReleaseUnusedCount { get; private set; }

        public void ReleaseUnused() => ReleaseUnusedCount++;

        /// <summary>Tranh trơn 4×4 dùng cho test.</summary>
        public static Sprite NewSprite(string name = "test_sprite")
        {
            var tex = new Texture2D(4, 4, TextureFormat.RGBA32, false);
            var sprite = Sprite.Create(tex, new Rect(0, 0, 4, 4), new Vector2(.5f, .5f));
            sprite.name = name;
            return sprite;
        }

        /// <summary>Âm thanh ngắn 0,1 giây dùng cho test.</summary>
        public static AudioClip NewClip(string name = "test_clip") => AudioClip.Create(name, 4410, 1, 44100, false);
    }
}
