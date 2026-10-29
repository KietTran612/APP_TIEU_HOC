using System.Linq;
using NUnit.Framework;
using UnityEngine;

namespace TapDoc.Tests
{
    public class FlowLayoutTests
    {
        [Test]
        public void WrapsWithinWidth()
        {
            var w = Enumerable.Repeat(190f, 9).ToList();
            var p = FlowLayout.Place(w, 170f, 1360f, 24f, 20f);
            Assert.That(p.Select(v => v.y).Distinct().Count(), Is.EqualTo(2));
            for (var i = 0; i < 9; i++) Assert.LessOrEqual(Mathf.Abs(p[i].x) + 95f, 680f);
        }

        [Test]
        public void SingleLine_IsCentered()
        {
            var p = FlowLayout.Place(new[] { 200f, 200f }, 100f, 1360f, 20f, 20f);
            Assert.AreEqual(-110f, p[0].x, .01f);
            Assert.AreEqual(110f, p[1].x, .01f);
            Assert.AreEqual(0f, p[0].y, .01f);
        }

        [Test]
        public void TwoLines_AreCenteredVertically_InReadingOrder()
        {
            var p = FlowLayout.Place(new[] { 600f, 600f, 600f }, 100f, 1300f, 20f, 40f);
            Assert.AreEqual(70f, p[0].y, .01f);   // khối cao 240: dòng 1 ở +70, dòng 2 ở -70
            Assert.AreEqual(70f, p[1].y, .01f);
            Assert.AreEqual(-70f, p[2].y, .01f);
            Assert.AreEqual(0f, p[2].x, .01f);
            Assert.Less(p[0].x, p[1].x);
        }

        [Test]
        public void Lines_GroupsIndicesGreedily()
        {
            var lines = FlowLayout.Lines(new[] { 500f, 500f, 500f, 100f }, 1100f, 20f);
            Assert.AreEqual(new[] { new[] { 0, 1 }, new[] { 2, 3 } }, lines.Select(l => l.ToArray()).ToArray());
        }

        [Test]
        public void TooWideItem_GetsItsOwnLine()
        {
            var lines = FlowLayout.Lines(new[] { 100f, 2000f, 100f }, 1000f, 20f);
            Assert.AreEqual(3, lines.Count);
        }
    }
}
