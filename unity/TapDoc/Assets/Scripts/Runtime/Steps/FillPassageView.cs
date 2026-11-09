using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Điền từ vào đoạn văn (lớp 2, thiết kế TV2 tập một mục 6): đoạn văn có các ô trống, hàng thẻ từ bên dưới (từ cho
    /// sẵn của sách, hoặc lựa chọn riêng của ô đang chọn). Bé chạm ô rồi chạm thẻ, hoặc kéo thẻ vào ô. Đúng thì ô điền
    /// chữ và app đọc cả câu; sai thì thẻ lắc, không chê; sai hai lần ở một ô thì thẻ đúng được tô gợi ý. Chạm thẻ khi
    /// chưa chọn ô thì điền vào ô trống đầu tiên còn lại. Điền đủ thì khen và đi tiếp. Đoạn dài thì chia trang theo câu.
    /// </summary>
    public class FillPassageView : StepViewBase
    {
        private const float TextWidth = 1080f;
        private const float TextTop = 300f;
        private const float TextHeight = 360f;
        private const float WordH = 70f;
        private const float WordGap = 12f;
        private const float LineGap = 14f;
        private const float WordFont = 44f;
        private const float ChoiceY = -200f;
        private const float ChoiceH = 100f;

        private sealed class Token
        {
            public string Text;
            public int Row;
            public int Blank = -1;  // chỉ số ô, -1 là chữ thường
            public float Width;
        }

        private readonly List<Token> _tokens = new();
        private readonly List<Item> _blankItems = new();
        private readonly Dictionary<int, Tile> _blankTiles = new();
        private readonly List<Tile> _wordTiles = new();
        private readonly List<Tile> _choiceTiles = new();
        private readonly HashSet<int> _filled = new();
        private readonly Dictionary<int, RoundFeedback> _feedback = new();
        private List<List<int>> _pages; // mỗi trang là danh sách chỉ số câu
        private PageButtons _pager;
        private int _page = -1;
        private bool _busy;
        private bool _auto;

        /// <summary>Ô đang chọn (thẻ chạm vào sẽ điền ô này); -1 khi đã điền hết.</summary>
        internal int Selected { get; private set; }
        internal int FilledCount => _filled.Count;
        internal int PageCount => _pages.Count;

        /// <summary>Chữ đã điền vào ô <paramref name="blank"/>; <c>null</c> khi ô còn trống.</summary>
        internal string FilledText(int blank) => _filled.Contains(blank) ? _blankItems[blank].answer : null;

        /// <summary>Thẻ của ô thứ <paramref name="blank"/> trên trang đang hiện; <c>null</c> khi ô ở trang khác.</summary>
        internal Tile BlankTile(int blank) => _blankTiles.TryGetValue(blank, out var t) ? t : null;

        /// <summary>Thẻ từ có chữ <paramref name="text"/>: ưu tiên thẻ đang hiện.</summary>
        internal Tile ChoiceTile(string text) =>
            _choiceTiles.FirstOrDefault(t => t.PlainText == text && t.gameObject.activeSelf)
            ?? _choiceTiles.FirstOrDefault(t => t.PlainText == text);

        private bool HasBank => Step.labels != null && Step.labels.Count > 0;

        private static float WordWidth(string text) => Mathf.Max(56f, 26f * text.Length + 36f);

        protected override void Build()
        {
            AddMarker();
            foreach (var item in Step.items)
            {
                if (item.role == "blank")
                {
                    var choices = item.choices != null && item.choices.Count > 0 ? item.choices : Step.labels;
                    var longest = Mathf.Max(item.answer.Length, choices.Count > 0 ? choices.Max(c => c.Length) : 0);
                    _tokens.Add(new Token { Text = item.answer, Row = item.row, Blank = _blankItems.Count,
                        Width = Mathf.Max(120f, 26f * longest + 60f) });
                    _blankItems.Add(item);
                    continue;
                }
                foreach (var word in (item.text ?? string.Empty).Split(' ').Where(w => w.Length > 0))
                    _tokens.Add(new Token { Text = word, Row = item.row, Width = WordWidth(word) });
            }
            _pages = Paginate();
            if (_pages.Count > 1) _pager = new PageButtons(Root.transform, Ctx.Assets, () => ShowPage(_page - 1), () => ShowPage(_page + 1));
            if (HasBank) BuildChoices(Step.labels);
            Select(0);
            _ = Ctx.Speech.PlayAsync(SystemAudio.hd_keo_vao_cho_trong);
        }

        /// <summary>Chia câu thành trang sao cho mỗi trang vừa khung chữ (câu không bị cắt giữa hai trang).</summary>
        private List<List<int>> Paginate()
        {
            var maxLines = Mathf.Max(1, Mathf.FloorToInt((TextHeight + LineGap) / (WordH + LineGap)));
            var rowsInOrder = _tokens.Select(t => t.Row).Distinct().ToList();
            var pages = new List<List<int>>();
            var current = new List<int>();
            foreach (var row in rowsInOrder)
            {
                var trial = current.Concat(new[] { row }).ToList();
                if (current.Count > 0 && LinesFor(trial) > maxLines)
                {
                    pages.Add(current);
                    current = new List<int> { row };
                }
                else current = trial;
            }
            if (current.Count > 0) pages.Add(current);
            return pages;
        }

        private int LinesFor(List<int> rows) =>
            FlowLayout.Lines(_tokens.Where(t => rows.Contains(t.Row)).Select(t => t.Width).ToList(), TextWidth, WordGap).Count;

        private int PageOfBlank(int blank) => _pages.FindIndex(p => p.Contains(_blankItems[blank].row));

        private void ShowPage(int page)
        {
            page = Mathf.Clamp(page, 0, _pages.Count - 1);
            if (page == _page) return;
            _page = page;
            foreach (var t in _wordTiles) Object.Destroy(t.gameObject);
            _wordTiles.Clear();
            foreach (var t in _blankTiles.Values) Object.Destroy(t.gameObject);
            _blankTiles.Clear();
            var rows = _pages[page];
            var tokens = _tokens.Where(t => rows.Contains(t.Row)).ToList();
            var centers = FlowLayout.Place(tokens.Select(t => t.Width).ToList(), WordH, TextWidth, WordGap, LineGap);
            var top = centers.Count > 0 ? centers.Max(c => c.y) : 0f;
            for (var k = 0; k < tokens.Count; k++)
            {
                var token = tokens[k];
                var pos = new Vector2(centers[k].x, TextTop - WordH / 2f - (top - centers[k].y));
                if (token.Blank < 0)
                {
                    var row = token.Row;
                    var word = AddTile(token.Text, new Vector2(token.Width, WordH), pos, WordFont);
                    word.Tapped += () => _ = Ctx.Speech.PlayAsync(RowAudio(row));
                    _wordTiles.Add(word);
                    continue;
                }
                var blank = token.Blank;
                var tile = AddTile(_filled.Contains(blank) ? token.Text : "……", new Vector2(token.Width, WordH), pos, WordFont);
                tile.Tapped += () => Select(blank);
                tile.gameObject.AddComponent<DropSlot>();
                tile.SetHighlighted(blank == Selected);
                _blankTiles[blank] = tile;
            }
            _pager?.Show(_page, _pages.Count);
        }

        private string RowAudio(int row) => Step.rows.FirstOrDefault(r => r.row == row)?.audio ?? Step.rows.ElementAtOrDefault(row)?.audio;

        private void BuildChoices(List<string> choices)
        {
            foreach (var t in _choiceTiles) Object.Destroy(t.gameObject);
            _choiceTiles.Clear();
            var widths = choices.Select(c => Mathf.Max(160f, 34f * c.Length + 60f)).ToList();
            var centers = FlowLayout.Place(widths, ChoiceH, FlowWidth, 24f, 16f);
            for (var k = 0; k < choices.Count; k++)
            {
                var text = choices[k];
                var tile = AddTile(text, new Vector2(widths[k], ChoiceH), centers[k] + new Vector2(0f, ChoiceY), 52f);
                var drag = tile.gameObject.AddComponent<DragTile>();
                drag.DroppedOn += slot =>
                {
                    var blank = _blankTiles.FirstOrDefault(p => p.Value != null && p.Value.gameObject == slot.gameObject).Key;
                    if (_blankTiles.ContainsKey(blank) && !_filled.Contains(blank))
                    {
                        Select(blank);
                        _ = Answer(text, tile);
                    }
                };
                tile.Tapped += () => _ = Answer(text, tile);
                _choiceTiles.Add(tile);
            }
        }

        private void Select(int blank)
        {
            if (blank < 0 || blank >= _blankItems.Count || _filled.Contains(blank)) return;
            Selected = blank;
            ShowPage(PageOfBlank(blank));
            foreach (var pair in _blankTiles) pair.Value.SetHighlighted(pair.Key == blank);
            if (!HasBank) BuildChoices(_blankItems[blank].choices);
        }

        private async Awaitable Answer(string choice, Tile chosen)
        {
            if (_busy || IsCompleted || Selected < 0) return;
            _busy = true;
            var blank = Selected;
            var item = _blankItems[blank];
            if (!_feedback.TryGetValue(blank, out var feedback)) _feedback[blank] = feedback = new RoundFeedback(Ctx, blank);
            var ok = await feedback.Handle(choice == item.answer, ChoiceTile(item.answer), chosen);
            if (!IsAlive) return;
            if (!ok)
            {
                _busy = false;
                return;
            }
            _filled.Add(blank);
            foreach (var t in _choiceTiles) t.SetHint(false);
            if (HasBank) chosen.gameObject.SetActive(false);
            if (_blankTiles.TryGetValue(blank, out var tile))
            {
                tile.SetText(item.answer);
                tile.SetHighlighted(false);
            }
            var next = -1;
            for (var i = 0; i < _blankItems.Count && next < 0; i++)
                if (!_filled.Contains(i)) next = i;
            Selected = next;
            // Âm thanh câu có thể bị cắt ngang ("Nghe lại", chạm chữ): điền đúng rồi thì vẫn sang ô sau.
            await Ctx.Speech.PlayAsync(RowAudio(item.row));
            if (!IsAlive) return;
            _busy = false;
            if (next >= 0)
            {
                Select(next);
                if (_auto) AnswerCorrectly();
                return;
            }
            await Ctx.Speech.PlayAsync(SystemAudio.khen_01);
            if (IsAlive) Complete();
        }

        private void AnswerCorrectly()
        {
            if (Selected < 0) return;
            var answer = _blankItems[Selected].answer;
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
