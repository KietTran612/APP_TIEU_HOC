using UnityEngine;

namespace TapDoc
{
    /// <summary>Nghe một từ rồi chạm đúng tranh.</summary>
    public class ListenPictureView : RoundViewBase
    {
        protected override void Build()
        {
            const float size = 380f;
            for (var k = 0; k < Order.Count; k++)
            {
                var option = Order[k];
                var id = Round.options[option].image;
                var sprite = Ctx.Assets.Image(id);
                var tile = AddTile(string.Empty, new Vector2(size, size), new Vector2(RowX(k, Order.Count, size, 40f), 0f), 68f, sprite);
                // Thiếu tranh thì hiện chữ thay tranh để bé vẫn chọn được.
                if (sprite == null) tile.SetText(Round.options[option].text);
                tile.SetSprite(sprite, id);
                tile.Tapped += () => Answer(option);
                OptionTiles[option] = tile;
            }
        }

        protected override void ActForTest() => OptionTiles[Round.answer].SimulateTap();
    }
}
