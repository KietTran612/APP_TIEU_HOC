using System;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Hai nút "Trang trước"/"Trang sau" xếp dọc ở mép phải Stage, dùng chung cho các màn phân trang.
    /// Trang đầu ẩn "Trang trước", trang cuối ẩn "Trang sau".
    /// </summary>
    public sealed class PageButtons
    {
        public const float DefaultX = 590f;
        public const float DefaultWidth = 220f;
        private const float OffsetY = 92f;

        private readonly Button _prev;
        private readonly Button _next;

        public PageButtons(Transform parent, Action prev, Action next, float x = DefaultX, float width = DefaultWidth)
        {
            _prev = Create(parent, UiText.PagePrev, new Vector2(x, OffsetY), width, prev);
            _next = Create(parent, UiText.PageNext, new Vector2(x, -OffsetY), width, next);
        }

        public void Show(int page, int pageCount)
        {
            _prev.gameObject.SetActive(page > 0);
            _next.gameObject.SetActive(page < pageCount - 1);
        }

        private static Button Create(Transform parent, string text, Vector2 position, float width, Action action)
        {
            var button = UiKit.CreateButton(parent, text, action);
            var rt = (RectTransform)button.transform;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = new Vector2(width, UiKit.MinTouch);
            rt.anchoredPosition = position;
            return button;
        }
    }
}
