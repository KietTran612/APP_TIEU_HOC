using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Bàn tay gợi ý khi bé ngồi im (bản thiết kế nâng cấp UI mục 4.1.3): chóp ngón trỏ chạm mép đích từ phía giữa màn,
    /// thân tay nằm ngoài đích (không che biểu tượng của nút), nhún nhẹ. Không nhận chạm. Thiếu ảnh
    /// <see cref="SystemIcons.PointHand"/> thì vẽ vòng vàng nhấp nháy quanh đích.
    /// </summary>
    public class HintHand : MonoBehaviour
    {
        public const float Size = 140f;

        /// <summary>Hướng ngón trỏ trong tranh (chỉ lên trái), độ.</summary>
        private const float ArtPointDegrees = 135f;

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
            Vector2 min = parent.InverseTransformPoint(corners[0]), max = parent.InverseTransformPoint(corners[2]);
            var center = (min + max) / 2f;
            var bounds = parent.rect;
            if (!_hasArt)
            {
                rt.localRotation = Quaternion.identity;
                rt.anchoredPosition = center;
            }
            else
            {
                // Tay đến từ phía giữa màn: chóp ngón chạm mép đích trên đường nối tâm đích với tâm màn; thân tay quay
                // về phía giữa màn nên không che đích, và nằm trong khung.
                var dir = bounds.center - center;
                dir = dir.sqrMagnitude < 1f ? new Vector2(-1f, 1f).normalized : dir.normalized;
                var half = (max - min) / 2f;
                var reach = Mathf.Min(Mathf.Abs(half.x / (dir.x == 0f ? 1e-4f : dir.x)), Mathf.Abs(half.y / (dir.y == 0f ? 1e-4f : dir.y)));
                var tip = center + dir * (reach + 6f);
                var pointing = -dir; // từ tay hướng vào đích
                var angle = Mathf.Atan2(pointing.y, pointing.x) * Mathf.Rad2Deg - ArtPointDegrees;
                rt.localRotation = Quaternion.Euler(0f, 0f, angle);
                rt.anchoredPosition = new Vector2(Mathf.Clamp(tip.x, bounds.xMin + 4f, bounds.xMax - 4f),
                    Mathf.Clamp(tip.y, bounds.yMin + 4f, bounds.yMax - 4f));
            }
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
