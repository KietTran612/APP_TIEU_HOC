using UnityEngine;

namespace TapDoc
{
    /// <summary>Âm hoặc vần mới: một thẻ chữ thật to. Tự đọc một lần; bé chạm và nghe xong thì báo xong.</summary>
    public class UnitView : StepViewBase
    {
        private Tile _tile;

        protected override void Build()
        {
            _tile = AddTile(TextStyler.Apply(Step.text, Step.hl), new Vector2(460f, 460f), Vector2.zero, 300f);
            _tile.Tapped += OnTapped;
            _ = Ctx.Speech.PlayAsync(Step.audio);
        }

        private async void OnTapped()
        {
            if (await Play(Step.audio)) Complete();
        }

        public override void Replay() => _ = Ctx.Speech.PlayAsync(Step.audio);

        protected override void ActForTest() => _tile.SimulateTap();
    }
}
