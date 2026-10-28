using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Nhìn chữ mẫu (to) rồi kéo đúng thẻ dấu vào ô chứa tiếng gốc. Kéo đúng thì ô đổi thành chữ mẫu.
    /// Dùng cho các cặp dấu mà giọng miền Nam đọc giống nhau, nên không có đề bằng âm thanh.
    /// </summary>
    public class LookToneView : RoundViewBase
    {
        private Tile _base;
        private DropSlot _slot;

        protected override void Build()
        {
            var model = AddTile(Round.prompt_text, new Vector2(360f, 260f), new Vector2(-380f, 120f), 180f);
            model.SetHighlighted(true);
            _base = AddTile(Round.base_text, new Vector2(360f, 260f), new Vector2(380f, 120f), 180f);
            _slot = _base.gameObject.AddComponent<DropSlot>();

            const float size = 200f;
            for (var k = 0; k < Order.Count; k++)
            {
                var option = Order[k];
                var tile = AddTile(Round.options[option].text, new Vector2(size, size), new Vector2(RowX(k, Order.Count, size, 80f), -190f), 150f);
                var drag = tile.gameObject.AddComponent<DragTile>();
                drag.DroppedOn += slot => { if (slot == _slot) Answer(option); };
                OptionTiles[option] = tile;
            }
        }

        protected override async Awaitable OnCorrect()
        {
            _base.SetText(Round.prompt_text);
            OptionTiles[Round.answer].gameObject.SetActive(false);
            await Awaitable.NextFrameAsync();
        }

        protected override void ActForTest() => OptionTiles[Round.answer].GetComponent<DragTile>().SimulateDropOn(_slot);
    }
}
