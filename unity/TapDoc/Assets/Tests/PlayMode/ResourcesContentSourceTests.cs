using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    /// <summary>Bản nguồn dữ liệu đọc từ Resources: nạp đúng kiểu, thiếu file thì trả <c>null</c> mà không ghi log.</summary>
    public class ResourcesContentSourceTests
    {
        [UnityTest]
        public IEnumerator LoadAsync_RealFiles_EachKind()
        {
            var source = new ResourcesContentSource();
            yield return Expect<Sprite>(source, ContentKind.Image, SystemImages.Mascot);
            yield return Expect<AudioClip>(source, ContentKind.Speech, "am_b");
            yield return Expect<AudioClip>(source, ContentKind.Sfx, SystemSfx.Tap);
            yield return Expect<TextAsset>(source, ContentKind.Lesson, "tv1_t1_b01");
            yield return Expect<TextAsset>(source, ContentKind.LessonIndex, null);
            yield return Expect<TextAsset>(source, ContentKind.Appendix, "tv1_t1_1990");
            yield return Expect<Font>(source, ContentKind.Font, "Andika-Regular");
        }

        [UnityTest]
        public IEnumerator LoadAsync_Missing_ReturnsNullWithoutLog()
        {
            Object result = new TextAsset("chưa nạp");
            yield return AwaitableTestUtil.Wait(new ResourcesContentSource().LoadAsync(ContentKind.Image, "khong_co"),
                r => result = r);
            Assert.IsNull(result);
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator Load_Sync_SameAsAsync()
        {
            var source = new ResourcesContentSource();
            Object async = null;
            yield return AwaitableTestUtil.Wait(source.LoadAsync(ContentKind.Speech, "am_b"), r => async = r);
            Assert.IsNotNull(async);
            Assert.AreSame(async, source.Load(ContentKind.Speech, "am_b"));
            Assert.IsNull(source.Load(ContentKind.Speech, "khong_co"));
        }

        private static IEnumerator Expect<T>(IContentSource source, ContentKind kind, string id) where T : Object
        {
            Object result = null;
            yield return AwaitableTestUtil.Wait(source.LoadAsync(kind, id), r => result = r);
            Assert.IsInstanceOf<T>(result, $"{kind} {id}");
        }
    }
}
