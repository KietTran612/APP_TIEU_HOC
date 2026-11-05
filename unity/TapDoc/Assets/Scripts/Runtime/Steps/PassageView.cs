using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Đọc cả bài (thiết kế tập 2, mục 7.2): bài hiện như trang sách, tên tác giả ở cuối. "Nghe cả bài" đọc lần lượt
    /// các câu (dùng lại âm thanh của từng câu), câu đang đọc được tô. Chạm tiếng nào thì nghe đánh vần tiếng đó.
    /// Bài dài chia trang; "Con đọc xong rồi" để đi tiếp.
    /// </summary>
    public class PassageView : StepViewBase
    {
        internal const float TextWidth = 1120f;
        internal const float TextCenterX = -100f;
        internal const float FontSize = 56f;
        private const float BigButton = 160f;

        private ReadingText _text;
        private Button _doneButton;
        private TMPro.TextMeshProUGUI _author;
        private PageButtons _pager;
        private int _generation;
        private int _reading = -1;

        internal ReadingText Text => _text;

        protected override void Build()
        {
            AddMarker();
            var poem = Step.labels != null && Step.labels.Count > 1 && Step.labels[1] == "poem";
            _text = ReadingText.Create(Root.transform, Step.rows, Step.items, poem, new Vector2(TextWidth, 460f),
                new Vector2(TextCenterX, 105f), FontSize);
            _text.WordTapped += OnWordTapped;
            _text.SetLook(Look);

            var author = Step.labels != null && Step.labels.Count > 0 ? Step.labels[0] : null;
            if (!string.IsNullOrEmpty(author))
            {
                _author = UiKit.CreateLabel(Root.transform, author, 32f);
                _author.alignment = TMPro.TextAlignmentOptions.Right;
                var rt = _author.rectTransform;
                rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
                rt.sizeDelta = new Vector2(TextWidth, 56f);
                rt.anchoredPosition = new Vector2(TextCenterX, -152f);
            }

            var listen = UiKit.CreateIconButton(Root.transform, Ctx.Assets, SystemIcons.Speaker, UiText.ListenAll, OnListen);
            Place(listen, new Vector2(TextCenterX - 110f, -262f));
            _doneButton = UiKit.CreateIconButton(Root.transform, Ctx.Assets, SystemIcons.Check, UiText.DoneReading, Complete,
                Palette.Orange);
            _doneButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;
            Place(_doneButton, new Vector2(TextCenterX + 110f, -262f));

            if (_text.PageCount > 1) _pager = new PageButtons(Root.transform, Ctx.Assets, () => ShowPage(_text.Page - 1), () => ShowPage(_text.Page + 1));
            ShowPage(0);
        }

        private static void Place(Button b, Vector2 pos)
        {
            var rt = (RectTransform)b.transform;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = new Vector2(BigButton, BigButton);
            rt.anchoredPosition = pos;
        }

        private void ShowPage(int page)
        {
            _text.ShowPage(page);
            _pager?.Show(_text.Page, _text.PageCount);
            // Tên tác giả in ở cuối bài: chỉ hiện ở trang cuối.
            if (_author != null) _author.gameObject.SetActive(_text.Page == _text.PageCount - 1);
        }

        private WordLook Look(int word) => _reading >= 0 && Step.items[word].row == _reading ? WordLook.Reading : WordLook.Normal;

        private void OnWordTapped(int index)
        {
            _generation++;
            SetReading(-1);
            var item = Step.items[index];
            var ids = item.spells.SelectMany(s => s.parts).Select(p => p.audio).ToList();
            if (ids.Count == 0 || ids[ids.Count - 1] != item.audio) ids.Add(item.audio);
            _ = Ctx.Speech.PlaySequenceAsync(ids);
        }

        private async void OnListen()
        {
            var gen = ++_generation;
            for (var s = 0; s < Step.rows.Count; s++)
            {
                if (_text.PageOfSentence(s) != _text.Page) ShowPage(_text.PageOfSentence(s));
                SetReading(s);
                var finished = await Ctx.Speech.PlayAsync(Step.rows[s].audio);
                if (!IsAlive || gen != _generation) return;
                if (!finished) break;
            }
            SetReading(-1);
        }

        private void SetReading(int sentence)
        {
            _reading = sentence;
            if (IsAlive) _text.Refresh();
        }

        internal int ReadingSentence => _reading;

        public override void Replay() => OnListen();

        protected override void ActForTest() => _doneButton.onClick.Invoke();
    }
}
