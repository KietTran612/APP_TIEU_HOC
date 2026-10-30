using System.Collections.Generic;
using System.Linq;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Từ ứng dụng (<c>words</c>) và đọc thêm (<c>reading</c>). Bé chạm đủ mọi thẻ thì báo xong.
    /// <list type="bullet">
    /// <item><c>words</c>: chạm một từ thì mở lần lượt màn đánh vần cho từng tiếng (bé tự đánh vần), rồi đọc trơn
    /// cả từ và hiện chú thích (nếu có).</item>
    /// <item><c>reading</c>: chạm một thẻ thì app làm mẫu đánh vần mọi tiếng rồi đọc thẻ.</item>
    /// </list>
    /// </summary>
    public class ItemsView : StepViewBase
    {
        private const float ReadingTileH = 170f;
        private const float ReadingGap = 24f;

        private readonly List<Tile> _tiles = new();
        private readonly Dictionary<int, RectTransform> _noteAnchors = new();
        private TapProgress _progress;
        private bool _busy;

        /// <summary>Màn đánh vần đang mở trên từ (chỉ ở bước <c>words</c>).</summary>
        internal SpellView ActiveOverlay { get; private set; }

        private bool IsWords => Step.type == "words";

        protected override void Build()
        {
            _progress = new TapProgress(Step.items.Count);
            AddMarker();
            if (IsWords) BuildWords();
            else BuildReading();
        }

        private void BuildWords()
        {
            var items = Step.items;
            const float colWidth = 420f;
            var left = -(items.Count - 1) * colWidth / 2f;
            // Không từ nào có tranh: thẻ chữ tự xuống dòng (ví dụ 4 từ của bảng y/i ở bài 14).
            var anyImage = items.Any(i => !string.IsNullOrEmpty(i.image));
            var anyNote = items.Any(i => !string.IsNullOrEmpty(i.note));
            var flow = anyImage ? null : FlowLayout.Place(items.Select(_ => 380f).ToList(), 160f, FlowWidth, 40f, anyNote ? 110f : 40f);
            for (var j = 0; j < items.Count; j++)
            {
                var index = j;
                var x = flow != null ? flow[j].x : left + j * colWidth;
                var item = items[j];
                var hasImage = !string.IsNullOrEmpty(item.image);
                if (hasImage)
                {
                    var sprite = Ctx.Assets.Image(item.image);
                    var pic = AddTile(string.Empty, new Vector2(320f, 280f), new Vector2(x, 140f), 68f, sprite);
                    pic.SetSprite(sprite, item.image);
                    pic.Tapped += () => OnWordTapped(index);
                    if (sprite == null) pic.gameObject.SetActive(false);
                }
                var y = flow != null ? flow[j].y : hasImage ? -95f : 0f;
                var tile = AddTile(TextStyler.Apply(item.text, item.hl), new Vector2(380f, 160f), new Vector2(x, y), 84f);
                tile.Tapped += () => OnWordTapped(index);
                _tiles.Add(tile);

                var anchor = new GameObject("NoteAnchor", typeof(RectTransform)).GetComponent<RectTransform>();
                anchor.SetParent(Root.transform, false);
                anchor.anchorMin = anchor.anchorMax = new Vector2(0.5f, 0.5f);
                anchor.sizeDelta = new Vector2(400f, 90f);
                anchor.anchoredPosition = new Vector2(x, y - 130f);
                _noteAnchors[j] = anchor;
            }
        }

        private void BuildReading()
        {
            // Mỗi hàng của sách là một hoặc nhiều dòng thẻ: hàng dài hơn Stage tự xuống dòng (ví dụ 9 tiếng ở bài 15).
            var lines = new List<List<(Item item, int index, float width, string label)>>();
            foreach (var group in Step.items.Select((it, j) => (it, j)).GroupBy(p => p.it.row).OrderBy(g => g.Key))
            {
                var row = group.ToList();
                var entries = row.Select(p => (item: p.it, index: p.j,
                    width: p.it.text.Length <= 3 ? 190f : 300f, label: (string)null)).ToList();
                var label = Step.labels != null && group.Key >= 0 && group.Key < Step.labels.Count ? Step.labels[group.Key] : null;
                if (!string.IsNullOrEmpty(label)) entries.Insert(0, (null, -1, 220f, label));
                var widths = entries.Select(p => p.width).ToList();
                foreach (var line in FlowLayout.Lines(widths, FlowWidth, ReadingGap))
                {
                    lines.Add(line.Select(k => entries[k]).ToList());
                }
            }
            var top = (lines.Count - 1) * (ReadingTileH + ReadingGap) / 2f;
            for (var r = 0; r < lines.Count; r++)
            {
                var line = lines[r];
                var x = -(line.Sum(p => p.width) + (line.Count - 1) * ReadingGap) / 2f;
                foreach (var (item, index, width, label) in line)
                {
                    var pos = new Vector2(x + width / 2f, top - r * (ReadingTileH + ReadingGap));
                    if (label != null)
                    {
                        var tmp = UiKit.CreateLabel(Root.transform, label, 60f);
                        var rt = tmp.rectTransform;
                        rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
                        rt.sizeDelta = new Vector2(width, ReadingTileH);
                        rt.anchoredPosition = pos;
                        x += width + ReadingGap;
                        continue;
                    }
                    var tile = AddTile(TextStyler.Apply(item.text, item.hl), new Vector2(width, ReadingTileH), pos, 76f);
                    tile.Tapped += () => OnReadingTapped(index);
                    _tiles.Add(tile);
                    x += width + ReadingGap;
                }
            }
        }

        private async void OnWordTapped(int index)
        {
            if (_busy) return;
            _busy = true;
            try
            {
                var item = Step.items[index];
                foreach (var spell in item.spells)
                {
                    if (!await SpellInOverlay(spell)) return;
                }
                _progress.Tap(index);
                var finished = await Play(item.audio);
                if (!IsAlive) return;
                if (!string.IsNullOrEmpty(item.note)) ShowNote(index, item.note);
                if (finished && _progress.AllTapped) Complete();
            }
            finally
            {
                _busy = false;
            }
        }

        /// <summary>Mở màn đánh vần phủ lên màn từ, chờ bé đánh vần xong rồi đóng.</summary>
        private async Awaitable<bool> SpellInOverlay(Spell spell)
        {
            var overlay = new GameObject("SpellOverlay", typeof(RectTransform), typeof(Image));
            overlay.transform.SetParent(Root.transform, false);
            var rt = (RectTransform)overlay.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = rt.offsetMax = Vector2.zero;
            var bg = overlay.GetComponent<Image>();
            bg.sprite = UiKit.WhiteSprite;
            bg.color = Palette.Paper;

            var ctx = new LessonContext { Lesson = Ctx.Lesson, Speech = Ctx.Speech, Assets = Ctx.Assets, Stage = rt, Fx = Ctx.Fx };
            var view = new SpellView();
            var done = false;
            view.Completed += () => done = true;
            ActiveOverlay = view;
            view.BindSpell(spell, null, null, ctx);
            while (!done && IsAlive) await Awaitable.NextFrameAsync();
            ActiveOverlay = null;
            if (overlay != null) Object.Destroy(overlay);
            return done && IsAlive;
        }

        private void ShowNote(int index, string note)
        {
            if (!_noteAnchors.TryGetValue(index, out var anchor) || anchor.childCount > 0) return;
            var label = UiKit.CreateLabel(anchor, note, 40f);
            var rt = label.rectTransform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = rt.offsetMax = Vector2.zero;
            label.fontStyle = FontStyles.Italic;
        }

        private async void OnReadingTapped(int index)
        {
            // Đánh dấu ngay khi chạm, như ở màn phân tích.
            _progress.Tap(index);
            var item = Step.items[index];
            var ids = item.spells.SelectMany(s => s.parts).Select(p => p.audio).ToList();
            if (ids.Count == 0 || ids[ids.Count - 1] != item.audio) ids.Add(item.audio);
            var finished = await Ctx.Speech.PlaySequenceAsync(ids);
            if (finished && IsAlive && _progress.AllTapped) Complete();
        }

        public override void Replay()
        {
            if (_busy) return;
            _ = Ctx.Speech.PlaySequenceAsync(Step.items.Select(i => i.audio).ToList());
        }

        protected override void ActForTest() => RunForTest();

        private async void RunForTest()
        {
            if (!IsWords)
            {
                for (var j = 0; j < Step.items.Count; j++) OnReadingTapped(j);
                return;
            }
            for (var j = 0; j < Step.items.Count && IsAlive; j++)
            {
                OnWordTapped(j);
                while (IsAlive && _busy)
                {
                    var overlay = ActiveOverlay;
                    if (overlay != null)
                    {
                        overlay.AutoPlayForTest();
                        while (IsAlive && ActiveOverlay == overlay) await Awaitable.NextFrameAsync();
                    }
                    else
                    {
                        await Awaitable.NextFrameAsync();
                    }
                }
            }
        }
    }
}
