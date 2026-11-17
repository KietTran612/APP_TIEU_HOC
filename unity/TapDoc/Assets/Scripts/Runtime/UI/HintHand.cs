using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Bàn tay gợi ý khi bé ngồi im (bản thiết kế nâng cấp UI mục 4.1.3): chóp ngón trỏ chỉ vào giữa đích, tay nằm lệch
    /// xuống dưới phải và nhún nhẹ. Không nhận chạm. Thiếu ảnh <see cref="SystemIcons.PointHand"/> thì vẽ vòng vàng
    /// nhấp nháy quanh đích.
    /// </summary>
    public class HintHand : MonoBehaviour
    {
        public const float Size = 140f;

        private Image _image;
        private bool _hasArt;

        public bool IsShown => gameObject.activeSelf;

        /// <summary>Đích đang chỉ.</summary>
        public RectTransform Target { get; private set; }

        public static HintHand Create(Transform parent, AssetCatalog assets)
        {
            var go = new GameObject("HintHand", typeof(RectTransform), typeof(Image), typeof(HintHand));
            go.transform.SetParent(parent, false);
            var hand = go.GetComponent<HintHand>();
            hand._image = go.GetComponent<Image>();
            hand._image.raycastTarget = false;
            var sprite = assets?.Image(SystemIcons.PointHand);
            hand._hasArt = sprite != null;
            hand._image.sprite = hand._hasArt ? sprite : UiShapes.Circle;
            hand._image.color = hand._hasArt ? Color.white : new Color(Palette.HintYellow.r, Palette.HintYellow.g, Palette.HintYellow.b, .55f);
            hand._image.preserveAspect = true;
            var rt = (RectTransform)go.transform;
            rt.anchorMin = rt.anchorMax = new Vector2(.5f, .5f);
            rt.sizeDelta = new Vector2(Size, Size);
            // Chóp ngón trỏ của tranh tay nằm gần góc trên trái.
            rt.pivot = hand._hasArt ? new Vector2(.18f, .86f) : new Vector2(.5f, .5f);
            go.SetActive(false);
            return hand;
        }

        /// <summary>Chỉ vào <paramref name="target"/>; cả bàn tay nằm trong khung cha.</summary>
        public void Show(RectTransform target)
        {
            if (target == null) return;
            Target = target;
            var parent = (RectTransform)transform.parent;
            var rt = (RectTransform)transform;
            var corners = new Vector3[4];
            target.GetWorldCorners(corners);
            Vector2 center = parent.InverseTransformPoint((corners[0] + corners[2]) / 2f);
            var bounds = parent.rect;
            // Giữ cả tay trong khung: chóp tay lệch tối đa theo phần tay còn lại.
            var minX = bounds.xMin + rt.pivot.x * Size;
            var maxX = bounds.xMax - (1f - rt.pivot.x) * Size;
            var minY = bounds.yMin + rt.pivot.y * Size;
            var maxY = bounds.yMax - (1f - rt.pivot.y) * Size;
            rt.anchoredPosition = new Vector2(Mathf.Clamp(center.x, minX, maxX), Mathf.Clamp(center.y, minY, maxY));
            transform.SetAsLastSibling();
            gameObject.SetActive(true);
            Pulse.StartOn(transform, .1f, 1f);
        }

        public void Hide()
        {
            Target = null;
            Pulse.StopOn(transform);
            gameObject.SetActive(false);
        }
    }
}
