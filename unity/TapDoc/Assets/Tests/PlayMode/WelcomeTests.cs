using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.UI;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>Màn chào bé (bản thiết kế nâng cấp UI mục 4.4, đợt 4): gà con chào, thẻ bé to, bé học gần nhất đứng đầu.</summary>
    public class WelcomeTests : AppTestBase
    {
        private static ProfileScreen Screen() => Object.FindAnyObjectByType<ProfileScreen>();

        private static Rect CanvasRect(RectTransform rt)
        {
            var corners = new Vector3[4];
            rt.GetWorldCorners(corners);
            var canvas = (RectTransform)AppRoot.Instance.Canvas.transform;
            var min = new Vector2(float.MaxValue, float.MaxValue);
            var max = new Vector2(float.MinValue, float.MinValue);
            foreach (var c in corners)
            {
                Vector2 p = canvas.InverseTransformPoint(c);
                min = Vector2.Min(min, p);
                max = Vector2.Max(max, p);
            }
            return Rect.MinMaxRect(min.x, min.y, max.x, max.y);
        }

        private IEnumerator OpenWithKids(int kids)
        {
            yield return LoadMainWithProfile(); // một bé "Bé thử"
            for (var i = 1; i < kids; i++) AppRoot.Instance.Progress.CreateProfile($"Bé {i + 1}", ProfileScreen.Avatars[i % 6]);
            AppRoot.Instance.SaveProgress();
            AppRoot.Instance.ShowProfiles();
            yield return null;
            yield return null;
        }

        [UnityTest]
        public IEnumerator Greets_WithBubble()
        {
            yield return OpenWithKids(2);
            var s = Screen();
            Assert.IsNotNull(s.Mascot, "Có gà con ở màn chọn bé");
            Assert.AreEqual(UiText.Greeting, s.Mascot.BubbleText, "Gà con chào, chỉ rõ việc: chạm vào hình");
            Assert.That(new[] { SystemAudio.hd_chao_be, null }, Has.Member(s.GreetingAudio),
                "Có file thì đọc hd_chao_be, chưa có thì chỉ hiện chữ");
            Assert.IsFalse(s.Mascot.GetComponentsInChildren<Graphic>().Any(g => g.raycastTarget), "Gà con không nhận chạm");
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator Scene_CoversScreen_NoGroundLine()
        {
            yield return OpenWithKids(1);
            var s = Screen();
            Assume.That(s.Scene, Is.Not.Null, "Chưa có tranh img_ui_canh_chao (gói media) thì bỏ qua");
            var ground = s.GetComponentsInChildren<Transform>(true).First(t => t.name == "Ground");
            Assert.IsFalse(ground.gameObject.activeSelf, "Có tranh thì không vẽ nét đất tạm");
            var app = AppRoot.Instance;
            foreach (var size in ScreenSizes.All)
            {
                var rt = ScreenSizes.Apply(app, size);
                app.ShowProfiles();
                yield return null;
                Canvas.ForceUpdateCanvases();
                var panel = CanvasRect((RectTransform)Screen().Scene.transform.parent);
                var scene = CanvasRect((RectTransform)Screen().Scene.transform);
                Assert.LessOrEqual(scene.xMin, panel.xMin + .5f, $"{size}: tranh phủ mép trái");
                Assert.GreaterOrEqual(scene.xMax, panel.xMax - .5f, $"{size}: tranh phủ mép phải");
                Assert.LessOrEqual(scene.yMin, panel.yMin + .5f, $"{size}: tranh phủ mép dưới");
                Assert.GreaterOrEqual(scene.yMax, panel.yMax - .5f, $"{size}: tranh phủ mép trên");
                Assert.AreEqual(.3f, Screen().Scene.color.a, .001f, "Tranh mờ 30%");
                ScreenSizes.Reset(app, rt);
            }
        }

        [UnityTest]
        public IEnumerator RecentKid_First_WithHalo()
        {
            yield return OpenWithKids(3);
            var store = AppRoot.Instance.Progress;
            var third = store.Profiles[2].id;
            Assert.AreEqual(store.Profiles[0].id, Screen().ProfileCards[0].name.Replace("Profile_", ""), "Chưa chọn lần nào: thứ tự tạo");
            Press(Screen().ButtonForProfile(third));
            yield return null;
            Assert.IsNotNull(Object.FindAnyObjectByType<ShelfScreen>(), "Chọn bé vào Tủ sách");
            Assert.Greater(store.Profiles[2].last_played, 0L);
            AppRoot.Instance.ShowProfiles();
            yield return null;
            var first = Screen().ProfileCards[0];
            Assert.AreEqual($"Profile_{third}", first.name, "Bé vừa học đứng đầu");
            Assert.IsTrue(Pulse.IsRunning(first.transform), "Bé học gần nhất có quầng cam nhún");
            Assert.IsFalse(Pulse.IsRunning(Screen().ProfileCards[1].transform));
            var reloaded = ProgressStore.Load(StorePath);
            Assert.AreEqual(third, reloaded.ProfilesByRecent[0].id, "Thứ tự lưu xuống file");
        }

        [UnityTest]
        public IEnumerator Cards_FitAllCounts_AllSizes()
        {
            UseStubsForMissingAssets();
            foreach (var kids in new[] { 1, 3, ProfileScreen.MaxProfiles })
            {
                yield return OpenWithKids(kids);
                var app = AppRoot.Instance;
                foreach (var size in ScreenSizes.All)
                {
                    var rt = ScreenSizes.Apply(app, size);
                    app.ShowProfiles();
                    yield return null;
                    var s = Screen();
                    s.ApplyPickLayout();
                    Canvas.ForceUpdateCanvases();
                    var mascot = CanvasRect((RectTransform)s.Mascot.transform);
                    var bubble = CanvasRect(s.Mascot.BubbleRect);
                    foreach (var card in s.ProfileCards.Concat(new[] { s.NewChildButton }).Where(c => c.gameObject.activeSelf))
                    {
                        var r = CanvasRect((RectTransform)card.transform);
                        Assert.GreaterOrEqual(r.width, UiKit.MinTouch, $"{size}, {kids} bé: thẻ đủ to để chạm");
                        Assert.IsFalse(r.Overlaps(mascot), $"{size}, {kids} bé: thẻ đè gà con");
                        Assert.IsFalse(r.Overlaps(bubble), $"{size}, {kids} bé: thẻ đè bong bóng card={r} bubble={bubble} mascot={mascot}");
                    }
                    if (kids == 1)
                    {
                        Assert.GreaterOrEqual(CanvasRect((RectTransform)s.ProfileCards[0].transform).width, 400f, $"{size}: ít bé thì thẻ to");
                    }
                    if (kids == 3) ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.Name}/app_dot4_chao_be.png");
                    LayoutProbe.AssertFits(app.Canvas);
                    ScreenSizes.Reset(app, rt);
                }
                yield return DestroyApp();
            }
        }
    }
}
