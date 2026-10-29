using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>Bảng ôn vần và từ ứng dụng. Chạm đủ các hàng trên mọi trang thì báo xong.</summary>
    public class RimeTableView : StepViewBase
    {
        private int PerPage => _rimes.Count > 12 ? 8 : 12;
        private const int RowsPerColumn = 4;
        private const float RimeW = 160f;
        private const float WordW = 262f;
        private const float CardH = 160f;
        private const float TileGap = 8f;
        private const float ColumnGap = 35f;
        private const float RowGap = 12f;
        private const float UnitW = RimeW + TileGap + WordW;

        private readonly List<Item> _rimes = new();
        private readonly List<Item> _words = new();
        private readonly List<Tile> _tiles = new();
        private TapProgress _progress;
        private Button _prev;
        private Button _next;
        private int _generation;

        internal int PageCount => Mathf.Max(1, (_rimes.Count + PerPage - 1) / PerPage);
        internal int Page { get; private set; }

        protected override void Build()
        {
            foreach (var rime in Step.items.Where(i => i.role == "rime").OrderBy(i => i.row))
            {
                _rimes.Add(rime);
                _words.Add(Step.items.First(i => i.role == "word" && i.row == rime.row));
            }
            _progress = new TapProgress(_rimes.Count);
            var shift = PageCount > 1 ? -120f : 0f;
            for (var j = 0; j < _rimes.Count; j++)
            {
                var index = j;
                var slot = j % PerPage;
                var count = Mathf.Min(PerPage, _rimes.Count - j / PerPage * PerPage);
                var columns = Mathf.CeilToInt(count / (float)RowsPerColumn);
                var rows = Mathf.Min(RowsPerColumn, count);
                var x = shift + (slot / RowsPerColumn - (columns - 1) / 2f) * (UnitW + ColumnGap);
                var y = ((rows - 1) / 2f - slot % RowsPerColumn) * (CardH + RowGap);
                var rime = _rimes[j];
                var parts = rime.spells.FirstOrDefault()?.parts;
                var text = rime.text;
                if (parts != null && parts.Count >= 2)
                    text += $"\n<size=55%>{parts[0].text} – {parts[1].text}</size>";
                var rimeTile = AddTile(text, new Vector2(RimeW, CardH),
                    new Vector2(x - UnitW / 2f + RimeW / 2f, y), 76f);
                var wordTile = AddTile(TextStyler.Apply(_words[j].text, _words[j].hl),
                    new Vector2(WordW, CardH), new Vector2(x + UnitW / 2f - WordW / 2f, y), 64f);
                rimeTile.Tapped += () => OnTapped(index);
                wordTile.Tapped += () => OnTapped(index);
                _tiles.Add(rimeTile);
                _tiles.Add(wordTile);
            }
            if (PageCount > 1)
            {
                _prev = AddPageButton(UiText.PagePrev, 92f, () => ShowPage(Page - 1));
                _next = AddPageButton(UiText.PageNext, -92f, () => ShowPage(Page + 1));
            }
            ShowPage(0);
        }

        private Button AddPageButton(string text, float y, System.Action action)
        {
            var button = UiKit.CreateButton(Root.transform, text, action);
            var rt = (RectTransform)button.transform;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = new Vector2(220f, UiKit.MinTouch);
            rt.anchoredPosition = new Vector2(590f, y);
            return button;
        }

        private void ShowPage(int page)
        {
            Page = Mathf.Clamp(page, 0, PageCount - 1);
            for (var j = 0; j < _tiles.Count; j++) _tiles[j].gameObject.SetActive(j / 2 / PerPage == Page);
            if (_prev != null) _prev.gameObject.SetActive(Page > 0);
            if (_next != null) _next.gameObject.SetActive(Page < PageCount - 1);
        }

        private async void OnTapped(int index)
        {
            var gen = ++_generation;
            _progress.Tap(index);
            foreach (var tile in _tiles) tile.SetHighlighted(false);
            _tiles[index * 2].SetHighlighted(true);
            _tiles[index * 2 + 1].SetHighlighted(true);
            var parts = _rimes[index].spells.FirstOrDefault()?.parts;
            var audios = parts != null ? parts.Select(p => p.audio).ToList() : new List<string>();
            audios.Add(_words[index].audio);
            var finished = await Ctx.Speech.PlaySequenceAsync(audios);
            if (!IsAlive || gen != _generation) return;
            _tiles[index * 2].SetHighlighted(false);
            _tiles[index * 2 + 1].SetHighlighted(false);
            if (finished && _progress.AllTapped) Complete();
        }

        /// <summary>Đọc lần lượt các vần trên trang đang mở.</summary>
        public override void Replay() => _ = Ctx.Speech.PlaySequenceAsync(
            _rimes.Skip(Page * PerPage).Take(PerPage).Select(i => i.audio).ToList());

        protected override void ActForTest()
        {
            for (var j = 0; j < _rimes.Count; j++)
            {
                ShowPage(j / PerPage);
                _tiles[j * 2].SimulateTap();
            }
        }
    }
}
