using System.Collections.Generic;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Chọn dòng đúng yêu cầu (lớp 2, thiết kế TV2 tập một mục 6): "Trong những dòng sau, dòng nào viết chưa thành
    /// câu?". App đọc câu hỏi; mỗi dòng là một thẻ. Chạm thẻ thì app đọc dòng đó; dòng đúng sáng lên và được đếm, dòng
    /// khác chỉ được đọc, không chê. Hai lần chạm chưa đúng liền nhau thì một dòng đúng còn thiếu được tô vàng gợi ý.
    /// Tìm đủ thì khen và đi tiếp.
    /// </summary>
    public class ChooseLineView : StepViewBase
    {
        private const float Top = 170f;
        private const float Bottom = -250f;
        private const float LineGap = 14f;

        private readonly List<Tile> _lines = new();
        private readonly HashSet<int> _found = new();
        private TMPro.TextMeshProUGUI _count;
        private int _misses;
        private int _hint = -1;

        internal int FoundCount => _found.Count;
        internal int HintIndex => _hint;
        internal Tile LineTile(int index) => _lines[index];

        private int Need => Mathf.Max(1, Step.need);

        protected override void Build()
        {
            AddMarker();
            var question = UiKit.CreateLabel(Root.transform, Step.text, 46f);
            var qrt = question.rectTransform;
            qrt.anchorMin = qrt.anchorMax = new Vector2(0.5f, 0.5f);
            qrt.sizeDelta = new Vector2(FlowWidth - 120f, 120f);
            qrt.anchoredPosition = new Vector2(60f, 270f);
            question.alignment = TMPro.TextAlignmentOptions.Left;

            var n = Step.items.Count;
            var height = Mathf.Min(110f, (Top - Bottom - LineGap * (n - 1)) / Mathf.Max(1, n));
            for (var k = 0; k < n; k++)
            {
                var index = k;
                var y = Top - height / 2f - k * (height + LineGap);
                var tile = AddTile(Step.items[k].text, new Vector2(FlowWidth * 0.8f, height), new Vector2(0f, y),
                    Mathf.Min(56f, height * 0.55f));
                tile.Tapped += () => _ = OnLineTapped(index);
                _lines.Add(tile);
            }

            _count = UiKit.CreateLabel(Root.transform, string.Empty, 40f);
            var crt = _count.rectTransform;
            crt.anchorMin = crt.anchorMax = new Vector2(0.5f, 0.5f);
            crt.sizeDelta = new Vector2(400f, 56f);
            crt.anchoredPosition = new Vector2(0f, Bottom - 40f);
            UpdateCount();
            Replay();
        }

        private void UpdateCount() => _count.text = string.Format(UiText.FoundFormat, Mathf.Min(_found.Count, Need), Need);

        private async Awaitable OnLineTapped(int index)
        {
            var item = Step.items[index];
            if (item.role != "target")
            {
                _ = Ctx.Speech.PlayAsync(item.audio);
                if (++_misses >= 2) ShowHint();
                return;
            }
            _misses = 0;
            if (_found.Add(index))
            {
                _lines[index].SetHighlighted(true);
                if (_hint == index)
                {
                    _lines[index].SetHint(false);
                    _hint = -1;
                }
                UpdateCount();
                Ctx.Fx?.Correct((RectTransform)_lines[index].transform);
            }
            await Ctx.Speech.PlayAsync(item.audio);
            if (!IsAlive || IsCompleted || _found.Count < Need) return;
            await Ctx.Speech.PlayAsync(SystemAudio.khen_01);
            if (IsAlive) Complete();
        }

        /// <summary>Tô vàng dòng đúng đầu tiên chưa tìm.</summary>
        private void ShowHint()
        {
            for (var k = 0; k < Step.items.Count; k++)
            {
                if (Step.items[k].role != "target" || _found.Contains(k)) continue;
                if (_hint >= 0) _lines[_hint].SetHint(false);
                _hint = k;
                _lines[k].SetHint(true);
                return;
            }
        }

        public override void Replay() => _ = Ctx.Speech.PlayAsync(Step.audio);

        protected override void ActForTest()
        {
            for (var k = 0; k < Step.items.Count; k++)
                if (Step.items[k].role == "target") _lines[k].SimulateTap();
        }
    }
}
