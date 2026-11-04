using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    public class DataTests
    {
        [Test]
        public void AudioIds_IncludesReadings()
        {
            var step = new Step { type = "unit", text = "a", audio = "van_a" };
            step.readings.Add(new Reading { audio = "r1" });
            step.readings.Add(new Reading { audio = "r2" });
            var lesson = new Lesson { part1 = new List<Step> { step } };

            var ids = LessonAssets.AudioIds(lesson).ToList();
            CollectionAssert.Contains(ids, "r1");
            CollectionAssert.Contains(ids, "r2");
        }

        [Test]
        public void ContentIds_IsUnionOfAudioAndImage()
        {
            var json = ((TextAsset)new ResourcesContentSource().Load(ContentKind.Lesson, "tv1_t1_b17")).text;
            var lesson = LessonRepository.Parse(json);

            var expected = LessonAssets.AudioIds(lesson).Select(id => (ContentKind.Speech, id))
                .Concat(LessonAssets.ImageIds(lesson).Select(id => (ContentKind.Image, id)))
                .ToList();
            var actual = LessonAssets.ContentIds(lesson).ToList();
            CollectionAssert.AreEquivalent(expected, actual);
            Assert.AreEqual(actual.Count, actual.Distinct().Count(), "ContentIds có mã trùng");
        }

        [Test]
        public void Load_Lesson13()
        {
            var l = TestLessons.Real.Get("tv1_t1_b13");
            Assert.AreEqual("u ư", l.title);
            Assert.AreEqual(11, l.part1.Count);
            Assert.AreEqual("tieng_cuwr", l.part1[7].spell.parts[4].audio);
            Assert.IsTrue(l.part1[7].spell.drag_tone);
            Assert.That(l.part2.Count, Is.InRange(6, 10));
        }

        [Test]
        public void Index_ListsLessonsInBookOrder()
        {
            // Danh sách bài đi liền từ bài 1 theo thứ tự sách (mỗi đợt thêm bài). Bài 42 nạp được theo mã kể cả khi
            // chưa nằm trong danh sách.
            var numbers = TestLessons.Real.Index.lessons.Select(e => e.lesson_no).ToList();
            CollectionAssert.AreEqual(Enumerable.Range(1, numbers.Count), numbers);
            Assert.GreaterOrEqual(numbers.Count, 17);
            Assert.AreEqual(42, TestLessons.Real.Get("tv1_t1_b42").lesson_no);
        }

        [Test]
        public void Parse_NormalizesNfc() =>
            Assert.AreEqual("cử", LessonRepository.Parse("{\"title\":\"cu\\u031b\\u0309\"}").title);

        [Test]
        public void Load_Unknown_Throws() =>
            Assert.Throws<InvalidDataException>(() => TestLessons.Real.Get("khong_co"));

        [Test]
        public void TextStyler_Apply()
        {
            Assert.AreEqual(
                "cái đ<color=#1F8A9E>u</color>",
                TextStyler.Apply("cái đu", new() { new Span { s = 5, n = 1 } }));
            Assert.AreEqual(
                "đ<color=#1F8A9E>u</color> đ<color=#1F8A9E>ủ</color>",
                TextStyler.Apply("đu đủ", new() { new Span { s = 1, n = 1 }, new Span { s = 4, n = 1 } }));
            Assert.AreEqual("ca", TextStyler.Apply("ca", new()));
        }

        [Test]
        public void AssetCatalog_Missing_LogsOnceAndReturnsNull()
        {
            var c = new AssetCatalog(new ResourcesContentSource());
            LogAssert.Expect(LogType.Error, "[TapDoc] Thiếu âm thanh: khong_co");
            Assert.IsNull(c.Audio("khong_co"));
            Assert.IsNull(c.Audio("khong_co"));
            LogAssert.NoUnexpectedReceived();
        }

        [Test]
        public void AllReferencedAssetsExist()
        {
            var source = new ResourcesContentSource();
            if (source.Load(ContentKind.Speech, SystemAudio.khen_01) == null &&
                source.Load(ContentKind.Image, SystemImages.Star) == null)
            {
                Assert.Ignore("Chưa giải gói media (tranh, âm thanh) vào Resources");
            }

            // Mã chung khai báo trong code, cộng mọi mã trong các bài.
            var ids = new SortedSet<(ContentKind kind, string id)>(
                SystemAudio.All.Select(id => (ContentKind.Speech, id))
                    .Concat(SystemImages.All.Select(id => (ContentKind.Image, id))));
            foreach (var e in TestLessons.Real.Index.lessons)
            {
                foreach (var key in LessonAssets.ContentIds(TestLessons.Real.Get(e.lesson_id)))
                {
                    Assert.IsFalse(string.IsNullOrWhiteSpace(key.id), $"Bài {e.lesson_id} có mã {key.kind} rỗng");
                    ids.Add(key);
                }
            }

            var missing = ids.Where(key => source.Load(key.kind, key.id) == null)
                .Select(key => $"{(key.kind == ContentKind.Image ? "tranh" : "âm thanh")} {key.id}")
                .ToList();
            Assert.IsEmpty(missing, $"Thiếu {missing.Count} tài nguyên:\n  " + string.Join("\n  ", missing));
        }

        [Test]
        public void Parse_InvalidJson_ThrowsWithLessonId()
        {
            var ex = Assert.Throws<InvalidDataException>(() => LessonRepository.Parse("{\"title\": ", "tv1_t1_b99"));
            StringAssert.StartsWith("Bài tv1_t1_b99: ", ex.Message);
        }

        [Test]
        public void Markers()
        {
            Assert.AreEqual("img_chung_em_doc", SystemImages.ForMarker("●"));
            Assert.AreEqual("img_chung_luyen_tap", SystemImages.ForMarker("⌂"));
            Assert.IsNull(SystemImages.ForMarker(""));
        }

        [Test]
        public void FontCoversAllDisplayText()
        {
            var text = string.Concat(
                           TestLessons.Real.Index.lessons.SelectMany(
                               e => LessonAssets.DisplayStrings(TestLessons.Real.Get(e.lesson_id))))
                     + string.Concat(UiText.All)
                     + "ˋˊˀ˜.";
            Assert.IsTrue(
                FontProvider.Main.HasCharacters(text, out uint[] missing, false, true),
                "Thiếu: " + string.Concat((missing ?? System.Array.Empty<uint>()).Select(c => char.ConvertFromUtf32((int)c))));
        }

        [Test]
        public void AllSfxExist()
        {
            // Tiếng động nằm riêng, tách khỏi âm thanh phát âm.
            var source = new ResourcesContentSource();
            foreach (var id in SystemSfx.All)
            {
                Assert.IsNotNull(source.Load(ContentKind.Sfx, id), $"Thiếu tiếng động {id}");
                Assert.IsNull(source.Load(ContentKind.Speech, id), $"Tiếng động {id} không được nằm trong thư mục giọng đọc");
            }
        }
    }
}
