using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    public abstract class ViewTestBase
    {
        protected Camera Cam;
        protected RenderTexture TargetTex;
        protected Canvas Canvas;
        protected LessonContext Ctx;
        private GameObject _rootGo;
        private Func<string, AudioClip> _audioLoader;
        private Func<string, Sprite> _imageLoader;
        private Texture2D _dummyTex;
        private readonly HashSet<object> _completedViews = new();

        [SetUp]
        public virtual void SetUp()
        {
            _completedViews.Clear();
            StepViewRegistry.RegisterAll();
            _dummyTex = new Texture2D(4, 4, TextureFormat.RGBA32, false);
            var pixels = new Color32[16];
            for (var i = 0; i < pixels.Length; i++) pixels[i] = new Color32(240, 200, 120, 255);
            _dummyTex.SetPixels32(pixels);
            _dummyTex.Apply();

            _audioLoader = id => AudioClip.Create(id, 4410, 1, 44100, false);
            _imageLoader = _ => Sprite.Create(_dummyTex, new Rect(0, 0, 4, 4), new Vector2(0.5f, 0.5f));

            _rootGo = new GameObject("ViewTestRoot");
            TargetTex = new RenderTexture(1920, 1080, 24);
            var camGo = new GameObject("TestCamera");
            camGo.transform.SetParent(_rootGo.transform, false);
            Cam = camGo.AddComponent<Camera>();
            Cam.clearFlags = CameraClearFlags.SolidColor;
            Cam.backgroundColor = new Color(0.965f, 0.933f, 0.863f);
            Cam.orthographic = true;
            Cam.targetTexture = TargetTex;
            // SpeechPlayer không tự tạo AudioListener: môi trường test đặt listener trên camera.
            if (Object.FindAnyObjectByType<AudioListener>() == null)
            {
                camGo.AddComponent<AudioListener>();
            }

            Canvas = UiKit.CreateCanvas(Cam);
            Canvas.transform.SetParent(_rootGo.transform, false);

            // Cùng hình học với app: vùng an toàn 1440 đơn vị, trong đó là màn bài học phủ kín, rồi Stage.
            var safeRt = UiKit.CreateSafeArea(Canvas.transform);
            var screenGo = new GameObject("LessonScreenArea", typeof(RectTransform));
            screenGo.transform.SetParent(safeRt, false);
            var screenRt = screenGo.GetComponent<RectTransform>();
            screenRt.anchorMin = Vector2.zero;
            screenRt.anchorMax = Vector2.one;
            screenRt.offsetMin = Vector2.zero;
            screenRt.offsetMax = Vector2.zero;
            var stageRt = UiKit.CreateStage(screenRt);

            if (Object.FindAnyObjectByType<EventSystem>() == null)
            {
                var esGo = new GameObject("EventSystem");
                esGo.transform.SetParent(_rootGo.transform, false);
                esGo.AddComponent<EventSystem>();
            }

            var spGo = new GameObject("SpeechPlayer");
            spGo.transform.SetParent(_rootGo.transform, false);
            var sp = spGo.AddComponent<SpeechPlayer>();
            var assets = new AssetCatalog(_audioLoader, _imageLoader);
            sp.Init(assets);
            sp.WaitScale = 0.05f;

            Ctx = new LessonContext
            {
                Assets = assets,
                Speech = sp,
                Stage = stageRt
            };
        }

        [TearDown]
        public virtual void TearDown()
        {
            if (Ctx?.Speech != null)
            {
                Ctx.Speech.Stop();
            }
            if (_rootGo != null)
            {
                Object.Destroy(_rootGo);
            }
            if (TargetTex != null)
            {
                Object.Destroy(TargetTex);
            }
            if (_dummyTex != null)
            {
                Object.Destroy(_dummyTex);
            }
        }

        /// <summary>
        /// Tạo màn Phần 1 qua <see cref="StepViewFactory"/> và theo dõi <c>Completed</c>. Handler được gắn
        /// trước <c>Bind</c>, nên màn báo xong ngay trong <c>Bind</c> vẫn được ghi nhận.
        /// </summary>
        protected IStepView CreateTrackedStep(Step step)
        {
            var tracker = TrackView();
            var view = StepViewFactory.CreateStep(step, Ctx, tracker.OnCompleted);
            tracker.Attach(view);
            return view;
        }

        /// <summary>Như <see cref="CreateTrackedStep"/>, cho lượt Phần 2.</summary>
        protected IRoundView CreateTrackedRound(Round round)
        {
            var tracker = TrackView();
            var view = StepViewFactory.CreateRound(round, Ctx, tracker.OnCompleted);
            tracker.Attach(view);
            return view;
        }

        /// <summary>
        /// Bộ theo dõi Completed cho một màn: truyền <see cref="ViewTracker.OnCompleted"/> làm handler cho
        /// StepViewFactory, rồi gọi <see cref="ViewTracker.Attach"/> với màn vừa tạo.
        /// </summary>
        protected ViewTracker TrackView() => new ViewTracker(_completedViews);

        protected sealed class ViewTracker
        {
            private readonly HashSet<object> _completed;
            private object _view;
            private bool _early;

            internal ViewTracker(HashSet<object> completed) => _completed = completed;

            public void OnCompleted()
            {
                if (_view == null) _early = true; // báo ngay trong Bind, trước khi biết màn
                else _completed.Add(_view);
            }

            public void Attach(object view)
            {
                _view = view;
                if (_early && view != null) _completed.Add(view);
            }
        }

        protected bool Done(object view) => _completedViews.Contains(view);

        /// <summary>Tạo màn cho bước <paramref name="part1Index"/> của bài thật <paramref name="lessonId"/>.</summary>
        protected IStepView Bind(string lessonId, int part1Index)
        {
            var lesson = LessonRepository.Load(lessonId);
            Ctx.Lesson = lesson;
            return CreateTrackedStep(lesson.part1[part1Index]);
        }

        /// <summary>Tạo màn cho lượt <paramref name="part2Index"/> của bài thật <paramref name="lessonId"/>.</summary>
        protected IRoundView BindRound(string lessonId, int part2Index)
        {
            var lesson = LessonRepository.Load(lessonId);
            Ctx.Lesson = lesson;
            return CreateTrackedRound(lesson.part2[part2Index]);
        }

        protected static DropSlot Slot(object view) => ResultSlot(view);

        /// <summary>Đổi loader tranh. Gọi trước <see cref="Bind"/>.</summary>
        protected void UseImageLoader(Func<string, Sprite> loader)
        {
            _imageLoader = loader;
            Ctx.Assets = new AssetCatalog(_audioLoader, _imageLoader);
            Ctx.Speech.Init(Ctx.Assets);
        }

        protected static GameObject RootOf(object view) =>
            view is IStepView s ? s.Root : (view as IRoundView)?.Root;

        protected static Tile TileWithText(object view, string plainText)
        {
            var tile = RootOf(view).GetComponentsInChildren<Tile>(true).FirstOrDefault(t => t.PlainText == plainText);
            Assert.IsNotNull(tile, $"Không có thẻ chữ '{plainText}'");
            return tile;
        }

        protected static Tile TileWithImage(object view, string imageId)
        {
            var tile = RootOf(view).GetComponentsInChildren<Tile>(true).FirstOrDefault(t => t.ImageId == imageId);
            Assert.IsNotNull(tile, $"Không có thẻ tranh '{imageId}'");
            return tile;
        }

        protected static List<string> Labels(object view) =>
            RootOf(view).GetComponentsInChildren<TMP_Text>(true).Select(t => t.text).ToList();

        /// <summary>Chờ tới khi màn đánh vần làm mẫu xong và đang chờ bé làm.</summary>
        protected static IEnumerator WaitPracticeReady(object view, float timeout = 5f)
        {
            var spell = (SpellView)view;
            var deadline = Time.realtimeSinceStartup + timeout;
            while (!spell.InPractice && Time.realtimeSinceStartup < deadline) yield return null;
            Assert.IsTrue(spell.InPractice, "Màn đánh vần chưa sẵn sàng cho bé làm");
        }

        protected static DragTile DragWithText(object view, string plainText)
        {
            var drag = TileWithText(view, plainText).GetComponent<DragTile>();
            Assert.IsNotNull(drag, $"Thẻ '{plainText}' không kéo được");
            return drag;
        }

        protected static DropSlot ResultSlot(object view)
        {
            var slot = RootOf(view).GetComponentInChildren<DropSlot>(true);
            Assert.IsNotNull(slot, "Màn không có ô nhận");
            return slot;
        }

        /// <summary>Chờ màn từ ứng dụng mở lớp đánh vần, cho lớp đó tự làm xong, rồi chờ lớp đóng lại.</summary>
        protected static IEnumerator CompleteOverlaySpell(object view, float timeout = 10f)
        {
            var items = (ItemsView)view;
            var deadline = Time.realtimeSinceStartup + timeout;
            while (items.ActiveOverlay == null && Time.realtimeSinceStartup < deadline) yield return null;
            var overlay = items.ActiveOverlay;
            Assert.IsNotNull(overlay, "Không thấy lớp đánh vần nào được mở");
            yield return ((ITestCompletable)overlay).CompleteForTest();
            while (items.ActiveOverlay == overlay && Time.realtimeSinceStartup < deadline) yield return null;
        }

        protected static UnityEngine.UI.Button ButtonWithText(object view, string label)
        {
            var button = RootOf(view).GetComponentsInChildren<UnityEngine.UI.Button>(true)
                .FirstOrDefault(b => b.GetComponentInChildren<TMP_Text>(true)?.text == label);
            Assert.IsNotNull(button, $"Không có nút '{label}'");
            return button;
        }

        protected static string MarkerOf(object view) =>
            RootOf(view).GetComponentInChildren<MarkerIcon>(true)?.ImageId;

        /// <summary>Khung tranh của thẻ tranh đầu tiên trong màn.</summary>
        protected static GameObject ImageBox(object view)
        {
            var tile = RootOf(view).GetComponentsInChildren<Tile>(true).FirstOrDefault(t => t.ImageId != null);
            Assert.IsNotNull(tile, "Màn không có thẻ tranh");
            return tile.ImageBox;
        }

        protected IEnumerator WaitCompleted(object view, float timeout = 5f)
        {
            var deadline = Time.realtimeSinceStartup + timeout;
            while (!Done(view) && Time.realtimeSinceStartup < deadline)
            {
                yield return null;
            }
            Assert.IsTrue(Done(view), $"Màn {view?.GetType().Name} chưa báo Completed sau {timeout}s");
        }
    }
}
