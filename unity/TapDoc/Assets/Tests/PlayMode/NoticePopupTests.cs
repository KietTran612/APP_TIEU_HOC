using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>Popup "Gửi phụ huynh" (bản thiết kế màn mở đầu, cảnh báo, cài đặt mục 5.2): hiện một lần sau khởi động.</summary>
    public class NoticePopupTests : AppTestBase
    {
        private static string TextOf(NoticePopup popup) =>
            string.Join("\n", popup.GetComponentsInChildren<TMP_Text>(true).Select(t => t.text));

        [UnityTest]
        public IEnumerator FirstRun_ShowsNoticeOverProfiles()
        {
            NoticeSeen = false;
            UseStubsForMissingAssets();
            yield return LoadMain();
            var app = AppRoot.Instance;
            Assert.IsNotNull(app.Notice, "Lần đầu mở app phải có popup");
            Assert.IsTrue(app.Notice.IsOpen);
            Assert.AreEqual(UiText.NoticeAccept, app.Notice.CloseButton.GetComponentInChildren<TMP_Text>().text);
            var profiles = Object.FindAnyObjectByType<ProfileScreen>();
            Assert.IsNotNull(profiles, "Màn chọn bé nằm bên dưới popup");

            Canvas.ForceUpdateCanvases();
            var done = (RectTransform)profiles.DoneButton.transform;
            var point = RectTransformUtility.WorldToScreenPoint(app.UiCamera, done.TransformPoint(done.rect.center));
            var hits = new List<RaycastResult>();
            EventSystem.current.RaycastAll(new PointerEventData(EventSystem.current) { position = point }, hits);
            Assert.IsNotEmpty(hits);
            Assert.IsTrue(hits[0].gameObject.transform.IsChildOf(app.Notice.transform), "Chạm vào màn phía sau phải trúng popup");
        }

        [UnityTest]
        public IEnumerator Accept_SavesVersion_NotShownAgain()
        {
            NoticeSeen = false;
            UseStubsForMissingAssets();
            yield return LoadMain();
            var app = AppRoot.Instance;
            Press(app.Notice.CloseButton);
            yield return null;
            Assert.IsNull(app.Notice);
            Assert.AreEqual(UiText.NoticeVersion, app.Progress.NoticeVersion);
            Assert.AreEqual(UiText.NoticeVersion, ProgressStore.Load(StorePath).NoticeVersion, "Đã ghi xuống file");

            yield return DestroyApp();
            yield return LoadMainKeepingStore();
            Assert.IsNull(AppRoot.Instance.Notice, "Lần mở sau không hiện lại");
        }

        [UnityTest]
        public IEnumerator Notice_DoubleTap_ClosesOnce()
        {
            NoticeSeen = false;
            UseStubsForMissingAssets();
            yield return LoadMain();
            var app = AppRoot.Instance;
            var popup = app.Notice;
            var closed = 0;
            popup.Closed += () => closed++;
            popup.CloseButton.onClick.Invoke();
            popup.CloseButton.onClick.Invoke();
            yield return null;
            Assert.AreEqual(1, closed, "Chỉ đóng một lần");
            Assert.IsNull(app.Notice);
            Assert.IsEmpty(Object.FindObjectsByType<NoticePopup>(FindObjectsSortMode.None));
        }

        [UnityTest]
        public IEnumerator OldFile_NoNoticeVersion_ShowsNoticeKeepsProfiles()
        {
            NoticeSeen = false;
            UseStubsForMissingAssets();
            File.WriteAllText(StorePath,
                "{\"schema\":1,\"profiles\":[{\"id\":\"a\",\"name\":\"Na\",\"avatar\":\"img_chung_avatar_01\",\"lessons\":[],\"mistakes\":[]}],\"current\":\"a\",\"sfx_off\":false}");
            yield return LoadMainKeepingStore();
            var app = AppRoot.Instance;
            Assert.IsNotNull(app.Notice, "File cũ chưa có phiên bản cảnh báo: hiện popup một lần");
            Assert.IsNotNull(Object.FindAnyObjectByType<ProfileScreen>().ButtonForProfile("a"), "Hồ sơ cũ vẫn còn");
        }

        [UnityTest]
        public IEnumerator Notice_Text_HasOwnerWarnings()
        {
            NoticeSeen = false;
            UseStubsForMissingAssets();
            yield return LoadMain();
            var text = TextOf(AppRoot.Instance.Notice);
            foreach (var must in new[]
                     {
                         UiText.NoticeTitle, "chỉ mang tính chất tham khảo", "không dựa hoàn toàn vào một nguồn sách nào",
                         "không cổ xúy", "không liên quan đến bất kỳ cá nhân, tổ chức nào", "có thể chưa chuẩn",
                         "chỉ được lưu trên máy này"
                     })
            {
                StringAssert.Contains(must, text);
            }
            StringAssert.DoesNotContain("1996", text);
            StringAssert.DoesNotContain("quảng cáo", text);
        }

        [UnityTest]
        public IEnumerator Notice_FitsAllSizes()
        {
            NoticeSeen = false;
            UseStubsForMissingAssets();
            yield return LoadMain();
            var app = AppRoot.Instance;
            foreach (var size in ScreenSizes.All)
            {
                var rt = ScreenSizes.Apply(app, size);
                yield return null;
                Canvas.ForceUpdateCanvases();
                ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.Name}/app_notice.png");
                LayoutProbe.AssertFits(app.Canvas);
                ScreenSizes.Reset(app, rt);
            }
        }
    }
}
