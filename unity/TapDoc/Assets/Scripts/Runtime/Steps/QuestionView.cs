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

        public override void Replay() =>
            _ = Ctx.Speech.PlaySequenceAsync(new System.Collections.Generic.List<string> { Step.audio, SystemAudio.hd_tra_loi_mieng });

        protected override void ActForTest() => _doneButton.onClick.Invoke();
    }
}
