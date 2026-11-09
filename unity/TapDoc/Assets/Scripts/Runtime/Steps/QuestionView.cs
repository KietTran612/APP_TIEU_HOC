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

        private const int LinesPerPage = 4;
        private const float LinesGridWidth = 1040f; // chừa hai bên cho nút lật trang
        private readonly System.Collections.Generic.List<Tile> _lineTiles = new();
        private const int WideLine = 48; // câu dài hơn thì một cột
        private PageButtons _pager;
        private int _page;
        private int _perPage = LinesPerPage;

        /// <summary>
        /// Câu hỏi lớp 2 có các câu sách in kèm ("Tìm bộ phận chính trong các câu sau: …"): câu hỏi ở trên, các câu là thẻ
        /// chạm để nghe (lưới 2 cột × 2 hàng, nhiều câu thì chia trang), nút "Con trả lời rồi" ở góc dưới phải. Mọi thẻ
        /// cao bằng mức chạm tối thiểu.
        /// </summary>
        private void BuildWithLines()
        {
            var question = AddTile(Step.text, new Vector2(FlowWidth - 100f, UiKit.MinTouch), new Vector2(50f, 255f), 50f);
            question.Tapped += Replay;
            const float colGap = 24f, rowGap = 14f, top = 160f;
            var n = Step.rows.Count;
            // Câu dài (đoạn thư, đoạn văn chưa chấm câu) cần cả bề rộng: một cột, hai câu mỗi trang.
            var single = n == 1 || Step.rows.Exists(r => r.text.Length > WideLine);
            _perPage = single ? 2 : LinesPerPage;
            var w = single ? LinesGridWidth : (LinesGridWidth - colGap) / 2f;
            for (var k = 0; k < n; k++)
            {
                var row = Step.rows[k];
                var slot = single ? (k % _perPage) * 2 : k % LinesPerPage;
                var x = single ? 0f : (slot % 2 == 0 ? -1f : 1f) * (w + colGap) / 2f;
                var y = top - UiKit.MinTouch / 2f - (slot / 2) * (UiKit.MinTouch + rowGap);
                var tile = AddTile(row.text, new Vector2(w, UiKit.MinTouch), new Vector2(x, y), 42f);
                tile.Tapped += () => _ = Ctx.Speech.PlayAsync(row.audio);
                _lineTiles.Add(tile);
            }
            var hint = UiKit.CreateLabel(Root.transform, UiText.AnswerWithParent, 38f);
            var rt = hint.rectTransform;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = new Vector2(FlowWidth - 2f * (UiKit.MinTouch + 20f), 60f);
            rt.anchoredPosition = new Vector2(0f, -275f);
            _doneButton = UiKit.CreateIconButton(Root.transform, Ctx.Assets, SystemIcons.Check, UiText.Answered, Complete,
                Palette.Orange);
            _doneButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;
            var brt = (RectTransform)_doneButton.transform;
            brt.anchorMin = brt.anchorMax = new Vector2(0.5f, 0.5f);
            brt.sizeDelta = new Vector2(UiKit.MinTouch, UiKit.MinTouch);
            brt.anchoredPosition = new Vector2(FlowWidth / 2f - UiKit.MinTouch / 2f, -258f);
            var pages = (n + _perPage - 1) / _perPage;
            if (pages > 1) _pager = new PageButtons(Root.transform, Ctx.Assets, () => ShowLinesPage(_page - 1), () => ShowLinesPage(_page + 1));
            ShowLinesPage(0);
            Replay();
        }

        private void ShowLinesPage(int page)
        {
            var pages = Mathf.Max(1, (_lineTiles.Count + _perPage - 1) / _perPage);
            _page = Mathf.Clamp(page, 0, pages - 1);
            for (var k = 0; k < _lineTiles.Count; k++) _lineTiles[k].gameObject.SetActive(k / _perPage == _page);
            _pager?.Show(_page, pages);
        }

        public override void Replay() =>
            _ = Ctx.Speech.PlaySequenceAsync(new System.Collections.Generic.List<string> { Step.audio, SystemAudio.hd_tra_loi_mieng });

        protected override void ActForTest() => _doneButton.onClick.Invoke();
    }
}
