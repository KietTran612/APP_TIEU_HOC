using System;
using UnityEngine;

namespace TapDoc.Tests
{
    /// <summary>
    /// Dựng catalog trên nguồn giả từ các hàm nạp theo mã (mỗi loại một hàm; không có hàm là thiếu file). Chữ (danh
    /// sách bài, bài học, Phụ lục) và font vẫn đọc thật từ Resources.
    /// </summary>
    public static class TestCatalog
    {
        private static readonly ResourcesContentSource Real = new();

        /// <summary>
        /// <paramref name="clip"/>: clip giả theo mã tranh (không tạo được <c>VideoClip</c> bằng code, nên test dùng
        /// vật bất kỳ cùng <see cref="FakeClipBackend"/>); không có thì không tranh nào có clip.
        /// </summary>
        public static FakeContentSource Source(
            Func<string, AudioClip> speech = null,
            Func<string, Sprite> image = null,
            Func<string, AudioClip> sfx = null,
            Func<string, UnityEngine.Object> clip = null) =>
            new()
            {
                Fallback = (kind, id) => kind switch
                {
                    ContentKind.Speech => speech?.Invoke(id),
                    ContentKind.Image => image?.Invoke(id),
                    ContentKind.Sfx => sfx?.Invoke(id),
                    ContentKind.Clip => clip?.Invoke(id),
                    _ => Real.Load(kind, id),
                },
            };

        public static AssetCatalog FromLoaders(
            Func<string, AudioClip> speech = null,
            Func<string, Sprite> image = null,
            Func<string, AudioClip> sfx = null,
            Func<string, UnityEngine.Object> clip = null) =>
            new(Source(speech, image, sfx, clip));
    }
}
