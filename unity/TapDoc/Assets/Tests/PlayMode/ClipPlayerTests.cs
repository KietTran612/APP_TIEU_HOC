using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.UI;

namespace TapDoc.Tests
{
    /// <summary>
    /// Bộ phát clip (thiết kế tranh động mục 5, 6, 10) trên phần phát giả: chỉ phát khi giọng đọc rảnh, giọng đọc bắt
    /// đầu thì dừng, mỗi lúc một clip, lớp phủ chỉ hiện khi có khung đầu, hỏng thì giữ tranh tĩnh.
    /// </summary>
    public class ClipPlayerTests
    {
        private const string LongSpeech = "am_dai";

        private GameObject _root;
        private Camera _cam;
        private RenderTexture _target;
        private Canvas _canvas;
        private SpeechPlayer _speech;
        private FakeClipBackend _backend;
        private ClipPlayer _player;
        private Texture2D _clipA;
        private Texture2D _clipB;
        private Sprite _sprite;

        [SetUp]
        public void SetUp()
        {
            Motion.Scale = 0f;
            ClipPlayer.Enabled = true;
            ClipPlayer.DeviceCheck = () => true;
            ClipPlayer.TimeoutScale = 1f;
            _backend = new FakeClipBackend();
            ClipPlayer.BackendFactory = _ => _backend;

            _root = new GameObject("ClipTestRoot");
            _target = new RenderTexture(640, 360, 0);
            _cam = new GameObject("Cam").AddComponent<Camera>();
            _cam.transform.SetParent(_root.transform, false);
            _cam.targetTexture = _target;
            if (Object.FindAnyObjectByType<AudioListener>() == null) _cam.gameObject.AddComponent<AudioListener>();
            _canvas = UiKit.CreateCanvas(_cam);
            _canvas.transform.SetParent(_root.transform, false);

            _clipA = new Texture2D(2, 2);
            _clipB = new Texture2D(2, 2);
            _sprite = FakeContentSource.NewSprite();
            var source = new FakeContentSource();
            source.Put(ContentKind.Clip, "img_a", _clipA);
            source.Put(ContentKind.Clip, "img_b", _clipB);
            source.Put(ContentKind.Speech, LongSpeech, AudioClip.Create(LongSpeech, 88200, 1, 44100, false));
            var catalog = new AssetCatalog(source);
            AwaitableTestUtil.RunNow(catalog.PrepareAsync(new[]
            {
                (ContentKind.Clip, "img_a"), (ContentKind.Clip, "img_b"), (ContentKind.Clip, "img_khong"),
                (ContentKind.Speech, LongSpeech),
            }));

            var spGo = new GameObject("SpeechPlayer");
            spGo.transform.SetParent(_root.transform, false);
            _speech = spGo.AddComponent<SpeechPlayer>();
            _speech.Init(catalog);

            var cpGo = new GameObject("ClipPlayer");
            cpGo.transform.SetParent(_root.transform, false);
            _player = cpGo.AddComponent<ClipPlayer>();
            _player.Init(catalog, _speech);
        }

        [TearDown]
        public void TearDown()
        {
            Motion.Scale = 1f;
            ClipPlayer.Enabled = true;
            ClipPlayer.DeviceCheck = null;
            ClipPlayer.BackendFactory = null;
            ClipPlayer.TimeoutScale = 1f;
            if (_speech != null) _speech.Stop();
            Object.DestroyImmediate(_root); // ngay, để test sau thấy đúng là không còn AudioListener nào
            Object.Destroy(_target);
            Object.Destroy(_clipA);
            Object.Destroy(_clipB);
        }

        private Tile NewTile(string imageId)
        {
            var tile = UiKit.CreateTile(_canvas.transform, string.Empty, _sprite);
            tile.SetSprite(_sprite, imageId);
            ((RectTransform)tile.transform).sizeDelta = new Vector2(460f, 460f);
            return tile;
        }

        private static ClipOverlay OverlayOf(Tile tile) =>
            tile == null ? null : tile.GetComponentInChildren<ClipOverlay>(true);

        private static IEnumerator Frames(int n)
        {
            for (var i = 0; i < n; i++) yield return null;
        }

        [UnityTest]
        public IEnumerator PlayAsync_WhenSpeechIdle_BeginsAndShowsOverlayAfterFirstFrame()
        {
            var tile = NewTile("img_a");
            var run = _player.PlayAsync(tile, "img_a").GetAwaiter();
            yield return null;
            Assert.AreEqual(1, _backend.BeginCount);
            Assert.AreSame(_clipA, _backend.LastClip);
            Assert.IsTrue(_player.IsPlaying);
            Assert.AreEqual("img_a", _player.CurrentId);
            var overlay = OverlayOf(tile);
            Assert.IsNotNull(overlay, "lớp phủ nằm trong thẻ tranh");
            Assert.IsTrue(overlay.transform.IsChildOf(tile.ImageBox.transform));
            Assert.AreEqual(0f, overlay.GetComponent<CanvasGroup>().alpha, "chưa có khung đầu: chưa hiện");

            _backend.FirstFrameReady = true;
            yield return Frames(2);
            Assert.AreEqual(1f, overlay.GetComponent<CanvasGroup>().alpha);
            var raw = overlay.GetComponent<RawImage>();
            Assert.AreSame(_backend.Texture, raw.texture);
            Assert.AreEqual(.221875f, raw.uvRect.x, 1e-4f, "phần vuông giữa, cắt thêm 4 điểm ảnh mỗi mép");
            Assert.AreEqual(4f / 720f, raw.uvRect.y, 1e-4f);
            Assert.AreEqual(.55625f, raw.uvRect.width, 1e-4f);
            Assert.IsFalse(run.IsCompleted);
        }

        [UnityTest]
        public IEnumerator PlayAsync_WhenSpeechBusy_DoesNotBegin()
        {
            var tile = NewTile("img_a");
            _ = _speech.PlayAsync(LongSpeech);
            yield return null;
            Assert.IsTrue(_speech.IsBusy);
            var run = _player.PlayAsync(tile, "img_a").GetAwaiter();
            yield return Frames(2);
            Assert.IsTrue(run.IsCompleted);
            Assert.IsFalse(run.GetResult());
            Assert.AreEqual(0, _backend.BeginCount);
            Assert.IsNull(OverlayOf(tile));
        }

        [UnityTest]
        public IEnumerator SpeechStarts_StopsClipAndRemovesOverlay()
        {
            var tile = NewTile("img_a");
            var run = _player.PlayAsync(tile, "img_a").GetAwaiter();
            yield return null;
            _backend.FirstFrameReady = true;
            yield return Frames(2);
            _ = _speech.PlayAsync(LongSpeech);
            yield return Frames(3);
            Assert.IsFalse(_player.IsPlaying);
            Assert.GreaterOrEqual(_backend.StopCount, 1);
            Assert.IsNull(OverlayOf(tile));
            Assert.IsTrue(run.IsCompleted);
            Assert.IsFalse(run.GetResult());
        }

        [UnityTest]
        public IEnumerator Finished_RemovesOverlayAndReturnsTrue()
        {
            var tile = NewTile("img_a");
            var run = _player.PlayAsync(tile, "img_a").GetAwaiter();
            yield return null;
            _backend.FirstFrameReady = true;
            yield return null;
            _backend.Finished = true;
            yield return Frames(3);
            Assert.IsTrue(run.IsCompleted);
            Assert.IsTrue(run.GetResult());
            Assert.IsFalse(_player.IsPlaying);
            Assert.IsNull(_player.CurrentId);
            Assert.IsNull(OverlayOf(tile));
            Assert.IsTrue(tile.ImageBox.activeSelf, "tranh tĩnh vẫn hiện");
        }

        [UnityTest]
        public IEnumerator Failed_ReturnsFalseKeepsPicture_LogsWarningOnce()
        {
            var tile = NewTile("img_a");
            _backend.FailOnBegin = true;
            LogAssert.Expect(LogType.Warning, "[TapDoc] Không phát được tranh động: img_a");
            var first = _player.PlayAsync(tile, "img_a").GetAwaiter();
            yield return Frames(2);
            Assert.IsTrue(first.IsCompleted);
            Assert.IsFalse(first.GetResult());
            Assert.IsNull(OverlayOf(tile));
            Assert.IsTrue(tile.ImageBox.activeSelf);
            Assert.AreEqual(1, _player.Failures);

            var second = _player.PlayAsync(tile, "img_a").GetAwaiter();
            yield return Frames(2);
            Assert.IsFalse(second.GetResult());
            LogAssert.NoUnexpectedReceived(); // cảnh báo một lần cho mỗi mã
        }

        [UnityTest]
        public IEnumerator FirstFrameTimeout_CountsAsFailure()
        {
            ClipPlayer.TimeoutScale = .01f; // 3 s × 0,01 = 0,03 s
            var tile = NewTile("img_a");
            LogAssert.Expect(LogType.Warning, "[TapDoc] Không phát được tranh động: img_a");
            var run = _player.PlayAsync(tile, "img_a").GetAwaiter();
            yield return new WaitForSecondsRealtime(.2f);
            Assert.IsTrue(run.IsCompleted);
            Assert.IsFalse(run.GetResult());
            Assert.AreEqual(1, _player.Failures);
            Assert.IsNull(OverlayOf(tile));
            Assert.IsFalse(_player.IsPlaying);
        }

        [UnityTest]
        public IEnumerator TwoFailuresInARow_TurnsClipsOff_SuccessResetsCount()
        {
            var tile = NewTile("img_a");
            _backend.FailOnBegin = true;
            LogAssert.Expect(LogType.Warning, "[TapDoc] Không phát được tranh động: img_a");
            yield return AwaitableTestUtil.Wait(_player.PlayAsync(tile, "img_a"), null);
            Assert.AreEqual(1, _player.Failures);

            _backend.FailOnBegin = false;
            var ok = _player.PlayAsync(tile, "img_a").GetAwaiter();
            yield return null;
            _backend.FirstFrameReady = true;
            yield return null;
            _backend.Finished = true;
            yield return Frames(3);
            Assert.IsTrue(ok.GetResult());
            Assert.AreEqual(0, _player.Failures, "phát được một lần thì đếm lại");

            _backend.FailOnBegin = true;
            LogAssert.Expect(LogType.Warning, "[TapDoc] Không phát được tranh động: img_b");
            yield return AwaitableTestUtil.Wait(_player.PlayAsync(tile, "img_a"), null);
            yield return AwaitableTestUtil.Wait(_player.PlayAsync(NewTile("img_b"), "img_b"), null);
            Assert.AreEqual(2, _player.Failures);
            Assert.IsFalse(_player.CanPlay("img_a"), "hỏng 2 lần liên tiếp: tắt clip");
            var begins = _backend.BeginCount;
            yield return AwaitableTestUtil.Wait(_player.PlayAsync(tile, "img_a"), null);
            Assert.AreEqual(begins, _backend.BeginCount);
        }

        [UnityTest]
        public IEnumerator PlayAsync_SecondTile_StopsFirst()
        {
            var tileA = NewTile("img_a");
            var tileB = NewTile("img_b");
            var runA = _player.PlayAsync(tileA, "img_a").GetAwaiter();
            yield return null;
            _backend.FirstFrameReady = true;
            yield return null;
            var runB = _player.PlayAsync(tileB, "img_b").GetAwaiter();
            yield return Frames(2);
            Assert.IsTrue(runA.IsCompleted);
            Assert.IsFalse(runA.GetResult());
            Assert.IsNull(OverlayOf(tileA));
            Assert.IsNotNull(OverlayOf(tileB));
            Assert.AreEqual("img_b", _player.CurrentId);
            Assert.AreSame(_clipB, _backend.LastClip);
            Assert.AreEqual(2, _backend.BeginCount);
            Assert.IsFalse(runB.IsCompleted);
        }

        // Thẻ bị huỷ đúng khung mà phần phát báo tin (khung đầu tới, hay clip hết), và PlayAsync chạy tiếp trước Update
        // của bộ phát: tắt component để giữ đúng thứ tự đó (thứ tự giữa await và Update không được Unity bảo đảm).

        [UnityTest]
        public IEnumerator TileDestroyedAsFirstFrameArrives_BeforePlayerUpdate_StopsWithoutError()
        {
            var tile = NewTile("img_a");
            var run = _player.PlayAsync(tile, "img_a").GetAwaiter();
            yield return null;
            _player.enabled = false;
            Object.DestroyImmediate(tile.gameObject);
            _backend.FirstFrameReady = true;
            yield return Frames(2);
            Assert.IsTrue(run.IsCompleted);
            Assert.IsFalse(run.GetResult(), "không lỗi, không phát");
            Assert.IsFalse(_player.IsPlaying);
            Assert.IsNull(_player.CurrentId);
            Assert.AreEqual(0, _player.Failures, "thẻ bị huỷ không phải clip hỏng");
            _player.enabled = true;
        }

        [UnityTest]
        public IEnumerator TileDestroyedAsClipEnds_BeforePlayerUpdate_StopsWithoutError()
        {
            var tile = NewTile("img_a");
            var run = _player.PlayAsync(tile, "img_a").GetAwaiter();
            yield return null;
            _backend.FirstFrameReady = true;
            yield return Frames(2);
            _player.enabled = false;
            Object.DestroyImmediate(tile.gameObject);
            _backend.Finished = true;
            yield return Frames(2);
            Assert.IsTrue(run.IsCompleted);
            Assert.IsFalse(run.GetResult());
            Assert.IsFalse(_player.IsPlaying);
            Assert.IsNull(_player.CurrentId);
            _player.enabled = true;
        }

        [UnityTest]
        public IEnumerator StepDestroyedDuringFadeOut_StopsCleanly()
        {
            Motion.Scale = 1f; // mờ ra thật (0,25 s)
            var tile = NewTile("img_a");
            var run = _player.PlayAsync(tile, "img_a").GetAwaiter();
            yield return null;
            _backend.FirstFrameReady = true;
            yield return new WaitForSecondsRealtime(ClipPlayer.FadeInSeconds + .1f);
            _backend.Finished = true;
            yield return Frames(2); // đang mờ ra
            Assert.IsTrue(_player.IsPlaying, "đối chứng: còn đang mờ ra");
            Object.Destroy(tile.gameObject); // bé bấm Tiếp ngay khi clip hết
            yield return new WaitForSecondsRealtime(ClipPlayer.FadeOutSeconds + .2f);
            Assert.IsTrue(run.IsCompleted);
            run.GetResult();
            Assert.IsFalse(_player.IsPlaying);
            Assert.IsNull(_player.CurrentId);
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator PlayAsync_StopDuringWaitForFirstFrame_LeavesNoOverlay()
        {
            var tile = NewTile("img_a");
            var run = _player.PlayAsync(tile, "img_a").GetAwaiter();
            yield return null;
            _player.Stop();
            yield return Frames(2);
            Assert.IsTrue(run.IsCompleted);
            Assert.IsFalse(run.GetResult());
            Assert.IsFalse(_player.IsPlaying);
            Assert.IsNull(OverlayOf(tile));
            _backend.FirstFrameReady = true; // khung đầu tới muộn: không được hiện lại lớp phủ
            yield return Frames(2);
            Assert.IsNull(OverlayOf(tile));
            Assert.AreEqual(0, _player.Failures, "bị dừng không phải hỏng");
        }

        [UnityTest]
        public IEnumerator TileDestroyedWhilePlaying_StopsAndClearsState()
        {
            var tile = NewTile("img_a");
            var run = _player.PlayAsync(tile, "img_a").GetAwaiter();
            yield return null;
            _backend.FirstFrameReady = true;
            yield return null;
            Object.Destroy(tile.gameObject);
            yield return Frames(3);
            Assert.IsFalse(_player.IsPlaying);
            Assert.IsNull(_player.CurrentId);
            Assert.GreaterOrEqual(_backend.StopCount, 1);
            Assert.IsTrue(run.IsCompleted);
            Assert.IsFalse(run.GetResult());
        }

        [UnityTest]
        public IEnumerator ReleaseAll_StopsAndReleasesBackend()
        {
            var tile = NewTile("img_a");
            _ = _player.PlayAsync(tile, "img_a");
            yield return null;
            _backend.FirstFrameReady = true;
            yield return null;
            _player.ReleaseAll();
            Assert.IsFalse(_player.IsPlaying);
            Assert.IsNull(_backend.LastClip, "bỏ tham chiếu clip");
            Assert.AreEqual(1, _backend.ReleaseCount);
            yield return null;
            Assert.IsNull(OverlayOf(tile));
        }

        [UnityTest]
        public IEnumerator ApplicationPause_StopsClip()
        {
            var tile = NewTile("img_a");
            _ = _player.PlayAsync(tile, "img_a");
            yield return null;
            _player.SendMessage("OnApplicationPause", true);
            yield return null;
            Assert.IsFalse(_player.IsPlaying);
        }

        [UnityTest]
        public IEnumerator SettingOff_CannotPlay_AndStopsCurrent()
        {
            var tile = NewTile("img_a");
            _ = _player.PlayAsync(tile, "img_a");
            yield return null;
            _player.SettingEnabled = false;
            Assert.IsFalse(_player.IsPlaying);
            Assert.IsFalse(_player.CanPlay("img_a"));
            var begins = _backend.BeginCount;
            yield return AwaitableTestUtil.Wait(_player.PlayAsync(tile, "img_a"), null);
            Assert.AreEqual(begins, _backend.BeginCount);
        }

        [UnityTest]
        public IEnumerator SettingOffThenOn_PlaysAgain()
        {
            var tile = NewTile("img_a");
            _backend.FailOnBegin = true;
            LogAssert.Expect(LogType.Warning, "[TapDoc] Không phát được tranh động: img_a");
            yield return AwaitableTestUtil.Wait(_player.PlayAsync(tile, "img_a"), null);
            yield return AwaitableTestUtil.Wait(_player.PlayAsync(tile, "img_a"), null);
            Assert.IsFalse(_player.CanPlay("img_a"));

            _player.SettingEnabled = false;
            _player.SettingEnabled = true;
            Assert.IsTrue(_player.CanPlay("img_a"), "bật lại: số lần hỏng về 0");
            _backend.FailOnBegin = false;
            _ = _player.PlayAsync(tile, "img_a");
            yield return null;
            Assert.IsTrue(_player.IsPlaying);
        }

        [Test]
        public void DeviceUnsupported_CannotPlay()
        {
            ClipPlayer.DeviceCheck = () => false;
            var go = new GameObject("ClipPlayer2");
            go.transform.SetParent(_root.transform, false);
            var weak = go.AddComponent<ClipPlayer>();
            weak.Init(new AssetCatalog(new FakeContentSource()), _speech);
            Assert.IsFalse(weak.CanPlay("img_a"));
        }

        [Test]
        public void Disabled_CannotPlay()
        {
            ClipPlayer.Enabled = false;
            Assert.IsFalse(_player.CanPlay("img_a"));
        }

        [UnityTest]
        public IEnumerator MissingClip_CannotPlay_NoLogs()
        {
            var tile = NewTile("img_khong");
            Assert.IsTrue(_player.CanPlay("img_a"), "đối chứng: có clip thì phát được");
            Assert.IsFalse(_player.CanPlay("img_khong"));
            Assert.IsFalse(_player.CanPlay(null));
            yield return AwaitableTestUtil.Wait(_player.PlayAsync(tile, "img_khong"), null);
            Assert.AreEqual(0, _backend.BeginCount);
            LogAssert.NoUnexpectedReceived();
        }
    }
}
