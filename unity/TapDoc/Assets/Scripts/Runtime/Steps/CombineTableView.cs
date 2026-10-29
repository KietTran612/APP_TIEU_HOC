using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Bảng ghép của bài ôn tập: cột âm đầu bên trái, các nguyên âm bên phải (như bảng trong sách). Bé chọn một âm
    /// đầu rồi một nguyên âm: app làm mẫu đánh vần tiếng ghép được và hiện tiếng đó cùng các tiếng có dấu của ô
    /// (chạm để nghe đánh vần). Mỗi âm đầu được ghép ít nhất một lần thì báo xong.
    /// </summary>
    public class CombineTableView : StepViewBase
    {
        private const float OnsetSize = 160f;
        private const float OnsetGap = 12f;
        private const float VowelSize = 160f;
        private const float VowelGap = 16f;
        private const float ResultW = 200f;
        private const float ResultH = 170f;
        private const float RightX = 140f;
        private const float RightWidth = 1100f;
        private const float ResultY = -235f;

        private readonly Dictionary<int, Tile> _onsets = new();   // theo row
        private readonly Dictionary<int, Tile> _vowels = new();   // theo col
        private readonly List<GameObject> _results = new();
        private TapProgress _progress;
        private int _onsetRow = -1;
        private int _generation;

        private IEnumerable<Item> ByRole(string role) => Step.items.Where(i => i.role == role);

        protected override void Build()
        {
            AddMarker();
            PlaceMarkerBesideVowels();
            var onsets = ByRole("onset").OrderBy(i => i.row).ToList();
            _progress = new TapProgress(onsets.Count);

            var columnHeight = onsets.Count * OnsetSize + (onsets.Count - 1) * OnsetGap;
            for (var k = 0; k < onsets.Count; k++)
            {
                var item = onsets[k];
                var y = columnHeight / 2f - OnsetSize / 2f - k * (OnsetSize + OnsetGap);
                var tile = AddTile(item.text, new Vector2(OnsetSize, OnsetSize), new Vector2(-610f, y), 110f);
                var row = item.row;
                tile.Tapped += () => OnOnsetTapped(row);
                _onsets[row] = tile;
            }

            var vowels = ByRole("vowel").OrderBy(i => i.col).ToList();
            var centers = FlowLayout.Place(vowels.Select(_ => VowelSize).ToList(), VowelSize, RightWidth, VowelGap, VowelGap);
            var vowelBlockTop = 330f;
            var vowelBlockHeight = centers.Count == 0 ? 0f : centers.Max(c => c.y) - centers.Min(c => c.y) + VowelSize;
            var vowelOffset = new Vector2(RightX, vowelBlockTop - vowelBlockHeight / 2f);
            for (var k = 0; k < vowels.Count; k++)
            {
                var item = vowels[k];
                var tile = AddTile(item.text, new Vector2(VowelSize, VowelSize), centers[k] + vowelOffset, 110f);
                var col = item.col;
                tile.Tapped += () => OnVowelTapped(col);
                _vowels[col] = tile;
            }
        }

        private void OnOnsetTapped(int row)
        {
            _onsetRow = row;
            foreach (var pair in _onsets) pair.Value.SetHighlighted(pair.Key == row);
            _ = Ctx.Speech.PlayAsync(ByRole("onset").First(i => i.row == row).audio);
        }

        private async void OnVowelTapped(int col)
        {
            if (_onsetRow < 0)
            {
                // Chưa chọn âm đầu: gợi ý chọn âm đầu trước, chỉ đọc nguyên âm.
                foreach (var t in _onsets.Values) t.SetHint(true);
                _ = Ctx.Speech.PlayAsync(ByRole("vowel").First(i => i.col == col).audio);
                return;
            }
            foreach (var t in _onsets.Values) t.SetHint(false);
            var row = _onsetRow;
            var baseItem = ByRole("base").FirstOrDefault(i => i.row == row && i.col == col);
            if (baseItem == null) return;

            foreach (var pair in _vowels) pair.Value.SetHighlighted(pair.Key == col);
            var gen = ++_generation;
            ShowResults(baseItem, ByRole("form").Where(i => i.row == row && i.col == col).ToList());
            _progress.Tap(_onsets.Keys.OrderBy(k => k).ToList().IndexOf(row));

            await Ctx.Speech.PlaySequenceAsync(SpellIds(baseItem));
            // Lần ghép mới hơn đã thay lần này: lần mới sẽ báo xong.
            if (!IsAlive || gen != _generation) return;
            if (_progress.AllTapped) Complete();
        }

        /// <summary>
        /// Kí hiệu ● đặt ở khe giữa cột âm đầu và khối nguyên âm (góc trên trái của Stage đã có cột âm đầu).
        /// </summary>
        private void PlaceMarkerBesideVowels()
        {
            var marker = Root.transform.Find("Marker") as RectTransform;
            if (marker == null) return;
            marker.anchorMin = marker.anchorMax = marker.pivot = new Vector2(0.5f, 0.5f);
            marker.anchoredPosition = new Vector2(RightX - RightWidth / 2f - 60f, 290f);
        }

        private void ShowResults(Item baseItem, List<Item> forms)
        {
            foreach (var go in _results) Object.Destroy(go);
            _results.Clear();
            var all = new List<Item> { baseItem };
            all.AddRange(forms);
            var centers = FlowLayout.Place(all.Select(_ => ResultW).ToList(), ResultH, RightWidth, 20f, 16f);
            for (var k = 0; k < all.Count; k++)
            {
                var item = all[k];
                var tile = AddTile(item.text, new Vector2(ResultW, ResultH), centers[k] + new Vector2(RightX, ResultY), 100f);
                if (k == 0) tile.SetHighlighted(true);
                tile.Tapped += () => _ = Ctx.Speech.PlaySequenceAsync(SpellIds(item));
                _results.Add(tile.gameObject);
            }
        }

        private static List<string> SpellIds(Item item)
        {
            var ids = item.spells.SelectMany(s => s.parts).Select(p => p.audio).ToList();
            if (ids.Count == 0) ids.Add(item.audio);
            return ids;
        }

        public override void Replay()
        {
            var ids = ByRole("onset").OrderBy(i => i.row).Select(i => i.audio)
                .Concat(ByRole("vowel").OrderBy(i => i.col).Select(i => i.audio)).ToList();
            _ = Ctx.Speech.PlaySequenceAsync(ids);
        }

        protected override void ActForTest()
        {
            foreach (var row in _onsets.Keys.OrderBy(k => k).ToList())
            {
                var baseItem = ByRole("base").First(i => i.row == row);
                OnOnsetTapped(row);
                OnVowelTapped(baseItem.col);
            }
        }
    }
}
