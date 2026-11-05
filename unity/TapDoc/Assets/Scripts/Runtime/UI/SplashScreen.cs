using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Màn mở đầu (bản thiết kế màn mở đầu, cảnh báo, cài đặt mục 4, 5.1): nền giấy phủ kín màn, gà con nhún, tên app,
    /// ba chấm chạy, hiện trong lúc app nạp dữ liệu khởi động; chặn mọi lần chạm. <see cref="HideAsync"/> chờ đủ
    /// <see cref="MinSeconds"/> kể từ lúc hiện rồi mờ ra. Nạp lỗi thì <see cref="ShowError"/> và màn ở lại.
    /// </summary>
    public sealed class SplashScreen : MonoBehaviour
    {
        public const float MinSeconds = 1f;
        public const float FadeSeconds = .3f;
        public const float MascotSize = 260f;
        private const float DotSize = 26f;
        private const float DotStep = .35f;

        private CanvasGroup _group;
        private float _shownAt;
        private Image[] _dots;
        private GameObject _dotRow;

        public bool IsShowing => gameObject.activeSelf;

        /// <summary>Dòng báo lỗi cho người lớn (ẩn cho tới khi nạp lỗi).</summary>
        public TMP_Text ErrorLabel { get; private set; }

        public static SplashScreen Create(Transform canvas, AssetCatalog assets)
        {
            var go = new GameObject("SplashScreen", typeof(RectTransform), typeof(Image), typeof(CanvasGroup));
            go.transform.SetParent(canvas, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            var paper = go.GetComponent<Image>();
            paper.sprite = UiKit.WhiteSprite;
            paper.color = Palette.Paper;
            paper.raycastTarget = true; // chặn chạm trong lúc nạp

            var splash = go.AddComponent<SplashScreen>();
            splash._group = go.GetComponent<CanvasGroup>();
            splash.Build(assets);
            splash._shownAt = Time.realtimeSinceStartup;
            go.transform.SetAsLastSibling();
            return splash;
        }

        private void Build(AssetCatalog assets)
        {
            // Hình gà con đã nạp thì gắn ngay; lúc khởi động thì AppRoot nạp xong mới gắn (AttachMascot).
            if (assets != null && assets.IsLoaded(ContentKind.Image, SystemImages.Mascot)) AttachMascot(assets);

            var title = UiKit.CreateLabel(transform, UiText.AppTitle, 96f);
            var trt = title.rectTransform;
            trt.anchorMin = trt.anchorMax = new Vector2(.5f, .5f);
            trt.sizeDelta = new Vector2(1200f, 140f);
            trt.anchoredPosition = new Vector2(0f, -100f);

            _dotRow = new GameObject("Dots", typeof(RectTransform));
            _dotRow.transform.SetParent(transform, false);
            var drt = (RectTransform)_dotRow.transform;
            drt.anchorMin = drt.anchorMax = new Vector2(.5f, .5f);
            drt.anchoredPosition = new Vector2(0f, -210f);
            _dots = new Image[3];
            for (var i = 0; i < _dots.Length; i++)
            {
                var dot = new GameObject($"Dot_{i}", typeof(RectTransform), typeof(Image));
                dot.transform.SetParent(_dotRow.transform, false);
                var rt = (RectTransform)dot.transform;
                rt.sizeDelta = new Vector2(DotSize, DotSize);
                rt.anchoredPosition = new Vector2((i - 1) * 2f * DotSize, 0f);
                var img = dot.GetComponent<Image>();
                img.sprite = UiShapes.Circle;
                img.color = Palette.Orange;
                img.raycastTarget = false;
                _dots[i] = img;
            }

            ErrorLabel = UiKit.CreateLabel(transform, string.Empty, 44f);
            var ert = ErrorLabel.rectTransform;
            ert.anchorMin = ert.anchorMax = new Vector2(.5f, .5f);
            ert.sizeDelta = new Vector2(1200f, 160f);
            ert.anchoredPosition = new Vector2(0f, -240f);
            ErrorLabel.gameObject.SetActive(false);
        }

        /// <summary>Gắn gà con (nhún nhẹ) phía trên tên app; gọi khi hình gà con đã được chuẩn bị.</summary>
        public void AttachMascot(AssetCatalog assets)
        {
            if (Mascot != null) return;
            Mascot = TapDoc.Mascot.Create(transform, assets, MascotSize);
            var mrt = (RectTransform)Mascot.transform;
            mrt.anchorMin = mrt.anchorMax = new Vector2(.5f, .5f);
            mrt.anchoredPosition = new Vector2(0f, 120f);
            Pulse.StartOn(Mascot.transform, .05f, 1.4f);
        }

        public Mascot Mascot { get; private set; }

        private void Update()
        {
            if (_dots == null || Motion.Scale <= 0f) return;
            var lit = (int)(Time.unscaledTime / DotStep) % (_dots.Length + 1);
            for (var i = 0; i < _dots.Length; i++)
            {
                _dots[i].color = i < lit ? Palette.Orange : Palette.OrangeLight;
            }
        }

        /// <summary>Nạp lỗi: hiện dòng báo cho người lớn, ẩn ba chấm; màn mở đầu ở lại.</summary>
        public void ShowError(string message)
        {
            transform.SetAsLastSibling();
            gameObject.SetActive(true);
            _group.alpha = 1f;
            _dotRow.SetActive(false);
            ErrorLabel.text = message;
            ErrorLabel.gameObject.SetActive(true);
        }

        /// <summary>Chờ đủ thời gian tối thiểu kể từ lúc hiện, nằm trên cùng (che popup, màn mới) rồi mờ ra và tắt.</summary>
        public async Awaitable HideAsync()
        {
            transform.SetAsLastSibling();
            while (MinSeconds * Motion.Scale - (Time.realtimeSinceStartup - _shownAt) > 0f)
            {
                await Awaitable.NextFrameAsync();
                if (this == null) return;
            }
            await Motion.Fade(_group, 0f, FadeSeconds);
            if (this == null) return;
            gameObject.SetActive(false);
        }
    }
}
