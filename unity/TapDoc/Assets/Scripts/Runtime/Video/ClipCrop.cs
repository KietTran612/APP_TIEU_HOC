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
        /// Số điểm ảnh app bỏ thêm ở mỗi mép phần tranh. Đo 19/11: 37/327 clip Flow có 3 hàng đen ở mép trên và mép dưới
        /// phần vuông (tranh tĩnh không có); bỏ 4 điểm ảnh (trên 720) thì che hết, tranh trong clip chỉ to hơn tranh tĩnh
        /// khoảng 1,1%.
        /// </summary>
        public const int EdgeInsetPx = 4;

        /// <summary>
        /// <c>RawImage.uvRect</c> lấy phần giữa clip <paramref name="clipWidth"/>×<paramref name="clipHeight"/> có tỉ lệ
        /// rộng/cao bằng <paramref name="pictureAspect"/>, bỏ thêm <paramref name="edgeInsetPx"/> điểm ảnh ở cạnh ngắn
        /// (giữ nguyên tỉ lệ). Thiếu cỡ hay tỉ lệ thì lấy cả clip; phần bỏ quá lớn (từ một phần tư cạnh) thì không bỏ.
        /// </summary>
        public static Rect UvRect(int clipWidth, int clipHeight, float pictureAspect, int edgeInsetPx = 0)
        {
            if (clipWidth <= 0 || clipHeight <= 0 || pictureAspect <= 0f) return new Rect(0f, 0f, 1f, 1f);
            var clipAspect = (float)clipWidth / clipHeight;
            var w = Mathf.Min(1f, pictureAspect / clipAspect);
            var h = Mathf.Min(1f, clipAspect / pictureAspect);
            var shorter = Mathf.Min(w * clipWidth, h * clipHeight);
            if (edgeInsetPx > 0 && 2f * edgeInsetPx < shorter / 2f)
            {
                var keep = 1f - 2f * edgeInsetPx / shorter;
                w *= keep;
                h *= keep;
            }
            return new Rect((1f - w) / 2f, (1f - h) / 2f, w, h);
        }
    }
}
