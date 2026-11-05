using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.UI;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// Khung màn học (bản thiết kế giao diện mục 9.3): nút biểu tượng, chấm tiến độ, gà con ngoài vùng học, chuyển bước
    /// như lật trang sách.
    /// </summary>
    public class LessonChromeTests : AppTestBase
    {
        private const string LessonId = "tv1_t1_b13";

        private IEnumerator Open()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            AppRoot.Instance.Speech.WaitScale = .02f;
            AppRoot.Instance.ShowLesson(LessonId);
            yield return WaitPrepared();
        }

        private static LessonScreen Screen() => Object.FindAnyObjectByType<LessonScreen>();

        private static IEnumerator CompleteStep(LessonScreen screen)
        {
            yield return ((ITestCompletable)screen.CurrentView).CompleteForTest();
            yield return null;
        }

        private static Rect CanvasRect(RectTransform rt)
        {
            var corners = new Vector3[4];
            rt.GetWorldCorners(corners);
            var canvas = (RectTransform)AppRoot.Instance.Canvas.transform;
            Vector2 min = canvas.InverseTransformPoint(corners[0]), max = canvas.InverseTransformPoint(corners[2]);
            return Rect.MinMaxRect(min.x, min.y, max.x, max.y);
        }

        [UnityTest]
        public IEnumerator Buttons_AreIconButtons()
        {
            yield return Open();
            var s = Screen();
            Assert.AreEqual(SystemIcons.Home, s.BackButton.GetComponent<IconButton>().IconId);
            Assert.AreEqual(SystemIcons.Speaker, s.ReplayButton.GetComponent<IconButton>().IconId);
            Assert.AreEqual(SystemIcons.Forward, s.NextButton.GetComponent<IconButton>().IconId);
            Assert.IsNull(s.NextButton.GetComponent<TapFeedback>().Sound, "Nút Tiếp dùng tiếng lật trang, không có tiếng tách");
            Assert.IsNull(s.ReplayButton.GetComponent<TapFeedback>().Sound, "Nút loa làm giọng đọc phát ngay: không có tiếng tách");
            Assert.AreEqual(SystemSfx.Tap, s.BackButton.GetComponent<TapFeedback>().Sound);
        }

        [UnityTest]
        public IEnumerator Dots_TrackPosition()
        {
            yield return Open();
            var s = Screen();
            Assert.AreEqual(s.Flow.TotalCount, s.Dots.Total);
            Assert.AreEqual(0, s.Dots.Current);
            yield return CompleteStep(s);
            s.NextButton.onClick.Invoke();
            yield return null;
            Assert.AreEqual(1, Screen().Dots.Current);
        }

        [Test]
        public void Dots_BarWhenTooMany()
        {
            var go = new GameObject("DotsCanvas", typeof(RectTransform), typeof(Canvas));
            try
            {
                Assert.IsTrue(ProgressDots.Create(go.transform, 40).IsBar);
                Assert.IsFalse(ProgressDots.Create(go.transform, 20).IsBar);
            }
            finally
            {
                Object.DestroyImmediate(go);
            }
        }

        [UnityTest]
        public IEnumerator NextTwice_AdvancesOnce()
        {
            yield return Open();
            var s = Screen();
            yield return CompleteStep(s);
            s.NextButton.onClick.Invoke();
            s.NextButton.onClick.Invoke();
            yield return null;
            Assert.AreEqual(1, Screen().Flow.Position);
        }

        [UnityTest]
        public IEnumerator Layout_ModeFollowsScreen_AllSizes()
        {
            UseStubsForMissingAssets(); // chỉ kiểm bố cục; tranh tập 2 chưa nhập không phải điều đang kiểm
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            foreach (var size in ScreenSizes.All)
            {
                var rt = ScreenSizes.Apply(app, size);
                app.ShowLesson(LessonId);
                yield return WaitPrepared();
                var s = Screen();
                Assert.AreEqual(size.Wide, s.IsWideLayout, $"{size}: kiểu mép");
                if (size.Wide)
                {
                    Assert.AreEqual(ScreenLayout.WideStageScale(app.KidRoot.rect.size), s.StageFit.Scale, .01f, $"{size}: phóng to");
                    Assert.GreaterOrEqual(s.StageFit.Scale, ScreenLayout.WideMinGain - .001f, $"{size}: phần học to lên");
                }
                else
                {
                    Assert.AreEqual(1f, s.StageFit.Scale, .001f, $"{size}: máy tính bảng giữ như cũ");
                }
                s.NextButton.gameObject.SetActive(true); // nút Tiếp hiện ra cũng không bị phần học đè
                Canvas.ForceUpdateCanvases();
                var stage = CanvasRect(s.Stage);
                foreach (var b in new[] { s.BackButton, s.ReplayButton, s.NextButton })
                {
                    Assert.IsFalse(stage.Overlaps(CanvasRect((RectTransform)b.transform)), $"{size}: phần học đè nút {b.name}");
                }
                ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.Name}/app_lesson_chrome.png");
                LayoutProbe.AssertFits(app.Canvas);
                ScreenSizes.Reset(app, rt);
            }
        }

        [UnityTest]
        public IEnumerator Mascot_OutsideStageAndButtons_AllSizes()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            foreach (var size in ScreenSizes.All)
            {
                var rt = ScreenSizes.Apply(app, size);
                app.ShowLesson(LessonId);
                yield return WaitPrepared();
                var s = Screen();
                s.NextButton.gameObject.SetActive(true); // nút Tiếp hiện thì gà con cũng không được đè
                Canvas.ForceUpdateCanvases();
                var mascot = CanvasRect((RectTransform)s.Mascot.transform);
                Assert.IsFalse(mascot.Overlaps(CanvasRect(s.Stage)), $"{size}: gà con không đè vùng học");
                foreach (var b in new[] { s.BackButton, s.ReplayButton, s.NextButton })
                {
                    Assert.IsFalse(mascot.Overlaps(CanvasRect((RectTransform)b.transform)), $"{size}: gà con không đè nút {b.name}");
                }
                ScreenSizes.Reset(app, rt);
            }
        }

        [UnityTest]
        public IEnumerator Wide_TallStep_ShrinksToFitScreen()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            var rt = ScreenSizes.Apply(app, ScreenSizes.Phone20x9);
            app.ShowLesson("tv1_t1_b80"); // bước đầu là bảng đọc nhiều hàng, cao hơn khung 680 của phần học
            yield return WaitPrepared();
            var s = Screen();
            Assert.IsTrue(s.IsWideLayout);
            Assert.Less(s.StageFit.Scale, ScreenLayout.WideStageScale(app.KidRoot.rect.size) - .05f,
                "Bước cao hơn khung thì phóng to ít hơn cho vừa màn");
            Assert.GreaterOrEqual(s.StageFit.Scale, 1f - .001f, "Không nhỏ hơn máy tính bảng");
            LayoutProbe.AssertFits(app.Canvas);
            ScreenSizes.Reset(app, rt);
        }

        [UnityTest]
        public IEnumerator Wide_EveryStep_NotSmallerThanTablet()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            app.Speech.WaitScale = .02f;
            var rt = ScreenSizes.Apply(app, ScreenSizes.Phone20x9);
            app.ShowLesson("tv1_t1_b15"); // bài đánh vần: các bước gọn trong khung, phải to hết cỡ
            yield return WaitPrepared();
            var s = Screen();
            for (var n = 0; n < 6 && s.Flow.Phase == Phase.Part1; n++)
            {
                Assert.GreaterOrEqual(s.StageFit.Scale, 1f - .001f, $"Bước {n}: thẻ không nhỏ hơn máy tính bảng");
                Assert.AreEqual(ScreenLayout.WideStageScale(app.KidRoot.rect.size), s.StageFit.Scale, .01f,
                    $"Bước {n}: bước gọn trong khung thì to hết cỡ (không đo lẫn bước cũ đang chờ huỷ)");
                LayoutProbe.AssertFits(app.Canvas);
                yield return CompleteStep(s);
                s.NextButton.onClick.Invoke();
                yield return null;
            }
            ScreenSizes.Reset(app, rt);
        }

        [UnityTest]
        public IEnumerator Resize_MidStep_NoRebuildNoReplay()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            app.Speech.WaitScale = .02f;
            var rt = ScreenSizes.Apply(app, ScreenSizes.IPad43);
            app.ShowLesson(LessonId);
            yield return WaitPrepared();
            var s = Screen();
            for (var i = 0; i < 30; i++) yield return null; // giọng đọc mở đầu của bước đã phát
            var view = s.CurrentView;
            var position = s.Flow.Position;
            var played = app.Speech.History.Count;
            Assert.IsFalse(s.IsWideLayout);

            var phone = ScreenSizes.Apply(app, ScreenSizes.Phone20x9);
            yield return null;
            yield return null;

            Assert.AreSame(view, s.CurrentView, "Đổi cỡ không dựng lại bước học");
            Assert.AreEqual(position, s.Flow.Position);
            Assert.AreEqual(played, app.Speech.History.Count, "Đổi cỡ không phát lại giọng đọc");
            Assert.IsTrue(s.IsWideLayout, "Màn học chuyển sang kiểu mép");
            Assert.Greater(s.StageFit.Scale, 1.05f);
            ScreenSizes.Reset(app, phone);
        }

        [UnityTest]
        public IEnumerator Next_TurnsPageLikeBook()
        {
            yield return Open();
            var s = Screen();
            yield return CompleteStep(s);
            var oldRoot = ((IStepView)s.CurrentView).Root;
            Motion.Scale = 1f;
            s.NextButton.onClick.Invoke();
            Assert.IsNotNull(s.TurningPage, "Trang cũ đang lật");
            Assert.AreNotSame(oldRoot, s.TurningPage, "Lật một bản sao để nhìn; bước cũ thật thôi chạy ngay");
            Assert.IsFalse(s.TurningPage.GetComponent<CanvasGroup>().blocksRaycasts, "Trang đang lật không nhận chạm");
            var newRoot = ((IStepView)s.CurrentView).Root;
            Assert.AreNotSame(oldRoot, newRoot, "Bước mới đã dựng bên dưới");
            Assert.AreEqual(s.Stage.childCount - 1, s.TurningPage.transform.GetSiblingIndex(), "Trang đang lật nằm trên bước mới");
            Assert.Less(newRoot.transform.GetSiblingIndex(), s.TurningPage.transform.GetSiblingIndex());
            Assert.IsNotNull(s.TurningPage.GetComponent<Image>(), "Trang đang lật có nền giấy che bước mới");
            yield return null;
            Assert.IsTrue(oldRoot == null, "Bước cũ thật bị huỷ ngay, không chờ hết lúc lật");
            CollectionAssert.Contains(AppRoot.Instance.Sfx.History, SystemSfx.PageFlip);
            CollectionAssert.DoesNotContain(AppRoot.Instance.Sfx.History, SystemSfx.Tap);
            yield return new WaitForSecondsRealtime(.6f);
            Assert.IsNull(s.TurningPage, "Lật xong thì trang lật bị huỷ");
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator Next_ScaleZero_NoLeftoverPage()
        {
            yield return Open();
            var s = Screen();
            yield return CompleteStep(s);
            s.NextButton.onClick.Invoke();
            yield return null;
            Assert.IsNull(s.TurningPage);
        }

        [UnityTest]
        public IEnumerator NextButton_PopsAndPulsesWhenShown()
        {
            yield return Open();
            var s = Screen();
            Assert.IsFalse(s.NextButton.gameObject.activeSelf);
            yield return CompleteStep(s);
            Assert.IsTrue(s.NextButton.gameObject.activeSelf);
            Assert.IsTrue(Pulse.IsRunning(s.NextButton.transform), "Nút Tiếp nhún mời bé bấm");
            s.NextButton.onClick.Invoke();
            Assert.IsFalse(Pulse.IsRunning(s.NextButton.transform));
        }

        [UnityTest]
        public IEnumerator ScreenChange_FadesIn()
        {
            yield return LoadMainWithProfile();
            Motion.Scale = 1f;
            AppRoot.Instance.ShowBook();
            var group = Object.FindAnyObjectByType<BookScreen>().GetComponent<CanvasGroup>();
            Assert.IsNotNull(group);
            Assert.Less(group.alpha, 1f, "Màn mới mờ sang rõ");
            yield return new WaitForSecondsRealtime(.4f);
            Assert.AreEqual(1f, group.alpha);
        }
    }
}
