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
            for (var j = 0; j < items.Count; j++)
            {
                var index = j;
                var x = left + j * colWidth;
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
                var y = hasImage ? -95f : 0f;
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
            var rows = Step.items.Select((it, j) => (it, j)).GroupBy(p => p.it.row).OrderBy(g => g.Key).ToList();
            const float tileH = 170f;
            const float gap = 24f;
            var top = (rows.Count - 1) * (tileH + gap) / 2f;
            for (var r = 0; r < rows.Count; r++)
            {
                var row = rows[r].ToList();
                var widths = row.Select(p => p.it.text.Length <= 3 ? 190f : 300f).ToList();
                var total = widths.Sum() + (row.Count - 1) * gap;
                var x = -total / 2f;
                for (var k = 0; k < row.Count; k++)
                {
                    var (item, index) = row[k];
                    var cx = x + widths[k] / 2f;
                    var tile = AddTile(item.text, new Vector2(widths[k], tileH), new Vector2(cx, top - r * (tileH + gap)), 76f);
                    tile.Tapped += () => OnReadingTapped(index);
                    _tiles.Add(tile);
                    x += widths[k] + gap;
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
            bg.color = new Color(0.965f, 0.933f, 0.863f, 1f);

            var ctx = new LessonContext { Lesson = Ctx.Lesson, Speech = Ctx.Speech, Assets = Ctx.Assets, Stage = rt };
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
