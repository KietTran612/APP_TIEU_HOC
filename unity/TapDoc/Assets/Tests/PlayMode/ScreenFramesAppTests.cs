using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    /// <summary>
    /// Khung màn của app theo cỡ máy (bản thiết kế tỷ lệ màn hình mục 5.1): canvas mở rộng, gốc màn của bé và khung
    /// chuẩn 1440 đặt theo vùng an toàn của máy.
    /// </summary>
    public class ScreenFramesAppTests : AppTestBase
    {
        private static void AssertNear(Vector2 expected, Vector2 actual, string what)
        {
            Assert.AreEqual(expected.x, actual.x, .5f, $"{what}.x");
            Assert.AreEqual(expected.y, actual.y, .5f, $"{what}.y");
        }

        private static void AssertRoot(Rect expected, RectTransform root, string what)
        {
            AssertNear(Vector2.zero, root.anchorMin, what + " anchorMin");
            AssertNear(Vector2.zero, root.anchorMax, what + " anchorMax");
            AssertNear(expected.position, root.anchoredPosition, what + " vị trí");
            AssertNear(expected.size, root.sizeDelta, what + " cỡ");
        }

        [UnityTest]
        public IEnumerator Roots_FollowFrames_AllSizes()
        {
            UseStubsForMissingAssets(); // chỉ kiểm khung màn; tranh tập 2 chưa nhập không phải điều đang kiểm
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            foreach (var size in ScreenSizes.All)
            {
                var rt = ScreenSizes.Apply(app, size);
                yield return null;
                var f = app.Frames;
                Assert.AreEqual(size.Wide, f.Wide, $"{size}: kiểu mép");
                AssertRoot(f.Kid, app.KidRoot, $"{size}: KidRoot");
                AssertRoot(f.Standard, app.SafeRoot, $"{size}: SafeRoot");
                var canvasRect = ((RectTransform)app.Canvas.transform).rect;
                AssertNear(f.Canvas, canvasRect.size, $"{size}: canvas");
                var bg = (RectTransform)app.Canvas.transform.Find("Background");
                AssertNear(canvasRect.size, bg.rect.size, $"{size}: nền giấy phủ kín");
                ScreenSizes.Reset(app, rt);
            }
        }

        [UnityTest]
        public IEnumerator Present_UsesNewSizeImmediately()
        {
            UseStubsForMissingAssets(); // chỉ kiểm khung màn; tranh tập 2 chưa nhập không phải điều đang kiểm
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            var rt = ScreenSizes.Apply(app, ScreenSizes.IPad43);
            yield return null;
            Assert.AreEqual(1440f, app.KidRoot.sizeDelta.x, .5f);

            // Đổi máy rồi mở màn ngay trong cùng khung hình, không gọi RefreshFrames.
            DeviceSafeArea.Override = _ => Insets.None;
            var phone = new RenderTexture(2400, 1080, 24);
            app.UiCamera.targetTexture = phone;
            Object.Destroy(rt);
            app.ShowLessonList();
            var list = Object.FindAnyObjectByType<LessonListScreen>();
            Assert.AreSame(app.KidRoot, list.transform.parent);
            Assert.AreEqual(2400f, ((RectTransform)list.transform).rect.width, .5f, "Màn mới dựng theo cỡ mới");
            ScreenSizes.Reset(app, phone);
        }

        [UnityTest]
        public IEnumerator ParentScreen_InStandardRoot()
        {
            UseStubsForMissingAssets(); // chỉ kiểm khung màn; tranh tập 2 chưa nhập không phải điều đang kiểm
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            var rt = ScreenSizes.Apply(app, ScreenSizes.Phone20x9);
            app.ShowParent();
            yield return WaitPrepared();
            var parent = Object.FindAnyObjectByType<ParentScreen>();
            Assert.IsNotNull(parent);
            Assert.AreSame(app.SafeRoot, parent.transform.parent, "Màn người lớn giữ khung 1440");
            Assert.AreEqual(1440f, ((RectTransform)parent.transform).rect.width, .5f);
            ScreenSizes.Reset(app, rt);
        }

        [UnityTest]
        public IEnumerator RefreshFrames_NoChange_NoRelayout()
        {
            UseStubsForMissingAssets(); // chỉ kiểm khung màn; tranh tập 2 chưa nhập không phải điều đang kiểm
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            var rt = ScreenSizes.Apply(app, ScreenSizes.Phone20x9);
            var applied = app.FramesApplied;
            app.RefreshFrames();
            app.RefreshFrames();
            Assert.AreEqual(applied, app.FramesApplied, "Cùng cỡ thì không đặt lại khung");
            ScreenSizes.Reset(app, rt);
        }
    }
}
