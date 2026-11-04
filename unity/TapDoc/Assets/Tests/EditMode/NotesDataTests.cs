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
            var b20 = TestLessons.Real.Get("tv1_t1_b20");
            Assert.That(b20.notes.Where(n => n.kind == "ten_doc").Select(n => n.text),
                Has.Some.Contains("\"k\" khi học đọc là \"ca\""));
            var b68 = TestLessons.Real.Get("tv1_t1_b68");
            Assert.That(b68.notes.Where(n => n.kind == "sach").Select(n => n.text), Has.Some.Contains("Vần ec rất ít gặp"));
            Assert.That(b68.notes.Select(n => n.kind), Has.Member("khac_sach"));
        }

        [Test]
        public void UiText_ReadingWording()
        {
            Assert.AreEqual("Đọc khi học", UiText.ReadingLearn);
            Assert.AreEqual("Âm chuẩn", UiText.ReadingStandard);
            Assert.AreEqual("Tên chữ cái", UiText.ReadingLetterName);
            Assert.AreEqual("Vì sao?", UiText.Why);
        }

        [Test]
        public void Unit_ReadingsParsed()
        {
            var g = TestLessons.Real.Get("tv1_t1_b25").part1[0];
            Assert.AreEqual(new[] { "am_g", "ghiam_g", "tenchu_g" }, g.readings.Select(r => r.audio).ToArray());
            Assert.AreEqual(new[] { "hoc" }, g.readings[0].kinds.ToArray());
            Assert.AreEqual("để phân biệt g và gh", g.readings[0].hint);
            Assert.AreEqual("giê", g.readings[2].text);
            var o = TestLessons.Real.Get("tv1_t1_b01").part1[0];
            Assert.IsNotNull(o.readings);
            Assert.AreEqual(0, o.readings.Count);
        }

        [Test]
        public void LetterAudio_FindsEveryReadingOfTheBookTables()
        {
            // Mỗi ô "Tên chữ cái"/"Ghi âm" của Phụ lục có file âm thanh lấy từ bước giới thiệu chữ của các bài.
            var audio = LetterAudio.FromLessons(TestLessons.Real.Index.lessons.Select(e => TestLessons.Real.Get(e.lesson_id)));
            Assert.AreEqual("tenchu_g", audio.Of("g", LetterAudio.LetterName));
            Assert.AreEqual("ghiam_g", audio.Of("g", LetterAudio.Sound));
            Assert.AreEqual("am_k", audio.Of("k", LetterAudio.LetterName));
            Assert.AreEqual("am_b", audio.Of("b", LetterAudio.Sound));
            Assert.AreEqual("am_ch", audio.Of("ch", LetterAudio.Sound));
            Assert.IsNull(audio.Of("iê", LetterAudio.Sound));
            var a = TestLessons.Real.Appendix("tv1_t1_1990");
            foreach (var row in a.alphabet.rows)
            {
                Assert.IsNotNull(audio.Of(row.lower, LetterAudio.LetterName), row.lower);
                Assert.IsNotNull(audio.Of(row.lower, LetterAudio.Sound), row.lower);
            }
        }

        [Test]
        public void Lesson_WithoutNotes_HasEmptyList()
        {
            var b13 = TestLessons.Real.Get("tv1_t1_b13");
            Assert.IsNotNull(b13.notes);
            Assert.AreEqual(0, b13.notes.Count);
        }

        [Test]
        public void Index_EntriesNameTheirBook()
        {
            // Màn Phụ huynh mở Phụ lục theo mã sách của các bài trong danh sách, không ghi cứng.
            var books = TestLessons.Real.Index.lessons.Select(e => e.book).Distinct().ToList();
            Assert.AreEqual(new[] { "tv1_t1_1990" }, books);
            Assert.AreEqual(books[0], TestLessons.Real.Appendix(books[0]).book);
        }

        [Test]
        public void Appendix_LoadsBookTables()
        {
            var a = TestLessons.Real.Appendix("tv1_t1_1990");
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
