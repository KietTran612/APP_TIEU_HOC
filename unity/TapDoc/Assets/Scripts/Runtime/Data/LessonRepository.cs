using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using UnityEngine;

namespace TapDoc
{
    public static class LessonRepository
    {
        public static LessonIndex LoadIndex()
        {
            var asset = Resources.Load<TextAsset>("lessons/index");
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

        public static Lesson Load(string lessonId)
        {
            if (string.IsNullOrWhiteSpace(lessonId))
            {
                throw new InvalidDataException($"Mã bài học rỗng: {lessonId}");
            }

            var asset = Resources.Load<TextAsset>($"lessons/{lessonId}");
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
