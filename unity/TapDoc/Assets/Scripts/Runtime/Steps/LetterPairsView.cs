using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace TapDoc
{
    /// <summary>Cặp chữ thường và chữ hoa, bốn cột như sách. Chạm đủ mọi trang thì báo xong.</summary>
    public class LetterPairsView : StepViewBase
    {
        private const int PerPage = 16;
        private const float CardW = 280f;
        private const float CardH = 160f;
        private const float Gap = 8f;

        private readonly List<Tile> _tiles = new();
        private TapProgress _progress;
        private PageButtons _pager;
        private int _generation;

        internal int PageCount => Mathf.Max(1, (Step.items.Count + PerPage - 1) / PerPage);
        internal int Page { get; private set; }

        protected override void Build()
        {
            _progress = new TapProgress(Step.items.Count);
            var shift = PageCount > 1 ? -120f : 0f;
            for (var j = 0; j < Step.items.Count; j++)
            {
                var index = j;
                var item = Step.items[j];
                var slot = j % PerPage;
                var rows = Mathf.CeilToInt(Mathf.Min(PerPage, Step.items.Count - j / PerPage * PerPage) / 4f);
                var pos = new Vector2(shift + (slot % 4 - 1.5f) * (CardW + Gap),
                    ((rows - 1) / 2f - slot / 4) * (CardH + Gap));
                var tile = AddTile(item.text + "   " + item.upper, new Vector2(CardW, CardH), pos, 96f);
                tile.Tapped += () => OnTapped(index);
                _tiles.Add(tile);
            }
            if (PageCount > 1) _pager = new PageButtons(Root.transform, () => ShowPage(Page - 1), () => ShowPage(Page + 1));
            ShowPage(0);
        }

        private void ShowPage(int page)
        {
            Page = Mathf.Clamp(page, 0, PageCount - 1);
            for (var j = 0; j < _tiles.Count; j++) _tiles[j].gameObject.SetActive(j / PerPage == Page);
            _pager?.Show(Page, PageCount);
        }

        private async void OnTapped(int index)
        {
            var gen = ++_generation;
            _progress.Tap(index);
            foreach (var tile in _tiles) tile.SetHighlighted(false);
            _tiles[index].SetHighlighted(true);
            var finished = await Play(Step.items[index].audio);
            if (!IsAlive || gen != _generation) return;
            _tiles[index].SetHighlighted(false);
            if (finished && _progress.AllTapped) Complete();
        }

        /// <summary>Đọc lần lượt các cặp trên trang đang mở.</summary>
        public override void Replay() => _ = Ctx.Speech.PlaySequenceAsync(
            Step.items.Skip(Page * PerPage).Take(PerPage).Select(i => i.audio).ToList());

        protected override void ActForTest()
        {
            for (var j = 0; j < _tiles.Count; j++)
            {
                ShowPage(j / PerPage);
                _tiles[j].SimulateTap();
            }
        }
    }
}
