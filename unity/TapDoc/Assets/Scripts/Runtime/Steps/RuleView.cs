using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace TapDoc
{
    /// <summary>Quy tắc ghép chữ: chạm từng dòng để nghe, đọc đủ mọi dòng thì báo xong.</summary>
    public class RuleView : StepViewBase
    {
        private readonly List<Tile> _tiles = new();
        private TapProgress _progress;
        private int _generation;

        protected override void Build()
        {
            AddMarker();
            _progress = new TapProgress(Step.items.Count);
            var top = (Step.items.Count - 1) * 184f / 2f;
            for (var j = 0; j < Step.items.Count; j++)
            {
                var index = j;
                var tile = AddTile(Step.items[j].text, new Vector2(1200f, 160f), new Vector2(0f, top - j * 184f), 64f);
                tile.Tapped += () => OnTapped(index);
                _tiles.Add(tile);
            }
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

        public override void Replay() => _ = Ctx.Speech.PlaySequenceAsync(Step.items.Select(i => i.audio).ToList());

        protected override void ActForTest()
        {
            foreach (var tile in _tiles) tile.SimulateTap();
        }
    }
}
