using System;
using System.IO;
using System.Linq;
using NUnit.Framework;

namespace TapDoc.Tests
{
    /// <summary>Sổ bé ngoan: trang theo thứ tự bài, cặp trang, trang mở đầu, số hoa và hình hoa.</summary>
    public class FlowerBookTests
    {
        private string P;

        /// <summary>Danh sách bài giả "b01".."b80" theo thứ tự, không cần nạp bài thật.</summary>
        private static readonly string[] Ids = Enumerable.Range(1, 80).Select(i => $"b{i:00}").ToArray();

        [SetUp]
        public void SetUp()
        {
            P = Path.Combine(Path.GetTempPath(), $"tapdoc_flowerbook_test_{Guid.NewGuid():N}.json");
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
        public void PageOf_FollowsOrder()
        {
            Assert.AreEqual(0, FlowerBook.PageOf(Ids, "b01"));
            Assert.AreEqual(2, FlowerBook.PageOf(Ids, "b03"));
            Assert.AreEqual(79, FlowerBook.PageOf(Ids, "b80"));
            Assert.AreEqual(-1, FlowerBook.PageOf(Ids, "khong_co"));
        }

        [Test]
        public void SpreadStart_EvenLeft()
        {
            Assert.AreEqual(0, FlowerBook.SpreadStart(0));
            Assert.AreEqual(0, FlowerBook.SpreadStart(1));
            Assert.AreEqual(4, FlowerBook.SpreadStart(5));
        }

        [Test]
        public void StartPage_LastCompletedInListOrder()
        {
            var s = new ProgressStore(P);
            s.CreateProfile("A", "x");
            s.MarkCompleted(Ids[69]); // bài thứ 70 học trước
            s.MarkCompleted(Ids[2]);  // rồi mới đến bài thứ 3
            Assert.AreEqual(69, FlowerBook.StartPage(s, Ids));
        }

        [Test]
        public void StartPage_NoneCompleted_IsZero()
        {
            var s = new ProgressStore(P);
            s.CreateProfile("A", "x");
            Assert.AreEqual(0, FlowerBook.StartPage(s, Ids));
        }

        [Test]
        public void FlowersFor_FromStars()
        {
            var s = new ProgressStore(P);
            s.CreateProfile("A", "x");
            Assert.AreEqual(0, FlowerBook.FlowersFor(s, "b01"));
            s.MarkCompleted("b01");
            Assert.AreEqual(3, FlowerBook.FlowersFor(s, "b01"));
            Assert.AreEqual(ProgressStore.MaxStars, FlowerBook.FlowersPerLesson);
        }

        [Test]
        public void FlowerImage_IsFlower()
        {
            for (var slot = 0; slot < FlowerBook.FlowersPerLesson; slot++)
            {
                Assert.AreEqual("img_chung_hoa_be_ngoan", FlowerBook.FlowerImage("b01", slot));
            }
        }
    }
}
