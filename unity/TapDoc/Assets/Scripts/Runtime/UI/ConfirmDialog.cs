using System;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Hộp hỏi xác nhận cho người lớn (xoá hồ sơ, xoá toàn bộ): nền giấy phủ kín màn chặn chạm, câu hỏi và hai nút
    /// "Huỷ" / nút xác nhận ở giữa khung chuẩn 1440. Bấm nút nào cũng đóng hộp; chỉ nút xác nhận gọi <c>onConfirm</c>.
    /// </summary>
    public class ConfirmDialog : MonoBehaviour
    {
        private const float ButtonWidth = 320f;
        private const float ButtonGap = 60f;

        private Action _onConfirm;
        private bool _closed;

        public TMP_Text Message { get; private set; }
        public Button ConfirmButton { get; private set; }
        public Button CancelButton { get; private set; }

        /// <summary>
        /// Mở hộp hỏi. <paramref name="confirmOnLeft"/>: đổi chỗ hai nút (xác nhận bên trái), dùng cho lần hỏi thứ hai
        /// của một việc không lấy lại được, để bấm nhanh hai lần cùng một chỗ không vượt qua cả hai lần hỏi.
        /// </summary>
        public static ConfirmDialog Show(Transform canvas, string message, string confirmLabel, Action onConfirm,
            bool confirmOnLeft = false)
        {
            var go = new GameObject("ConfirmDialog", typeof(RectTransform), typeof(Image), typeof(ConfirmDialog));
            go.transform.SetParent(canvas, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            var paper = go.GetComponent<Image>();
            paper.sprite = UiKit.WhiteSprite;
            paper.color = Palette.Paper;
            paper.raycastTarget = true;

            var dialog = go.GetComponent<ConfirmDialog>();
            dialog._onConfirm = onConfirm;
            dialog.Build(message, confirmLabel, confirmOnLeft);
            go.transform.SetAsLastSibling();
            return dialog;
        }

        private void Build(string message, string confirmLabel, bool confirmOnLeft)
        {
            Message = UiKit.CreateLabel(transform, message, 56f);
            var mrt = Message.rectTransform;
            mrt.anchorMin = mrt.anchorMax = new Vector2(.5f, .5f);
            mrt.sizeDelta = new Vector2(UiKit.SafeWidth - 160f, 300f);
            mrt.anchoredPosition = new Vector2(0f, 120f);

            var side = (ButtonWidth + ButtonGap) / 2f;
            CancelButton = UiKit.CreateButton(transform, UiText.Cancel, () => Close(false));
            Place((RectTransform)CancelButton.transform, new Vector2(confirmOnLeft ? side : -side, -160f));
            ConfirmButton = UiKit.CreateButton(transform, confirmLabel, () => Close(true));
            Place((RectTransform)ConfirmButton.transform, new Vector2(confirmOnLeft ? -side : side, -160f));
            ConfirmButton.transform.Find("Fill").GetComponent<Image>().color = Palette.StampRed;
        }

        private static void Place(RectTransform rt, Vector2 position)
        {
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(.5f, .5f);
            rt.sizeDelta = new Vector2(ButtonWidth, UiKit.MinTouch);
            rt.anchoredPosition = position;
        }

        private void Close(bool confirmed)
        {
            if (_closed) return;
            _closed = true;
            gameObject.SetActive(false);
            Destroy(gameObject);
            if (confirmed) _onConfirm?.Invoke();
        }
    }
}
