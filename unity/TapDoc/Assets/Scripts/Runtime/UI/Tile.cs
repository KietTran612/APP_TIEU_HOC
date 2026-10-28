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
            if (IsHinted)
            {
                _background.color = new Color(1f, 0.92f, 0.45f, 1f);
            }
            else if (_isHighlighted)
            {
                _background.color = new Color(0.82f, 0.95f, 0.98f, 1f);
            }
            else
            {
                _background.color = new Color(1f, 0.99f, 0.95f, 1f);
            }
        }
    }
}
