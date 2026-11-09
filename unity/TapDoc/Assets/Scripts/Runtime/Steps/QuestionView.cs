using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Câu hỏi hiểu bài (thiết kế tập 2, mục 7.2): câu hỏi hiện to, app đọc rồi nhắc "Con trả lời cùng bố mẹ nhé".
    /// Bé trả lời bằng miệng, app không chấm; bấm "Con trả lời rồi" để đi tiếp.
    /// </summary>
    public class QuestionView : StepViewBase
    {
        private const float BigButton = 180f;
        private Button _doneButton;

        protected override void Build()
        {
            AddMarker();
            if (Step.rows != null && Step.rows.Count > 0)
            {
                BuildWithLines();
                return;
            }
            var question = AddTile(Step.text, new Vector2(FlowWidth, 300f), new Vector2(0f, 120f), 72f);
            question.Tapped += Replay;
            var hint = UiKit.CreateLabel(Root.transform, UiText.AnswerWithParent, 44f);
            var rt = hint.rectTransform;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = new Vector2(FlowWidth, 70f);
            rt.anchoredPosition = new Vector2(0f, -70f);
            _doneButton = UiKit.CreateIconButton(Root.transform, Ctx.Assets, SystemIcons.Check, UiText.Answered, Complete,
                Palette.Orange);
            _doneButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;
            var brt = (RectTransform)_doneButton.transform;
            brt.anchorMin = brt.anchorMax = new Vector2(0.5f, 0.5f);
            brt.sizeDelta = new Vector2(BigButton, BigButton);
            brt.anchoredPosition = new Vector2(0f, -210f);
            Replay();
        }

        /// <summary>
        /// Câu hỏi lớp 2 có các câu sách in kèm ("Tìm bộ phận chính trong các câu sau: …"): câu hỏi ở trên, mỗi câu một
        /// thẻ chạm để nghe, nút "Con trả lời rồi" ở góc dưới phải.
        /// </summary>
        private void BuildWithLines()
        {
            var question = AddTile(Step.text, new Vector2(FlowWidth, 170f), new Vector2(0f, 235f), 54f);
            question.Tapped += Replay;
            var n = Step.rows.Count;
            const float top = 130f, bottom = -170f, gap = 12f;
            var height = Mathf.Min(90f, (top - bottom - gap * (n - 1)) / n);
            for (var k = 0; k < n; k++)
            {
                var row = Step.rows[k];
                var tile = AddTile(row.text, new Vector2(FlowWidth * 0.8f, height),
                    new Vector2(0f, top - height / 2f - k * (height + gap)), Mathf.Min(48f, height * 0.55f));
                tile.Tapped += () => _ = Ctx.Speech.PlayAsync(row.audio);
            }
            var hint = UiKit.CreateLabel(Root.transform, UiText.AnswerWithParent, 40f);
            var rt = hint.rectTransform;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = new Vector2(FlowWidth - 2f * 170f, 60f);
            rt.anchoredPosition = new Vector2(0f, -250f);
            _doneButton = UiKit.CreateIconButton(Root.transform, Ctx.Assets, SystemIcons.Check, UiText.Answered, Complete,
                Palette.Orange);
            _doneButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;
            var brt = (RectTransform)_doneButton.transform;
            brt.anchorMin = brt.anchorMax = new Vector2(0.5f, 0.5f);
            brt.sizeDelta = new Vector2(140f, 140f);
            brt.anchoredPosition = new Vector2(FlowWidth / 2f - 70f, -250f);
            Replay();
        }

        public override void Replay() =>
            _ = Ctx.Speech.PlaySequenceAsync(new System.Collections.Generic.List<string> { Step.audio, SystemAudio.hd_tra_loi_mieng });

        protected override void ActForTest() => _doneButton.onClick.Invoke();
    }
}
