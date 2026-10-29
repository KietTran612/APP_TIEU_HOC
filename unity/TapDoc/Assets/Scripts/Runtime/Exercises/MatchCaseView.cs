using UnityEngine;

namespace TapDoc
{
    /// <summary>Nhìn chữ thường mẫu rồi chạm chữ hoa tương ứng.</summary>
    public class MatchCaseView : RoundViewBase
    {
        protected override void Build()
        {
            var model = AddTile(Round.prompt_text, new Vector2(360f, 260f), new Vector2(0f, 170f), 180f);
            model.SetHighlighted(true);
            const float size = 240f;
            for (var k = 0; k < Order.Count; k++)
            {
                var option = Order[k];
                var tile = AddTile(Round.options[option].text, new Vector2(size, size),
                    new Vector2(RowX(k, Order.Count, size, 60f), -170f), 150f);
                tile.Tapped += () => Answer(option);
                OptionTiles[option] = tile;
            }
        }

        protected override void ActForTest() => OptionTiles[Round.answer].SimulateTap();
    }
}
