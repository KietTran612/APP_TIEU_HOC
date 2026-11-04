using System;
using System.IO;
using System.Linq;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.InputSystem.UI;
using UnityEngine.SceneManagement;
using UnityEngine.UI;
using Object = UnityEngine.Object;

namespace TapDoc
{
    public class AppRoot : MonoBehaviour
    {
        private static bool _sceneHookRegistered;
        public static AppRoot Instance { get; private set; }

        /// <summary>
        /// Móc cho test: nguồn dữ liệu giả. <c>null</c> (mặc định, và luôn luôn trong app thật) nghĩa là đọc từ
        /// Resources (<see cref="ResourcesContentSource"/>); thiếu file thì catalog báo lỗi rõ trong Console, không có
        /// âm thanh hay tranh thay thế.
        /// </summary>
        internal static Func<IContentSource> SourceFactory;

        /// <summary>
        /// Móc cho test: tạo kho tiến độ trỏ tới file tạm. <c>null</c> (mặc định, và luôn luôn trong app thật)
        /// nghĩa là dùng <see cref="ProgressStore.Default"/>.
        /// </summary>
        internal static Func<ProgressStore> StoreFactory;

        public Camera UiCamera { get; private set; }
        public Canvas Canvas { get; private set; }
        public SpeechPlayer Speech { get; private set; }

        /// <summary>Kênh tiếng động khi tương tác, tách khỏi giọng đọc.</summary>
        public SfxPlayer Sfx { get; private set; }
        public AssetCatalog Assets { get; private set; }

        /// <summary>Kho bài: danh sách bài, bài học và Phụ lục, đọc qua cùng nguồn dữ liệu với <see cref="Assets"/>.</summary>
        public LessonRepository Lessons { get; private set; }
        public RectTransform SafeRoot { get; private set; }

        /// <summary>Hồ sơ bé và tiến độ học; <c>Progress.Current</c> là bé đang học.</summary>
        public ProgressStore Progress { get; private set; }

        /// <summary>Màn chuyển phủ lên trong lúc chuẩn bị bài, ôn lại, màn Phụ huynh.</summary>
        public PrepareCurtain Curtain { get; private set; }

        /// <summary><c>true</c> trong lúc đang chuẩn bị một màn; mọi lời mở màn có chuẩn bị khác bị bỏ qua.</summary>
        public bool IsPreparing { get; private set; }

        private GameObject _currentScreen;
        private IContentSource _source;

        /// <summary>Bộ tranh, âm thanh của màn hiện tại (bài, ôn lại, Phụ huynh); bộ chung nằm riêng trong catalog.</summary>
        private ContentSet _currentSet;

        private const float ScreenFadeSeconds = .25f;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
        private static void OnAfterSceneLoad()
        {
            if (!_sceneHookRegistered)
            {
                _sceneHookRegistered = true;
                SceneManager.sceneLoaded += OnSceneLoaded;
            }
            TryBootMainScene(SceneManager.GetActiveScene());
        }

        private static void OnSceneLoaded(Scene scene, LoadSceneMode mode)
        {
            TryBootMainScene(scene);
        }

        private static void TryBootMainScene(Scene scene)
        {
            if (scene.name != "Main") return;
            _ = EnsureInstance().BootAsync();
        }

        /// <summary><c>true</c> khi đã nạp xong bộ chung, danh sách bài và Phụ lục (khởi động xong).</summary>
        public bool IsReady { get; private set; }

        /// <summary>Nạp bộ chung, danh sách bài và Phụ lục của sách rồi mới hiện màn chọn bé.</summary>
        private async Awaitable BootAsync()
        {
            try
            {
                await Assets.PrepareCommonAsync();
                if (this == null) return;
                var index = await Lessons.LoadIndexAsync();
                if (this == null) return;
                if (index.lessons.Count > 0) await Lessons.LoadAppendixAsync(index.lessons[0].book);
                if (this == null) return;
            }
            catch (Exception ex)
            {
                Debug.LogError($"[TapDoc] Không khởi động được: {ex.Message}");
                return;
            }
            IsReady = true;
            // Chưa có hồ sơ thì màn chọn bé mở thẳng phần tạo hồ sơ; có rồi thì cho chọn bé.
            ShowProfiles();
        }

        public static AppRoot EnsureInstance()
        {
            if (Instance != null) return Instance;
            var existing = Object.FindAnyObjectByType<AppRoot>();
            if (existing != null)
            {
                Instance = existing;
                existing.InitIfNeeded();
                return existing;
            }

            var go = new GameObject("AppRoot");
            var root = go.AddComponent<AppRoot>();
            root.InitIfNeeded();
            return root;
        }

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }
            Instance = this;
            InitIfNeeded();
        }

        private void OnDestroy()
        {
            if (Instance == this)
            {
                Instance = null;
            }
        }

        private void InitIfNeeded()
        {
            if (Canvas != null) return;

            StepViewRegistry.RegisterAll();

            var camGo = new GameObject("UiCamera");
            camGo.transform.SetParent(transform, false);
            camGo.transform.position = new Vector3(0f, 0f, -10f);
            UiCamera = camGo.AddComponent<Camera>();
            UiCamera.clearFlags = CameraClearFlags.SolidColor;
            UiCamera.backgroundColor = Palette.Paper;
            UiCamera.orthographic = true;
            UiCamera.orthographicSize = 5f;
            // AudioListener nằm trên camera giao diện (SpeechPlayer không tự tạo listener).
            if (Object.FindAnyObjectByType<AudioListener>() == null)
            {
                camGo.AddComponent<AudioListener>();
            }

            Canvas = UiKit.CreateCanvas(UiCamera);
            Canvas.transform.SetParent(transform, false);

            var bgGo = new GameObject("Background", typeof(RectTransform), typeof(Image));
            bgGo.transform.SetParent(Canvas.transform, false);
            var bgRt = bgGo.GetComponent<RectTransform>();
            bgRt.anchorMin = Vector2.zero;
            bgRt.anchorMax = Vector2.one;
            bgRt.offsetMin = Vector2.zero;
            bgRt.offsetMax = Vector2.zero;
            var bgImg = bgGo.GetComponent<Image>();
            bgImg.sprite = UiKit.WhiteSprite;
            bgImg.color = Palette.Paper;
            bgImg.raycastTarget = false;

            SafeRoot = UiKit.CreateSafeArea(Canvas.transform);
            Curtain = PrepareCurtain.Create(SafeRoot);

            if (Object.FindAnyObjectByType<EventSystem>() == null)
            {
                var esGo = new GameObject("EventSystem", typeof(EventSystem), typeof(InputSystemUIInputModule));
                esGo.transform.SetParent(transform, false);
            }

            _source = SourceFactory?.Invoke() ?? new ResourcesContentSource();
            Assets = new AssetCatalog(_source);
            Lessons = new LessonRepository(_source);
            var spGo = new GameObject("SpeechPlayer");
            spGo.transform.SetParent(transform, false);
            Speech = spGo.AddComponent<SpeechPlayer>();
            Speech.Init(Assets);

            Progress = StoreFactory != null ? StoreFactory() : ProgressStore.Default();

            var sfxGo = new GameObject("SfxPlayer");
            sfxGo.transform.SetParent(transform, false);
            Sfx = sfxGo.AddComponent<SfxPlayer>();
            Sfx.Init(Assets, Speech);
            Sfx.Enabled = Progress.SfxEnabled;
        }

        /// <summary>Màn chọn bé. Chưa có hồ sơ nào thì mở thẳng phần tạo hồ sơ.</summary>
        public void ShowProfiles()
        {
            InitIfNeeded();
            ReleaseCurrentSet();
            Present<ProfileScreen>().Build(this);
        }

        /// <summary>Danh sách bài của bé đang học. Chưa chọn bé thì về màn chọn bé.</summary>
        public void ShowLessonList()
        {
            InitIfNeeded();
            ReleaseCurrentSet();
            if (Progress.Current == null)
            {
                ShowProfiles();
                return;
            }
            Present<LessonListScreen>().Build(this);
        }

        /// <summary>Mở bài: màn chuyển hiện, nạp bài cùng tranh, âm thanh của bài, nạp xong mới hiện màn bài.</summary>
        public void ShowLesson(string lessonId)
        {
            _ = OpenLessonAsync(null, async () => (await Lessons.LoadAsync(lessonId), null), lessonId);
        }

        public void ShowLesson(Lesson lesson)
        {
            _ = OpenLessonAsync(lesson, null, lesson?.lesson_id);
        }

        /// <summary>
        /// Phiên "Ôn lại" của bé đang học: làm lại các lượt bé đã nhầm. Lượt lỗi thời bị xóa và lưu ngay.
        /// Không còn lượt nào để ôn thì về danh sách bài.
        /// </summary>
        public void ShowReview()
        {
            InitIfNeeded();
            _ = OpenLessonAsync(null, LoadReviewAsync, ReviewSession.LessonId);
        }

        private async Awaitable<(Lesson, ReviewSession)> LoadReviewAsync()
        {
            // Nạp trước các bài có lượt cần ôn; bài hỏng hay không còn thì ReviewSession bỏ lượt đó.
            foreach (var lessonId in Progress.Mistakes(int.MaxValue).Select(m => m.lesson_id).Distinct().ToList())
            {
                try
                {
                    await Lessons.LoadAsync(lessonId);
                }
                catch (InvalidDataException)
                {
                }
            }
            var session = ReviewSession.Build(Progress, Lessons.Get);
            SaveProgress();
            return session.Lesson.part2.Count == 0 ? (null, null) : (session.Lesson, session);
        }

        /// <summary>
        /// Luồng chung của mở bài và ôn lại. Nạp lỗi (file bài thiếu hay hỏng) thì ở lại màn đang hiện, giữ bộ cũ.
        /// Bộ cũ chỉ được nhả sau khi bộ mới đã nạp xong, để những gì hai bài dùng chung không bị nhả rồi nạp lại.
        /// </summary>
        /// <param name="known">Bài đã có sẵn (không cần nạp); <c>null</c> thì lấy bài qua <paramref name="load"/>.</param>
        private async Awaitable OpenLessonAsync(Lesson known, Func<Awaitable<(Lesson, ReviewSession)>> load, string what)
        {
            InitIfNeeded();
            if (IsPreparing) return;
            IsPreparing = true;
            Curtain.Show();

            Lesson lesson;
            ReviewSession session;
            ContentSet set = null;
            try
            {
                (lesson, session) = known != null ? (known, null) : await load();
                if (this == null) return;
                if (lesson != null)
                {
                    set = await Assets.PrepareAsync(LessonAssets.ContentIds(lesson));
                    if (this == null)
                    {
                        set.Dispose();
                        return;
                    }
                }
            }
            catch (InvalidDataException ex)
            {
                if (this == null) return;
                Debug.LogError($"[TapDoc] Không mở được bài {what}: {ex.Message}");
                EndPreparing();
                return;
            }

            if (lesson == null)
            {
                EndPreparing();
                ShowLessonList(); // không còn lượt nào để ôn
                return;
            }
            Present<LessonScreen>().Build(this, lesson, session);
            HoldSet(set);
            EndPreparing();
        }

        private void EndPreparing()
        {
            Curtain.Hide();
            IsPreparing = false;
        }

        /// <summary>Giữ <paramref name="set"/> làm bộ hiện tại; nhả bộ cũ rồi nhờ nguồn dọn.</summary>
        private void HoldSet(ContentSet set)
        {
            var old = _currentSet;
            _currentSet = set;
            Assets.CurrentHolder = set;
            if (old == null) return;
            old.Dispose();
            _source.ReleaseUnused();
        }

        private void ReleaseCurrentSet() => HoldSet(null);

        public void ShowResult(string lessonId)
        {
            Present<ResultScreen>().Build(this, lessonId);
        }

        /// <summary>Màn Sổ bé ngoan của bé đang học. Chưa chọn bé thì về màn chọn bé.</summary>
        public void ShowBook()
        {
            InitIfNeeded();
            ReleaseCurrentSet();
            if (Progress.Current == null)
            {
                ShowProfiles();
                return;
            }
            Present<BookScreen>().Build(this);
        }

        /// <summary>Màn phụ huynh: khóa phép tính trước, mở khóa xong mới xem tiến độ và chữ hay nhầm của từng bé.</summary>
        public void ShowParent()
        {
            InitIfNeeded();
            ReleaseCurrentSet();
            Present<ParentScreen>().Build(this);
        }

        /// <summary>
        /// Ghi tiến độ xuống file. Lỗi đĩa (đầy, không ghi được) chỉ báo cảnh báo trong Console: app không dừng và
        /// bé không bị gián đoạn.
        /// </summary>
        public void SaveProgress()
        {
            try
            {
                Progress.Save();
            }
            catch (Exception ex) when (ex is System.IO.IOException || ex is UnauthorizedAccessException)
            {
                Debug.LogWarning($"[TapDoc] Không lưu được tiến độ: {ex.Message}");
            }
        }

        /// <summary>Dừng tiếng, bỏ màn đang hiện và tạo màn <typeparamref name="T"/> phủ kín vùng an toàn.</summary>
        private T Present<T>() where T : MonoBehaviour
        {
            InitIfNeeded();
            Speech.Stop();
            ClearCurrentScreen();

            var go = new GameObject(typeof(T).Name, typeof(RectTransform), typeof(CanvasGroup), typeof(T));
            go.transform.SetParent(SafeRoot, false);
            Stretch(go.GetComponent<RectTransform>());
            _currentScreen = go;
            // Màn mới mờ sang rõ (tắt hiệu ứng thì hiện ngay).
            var group = go.GetComponent<CanvasGroup>();
            group.alpha = 0f;
            _ = Motion.Fade(group, 1f, ScreenFadeSeconds);
            return go.GetComponent<T>();
        }

        private void ClearCurrentScreen()
        {
            if (_currentScreen != null)
            {
                _currentScreen.SetActive(false);
                Destroy(_currentScreen);
                _currentScreen = null;
            }
        }

        private static void Stretch(RectTransform rt)
        {
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
        }
    }
}
