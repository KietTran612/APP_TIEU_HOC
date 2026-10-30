using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Bảng màu của app theo phong cách tranh SGK 1990 (bản thiết kế giao diện mục 4.1). Code màn không viết mã màu
    /// trực tiếp mà lấy từ đây.
    /// </summary>
    public static class Palette
    {
        /// <summary>Mực: viền, nét, chữ.</summary>
        public static readonly Color Ink = Hex("#2B2621");

        /// <summary>Giấy ngà: nền màn.</summary>
        public static readonly Color Paper = Hex("#F6EEDB");

        /// <summary>Giấy sáng: nền thẻ, khung tranh, trang sổ.</summary>
        public static readonly Color PaperLight = Hex("#FBF6E9");

        /// <summary>Lam ngọc: nút chính, chấm tiến độ đã qua.</summary>
        public static readonly Color Teal = Hex("#2F8C9B");

        /// <summary>Lam ngọc nhạt: viền ô hoa trong sổ, nền phụ.</summary>
        public static readonly Color TealLight = Hex("#A9D4D6");

        /// <summary>Cam: nút "Tiếp", chấm tiến độ đang làm.</summary>
        public static readonly Color Orange = Hex("#EF9D4F");

        /// <summary>Cam nhạt: thẻ đang được đọc, bài đang học tới.</summary>
        public static readonly Color OrangeLight = Hex("#F8D3A6");

        /// <summary>Vàng gợi ý: thẻ gợi ý khi bé sai lần hai.</summary>
        public static readonly Color HintYellow = Hex("#F4C54A");

        /// <summary>Đỏ son: chỉ dùng cho con dấu "Bé ngoan".</summary>
        public static readonly Color StampRed = Hex("#D0453B");

        /// <summary>Nền của bài chưa mở.</summary>
        public static readonly Color LockedFill = Hex("#E9E1CC");

        /// <summary>Viền và chữ của bài chưa mở.</summary>
        public static readonly Color LockedInk = Hex("#B5AA93");

        /// <summary>Màu từ chuỗi <c>#RRGGBB</c> (không có alpha thì alpha = 1).</summary>
        public static Color Hex(string hex)
        {
            if (!ColorUtility.TryParseHtmlString(hex, out var color))
            {
                throw new System.ArgumentException($"Mã màu sai: {hex}", nameof(hex));
            }
            return color;
        }
    }
}
