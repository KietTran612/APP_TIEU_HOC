using System;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Hai nút lật trang trong một bước (bảng chữ hoa, bảng ôn vần, bảng nhóm vần), xếp dọc ở mép phải Stage: biểu tượng
    /// tờ giấy gấp góc trên nền giấy sáng, khác hẳn nút "Tiếp" màu cam để bé không lẫn "sang trang" với "sang bước".
    /// Trang đầu ẩn nút trang trước, trang cuối ẩn nút trang sau.
    /// </summary>
    public sealed class PageButtons
    {
        public const float DefaultX = 590f;
        private const float OffsetY = 92f;

        private readonly Button _prev;
        private readonly Button _next;

        public PageButtons(Transform parent, AssetCatalog assets, Action prev, Action next, float x = DefaultX)
        {
            _prev = Create(parent, assets, SystemIcons.PagePrev, UiText.PagePrev, new Vector2(x, OffsetY), prev);
            _next = Create(parent, assets, SystemIcons.PageNext, UiText.PageNext, new Vector2(x, -OffsetY), next);
        }

        public void Show(int page, int pageCount)
        {
            _prev.gameObject.SetActive(page > 0);
            _next.gameObject.SetActive(page < pageCount - 1);
        }

        private static Button Create(Transform parent, AssetCatalog assets, string icon, string label, Vector2 position,
            Action action)
        {
            var button = UiKit.CreateIconButton(parent, assets, icon, label, action, Palette.PaperLight);
            button.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;
            var rt = (RectTransform)button.transform;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = position;
            return button;
        }
    }
}
