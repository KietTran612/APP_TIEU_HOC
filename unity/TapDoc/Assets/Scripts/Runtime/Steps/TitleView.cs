using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Tên bài tập đọc (hoặc tên phần của trang chính tả): chữ to giữa màn, dòng phụ "(Học thuộc lòng)" nếu có.
    /// App đọc tên bài một lần rồi cho đi tiếp; chạm vào tên thì nghe lại.
    /// </summary>
    public class TitleView : StepViewBase
    {
        private Tile _title;

        protected override void Build()
        {
            AddMarker();
            _title = AddTile(Step.text, new Vector2(FlowWidth, 240f), new Vector2(0f, 60f), 110f);
            _title.Tapped += Replay;
            var sub = Step.labels != null && Step.labels.Count > 0 ? Step.labels[0] : null;
            if (!string.IsNullOrEmpty(sub))
            {
                var label = UiKit.CreateLabel(Root.transform, $"({sub})", 52f);
                var rt = label.rectTransform;
                rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
                rt.sizeDelta = new Vector2(FlowWidth, 90f);
                rt.anchoredPosition = new Vector2(0f, -130f);
                label.fontStyle = TMPro.FontStyles.Italic;
            }
            _ = Start();
        }

        private async Awaitable Start()
        {
            await Play(Step.audio);
            Complete();
        }

        public override void Replay() => _ = Ctx.Speech.PlayAsync(Step.audio);

        protected override void ActForTest() => Complete();
    }
}
