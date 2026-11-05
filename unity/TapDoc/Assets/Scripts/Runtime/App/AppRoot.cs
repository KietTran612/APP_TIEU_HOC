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
        /// <summary>Khung chuẩn 1440 trong vùng an toàn của máy: màn người lớn, màn chuẩn bị.</summary>
        public RectTransform SafeRoot { get; private set; }

        /// <summary>Khung các màn của bé: rộng hết vùng an toàn trên điện thoại, 1440 trên máy tính bảng.</summary>
        public RectTransform KidRoot { get; private set; }

        /// <summary>Các khung màn hiện tại, theo cỡ đích vẽ và lề an toàn của máy.</summary>
        public ScreenFrames Frames { get; private set; }

        /// <summary>Số lần đã đặt lại hai gốc màn (test dùng để biết cỡ không đổi thì không đặt lại).</summary>
        internal int FramesApplied { get; private set; }

        private bool _framesSet;

        /// <summary>Hồ sơ bé và tiến độ học; <c>Progress.Current</c> là bé đang học.</summary>
        public ProgressStore Progress { get; private set; }

        /// <summary>
        /// Màn chuyển phủ lên trong lúc chuẩn bị bài, ôn lại, màn Phụ huynh. Dựng lần đầu khi cần (sau khi bộ chung đã
        /// nạp, để hình gà con có sẵn).
        /// </summary>
        public PrepareCurtain Curtain => _curtain != null ? _curtain : _curtain = PrepareCurtain.Create(SafeRoot, Assets);

        private PrepareCurtain _curtain;

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
                // Mỗi quyển dùng Phụ lục ghi trong `books` (tập 2 dùng của tập 1); kho bài tự quy về một file.
                foreach (var book in index.lessons.Select(e => e.book).Where(b => !string.IsNullOrWhiteSpace(b)).Distinct())
                {
                    await Lessons.LoadAppendixAsync(book);
                    if (this == null) return;
                }
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

            KidRoot = CreateRoot("KidRoot");
            SafeRoot = CreateRoot("SafeArea");
            RefreshFrames();

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

        private void Update()
        {
            RefreshFrames();
        }

        /// <summary>
        /// Tính lại khung màn theo cỡ đích vẽ của camera giao diện và lề an toàn của máy; khác lần trước thì đặt lại
        /// hai gốc màn. Màn đang hiện không bị dựng lại: chúng neo theo gốc và tự chỉnh khi cỡ đổi.
        /// </summary>
        public void RefreshFrames()
        {
            if (UiCamera == null || KidRoot == null) return;
            var pixels = new Vector2Int(UiCamera.pixelWidth, UiCamera.pixelHeight);
            if (pixels.x <= 0 || pixels.y <= 0) return;
            var frames = ScreenLayout.Compute(pixels, DeviceSafeArea.For(pixels));
            if (_framesSet && frames.Same(Frames)) return;
            _framesSet = true;
            Frames = frames;
            Place(KidRoot, frames.Kid);
            Place(SafeRoot, frames.Standard);
            FramesApplied++;
        }

        private RectTransform CreateRoot(string name)
        {
            var go = new GameObject(name, typeof(RectTransform));
            go.transform.SetParent(Canvas.transform, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = rt.anchorMax = rt.pivot = Vector2.zero;
            return rt;
        }

        private static void Place(RectTransform root, Rect frame)
        {
            root.anchoredPosition = frame.position;
            root.sizeDelta = frame.size;
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
            _ = PrepareAndShowAsync(async () => await PrepareLessonAsync(await Lessons.LoadAsync(lessonId), null), "bài " + lessonId);
        }

        /// <summary>Như <see cref="ShowLesson(string)"/> với bài đã có sẵn (không cần nạp chữ).</summary>
        public void ShowLesson(Lesson lesson)
        {
            _ = PrepareAndShowAsync(() => PrepareLessonAsync(lesson, null), "bài " + lesson?.lesson_id);
        }

        /// <summary>
        /// Phiên "Ôn lại" của bé đang học: làm lại các lượt bé đã nhầm. Lượt lỗi thời bị xóa và lưu ngay.
        /// Không còn lượt nào để ôn thì về danh sách bài.
        /// </summary>
        public void ShowReview()
        {
            _ = PrepareAndShowAsync(PrepareReviewAsync, "phiên ôn lại");
        }

        /// <summary>
        /// Màn phụ huynh: khóa phép tính trước, mở khóa xong mới xem tiến độ và chữ hay nhầm của từng bé. Chuẩn bị chữ
        /// của mọi bài (Phụ lục và chữ hay nhầm cần); âm thanh chỉ nạp khi phụ huynh chạm vào, tính vào bộ của màn.
        /// </summary>
        public void ShowParent()
        {
            _ = PrepareAndShowAsync(async () =>
            {
                await Lessons.LoadAllAsync();
                var set = await Assets.PrepareAsync(Enumerable.Empty<(ContentKind, string)>());
                return (set, () => Present<ParentScreen>(kid: false).Build(this));
            }, "màn phụ huynh");
        }

        private async Awaitable<(ContentSet, Action)> PrepareLessonAsync(Lesson lesson, ReviewSession session)
        {
            var set = await Assets.PrepareAsync(LessonAssets.ContentIds(lesson));
            return (set, () => Present<LessonScreen>().Build(this, lesson, session));
        }

        private async Awaitable<(ContentSet, Action)> PrepareReviewAsync()
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
            if (session.Lesson.part2.Count == 0) return (null, ShowLessonList);
            return await PrepareLessonAsync(session.Lesson, session);
        }

        /// <summary>
        /// Luồng chung của các màn cần chuẩn bị (bài, ôn lại, phụ huynh): hiện màn chuyển, chạy
        /// <paramref name="prepare"/> (trả bộ đã giữ và hàm dựng màn), dựng màn rồi giữ bộ mới. Bộ cũ chỉ được nhả sau
        /// khi bộ mới đã nạp xong, để những gì hai bài dùng chung không bị nhả rồi nạp lại. Nạp lỗi (file bài thiếu
        /// hay hỏng) thì ở lại màn đang hiện, giữ bộ cũ. Đang chuẩn bị thì bỏ qua lời gọi mới.
        /// </summary>
        private async Awaitable PrepareAndShowAsync(Func<Awaitable<(ContentSet set, Action show)>> prepare, string what)
        {
            InitIfNeeded();
            if (IsPreparing) return;
            IsPreparing = true;
            Curtain.Show();

            (ContentSet set, Action show) prepared;
            try
            {
                prepared = await prepare();
            }
            catch (Exception ex)
            {
                if (this == null) return;
                Debug.LogError($"[TapDoc] Không mở được {what}: {ex.Message}");
                await EndPreparingAsync();
                return;
            }
            if (this == null)
            {
                prepared.set?.Dispose();
                return;
            }

            // Thứ màn mới hỏi lúc dựng mà chưa chuẩn bị thì tính vào bộ mới, không vào bộ cũ sắp bị nhả.
            if (prepared.set != null) Assets.CurrentHolder = prepared.set;
            try
            {
                prepared.show();
            }
            catch (Exception ex)
            {
                // Màn cũ đã bị thay: về danh sách bài để bé vẫn còn chỗ bấm.
                Debug.LogError($"[TapDoc] Không mở được {what}: {ex.Message}");
                prepared.set?.Dispose();
                ShowLessonList();
                await EndPreparingAsync();
                return;
            }
            if (prepared.set != null) HoldSet(prepared.set);
            await EndPreparingAsync();
        }

        /// <summary>Màn chuyển mờ ra (sau thời gian tối thiểu); xong mới nhận lời mở màn khác.</summary>
        private async Awaitable EndPreparingAsync()
        {
            await Curtain.HideAsync();
            if (this != null) IsPreparing = false;
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

        /// <summary>
        /// Dừng tiếng, bỏ màn đang hiện và tạo màn <typeparamref name="T"/> phủ kín khung của bé
        /// (<paramref name="kid"/>) hay khung chuẩn 1440 (màn người lớn).
        /// </summary>
        private T Present<T>(bool kid = true) where T : MonoBehaviour
        {
            InitIfNeeded();
            Speech.Stop();
            ClearCurrentScreen();
            RefreshFrames();

            var go = new GameObject(typeof(T).Name, typeof(RectTransform), typeof(CanvasGroup), typeof(T));
            go.transform.SetParent(kid ? KidRoot : SafeRoot, false);
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
