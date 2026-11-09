using System.Collections.Generic;
using System.Linq;

namespace TapDoc
{
    /// <summary>
    /// Luật của Tủ sách (bản thiết kế Tủ sách mục 7): quyển theo thứ tự trong <see cref="LessonIndex.books"/>; quyển đầu
    /// luôn mở, quyển sau mở khi mọi bài của quyển trước đã học xong, "Mở mọi bài" mở hết. Trong một quyển, bài mở theo
    /// <see cref="ProgressStore.IsUnlocked"/> với chuỗi là các bài của quyển đó.
    /// </summary>
    public static class BookShelf
    {
        /// <summary>Mã các quyển theo thứ tự học; index cũ không có <c>books</c> thì theo thứ tự bài.</summary>
        public static IReadOnlyList<string> BookIds(LessonIndex index)
        {
            if (index == null) return new List<string>();
            if (index.books != null && index.books.Count > 0) return index.books.Select(b => b.book_id).ToList();
            return index.lessons.Select(e => e.book).Where(b => !string.IsNullOrEmpty(b)).Distinct().ToList();
        }

        /// <summary>Mã các bài của quyển <paramref name="bookId"/>, theo thứ tự học.</summary>
        public static IReadOnlyList<string> LessonIds(LessonIndex index, string bookId) =>
            index == null ? new List<string>() : index.lessons.Where(e => e.book == bookId).Select(e => e.lesson_id).ToList();

        /// <summary>Quyển của bài <paramref name="lessonId"/>; không có trong danh sách thì <c>null</c>.</summary>
        public static string BookOf(LessonIndex index, string lessonId) =>
            index?.lessons.FirstOrDefault(e => e.lesson_id == lessonId)?.book;

        /// <summary>Thông tin quyển trong <c>books</c>; không có thì <c>null</c>.</summary>
        public static BookEntry Book(LessonIndex index, string bookId) =>
            index?.books?.FirstOrDefault(b => b.book_id == bookId);

        public static bool IsBookUnlocked(LessonIndex index, ProgressStore store, string bookId)
        {
            var books = BookIds(index);
            var k = IndexOf(books, bookId);
            if (k < 0) return false;
            if (k == 0 || (store != null && store.UnlockAll)) return true;
            return IsBookDone(index, store, books[k - 1]);
        }

        /// <summary>Mọi bài của quyển đã học xong (quyển không có bài thì coi như chưa xong).</summary>
        public static bool IsBookDone(LessonIndex index, ProgressStore store, string bookId)
        {
            if (store?.Current == null) return false;
            var ids = LessonIds(index, bookId);
            return ids.Count > 0 && ids.All(store.IsCompleted);
        }

        /// <summary>Quyển đầu tiên đã mở mà chưa học xong; học xong hết thì quyển cuối.</summary>
        public static string CurrentBookId(LessonIndex index, ProgressStore store)
        {
            var books = BookIds(index);
            foreach (var id in books)
            {
                if (IsBookUnlocked(index, store, id) && !IsBookDone(index, store, id)) return id;
            }
            return books.Count > 0 ? books[books.Count - 1] : null;
        }

        public static bool IsLessonUnlocked(LessonIndex index, ProgressStore store, string lessonId)
        {
            var book = BookOf(index, lessonId);
            if (book == null || store == null || !IsBookUnlocked(index, store, book)) return false;
            return store.IsUnlocked(LessonIds(index, book), lessonId);
        }

        /// <summary>Bài sau <paramref name="lessonId"/> trong cùng quyển nếu đã mở; hết quyển thì <c>null</c>.</summary>
        public static string NextLessonInBook(LessonIndex index, ProgressStore store, string lessonId)
        {
            var ids = LessonIds(index, BookOf(index, lessonId));
            var k = IndexOf(ids, lessonId);
            if (k < 0 || k + 1 >= ids.Count) return null;
            var next = ids[k + 1];
            return IsLessonUnlocked(index, store, next) ? next : null;
        }

        /// <summary>Quyển đứng sau <paramref name="bookId"/>; quyển cuối thì <c>null</c>.</summary>
        public static string NextBookId(LessonIndex index, string bookId)
        {
            var books = BookIds(index);
            var k = IndexOf(books, bookId);
            return k >= 0 && k + 1 < books.Count ? books[k + 1] : null;
        }

        /// <summary>Số bài đã học xong và tổng số bài của quyển, cho bé <paramref name="profile"/>.</summary>
        public static (int done, int total) Progress(LessonIndex index, Profile profile, string bookId)
        {
            var ids = LessonIds(index, bookId);
            return (ids.Count(id => ProgressStore.IsCompleted(profile, id)), ids.Count);
        }

        private static int IndexOf(IReadOnlyList<string> list, string value)
        {
            for (var i = 0; i < list.Count; i++)
            {
                if (list[i] == value) return i;
            }
            return -1;
        }
    }
}
