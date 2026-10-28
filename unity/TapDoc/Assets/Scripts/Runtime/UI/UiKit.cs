using System;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    public static class UiKit
    {
        public const float MinTouch = 160f;
        public const float SafeWidth = 1440f;
        public static readonly Vector2 Reference = new(1920f, 1080f);

        /// <summary>Chữ tự co nhưng không nhỏ hơn cỡ này (đơn vị canvas 1920×1080).</summary>
        public const float MinFontSize = 28f;

        // Vùng màn học (Stage) nằm trong vùng an toàn rộng SafeWidth: trên chừa nút "Về",
        // dưới chừa nút "Nghe lại"/"Tiếp". Ở canvas tham chiếu, Stage = 1400×680.
        public const float StageSideInset = 20f;
        public const float StageTopInset = 200f;
        public const float StageBottomInset = 200f;

        private static Sprite _whiteSprite;

        public static Sprite WhiteSprite
        {
            get
            {
                if (_whiteSprite == null)
                {
                    var tex = Texture2D.whiteTexture;
                    _whiteSprite = Sprite.Create(tex, new Rect(0, 0, tex.width, tex.height), new Vector2(0.5f, 0.5f));
                }
                return _whiteSprite;
            }
        }

        public static Canvas CreateCanvas(Camera cam)
        {
            var go = new GameObject("Canvas", typeof(RectTransform), typeof(Canvas), typeof(CanvasScaler), typeof(GraphicRaycaster));
            var canvas = go.GetComponent<Canvas>();
            canvas.renderMode = cam != null ? RenderMode.ScreenSpaceCamera : RenderMode.ScreenSpaceOverlay;
            canvas.worldCamera = cam;
            canvas.planeDistance = 10f;

            var scaler = go.GetComponent<CanvasScaler>();
            scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
            scaler.referenceResolution = Reference;
            scaler.screenMatchMode = CanvasScaler.ScreenMatchMode.MatchWidthOrHeight;
            scaler.matchWidthOrHeight = 1f;

            return canvas;
        }

        /// <summary>Vùng an toàn rộng <see cref="SafeWidth"/>, cao hết canvas, đặt giữa màn hình.</summary>
        public static RectTransform CreateSafeArea(Transform canvas)
        {
            var go = new GameObject("SafeArea", typeof(RectTransform));
            go.transform.SetParent(canvas, false);
            var rt = go.GetComponent<RectTransform>();
            rt.anchorMin = new Vector2(0.5f, 0f);
            rt.anchorMax = new Vector2(0.5f, 1f);
            rt.sizeDelta = new Vector2(SafeWidth, 0f);
            rt.anchoredPosition = Vector2.zero;
            return rt;
        }

        /// <summary>
        /// Vùng đặt màn học bên trong <paramref name="parent"/> (thường là màn bài học, phủ hết vùng an toàn).
        /// App và test dùng chung hàm này để có cùng kích thước.
        /// </summary>
        public static RectTransform CreateStage(RectTransform parent)
        {
            var go = new GameObject("Stage", typeof(RectTransform));
            go.transform.SetParent(parent, false);
            var rt = go.GetComponent<RectTransform>();
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = new Vector2(StageSideInset, StageBottomInset);
            rt.offsetMax = new Vector2(-StageSideInset, -StageTopInset);
            return rt;
        }

        public static Tile CreateTile(Transform parent, string richText, Sprite image = null)
        {
            var go = new GameObject("Tile", typeof(RectTransform), typeof(Image), typeof(LayoutElement), typeof(Tile));
            go.transform.SetParent(parent, false);

            var rt = go.GetComponent<RectTransform>();
            rt.sizeDelta = new Vector2(220f, 180f);

            var le = go.GetComponent<LayoutElement>();
            le.minWidth = MinTouch;
            le.minHeight = MinTouch;
            le.preferredWidth = 220f;
            le.preferredHeight = 180f;

            var bg = go.GetComponent<Image>();
            bg.sprite = WhiteSprite;
            bg.color = new Color(1f, 0.99f, 0.95f, 1f);

            var picGo = new GameObject("ImageBox", typeof(RectTransform), typeof(Image));
            picGo.transform.SetParent(go.transform, false);
            var picRt = picGo.GetComponent<RectTransform>();
            picRt.anchorMin = new Vector2(0.1f, 0.32f);
            picRt.anchorMax = new Vector2(0.9f, 0.92f);
            picRt.offsetMin = Vector2.zero;
            picRt.offsetMax = Vector2.zero;
            var pic = picGo.GetComponent<Image>();
            pic.raycastTarget = false;

            var lblGo = new GameObject("Label", typeof(RectTransform), typeof(TextMeshProUGUI));
            lblGo.transform.SetParent(go.transform, false);
            var lblRt = lblGo.GetComponent<RectTransform>();
            lblRt.anchorMin = Vector2.zero;
            lblRt.anchorMax = Vector2.one;
            lblRt.offsetMin = new Vector2(12f, 8f);
            lblRt.offsetMax = new Vector2(-12f, -8f);

            var tmp = lblGo.GetComponent<TextMeshProUGUI>();
            ConfigureText(tmp, richText ?? string.Empty, 68f);
            tmp.raycastTarget = false;

            var tile = go.GetComponent<Tile>();
            tile.Setup(bg, pic, tmp, richText, image);
            return tile;
        }

        public static Button CreateButton(Transform parent, string label, Action onClick)
        {
            var go = new GameObject($"Button_{label}", typeof(RectTransform), typeof(Image), typeof(Button), typeof(LayoutElement));
            go.transform.SetParent(parent, false);

            var rt = go.GetComponent<RectTransform>();
            rt.sizeDelta = new Vector2(260f, MinTouch);

            var le = go.GetComponent<LayoutElement>();
            le.minWidth = MinTouch;
            le.minHeight = MinTouch;
            le.preferredWidth = 260f;
            le.preferredHeight = MinTouch;

            var img = go.GetComponent<Image>();
            img.sprite = WhiteSprite;
            img.color = label == UiText.Next
                ? new Color(0.22f, 0.65f, 0.32f, 1f)
                : new Color(0.18f, 0.52f, 0.62f, 1f);

            var btn = go.GetComponent<Button>();
            btn.targetGraphic = img;
            if (onClick != null)
            {
                btn.onClick.AddListener(() => onClick());
            }

            var lblGo = new GameObject("Text", typeof(RectTransform), typeof(TextMeshProUGUI));
            lblGo.transform.SetParent(go.transform, false);
            var lblRt = lblGo.GetComponent<RectTransform>();
            lblRt.anchorMin = Vector2.zero;
            lblRt.anchorMax = Vector2.one;
            lblRt.offsetMin = new Vector2(14f, 10f);
            lblRt.offsetMax = new Vector2(-14f, -10f);

            var tmp = lblGo.GetComponent<TextMeshProUGUI>();
            ConfigureText(tmp, label ?? string.Empty, 44f);
            tmp.color = Color.white;
            tmp.raycastTarget = false;

            return btn;
        }

        public static TextMeshProUGUI CreateLabel(Transform parent, string text, float maxSize)
        {
            var go = new GameObject("Label", typeof(RectTransform), typeof(TextMeshProUGUI));
            go.transform.SetParent(parent, false);
            var rt = go.GetComponent<RectTransform>();
            rt.sizeDelta = new Vector2(600f, 120f);

            var tmp = go.GetComponent<TextMeshProUGUI>();
            ConfigureText(tmp, text ?? string.Empty, maxSize);
            tmp.raycastTarget = false;
            return tmp;
        }

        private static void ConfigureText(TextMeshProUGUI tmp, string text, float maxSize)
        {
            tmp.font = FontProvider.Main;
            tmp.text = text;
            tmp.enableAutoSizing = true;
            tmp.fontSizeMin = Mathf.Min(MinFontSize, maxSize);
            tmp.fontSizeMax = maxSize;
            tmp.fontSize = maxSize;
            tmp.color = new Color(0.15f, 0.14f, 0.12f, 1f);
            tmp.alignment = TextAlignmentOptions.Center;
            tmp.textWrappingMode = TextWrappingModes.Normal;
            tmp.overflowMode = TextOverflowModes.Overflow;
        }
    }
}
