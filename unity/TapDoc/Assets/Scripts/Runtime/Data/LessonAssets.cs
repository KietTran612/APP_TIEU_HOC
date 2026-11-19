using System.Collections.Generic;
using System.Linq;

namespace TapDoc
{
    public static class LessonAssets
    {
        /// <summary>Loại bước có một tranh chính phát clip (<c>step.image</c>), thiết kế tranh động mục 4.</summary>
        private static readonly HashSet<string> ClipStepTypes = new() { "keyword", "picture", "riddle_answer", "tone_attach" };

        /// <summary>
        /// Mọi tranh, âm thanh phát âm và clip tranh động bài dùng, kèm loại: là bộ cần chuẩn bị trước khi mở bài.
        /// </summary>
        public static IEnumerable<(ContentKind kind, string id)> ContentIds(Lesson lesson) =>
            AudioIds(lesson).Select(id => (ContentKind.Speech, id))
                .Concat(ImageIds(lesson).Select(id => (ContentKind.Image, id)))
                .Concat(ClipIds(lesson).Select(id => (ContentKind.Clip, id)));

        /// <summary>
        /// Mã tranh ở những chỗ phát clip (chỉ Phần 1): tranh chính của bước <c>keyword</c>, <c>picture</c>,
        /// <c>riddle_answer</c>, <c>tone_attach</c> và tranh của từng từ trong bước <c>words</c>. Không trùng.
        /// </summary>
        public static IEnumerable<string> ClipIds(Lesson lesson)
        {
            if (lesson?.part1 == null) yield break;
            var seen = new HashSet<string>();
            foreach (var step in lesson.part1)
            {
                if (step == null) continue;
                if (ClipStepTypes.Contains(step.type) && !string.IsNullOrEmpty(step.image) && seen.Add(step.image))
                    yield return step.image;
                if (step.type != "words" || step.items == null) continue;
                foreach (var item in step.items)
                {
                    if (item != null && !string.IsNullOrEmpty(item.image) && seen.Add(item.image)) yield return item.image;
                }
            }
        }

        public static IEnumerable<string> AudioIds(Lesson lesson)
        {
            if (lesson == null) yield break;

            var seen = new HashSet<string>();

            IEnumerable<string> Raw()
            {
                if (lesson.part1 != null)
                {
                    foreach (var step in lesson.part1)
                    {
                        if (step == null) continue;
                        yield return step.audio;
                        yield return step.then_audio;
                        if (step.readings != null)
                        {
                            foreach (var reading in step.readings)
                            {
                                if (reading != null) yield return reading.audio;
                            }
                        }
                        foreach (var a in SpellAudio(step.spell)) yield return a;
                        if (step.rows != null)
                        {
                            foreach (var row in step.rows)
                            {
                                if (row == null) continue;
                                yield return row.audio;
                                if (row.spells != null)
                                {
                                    foreach (var sp in row.spells)
                                        foreach (var a in SpellAudio(sp)) yield return a;
                                }
                            }
                        }
                        if (step.items != null)
                        {
                            foreach (var item in step.items)
                            {
                                if (item == null) continue;
                                yield return item.audio;
                                if (item.spells != null)
                                {
                                    foreach (var sp in item.spells)
                                        foreach (var a in SpellAudio(sp)) yield return a;
                                }
                            }
                        }
                    }
                }

                if (lesson.part2 != null)
                {
                    foreach (var round in lesson.part2)
                    {
                        if (round == null) continue;
                        yield return round.instruction_audio;
                        yield return round.prompt_audio;
                        if (round.options != null)
                        {
                            foreach (var opt in round.options)
                            {
                                if (opt != null) yield return opt.audio;
                            }
                        }
                    }
                }
            }

            foreach (var id in Raw())
            {
                if (!string.IsNullOrEmpty(id) && seen.Add(id))
                {
                    yield return id;
                }
            }
        }

        public static IEnumerable<string> ImageIds(Lesson lesson)
        {
            if (lesson == null) yield break;

            var seen = new HashSet<string>();

            IEnumerable<string> Raw()
            {
                if (lesson.part1 != null)
                {
                    foreach (var step in lesson.part1)
                    {
                        if (step == null) continue;
                        yield return step.image;
                        if (step.rows != null)
                        {
                            foreach (var row in step.rows)
                            {
                                if (row != null) yield return row.image;
                            }
                        }
                        if (step.items != null)
                        {
                            foreach (var item in step.items)
                            {
                                if (item != null) yield return item.image;
                            }
                        }
                    }
                }

                if (lesson.part2 != null)
                {
                    foreach (var round in lesson.part2)
                    {
                        if (round == null) continue;
                        yield return round.image;
                        if (round.options != null)
                        {
                            foreach (var opt in round.options)
                            {
                                if (opt != null) yield return opt.image;
                            }
                        }
                    }
                }
            }

            foreach (var id in Raw())
            {
                if (!string.IsNullOrEmpty(id) && seen.Add(id))
                {
                    yield return id;
                }
            }
        }

        public static IEnumerable<string> DisplayStrings(Lesson lesson)
        {
            if (lesson == null) yield break;

            IEnumerable<string> Raw()
            {
                yield return lesson.title;

                if (lesson.part1 != null)
                {
                    foreach (var step in lesson.part1)
                    {
                        if (step == null) continue;
                        yield return step.text;
                        yield return step.glyph;
                        yield return step.then_text;
                        foreach (var s in SpellTexts(step.spell)) yield return s;

                        if (step.rows != null)
                        {
                            foreach (var row in step.rows)
                            {
                                if (row == null) continue;
                                yield return row.text;
                                yield return row.note;
                                if (row.spells != null)
                                {
                                    foreach (var sp in row.spells)
                                        foreach (var s in SpellTexts(sp)) yield return s;
                                }
                            }
                        }

                        if (step.items != null)
                        {
                            foreach (var item in step.items)
                            {
                                if (item == null) continue;
                                yield return item.text;
                                yield return item.note;
                                if (item.spells != null)
                                {
                                    foreach (var sp in item.spells)
                                        foreach (var s in SpellTexts(sp)) yield return s;
                                }
                            }
                        }
                    }
                }

                if (lesson.part2 != null)
                {
                    foreach (var round in lesson.part2)
                    {
                        if (round == null) continue;
                        yield return round.prompt_text;
                        yield return round.base_text;
                        if (round.options != null)
                        {
                            foreach (var opt in round.options)
                            {
                                if (opt != null) yield return opt.text;
                            }
                        }
                    }
                }
            }

            foreach (var text in Raw().Where(t => !string.IsNullOrEmpty(t)))
            {
                yield return text;
            }
        }

        private static IEnumerable<string> SpellAudio(Spell spell)
        {
            if (spell?.parts == null) yield break;
            foreach (var part in spell.parts)
            {
                if (part != null && !string.IsNullOrEmpty(part.audio))
                    yield return part.audio;
            }
        }

        private static IEnumerable<string> SpellTexts(Spell spell)
        {
            if (spell == null) yield break;
            if (!string.IsNullOrEmpty(spell.target)) yield return spell.target;
            if (spell.parts == null) yield break;
            foreach (var part in spell.parts)
            {
                if (part != null && !string.IsNullOrEmpty(part.text))
                    yield return part.text;
            }
        }
    }
}
