using System.Collections.Generic;
using System.Linq;

namespace TapDoc
{
    public static class LessonAssets
    {
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
