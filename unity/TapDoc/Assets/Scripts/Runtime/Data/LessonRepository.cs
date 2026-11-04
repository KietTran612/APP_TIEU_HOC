using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Kho bài: đọc danh sách bài, bài học và Phụ lục qua <see cref="IContentSource"/>, giữ trong bộ nhớ đệm đến khi app
    /// tắt (chỉ là chữ, rất nhẹ). Bản có chờ (<c>…Async</c>) dùng khi chuẩn bị màn; <see cref="Get"/>,
    /// <see cref="Index"/>, <see cref="Appendix"/> trả ngay từ bộ nhớ đệm, chưa có thì nạp ngay và cảnh báo một lần.
    /// </summary>
    public sealed class LessonRepository
    {
        private static readonly string IndexName = ContentPaths.PathOf(ContentKind.LessonIndex, null);

        private readonly IContentSource _source;
        private readonly Dictionary<string, Lesson> _lessons = new();
        private readonly Dictionary<string, Appendix> _appendices = new();
        private readonly HashSet<string> _warned = new();
        private LessonIndex _index;

        public LessonRepository(IContentSource source)
        {
            _source = source ?? throw new ArgumentNullException(nameof(source));
        }

        public LessonIndex Index
        {
            get
            {
                if (_index == null)
                {
                    WarnUnprepared(IndexName);
                    _index = ParseIndex(_source.Load(ContentKind.LessonIndex, null) as TextAsset);
                }
                return _index;
            }
        }

        public async Awaitable<LessonIndex> LoadIndexAsync()
        {
            _index ??= ParseIndex(await _source.LoadAsync(ContentKind.LessonIndex, null) as TextAsset);
            return _index;
        }

        public Lesson Get(string lessonId)
        {
            CheckId(lessonId);
            if (_lessons.TryGetValue(lessonId, out var lesson)) return lesson;
            WarnUnprepared(lessonId);
            return _lessons[lessonId] = ParseLesson(_source.Load(ContentKind.Lesson, lessonId) as TextAsset, lessonId);
        }

        public async Awaitable<Lesson> LoadAsync(string lessonId)
        {
            CheckId(lessonId);
            if (_lessons.TryGetValue(lessonId, out var lesson)) return lesson;
            var asset = await _source.LoadAsync(ContentKind.Lesson, lessonId) as TextAsset;
            if (_lessons.TryGetValue(lessonId, out lesson)) return lesson; // một lời gọi khác đã nạp xong trước
            return _lessons[lessonId] = ParseLesson(asset, lessonId);
        }

        /// <summary>
        /// Nạp đủ các bài trong danh sách, cùng lúc (màn Phụ huynh cần chữ của cả quyển). Bài thiếu hay hỏng thì báo lỗi
        /// rồi bỏ qua, không chặn các bài khác.
        /// </summary>
        public async Awaitable LoadAllAsync()
        {
            var index = await LoadIndexAsync();
            var pending = new List<Awaitable<Lesson>>();
            foreach (var entry in index.lessons)
            {
                if (entry != null && !_lessons.ContainsKey(entry.lesson_id)) pending.Add(LoadAsync(entry.lesson_id));
            }
            foreach (var load in pending)
            {
                try
                {
                    await load;
                }
                catch (InvalidDataException ex)
                {
                    Debug.LogError($"[TapDoc] {ex.Message}");
                }
            }
        }

        /// <summary>Phụ lục cuối sách của <paramref name="book"/>.</summary>
        public Appendix Appendix(string book)
        {
            if (string.IsNullOrWhiteSpace(book)) throw new InvalidDataException("Mã sách rỗng");
            if (_appendices.TryGetValue(book, out var appendix)) return appendix;
            WarnUnprepared(book);
            return _appendices[book] = AppendixData.Parse(_source.Load(ContentKind.Appendix, book) as TextAsset, book);
        }

        public async Awaitable<Appendix> LoadAppendixAsync(string book)
        {
            if (string.IsNullOrWhiteSpace(book)) throw new InvalidDataException("Mã sách rỗng");
            if (_appendices.TryGetValue(book, out var appendix)) return appendix;
            var asset = await _source.LoadAsync(ContentKind.Appendix, book) as TextAsset;
            if (_appendices.TryGetValue(book, out appendix)) return appendix;
            return _appendices[book] = AppendixData.Parse(asset, book);
        }

        private void WarnUnprepared(string id)
        {
            if (_warned.Add(id)) Debug.LogWarning($"[TapDoc] Chưa chuẩn bị trước: {id}");
        }

        private static void CheckId(string lessonId)
        {
            if (string.IsNullOrWhiteSpace(lessonId))
            {
                throw new InvalidDataException($"Mã bài học rỗng: {lessonId}");
            }
        }

        private static LessonIndex ParseIndex(TextAsset asset)
        {
            if (asset == null || string.IsNullOrWhiteSpace(asset.text))
            {
                throw new InvalidDataException("Không tìm thấy hoặc hỏng lessons/index.json");
            }

            LessonIndex index;
            try
            {
                index = JsonUtility.FromJson<LessonIndex>(asset.text);
            }
            catch (Exception ex)
            {
                throw new InvalidDataException("Dữ liệu lessons/index.json không hợp lệ", ex);
            }

            if (index == null)
            {
                throw new InvalidDataException("Dữ liệu lessons/index.json rỗng");
            }

            index.lessons ??= new List<LessonEntry>();
            foreach (var entry in index.lessons)
            {
                if (entry == null) continue;
                entry.lesson_id = Nfc(entry.lesson_id);
                entry.title = Nfc(entry.title);
                entry.type = Nfc(entry.type);
                entry.book = Nfc(entry.book);
            }

            return index;
        }

        private static Lesson ParseLesson(TextAsset asset, string lessonId)
        {
            if (asset == null || string.IsNullOrWhiteSpace(asset.text))
            {
                throw new InvalidDataException($"Không tìm thấy bài học: {lessonId}");
            }

            var lesson = Parse(asset.text, lessonId);
            if (string.IsNullOrEmpty(lesson.lesson_id))
            {
                throw new InvalidDataException($"Bài {lessonId}: dữ liệu bài học hỏng (thiếu lesson_id)");
            }
            return lesson;
        }

        /// <summary>
        /// Như <see cref="Parse(string)"/>, nhưng mọi lỗi được bọc thành <see cref="InvalidDataException"/>
        /// có mã bài ở đầu thông điệp, để biết ngay file nào hỏng.
        /// </summary>
        internal static Lesson Parse(string json, string lessonId)
        {
            try
            {
                return Parse(json);
            }
            catch (Exception ex)
            {
                throw new InvalidDataException($"Bài {lessonId}: {ex.Message}", ex);
            }
        }

        public static Lesson Parse(string json)
        {
            if (string.IsNullOrWhiteSpace(json))
            {
                throw new InvalidDataException("Chuỗi JSON bài học rỗng");
            }

            Lesson lesson;
            try
            {
                lesson = JsonUtility.FromJson<Lesson>(json);
            }
            catch (Exception ex)
            {
                throw new InvalidDataException($"JSON bài học không hợp lệ: {ex.Message}", ex);
            }

            if (lesson == null)
            {
                throw new InvalidDataException("Không phân tích được đối tượng Lesson từ JSON");
            }

            NormalizeLesson(lesson);
            return lesson;
        }

        internal static string Nfc(string value) =>
            string.IsNullOrEmpty(value) ? value : value.Normalize(NormalizationForm.FormC);

        private static void NormalizeLesson(Lesson lesson)
        {
            lesson.lesson_id = Nfc(lesson.lesson_id);
            lesson.book = Nfc(lesson.book);
            lesson.type = Nfc(lesson.type);
            lesson.title = Nfc(lesson.title);

            lesson.notes ??= new List<LessonNote>();
            foreach (var note in lesson.notes)
            {
                if (note == null) continue;
                note.kind = Nfc(note.kind);
                note.text = Nfc(note.text);
            }

            lesson.new_units ??= new List<string>();
            for (var i = 0; i < lesson.new_units.Count; i++)
            {
                lesson.new_units[i] = Nfc(lesson.new_units[i]);
            }

            if (lesson.source != null)
            {
                lesson.source.pages ??= new List<int>();
                lesson.source.scan_file = Nfc(lesson.source.scan_file);
                lesson.source.verification = Nfc(lesson.source.verification);
            }

            if (lesson.review != null)
            {
                lesson.review.status = Nfc(lesson.review.status);
                lesson.review.can_duyet ??= new List<ReviewNote>();
                foreach (var note in lesson.review.can_duyet)
                {
                    if (note == null) continue;
                    note.where = Nfc(note.where);
                    note.note = Nfc(note.note);
                }
            }

            lesson.part1 ??= new List<Step>();
            foreach (var step in lesson.part1)
            {
                if (step == null) continue;
                step.type = Nfc(step.type);
                step.text = Nfc(step.text);
                step.audio = Nfc(step.audio);
                step.image = Nfc(step.image);
                step.tone = Nfc(step.tone);
                step.glyph = Nfc(step.glyph);
                step.marker = Nfc(step.marker);
                step.then_text = Nfc(step.then_text);
                step.then_audio = Nfc(step.then_audio);
                NormalizeSpell(step.spell);
                step.hl ??= new List<Span>();
                step.rows ??= new List<Item>();
                foreach (var row in step.rows) NormalizeItem(row);
                step.items ??= new List<Item>();
                foreach (var item in step.items) NormalizeItem(item);
                step.readings ??= new List<Reading>();
                foreach (var reading in step.readings)
                {
                    if (reading == null) continue;
                    reading.kinds ??= new List<string>();
                    for (var i = 0; i < reading.kinds.Count; i++) reading.kinds[i] = Nfc(reading.kinds[i]);
                    reading.text = Nfc(reading.text);
                    reading.audio = Nfc(reading.audio);
                    reading.hint = Nfc(reading.hint);
                }
            }

            lesson.part2 ??= new List<Round>();
            foreach (var round in lesson.part2)
            {
                if (round == null) continue;
                round.kind = Nfc(round.kind);
                round.tag = Nfc(round.tag);
                round.instruction_audio = Nfc(round.instruction_audio);
                round.prompt_audio = Nfc(round.prompt_audio);
                round.prompt_text = Nfc(round.prompt_text);
                round.base_text = Nfc(round.base_text);
                round.image = Nfc(round.image);
                round.options ??= new List<Option>();
                foreach (var opt in round.options)
                {
                    if (opt == null) continue;
                    opt.text = Nfc(opt.text);
                    opt.audio = Nfc(opt.audio);
                    opt.image = Nfc(opt.image);
                    opt.tone = Nfc(opt.tone);
                }
            }
        }

        private static void NormalizeItem(Item item)
        {
            if (item == null) return;
            item.text = Nfc(item.text);
            item.audio = Nfc(item.audio);
            item.image = Nfc(item.image);
            item.note = Nfc(item.note);
            item.hl ??= new List<Span>();
            item.spells ??= new List<Spell>();
            foreach (var spell in item.spells) NormalizeSpell(spell);
        }

        private static void NormalizeSpell(Spell spell)
        {
            if (spell == null) return;
            spell.target = Nfc(spell.target);
            spell.parts ??= new List<Part>();
            foreach (var part in spell.parts)
            {
                if (part == null) continue;
                part.kind = Nfc(part.kind);
                part.text = Nfc(part.text);
                part.audio = Nfc(part.audio);
                part.tone = Nfc(part.tone);
            }
        }
    }
}
