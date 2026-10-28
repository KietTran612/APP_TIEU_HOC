using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Nhìn tranh và khuôn chữ có chỗ trống "_" rồi kéo thẻ vào chỗ trống. Kéo đúng thì khuôn hiện đủ chữ và
    /// app đọc lại từ.
    /// </summary>
    public class ComposeView : RoundViewBase
    {
        private Tile _word;
        private Tile _gap;
        private Tile _after;
        private DropSlot _slot;

        protected override void Build()
        {
            var hasImage = !string.IsNullOrEmpty(Round.image);
            if (hasImage)
            {
                var sprite = Ctx.Assets.Image(Round.image);
                var pic = AddTile(string.Empty, new Vector2(300f, 300f), new Vector2(-470f, 110f), 68f, sprite);
                pic.SetSprite(sprite, Round.image);
            }

            // Khuôn đúng thứ tự đọc: [phần trước] [ô trống] [phần sau]. Ví dụ "l_ can" → "l" [?] "can".
            var template = Round.prompt_text ?? string.Empty;
            var cut = template.IndexOf('_');
            var before = (cut >= 0 ? template.Substring(0, cut) : template).Trim();
            var after = (cut >= 0 ? template.Substring(cut + 1) : string.Empty).Trim();
            const float gapW = 200f, partGap = 20f, h = 220f;
            var beforeW = Mathf.Max(UiKit.MinTouch, 70f * before.Length + 60f);
            var afterW = after.Length > 0 ? Mathf.Max(UiKit.MinTouch, 70f * after.Length + 60f) : 0f;
            var total = beforeW + partGap + gapW + (afterW > 0 ? partGap + afterW : 0f);
            var center = hasImage ? 150f : 0f;
            var x = center - total / 2f;
            _word = AddTile(before, new Vector2(beforeW, h), new Vector2(x + beforeW / 2f, 110f), 130f);
            x += beforeW + partGap;
            _gap = AddTile("?", new Vector2(gapW, h), new Vector2(x + gapW / 2f, 110f), 130f);
            _slot = _gap.gameObject.AddComponent<DropSlot>();
            x += gapW + partGap;
            if (afterW > 0) _after = AddTile(after, new Vector2(afterW, h), new Vector2(x + afterW / 2f, 110f), 130f);

            const float size = 200f;
            for (var k = 0; k < Order.Count; k++)
            {
                var option = Order[k];
                var tile = AddTile(Round.options[option].text, new Vector2(size, size), new Vector2(RowX(k, Order.Count, size, 70f), -190f), 140f);
                var drag = tile.gameObject.AddComponent<DragTile>();
                drag.DroppedOn += slot => { if (slot == _slot) Answer(option); };
                OptionTiles[option] = tile;
            }
        }

        protected override async Awaitable OnCorrect()
        {
            var full = (Round.prompt_text ?? string.Empty).Replace("_", Round.options[Round.answer].text);
            _word.SetText(full);
            var rt = (RectTransform)_word.transform;
            rt.sizeDelta = new Vector2(Mathf.Max(rt.sizeDelta.x, 70f * full.Length + 60f), rt.sizeDelta.y);
            _gap.gameObject.SetActive(false);
            if (_after != null) _after.gameObject.SetActive(false);
            OptionTiles[Round.answer].gameObject.SetActive(false);
            await Ctx.Speech.PlayAsync(Round.prompt_audio);
        }

        protected override void ActForTest() => OptionTiles[Round.answer].GetComponent<DragTile>().SimulateDropOn(_slot);
    }
}
