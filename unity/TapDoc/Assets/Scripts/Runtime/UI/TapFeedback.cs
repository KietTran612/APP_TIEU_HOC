using UnityEngine;
using UnityEngine.EventSystems;

namespace TapDoc
{
    /// <summary>
    /// Thẻ hoặc nút lún xuống khi bé nhấn và bật lại khi thả. <see cref="Sound"/> khác <c>null</c> thì phát tiếng động đó
    /// lúc nhấn; chỗ chạm làm giọng đọc phát ngay thì để <c>null</c>, để tiếng "tách" không đè lên lời đánh vần.
    /// </summary>
    public class TapFeedback : MonoBehaviour, IPointerDownHandler, IPointerUpHandler
    {
        public const float PressedScale = .92f;

        /// <summary>Mã tiếng động (<see cref="SystemSfx"/>) phát khi nhấn; <c>null</c> là im lặng.</summary>
        public string Sound { get; set; }

        public void OnPointerDown(PointerEventData eventData)
        {
            _ = Motion.ScaleTo(transform, PressedScale, .06f);
            if (Sound != null && SfxPlayer.Instance != null) SfxPlayer.Instance.Play(Sound);
        }

        public void OnPointerUp(PointerEventData eventData)
        {
            _ = Motion.ScaleTo(transform, 1f, .09f);
        }
    }
}
