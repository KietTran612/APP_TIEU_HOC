using System.Linq;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Màn Sổ bé ngoan (bản thiết kế giao diện mục 8.5): tiêu đề "Sổ bé ngoan của …", quyển sổ hai trang mở ở bài học
    /// xong đứng sau cùng, nút lật trang hai bên (hết trang thì mờ), vuốt ngang để lật, nút nhà về danh sách bài.
    /// </summary>
    public class BookScreen : MonoBehaviour, IBeginDragHandler, IDragHandler, IEndDragHandler
    {
        /// <summary>Vuốt ngang quá chừng này (đơn vị canvas) thì lật trang.</summary>
        public const float SwipeDistance = 120f;

        private const float TopBand = 200f;
        private const float BottomBand = 200f;
        private const float Margin = 20f;

        public BookSpread Spread { get; private set; }
        public Button HomeButton { get; private set; }
        public Button PrevButton { get; private set; }
        public Button NextButton { get; private set; }

        public void Build(AppRoot app)
        {
            // Nền trong suốt phủ màn để nhận thao tác vuốt.
            var catcher = gameObject.AddComponent<Image>();
            catcher.color = Color.clear;

            HomeButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Home, UiText.Back, app.ShowLessonList);
            Place(HomeButton, new Vector2(0f, 1f), new Vector2(Margin, -Margin));

            var title = UiKit.CreateLabel(transform, string.Format(UiText.BookTitleFormat, app.Progress.Current?.name), 56f);
            title.textWrappingMode = TextWrappingModes.NoWrap;
            var trt = title.rectTransform;
            trt.anchorMin = trt.anchorMax = trt.pivot = new Vector2(.5f, 1f);
            trt.sizeDelta = new Vector2(UiKit.SafeWidth - 2f * (UiKit.MinTouch + 2f * Margin), UiKit.MinTouch);
            trt.anchoredPosition = new Vector2(0f, -Margin);

            var bookArea = new GameObject("BookArea", typeof(RectTransform));
            bookArea.transform.SetParent(transform, false);
            var brt = (RectTransform)bookArea.transform;
            brt.anchorMin = Vector2.zero;
            brt.anchorMax = Vector2.one;
            brt.offsetMin = new Vector2(Margin, BottomBand);
            brt.offsetMax = new Vector2(-Margin, -TopBand);
            var entries = LessonRepository.LoadIndex().lessons;
            Spread = BookSpread.Create(brt, entries, app.Progress, app.Assets);
            Spread.ShowPage(FlowerBook.StartPage(app.Progress, entries.Select(e => e.lesson_id).ToList()));

            PrevButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Backward, UiText.PagePrev,
                () => Flip(-2), Palette.PaperLight);
            Place(PrevButton, Vector2.zero, new Vector2(Margin, Margin));
            NextButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Forward, UiText.PageNext,
                () => Flip(2), Palette.Orange);
            Place(NextButton, new Vector2(1f, 0f), new Vector2(-Margin, Margin));
            RefreshButtons();
        }

        private static void Place(Button button, Vector2 corner, Vector2 offset)
        {
            var rt = (RectTransform)button.transform;
            rt.anchorMin = rt.anchorMax = rt.pivot = corner;
            rt.anchoredPosition = offset;
        }

        private void Flip(int delta)
        {
            var target = Spread.LeftPage + delta;
            if (target < 0 || target >= Spread.PageCount) return;
            _ = Spread.FlipTo(target);
            RefreshButtons();
        }

        /// <summary>Nút lật mờ đi ở trang đầu và trang cuối.</summary>
        public void RefreshButtons()
        {
            PrevButton.interactable = Spread.LeftPage > 0;
            NextButton.interactable = Spread.LeftPage + 2 < Spread.PageCount;
        }

        public void OnBeginDrag(PointerEventData eventData)
        {
        }

        public void OnDrag(PointerEventData eventData)
        {
        }

        public void OnEndDrag(PointerEventData eventData)
        {
            var canvas = GetComponentInParent<Canvas>();
            var scale = canvas != null && canvas.scaleFactor > 0f ? canvas.scaleFactor : 1f;
            var dx = (eventData.position.x - eventData.pressPosition.x) / scale;
            if (dx <= -SwipeDistance) Flip(2);
            else if (dx >= SwipeDistance) Flip(-2);
        }
    }
}
