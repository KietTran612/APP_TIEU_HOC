using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Con dấu đỏ "BÉ NGOAN" vẽ bằng code (hai vòng tròn màu đỏ son và chữ bằng font của app), nghiêng nhẹ, không nhận
    /// chạm. Vẽ bằng code vì tranh vẽ máy hay sai chữ tiếng Việt có dấu (bản thiết kế giao diện mục 8.4).
    /// </summary>
    public class Stamp : MonoBehaviour
    {
        public const float DefaultSize = 220f;
        public const float Tilt = -14f;

        public CanvasGroup Group { get; private set; }

        public static Stamp Create(Transform parent, float size = DefaultSize)
        {
            var go = new GameObject("Stamp", typeof(RectTransform), typeof(CanvasGroup), typeof(Stamp));
            go.transform.SetParent(parent, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = rt.anchorMax = new Vector2(.5f, .5f);
            rt.sizeDelta = new Vector2(size, size);
            rt.localRotation = Quaternion.Euler(0f, 0f, Tilt);
            var stamp = go.GetComponent<Stamp>();
            stamp.Group = go.GetComponent<CanvasGroup>();
            stamp.Group.blocksRaycasts = false;

            // Vòng ngoài dày, vòng trong mảnh, giữa là chữ.
            Ring(rt, 0f, Palette.StampRed);
            Ring(rt, size * .05f, Palette.PaperLight);
            Ring(rt, size * .08f, Palette.StampRed);
            Ring(rt, size * .1f, Palette.PaperLight);
            var label = UiKit.CreateLabel(rt, UiText.StampText, size * .2f);
            label.color = Palette.StampRed;
            label.fontStyle = FontStyles.Bold;
            var lrt = label.rectTransform;
            lrt.anchorMin = Vector2.zero;
            lrt.anchorMax = Vector2.one;
            lrt.offsetMin = new Vector2(size * .16f, size * .16f);
            lrt.offsetMax = new Vector2(-size * .16f, -size * .16f);
            return stamp;
        }

        private static void Ring(RectTransform parent, float inset, Color color)
        {
            var go = new GameObject("Ring", typeof(RectTransform), typeof(Image));
            go.transform.SetParent(parent, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = new Vector2(inset, inset);
            rt.offsetMax = new Vector2(-inset, -inset);
            var img = go.GetComponent<Image>();
            img.sprite = UiShapes.Circle;
            img.color = color;
            img.raycastTarget = false;
        }
    }
}
