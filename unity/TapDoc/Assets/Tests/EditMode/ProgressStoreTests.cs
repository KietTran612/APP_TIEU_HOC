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

        [Test]
        public void SfxEnabled_DefaultOn_PersistsOff()
        {
            var s = new ProgressStore(P);
            Assert.IsTrue(s.SfxEnabled, "Tiếng động mặc định bật");
            s.SfxEnabled = false;
            s.Save();
            Assert.IsFalse(ProgressStore.Load(P).SfxEnabled);
        }

        [Test]
        public void OldFile_SfxOnAndFlowersKept()
        {
            // File tiến độ trước bản giao diện mới: không có trường sfx_off, bài đã học có 3 sao.
            File.WriteAllText(P, "{\"schema\":1,\"profiles\":[{\"id\":\"p1\",\"name\":\"A\",\"avatar\":\"x\"," +
                                 "\"lessons\":[{\"lesson_id\":\"b01\",\"completed\":true,\"stars\":3}],\"mistakes\":[]}]," +
                                 "\"current\":\"p1\"}");
            var s = ProgressStore.Load(P);
            Assert.IsTrue(s.SfxEnabled);
            Assert.AreEqual(3, s.StarsFor("b01"));
            Assert.AreEqual(3, FlowerBook.FlowersFor(s, "b01"));
        }

        private static readonly string[] Order = { "tv1_t1_b01", "tv1_t1_b02", "tv1_t2_b81" };

        [Test]
        public void UnlockAll_On_OpensEveryLesson()
        {
            var s = new ProgressStore(P);
            s.CreateProfile("Bông", "img_chung_avatar_01");
            s.UnlockAll = true;
            Assert.IsTrue(Order.All(id => s.IsUnlocked(Order, id)));
            Assert.IsFalse(s.IsUnlocked(Order, "khong_co"));
        }

        [Test]
        public void UnlockAll_Off_KeepsSequentialRule()
        {
            var s = new ProgressStore(P);
            s.CreateProfile("Bông", "img_chung_avatar_01");
            s.MarkCompleted("tv1_t1_b01");
            s.UnlockAll = true;
            s.UnlockAll = false;
            Assert.IsTrue(s.IsUnlocked(Order, "tv1_t1_b02"));
            Assert.IsFalse(s.IsUnlocked(Order, "tv1_t2_b81"));
            Assert.IsTrue(s.IsCompleted("tv1_t1_b01"));
        }

        [Test]
        public void UnlockAll_SavedPerProfile()
        {
            var s = new ProgressStore(P);
            var a = s.CreateProfile("A", "img_chung_avatar_01");
            s.UnlockAll = true;
            var b = s.CreateProfile("B", "img_chung_avatar_02");
            s.Save();
            var t = ProgressStore.Load(P);
            t.Select(a.id);
            Assert.IsTrue(t.UnlockAll);
            t.Select(b.id);
            Assert.IsFalse(t.UnlockAll);
        }

        [Test]
        public void UnlockAll_OldFileWithoutField_IsOff()
        {
            File.WriteAllText(P, "{\"profiles\":[{\"id\":\"x\",\"name\":\"Cũ\",\"avatar\":\"a\",\"lessons\":[],\"mistakes\":[]}],\"current\":\"x\"}");
            var t = ProgressStore.Load(P);
            Assert.IsFalse(t.UnlockAll);
        }

        [Test]
        public void NoticeVersion_DefaultZero_RoundTrips()
        {
            var s = new ProgressStore(P);
            Assert.AreEqual(0, s.NoticeVersion);
            s.NoticeVersion = 1;
            s.Save();
            Assert.AreEqual(1, ProgressStore.Load(P).NoticeVersion);
        }

        [Test]
        public void OldFile_NoNoticeVersion_ReadsZero()
        {
            File.WriteAllText(P, "{\"schema\":1,\"profiles\":[{\"id\":\"a\",\"name\":\"Na\",\"avatar\":\"img_chung_avatar_01\",\"lessons\":[],\"mistakes\":[]}],\"current\":\"a\",\"sfx_off\":false}");
            var s = ProgressStore.Load(P);
            Assert.AreEqual(0, s.NoticeVersion);
            Assert.AreEqual(1, s.Profiles.Count);
            Assert.AreEqual("Na", s.Profiles[0].name);
        }

        [Test]
        public void RenameProfile_CleansName()
        {
            var s = new ProgressStore(P);
            var p = s.CreateProfile("Na", "img_chung_avatar_01");
            Assert.IsTrue(s.RenameProfile(p.id, "  Bông  "));
            Assert.AreEqual("Bông", p.name);
            Assert.IsFalse(s.RenameProfile(p.id, "   "), "Tên trống sau khi làm sạch thì không đổi");
            Assert.AreEqual("Bông", p.name);
            Assert.IsFalse(s.RenameProfile("khong_co", "Su"));
        }

        [Test]
        public void SetAvatar_ChangesAvatar()
        {
            var s = new ProgressStore(P);
            var p = s.CreateProfile("Na", "img_chung_avatar_01");
            Assert.IsTrue(s.SetAvatar(p.id, "img_chung_avatar_03"));
            Assert.AreEqual("img_chung_avatar_03", p.avatar);
            Assert.IsFalse(s.SetAvatar("khong_co", "img_chung_avatar_03"));
        }

        [Test]
        public void DeleteProfile_Current_ClearsCurrent()
        {
            var s = new ProgressStore(P);
            var a = s.CreateProfile("A", "img_chung_avatar_01");
            var b = s.CreateProfile("B", "img_chung_avatar_02");
            s.Select(a.id);
            Assert.IsTrue(s.DeleteProfile(b.id));
            Assert.AreEqual(a.id, s.Current.id, "Xoá bé khác thì bé đang học giữ nguyên");
            Assert.IsTrue(s.DeleteProfile(a.id));
            Assert.IsNull(s.Current, "Xoá bé đang học thì không còn bé đang học");
            Assert.AreEqual(0, s.Profiles.Count);
            Assert.IsFalse(s.DeleteProfile(a.id));
        }

        [Test]
        public void ResetAll_DeletesSideFiles()
        {
            var s = new ProgressStore(P);
            s.CreateProfile("Na", "img_chung_avatar_01");
            s.NoticeVersion = 1;
            s.SfxEnabled = false;
            s.Save();
            File.WriteAllText(P + ".tmp", "x");
            File.WriteAllText(P + ".bak", "x");
            s.ResetAll();
            Assert.IsFalse(File.Exists(P));
            Assert.IsFalse(File.Exists(P + ".tmp"));
            Assert.IsFalse(File.Exists(P + ".bak"));
            Assert.AreEqual(0, s.Profiles.Count);
            Assert.IsNull(s.Current);
            Assert.AreEqual(0, s.NoticeVersion);
            Assert.IsTrue(s.SfxEnabled);
        }
    }
}
