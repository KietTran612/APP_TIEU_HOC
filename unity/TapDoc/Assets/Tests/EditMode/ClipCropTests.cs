using NUnit.Framework;
using UnityEngine;

namespace TapDoc.Tests
{
    /// <summary>
    /// Cắt phần tranh ở giữa clip (thiết kế tranh động mục 7) và điều kiện máy được phát clip (mục 10).
    /// </summary>
    public class ClipCropTests
    {
        private const float Eps = 1e-5f;

        private static void AssertRect(Rect actual, float x, float y, float w, float h)
        {
            Assert.AreEqual(x, actual.x, Eps, "x");
            Assert.AreEqual(y, actual.y, Eps, "y");
            Assert.AreEqual(w, actual.width, Eps, "width");
            Assert.AreEqual(h, actual.height, Eps, "height");
        }

        [Test]
        public void UvRect_Wide720p_SquarePicture_TakesCentreSquare()
        {
            // 1280×720, tranh vuông đệm giữa: hình vuông 720 ở giữa, lề 280 mỗi bên.
            AssertRect(ClipCrop.UvRect(1280, 720, 1f), .21875f, 0f, .5625f, 1f);
        }

        [Test]
        public void UvRect_SquareClip_TakesWhole()
        {
            AssertRect(ClipCrop.UvRect(720, 720, 1f), 0f, 0f, 1f, 1f);
        }

        [Test]
        public void UvRect_TallClip_CropsTopAndBottom()
        {
            AssertRect(ClipCrop.UvRect(720, 1280, 1f), 0f, .21875f, 1f, .5625f);
        }

        [Test]
        public void UvRect_FourThirdsPicture_WiderCrop()
        {
            // Rộng cần: 720 × 4/3 = 960 trên 1280 → 0,75; lề 160 mỗi bên → x = 0,125.
            AssertRect(ClipCrop.UvRect(1280, 720, 4f / 3f), .125f, 0f, .75f, 1f);
        }

        [Test]
        public void UvRect_EdgeInset_TrimsEachSideOfCrop_StaysSquare()
        {
            // 37/327 clip có 3 hàng đen ở mép trên, mép dưới phần vuông: cắt thêm 4 điểm ảnh mỗi mép (trên khung 720).
            // Phần vuông 720 còn 712: x = 284/1280, y = 4/720, rộng 712/1280, cao 712/720.
            AssertRect(ClipCrop.UvRect(1280, 720, 1f, 4), .221875f, .0055556f, .55625f, .9888889f);
        }

        [Test]
        public void UvRect_EdgeInset_TooLarge_FallsBackToNoInset()
        {
            AssertRect(ClipCrop.UvRect(1280, 720, 1f, 400), .21875f, 0f, .5625f, 1f);
        }

        [Test]
        public void AppInset_HidesThreeDarkRows()
        {
            Assert.GreaterOrEqual(ClipCrop.EdgeInsetPx, 4, "che được 3 hàng đen ở mép clip Flow");
            Assert.LessOrEqual(ClipCrop.EdgeInsetPx, 8, "không phóng tranh quá 2,2% so với tranh tĩnh");
        }

        [Test]
        public void UvRect_UnknownSize_WholeClip()
        {
            AssertRect(ClipCrop.UvRect(0, 0, 1f), 0f, 0f, 1f, 1f);
            AssertRect(ClipCrop.UvRect(1280, 720, 0f), 0f, 0f, 1f, 1f);
        }

        [Test]
        public void CanPlay_NeedsMemoryGraphicsAndRenderTexture()
        {
            Assert.IsFalse(ClipSupport.CanPlay(1999, true, true), "máy 2 GB trở xuống");
            Assert.IsTrue(ClipSupport.CanPlay(2000, true, true));
            Assert.IsTrue(ClipSupport.CanPlay(16000, true, true));
            Assert.IsFalse(ClipSupport.CanPlay(16000, false, true), "không có đồ hoạ (-nographics)");
            Assert.IsFalse(ClipSupport.CanPlay(16000, true, false), "không tạo được RenderTexture");
        }
    }
}
