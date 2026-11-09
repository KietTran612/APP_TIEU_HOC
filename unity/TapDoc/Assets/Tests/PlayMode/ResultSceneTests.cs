using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// Cảnh học xong bài (bản thiết kế giao diện mục 8.4): sổ mở ở trang của bài, 3 bông hoa bay vào ô, đóng dấu
    /// "Bé ngoan", gà con khen, rồi mới hiện nút; chạm màn thì nhảy tới cuối.
    /// </summary>
    public class ResultSceneTests : AppTestBase
    {
        private static ResultScreen Result()
        {
            var screen = Object.FindAnyObjectByType<ResultScreen>();
            Assert.IsNotNull(screen, "Không có màn kết thúc bài");
            return screen;
        }

        private static int Count(string sfx) => AppRoot.Instance.Sfx.History.Count(id => id == sfx);

        [UnityTest]
        public IEnumerator NewLesson_ThreeFlowersFly()
        {
            yield return LoadMainWithProfile();
            var id = Ordered()[0];
            AppRoot.Instance.ShowResult(id);
            yield return null;
            var screen = Result();
            Assert.IsTrue(screen.IsSceneDone);
            Assert.AreEqual(3, screen.FlownFlowers);
            Assert.AreEqual(3, screen.Spread.PageFor(id).FlowerCount, "Sổ mở ở trang của bài, đủ 3 hoa");
            Assert.AreEqual(3, Count(SystemSfx.FlowerFly));
            Assert.AreEqual(1, Count(SystemSfx.Stamp));
            Assert.AreEqual(MascotMood.Cheer, screen.Mascot.LastMood);
            Assert.IsTrue(AppRoot.Instance.Progress.IsCompleted(id), "Bài được ghi là đã học xong");
            Assert.IsTrue(screen.ToListButton.gameObject.activeInHierarchy);
            Assert.IsTrue(screen.NextLessonButton.gameObject.activeInHierarchy);
        }

        [UnityTest]
        public IEnumerator Relearn_NoFlowersFly_StampStill()
        {
            yield return LoadMainWithProfile();
            var id = Ordered()[0];
            AppRoot.Instance.Progress.MarkCompleted(id);
            AppRoot.Instance.ShowResult(id);
            yield return null;
            var screen = Result();
            Assert.AreEqual(0, screen.FlownFlowers, "Học lại không thêm hoa");
            Assert.AreEqual(3, screen.Spread.PageFor(id).FlowerCount);
            Assert.AreEqual(0, Count(SystemSfx.FlowerFly));
            Assert.AreEqual(1, Count(SystemSfx.Stamp), "Vẫn đóng dấu và khen");
        }

        [UnityTest]
        public IEnumerator Review_NoBook_NoNextButton()
        {
            yield return LoadMainWithProfile();
            AppRoot.Instance.ShowResult(ReviewSession.LessonId);
            yield return null;
            var screen = Result();
            Assert.IsNull(screen.Spread, "Phiên ôn không có sổ");
            Assert.IsNull(screen.NextLessonButton);
            Assert.IsTrue(screen.ToListButton.gameObject.activeInHierarchy);
            Assert.AreEqual(MascotMood.Cheer, screen.Mascot.LastMood);
            Assert.AreEqual(0, Count(SystemSfx.FlowerFly));
        }

        [UnityTest]
        public IEnumerator TapSkips_ShowsButtons()
        {
            yield return LoadMainWithProfile();
            Motion.Scale = 1f;
            var id = Ordered()[0];
            AppRoot.Instance.ShowResult(id);
            yield return null;
            var screen = Result();
            Assert.IsFalse(screen.IsSceneDone, "Cảnh đang chạy");
            Assert.IsFalse(screen.ToListButton.gameObject.activeInHierarchy, "Nút chỉ hiện khi cảnh xong");
            screen.GetComponentInChildren<SceneSkipper>().OnPointerClick(new PointerEventData(EventSystem.current));
            yield return null;
            Assert.IsTrue(screen.IsSceneDone);
            Assert.IsTrue(screen.ToListButton.gameObject.activeInHierarchy);
            Assert.AreEqual(3, screen.Spread.PageFor(id).FlowerCount, "Bỏ qua thì hoa đã dán đủ");
            yield return new WaitForSecondsRealtime(3.5f);
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator SceneRunsToEndWithMotion()
        {
            yield return LoadMainWithProfile();
            Motion.Scale = 1f;
            AppRoot.Instance.ShowResult(Ordered()[0]);
            yield return null;
            var screen = Result();
            var deadline = Time.realtimeSinceStartup + 6f;
            while (!screen.IsSceneDone && Time.realtimeSinceStartup < deadline) yield return null;
            Assert.IsTrue(screen.IsSceneDone, "Cảnh tự chạy hết trong vài giây");
            Assert.AreEqual(3, screen.FlownFlowers);
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator LeaveMidScene_NoErrors()
        {
            yield return LoadMainWithProfile();
            Motion.Scale = 1f;
            AppRoot.Instance.ShowResult(Ordered()[0]);
            yield return new WaitForSecondsRealtime(.2f);
            Result().ToListButton.onClick.Invoke(); // nút đã có nhưng còn ẩn: gọi thẳng như khi bé thoát giữa chừng
            yield return new WaitForSecondsRealtime(2f);
            Assert.IsNotNull(Object.FindAnyObjectByType<LessonListScreen>());
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator MissingFlowerImage_ReportsErrorAndFinishes()
        {
            var clip = AudioClip.Create("stub", 441, 1, 44100, false);
            var real = new ResourcesContentSource();
            AppRoot.SourceFactory = () => TestCatalog.Source(
                _ => clip,
                imageId => imageId == SystemImages.Flower ? null : real.Load(ContentKind.Image, imageId) as Sprite);
            try
            {
                LogAssert.Expect(LogType.Error, "[TapDoc] Thiếu tranh: " + SystemImages.Flower);
                yield return LoadMainWithProfile();
                AppRoot.Instance.ShowResult(Ordered()[0]);
                yield return null;
                Assert.IsTrue(Result().IsSceneDone, "Thiếu hình hoa thì cảnh vẫn chạy hết");
            }
            finally
            {
                AppRoot.SourceFactory = null;
                Object.Destroy(clip);
            }
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
        public IEnumerator Result_Fits_AllSizes()
        {
            UseStubsForMissingAssets(); // chỉ kiểm bố cục; tranh tập 2 chưa nhập không phải điều đang kiểm
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            foreach (var size in ScreenSizes.All)
            {
                var rt = ScreenSizes.Apply(app, size);
                app.ShowResult(Ordered()[0]);
                yield return null;
                var screen = Result();
                screen.SkipScene();
                yield return null;
                Canvas.ForceUpdateCanvases();
                if (size.Wide) Assert.Greater(screen.BookFit.Scale, 1f, $"{size}: sổ to lên");
                else Assert.AreEqual(1f, screen.BookFit.Scale, .05f, $"{size}: máy tính bảng giữ như cũ");
                var book = CanvasRect((RectTransform)screen.Spread.transform);
                var mascot = CanvasRect((RectTransform)screen.Mascot.transform);
                foreach (var b in new[] { screen.ToListButton, screen.NextLessonButton })
                {
                    var br = CanvasRect((RectTransform)b.transform);
                    Assert.IsFalse(book.Overlaps(br), $"{size}: sổ đè nút {b.name}");
                    Assert.IsFalse(mascot.Overlaps(br), $"{size}: gà con đè nút {b.name}");
                }
                Assert.IsFalse(book.Overlaps(mascot), $"{size}: gà con đè sổ");
                ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.Name}/app_result.png");
                LayoutProbe.AssertFits(app.Canvas);
                ScreenSizes.Reset(app, rt);
            }
        }

        [UnityTest]
        public IEnumerator Resize_DuringScene_SkipsToEnd_PraiseOnce()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            ScreenSizes.Apply(app, ScreenSizes.IPad43);
            Motion.Scale = 1f;
            app.ShowResult(Ordered()[0]);
            yield return null;
            var screen = Result();
            Assert.IsFalse(screen.IsSceneDone, "Cảnh đang chạy");

            var phone = ScreenSizes.Apply(app, ScreenSizes.Phone20x9);
            yield return null;
            yield return null;
            Assert.IsTrue(screen.IsSceneDone, "Đổi cỡ giữa cảnh thì nhảy tới cuối");
            yield return new WaitForSecondsRealtime(1.5f);
            Assert.AreEqual(1, app.Speech.History.Count(id => id == SystemAudio.khen_hoan_thanh), "Lời khen chỉ phát một lần");
            Assert.AreEqual(3, screen.Spread.PageFor(Ordered()[0]).FlowerCount);
            ScreenSizes.Reset(app, phone);
        }

        [UnityTest]
        public IEnumerator FlowerLands_AtSlotSize_Wide()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            var rt = ScreenSizes.Apply(app, ScreenSizes.Phone20x9);
            app.ShowResult(Ordered()[0]);
            yield return null;
            var screen = Result();
            Assert.Greater(screen.BookFit.Scale, 1.2f);
            Assert.AreEqual(screen.BookFit.Scale, screen.FlowerLandingScale, .02f, "Hoa bay hạ cánh đúng cỡ ô của sổ đã phóng to");
            ScreenSizes.Reset(app, rt);
        }

        [UnityTest]
        public IEnumerator EmptySlots_StayLitUntilTheirFlowerLands()
        {
            yield return LoadMainWithProfile();
            Motion.Scale = 1f;
            var id = Ordered()[0];
            AppRoot.Instance.ShowResult(id);
            yield return null;
            var screen = Result();
            var deadline = Time.realtimeSinceStartup + 3f;
            while (screen.FlownFlowers < 1 && Time.realtimeSinceStartup < deadline) yield return null;
            Assert.AreEqual(1, screen.FlownFlowers);
            var slots = screen.Spread.PageFor(id).Slots;
            for (var i = 1; i < slots.Count; i++)
            {
                Assert.That(Vector4.Distance(slots[i].GetComponent<UnityEngine.UI.Image>().color, Palette.Orange),
                    Is.LessThan(1e-3f), $"Ô {i} chưa có hoa vẫn sáng viền cam");
            }
            screen.SkipScene();
            yield return null;
        }

        private static LessonIndex Idx => AppRoot.Instance.Lessons.Index;

        [UnityTest]
        public IEnumerator EndOfBook_ShowsShelfButton_NotNextLesson()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            var books = BookShelf.BookIds(Idx);
            var ids = BookShelf.LessonIds(Idx, books[0]);
            foreach (var id in ids.Take(ids.Count - 1)) app.Progress.MarkCompleted(id);
            app.ShowResult(ids[ids.Count - 1]);
            yield return null;
            var screen = Result();
            Assert.IsNull(screen.NextLessonButton, "Hết quyển: không có Bài tiếp");
            Assert.IsNotNull(screen.ShelfButton, "Hết quyển: có nút Tủ sách");
            Assert.AreEqual(SystemIcons.Shelf, screen.ShelfButton.GetComponent<IconButton>().IconId);
            Press(screen.ShelfButton);
            yield return null;
            var shelf = Object.FindAnyObjectByType<ShelfScreen>();
            Assert.IsNotNull(shelf);
            Assert.AreEqual(books[1], shelf.CelebratedBookId, "Quyển vừa mở khoá chạy hiệu ứng");
            Assert.AreEqual(ShelfBookState.Current, shelf.StateOf(books[1]));
        }

        [UnityTest]
        public IEnumerator MidBook_NextLessonStaysInBook()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            var ids = BookShelf.LessonIds(Idx, BookShelf.BookIds(Idx)[0]);
            AppRoot.Instance.ShowResult(ids[0]);
            yield return null;
            Assert.IsNotNull(Result().NextLessonButton);
            Assert.IsNull(Result().ShelfButton);
        }

        [UnityTest]
        public IEnumerator LastBook_LastLesson_NoNextNoShelf()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile(unlockAll: true);
            var books = BookShelf.BookIds(Idx);
            var last = BookShelf.LessonIds(Idx, books[books.Count - 1]).Last();
            AppRoot.Instance.ShowResult(last);
            yield return null;
            Assert.IsNull(Result().NextLessonButton);
            Assert.IsNull(Result().ShelfButton);
            Assert.IsTrue(Result().ToListButton.gameObject.activeInHierarchy);
        }

        [UnityTest]
        public IEnumerator ResultBook_ShowsOnlyLessonsOfThatBook()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            var book = BookShelf.BookIds(Idx)[0];
            AppRoot.Instance.ShowResult(BookShelf.LessonIds(Idx, book)[0]);
            yield return null;
            Assert.AreEqual(BookShelf.LessonIds(Idx, book).Count, Result().Spread.PageCount);
        }
    }
}
