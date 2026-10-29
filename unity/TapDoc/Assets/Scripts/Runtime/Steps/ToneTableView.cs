using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Bảng dấu (bài dấu thanh): tiếng gốc và 5 ô trống, trên mỗi ô có sẵn kí hiệu dấu như trong sách. Bé kéo thẻ dấu
    /// vào đúng ô: ô hiện tiếng có dấu và app làm mẫu "tiếng gốc – dấu – tiếng có dấu". Kéo nhầm ô thì thẻ trượt về,
    /// không phạt. Điền đủ các ô thì báo xong.
    /// </summary>
    public class ToneTableView : StepViewBase
    {
        private const float CellW = 190f;
        private const float CellH = 190f;
        private const float Gap = 20f;
        private const float RowY = 110f;

        private readonly Dictionary<int, Tile> _cells = new();
        private readonly Dictionary<int, DragTile> _drags = new();
        private readonly HashSet<int> _filled = new();

        protected override void Build()
        {
            var items = Step.items;
            var count = items.Count + 1;
            var left = -((count - 1) * (CellW + Gap)) / 2f;

            var baseTile = AddTile(Step.text, new Vector2(CellW, CellH), new Vector2(left, RowY), 110f);
            baseTile.SetHighlighted(true);
            baseTile.Tapped += () => _ = Ctx.Speech.PlayAsync(Step.audio);

            for (var j = 0; j < items.Count; j++)
            {
                var index = j;
                var x = left + (j + 1) * (CellW + Gap);
                var cell = AddTile(string.Empty, new Vector2(CellW, CellH), new Vector2(x, RowY), 110f);
                cell.Tone = items[j].tone;
                cell.gameObject.AddComponent<DropSlot>();
                cell.Tapped += () => OnCellTapped(index);
                _cells[j] = cell;

                // Kí hiệu dấu in sẵn phía trên ô, như trong sách.
                // Kí tự dấu vốn nhỏ và nằm cao trong dòng chữ: cỡ chữ lớn, không tự co, hạ hộp chữ xuống sát ô.
                var mark = UiKit.CreateLabel(Root.transform, items[j].glyph, 150f);
                mark.enableAutoSizing = false;
                mark.fontSize = 150f;
                mark.overflowMode = TMPro.TextOverflowModes.Overflow;
                var mrt = mark.rectTransform;
                mrt.anchorMin = mrt.anchorMax = new Vector2(0.5f, 0.5f);
                // Hộp cao vừa dòng chữ (không tính là tràn). Như sách: dấu nặng in dưới ô, các dấu khác in trên ô;
                // đặt theo tâm nét chữ thật vì nét dấu nằm lệch trong dòng.
                var line = mark.GetPreferredValues(items[j].glyph);
                mrt.sizeDelta = new Vector2(Mathf.Max(CellW, line.x), line.y + 2f);
                var target = items[j].tone == "nang"
                    ? new Vector2(x, RowY - CellH / 2f - 40f)
                    : new Vector2(x, RowY + CellH / 2f + 45f);
                mrt.anchoredPosition = target;
                if (Tile.InkBounds(mark, out var ink)) mrt.anchoredPosition = target - (Vector2)ink.center;
            }

            // Thẻ dấu để kéo, xếp theo thứ tự xáo (không trùng thứ tự các ô).
            var order = Shuffled(items.Count);
            const float dragSize = 170f;
            for (var k = 0; k < order.Count; k++)
            {
                var index = order[k];
                var x = -((order.Count - 1) * (dragSize + 40f)) / 2f + k * (dragSize + 40f);
                var tile = AddTile(items[index].glyph, new Vector2(dragSize, dragSize), new Vector2(x, -200f), 110f);
                tile.SetTone(items[index].tone);
                var drag = tile.gameObject.AddComponent<DragTile>();
                drag.DroppedOn += slot => OnDropped(index, slot);
                _drags[index] = drag;
            }

            _ = PlayIntro();
        }

        private async Awaitable PlayIntro()
        {
            if (!await Play(Step.audio)) return;
            await Play(SystemAudio.hd_keo_dau_vao_chu);
        }

        private static List<int> Shuffled(int n)
        {
            var order = Enumerable.Range(0, n).ToList();
            if (n < 2) return order;
            var rng = new System.Random();
            do
            {
                order = order.OrderBy(_ => rng.Next()).ToList();
            }
            while (order.Select((v, i) => v == i).All(x => x));
            return order;
        }

        private async void OnDropped(int index, DropSlot slot)
        {
            if (_filled.Contains(index) || slot == null) return;
            if (!_cells.TryGetValue(index, out var cell) || slot.gameObject != cell.gameObject) return; // nhầm ô: thẻ trượt về

            _filled.Add(index);
            var item = Step.items[index];
            cell.SetText(item.text);
            cell.SetHighlighted(true);
            _drags[index].gameObject.SetActive(false);

            await PlaySpell(item);
            if (IsAlive && _filled.Count == Step.items.Count) Complete();
        }

        private void OnCellTapped(int index)
        {
            if (_filled.Contains(index)) _ = PlaySpell(Step.items[index]);
        }

        private Awaitable<bool> PlaySpell(Item item)
        {
            var ids = item.spells.SelectMany(s => s.parts).Select(p => p.audio).ToList();
            if (ids.Count == 0) ids.Add(item.audio);
            return Ctx.Speech.PlaySequenceAsync(ids);
        }

        public override void Replay() => _ = PlayIntro();

        protected override void ActForTest()
        {
            foreach (var pair in _drags.ToList())
            {
                if (!_filled.Contains(pair.Key)) pair.Value.SimulateDropOn(_cells[pair.Key].GetComponent<DropSlot>());
            }
        }
    }
}
