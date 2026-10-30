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
        private const int HatchSize = 12;
        private const int Samples = 4; // lấy mẫu 4×4 trong mỗi điểm ảnh để viền mịn

        private static Sprite _rounded;
        private static Sprite _circle;
        private static Sprite _hatch;

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

        /// <summary>Vân gạch chéo màu mực trên nền trong suốt, lặp được (<c>Image.Type.Tiled</c>).</summary>
        public static Sprite Hatch
        {
            get
            {
                if (_hatch == null)
                {
                    // Nét chéo 45° dày khoảng 2 điểm ảnh, cách nhau HatchSize: khớp mép khi lặp.
                    var tex = Draw("UiHatch", HatchSize, (x, y) =>
                    {
                        var d = Mathf.Repeat(x + y, HatchSize);
                        return d < 2.2f;
                    }, Palette.Ink, TextureWrapMode.Repeat);
                    _hatch = Sprite.Create(tex, new Rect(0, 0, HatchSize, HatchSize), new Vector2(.5f, .5f));
                    _hatch.name = "UiHatch";
                }
                return _hatch;
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
