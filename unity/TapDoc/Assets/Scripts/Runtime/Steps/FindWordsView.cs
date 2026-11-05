using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Câu hỏi về chữ (thiết kế tập 2, mục 7.2): "Tìm tiếng trong bài có vần ươn". App đọc câu hỏi; bé chạm các tiếng
    /// trong bài. Tiếng đúng sáng lên, tô phần được hỏi rồi app đánh vần (hoặc đọc) tiếng đó. Tiếng không đúng chỉ
    /// được đọc lên, không chê. Một tiếng lặp nhiều lần chỉ cần chạm một lần. Hai lần chạm chưa đúng liền nhau thì
    /// một tiếng còn thiếu được tô vàng gợi ý. Tìm đủ thì khen và đi tiếp.
    /// </summary>
    public class FindWordsView : StepViewBase
    {
        private ReadingText _text;
        private TMPro.TextMeshProUGUI _count;
        private PageButtons _pager;
        private readonly HashSet<string> _found = new();
        private string _hint;
        private int _misses;

        internal int FoundCount => _found.Count;
        internal string HintWord => _hint;
        internal ReadingText Text => _text;

        protected override void Build()
        {
            AddMarker();
            var question = UiKit.CreateLabel(Root.transform, Step.text, 46f);
            var qrt = question.rectTransform;
            qrt.anchorMin = qrt.anchorMax = new Vector2(0.5f, 0.5f);
            qrt.sizeDelta = new Vector2(PassageView.TextWidth, 130f);
            qrt.anchoredPosition = new Vector2(PassageView.TextCenterX + 40f, 250f);
            question.alignment = TMPro.TextAlignmentOptions.Left;

            _text = ReadingText.Create(Root.transform, Step.rows, Step.items, false, new Vector2(PassageView.TextWidth, 360f),
                new Vector2(PassageView.TextCenterX, -10f), PassageView.FontSize);
            _text.WordTapped += OnWordTapped;
            _text.SetLook(Look);

            _count = UiKit.CreateLabel(Root.transform, string.Empty, 40f);
            var crt = _count.rectTransform;
            crt.anchorMin = crt.anchorMax = new Vector2(0.5f, 0.5f);
            crt.sizeDelta = new Vector2(400f, 60f);
            crt.anchoredPosition = new Vector2(PassageView.TextCenterX, -250f);
            UpdateCount();

            if (_text.PageCount > 1) _pager = new PageButtons(Root.transform, Ctx.Assets, () => ShowPage(_text.Page - 1), () => ShowPage(_text.Page + 1));
            ShowPage(0);
            Replay();
        }

        private int Need => Mathf.Max(1, Step.need);

        private void ShowPage(int page)
        {
            _text.ShowPage(page);
            _pager?.Show(_text.Page, _text.PageCount);
        }

        private static string Key(Item word) => word.text.ToLowerInvariant();

        private WordLook Look(int index)
        {
            var word = Step.items[index];
            if (word.role == "target" && _found.Contains(Key(word))) return WordLook.Found;
            if (_hint != null && Key(word) == _hint) return WordLook.Hint;
            return WordLook.Normal;
        }

        private void UpdateCount() => _count.text = string.Format(UiText.FoundFormat, Mathf.Min(_found.Count, Need), Need);

        private async void OnWordTapped(int index)
        {
            var word = Step.items[index];
            if (word.role != "target")
            {
                _ = Ctx.Speech.PlayAsync(word.audio);
                if (++_misses >= 2) ShowHint();
                return;
            }
            _misses = 0;
            var isNew = _found.Add(Key(word));
            if (_hint == Key(word)) _hint = null;
            _text.Refresh();
            UpdateCount();
            if (isNew) Ctx.Fx?.Correct((RectTransform)_text.transform);
            var ids = word.spells.SelectMany(s => s.parts).Select(p => p.audio).ToList();
            if (ids.Count == 0 || ids[ids.Count - 1] != word.audio) ids.Add(word.audio);
            // Âm thanh có thể bị cắt ngang (bé chạm tiếng khác, bấm "Nghe lại"): tìm đủ thì vẫn xong bước.
            await Ctx.Speech.PlaySequenceAsync(ids);
            if (!IsAlive || IsCompleted || _found.Count < Need) return;
            await Ctx.Speech.PlayAsync(SystemAudio.khen_01);
            if (IsAlive) Complete();
        }

        /// <summary>Tô vàng tiếng đúng đầu tiên chưa tìm, mở trang có tiếng đó.</summary>
        private void ShowHint()
        {
            for (var i = 0; i < Step.items.Count; i++)
            {
                var word = Step.items[i];
                if (word.role != "target" || _found.Contains(Key(word))) continue;
                _hint = Key(word);
                if (_text.PageOfWord(i) != _text.Page) ShowPage(_text.PageOfWord(i));
                _text.Refresh();
                return;
            }
        }

        public override void Replay() =>
            _ = Ctx.Speech.PlaySequenceAsync(new List<string> { Step.audio, SystemAudio.hd_tim_tieng });

        protected override void ActForTest()
        {
            var keys = new HashSet<string>();
            for (var i = 0; i < Step.items.Count && keys.Count < Need; i++)
            {
                if (Step.items[i].role == "target" && keys.Add(Key(Step.items[i]))) _text.SimulateTapWord(i);
            }
        }
    }
}
