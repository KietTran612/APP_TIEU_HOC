using System.Linq;
using NUnit.Framework;

namespace TapDoc.Tests
{
    /// <summary>Khen theo cách làm và tem bài học (bản thiết kế nâng cấp UI mục 4.3, đợt 3).</summary>
    public class PraiseAndStickerTests
    {
        [Test]
        public void Praise_SelfFix_First()
        {
            var e = new LessonEffort();
            e.RecordRound(0);
            e.RecordRound(1); // nhầm một lần rồi tự làm đúng, trước khi gợi ý hiện
            e.RecordReplay();
            Assert.AreEqual((SystemAudio.khen_tu_sua, UiText.PraiseSelfFix), e.Praise());
        }

        [Test]
        public void Praise_HintedRound_IsNotSelfFix()
        {
            var e = new LessonEffort();
            e.RecordRound(2); // nhầm hai lần: gợi ý đã hiện, không tính tự sửa
            Assert.AreEqual(0, e.SelfCorrected);
            Assert.AreEqual((SystemAudio.khen_cham, UiText.PraiseHardWork), e.Praise());
        }

        [Test]
        public void Praise_Replay_WhenNoSelfFix()
        {
            var e = new LessonEffort();
            e.RecordRound(0);
            e.RecordReplay();
            Assert.AreEqual((SystemAudio.khen_nghe_lai, UiText.PraiseReplay), e.Praise());
        }

        [Test]
        public void Praise_AllRight_NoMistakes()
        {
            var e = new LessonEffort();
            e.RecordRound(0);
            e.RecordRound(0);
            Assert.AreEqual((SystemAudio.khen_nghe_ki, UiText.PraiseAllRight), e.Praise());
        }

        [Test]
        public void Praise_NoRounds_HardWork()
        {
            Assert.AreEqual((SystemAudio.khen_cham, UiText.PraiseHardWork), new LessonEffort().Praise());
        }

        [Test]
        public void Praise_NeverSaysSmartOrLoud()
        {
            foreach (var text in new[] { UiText.PraiseSelfFix, UiText.PraiseReplay, UiText.PraiseAllRight, UiText.PraiseHardWork })
            {
                StringAssert.DoesNotContain("thông minh", text);
                StringAssert.DoesNotContain("đọc to", text);
            }
            CollectionAssert.IsEmpty(SystemAudio.Praise.Intersect(SystemAudio.All), "Câu khen mới là tiếng không bắt buộc");
        }

        [Test]
        public void Sticker_KeywordPictureFirst()
        {
            var lesson = TestLessons.Real.Get("tv1_t1_b13");
            var keyword = lesson.part1.First(s => (s.type == "keyword" || s.type == "picture") && !string.IsNullOrEmpty(s.image));
            var (image, caption) = LessonSticker.For(lesson);
            Assert.AreEqual(keyword.image, image);
            Assert.IsNotEmpty(caption);
            StringAssert.DoesNotContain("<", caption, "Chữ dưới tem không còn thẻ định dạng");
        }

        [Test]
        public void Sticker_EveryLesson_PictureFromLessonOrTitle()
        {
            // Mọi bài: tem là một tranh có trong bài, theo đúng thứ tự ưu tiên; không có tranh thì là tên bài.
            var withPicture = 0;
            foreach (var entry in TestLessons.Real.Index.lessons)
            {
                var lesson = TestLessons.Real.Get(entry.lesson_id);
                var (image, caption) = LessonSticker.For(lesson, entry.title);
                var stepImages = lesson.part1.Where(s => !string.IsNullOrEmpty(s.image)).Select(s => s.image).ToList();
                var roundImages = lesson.part2.SelectMany(r => new[] { r.image }.Concat(r.options.Select(o => o.image)))
                    .Where(i => !string.IsNullOrEmpty(i)).ToList();
                if (image == null)
                {
                    CollectionAssert.IsEmpty(stepImages, entry.lesson_id);
                    CollectionAssert.IsEmpty(roundImages, entry.lesson_id);
                    Assert.AreEqual(entry.title, caption, entry.lesson_id);
                    continue;
                }
                withPicture++;
                Assert.That(stepImages.Concat(roundImages), Has.Member(image), entry.lesson_id);
                var keyword = lesson.part1.FirstOrDefault(s => (s.type == "keyword" || s.type == "picture") && !string.IsNullOrEmpty(s.image));
                if (keyword != null) Assert.AreEqual(keyword.image, image, $"{entry.lesson_id}: ưu tiên tranh từ khoá");
                else if (stepImages.Count > 0) Assert.AreEqual(stepImages[0], image, $"{entry.lesson_id}: rồi tranh phần 1");
            }
            Assert.Greater(withPicture, TestLessons.Real.Index.lessons.Count / 2, "Phần lớn bài có tem tranh");
        }
    }
}
