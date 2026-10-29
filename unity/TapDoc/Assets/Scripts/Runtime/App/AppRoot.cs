using System;
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
        /// Móc cho test: tạo <see cref="AssetCatalog"/> với loader giả. <c>null</c> (mặc định, và luôn luôn
        /// trong app thật) nghĩa là dùng <c>new AssetCatalog()</c> nạp từ Resources; thiếu file thì catalog
        /// báo lỗi rõ trong Console, không có âm thanh hay tranh thay thế.
        /// </summary>
        internal static Func<AssetCatalog> CatalogFactory;

        /// <summary>
        /// Móc cho test: tạo kho tiến độ trỏ tới file tạm. <c>null</c> (mặc định, và luôn luôn trong app thật)
        /// nghĩa là dùng <see cref="ProgressStore.Default"/>.
        /// </summary>
        internal static Func<ProgressStore> StoreFactory;

        public Camera UiCamera { get; private set; }
        public Canvas Canvas { get; private set; }
        public SpeechPlayer Speech { get; private set; }
        public AssetCatalog Assets { get; private set; }
        public RectTransform SafeRoot { get; private set; }

        /// <summary>Hồ sơ bé và tiến độ học; <c>Progress.Current</c> là bé đang học.</summary>
        public ProgressStore Progress { get; private set; }

        private GameObject _currentScreen;

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
            var app = EnsureInstance();
            // Chưa có hồ sơ thì màn chọn bé mở thẳng phần tạo hồ sơ; có rồi thì cho chọn bé.
            app.ShowProfiles();
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
            UiCamera.backgroundColor = new Color(0.965f, 0.933f, 0.863f, 1f); // #F6EEDC
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
            bgImg.color = new Color(0.965f, 0.933f, 0.863f, 1f);
            bgImg.raycastTarget = false;

            SafeRoot = UiKit.CreateSafeArea(Canvas.transform);

            if (Object.FindAnyObjectByType<EventSystem>() == null)
            {
                var esGo = new GameObject("EventSystem", typeof(EventSystem), typeof(InputSystemUIInputModule));
                esGo.transform.SetParent(transform, false);
            }

            Assets = CatalogFactory != null ? CatalogFactory() : new AssetCatalog();
            var spGo = new GameObject("SpeechPlayer");
            spGo.transform.SetParent(transform, false);
            Speech = spGo.AddComponent<SpeechPlayer>();
            Speech.Init(Assets);

            Progress = StoreFactory != null ? StoreFactory() : ProgressStore.Default();
        }

        /// <summary>Màn chọn bé. Chưa có hồ sơ nào thì mở thẳng phần tạo hồ sơ.</summary>
        public void ShowProfiles()
        {
            Present<ProfileScreen>().Build(this);
        }

        /// <summary>Danh sách bài của bé đang học. Chưa chọn bé thì về màn chọn bé.</summary>
        public void ShowLessonList()
        {
            InitIfNeeded();
            if (Progress.Current == null)
            {
                ShowProfiles();
                return;
            }
            Present<LessonListScreen>().Build(this);
        }

        public void ShowLesson(string lessonId)
        {
            var lesson = LessonRepository.Load(lessonId);
            ShowLesson(lesson);
        }

        public void ShowLesson(Lesson lesson)
        {
            Present<LessonScreen>().Build(this, lesson);
        }

        /// <summary>
        /// Phiên "Ôn lại" của bé đang học: làm lại các lượt bé đã nhầm. Lượt lỗi thời bị xóa và lưu ngay.
        /// Không còn lượt nào để ôn thì về danh sách bài.
        /// </summary>
        public void ShowReview()
        {
            InitIfNeeded();
            var session = ReviewSession.Build(Progress, LessonRepository.Load);
            SaveProgress();
            if (session.Lesson.part2.Count == 0)
            {
                ShowLessonList();
                return;
            }
            Present<LessonScreen>().Build(this, session.Lesson, session);
        }

        public void ShowResult(string lessonId)
        {
            Present<ResultScreen>().Build(this, lessonId);
        }

        /// <summary>Màn phụ huynh: khóa phép tính trước, mở khóa xong mới xem tiến độ và chữ hay nhầm của từng bé.</summary>
        public void ShowParent()
        {
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

            var go = new GameObject(typeof(T).Name, typeof(RectTransform), typeof(T));
            go.transform.SetParent(SafeRoot, false);
            Stretch(go.GetComponent<RectTransform>());
            _currentScreen = go;
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
