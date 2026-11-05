using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    /// <summary>Khối phóng to đều cho vừa chỗ (phần học, quyển sổ) và báo đổi cỡ.</summary>
    public class FitBoxTests
    {
        private GameObject _canvas;

        [SetUp]
        public void SetUp()
        {
            _canvas = new GameObject("TestCanvas", typeof(RectTransform), typeof(Canvas));
        }

        [TearDown]
        public void TearDown()
        {
            Object.Destroy(_canvas);
        }

        private RectTransform Area(Vector2 size)
        {
            var go = new GameObject("Area", typeof(RectTransform));
            go.transform.SetParent(_canvas.transform, false);
            var rt = (RectTransform)go.transform;
            rt.sizeDelta = size;
            return rt;
        }

        [UnityTest]
        public IEnumerator Fit_ScalesUniformly()
        {
            var area = Area(new Vector2(2000f, 971f));
            var content = FitBox.Create(area, "Stage", ScreenLayout.StageSize);
            var fit = area.GetComponent<FitBox>();
            yield return null;
            Assert.AreSame(content, fit.Content);
            Assert.AreEqual(971f / 680f, fit.Scale, .001f, "Lấy cạnh hẹp hơn");
            Assert.AreEqual(fit.Scale, content.localScale.x, .001f);
            Assert.AreEqual(fit.Scale, content.localScale.y, .001f);
            Assert.AreEqual(ScreenLayout.StageSize, content.rect.size, "Cỡ thiết kế không đổi");

            area.sizeDelta = new Vector2(1400f, 680f);
            yield return null;
            Assert.AreEqual(1f, fit.Scale, .001f);
            Assert.AreEqual(1f, content.localScale.x, .001f);
        }

        [UnityTest]
        public IEnumerator FrameWatcher_FiresOnlyOnRealChange()
        {
            var area = Area(new Vector2(1440f, 1080f));
            var watcher = FrameWatcher.On(area.gameObject);
            var calls = 0;
            var last = Vector2.zero;
            watcher.Changed += size =>
            {
                calls++;
                last = size;
            };
            yield return null;

            area.sizeDelta = new Vector2(2400f, 1080f);
            yield return null;
            Assert.AreEqual(1, calls);
            Assert.AreEqual(new Vector2(2400f, 1080f), last);
            Assert.AreEqual(new Vector2(2400f, 1080f), watcher.Size);

            area.sizeDelta = new Vector2(2400f, 1080f);
            area.sizeDelta = new Vector2(2400.1f, 1080f);
            yield return null;
            Assert.AreEqual(1, calls, "Đổi dưới 0,5 đơn vị thì không báo");
        }
    }
}
