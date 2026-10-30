using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// Cảnh học xong bài (bản thiết kế giao diện mục 8.4): sổ mở ở trang của bài, 3 bông hoa bay vào ô, đóng dấu
    /// "Bé ngoan", gà con khen, rồi mới hiện nút; chạm màn thì nhảy tới cuối.
    /// </summary>
    public class ResultSceneTests : AppTestBase
    {
        private static ResultScreen Result()
        {
            var screen = Object.FindAnyObjectByType<ResultScreen>();
            Assert.IsNotNull(screen, "Không có màn kết thúc bài");
            return screen;
        }

        private static int Count(string sfx) => AppRoot.Instance.Sfx.History.Count(id => id == sfx);

        [UnityTest]
        public IEnumerator NewLesson_ThreeFlowersFly()
        {
            yield return LoadMainWithProfile();
            var id = Ordered()[0];
            AppRoot.Instance.ShowResult(id);
            yield return null;
            var screen = Result();
            Assert.IsTrue(screen.IsSceneDone);
            Assert.AreEqual(3, screen.FlownFlowers);
            Assert.AreEqual(3, screen.Spread.PageFor(id).FlowerCount, "Sổ mở ở trang của bài, đủ 3 hoa");
            Assert.AreEqual(3, Count(SystemSfx.FlowerFly));
            Assert.AreEqual(1, Count(SystemSfx.Stamp));
            Assert.AreEqual(MascotMood.Cheer, screen.Mascot.LastMood);
            Assert.IsTrue(AppRoot.Instance.Progress.IsCompleted(id), "Bài được ghi là đã học xong");
            Assert.IsTrue(screen.ToListButton.gameObject.activeInHierarchy);
            Assert.IsTrue(screen.NextLessonButton.gameObject.activeInHierarchy);
        }

        [UnityTest]
        public IEnumerator Relearn_NoFlowersFly_StampStill()
        {
            yield return LoadMainWithProfile();
            var id = Ordered()[0];
            AppRoot.Instance.Progress.MarkCompleted(id);
            AppRoot.Instance.ShowResult(id);
            yield return null;
            var screen = Result();
            Assert.AreEqual(0, screen.FlownFlowers, "Học lại không thêm hoa");
            Assert.AreEqual(3, screen.Spread.PageFor(id).FlowerCount);
            Assert.AreEqual(0, Count(SystemSfx.FlowerFly));
            Assert.AreEqual(1, Count(SystemSfx.Stamp), "Vẫn đóng dấu và khen");
        }

        [UnityTest]
        public IEnumerator Review_NoBook_NoNextButton()
        {
            yield return LoadMainWithProfile();
            AppRoot.Instance.ShowResult(ReviewSession.LessonId);
            yield return null;
            var screen = Result();
            Assert.IsNull(screen.Spread, "Phiên ôn không có sổ");
            Assert.IsNull(screen.NextLessonButton);
            Assert.IsTrue(screen.ToListButton.gameObject.activeInHierarchy);
            Assert.AreEqual(MascotMood.Cheer, screen.Mascot.LastMood);
            Assert.AreEqual(0, Count(SystemSfx.FlowerFly));
        }

        [UnityTest]
        public IEnumerator TapSkips_ShowsButtons()
        {
            yield return LoadMainWithProfile();
            Motion.Scale = 1f;
            var id = Ordered()[0];
            AppRoot.Instance.ShowResult(id);
            yield return null;
            var screen = Result();
            Assert.IsFalse(screen.IsSceneDone, "Cảnh đang chạy");
            Assert.IsFalse(screen.ToListButton.gameObject.activeInHierarchy, "Nút chỉ hiện khi cảnh xong");
            screen.GetComponentInChildren<SceneSkipper>().OnPointerClick(new PointerEventData(EventSystem.current));
            yield return null;
            Assert.IsTrue(screen.IsSceneDone);
            Assert.IsTrue(screen.ToListButton.gameObject.activeInHierarchy);
            Assert.AreEqual(3, screen.Spread.PageFor(id).FlowerCount, "Bỏ qua thì hoa đã dán đủ");
            yield return new WaitForSecondsRealtime(3.5f);
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator SceneRunsToEndWithMotion()
        {
            yield return LoadMainWithProfile();
            Motion.Scale = 1f;
            AppRoot.Instance.ShowResult(Ordered()[0]);
            yield return null;
            var screen = Result();
            var deadline = Time.realtimeSinceStartup + 6f;
            while (!screen.IsSceneDone && Time.realtimeSinceStartup < deadline) yield return null;
            Assert.IsTrue(screen.IsSceneDone, "Cảnh tự chạy hết trong vài giây");
            Assert.AreEqual(3, screen.FlownFlowers);
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator LeaveMidScene_NoErrors()
        {
            yield return LoadMainWithProfile();
            Motion.Scale = 1f;
            AppRoot.Instance.ShowResult(Ordered()[0]);
            yield return new WaitForSecondsRealtime(.2f);
            Result().ToListButton.onClick.Invoke(); // nút đã có nhưng còn ẩn: gọi thẳng như khi bé thoát giữa chừng
            yield return new WaitForSecondsRealtime(2f);
            Assert.IsNotNull(Object.FindAnyObjectByType<LessonListScreen>());
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator MissingFlowerImage_ReportsErrorAndFinishes()
        {
            var clip = AudioClip.Create("stub", 441, 1, 44100, false);
            AppRoot.CatalogFactory = () => new AssetCatalog(
                _ => clip,
                imageId => imageId == SystemImages.Flower ? null : Resources.Load<Sprite>($"images/{imageId}"));
            try
            {
                LogAssert.Expect(LogType.Error, "[TapDoc] Thiếu tranh: " + SystemImages.Flower);
                yield return LoadMainWithProfile();
                AppRoot.Instance.ShowResult(Ordered()[0]);
                yield return null;
                Assert.IsTrue(Result().IsSceneDone, "Thiếu hình hoa thì cảnh vẫn chạy hết");
            }
            finally
            {
                AppRoot.CatalogFactory = null;
                Object.Destroy(clip);
            }
        }

        [UnityTest]
        public IEnumerator Layout_BothSizes()
        {
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            foreach (var size in new[] { new Vector2Int(2400, 1080), new Vector2Int(2048, 1536) })
            {
                var rt = new RenderTexture(size.x, size.y, 24);
                app.UiCamera.targetTexture = rt;
                app.ShowResult(Ordered()[0]);
                yield return null;
                ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.x}x{size.y}/app_result.png");
                LayoutProbe.AssertFits(app.Canvas);
                app.UiCamera.targetTexture = null;
                Object.Destroy(rt);
            }
        }
    }
}
