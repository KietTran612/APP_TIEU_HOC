using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>Tủ sách (bản thiết kế Tủ sách mục 4–7): chọn quyển, danh sách bài theo quyển, mở quyển theo thứ tự.</summary>
    public class ShelfScreenTests : AppTestBase
    {
        private static AppRoot App => AppRoot.Instance;
        private static LessonIndex Index => App.Lessons.Index;
        private static ShelfScreen Shelf() => Object.FindAnyObjectByType<ShelfScreen>();
        private static LessonListScreen List() => Object.FindAnyObjectByType<LessonListScreen>();
        private static string BookAt(int k) => BookShelf.BookIds(Index)[k];

        /// <summary>Mở app có một bé, rồi về Tủ sách.</summary>
        private IEnumerator OpenShelf()
        {
            UseStubsForMissingAssets(); // chỉ kiểm giao diện; tranh của quyển đang làm dở không phải điều đang kiểm
            yield return LoadMainWithProfile();
            App.ShowShelf();
            yield return null;
        }

        private static void CompleteBook(string bookId)
        {
            foreach (var id in BookShelf.LessonIds(Index, bookId)) App.Progress.MarkCompleted(id);
        }

        [UnityTest]
        public IEnumerator ChooseChild_OpensShelf_WithBooksInOrder()
        {
            UseStubsForMissingAssets();
            yield return LoadMain();
            var profiles = Object.FindAnyObjectByType<ProfileScreen>();
            profiles.SimulateCreate("Na", ProfileScreen.Avatars[0]);
            yield return null;
            var shelf = Shelf();
            Assert.IsNotNull(shelf, "Tạo bé xong thì vào Tủ sách");
            Assert.IsNull(List());
            CollectionAssert.AreEqual(BookShelf.BookIds(Index), shelf.BookIds);
            StringAssert.Contains("Na", shelf.Title.text);
            foreach (var id in shelf.BookIds)
            {
                Assert.IsNotNull(shelf.CoverButton(id), id);
                Assert.AreEqual(BookShelf.Book(Index, id).title.Replace(" – ", "\n"), shelf.TitleOf(id).text);
            }
        }

        [UnityTest]
        public IEnumerator NewChild_ShelfHighlightsFirstBook()
        {
            yield return OpenShelf();
            var shelf = Shelf();
            Assert.AreEqual(ShelfBookState.Current, shelf.StateOf(BookAt(0)));
            for (var k = 1; k < shelf.BookIds.Count; k++) Assert.AreEqual(ShelfBookState.Locked, shelf.StateOf(BookAt(k)));
            Assert.IsTrue(Pulse.IsRunning(shelf.CoverButton(BookAt(0)).transform), "Quyển đang học nhún");
            Assert.AreEqual(string.Format(UiText.BookProgressFormat, 0, BookShelf.LessonIds(Index, BookAt(0)).Count),
                shelf.ProgressOf(BookAt(0)).text);
        }

        [UnityTest]
        public IEnumerator TapLockedBook_DoesNothing()
        {
            yield return OpenShelf();
            Press(Shelf().CoverButton(BookAt(1)));
            yield return null;
            Assert.IsNotNull(Shelf(), "Quyển khoá: vẫn ở Tủ sách");
            Assert.IsNull(List());
        }

        [UnityTest]
        public IEnumerator TapOpenBook_ShowsOnlyItsLessons()
        {
            yield return OpenShelf();
            Press(Shelf().CoverButton(BookAt(0)));
            yield return null;
            var list = List();
            Assert.IsNotNull(list);
            Assert.AreEqual(BookAt(0), list.BookId);
            Assert.AreEqual(BookShelf.LessonIds(Index, BookAt(0)).Count, list.LessonCount, "Chỉ có bài của quyển này");
            Assert.AreEqual(BookShelf.Book(Index, BookAt(0)).title, list.Header.text);
            Assert.AreEqual(BookAt(0), App.Progress.OpenBook, "Nhớ quyển đang mở");
        }

        [UnityTest]
        public IEnumerator ShelfButton_BackToShelf()
        {
            yield return OpenShelf();
            Press(Shelf().CoverButton(BookAt(0)));
            yield return null;
            Assert.AreEqual(SystemIcons.Shelf, List().ShelfButton.GetComponent<IconButton>().IconId);
            Press(List().ShelfButton);
            yield return null;
            Assert.IsNotNull(Shelf());
        }

        [UnityTest]
        public IEnumerator CompletedBook_ShowsDone_NextCurrent()
        {
            yield return OpenShelf();
            CompleteBook(BookAt(0));
            App.ShowShelf();
            yield return null;
            Assert.AreEqual(ShelfBookState.Done, Shelf().StateOf(BookAt(0)));
            Assert.AreEqual(ShelfBookState.Current, Shelf().StateOf(BookAt(1)));
            Press(Shelf().CoverButton(BookAt(1)));
            yield return null;
            Assert.AreEqual(BookAt(1), List().BookId, "Quyển vừa mở vào được");
        }

        [UnityTest]
        public IEnumerator UnlockAll_AllBooksOpen()
        {
            yield return OpenShelf();
            App.Progress.UnlockAll = true;
            App.ShowShelf();
            yield return null;
            foreach (var id in Shelf().BookIds) Assert.AreNotEqual(ShelfBookState.Locked, Shelf().StateOf(id), id);
        }

        [UnityTest]
        public IEnumerator ShowLessonList_LockedOpenBook_GoesToShelf()
        {
            yield return OpenShelf();
            App.Progress.OpenBook = BookAt(Shelf().BookIds.Count - 1);
            App.ShowLessonList();
            yield return null;
            Assert.IsNotNull(Shelf(), "Quyển đang mở bị khoá thì về Tủ sách");
            Assert.IsNull(List());
        }

        [UnityTest]
        public IEnumerator Shelf_MissingCover_FallsBackToColor()
        {
            // Nguồn giả: mọi ảnh bìa đều thiếu.
            var real = new ResourcesContentSource();
            var tex = new Texture2D(4, 4);
            var sprite = Sprite.Create(tex, new Rect(0, 0, 4, 4), new Vector2(.5f, .5f));
            var clip = AudioClip.Create("stub", 441, 1, 44100, false);
            AppRoot.SourceFactory = () => new FakeContentSource
            {
                Fallback = (kind, id) => kind == ContentKind.Image && id.StartsWith("img_bia_")
                    ? null
                    : real.Load(kind, id) ?? kind switch
                    {
                        ContentKind.Image => sprite,
                        ContentKind.Speech or ContentKind.Sfx => clip,
                        _ => null,
                    },
            };
            yield return LoadMainWithProfile();
            App.ShowShelf();
            yield return null;
            foreach (var id in Shelf().BookIds)
            {
                Assert.IsNotNull(Shelf().TitleOf(id), id);
                Assert.IsTrue(Shelf().TitleOf(id).text.Length > 0);
            }
            LogAssert.NoUnexpectedReceived();
            AppRoot.SourceFactory = null;
            Object.Destroy(tex);
        }

        [UnityTest]
        public IEnumerator Shelf_FitsAllSizes()
        {
            yield return OpenShelf();
            CompleteBook(BookAt(0)); // đủ ba trạng thái: xong, đang học, khoá
            foreach (var size in ScreenSizes.All)
            {
                var rt = ScreenSizes.Apply(App, size);
                App.ShowShelf();
                yield return null;
                Canvas.ForceUpdateCanvases();
                ScreenProbe.Save(App.UiCamera, $"TestOutput/screens/{size.Name}/app_shelf.png");
                LayoutProbe.AssertFits(App.Canvas);
                foreach (var id in BookShelf.BookIds(Index).Take(2))
                {
                    App.OpenBook(id);
                    yield return null;
                    Canvas.ForceUpdateCanvases();
                    ScreenProbe.Save(App.UiCamera, $"TestOutput/screens/{size.Name}/app_lesson_list_{id}.png");
                    LayoutProbe.AssertFits(App.Canvas);
                }
                ScreenSizes.Reset(App, rt);
            }
        }
    }
}
