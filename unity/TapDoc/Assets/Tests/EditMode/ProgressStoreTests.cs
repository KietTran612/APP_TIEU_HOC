using System;
using System.IO;
using System.Linq;
using NUnit.Framework;

namespace TapDoc.Tests
{
    /// <summary>Kho tiến độ: hồ sơ bé, khóa bài, lượt nhầm, ghi file an toàn.</summary>
    public class ProgressStoreTests
    {
        private string P;

        [SetUp]
        public void SetUp()
        {
            P = Path.Combine(Path.GetTempPath(), $"tapdoc_progress_test_{Guid.NewGuid():N}.json");
        }

        [TearDown]
        public void TearDown()
        {
            foreach (var f in new[] { P, P + ".tmp", P + ".bak" })
            {
                if (File.Exists(f)) File.Delete(f);
            }
        }

        [Test]
        public void CreateSelectAndPersist()
        {
            var s = new ProgressStore(P);
            var p = s.CreateProfile("  Bông  ", "img_chung_avatar_01");
            Assert.AreEqual("Bông", p.name);
            s.MarkCompleted("tv1_t1_b01");
            s.Save();
            var t = ProgressStore.Load(P);
            Assert.AreEqual("Bông", t.Current.name);
            Assert.IsTrue(t.Current.lessons.Single().completed);
        }

        [Test]
        public void Name_IsTrimmedAndCapped()
        {
            var s = new ProgressStore(P);
            Assert.AreEqual(20, s.CreateProfile(new string('a', 30), "x").name.Length);
            Assert.Throws<ArgumentException>(() => s.CreateProfile("   ", "x"));
        }

        [Test]
        public void UnlockInOrder()
        {
            var s = new ProgressStore(P);
            s.CreateProfile("A", "x");
            var ids = new[] { "b01", "b02", "b03" };
            Assert.IsTrue(s.IsUnlocked(ids, "b01"));
            Assert.IsFalse(s.IsUnlocked(ids, "b02"));
            s.MarkCompleted("b01");
            Assert.IsTrue(s.IsUnlocked(ids, "b02"));
        }

        [Test]
        public void Mistakes_CountAndClear()
        {
            var s = new ProgressStore(P);
            s.CreateProfile("A", "x");
            s.RecordMistake("b13", 2);
            s.RecordMistake("b13", 2);
            s.RecordMistake("b04", 0);
            Assert.AreEqual(("b13", 2, 2), (s.Mistakes()[0].lesson_id, s.Mistakes()[0].round, s.Mistakes()[0].count));
            s.ClearMistake("b13", 2);
            Assert.AreEqual(1, s.Mistakes().Count);
        }

        [Test]
        public void ProfilesAreSeparate()
        {
            var s = new ProgressStore(P);
            var a = s.CreateProfile("A", "x");
            s.MarkCompleted("b01");
            s.CreateProfile("B", "y");
            Assert.IsEmpty(s.Current.lessons);
            s.Select(a.id);
            Assert.AreEqual(1, s.Current.lessons.Count);
        }

        [Test]
        public void CorruptFile_IsBackedUpAndStartsFresh()
        {
            File.WriteAllText(P, "{hỏng");
            var s = ProgressStore.Load(P);
            Assert.IsEmpty(s.Profiles);
            Assert.IsTrue(File.Exists(P + ".bak"));
        }

        [Test]
        public void Save_IsAtomic()
        {
            var s = new ProgressStore(P);
            s.CreateProfile("A", "x");
            s.Save();
            Assert.IsFalse(File.Exists(P + ".tmp"));
            StringAssert.Contains("\"A\"", File.ReadAllText(P));
        }
    }
}
