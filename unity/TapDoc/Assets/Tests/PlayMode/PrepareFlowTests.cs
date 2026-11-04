using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// Mở bài và ôn lại: màn chuyển hiện trong lúc nạp, màn bài chỉ hiện khi nạp xong; bộ của bài được giữ qua màn kết
    /// quả và nhả khi về danh sách hoặc khi bài mới đã nạp xong.
    /// </summary>
    public class PrepareFlowTests : AppTestBase
    {
        private FakeContentSource _source;

        [SetUp]
        public void SetUpSource()
        {
            var sprite = FakeContentSource.NewSprite();
            var clip = FakeContentSource.NewClip();
            var real = new ResourcesContentSource();
            _source = new FakeContentSource
            {
                DelayFrames = 3,
                Fallback = (kind, id) => kind switch
                {
                    ContentKind.Image => sprite,
                    ContentKind.Speech or ContentKind.Sfx => clip,
                    _ => real.Load(kind, id),
                },
            };
            var source = _source;
            AppRoot.SourceFactory = () => source;
        }

        [TearDown]
        public void TearDownSource() => AppRoot.SourceFactory = null;

        private static readonly HashSet<string> CommonIds =
            new(SystemAudio.All.Concat(SystemImages.All).Concat(SystemSfx.All).Concat(ProfileScreen.Avatars));

        /// <summary>Mã tranh, âm thanh riêng của bài (không thuộc bộ chung).</summary>
        private static List<(ContentKind kind, string id)> OwnIds(string lessonId) =>
            LessonAssets.ContentIds(TestLessons.Real.Get(lessonId)).Where(k => !CommonIds.Contains(k.id)).ToList();

        [UnityTest]
        public IEnumerator ShowLesson_ScreenAppearsOnlyAfterPrepared()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            app.ShowLesson("tv1_t1_b01");
            Assert.IsTrue(app.IsPreparing);
            yield return null;
            Assert.IsTrue(app.Curtain.IsShowing, "Không có màn chuyển trong lúc nạp");
            Assert.IsNull(Object.FindAnyObjectByType<LessonScreen>(), "Màn bài hiện trước khi nạp xong");

            yield return WaitPrepared();
            Assert.IsNotNull(Object.FindAnyObjectByType<LessonScreen>());
            Assert.IsFalse(app.Curtain.IsShowing, "Màn chuyển không tắt");
        }

        [UnityTest]
        public IEnumerator DoubleTap_OpensOnce()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            AppRoot.Instance.ShowLesson("tv1_t1_b01");
            AppRoot.Instance.ShowLesson("tv1_t1_b01");
            yield return WaitPrepared();
            yield return null;
            Assert.AreEqual(1, Object.FindObjectsByType<LessonScreen>(FindObjectsSortMode.None).Length);
            foreach (var (kind, id) in LessonAssets.ContentIds(TestLessons.Real.Get("tv1_t1_b01")))
            {
                Assert.AreEqual(1, _source.LoadCount(kind, id), $"{kind} {id} nạp nhiều lần");
            }
        }

        [UnityTest]
        public IEnumerator BackToList_ReleasesLessonSet()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            AppRoot.Instance.ShowLesson("tv1_t1_b01");
            yield return WaitPrepared();
            AppRoot.Instance.ShowLessonList();
            yield return null;
            var own = OwnIds("tv1_t1_b01");
            Assert.IsNotEmpty(own);
            foreach (var (kind, id) in own) Assert.AreEqual(1, _source.ReleaseCount(kind, id), $"{kind} {id} chưa được nhả");
        }

        [UnityTest]
        public IEnumerator ResultScreen_KeepsSet_NextLessonReusesShared()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            app.ShowLesson("tv1_t1_b16");
            yield return WaitPrepared();
            app.ShowResult("tv1_t1_b16");
            yield return null;
            app.ShowLesson("tv1_t1_b17");
            yield return WaitPrepared();

            var b16 = OwnIds("tv1_t1_b16");
            var b17 = OwnIds("tv1_t1_b17");
            var shared = b16.Intersect(b17).ToList();
            Assert.IsNotEmpty(shared, "Bài 16 và 17 không có mã chung để kiểm tra");
            foreach (var (kind, id) in shared)
            {
                Assert.AreEqual(1, _source.LoadCount(kind, id), $"{kind} {id} bị nạp lại");
                Assert.AreEqual(0, _source.ReleaseCount(kind, id), $"{kind} {id} bị nhả dù bài 17 vẫn dùng");
            }
            foreach (var (kind, id) in b16.Except(b17))
            {
                Assert.AreEqual(1, _source.ReleaseCount(kind, id), $"{kind} {id} của bài 16 chưa được nhả");
            }
        }

        [UnityTest]
        public IEnumerator NextLesson_Broken_StaysOnResult()
        {
            _source.Put(ContentKind.Lesson, "tv1_t1_b17", new TextAsset("{ hỏng"));
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            app.ShowLesson("tv1_t1_b16");
            yield return WaitPrepared();
            app.ShowResult("tv1_t1_b16");
            yield return null;

            LogAssert.Expect(LogType.Error, new Regex("Không mở được bài.*tv1_t1_b17"));
            app.ShowLesson("tv1_t1_b17");
            yield return WaitPrepared();

            Assert.IsNotNull(Object.FindAnyObjectByType<ResultScreen>(), "Bài sau hỏng thì phải ở lại màn kết quả");
            Assert.IsNull(Object.FindAnyObjectByType<LessonScreen>());
            Assert.IsFalse(app.Curtain.IsShowing);
            foreach (var (kind, id) in OwnIds("tv1_t1_b16"))
            {
                Assert.AreEqual(0, _source.ReleaseCount(kind, id), $"{kind} {id} bị nhả dù vẫn ở màn kết quả");
            }
        }

        [UnityTest]
        public IEnumerator MissingPicture_StillEntersLesson()
        {
            var picture = LessonAssets.ImageIds(TestLessons.Real.Get("tv1_t1_b01")).First();
            _source.Put(ContentKind.Image, picture, null);
            yield return LoadMainWithProfile(unlockAll: true);
            LogAssert.Expect(LogType.Error, "[TapDoc] Thiếu tranh: " + picture);
            AppRoot.Instance.ShowLesson("tv1_t1_b01");
            yield return WaitPrepared();
            Assert.IsNotNull(Object.FindAnyObjectByType<LessonScreen>());
        }

        [UnityTest]
        public IEnumerator AppDestroyedWhilePreparing_NoErrors()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            AppRoot.Instance.ShowLesson("tv1_t1_b01");
            yield return null;
            Object.Destroy(AppRoot.Instance.gameObject);
            for (var i = 0; i < 8; i++) yield return null;
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator Review_PreparesRoundsFromSeveralLessons()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            app.Progress.RecordMistake("tv1_t1_b13", 0);
            app.Progress.RecordMistake("tv1_t1_b04", 3);
            app.ShowReview();
            yield return WaitPrepared();
            var screen = Object.FindAnyObjectByType<LessonScreen>();
            Assert.IsNotNull(screen, "Ôn lại không mở");
            Assert.AreEqual(2, screen.Flow.TotalCount);
            yield return null;
            CollectionAssert.IsEmpty(app.Assets.UnpreparedAsks, "Phiên ôn hỏi tranh, âm thanh chưa chuẩn bị");
        }
    }
}
