using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace TapDoc
{
    /// <summary>
    /// Gợi ý chơi cùng con ngoài màn hình, sinh từ bài bé vừa học (bản thiết kế nâng cấp UI mục 4.6; N5, N8: học cùng
    /// bố mẹ, gắn với bài). Câu theo mẫu trong <see cref="UiText"/>; phụ huynh đọc, không có tiếng.
    /// </summary>
    public static class ParentSuggestions
    {
        public const int Max = 3;
        private static readonly Regex Tags = new("<[^>]+>");

        /// <summary>Tối đa <see cref="Max"/> gợi ý cho bài <paramref name="entry"/>; chưa học bài nào thì một câu mời.</summary>
        public static List<string> For(LessonEntry entry, Lesson lesson)
        {
            var result = new List<string>();
            if (entry == null)
            {
                result.Add(UiText.PlayNone);
                return result;
            }
            var title = Plain(entry.title);
            var type = entry.type ?? string.Empty;
            var grade1 = entry.EffectiveGrade == 1;
            var soundLesson = grade1 && (type == "am_moi" || type == "van_moi" || type == "dau_thanh" || type.StartsWith("on_tap"));
            var units = soundLesson ? Units(title) : new List<string>();
            if (units.Count > 0 && !type.StartsWith("on_tap") && type != "dau_thanh")
                result.Add(string.Format(UiText.PlayFindSound, string.Join(", ", units)));
            var keyword = lesson?.part1?.FirstOrDefault(s => (s.type == "keyword" || s.type == "picture")
                && !string.IsNullOrEmpty(s.text));
            if (keyword != null) result.Add(string.Format(UiText.PlayActWord, Plain(keyword.text)));
            if (units.Count > 0 && !type.StartsWith("on_tap")) result.Add(string.Format(UiText.PlayWriteSalt, units[0]));
            if (!soundLesson && !string.IsNullOrEmpty(title)) result.Add(string.Format(UiText.PlayReadAgain, title));
            if (result.Count == 0) result.Add(string.Format(UiText.PlayReadAgain, title));
            return result.Take(Max).ToList();
        }

        /// <summary>Các âm, vần của bài (tên bài "u ư" thành "u", "ư").</summary>
        private static List<string> Units(string title) =>
            string.IsNullOrEmpty(title) ? new List<string>() : title.Split(' ').Where(u => u.Length > 0 && u.Length <= 5).ToList();

        private static string Plain(string text) => string.IsNullOrEmpty(text) ? text ?? string.Empty : Tags.Replace(text, string.Empty).Trim();
    }
}
