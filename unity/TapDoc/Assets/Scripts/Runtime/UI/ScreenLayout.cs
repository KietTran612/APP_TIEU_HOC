using UnityEngine;

namespace TapDoc
{
    /// <summary>Lề bị tai thỏ, lỗ camera, góc bo hay thanh vuốt che, tính theo từng mép.</summary>
    public readonly struct Insets
    {
        public readonly float Left;
        public readonly float Right;
        public readonly float Bottom;
        public readonly float Top;

        public static readonly Insets None = new(0f, 0f, 0f, 0f);

        public Insets(float left, float right, float bottom, float top)
        {
            Left = left;
            Right = right;
            Bottom = bottom;
            Top = top;
        }
    }

    /// <summary>
    /// Các khung màn của một cỡ máy, tính bằng đơn vị canvas, gốc ở góc dưới trái canvas (bản thiết kế tỷ lệ màn
    /// hình mục 5).
    /// </summary>
    public readonly struct ScreenFrames
    {
        /// <summary>Cỡ canvas.</summary>
        public readonly Vector2 Canvas;

        /// <summary>Vùng không bị máy che; lề hai bên đối xứng.</summary>
        public readonly Rect Safe;

        /// <summary>Khung các màn của bé: rộng hết vùng an toàn ở kiểu mép, 1440 ở kiểu góc; cao tối đa 1080.</summary>
        public readonly Rect Kid;

        /// <summary>Khung chuẩn 1440 (màn người lớn, màn chuẩn bị), đặt giữa vùng an toàn.</summary>
        public readonly Rect Standard;

        /// <summary>Màn đủ rộng để nút của bé dạt ra hai mép (kiểu mép).</summary>
        public readonly bool Wide;

        public ScreenFrames(Vector2 canvas, Rect safe, Rect kid, Rect standard, bool wide)
        {
            Canvas = canvas;
            Safe = safe;
            Kid = kid;
            Standard = standard;
            Wide = wide;
        }

        /// <summary>Cùng khung (sai số 0,01 đơn vị canvas).</summary>
        public bool Same(ScreenFrames other) =>
            Wide == other.Wide && Near(Canvas, other.Canvas) && Near(Safe, other.Safe) && Near(Kid, other.Kid) &&
            Near(Standard, other.Standard);

        private static bool Near(Vector2 a, Vector2 b) => Mathf.Abs(a.x - b.x) < .01f && Mathf.Abs(a.y - b.y) < .01f;

        private static bool Near(Rect a, Rect b) => Near(a.position, b.position) && Near(a.size, b.size);
    }

    /// <summary>
    /// Tính khung màn theo cỡ máy (bản thiết kế tỷ lệ màn hình mục 5): canvas mở rộng quanh khung 1440×1080, vùng an
    /// toàn của máy, chọn kiểu góc hay kiểu mép cho các màn của bé.
    /// </summary>
    public static class ScreenLayout
    {
        /// <summary>Khung chuẩn: canvas luôn chứa trọn khung này.</summary>
        public static readonly Vector2 Frame = new(1440f, 1080f);

        /// <summary>Cỡ thiết kế của phần học (Stage); các bước học dựng theo cỡ này.</summary>
        public static readonly Vector2 StageSize = new(1400f, 680f);

        /// <summary>Dải mép ở kiểu mép: lề + nút tròn + lề.</summary>
        public const float SideBand = 200f;

        /// <summary>Dải trên của phần học ở kiểu mép (hàng chấm tiến độ).</summary>
        public const float WideTopBand = 70f;

        /// <summary>Lề dưới của phần học ở kiểu mép.</summary>
        public const float WideBottom = 20f;

        /// <summary>Kiểu mép chỉ dùng khi phần học to thêm ít nhất chừng này lần.</summary>
        public const float WideMinGain = 1.05f;

        /// <summary>Số điểm ảnh cho một đơn vị canvas: canvas mở rộng (Expand) quanh <see cref="Frame"/>.</summary>
        public static float CanvasScale(Vector2Int pixels) => Mathf.Min(pixels.x / Frame.x, pixels.y / Frame.y);

        /// <summary>Mức phóng to phần học nếu đặt nút ở hai dải mép của khung cỡ <paramref name="frame"/>.</summary>
        public static float WideStageScale(Vector2 frame) =>
            Mathf.Min((frame.x - 2f * SideBand) / StageSize.x, (frame.y - WideTopBand - WideBottom) / StageSize.y);

        /// <summary>Khung có cỡ <paramref name="frameSize"/> là khung kiểu mép (rộng hơn khung chuẩn).</summary>
        public static bool IsWide(Vector2 frameSize) => frameSize.x > Frame.x + .5f;

        public static ScreenFrames Compute(Vector2Int pixels, Insets pixelInsets)
        {
            var scale = CanvasScale(pixels);
            if (scale <= 0f) scale = 1f;
            var canvas = new Vector2(pixels.x / scale, pixels.y / scale);

            // Lề ngang lấy đối xứng theo bên lớn hơn để nội dung luôn cân giữa màn; lề dọc lấy đúng từng bên.
            var side = Mathf.Max(Mathf.Max(pixelInsets.Left, pixelInsets.Right), 0f) / scale;
            var bottom = Mathf.Max(pixelInsets.Bottom, 0f) / scale;
            var top = Mathf.Max(pixelInsets.Top, 0f) / scale;
            var safe = new Rect(side, bottom, canvas.x - 2f * side, canvas.y - bottom - top);

            var height = Mathf.Min(safe.height, Frame.y);
            var y = safe.y + (safe.height - height) / 2f;
            var wide = WideStageScale(new Vector2(safe.width, height)) >= WideMinGain;
            var standardWidth = Mathf.Min(Frame.x, safe.width);
            var kidWidth = wide ? safe.width : standardWidth;

            return new ScreenFrames(canvas, safe,
                new Rect(safe.center.x - kidWidth / 2f, y, kidWidth, height),
                new Rect(safe.center.x - standardWidth / 2f, y, standardWidth, height),
                wide);
        }
    }
}
