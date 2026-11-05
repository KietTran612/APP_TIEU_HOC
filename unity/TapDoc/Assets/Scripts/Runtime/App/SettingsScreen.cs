using System;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Menu Cài đặt (bản thiết kế màn mở đầu, cảnh báo, cài đặt mục 5.3), mở bằng nút bánh răng ở danh sách bài và màn
    /// chọn bé. Ai cũng dùng được: tiếng động, xem lại lưu ý, thông tin ứng dụng. Chạy được cả khi chưa chọn bé nào.
    /// </summary>
    public class SettingsScreen : MonoBehaviour
    {
        private const float Margin = 20f;
        private const float RowGap = 20f;
        private const float InfoHeight = 260f;

        private AppRoot _app;
        private Action _back;

        public Button BackButton { get; private set; }
        public Button SfxToggle { get; private set; }
        public Button ReviewNoticeButton { get; private set; }
        public TMP_Text InfoLabel { get; private set; }

        /// <summary>Hàng các mục, cuộn được, rộng bằng khung chuẩn 1440 ở giữa.</summary>
        internal RectTransform Content { get; private set; }

        public void Build(AppRoot app, Action back)
        {
            _app = app;
            _back = back;

            BackButton = UiKit.CreateButton(transform, UiText.Back, () => _back?.Invoke());
            var backRt = (RectTransform)BackButton.transform;
            backRt.anchorMin = backRt.anchorMax = backRt.pivot = new Vector2(0f, 1f);
            backRt.sizeDelta = new Vector2(220f, UiKit.MinTouch);
            backRt.anchoredPosition = new Vector2(Margin, -Margin);

            var header = UiKit.CreateLabel(transform, UiText.Settings, 64f);
            var hrt = header.rectTransform;
            hrt.anchorMin = hrt.anchorMax = hrt.pivot = new Vector2(.5f, 1f);
            hrt.sizeDelta = new Vector2(800f, UiKit.MinTouch);
            hrt.anchoredPosition = new Vector2(0f, -Margin);

            Content = BuildScroll();

            SfxToggle = Row(SfxLabel(), ToggleSfx);
            ReviewNoticeButton = Row(UiText.ReviewNotice, () => _app.ShowNotice(firstRun: false));

            InfoLabel = UiKit.CreateLabel(Content, InfoText(), 40f);
            InfoLabel.alignment = TextAlignmentOptions.TopLeft;
            InfoLabel.gameObject.AddComponent<LayoutElement>().preferredHeight = InfoHeight;
        }

        private static string InfoText() =>
            $"<b>{UiText.AppInfo}</b>\n{UiText.AppTitle} · {string.Format(UiText.VersionFormat, Application.version)}\n{UiText.Credits}";

        /// <summary>Một hàng là một nút người lớn có chữ, cao bằng vùng chạm tối thiểu.</summary>
        internal Button Row(string label, Action onClick)
        {
            var button = UiKit.CreateButton(Content, label, onClick);
            var le = button.GetComponent<LayoutElement>() ?? button.gameObject.AddComponent<LayoutElement>();
            le.preferredHeight = UiKit.MinTouch;
            le.minHeight = UiKit.MinTouch;
            return button;
        }

        private RectTransform BuildScroll()
        {
            var scrollGo = new GameObject("Rows", typeof(RectTransform), typeof(ScrollRect));
            scrollGo.transform.SetParent(transform, false);
            var srt = (RectTransform)scrollGo.transform;
            srt.anchorMin = new Vector2(.5f, 0f);
            srt.anchorMax = new Vector2(.5f, 1f);
            srt.pivot = new Vector2(.5f, .5f);
            srt.offsetMin = new Vector2(-UiKit.SafeWidth / 2f + 2f * Margin, 2f * Margin);
            srt.offsetMax = new Vector2(UiKit.SafeWidth / 2f - 2f * Margin, -(2f * Margin + UiKit.MinTouch));

            var viewport = new GameObject("Viewport", typeof(RectTransform), typeof(Image), typeof(RectMask2D));
            viewport.transform.SetParent(scrollGo.transform, false);
            var vrt = (RectTransform)viewport.transform;
            vrt.anchorMin = Vector2.zero;
            vrt.anchorMax = Vector2.one;
            vrt.offsetMin = Vector2.zero;
            vrt.offsetMax = Vector2.zero;
            viewport.GetComponent<Image>().color = Color.clear; // nhận thao tác kéo cuộn

            var contentGo = new GameObject("Content", typeof(RectTransform), typeof(VerticalLayoutGroup), typeof(ContentSizeFitter));
            contentGo.transform.SetParent(viewport.transform, false);
            var crt = (RectTransform)contentGo.transform;
            crt.anchorMin = new Vector2(0f, 1f);
            crt.anchorMax = Vector2.one;
            crt.pivot = new Vector2(.5f, 1f);
            crt.sizeDelta = Vector2.zero;
            var vlg = contentGo.GetComponent<VerticalLayoutGroup>();
            vlg.spacing = RowGap;
            vlg.childControlWidth = vlg.childControlHeight = true;
            vlg.childForceExpandWidth = true;
            vlg.childForceExpandHeight = false;
            contentGo.GetComponent<ContentSizeFitter>().verticalFit = ContentSizeFitter.FitMode.PreferredSize;

            var scroll = scrollGo.GetComponent<ScrollRect>();
            scroll.viewport = vrt;
            scroll.content = crt;
            scroll.horizontal = false;
            scroll.vertical = true;
            scroll.movementType = ScrollRect.MovementType.Clamped;
            return crt;
        }

        private string SfxLabel() => _app.Progress.SfxEnabled ? UiText.SfxOn : UiText.SfxOff;

        private void ToggleSfx()
        {
            _app.Progress.SfxEnabled = !_app.Progress.SfxEnabled;
            if (_app.Sfx != null) _app.Sfx.Enabled = _app.Progress.SfxEnabled;
            _app.SaveProgress();
            SfxToggle.GetComponentInChildren<TMP_Text>().text = SfxLabel();
        }
    }
}
