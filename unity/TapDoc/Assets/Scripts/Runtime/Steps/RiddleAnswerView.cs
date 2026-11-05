using System.Collections.Generic;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Đoán đáp án câu đố (thiết kế tập 2, mục 7.3): ba tranh, app nhắc "Con đoán xem là gì nhé". Chọn đúng thì hiện
    /// chữ đáp án như ở trang "Trả lời câu đố" (tr.138) và app đọc đáp án. Chọn sai không chê, cho chọn lại; sai hai lần
    /// thì tranh đúng được tô gợi ý.
    /// </summary>
    public class RiddleAnswerView : StepViewBase
    {
        private const float PictureSize = 320f;

        private readonly List<Tile> _options = new();
        private TMPro.TextMeshProUGUI _answer;
        private RoundFeedback _feedback;
        private bool _busy;

        internal bool AnswerShown => _answer != null && _answer.gameObject.activeSelf;

        protected override void Build()
        {
            AddMarker();
            _feedback = new RoundFeedback(Ctx, 0, SystemAudio.hd_doan_do);
            for (var k = 0; k < Step.items.Count; k++)
            {
                var item = Step.items[k];
                var x = (k - (Step.items.Count - 1) / 2f) * (PictureSize + 60f);
                var sprite = Ctx.Assets.Image(item.image);
                var tile = AddTile(string.Empty, new Vector2(PictureSize, PictureSize), new Vector2(x, 80f), 60f, sprite);
                tile.SetSprite(sprite, item.image);
                tile.Tapped += () => _ = Choose(item, tile);
                _options.Add(tile);
            }
            _answer = UiKit.CreateLabel(Root.transform, Step.text, 84f);
            var rt = _answer.rectTransform;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = new Vector2(FlowWidth, 130f);
            rt.anchoredPosition = new Vector2(0f, -200f);
            _answer.gameObject.SetActive(false);
            _ = Ctx.Speech.PlayAsync(SystemAudio.hd_doan_do);
        }

        private Tile CorrectTile => _options.Find(t => t.ImageId == Step.image);

        private async Awaitable Choose(Item item, Tile chosen)
        {
            if (_busy || IsCompleted) return;
            _busy = true;
            var ok = await _feedback.Handle(item.image == Step.image, CorrectTile, chosen);
            if (!IsAlive) return;
            if (!ok)
            {
                _busy = false;
                return;
            }
            foreach (var tile in _options)
                if (tile != CorrectTile) tile.gameObject.SetActive(false);
            _answer.gameObject.SetActive(true);
            await Play(Step.audio);
            _busy = false;
            Complete();
        }

        public override void Replay() => _ = Ctx.Speech.PlayAsync(AnswerShown ? Step.audio : SystemAudio.hd_doan_do);

        protected override void ActForTest() => _ = Choose(Step.items.Find(i => i.image == Step.image), CorrectTile);
    }
}
