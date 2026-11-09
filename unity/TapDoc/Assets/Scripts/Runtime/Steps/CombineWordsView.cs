using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Ghép chữ rồi đọc lên (lớp 2, thiết kế TV2 tập một mục 6): "Ghép chữ dúm với các chữ: lông, muối". Thẻ chữ gốc ở
    /// trên, các thẻ chữ ghép ở dưới. Bé chạm thẻ chữ ghép thì thẻ ấy hiện cả cụm ("dúm lông"), sáng lên và app đọc.
    /// Ghép đủ mọi chữ thì khen và đi tiếp. Chạm chữ gốc hay cụm đã ghép thì nghe lại. Thẻ cao bằng mức chạm tối thiểu.
    /// </summary>
    public class CombineWordsView : StepViewBase
    {
        private const float Gap = 30f;

        private readonly List<Tile> _parts = new();
        private readonly HashSet<int> _done = new();
        private bool _auto;

        /// <summary>Số cụm đã ghép.</summary>
        internal int Revealed => _done.Count;

        protected override void Build()
        {
            AddMarker();
            var baseTile = AddTile(Step.text, new Vector2(Mathf.Max(260f, 64f * Step.text.Length + 80f), UiKit.MinTouch + 10f),
                new Vector2(0f, 215f), 96f);
            baseTile.Tapped += Replay;

            // Thẻ đủ rộng cho cả cụm sau khi ghép, để chữ không phải co lại.
            var widths = Step.items.Select(i => Mathf.Clamp(44f * i.text.Length + 70f, 260f, FlowWidth)).ToList();
            var centers = FlowLayout.Place(widths, UiKit.MinTouch, FlowWidth, Gap, 24f);
            var shift = centers.Count > 0 ? -60f - centers.Max(c => c.y) + UiKit.MinTouch / 2f : 0f;
            for (var k = 0; k < Step.items.Count; k++)
            {
                var index = k;
                var tile = AddTile(Step.items[k].part ?? Step.items[k].text, new Vector2(widths[k], UiKit.MinTouch),
                    centers[k] + new Vector2(0f, shift), 72f);
                tile.Tapped += () => _ = Reveal(index);
                _parts.Add(tile);
            }
            Replay();
        }

        private async Awaitable Reveal(int index)
        {
            var item = Step.items[index];
            if (_done.Add(index))
            {
                _parts[index].SetText(item.text);
                _parts[index].SetHighlighted(true);
                Ctx.Fx?.Correct((RectTransform)_parts[index].transform);
            }
            // Âm thanh có thể bị cắt ngang (bé chạm thẻ khác): ghép đủ thì vẫn xong bước.
            await Ctx.Speech.PlayAsync(item.audio);
            if (!IsAlive || IsCompleted) return;
            if (_done.Count < Step.items.Count)
            {
                if (_auto) _ = Reveal(Enumerable.Range(0, Step.items.Count).First(i => !_done.Contains(i)));
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
