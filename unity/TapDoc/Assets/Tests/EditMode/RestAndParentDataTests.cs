using System;
using System.IO;
using System.Linq;
using NUnit.Framework;

namespace TapDoc.Tests
{
    /// <summary>Dữ liệu đợt 5 (bản thiết kế nâng cấp UI mục 4.5, 4.6, 7): nhật ký ngày, số bài mỗi lần học, gợi ý chơi cùng con.</summary>
    public class RestAndParentDataTests
    {
        private string _path;

        [SetUp]
        public void SetUp() => _path = Path.Combine(Path.GetTempPath(), $"tapdoc_rest_{Guid.NewGuid():N}.json");

        [TearDown]
        public void TearDown()
        {
            if (File.Exists(_path)) File.Delete(_path);
        }

        [Test]
        public void OldFile_SessionLessonsDefaultsToThree()
        {
            var store = new ProgressStore(_path);
            store.CreateProfile("A", "x");
            store.Save();
            var json = File.ReadAllText(_path);
            StringAssert.Contains("\"session_lessons\"", json);
            // File cũ chưa có trường: mặc định 3 bài (root 17/11), không phải "không nhắc".
            File.WriteAllText(_path, System.Text.RegularExpressions.Regex.Replace(json, "\"session_lessons\":\\s*\\d+,?", ""));
            var loaded = ProgressStore.Load(_path);
            Assert.AreEqual(ProgressStore.DefaultSessionLessons, loaded.Current.session_lessons);
            Assert.AreEqual(3, ProgressStore.DefaultSessionLessons);
        }

        [Test]
        public void DayLog_RecordsLessonsAndSeconds_Keeps14Days()
        {
            var store = new ProgressStore(_path);
            store.CreateProfile("A", "x");
            var day = new DateTime(2026, 11, 17, 10, 0, 0);
            store.RecordLessonDone("tv1_t1_b13", day);
            store.RecordLessonDone("tv1_t1_b14", day);
            store.AddStudySeconds(125.4f, day);
            var log = ProgressStore.DayOf(store.Current, day);
            Assert.AreEqual(2, log.lessons);
            Assert.AreEqual(125, log.seconds);
            Assert.AreEqual("tv1_t1_b14", store.Current.last_lesson_id);
            for (var k = 1; k <= 20; k++) store.AddStudySeconds(10f, day.AddDays(k));
            Assert.AreEqual(ProgressStore.DaysKept, store.Current.days.Count, "Giữ 14 ngày gần nhất");
            var week = ProgressStore.LastWeek(store.Current, day.AddDays(20));
            Assert.AreEqual(7, week.Count);
            Assert.AreEqual(day.AddDays(20).Date, week.Last().day);
            Assert.IsTrue(week.All(d => d.seconds == 10));
            store.Save();
            var loaded = ProgressStore.Load(_path);
            Assert.AreEqual(ProgressStore.DaysKept, loaded.Current.days.Count, "Lưu xuống file");
        }

        [Test]
        public void Suggestions_SoundLesson()
        {
            var entry = TestLessons.Real.Index.lessons.First(e => e.lesson_id == "tv1_t1_b13");
            var lines = ParentSuggestions.For(entry, TestLessons.Real.Get(entry.lesson_id));
            Assert.That(lines, Has.Member(string.Format(UiText.PlayFindSound, "u, ư")));
            Assert.IsTrue(lines.Any(l => l.StartsWith("Con đọc \"")), "Có trò đọc từ khoá rồi làm động tác");
            Assert.That(lines, Has.Member(string.Format(UiText.PlayWriteSalt, "u")));
            Assert.LessOrEqual(lines.Count, ParentSuggestions.Max);
            Assert.IsFalse(lines.Any(l => l.Contains("<")), "Không còn thẻ định dạng");
        }

        [Test]
        public void Suggestions_ReadingAndNone()
        {
            var entry = TestLessons.Real.Index.lessons.First(e => e.lesson_id == "tv2_t1_b180");
            var lines = ParentSuggestions.For(entry, TestLessons.Real.Get(entry.lesson_id));
            Assert.That(lines, Has.Member(string.Format(UiText.PlayReadAgain, entry.title)));
            CollectionAssert.AreEqual(new[] { UiText.PlayNone }, ParentSuggestions.For(null, null));
            var review = TestLessons.Real.Index.lessons.First(e => e.lesson_id == "tv1_t1_b07");
            Assert.IsNotEmpty(ParentSuggestions.For(review, TestLessons.Real.Get(review.lesson_id)), "Bài ôn tập vẫn có gợi ý");
        }
    }
}
