using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Phần của clip cần hiện: tranh vuông được đệm giấy hai bên thành 16:9 và đặt giữa khung, nên app chỉ lấy phần ở
    /// giữa có cùng tỉ lệ với tranh tĩnh (thiết kế tranh động mục 7).
    /// </summary>
    public static class ClipCrop
    {
        /// <summary>
        /// <c>RawImage.uvRect</c> lấy phần giữa clip <paramref name="clipWidth"/>×<paramref name="clipHeight"/> có tỉ lệ
        /// rộng/cao bằng <paramref name="pictureAspect"/>. Thiếu cỡ hay tỉ lệ thì lấy cả clip.
        /// </summary>
        public static Rect UvRect(int clipWidth, int clipHeight, float pictureAspect)
        {
            if (clipWidth <= 0 || clipHeight <= 0 || pictureAspect <= 0f) return new Rect(0f, 0f, 1f, 1f);
            var clipAspect = (float)clipWidth / clipHeight;
            var w = Mathf.Min(1f, pictureAspect / clipAspect);
            var h = Mathf.Min(1f, clipAspect / pictureAspect);
            return new Rect((1f - w) / 2f, (1f - h) / 2f, w, h);
        }
    }
}
