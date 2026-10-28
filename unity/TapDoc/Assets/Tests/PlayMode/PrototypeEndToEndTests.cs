using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    /// <summary>Chạy trọn 3 bài mẫu với tài nguyên thật: Phần 1 → Phần 2 → Kết thúc; kiểm tra bố cục từng màn.</summary>
    public class PrototypeEndToEndTests
    {
        private static readonly string[] Lessons = { "tv1_t1_b04", "tv1_t1_b13", "tv1_t1_b42" };

        [UnityTearDown]
        public IEnumerator TearDown()
        {
            if (AppRoot.Instance != null)
            {
                if (AppRoot.Instance.Speech != null) AppRoot.Instance.Speech.Stop();
                var cam = AppRoot.Instance.UiCamera;
                if (cam != null && cam.targetTexture != null)
                {
                    var rt = cam.targetTexture;
                    cam.targetTexture = null;
                    Object.Destroy(rt);
                }
                Object.Destroy(AppRoot.Instance.gameObject);
            }
            yield return null;
        }

        private static IEnumerator OpenLesson(string id, Vector2Int? size = null)
        {
            SceneManager.LoadScene("Main");
            yield return null;
            yield return null;
            var app = AppRoot.Instance;
            Assert.IsNotNull(app, "AppRoot chưa khởi động trong scene Main");
            app.Speech.WaitScale = .02f;
            if (size.HasValue) app.UiCamera.targetTexture = new RenderTexture(size.Value.x, size.Value.y, 24);
            app.ShowLesson(id);
            yield return null;
        }

        /// <summary>Đi hết bài; ở mỗi màn gọi <paramref name="onView"/> trước khi làm xong màn đó.</summary>
        private static IEnumerator Walk(System.Action<LessonScreen, int> onView = null)
        {
            var screen = Object.FindAnyObjectByType<LessonScreen>();
            var n = 0;
            while (screen != null && screen.Flow.Phase != Phase.Done)
            {
                yield return null;
                onView?.Invoke(screen, n++);
                yield return ((ITestCompletable)screen.CurrentView).CompleteForTest();
                if (screen.Flow.Phase == Phase.Part1) screen.NextButton.onClick.Invoke();
                yield return new WaitForSeconds(.2f);
                screen = Object.FindAnyObjectByType<LessonScreen>();
            }
        }

        [UnityTest]
        public IEnumerator AllLessons_EndToEnd([ValueSource(nameof(Lessons))] string id)
        {
            yield return OpenLesson(id);
            yield return Walk();
            Assert.IsNotNull(Object.FindAnyObjectByType<ResultScreen>(), "Không tới màn kết quả");
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator Layout_AllSteps_FitAndNoOverflow([ValueSource(nameof(Lessons))] string id)
        {
            foreach (var size in new[] { new Vector2Int(2400, 1080), new Vector2Int(2048, 1536) })
            {
                yield return OpenLesson(id, size);
                var dir = $"TestOutput/screens/{size.x}x{size.y}";
                yield return Walk((screen, n) =>
                {
                    var phase = screen.Flow.Phase == Phase.Part1 ? "p1" : "p2";
                    var name = $"{dir}/{id}_{n:00}_{phase}_{screen.Flow.StepIndex}.png";
                    ScreenProbe.Save(AppRoot.Instance.UiCamera, name);
                    LayoutProbe.AssertFits(AppRoot.Instance.Canvas);
                });
                yield return null;
                ScreenProbe.Save(AppRoot.Instance.UiCamera, $"{dir}/{id}_zz_result.png");
                LayoutProbe.AssertFits(AppRoot.Instance.Canvas);
                yield return TearDown();
            }
        }
    }
}
