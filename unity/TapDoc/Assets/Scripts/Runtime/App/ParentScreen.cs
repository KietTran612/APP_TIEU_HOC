using System;
using System.Collections.Generic;
using System.Linq;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Màn phụ huynh. Trước hết là khóa phép tính (<see cref="ParentGate"/>) với 3 nút đáp án. Mở khóa xong, mỗi
    /// hồ sơ có một khối gồm: tên bé, dòng "Đã học n/N bài" (N là số bài trong <c>index.json</c>) và tối đa 5 chữ
    /// bé hay nhầm, mỗi chữ một thẻ, nhầm nhiều trước. Chữ lấy từ đáp án đúng của lượt bé nhầm; lượt lỗi thời bị bỏ qua.
    /// </summary>
    public class ParentScreen : MonoBehaviour
    {
        private const int MaxConfusions = 5;
        private const float ChipHeight = UiKit.MinTouch; // thẻ chữ hay nhầm chạm để nghe (vùng chạm ≥ 160)
        private const float WeekBlock = 64f;    // dòng "7 ngày qua" + cột theo ngày
        private const float NameBlock = 80f;      // tên bé ở trên cùng khối
        private const float LineHeight = 52f;     // một dòng tiến độ
        private const float ProgressFont = 38f;
        private const float ProgressFontMin = 30f;
        private const int ProgressColumns = 2;    // nhiều quyển: xếp hai cột, khối cao thêm theo số hàng
        private const float MinRowHeight = 370f;  // thẻ chữ hay nhầm luôn nằm dưới nút "Mở mọi bài" (cao 160)

        private static readonly Color RowColor = Palette.PaperLight;
        private static readonly Color ChipColor = Palette.ChipYellow;
        private static readonly Color MutedText = Palette.MutedInk;

        private AppRoot _app;
        private ParentGatePanel _gatePanel;
        private GameObject _progressPanel;
        private GameObject _appendixPanel;

        internal ParentGate Gate => _gatePanel.Gate;
        internal IReadOnlyList<Button> ChoiceButtons => _gatePanel.ChoiceButtons;
        internal Button BackButton { get; private set; }

        internal bool IsUnlocked => _progressPanel != null && _progressPanel.activeSelf;

        public void Build(AppRoot app)
        {
            _app = app;

            BackButton = UiKit.CreateButton(transform, UiText.Back, app.ShowLessonList);
            var backRt = (RectTransform)BackButton.transform;
            backRt.anchorMin = new Vector2(0f, 1f);
            backRt.anchorMax = new Vector2(0f, 1f);
            backRt.pivot = new Vector2(0f, 1f);
            backRt.sizeDelta = new Vector2(220f, UiKit.MinTouch);
            backRt.anchoredPosition = new Vector2(20f, -20f);

            var header = UiKit.CreateLabel(transform, UiText.Parent, 64f);
            Place(header.rectTransform, new Vector2(0.5f, 1f), new Vector2(800f, UiKit.MinTouch), new Vector2(0f, -20f));

            _gatePanel = ParentGatePanel.Create(transform, new System.Random(), Unlock);
            _progressPanel = Panel("ProgressPanel");
            _progressPanel.SetActive(false);
        }

        /// <summary>Móc cho test: bấm nút đáp án đúng.</summary>
        internal void SimulateUnlock() => _gatePanel.SimulateUnlock();

        private void Unlock()
        {
            BuildProgress();
            _progressPanel.SetActive(true);
        }

        /// <summary>Các mục của màn Phụ huynh (bản thiết kế nâng cấp UI mục 4.6).</summary>
        internal enum ParentTab
        {
            Week,
            Play,
            Time
        }

        private readonly Dictionary<ParentTab, GameObject> _tabPanels = new();
        private readonly Dictionary<ParentTab, Button> _tabButtons = new();
        private readonly Dictionary<string, TMP_Text> _weekLines = new();
        private readonly Dictionary<string, List<Button>> _chipButtons = new();
        private readonly Dictionary<string, List<string>> _playLines = new();
        private readonly Dictionary<(string, int), Button> _sessionButtons = new();
        private const float TabWidth = 320f;
        private const float TabsTop = 196f;
        private const float ContentTop = TabsTop + UiKit.MinTouch + 16f;

        internal ParentTab CurrentTab { get; private set; }
        internal Button TabButton(ParentTab tab) => _tabButtons.TryGetValue(tab, out var b) ? b : null;
        internal TMP_Text WeekLineFor(string profileId) => _weekLines.TryGetValue(profileId, out var t) ? t : null;
        internal IReadOnlyList<Button> ChipButtonsFor(string profileId) =>
            _chipButtons.TryGetValue(profileId, out var l) ? l : new List<Button>();
        internal IReadOnlyList<string> PlayLinesFor(string profileId) =>
            _playLines.TryGetValue(profileId, out var l) ? l : new List<string>();
        internal Button SessionButtonFor(string profileId, int lessons) =>
            _sessionButtons.TryGetValue((profileId, lessons), out var b) ? b : null;

        /// <summary>Số bài mỗi lần học phụ huynh chọn được (0 = không nhắc).</summary>
        internal static readonly int[] SessionChoices = { 0, 2, 3, 5 };

        /// <summary>Hiện mục <paramref name="tab"/>.</summary>
        internal void ShowTab(ParentTab tab)
        {
            CurrentTab = tab;
            foreach (var pair in _tabPanels) pair.Value.SetActive(pair.Key == tab);
            foreach (var pair in _tabButtons) PaintChoice(pair.Value, pair.Key == tab);
        }

        /// <summary>Nút chọn đang chọn: nền lam ngọc chữ trắng; chưa chọn: nền giấy chữ mực.</summary>
        private static void PaintChoice(Button button, bool on)
        {
            var fill = button.transform.Find("Fill")?.GetComponent<Image>();
            if (fill != null) fill.color = on ? Palette.Teal : Palette.PaperLight;
            var label = button.GetComponentInChildren<TMP_Text>();
            if (label != null) label.color = on ? Color.white : Palette.Ink;
        }

        private void BuildTabs()
        {
            var tabs = new[] { (ParentTab.Week, UiText.TabWeek), (ParentTab.Play, UiText.TabPlay), (ParentTab.Time, UiText.TabTime) };
            for (var k = 0; k < tabs.Length; k++)
            {
                var (tab, label) = tabs[k];
                var button = UiKit.CreateButton(_progressPanel.transform, label, () => ShowTab(tab));
                button.name = $"Tab_{tab}";
                var rt = (RectTransform)button.transform;
                rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(.5f, 1f);
                rt.sizeDelta = new Vector2(TabWidth, UiKit.MinTouch);
                rt.anchoredPosition = new Vector2((k - 1) * (TabWidth + 20f), -TabsTop);
                button.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;
                _tabButtons[tab] = button;
            }
        }

        /// <summary>Một vùng cuộn dọc của mục <paramref name="tab"/>; trả về khung nội dung (xếp dọc).</summary>
        private Transform NewTabScroll(ParentTab tab, string name)
        {
            var scrollGo = new GameObject(name, typeof(RectTransform), typeof(ScrollRect));
            scrollGo.transform.SetParent(_progressPanel.transform, false);
            var scrollRt = (RectTransform)scrollGo.transform;
            scrollRt.anchorMin = Vector2.zero;
            scrollRt.anchorMax = Vector2.one;
            scrollRt.offsetMin = new Vector2(40f, 20f);
            scrollRt.offsetMax = new Vector2(-40f, -ContentTop);

            var viewportGo = new GameObject("Viewport", typeof(RectTransform), typeof(RectMask2D), typeof(Image));
            viewportGo.transform.SetParent(scrollGo.transform, false);
            var viewportRt = (RectTransform)viewportGo.transform;
            viewportRt.anchorMin = Vector2.zero;
            viewportRt.anchorMax = Vector2.one;
            viewportRt.offsetMin = Vector2.zero;
            viewportRt.offsetMax = Vector2.zero;
            var viewportImg = viewportGo.GetComponent<Image>();
            viewportImg.sprite = UiKit.WhiteSprite;
            viewportImg.color = new Color(1f, 1f, 1f, 0f); // trong suốt, chỉ để nhận thao tác kéo cuộn

            var contentGo = new GameObject("Content", typeof(RectTransform), typeof(VerticalLayoutGroup), typeof(ContentSizeFitter));
            contentGo.transform.SetParent(viewportGo.transform, false);
            var contentRt = (RectTransform)contentGo.transform;
            contentRt.anchorMin = new Vector2(0f, 1f);
            contentRt.anchorMax = new Vector2(1f, 1f);
            contentRt.pivot = new Vector2(0.5f, 1f);
            contentRt.sizeDelta = Vector2.zero;
            contentRt.anchoredPosition = Vector2.zero;
            var vlg = contentGo.GetComponent<VerticalLayoutGroup>();
            vlg.spacing = 16f;
            vlg.childControlWidth = true;
            vlg.childControlHeight = true;
            vlg.childForceExpandWidth = true;
            vlg.childForceExpandHeight = false;
            contentGo.GetComponent<ContentSizeFitter>().verticalFit = ContentSizeFitter.FitMode.PreferredSize;

            var scroll = scrollGo.GetComponent<ScrollRect>();
            scroll.viewport = viewportRt;
            scroll.content = contentRt;
            scroll.horizontal = false;
            scroll.vertical = true;
            scroll.movementType = ScrollRect.MovementType.Clamped;
            _tabPanels[tab] = scrollGo;
            return contentGo.transform;
        }

        private void BuildProgress()
        {
            BuildTabs();
            var contentGo = NewTabScroll(ParentTab.Week, "Children").gameObject;
            var ordered = _app.Lessons.Index.lessons.Select(e => e.lesson_id).ToList();
            var appendix = UiKit.CreateButton(contentGo.transform, UiText.BookAppendix, OpenAppendix);
            appendix.GetComponent<LayoutElement>().preferredHeight = UiKit.MinTouch;
            var lessons = new Dictionary<string, Lesson>();
            foreach (var profile in _app.Progress.Profiles)
            {
                BuildRow(contentGo.transform, profile, ordered, lessons);
            }
            BuildPlay(lessons);
            BuildTime();
            ShowTab(ParentTab.Week);
        }

        /// <summary>Mục "Chơi cùng con": mỗi bé 2–3 việc làm cùng bố mẹ, sinh từ bài bé vừa học.</summary>
        private void BuildPlay(Dictionary<string, Lesson> lessons)
        {
            var content = NewTabScroll(ParentTab.Play, "Play");
            foreach (var profile in _app.Progress.Profiles)
            {
                var entry = _app.Lessons.Index.lessons.FirstOrDefault(e => e.lesson_id == profile.last_lesson_id);
                Lesson lesson = null;
                if (entry != null && !lessons.TryGetValue(entry.lesson_id, out lesson))
                {
                    try
                    {
                        lesson = _app.Lessons.Get(entry.lesson_id);
                    }
                    catch (Exception)
                    {
                        lesson = null;
                    }
                }
                var lines = ParentSuggestions.For(entry, lesson);
                _playLines[profile.id] = lines;
                var block = Block(content, $"Play_{profile.id}", 90f + lines.Count * PlayLineHeight);
                var name = LeftLabel(block, profile.name, 44f);
                PlaceTop(name.rectTransform, 14f, 64f);
                for (var k = 0; k < lines.Count; k++)
                {
                    var line = LeftLabel(block, "• " + lines[k], 34f);
                    line.name = $"Suggestion_{k}";
                    line.enableAutoSizing = true;
                    line.fontSizeMax = 34f;
                    line.fontSizeMin = UiKit.MinFontSize;
                    PlaceTop(line.rectTransform, 84f + k * PlayLineHeight, PlayLineHeight - 6f);
                }
            }
            var note = LeftLabel(content, UiText.PlayTogetherNote, 30f);
            note.color = MutedText;
            note.gameObject.AddComponent<LayoutElement>().preferredHeight = 60f;
        }

        private const float PlayLineHeight = 100f;

        /// <summary>Mục "Thời lượng": mỗi bé chọn số bài mỗi lần học rồi gà con rủ nghỉ mắt (0 = không nhắc).</summary>
        private void BuildTime()
        {
            var content = NewTabScroll(ParentTab.Time, "Time");
            foreach (var profile in _app.Progress.Profiles)
            {
                var block = Block(content, $"Time_{profile.id}", 90f + UiKit.MinTouch + 20f);
                var name = LeftLabel(block, profile.name, 44f);
                PlaceTop(name.rectTransform, 14f, 64f);
                var label = LeftLabel(block, UiText.SessionLabel, 36f);
                PlaceLeft(label.rectTransform, 0f, new Vector2(20f, 20f), new Vector2(260f, UiKit.MinTouch));
                for (var k = 0; k < SessionChoices.Length; k++)
                {
                    var value = SessionChoices[k];
                    var text = value == 0 ? UiText.SessionOff : string.Format(UiText.SessionCountFormat, value);
                    var p = profile;
                    Button button = null;
                    button = UiKit.CreateButton(block, text, () => SetSession(p, value));
                    button.name = $"Session_{value}";
                    var rt = (RectTransform)button.transform;
                    rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0f, 0f);
                    rt.sizeDelta = new Vector2(220f, UiKit.MinTouch);
                    rt.anchoredPosition = new Vector2(290f + k * 240f, 20f);
                    button.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;
                    _sessionButtons[(profile.id, value)] = button;
                }
                RefreshSession(profile);
            }
            var note = LeftLabel(content, UiText.SessionNote, 30f);
            note.color = MutedText;
            note.enableAutoSizing = true;
            note.fontSizeMin = UiKit.MinFontSize;
            note.gameObject.AddComponent<LayoutElement>().preferredHeight = 90f;
        }

        private void SetSession(Profile profile, int lessons)
        {
            profile.session_lessons = lessons;
            _app.SaveProgress();
            RefreshSession(profile);
        }

        private void RefreshSession(Profile profile)
        {
            foreach (var value in SessionChoices)
            {
                if (_sessionButtons.TryGetValue((profile.id, value), out var b)) PaintChoice(b, value == profile.session_lessons);
            }
        }

        /// <summary>Khối nền giấy sáng cao <paramref name="height"/> trong danh sách dọc.</summary>
        private static Transform Block(Transform content, string name, float height)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(Image), typeof(LayoutElement));
            go.transform.SetParent(content, false);
            var bg = go.GetComponent<Image>();
            bg.sprite = UiKit.WhiteSprite;
            bg.color = RowColor;
            var le = go.GetComponent<LayoutElement>();
            le.minHeight = le.preferredHeight = height;
            return go.transform;
        }

        /// <summary>Nhãn kéo dài theo bề ngang khối, cách đỉnh <paramref name="top"/>, cao <paramref name="height"/>.</summary>
        private static void PlaceTop(RectTransform rt, float top, float height)
        {
            rt.anchorMin = new Vector2(0f, 1f);
            rt.anchorMax = new Vector2(1f, 1f);
            rt.pivot = new Vector2(0f, 1f);
            rt.offsetMin = new Vector2(20f, -top - height);
            rt.offsetMax = new Vector2(-20f, -top);
        }

        private const float UnlockWidth = 380f;
        private readonly Dictionary<string, Button> _unlockToggles = new();

        /// <summary>Nút "Mở mọi bài" của bé <paramref name="profileId"/> (cho test).</summary>
        internal Button UnlockToggleFor(string profileId) => _unlockToggles.TryGetValue(profileId, out var b) ? b : null;

        private static string UnlockLabel(Profile profile) => profile.unlock_all ? UiText.UnlockAllOn : UiText.UnlockAllOff;

        private void ToggleUnlockAll(Profile profile, Button button)
        {
            profile.unlock_all = !profile.unlock_all;
            _app.Progress.Save();
            button.GetComponentInChildren<TMPro.TMP_Text>().text = UnlockLabel(profile);
        }

        private void OpenAppendix()
        {
            if (_appendixPanel == null)
            {
                // Mọi bài trong danh sách thuộc cùng một quyển sách: Phụ lục lấy theo mã sách đó.
                var lessons = _app.Lessons.Index.lessons;
                var audio = LetterAudio.FromLessons(lessons.Select(e => _app.Lessons.Get(e.lesson_id)));
                _appendixPanel = NotesPanel.ForAppendix(transform, _app.Lessons.Appendix(lessons.First().book), audio,
                    id => _ = _app.Speech.PlayAsync(id));
            }
            _appendixPanel.transform.SetAsLastSibling();
            _appendixPanel.SetActive(true);
        }

        private void BuildRow(Transform content, Profile profile, List<string> ordered, Dictionary<string, Lesson> lessons)
        {
            var row = new GameObject($"Child_{profile.id}", typeof(RectTransform), typeof(Image), typeof(LayoutElement));
            row.transform.SetParent(content, false);
            var bg = row.GetComponent<Image>();
            bg.sprite = UiKit.WhiteSprite;
            bg.color = RowColor;

            var avatarBox = new GameObject("AvatarBox", typeof(RectTransform));
            avatarBox.transform.SetParent(row.transform, false);
            PlaceLeft((RectTransform)avatarBox.transform, 1f, new Vector2(20f, -14f), new Vector2(100f, 100f));
            ProfileScreen.AddAvatar(avatarBox.transform, _app.Assets, profile.avatar, profile.name);

            var name = LeftLabel(row.transform, profile.name, 48f);
            PlaceLeft(name.rectTransform, 1f, new Vector2(140f, -14f), new Vector2(520f, 60f));
            name.overflowMode = TextOverflowModes.Ellipsis;

            var index = _app.Lessons.Index;
            var books = BookShelf.BookIds(index);
            var perBook = books.Count > 1;
            List<string> lines;
            if (perBook)
            {
                // Tủ sách (bản thiết kế mục 7): mỗi quyển một dòng tiến độ.
                lines = books.Select(b =>
                {
                    var ids = BookShelf.LessonIds(index, b);
                    return string.Format(UiText.BookLearnedFormat, BookShelf.Book(index, b)?.title ?? b,
                        ids.Count(id => ProgressStore.IsCompleted(profile, id)), ids.Count);
                }).ToList();
            }
            else
            {
                var learned = ordered.Count(id => ProgressStore.IsCompleted(profile, id));
                lines = new List<string> { string.Format(UiText.LearnedFormat, learned, ordered.Count) };
            }
            var rows = AddProgressLines(row.transform, lines, perBook ? ProgressColumns : 1);

            // Khối cao theo số hàng tiến độ: số quyển nào cũng không tràn chữ (khối cao thì cuộn danh sách bé).
            var le = row.GetComponent<LayoutElement>();
            le.minHeight = le.preferredHeight =
                Mathf.Max(MinRowHeight, NameBlock + rows * LineHeight + WeekBlock + 24f + ChipHeight + 12f);

            // 7 ngày qua: số bài, số phút, cột theo ngày (nâng cấp UI mục 4.6).
            AddWeek(row.transform, profile, NameBlock + rows * LineHeight);

            // "Mở mọi bài" theo từng bé: bé đã học phần trước ở trường vào thẳng bài sau; tắt lại không mất tiến độ.
            var unlock = UiKit.CreateButton(row.transform, UnlockLabel(profile), null);
            unlock.name = $"UnlockAll_{profile.id}";
            var unlockRt = (RectTransform)unlock.transform;
            unlockRt.anchorMin = unlockRt.anchorMax = unlockRt.pivot = new Vector2(1f, 1f);
            unlockRt.anchoredPosition = new Vector2(-20f, -14f);
            unlockRt.sizeDelta = new Vector2(UnlockWidth, UiKit.MinTouch);
            unlock.onClick.AddListener(() => ToggleUnlockAll(profile, unlock));
            _unlockToggles[profile.id] = unlock;

            var confusedLabel = LeftLabel(row.transform, UiText.OftenConfused, 36f);
            PlaceLeft(confusedLabel.rectTransform, 0f, new Vector2(20f, 12f), new Vector2(300f, ChipHeight));

            var chipsGo = new GameObject("Confusions", typeof(RectTransform), typeof(HorizontalLayoutGroup));
            chipsGo.transform.SetParent(row.transform, false);
            var chipsRt = (RectTransform)chipsGo.transform;
            chipsRt.anchorMin = new Vector2(0f, 0f);
            chipsRt.anchorMax = new Vector2(1f, 0f);
            chipsRt.pivot = new Vector2(0f, 0f);
            chipsRt.offsetMin = new Vector2(330f, 12f);
            chipsRt.offsetMax = new Vector2(-20f, 12f + ChipHeight);
            var hlg = chipsGo.GetComponent<HorizontalLayoutGroup>();
            hlg.spacing = 14f;
            hlg.childAlignment = TextAnchor.MiddleLeft;
            hlg.childControlWidth = true;
            hlg.childControlHeight = true;
            hlg.childForceExpandWidth = false;
            hlg.childForceExpandHeight = true;

            var confusions = Confusions(profile, lessons);
            _chipButtons[profile.id] = new List<Button>();
            if (confusions.Count == 0)
            {
                var none = LeftLabel(chipsGo.transform, UiText.NoConfusion, 36f);
                none.color = MutedText;
                none.gameObject.AddComponent<LayoutElement>().preferredWidth = 400f;
            }
            foreach (var (text, audio) in confusions)
            {
                _chipButtons[profile.id].Add(AddChip(chipsGo.transform, text, audio));
            }
        }

        private const float BarWidth = 22f;
        private const float BarMaxHeight = 46f;

        private void AddWeek(Transform row, Profile profile, float top)
        {
            var week = ProgressStore.LastWeek(profile, DateTime.Now);
            var lessons = week.Sum(d => d.lessons);
            var minutes = Mathf.RoundToInt(week.Sum(d => d.seconds) / 60f);
            var line = LeftLabel(row, string.Format(UiText.WeekSummaryFormat, lessons, minutes), 34f);
            line.name = "Week";
            line.enableAutoSizing = true;
            line.fontSizeMax = 34f;
            line.fontSizeMin = UiKit.MinFontSize;
            PlaceLeft(line.rectTransform, 1f, new Vector2(140f, -top - 4f), new Vector2(520f, WeekBlock - 8f));
            _weekLines[profile.id] = line;
            var most = Mathf.Max(1, week.Max(d => d.lessons));
            for (var k = 0; k < week.Count; k++)
            {
                var bar = new GameObject($"Day_{k}", typeof(RectTransform), typeof(Image));
                bar.transform.SetParent(row, false);
                var rt = (RectTransform)bar.transform;
                rt.anchorMin = rt.anchorMax = new Vector2(0f, 1f);
                rt.pivot = new Vector2(0f, 0f);
                var h = week[k].lessons > 0 ? Mathf.Max(6f, BarMaxHeight * week[k].lessons / most) : 3f;
                rt.sizeDelta = new Vector2(BarWidth, h);
                rt.anchoredPosition = new Vector2(680f + k * (BarWidth + 8f), -top - WeekBlock + 6f);
                var img = bar.GetComponent<Image>();
                img.sprite = UiKit.WhiteSprite;
                img.color = k == week.Count - 1 ? Palette.Orange : Palette.Teal;
                img.raycastTarget = false;
            }
        }

        /// <summary>
        /// Các dòng tiến độ dưới tên bé, xếp theo hàng (trái sang phải, trên xuống dưới) trong vùng từ cột tên tới mép
        /// trái nút "Mở mọi bài" (không nằm dưới nút). Trả về số hàng.
        /// </summary>
        private static int AddProgressLines(Transform row, IReadOnlyList<string> lines, int columns)
        {
            var area = new GameObject("Progress", typeof(RectTransform));
            area.transform.SetParent(row, false);
            var art = (RectTransform)area.transform;
            art.anchorMin = new Vector2(0f, 1f);
            art.anchorMax = Vector2.one;
            art.pivot = new Vector2(0f, 1f);
            var rows = Mathf.Max(1, Mathf.CeilToInt(lines.Count / (float)columns));
            art.offsetMin = new Vector2(140f, -NameBlock - rows * LineHeight);
            art.offsetMax = new Vector2(-(UnlockWidth + 40f), -NameBlock);
            var size = columns > 1 ? ProgressFont : 44f;
            for (var i = 0; i < lines.Count; i++)
            {
                int r = i / columns, c = i % columns;
                var label = LeftLabel(area.transform, lines[i], size);
                label.name = $"Progress_{i}";
                label.enableAutoSizing = true;
                label.fontSizeMax = size;
                label.fontSizeMin = ProgressFontMin;
                var lrt = label.rectTransform;
                lrt.anchorMin = new Vector2(c / (float)columns, 1f);
                lrt.anchorMax = new Vector2((c + 1) / (float)columns, 1f);
                lrt.pivot = new Vector2(0f, 1f);
                lrt.offsetMin = new Vector2(0f, -(r + 1) * LineHeight);
                lrt.offsetMax = new Vector2(-16f, -r * LineHeight);
            }
            return rows;
        }

        /// <summary>
        /// Tối đa 5 chữ bé hay nhầm: đáp án đúng của các lượt bé nhầm, gộp chữ trùng nhau, nhầm nhiều trước rồi mới
        /// nhầm trước. Lượt lỗi thời (bài không nạp được, chỉ số lượt hay đáp án không còn) bị bỏ qua.
        /// </summary>
        private List<(string text, string audio)> Confusions(Profile profile, Dictionary<string, Lesson> lessons)
        {
            var totals = new Dictionary<string, (int count, long last, string audio)>();
            foreach (var mistake in ProgressStore.MistakesOf(profile, int.MaxValue))
            {
                var (text, audio) = Answer(mistake, lessons);
                if (string.IsNullOrEmpty(text)) continue;
                totals.TryGetValue(text, out var t);
                totals[text] = (t.count + mistake.count, Math.Max(t.last, mistake.last_ticks), t.audio ?? audio);
            }
            return totals
                .OrderByDescending(p => p.Value.count)
                .ThenByDescending(p => p.Value.last)
                .Select(p => (p.Key, p.Value.audio))
                .Take(MaxConfusions)
                .ToList();
        }

        /// <summary>Chữ (và tiếng, nếu có) của đáp án đúng ở lượt bé nhầm.</summary>
        private (string text, string audio) Answer(Mistake mistake, Dictionary<string, Lesson> lessons)
        {
            if (!lessons.TryGetValue(mistake.lesson_id, out var lesson))
            {
                try
                {
                    lesson = _app.Lessons.Get(mistake.lesson_id);
                }
                catch (Exception)
                {
                    lesson = null;
                }
                lessons[mistake.lesson_id] = lesson;
            }
            if (lesson?.part2 == null || mistake.round < 0 || mistake.round >= lesson.part2.Count) return (null, null);
            var round = lesson.part2[mistake.round];
            if (round?.options == null || round.answer < 0 || round.answer >= round.options.Count) return (null, null);
            // Lượt nhìn chữ kéo dấu: phương án là kí hiệu dấu; phụ huynh cần thấy chữ mẫu có dấu (ví dụ "cá").
            if (round.kind == "look_tone" && !string.IsNullOrEmpty(round.prompt_text)) return (round.prompt_text, round.prompt_audio);
            var option = round.options[round.answer];
            return (option?.text, option?.audio);
        }

        /// <summary>Thẻ chữ hay nhầm: chạm để nghe (có tiếng thì có biểu tượng loa).</summary>
        private Button AddChip(Transform parent, string text, string audio)
        {
            var chip = new GameObject("Confusion", typeof(RectTransform), typeof(Image), typeof(LayoutElement), typeof(Button),
                typeof(TapFeedback));
            chip.transform.SetParent(parent, false);
            var img = chip.GetComponent<Image>();
            img.sprite = UiKit.WhiteSprite;
            img.color = ChipColor;
            var hasAudio = !string.IsNullOrEmpty(audio);
            var iconWidth = hasAudio ? 56f : 0f;
            if (hasAudio)
            {
                var icon = new GameObject("Speaker", typeof(RectTransform), typeof(Image));
                icon.transform.SetParent(chip.transform, false);
                var irt = (RectTransform)icon.transform;
                irt.anchorMin = irt.anchorMax = irt.pivot = new Vector2(0f, .5f);
                irt.sizeDelta = new Vector2(44f, 44f);
                irt.anchoredPosition = new Vector2(10f, 0f);
                var iimg = icon.GetComponent<Image>();
                iimg.sprite = _app.Assets.Image(SystemIcons.Speaker);
                iimg.preserveAspect = true;
                iimg.raycastTarget = false;
                iimg.enabled = iimg.sprite != null;
            }

            var label = UiKit.CreateLabel(chip.transform, text, 56f);
            var lrt = label.rectTransform;
            lrt.anchorMin = Vector2.zero;
            lrt.anchorMax = Vector2.one;
            lrt.offsetMin = new Vector2(10f + iconWidth, 4f);
            lrt.offsetMax = new Vector2(-10f, -4f);
            label.raycastTarget = false;

            var width = label.GetPreferredValues(text, 10000f, ChipHeight).x + 28f + iconWidth;
            var le = chip.GetComponent<LayoutElement>();
            le.preferredWidth = Mathf.Clamp(width, ChipHeight, 340f);
            le.minWidth = ChipHeight;

            var button = chip.GetComponent<Button>();
            button.targetGraphic = img;
            button.interactable = hasAudio;
            var colors = button.colors;
            colors.disabledColor = Color.white;
            button.colors = colors;
            if (hasAudio) button.onClick.AddListener(() => _ = _app.Speech.PlayAsync(audio));
            chip.GetComponent<TapFeedback>().Sound = null;
            return button;
        }

        private static TextMeshProUGUI LeftLabel(Transform parent, string text, float size)
        {
            var label = UiKit.CreateLabel(parent, text, size);
            label.alignment = TextAlignmentOptions.Left;
            return label;
        }

        /// <summary>Đặt theo góc trái: <paramref name="top"/> 1 là góc trên trái, 0 là góc dưới trái.</summary>
        private static void PlaceLeft(RectTransform rt, float top, Vector2 position, Vector2 size)
        {
            rt.anchorMin = new Vector2(0f, top);
            rt.anchorMax = new Vector2(0f, top);
            rt.pivot = new Vector2(0f, top);
            rt.sizeDelta = size;
            rt.anchoredPosition = position;
        }

        private static void Place(RectTransform rt, Vector2 anchor, Vector2 size, Vector2 position)
        {
            rt.anchorMin = anchor;
            rt.anchorMax = anchor;
            rt.pivot = anchor;
            rt.sizeDelta = size;
            rt.anchoredPosition = position;
        }

        private GameObject Panel(string name)
        {
            var go = new GameObject(name, typeof(RectTransform));
            go.transform.SetParent(transform, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            return go;
        }
    }
}
