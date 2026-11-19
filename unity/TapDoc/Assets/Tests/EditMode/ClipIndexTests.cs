using NUnit.Framework;

namespace TapDoc.Tests
{
    /// <summary>
    /// Danh sách clip "tiếp" (hết clip giữ khung cuối) trong Resources/clips/index.json, do lệnh clips ghi từ trường
    /// "ket": "giu" của video_manifest.json (thiết kế tranh động mục 4, 12).
    /// </summary>
    public class ClipIndexTests
    {
        [Test]
        public void Parse_ReadsHoldList()
        {
            var hold = ClipIndex.Parse("{\"giu\": [\"img_a\", \"img_b\"]}");
            CollectionAssert.AreEquivalent(new[] { "img_a", "img_b" }, hold);
        }

        [Test]
        public void Parse_EmptyList()
        {
            CollectionAssert.IsEmpty(ClipIndex.Parse("{\"giu\": []}"));
        }

        [Test]
        public void Parse_MissingOrBroken_IsEmpty_NoThrow()
        {
            // Máy chưa chạy lệnh clips bản mới (không có index.json) hay file hỏng: mọi clip như cũ, mờ về tranh.
            CollectionAssert.IsEmpty(ClipIndex.Parse(null));
            CollectionAssert.IsEmpty(ClipIndex.Parse(string.Empty));
            CollectionAssert.IsEmpty(ClipIndex.Parse("không phải json"));
            CollectionAssert.IsEmpty(ClipIndex.Parse("{\"khac\": [\"img_a\"]}"));
        }

        [Test]
        public void Parse_SkipsEmptyIds()
        {
            CollectionAssert.AreEquivalent(new[] { "img_a" }, ClipIndex.Parse("{\"giu\": [\"img_a\", \"\"]}"));
        }
    }
}
