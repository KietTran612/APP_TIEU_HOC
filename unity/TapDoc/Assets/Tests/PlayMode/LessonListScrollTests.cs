using System.Collections;
using System.Linq;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.UI;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>Danh sách bài cuộn tới được thẻ cuối và hiện tiêu đề theo phần của sách.</summary>
    public class LessonListScrollTests : AppTestBase
    {
        [UnityTest]
        public IEnumerator LastLesson_ReachableByScroll()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            var list = Object.FindAnyObjectByType<LessonListScreen>();
            var last = Ordered().Last();
            list.ScrollTo(last);
            yield return null;
            Assert.IsTrue(IsOnScreen(list, list.ButtonFor(last)));
            Assert.IsTrue(list.ButtonFor(last).interactable);
            LayoutProbe.AssertFits(AppRoot.Instance.Canvas);
        }

        [UnityTest]
        public IEnumerator FirstLesson_VisibleAtStart()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            var list = Object.FindAnyObjectByType<LessonListScreen>();
            Assert.IsTrue(IsOnScreen(list, list.ButtonFor(Ordered()[0])));
            LayoutProbe.AssertFits(AppRoot.Instance.Canvas);
        }

        [UnityTest]
        public IEnumerator SectionHeader_LettersShown()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            var list = Object.FindAnyObjectByType<LessonListScreen>();
            var labels = list.GetComponentsInChildren<TMP_Text>().Select(t => t.text).ToList();
            Assert.That(labels, Has.Member(UiText.PartLetters));
            if (!LessonRepository.LoadIndex().lessons.Any(e => e.lesson_no >= 42))
                Assert.That(labels, Has.No.Member(UiText.PartRimes));
        }

        [UnityTest]
        public IEnumerator ScrollTo_UnknownId_DoesNothing()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            var list = Object.FindAnyObjectByType<LessonListScreen>();
            var position = list.Scroll.content.anchoredPosition;
            list.ScrollTo("khong_co");
            Assert.AreEqual(position, list.Scroll.content.anchoredPosition);
        }

        /// <summary>Cả bốn góc thẻ phải nằm trong vùng nhìn của danh sách, sai số một pixel.</summary>
        private static bool IsOnScreen(LessonListScreen list, Button b)
        {
            var corners = new Vector3[4];
            ((RectTransform)b.transform).GetWorldCorners(corners);
            var viewport = list.Scroll.viewport;
            var rect = viewport.rect;
            foreach (var corner in corners)
            {
                var local = viewport.InverseTransformPoint(corner);
                if (local.x < rect.xMin - 1f || local.x > rect.xMax + 1f ||
                    local.y < rect.yMin - 1f || local.y > rect.yMax + 1f) return false;
            }
            return true;
        }
    }
}
