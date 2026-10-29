using System;
using System.Collections.Generic;
using System.Linq;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Danh sách bài của bé đang học, theo thứ tự <c>index.json</c>, xếp 6 cột. Bài bị khóa hiện mờ và không bấm
    /// được; bài đã học hiện sao. Hai góc trên có nút "Đổi bé" và "Phụ huynh"; dưới cùng là nút "Ôn lại", chỉ bấm
    /// được khi bé có lượt nhầm.
    /// </summary>
    public class LessonListScreen : MonoBehaviour
    {
        private const int Columns = 6;
        private const float CardWidth = 216f;
        private const float CardHeight = 210f;
        private const float CardGap = 18f;
        private const float StarSize = 40f;
        private const float LockedAlpha = 0.45f;

        private readonly Dictionary<string, Button> _lessonButtons = new();

        internal Button ReviewButton { get; private set; }
        internal Button ParentButton { get; private set; }
        internal Button SwitchChildButton { get; private set; }
        internal ScrollRect Scroll { get; private set; }
        internal int LessonCount => _lessonButtons.Count;

        /// <summary>Thẻ của bài <paramref name="lessonId"/>; <c>null</c> nếu bài không có trong danh sách.</summary>
        internal Button ButtonFor(string lessonId) =>
            lessonId != null && _lessonButtons.TryGetValue(lessonId, out var b) ? b : null;

        public void Build(AppRoot app)
        {
            var progress = app.Progress;

            SwitchChildButton = CornerButton(UiText.SwitchChild, 0f, 240f, app.ShowProfiles);
            ParentButton = CornerButton(UiText.Parent, 1f, 280f, app.ShowParent);

            var header = UiKit.CreateLabel(transform, UiText.AppTitle, 64f);
            var headerRt = header.rectTransform;
            headerRt.anchorMin = new Vector2(0.5f, 1f);
            headerRt.anchorMax = new Vector2(0.5f, 1f);
            headerRt.pivot = new Vector2(0.5f, 1f);
            headerRt.sizeDelta = new Vector2(800f, UiKit.MinTouch);
            headerRt.anchoredPosition = new Vector2(0f, -20f);

            var scrollGo = new GameObject("LessonScroll", typeof(RectTransform), typeof(ScrollRect), typeof(Image), typeof(RectMask2D));
            scrollGo.transform.SetParent(transform, false);
            var viewport = (RectTransform)scrollGo.transform;
            viewport.anchorMin = new Vector2(0.5f, 0f);
            viewport.anchorMax = new Vector2(0.5f, 1f);
            viewport.sizeDelta = new Vector2(Columns * CardWidth + (Columns - 1) * CardGap, -2f * (UiKit.MinTouch + 40f));
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
                    var btn = UiKit.CreateButton(gridGo.transform, label, () => app.ShowLesson(lessonId));
                    btn.name = $"Lesson_{lessonId}";
                    var text = btn.GetComponentInChildren<TMP_Text>();
                    var textRt = text.rectTransform;
                    textRt.anchorMin = new Vector2(0f, 0.24f);
                    textRt.anchorMax = Vector2.one;
                    textRt.offsetMin = new Vector2(8f, 0f);
                    textRt.offsetMax = new Vector2(-8f, -6f);

                    if (!progress.IsUnlocked(ordered, lessonId))
                    {
                        btn.interactable = false;
                        btn.gameObject.AddComponent<CanvasGroup>().alpha = LockedAlpha;
                    }

                    var stars = progress.StarsFor(lessonId);
                    if (stars > 0) AddStars(btn.transform, app.Assets, stars);

                    _lessonButtons[lessonId] = btn;
                }
            }

            ReviewButton = UiKit.CreateButton(transform, UiText.ReviewMistakes, app.ShowReview);
            var reviewRt = (RectTransform)ReviewButton.transform;
            reviewRt.anchorMin = new Vector2(0.5f, 0f);
            reviewRt.anchorMax = new Vector2(0.5f, 0f);
            reviewRt.pivot = new Vector2(0.5f, 0f);
            reviewRt.sizeDelta = new Vector2(360f, UiKit.MinTouch);
            reviewRt.anchoredPosition = new Vector2(0f, 20f);
            ReviewButton.interactable = progress.Mistakes().Count > 0;
            Canvas.ForceUpdateCanvases();
            LayoutRebuilder.ForceRebuildLayoutImmediate(content);
            Scroll.verticalNormalizedPosition = 1f;
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

        /// <summary>Nút ở góc trên (<paramref name="side"/> 0 là trái, 1 là phải), cao đúng <see cref="UiKit.MinTouch"/>.</summary>
        private Button CornerButton(string label, float side, float width, Action onClick)
        {
            var btn = UiKit.CreateButton(transform, label, onClick);
            var rt = (RectTransform)btn.transform;
            rt.anchorMin = new Vector2(side, 1f);
            rt.anchorMax = new Vector2(side, 1f);
            rt.pivot = new Vector2(side, 1f);
            rt.sizeDelta = new Vector2(width, UiKit.MinTouch);
            rt.anchoredPosition = new Vector2(side < 0.5f ? 20f : -20f, -20f);
            return btn;
        }

        /// <summary>Hàng <paramref name="count"/> ngôi sao ở đáy thẻ bài.</summary>
        private static void AddStars(Transform card, AssetCatalog assets, int count)
        {
            var row = new GameObject("Stars", typeof(RectTransform), typeof(HorizontalLayoutGroup));
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
                MarkerIcon.CreateStar(row.transform, assets, StarSize);
            }
        }
    }
}
