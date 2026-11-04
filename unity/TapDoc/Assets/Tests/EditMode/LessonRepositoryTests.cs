using System.IO;
using System.Text;
using NUnit.Framework;
using UnityEngine;

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
        public void Appendix_Missing_ThrowsOldMessage()
        {
            var ex = Assert.Throws<InvalidDataException>(() => _repo.Appendix("x"));
            Assert.AreEqual("Không tìm thấy phụ lục: x", ex.Message);
        }
    }
}
