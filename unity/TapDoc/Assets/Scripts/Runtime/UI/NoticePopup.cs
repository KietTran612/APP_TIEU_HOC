using System;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Popup "Gửi phụ huynh" (bản thiết kế màn mở đầu, cảnh báo, cài đặt mục 5.2): nền giấy phủ kín màn chặn chạm phía
    /// sau, nội dung trong khung chuẩn 1440 ở giữa vùng an toàn, cuộn được; một nút người lớn đóng popup. Không phát
    /// giọng đọc hay tiếng động.
    /// </summary>
    public class NoticePopup : MonoBehaviour
    {
        private const float Margin = 40f;
        private const float MascotSize = 120f;

        private RectTransform _frame;

        /// <summary>Nút "Đã hiểu" (lần đầu) hoặc "Đóng" (mở lại từ Cài đặt).</summary>
        public Button CloseButton { get; private set; }

        public bool IsOpen { get; private set; }

        /// <summary>Phát đúng một lần khi popup đóng.</summary>
        public event Action Closed;

        /// <summary>Mở popup trên cùng <paramref name="canvas"/>.</summary>
        public static NoticePopup Show(Transform canvas, AssetCatalog assets, bool firstRun, Action onClosed = null)
        {
            var go = new GameObject("NoticePopup", typeof(RectTransform), typeof(Image), typeof(NoticePopup));
            go.transform.SetParent(canvas, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            var paper = go.GetComponent<Image>();
            paper.sprite = UiKit.WhiteSprite;
            paper.color = Palette.Paper;
            paper.raycastTarget = true; // chặn chạm vào màn phía sau

            var popup = go.GetComponent<NoticePopup>();
            popup.IsOpen = true;
            if (onClosed != null) popup.Closed += onClosed;
            popup.Build(assets, firstRun);
            return popup;
        }

        private void Build(AssetCatalog assets, bool firstRun)
        {
            var frameGo = new GameObject("Frame", typeof(RectTransform));
            frameGo.transform.SetParent(transform, false);
            _frame = (RectTransform)frameGo.transform;
            _frame.anchorMin = _frame.anchorMax = _frame.pivot = Vector2.zero;
            FollowStandardFrame();

            var title = UiKit.CreateLabel(_frame, UiText.NoticeTitle, 60f);
            var trt = title.rectTransform;
            trt.anchorMin = new Vector2(0f, 1f);
            trt.anchorMax = Vector2.one;
            trt.pivot = new Vector2(.5f, 1f);
            trt.offsetMin = new Vector2(Margin, -Margin - UiKit.MinTouch);
            trt.offsetMax = new Vector2(-Margin, -Margin);

            // Khung giấy sáng có bóng gạch chéo, nội dung cuộn bên trong.
            var card = new GameObject("Card", typeof(RectTransform), typeof(Image));
            card.transform.SetParent(_frame, false);
            var crt = (RectTransform)card.transform;
            crt.anchorMin = Vector2.zero;
            crt.anchorMax = Vector2.one;
            crt.offsetMin = new Vector2(Margin + MascotSize, 2f * Margin + UiKit.MinTouch);
            crt.offsetMax = new Vector2(-(Margin + MascotSize), -(Margin + UiKit.MinTouch + 10f));
            UiKit.SetRounded(card.GetComponent<Image>(), Palette.Ink);
            UiKit.AddFill(card.transform, UiShapes.Rounded, Palette.PaperLight);
            UiKit.AddHatchShadow(crt);

            var scrollGo = new GameObject("Scroll", typeof(RectTransform), typeof(ScrollRect));
            scrollGo.transform.SetParent(card.transform, false);
            var srt = (RectTransform)scrollGo.transform;
            srt.anchorMin = Vector2.zero;
            srt.anchorMax = Vector2.one;
            srt.offsetMin = new Vector2(30f, 20f);
            srt.offsetMax = new Vector2(-30f, -20f);
            var viewport = new GameObject("Viewport", typeof(RectTransform), typeof(Image), typeof(RectMask2D));
            viewport.transform.SetParent(scrollGo.transform, false);
            var vrt = (RectTransform)viewport.transform;
            vrt.anchorMin = Vector2.zero;
            vrt.anchorMax = Vector2.one;
            vrt.offsetMin = Vector2.zero;
            vrt.offsetMax = Vector2.zero;
            viewport.GetComponent<Image>().color = Color.clear; // nhận thao tác kéo cuộn

            var body = UiKit.CreateLabel(viewport.transform, UiText.NoticeBody, 40f);
            body.alignment = TextAlignmentOptions.TopLeft;
            body.textWrappingMode = TextWrappingModes.Normal;
            body.enableAutoSizing = false;
            body.fontSize = 40f;
            var brt = body.rectTransform;
            brt.anchorMin = new Vector2(0f, 1f);
            brt.anchorMax = Vector2.one;
            brt.pivot = new Vector2(.5f, 1f);
            brt.sizeDelta = Vector2.zero;
            body.gameObject.AddComponent<ContentSizeFitter>().verticalFit = ContentSizeFitter.FitMode.PreferredSize;
            var scroll = scrollGo.GetComponent<ScrollRect>();
            scroll.viewport = vrt;
            scroll.content = brt;
            scroll.horizontal = false;
            scroll.vertical = true;
            scroll.movementType = ScrollRect.MovementType.Clamped;

            CloseButton = UiKit.CreateButton(_frame, firstRun ? UiText.NoticeAccept : UiText.Close, Close);
            var brt2 = (RectTransform)CloseButton.transform;
            brt2.anchorMin = brt2.anchorMax = brt2.pivot = new Vector2(.5f, 0f);
            brt2.sizeDelta = new Vector2(360f, UiKit.MinTouch);
            brt2.anchoredPosition = new Vector2(0f, Margin);

            var mascot = Mascot.Create(_frame, assets, MascotSize);
            var mrt = (RectTransform)mascot.transform;
            mrt.anchorMin = mrt.anchorMax = mrt.pivot = new Vector2(1f, 0f);
            mrt.anchoredPosition = new Vector2(-Margin / 2f, Margin);
        }

        /// <summary>Đặt khung nội dung trùng khung chuẩn 1440 của app (đổi theo khi xoay máy).</summary>
        private void FollowStandardFrame()
        {
            var app = AppRoot.Instance;
            if (app != null && app.SafeRoot != null)
            {
                _frame.anchoredPosition = app.SafeRoot.anchoredPosition;
                _frame.sizeDelta = app.SafeRoot.sizeDelta;
                return;
            }
            _frame.anchorMin = new Vector2(.5f, 0f);
            _frame.anchorMax = new Vector2(.5f, 1f);
            _frame.pivot = new Vector2(.5f, .5f);
            _frame.sizeDelta = new Vector2(UiKit.SafeWidth, 0f);
        }

        private void LateUpdate()
        {
            if (_frame != null) FollowStandardFrame();
        }

        /// <summary>Đóng popup (gọi nhiều lần chỉ đóng một lần).</summary>
        public void Close()
        {
            if (!IsOpen) return;
            IsOpen = false;
            gameObject.SetActive(false);
            Closed?.Invoke();
            Destroy(gameObject);
        }
    }
}
