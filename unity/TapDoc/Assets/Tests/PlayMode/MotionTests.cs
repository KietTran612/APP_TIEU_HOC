using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.TestTools;
using UnityEngine.UI;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>Bộ chạy hiệu ứng: nhảy tới cuối khi tắt, về đúng trạng thái cuối, huỷ theo kênh, an toàn khi bị huỷ.</summary>
    public class MotionTests
    {
        private GameObject _canvas;

        [SetUp]
        public void SetUp()
        {
            Motion.Scale = 1f;
            _canvas = new GameObject("MotionCanvas", typeof(RectTransform), typeof(Canvas));
        }

        [TearDown]
        public void TearDown()
        {
            Motion.Scale = 1f;
            if (_canvas != null) Object.Destroy(_canvas);
        }

        private RectTransform Box(Vector2 size)
        {
            var go = new GameObject("Box", typeof(RectTransform), typeof(Image));
            go.transform.SetParent(_canvas.transform, false);
            var rt = (RectTransform)go.transform;
            rt.sizeDelta = size;
            return rt;
        }

        private static IEnumerator Wait(Awaitable a)
        {
            while (!a.GetAwaiter().IsCompleted) yield return null;
        }

        [Test]
        public void ScaleZero_JumpsToEnd()
        {
            Motion.Scale = 0f;
            var rt = Box(new Vector2(100f, 100f));
            var move = Motion.MoveTo(rt, new Vector2(100f, 0f), 1f);
            Assert.IsTrue(move.GetAwaiter().IsCompleted, "Tắt hiệu ứng thì xong ngay trong khung hình");
            Assert.AreEqual(new Vector2(100f, 0f), rt.anchoredPosition);
            var scale = Motion.ScaleTo(rt, 1.5f, 1f);
            Assert.IsTrue(scale.GetAwaiter().IsCompleted);
            Assert.AreEqual(Vector3.one * 1.5f, rt.localScale);
        }

        [UnityTest]
        public IEnumerator Punch_ReturnsToOne()
        {
            var rt = Box(new Vector2(100f, 100f));
            yield return Wait(Motion.Punch(rt, 1.2f, .1f));
            Assert.That(Vector3.Distance(rt.localScale, Vector3.one), Is.LessThan(1e-4f));
        }

        [UnityTest]
        public IEnumerator NewAnimation_CancelsOld_EndsExact()
        {
            var rt = Box(new Vector2(100f, 100f));
            _ = Motion.ScaleTo(rt, 1.5f, .3f);
            yield return new WaitForSecondsRealtime(.05f);
            _ = Motion.ScaleTo(rt, 1f, .05f);
            yield return new WaitForSecondsRealtime(.4f);
            Assert.That(Vector3.Distance(rt.localScale, Vector3.one), Is.LessThan(1e-4f),
                "Hiệu ứng cũ bị huỷ, cỡ dừng đúng ở 1");
        }

        [UnityTest]
        public IEnumerator Shake_EndsAtStart()
        {
            var rt = Box(new Vector2(100f, 100f));
            rt.anchoredPosition = new Vector2(30f, 40f);
            yield return Wait(Motion.Shake(rt, 18f, .2f));
            Assert.AreEqual(new Vector2(30f, 40f), rt.anchoredPosition);
        }

        [UnityTest]
        public IEnumerator Wiggle_EndsUpright()
        {
            var rt = Box(new Vector2(100f, 100f));
            yield return Wait(Motion.Wiggle(rt, 3f, .2f));
            Assert.That(Mathf.Abs(Mathf.DeltaAngle(0f, rt.localEulerAngles.z)), Is.LessThan(1e-3f));
        }

        [UnityTest]
        public IEnumerator Fade_ReachesTarget()
        {
            var rt = Box(new Vector2(100f, 100f));
            var group = rt.gameObject.AddComponent<CanvasGroup>();
            group.alpha = 0f;
            yield return Wait(Motion.Fade(group, 1f, .1f));
            Assert.AreEqual(1f, group.alpha);
        }

        [UnityTest]
        public IEnumerator DestroyedTarget_NoException()
        {
            var rt = Box(new Vector2(100f, 100f));
            _ = Motion.MoveTo(rt, new Vector2(300f, 0f), .3f);
            _ = Motion.ScaleTo(rt, 2f, .3f);
            yield return null;
            Object.Destroy(rt.gameObject);
            yield return new WaitForSecondsRealtime(.4f);
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator PageTurn_KeepsLeftEdge_EndsFolded()
        {
            var rt = Box(new Vector2(400f, 300f));
            rt.anchoredPosition = new Vector2(50f, 20f);
            var corners = new Vector3[4];
            rt.GetWorldCorners(corners);
            var leftBefore = corners[0];
            var turn = Motion.PageTurn(rt, .2f);
            yield return new WaitForSecondsRealtime(.08f);
            rt.GetWorldCorners(corners);
            Assert.That(Vector3.Distance(corners[0], leftBefore), Is.LessThan(.01f), "Mép trái đứng yên trong lúc lật");
            Assert.Less(rt.localScale.x, 1f);
            yield return Wait(turn);
            Assert.AreEqual(0f, rt.localScale.x);
            rt.GetWorldCorners(corners);
            Assert.That(Vector3.Distance(corners[0], leftBefore), Is.LessThan(.01f));
        }

        [UnityTest]
        public IEnumerator PageTurn_HingeRight_KeepsRightEdge()
        {
            var rt = Box(new Vector2(400f, 300f));
            var corners = new Vector3[4];
            rt.GetWorldCorners(corners);
            var rightBefore = corners[3];
            var turn = Motion.PageTurn(rt, .2f, hingeLeft: false);
            yield return new WaitForSecondsRealtime(.08f);
            rt.GetWorldCorners(corners);
            Assert.That(Vector3.Distance(corners[3], rightBefore), Is.LessThan(.01f), "Lật lùi: mép phải đứng yên");
            yield return Wait(turn);
            Assert.AreEqual(0f, rt.localScale.x);
        }

        [UnityTest]
        public IEnumerator PageTurn_StretchedChild_KeepsLeftEdge()
        {
            // Trang thật (Root của bước, tờ sổ) là khung giãn theo cha, sizeDelta = 0.
            var parent = Box(new Vector2(400f, 300f));
            parent.anchoredPosition = new Vector2(-60f, 10f);
            var go = new GameObject("Page", typeof(RectTransform));
            go.transform.SetParent(parent, false);
            var page = (RectTransform)go.transform;
            page.anchorMin = Vector2.zero;
            page.anchorMax = Vector2.one;
            page.offsetMin = Vector2.zero;
            page.offsetMax = Vector2.zero;
            var corners = new Vector3[4];
            page.GetWorldCorners(corners);
            var leftBefore = corners[0];
            var turn = Motion.PageTurn(page, .2f);
            page.GetWorldCorners(corners);
            Assert.That(Vector3.Distance(corners[0], leftBefore), Is.LessThan(.01f), "Đổi pivot không được dịch trang");
            yield return Wait(turn);
            page.GetWorldCorners(corners);
            Assert.That(Vector3.Distance(corners[0], leftBefore), Is.LessThan(.01f), "Lật xong mép trái vẫn ở chỗ cũ");
        }

        [UnityTest]
        public IEnumerator Shake_Twice_EndsAtOriginalHome()
        {
            var rt = Box(new Vector2(100f, 100f));
            rt.anchoredPosition = new Vector2(30f, 40f);
            _ = Motion.Shake(rt, 18f, .3f);
            yield return new WaitForSecondsRealtime(.04f);
            Assert.AreNotEqual(new Vector2(30f, 40f), rt.anchoredPosition, "Đang lắc thì lệch khỏi chỗ");
            yield return Wait(Motion.Shake(rt, 18f, .3f));
            Assert.That(Vector2.Distance(rt.anchoredPosition, new Vector2(30f, 40f)), Is.LessThan(1e-3f),
                "Lắc lần hai vẫn về đúng chỗ ban đầu");
        }

        [UnityTest]
        public IEnumerator Pulse_StopRestoresScale()
        {
            var rt = Box(new Vector2(100f, 100f));
            Pulse.StartOn(rt);
            Assert.IsTrue(Pulse.IsRunning(rt));
            yield return new WaitForSecondsRealtime(.3f);
            Assert.AreNotEqual(Vector3.one, rt.localScale, "Đang nhún thì cỡ thay đổi");
            Pulse.StopOn(rt);
            Assert.IsFalse(Pulse.IsRunning(rt));
            Assert.AreEqual(Vector3.one, rt.localScale);
        }

        [UnityTest]
        public IEnumerator Pulse_StopRestoresScaleBeforePulse()
        {
            var rt = Box(new Vector2(100f, 100f));
            rt.localScale = Vector3.one * 1.1f; // thẻ đang được đọc tới thì phồng 1,1
            Pulse.StartOn(rt);
            yield return new WaitForSecondsRealtime(.3f);
            Pulse.StopOn(rt);
            Assert.That(Vector3.Distance(rt.localScale, Vector3.one * 1.1f), Is.LessThan(1e-4f),
                "Tắt nhún thì về cỡ trước khi nhún, không ép về 1");
        }

        [UnityTest]
        public IEnumerator Pulse_ScaleZero_StaysStill()
        {
            Motion.Scale = 0f;
            var rt = Box(new Vector2(100f, 100f));
            Pulse.StartOn(rt);
            yield return new WaitForSecondsRealtime(.3f);
            Assert.IsTrue(Pulse.IsRunning(rt));
            Assert.AreEqual(Vector3.one, rt.localScale, "Tắt hiệu ứng thì ảnh chụp ổn định");
        }

        [UnityTest]
        public IEnumerator TapFeedback_PressShrinks_ReleaseRestores()
        {
            var rt = Box(new Vector2(200f, 200f));
            var tap = rt.gameObject.AddComponent<TapFeedback>();
            var data = new PointerEventData(null);
            tap.OnPointerDown(data);
            yield return new WaitForSecondsRealtime(.15f);
            Assert.Less(rt.localScale.x, .95f, "Nhấn thì thẻ lún xuống");
            tap.OnPointerUp(data);
            yield return new WaitForSecondsRealtime(.2f);
            Assert.That(Vector3.Distance(rt.localScale, Vector3.one), Is.LessThan(1e-4f), "Thả thì thẻ về cỡ cũ");
        }

        private (TapFeedback tap, SfxPlayer sfx, SpeechPlayer speech) TapWithSound(float speechSeconds = 1f)
        {
            if (Object.FindAnyObjectByType<AudioListener>() == null) new GameObject("Listener", typeof(AudioListener)).transform.SetParent(_canvas.transform);
            var catalog = new AssetCatalog(id => AudioClip.Create(id, (int)(44100 * speechSeconds), 1, 44100, false), _ => null,
                id => AudioClip.Create(id, 441, 1, 44100, false));
            var audio = new GameObject("Audio");
            audio.transform.SetParent(_canvas.transform);
            var speech = audio.AddComponent<SpeechPlayer>();
            speech.Init(catalog);
            var sfx = new GameObject("Sfx").AddComponent<SfxPlayer>();
            sfx.transform.SetParent(_canvas.transform);
            sfx.Init(catalog, speech);
            var tap = Box(new Vector2(200f, 200f)).gameObject.AddComponent<TapFeedback>();
            tap.Sound = SystemSfx.Tap;
            return (tap, sfx, speech);
        }

        [UnityTest]
        public IEnumerator TapFeedback_SoundOnClick_SilentWhileSpeaking()
        {
            var (tap, sfx, speech) = TapWithSound();
            tap.OnPointerDown(new PointerEventData(null));
            CollectionAssert.IsEmpty(sfx.History, "Tiếng tách phát khi chạm xong (click), không phát lúc vừa nhấn");
            tap.OnPointerClick(new PointerEventData(null));
            CollectionAssert.AreEqual(new[] { SystemSfx.Tap }, sfx.History);
            _ = speech.PlayAsync("tieng_ca");
            yield return null;
            tap.OnPointerClick(new PointerEventData(null));
            Assert.AreEqual(1, sfx.History.Count, "Đang đánh vần hay đọc câu thì không có tiếng tách");
            speech.Stop();
        }

        [UnityTest]
        public IEnumerator TapFeedback_NoSoundAfterDragOrWhenDisabled()
        {
            var (tap, sfx, _) = TapWithSound();
            tap.OnPointerClick(new PointerEventData(null) { dragging = true });
            CollectionAssert.IsEmpty(sfx.History, "Cuộn danh sách bắt đầu trên thẻ không kêu");
            var button = tap.gameObject.AddComponent<Button>();
            button.interactable = false;
            tap.OnPointerDown(new PointerEventData(null));
            tap.OnPointerClick(new PointerEventData(null));
            CollectionAssert.IsEmpty(sfx.History, "Bài chưa mở (nút tắt) không kêu");
            Assert.AreEqual(Vector3.one, tap.transform.localScale, "Nút tắt không lún");
            yield return null;
        }

        [UnityTest]
        public IEnumerator Mascot_CheerTwice_HopsOnceAtATime()
        {
            var mascot = Mascot.Create(_canvas.transform, null);
            var body = (RectTransform)mascot.transform.Find("Body");
            mascot.Cheer(UiText.MascotCorrect);
            yield return new WaitForSecondsRealtime(.05f);
            mascot.Cheer(UiText.MascotCorrect);
            var lastY = body.anchoredPosition.y;
            var reversals = 0;
            var lastDir = 0;
            var deadline = Time.realtimeSinceStartup + .7f;
            while (Time.realtimeSinceStartup < deadline)
            {
                yield return null;
                var y = body.anchoredPosition.y;
                var dir = y > lastY + 1e-3f ? 1 : y < lastY - 1e-3f ? -1 : 0;
                if (dir != 0 && lastDir != 0 && dir != lastDir) reversals++;
                if (dir != 0) lastDir = dir;
                lastY = y;
            }
            Assert.LessOrEqual(reversals, 3, "Hai nhịp nhảy chỉ đổi chiều vài lần, không giật qua lại");
            Assert.That(body.anchoredPosition.magnitude, Is.LessThan(1e-3f), "Nhảy xong về đúng chỗ");
        }
    }
}
