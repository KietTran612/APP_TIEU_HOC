using System;
using System.Text.RegularExpressions;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace TapDoc
{
    public class Tile : MonoBehaviour, IPointerClickHandler
    {
        private static readonly Regex TagRegex = new(@"<[^>]+>", RegexOptions.Compiled);

        private Image _background;
        private Image _picture;
        private TextMeshProUGUI _label;
        private bool _isHighlighted;

        public event Action Tapped;
        public bool IsHinted { get; private set; }
        public GameObject ImageBox => _picture != null ? _picture.gameObject : null;
        internal string PlainText { get; private set; } = string.Empty;
        internal string ImageId { get; set; }

        /// <summary>Dấu thanh của thẻ (<c>huyen</c>, <c>sac</c>…), nếu thẻ gắn với một dấu.</summary>
        internal string Tone { get; set; }

        // Thẻ chỉ chứa một kí hiệu dấu: phóng to và đặt kí hiệu vào giữa thẻ (kí tự dấu vốn nhỏ và nằm cao).
        private bool _glyphMode;
        private (Vector2 min, Vector2 max)? _labelOffsets;

        // Nét kí hiệu chiếm từ 35% đến 70% chiều cao thẻ (và không quá 80% bề rộng); dấu nhỏ (dấu nặng) được phóng tối đa gấp 4 cỡ chữ gốc.
        private const float GlyphScale = 1.6f;
        private const float GlyphMinInk = 0.35f;
        private const float GlyphMaxInk = 0.7f;
        private const float GlyphMaxGrow = 4f;

        internal void Setup(Image background, Image picture, TextMeshProUGUI label, string richText, Sprite sprite, string imageId = null)
        {
            _background = background;
            _picture = picture;
            _label = label;
            ImageId = imageId;
            SetSprite(sprite, imageId);
            SetText(richText);
            RefreshColors();
        }

        public void SetSprite(Sprite sprite, string imageId = null)
        {
            if (imageId != null)
            {
                ImageId = imageId;
            }
            if (_picture != null)
            {
                _picture.sprite = sprite;
                _picture.preserveAspect = true;
                _picture.gameObject.SetActive(sprite != null);
            }
        }

        public void SetText(string rich)
        {
            var value = rich ?? string.Empty;
            PlainText = TagRegex.Replace(value, string.Empty);
            if (_label != null)
            {
                _label.text = value;
                _label.gameObject.SetActive(!string.IsNullOrEmpty(value));
            }
            if (_glyphMode) FitGlyph();
        }

        /// <summary>
        /// Gắn dấu <paramref name="tone"/> và hiện thẻ ở kiểu kí hiệu dấu: chữ to gấp 1,6 lần cỡ tối đa của thẻ,
        /// kí hiệu nằm giữa thẻ theo chiều dọc. Gọi sau khi đã đặt kích thước và cỡ chữ của thẻ.
        /// </summary>
        internal void SetTone(string tone)
        {
            Tone = tone;
            _glyphMode = true;
            FitGlyph();
        }

        private void FitGlyph()
        {
            if (_label == null || string.IsNullOrEmpty(_label.text)) return;
            var rt = _label.rectTransform;
            if (_labelOffsets == null) _labelOffsets = (rt.offsetMin, rt.offsetMax);
            rt.offsetMin = _labelOffsets.Value.min;
            rt.offsetMax = _labelOffsets.Value.max;
            var box = rt.rect;
            if (box.height <= 0f || box.width <= 0f) return;

            var baseSize = _label.fontSizeMax;
            _label.enableAutoSizing = false;
            _label.overflowMode = TextOverflowModes.Overflow;
            _label.margin = Vector4.zero;
            _label.fontSize = baseSize * GlyphScale;
            if (!InkBounds(_label, out var ink)) return;

            // Đo nét chữ thật (textBounds của TMP là chiều cao dòng, với kí tự dấu lớn hơn nét nhiều lần).
            var tileH = ((RectTransform)transform).rect.height;
            var scale = 1f;
            if (ink.size.y < GlyphMinInk * tileH) scale = Mathf.Min(GlyphMinInk * tileH / ink.size.y, GlyphMaxGrow / GlyphScale);
            scale = Mathf.Min(scale, GlyphMaxInk * tileH / ink.size.y, 0.8f * box.width / ink.size.x);
            _label.fontSize *= scale;

            // Dòng chữ của kí tự dấu cao hơn nét nhiều: nới hộp nhãn (vô hình, không nhận chạm) cho vừa dòng, để chữ
            // không bị tính là tràn, rồi mới căn nét vào giữa thẻ.
            var preferred = _label.GetPreferredValues(_label.text);
            var grow = new Vector2(Mathf.Max(0f, preferred.x - box.width), Mathf.Max(0f, preferred.y - box.height)) / 2f + Vector2.one;
            rt.offsetMin -= grow;
            rt.offsetMax += grow;
            if (!InkBounds(_label, out ink)) return;

            // Dời cả vùng chữ để tâm nét kí hiệu trùng tâm thẻ.
            var shift = new Vector2(-ink.center.x, -ink.center.y);
            rt.offsetMin += shift;
            rt.offsetMax += shift;
        }

        /// <summary>Hộp bao nét của các kí tự hiện được, trong toạ độ của nhãn; <c>false</c> khi chưa có nét nào.</summary>
        internal static bool InkBounds(TMP_Text text, out Bounds ink)
        {
            text.ForceMeshUpdate();
            var info = text.textInfo;
            var min = new Vector2(float.MaxValue, float.MaxValue);
            var max = new Vector2(float.MinValue, float.MinValue);
            for (var i = 0; i < info.characterCount; i++)
            {
                var c = info.characterInfo[i];
                if (!c.isVisible) continue;
                min = Vector2.Min(min, c.bottomLeft);
                max = Vector2.Max(max, c.topRight);
            }
            ink = new Bounds();
            if (min.x >= max.x || min.y >= max.y) return false;
            ink.SetMinMax(min, max);
            return true;
        }

        /// <summary>Cỡ chữ tối đa của nhãn (vẫn tự co, không nhỏ hơn <see cref="UiKit.MinFontSize"/>).</summary>
        public void SetFontSize(float max)
        {
            if (_label == null) return;
            _label.fontSizeMax = max;
            _label.fontSize = max;
        }

        public void SetHighlighted(bool highlighted)
        {
            _isHighlighted = highlighted;
            RefreshColors();
        }

        public void SetHint(bool hint)
        {
            IsHinted = hint;
            RefreshColors();
        }

        public void OnPointerClick(PointerEventData eventData)
        {
            // Thả tay sau khi kéo (DragTile) vẫn sinh sự kiện click trên cùng thẻ: không tính là chạm.
            if (eventData != null && eventData.dragging) return;
            Tapped?.Invoke();
        }

        internal void SimulateTap()
        {
            Tapped?.Invoke();
        }

        private void RefreshColors()
        {
            if (_background == null) return;
            _background.color = IsHinted ? Palette.HintYellow
                : _isHighlighted ? Palette.OrangeLight
                : Palette.PaperLight;
        }
    }
}
