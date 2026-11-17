using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Từ khóa (tranh và chữ) hoặc tranh không chữ (<c>picture</c>). Tự đọc một lần; bé chạm tranh hoặc chữ
    /// lần đầu và nghe xong thì báo xong. Thiếu tranh thì ẩn khung tranh.
    /// </summary>
    public class KeywordView : StepViewBase
    {
        /// <summary>Tranh chiếm từ 5% tới 95% thẻ theo cả hai chiều.</summary>
        internal static readonly Vector2 PictureFill = new(.05f, .95f);

        private Tile _imageTile;
        private Tile _textTile;

        protected override void Build()
        {
            var hasText = !string.IsNullOrEmpty(Step.text);
            var sprite = string.IsNullOrEmpty(Step.image) ? null : Ctx.Assets.Image(Step.image);

            if (!string.IsNullOrEmpty(Step.image))
            {
                var size = hasText ? new Vector2(460f, 460f) : new Vector2(600f, 600f);
                var offset = hasText ? new Vector2(-280f, 0f) : Vector2.zero;
                _imageTile = AddTile(string.Empty, size, offset, 68f, sprite);
                _imageTile.SetSprite(sprite, Step.image);
                // Thẻ tranh không có chữ: tranh lấp gần hết thẻ (bản thiết kế nâng cấp UI mục 4.1.4).
                if (_imageTile.ImageBox != null)
                {
                    var pic = (RectTransform)_imageTile.ImageBox.transform;
                    pic.anchorMin = new Vector2(PictureFill.x, PictureFill.x);
                    pic.anchorMax = new Vector2(PictureFill.y, PictureFill.y);
                }
                _imageTile.Tapped += OnTapped;
                // Thiếu tranh mà vẫn còn thẻ chữ thì bỏ hẳn thẻ tranh trống; tranh không chữ thì giữ để bé còn chạm được.
                if (sprite == null && hasText) _imageTile.gameObject.SetActive(false);
            }

            if (hasText)
            {
                var offset = string.IsNullOrEmpty(Step.image) ? Vector2.zero : new Vector2(300f, 0f);
                _textTile = AddTile(TextStyler.Apply(Step.text, Step.hl), new Vector2(560f, 240f), offset, 110f);
                _textTile.Tapped += OnTapped;
            }

            _ = Ctx.Speech.PlayAsync(Step.audio);
        }

        private async void OnTapped()
        {
            if (await Play(Step.audio)) Complete();
        }

        public override void Replay() => _ = Ctx.Speech.PlayAsync(Step.audio);

        protected override void ActForTest()
        {
            if (_textTile != null) _textTile.SimulateTap();
            else _imageTile?.SimulateTap();
        }
    }
}
