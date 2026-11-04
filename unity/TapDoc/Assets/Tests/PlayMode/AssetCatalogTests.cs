using System.Collections;
using System.Collections.Generic;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    /// <summary>
    /// <see cref="AssetCatalog"/> trên nguồn giả: nạp theo bộ, mỗi mã nạp một lần, đếm chỗ giữ và nhả khi về 0,
    /// bộ chung không bao giờ nhả, báo thiếu file như cũ, cảnh báo khi màn hỏi thứ chưa chuẩn bị.
    /// </summary>
    public class AssetCatalogTests
    {
        private FakeContentSource _source;
        private AssetCatalog _catalog;

        [SetUp]
        public void SetUp()
        {
            _source = new FakeContentSource();
            _catalog = new AssetCatalog(_source);
        }

        private static (ContentKind, string)[] Ids(params (ContentKind, string)[] ids) => ids;

        private IEnumerator Prepare(IEnumerable<(ContentKind, string)> ids, System.Action<ContentSet> done) =>
            AwaitableTestUtil.Wait(_catalog.PrepareAsync(ids), done);

        /// <summary>Nguồn có đủ mọi mã của bộ chung (tranh, âm thanh, tiếng động, font).</summary>
        private void FillCommon()
        {
            var sprite = FakeContentSource.NewSprite();
            var clip = FakeContentSource.NewClip();
            foreach (var id in SystemImages.All) _source.Put(ContentKind.Image, id, sprite);
            foreach (var id in ProfileScreen.Avatars) _source.Put(ContentKind.Image, id, sprite);
            foreach (var id in SystemAudio.All) _source.Put(ContentKind.Speech, id, clip);
            foreach (var id in SystemSfx.All) _source.Put(ContentKind.Sfx, id, clip);
            _source.Put(ContentKind.Font, FontProvider.MainFontId, Font.CreateDynamicFontFromOSFont("Arial", 16));
        }

        [UnityTest]
        public IEnumerator Prepare_LoadsEachIdOnce_EvenWhenTwoSetsHoldIt()
        {
            _source.Put(ContentKind.Image, "img_a", FakeContentSource.NewSprite());
            yield return Prepare(Ids((ContentKind.Image, "img_a")), null);
            yield return Prepare(Ids((ContentKind.Image, "img_a"), (ContentKind.Image, "img_a")), null);
            Assert.AreEqual(1, _source.LoadCount(ContentKind.Image, "img_a"));
            Assert.IsNotNull(_catalog.Image("img_a"));
            Assert.IsEmpty(_catalog.UnpreparedAsks);
        }

        [UnityTest]
        public IEnumerator Dispose_ReleasesAtZero()
        {
            _source.Put(ContentKind.Image, "img_a", FakeContentSource.NewSprite());
            ContentSet first = null, second = null;
            yield return Prepare(Ids((ContentKind.Image, "img_a")), s => first = s);
            yield return Prepare(Ids((ContentKind.Image, "img_a")), s => second = s);

            first.Dispose();
            Assert.AreEqual(0, _source.ReleaseCount(ContentKind.Image, "img_a"));
            second.Dispose();
            Assert.AreEqual(1, _source.ReleaseCount(ContentKind.Image, "img_a"));
            second.Dispose();
            first.Dispose();
            Assert.AreEqual(1, _source.ReleaseCount(ContentKind.Image, "img_a"));
        }

        [UnityTest]
        public IEnumerator CommonSet_NeverReleased_EvenIfLessonSetHasSameId()
        {
            FillCommon();
            yield return AwaitableTestUtil.Wait(_catalog.PrepareCommonAsync());
            ContentSet lesson = null;
            yield return Prepare(Ids((ContentKind.Speech, SystemAudio.hd_nghe_chon_tranh)), s => lesson = s);
            lesson.Dispose();

            Assert.AreEqual(0, _source.ReleaseCount(ContentKind.Speech, SystemAudio.hd_nghe_chon_tranh));
            Assert.AreEqual(1, _source.LoadCount(ContentKind.Speech, SystemAudio.hd_nghe_chon_tranh));
            Assert.IsNotNull(_catalog.Audio(SystemAudio.hd_nghe_chon_tranh));
            Assert.IsNotNull(_catalog.Font(FontProvider.MainFontId));
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator Prepare_MissingFile_LogsOnceAndCompletes()
        {
            LogAssert.Expect(LogType.Error, "[TapDoc] Thiếu tranh: img_x");
            ContentSet set = null;
            yield return Prepare(Ids((ContentKind.Image, "img_x")), s => set = s);
            Assert.IsNotNull(set);
            Assert.IsNull(_catalog.Image("img_x"));
            Assert.IsNull(_catalog.Image("img_x"));
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator MissingSfx_IsWarning()
        {
            LogAssert.Expect(LogType.Warning, "[TapDoc] Thiếu tiếng động: sfx_x");
            yield return Prepare(Ids((ContentKind.Sfx, "sfx_x")), null);
            Assert.IsNull(_catalog.Sfx("sfx_x"));
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator OptionalAvatar_Missing_NoLog()
        {
            FillCommon();
            _source.Put(ContentKind.Image, ProfileScreen.Avatars[2], null);
            yield return AwaitableTestUtil.Wait(_catalog.PrepareCommonAsync());
            Assert.IsFalse(_catalog.HasImage(ProfileScreen.Avatars[2]));
            Assert.IsTrue(_catalog.HasImage(ProfileScreen.Avatars[0]));
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator UnpreparedAsk_StillReturns_WarnsOnce_Recorded()
        {
            _source.Put(ContentKind.Image, "img_b", FakeContentSource.NewSprite());
            LogAssert.Expect(LogType.Warning, "[TapDoc] Chưa chuẩn bị trước: img_b");
            Assert.IsNotNull(_catalog.Image("img_b"));
            Assert.IsNotNull(_catalog.Image("img_b"));
            CollectionAssert.Contains(_catalog.UnpreparedAsks, "img_b");
            Assert.AreEqual(1, _source.LoadCount(ContentKind.Image, "img_b"));
            LogAssert.NoUnexpectedReceived();
            yield return null;
        }

        [UnityTest]
        public IEnumerator UnpreparedAsk_CountsIntoCurrentHolder()
        {
            _source.Put(ContentKind.Image, "img_b", FakeContentSource.NewSprite());
            ContentSet holder = null;
            yield return Prepare(Ids(), s => holder = s);
            _catalog.CurrentHolder = holder;
            LogAssert.Expect(LogType.Warning, "[TapDoc] Chưa chuẩn bị trước: img_b");
            _catalog.Image("img_b");
            holder.Dispose();
            Assert.AreEqual(1, _source.ReleaseCount(ContentKind.Image, "img_b"));
        }

        [UnityTest]
        public IEnumerator PreparedAudio_IsLoaded()
        {
            _source.Put(ContentKind.Speech, "am_b", FakeContentSource.NewClip());
            yield return Prepare(Ids((ContentKind.Speech, "am_b")), null);
            Assert.AreEqual(AudioDataLoadState.Loaded, _catalog.Audio("am_b").loadState);
        }

        [UnityTest]
        public IEnumerator AudioAsync_CountsIntoHolder()
        {
            _source.Put(ContentKind.Speech, "am_b", FakeContentSource.NewClip());
            ContentSet holder = null;
            yield return Prepare(Ids(), s => holder = s);
            AudioClip clip = null;
            yield return AwaitableTestUtil.Wait(_catalog.AudioAsync("am_b", holder), c => clip = c);
            Assert.IsNotNull(clip);
            // Nạp lẻ có chờ: không cảnh báo, nhưng vẫn ghi lại là mã chưa được chuẩn bị trước.
            CollectionAssert.Contains(_catalog.UnpreparedAsks, "am_b");
            LogAssert.NoUnexpectedReceived();
            holder.Dispose();
            Assert.AreEqual(1, _source.ReleaseCount(ContentKind.Speech, "am_b"));
        }

        [UnityTest]
        public IEnumerator IsLoaded_OnlyAfterPrepared()
        {
            _source.Put(ContentKind.Speech, "am_b", FakeContentSource.NewClip());
            Assert.IsFalse(_catalog.IsLoaded(ContentKind.Speech, "am_b"));
            yield return Prepare(Ids((ContentKind.Speech, "am_b")), null);
            Assert.IsTrue(_catalog.IsLoaded(ContentKind.Speech, "am_b"));
        }

        [UnityTest]
        public IEnumerator Prepare_WaitsForSlowSource()
        {
            _source.Put(ContentKind.Image, "img_a", FakeContentSource.NewSprite());
            _source.DelayFrames = 3;
            var awaiter = _catalog.PrepareAsync(Ids((ContentKind.Image, "img_a"))).GetAwaiter();
            yield return null;
            Assert.IsFalse(awaiter.IsCompleted, "Bộ đã xong trước khi nguồn trả");
            for (var i = 0; i < 10 && !awaiter.IsCompleted; i++) yield return null;
            Assert.IsTrue(awaiter.IsCompleted);
            Assert.IsNotNull(awaiter.GetResult());
        }
    }
}
