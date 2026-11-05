using System.Collections;
using System.Linq;
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

        private static Rect CanvasRect(RectTransform rt)
        {
            var corners = new Vector3[4];
            rt.GetWorldCorners(corners);
            var canvas = (RectTransform)AppRoot.Instance.Canvas.transform;
            Vector2 min = canvas.InverseTransformPoint(corners[0]), max = canvas.InverseTransformPoint(corners[2]);
            return Rect.MinMaxRect(min.x, min.y, max.x, max.y);
        }

        /// <summary>Mọi nút đang hiện nằm trong khung của bé (đổi sang toạ độ canvas, gốc ở tâm).</summary>
        private static void AssertButtonsInsideKid(string screen)
        {
            var app = AppRoot.Instance;
            var kid = CanvasRect(app.KidRoot);
            // Nút trong vùng cuộn bị che ngoài khung nhìn: kiểm khung nhìn thay cho từng nút.
            var targets = app.Canvas.GetComponentsInChildren<UnityEngine.UI.Button>(false)
                .Where(b => b.GetComponentInParent<UnityEngine.UI.ScrollRect>() == null)
                .Select(b => (RectTransform)b.transform)
                .Concat(app.Canvas.GetComponentsInChildren<UnityEngine.UI.ScrollRect>(false).Select(sr => sr.viewport));
            foreach (var t in targets)
            {
                var b = t;
                var r = CanvasRect(t);
                Assert.IsTrue(r.xMin >= kid.xMin - 1f && r.xMax <= kid.xMax + 1f && r.yMin >= kid.yMin - 1f && r.yMax <= kid.yMax + 1f,
                    $"{screen}: nút {b.name} {r} ra ngoài khung {kid}");
            }
        }

        [UnityTest]
        public IEnumerator Portrait_KidRootCentered_ButtonsInsideFrame()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            var rt = ScreenSizes.Apply(app, ScreenSizes.TabletPortrait);
            yield return null;
            Assert.AreEqual(420f, app.KidRoot.anchoredPosition.y, .5f, "Khung 1080 nằm giữa canvas cao 1920");
            Assert.AreEqual(1080f, app.KidRoot.sizeDelta.y, .5f);

            app.ShowProfiles();
            yield return null;
            AssertButtonsInsideKid("màn chọn bé");
            app.ShowLessonList();
            yield return null;
            AssertButtonsInsideKid("danh sách bài");
            app.ShowLesson("tv1_t1_b13");
            yield return WaitPrepared();
            AssertButtonsInsideKid("màn học");
            app.ShowBook();
            yield return null;
            AssertButtonsInsideKid("Sổ bé ngoan");
            ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{ScreenSizes.TabletPortrait.Name}/app_book_portrait.png");
            ScreenSizes.Reset(app, rt);
        }

        [UnityTest]
        public IEnumerator Profile_TypedName_SurvivesResize()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            ScreenSizes.Apply(app, ScreenSizes.IPad43);
            app.ShowProfiles();
            yield return null;
            var ps = Object.FindAnyObjectByType<ProfileScreen>();
            ps.OpenCreate();
            ps.SetName("Na");
            ps.PickAvatar(ProfileScreen.Avatars[2]);

            var phone = ScreenSizes.Apply(app, ScreenSizes.IPhone);
            yield return null;
            yield return null;
            Assert.AreSame(ps, Object.FindAnyObjectByType<ProfileScreen>(), "Đổi cỡ không dựng lại màn");
            Assert.AreEqual("Na", ps.GetComponentInChildren<TMPro.TMP_InputField>().text, "Tên đang gõ còn nguyên");
            Assert.AreEqual(Palette.Orange, ps.AvatarFrame(ProfileScreen.Avatars[2]).color, "Hình đã chọn vẫn được chọn");
            Assert.IsTrue(ps.DoneButton.interactable);
            LayoutProbe.AssertFits(app.Canvas);
            ScreenSizes.Reset(app, phone);
        }

        [UnityTest]
        public IEnumerator ParentGate_SurvivesResize()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            ScreenSizes.Apply(app, ScreenSizes.IPad43);
            app.ShowParent();
            yield return WaitPrepared();
            var parent = Object.FindAnyObjectByType<ParentScreen>();
            var question = parent.Gate.Question;
            var choices = parent.ChoiceButtons.ToArray();

            var phone = ScreenSizes.Apply(app, ScreenSizes.Phone20x9);
            yield return null;
            yield return null;
            Assert.AreSame(parent, Object.FindAnyObjectByType<ParentScreen>(), "Đổi cỡ không dựng lại màn");
            Assert.AreEqual(question, parent.Gate.Question, "Câu hỏi khoá phụ huynh còn nguyên");
            CollectionAssert.AreEqual(choices, parent.ChoiceButtons);
            Assert.IsFalse(parent.IsUnlocked);
            LayoutProbe.AssertFits(app.Canvas);
            ScreenSizes.Reset(app, phone);
        }
    }
}
