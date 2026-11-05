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
    }
}
