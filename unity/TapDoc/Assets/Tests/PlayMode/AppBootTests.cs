using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    /// <summary>Khởi động: chờ nạp xong bộ chung, danh sách bài và Phụ lục rồi mới hiện màn chọn bé.</summary>
    public class AppBootTests : AppTestBase
    {
        [UnityTest]
        public IEnumerator Boot_ShowsProfiles_OnlyAfterCommonReady()
        {
            var sprite = FakeContentSource.NewSprite();
            var clip = FakeContentSource.NewClip();
            var real = new ResourcesContentSource();
            AppRoot.SourceFactory = () => new FakeContentSource
            {
                DelayFrames = 5,
                Fallback = (kind, id) => kind switch
                {
                    ContentKind.Image => sprite,
                    ContentKind.Speech or ContentKind.Sfx => clip,
                    _ => real.Load(kind, id),
                },
            };
            try
            {
                SceneManager.LoadScene("Main");
                yield return null;
                Assert.IsNotNull(AppRoot.Instance, "AppRoot chưa khởi động");
                Assert.IsFalse(AppRoot.Instance.IsReady, "Bộ chung chưa nạp xong mà đã báo sẵn sàng");
                Assert.IsNull(Object.FindAnyObjectByType<ProfileScreen>(), "Màn chọn bé hiện trước khi nạp xong");

                for (var i = 0; i < 120 && !AppRoot.Instance.IsReady; i++) yield return null;
                Assert.IsTrue(AppRoot.Instance.IsReady, "Khởi động không xong");
                yield return null;
                Assert.IsNotNull(Object.FindAnyObjectByType<ProfileScreen>(), "Nạp xong mà không hiện màn chọn bé");
                Assert.IsNotNull(AppRoot.Instance.Assets.Font(FontProvider.MainFontId));
            }
            finally
            {
                AppRoot.SourceFactory = null;
            }
        }

        [UnityTest]
        public IEnumerator Boot_NoUnpreparedAsks_OnProfileAndList()
        {
            yield return LoadMainWithProfile();
            CollectionAssert.IsEmpty(AppRoot.Instance.Assets.UnpreparedAsks,
                "Màn chọn bé và danh sách bài hỏi tranh, âm thanh chưa có trong bộ chung");
        }
    }
}
