using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Màn chuyển phủ lên trên cùng trong lúc app chuẩn bị bài (nạp tranh, âm thanh); chặn mọi lần chạm cho đến khi
    /// <see cref="Hide"/>.
    /// </summary>
    public sealed class PrepareCurtain : MonoBehaviour
    {
        public bool IsShowing => gameObject.activeSelf;

        internal static PrepareCurtain Create(Transform parent)
        {
            var go = new GameObject("PrepareCurtain", typeof(RectTransform), typeof(Image));
            go.transform.SetParent(parent, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            var blocker = go.GetComponent<Image>();
            blocker.sprite = UiKit.WhiteSprite;
            blocker.color = Color.clear;
            blocker.raycastTarget = true;
            var curtain = go.AddComponent<PrepareCurtain>();
            go.SetActive(false);
            return curtain;
        }

        public void Show()
        {
            transform.SetAsLastSibling();
            gameObject.SetActive(true);
        }

        public void Hide()
        {
            gameObject.SetActive(false);
        }
    }
}
