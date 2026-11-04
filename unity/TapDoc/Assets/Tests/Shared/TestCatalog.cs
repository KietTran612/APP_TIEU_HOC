using System;
using UnityEngine;

namespace TapDoc.Tests
{
    /// <summary>Dựng catalog trên nguồn giả từ các hàm nạp theo mã (mỗi loại một hàm; không có hàm là thiếu file).</summary>
    public static class TestCatalog
    {
        public static FakeContentSource Source(
            Func<string, AudioClip> speech = null,
            Func<string, Sprite> image = null,
            Func<string, AudioClip> sfx = null) =>
            new()
            {
                Fallback = (kind, id) => kind switch
                {
                    ContentKind.Speech => speech?.Invoke(id),
                    ContentKind.Image => image?.Invoke(id),
                    ContentKind.Sfx => sfx?.Invoke(id),
                    _ => null,
                },
            };

        public static AssetCatalog FromLoaders(
            Func<string, AudioClip> speech = null,
            Func<string, Sprite> image = null,
            Func<string, AudioClip> sfx = null) =>
            new(Source(speech, image, sfx));
    }
}
