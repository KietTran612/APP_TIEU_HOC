using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Hình kí hiệu đặt ở đầu mục hoặc trên thẻ; không bấm được. Gồm kí hiệu của sách (● Em đọc, ⌂ Luyện tập)
    /// và ngôi sao phần thưởng (<see cref="CreateStar"/>).
    /// </summary>
    public class MarkerIcon : MonoBehaviour
    {
        /// <summary>Màu của ngôi sao vẽ thay khi thiếu tranh.</summary>
        internal static readonly Color StarYellow = new(1f, 0.78f, 0.1f, 1f);

        private static Sprite _fallbackStar;

        internal string ImageId { get; set; }

        /// <summary><c>true</c> khi thiếu tranh nên đang hiện hình vẽ thay.</summary>
        internal bool IsFallback { get; private set; }

        /// <summary>
        /// Ngôi sao phần thưởng cạnh <paramref name="size"/>, dùng chung cho màn kết quả và danh sách bài. Hiện tranh
        /// <see cref="SystemImages.Star"/>; thiếu tranh thì vẽ ngôi sao năm cánh màu vàng, không vẽ ô vuông. Font của
        /// app (Andika) không có kí tự "★", nên ngôi sao thay thế là hình vẽ chứ không phải chữ.
        /// </summary>
        internal static MarkerIcon CreateStar(Transform parent, AssetCatalog assets, float size)
        {
            var go = new GameObject("Star", typeof(RectTransform), typeof(Image), typeof(MarkerIcon));
            go.transform.SetParent(parent, false);
            ((RectTransform)go.transform).sizeDelta = new Vector2(size, size);

            var sprite = assets?.Image(SystemImages.Star);
            var img = go.GetComponent<Image>();
            img.sprite = sprite != null ? sprite : FallbackStar;
            img.color = sprite != null ? Color.white : StarYellow;
            img.preserveAspect = true;
            img.raycastTarget = false;

            var icon = go.GetComponent<MarkerIcon>();
            icon.ImageId = SystemImages.Star;
            icon.IsFallback = sprite == null;
            return icon;
        }

        /// <summary>Ngôi sao năm cánh màu trắng trên nền trong suốt; tô màu bằng <see cref="Graphic.color"/>.</summary>
        internal static Sprite FallbackStar
        {
            get
            {
                if (_fallbackStar == null) _fallbackStar = DrawStar(128);
                return _fallbackStar;
            }
        }

        private static Sprite DrawStar(int n)
        {
            // 10 đỉnh xen kẽ: đầu cánh và góc trong; cánh đầu tiên chĩa lên.
            var points = new Vector2[10];
            var center = new Vector2(n / 2f, n / 2f);
            var outer = n * 0.48f;
            var inner = outer * 0.42f;
            for (var i = 0; i < points.Length; i++)
            {
                var r = i % 2 == 0 ? outer : inner;
                var a = Mathf.PI / 2f + i * Mathf.PI / 5f;
                points[i] = center + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * r;
            }

            const int samples = 4; // lấy mẫu 4×4 trong mỗi điểm ảnh để viền mịn
            var pixels = new Color32[n * n];
            for (var y = 0; y < n; y++)
            {
                for (var x = 0; x < n; x++)
                {
                    var hits = 0;
                    for (var sy = 0; sy < samples; sy++)
                    {
                        for (var sx = 0; sx < samples; sx++)
                        {
                            var p = new Vector2(x + (sx + .5f) / samples, y + (sy + .5f) / samples);
                            if (Inside(points, p)) hits++;
                        }
                    }
                    pixels[y * n + x] = new Color32(255, 255, 255, (byte)(255 * hits / (samples * samples)));
                }
            }

            var tex = new Texture2D(n, n, TextureFormat.RGBA32, false)
            {
                name = "FallbackStar",
                wrapMode = TextureWrapMode.Clamp,
                filterMode = FilterMode.Bilinear
            };
            tex.SetPixels32(pixels);
            tex.Apply(false, true);
            var sprite = Sprite.Create(tex, new Rect(0, 0, n, n), new Vector2(.5f, .5f));
            sprite.name = "FallbackStar";
            return sprite;
        }

        /// <summary>Điểm <paramref name="p"/> nằm trong đa giác <paramref name="poly"/> (quy tắc chẵn lẻ).</summary>
        private static bool Inside(Vector2[] poly, Vector2 p)
        {
            var inside = false;
            for (int i = 0, j = poly.Length - 1; i < poly.Length; j = i++)
            {
                if ((poly[i].y > p.y) != (poly[j].y > p.y) &&
                    p.x < (poly[j].x - poly[i].x) * (p.y - poly[i].y) / (poly[j].y - poly[i].y) + poly[i].x)
                {
                    inside = !inside;
                }
            }
            return inside;
        }
    }
}
