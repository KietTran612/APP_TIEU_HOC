using System.Linq;
using NUnit.Framework;

namespace TapDoc.Tests
{
    /// <summary>Ghi chú cho phụ huynh trong bài và dữ liệu Phụ lục (tr.120–122).</summary>
    public class NotesDataTests
    {
        [Test]
        public void UiText_NoteWording()
        {
            Assert.AreEqual("Ghi chú", UiText.Notes);
            Assert.AreEqual("Sách ghi", UiText.NoteKindBook);
            Assert.AreEqual("Cách đọc theo sách", UiText.NoteKindReading);
            Assert.AreEqual("App khác sách", UiText.NoteKindApp);
            Assert.AreEqual("Đóng", UiText.Close);
            Assert.AreEqual("Chú ý và Phụ lục", UiText.BookAppendix);
        }

        [Test]
        public void Lesson_NotesParsed()
        {
            var b20 = LessonRepository.Load("tv1_t1_b20");
            Assert.That(b20.notes.Where(n => n.kind == "ten_doc").Select(n => n.text),
                Has.Some.Contains("\"k\" đọc là \"ca\""));
            var b68 = LessonRepository.Load("tv1_t1_b68");
            Assert.That(b68.notes.Where(n => n.kind == "sach").Select(n => n.text), Has.Some.Contains("Vần ec rất ít gặp"));
            Assert.That(b68.notes.Select(n => n.kind), Has.Member("khac_sach"));
        }

        [Test]
        public void Lesson_WithoutNotes_HasEmptyList()
        {
            var b13 = LessonRepository.Load("tv1_t1_b13");
            Assert.IsNotNull(b13.notes);
            Assert.AreEqual(0, b13.notes.Count);
        }

        [Test]
        public void Index_EntriesNameTheirBook()
        {
            // Màn Phụ huynh mở Phụ lục theo mã sách của các bài trong danh sách, không ghi cứng.
            var books = LessonRepository.LoadIndex().lessons.Select(e => e.book).Distinct().ToList();
            Assert.AreEqual(new[] { "tv1_t1_1990" }, books);
            Assert.AreEqual(books[0], AppendixData.Load(books[0]).book);
        }

        [Test]
        public void Appendix_LoadsBookTables()
        {
            var a = AppendixData.Load("tv1_t1_1990");
            Assert.AreEqual(29, a.alphabet.rows.Count);
            var s = a.alphabet.rows[22];
            Assert.AreEqual(("s", "S", "ét-sì", "sờ"), (s.lower, s.upper, s.name, s.sound));
            Assert.AreEqual(14, a.digraphs.rows.Count);
            Assert.AreEqual(("gi", "giờ"), (a.digraphs.rows[13].letters, a.digraphs.rows[13].reading));
            Assert.AreEqual(122, a.chu_y.page);
            Assert.That(a.chu_y.paragraphs[0], Does.Contain("phụ huynh học sinh"));
            Assert.That(a.app_notes, Has.Some.Contains("Phần luyện tập"));
        }
    }
}
