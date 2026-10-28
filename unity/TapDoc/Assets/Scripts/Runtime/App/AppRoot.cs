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

        public Camera UiCamera { get; private set; }
        public Canvas Canvas { get; private set; }
        public SpeechPlayer Speech { get; private set; }
        public AssetCatalog Assets { get; private set; }
        public RectTransform SafeRoot { get; private set; }

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
            app.ShowLessonList();
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
        }

        public void ShowLessonList()
        {
            InitIfNeeded();
            Speech.Stop();
            ClearCurrentScreen();

            var go = new GameObject("LessonListScreen", typeof(RectTransform), typeof(LessonListScreen));
            go.transform.SetParent(SafeRoot, false);
            Stretch(go.GetComponent<RectTransform>());
            _currentScreen = go;
            go.GetComponent<LessonListScreen>().Build(this);
        }

        public void ShowLesson(string lessonId)
        {
            var lesson = LessonRepository.Load(lessonId);
            ShowLesson(lesson);
        }

        public void ShowLesson(Lesson lesson)
        {
            InitIfNeeded();
            Speech.Stop();
            ClearCurrentScreen();

            var go = new GameObject("LessonScreen", typeof(RectTransform), typeof(LessonScreen));
            go.transform.SetParent(SafeRoot, false);
            Stretch(go.GetComponent<RectTransform>());
            _currentScreen = go;
            go.GetComponent<LessonScreen>().Build(this, lesson);
        }

        public void ShowResult(string lessonId)
        {
            InitIfNeeded();
            Speech.Stop();
            ClearCurrentScreen();

            var go = new GameObject("ResultScreen", typeof(RectTransform), typeof(ResultScreen));
            go.transform.SetParent(SafeRoot, false);
            Stretch(go.GetComponent<RectTransform>());
            _currentScreen = go;
            go.GetComponent<ResultScreen>().Build(this, lessonId);
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
