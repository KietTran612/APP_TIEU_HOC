using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    /// <summary>
    /// Chạy trọn bài mẫu 42 (vần mới) với tài nguyên thật. Bài 42 không nằm trong danh sách bài nên chỉ test này chạy tới;
    /// bài 4 và 13 đã có trong <see cref="MvpEndToEndTests"/>.
    /// </summary>
    public class PrototypeEndToEndTests : AppTestBase
    {
        private static readonly string[] Lessons = { "tv1_t1_b42" };

        /// <summary>Mở app với một bé đã mở mọi bài, rồi vào thẳng bài <paramref name="id"/> (nạp theo mã).</summary>
        private IEnumerator OpenLesson(string id, Vector2Int? size = null)
        {
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            app.Speech.WaitScale = .02f;
            if (size.HasValue) app.UiCamera.targetTexture = new RenderTexture(size.Value.x, size.Value.y, 24);
            app.ShowLesson(id);
            yield return null;
        }

        [UnityTest]
        public IEnumerator AllLessons_EndToEnd([ValueSource(nameof(Lessons))] string id)
        {
            yield return OpenLesson(id);
            yield return WalkAll(Object.FindAnyObjectByType<LessonScreen>());
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
                yield return WalkAll(Object.FindAnyObjectByType<LessonScreen>(), (screen, n) =>
                {
                    var phase = screen.Flow.Phase == Phase.Part1 ? "p1" : "p2";
                    var name = $"{dir}/{id}_{n:00}_{phase}_{screen.Flow.StepIndex}.png";
                    ScreenProbe.Save(AppRoot.Instance.UiCamera, name);
                    LayoutProbe.AssertFits(AppRoot.Instance.Canvas);
                });
                yield return null;
                ScreenProbe.Save(AppRoot.Instance.UiCamera, $"{dir}/{id}_zz_result.png");
                LayoutProbe.AssertFits(AppRoot.Instance.Canvas);
                yield return DestroyApp();
            }
        }
    }
}
