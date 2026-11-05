using System.Collections;
using System.Text.RegularExpressions;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    /// <summary>Màn mở đầu (bản thiết kế màn mở đầu, cảnh báo, cài đặt mục 4, 5.1): hiện trong lúc app nạp dữ liệu.</summary>
    public class SplashScreenTests : AppTestBase
    {
        private Texture2D _tex;

        [TearDown]
        public void TearDownSource()
        {
            AppRoot.SourceFactory = null;
            LogAssert.ignoreFailingMessages = false;
            if (_tex != null) Object.Destroy(_tex);
        }

        /// <summary>Nguồn nạp chậm vài khung hình; tranh, âm thanh chưa có thì thay bằng đồ giả; danh sách bài có thể hỏng.</summary>
        private void UseSlowSource(int delayFrames, bool brokenIndex = false)
        {
            _tex = new Texture2D(4, 4);
            var sprite = Sprite.Create(_tex, new Rect(0, 0, 4, 4), new Vector2(.5f, .5f));
            var clip = AudioClip.Create("stub", 441, 1, 44100, false);
            var real = new ResourcesContentSource();
            AppRoot.SourceFactory = () => new FakeContentSource
            {
                DelayFrames = delayFrames,
                Fallback = (kind, id) =>
                {
                    if (brokenIndex && kind == ContentKind.LessonIndex) return null;
                    return real.Load(kind, id) ?? kind switch
                    {
                        ContentKind.Image => sprite,
                        ContentKind.Speech or ContentKind.Sfx => clip,
                        _ => null,
                    };
                },
            };
        }

        [UnityTest]
        public IEnumerator Splash_ShownDuringBoot_HiddenAfterReady()
        {
            UseSlowSource(5);
            SceneManager.LoadScene("Main");
            yield return null;
            var app = AppRoot.Instance;
            Assert.IsNotNull(app.Splash, "Màn mở đầu có ngay khi app bắt đầu nạp");
            Assert.IsTrue(app.Splash.IsShowing);
            Assert.IsFalse(app.IsReady);
            Assert.AreEqual(app.Canvas.transform.childCount - 1, app.Splash.transform.GetSiblingIndex(), "Nằm trên cùng");

            for (var i = 0; i < 600 && !app.IsReady; i++) yield return null;
            Assert.IsTrue(app.IsReady);
            for (var i = 0; i < 5; i++) yield return null;
            Assert.IsFalse(app.Splash.IsShowing, "Nạp xong thì màn mở đầu tắt");
            Assert.IsNotNull(Object.FindAnyObjectByType<ProfileScreen>());
        }

        [UnityTest]
        public IEnumerator Splash_BootError_ShowsMessage()
        {
            UseSlowSource(0, brokenIndex: true);
            LogAssert.ignoreFailingMessages = true; // lỗi nạp là điều đang thử
            SceneManager.LoadScene("Main");
            for (var i = 0; i < 30; i++) yield return null;
            var app = AppRoot.Instance;
            Assert.IsFalse(app.IsReady);
            Assert.IsTrue(app.Splash.IsShowing, "Nạp lỗi: màn mở đầu ở lại");
            Assert.IsTrue(app.Splash.ErrorLabel.gameObject.activeInHierarchy);
            Assert.AreEqual(UiText.BootError, app.Splash.ErrorLabel.text);
        }

        [UnityTest]
        public IEnumerator Splash_FitsAllSizes()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            foreach (var size in ScreenSizes.All)
            {
                var rt = ScreenSizes.Apply(app, size);
                var splash = SplashScreen.Create(app.Canvas.transform, app.Assets);
                yield return null;
                Canvas.ForceUpdateCanvases();
                ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.Name}/app_splash.png");
                LayoutProbe.AssertFits(app.Canvas);
                Object.Destroy(splash.gameObject);
                ScreenSizes.Reset(app, rt);
            }
        }
    }
}
