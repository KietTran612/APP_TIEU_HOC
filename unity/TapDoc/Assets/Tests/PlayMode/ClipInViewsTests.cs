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
    /// Bốn màn Phần 1 phát clip ngay sau khi đọc chữ của tranh (thiết kế tranh động mục 4), trên phần phát giả.
    /// </summary>
    public class ClipInViewsTests : ViewTestBase
    {
        private FakeClipBackend _backend;
        private ClipPlayer _clips;
        private GameObject _host;
        private Texture2D _fakeClip;

        [SetUp]
        public override void SetUp()
        {
            base.SetUp();
            ClipPlayer.Enabled = true;
            ClipPlayer.DeviceCheck = () => true;
            _backend = new FakeClipBackend();
            ClipPlayer.BackendFactory = _ => _backend;
            _fakeClip = new Texture2D(2, 2);
            var clip = _fakeClip;
            UseClipLoader(_ => clip);
            _host = new GameObject("ClipPlayer");
            _clips = _host.AddComponent<ClipPlayer>();
            _clips.Init(Ctx.Assets, Ctx.Speech);
            Ctx.Clips = _clips;
        }

        [TearDown]
        public override void TearDown()
        {
            ClipPlayer.DeviceCheck = null;
            ClipPlayer.BackendFactory = null;
            Object.Destroy(_host);
            Object.Destroy(_fakeClip);
            base.TearDown();
        }

        private static IEnumerator WaitFor(Func<bool> condition, float timeout = 3f)
        {
            var deadline = Time.realtimeSinceStartup + timeout;
            while (!condition() && Time.realtimeSinceStartup < deadline) yield return null;
        }

        /// <summary>Cho clip đang chạy hiện khung đầu rồi hết, chờ bộ phát rảnh.</summary>
        private IEnumerator FinishClip()
        {
            _backend.FirstFrameReady = true;
            yield return null;
            _backend.Finished = true;
            yield return WaitFor(() => !_clips.IsPlaying);
        }

        [UnityTest]
        public IEnumerator Keyword_AutoPlaysAfterOpeningRead()
        {
            var v = Bind("tv1_t1_b01", 1);
            yield return WaitFor(() => _backend.BeginCount > 0);
            Assert.AreEqual(1, _backend.BeginCount);
            Assert.AreEqual("img_b01_gaf_troongs", _clips.CurrentId);
            Assert.AreEqual("tu_of_os_o_o", Ctx.Speech.History.Last(), "clip phát sau khi đọc chữ");
            Assert.IsFalse(Done(v), "lần tự đọc không làm bước xong");
            Assert.IsNotNull(TileWithImage(v, "img_b01_gaf_troongs").GetComponentInChildren<ClipOverlay>(true));
        }

        [UnityTest]
        public IEnumerator Picture_AutoPlaysAfterOpeningRead()
        {
            Bind("tv1_t1_b01", 3);
            yield return WaitFor(() => _backend.BeginCount > 0);
            Assert.AreEqual("img_b01_chumf_nho", _clips.CurrentId);
        }

        [UnityTest]
        public IEnumerator Keyword_OpeningInterruptedByTextTap_PlaysAfterThatRead()
        {
            var v = Bind("tv1_t1_b01", 1);
            TileWithText(v, "ò ó o... o!").SimulateTap(); // cắt ngang lần tự đọc ngay trong khung đầu
            yield return WaitCompleted(v);
            yield return WaitFor(() => _backend.BeginCount > 0);
            Assert.AreEqual(1, _backend.BeginCount, "lần đọc trọn đầu tiên (do chạm chữ) cho clip tự phát");
            Assert.AreEqual(2, Ctx.Speech.History.Count(id => id == "tu_of_os_o_o"));
            yield return new WaitForSeconds(.3f);
            Assert.AreEqual(1, _backend.BeginCount);
        }

        [UnityTest]
        public IEnumerator Keyword_AfterAutoPlay_TextTapDoesNotPlay_PictureTapDoes()
        {
            var v = Bind("tv1_t1_b01", 1);
            yield return WaitFor(() => _backend.BeginCount > 0);
            yield return FinishClip();

            TileWithText(v, "ò ó o... o!").SimulateTap();
            yield return WaitCompleted(v);
            yield return new WaitForSeconds(.3f);
            Assert.AreEqual(1, _backend.BeginCount, "chạm chữ chỉ đọc");

            TileWithImage(v, "img_b01_gaf_troongs").SimulateTap();
            yield return WaitFor(() => _backend.BeginCount > 1);
            Assert.AreEqual(2, _backend.BeginCount, "chạm tranh: đọc rồi xem lại clip");
            Assert.AreEqual("tu_of_os_o_o", Ctx.Speech.History.Last());
        }

        [UnityTest]
        public IEnumerator Keyword_PictureTapStillCompletesStep()
        {
            var v = Bind("tv1_t1_b01", 1);
            yield return WaitFor(() => _backend.BeginCount > 0);
            Assert.IsFalse(Done(v));
            TileWithImage(v, "img_b01_gaf_troongs").SimulateTap();
            yield return WaitCompleted(v);
            Assert.IsTrue(Done(v));
        }

        [UnityTest]
        public IEnumerator Words_PlaysAfterWordRead()
        {
            var v = Bind("tv1_t1_b13", 8);
            yield return null;
            Assert.AreEqual(0, _backend.BeginCount, "mở bước words không tự phát");
            TileWithText(v, "đu đủ").SimulateTap();
            yield return CompleteOverlaySpell(v);
            yield return CompleteOverlaySpell(v);
            yield return WaitFor(() => _backend.BeginCount > 0);
            Assert.AreEqual("img_b13_ddu_ddur", _clips.CurrentId);
            Assert.AreEqual("tu_ddu_ddur", Ctx.Speech.History.Last());
            Assert.IsNotNull(TileWithImage(v, "img_b13_ddu_ddur").GetComponentInChildren<ClipOverlay>(true));
        }

        [UnityTest]
        public IEnumerator Riddle_CorrectAnswer_PlaysAnswerClip_CompletesWithoutWaiting()
        {
            var v = Bind("tv1_t2_b137", 7);
            yield return null;
            TileWithImage(v, "img_b137_cais_taayr").SimulateTap();
            yield return WaitCompleted(v);
            yield return WaitFor(() => _backend.BeginCount > 0);
            Assert.AreEqual("img_b137_cais_taayr", _clips.CurrentId);
            Assert.IsTrue(_clips.IsPlaying);
            Assert.IsTrue(Done(v), "bước xong không chờ clip");

            yield return FinishClip();
            TileWithImage(v, "img_b137_cais_taayr").SimulateTap();
            yield return WaitFor(() => _backend.BeginCount > 1);
            Assert.AreEqual(2, _backend.BeginCount, "đã xong: chạm tranh đáp án thì xem lại clip");
        }

        [UnityTest]
        public IEnumerator Riddle_WrongPicture_NoClip()
        {
            var v = Bind("tv1_t2_b137", 7);
            yield return null;
            TileWithImage(v, "img_b137_cais_thuwowcs").SimulateTap();
            yield return new WaitForSeconds(.5f);
            Assert.AreEqual(0, _backend.BeginCount);
        }

        [UnityTest]
        public IEnumerator ToneAttach_PlaysAfterPictureShown()
        {
            var v = Bind("tv1_t1_b04", 3);
            yield return WaitPracticeReady(v);
            Assert.AreEqual(0, _backend.BeginCount);
            DragWithText(v, "ˋ").SimulateDropOn(ResultSlot(v));
            yield return WaitCompleted(v);
            yield return WaitFor(() => _backend.BeginCount > 0);
            Assert.AreEqual("img_b04_caf", _clips.CurrentId);

            yield return FinishClip();
            TileWithImage(v, "img_b04_caf").SimulateTap();
            yield return WaitFor(() => _backend.BeginCount > 1);
            Assert.AreEqual(2, _backend.BeginCount);
        }

        [UnityTest]
        public IEnumerator NoClipsOnContext_ViewsBehaveAsBefore()
        {
            Ctx.Clips = null;
            var v = Bind("tv1_t1_b01", 1);
            yield return new WaitForSeconds(.2f);
            TileWithImage(v, "img_b01_gaf_troongs").SimulateTap();
            yield return WaitCompleted(v);
            Assert.AreEqual(0, _backend.BeginCount);
        }
    }
}
