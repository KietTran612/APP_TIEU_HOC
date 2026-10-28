using UnityEngine;

namespace TapDoc
{
    /// <summary>Nghe rồi chạm đúng thẻ chữ.</summary>
    public class ListenChooseView : RoundViewBase
    {
        protected override void Build()
        {
            const float size = 240f;
            for (var k = 0; k < Order.Count; k++)
            {
                var option = Order[k];
                var tile = AddTile(Round.options[option].text, new Vector2(size, size), new Vector2(RowX(k, Order.Count, size, 60f), 0f), 150f);
                tile.Tapped += () => Answer(option);
                OptionTiles[option] = tile;
            }
        }

        protected override void ActForTest() => OptionTiles[Round.answer].SimulateTap();
    }
}
