using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Điền từ vào đoạn văn (lớp 2, thiết kế TV2 tập một mục 6), từng câu một như màn điền chỗ trống: câu đang làm hiện
    /// to, ô đang điền là "……" gạch chân; bên dưới một hàng thẻ (đáp án và hai từ khác của sách, hoặc lựa chọn riêng
    /// của ô). Bé chạm hoặc kéo thẻ vào câu: đúng thì chữ hiện vào ô, sai thì thẻ lắc, không chê; sai hai lần ở một ô
    /// thì thẻ đúng được tô gợi ý. Đủ ô của một câu thì app đọc cả câu rồi sang câu sau. Điền hết thì khen và đi tiếp.
    /// </summary>
    public class FillPassageView : StepViewBase
    {
        private const string Gap = "……";
        private const int MaxChoices = 3;
        private const float ChoiceY = -215f;
        private const float ChoiceGap = 24f;

        private readonly List<Item> _blanks = new();
        private readonly List<int> _blankItemIndex = new();
        private readonly HashSet<int> _filled = new();
        private readonly List<Tile> _choiceTiles = new();
        private readonly Dictionary<int, RoundFeedback> _feedback = new();
        private TMPro.TextMeshProUGUI _sentence;
        private TMPro.TextMeshProUGUI _progress;
        private bool _busy;
        private bool _auto;

        /// <summary>Ô đang điền; -1 khi đã điền hết.</summary>
        internal int Selected { get; private set; }
        internal int FilledCount => _filled.Count;

        /// <summary>Các thẻ đang hiện cho ô đang điền.</summary>
        internal IReadOnlyList<string> CurrentChoices { get; private set; } = new List<string>();

        /// <summary>Chữ đã điền vào ô <paramref name="blank"/>; <c>null</c> khi ô còn trống.</summary>
        internal string FilledText(int blank) => _filled.Contains(blank) ? _blanks[blank].answer : null;

        /// <summary>Thẻ có chữ <paramref name="text"/> trong hàng thẻ đang hiện.</summary>
        internal Tile ChoiceTile(string text) => _choiceTiles.FirstOrDefault(t => t.PlainText == text);

        protected override void Build()
        {
            AddMarker();
            for (var i = 0; i < Step.items.Count; i++)
            {
                if (Step.items[i].role != "blank") continue;
                _blanks.Add(Step.items[i]);
                _blankItemIndex.Add(i);
            }
            _progress = UiKit.CreateLabel(Root.transform, string.Empty, 40f);
            var prt = _progress.rectTransform;
            prt.anchorMin = prt.anchorMax = new Vector2(0.5f, 0.5f);
            prt.sizeDelta = new Vector2(300f, 60f);
            prt.anchoredPosition = new Vector2(0f, 290f);

            _sentence = UiKit.CreateLabel(Root.transform, string.Empty, 60f);
            var srt = _sentence.rectTransform;
            srt.anchorMin = srt.anchorMax = new Vector2(0.5f, 0.5f);
            srt.sizeDelta = new Vector2(FlowWidth, 330f);
            srt.anchoredPosition = new Vector2(0f, 75f);
            _sentence.enableAutoSizing = true;
            _sentence.fontSizeMax = 60f;
            _sentence.fontSizeMin = 32f;
            _sentence.richText = true;
            _sentence.gameObject.AddComponent<DropSlot>();

            Select(0);
            _ = Ctx.Speech.PlayAsync(SystemAudio.hd_keo_vao_cho_trong);
        }

        private int RowOf(int blank) => _blanks[blank].row;

        /// <summary>Câu chứa ô <paramref name="blank"/>: chữ thường, ô đã điền tô màu, ô đang điền gạch chân.</summary>
        private string SentenceText(int blank)
        {
            var row = RowOf(blank);
            var sb = new StringBuilder();
            for (var i = 0; i < Step.items.Count; i++)
            {
                var item = Step.items[i];
                if (item.row != row) continue;
                string piece;
                if (item.role != "blank") piece = item.text;
                else
                {
                    var b = _blankItemIndex.IndexOf(i);
                    piece = _filled.Contains(b) ? $"<color=#{ColorUtility.ToHtmlStringRGB(Palette.Teal)}>{item.answer}</color>"
                        : b == blank ? $"<u><color=#{ColorUtility.ToHtmlStringRGB(Palette.Orange)}>{Gap}</color></u>" : Gap;
                }
                if (sb.Length > 0 && !piece.StartsWith(",") && !piece.StartsWith(".") && !piece.StartsWith(":")) sb.Append(' ');
                sb.Append(piece);
            }
            return sb.ToString();
        }

        /// <summary>
        /// Thẻ của ô: lựa chọn riêng nếu có; không thì đáp án và hai từ khác của sách (ưu tiên từ chưa dùng), thứ tự cố
        /// định theo ô để bé làm lại vẫn như cũ.
        /// </summary>
        private List<string> ChoicesFor(int blank)
        {
            var item = _blanks[blank];
            var own = item.choices != null && item.choices.Count > 0 && (Step.labels == null || Step.labels.Count == 0);
            List<string> choices;
            if (own) choices = item.choices.Take(MaxChoices).ToList();
            else
            {
                var used = new HashSet<string>(_filled.Select(b => _blanks[b].answer));
                var bank = Step.labels.Count > 0 ? Step.labels : item.choices;
                var start = Mathf.Max(0, bank.IndexOf(item.answer));
                var others = Enumerable.Range(1, bank.Count).Select(k => bank[(start + k) % bank.Count])
                    .Where(w => w != item.answer).Distinct().OrderBy(w => used.Contains(w) ? 1 : 0).Take(MaxChoices - 1).ToList();
                choices = new List<string> { item.answer };
                choices.AddRange(others);
                var shift = blank % choices.Count;
                choices = choices.Skip(shift).Concat(choices.Take(shift)).ToList();
            }
            if (!choices.Contains(item.answer)) choices[0] = item.answer;
            return choices;
        }

        private void Select(int blank)
        {
            Selected = blank;
            foreach (var t in _choiceTiles) Object.Destroy(t.gameObject);
            _choiceTiles.Clear();
            if (blank < 0) return;
            _sentence.text = SentenceText(blank);
            _progress.text = $"{blank + 1}/{_blanks.Count}";
            var choices = ChoicesFor(blank);
            CurrentChoices = choices;
            var maxW = (FlowWidth - ChoiceGap * (MaxChoices - 1)) / MaxChoices;
            var widths = choices.Select(c => Mathf.Clamp(34f * c.Length + 80f, 260f, maxW)).ToList();
            var total = widths.Sum() + ChoiceGap * (widths.Count - 1);
            var x = -total / 2f;
            for (var k = 0; k < choices.Count; k++)
            {
                var text = choices[k];
                var tile = AddTile(text, new Vector2(widths[k], UiKit.MinTouch), new Vector2(x + widths[k] / 2f, ChoiceY), 52f);
                x += widths[k] + ChoiceGap;
                var drag = tile.gameObject.AddComponent<DragTile>();
                drag.DroppedOn += slot => { if (slot != null && slot.gameObject == _sentence.gameObject) _ = Answer(text, tile); };
                tile.Tapped += () => _ = Answer(text, tile);
                _choiceTiles.Add(tile);
            }
        }

        private async Awaitable Answer(string choice, Tile chosen)
        {
            if (_busy || IsCompleted || Selected < 0) return;
            _busy = true;
            var blank = Selected;
            var item = _blanks[blank];
            if (!_feedback.TryGetValue(blank, out var feedback)) _feedback[blank] = feedback = new RoundFeedback(Ctx, blank);
            var ok = await feedback.Handle(choice == item.answer, ChoiceTile(item.answer), chosen);
            if (!IsAlive) return;
            if (!ok)
            {
                _busy = false;
                return;
            }
            _filled.Add(blank);
            var next = -1;
            for (var i = 0; i < _blanks.Count && next < 0; i++)
                if (!_filled.Contains(i)) next = i;
            var row = RowOf(blank);
            var sentenceDone = next < 0 || RowOf(next) != row;
            _sentence.text = SentenceText(next >= 0 && !sentenceDone ? next : blank);
            if (sentenceDone)
            {
                // Âm thanh câu có thể bị cắt ngang ("Nghe lại"): điền đúng rồi thì vẫn sang câu sau.
                var audio = Step.rows.FirstOrDefault(r => r.row == row)?.audio;
                if (!string.IsNullOrEmpty(audio)) await Ctx.Speech.PlayAsync(audio);
                if (!IsAlive) return;
            }
            _busy = false;
            if (next >= 0)
            {
                Select(next);
                if (_auto) AnswerCorrectly();
                return;
            }
            Select(-1);
            await Ctx.Speech.PlayAsync(SystemAudio.khen_01);
            if (IsAlive) Complete();
        }

        private void AnswerCorrectly()
        {
            if (Selected < 0) return;
            var answer = _blanks[Selected].answer;
            _ = Answer(answer, ChoiceTile(answer));
        }

        public override void Replay() => _ = Ctx.Speech.PlayAsync(SystemAudio.hd_keo_vao_cho_trong);

        protected override void ActForTest()
        {
            _auto = true;
            AnswerCorrectly();
        }
    }
}
