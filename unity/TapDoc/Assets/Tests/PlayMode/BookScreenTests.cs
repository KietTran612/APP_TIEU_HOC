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
            Assert.AreEqual(ordered.Length, screen.Spread.PageCount, "Mỗi bài một trang");
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

        [UnityTest]
        public IEnumerator LongTitles_Fit()
        {
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            app.Progress.Current.name = new string('Đ', ProgressStore.MaxNameLength);
            var ordered = Ordered();
            var b06 = System.Array.IndexOf(ordered, "tv1_t1_b06");
            Assert.GreaterOrEqual(b06, 0);
            foreach (var size in new[] { new Vector2Int(2400, 1080), new Vector2Int(2048, 1536) })
            {
                var rt = new RenderTexture(size.x, size.y, 24);
                app.UiCamera.targetTexture = rt;
                var screen = OpenBook();
                screen.Spread.ShowPage(b06);
                screen.RefreshButtons();
                yield return null;
                Assert.IsNotNull(screen.Spread.PageFor("tv1_t1_b06"));
                ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.x}x{size.y}/app_book.png");
                LayoutProbe.AssertFits(app.Canvas);
                app.UiCamera.targetTexture = null;
                Object.Destroy(rt);
            }
        }
    }
}
