using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>Màn Sổ bé ngoan: mỗi trang một bài, 3 ô hoa ở trên, vùng nội dung để trống, lật trang, vừa hai khung hình.</summary>
    public class BookScreenTests : AppTestBase
    {
        private static BookScreen OpenBook()
        {
            AppRoot.Instance.ShowBook();
            var screen = Object.FindAnyObjectByType<BookScreen>();
            Assert.IsNotNull(screen, "Không mở được màn Sổ bé ngoan");
            return screen;
        }

        [UnityTest]
        public IEnumerator OpensAtLastCompleted()
        {
            yield return LoadMainWithProfile();
            var ordered = Ordered();
            AppRoot.Instance.Progress.MarkCompleted(ordered[0]);
            AppRoot.Instance.Progress.MarkCompleted(ordered[2]);
            var screen = OpenBook();
            yield return null;
            Assert.AreEqual(2, screen.Spread.LeftPage, "Mở ở cặp trang có bài học xong đứng sau cùng");
            Assert.AreEqual(3, screen.Spread.PageFor(ordered[2]).FlowerCount);
            Assert.AreEqual(0, screen.Spread.PageFor(ordered[3]).FlowerCount);
            var index = AppRoot.Instance.Lessons.Index;
            Assert.AreEqual(BookShelf.LessonIds(index, BookShelf.BookIds(index)[0]).Count, screen.Spread.PageCount,
                "Mỗi bài của quyển đang mở một trang");
        }

        [UnityTest]
        public IEnumerator PrevNext_DisabledAtEnds()
        {
            yield return LoadMainWithProfile();
            var screen = OpenBook();
            yield return null;
            Assert.AreEqual(0, screen.Spread.LeftPage);
            Assert.IsFalse(screen.PrevButton.interactable, "Trang đầu: không lật lùi được");
            Assert.IsTrue(screen.NextButton.interactable);
            Press(screen.NextButton);
            yield return null;
            Assert.AreEqual(2, screen.Spread.LeftPage);
            Assert.IsTrue(screen.PrevButton.interactable);
            screen.Spread.ShowPage(screen.Spread.PageCount - 1);
            screen.RefreshButtons();
            Assert.IsFalse(screen.NextButton.interactable, "Trang cuối: không lật tới được");
        }

        [UnityTest]
        public IEnumerator Page_HasThreeSlotsAndEmptyContent()
        {
            yield return LoadMainWithProfile();
            var screen = OpenBook();
            yield return null;
            var page = screen.Spread.PageFor(Ordered()[0]);
            Assert.AreEqual(FlowerBook.FlowersPerLesson, page.Slots.Count);
            Assert.AreEqual("PageContent", page.Content.name);
            Assert.AreEqual(0, page.Content.childCount, "Phần dưới trang để trống cho nội dung sau này");
            foreach (var slot in page.Slots)
            {
                Assert.AreEqual(SystemSfx.Tap, slot.GetComponent<TapFeedback>().Sound, "Chạm ô hoa có tiếng tách");
            }
        }

        [UnityTest]
        public IEnumerator NotLearned_EmptySlots()
        {
            yield return LoadMainWithProfile();
            AppRoot.Instance.Progress.MarkCompleted(Ordered()[0]);
            var screen = OpenBook();
            yield return null;
            var learned = screen.Spread.PageFor(Ordered()[0]);
            var notLearned = screen.Spread.PageFor(Ordered()[1]);
            Assert.AreEqual(3, learned.FlowerCount);
            Assert.IsTrue(learned.Slots.All(s => s.ImageId == SystemImages.Flower && s.ImageBox.activeSelf));
            Assert.AreEqual(0, notLearned.FlowerCount);
            Assert.IsTrue(notLearned.Slots.All(s => !s.ImageBox.activeSelf), "Bài chưa học: ô trống");
        }

        [UnityTest]
        public IEnumerator HomeButton_BackToList()
        {
            yield return LoadMainWithProfile();
            var screen = OpenBook();
            yield return null;
            Press(screen.HomeButton);
            yield return null;
            Assert.IsNotNull(Object.FindAnyObjectByType<LessonListScreen>());
        }

        [UnityTest]
        public IEnumerator Swipe_Flips()
        {
            yield return LoadMainWithProfile();
            var screen = OpenBook();
            yield return null;
            var start = new PointerEventData(EventSystem.current) { position = new Vector2(1500f, 500f), pressPosition = new Vector2(1500f, 500f) };
            screen.OnBeginDrag(start);
            var end = new PointerEventData(EventSystem.current) { position = new Vector2(900f, 500f), pressPosition = new Vector2(1500f, 500f) };
            screen.OnDrag(end);
            screen.OnEndDrag(end);
            yield return null;
            Assert.AreEqual(2, screen.Spread.LeftPage, "Vuốt sang trái thì lật tới");
            var back = new PointerEventData(EventSystem.current) { position = new Vector2(1500f, 500f), pressPosition = new Vector2(900f, 500f) };
            screen.OnBeginDrag(back);
            screen.OnEndDrag(back);
            yield return null;
            Assert.AreEqual(0, screen.Spread.LeftPage, "Vuốt sang phải thì lật lùi");
        }

        [UnityTest]
        public IEnumerator FlipWithMotion_PlaysPageSoundAndCleansUp()
        {
            UseStubsForMissingAssets(); // tiếng động thật chưa nhập (Task 12): dùng tiếng giả
            yield return LoadMainWithProfile();
            var screen = OpenBook();
            yield return null;
            Motion.Scale = 1f;
            Press(screen.NextButton);
            Assert.AreEqual(2, screen.Spread.LeftPage, "Trang mới hiện ngay bên dưới");
            CollectionAssert.Contains(AppRoot.Instance.Sfx.History, SystemSfx.PageFlip);
            Assert.IsNotNull(screen.Spread.TurningPage, "Trang cũ đang lật");
            yield return new WaitForSecondsRealtime(.7f);
            Assert.IsNull(screen.Spread.TurningPage, "Lật xong thì trang cũ bị huỷ");
            LogAssert.NoUnexpectedReceived();
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
        public IEnumerator Book_Fits_AllSizes()
        {
            UseStubsForMissingAssets(); // chỉ kiểm bố cục; tranh tập 2 chưa nhập không phải điều đang kiểm
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            app.Progress.Current.name = new string('Đ', ProgressStore.MaxNameLength);
            var ordered = Ordered();
            var b06 = System.Array.IndexOf(ordered, "tv1_t1_b06");
            Assert.GreaterOrEqual(b06, 0);
            foreach (var size in ScreenSizes.All)
            {
                var rt = ScreenSizes.Apply(app, size);
                var screen = OpenBook();
                screen.Spread.ShowPage(b06);
                screen.RefreshButtons();
                yield return null;
                Canvas.ForceUpdateCanvases();
                if (size.Wide)
                {
                    if (size.Name == ScreenSizes.Phone20x9.Name) Assert.Greater(screen.BookFit.Scale, 1.2f, $"{size}: sổ to lên");
                    Assert.Greater(screen.BookFit.Scale, 1f, $"{size}: sổ to lên");
                }
                else
                {
                    Assert.AreEqual(1f, screen.BookFit.Scale, .05f, $"{size}: máy tính bảng giữ như cũ");
                }
                var book = CanvasRect((RectTransform)screen.Spread.transform);
                var title = CanvasRect(screen.Title.rectTransform);
                foreach (var b in new[] { screen.HomeButton, screen.PrevButton, screen.NextButton })
                {
                    var br = CanvasRect((RectTransform)b.transform);
                    Assert.IsFalse(book.Overlaps(br), $"{size}: sổ đè nút {b.name}");
                    Assert.IsFalse(title.Overlaps(br), $"{size}: tiêu đề đè nút {b.name}");
                }
                ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.Name}/app_book.png");
                LayoutProbe.AssertFits(app.Canvas);
                ScreenSizes.Reset(app, rt);
            }
        }

        [UnityTest]
        public IEnumerator Resize_KeepsPage()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            ScreenSizes.Apply(app, ScreenSizes.IPad43);
            var screen = OpenBook();
            screen.Spread.ShowPage(4);
            screen.RefreshButtons();
            yield return null;
            var spread = screen.Spread;

            var phone = ScreenSizes.Apply(app, ScreenSizes.Phone20x9);
            yield return null;
            yield return null;
            Assert.AreSame(spread, screen.Spread, "Đổi cỡ không dựng lại sổ");
            Assert.AreEqual(4, screen.Spread.LeftPage, "Vẫn ở trang đang xem");
            Assert.Greater(screen.BookFit.Scale, 1.2f, "Sổ to lên theo màn mới");
            ScreenSizes.Reset(app, phone);
        }

        [UnityTest]
        public IEnumerator Book_OpenBookPagesOnly()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            var book = BookShelf.BookIds(app.Lessons.Index)[1];
            app.Progress.UnlockAll = true;
            app.OpenBook(book);
            yield return null;
            var screen = OpenBook();
            yield return null;
            Assert.AreEqual(BookShelf.LessonIds(app.Lessons.Index, book).Count, screen.Spread.PageCount,
                "Sổ chỉ có trang của quyển đang mở");
        }
    }
}
