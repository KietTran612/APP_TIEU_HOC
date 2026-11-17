using System;
using System.Collections.Generic;
using System.Linq;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Con đường bài học của quyển đang mở (bản thiết kế nâng cấp UI mục 4.2): mỗi bài là một trạm tròn trên con đường
    /// lượn ngang, theo thứ tự <c>index.json</c>; đầu mỗi chặng (lớp 1: phần "Chữ cái và âm", "Vần", "Tập đọc"; lớp 2:
    /// chủ điểm) có biển chặng. Bài đã học có hoa bé ngoan; bài đang học tới to hơn, nền cam, nhún chậm, gà con đứng
    /// trên; bài chưa mở màu khoá, có ổ khoá, không bấm được. Lớp 1 ghi chữ của bài trong trạm; bài tên dài (lớp 2, tập
    /// đọc) ghi nhãn ngắn trong trạm, tên bài nhỏ bên dưới. Cuộn ngang (tự cuộn tới bài đang học) và hai nút mũi tên to
    /// nhảy từng chặng. Góc trên: Tủ sách, tên quyển, bánh răng, Sổ bé ngoan, "Phụ huynh"; góc dưới: "Ôn lại" (trái),
    /// "Học tiếp" (phải). Nút của bé chừa ít nhất 48 tới mép bên và mép dưới.
    /// </summary>
    public class LessonListScreen : MonoBehaviour
    {
        public const float NodeSize = 200f;
        public const float CurrentNodeSize = 230f;
        public const float NodeStep = 260f;
        public const float WaveAmplitude = 90f;
        private const float WavePhase = .8f;
        private const float SignGap = 380f;
        private const float PadX = 140f;
        private const float PathCenterY = -20f;
        private const float RoadWidth = 54f;
        private const float CaptionWidth = 250f;
        private const float CaptionHeight = 72f;
        private const float MascotSize = 130f;
        private const float FlowerSize = 36f;
        private const float LockSize = 52f;
        private const float TypeIconSize = 56f;
        private const float Margin = 20f;
        private const float ParentWidth = 280f;
        private const float ContinueWidth = 400f;
        private const int CircleTitleMaxLength = 10;
        private static readonly Color RoadColor = new(.886f, .839f, .722f); // #E2D6B8, đất nhạt

        private readonly Dictionary<string, Button> _lessonButtons = new();
        private readonly List<float> _sectionStarts = new();
        private RectTransform _content;
        private float _contentWidth;
        private string _focusLesson;
        private bool _placed;
        private const float WeekRowY = -306f;

        /// <summary>Quyển đang hiện (bản thiết kế Tủ sách mục 6): đường chỉ có bài của quyển này.</summary>
        internal string BookId { get; private set; }

        /// <summary>Lớp của quyển đang hiện: lớp 1 chia chặng theo phần, lớp 2 theo chủ điểm.</summary>
        private int _grade = 1;

        internal Button ReviewButton { get; private set; }
        internal Button ParentButton { get; private set; }
        /// <summary>Nút về Tủ sách (góc trên trái; nút đổi bé nằm ở Tủ sách).</summary>
        internal Button ShelfButton { get; private set; }
        internal Button BookButton { get; private set; }
        internal Button SettingsButton { get; private set; }
        /// <summary>Nút to "Học tiếp": vào thẳng bài đang học tới.</summary>
        internal Button ContinueButton { get; private set; }
        /// <summary>Nút lật về chặng trước.</summary>
        internal Button PrevButton { get; private set; }
        /// <summary>Nút lật sang chặng sau.</summary>
        internal Button NextButton { get; private set; }
        internal TMP_Text Header { get; private set; }
        internal ScrollRect Scroll { get; private set; }
        /// <summary>Gà con, đứng trên bài đang học tới (hoặc bài cuối khi đã học hết).</summary>
        internal Mascot Mascot { get; private set; }

        internal int LessonCount => _lessonButtons.Count;

        /// <summary>Số chặng (biển chặng) trên đường.</summary>
        internal int SectionCount => _sectionStarts.Count;

        /// <summary>Bài đang học tới: bài đầu tiên đã mở mà chưa học xong; <c>null</c> khi đã học hết.</summary>
        internal string CurrentLessonId { get; private set; }

        /// <summary>Trạm của bài <paramref name="lessonId"/>; <c>null</c> nếu bài không có trên đường.</summary>
        internal Button ButtonFor(string lessonId) =>
            lessonId != null && _lessonButtons.TryGetValue(lessonId, out var b) ? b : null;

        public void Build(AppRoot app)
        {
            var progress = app.Progress;
            var gap = ScreenLayout.EdgeGap;

            ShelfButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Shelf, UiText.Shelf, app.ShowShelf,
                Palette.PaperLight);
            Corner(ShelfButton, new Vector2(0f, 1f), new Vector2(gap, -Margin));
            ShelfButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;

            ParentButton = UiKit.CreateButton(transform, UiText.Parent, app.ShowParent);
            Corner(ParentButton, Vector2.one, new Vector2(-gap, -Margin));
            ((RectTransform)ParentButton.transform).sizeDelta = new Vector2(ParentWidth, UiKit.MinTouch);

            BookButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Book, UiText.Book, app.ShowBook,
                Palette.PaperLight);
            Corner(BookButton, Vector2.one, new Vector2(-(gap + Margin + ParentWidth), -Margin));
            BookButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;

            // Bánh răng mở menu Cài đặt, bên trái nút Sổ bé ngoan.
            SettingsButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Settings, UiText.Settings,
                () => app.ShowSettings(app.ShowLessonList), Palette.PaperLight);
            Corner(SettingsButton, Vector2.one, new Vector2(-(gap + 2f * Margin + ParentWidth + UiKit.MinTouch), -Margin));
            SettingsButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;

            var index = app.Lessons.Index;
            BookId = progress.OpenBook ?? BookShelf.CurrentBookId(index, progress);
            var book = BookShelf.Book(index, BookId);
            Header = UiKit.CreateLabel(transform, book?.title ?? UiText.AppTitle, 64f);
            var headerRt = Header.rectTransform;
            headerRt.anchorMin = headerRt.anchorMax = headerRt.pivot = new Vector2(0.5f, 1f);
            // Giữa nút Tủ sách (trái) và hàng nút bánh răng, Sổ, Phụ huynh (phải).
            headerRt.sizeDelta = new Vector2(540f, UiKit.MinTouch);
            headerRt.anchoredPosition = new Vector2(-240f, -Margin);

            BuildScroll(gap, app.Assets);

            // Chỉ bài của quyển đang mở; mở bài theo luật Tủ sách (quyển phải mở, bài trước phải xong).
            var entries = index.lessons.Where(e => e.book == BookId).ToList();
            _grade = book?.grade > 0 ? book.grade : entries.Count > 0 ? entries[0].EffectiveGrade : 1;
            var ordered = entries.Select(e => e.lesson_id).ToList();
            var unlocked = BookShelf.IsBookUnlocked(index, progress, BookId)
                ? new HashSet<string>(ordered.Where(id => progress.IsUnlocked(ordered, id)))
                : new HashSet<string>();
            CurrentLessonId = ordered.FirstOrDefault(id => unlocked.Contains(id) && !progress.IsCompleted(id));
            BuildPath(app, entries, unlocked, progress);

            ReviewButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Review, UiText.ReviewMistakes, app.ShowReview);
            Corner(ReviewButton, Vector2.zero, new Vector2(gap, gap));
            // Chỉ ôn lượt nhầm của quyển đang mở (bản thiết kế Tủ sách mục 7).
            var bookLessons = new HashSet<string>(ordered);
            ReviewButton.interactable = progress.Mistakes(int.MaxValue).Any(m => bookLessons.Contains(m.lesson_id));
            ReviewButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;

            ContinueButton = CreateContinueButton(app);
            Corner(ContinueButton, new Vector2(1f, 0f), new Vector2(-gap, gap));
            ContinueButton.gameObject.SetActive(CurrentLessonId != null);

            // Học hết quyển thì mở ở đầu đường (gà con vẫn đứng ở bài cuối).
            _focusLesson = CurrentLessonId;
            // Đặt bài đang học vào vùng nhìn ở khung hình đầu (LateUpdate), khi vùng nhìn đã có bề rộng thật.
            Scroll.onValueChanged.AddListener(_ => OnScrolled());

            // Xoay máy, đổi cỡ cửa sổ: giữ bài đang học trong vùng nhìn.
            FrameWatcher.On(gameObject).Changed += _ =>
            {
                Canvas.ForceUpdateCanvases();
                CenterOn(_focusLesson ?? CurrentLessonId);
                RefreshArrows();
            };
        }

        /// <summary>
        /// Lúc mở màn: đặt bài đang học vào vùng nhìn và bật gợi ý mũi tên. Gọi lại ở khung hình đầu nếu lúc dựng vùng nhìn
        /// chưa có bề rộng thật; bỏ qua nếu đã có lệnh cuộn khác (<see cref="ScrollTo"/>, lật chặng).
        /// </summary>
        private void PlaceInitial()
        {
            if (_placed || Scroll == null) return;
            Canvas.ForceUpdateCanvases();
            if (Scroll.viewport.rect.width < 1f) return;
            _placed = true;
            if (_focusLesson != null) CenterOn(_focusLesson);
            else SetLeft(0f);
            // Còn đường phía sau: mũi tên nhún nhẹ gợi ý hướng vuốt, tới khi bé cuộn hay bấm lật.
            if (NextButton.interactable) Pulse.StartOn(NextButton.transform);
        }

        private void LateUpdate()
        {
            if (!_placed) PlaceInitial();
        }

        private void BuildScroll(float gap, AssetCatalog assets)
        {
            var side = gap + UiKit.MinTouch + 16f;
            PrevButton = UiKit.CreateIconButton(transform, assets, SystemIcons.Backward, UiText.PrevStage, () => JumpSection(-1),
                Palette.PaperLight);
            NextButton = UiKit.CreateIconButton(transform, assets, SystemIcons.Forward, UiText.NextStage, () => JumpSection(1),
                Palette.PaperLight);

            var scrollGo = new GameObject("LessonScroll", typeof(RectTransform), typeof(ScrollRect), typeof(Image), typeof(RectMask2D));
            scrollGo.transform.SetParent(transform, false);
            var viewport = (RectTransform)scrollGo.transform;
            viewport.anchorMin = Vector2.zero;
            viewport.anchorMax = Vector2.one;
            viewport.offsetMin = new Vector2(side, gap + UiKit.MinTouch + 10f);
            viewport.offsetMax = new Vector2(-side, -(Margin + UiKit.MinTouch + 10f));
            scrollGo.GetComponent<Image>().color = Color.clear;

            var contentGo = new GameObject("Content", typeof(RectTransform));
            contentGo.transform.SetParent(viewport, false);
            _content = (RectTransform)contentGo.transform;
            _content.anchorMin = new Vector2(0f, 0f);
            _content.anchorMax = new Vector2(0f, 1f);
            _content.pivot = new Vector2(0f, .5f);
            _content.anchoredPosition = Vector2.zero;

            Scroll = scrollGo.GetComponent<ScrollRect>();
            Scroll.viewport = viewport;
            Scroll.content = _content;
            Scroll.horizontal = true;
            Scroll.vertical = false;
            Scroll.movementType = ScrollRect.MovementType.Clamped;

            // Mũi tên lật chặng ở hai bên, giữa chiều cao vùng đường; cách mép bên ít nhất 48.
            foreach (var (button, corner, x) in new[]
                     {
                         (PrevButton, new Vector2(0f, .5f), gap),
                         (NextButton, new Vector2(1f, .5f), -gap)
                     })
            {
                var rt = (RectTransform)button.transform;
                rt.anchorMin = rt.anchorMax = rt.pivot = corner;
                var mid = ((gap + UiKit.MinTouch + 10f) - (Margin + UiKit.MinTouch + 10f)) / 2f;
                rt.anchoredPosition = new Vector2(x, mid);
                button.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;
            }
        }

        private Button CreateContinueButton(AppRoot app)
        {
            var button = UiKit.CreateButton(transform, UiText.ContinueLearning, () =>
            {
                if (CurrentLessonId != null) app.ShowLesson(CurrentLessonId);
            });
            button.name = "ContinueButton";
            ((RectTransform)button.transform).sizeDelta = new Vector2(ContinueWidth, UiKit.MinTouch);
            var fill = button.transform.Find("Fill")?.GetComponent<Image>();
            if (fill != null) fill.color = Palette.Orange;
            var label = button.GetComponentInChildren<TMP_Text>();
            label.color = Palette.Ink;
            var lrt = label.rectTransform;
            lrt.offsetMax = new Vector2(lrt.offsetMax.x - 110f, lrt.offsetMax.y);
            var iconGo = new GameObject("Icon", typeof(RectTransform), typeof(Image));
            iconGo.transform.SetParent(button.transform, false);
            var irt = (RectTransform)iconGo.transform;
            irt.anchorMin = irt.anchorMax = new Vector2(1f, .5f);
            irt.pivot = new Vector2(1f, .5f);
            irt.sizeDelta = new Vector2(96f, 96f);
            irt.anchoredPosition = new Vector2(-28f, 0f);
            var icon = iconGo.GetComponent<Image>();
            icon.sprite = app.Assets.Image(SystemIcons.Forward);
            icon.preserveAspect = true;
            icon.raycastTarget = false;
            icon.enabled = icon.sprite != null;
            button.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;
            return button;
        }

        /// <summary>Độ cao tâm trạm thứ <paramref name="i"/> (tính từ 0, cả quyển) so với giữa vùng đường.</summary>
        private static float WaveY(int i) => PathCenterY + WaveAmplitude * Mathf.Sin(i * WavePhase);

        private void BuildPath(AppRoot app, List<LessonEntry> entries, ISet<string> unlocked, ProgressStore progress)
        {
            var roadLayer = NewLayer("Road");
            var signLayer = NewLayer("Signs");
            var nodeLayer = NewLayer("Stations");
            var centers = new List<Vector2>();
            var x = PadX;
            var n = 0;
            foreach (var (title, section, byWeek) in Sections(entries))
            {
                _sectionStarts.Add(x);
                AddSign(signLayer, title, x + SignGap / 2f, WaveY(n));
                x += SignGap;
                var week = -1;
                foreach (var entry in section)
                {
                    var center = new Vector2(x + NodeStep / 2f, WaveY(n));
                    if (byWeek && entry.week > 0 && entry.week != week)
                    {
                        week = entry.week;
                        AddWeekMark(signLayer, string.Format(UiText.WeekFormat, week), center.x);
                    }
                    centers.Add(center);
                    AddStation(nodeLayer, entry, center, unlocked, progress, app);
                    x += NodeStep;
                    n++;
                }
            }
            _contentWidth = x + PadX;
            _content.sizeDelta = new Vector2(_contentWidth, 0f);

            // Con đường đất nhạt nối các trạm (nằm dưới), có khúc dẫn vào và dẫn ra.
            if (centers.Count > 0)
            {
                AddRoad(roadLayer, new Vector2(0f, centers[0].y), centers[0]);
                for (var i = 0; i + 1 < centers.Count; i++) AddRoad(roadLayer, centers[i], centers[i + 1]);
                AddRoad(roadLayer, centers[centers.Count - 1], new Vector2(_contentWidth, centers[centers.Count - 1].y));
            }

            // Một gà con: đứng trên bài đang học tới (đã học hết thì trên bài cuối).
            var standOn = CurrentLessonId ?? entries.LastOrDefault()?.lesson_id;
            Mascot = Mascot.Create(nodeLayer, app.Assets, MascotSize);
            var mrt = (RectTransform)Mascot.transform;
            mrt.anchorMin = mrt.anchorMax = new Vector2(0f, .5f);
            mrt.pivot = new Vector2(.5f, 0f);
            var station = ButtonFor(standOn);
            if (station != null)
            {
                var srt = (RectTransform)station.transform;
                mrt.anchoredPosition = srt.anchoredPosition + new Vector2(0f, srt.sizeDelta.y / 2f + 6f);
            }
            Mascot.transform.SetAsLastSibling();
        }

        private RectTransform NewLayer(string name)
        {
            var go = new GameObject(name, typeof(RectTransform));
            go.transform.SetParent(_content, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = rt.offsetMax = Vector2.zero;
            return rt;
        }

        private static void AddRoad(Transform layer, Vector2 from, Vector2 to)
        {
            var go = new GameObject("Road", typeof(RectTransform), typeof(Image));
            go.transform.SetParent(layer, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = rt.anchorMax = new Vector2(0f, .5f);
            var d = to - from;
            rt.sizeDelta = new Vector2(d.magnitude + RoadWidth * .5f, RoadWidth);
            rt.anchoredPosition = (from + to) / 2f;
            rt.localRotation = Quaternion.Euler(0f, 0f, Mathf.Atan2(d.y, d.x) * Mathf.Rad2Deg);
            var img = go.GetComponent<Image>();
            img.sprite = UiShapes.Rounded;
            img.type = Image.Type.Sliced;
            img.color = RoadColor;
            img.raycastTarget = false;
        }

        /// <summary>Mốc "Tuần N" chữ nhỏ ở đáy vùng đường, dưới trạm đầu tuần.</summary>
        private static void AddWeekMark(Transform layer, string text, float x)
        {
            var label = UiKit.CreateLabel(layer, text, UiKit.MinFontSize);
            label.name = "Week";
            label.color = Palette.MutedInk;
            label.raycastTarget = false;
            var rt = label.rectTransform;
            rt.anchorMin = rt.anchorMax = new Vector2(0f, .5f);
            rt.sizeDelta = new Vector2(NodeStep - 10f, 56f);
            rt.anchoredPosition = new Vector2(x, WeekRowY);
        }

        /// <summary>Biển chặng: tấm biển giấy viền mực trên cột, đặt giữa khoảng trống đầu chặng.</summary>
        private static void AddSign(Transform layer, string title, float x, float roadY)
        {
            var post = new GameObject("SignPost", typeof(RectTransform), typeof(Image));
            post.transform.SetParent(layer, false);
            var prt = (RectTransform)post.transform;
            prt.anchorMin = prt.anchorMax = new Vector2(0f, .5f);
            const float signY = 150f;
            prt.sizeDelta = new Vector2(6f, Mathf.Max(0f, signY - roadY));
            prt.pivot = new Vector2(.5f, 0f);
            prt.anchoredPosition = new Vector2(x, roadY);
            var pimg = post.GetComponent<Image>();
            pimg.sprite = UiKit.WhiteSprite;
            pimg.color = Palette.Ink;
            pimg.raycastTarget = false;

            var sign = new GameObject("Sign", typeof(RectTransform), typeof(Image));
            sign.transform.SetParent(layer, false);
            var srt = (RectTransform)sign.transform;
            srt.anchorMin = srt.anchorMax = new Vector2(0f, .5f);
            srt.sizeDelta = new Vector2(SignGap - 40f, 96f);
            srt.anchoredPosition = new Vector2(x, signY);
            var border = sign.GetComponent<Image>();
            UiKit.SetRounded(border, Palette.Ink);
            border.raycastTarget = false;
            UiKit.AddFill(sign.transform, UiShapes.Rounded, Palette.PaperLight);
            var label = UiKit.CreateLabel(sign.transform, title, 38f);
            label.enableAutoSizing = true;
            label.fontSizeMax = 38f;
            label.fontSizeMin = 24f;
            var lrt = label.rectTransform;
            lrt.anchorMin = Vector2.zero;
            lrt.anchorMax = Vector2.one;
            lrt.offsetMin = new Vector2(14f, 6f);
            lrt.offsetMax = new Vector2(-14f, -6f);
            label.raycastTarget = false;
        }

        private const string ReadingPart = "tap_doc";

        /// <summary>
        /// Các chặng của quyển: lớp 1 theo <c>part</c> (ba phần cố định), lớp 2 theo chủ điểm (thứ tự xuất hiện).
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

        /// <summary>Nhãn của bài: lấy từ <c>index.json</c>, không có thì "Bài N".</summary>
        internal static string LabelOf(LessonEntry entry) =>
            string.IsNullOrEmpty(entry.label) ? $"{UiText.LessonPrefix} {entry.lesson_no}" : entry.label;

        /// <summary>
        /// Tên bài nằm trong trạm (lớp 1, tên ngắn như "u ư", "anh"); ngược lại trạm ghi nhãn ngắn, tên bài nằm dưới trạm.
        /// </summary>
        internal static bool TitleInCircle(LessonEntry entry, int grade) =>
            grade == 1 && !string.IsNullOrEmpty(entry.title) && entry.title.Length <= CircleTitleMaxLength;

        /// <summary>Biểu tượng nhỏ theo loại bài (ôn tập, tập đọc, luyện tập, câu đố); <c>null</c> nếu không có.</summary>
        internal static string TypeIcon(string type)
        {
            if (string.IsNullOrEmpty(type)) return null;
            if (type.StartsWith("on_tap")) return SystemImages.Star;
            switch (type)
            {
                case "tap_doc":
                case "doc_them":
                case "hoc_thuoc_long":
                    return SystemImages.EmDoc;
                case "tap_chep_chinh_ta":
                case "tu_ngu":
                case "ngu_phap":
                case "tap_lam_van":
                    return SystemImages.LuyenTap;
                case "cau_do":
                    return SystemImages.CauHoi;
                default:
                    return null;
            }
        }

        private void AddStation(Transform layer, LessonEntry entry, Vector2 center, ISet<string> unlocked,
            ProgressStore progress, AppRoot app)
        {
            var lessonId = entry.lesson_id;
            var isCurrent = lessonId == CurrentLessonId && unlocked.Contains(lessonId);
            var size = isCurrent ? CurrentNodeSize : NodeSize;
            var go = new GameObject($"Lesson_{lessonId}", typeof(RectTransform), typeof(Image), typeof(Button),
                typeof(TapFeedback));
            go.transform.SetParent(layer, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = rt.anchorMax = new Vector2(0f, .5f);
            rt.sizeDelta = new Vector2(size, size);
            rt.anchoredPosition = center;
            var hit = go.GetComponent<Image>();
            hit.sprite = UiShapes.Circle;
            hit.color = Color.clear; // vùng chạm tròn cả trạm

            var border = new GameObject("Border", typeof(RectTransform), typeof(Image));
            border.transform.SetParent(go.transform, false);
            var brt = (RectTransform)border.transform;
            brt.anchorMin = Vector2.zero;
            brt.anchorMax = Vector2.one;
            brt.offsetMin = brt.offsetMax = Vector2.zero;
            var borderImg = border.GetComponent<Image>();
            borderImg.sprite = UiShapes.Circle;
            borderImg.color = Palette.Ink;
            borderImg.raycastTarget = false;
            var fill = UiKit.AddFill(go.transform, UiShapes.Circle,
                progress.IsCompleted(lessonId) ? Palette.TealLight : Palette.PaperLight);

            var label = LabelOf(entry);
            var inCircle = TitleInCircle(entry, _grade);
            var iconId = TypeIcon(entry.type);
            var titleScale = entry.title == null ? 100 : entry.title.Length <= 4 ? 190 : entry.title.Length <= 7 ? 150 : 115;
            var text = UiKit.CreateLabel(go.transform,
                inCircle ? $"{label}\n<size={titleScale}%>{entry.title}</size>" : label, 34f);
            text.enableAutoSizing = true;
            text.fontSizeMax = 34f;
            text.fontSizeMin = 18f;
            text.raycastTarget = false;
            var trt = text.rectTransform;
            trt.anchorMin = new Vector2(.12f, iconId != null && !inCircle ? .28f : .26f);
            trt.anchorMax = new Vector2(.88f, iconId != null && !inCircle ? .62f : .86f);
            trt.offsetMin = trt.offsetMax = Vector2.zero;

            if (iconId != null && (!inCircle || entry.type.StartsWith("on_tap")))
            {
                var iconGo = new GameObject("TypeIcon", typeof(RectTransform), typeof(Image));
                iconGo.transform.SetParent(go.transform, false);
                var irt = (RectTransform)iconGo.transform;
                irt.anchorMin = irt.anchorMax = new Vector2(.5f, inCircle ? .84f : .78f);
                irt.sizeDelta = new Vector2(TypeIconSize, TypeIconSize);
                var icon = iconGo.GetComponent<Image>();
                icon.sprite = app.Assets.Image(iconId);
                icon.preserveAspect = true;
                icon.raycastTarget = false;
                icon.enabled = icon.sprite != null;
                if (inCircle) trt.anchorMax = new Vector2(.88f, .72f);
            }

            if (!inCircle)
            {
                // Tên bài nhỏ dưới trạm, tối đa 2 dòng, cắt bằng "…".
                var caption = UiKit.CreateLabel(go.transform, entry.title, CaptionFont);
                caption.name = "Caption";
                caption.enableAutoSizing = false;
                caption.fontSize = CaptionFont;
                caption.raycastTarget = false;
                caption.text = FitTwoLines(caption, entry.title ?? string.Empty);
                var crt = caption.rectTransform;
                crt.anchorMin = crt.anchorMax = new Vector2(.5f, 0f);
                crt.pivot = new Vector2(.5f, 1f);
                crt.sizeDelta = new Vector2(CaptionWidth, CaptionHeight);
                crt.anchoredPosition = new Vector2(0f, -6f);
            }

            var btn = go.GetComponent<Button>();
            btn.targetGraphic = fill;
            btn.onClick.AddListener(() => app.ShowLesson(lessonId));
            go.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;

            if (!unlocked.Contains(lessonId)) Lock(btn, app.Assets);
            else if (isCurrent) MarkCurrent(btn);

            var flowers = FlowerBook.FlowersFor(progress, lessonId);
            if (flowers > 0) AddFlowers(go.transform, app.Assets, lessonId, flowers);

            _lessonButtons[lessonId] = btn;
        }

        private const float CaptionFont = 26f;

        /// <summary>
        /// Rút gọn <paramref name="title"/> theo từng chữ cho vừa hai dòng của <paramref name="caption"/>, thêm "…" khi
        /// phải bỏ bớt.
        /// </summary>
        internal static string FitTwoLines(TMP_Text caption, string title)
        {
            bool Fits(string s) => caption.GetPreferredValues(s, CaptionWidth, 0f).y <= CaptionHeight + .5f;
            if (Fits(title)) return title;
            var words = title.Split(' ');
            for (var n = words.Length - 1; n > 0; n--)
            {
                var candidate = string.Join(" ", words.Take(n)).TrimEnd(',', ':', '–', '-', ' ') + "…";
                if (Fits(candidate)) return candidate;
            }
            return words[0] + "…";
        }

        /// <summary>Cuộn để trạm của bài nằm trọn trong vùng nhìn (đặt vào giữa); bỏ qua mã bài không có.</summary>
        internal void ScrollTo(string lessonId)
        {
            var button = ButtonFor(lessonId);
            if (button == null) return;
            _focusLesson = lessonId;
            _placed = true;
            var rt = (RectTransform)button.transform;
            var left = -_content.anchoredPosition.x;
            var view = Scroll.viewport.rect.width;
            var x = rt.anchoredPosition.x;
            var half = rt.sizeDelta.x / 2f;
            if (x - half >= left && x + half <= left + view) return;
            CenterOn(lessonId);
        }

        /// <summary>Đặt trạm của bài vào giữa vùng nhìn (trong giới hạn cuộn).</summary>
        private void CenterOn(string lessonId)
        {
            var button = ButtonFor(lessonId);
            if (button == null) return;
            _focusLesson = lessonId;
            var rt = (RectTransform)button.transform;
            var view = Scroll.viewport.rect.width;
            // Trạm thấy được ngay từ đầu đường thì để đường ở đầu (thấy cả biển chặng đầu).
            var fromStart = rt.anchoredPosition.x + rt.sizeDelta.x / 2f + 40f <= view;
            SetLeft(fromStart ? 0f : rt.anchoredPosition.x - view / 2f);
        }

        private float MaxLeft => Mathf.Max(0f, _contentWidth - Scroll.viewport.rect.width);

        private void SetLeft(float left)
        {
            Scroll.StopMovement();
            _content.anchoredPosition = new Vector2(-Mathf.Clamp(left, 0f, MaxLeft), 0f);
            RefreshArrows();
        }

        /// <summary>
        /// Lật sang chặng sau (<paramref name="direction"/> &gt; 0) hoặc về chặng trước: biển chặng nằm ở mép trái vùng
        /// nhìn; hết chặng thì tới cuối (hoặc đầu) đường.
        /// </summary>
        internal void JumpSection(int direction)
        {
            _placed = true;
            StopHint();
            var left = -_content.anchoredPosition.x;
            const float slack = 5f;
            if (direction > 0)
            {
                var next = _sectionStarts.Where(s => s > left + slack).DefaultIfEmpty(float.NaN).First();
                SetLeft(float.IsNaN(next) || next > MaxLeft ? MaxLeft : next);
            }
            else
            {
                var prev = _sectionStarts.Where(s => s < left - slack).DefaultIfEmpty(float.NaN).Last();
                SetLeft(float.IsNaN(prev) ? 0f : prev);
            }
        }

        private void OnScrolled()
        {
            RefreshArrows();
            if (Scroll.velocity.sqrMagnitude > 1f) StopHint();
        }

        private void StopHint()
        {
            if (NextButton != null) Pulse.StopOn(NextButton.transform);
        }

        private void RefreshArrows()
        {
            if (PrevButton == null || NextButton == null || Scroll == null) return;
            var left = -_content.anchoredPosition.x;
            PrevButton.interactable = left > 1f;
            NextButton.interactable = left < MaxLeft - 1f;
        }

        private static void Corner(Button button, Vector2 corner, Vector2 offset)
        {
            var rt = (RectTransform)button.transform;
            rt.anchorMin = rt.anchorMax = rt.pivot = corner;
            rt.anchoredPosition = offset;
        }

        /// <summary>Bài đang học tới: nền cam nhạt, nhún chậm để bé biết bấm vào đâu.</summary>
        private static void MarkCurrent(Button station)
        {
            station.transform.Find("Fill").GetComponent<Image>().color = Palette.OrangeLight;
            Pulse.StartOn(station.transform);
        }

        /// <summary>Bài chưa mở: nền và chữ màu khoá, có ổ khoá, không bấm được (giữ màu, không làm xám cả trạm).</summary>
        private static void Lock(Button station, AssetCatalog assets)
        {
            station.interactable = false;
            var colors = station.colors;
            colors.disabledColor = Color.white;
            station.colors = colors;
            station.transform.Find("Fill").GetComponent<Image>().color = Palette.LockedFill;
            station.transform.Find("Border").GetComponent<Image>().color = Palette.LockedInk;
            foreach (var t in station.GetComponentsInChildren<TMP_Text>()) t.color = Palette.LockedInk;

            var go = new GameObject("Lock", typeof(RectTransform), typeof(Image));
            go.transform.SetParent(station.transform, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = rt.anchorMax = new Vector2(.82f, .82f);
            rt.sizeDelta = new Vector2(LockSize, LockSize);
            var img = go.GetComponent<Image>();
            img.sprite = assets.Image(SystemIcons.Lock);
            img.preserveAspect = true;
            img.raycastTarget = false;
        }

        /// <summary>Hàng <paramref name="count"/> bông hoa bé ngoan nhỏ ở đáy trạm.</summary>
        private static void AddFlowers(Transform station, AssetCatalog assets, string lessonId, int count)
        {
            var row = new GameObject("Flowers", typeof(RectTransform), typeof(HorizontalLayoutGroup));
            row.transform.SetParent(station, false);
            var rt = (RectTransform)row.transform;
            rt.anchorMin = new Vector2(.15f, .06f);
            rt.anchorMax = new Vector2(.85f, .25f);
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            var hlg = row.GetComponent<HorizontalLayoutGroup>();
            hlg.spacing = 2f;
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
