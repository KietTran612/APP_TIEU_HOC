using System;
using System.Collections;
using System.Collections.Generic;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>Kênh tiếng động: tách khỏi giọng đọc, có công tắc, không cắt giọng đọc, thiếu file chỉ cảnh báo.</summary>
    public class SfxPlayerTests
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

        private (SfxPlayer sfx, SpeechPlayer speech) Make(Func<string, AudioClip> sfxLoader = null,
            float speechSeconds = .1f)
        {
            if (Object.FindAnyObjectByType<AudioListener>() == null)
            {
                _created.Add(new GameObject("TestAudioListener", typeof(AudioListener)));
            }
            var catalog = new AssetCatalog(
                id => AudioClip.Create(id, (int)(44100 * speechSeconds), 1, 44100, false),
                _ => null,
                sfxLoader ?? (id => AudioClip.Create(id, 2205, 1, 44100, false)));
            var go = new GameObject("TestAudio");
            _created.Add(go);
            var speech = go.AddComponent<SpeechPlayer>();
            speech.Init(catalog);
            var sfxGo = new GameObject("TestSfx");
            _created.Add(sfxGo);
            var sfx = sfxGo.AddComponent<SfxPlayer>();
            sfx.Init(catalog, speech);
            return (sfx, speech);
        }

        [Test]
        public void Enabled_PlaysAndRecords()
        {
            var (sfx, _) = Make();
            sfx.Play(SystemSfx.Correct);
            CollectionAssert.AreEqual(new[] { SystemSfx.Correct }, sfx.History);
            Assert.AreSame(sfx, SfxPlayer.Instance);
        }

        [Test]
        public void Disabled_PlaysNothing()
        {
            var (sfx, _) = Make();
            sfx.Enabled = false;
            sfx.Play(SystemSfx.Correct);
            sfx.PlayUnlessSpeaking(SystemSfx.Tap);
            CollectionAssert.IsEmpty(sfx.History);
        }

        [UnityTest]
        public IEnumerator PlayUnlessSpeaking_SkipsWhileBusy()
        {
            var (sfx, speech) = Make(speechSeconds: 1f);
            var talk = speech.PlayAsync("tieng_ca");
            yield return null;
            Assert.IsTrue(speech.IsBusy);
            sfx.PlayUnlessSpeaking(SystemSfx.Tap);
            CollectionAssert.IsEmpty(sfx.History);
            speech.Stop();
            sfx.PlayUnlessSpeaking(SystemSfx.Tap);
            CollectionAssert.AreEqual(new[] { SystemSfx.Tap }, sfx.History);
        }

        [UnityTest]
        public IEnumerator DoesNotInterruptSpeech()
        {
            var (sfx, speech) = Make(speechSeconds: 1f);
            var talk = speech.PlayAsync("tieng_ca");
            yield return null;
            sfx.Play(SystemSfx.Correct);
            yield return null;
            Assert.IsTrue(speech.IsBusy, "Giọng đọc vẫn đang phát");
            Assert.IsFalse(talk.GetAwaiter().IsCompleted, "Tiếng động không cắt giọng đọc");
            speech.Stop();
        }

        [Test]
        public void RejectsSpeechIds()
        {
            var (sfx, _) = Make();
            LogAssert.Expect(LogType.Error, "[TapDoc] Không phải mã tiếng động: tieng_ca");
            sfx.Play("tieng_ca");
            CollectionAssert.IsEmpty(sfx.History);
        }

        [Test]
        public void MissingClip_WarningOnly()
        {
            var (sfx, _) = Make(_ => null);
            LogAssert.Expect(LogType.Warning, "[TapDoc] Thiếu tiếng động: sfx_dung");
            sfx.Play(SystemSfx.Correct);
            LogAssert.NoUnexpectedReceived();
            CollectionAssert.AreEqual(new[] { SystemSfx.Correct }, sfx.History);
        }

        [Test]
        public void CatalogLoadsFromSfxFolderOnly()
        {
            var catalog = new AssetCatalog();
            LogAssert.Expect(LogType.Warning, "[TapDoc] Thiếu tiếng động: sfx_khong_co");
            Assert.IsNull(catalog.Sfx("sfx_khong_co"));
            // Mã giọng đọc có thật không nạp được qua kênh tiếng động (khác thư mục).
            LogAssert.Expect(LogType.Warning, "[TapDoc] Thiếu tiếng động: khen_01");
            Assert.IsNull(catalog.Sfx(SystemAudio.khen_01));
            Assert.IsNotNull(catalog.Audio(SystemAudio.khen_01));
        }
    }
}
