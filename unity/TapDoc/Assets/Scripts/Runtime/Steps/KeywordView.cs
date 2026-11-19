using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Từ khóa (tranh và chữ) hoặc tranh không chữ (<c>picture</c>). Tự đọc một lần; bé chạm tranh hoặc chữ
    /// lần đầu và nghe xong thì báo xong. Thiếu tranh thì ẩn khung tranh.
    /// Tranh động: tự phát một lần sau lần đọc trọn đầu tiên của bước (app tự đọc hay bé chạm); sau đó chạm tranh thì
    /// đọc rồi xem lại, chạm chữ hay nút Nghe lại thì chỉ đọc.
    /// </summary>
    public class KeywordView : StepViewBase
    {
        /// <summary>Tranh chiếm từ 5% tới 95% thẻ theo cả hai chiều.</summary>
        internal static readonly Vector2 PictureFill = new(.05f, .95f);

        private Tile _imageTile;
        private Tile _textTile;
        private bool _clipAutoPlayed;

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
                _imageTile.Tapped += () => Read(picture: true, completes: true);
                // Thiếu tranh mà vẫn còn thẻ chữ thì bỏ hẳn thẻ tranh trống; tranh không chữ thì giữ để bé còn chạm được.
                if (sprite == null && hasText) _imageTile.gameObject.SetActive(false);
            }

            if (hasText)
            {
                var offset = string.IsNullOrEmpty(Step.image) ? Vector2.zero : new Vector2(300f, 0f);
                _textTile = AddTile(TextStyler.Apply(Step.text, Step.hl), new Vector2(560f, 240f), offset, 110f);
                _textTile.Tapped += () => Read(picture: false, completes: true);
            }

            Read(picture: false, completes: false);
        }

        /// <summary>
        /// Đọc chữ của bước. Đọc trọn thì: bé chạm (<paramref name="completes"/>) thì báo xong; rồi phát tranh động nếu bé
        /// chạm tranh, hoặc nếu đây là lần đọc trọn đầu tiên của bước.
        /// </summary>
        private async void Read(bool picture, bool completes)
        {
            if (!await Play(Step.audio)) return;
            if (completes) Complete();
            if (!picture && _clipAutoPlayed) return;
            _clipAutoPlayed = true;
            PlayClip(_imageTile, Step.image);
        }

        public override void Replay() => Read(picture: false, completes: false);

        protected override void ActForTest()
        {
            if (_textTile != null) _textTile.SimulateTap();
            else _imageTile?.SimulateTap();
        }
    }
}
