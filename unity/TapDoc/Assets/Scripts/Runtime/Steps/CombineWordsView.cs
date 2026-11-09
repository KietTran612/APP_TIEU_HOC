using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Ghép chữ rồi đọc lên (lớp 2, thiết kế TV2 tập một mục 6): "Ghép chữ dúm với các chữ: lông, muối". Thẻ chữ gốc ở
    /// trên, hàng thẻ chữ ghép ở giữa. Bé chạm thẻ chữ ghép thì cụm từ ("dúm lông") hiện ở hàng dưới và app đọc. Ghép đủ
    /// mọi chữ thì khen và đi tiếp. Chạm chữ gốc hay cụm đã ghép thì nghe lại.
    /// </summary>
    public class CombineWordsView : StepViewBase
    {
        private const float PartH = 150f;
        private const float ResultH = 140f;
        private const float Gap = 30f;

        private readonly List<Tile> _parts = new();
        private readonly Dictionary<int, Tile> _results = new();
        private List<Vector2> _resultCenters;
        private List<float> _resultWidths;
        private bool _auto;

        /// <summary>Số cụm đã ghép.</summary>
        internal int Revealed => _results.Count;

        private static float WidthOf(string text, float perChar, float min) => Mathf.Max(min, perChar * text.Length + 70f);

        protected override void Build()
        {
            AddMarker();
            var baseTile = AddTile(Step.text, new Vector2(WidthOf(Step.text, 64f, 220f), 170f), new Vector2(0f, 230f), 96f);
            baseTile.Tapped += Replay;

            var partWidths = Step.items.Select(i => WidthOf(i.part ?? i.text, 52f, 180f)).ToList();
            var partCenters = FlowLayout.Place(partWidths, PartH, FlowWidth, Gap, 20f);
            for (var k = 0; k < Step.items.Count; k++)
            {
                var index = k;
                var tile = AddTile(Step.items[k].part ?? Step.items[k].text, new Vector2(partWidths[k], PartH),
                    partCenters[k] + new Vector2(0f, 40f), 80f);
                tile.Tapped += () => _ = Reveal(index);
                _parts.Add(tile);
            }

            _resultWidths = Step.items.Select(i => WidthOf(i.text, 40f, 220f)).ToList();
            _resultCenters = FlowLayout.Place(_resultWidths, ResultH, FlowWidth, Gap, 18f);
            Replay();
        }

        private async Awaitable Reveal(int index)
        {
            var item = Step.items[index];
            if (!_results.TryGetValue(index, out var result))
            {
                result = AddTile(item.text, new Vector2(_resultWidths[index], ResultH),
                    _resultCenters[index] + new Vector2(0f, -190f), 64f);
                result.Tapped += () => _ = Ctx.Speech.PlayAsync(item.audio);
                _results[index] = result;
                _parts[index].SetHighlighted(true);
                Ctx.Fx?.Correct((RectTransform)result.transform);
            }
            // Âm thanh có thể bị cắt ngang (bé chạm thẻ khác): ghép đủ thì vẫn xong bước.
            await Ctx.Speech.PlayAsync(item.audio);
            if (!IsAlive || IsCompleted) return;
            if (_results.Count < Step.items.Count)
            {
                if (_auto) _ = Reveal(Enumerable.Range(0, Step.items.Count).First(i => !_results.ContainsKey(i)));
                return;
            }
            await Ctx.Speech.PlayAsync(SystemAudio.khen_01);
            if (IsAlive) Complete();
        }

        public override void Replay() => _ = Ctx.Speech.PlayAsync(Step.audio);

        protected override void ActForTest()
        {
            _auto = true;
            _ = Reveal(0);
        }
    }
}
