using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>Ôn lại: làm lại đúng các lượt bé đã nhầm; làm đúng thì xóa, nhầm nữa thì tăng số lần nhầm.</summary>
    public class ReviewSessionTests : AppTestBase
    {
        [UnityTest]
        public IEnumerator Review_PlaysMistakenRoundsAndClearsThem()
        {
            yield return LoadMainWithProfile();
            var s = AppRoot.Instance.Progress;
            s.RecordMistake("tv1_t1_b13", 0);
            s.RecordMistake("tv1_t1_b04", 3);
            AppRoot.Instance.Speech.WaitScale = .02f;
            AppRoot.Instance.ShowReview();
            yield return null;
            var screen = Object.FindAnyObjectByType<LessonScreen>();
            Assert.AreEqual(2, screen.Flow.TotalCount);
            yield return WalkAll(screen);
            Assert.AreEqual(0, s.Mistakes().Count);
            Assert.AreEqual(0, ProgressStore.Load(StorePath).Current.mistakes.Count, "Kết quả ôn chưa được lưu xuống file");
        }

        [UnityTest]
        public IEnumerator StaleMistake_IsDropped()
        {
            yield return LoadMainWithProfile();
            var s = AppRoot.Instance.Progress;
            s.RecordMistake("tv1_t1_b13", 99);
            s.RecordMistake("tv1_t1_b99", 0);
            s.RecordMistake("tv1_t1_b13", 1);
            var r = ReviewSession.Build(s, LessonRepository.Load);
            Assert.AreEqual(1, r.Lesson.part2.Count);
            Assert.AreEqual(1, s.Mistakes().Count);
            Assert.AreEqual(("tv1_t1_b13", 1), r.Sources.Single());
        }

        [UnityTest]
        public IEnumerator Review_MistakeAgain_KeepsAndCountsIt()
        {
            yield return LoadMainWithProfile();
            var s = AppRoot.Instance.Progress;
            s.RecordMistake("tv1_t1_b13", 0);
            AppRoot.Instance.Speech.WaitScale = .02f;
            AppRoot.Instance.ShowReview();
            yield return null;
            yield return WalkWithOneMistake(Object.FindAnyObjectByType<LessonScreen>());
            var m = s.Mistakes().Single();
            Assert.AreEqual(("tv1_t1_b13", 0, 2), (m.lesson_id, m.round, m.count));
        }

        [UnityTest]
        public IEnumerator ReviewButton_OpensReview_ResultDoesNotCompleteOrOfferNextLesson()
        {
            yield return LoadMainWithProfile();
            var s = AppRoot.Instance.Progress;
            s.RecordMistake("tv1_t1_b13", 0);
            AppRoot.Instance.Speech.WaitScale = .02f;
            AppRoot.Instance.ShowLessonList();
            yield return null;
            Press(Object.FindAnyObjectByType<LessonListScreen>().ReviewButton);
            yield return null;

            var screen = Object.FindAnyObjectByType<LessonScreen>();
            Assert.IsNotNull(screen, "Nút Ôn lại không mở phiên ôn");
            yield return WalkAll(screen);

            var result = Object.FindAnyObjectByType<ResultScreen>();
            Assert.IsNotNull(result, "Hết phiên ôn không tới màn kết quả");
            Assert.IsNull(result.NextLessonButton, "Màn kết quả của phiên ôn không có nút Học bài tiếp");
            Assert.IsFalse(s.Current.lessons.Any(l => l.lesson_id == ReviewSession.LessonId), "Phiên ôn không phải là một bài đã học");
            Assert.IsFalse(s.IsUnlocked(Ordered(), Ordered()[1]), "Ôn lại không được mở bài mới");
        }
    }
}
