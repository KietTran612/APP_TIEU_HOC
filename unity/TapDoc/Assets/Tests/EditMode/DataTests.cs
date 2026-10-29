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
        public void Load_Lesson13()
        {
            var l = LessonRepository.Load("tv1_t1_b13");
            Assert.AreEqual("u ư", l.title);
            Assert.AreEqual(11, l.part1.Count);
            Assert.AreEqual("tieng_cuwr", l.part1[7].spell.parts[4].audio);
            Assert.IsTrue(l.part1[7].spell.drag_tone);
            Assert.That(l.part2.Count, Is.InRange(6, 10));
        }

        [Test]
        public void Index_ListsLessons1To17InOrder()
        {
            // Bản đầu tiên: bài 1–17. Bài mẫu 42 vẫn nạp được theo mã nhưng không nằm trong danh sách bài.
            CollectionAssert.AreEqual(
                Enumerable.Range(1, 17),
                LessonRepository.LoadIndex().lessons.Select(e => e.lesson_no));
            Assert.AreEqual(42, LessonRepository.Load("tv1_t1_b42").lesson_no);
        }

        [Test]
        public void Parse_NormalizesNfc() =>
            Assert.AreEqual("cử", LessonRepository.Parse("{\"title\":\"cu\\u031b\\u0309\"}").title);

        [Test]
        public void Load_Unknown_Throws() =>
            Assert.Throws<InvalidDataException>(() => LessonRepository.Load("khong_co"));

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
            var c = new AssetCatalog();
            LogAssert.Expect(LogType.Error, "[TapDoc] Thiếu âm thanh: khong_co");
            Assert.IsNull(c.Audio("khong_co"));
            Assert.IsNull(c.Audio("khong_co"));
            LogAssert.NoUnexpectedReceived();
        }

        [Test]
        public void AllReferencedAssetsExist()
        {
            if (Resources.LoadAll<AudioClip>("audio").Length == 0 && Resources.LoadAll<Sprite>("images").Length == 0)
            {
                Assert.Ignore("Chưa nhập tài nguyên (Task 11–12)");
            }

            var audioIds = new SortedSet<string>(SystemAudio.All, StringComparer.Ordinal);
            var imageIds = new SortedSet<string>(SystemImages.All, StringComparer.Ordinal);
            foreach (var e in LessonRepository.LoadIndex().lessons)
            {
                var l = LessonRepository.Load(e.lesson_id);
                foreach (var id in LessonAssets.AudioIds(l))
                {
                    Assert.IsFalse(string.IsNullOrWhiteSpace(id), $"Bài {e.lesson_id} có mã âm thanh rỗng");
                    audioIds.Add(id);
                }
                foreach (var id in LessonAssets.ImageIds(l))
                {
                    Assert.IsFalse(string.IsNullOrWhiteSpace(id), $"Bài {e.lesson_id} có mã tranh rỗng");
                    imageIds.Add(id);
                }
            }

            // Kiểm tra thật bằng AssetCatalog mặc định (Resources), không loader giả. Mã nào thiếu thì
            // catalog ghi lỗi một lần: báo trước cho LogAssert để danh sách thiếu là thông điệp lỗi duy nhất.
            var c = new AssetCatalog();
            var missing = new List<string>();
            foreach (var id in audioIds)
            {
                var exists = Resources.Load<AudioClip>("audio/" + id) != null;
                if (!exists) LogAssert.Expect(LogType.Error, "[TapDoc] Thiếu âm thanh: " + id);
                if (c.Audio(id) == null) missing.Add("âm thanh " + id);
            }
            foreach (var id in imageIds)
            {
                var exists = Resources.Load<Sprite>("images/" + id) != null;
                if (!exists) LogAssert.Expect(LogType.Error, "[TapDoc] Thiếu tranh: " + id);
                if (c.Image(id) == null) missing.Add("tranh " + id);
            }

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
                           LessonRepository.LoadIndex().lessons.SelectMany(
                               e => LessonAssets.DisplayStrings(LessonRepository.Load(e.lesson_id))))
                     + string.Concat(UiText.All)
                     + "ˋˊˀ˜.";
            Assert.IsTrue(
                FontProvider.Main.HasCharacters(text, out uint[] missing, false, true),
                "Thiếu: " + string.Concat((missing ?? System.Array.Empty<uint>()).Select(c => char.ConvertFromUtf32((int)c))));
        }
    }
}
