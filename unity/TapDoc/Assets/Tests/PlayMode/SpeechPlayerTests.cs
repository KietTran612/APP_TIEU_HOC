using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    public class SpeechPlayerTests
    {
        private readonly List<GameObject> _created = new();

        [TearDown]
        public void TearDown()
        {
            foreach (var go in _created)
            {
                if (go != null) Object.Destroy(go);
            }
            _created.Clear();
        }

        private SpeechPlayer Speech(Func<string, AudioClip> audioLoader = null)
        {
            // SpeechPlayer không tự tạo AudioListener; test tự đặt một cái nếu cảnh chưa có.
            if (Object.FindAnyObjectByType<AudioListener>() == null)
            {
                var listenerGo = new GameObject("TestAudioListener", typeof(AudioListener));
                _created.Add(listenerGo);
            }

            var go = new GameObject("TestSpeechPlayer");
            _created.Add(go);
            var sp = go.AddComponent<SpeechPlayer>();
            var loader = audioLoader ?? (id => AudioClip.Create(id, 4410, 1, 44100, false));
            sp.Init(new AssetCatalog(loader));
            return sp;
        }

        [UnityTest]
        public IEnumerator PlaySequence_CallsOnPartInOrder()
        {
            var sp = Speech();
            var calls = new List<int>();
            var t0 = Time.realtimeSinceStartup;
            var task = sp.PlaySequenceAsync(new[] { "a", "b", "c" }, calls.Add, .05f);
            yield return new WaitUntil(() => task.GetAwaiter().IsCompleted);
            CollectionAssert.AreEqual(new[] { 0, 1, 2 }, calls);
            Assert.GreaterOrEqual(Time.realtimeSinceStartup - t0, .39f);
        }

        [UnityTest]
        public IEnumerator Play_WhileSequencePlaying_StopsOldSequence()
        {
            var sp = Speech();
            var calls = new List<int>();
            _ = sp.PlaySequenceAsync(new[] { "a", "b", "c" }, calls.Add, .05f);
            yield return new WaitUntil(() => calls.Count == 1);
            var t = sp.PlayAsync("x");
            yield return new WaitUntil(() => t.GetAwaiter().IsCompleted);
            yield return new WaitForSeconds(.4f);
            CollectionAssert.AreEqual(new[] { 0 }, calls);
            Assert.AreEqual("x", sp.History.Last());
        }

        [UnityTest]
        public IEnumerator MissingClip_CompletesImmediately()
        {
            LogAssert.Expect(LogType.Error, "[TapDoc] Thiếu âm thanh: khong_co");
            var sp = Speech(id => null);
            var t0 = Time.realtimeSinceStartup;
            var t = sp.PlayAsync("khong_co");
            yield return new WaitUntil(() => t.GetAwaiter().IsCompleted);
            Assert.Less(Time.realtimeSinceStartup - t0, .1f);
        }

        [UnityTest]
        public IEnumerator Stop_ThenDestroy_NoErrors()
        {
            var sp = Speech();
            var calls = new List<int>();
            _ = sp.PlaySequenceAsync(new[] { "a", "b", "c" }, calls.Add, .05f);
            yield return null;
            sp.Stop();
            Object.Destroy(sp.gameObject);
            yield return new WaitForSeconds(.5f);
            Assert.LessOrEqual(calls.Count, 1);
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator PlayAsync_RunsToEnd_ReturnsTrue()
        {
            var sp = Speech();
            var t = sp.PlayAsync("a");
            yield return new WaitUntil(() => t.GetAwaiter().IsCompleted);
            Assert.IsTrue(t.GetAwaiter().GetResult());
            Assert.IsFalse(sp.IsBusy);
        }

        [UnityTest]
        public IEnumerator PlayAsync_Superseded_ReturnsFalse()
        {
            var sp = Speech(id => AudioClip.Create(id, 44100, 1, 44100, false)); // clip 1 s
            var first = sp.PlayAsync("a");
            Assert.IsFalse(first.GetAwaiter().IsCompleted);
            var second = sp.PlayAsync("b");
            yield return new WaitUntil(() => first.GetAwaiter().IsCompleted && second.GetAwaiter().IsCompleted);
            Assert.IsFalse(first.GetAwaiter().GetResult(), "Lần phát bị cắt ngang phải trả false");
            Assert.IsTrue(second.GetAwaiter().GetResult());
        }

        [UnityTest]
        public IEnumerator PlaySequenceAsync_Stopped_ReturnsFalse()
        {
            var sp = Speech();
            var t = sp.PlaySequenceAsync(new[] { "a", "b", "c" }, null, .05f);
            Assert.IsFalse(t.GetAwaiter().IsCompleted);
            sp.Stop();
            yield return new WaitUntil(() => t.GetAwaiter().IsCompleted);
            Assert.IsFalse(t.GetAwaiter().GetResult());
        }

        [UnityTest]
        public IEnumerator MissingClip_ReturnsTrue()
        {
            LogAssert.Expect(LogType.Error, "[TapDoc] Thiếu âm thanh: khong_co");
            var sp = Speech(id => null);
            var t = sp.PlayAsync("khong_co");
            Assert.IsTrue(t.GetAwaiter().IsCompleted, "Thiếu file thì xong ngay, không chờ khung hình");
            Assert.IsTrue(t.GetAwaiter().GetResult());
            yield return null;
        }
    }
}
