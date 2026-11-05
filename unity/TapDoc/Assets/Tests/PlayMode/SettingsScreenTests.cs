using System.Collections;
using System.Linq;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>Menu Cài đặt (bản thiết kế màn mở đầu, cảnh báo, cài đặt mục 5.3).</summary>
    public class SettingsScreenTests : AppTestBase
    {
        private static SettingsScreen Settings() => Object.FindAnyObjectByType<SettingsScreen>();

        private static string Label(UnityEngine.UI.Button b) => b.GetComponentInChildren<TMP_Text>().text;

        private static Rect CanvasRect(RectTransform rt)
        {
            var corners = new Vector3[4];
            rt.GetWorldCorners(corners);
            var canvas = (RectTransform)AppRoot.Instance.Canvas.transform;
            Vector2 min = canvas.InverseTransformPoint(corners[0]), max = canvas.InverseTransformPoint(corners[2]);
            return Rect.MinMaxRect(min.x, min.y, max.x, max.y);
        }

        [UnityTest]
        public IEnumerator Gear_OnListAndProfiles_OpensSettings()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            var list = Object.FindAnyObjectByType<LessonListScreen>();
            Assert.AreEqual(SystemIcons.Settings, list.SettingsButton.GetComponent<IconButton>().IconId);
            Press(list.SettingsButton);
            yield return null;
            Assert.IsNotNull(Settings(), "Bánh răng ở danh sách bài mở Cài đặt");
            Press(Settings().BackButton);
            yield return null;
            Assert.IsNotNull(Object.FindAnyObjectByType<LessonListScreen>(), "Về thì quay lại danh sách bài");

            AppRoot.Instance.ShowProfiles();
            yield return null;
            Press(Object.FindAnyObjectByType<ProfileScreen>().SettingsButton);
            yield return null;
            Assert.IsNotNull(Settings(), "Bánh răng ở màn chọn bé mở Cài đặt");
            Press(Settings().BackButton);
            yield return null;
            Assert.IsNotNull(Object.FindAnyObjectByType<ProfileScreen>(), "Về thì quay lại màn chọn bé");
        }

        [UnityTest]
        public IEnumerator SfxToggle_SharesFlag()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            AppRoot.Instance.ShowSettings(AppRoot.Instance.ShowLessonList);
            yield return null;
            var toggle = Settings().SfxToggle;
            Assert.AreEqual(UiText.SfxOn, Label(toggle));
            Press(toggle);
            yield return null;
            Assert.AreEqual(UiText.SfxOff, Label(toggle));
            Assert.IsFalse(AppRoot.Instance.Progress.SfxEnabled);
            Assert.IsFalse(AppRoot.Instance.Sfx.Enabled, "Tắt thì không phát tiếng động nữa");
            Assert.IsFalse(ProgressStore.Load(StorePath).SfxEnabled, "Cài đặt được lưu");
            Press(toggle);
            Assert.IsTrue(AppRoot.Instance.Sfx.Enabled);
            Assert.AreEqual(UiText.SfxOn, Label(toggle));
        }

        [UnityTest]
        public IEnumerator ReviewNotice_OpensPopup_KeepsVersion()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            Assert.AreEqual(UiText.NoticeVersion, app.Progress.NoticeVersion);
            app.ShowSettings(app.ShowLessonList);
            yield return null;
            Press(Settings().ReviewNoticeButton);
            yield return null;
            Assert.IsNotNull(app.Notice);
            Assert.AreEqual(UiText.Close, Label(app.Notice.CloseButton), "Mở lại thì nút là Đóng");
            Press(app.Notice.CloseButton);
            yield return null;
            Assert.IsNull(app.Notice);
            Assert.AreEqual(UiText.NoticeVersion, app.Progress.NoticeVersion);
            Assert.IsNotNull(Settings(), "Đóng popup thì vẫn ở Cài đặt");
        }

        [UnityTest]
        public IEnumerator Info_ShowsVersionAndCredits()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            AppRoot.Instance.ShowSettings(AppRoot.Instance.ShowLessonList);
            yield return null;
            var info = Settings().InfoLabel.text;
            StringAssert.Contains(UiText.AppTitle, info);
            StringAssert.Contains(Application.version, info);
            StringAssert.Contains("Andika", info);
            StringAssert.Contains("CC0", info);
        }

        [UnityTest]
        public IEnumerator Settings_FromProfiles_NoChild_Works()
        {
            UseStubsForMissingAssets();
            yield return LoadMain();
            var app = AppRoot.Instance;
            Assert.AreEqual(0, app.Progress.Profiles.Count);
            Press(Object.FindAnyObjectByType<ProfileScreen>().SettingsButton);
            yield return null;
            var s = Settings();
            Press(s.SfxToggle);
            Press(s.ReviewNoticeButton);
            yield return null;
            Press(app.Notice.CloseButton);
            yield return null;
            Press(s.BackButton);
            yield return null;
            Assert.IsNotNull(Object.FindAnyObjectByType<ProfileScreen>());
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator Settings_FitsAllSizes()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            foreach (var size in ScreenSizes.All)
            {
                var rt = ScreenSizes.Apply(app, size);
                app.ShowLessonList();
                yield return null;
                Canvas.ForceUpdateCanvases();
                var list = Object.FindAnyObjectByType<LessonListScreen>();
                var gear = CanvasRect((RectTransform)list.SettingsButton.transform);
                foreach (var b in new[] { list.BookButton, list.ParentButton, list.SwitchChildButton })
                {
                    Assert.IsFalse(gear.Overlaps(CanvasRect((RectTransform)b.transform)), $"{size}: bánh răng đè nút {b.name}");
                }
                Assert.IsFalse(gear.Overlaps(CanvasRect(list.Header.rectTransform)), $"{size}: bánh răng đè tiêu đề");
                LayoutProbe.AssertFits(app.Canvas);

                app.ShowProfiles();
                yield return null;
                LayoutProbe.AssertFits(app.Canvas);

                app.ShowSettings(app.ShowLessonList);
                yield return null;
                ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.Name}/app_settings.png");
                LayoutProbe.AssertFits(app.Canvas);
                ScreenSizes.Reset(app, rt);
            }
        }

        /// <summary>Mở Cài đặt từ danh sách bài với 2 bé (A đang học, B), mở khoá nhóm quản lý hồ sơ.</summary>
        private IEnumerator OpenManageWithTwoChildren()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            var first = app.Progress.Current.id;
            app.Progress.CreateProfile("Bi", ProfileScreen.Avatars[1]); // tạo xong thì bé mới thành bé đang học
            app.Progress.Select(first);
            app.SaveProgress();
            app.ShowSettings(app.ShowLessonList);
            yield return null;
            Press(Settings().ManageButton);
            yield return null;
            Settings().GatePanel.SimulateUnlock();
            yield return null;
        }

        private static AppRoot App => AppRoot.Instance;
        private static string ChildA => App.Progress.Current.id;
        private static string ChildB => App.Progress.Profiles.First(p => p.id != App.Progress.Current.id).id;
        private static ConfirmDialog Dialog() => Object.FindAnyObjectByType<ConfirmDialog>();

        [UnityTest]
        public IEnumerator Locked_NoEditButtons_UntilGate()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            App.ShowSettings(App.ShowLessonList);
            yield return null;
            var s = Settings();
            Press(s.ManageButton);
            yield return null;
            Assert.IsNotNull(s.GatePanel, "Phải qua khoá phụ huynh");
            var id = App.Progress.Current.id;
            Assert.IsNull(s.DeleteButtonFor(id), "Chưa mở khoá thì chưa có nút xoá");
            Assert.IsNull(s.DeleteAllButton);
            s.GatePanel.SimulateUnlock();
            yield return null;
            Assert.IsNotNull(s.RenameButtonFor(id));
            Assert.IsNotNull(s.AvatarButtonFor(id));
            Assert.IsNotNull(s.DeleteButtonFor(id));
            Assert.IsNotNull(s.DeleteAllButton);
        }

        [UnityTest]
        public IEnumerator Rename_And_ChangeAvatar_Persist()
        {
            yield return OpenManageWithTwoChildren();
            var s = Settings();
            var id = ChildA;
            Press(s.RenameButtonFor(id));
            yield return null;
            s.EditNameInput.text = "Su";
            Press(s.EditAvatarChoice(ProfileScreen.Avatars[2]));
            Press(s.EditSaveButton);
            yield return null;
            var saved = ProgressStore.Load(StorePath).Profiles.First(p => p.id == id);
            Assert.AreEqual("Su", saved.name);
            Assert.AreEqual(ProfileScreen.Avatars[2], saved.avatar);
        }

        [UnityTest]
        public IEnumerator DeleteOtherChild_StaysInSettings()
        {
            yield return OpenManageWithTwoChildren();
            var s = Settings();
            var a = ChildA;
            Press(s.DeleteButtonFor(ChildB));
            yield return null;
            StringAssert.Contains("Bi", Dialog().Message.text);
            Press(Dialog().ConfirmButton);
            yield return null;
            Assert.AreEqual(1, App.Progress.Profiles.Count);
            Assert.AreEqual(a, App.Progress.Current.id, "Bé đang học giữ nguyên");
            Assert.IsNotNull(Settings(), "Vẫn ở Cài đặt");
            Assert.AreEqual(1, ProgressStore.Load(StorePath).Profiles.Count, "Đã lưu");
        }

        [UnityTest]
        public IEnumerator Settings_DeleteCurrentChild_BackGoesToProfiles()
        {
            yield return OpenManageWithTwoChildren();
            var s = Settings();
            Press(s.DeleteButtonFor(ChildA));
            yield return null;
            Press(Dialog().ConfirmButton);
            yield return null;
            Assert.IsNull(App.Progress.Current);
            Press(Settings().BackButton);
            yield return null;
            Assert.IsNotNull(Object.FindAnyObjectByType<ProfileScreen>());
            Assert.IsNull(Object.FindAnyObjectByType<LessonListScreen>());
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator DeleteProfile_Cancel_KeepsChild()
        {
            yield return OpenManageWithTwoChildren();
            Press(Settings().DeleteButtonFor(ChildB));
            yield return null;
            Press(Dialog().CancelButton);
            yield return null;
            Assert.AreEqual(2, App.Progress.Profiles.Count);
            Assert.IsNull(Dialog());
        }

        [UnityTest]
        public IEnumerator DeleteAll_TwoConfirms_ResetsLikeFreshInstall()
        {
            yield return OpenManageWithTwoChildren();
            System.IO.File.WriteAllText(StorePath + ".bak", "x");
            Press(Settings().DeleteAllButton);
            yield return null;
            Press(Dialog().ConfirmButton);
            yield return null;
            Assert.AreEqual(2, App.Progress.Profiles.Count, "Lần xác nhận thứ nhất chưa xoá");
            Assert.IsNotNull(Dialog(), "Hỏi lần thứ hai");
            StringAssert.Contains(UiText.DeleteAllConfirm2, Dialog().Message.text);
            Press(Dialog().ConfirmButton);
            yield return null;
            Assert.AreEqual(0, App.Progress.Profiles.Count);
            Assert.IsTrue(App.Progress.SfxEnabled);
            Assert.IsTrue(App.Sfx.Enabled);
            Assert.IsFalse(System.IO.File.Exists(StorePath + ".bak"));
            Assert.IsNotNull(App.Notice, "Như lúc mới cài: popup Gửi phụ huynh");
            Assert.AreEqual(UiText.NoticeAccept, Label(App.Notice.CloseButton));
            Assert.IsNotNull(Object.FindAnyObjectByType<ProfileScreen>(), "Bên dưới là màn tạo bé");
        }

        [UnityTest]
        public IEnumerator Manage_FitsAllSizes()
        {
            yield return OpenManageWithTwoChildren();
            App.Progress.CreateProfile("Đỗ Gia Bảo Ngọc", ProfileScreen.Avatars[3]);
            App.SaveProgress();
            foreach (var size in ScreenSizes.All)
            {
                var rt = ScreenSizes.Apply(App, size);
                App.ShowSettings(App.ShowLessonList);
                yield return null;
                Press(Settings().ManageButton);
                yield return null;
                LayoutProbe.AssertFits(App.Canvas);
                Settings().GatePanel.SimulateUnlock();
                yield return null;
                Canvas.ForceUpdateCanvases();
                ScreenProbe.Save(App.UiCamera, $"TestOutput/screens/{size.Name}/app_settings_manage.png");
                LayoutProbe.AssertFits(App.Canvas);
                Press(Settings().RenameButtonFor(ChildA));
                yield return null;
                ScreenProbe.Save(App.UiCamera, $"TestOutput/screens/{size.Name}/app_settings_edit.png");
                LayoutProbe.AssertFits(App.Canvas);
                ScreenSizes.Reset(App, rt);
            }
        }
    }
}
