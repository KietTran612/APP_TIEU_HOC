using System;
using UnityEngine;
using UnityEngine.EventSystems;
using Object = UnityEngine.Object;

namespace TapDoc
{
    [RequireComponent(typeof(Tile))]
    public class DragTile : MonoBehaviour, IBeginDragHandler, IDragHandler, IEndDragHandler
    {
        private RectTransform _rect;
        private Vector2 _startAnchoredPos;
        private Transform _startParent;
        private int _startSiblingIndex;
        private Canvas _canvas;

        public event Action<DropSlot> DroppedOn;

        private void Awake()
        {
            _rect = GetComponent<RectTransform>();
        }

        public void OnBeginDrag(PointerEventData eventData)
        {
            if (_rect == null) _rect = GetComponent<RectTransform>();
            _startAnchoredPos = _rect.anchoredPosition;
            _startParent = transform.parent;
            _startSiblingIndex = transform.GetSiblingIndex();
            _canvas = GetComponentInParent<Canvas>();
            // Vẽ thẻ đang kéo lên trên các thẻ cùng cha; trả lại thứ tự cũ khi thẻ về chỗ.
            transform.SetAsLastSibling();
        }

        public void OnDrag(PointerEventData eventData)
        {
            if (_rect == null) return;
            var scale = _canvas != null && _canvas.scaleFactor > 0f ? _canvas.scaleFactor : 1f;
            _rect.anchoredPosition += eventData.delta / scale;
        }

        public void OnEndDrag(PointerEventData eventData)
        {
            DropSlot hitSlot = null;
            var cam = _canvas != null ? _canvas.worldCamera : null;
            foreach (var slot in Object.FindObjectsByType<DropSlot>())
            {
                if (!slot.gameObject.activeInHierarchy || slot.Area == null) continue;
                if (RectTransformUtility.RectangleContainsScreenPoint(slot.Area, eventData.position, cam))
                {
                    hitSlot = slot;
                    break;
                }
            }

            if (hitSlot != null)
            {
                ResetPosition();
                DroppedOn?.Invoke(hitSlot);
            }
            else
            {
                ResetPosition();
            }
        }

        internal void SimulateDropOn(DropSlot slot)
        {
            if (slot != null)
            {
                DroppedOn?.Invoke(slot);
            }
        }

        internal void SimulateDropNowhere()
        {
            ResetPosition();
        }

        private void ResetPosition()
        {
            if (_rect == null) _rect = GetComponent<RectTransform>();
            if (_startParent == null) return; // chưa từng kéo: thẻ vẫn ở chỗ cũ
            if (transform.parent != _startParent)
            {
                transform.SetParent(_startParent, false);
            }
            transform.SetSiblingIndex(_startSiblingIndex);
            if (_rect != null)
            {
                _rect.anchoredPosition = _startAnchoredPos;
            }
        }
    }
}
