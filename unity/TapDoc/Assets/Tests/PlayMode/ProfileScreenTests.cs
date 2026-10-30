using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>Màn chọn bé, danh sách bài có khóa và sao, ghi tiến độ khi học xong.</summary>
    public class ProfileScreenTests : AppTestBase
    {
        [UnityTest]
        public IEnumerator FirstRun_CreatesProfile()
        {
            yield return LoadMain();
            var ps = Object.FindAnyObjectByType<ProfileScreen>();
            Assert.IsNotNull(ps);
            ps.SimulateCreate("Bông", "img_chung_avatar_02");
            yield return null;
            Assert.IsNotNull(Object.FindAnyObjectByType<LessonListScreen>());
            Assert.AreEqual("Bông", AppRoot.Instance.Progress.Current.name);
        }

        [UnityTest]
        public IEnumerator EmptyName_CannotCreate()
        {
            yield return LoadMain();
            var ps = Object.FindAnyObjectByType<ProfileScreen>();
            ps.OpenCreate();
            ps.SetName("   ");
            ps.PickAvatar("img_chung_avatar_01");
            Assert.IsFalse(ps.DoneButton.interactable);
        }

        [UnityTest]
        public IEnumerator List_LocksAfterFirstIncomplete()
        {
            yield return LoadMainWithProfile();
            var list = Object.FindAnyObjectByType<LessonListScreen>();
            Assert.IsTrue(list.ButtonFor(Ordered()[0]).interactable);
            Assert.IsFalse(list.ButtonFor(Ordered()[1]).interactable);
            Assert.IsFalse(list.ReviewButton.interactable);
        }

        [UnityTest]
        public IEnumerator FinishingLesson_UnlocksNextAndRecordsMistake()
        {
            // Bài đầu danh sách có thể chưa có tranh, âm thanh (nhập ở Task 5): test này chỉ kiểm tra ghi tiến độ.
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            AppRoot.Instance.Speech.WaitScale = .02f;
            AppRoot.Instance.ShowLesson(Ordered()[0]);
            yield return null;
            var screen = Object.FindAnyObjectByType<LessonScreen>();
            // làm sai một lần ở lượt đầu Phần 2, rồi đi hết bài
            yield return WalkWithOneMistake(screen);
            Assert.IsTrue(AppRoot.Instance.Progress.IsUnlocked(Ordered(), Ordered()[1]));
            Assert.AreEqual(1, AppRoot.Instance.Progress.Mistakes().Count);
        }

        [UnityTest]
        public IEnumerator SwitchChild_KeepsProgressSeparate()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            var list = Object.FindAnyObjectByType<LessonListScreen>();
            Assert.IsTrue(list.ButtonFor(Ordered()[1]).interactable);
            Press(list.SwitchChildButton);
            yield return null;

            var ps = Object.FindAnyObjectByType<ProfileScreen>();
            Assert.IsNotNull(ps, "Nút Đổi bé không về màn chọn bé");
            Assert.That(LabelsUnder(ps), Has.Member(TestChildName));
            ps.SimulateCreate("Na", "img_chung_avatar_03");
            yield return null;

            list = Object.FindAnyObjectByType<LessonListScreen>();
            Assert.AreEqual("Na", AppRoot.Instance.Progress.Current.name);
            Assert.IsFalse(list.ButtonFor(Ordered()[1]).interactable, "Bé mới phải bắt đầu từ bài đầu");

            // Tiến độ đã ghi xuống file: mở lại app vẫn còn đủ hai bé.
            Assert.AreEqual(2, ProgressStore.Load(StorePath).Profiles.Count);
        }

        [UnityTest]
        public IEnumerator Screens_FitPhoneAndTablet()
        {
            // Danh sách có đủ ba kiểu thẻ: đã học (có sao), đang mở, bị khóa.
            yield return LoadMainWithProfile();
            AppRoot.Instance.Progress.MarkCompleted(Ordered()[0]);
            AppRoot.Instance.Progress.RecordMistake(Ordered()[0], 0);
            foreach (var size in new[] { new Vector2Int(2400, 1080), new Vector2Int(2048, 1536) })
            {
                var rt = new RenderTexture(size.x, size.y, 24);
                AppRoot.Instance.UiCamera.targetTexture = rt;
                var dir = $"TestOutput/screens/{size.x}x{size.y}";

                AppRoot.Instance.ShowLessonList();
                yield return null;
                Assert.IsTrue(Object.FindAnyObjectByType<LessonListScreen>().ReviewButton.interactable);
                ScreenProbe.Save(AppRoot.Instance.UiCamera, $"{dir}/app_lesson_list.png");
                LayoutProbe.AssertFits(AppRoot.Instance.Canvas);

                AppRoot.Instance.ShowProfiles();
                yield return null;
                ScreenProbe.Save(AppRoot.Instance.UiCamera, $"{dir}/app_profiles.png");
                LayoutProbe.AssertFits(AppRoot.Instance.Canvas);

                var ps = Object.FindAnyObjectByType<ProfileScreen>();
                ps.OpenCreate();
                ps.SetName("Bông");
                ps.PickAvatar(ProfileScreen.Avatars[2]);
                yield return null;
                ScreenProbe.Save(AppRoot.Instance.UiCamera, $"{dir}/app_profile_create.png");
                LayoutProbe.AssertFits(AppRoot.Instance.Canvas);

                AppRoot.Instance.UiCamera.targetTexture = null;
                Object.Destroy(rt);
            }
        }

        [UnityTest]
        public IEnumerator PickAvatar_HighlightsOrange()
        {
            yield return LoadMain();
            var ps = Object.FindAnyObjectByType<ProfileScreen>();
            ps.OpenCreate();
            ps.PickAvatar(ProfileScreen.Avatars[2]);
            yield return null;
            var picked = ps.AvatarFrame(ProfileScreen.Avatars[2]);
            var other = ps.AvatarFrame(ProfileScreen.Avatars[0]);
            Assert.That(Vector4.Distance(picked.color, Palette.Orange), Is.LessThan(1e-3f), "Hình đang chọn viền cam");
            Assert.That(Vector4.Distance(other.color, Palette.PaperLight), Is.LessThan(1e-3f));
        }

        [UnityTest]
        public IEnumerator ProfileCards_AreCardsWithTapSound()
        {
            yield return LoadMainWithProfile();
            AppRoot.Instance.ShowProfiles();
            yield return null;
            var ps = Object.FindAnyObjectByType<ProfileScreen>();
            var card = ps.ButtonForProfile(AppRoot.Instance.Progress.Profiles[0].id);
            Assert.AreEqual("Shadow", card.transform.GetChild(0).name, "Thẻ bé có bóng gạch chéo");
            Assert.AreEqual(SystemSfx.Tap, card.GetComponent<TapFeedback>().Sound);
            Assert.AreEqual(SystemSfx.Tap, ps.NewChildButton.GetComponent<TapFeedback>().Sound);
        }

        [UnityTest]
        public IEnumerator PickAvatar_StaysEnlarged_PreviousReturns()
        {
            yield return LoadMain();
            var ps = Object.FindAnyObjectByType<ProfileScreen>();
            ps.OpenCreate();
            ps.PickAvatar(ProfileScreen.Avatars[2]);
            yield return null;
            Assert.That(ps.AvatarFrame(ProfileScreen.Avatars[2]).transform.localScale.x, Is.EqualTo(ProfileScreen.PickedScale).Within(1e-3f));
            ps.PickAvatar(ProfileScreen.Avatars[0]);
            yield return null;
            Assert.That(ps.AvatarFrame(ProfileScreen.Avatars[0]).transform.localScale.x, Is.EqualTo(ProfileScreen.PickedScale).Within(1e-3f));
            Assert.That(ps.AvatarFrame(ProfileScreen.Avatars[2]).transform.localScale.x, Is.EqualTo(1f).Within(1e-3f));
        }
    }
}
