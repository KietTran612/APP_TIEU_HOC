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
    /// Danh sách bài kiểu mới (bản thiết kế giao diện mục 9.2): bài đã học có 3 hoa nhỏ, bài đang học tới màu cam và
    /// nhún, bài chưa mở có ổ khoá, nút biểu tượng đổi bé, sổ, ôn lại.
    /// </summary>
    public class LessonListStyleTests : AppTestBase
    {
        private static LessonListScreen List()
        {
            AppRoot.Instance.ShowLessonList();
            var list = Object.FindAnyObjectByType<LessonListScreen>();
            Assert.IsNotNull(list);
            return list;
        }

        private static Color FillOf(Button card) => card.transform.Find("Fill").GetComponent<Image>().color;

        private static void AssertColor(Color expected, Color actual, string what) =>
            Assert.That(Vector4.Distance(expected, actual), Is.LessThan(1e-3f), $"{what}: {actual} khác {expected}");

        [UnityTest]
        public IEnumerator CompletedLesson_ShowsThreeFlowers()
        {
            yield return LoadMainWithProfile();
            AppRoot.Instance.Progress.MarkCompleted(Ordered()[0]);
            var list = List();
            yield return null;
            var flowers = list.ButtonFor(Ordered()[0]).transform.Find("Flowers");
            Assert.IsNotNull(flowers, "Bài đã học có hàng hoa");
            var images = flowers.GetComponentsInChildren<Image>();
            Assert.AreEqual(3, images.Length);
            var flower = AppRoot.Instance.Assets.Image(SystemImages.Flower);
            Assert.IsTrue(images.All(i => i.sprite == flower));
            Assert.IsNull(list.ButtonFor(Ordered()[1]).transform.Find("Flowers"), "Bài chưa học không có hoa");
        }

        [UnityTest]
        public IEnumerator CurrentLesson_OrangeAndPulsing()
        {
            yield return LoadMainWithProfile();
            AppRoot.Instance.Progress.MarkCompleted(Ordered()[0]);
            var list = List();
            yield return null;
            Assert.AreEqual(Ordered()[1], list.CurrentLessonId, "Bài đang học tới là bài mở đầu tiên chưa học");
            var card = list.ButtonFor(Ordered()[1]);
            AssertColor(Palette.OrangeLight, FillOf(card), "nền bài đang học tới");
            Assert.IsTrue(Pulse.IsRunning(card.transform));
            Assert.IsFalse(Pulse.IsRunning(list.ButtonFor(Ordered()[0]).transform), "Bài đã học không nhún");
        }

        [UnityTest]
        public IEnumerator Locked_HasLockIcon_NotInteractable()
        {
            yield return LoadMainWithProfile();
            var list = List();
            yield return null;
            var card = list.ButtonFor(Ordered()[2]);
            Assert.IsFalse(card.interactable);
            Assert.IsNull(card.GetComponent<CanvasGroup>(), "Không làm mờ cả thẻ; dùng màu khoá");
            AssertColor(Palette.LockedFill, FillOf(card), "nền bài chưa mở");
            var lockIcon = card.transform.Find("Lock")?.GetComponent<Image>();
            Assert.IsNotNull(lockIcon, "Bài chưa mở có ổ khoá");
            Assert.AreSame(AppRoot.Instance.Assets.Image(SystemIcons.Lock), lockIcon.sprite);
        }

        [UnityTest]
        public IEnumerator TopAndBottomButtons_AreIcons()
        {
            yield return LoadMainWithProfile();
            var list = List();
            yield return null;
            Assert.AreEqual(AppRoot.Instance.Progress.Current.avatar, list.SwitchChildButton.GetComponent<IconButton>().IconId,
                "Nút đổi bé là hình đại diện của bé");
            Assert.AreEqual(SystemIcons.Book, list.BookButton.GetComponent<IconButton>().IconId);
            Assert.AreEqual(SystemIcons.Review, list.ReviewButton.GetComponent<IconButton>().IconId);
            Assert.IsNull(list.ParentButton.GetComponent<IconButton>(), "Nút Phụ huynh vẫn là nút có chữ");
            Assert.IsNotNull(list.GetComponentInChildren<Mascot>(), "Có bạn gà con");
        }

        [UnityTest]
        public IEnumerator BookButton_OpensBook()
        {
            yield return LoadMainWithProfile();
            var list = List();
            yield return null;
            Press(list.BookButton);
            yield return null;
            Assert.IsNotNull(Object.FindAnyObjectByType<BookScreen>());
        }

        [UnityTest]
        public IEnumerator CurrentLesson_ScrolledIntoView()
        {
            yield return LoadMainWithProfile();
            var ordered = Ordered();
            Assert.Greater(ordered.Length, 70);
            for (var i = 0; i < 69; i++) AppRoot.Instance.Progress.MarkCompleted(ordered[i]);
            var list = List();
            yield return null;
            Assert.AreEqual(ordered[69], list.CurrentLessonId);
            var corners = new Vector3[4];
            ((RectTransform)list.ButtonFor(ordered[69]).transform).GetWorldCorners(corners);
            var view = list.Scroll.viewport.rect;
            foreach (var c in corners)
            {
                var local = list.Scroll.viewport.InverseTransformPoint(c);
                Assert.That(local.y, Is.InRange(view.yMin - 1f, view.yMax + 1f), "Thẻ bài đang học nằm trong vùng nhìn");
            }
        }

        [UnityTest]
        public IEnumerator Layout_BothSizes()
        {
            yield return LoadMainWithProfile();
            AppRoot.Instance.Progress.MarkCompleted(Ordered()[0]);
            AppRoot.Instance.Progress.RecordMistake(Ordered()[0], 0);
            var app = AppRoot.Instance;
            foreach (var size in new[] { new Vector2Int(2400, 1080), new Vector2Int(2048, 1536) })
            {
                var rt = new RenderTexture(size.x, size.y, 24);
                app.UiCamera.targetTexture = rt;
                List();
                yield return null;
                ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.x}x{size.y}/app_lesson_list.png");
                LayoutProbe.AssertFits(app.Canvas);
                app.UiCamera.targetTexture = null;
                Object.Destroy(rt);
            }
        }
    }
}
