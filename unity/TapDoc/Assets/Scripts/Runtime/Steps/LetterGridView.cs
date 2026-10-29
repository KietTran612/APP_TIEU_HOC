using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Khung chữ đầu bài ôn tập: hàng chữ cái, bên dưới là hàng dấu thanh (nếu có), như khung trong sách.
    /// Chạm thẻ nào thì nghe thẻ đó; bé chạm đủ mọi thẻ thì báo xong.
    /// </summary>
    public class LetterGridView : StepViewBase
    {
        private const float TileSize = 170f;
        private const float Gap = 22f;
        private const float RowGap = 50f;

        private readonly Dictionary<int, Tile> _tiles = new();
        private TapProgress _progress;

        protected override void Build()
        {
            var items = Step.items;
            _progress = new TapProgress(items.Count);
            var rows = items.Select((it, j) => (it, j)).GroupBy(p => p.it.row).OrderBy(g => g.Key).ToList();
            var top = (rows.Count - 1) * (TileSize + RowGap) / 2f;
            for (var r = 0; r < rows.Count; r++)
            {
                var row = rows[r].ToList();
                var centers = FlowLayout.Place(row.Select(_ => TileSize).ToList(), TileSize, FlowWidth, Gap, Gap);
                for (var k = 0; k < row.Count; k++)
                {
                    var (item, index) = row[k];
                    var tile = AddTile(item.text, new Vector2(TileSize, TileSize), centers[k] + new Vector2(0f, top - r * (TileSize + RowGap)), 120f);
                    if (item.role == "tone") tile.SetTone(item.tone);
                    tile.Tapped += () => OnTapped(index);
                    _tiles[index] = tile;
                }
            }
        }

        private async void OnTapped(int index)
        {
            _progress.Tap(index);
            foreach (var t in _tiles.Values) t.SetHighlighted(false);
            _tiles[index].SetHighlighted(true);
            var finished = await Play(Step.items[index].audio);
            if (!IsAlive) return;
            _tiles[index].SetHighlighted(false);
            if (finished && _progress.AllTapped) Complete();
        }

        /// <summary>Đọc lần lượt cả khung.</summary>
        public override void Replay() => _ = Ctx.Speech.PlaySequenceAsync(Step.items.Select(i => i.audio).ToList());

        protected override void ActForTest()
        {
            for (var j = 0; j < Step.items.Count; j++) OnTapped(j);
        }
    }
}
