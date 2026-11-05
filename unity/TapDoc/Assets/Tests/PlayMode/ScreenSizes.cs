using System.Collections.Generic;
using UnityEngine;

namespace TapDoc.Tests
{
    /// <summary>Một cỡ máy thử: cỡ điểm ảnh (màn ngang), lề an toàn (điểm ảnh) và kiểu mong đợi.</summary>
    public readonly struct ScreenSize
    {
        public readonly string Name;
        public readonly Vector2Int Pixels;
        public readonly Insets Insets;
        public readonly bool Wide;

        public ScreenSize(string name, int width, int height, Insets insets, bool wide)
        {
            Name = name;
            Pixels = new Vector2Int(width, height);
            Insets = insets;
            Wide = wide;
        }

        public override string ToString() => $"{Name} {Pixels.x}x{Pixels.y}";
    }

    /// <summary>
    /// Các cỡ máy của bản thiết kế tỷ lệ màn hình (mục 4, 7). Test bố cục chạy qua tất cả; ảnh chụp lưu theo
    /// <see cref="ScreenSize.Name"/>.
    /// </summary>
    public static class ScreenSizes
    {
        public static readonly ScreenSize Phone20x9 = new("phone_20x9", 2400, 1080, Insets.None, true);
        public static readonly ScreenSize Phone20x9Camera = new("phone_20x9_cam", 2400, 1080, new Insets(110f, 0f, 0f, 0f), true);
        public static readonly ScreenSize IPhone = new("iphone", 2556, 1179, new Insets(177f, 177f, 63f, 0f), true);
        public static readonly ScreenSize Phone16x9 = new("phone_16x9", 1334, 750, Insets.None, true);
        public static readonly ScreenSize IPadAir = new("ipad_air", 2360, 1640, new Insets(0f, 0f, 40f, 0f), false);
        public static readonly ScreenSize IPad43 = new("ipad_43", 2048, 1536, Insets.None, false);
        public static readonly ScreenSize Tablet16x10 = new("tab_16x10", 2560, 1600, Insets.None, false);
        public static readonly ScreenSize TabletPortrait = new("tab_portrait", 1536, 2048, Insets.None, false);
        public static readonly ScreenSize Fold = new("fold", 2208, 1840, Insets.None, false);

        public static readonly IReadOnlyList<ScreenSize> All = new[]
        {
            Phone20x9, Phone20x9Camera, IPhone, Phone16x9, IPadAir, IPad43, Tablet16x10, TabletPortrait, Fold
        };

        /// <summary>
        /// Cỡ cho test đi hết mọi bài (rất nhiều bài × bước): màn rộng nhất, iPhone có tai thỏ, màn vừa đủ rộng, iPad có
        /// thanh vuốt, iPad 4:3. Máy tính bảng 16:10, xoay dọc, gập dùng cùng khung 1440×1080 như iPad 4:3.
        /// </summary>
        public static readonly IReadOnlyList<ScreenSize> LessonWalk = new[] { Phone20x9, IPhone, Phone16x9, IPadAir, IPad43 };

        /// <summary>
        /// Giả lập máy <paramref name="size"/>: lề an toàn, đích vẽ của camera giao diện, rồi tính lại khung màn.
        /// Trả RenderTexture để <see cref="Reset"/> huỷ.
        /// </summary>
        public static RenderTexture Apply(AppRoot app, ScreenSize size)
        {
            var insets = size.Insets;
            DeviceSafeArea.Override = _ => insets;
            var old = app.UiCamera.targetTexture;
            var rt = new RenderTexture(size.Pixels.x, size.Pixels.y, 24);
            app.UiCamera.targetTexture = rt;
            if (old != null) Object.Destroy(old);
            app.RefreshFrames();
            return rt;
        }

        /// <summary>Bỏ giả lập: lề của máy thật, camera vẽ ra màn hình.</summary>
        public static void Reset(AppRoot app, RenderTexture rt)
        {
            DeviceSafeArea.Override = null;
            if (app != null && app.UiCamera != null)
            {
                if (app.UiCamera.targetTexture == rt) app.UiCamera.targetTexture = null;
                app.RefreshFrames();
            }
            if (rt != null) Object.Destroy(rt);
        }
    }
}
