using System;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Lề an toàn của máy (tai thỏ, lỗ camera, góc bo, thanh vuốt), tính bằng điểm ảnh của đích vẽ. Mọi code đọc lề
    /// qua đây; test gán <see cref="Override"/> để giả lập máy có tai thỏ (Editor không có).
    /// </summary>
    public static class DeviceSafeArea
    {
        /// <summary>Hàm thay thế dùng trong test; <c>null</c> thì lấy từ hệ điều hành.</summary>
        public static Func<Vector2Int, Insets> Override;

        /// <summary>Lề cho đích vẽ cỡ <paramref name="pixels"/>.</summary>
        public static Insets For(Vector2Int pixels)
        {
            if (Override != null) return Override(pixels);
            var sw = Screen.width;
            var sh = Screen.height;
            if (sw <= 0 || sh <= 0) return Insets.None;

            // Lề của màn thật, quy theo tỷ lệ ra cỡ đích vẽ (đích vẽ có thể là RenderTexture trong test).
            var safe = Screen.safeArea;
            var fx = pixels.x / (float)sw;
            var fy = pixels.y / (float)sh;
            return new Insets(
                Mathf.Max(safe.xMin, 0f) * fx,
                Mathf.Max(sw - safe.xMax, 0f) * fx,
                Mathf.Max(safe.yMin, 0f) * fy,
                Mathf.Max(sh - safe.yMax, 0f) * fy);
        }
    }
}
