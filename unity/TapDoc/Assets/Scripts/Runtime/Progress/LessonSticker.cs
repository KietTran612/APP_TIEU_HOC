using System.Linq;
using System.Text.RegularExpressions;

namespace TapDoc
{
    /// <summary>
    /// Tem bài học dán vào Sổ bé ngoan (bản thiết kế nâng cấp UI mục 4.3): tranh của bài, gợi lại bài đã học. Chọn tranh
    /// theo thứ tự: tranh của bước từ khoá/tranh; tranh đầu tiên ở bất kỳ bước phần 1; tranh đầu tiên ở phần 2 (tranh
    /// lượt, rồi tranh phương án). Bài không có tranh nào: tem là tên bài viết to.
    /// </summary>
    public static class LessonSticker
    {
        private static readonly Regex Tags = new("<[^>]+>");

        /// <summary>Mã tranh của tem (<c>null</c> nếu bài không có tranh) và chữ dưới tem.</summary>
        public static (string image, string caption) For(Lesson lesson, string fallbackTitle = null)
        {
            var title = Plain(fallbackTitle ?? lesson?.title);
            if (lesson == null) return (null, title);
            var steps = lesson.part1 ?? new System.Collections.Generic.List<Step>();
            var keyword = steps.FirstOrDefault(s => (s.type == "keyword" || s.type == "picture") && !string.IsNullOrEmpty(s.image));
            if (keyword != null)
            {
                var text = Plain(keyword.text);
                return (keyword.image, string.IsNullOrEmpty(text) ? title : text);
            }
            var anyStep = steps.FirstOrDefault(s => !string.IsNullOrEmpty(s.image));
            if (anyStep != null) return (anyStep.image, title);
            foreach (var round in lesson.part2 ?? new System.Collections.Generic.List<Round>())
            {
                if (!string.IsNullOrEmpty(round.image)) return (round.image, title);
                var option = round.options?.FirstOrDefault(o => !string.IsNullOrEmpty(o.image));
                if (option != null) return (option.image, title);
            }
            return (null, title);
        }

        private static string Plain(string text) => string.IsNullOrEmpty(text) ? text : Tags.Replace(text, string.Empty).Trim();
    }
}
