using System;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Lớp trong suốt phủ màn khi một cảnh hiệu ứng đang chạy: bé chạm bất kỳ chỗ nào thì cảnh nhảy tới cuối.
    /// Không phải nút (không tính là vùng chạm của bé trong kiểm tra bố cục).
    /// </summary>
    public class SceneSkipper : MonoBehaviour, IPointerClickHandler
    {
        private Action _onSkip;

        public static SceneSkipper Create(Transform parent, Action onSkip)
        {
            var go = new GameObject("SceneSkipper", typeof(RectTransform), typeof(Image), typeof(SceneSkipper));
            go.transform.SetParent(parent, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            go.GetComponent<Image>().color = Color.clear;
            var skipper = go.GetComponent<SceneSkipper>();
            skipper._onSkip = onSkip;
            return skipper;
        }

        public void OnPointerClick(PointerEventData eventData) => _onSkip?.Invoke();
    }
}
