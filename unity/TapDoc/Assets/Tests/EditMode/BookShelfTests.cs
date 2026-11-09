using System;
using System.Collections.Generic;
using System.IO;
using NUnit.Framework;

namespace TapDoc.Tests
{
    /// <summary>Luật mở quyển và bài theo quyển (bản thiết kế Tủ sách mục 7).</summary>
    public class BookShelfTests
    {
        private string _path;
        private ProgressStore _store;
        private LessonIndex _index;

        [SetUp]
        public void SetUp()
        {
            _path = Path.Combine(Path.GetTempPath(), $"tapdoc_shelf_test_{Guid.NewGuid():N}.json");
            _store = new ProgressStore(_path);
            _store.CreateProfile("Na", "img_chung_avatar_01");
            _index = new LessonIndex
            {
                books = new List<BookEntry>
                {
                    new() { book_id = "A", title = "Quyển A", grade = 1 },
                    new() { book_id = "B", title = "Quyển B", grade = 1 },
                    new() { book_id = "C", title = "Quyển C", grade = 2 },
                },
                lessons = new List<LessonEntry>
                {
                    new() { lesson_id = "a1", book = "A" }, new() { lesson_id = "a2", book = "A" },
                    new() { lesson_id = "b1", book = "B" }, new() { lesson_id = "b2", book = "B" },
                    new() { lesson_id = "c1", book = "C", grade = 2 },
                },
            };
        }

        [TearDown]
        public void TearDown()
        {
            foreach (var f in new[] { _path, _path + ".tmp", _path + ".bak" })
            {
                if (File.Exists(f)) File.Delete(f);
            }
        }

        [Test]
        public void Books_InIndexOrder()
        {
            CollectionAssert.AreEqual(new[] { "A", "B", "C" }, BookShelf.BookIds(_index));
            CollectionAssert.AreEqual(new[] { "b1", "b2" }, BookShelf.LessonIds(_index, "B"));
            Assert.AreEqual("B", BookShelf.BookOf(_index, "b2"));
            Assert.AreEqual("Quyển C", BookShelf.Book(_index, "C").title);
        }

        [Test]
        public void Books_FallbackFromLessons_WhenNoBooks()
        {
            _index.books.Clear();
            CollectionAssert.AreEqual(new[] { "A", "B", "C" }, BookShelf.BookIds(_index));
            Assert.IsNull(BookShelf.Book(_index, "A"));
        }

        [Test]
        public void FirstBookAlwaysUnlocked()
        {
            Assert.IsTrue(BookShelf.IsBookUnlocked(_index, _store, "A"));
            Assert.IsFalse(BookShelf.IsBookUnlocked(_index, _store, "B"));
            Assert.IsFalse(BookShelf.IsBookUnlocked(_index, _store, "C"));
        }

        [Test]
        public void NextBook_UnlocksOnlyWhenPreviousAllDone()
        {
            _store.MarkCompleted("a1");
            Assert.IsFalse(BookShelf.IsBookUnlocked(_index, _store, "B"), "Còn bài a2 chưa học");
            _store.MarkCompleted("a2");
            Assert.IsTrue(BookShelf.IsBookUnlocked(_index, _store, "B"));
            Assert.IsTrue(BookShelf.IsBookDone(_index, _store, "A"));
            Assert.IsFalse(BookShelf.IsBookUnlocked(_index, _store, "C"), "Quyển C chờ xong quyển B");
        }

        [Test]
        public void UnlockAll_OpensEveryBook()
        {
            _store.UnlockAll = true;
            foreach (var id in new[] { "A", "B", "C" }) Assert.IsTrue(BookShelf.IsBookUnlocked(_index, _store, id), id);
            Assert.IsTrue(BookShelf.IsLessonUnlocked(_index, _store, "c1"));
        }

        [Test]
        public void LessonInLockedBook_IsLocked()
        {
            _store.MarkCompleted("b1"); // bé đã lỡ học b1 khi quyển B còn mở sẵn
            Assert.IsFalse(BookShelf.IsLessonUnlocked(_index, _store, "b1"), "Quyển khoá thì bài trong đó khoá hẳn");
        }

        [Test]
        public void LessonChain_WithinBook()
        {
            Assert.IsTrue(BookShelf.IsLessonUnlocked(_index, _store, "a1"));
            Assert.IsFalse(BookShelf.IsLessonUnlocked(_index, _store, "a2"));
            _store.MarkCompleted("a1");
            Assert.IsTrue(BookShelf.IsLessonUnlocked(_index, _store, "a2"));
            _store.MarkCompleted("a2");
            Assert.IsTrue(BookShelf.IsLessonUnlocked(_index, _store, "b1"), "Mở quyển thì bài đầu mở");
            Assert.IsFalse(BookShelf.IsLessonUnlocked(_index, _store, "b2"));
            Assert.IsFalse(BookShelf.IsLessonUnlocked(_index, _store, "khong_co"));
        }

        [Test]
        public void CurrentBook_FirstUnlockedNotDone()
        {
            Assert.AreEqual("A", BookShelf.CurrentBookId(_index, _store));
            _store.MarkCompleted("a1");
            _store.MarkCompleted("a2");
            Assert.AreEqual("B", BookShelf.CurrentBookId(_index, _store));
        }

        [Test]
        public void CurrentBook_AllDone_IsLast()
        {
            foreach (var id in new[] { "a1", "a2", "b1", "b2", "c1" }) _store.MarkCompleted(id);
            Assert.AreEqual("C", BookShelf.CurrentBookId(_index, _store));
        }

        [Test]
        public void NextLessonInBook_StopsAtBookEnd()
        {
            _store.MarkCompleted("a1");
            Assert.AreEqual("a2", BookShelf.NextLessonInBook(_index, _store, "a1"));
            _store.MarkCompleted("a2");
            Assert.IsNull(BookShelf.NextLessonInBook(_index, _store, "a2"), "Hết quyển thì không nhảy sang quyển sau");
            Assert.AreEqual("B", BookShelf.NextBookId(_index, "A"));
            Assert.IsNull(BookShelf.NextBookId(_index, "C"));
        }

        [Test]
        public void Progress_CountsDoneOfBook()
        {
            _store.MarkCompleted("b1");
            Assert.AreEqual((1, 2), BookShelf.Progress(_index, _store.Current, "B"));
            Assert.AreEqual((0, 2), BookShelf.Progress(_index, _store.Current, "A"));
        }

        [Test]
        public void OpenBook_PerChild_Persists()
        {
            var first = _store.Current.id;
            Assert.IsNull(_store.OpenBook, "Bé mới chưa mở quyển nào");
            _store.OpenBook = "B";
            _store.CreateProfile("Bi", "img_chung_avatar_02");
            _store.OpenBook = "C";
            _store.Save();
            var loaded = ProgressStore.Load(_path);
            Assert.AreEqual("C", loaded.OpenBook);
            loaded.Select(first);
            Assert.AreEqual("B", loaded.OpenBook);
        }
    }
}
