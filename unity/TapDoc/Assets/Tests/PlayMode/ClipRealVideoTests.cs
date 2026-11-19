using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.UI;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// Clip thật qua <c>VideoPlayer</c> (thiết kế tranh động mục 14). Chỉ chạy khi máy đã chép clip vào
    /// <c>Resources/clips</c> (<c>python tools/run_unity_media.py clips</c>); không có thì không kết luận. Tắt tiếng.
    /// </summary>
    [Category("Clip")]
    public class ClipRealVideoTests
    {
        private const string ClipId = "img_b01_bof";

        private GameObject _root;
        private RenderTexture _target;
        private float _volume;

        [SetUp]
        public void SetUp()
        {
            Motion.Scale = 0f;
            ClipPlayer.Enabled = true;
            ClipPlayer.DeviceCheck = null;
            ClipPlayer.BackendFactory = null;
            _volume = AudioListener.volume;
            AudioListener.volume = 0f;
        }

        [TearDown]
        public void TearDown()
        {
            AudioListener.volume = _volume;
            Motion.Scale = 1f;
            if (_root != null) Object.DestroyImmediate(_root);
            if (_target != null) Object.Destroy(_target);
        }

        [UnityTest]
        public IEnumerator RealClip_FirstFrameIn3s_CroppedCentre_PlaysToEnd_ThenStaticPicture()
        {
            var source = new ResourcesContentSource();
            if (source.Load(ContentKind.Clip, ClipId) == null)
                Assert.Inconclusive("Chưa chép clip vào Resources/clips (python tools/run_unity_media.py clips)");
            if (!ClipSupport.CurrentDevice()) Assert.Inconclusive("Máy chạy test không phát được clip");

            _root = new GameObject("RealClipRoot");
            _target = new RenderTexture(1280, 720, 0);
            var cam = new GameObject("Cam").AddComponent<Camera>();
            cam.transform.SetParent(_root.transform, false);
            cam.targetTexture = _target;
            if (Object.FindAnyObjectByType<AudioListener>() == null) cam.gameObject.AddComponent<AudioListener>();
            var canvas = UiKit.CreateCanvas(cam);
            canvas.transform.SetParent(_root.transform, false);

            var catalog = new AssetCatalog(source);
            yield return AwaitableTestUtil.Wait(catalog.PrepareAsync(new[] { (ContentKind.Clip, ClipId) }), null);
            var speech = new GameObject("Speech").AddComponent<SpeechPlayer>();
            speech.transform.SetParent(_root.transform, false);
            speech.Init(catalog);
            var player = new GameObject("ClipPlayer").AddComponent<ClipPlayer>();
            player.transform.SetParent(_root.transform, false);
            player.Init(catalog, speech);

            var sprite = FakeContentSource.NewSprite();
            var tile = UiKit.CreateTile(canvas.transform, string.Empty, sprite);
            tile.SetSprite(sprite, ClipId);
            ((RectTransform)tile.transform).sizeDelta = new Vector2(460f, 460f);

            var start = Time.realtimeSinceStartup;
            var run = player.PlayAsync(tile, ClipId).GetAwaiter();
            ClipOverlay overlay = null;
            while (Time.realtimeSinceStartup - start < ClipPlayer.FirstFrameTimeout + .5f)
            {
                overlay = tile.GetComponentInChildren<ClipOverlay>(true);
                if (overlay != null && overlay.GetComponent<CanvasGroup>().alpha >= 1f) break;
                yield return null;
            }
            Assert.IsNotNull(overlay, "có lớp phủ");
            Assert.AreEqual(1f, overlay.GetComponent<CanvasGroup>().alpha, "có khung đầu trong 3 s");
            Assert.AreEqual(0, player.Failures);

            var raw = overlay.GetComponent<RawImage>();
            Assert.AreEqual(.221875f, raw.uvRect.x, 1e-3f, "cắt phần vuông giữa clip 1280×720, bỏ 4 điểm ảnh mỗi mép");
            Assert.AreEqual(.55625f, raw.uvRect.width, 1e-3f);
            Assert.AreEqual(4f / 720f, raw.uvRect.y, 1e-3f);

            // Giữa clip: điểm giữa tranh không đen, không trong suốt (không có khung đen hay khung xoá trắng).
            yield return new WaitForSecondsRealtime(1f);
            var centre = CentrePixel((RenderTexture)raw.texture);
            Assert.Greater(centre.a, .5f, "khung hình có nội dung");
            Assert.Greater(centre.r + centre.g + centre.b, .3f, "không phải khung đen");

            while (!run.IsCompleted && Time.realtimeSinceStartup - start < 14f) yield return null;
            Assert.IsTrue(run.IsCompleted, "phát hết trong 14 s");
            Assert.IsTrue(run.GetResult());
            yield return null;
            Assert.IsNull(tile.GetComponentInChildren<ClipOverlay>(true), "hết clip thì về tranh tĩnh");
            Assert.IsFalse(player.IsPlaying);

            // Rời bài (thiết kế mục 9): bộ phát bỏ clip và nhả RenderTexture của nó.
            player.ReleaseAll();
            yield return null;
            var video = player.GetComponent<UnityEngine.Video.VideoPlayer>();
            Assert.IsNotNull(video, "phần phát thật đã được dùng");
            Assert.IsNull(video.clip, "không còn giữ clip");
            Assert.IsNull(video.targetTexture);
            var left = 0;
            foreach (var rt in Resources.FindObjectsOfTypeAll<RenderTexture>())
                if (rt != null && rt.name == "ClipTexture") left++;
            Assert.AreEqual(0, left, "không còn RenderTexture của bộ phát");
            Object.Destroy(sprite.texture);
        }

        private static Color CentrePixel(RenderTexture rt)
        {
            var active = RenderTexture.active;
            RenderTexture.active = rt;
            var tex = new Texture2D(1, 1, TextureFormat.RGBA32, false);
            tex.ReadPixels(new Rect(rt.width / 2f, rt.height / 2f, 1f, 1f), 0, 0);
            tex.Apply();
            RenderTexture.active = active;
            var c = tex.GetPixel(0, 0);
            Object.Destroy(tex);
            return c;
        }
    }

    /// <summary>
    /// Ảnh chụp cho root soát (thiết kế tranh động mục 14): bước từ khoá bài 1 (clip loop) ở 3 s và sau khi hết, bước
    /// tranh chùm nho (clip build) ở 0,2 s và 3 s; trên phone_20x9 và ipad_43. Lưu ở TestOutput/screens/&lt;máy&gt;/.
    /// </summary>
    [Category("Clip")]
    public class ClipScreensTests : AppTestBase
    {
        private const string Lesson = "tv1_t1_b01";
        private const string LoopId = "img_b01_gaf_troongs";
        private const string BuildId = "img_b01_chumf_nho";

        private float _volume;

        [SetUp]
        public void EnableRealClips()
        {
            ClipPlayer.Enabled = true;
            ClipPlayer.DeviceCheck = null;
            ClipPlayer.BackendFactory = null;
            _volume = AudioListener.volume;
            AudioListener.volume = 0f;
        }

        [TearDown]
        public void RestoreVolume() => AudioListener.volume = _volume;

        [UnityTest]
        public IEnumerator Screens_Phone20x9() => Shoot(ScreenSizes.Phone20x9);

        [UnityTest]
        public IEnumerator Screens_IPad43() => Shoot(ScreenSizes.IPad43);

        private IEnumerator Shoot(ScreenSize size)
        {
            var source = new ResourcesContentSource();
            if (source.Load(ContentKind.Clip, LoopId) == null || source.Load(ContentKind.Clip, BuildId) == null)
                Assert.Inconclusive("Chưa chép clip vào Resources/clips (python tools/run_unity_media.py clips)");
            if (!ClipSupport.CurrentDevice()) Assert.Inconclusive("Máy chạy test không phát được clip");

            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            app.Speech.WaitScale = .02f;
            var rt = ScreenSizes.Apply(app, size);
            app.ShowLesson(Lesson);
            yield return WaitPrepared();
            var s = Object.FindAnyObjectByType<LessonScreen>();

            yield return CompleteAndNext(s); // bước 1 (âm) → bước từ khoá
            yield return WaitClipShown(app.Clips, LoopId);
            yield return new WaitForSecondsRealtime(3f);
            Save(app, size, "clip_loop_3s");
            yield return WaitClipEnded(app.Clips);
            Save(app, size, "clip_loop_het");

            yield return CompleteAndNext(s); // từ khoá → phân tích
            yield return CompleteAndNext(s); // phân tích → tranh chùm nho
            yield return WaitClipShown(app.Clips, BuildId);
            yield return new WaitForSecondsRealtime(.2f);
            Save(app, size, "clip_build_0_2s");
            yield return new WaitForSecondsRealtime(2.8f);
            Save(app, size, "clip_build_3s");

            ScreenSizes.Reset(app, rt);
        }

        private static IEnumerator CompleteAndNext(LessonScreen s)
        {
            yield return ((ITestCompletable)s.CurrentView).CompleteForTest();
            yield return null;
            s.NextButton.onClick.Invoke();
            yield return null;
        }

        private static IEnumerator WaitClipShown(ClipPlayer clips, string id)
        {
            var deadline = Time.realtimeSinceStartup + 8f;
            while (Time.realtimeSinceStartup < deadline)
            {
                var overlay = clips.ActiveOverlay;
                if (clips.CurrentId == id && overlay != null && overlay.GetComponent<CanvasGroup>().alpha >= 1f) yield break;
                yield return null;
            }
            Assert.Fail($"Clip {id} không hiện");
        }

        private static IEnumerator WaitClipEnded(ClipPlayer clips)
        {
            var deadline = Time.realtimeSinceStartup + 12f;
            while (clips.IsPlaying && Time.realtimeSinceStartup < deadline) yield return null;
            Assert.IsFalse(clips.IsPlaying, "clip chạy hết");
            yield return null;
        }

        private static void Save(AppRoot app, ScreenSize size, string name) =>
            ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.Name}/{name}.png");
    }
}
