using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Thẻ hoặc nút lún xuống khi bé nhấn và bật lại khi thả. <see cref="Sound"/> khác <c>null</c> thì phát tiếng động đó
    /// khi chạm xong (không phát khi bé đang kéo hay cuộn); chỗ chạm làm giọng đọc phát ngay thì để <c>null</c>. Tiếng chạm
    /// không phát khi giọng đọc đang đánh vần hay đọc câu, và nút đang tắt (bài chưa mở) thì không lún, không kêu.
    /// </summary>
    public class TapFeedback : MonoBehaviour, IPointerDownHandler, IPointerUpHandler, IPointerClickHandler
    {
        public const float PressedScale = .92f;

        /// <summary>Mã tiếng động (<see cref="SystemSfx"/>) phát khi chạm; <c>null</c> là im lặng.</summary>
        public string Sound { get; set; }

        private bool Interactable
        {
            get
            {
                var selectable = GetComponent<Selectable>();
                return selectable == null || selectable.IsInteractable();
            }
        }

        public void OnPointerDown(PointerEventData eventData)
        {
            if (!Interactable) return;
            _ = Motion.ScaleTo(transform, PressedScale, .06f);
        }

        public void OnPointerUp(PointerEventData eventData)
        {
            _ = Motion.ScaleTo(transform, 1f, .09f);
        }

        public void OnPointerClick(PointerEventData eventData)
        {
            if (Sound == null || !Interactable || (eventData != null && eventData.dragging)) return;
            if (SfxPlayer.Instance != null) SfxPlayer.Instance.PlayUnlessSpeaking(Sound);
        }
    }
}
