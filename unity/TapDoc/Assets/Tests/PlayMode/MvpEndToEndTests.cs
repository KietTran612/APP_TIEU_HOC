using System.Collections;
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    /// <summary>
    /// Chạy trọn mọi bài trong danh sách (bản đầu tiên: bài 1–17) với tài nguyên thật: Phần 1 → Phần 2 → Kết thúc;
    /// kiểm tra bố cục từng màn ở khung 20:9 và 4:3, lưu ảnh chụp để xem lại.
    /// </summary>
    public class MvpEndToEndTests : AppTestBase
    {
        private static IEnumerable<string> Lessons() => LessonRepository.LoadIndex().lessons.Select(e => e.lesson_id);

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
