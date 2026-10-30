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

        /// <summary>Độ dày viền mực của thẻ và nút.</summary>
        public const float BorderWidth = 3f;

        /// <summary>Độ lệch của bóng gạch chéo so với vật (xuống dưới, sang phải).</summary>
        public static readonly Vector2 ShadowOffset = new(10f, -10f);

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

        /// <summary>
        /// Thẻ chữ/tranh: gốc là khung bo góc màu mực (nhận chạm), con <c>Fill</c> thụt vào <see cref="BorderWidth"/>
        /// là nền giấy, đổi màu theo trạng thái của <see cref="Tile"/>.
        /// </summary>
        public static Tile CreateTile(Transform parent, string richText, Sprite image = null)
        {
            var go = new GameObject("Tile", typeof(RectTransform), typeof(Image), typeof(LayoutElement), typeof(Tile),
                typeof(TapFeedback));
            go.transform.SetParent(parent, false);

            var rt = go.GetComponent<RectTransform>();
            rt.sizeDelta = new Vector2(220f, 180f);

            var le = go.GetComponent<LayoutElement>();
            le.minWidth = MinTouch;
            le.minHeight = MinTouch;
            le.preferredWidth = 220f;
            le.preferredHeight = 180f;

            SetRounded(go.GetComponent<Image>(), Palette.Ink);
            var fill = AddFill(go.transform, UiShapes.Rounded, Palette.PaperLight);

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
            tile.Setup(fill, pic, tmp, richText, image);
            return tile;
        }

        /// <summary>Nút của người lớn: bo góc, viền mực, nền lam ngọc, chữ trắng. Tên GameObject <c>Button_&lt;nhãn&gt;</c>.</summary>
        public static Button CreateButton(Transform parent, string label, Action onClick) =>
            CreateTextButton(parent, label, onClick, Palette.Teal, Color.white, false);

        /// <summary>
        /// Thẻ to (thẻ bé, thẻ bài): nền giấy sáng, chữ màu mực, có bóng gạch chéo. Bóng là con đầu tiên của thẻ,
        /// nên thẻ đặt được trong layout group mà không thêm ô thừa.
        /// </summary>
        public static Button CreateCardButton(Transform parent, string label, Action onClick) =>
            CreateTextButton(parent, label, onClick, Palette.PaperLight, Palette.Ink, true);

        /// <summary>
        /// Nút của bé: hình tròn 160×160, viền mực, nền <paramref name="fill"/> (mặc định lam ngọc), ở giữa là biểu tượng
        /// <paramref name="iconId"/>; không có chữ. <paramref name="label"/> (chữ trong <see cref="UiText"/>) chỉ dùng đặt
        /// tên GameObject <c>Button_&lt;nhãn&gt;</c> và ghi vào <see cref="IconButton.Label"/>.
        /// </summary>
        public static Button CreateIconButton(Transform parent, AssetCatalog assets, string iconId, string label,
            Action onClick, Color? fill = null)
        {
            var go = new GameObject($"Button_{label}", typeof(RectTransform), typeof(Image), typeof(Button),
                typeof(LayoutElement), typeof(IconButton), typeof(TapFeedback));
            go.transform.SetParent(parent, false);
            ((RectTransform)go.transform).sizeDelta = new Vector2(MinTouch, MinTouch);

            var le = go.GetComponent<LayoutElement>();
            le.minWidth = le.preferredWidth = MinTouch;
            le.minHeight = le.preferredHeight = MinTouch;

            var border = go.GetComponent<Image>();
            border.sprite = UiShapes.Circle;
            border.color = Palette.Ink;
            var fillImg = AddFill(go.transform, UiShapes.Circle, fill ?? Palette.Teal);

            var iconGo = new GameObject("Icon", typeof(RectTransform), typeof(Image));
            iconGo.transform.SetParent(go.transform, false);
            var irt = (RectTransform)iconGo.transform;
            irt.anchorMin = new Vector2(0.21f, 0.21f);
            irt.anchorMax = new Vector2(0.79f, 0.79f);
            irt.offsetMin = Vector2.zero;
            irt.offsetMax = Vector2.zero;
            var icon = iconGo.GetComponent<Image>();
            icon.sprite = assets?.Image(iconId);
            icon.preserveAspect = true;
            icon.raycastTarget = false;
            icon.enabled = icon.sprite != null;

            var btn = go.GetComponent<Button>();
            btn.targetGraphic = fillImg;
            if (onClick != null) btn.onClick.AddListener(() => onClick());

            var marker = go.GetComponent<IconButton>();
            marker.IconId = iconId;
            marker.Label = label;
            return btn;
        }

        /// <summary>
        /// Bóng gạch chéo kiểu tranh SGK cho một vật đặt tự do (khung tranh, quyển sổ): anh em đứng ngay trước
        /// <paramref name="target"/>, cùng neo và cỡ, lệch <see cref="ShadowOffset"/>, không nhận chạm.
        /// Vật nằm trong layout group thì dùng <see cref="CreateCardButton"/> (bóng là con của thẻ).
        /// </summary>
        public static GameObject AddHatchShadow(RectTransform target)
        {
            var shadow = CreateHatch(target.parent, "Shadow");
            var srt = (RectTransform)shadow.transform;
            srt.anchorMin = target.anchorMin;
            srt.anchorMax = target.anchorMax;
            srt.pivot = target.pivot;
            srt.sizeDelta = target.sizeDelta;
            srt.anchoredPosition = target.anchoredPosition + ShadowOffset;
            shadow.transform.SetSiblingIndex(target.GetSiblingIndex());
            return shadow;
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

        private static Button CreateTextButton(Transform parent, string label, Action onClick, Color fillColor,
            Color textColor, bool withShadow)
        {
            var go = new GameObject($"Button_{label}", typeof(RectTransform), typeof(Image), typeof(Button), typeof(LayoutElement),
                typeof(TapFeedback));
            go.transform.SetParent(parent, false);

            var rt = go.GetComponent<RectTransform>();
            rt.sizeDelta = new Vector2(260f, MinTouch);

            var le = go.GetComponent<LayoutElement>();
            le.minWidth = MinTouch;
            le.minHeight = MinTouch;
            le.preferredWidth = 260f;
            le.preferredHeight = MinTouch;

            var root = go.GetComponent<Image>();
            if (withShadow)
            {
                // Gốc trong suốt nhận chạm; bóng và viền là con, bóng đứng đầu nên nằm dưới cùng.
                SetRounded(root, Color.clear);
                var shadow = CreateHatch(go.transform, "Shadow");
                var srt = (RectTransform)shadow.transform;
                srt.anchorMin = Vector2.zero;
                srt.anchorMax = Vector2.one;
                srt.offsetMin = ShadowOffset;
                srt.offsetMax = ShadowOffset;
                var borderGo = new GameObject("Border", typeof(RectTransform), typeof(Image));
                borderGo.transform.SetParent(go.transform, false);
                Stretch((RectTransform)borderGo.transform, 0f);
                var border = borderGo.GetComponent<Image>();
                SetRounded(border, Palette.Ink);
                border.raycastTarget = false;
            }
            else
            {
                SetRounded(root, Palette.Ink);
            }
            var fill = AddFill(go.transform, UiShapes.Rounded, fillColor);

            var btn = go.GetComponent<Button>();
            btn.targetGraphic = fill;
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
            tmp.color = textColor;
            tmp.raycastTarget = false;

            return btn;
        }

        /// <summary>Lớp nền thụt vào <see cref="BorderWidth"/> so với cha, không nhận chạm.</summary>
        private static Image AddFill(Transform parent, Sprite shape, Color color)
        {
            var go = new GameObject("Fill", typeof(RectTransform), typeof(Image));
            go.transform.SetParent(parent, false);
            Stretch((RectTransform)go.transform, BorderWidth);
            var img = go.GetComponent<Image>();
            img.sprite = shape;
            img.type = shape == UiShapes.Rounded ? Image.Type.Sliced : Image.Type.Simple;
            img.color = color;
            img.raycastTarget = false;
            return img;
        }

        /// <summary>Khung bo góc có mặt nạ, bên trong lặp vân gạch chéo; không nhận chạm.</summary>
        private static GameObject CreateHatch(Transform parent, string name)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(Image), typeof(Mask));
            go.transform.SetParent(parent, false);
            var mask = go.GetComponent<Image>();
            mask.sprite = UiShapes.Rounded;
            mask.type = Image.Type.Sliced;
            mask.raycastTarget = false;
            go.GetComponent<Mask>().showMaskGraphic = false;

            var lines = new GameObject("Lines", typeof(RectTransform), typeof(Image));
            lines.transform.SetParent(go.transform, false);
            Stretch((RectTransform)lines.transform, 0f);
            var img = lines.GetComponent<Image>();
            img.sprite = UiShapes.Hatch;
            img.type = Image.Type.Tiled;
            img.raycastTarget = false;
            return go;
        }

        private static void SetRounded(Image img, Color color)
        {
            img.sprite = UiShapes.Rounded;
            img.type = Image.Type.Sliced;
            img.color = color;
        }

        private static void Stretch(RectTransform rt, float inset)
        {
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = new Vector2(inset, inset);
            rt.offsetMax = new Vector2(-inset, -inset);
        }

        private static void ConfigureText(TextMeshProUGUI tmp, string text, float maxSize)
        {
            tmp.font = FontProvider.Main;
            tmp.text = text;
            tmp.enableAutoSizing = true;
            tmp.fontSizeMin = Mathf.Min(MinFontSize, maxSize);
            tmp.fontSizeMax = maxSize;
            tmp.fontSize = maxSize;
            tmp.color = Palette.Ink;
            tmp.alignment = TextAlignmentOptions.Center;
            tmp.textWrappingMode = TextWrappingModes.Normal;
            tmp.overflowMode = TextOverflowModes.Overflow;
        }
    }
}
