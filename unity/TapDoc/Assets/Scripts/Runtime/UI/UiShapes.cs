using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Hình khối của giao diện, sinh một lần lúc chạy rồi giữ lại (không có file ảnh): khung bo góc 9 mảnh, hình tròn
    /// và vân gạch chéo lặp được cho bóng đổ kiểu tranh SGK. Tất cả màu trắng để tô bằng <c>Image.color</c>, trừ vân
    /// gạch chéo đã có sẵn màu mực.
    /// </summary>
    internal static class UiShapes
    {
        /// <summary>Bán kính góc của khung bo góc (đơn vị canvas, cũng là điểm ảnh của sprite).</summary>
        public const int CornerRadius = 16;

        private const int RoundedSize = 64;
        private const int RoundedBorder = 24;
        private const int CircleSize = 128;
        private const int HatchRoundedSize = 48;
        private const int HatchRoundedBorder = 16;
        private const int HatchRoundedPeriod = 8; // chia hết cạnh và viền, để vân nối liền khi lặp
        private const int Samples = 4; // lấy mẫu 4×4 trong mỗi điểm ảnh để viền mịn

        private static Sprite _rounded;
        private static Sprite _circle;
        private static Sprite _hatchRounded;

        /// <summary>Khung bo góc trắng, 9 mảnh (<c>Image.Type.Sliced</c>): góc giữ nguyên khi kéo giãn.</summary>
        public static Sprite Rounded
        {
            get
            {
                if (_rounded == null)
                {
                    var tex = Draw("UiRounded", RoundedSize, (x, y) => InsideRounded(x, y, RoundedSize, CornerRadius));
                    _rounded = Sprite.Create(tex, new Rect(0, 0, RoundedSize, RoundedSize), new Vector2(.5f, .5f), 100f,
                        0, SpriteMeshType.FullRect, new Vector4(RoundedBorder, RoundedBorder, RoundedBorder, RoundedBorder));
                    _rounded.name = "UiRounded";
                }
                return _rounded;
            }
        }

        /// <summary>Hình tròn trắng.</summary>
        public static Sprite Circle
        {
            get
            {
                if (_circle == null)
                {
                    const float r = CircleSize / 2f;
                    var tex = Draw("UiCircle", CircleSize, (x, y) => (x - r) * (x - r) + (y - r) * (y - r) <= r * r);
                    _circle = Sprite.Create(tex, new Rect(0, 0, CircleSize, CircleSize), new Vector2(.5f, .5f));
                    _circle.name = "UiCircle";
                }
                return _circle;
            }
        }

        /// <summary>
        /// Khung bo góc tô vân gạch chéo màu mực, có viền 9 mảnh để dùng kiểu lặp (<c>Image.Type.Tiled</c>): góc giữ bo,
        /// vân lặp liền ở cạnh và giữa. Dùng cho bóng đổ, không cần mặt nạ (Mask).
        /// </summary>
        public static Sprite HatchRounded
        {
            get
            {
                if (_hatchRounded == null)
                {
                    var tex = Draw("UiHatchRounded", HatchRoundedSize, (x, y) =>
                        InsideRounded(x, y, HatchRoundedSize, CornerRadius) && Mathf.Repeat(x + y, HatchRoundedPeriod) < 1.6f,
                        Palette.Ink);
                    _hatchRounded = Sprite.Create(tex, new Rect(0, 0, HatchRoundedSize, HatchRoundedSize), new Vector2(.5f, .5f),
                        100f, 0, SpriteMeshType.FullRect,
                        new Vector4(HatchRoundedBorder, HatchRoundedBorder, HatchRoundedBorder, HatchRoundedBorder));
                    _hatchRounded.name = "UiHatchRounded";
                }
                return _hatchRounded;
            }
        }

        private static bool InsideRounded(float x, float y, int size, int radius)
        {
            var cx = Mathf.Clamp(x, radius, size - radius);
            var cy = Mathf.Clamp(y, radius, size - radius);
            return (x - cx) * (x - cx) + (y - cy) * (y - cy) <= radius * radius;
        }

        private static Texture2D Draw(string name, int n, System.Func<float, float, bool> inside,
            Color? color = null, TextureWrapMode wrap = TextureWrapMode.Clamp)
        {
            var c = (Color32)(color ?? Color.white);
            var pixels = new Color32[n * n];
            for (var y = 0; y < n; y++)
            {
                for (var x = 0; x < n; x++)
                {
                    var hits = 0;
                    for (var sy = 0; sy < Samples; sy++)
                    {
                        for (var sx = 0; sx < Samples; sx++)
                        {
                            if (inside(x + (sx + .5f) / Samples, y + (sy + .5f) / Samples)) hits++;
                        }
                    }
                    pixels[y * n + x] = new Color32(c.r, c.g, c.b, (byte)(255 * hits / (Samples * Samples)));
                }
            }

            var tex = new Texture2D(n, n, TextureFormat.RGBA32, false)
            {
                name = name,
                wrapMode = wrap,
                filterMode = FilterMode.Bilinear
            };
            tex.SetPixels32(pixels);
            tex.Apply(false, true);
            return tex;
        }
    }
}
