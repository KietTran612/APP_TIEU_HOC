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
        private const float ResultY = -235f;

        // Một cột âm đầu chứa tối đa 4 thẻ 160 trong chiều cao Stage (680). Bảng 5 âm đầu (bài 22, 27, 37) xếp âm đầu
        // thành 2 cột và dời khối nguyên âm sang phải cho khỏi chồng lên nhau.
        private const int MaxOnsetsPerColumn = 4;
        private const float OnsetX = -610f;
        private const float OnsetX2A = -620f;
        private const float OnsetX2B = -450f;

        private float _rightX = 140f;
        private float _rightWidth = 1100f;

        private readonly Dictionary<int, Tile> _onsets = new();   // theo row
        private readonly Dictionary<int, Tile> _vowels = new();   // theo col
        private readonly Dictionary<int, GameObject> _blocked = new(); // dấu gạch chéo theo col
        private readonly List<GameObject> _results = new();
        private TapProgress _progress;
        private int _onsetRow = -1;
        private int _generation;

        private IEnumerable<Item> ByRole(string role) => Step.items.Where(i => i.role == role);

        protected override void Build()
        {
            var onsets = ByRole("onset").OrderBy(i => i.row).ToList();
            _progress = new TapProgress(onsets.Count);
            var twoColumns = onsets.Count > MaxOnsetsPerColumn;
            if (twoColumns)
            {
                _rightX = 170f;
                _rightWidth = 1040f;
            }

            AddMarker();
            // Hai cột âm đầu đã chiếm khe bên trái khối nguyên âm: kí hiệu ● giữ ở góc trên trái Stage.
            if (!twoColumns) PlaceMarkerBesideVowels();

            var perColumn = twoColumns ? (onsets.Count + 1) / 2 : onsets.Count;
            var columnHeight = perColumn * OnsetSize + (perColumn - 1) * OnsetGap;
            for (var k = 0; k < onsets.Count; k++)
            {
                var item = onsets[k];
                var x = twoColumns ? (k < perColumn ? OnsetX2A : OnsetX2B) : OnsetX;
                // Hai cột: hạ xuống một chút để thẻ đầu không chạm kí hiệu ● ở góc trên trái.
                var y = columnHeight / 2f - OnsetSize / 2f - k % perColumn * (OnsetSize + OnsetGap) - (twoColumns ? 12f : 0f);
                var tile = AddTile(item.text, new Vector2(OnsetSize, OnsetSize), new Vector2(x, y), 110f);
                var row = item.row;
                tile.Tapped += () => OnOnsetTapped(row);
                _onsets[row] = tile;
            }

            var vowels = ByRole("vowel").OrderBy(i => i.col).ToList();
            var centers = FlowLayout.Place(vowels.Select(_ => VowelSize).ToList(), VowelSize, _rightWidth, VowelGap, VowelGap);
            var vowelBlockTop = 330f;
            var vowelBlockHeight = centers.Count == 0 ? 0f : centers.Max(c => c.y) - centers.Min(c => c.y) + VowelSize;
            var vowelOffset = new Vector2(_rightX, vowelBlockTop - vowelBlockHeight / 2f);
            for (var k = 0; k < vowels.Count; k++)
            {
                var item = vowels[k];
                var tile = AddTile(item.text, new Vector2(VowelSize, VowelSize), centers[k] + vowelOffset, 110f);
                var col = item.col;
                tile.Tapped += () => OnVowelTapped(col);
                _vowels[col] = tile;
                _blocked[col] = AddBlockedOverlay(tile);
            }
        }

        private bool IsBlocked(int row, int col) => ByRole("blocked").Any(i => i.row == row && i.col == col);

        /// <summary>Hai nét chéo chỉ để nhìn, không chặn thao tác chạm vào thẻ.</summary>
        private static GameObject AddBlockedOverlay(Tile tile)
        {
            var go = new GameObject("Blocked", typeof(RectTransform));
            var rt = (RectTransform)go.transform;
            rt.SetParent(tile.transform, false);
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = rt.offsetMax = Vector2.zero;
            foreach (var angle in new[] { -45f, 45f })
            {
                var bar = new GameObject("Bar", typeof(RectTransform), typeof(UnityEngine.UI.Image));
                var brt = (RectTransform)bar.transform;
                brt.SetParent(rt, false);
                brt.anchorMin = brt.anchorMax = new Vector2(0.5f, 0.5f);
                brt.sizeDelta = new Vector2(180f, 6f);
                brt.localRotation = Quaternion.Euler(0f, 0f, angle);
                var image = bar.GetComponent<UnityEngine.UI.Image>();
                image.sprite = UiKit.WhiteSprite;
                image.color = new Color(0.15f, 0.14f, 0.12f, 1f);
                image.raycastTarget = false;
            }
            go.SetActive(false);
            return go;
        }

        private void OnOnsetTapped(int row)
        {
            _onsetRow = row;
            foreach (var pair in _blocked) pair.Value.SetActive(IsBlocked(row, pair.Key));
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
            if (IsBlocked(_onsetRow, col)) return;
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
            marker.anchoredPosition = new Vector2(_rightX - _rightWidth / 2f - 60f, 290f);
        }

        private void ShowResults(Item baseItem, List<Item> forms)
        {
            foreach (var go in _results) Object.Destroy(go);
            _results.Clear();
            var all = new List<Item> { baseItem };
            all.AddRange(forms);
            var centers = FlowLayout.Place(all.Select(_ => ResultW).ToList(), ResultH, _rightWidth, 20f, 16f);
            for (var k = 0; k < all.Count; k++)
            {
                var item = all[k];
                var tile = AddTile(item.text, new Vector2(ResultW, ResultH), centers[k] + new Vector2(_rightX, ResultY), 100f);
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
