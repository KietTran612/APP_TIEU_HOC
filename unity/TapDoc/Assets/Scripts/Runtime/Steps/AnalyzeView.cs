using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Phân tích từ trên xuống (từ khóa → tiếng → âm/vần): các dòng xếp dọc, căn phải như trong sách.
    /// Không tự đọc; bé chạm đủ mọi dòng thì báo xong.
    /// </summary>
    public class AnalyzeView : StepViewBase
    {
        private const float RowWidth = 520f;
        private const float RowHeight = 170f;
        private const float RowGap = 18f;

        private readonly List<Tile> _rows = new();
        private TapProgress _progress;

        protected override void Build()
        {
            var rows = Step.rows;
            _progress = new TapProgress(rows.Count);
            var top = (rows.Count - 1) * (RowHeight + RowGap) / 2f;
            for (var i = 0; i < rows.Count; i++)
            {
                var index = i;
                var offset = new Vector2(200f, top - i * (RowHeight + RowGap));
                var tile = AddTile(TextStyler.Apply(rows[i].text, rows[i].hl), new Vector2(RowWidth, RowHeight), offset, 96f);
                tile.Tapped += () => OnRowTapped(index);
                _rows.Add(tile);
            }
        }

        private async void OnRowTapped(int index)
        {
            // Đánh dấu ngay khi chạm: bé chạm nhanh dòng sau thì âm dòng trước bị cắt, nhưng dòng đó vẫn tính.
            _progress.Tap(index);
            if (await Play(Step.rows[index].audio) && _progress.AllTapped) Complete();
        }

        public override void Replay() =>
            _ = Ctx.Speech.PlaySequenceAsync(Step.rows.Select(r => r.audio).ToList());

        protected override void ActForTest()
        {
            foreach (var row in _rows) row.SimulateTap();
        }
    }
}
