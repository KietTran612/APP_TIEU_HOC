using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// 7 tiếng mới của nâng cấp UI (hd_chao_be, hd_cung_hoc, hd_nghi_mat, khen_*): phát đúng màn, đúng lúc, và không bị
    /// màn kế cắt ngang ngay. Kiểm bằng tiếng thật (gói media); máy chưa có file thì bỏ qua.
    /// </summary>
    public class GuideVoiceTests : AppTestBase
    {
        private const string LessonId = "tv1_t1_b01";

        private static void NeedAudio(params string[] ids)
        {
            foreach (var id in ids)
                Assume.That(AppRoot.Instance.Assets.Audio(id), Is.Not.Null, $"Chưa có tiếng {id} (gói media)");
        }

        /// <summary>Tiếng <paramref name="id"/> vừa phát và vẫn đang phát sau vài khung hình (không bị cắt ngang).</summary>
        private static IEnumerator AssertStillPlaying(string id, string where)
        {
            for (var i = 0; i < 5; i++) yield return null;
            var speech = AppRoot.Instance.Speech;
            Assert.AreEqual(id, speech.History.LastOrDefault(), $"{where}: phát {id}");
            Assert.IsTrue(speech.IsBusy, $"{where}: {id} không bị cắt ngang");
        }

        private static int Count(string id) => AppRoot.Instance.Speech.History.Count(h => h == id);

        [UnityTest]
        public IEnumerator Welcome_GreetsOnce_ThenCungHocOnShelf()
        {
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            NeedAudio(SystemAudio.hd_chao_be, SystemAudio.hd_cung_hoc);
            app.Speech.WaitScale = 1f;
            var before = Count(SystemAudio.hd_chao_be);
            var cungHoc = Count(SystemAudio.hd_cung_hoc); // LoadMainWithProfile đã chọn bé một lần
            app.ShowProfiles();
            yield return AssertStillPlaying(SystemAudio.hd_chao_be, "Vào màn chọn bé");
            Assert.AreEqual(before + 1, Count(SystemAudio.hd_chao_be), "Chào một lần khi vào màn");

            var s = Object.FindAnyObjectByType<ProfileScreen>();
            Press(s.NewChildButton);
            yield return null;
            Press(s.CancelButton);
            yield return null;
            Assert.AreEqual(before + 1, Count(SystemAudio.hd_chao_be), "Mở tạo bé rồi bấm Về: không chào lại");
            Assert.AreEqual(UiText.Greeting, s.Mascot.BubbleText, "Bong bóng chào vẫn hiện");

            Press(s.ProfileCards[0]);
            yield return null;
            Assert.IsNotNull(Object.FindAnyObjectByType<ShelfScreen>(), "Chọn bé xong vào Tủ sách");
            yield return AssertStillPlaying(SystemAudio.hd_cung_hoc, "Chọn bé xong");
            Assert.AreEqual(cungHoc + 1, Count(SystemAudio.hd_cung_hoc), "Chọn bé: rủ cùng học một lần");

            app.ShowProfiles();
            yield return AssertStillPlaying(SystemAudio.hd_chao_be, "Vào lại màn chọn bé");
            Assert.AreEqual(before + 2, Count(SystemAudio.hd_chao_be), "Mỗi lần vào màn chào một lần");
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator Break_PlaysNghiMat()
        {
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            NeedAudio(SystemAudio.hd_nghi_mat);
            app.Speech.WaitScale = 1f;
            app.ShowBreak(() => { });
            yield return AssertStillPlaying(SystemAudio.hd_nghi_mat, "Màn nghỉ mắt");
            Assert.AreEqual(SystemAudio.hd_nghi_mat, Object.FindAnyObjectByType<BreakScreen>().MascotAudio);
        }

        private static LessonEffort Effort(int[] roundMistakes, int replays)
        {
            var e = new LessonEffort();
            foreach (var m in roundMistakes) e.RecordRound(m);
            for (var i = 0; i < replays; i++) e.RecordReplay();
            return e;
        }

        [UnityTest]
        public IEnumerator Result_PraiseByEffort_PlaysMatchingVoice()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            NeedAudio(SystemAudio.Praise);
            app.Speech.WaitScale = 1f;
            app.Progress.RecordLessonDone(LessonId);
            Motion.Scale = 1f; // bật cảnh hoa bay để kiểm câu khen đến sau cảnh, không trước
            var cases = new (LessonEffort effort, string audio, string text, string how)[]
            {
                (Effort(new[] { 0, 1, 0 }, 0), SystemAudio.khen_tu_sua, UiText.PraiseSelfFix, "nhầm một lần rồi tự sửa"),
                (Effort(new[] { 0, 0 }, 2), SystemAudio.khen_nghe_lai, UiText.PraiseReplay, "bấm nghe lại"),
                (Effort(new[] { 0, 0, 0 }, 0), SystemAudio.khen_nghe_ki, UiText.PraiseAllRight, "không nhầm lượt nào"),
                (Effort(new[] { 2, 3 }, 0), SystemAudio.khen_cham, UiText.PraiseHardWork, "nhầm nhiều, vẫn làm xong"),
            };
            foreach (var c in cases)
            {
                app.LastEffort = c.effort;
                app.ShowResult(LessonId);
                yield return null;
                var result = Object.FindAnyObjectByType<ResultScreen>();
                Assert.IsNull(result.PraiseAudio, $"{c.how}: chưa khen khi cảnh hoa đang chạy");
                result.SkipScene();
                yield return AssertStillPlaying(c.audio, $"Xong bài, {c.how}");
                Assert.AreEqual(c.audio, result.PraiseAudio, c.how);
                Assert.AreEqual(c.text, result.Mascot.BubbleText, $"{c.how}: chữ trong bong bóng khớp tiếng");
            }
            LogAssert.NoUnexpectedReceived();
        }
    }
}
