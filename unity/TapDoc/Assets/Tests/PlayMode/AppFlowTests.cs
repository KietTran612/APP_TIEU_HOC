using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.UI;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    public class AppFlowTests : AppTestBase
    {
        private const string TapType = "test_tap";
        private const string SyncType = "test_sync";
        private const string MissingAudio = "khong_co";

        private AudioClip _clip;
        private Texture2D _tex;
        private Sprite _sprite;

        private class TestTapView : IStepView, IRoundView, ITestCompletable
        {
            public GameObject Root { get; private set; }
            public event Action Completed;
            private Tile _tile;

            public void Bind(Step step, LessonContext ctx) => Build(ctx);

            public void Bind(Round round, LessonContext ctx) => Build(ctx);

            private void Build(LessonContext ctx)
            {
                Root = new GameObject("TestTapView", typeof(RectTransform));
                Root.transform.SetParent(ctx.Stage, false);
                _tile = UiKit.CreateTile(Root.transform, "Chạm");
                _tile.Tapped += () => Completed?.Invoke();
            }

            public void Replay() { }

            public IEnumerator CompleteForTest()
            {
                var done = false;
                Action mark = () => done = true;
                Completed += mark;
                try
                {
                    _tile.SimulateTap();
                    while (!done) yield return null;
                }
                finally
                {
                    Completed -= mark;
                }
            }
        }

        /// <summary>
        /// Màn đọc một âm thanh rồi báo Completed nếu đọc trọn. Âm thanh thiếu file xong ngay, nên
        /// Completed được báo ngay trong Bind, trước khi Bind trả về.
        /// </summary>
        private class SyncCompleteView : IStepView, IRoundView, ITestCompletable
        {
            public GameObject Root { get; private set; }
            public event Action Completed;

            public void Bind(Step step, LessonContext ctx) => _ = SpeakThenComplete(ctx);

            public void Bind(Round round, LessonContext ctx) => _ = SpeakThenComplete(ctx);

            private async Awaitable SpeakThenComplete(LessonContext ctx)
            {
                Root = new GameObject("SyncCompleteView", typeof(RectTransform));
                Root.transform.SetParent(ctx.Stage, false);
                UiKit.CreateTile(Root.transform, "Xong");
                if (await ctx.Speech.PlayAsync(MissingAudio))
                {
                    Completed?.Invoke();
                }
            }

            public void Replay() { }

            public IEnumerator CompleteForTest()
            {
                yield break;
            }
        }

        [SetUp]
        public void SetUp()
        {
            // Loader giả dùng chung một clip và một sprite (không tạo mới mỗi lần gọi).
            _clip = AudioClip.Create("test_clip", 4410, 1, 44100, false);
            _tex = new Texture2D(4, 4, TextureFormat.RGBA32, false);
            _sprite = Sprite.Create(_tex, new Rect(0, 0, 4, 4), new Vector2(0.5f, 0.5f));
            AppRoot.CatalogFactory = () => new AssetCatalog(
                id => id == MissingAudio ? null : _clip,
                _ => _sprite);
        }

        [UnityTearDown]
        public IEnumerator TearDown()
        {
            if (AppRoot.Instance != null)
            {
                if (AppRoot.Instance.Speech != null) AppRoot.Instance.Speech.Stop();
                Object.Destroy(AppRoot.Instance.gameObject);
            }
            AppRoot.CatalogFactory = null;
            StepViewFactory.Unregister(TapType);
            StepViewFactory.Unregister(SyncType);
            yield return null; // để Destroy chạy xong trước test sau

            if (_sprite != null) Object.Destroy(_sprite);
            if (_tex != null) Object.Destroy(_tex);
            if (_clip != null) Object.Destroy(_clip);
            _sprite = null;
            _tex = null;
            _clip = null;
        }

        private LessonScreen OpenSynthetic(int steps, int rounds, string stepType = TapType, string roundType = TapType)
        {
            StepViewFactory.Register(TapType, () => new TestTapView());
            StepViewFactory.RegisterRound(TapType, () => new TestTapView());
            StepViewFactory.Register(SyncType, () => new SyncCompleteView());
            StepViewFactory.RegisterRound(SyncType, () => new SyncCompleteView());

            var app = AppRoot.EnsureInstance();
            app.Speech.WaitScale = 0.05f;
            // Bé phải có hồ sơ mới vào được bài (nút "Về" đưa về danh sách bài của bé đó).
            if (app.Progress.Current == null) app.Progress.CreateProfile(TestChildName, ProfileScreen.Avatars[0]);

            var lesson = new Lesson
            {
                lesson_id = "tv1_t1_b04",
                lesson_no = 4,
                title = "Bài thử",
                type = "dau_thanh",
                part1 = Enumerable.Range(0, steps).Select(_ => new Step { type = stepType }).ToList(),
                part2 = Enumerable.Range(0, rounds).Select(_ => new Round { kind = roundType }).ToList()
            };

            app.ShowLesson(lesson);
            return Object.FindAnyObjectByType<LessonScreen>();
        }

        private static void TapCurrent(LessonScreen screen)
        {
            var root = screen.CurrentView switch
            {
                IStepView sv => sv.Root,
                IRoundView rv => rv.Root,
                _ => null
            };
            Assert.IsNotNull(root, "CurrentView root is null");
            var tile = root.GetComponentInChildren<Tile>();
            Assert.IsNotNull(tile, "No Tile in CurrentView");
            tile.SimulateTap();
        }

        private static void Click(Button btn)
        {
            Assert.IsNotNull(btn, "Button is null");
            if (!btn.gameObject.activeInHierarchy || !btn.interactable) return;
            btn.onClick.Invoke();
        }

        [UnityTest]
        public IEnumerator MainScene_ListsIndexLessons()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            var list = Object.FindObjectsByType<LessonListScreen>(FindObjectsSortMode.None).Single();
            var labels = list
                .GetComponentsInChildren<TMP_Text>()
                .Select(t => t.text)
                .ToList();
            var entries = LessonRepository.LoadIndex().lessons;
            Assert.AreEqual(entries.Count, list.LessonCount);
            foreach (var e in entries)
            {
                Assert.That(labels, Has.Some.StartsWith($"{UiText.LessonPrefix} {e.lesson_no}\n"));
                Assert.IsNotNull(list.ButtonFor(e.lesson_id), $"Không có thẻ bài {e.lesson_id}");
            }
        }

        [UnityTest]
        public IEnumerator NextHiddenUntilCompleted_ThenResult()
        {
            var screen = OpenSynthetic(steps: 2, rounds: 1);
            Assert.IsFalse(screen.NextButton.gameObject.activeSelf);
            TapCurrent(screen);
            yield return null;
            Assert.IsTrue(screen.NextButton.gameObject.activeSelf);
            Click(screen.NextButton);
            yield return null;
            Assert.AreEqual(1, screen.Flow.StepIndex);
            TapCurrent(screen);
            yield return null;
            Click(screen.NextButton);
            yield return null;
            Assert.AreEqual(Phase.Part2, screen.Flow.Phase);
            TapCurrent(screen);
            yield return new WaitForSeconds(1f);
            Assert.IsNotNull(Object.FindAnyObjectByType<ResultScreen>());
        }

        [UnityTest]
        public IEnumerator DoubleClickNext_AdvancesOnce()
        {
            var screen = OpenSynthetic(steps: 3, rounds: 1);
            TapCurrent(screen);
            yield return null;
            Click(screen.NextButton);
            // Gọi thẳng onClick (bỏ qua kiểm tra nút đang hiện của Click) để thử chốt chặn trong LessonScreen.
            screen.NextButton.onClick.Invoke();
            yield return null;
            Assert.AreEqual(1, screen.Flow.StepIndex);
        }

        [UnityTest]
        public IEnumerator BackDuringSpeech_StopsAndReturnsToList()
        {
            var screen = OpenSynthetic(steps: 1, rounds: 1);
            _ = AppRoot.Instance.Speech.PlaySequenceAsync(new[] { "am_dd", "van_u", "tieng_ddu" }, _ => { });
            Click(screen.BackButton);
            yield return new WaitForSeconds(.3f);
            Assert.IsFalse(AppRoot.Instance.Speech.IsBusy);
            Assert.IsNotNull(Object.FindAnyObjectByType<LessonListScreen>());
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator LessonList_FitsPhoneAndTablet()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            foreach (var size in new[] { new Vector2Int(2400, 1080), new Vector2Int(2048, 1536) })
            {
                var rt = new RenderTexture(size.x, size.y, 24);
                AppRoot.Instance.UiCamera.targetTexture = rt;
                AppRoot.Instance.ShowLessonList();
                yield return null;
                LayoutProbe.AssertFits(AppRoot.Instance.Canvas);
                AppRoot.Instance.UiCamera.targetTexture = null;
                Object.Destroy(rt);
            }
        }

        [UnityTest]
        public IEnumerator CompletedInsideBind_ShowsNext()
        {
            LogAssert.Expect(LogType.Error, "[TapDoc] Thiếu âm thanh: " + MissingAudio);
            var screen = OpenSynthetic(steps: 2, rounds: 1, stepType: SyncType);
            Assert.IsInstanceOf<SyncCompleteView>(screen.CurrentView);
            Assert.IsTrue(screen.NextButton.gameObject.activeSelf, "Màn báo xong trong Bind nhưng nút Tiếp không hiện");
            yield return null;
            Click(screen.NextButton);
            yield return null;
            Assert.AreEqual(1, screen.Flow.StepIndex);
            Assert.IsTrue(screen.NextButton.gameObject.activeSelf);
        }

        [UnityTest]
        public IEnumerator RoundCompletedInsideBind_AdvancesToResult()
        {
            LogAssert.Expect(LogType.Error, "[TapDoc] Thiếu âm thanh: " + MissingAudio);
            var screen = OpenSynthetic(steps: 1, rounds: 2, roundType: SyncType);
            TapCurrent(screen);
            yield return null;
            Click(screen.NextButton);
            yield return null;
            Assert.AreEqual(Phase.Done, screen.Flow.Phase);
            Assert.IsNotNull(Object.FindAnyObjectByType<ResultScreen>());
        }

        [UnityTest]
        public IEnumerator Result_MissingStarImage_DrawsStarNotSquare()
        {
            // Thiếu tranh ngôi sao: catalog báo thiếu như mọi tranh khác; màn kết quả vẽ ngôi sao vàng, không vẽ ô vuông.
            AppRoot.CatalogFactory = () => new AssetCatalog(
                _ => _clip,
                id => id == SystemImages.Star ? null : _sprite);
            LogAssert.Expect(LogType.Error, "[TapDoc] Thiếu tranh: " + SystemImages.Star);
            var app = AppRoot.EnsureInstance();
            app.Progress.CreateProfile(TestChildName, ProfileScreen.Avatars[0]);
            app.ShowResult("tv1_t1_b04");
            yield return null;

            var stars = Object.FindAnyObjectByType<ResultScreen>().GetComponentsInChildren<MarkerIcon>();
            Assert.AreEqual(3, stars.Length);
            foreach (var star in stars)
            {
                var img = star.GetComponent<Image>();
                Assert.IsTrue(star.IsFallback);
                Assert.AreSame(MarkerIcon.FallbackStar, img.sprite);
                Assert.AreNotSame(UiKit.WhiteSprite, img.sprite);
                Assert.AreEqual(MarkerIcon.StarYellow, img.color);
            }
        }
    }
}
