using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.UI;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// Tem bài học trong Sổ bé ngoan và câu khen theo cách làm ở màn Xong bài (bản thiết kế nâng cấp UI mục 4.3, đợt 3).
    /// </summary>
    public class LessonStickerTests : AppTestBase
    {
        private const string LessonId = "tv1_t1_b13";

        private static IEnumerator WaitSticker(BookPage page)
        {
            for (var i = 0; i < 300 && !page.StickerLoaded; i++) yield return null;
            Assert.IsTrue(page.StickerLoaded, "Tem không nạp xong");
        }

        [UnityTest]
        public IEnumerator Result_StickerAppearsWhenSceneDone()
        {
            yield return LoadMainWithProfile(); // bài chưa học: tem dán lần đầu
            Motion.Scale = 1f; // cảnh chạy thật (tắt hiệu ứng thì cảnh xong ngay khi dựng)
            AppRoot.Instance.ShowResult(LessonId);
            var result = Object.FindAnyObjectByType<ResultScreen>();
            var page = result.Spread.PageFor(LessonId);
            Assert.IsNotNull(page.Sticker, "Bài vừa học có tem");
            Assert.IsFalse(page.StickerVisible, "Tem dán vào lúc cảnh xong");
            result.SkipScene();
            yield return null;
            Assert.IsTrue(page.StickerVisible);
            yield return WaitSticker(page);
            var (image, _) = LessonSticker.For(TestLessons.Real.Get(LessonId));
            Assert.AreEqual(image, page.StickerImageId, "Tem là tranh từ khoá của bài");
            Assert.IsTrue(page.Sticker.Find("Picture").GetComponent<Image>().enabled);
            Canvas.ForceUpdateCanvases();
            LayoutProbe.AssertFits(AppRoot.Instance.Canvas);
        }

        [UnityTest]
        public IEnumerator Book_CompletedHasSticker_NextHasEmptySlot()
        {
            yield return LoadMainWithProfile();
            var ordered = Ordered();
            AppRoot.Instance.Progress.MarkCompleted(ordered[0]);
            AppRoot.Instance.ShowBook();
            yield return null;
            var book = Object.FindAnyObjectByType<BookScreen>();
            var done = book.Spread.PageFor(ordered[0]);
            Assert.IsNotNull(done);
            Assert.IsNotNull(done.Sticker);
            Assert.IsTrue(done.StickerVisible);
            yield return WaitSticker(done);
            var next = book.Spread.PageFor(ordered[1]);
            Assert.IsNotNull(next, "Trang bên là bài sau");
            Assert.IsNull(next.Sticker, "Bài chưa học không có tem");
            Assert.IsNotNull(next.StickerSlot, "Bài chưa học có khung tem trống");
        }

        [UnityTest]
        public IEnumerator Praise_AllRight_WhenNoMistakes()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            AppRoot.Instance.Speech.WaitScale = .02f;
            AppRoot.Instance.ShowLesson(LessonId);
            yield return WaitPrepared();
            yield return WalkAll(Object.FindAnyObjectByType<LessonScreen>());
            var result = Object.FindAnyObjectByType<ResultScreen>();
            Assert.IsNotNull(result);
            result.SkipScene();
            yield return null;
            Assert.AreEqual(UiText.PraiseAllRight, result.PraiseText, "Không nhầm lượt nào: khen nghe kĩ");
            Assert.AreEqual(UiText.PraiseAllRight, result.Mascot.BubbleText);
            Assert.That(new[] { SystemAudio.khen_nghe_ki, SystemAudio.khen_hoan_thanh }, Has.Member(result.PraiseAudio),
                "Có tiếng câu khen thì phát, chưa có thì phát câu chung");
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator Praise_SelfFix_WhenOneMistakeThenRight()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            AppRoot.Instance.Speech.WaitScale = .02f;
            AppRoot.Instance.ShowLesson(LessonId);
            yield return WaitPrepared();
            yield return WalkWithOneMistake(Object.FindAnyObjectByType<LessonScreen>());
            var result = Object.FindAnyObjectByType<ResultScreen>();
            result.SkipScene();
            yield return null;
            Assert.AreEqual(UiText.PraiseSelfFix, result.PraiseText, "Nhầm một lần rồi tự làm đúng: khen tự sửa");
            Canvas.ForceUpdateCanvases();
            LayoutProbe.AssertFits(AppRoot.Instance.Canvas);
        }

        [UnityTest]
        public IEnumerator Review_GenericPraise()
        {
            yield return LoadMainWithProfile();
            AppRoot.Instance.ShowResult(ReviewSession.LessonId);
            yield return null;
            var result = Object.FindAnyObjectByType<ResultScreen>();
            result.SkipScene();
            yield return null;
            Assert.AreEqual(UiText.MascotLessonDone, result.PraiseText, "Phiên ôn: câu khen chung");
            Assert.AreEqual(SystemAudio.khen_hoan_thanh, result.PraiseAudio);
        }

        [UnityTest]
        public IEnumerator Screens_ResultAndBook_FourSizes()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            app.Progress.MarkCompleted(Ordered()[0]);
            foreach (var size in new[] { ScreenSizes.Phone20x9, ScreenSizes.IPad43, ScreenSizes.Tablet16x10, ScreenSizes.TabletPortrait })
            {
                var rt = ScreenSizes.Apply(app, size);
                app.ShowResult(LessonId);
                yield return null;
                var result = Object.FindAnyObjectByType<ResultScreen>();
                result.SkipScene();
                yield return WaitSticker(result.Spread.PageFor(LessonId));
                Canvas.ForceUpdateCanvases();
                ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.Name}/app_dot3_xong_bai.png");
                LayoutProbe.AssertFits(app.Canvas);
                app.ShowBook();
                yield return null;
                var book = Object.FindAnyObjectByType<BookScreen>();
                var page = book.Spread.PageFor(Ordered()[0]);
                if (page != null) yield return WaitSticker(page);
                Canvas.ForceUpdateCanvases();
                ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.Name}/app_dot3_so_be_ngoan.png");
                LayoutProbe.AssertFits(app.Canvas);
                ScreenSizes.Reset(app, rt);
            }
        }
    }
}
