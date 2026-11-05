using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Học thuộc lòng (thiết kế tập 2, mục 7.2): bài thơ hiện đủ; mỗi lần bấm "Ẩn bớt" thì che thêm một mức tiếng
    /// (mức 1 khoảng một phần ba, mức 2 khoảng hai phần ba, mức 3 chỉ còn tiếng đầu mỗi dòng), bấm ở mức 3 thì hiện
    /// hết. Chạm ô bị che thì tiếng đó hiện lại và được đọc. "Nghe cả bài" luôn có; "Con thuộc rồi" đi tiếp ở mức nào
    /// cũng được.
    /// </summary>
    public class MemorizeView : StepViewBase
    {
        internal const int MaxLevel = 3;
        private const float BigButton = 160f;

        private ReadingText _text;
        private Button _hideButton;
        private Button _doneButton;
        private PageButtons _pager;
        private readonly HashSet<int> _revealed = new();
        private int _generation;
        private int _reading = -1;

        internal int Level { get; private set; }
        internal ReadingText Text => _text;

        protected override void Build()
        {
            AddMarker();
            var hasQuestion = !string.IsNullOrEmpty(Step.text);
            if (hasQuestion)
            {
                // Câu lệnh của sách ("Học thuộc lòng cả bài.") ở trên bài thơ.
                var question = UiKit.CreateLabel(Root.transform, Step.text, 44f);
                var qrt = question.rectTransform;
                qrt.anchorMin = qrt.anchorMax = new Vector2(0.5f, 0.5f);
                qrt.sizeDelta = new Vector2(PassageView.TextWidth, 70f);
                qrt.anchoredPosition = new Vector2(PassageView.TextCenterX + 40f, 285f);
                question.alignment = TMPro.TextAlignmentOptions.Left;
            }
            _text = ReadingText.Create(Root.transform, Step.rows, Step.items, true,
                new Vector2(PassageView.TextWidth, hasQuestion ? 360f : 420f),
                new Vector2(PassageView.TextCenterX, hasQuestion ? 60f : 90f), PassageView.FontSize);
            _text.WordTapped += OnWordTapped;
            _text.SetLook(Look);

            _hideButton = UiKit.CreateButton(Root.transform, UiText.HideMore, NextLevel);
            Place(_hideButton, new Vector2(PassageView.TextCenterX - 300f, -250f), new Vector2(300f, BigButton));
            var listen = UiKit.CreateIconButton(Root.transform, Ctx.Assets, SystemIcons.Speaker, UiText.ListenAll, OnListen);
            Place(listen, new Vector2(PassageView.TextCenterX, -250f), new Vector2(BigButton, BigButton));
            _doneButton = UiKit.CreateIconButton(Root.transform, Ctx.Assets, SystemIcons.Check, UiText.Memorized, Complete,
                Palette.Orange);
            _doneButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;
            Place(_doneButton, new Vector2(PassageView.TextCenterX + 220f, -250f), new Vector2(BigButton, BigButton));

            if (_text.PageCount > 1) _pager = new PageButtons(Root.transform, Ctx.Assets, () => ShowPage(_text.Page - 1), () => ShowPage(_text.Page + 1));
            ShowPage(0);
            var intro = new System.Collections.Generic.List<string>();
            if (hasQuestion) intro.Add(Step.audio);
            intro.Add(SystemAudio.hd_hoc_thuoc);
            _ = Ctx.Speech.PlaySequenceAsync(intro);
        }

        private static void Place(Button b, Vector2 pos, Vector2 size)
        {
            var rt = (RectTransform)b.transform;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = size;
            rt.anchoredPosition = pos;
        }

        private void ShowPage(int page)
        {
            _text.ShowPage(page);
            _pager?.Show(_text.Page, _text.PageCount);
        }

        internal bool IsHidden(int word)
        {
            var level = Step.items[word].level;
            return level > 0 && level <= Level && !_revealed.Contains(word);
        }

        private WordLook Look(int word)
        {
            if (IsHidden(word)) return WordLook.Hidden;
            return _reading >= 0 && Step.items[word].row == _reading ? WordLook.Reading : WordLook.Normal;
        }

        /// <summary>Che thêm một mức; ở mức cao nhất thì quay về hiện hết.</summary>
        internal void NextLevel()
        {
            Level = Level >= MaxLevel ? 0 : Level + 1;
            _revealed.Clear();
            _hideButton.GetComponentInChildren<TMPro.TMP_Text>().text = Level >= MaxLevel ? UiText.ShowAll : UiText.HideMore;
            _text.Refresh();
        }

        private void OnWordTapped(int index)
        {
            _generation++;
            _reading = -1;
            _revealed.Add(index);
            _text.Refresh();
            _ = Ctx.Speech.PlayAsync(Step.items[index].audio);
        }

        private async void OnListen()
        {
            var gen = ++_generation;
            for (var s = 0; s < Step.rows.Count; s++)
            {
                if (_text.PageOfSentence(s) != _text.Page) ShowPage(_text.PageOfSentence(s));
                _reading = s;
                _text.Refresh();
                var finished = await Ctx.Speech.PlayAsync(Step.rows[s].audio);
                if (!IsAlive || gen != _generation) return;
                if (!finished) break;
            }
            _reading = -1;
            _text.Refresh();
        }

        public override void Replay() => OnListen();

        protected override void ActForTest() => _doneButton.onClick.Invoke();
    }
}
