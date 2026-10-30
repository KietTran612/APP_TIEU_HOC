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
            yield return null;
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
        public IEnumerator Mascot_OutsideStageAndButtons_BothSizes()
        {
            yield return Open();
            var app = AppRoot.Instance;
            foreach (var size in new[] { new Vector2Int(2400, 1080), new Vector2Int(2048, 1536) })
            {
                var rt = new RenderTexture(size.x, size.y, 24);
                app.UiCamera.targetTexture = rt;
                app.ShowLesson(LessonId);
                yield return null;
                var s = Screen();
                var mascot = CanvasRect((RectTransform)s.Mascot.transform);
                Assert.IsFalse(mascot.Overlaps(CanvasRect(s.Stage)), "Gà con không đè vùng học");
                foreach (var b in new[] { s.BackButton, s.ReplayButton, s.NextButton })
                {
                    Assert.IsFalse(mascot.Overlaps(CanvasRect((RectTransform)b.transform)), $"Gà con không đè nút {b.name}");
                }
                ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.x}x{size.y}/app_lesson_chrome.png");
                LayoutProbe.AssertFits(app.Canvas);
                app.UiCamera.targetTexture = null;
                Object.Destroy(rt);
            }
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
            Assert.AreSame(oldRoot, s.TurningPage);
            Assert.IsFalse(s.TurningPage.GetComponent<CanvasGroup>().blocksRaycasts, "Trang đang lật không nhận chạm");
            Assert.AreNotSame(oldRoot, ((IStepView)s.CurrentView).Root, "Bước mới đã dựng bên dưới");
            CollectionAssert.Contains(AppRoot.Instance.Sfx.History, SystemSfx.PageFlip);
            CollectionAssert.DoesNotContain(AppRoot.Instance.Sfx.History, SystemSfx.Tap);
            yield return new WaitForSecondsRealtime(.6f);
            Assert.IsNull(s.TurningPage);
            Assert.IsTrue(oldRoot == null, "Lật xong thì trang cũ bị huỷ");
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
