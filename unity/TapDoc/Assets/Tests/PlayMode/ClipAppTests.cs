using System;
using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// Tranh động ráp vào app (thiết kế tranh động mục 6, 8.3, 9, 11): màn học dừng clip khi đi tiếp, về danh sách,
    /// mở ghi chú; clip đang chạy tính là bận; trang lật không mang lớp phủ; rời bài thì nhả clip trước khi dọn bộ.
    /// </summary>
    public class ClipAppTests : AppTestBase
    {
        private const string Lesson01 = "tv1_t1_b01";
        private const string Keyword01 = "img_b01_gaf_troongs";

        private FakeClipBackend _backend;
        private ClipSource _source;
        private Texture2D _fakeClip;

        /// <summary>
        /// Nguồn thật cho mọi thứ trừ clip (clip giả cho mọi mã tranh). Ghi lại, ở lần được nhờ dọn đầu tiên sau khi có
        /// clip chạy, phần phát đã bỏ clip và nhả chưa.
        /// </summary>
        private sealed class ClipSource : IContentSource
        {
            private readonly ResourcesContentSource _real = new();
            private readonly Object _clip;
            private readonly FakeClipBackend _backend;

            public ClipSource(Object clip, FakeClipBackend backend)
            {
                _clip = clip;
                _backend = backend;
            }

            /// <summary>Ở lần dọn đầu tiên sau khi clip đã bắt đầu: (đã nhả phần phát, còn giữ clip).</summary>
            public (bool released, bool holdsClip)? AtFirstCleanupAfterPlay { get; private set; }

            public async Awaitable<Object> LoadAsync(ContentKind kind, string id) =>
                kind == ContentKind.Clip ? _clip : await _real.LoadAsync(kind, id);

            public Object Load(ContentKind kind, string id) => kind == ContentKind.Clip ? _clip : _real.Load(kind, id);

            public void Release(ContentKind kind, string id, Object asset) => _real.Release(kind, id, asset);

            public void ReleaseUnused()
            {
                if (_backend.BeginCount > 0 && AtFirstCleanupAfterPlay == null)
                    AtFirstCleanupAfterPlay = (_backend.ReleaseCount > 0, _backend.LastClip != null);
                _real.ReleaseUnused();
            }
        }

        [SetUp]
        public void SetUpClips()
        {
            Assert.IsFalse(ClipPlayer.Enabled, "test app chạy với clip tắt (AppTestBase)");
            ClipPlayer.Enabled = true;
            ClipPlayer.DeviceCheck = () => true;
            _backend = new FakeClipBackend();
            ClipPlayer.BackendFactory = _ => _backend;
            _fakeClip = new Texture2D(2, 2);
            _source = new ClipSource(_fakeClip, _backend);
            var source = _source;
            AppRoot.SourceFactory = () => source;
        }

        [TearDown]
        public void TearDownClips()
        {
            AppRoot.SourceFactory = null;
            ClipPlayer.DeviceCheck = null;
            ClipPlayer.BackendFactory = null;
            Object.Destroy(_fakeClip);
        }

        private static LessonScreen Screen() => Object.FindAnyObjectByType<LessonScreen>();

        private static ClipPlayer Clips => AppRoot.Instance.Clips;

        private static IEnumerator WaitFor(Func<bool> condition, float timeout = 3f)
        {
            var deadline = Time.realtimeSinceStartup + timeout;
            while (!condition() && Time.realtimeSinceStartup < deadline) yield return null;
        }

        /// <summary>Mở bài 1 và đi tới bước từ khoá (bước 2), chờ clip tự phát và có khung đầu.</summary>
        private IEnumerator OpenKeywordWithClip()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            AppRoot.Instance.Speech.WaitScale = .02f;
            AppRoot.Instance.ShowLesson(Lesson01);
            yield return WaitPrepared();
            var s = Screen();
            yield return ((ITestCompletable)s.CurrentView).CompleteForTest();
            yield return null;
            s.NextButton.onClick.Invoke();
            yield return WaitFor(() => _backend.BeginCount > 0);
            Assert.AreEqual(Keyword01, Clips.CurrentId, "bước từ khoá tự phát clip");
            _backend.FirstFrameReady = true;
            yield return null;
        }

        private static Tile PictureTile(LessonScreen s) =>
            ((IStepView)s.CurrentView).Root.GetComponentsInChildren<Tile>(true).First(t => t.ImageId == Keyword01);

        [UnityTest]
        public IEnumerator Next_StopsClip()
        {
            yield return OpenKeywordWithClip();
            var s = Screen();
            PictureTile(s).SimulateTap(); // làm bước xong; đọc xong thì clip phát lại
            yield return WaitFor(() => _backend.BeginCount > 1 && Clips.IsPlaying);
            Assert.IsTrue(s.NextButton.gameObject.activeSelf);
            s.NextButton.onClick.Invoke();
            yield return null;
            Assert.IsFalse(Clips.IsPlaying);
        }

        [UnityTest]
        public IEnumerator BackToList_ReleasesClipBeforeSetCleanup()
        {
            yield return OpenKeywordWithClip();
            Assert.IsTrue(Clips.IsPlaying);
            Screen().BackButton.onClick.Invoke();
            yield return null;
            Assert.IsFalse(Clips.IsPlaying);
            Assert.IsNotNull(_source.AtFirstCleanupAfterPlay, "rời bài có dọn bộ");
            var (released, holdsClip) = _source.AtFirstCleanupAfterPlay.Value;
            Assert.IsTrue(released, "phần phát nhả RenderTexture trước khi dọn");
            Assert.IsFalse(holdsClip, "phần phát bỏ clip trước khi dọn");
        }

        [UnityTest]
        public IEnumerator OpenNotes_StopsClip()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            AppRoot.Instance.Speech.WaitScale = .02f;
            AppRoot.Instance.ShowLesson("tv1_t1_b68"); // bước 2 là tranh có clip, bài có ghi chú
            yield return WaitPrepared();
            var s = Screen();
            yield return ((ITestCompletable)s.CurrentView).CompleteForTest();
            yield return null;
            s.NextButton.onClick.Invoke();
            yield return WaitFor(() => Clips.IsPlaying);
            Assert.IsTrue(Clips.IsPlaying);
            Press(s.NotesButton);
            yield return null;
            Assert.IsFalse(Clips.IsPlaying);
        }

        [UnityTest]
        public IEnumerator ClipPlaying_CountsAsBusy_NoNudge()
        {
            yield return OpenKeywordWithClip();
            var s = Screen();
            var now = 1000f;
            IdleNudge.Enabled = true;
            s.Clock = () => now;
            yield return null;
            s.Nudge.NoteActivity(now);
            now += IdleNudge.TapRepromptSeconds + 1f; // quá giờ nhắc trong lúc clip vẫn chạy
            yield return null;
            yield return null;
            Assert.IsTrue(Clips.IsPlaying, "nhắc không được cắt clip");
            Assert.AreEqual(0, s.Nudge.Count);
        }

        [UnityTest]
        public IEnumerator PageTurnCopy_HasNoOverlay()
        {
            yield return OpenKeywordWithClip();
            var s = Screen();
            PictureTile(s).SimulateTap(); // làm bước xong; đọc xong thì clip phát lại
            yield return WaitFor(() => _backend.BeginCount > 1 && Clips.IsPlaying);
            _backend.FirstFrameReady = true;
            yield return null;
            Assert.IsNotNull(PictureTile(s).GetComponentInChildren<ClipOverlay>(true), "đối chứng: clip đang hiện");
            Motion.Scale = 1f; // có trang lật
            s.NextButton.onClick.Invoke();
            Assert.IsNotNull(s.TurningPage, "đang lật trang");
            Assert.IsEmpty(s.TurningPage.GetComponentsInChildren<ClipOverlay>(true), "trang lật chỉ có tranh tĩnh");
            Motion.Scale = 0f;
        }

        [UnityTest]
        public IEnumerator SavedSettingOff_AppliedOnStart()
        {
            var store = new ProgressStore(StorePath);
            store.ClipsEnabled = false;
            store.Save();
            yield return LoadMainKeepingStore();
            Assert.IsFalse(Clips.SettingEnabled);
            Assert.IsFalse(Clips.CanPlay(Keyword01));
        }
    }
}
