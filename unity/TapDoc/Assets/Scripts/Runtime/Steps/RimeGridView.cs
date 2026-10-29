using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Bảng nhóm vần (bài 79): hàng tiêu đề là các âm cuối, mỗi trang 3 hàng nguyên âm ở trái và các ô vần.
    /// Chạm ô nào thì đánh vần lần lượt các vần trong ô; mỗi trang có ít nhất một ô được chạm thì báo xong.
    /// </summary>
    public class RimeGridView : StepViewBase
    {
        private const int RowsPerPage = 3;
        private const float CellSize = 160f;
        private const float Gap = 6f;
        private const float VowelW = 56f;
        private const float HeaderH = 50f;
        private const float GridLeft = -695f;
        // 7 cột ô 160 chỉ còn chừa ~170 ở mép phải nên nút trang hẹp hơn mặc định.
        private const float ButtonX = 615f;
        private const float ButtonW = 160f;

        private readonly List<(Tile tile, Item item, int page)> _cells = new();
        private readonly List<(GameObject go, int page)> _rowLabels = new();
        private TapProgress _progress;
        private PageButtons _pager;
        private Item _lastTapped;
        private int _generation;

        internal int PageCount { get; private set; }
        internal int Page { get; private set; }

        private IEnumerable<Item> ByRole(string role) => Step.items.Where(i => i.role == role);

        protected override void Build()
        {
            var finals = ByRole("final").OrderBy(i => i.col).ToList();
            var vowels = ByRole("vowel").OrderBy(i => i.row).ToList();
            var cells = ByRole("cell").ToList();

            PageCount = Mathf.Max(1, (vowels.Count + RowsPerPage - 1) / RowsPerPage);
            _progress = new TapProgress(PageCount);

            // Bảng cao HeaderH + 3 hàng ô, đặt giữa Stage theo chiều dọc.
            var top = (HeaderH + RowsPerPage * (Gap + CellSize)) / 2f;
            var headerY = top - HeaderH / 2f;
            var col0X = GridLeft + VowelW + Gap + CellSize / 2f;

            foreach (var final in finals)
                Place(UiKit.CreateLabel(Root.transform, final.text, 44f).rectTransform,
                    new Vector2(CellSize, HeaderH), new Vector2(ColumnX(col0X, final.col), headerY));

            for (var r = 0; r < vowels.Count; r++)
            {
                var vowel = vowels[r];
                var page = r / RowsPerPage;
                var rowY = top - HeaderH - Gap - CellSize / 2f - r % RowsPerPage * (CellSize + Gap);

                var label = UiKit.CreateLabel(Root.transform, vowel.text, 52f);
                Place(label.rectTransform, new Vector2(VowelW, CellSize), new Vector2(GridLeft + VowelW / 2f, rowY));
                _rowLabels.Add((label.gameObject, page));

                foreach (var cell in cells.Where(i => i.row == vowel.row).OrderBy(i => i.col))
                {
                    var tile = AddTile(cell.text, new Vector2(CellSize, CellSize), new Vector2(ColumnX(col0X, cell.col), rowY), 76f);
                    var index = _cells.Count;
                    tile.Tapped += () => OnCellTapped(index);
                    _cells.Add((tile, cell, page));
                }
            }

            // Trang toàn ô trống không có gì để chạm: không được chặn việc báo xong.
            for (var p = 0; p < PageCount; p++)
                if (_cells.All(c => c.page != p)) _progress.Tap(p);

            if (PageCount > 1)
                _pager = new PageButtons(Root.transform, () => ShowPage(Page - 1), () => ShowPage(Page + 1), ButtonX, ButtonW);
            ShowPage(0);
        }

        private static float ColumnX(float col0X, int col) => col0X + col * (CellSize + Gap);

        private static void Place(RectTransform rt, Vector2 size, Vector2 position)
        {
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = size;
            rt.anchoredPosition = position;
        }

        private void ShowPage(int page)
        {
            Page = Mathf.Clamp(page, 0, PageCount - 1);
            foreach (var (go, p) in _rowLabels) go.SetActive(p == Page);
            foreach (var (tile, _, p) in _cells) tile.gameObject.SetActive(p == Page);
            _pager?.Show(Page, PageCount);
        }

        private async void OnCellTapped(int index)
        {
            var gen = ++_generation;
            var (tile, item, page) = _cells[index];
            _lastTapped = item;
            _progress.Tap(page);
            foreach (var c in _cells) c.tile.SetHighlighted(false);
            tile.SetHighlighted(true);
            var finished = await Ctx.Speech.PlaySequenceAsync(SpellIds(item));
            if (!IsAlive || gen != _generation) return;
            tile.SetHighlighted(false);
            if (finished && _progress.AllTapped) Complete();
        }

        // Ô "ai - ay" có hai lượt đánh vần, đọc nối tiếp.
        private static List<string> SpellIds(Item item) =>
            item.spells.SelectMany(s => s.parts).Select(p => p.audio).ToList();

        /// <summary>Đọc lại ô vừa chạm; chưa chạm ô nào thì không làm gì.</summary>
        public override void Replay()
        {
            if (_lastTapped == null) return;
            _ = Ctx.Speech.PlaySequenceAsync(SpellIds(_lastTapped));
        }

        protected override void ActForTest()
        {
            for (var p = 0; p < PageCount; p++)
            {
                ShowPage(p);
                _cells.FirstOrDefault(c => c.page == p).tile?.SimulateTap();
            }
        }
    }
}
