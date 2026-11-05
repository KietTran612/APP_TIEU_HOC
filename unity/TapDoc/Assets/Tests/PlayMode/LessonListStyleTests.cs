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

        [Test]
        public void ColumnsFor_Values()
        {
            Assert.AreEqual(6, LessonListScreen.ColumnsFor(1440f), "Máy tính bảng: 6 cột như cũ");
            Assert.AreEqual(10, LessonListScreen.ColumnsFor(2400f));
            Assert.AreEqual(8, LessonListScreen.ColumnsFor(2017.1f));
            Assert.AreEqual(6, LessonListScreen.ColumnsFor(1000f), "Không ít hơn 6 cột");
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
        public IEnumerator Columns_FollowFrame_AllSizes()
        {
            UseStubsForMissingAssets(); // chỉ kiểm bố cục; tranh tập 2 chưa nhập không phải điều đang kiểm
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            app.Progress.RecordMistake(Ordered()[0], 0);
            foreach (var size in ScreenSizes.All)
            {
                var rt = ScreenSizes.Apply(app, size);
                var list = List();
                yield return null;
                Canvas.ForceUpdateCanvases();
                Assert.AreEqual(LessonListScreen.ColumnsFor(app.KidRoot.rect.width), list.Columns, $"{size}: số cột");
                foreach (var grid in list.Scroll.content.GetComponentsInChildren<GridLayoutGroup>())
                {
                    Assert.AreEqual(list.Columns, grid.constraintCount, $"{size}: mọi lưới cùng số cột");
                }
                var view = CanvasRect(list.Scroll.viewport);
                foreach (var b in new[] { list.SwitchChildButton, list.BookButton, list.ParentButton, list.ReviewButton })
                {
                    Assert.IsFalse(view.Overlaps(CanvasRect((RectTransform)b.transform)), $"{size}: vùng cuộn đè nút {b.name}");
                }
                ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.Name}/app_lesson_list.png");
                LayoutProbe.AssertFits(app.Canvas);
                ScreenSizes.Reset(app, rt);
            }
        }

        [UnityTest]
        public IEnumerator Resize_KeepsScrollPosition()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            var rt = ScreenSizes.Apply(app, ScreenSizes.IPad43);
            var list = List();
            yield return null;
            var ordered = Ordered();
            var target = ordered[60];
            list.ScrollTo(target);
            Canvas.ForceUpdateCanvases();
            var scroll = list.Scroll;

            var phone = ScreenSizes.Apply(app, ScreenSizes.Phone20x9);
            yield return null;
            yield return null;
            Canvas.ForceUpdateCanvases();
            Assert.AreSame(scroll, list.Scroll, "Đổi cỡ không dựng lại danh sách");
            Assert.AreEqual(10, list.Columns);
            var corners = new Vector3[4];
            ((RectTransform)list.ButtonFor(target).transform).GetWorldCorners(corners);
            var view = list.Scroll.viewport.rect;
            foreach (var c in corners)
            {
                var local = list.Scroll.viewport.InverseTransformPoint(c);
                Assert.That(local.y, Is.InRange(view.yMin - 1f, view.yMax + 1f), "Bài đang xem vẫn nằm trong vùng nhìn sau khi đổi cỡ");
            }
            ScreenSizes.Reset(app, phone); // rt cũ đã bị Apply huỷ
        }
    }
}
