using System;
using System.Collections.Generic;

namespace TapDoc
{
    /// <summary>
    /// Phiên "Ôn lại": một bài tạm chỉ có Phần 2, gồm đúng các lượt bé đã nhầm (nhầm nhiều trước), nạp lại từ bài gốc.
    /// Lượt không còn dùng được (bài không nạp được, chỉ số lượt không còn, lượt hỏng) bị xóa khỏi danh sách nhầm
    /// và bỏ qua, không làm hỏng phiên ôn.
    /// </summary>
    public class ReviewSession
    {
        /// <summary><c>lesson_id</c> của bài tạm; màn kết quả không ghi bài này là đã học.</summary>
        public const string LessonId = "on_lai";

        public const int MaxRounds = 8;

        private ReviewSession(Lesson lesson, List<(string lessonId, int round)> sources)
        {
            Lesson = lesson;
            Sources = sources;
        }

        public Lesson Lesson { get; }

        /// <summary>Lượt thứ k của <see cref="Lesson"/> là lượt <c>Sources[k].round</c> của bài <c>Sources[k].lessonId</c>.</summary>
        public List<(string lessonId, int round)> Sources { get; }

        /// <summary>
        /// Lấy tối đa <see cref="MaxRounds"/> lượt còn dùng được theo thứ tự <see cref="ProgressStore.Mistakes"/>.
        /// Mọi lượt lỗi thời gặp phải đều bị <see cref="ProgressStore.ClearMistake"/>; người gọi lưu kho sau đó.
        /// </summary>
        public static ReviewSession Build(ProgressStore store, Func<string, Lesson> load)
        {
            if (store == null) throw new ArgumentNullException(nameof(store));
            if (load == null) throw new ArgumentNullException(nameof(load));

            var lesson = new Lesson
            {
                lesson_id = LessonId,
                title = UiText.ReviewMistakes,
                part1 = new List<Step>(),
                part2 = new List<Round>()
            };
            var sources = new List<(string lessonId, int round)>();
            var loaded = new Dictionary<string, Lesson>();

            // Duyệt hết danh sách nhầm (đã sắp xếp) để dọn mọi lượt lỗi thời; chỉ lấy đủ MaxRounds lượt dùng được.
            foreach (var mistake in store.Mistakes(int.MaxValue))
            {
                var round = FindRound(mistake, load, loaded);
                if (round == null)
                {
                    store.ClearMistake(mistake.lesson_id, mistake.round);
                    continue;
                }
                if (lesson.part2.Count >= MaxRounds) continue;
                lesson.part2.Add(round);
                sources.Add((mistake.lesson_id, mistake.round));
            }

            return new ReviewSession(lesson, sources);
        }

        private static Round FindRound(Mistake mistake, Func<string, Lesson> load, Dictionary<string, Lesson> loaded)
        {
            if (!loaded.TryGetValue(mistake.lesson_id, out var source))
            {
                try
                {
                    source = load(mistake.lesson_id);
                }
                catch (Exception)
                {
                    // Bài không còn hoặc hỏng: lượt nhầm của bài này lỗi thời.
                    source = null;
                }
                loaded[mistake.lesson_id] = source;
            }

            if (source?.part2 == null || mistake.round < 0 || mistake.round >= source.part2.Count) return null;
            var round = source.part2[mistake.round];
            if (round?.options == null || round.answer < 0 || round.answer >= round.options.Count) return null;
            return round;
        }
    }
}
