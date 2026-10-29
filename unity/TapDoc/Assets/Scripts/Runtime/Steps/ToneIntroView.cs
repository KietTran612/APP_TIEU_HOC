using UnityEngine;

namespace TapDoc
{
    /// <summary>Giới thiệu dấu: kí hiệu dấu thật to và tên dấu. Tự đọc; đọc xong thì báo xong; chạm thì đọc lại.</summary>
    public class ToneIntroView : StepViewBase
    {
        private Tile _glyphTile;

        protected override void Build()
        {
            _glyphTile = AddTile(Step.glyph, new Vector2(420f, 420f), new Vector2(0f, 90f), 320f);
            _glyphTile.SetTone(Step.tone);
            _glyphTile.Tapped += Replay;
            var name = UiKit.CreateLabel(Root.transform, Step.text, 96f);
            var rt = name.rectTransform;
            rt.anchorMin = new Vector2(0.5f, 0.5f);
            rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = new Vector2(600f, 140f);
            rt.anchoredPosition = new Vector2(0f, -220f);
            PlayIntro();
        }

        private async void PlayIntro()
        {
            if (await Play(Step.audio)) Complete();
        }

        public override void Replay() => _ = Ctx.Speech.PlayAsync(Step.audio);

        // Màn tự báo xong sau khi đọc; test chỉ cần chờ.
        protected override void ActForTest() { }
    }
}
