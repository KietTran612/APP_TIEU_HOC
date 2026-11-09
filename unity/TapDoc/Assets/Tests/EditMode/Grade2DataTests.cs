using System;
using System.IO;
using NUnit.Framework;
using UnityEngine;

namespace TapDoc.Tests
{
    /// <summary>
    /// Lớp 2 trong app (thiết kế TV2 tập một, mục 4): lớp của bài, chuỗi mở khoá theo lớp, lớp đang xem theo bé,
    /// nhãn trang Sổ bé ngoan.
    /// </summary>
    public class Grade2DataTests
    {
        private const string Index =
            "{\"books\":[],\"lessons\":[" +
            "{\"lesson_id\":\"tv1_t1_b01\",\"lesson_no\":1,\"title\":\"o\",\"type\":\"am_moi\",\"book\":\"tv1_t1_1990\",\"part\":\"chu_cai\",\"label\":\"Bài 1\",\"week\":0,\"grade\":1}," +
            "{\"lesson_id\":\"tv1_t1_b02\",\"lesson_no\":2,\"title\":\"c\",\"type\":\"am_moi\",\"book\":\"tv1_t1_1990\",\"part\":\"chu_cai\",\"label\":\"Bài 2\",\"week\":0,\"grade\":1}," +
            "{\"lesson_id\":\"tv1_t1_b03\",\"lesson_no\":3,\"title\":\"ô\",\"type\":\"am_moi\",\"book\":\"tv1_t1_1990\",\"part\":\"chu_cai\",\"label\":\"Bài 3\",\"week\":0,\"grade\":1}," +
            "{\"lesson_id\":\"tv2_t1_b172\",\"lesson_no\":172,\"title\":\"Bác Hồ khuyên học sinh\",\"type\":\"tap_doc\",\"book\":\"tv2_t1_2001\",\"part\":\"lop2\",\"label\":\"Bài 1\",\"week\":1,\"grade\":2,\"theme\":\"Nhà trường\"}," +
            "{\"lesson_id\":\"tv2_t1_b173\",\"lesson_no\":173,\"title\":\"Cái trống trường em\",\"type\":\"hoc_thuoc_long\",\"book\":\"tv2_t1_2001\",\"part\":\"lop2\",\"label\":\"Bài 2\",\"week\":1,\"grade\":2,\"theme\":\"Nhà trường\"}" +
            "]}";

        private string _path;
        private LessonIndex _index;

        [SetUp]
        public void SetUp()
        {
            _path = Path.Combine(Path.GetTempPath(), $"tapdoc_grade2_test_{Guid.NewGuid():N}.json");
            _index = JsonUtility.FromJson<LessonIndex>(Index);
        }

        [TearDown]
        public void TearDown()
        {
            foreach (var f in new[] { _path, _path + ".tmp", _path + ".bak" })
            {
                if (File.Exists(f)) File.Delete(f);
            }
        }

        [Test]
        public void MissingGradeMeansGrade1()
        {
            var old = JsonUtility.FromJson<LessonIndex>(
                "{\"lessons\":[{\"lesson_id\":\"a\",\"lesson_no\":1,\"title\":\"o\",\"type\":\"am_moi\",\"book\":\"t1\"}]}");
            Assert.AreEqual(1, old.lessons[0].EffectiveGrade);
            Assert.IsFalse(old.HasGrade2);
        }

        [Test]
        public void Index_ParsesGradeAndTheme()
        {
            Assert.AreEqual(2, _index.lessons[3].EffectiveGrade);
            Assert.AreEqual("Nhà trường", _index.lessons[3].theme);
            Assert.IsTrue(_index.HasGrade2);
            CollectionAssert.AreEqual(new[] { "tv2_t1_b172", "tv2_t1_b173" }, _index.OrderedIds(2));
            CollectionAssert.AreEqual(new[] { "tv1_t1_b01", "tv1_t1_b02", "tv1_t1_b03" }, _index.SameGradeIds("tv1_t1_b02"));
        }

        [Test]
        public void GradeTabDefaultsTo1AndPersists()
        {
            var s = new ProgressStore(_path);
            s.CreateProfile("Bông", "img_chung_avatar_01");
            Assert.AreEqual(1, s.GradeTab);
            s.GradeTab = 2;
            s.Save();
            Assert.AreEqual(2, ProgressStore.Load(_path).GradeTab);
        }

        [Test]
        public void LegacyChainUnchangedWhenGrade2Added()
        {
            var s = new ProgressStore(_path);
            s.CreateProfile("Bông", "img_chung_avatar_01");
            s.MarkCompleted("tv1_t1_b01");
            var grade1 = _index.OrderedIds(1);
            Assert.IsTrue(s.IsUnlocked(grade1, "tv1_t1_b02"));
            Assert.IsFalse(s.IsUnlocked(grade1, "tv1_t1_b03"));
        }

        [Test]
        public void FirstGrade2LessonOpenWithoutGrade1()
        {
            var s = new ProgressStore(_path);
            s.CreateProfile("Bông", "img_chung_avatar_01");
            var grade2 = _index.OrderedIds(2);
            Assert.IsTrue(s.IsUnlocked(grade2, "tv2_t1_b172"));
            Assert.IsFalse(s.IsUnlocked(grade2, "tv2_t1_b173"));
        }

        [Test]
        public void BookPageHeaderUsesLabel()
        {
            Assert.AreEqual("Bài 1 · Bác Hồ khuyên học sinh", BookPage.HeaderText(_index.lessons[3]));
            var noLabel = new LessonEntry { lesson_no = 5, title = "x" };
            Assert.AreEqual("Bài 5 · x", BookPage.HeaderText(noLabel));
        }
    }
}
