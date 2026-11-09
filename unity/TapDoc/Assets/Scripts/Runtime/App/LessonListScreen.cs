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
        private const int MinColumns = 6;
        private const float CardWidth = 216f;
        private const float CardHeight = 210f;
        private const float CardGap = 18f;
        private const float MinCardFont = 22f; // tên bài chính tả tập 2 dài nhất ("Chim non chăm học – Dưới ánh trăng") vừa 4 dòng
        private const float FlowerSize = 40f;
        private const float LockSize = 56f;
        private const float Margin = 20f;
        private const float ParentWidth = 280f;

        private readonly Dictionary<string, Button> _lessonButtons = new();

        /// <summary>Quyển đang hiện (bản thiết kế Tủ sách mục 6): danh sách chỉ có bài của quyển này.</summary>
        internal string BookId { get; private set; }

        /// <summary>Lớp của quyển đang hiện: lớp 1 chia theo phần, lớp 2 theo chủ điểm.</summary>
        private int _grade = 1;

        internal Button ReviewButton { get; private set; }
        internal Button ParentButton { get; private set; }
        /// <summary>Nút về Tủ sách (góc trên trái; nút đổi bé nằm ở Tủ sách).</summary>
        internal Button ShelfButton { get; private set; }
        internal Button BookButton { get; private set; }
        internal Button SettingsButton { get; private set; }
        internal TMP_Text Header { get; private set; }
        internal ScrollRect Scroll { get; private set; }

        /// <summary>Số cột thẻ bài hiện tại (6 trên máy tính bảng, nhiều hơn trên màn rộng).</summary>
        internal int Columns { get; private set; } = MinColumns;

        /// <summary>Số cột vừa khung rộng <paramref name="width"/>, không ít hơn 6.</summary>
        internal static int ColumnsFor(float width) =>
            Mathf.Max(MinColumns, Mathf.FloorToInt((width - 2f * Margin + CardGap) / (CardWidth + CardGap)));

        private static float ViewportWidth(int columns) =>
            columns * CardWidth + (columns - 1) * CardGap + UiKit.ShadowOffset.x;
        internal int LessonCount => _lessonButtons.Count;

        /// <summary>Bài đang học tới: bài đầu tiên đã mở mà chưa học xong; <c>null</c> khi đã học hết.</summary>
        internal string CurrentLessonId { get; private set; }

        /// <summary>Thẻ của bài <paramref name="lessonId"/>; <c>null</c> nếu bài không có trong danh sách.</summary>
        internal Button ButtonFor(string lessonId) =>
            lessonId != null && _lessonButtons.TryGetValue(lessonId, out var b) ? b : null;

        public void Build(AppRoot app)
        {
            var progress = app.Progress;

            ShelfButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Shelf, UiText.Shelf, app.ShowShelf,
                Palette.PaperLight);
            Corner(ShelfButton, new Vector2(0f, 1f), new Vector2(Margin, -Margin));
            ShelfButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;

            ParentButton = UiKit.CreateButton(transform, UiText.Parent, app.ShowParent);
            Corner(ParentButton, Vector2.one, new Vector2(-Margin, -Margin));
            ((RectTransform)ParentButton.transform).sizeDelta = new Vector2(ParentWidth, UiKit.MinTouch);

            BookButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Book, UiText.Book, app.ShowBook,
                Palette.PaperLight);
            Corner(BookButton, Vector2.one, new Vector2(-(2f * Margin + ParentWidth), -Margin));
            BookButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;

            // Bánh răng mở menu Cài đặt, bên trái nút Sổ bé ngoan.
            SettingsButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Settings, UiText.Settings,
                () => app.ShowSettings(app.ShowLessonList), Palette.PaperLight);
            Corner(SettingsButton, Vector2.one, new Vector2(-(3f * Margin + ParentWidth + UiKit.MinTouch), -Margin));
            SettingsButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;

            var index = app.Lessons.Index;
            BookId = progress.OpenBook ?? BookShelf.CurrentBookId(index, progress);
            var book = BookShelf.Book(index, BookId);
            var header = UiKit.CreateLabel(transform, book?.title ?? UiText.AppTitle, 64f);
            Header = header;
            var headerRt = header.rectTransform;
            headerRt.anchorMin = new Vector2(0.5f, 1f);
            headerRt.anchorMax = new Vector2(0.5f, 1f);
            headerRt.pivot = new Vector2(0.5f, 1f);
            // Giữa nút Tủ sách (trái) và hàng nút bánh răng, Sổ, Phụ huynh (phải).
            headerRt.sizeDelta = new Vector2(540f, UiKit.MinTouch);
            headerRt.anchoredPosition = new Vector2(-240f, -Margin);

            var scrollGo = new GameObject("LessonScroll", typeof(RectTransform), typeof(ScrollRect), typeof(Image), typeof(RectMask2D));
            scrollGo.transform.SetParent(transform, false);
            var viewport = (RectTransform)scrollGo.transform;
            viewport.anchorMin = new Vector2(0.5f, 0f);
            viewport.anchorMax = new Vector2(0.5f, 1f);
            // Thêm chỗ cho bóng gạch chéo của thẻ ở mép phải và mép dưới.
            Columns = ColumnsFor(((RectTransform)transform).rect.width);
            viewport.sizeDelta = new Vector2(ViewportWidth(Columns), -2f * (UiKit.MinTouch + 2f * Margin));
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

            // Chỉ bài của quyển đang mở; mở bài theo luật Tủ sách (quyển phải mở, bài trước phải xong).
            var entries = index.lessons.Where(e => e.book == BookId).ToList();
            _grade = book?.grade > 0 ? book.grade : entries.Count > 0 ? entries[0].EffectiveGrade : 1;
            // Tính một lần cho cả danh sách: quyển có mở không, rồi chuỗi bài trong quyển.
            var ordered = entries.Select(e => e.lesson_id).ToList();
            var unlocked = BookShelf.IsBookUnlocked(index, progress, BookId)
                ? new HashSet<string>(ordered.Where(id => progress.IsUnlocked(ordered, id)))
                : new HashSet<string>();
            CurrentLessonId = ordered.FirstOrDefault(id => unlocked.Contains(id) && !progress.IsCompleted(id));
            foreach (var (title, section, byWeek) in Sections(entries))
            {
                var sectionHeader = UiKit.CreateLabel(content, title, 44f);
                sectionHeader.alignment = TextAlignmentOptions.Left;
                sectionHeader.gameObject.AddComponent<LayoutElement>().preferredHeight = 64f;
                // Phần Tập đọc và lớp 2 chia nhóm theo tuần như mục lục sách; hai phần đầu lớp 1 là một lưới.
                foreach (var group in section.GroupBy(e => byWeek ? e.week : 0))
                {
                    if (byWeek && group.Key > 0)
                    {
                        var weekHeader = UiKit.CreateLabel(content, string.Format(UiText.WeekFormat, group.Key), 34f);
                        weekHeader.alignment = TextAlignmentOptions.Left;
                        weekHeader.gameObject.AddComponent<LayoutElement>().preferredHeight = 48f;
                    }
                    var grid = CreateGrid(content, Columns);
                    foreach (var entry in group) AddCard(grid, entry, unlocked, progress, app);
                }
            }

            ReviewButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Review, UiText.ReviewMistakes, app.ShowReview);
            Corner(ReviewButton, Vector2.zero, new Vector2(Margin, Margin));
            // Chỉ ôn lượt nhầm của quyển đang mở (bản thiết kế Tủ sách mục 7).
            var bookLessons = new HashSet<string>(entries.Select(e => e.lesson_id));
            ReviewButton.interactable = progress.Mistakes(int.MaxValue).Any(m => bookLessons.Contains(m.lesson_id));
            ReviewButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;

            var mascot = Mascot.Create(transform, app.Assets);
            var mrt = (RectTransform)mascot.transform;
            mrt.anchorMin = mrt.anchorMax = mrt.pivot = new Vector2(1f, 0f);
            mrt.anchoredPosition = new Vector2(-Margin, Margin);

            Canvas.ForceUpdateCanvases();
            LayoutRebuilder.ForceRebuildLayoutImmediate(content);
            Scroll.verticalNormalizedPosition = 1f;
            ScrollTo(CurrentLessonId);

            // Xoay máy, đổi cỡ cửa sổ: đổi số cột tại chỗ, giữ bài đang xem trong vùng nhìn.
            FrameWatcher.On(gameObject).Changed += size => ApplyColumns(size.x);
        }

        /// <summary>Đặt lại số cột theo khung rộng <paramref name="width"/>; bài đang ở đầu vùng nhìn vẫn ở đầu.</summary>
        private void ApplyColumns(float width)
        {
            var columns = ColumnsFor(width);
            if (columns == Columns) return;
            var anchor = TopVisibleLesson();
            Columns = columns;
            var viewport = Scroll.viewport;
            viewport.sizeDelta = new Vector2(ViewportWidth(columns), viewport.sizeDelta.y);
            foreach (var grid in Scroll.content.GetComponentsInChildren<GridLayoutGroup>()) grid.constraintCount = columns;
            Canvas.ForceUpdateCanvases();
            LayoutRebuilder.ForceRebuildLayoutImmediate(Scroll.content);
            if (anchor != null) ScrollToTop(anchor);
        }

        /// <summary>Bài đầu tiên (theo thứ tự) có đỉnh thẻ nằm trong vùng nhìn.</summary>
        private string TopVisibleLesson()
        {
            var view = Scroll.viewport.rect;
            var corners = new Vector3[4];
            foreach (var pair in _lessonButtons)
            {
                ((RectTransform)pair.Value.transform).GetWorldCorners(corners);
                var top = Scroll.viewport.InverseTransformPoint(corners[1]).y;
                if (top <= view.yMax + 1f && top >= view.yMin) return pair.Key;
            }
            return null;
        }

        /// <summary>Cuộn để đỉnh thẻ bài <paramref name="lessonId"/> nằm ở đỉnh vùng nhìn (trong giới hạn cuộn).</summary>
        private void ScrollToTop(string lessonId)
        {
            var button = ButtonFor(lessonId);
            if (button == null) return;
            var corners = new Vector3[4];
            ((RectTransform)button.transform).GetWorldCorners(corners);
            var top = Scroll.viewport.InverseTransformPoint(corners[1]).y;
            var view = Scroll.viewport.rect;
            var position = Scroll.content.anchoredPosition;
            position.y += view.yMax - top;
            position.y = Mathf.Clamp(position.y, 0f, Mathf.Max(0f, Scroll.content.rect.height - view.height));
            Scroll.StopMovement();
            Scroll.content.anchoredPosition = position;
        }

        private const string ReadingPart = "tap_doc";

        /// <summary>
        /// Các phần của lớp đang hiện: lớp 1 theo <c>part</c> (ba phần cố định), lớp 2 theo chủ điểm (thứ tự xuất hiện).
        /// Bài lớp 1 không thuộc phần nào vẫn hiện ở cuối, để chuỗi mở khoá không bị đứt.
        /// </summary>
        private IEnumerable<(string title, List<LessonEntry> lessons, bool byWeek)> Sections(List<LessonEntry> entries)
        {
            if (_grade == 2)
            {
                foreach (var group in entries.GroupBy(e => e.theme ?? string.Empty))
                {
                    yield return (string.IsNullOrEmpty(group.Key) ? UiText.PartReading : group.Key, group.ToList(), true);
                }
                yield break;
            }
            foreach (var (part, title) in Parts)
            {
                var section = entries.Where(e => PartOf(e) == part).ToList();
                if (section.Count > 0) yield return (title, section, part == ReadingPart);
            }
            var known = new HashSet<string>(Parts.Select(p => p.part));
            var other = entries.Where(e => !known.Contains(PartOf(e))).ToList();
            if (other.Count > 0) yield return (UiText.PartReading, other, true);
        }

        private static readonly (string part, string title)[] Parts =
        {
            ("chu_cai", UiText.PartLetters),
            ("van", UiText.PartRimes),
            (ReadingPart, UiText.PartReading),
        };

        /// <summary>Phần của bài theo <c>index.json</c>; index cũ chưa ghi phần thì chia theo số bài như trước.</summary>
        private static string PartOf(LessonEntry entry)
        {
            if (!string.IsNullOrEmpty(entry.part)) return entry.part;
            return entry.lesson_no >= 42 ? "van" : "chu_cai";
        }

        /// <summary>Nhãn trên thẻ: lấy từ <c>index.json</c>, không có thì "Bài N".</summary>
        internal static string LabelOf(LessonEntry entry) =>
            string.IsNullOrEmpty(entry.label) ? $"{UiText.LessonPrefix} {entry.lesson_no}" : entry.label;

        private static Transform CreateGrid(Transform content, int columns)
        {
            var gridGo = new GameObject("LessonButtons", typeof(RectTransform), typeof(GridLayoutGroup));
            gridGo.transform.SetParent(content, false);
            var grid = gridGo.GetComponent<GridLayoutGroup>();
            grid.cellSize = new Vector2(CardWidth, CardHeight);
            grid.spacing = new Vector2(CardGap, CardGap);
            grid.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
            grid.constraintCount = columns;
            grid.childAlignment = TextAnchor.UpperLeft;
            return gridGo.transform;
        }

        private void AddCard(Transform grid, LessonEntry entry, ISet<string> unlocked, ProgressStore progress, AppRoot app)
        {
            var lessonId = entry.lesson_id;
            var label = LabelOf(entry) + "\n" + entry.title;
            var btn = UiKit.CreateCardButton(grid, label, () => app.ShowLesson(lessonId));
            btn.name = $"Lesson_{lessonId}";
            btn.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;
            var text = btn.GetComponentInChildren<TMP_Text>();
            var textRt = text.rectTransform;
            textRt.anchorMin = new Vector2(0f, 0.24f);
            textRt.anchorMax = Vector2.one;
            textRt.offsetMin = new Vector2(8f, 0f);
            textRt.offsetMax = new Vector2(-8f, -6f);
            // Tên bài tập đọc dài ("Người nông dân và con gấu"): cho chữ tự thu nhỏ trong thẻ, không tràn.
            text.enableAutoSizing = true;
            text.fontSizeMax = text.fontSize;
            text.fontSizeMin = Mathf.Min(text.fontSize, MinCardFont);

            if (!unlocked.Contains(lessonId)) Lock(btn, app.Assets);
            else if (lessonId == CurrentLessonId) MarkCurrent(btn);

            var flowers = FlowerBook.FlowersFor(progress, lessonId);
            if (flowers > 0) AddFlowers(btn.transform, app.Assets, lessonId, flowers);

            _lessonButtons[lessonId] = btn;
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
