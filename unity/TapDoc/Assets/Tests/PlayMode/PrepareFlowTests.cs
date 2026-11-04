using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.UI;
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
        public IEnumerator Curtain_ShowsMascot()
        {
            var mascot = FakeContentSource.NewSprite("ga_con");
            _source.Put(ContentKind.Image, SystemImages.Mascot, mascot);
            yield return LoadMainWithProfile(unlockAll: true);
            AppRoot.Instance.ShowLesson("tv1_t1_b01");
            yield return null;
            var curtain = AppRoot.Instance.Curtain;
            Assert.IsTrue(curtain.IsShowing);
            Assert.IsTrue(curtain.GetComponentsInChildren<Image>().Any(i => i.sprite == mascot), "Màn chuyển không có gà con");
            yield return WaitPrepared();
        }

        [UnityTest]
        public IEnumerator Curtain_MinDuration_WhenMotionOn()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            _source.DelayFrames = 0;
            Motion.Scale = 1f;
            AppRoot.Instance.ShowLesson("tv1_t1_b01");
            yield return new WaitForSecondsRealtime(.2f);
            Assert.IsTrue(AppRoot.Instance.Curtain.IsShowing, "Màn chuyển tắt trước thời gian tối thiểu");
            yield return new WaitForSecondsRealtime(.8f);
            Assert.IsFalse(AppRoot.Instance.Curtain.IsShowing, "Màn chuyển không tắt");
            Assert.IsFalse(AppRoot.Instance.IsPreparing);
        }

        [UnityTest]
        public IEnumerator Curtain_FitsBothFrames()
        {
            // Ảnh chụp cho chủ dự án xem: dùng tranh gà con thật.
            _source.Put(ContentKind.Image, SystemImages.Mascot,
                new ResourcesContentSource().Load(ContentKind.Image, SystemImages.Mascot));
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            foreach (var size in new[] { new Vector2Int(2400, 1080), new Vector2Int(2048, 1536) })
            {
                var rt = new RenderTexture(size.x, size.y, 24);
                app.UiCamera.targetTexture = rt;
                app.Curtain.Show();
                yield return null;
                Canvas.ForceUpdateCanvases();
                var mascot = app.Curtain.GetComponentInChildren<Mascot>();
                Assert.IsNotNull(mascot, "Màn chuyển không có gà con");
                AssertInside(app.SafeRoot, (RectTransform)mascot.transform, size);
                LayoutProbe.AssertFits(app.Canvas);
                ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.x}x{size.y}/app_prepare_curtain.png");
                app.Curtain.Hide();
                app.UiCamera.targetTexture = null;
                Object.Destroy(rt);
            }
        }

        private static void AssertInside(RectTransform outer, RectTransform inner, Vector2Int size)
        {
            var o = new Vector3[4];
            var i = new Vector3[4];
            outer.GetWorldCorners(o);
            inner.GetWorldCorners(i);
            const float eps = .01f;
            Assert.IsTrue(i[0].x >= o[0].x - eps && i[0].y >= o[0].y - eps && i[2].x <= o[2].x + eps && i[2].y <= o[2].y + eps,
                $"Gà con tràn khỏi vùng an toàn ở khung {size.x}×{size.y}");
        }

        /// <summary>Màn bước thử: <c>Bind</c> hỏi một tranh không có trong bài, hoặc ném lỗi.</summary>
        private sealed class ProbeStepView : IStepView
        {
            public const string AsksImage = "test_hoi_tranh";
            public const string Throws = "test_nem_loi";
            public const string ExtraImage = "img_test_ngoai_bai";

            public GameObject Root { get; private set; }
            public event System.Action Completed;

            public void Bind(Step step, LessonContext ctx)
            {
                if (step.type == Throws) throw new System.InvalidOperationException("màn thử hỏng");
                Root = new GameObject("ProbeStepView", typeof(RectTransform));
                Root.transform.SetParent(ctx.Stage, false);
                ctx.Assets.Image(ExtraImage);
                Completed?.Invoke();
            }

            public void Replay() { }
        }

        private static Lesson Synthetic(string stepType) => new()
        {
            lesson_id = "tv1_t1_b04",
            lesson_no = 4,
            title = "Bài thử",
            part1 = new List<Step> { new() { type = stepType } },
            part2 = new List<Round>(),
        };

        [UnityTest]
        public IEnumerator OtherError_WhilePreparing_DoesNotFreeze()
        {
            var inner = _source.Fallback;
            _source.Fallback = (kind, id) => kind == ContentKind.Lesson && id == "tv1_t1_b17"
                ? throw new System.InvalidOperationException("nguồn hỏng")
                : inner(kind, id);
            yield return LoadMainWithProfile(unlockAll: true);
            LogAssert.Expect(LogType.Error, new Regex("Không mở được bài tv1_t1_b17"));
            AppRoot.Instance.ShowLesson("tv1_t1_b17");
            yield return WaitPrepared();
            Assert.IsFalse(AppRoot.Instance.Curtain.IsShowing, "Màn chuyển kẹt lại, bé không chạm được gì");
            Assert.IsNotNull(Object.FindAnyObjectByType<LessonListScreen>());
        }

        [UnityTest]
        public IEnumerator ScreenBuildThrows_FallsBackToList()
        {
            StepViewFactory.Register(ProbeStepView.Throws, () => new ProbeStepView());
            try
            {
                yield return LoadMainWithProfile(unlockAll: true);
                LogAssert.Expect(LogType.Error, new Regex("Không mở được bài"));
                AppRoot.Instance.ShowLesson(Synthetic(ProbeStepView.Throws));
                yield return WaitPrepared();
                Assert.IsFalse(AppRoot.Instance.Curtain.IsShowing, "Màn chuyển kẹt lại, bé không chạm được gì");
                Assert.IsNotNull(Object.FindAnyObjectByType<LessonListScreen>(), "Dựng màn bài lỗi thì phải về danh sách bài");
            }
            finally
            {
                StepViewFactory.Unregister(ProbeStepView.Throws);
            }
        }

        [UnityTest]
        public IEnumerator UnpreparedAskDuringBuild_CountsIntoNewSet()
        {
            StepViewFactory.Register(ProbeStepView.AsksImage, () => new ProbeStepView());
            try
            {
                yield return LoadMainWithProfile(unlockAll: true);
                AppRoot.Instance.ShowLesson("tv1_t1_b01");
                yield return WaitPrepared();
                LogAssert.Expect(LogType.Warning, "[TapDoc] Chưa chuẩn bị trước: " + ProbeStepView.ExtraImage);
                AppRoot.Instance.ShowLesson(Synthetic(ProbeStepView.AsksImage));
                yield return WaitPrepared();
                Assert.AreEqual(0, _source.ReleaseCount(ContentKind.Image, ProbeStepView.ExtraImage),
                    "Tranh màn mới hỏi lúc dựng bị tính vào bộ cũ và bị nhả ngay");
            }
            finally
            {
                StepViewFactory.Unregister(ProbeStepView.AsksImage);
            }
        }

        [UnityTest]
        public IEnumerator Parent_PreparesLessonTexts_ReadsOnce()
        {
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            app.ShowParent();
            Assert.IsTrue(app.IsPreparing);
            var frames = 0;
            for (; frames < 300 && app.IsPreparing; frames++) yield return null;
            Assert.Less(frames, 40, "Nạp chữ các bài lần lượt từng bài một, quá chậm");
            yield return WaitPrepared();
            Assert.IsNotNull(Object.FindAnyObjectByType<ParentScreen>());
            app.ShowLessonList();
            yield return null;
            app.ShowParent();
            yield return WaitPrepared();
            Assert.AreEqual(1, _source.LoadCount(ContentKind.Lesson, "tv1_t1_b01"));
            Assert.AreEqual(1, _source.LoadCount(ContentKind.Lesson, "tv1_t1_b80"));
        }

        [UnityTest]
        public IEnumerator Parent_AppendixTap_LoadsAudioWithoutWarning_ReleasedOnLeave()
        {
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            app.ShowParent();
            yield return WaitPrepared();
            var p = Object.FindAnyObjectByType<ParentScreen>();
            p.SimulateUnlock();
            yield return null;
            Press(ButtonUnder(p, UiText.BookAppendix));
            yield return null;
            Press(ButtonUnder(p, "sờ"));
            for (var i = 0; i < 10; i++) yield return null;
            Assert.AreEqual("am_s", app.Speech.History.Last());
            LogAssert.NoUnexpectedReceived();

            app.ShowLessonList();
            yield return null;
            Assert.AreEqual(1, _source.LoadCount(ContentKind.Speech, "am_s"));
            Assert.AreEqual(1, _source.ReleaseCount(ContentKind.Speech, "am_s"), "Âm thanh nạp lẻ ở màn Phụ huynh chưa được nhả");
        }

        private static Button ButtonUnder(Component root, string text) =>
            root.GetComponentsInChildren<Button>(false)
                .FirstOrDefault(b => b.GetComponentInChildren<TMPro.TMP_Text>(true)?.text == text);

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
