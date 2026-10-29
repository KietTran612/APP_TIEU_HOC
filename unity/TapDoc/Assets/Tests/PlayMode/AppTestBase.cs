using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;
using UnityEngine.UI;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// Lớp cơ sở cho test màn app. Mỗi test dùng một file tiến độ tạm (qua <see cref="AppRoot.StoreFactory"/>),
    /// xóa khi xong. Có sẵn các hàm mở app, đi hết bài và đọc chữ trên màn.
    /// </summary>
    public abstract class AppTestBase
    {
        protected const string TestChildName = "Bé thử";

        /// <summary>File tiến độ tạm của test này (trong <see cref="Path.GetTempPath"/>).</summary>
        protected string StorePath { get; private set; }

        private Texture2D _stubTex;
        private Sprite _stubSprite;
        private AudioClip _stubClip;

        [SetUp]
        public void SetUpProgressStore()
        {
            StorePath = Path.Combine(Path.GetTempPath(), $"tapdoc_app_test_{Guid.NewGuid():N}.json");
            var path = StorePath;
            AppRoot.StoreFactory = () => ProgressStore.Load(path);
        }

        [UnityTearDown]
        public IEnumerator TearDownApp()
        {
            yield return DestroyApp();
            AppRoot.StoreFactory = null;
            if (_stubSprite != null || _stubClip != null)
            {
                AppRoot.CatalogFactory = null;
                if (_stubSprite != null) Object.Destroy(_stubSprite);
                if (_stubTex != null) Object.Destroy(_stubTex);
                if (_stubClip != null) Object.Destroy(_stubClip);
                _stubSprite = null;
                _stubTex = null;
                _stubClip = null;
            }
            DeleteStoreFiles();
        }

        /// <summary>Dừng tiếng, trả RenderTexture của camera và hủy AppRoot (nếu còn), rồi chờ một khung hình.</summary>
        protected static IEnumerator DestroyApp()
        {
            var app = AppRoot.Instance;
            if (app != null)
            {
                if (app.Speech != null) app.Speech.Stop();
                var cam = app.UiCamera;
                if (cam != null && cam.targetTexture != null)
                {
                    var rt = cam.targetTexture;
                    cam.targetTexture = null;
                    Object.Destroy(rt);
                }
                Object.Destroy(app.gameObject);
            }
            yield return null;
        }

        /// <summary>Kho trống (chưa có hồ sơ nào), rồi nạp scene <c>Main</c>.</summary>
        protected IEnumerator LoadMain()
        {
            DeleteStoreFiles();
            yield return LoadMainScene();
        }

        /// <summary>
        /// Kho có sẵn một hồ sơ (<paramref name="unlockAll"/>: mọi bài trong danh sách đã học xong), nạp scene
        /// <c>Main</c>, chạm thẻ của bé ở màn chọn bé và chờ tới danh sách bài.
        /// </summary>
        protected IEnumerator LoadMainWithProfile(bool unlockAll = false)
        {
            DeleteStoreFiles();
            var store = new ProgressStore(StorePath);
            var profile = store.CreateProfile(TestChildName, ProfileScreen.Avatars[0]);
            if (unlockAll)
            {
                foreach (var id in Ordered()) store.MarkCompleted(id);
            }
            store.Save();

            yield return LoadMainScene();
            var ps = Object.FindAnyObjectByType<ProfileScreen>();
            Assert.IsNotNull(ps, "Khởi động không mở màn chọn bé");
            Press(ps.ButtonForProfile(profile.id));
            yield return null;
            Assert.IsNotNull(Object.FindAnyObjectByType<LessonListScreen>(), "Chọn bé xong mà không tới danh sách bài");
        }

        private static IEnumerator LoadMainScene()
        {
            SceneManager.LoadScene("Main");
            yield return null;
            yield return null;
            Assert.IsNotNull(AppRoot.Instance, "AppRoot chưa khởi động trong scene Main");
        }

        /// <summary>Mã bài theo thứ tự trong <c>index.json</c>.</summary>
        protected static string[] Ordered() =>
            LessonRepository.LoadIndex().lessons.Select(e => e.lesson_id).ToArray();

        /// <summary>Đi hết bài bằng <c>CompleteForTest</c>; ở mỗi màn gọi <paramref name="onView"/> trước khi làm xong màn đó.</summary>
        protected static IEnumerator WalkAll(LessonScreen s, Action<LessonScreen, int> onView = null) =>
            Walk(s, false, onView);

        /// <summary>Như <see cref="WalkAll"/>, nhưng ở lượt Phần 2 đầu tiên chọn một phương án sai trước.</summary>
        protected static IEnumerator WalkWithOneMistake(LessonScreen s) => Walk(s, true, null);

        private static IEnumerator Walk(LessonScreen screen, bool oneMistake, Action<LessonScreen, int> onView)
        {
            Assert.IsNotNull(screen, "Chưa có màn bài học");
            var n = 0;
            var mistakeDone = !oneMistake;
            while (screen != null && screen.Flow.Phase != Phase.Done)
            {
                yield return null;
                onView?.Invoke(screen, n++);
                if (!mistakeDone && screen.Flow.Phase == Phase.Part2)
                {
                    var round = screen.CurrentView as RoundViewBase;
                    Assert.IsNotNull(round, "Lượt Phần 2 đầu tiên không phải màn có phương án");
                    round.ActWrongForTest();
                    mistakeDone = true;
                    yield return new WaitForSeconds(.2f);
                }
                yield return ((ITestCompletable)screen.CurrentView).CompleteForTest();
                if (screen.Flow.Phase == Phase.Part1) screen.NextButton.onClick.Invoke();
                yield return new WaitForSeconds(.2f);
                screen = Object.FindAnyObjectByType<LessonScreen>();
            }
            Assert.IsTrue(mistakeDone, "Bài không có lượt Phần 2 nào để làm sai");
        }

        /// <summary>Mọi chữ <see cref="TMP_Text"/> bên trong <paramref name="c"/> (kể cả đang ẩn).</summary>
        protected static List<string> LabelsUnder(Component c) =>
            c.GetComponentsInChildren<TMP_Text>(true).Select(t => t.text).ToList();

        /// <summary>Bấm nút như bé chạm: nút phải đang hiện và bấm được.</summary>
        protected static void Press(Button button)
        {
            Assert.IsNotNull(button, "Không có nút");
            Assert.IsTrue(button.gameObject.activeInHierarchy, $"Nút '{button.name}' đang ẩn");
            Assert.IsTrue(button.interactable, $"Nút '{button.name}' không bấm được");
            button.onClick.Invoke();
        }

        /// <summary>
        /// Cho test chỉ kiểm tra luồng app, không kiểm tra tài nguyên. Tranh và âm thanh có thật thì nạp như app;
        /// chưa có (bài mới mà tài nguyên chưa nhập) thì thay bằng tranh trơn và clip ngắn, không báo thiếu.
        /// Gọi trước khi mở app.
        /// </summary>
        protected void UseStubsForMissingAssets()
        {
            _stubTex = new Texture2D(4, 4, TextureFormat.RGBA32, false);
            _stubSprite = Sprite.Create(_stubTex, new Rect(0, 0, 4, 4), new Vector2(.5f, .5f));
            _stubClip = AudioClip.Create("stub", 4410, 1, 44100, false);
            var sprite = _stubSprite;
            var clip = _stubClip;
            AppRoot.CatalogFactory = () => new AssetCatalog(
                id =>
                {
                    var real = Resources.Load<AudioClip>($"audio/{id}");
                    return real != null ? real : clip;
                },
                id =>
                {
                    var real = Resources.Load<Sprite>($"images/{id}");
                    return real != null ? real : sprite;
                });
        }

        private void DeleteStoreFiles()
        {
            if (string.IsNullOrEmpty(StorePath)) return;
            foreach (var f in new[] { StorePath, StorePath + ".tmp", StorePath + ".bak" })
            {
                if (File.Exists(f)) File.Delete(f);
            }
        }
    }
}
