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
        private const float RowHeight = 210f;
        private const float ChipHeight = 90f;

        private static readonly Color RowColor = new(1f, 0.99f, 0.95f, 1f);
        private static readonly Color ChipColor = new(1f, 0.92f, 0.62f, 1f);
        private static readonly Color MutedText = new(0.45f, 0.43f, 0.4f, 1f);

        private AppRoot _app;
        private GameObject _gatePanel;
        private GameObject _progressPanel;
        private GameObject _appendixPanel;
        private TMP_Text _questionLabel;
        private readonly List<Button> _choiceButtons = new();

        internal ParentGate Gate { get; private set; }
        internal IReadOnlyList<Button> ChoiceButtons => _choiceButtons;
        internal Button BackButton { get; private set; }
        internal bool IsUnlocked => _progressPanel != null && _progressPanel.activeSelf;

        public void Build(AppRoot app)
        {
            _app = app;
            Gate = new ParentGate(new System.Random());

            BackButton = UiKit.CreateButton(transform, UiText.Back, app.ShowLessonList);
            var backRt = (RectTransform)BackButton.transform;
            backRt.anchorMin = new Vector2(0f, 1f);
            backRt.anchorMax = new Vector2(0f, 1f);
            backRt.pivot = new Vector2(0f, 1f);
            backRt.sizeDelta = new Vector2(220f, UiKit.MinTouch);
            backRt.anchoredPosition = new Vector2(20f, -20f);

            var header = UiKit.CreateLabel(transform, UiText.Parent, 64f);
            Place(header.rectTransform, new Vector2(0.5f, 1f), new Vector2(800f, UiKit.MinTouch), new Vector2(0f, -20f));

            _gatePanel = Panel("GatePanel");
            BuildGate();
            _progressPanel = Panel("ProgressPanel");
            _progressPanel.SetActive(false);
        }

        /// <summary>Móc cho test: bấm nút đáp án đúng.</summary>
        internal void SimulateUnlock()
        {
            var k = Gate.Choices.ToList().IndexOf(Gate.Expected);
            _choiceButtons[k].onClick.Invoke();
        }

        private void BuildGate()
        {
            var prompt = UiKit.CreateLabel(_gatePanel.transform, UiText.ParentGatePrompt, 48f);
            Place(prompt.rectTransform, new Vector2(0.5f, 1f), new Vector2(1000f, 110f), new Vector2(0f, -220f));

            _questionLabel = UiKit.CreateLabel(_gatePanel.transform, Gate.Question, 110f);
            Place(_questionLabel.rectTransform, new Vector2(0.5f, 0.5f), new Vector2(1000f, 180f), new Vector2(0f, 60f));

            const float width = 280f, gap = 60f;
            for (var k = 0; k < Gate.Choices.Count; k++)
            {
                var index = k;
                var button = UiKit.CreateButton(_gatePanel.transform, string.Empty, () => OnChoice(index));
                button.name = $"Choice_{k}";
                var x = -((Gate.Choices.Count - 1) * (width + gap)) / 2f + k * (width + gap);
                Place((RectTransform)button.transform, new Vector2(0.5f, 0.5f), new Vector2(width, UiKit.MinTouch), new Vector2(x, -200f));
                button.GetComponentInChildren<TMP_Text>().fontSizeMax = 64f;
                _choiceButtons.Add(button);
            }
            RefreshGate();
        }

        private void RefreshGate()
        {
            _questionLabel.text = Gate.Question;
            for (var k = 0; k < _choiceButtons.Count; k++)
            {
                _choiceButtons[k].GetComponentInChildren<TMP_Text>().text = Gate.Choices[k].ToString();
            }
        }

        private void OnChoice(int index)
        {
            if (IsUnlocked || index < 0 || index >= Gate.Choices.Count) return;
            if (Gate.Answer(Gate.Choices[index]))
            {
                Unlock();
            }
            else
            {
                RefreshGate();
            }
        }

        private void Unlock()
        {
            _gatePanel.SetActive(false);
            BuildProgress();
            _progressPanel.SetActive(true);
        }

        private void BuildProgress()
        {
            var scrollGo = new GameObject("Children", typeof(RectTransform), typeof(ScrollRect));
            scrollGo.transform.SetParent(_progressPanel.transform, false);
            var scrollRt = (RectTransform)scrollGo.transform;
            scrollRt.anchorMin = Vector2.zero;
            scrollRt.anchorMax = Vector2.one;
            scrollRt.offsetMin = new Vector2(40f, 20f);
            scrollRt.offsetMax = new Vector2(-40f, -200f);

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

            var ordered = LessonRepository.LoadIndex().lessons.Select(e => e.lesson_id).ToList();
            var appendix = UiKit.CreateButton(contentGo.transform, UiText.BookAppendix, OpenAppendix);
            appendix.GetComponent<LayoutElement>().preferredHeight = UiKit.MinTouch;
            var lessons = new Dictionary<string, Lesson>();
            foreach (var profile in _app.Progress.Profiles)
            {
                BuildRow(contentGo.transform, profile, ordered, lessons);
            }
        }

        private void OpenAppendix()
        {
            if (_appendixPanel == null)
            {
                // Mọi bài trong danh sách thuộc cùng một quyển sách: Phụ lục lấy theo mã sách đó.
                var book = LessonRepository.LoadIndex().lessons.First().book;
                _appendixPanel = NotesPanel.ForAppendix(transform, AppendixData.Load(book));
            }
            _appendixPanel.transform.SetAsLastSibling();
            _appendixPanel.SetActive(true);
        }

        private void BuildRow(Transform content, Profile profile, List<string> ordered, Dictionary<string, Lesson> lessons)
        {
            var row = new GameObject($"Child_{profile.id}", typeof(RectTransform), typeof(Image), typeof(LayoutElement));
            row.transform.SetParent(content, false);
            var le = row.GetComponent<LayoutElement>();
            le.minHeight = RowHeight;
            le.preferredHeight = RowHeight;
            var bg = row.GetComponent<Image>();
            bg.sprite = UiKit.WhiteSprite;
            bg.color = RowColor;

            var avatarBox = new GameObject("AvatarBox", typeof(RectTransform));
            avatarBox.transform.SetParent(row.transform, false);
            PlaceLeft((RectTransform)avatarBox.transform, 1f, new Vector2(20f, -14f), new Vector2(100f, 100f));
            ProfileScreen.AddAvatar(avatarBox.transform, _app.Assets, profile.avatar, profile.name);

            var name = LeftLabel(row.transform, profile.name, 48f);
            PlaceLeft(name.rectTransform, 1f, new Vector2(140f, -14f), new Vector2(520f, 100f));
            name.overflowMode = TextOverflowModes.Ellipsis;

            var learned = ordered.Count(id => ProgressStore.IsCompleted(profile, id));
            var progress = LeftLabel(row.transform, string.Format(UiText.LearnedFormat, learned, ordered.Count), 44f);
            PlaceLeft(progress.rectTransform, 1f, new Vector2(680f, -14f), new Vector2(620f, 100f));

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
            if (confusions.Count == 0)
            {
                var none = LeftLabel(chipsGo.transform, UiText.NoConfusion, 36f);
                none.color = MutedText;
                none.gameObject.AddComponent<LayoutElement>().preferredWidth = 400f;
            }
            foreach (var text in confusions)
            {
                AddChip(chipsGo.transform, text);
            }
        }

        /// <summary>
        /// Tối đa 5 chữ bé hay nhầm: đáp án đúng của các lượt bé nhầm, gộp chữ trùng nhau, nhầm nhiều trước rồi mới
        /// nhầm trước. Lượt lỗi thời (bài không nạp được, chỉ số lượt hay đáp án không còn) bị bỏ qua.
        /// </summary>
        private static List<string> Confusions(Profile profile, Dictionary<string, Lesson> lessons)
        {
            var totals = new Dictionary<string, (int count, long last)>();
            foreach (var mistake in ProgressStore.MistakesOf(profile, int.MaxValue))
            {
                var text = AnswerText(mistake, lessons);
                if (string.IsNullOrEmpty(text)) continue;
                totals.TryGetValue(text, out var t);
                totals[text] = (t.count + mistake.count, Math.Max(t.last, mistake.last_ticks));
            }
            return totals
                .OrderByDescending(p => p.Value.count)
                .ThenByDescending(p => p.Value.last)
                .Select(p => p.Key)
                .Take(MaxConfusions)
                .ToList();
        }

        private static string AnswerText(Mistake mistake, Dictionary<string, Lesson> lessons)
        {
            if (!lessons.TryGetValue(mistake.lesson_id, out var lesson))
            {
                try
                {
                    lesson = LessonRepository.Load(mistake.lesson_id);
                }
                catch (Exception)
                {
                    lesson = null;
                }
                lessons[mistake.lesson_id] = lesson;
            }
            if (lesson?.part2 == null || mistake.round < 0 || mistake.round >= lesson.part2.Count) return null;
            var round = lesson.part2[mistake.round];
            if (round?.options == null || round.answer < 0 || round.answer >= round.options.Count) return null;
            // Lượt nhìn chữ kéo dấu: phương án là kí hiệu dấu; phụ huynh cần thấy chữ mẫu có dấu (ví dụ "cá").
            if (round.kind == "look_tone" && !string.IsNullOrEmpty(round.prompt_text)) return round.prompt_text;
            return round.options[round.answer]?.text;
        }

        private static void AddChip(Transform parent, string text)
        {
            var chip = new GameObject("Confusion", typeof(RectTransform), typeof(Image), typeof(LayoutElement));
            chip.transform.SetParent(parent, false);
            var img = chip.GetComponent<Image>();
            img.sprite = UiKit.WhiteSprite;
            img.color = ChipColor;
            img.raycastTarget = false;

            var label = UiKit.CreateLabel(chip.transform, text, 56f);
            var lrt = label.rectTransform;
            lrt.anchorMin = Vector2.zero;
            lrt.anchorMax = Vector2.one;
            lrt.offsetMin = new Vector2(10f, 4f);
            lrt.offsetMax = new Vector2(-10f, -4f);

            var width = label.GetPreferredValues(text, 10000f, ChipHeight).x + 28f;
            var le = chip.GetComponent<LayoutElement>();
            le.preferredWidth = Mathf.Clamp(width, ChipHeight, 300f);
            le.minWidth = ChipHeight;
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
