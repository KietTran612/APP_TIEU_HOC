using System.Collections.Generic;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Chọn dòng đúng yêu cầu (lớp 2, thiết kế TV2 tập một mục 6): "Trong những dòng sau, dòng nào viết chưa thành
    /// câu?". App đọc câu hỏi; mỗi dòng là một thẻ (lưới 2 cột × 2 hàng, nhiều dòng thì chia trang). Chạm thẻ thì app đọc
    /// dòng đó; dòng đúng sáng lên và được đếm, dòng khác chỉ được đọc, không chê. Hai lần chạm chưa đúng liền nhau thì
    /// một dòng đúng còn thiếu được tô vàng gợi ý (mở trang có dòng đó). Tìm đủ thì khen và đi tiếp.
    /// </summary>
    public class ChooseLineView : StepViewBase
    {
        private const int PerPage = 4;
        private const float ColGap = 24f;
        private const float RowGap = 18f;
        private const float GridWidth = 1040f; // chừa hai bên cho nút lật trang
        private const float GridTop = 175f;

        private readonly List<Tile> _lines = new();
        private readonly HashSet<int> _found = new();
        private TMPro.TextMeshProUGUI _count;
        private PageButtons _pager;
        private int _misses;
        private int _hint = -1;

        internal int FoundCount => _found.Count;
        internal int HintIndex => _hint;
        internal int Page { get; private set; }
        internal int PageCount => Mathf.Max(1, (Step.items.Count + PerPage - 1) / PerPage);
        internal Tile LineTile(int index) => _lines[index];

        private int Need => Mathf.Max(1, Step.need);

        protected override void Build()
        {
            AddMarker();
            var question = UiKit.CreateLabel(Root.transform, Step.text, 44f);
            var qrt = question.rectTransform;
            qrt.anchorMin = qrt.anchorMax = new Vector2(0.5f, 0.5f);
            qrt.sizeDelta = new Vector2(GridWidth + 120f, 120f);
            qrt.anchoredPosition = new Vector2(40f, 265f);
            question.alignment = TMPro.TextAlignmentOptions.Left;
            question.enableAutoSizing = true;
            question.fontSizeMax = 44f;
            question.fontSizeMin = 30f;

            var w = (GridWidth - ColGap) / 2f;
            for (var k = 0; k < Step.items.Count; k++)
            {
                var index = k;
                var slot = k % PerPage;
                var x = (slot % 2 == 0 ? -1f : 1f) * (w + ColGap) / 2f;
                var y = GridTop - UiKit.MinTouch / 2f - (slot / 2) * (UiKit.MinTouch + RowGap);
                var tile = AddTile(Step.items[k].text, new Vector2(w, UiKit.MinTouch), new Vector2(x, y), 46f);
                tile.Tapped += () => _ = OnLineTapped(index);
                _lines.Add(tile);
            }

            _count = UiKit.CreateLabel(Root.transform, string.Empty, 40f);
            var crt = _count.rectTransform;
            crt.anchorMin = crt.anchorMax = new Vector2(0.5f, 0.5f);
            crt.sizeDelta = new Vector2(400f, 56f);
            crt.anchoredPosition = new Vector2(0f, -300f);
            UpdateCount();
            if (PageCount > 1) _pager = new PageButtons(Root.transform, Ctx.Assets, () => ShowPage(Page - 1), () => ShowPage(Page + 1));
            ShowPage(0);
            Replay();
        }

        private void ShowPage(int page)
        {
            Page = Mathf.Clamp(page, 0, PageCount - 1);
            for (var k = 0; k < _lines.Count; k++) _lines[k].gameObject.SetActive(k / PerPage == Page);
            _pager?.Show(Page, PageCount);
        }

        private void UpdateCount() => _count.text = string.Format(UiText.FoundFormat, Mathf.Min(_found.Count, Need), Need);

        private async Awaitable OnLineTapped(int index)
        {
            var item = Step.items[index];
            if (item.role != "target")
            {
                _ = Ctx.Speech.PlayAsync(item.audio);
                if (++_misses >= 2) ShowHint();
                return;
            }
            _misses = 0;
            if (_found.Add(index))
            {
                _lines[index].SetHighlighted(true);
                if (_hint == index)
                {
                    _lines[index].SetHint(false);
                    _hint = -1;
                }
                UpdateCount();
                Ctx.Fx?.Correct((RectTransform)_lines[index].transform);
            }
            await Ctx.Speech.PlayAsync(item.audio);
            if (!IsAlive || IsCompleted || _found.Count < Need) return;
            await Ctx.Speech.PlayAsync(SystemAudio.khen_01);
            if (IsAlive) Complete();
        }

        /// <summary>Tô vàng dòng đúng đầu tiên chưa tìm, mở trang có dòng đó.</summary>
        private void ShowHint()
        {
            for (var k = 0; k < Step.items.Count; k++)
            {
                if (Step.items[k].role != "target" || _found.Contains(k)) continue;
                if (_hint >= 0) _lines[_hint].SetHint(false);
                _hint = k;
                if (k / PerPage != Page) ShowPage(k / PerPage);
                _lines[k].SetHint(true);
                return;
            }
        }

        public override void Replay() => _ = Ctx.Speech.PlayAsync(Step.audio);

        protected override void ActForTest()
        {
            for (var k = 0; k < Step.items.Count; k++)
                if (Step.items[k].role == "target") _lines[k].SimulateTap();
        }
    }
}
