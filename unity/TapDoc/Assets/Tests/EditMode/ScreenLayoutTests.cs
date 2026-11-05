using NUnit.Framework;
using UnityEngine;

namespace TapDoc.Tests
{
    /// <summary>
    /// Khung màn theo cỡ máy (bản thiết kế tỷ lệ màn hình mục 4, 5.1, 5.6): cỡ canvas, vùng an toàn, khung của bé,
    /// khung chuẩn 1440 và kiểu mép/góc. Cỡ vào và lề tính bằng điểm ảnh; giá trị ra tính bằng đơn vị canvas.
    /// </summary>
    public class ScreenLayoutTests
    {
        private const float Tol = 0.5f;

        [TearDown]
        public void TearDown()
        {
            DeviceSafeArea.Override = null;
        }

        private static ScreenFrames Compute(int w, int h, float left = 0f, float right = 0f, float bottom = 0f, float top = 0f) =>
            ScreenLayout.Compute(new Vector2Int(w, h), new Insets(left, right, bottom, top));

        private static void AssertRect(Rect expected, Rect actual, string what)
        {
            Assert.AreEqual(expected.x, actual.x, Tol, $"{what}.x");
            Assert.AreEqual(expected.y, actual.y, Tol, $"{what}.y");
            Assert.AreEqual(expected.width, actual.width, Tol, $"{what}.width");
            Assert.AreEqual(expected.height, actual.height, Tol, $"{what}.height");
        }

        [Test]
        public void Phone20x9_Wide_FullWidth()
        {
            var f = Compute(2400, 1080);
            Assert.AreEqual(2400f, f.Canvas.x, Tol);
            Assert.AreEqual(1080f, f.Canvas.y, Tol);
            AssertRect(new Rect(0f, 0f, 2400f, 1080f), f.Kid, "Kid");
            Assert.AreEqual(480f, f.Standard.x, Tol);
            Assert.AreEqual(1440f, f.Standard.width, Tol);
            Assert.IsTrue(f.Wide);
        }

        [Test]
        public void Phone20x9_CameraLeft_SymmetricInsets()
        {
            var f = Compute(2400, 1080, left: 110f);
            AssertRect(new Rect(110f, 0f, 2180f, 1080f), f.Safe, "Safe");
            Assert.AreEqual(110f, f.Kid.x, Tol);
            Assert.AreEqual(2180f, f.Kid.width, Tol);
            Assert.AreEqual(480f, f.Standard.x, Tol);
            Assert.IsTrue(f.Wide);
        }

        [Test]
        public void IPhone_NotchAndHomeBar()
        {
            var f = Compute(2556, 1179, left: 177f, right: 177f, bottom: 63f);
            Assert.AreEqual(2341.4f, f.Canvas.x, Tol);
            AssertRect(new Rect(162.1f, 57.7f, 2017.1f, 1022.3f), f.Safe, "Safe");
            AssertRect(f.Safe, f.Kid, "Kid");
            Assert.AreEqual(450.7f, f.Standard.x, Tol);
            Assert.IsTrue(f.Wide);
            Assert.AreEqual(1.155f, ScreenLayout.WideStageScale(f.Kid.size), 0.005f);
        }

        [Test]
        public void Phone16x9_JustWide()
        {
            var f = Compute(1334, 750);
            Assert.AreEqual(1921f, f.Canvas.x, Tol);
            Assert.IsTrue(f.Wide);
            Assert.AreEqual(1.086f, ScreenLayout.WideStageScale(f.Kid.size), 0.005f);
        }

        [Test]
        public void IPadAir_Corner_HomeBar()
        {
            var f = Compute(2360, 1640, bottom: 40f);
            Assert.AreEqual(1554.1f, f.Canvas.x, Tol);
            AssertRect(new Rect(57.1f, 26.3f, 1440f, 1053.7f), f.Kid, "Kid");
            Assert.IsFalse(f.Wide);
        }

        [Test]
        public void IPad43_Corner()
        {
            var f = Compute(2048, 1536);
            AssertRect(new Rect(0f, 0f, 1440f, 1080f), f.Kid, "Kid");
            AssertRect(f.Kid, f.Standard, "Standard");
            Assert.IsFalse(f.Wide);
        }

        [Test]
        public void Tablet16x10_Corner()
        {
            var f = Compute(2560, 1600);
            Assert.AreEqual(1728f, f.Canvas.x, Tol);
            Assert.AreEqual(144f, f.Kid.x, Tol);
            Assert.AreEqual(1440f, f.Kid.width, Tol);
            Assert.IsFalse(f.Wide);
        }

        [Test]
        public void TabletPortrait_FrameCentered()
        {
            var f = Compute(1536, 2048);
            Assert.AreEqual(1440f, f.Canvas.x, Tol);
            Assert.AreEqual(1920f, f.Canvas.y, Tol);
            AssertRect(new Rect(0f, 420f, 1440f, 1080f), f.Kid, "Kid");
            Assert.IsFalse(f.Wide);
        }

        [Test]
        public void Fold_FrameCentered()
        {
            var f = Compute(2208, 1840);
            Assert.AreEqual(1440f, f.Canvas.x, Tol);
            Assert.AreEqual(1200f, f.Canvas.y, Tol);
            AssertRect(new Rect(0f, 60f, 1440f, 1080f), f.Kid, "Kid");
            Assert.IsFalse(f.Wide);
        }

        [Test]
        public void IsWide_Threshold()
        {
            Assert.IsFalse(ScreenLayout.IsWide(new Vector2(1440f, 1080f)));
            Assert.IsTrue(ScreenLayout.IsWide(new Vector2(1441f, 1080f)));
        }

        [Test]
        public void SafeArea_OverrideWins()
        {
            DeviceSafeArea.Override = _ => new Insets(1f, 2f, 3f, 4f);
            var i = DeviceSafeArea.For(new Vector2Int(2400, 1080));
            Assert.AreEqual(1f, i.Left);
            Assert.AreEqual(2f, i.Right);
            Assert.AreEqual(3f, i.Bottom);
            Assert.AreEqual(4f, i.Top);
        }

        [Test]
        public void Frames_Same_ToleratesTinyDifference()
        {
            var a = Compute(2400, 1080);
            var b = Compute(2400, 1080);
            Assert.IsTrue(a.Same(b));
            Assert.IsFalse(a.Same(Compute(2400, 1080, left: 50f)));
        }
    }
}
