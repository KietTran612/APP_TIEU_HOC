using System.Collections.Generic;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Điền vào chỗ trống ở trang Tập chép – Chính tả (thiết kế tập 2, mục 7.4), từng mục một. Mục chữ: "chạy …on ton"
    /// với hai thẻ "l", "n". Mục dấu: chữ in nghiêng hiện không dấu, các thẻ là tên dấu. Bé kéo (hoặc chạm) thẻ vào
    /// chỗ trống: đúng thì chữ hiện đủ và app đọc cả từ; sai thì thẻ lắc nhẹ, cho làm lại, sai hai lần thì thẻ đúng
    /// được tô gợi ý. Làm hết các mục thì đi tiếp.
    /// </summary>
    public class FillBlankView : StepViewBase
    {
        private const float PartH = 200f;
        private const float ChoiceSize = 180f;

        private readonly List<Item> _items = new();
        private readonly List<GameObject> _row = new();
        private readonly List<Tile> _choices = new();
        private DropSlot _slot;
        private Tile _gap;
        private TMPro.TextMeshProUGUI _progress;
        private RoundFeedback _feedback;
        private bool _busy;
        private bool _auto;

        internal int Current { get; private set; }
        /// <summary>Mục dấu: các thẻ là tên dấu; chỗ trống hiện chữ không dấu.</summary>
        internal bool IsToneMode => TonesOnly();

        protected override void Build()
        {
            AddMarker();
            foreach (var item in Step.items)
                if (item.role == "blank") _items.Add(item);
            _progress = UiKit.CreateLabel(Root.transform, string.Empty, 40f);
            var prt = _progress.rectTransform;
            prt.anchorMin = prt.anchorMax = new Vector2(0.5f, 0.5f);
            prt.sizeDelta = new Vector2(300f, 60f);
            prt.anchoredPosition = new Vector2(0f, 290f);
            for (var k = 0; k < Step.labels.Count; k++)
            {
                var choice = Step.labels[k];
                var x = (k - (Step.labels.Count - 1) / 2f) * (ChoiceSize + 60f);
                var tile = AddTile(choice, new Vector2(ChoiceSize, ChoiceSize), new Vector2(x, -200f), 96f);
                var drag = tile.gameObject.AddComponent<DragTile>();
                drag.DroppedOn += slot => { if (slot == _slot) _ = Answer(choice, tile); };
                tile.Tapped += () => _ = Answer(choice, tile);
                _choices.Add(tile);
            }
            ShowItem(0);
            _ = Ctx.Speech.PlayAsync(SystemAudio.hd_keo_vao_cho_trong);
        }

        private bool TonesOnly()
        {
            foreach (var label in Step.labels)
                if (label != "huyền" && label != "sắc" && label != "hỏi" && label != "ngã" && label != "nặng") return false;
            return true;
        }

        /// <summary>Dựng mục thứ <paramref name="index"/>: [phần trước] [chỗ trống] [phần sau].</summary>
        private void ShowItem(int index)
        {
            Current = index;
            foreach (var go in _row) Object.Destroy(go);
            _row.Clear();
            _feedback = new RoundFeedback(Ctx, index);
            foreach (var c in _choices) c.SetHint(false);
            var item = _items[index];
            var span = item.hl != null && item.hl.Count > 0 ? item.hl[0] : new Span { s = 0, n = item.text.Length };
            var before = item.text.Substring(0, span.s).TrimEnd();
            var blank = item.text.Substring(span.s, span.n);
            var after = item.text.Substring(span.s + span.n).TrimStart();
            var gapText = IsToneMode ? VietText.StripTone(blank) : "?";
            var startsWord = span.s == 0 || item.text[span.s - 1] == ' ';
            var endsWord = span.s + span.n >= item.text.Length || item.text[span.s + span.n] == ' ';
            // Chữ dính liền chỗ trống (ví dụ "t" và "a" của "toa") đặt sát hơn để vẫn đọc ra một tiếng.
            var parts = new List<(string text, bool gap, float gapBefore)>();
            if (before.Length > 0) parts.Add((before, false, 0f));
            parts.Add((gapText, true, before.Length > 0 ? (startsWord ? 30f : 6f) : 0f));
            if (after.Length > 0) parts.Add((after, false, endsWord ? 30f : 6f));
            var widths = new List<float>();
            var total = 0f;
            foreach (var p in parts)
            {
                var w = Mathf.Max(UiKit.MinTouch, 64f * p.text.Length + 50f);
                widths.Add(w);
                total += w + p.gapBefore;
            }
            var x = -total / 2f;
            for (var k = 0; k < parts.Count; k++)
            {
                x += parts[k].gapBefore;
                var tile = AddTile(parts[k].text, new Vector2(widths[k], PartH), new Vector2(x + widths[k] / 2f, 90f), 110f);
                x += widths[k];
                _row.Add(tile.gameObject);
                if (!parts[k].gap) continue;
                _gap = tile;
                _slot = tile.gameObject.AddComponent<DropSlot>();
            }
            _progress.text = $"{index + 1}/{_items.Count}";
        }

        private async Awaitable Answer(string choice, Tile chosen)
        {
            if (_busy || IsCompleted) return;
            _busy = true;
            var item = _items[Current];
            var correctTile = _choices.Find(t => t.PlainText == item.answer);
            var ok = await _feedback.Handle(choice == item.answer, correctTile, chosen);
            if (!IsAlive) return;
            if (!ok)
            {
                _busy = false;
                return;
            }
            foreach (var go in _row) Object.Destroy(go);
            _row.Clear();
            var full = AddTile(item.text, new Vector2(Mathf.Max(UiKit.MinTouch, 64f * item.text.Length + 60f), PartH),
                new Vector2(0f, 90f), 110f);
            _row.Add(full.gameObject);
            // Âm thanh từ có thể bị cắt ngang ("Nghe lại"): điền đúng rồi thì vẫn sang mục sau.
            await Ctx.Speech.PlayAsync(item.audio);
            if (!IsAlive) return;
            _busy = false;
            if (Current + 1 < _items.Count)
            {
                ShowItem(Current + 1);
                if (_auto) AnswerCorrectly();
            }
            else Complete();
        }

        private void AnswerCorrectly()
        {
            var answer = _items[Current].answer;
            _ = Answer(answer, _choices.Find(t => t.PlainText == answer));
        }

        public override void Replay()
        {
            if (Current < _items.Count) _ = Ctx.Speech.PlayAsync(SystemAudio.hd_keo_vao_cho_trong);
        }

        protected override void ActForTest()
        {
            _auto = true;
            AnswerCorrectly();
        }
    }
}
