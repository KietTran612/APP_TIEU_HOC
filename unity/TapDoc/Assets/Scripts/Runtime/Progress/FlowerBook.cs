using System.Collections.Generic;

namespace TapDoc
{
    /// <summary>
    /// Phần tính toán của Sổ bé ngoan: mỗi bài một trang, trang tính từ 0 theo thứ tự danh sách bài
    /// (<c>ordered</c>). Hai trang liền nhau tạo thành một cặp trang mở ra cùng lúc (trang chẵn bên trái).
    /// Mỗi bài có tối đa <see cref="FlowersPerLesson"/> bông hoa, bằng số sao trong <see cref="ProgressStore"/>.
    /// </summary>
    public static class FlowerBook
    {
        public const int FlowersPerLesson = ProgressStore.MaxStars;

        /// <summary>Số hoa của bài với bé đang học: bằng số sao; 0 khi chưa học xong hoặc không có kho.</summary>
        public static int FlowersFor(ProgressStore p, string lessonId) => p?.StarsFor(lessonId) ?? 0;

        /// <summary>Trang của bài trong <paramref name="ordered"/>; −1 khi bài không có trong danh sách.</summary>
        public static int PageOf(IReadOnlyList<string> ordered, string lessonId)
        {
            if (ordered == null || string.IsNullOrEmpty(lessonId)) return -1;
            for (var i = 0; i < ordered.Count; i++)
            {
                if (ordered[i] == lessonId) return i;
            }
            return -1;
        }

        /// <summary>Trang bên trái của cặp trang chứa <paramref name="page"/>.</summary>
        public static int SpreadStart(int page) => page - page % 2;

        /// <summary>
        /// Trang mở sổ: trang của bài đứng sau cùng trong <paramref name="ordered"/> trong số các bài bé đã học xong
        /// (theo thứ tự danh sách, không theo thứ tự bé học). Chưa học xong bài nào thì 0.
        /// </summary>
        public static int StartPage(ProgressStore p, IReadOnlyList<string> ordered)
        {
            if (p == null || ordered == null) return 0;
            for (var i = ordered.Count - 1; i >= 0; i--)
            {
                if (p.IsCompleted(ordered[i])) return i;
            }
            return 0;
        }

        /// <summary>Hình bông hoa ở ô <paramref name="slot"/> của bài; tạm thời mọi ô dùng chung một hình.</summary>
        public static string FlowerImage(string lessonId, int slot) =>
            SystemImages.Flower;
    }
}
