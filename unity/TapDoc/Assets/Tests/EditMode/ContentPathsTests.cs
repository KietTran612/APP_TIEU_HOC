using NUnit.Framework;
using UnityEngine;

namespace TapDoc.Tests
{
    /// <summary><see cref="ContentPaths"/> là chỗ duy nhất biết thư mục và kiểu Unity của từng loại dữ liệu.</summary>
    public class ContentPathsTests
    {
        [Test]
        public void PathOf_EachKind()
        {
            Assert.AreEqual("lessons/index", ContentPaths.PathOf(ContentKind.LessonIndex, null));
            Assert.AreEqual("lessons/tv1_t1_b01", ContentPaths.PathOf(ContentKind.Lesson, "tv1_t1_b01"));
            Assert.AreEqual("appendix/tv1_t1_1990", ContentPaths.PathOf(ContentKind.Appendix, "tv1_t1_1990"));
            Assert.AreEqual("images/img_b01_bof", ContentPaths.PathOf(ContentKind.Image, "img_b01_bof"));
            Assert.AreEqual("audio/van_o", ContentPaths.PathOf(ContentKind.Speech, "van_o"));
            Assert.AreEqual("sfx/sfx_cham", ContentPaths.PathOf(ContentKind.Sfx, "sfx_cham"));
            Assert.AreEqual("fonts/Andika-Regular", ContentPaths.PathOf(ContentKind.Font, "Andika-Regular"));
            Assert.AreEqual("clips/clip_b01_bof", ContentPaths.PathOf(ContentKind.Clip, "clip_b01_bof"));
        }

        [Test]
        public void TypeOf_EachKind()
        {
            Assert.AreEqual(typeof(TextAsset), ContentPaths.TypeOf(ContentKind.LessonIndex));
            Assert.AreEqual(typeof(TextAsset), ContentPaths.TypeOf(ContentKind.Lesson));
            Assert.AreEqual(typeof(TextAsset), ContentPaths.TypeOf(ContentKind.Appendix));
            Assert.AreEqual(typeof(Sprite), ContentPaths.TypeOf(ContentKind.Image));
            Assert.AreEqual(typeof(AudioClip), ContentPaths.TypeOf(ContentKind.Speech));
            Assert.AreEqual(typeof(AudioClip), ContentPaths.TypeOf(ContentKind.Sfx));
            Assert.AreEqual(typeof(Font), ContentPaths.TypeOf(ContentKind.Font));
            // Tranh động chỉ chừa chỗ: chưa có module video, kiểu cụ thể gắn khi đưa clip vào app.
            Assert.AreEqual(typeof(Object), ContentPaths.TypeOf(ContentKind.Clip));
        }
    }
}
