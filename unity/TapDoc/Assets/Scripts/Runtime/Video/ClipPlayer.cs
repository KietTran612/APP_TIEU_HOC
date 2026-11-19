using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using Object = UnityEngine.Object;

namespace TapDoc
{
    /// <summary>
    /// Phát tranh động (clip) trên tranh của một thẻ (thiết kế tranh động mục 5, 6, 10). Một bộ cho cả app, mỗi lúc một
    /// clip:
    /// <list type="bullet">
    /// <item>Chỉ bắt đầu khi giọng đọc rảnh; giọng đọc bắt đầu thì clip dừng ngay (giọng đọc luôn được ưu tiên).</item>
    /// <item>Clip hiện trên lớp phủ nằm trong khung tranh, chỉ hiện khi đã có khung đầu, mờ vào; hết thì mờ về tranh
    /// tĩnh (khung cuối của clip khớp tranh).</item>
    /// <item>Máy không phát được, cài đặt tắt, hỏng 2 lần liên tiếp: không phát, tranh tĩnh như cũ, không báo lỗi.</item>
    /// </list>
    /// </summary>
    public sealed class ClipPlayer : MonoBehaviour
    {
        public const float FadeInSeconds = .3f;
        public const float FadeOutSeconds = .25f;
        public const float StopFadeSeconds = .15f;

        /// <summary>Thời gian chờ khung đầu tối đa (giây thật) trước khi coi clip là hỏng.</summary>
        public const float FirstFrameTimeout = 3f;

        /// <summary>Hỏng liên tiếp chừng này lần thì tắt clip đến hết lần mở app.</summary>
        public const int MaxFailures = 2;

        /// <summary>Âm lượng clip: clip vốn nhỏ hơn giọng đọc khoảng 12 dB (đo 18/11), nên để nguyên.</summary>
        public const float Volume = 1f;

        /// <summary>Tắt hẳn clip (test app tắt mặc định để không phát video thật).</summary>
        public static bool Enabled = true;

        /// <summary>Tạo phần phát; <c>null</c> là <see cref="VideoPlayerBackend"/> (test thay bằng bản giả).</summary>
        public static Func<GameObject, IClipBackend> BackendFactory;

        /// <summary>Kiểm tra máy lúc <see cref="Init"/>; <c>null</c> là <see cref="ClipSupport.CurrentDevice"/>.</summary>
        public static Func<bool> DeviceCheck;

        /// <summary>Nhân vào thời gian chờ khung đầu (test thu ngắn).</summary>
        public static float TimeoutScale = 1f;

        private readonly HashSet<string> _warned = new();
        private AssetCatalog _catalog;
        private SpeechPlayer _speech;
        private IClipBackend _backend;
        private bool _deviceOk;
        private bool _settingEnabled = true;
        private int _generation;

        /// <summary>Cài đặt "Tranh động" của phụ huynh. Tắt thì dừng clip đang chạy; bật lại thì đếm hỏng lại từ 0.</summary>
        public bool SettingEnabled
        {
            get => _settingEnabled;
            set
            {
                _settingEnabled = value;
                if (value) Failures = 0;
                else Stop();
            }
        }

        /// <summary>Có clip đang chạy (từ lúc bắt đầu tới khi gỡ lớp phủ).</summary>
        public bool IsPlaying { get; private set; }

        /// <summary>Mã tranh của clip đang chạy.</summary>
        public string CurrentId { get; private set; }

        /// <summary>Số lần hỏng liên tiếp.</summary>
        public int Failures { get; private set; }

        internal ClipOverlay ActiveOverlay { get; private set; }

        public void Init(AssetCatalog catalog, SpeechPlayer speech)
        {
            _catalog = catalog;
            _speech = speech;
            _deviceOk = (DeviceCheck ?? ClipSupport.CurrentDevice)();
        }

        private IClipBackend Backend => _backend ??= (BackendFactory ?? (host => new VideoPlayerBackend(host)))(gameObject);

        /// <summary>Tranh <paramref name="imageId"/> có clip và lúc này được phát.</summary>
        public bool CanPlay(string imageId) =>
            Enabled && _settingEnabled && _deviceOk && Failures < MaxFailures && _catalog != null
            && !string.IsNullOrEmpty(imageId) && _catalog.Clip(imageId) != null;

        /// <summary>
        /// Phát clip của <paramref name="imageId"/> trên tranh của <paramref name="tile"/>. Trả <c>true</c> khi phát hết;
        /// <c>false</c> khi không phát được, bị dừng (giọng đọc, clip khác, thẻ bị huỷ) hoặc hỏng.
        /// </summary>
        public async Awaitable<bool> PlayAsync(Tile tile, string imageId)
        {
            if (tile == null || tile.ImageBox == null || !tile.ImageBox.activeInHierarchy) return false;
            if (_speech != null && _speech.IsBusy) return false;
            if (!CanPlay(imageId)) return false;

            Stop();
            var gen = ++_generation;
            var backend = Backend;
            var overlay = CreateOverlay(tile, out var aspect);
            ActiveOverlay = overlay;
            IsPlaying = true;
            CurrentId = imageId;
            backend.Begin(_catalog.Clip(imageId));

            var deadline = Time.realtimeSinceStartup + FirstFrameTimeout * TimeoutScale;
            while (gen == _generation && !backend.FirstFrameReady && !backend.Failed
                   && Time.realtimeSinceStartup < deadline)
            {
                await Awaitable.NextFrameAsync();
            }
            if (Abandoned(gen, overlay)) return false;
            if (!backend.FirstFrameReady || backend.Failed)
            {
                Fail(imageId);
                return false;
            }

            var raw = overlay.GetComponent<RawImage>();
            raw.texture = backend.Texture;
            raw.uvRect = ClipCrop.UvRect(backend.Width, backend.Height, aspect, ClipCrop.EdgeInsetPx);
            await Motion.Fade(overlay.GetComponent<CanvasGroup>(), 1f, FadeInSeconds);
            if (Abandoned(gen, overlay)) return false;

            while (this != null && gen == _generation && !backend.Finished && !backend.Failed)
            {
                await Awaitable.NextFrameAsync();
            }
            if (Abandoned(gen, overlay)) return false;
            if (backend.Failed)
            {
                Fail(imageId);
                return false;
            }

            Failures = 0;
            // Giữ khung cuối (khớp tranh) rồi mờ về tranh tĩnh bên dưới.
            await Motion.Fade(overlay.GetComponent<CanvasGroup>(), 0f, FadeOutSeconds);
            if (this != null && gen == _generation) Clear(fadeSeconds: 0f);
            return true;
        }

        /// <summary>
        /// Lần phát <paramref name="gen"/> phải thôi: bộ phát bị huỷ, đã có lần phát khác hay <see cref="Stop"/>, hoặc thẻ
        /// bị huỷ trước khi <see cref="Update"/> kịp dừng (thứ tự giữa await và Update không chắc chắn) — khi đó dọn luôn.
        /// </summary>
        private bool Abandoned(int gen, ClipOverlay overlay)
        {
            if (this == null || gen != _generation) return true;
            if (overlay != null) return false;
            _generation++;
            Clear(fadeSeconds: 0f);
            return true;
        }

        /// <summary>Dừng clip đang chạy (tắt tiếng ngay, lớp phủ mờ đi rồi gỡ). Không có gì chạy thì thôi.</summary>
        public void Stop()
        {
            _generation++;
            if (!IsPlaying && ActiveOverlay == null) return;
            Clear(StopFadeSeconds);
        }

        /// <summary>Dừng, gỡ lớp phủ ngay, bỏ tham chiếu clip và nhả bộ nhớ hình. Gọi khi rời bài, trước khi nhả bộ của bài.</summary>
        public void ReleaseAll()
        {
            _generation++;
            Clear(fadeSeconds: 0f);
            _backend?.Release();
        }

        private void Update()
        {
            if (!IsPlaying) return;
            // Giọng đọc luôn được ưu tiên; thẻ bị huỷ hay bị ẩn (bước bị huỷ, trang lật) thì clip dừng.
            if ((_speech != null && _speech.IsBusy) || ActiveOverlay == null || !ActiveOverlay.gameObject.activeInHierarchy)
            {
                Stop();
            }
        }

        private void OnApplicationPause(bool paused)
        {
            if (paused) Stop();
        }

        private void OnDestroy() => ReleaseAll();

        private void Fail(string imageId)
        {
            Clear(fadeSeconds: 0f);
            Failures++;
            if (_warned.Add(imageId)) Debug.LogWarning($"[TapDoc] Không phát được tranh động: {imageId}");
        }

        /// <summary>Dừng phần phát, đưa trạng thái về rảnh và gỡ lớp phủ (mờ đi trong <paramref name="fadeSeconds"/>).</summary>
        private void Clear(float fadeSeconds)
        {
            _backend?.Stop();
            IsPlaying = false;
            CurrentId = null;
            var overlay = ActiveOverlay;
            ActiveOverlay = null;
            if (overlay != null) _ = FadeAndDestroy(overlay, fadeSeconds);
        }

        private static async Awaitable FadeAndDestroy(ClipOverlay overlay, float seconds)
        {
            var group = overlay.GetComponent<CanvasGroup>();
            if (seconds > 0f && group != null && group.alpha > 0f) await Motion.Fade(group, 0f, seconds);
            if (overlay != null) Destroy(overlay.gameObject);
        }

        /// <summary>
        /// Lớp phủ trong khung tranh của thẻ, trùng đúng phần tranh đang hiện (tranh giữ tỉ lệ nên chỉ chiếm phần giữa
        /// khung): <c>RawImage</c> không nhận chạm, ẩn cho tới khi có khung đầu.
        /// </summary>
        private static ClipOverlay CreateOverlay(Tile tile, out float aspect)
        {
            var go = new GameObject("ClipOverlay", typeof(RectTransform), typeof(CanvasGroup), typeof(RawImage),
                typeof(AspectRatioFitter), typeof(ClipOverlay));
            go.transform.SetParent(tile.ImageBox.transform, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;

            var picture = tile.ImageBox.GetComponent<Image>();
            var sprite = picture != null ? picture.sprite : null;
            aspect = sprite != null && sprite.rect.height > 0f ? sprite.rect.width / sprite.rect.height : 1f;
            var fitter = go.GetComponent<AspectRatioFitter>();
            fitter.aspectMode = AspectRatioFitter.AspectMode.FitInParent;
            fitter.aspectRatio = aspect;

            var raw = go.GetComponent<RawImage>();
            raw.raycastTarget = false;
            var group = go.GetComponent<CanvasGroup>();
            group.alpha = 0f;
            group.blocksRaycasts = false;
            group.interactable = false;
            return go.GetComponent<ClipOverlay>();
        }
    }
}
