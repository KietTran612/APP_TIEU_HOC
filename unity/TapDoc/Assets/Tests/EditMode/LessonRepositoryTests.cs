using System.IO;
using System.Text;
using System.Text.RegularExpressions;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    /// <summary>Kho bài đọc qua nguồn dữ liệu, giữ trong bộ nhớ đệm; chuẩn hoá NFC và thông điệp lỗi như cũ.</summary>
    public class LessonRepositoryTests
    {
        private const string LessonJson = "{\"lesson_id\":\"b\",\"title\":\"TITLE\",\"part1\":[],\"part2\":[]}";

        private FakeContentSource _source;
        private LessonRepository _repo;

        [SetUp]
        public void SetUp()
        {
            _source = new FakeContentSource();
            _repo = new LessonRepository(_source);
        }

        private void PutText(ContentKind kind, string id, string text) => _source.Put(kind, id, new TextAsset(text));

        [Test]
        public void Get_ReadsSourceOnce()
        {
            PutText(ContentKind.Lesson, "b", LessonJson.Replace("TITLE", "o"));
            Assert.AreEqual("b", _repo.Get("b").lesson_id);
            Assert.AreSame(_repo.Get("b"), _repo.Get("b"));
            Assert.AreEqual(1, _source.LoadCount(ContentKind.Lesson, "b"));
        }

        [Test]
        public void Get_NormalizesNfc()
        {
            var nfd = "cá".Normalize(NormalizationForm.FormD);
            PutText(ContentKind.Lesson, "b", LessonJson.Replace("TITLE", nfd));
            Assert.AreEqual("cá".Normalize(NormalizationForm.FormC), _repo.Get("b").title);
        }

        [Test]
        public void Get_Missing_ThrowsOldMessage()
        {
            var ex = Assert.Throws<InvalidDataException>(() => _repo.Get("x"));
            Assert.AreEqual("Không tìm thấy bài học: x", ex.Message);
        }

        [Test]
        public void Get_Broken_PrefixesLessonId()
        {
            PutText(ContentKind.Lesson, "x", "{ hỏng");
            var ex = Assert.Throws<InvalidDataException>(() => _repo.Get("x"));
            StringAssert.StartsWith("Bài x: ", ex.Message);
        }

        [Test]
        public void Index_Missing_ThrowsOldMessage()
        {
            var ex = Assert.Throws<InvalidDataException>(() => _ = _repo.Index);
            Assert.AreEqual("Không tìm thấy hoặc hỏng lessons/index.json", ex.Message);
        }

        [Test]
        public void Index_ReadsOnce()
        {
            PutText(ContentKind.LessonIndex, null, "{\"lessons\":[{\"lesson_id\":\"b\",\"lesson_no\":1}]}");
            Assert.AreEqual("b", _repo.Index.lessons[0].lesson_id);
            Assert.AreSame(_repo.Index, _repo.Index);
            Assert.AreEqual(1, _source.LoadCount(ContentKind.LessonIndex, null));
        }

        [Test]
        public void Appendix_ReadsOnce_AndNormalizes()
        {
            var nfd = "Phụ lục".Normalize(NormalizationForm.FormD);
            PutText(ContentKind.Appendix, "sach", "{\"book\":\"sach\",\"title\":\"" + nfd + "\"}");
            var appendix = _repo.Appendix("sach");
            Assert.AreEqual("Phụ lục".Normalize(NormalizationForm.FormC), appendix.title);
            Assert.AreSame(appendix, _repo.Appendix("sach"));
            Assert.AreEqual(1, _source.LoadCount(ContentKind.Appendix, "sach"));
        }

        [Test]
        public void LoadAll_SkipsBrokenLesson()
        {
            PutText(ContentKind.LessonIndex, null,
                "{\"lessons\":[{\"lesson_id\":\"a\",\"lesson_no\":1},{\"lesson_id\":\"b\",\"lesson_no\":2}]}");
            PutText(ContentKind.Lesson, "a", "{ hỏng");
            PutText(ContentKind.Lesson, "b", LessonJson.Replace("TITLE", "o"));
            LogAssert.Expect(LogType.Error, new Regex("^\\[TapDoc\\] Bài a: "));

            var all = _repo.LoadAllAsync().GetAwaiter();
            Assert.IsTrue(all.IsCompleted, "Nguồn giả không chậm thì phải xong ngay");
            all.GetResult();
            Assert.AreEqual(1, _source.LoadCount(ContentKind.Lesson, "b"));
            Assert.AreEqual("b", _repo.Get("b").lesson_id);
        }

        private const string TwoBooksIndex =
            "{\"books\":[{\"book_id\":\"t1\",\"title\":\"Tập một\",\"appendix\":\"t1\"}," +
            "{\"book_id\":\"t2\",\"title\":\"Tập hai\",\"appendix\":\"t1\"}]," +
            "\"lessons\":[{\"lesson_id\":\"a\",\"lesson_no\":42,\"title\":\"an\",\"type\":\"van_moi\",\"book\":\"t1\"," +
            "\"part\":\"van\",\"label\":\"Bài 42\",\"week\":0}," +
            "{\"lesson_id\":\"b\",\"lesson_no\":126,\"title\":\"Trường em\",\"type\":\"tap_doc\",\"book\":\"t2\"," +
            "\"part\":\"tap_doc\",\"label\":\"Bài 1\",\"week\":27}]}";

        [Test]
        public void Index_ParsesBooksPartsLabels()
        {
            PutText(ContentKind.LessonIndex, null, TwoBooksIndex);
            var index = _repo.Index;
            Assert.AreEqual(2, index.books.Count);
            Assert.AreEqual("t1", index.books[1].appendix);
            Assert.AreEqual("tap_doc", index.lessons[1].part);
            Assert.AreEqual("Bài 1", index.lessons[1].label);
            Assert.AreEqual(27, index.lessons[1].week);
        }

        [Test]
        public void Appendix_BookWithoutOwn_UsesListedAppendix()
        {
            PutText(ContentKind.LessonIndex, null, TwoBooksIndex);
            PutText(ContentKind.Appendix, "t1", "{\"book\":\"t1\",\"title\":\"Phụ lục\"}");
            AwaitableTestUtil.RunNow(_repo.LoadIndexAsync());
            AwaitableTestUtil.RunNow(_repo.LoadAppendixAsync("t2"));
            Assert.AreSame(_repo.Appendix("t1"), _repo.Appendix("t2"));
            Assert.AreEqual(1, _source.LoadCount(ContentKind.Appendix, "t1"));
            Assert.AreEqual(0, _source.LoadCount(ContentKind.Appendix, "t2"));
        }

        [Test]
        public void Appendix_OldIndexWithoutBooks_UsesOwnBook()
        {
            PutText(ContentKind.LessonIndex, null, "{\"lessons\":[]}");
            PutText(ContentKind.Appendix, "sach", "{\"book\":\"sach\",\"title\":\"x\"}");
            AwaitableTestUtil.RunNow(_repo.LoadIndexAsync());
            Assert.AreEqual("sach", _repo.Appendix("sach").book);
        }

        [Test]
        public void Appendix_Missing_ThrowsOldMessage()
        {
            var ex = Assert.Throws<InvalidDataException>(() => _repo.Appendix("x"));
            Assert.AreEqual("Không tìm thấy phụ lục: x", ex.Message);
        }
    }
}
