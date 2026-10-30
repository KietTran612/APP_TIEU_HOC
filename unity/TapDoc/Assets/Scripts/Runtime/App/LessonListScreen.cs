using System;
using System.Collections.Generic;
using System.Linq;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Danh sách bài của bé đang học, theo thứ tự <c>index.json</c>, xếp 6 cột, chia phần "Chữ cái và âm" / "Vần"
    /// (bản thiết kế giao diện mục 9.2). Bài đã học có hàng hoa bé ngoan nhỏ; bài đang học tới nền cam và nhún chậm;
    /// bài chưa mở có ổ khoá và không bấm được. Góc trên: hình đại diện của bé (đổi bé), nút Sổ bé ngoan, nút "Phụ
    /// huynh"; góc dưới trái: nút "Ôn lại" (chỉ bấm được khi bé có lượt nhầm); góc dưới phải: bạn gà con.
    /// Mở màn thì cuộn sẵn tới bài đang học tới.
    /// </summary>
    public class LessonListScreen : MonoBehaviour
    {
        private const int Columns = 6;
        private const float CardWidth = 216f;
        private const float CardHeight = 210f;
        private const float CardGap = 18f;
        private const float FlowerSize = 40f;
        private const float LockSize = 56f;
        private const float Margin = 20f;
        private const float ParentWidth = 280f;

        private readonly Dictionary<string, Button> _lessonButtons = new();

        internal Button ReviewButton { get; private set; }
        internal Button ParentButton { get; private set; }
        internal Button SwitchChildButton { get; private set; }
        internal Button BookButton { get; private set; }
        internal ScrollRect Scroll { get; private set; }
        internal int LessonCount => _lessonButtons.Count;

        /// <summary>Bài đang học tới: bài đầu tiên đã mở mà chưa học xong; <c>null</c> khi đã học hết.</summary>
        internal string CurrentLessonId { get; private set; }

        /// <summary>Thẻ của bài <paramref name="lessonId"/>; <c>null</c> nếu bài không có trong danh sách.</summary>
        internal Button ButtonFor(string lessonId) =>
            lessonId != null && _lessonButtons.TryGetValue(lessonId, out var b) ? b : null;

        public void Build(AppRoot app)
        {
            var progress = app.Progress;

            SwitchChildButton = UiKit.CreateIconButton(transform, app.Assets, progress.Current?.avatar, UiText.SwitchChild,
                app.ShowProfiles, Palette.PaperLight);
            Corner(SwitchChildButton, new Vector2(0f, 1f), new Vector2(Margin, -Margin));
            SwitchChildButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;

            ParentButton = UiKit.CreateButton(transform, UiText.Parent, app.ShowParent);
            Corner(ParentButton, Vector2.one, new Vector2(-Margin, -Margin));
            ((RectTransform)ParentButton.transform).sizeDelta = new Vector2(ParentWidth, UiKit.MinTouch);

            BookButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Book, UiText.Book, app.ShowBook,
                Palette.PaperLight);
            Corner(BookButton, Vector2.one, new Vector2(-(2f * Margin + ParentWidth), -Margin));
            BookButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;

            var header = UiKit.CreateLabel(transform, UiText.AppTitle, 64f);
            var headerRt = header.rectTransform;
            headerRt.anchorMin = new Vector2(0.5f, 1f);
            headerRt.anchorMax = new Vector2(0.5f, 1f);
            headerRt.pivot = new Vector2(0.5f, 1f);
            headerRt.sizeDelta = new Vector2(640f, UiKit.MinTouch);
            headerRt.anchoredPosition = new Vector2(-80f, -Margin);

            var scrollGo = new GameObject("LessonScroll", typeof(RectTransform), typeof(ScrollRect), typeof(Image), typeof(RectMask2D));
            scrollGo.transform.SetParent(transform, false);
            var viewport = (RectTransform)scrollGo.transform;
            viewport.anchorMin = new Vector2(0.5f, 0f);
            viewport.anchorMax = new Vector2(0.5f, 1f);
            // Thêm chỗ cho bóng gạch chéo của thẻ ở mép phải và mép dưới.
            viewport.sizeDelta = new Vector2(Columns * CardWidth + (Columns - 1) * CardGap + UiKit.ShadowOffset.x,
                -2f * (UiKit.MinTouch + 2f * Margin));
            viewport.anchoredPosition = Vector2.zero;
            scrollGo.GetComponent<Image>().color = Color.clear;
            var contentGo = new GameObject("Content", typeof(RectTransform), typeof(VerticalLayoutGroup), typeof(ContentSizeFitter));
            contentGo.transform.SetParent(viewport, false);
            var content = (RectTransform)contentGo.transform;
            content.anchorMin = new Vector2(0f, 1f);
            content.anchorMax = Vector2.one;
            content.pivot = new Vector2(0.5f, 1f);
            content.sizeDelta = Vector2.zero;
            content.anchoredPosition = Vector2.zero;
            var layout = contentGo.GetComponent<VerticalLayoutGroup>();
            layout.spacing = CardGap;
            layout.padding = new RectOffset(0, (int)UiKit.ShadowOffset.x, 0, (int)-UiKit.ShadowOffset.y);
            layout.childAlignment = TextAnchor.UpperLeft;
            layout.childControlWidth = true;
            layout.childControlHeight = true;
            layout.childForceExpandWidth = true;
            layout.childForceExpandHeight = false;
            contentGo.GetComponent<ContentSizeFitter>().verticalFit = ContentSizeFitter.FitMode.PreferredSize;
            Scroll = scrollGo.GetComponent<ScrollRect>();
            Scroll.viewport = viewport;
            Scroll.content = content;
            Scroll.horizontal = false;
            Scroll.vertical = true;
            Scroll.movementType = ScrollRect.MovementType.Clamped;

            var entries = LessonRepository.LoadIndex().lessons;
            var ordered = entries.Select(e => e.lesson_id).ToList();
            CurrentLessonId = ordered.FirstOrDefault(id => progress.IsUnlocked(ordered, id) && !progress.IsCompleted(id));
            foreach (var part in new[] { false, true })
            {
                var section = entries.Where(e => part ? e.lesson_no >= 42 : e.lesson_no >= 1 && e.lesson_no <= 41).ToList();
                if (section.Count == 0) continue;
                var sectionHeader = UiKit.CreateLabel(content, part ? UiText.PartRimes : UiText.PartLetters, 44f);
                sectionHeader.alignment = TextAlignmentOptions.Left;
                sectionHeader.gameObject.AddComponent<LayoutElement>().preferredHeight = 64f;
                var gridGo = new GameObject("LessonButtons", typeof(RectTransform), typeof(GridLayoutGroup));
                gridGo.transform.SetParent(content, false);
                var grid = gridGo.GetComponent<GridLayoutGroup>();
                grid.cellSize = new Vector2(CardWidth, CardHeight);
                grid.spacing = new Vector2(CardGap, CardGap);
                grid.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
                grid.constraintCount = Columns;
                grid.childAlignment = TextAnchor.UpperLeft;
                foreach (var entry in section)
                {
                    var lessonId = entry.lesson_id;
                    var label = $"{UiText.LessonPrefix} {entry.lesson_no}\n{entry.title}";
                    var btn = UiKit.CreateCardButton(gridGo.transform, label, () => app.ShowLesson(lessonId));
                    btn.name = $"Lesson_{lessonId}";
                    btn.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;
                    var text = btn.GetComponentInChildren<TMP_Text>();
                    var textRt = text.rectTransform;
                    textRt.anchorMin = new Vector2(0f, 0.24f);
                    textRt.anchorMax = Vector2.one;
                    textRt.offsetMin = new Vector2(8f, 0f);
                    textRt.offsetMax = new Vector2(-8f, -6f);

                    if (!progress.IsUnlocked(ordered, lessonId)) Lock(btn, app.Assets);
                    else if (lessonId == CurrentLessonId) MarkCurrent(btn);

                    var flowers = FlowerBook.FlowersFor(progress, lessonId);
                    if (flowers > 0) AddFlowers(btn.transform, app.Assets, lessonId, flowers);

                    _lessonButtons[lessonId] = btn;
                }
            }

            ReviewButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Review, UiText.ReviewMistakes, app.ShowReview);
            Corner(ReviewButton, Vector2.zero, new Vector2(Margin, Margin));
            ReviewButton.interactable = progress.Mistakes().Count > 0;
            ReviewButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;

            var mascot = Mascot.Create(transform, app.Assets);
            var mrt = (RectTransform)mascot.transform;
            mrt.anchorMin = mrt.anchorMax = mrt.pivot = new Vector2(1f, 0f);
            mrt.anchoredPosition = new Vector2(-Margin, Margin);

            Canvas.ForceUpdateCanvases();
            LayoutRebuilder.ForceRebuildLayoutImmediate(content);
            Scroll.verticalNormalizedPosition = 1f;
            ScrollTo(CurrentLessonId);
        }

        /// <summary>Cuộn để thẻ bài nằm trọn trong vùng nhìn; bỏ qua mã bài không có.</summary>
        internal void ScrollTo(string lessonId)
        {
            var button = ButtonFor(lessonId);
            if (button == null) return;
            Canvas.ForceUpdateCanvases();
            LayoutRebuilder.ForceRebuildLayoutImmediate(Scroll.content);
            var corners = new Vector3[4];
            ((RectTransform)button.transform).GetWorldCorners(corners);
            var bottom = Scroll.viewport.InverseTransformPoint(corners[0]).y;
            var top = Scroll.viewport.InverseTransformPoint(corners[1]).y;
            var rect = Scroll.viewport.rect;
            if (bottom >= rect.yMin && top <= rect.yMax) return;
            var position = Scroll.content.anchoredPosition;
            position.y += bottom < rect.yMin ? rect.yMin - bottom : rect.yMax - top;
            position.y = Mathf.Clamp(position.y, 0f, Mathf.Max(0f, Scroll.content.rect.height - rect.height));
            Scroll.StopMovement();
            Scroll.content.anchoredPosition = position;
        }

        private static void Corner(Button button, Vector2 corner, Vector2 offset)
        {
            var rt = (RectTransform)button.transform;
            rt.anchorMin = rt.anchorMax = rt.pivot = corner;
            rt.anchoredPosition = offset;
        }

        /// <summary>Bài đang học tới: nền cam nhạt, nhún chậm để bé biết bấm vào đâu.</summary>
        private static void MarkCurrent(Button card)
        {
            card.transform.Find("Fill").GetComponent<Image>().color = Palette.OrangeLight;
            Pulse.StartOn(card.transform);
        }

        /// <summary>Bài chưa mở: nền và chữ màu khoá, có ổ khoá, không bấm được (giữ màu, không làm xám cả thẻ).</summary>
        private static void Lock(Button card, AssetCatalog assets)
        {
            card.interactable = false;
            var colors = card.colors;
            colors.disabledColor = Color.white;
            card.colors = colors;
            card.transform.Find("Fill").GetComponent<Image>().color = Palette.LockedFill;
            card.transform.Find("Border").GetComponent<Image>().color = Palette.LockedInk;
            card.GetComponentInChildren<TMP_Text>().color = Palette.LockedInk;

            var go = new GameObject("Lock", typeof(RectTransform), typeof(Image));
            go.transform.SetParent(card.transform, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = rt.anchorMax = new Vector2(.5f, .14f);
            rt.sizeDelta = new Vector2(LockSize, LockSize);
            var img = go.GetComponent<Image>();
            img.sprite = assets.Image(SystemIcons.Lock);
            img.preserveAspect = true;
            img.raycastTarget = false;
        }

        /// <summary>Hàng <paramref name="count"/> bông hoa bé ngoan nhỏ ở đáy thẻ bài (thay hàng sao cũ).</summary>
        private static void AddFlowers(Transform card, AssetCatalog assets, string lessonId, int count)
        {
            var row = new GameObject("Flowers", typeof(RectTransform), typeof(HorizontalLayoutGroup));
            row.transform.SetParent(card, false);
            var rt = (RectTransform)row.transform;
            rt.anchorMin = new Vector2(0f, 0.03f);
            rt.anchorMax = new Vector2(1f, 0.24f);
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            var hlg = row.GetComponent<HorizontalLayoutGroup>();
            hlg.spacing = 6f;
            hlg.childAlignment = TextAnchor.MiddleCenter;
            hlg.childControlWidth = false;
            hlg.childControlHeight = false;
            hlg.childForceExpandWidth = false;
            hlg.childForceExpandHeight = false;
            for (var i = 0; i < count; i++)
            {
                var go = new GameObject("Flower", typeof(RectTransform), typeof(Image));
                go.transform.SetParent(row.transform, false);
                ((RectTransform)go.transform).sizeDelta = new Vector2(FlowerSize, FlowerSize);
                var img = go.GetComponent<Image>();
                img.sprite = assets.Image(FlowerBook.FlowerImage(lessonId, i));
                img.preserveAspect = true;
                img.raycastTarget = false;
            }
        }
    }
}
