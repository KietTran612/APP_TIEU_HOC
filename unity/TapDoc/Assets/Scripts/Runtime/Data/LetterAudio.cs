using System.Collections.Generic;

namespace TapDoc
{
    /// <summary>
    /// File âm thanh của từng cách đọc một chữ, gom từ bước giới thiệu chữ (<c>unit</c>) của các bài: chữ có nhiều
    /// cách đọc lấy theo <see cref="Step.readings"/>, chữ chỉ có một cách đọc thì mọi cách đọc dùng chung
    /// <see cref="Step.audio"/>. Dùng cho bảng chữ cái ở mục "Chú ý và Phụ lục".
    /// </summary>
    public sealed class LetterAudio
    {
        public const string Learn = "hoc";
        public const string Sound = "chuan";
        public const string LetterName = "tenchu";

        private static readonly string[] Kinds = { Learn, Sound, LetterName };

        private readonly Dictionary<(string letter, string kind), string> _audio = new();

        public static LetterAudio FromLessons(IEnumerable<Lesson> lessons)
        {
            var result = new LetterAudio();
            foreach (var lesson in lessons)
            {
                if (lesson?.part1 == null) continue;
                foreach (var step in lesson.part1)
                {
                    if (step?.type != "unit" || string.IsNullOrEmpty(step.text)) continue;
                    if (step.readings.Count == 0)
                    {
                        foreach (var kind in Kinds) result.Add(step.text, kind, step.audio);
                        continue;
                    }
                    foreach (var reading in step.readings)
                    foreach (var kind in reading.kinds)
                        result.Add(step.text, kind, reading.audio);
                }
            }
            return result;
        }

        /// <summary>Mã âm thanh của cách đọc <paramref name="kind"/> của chữ; <c>null</c> khi không bài nào dạy chữ đó.</summary>
        public string Of(string letter, string kind) =>
            letter != null && _audio.TryGetValue((letter, kind), out var id) ? id : null;

        private void Add(string letter, string kind, string audio)
        {
            if (!string.IsNullOrEmpty(audio)) _audio.TryAdd((letter, kind), audio);
        }
    }
}
