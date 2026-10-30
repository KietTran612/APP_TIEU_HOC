using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Câu ứng dụng: mỗi tiếng một thẻ trên một dòng. Chạm tiếng nào thì app làm mẫu đánh vần tiếng đó.
    /// "Nghe cả câu" đọc câu, các tiếng sáng lần lượt. "Con đọc xong rồi" báo xong.
    /// </summary>
    public class SentenceView : StepViewBase
    {
        private const float BigButton = 180f;

        private readonly List<Tile> _tokens = new();
        private Button _doneButton;
        private int _listenGeneration;

        protected override void Build()
        {
            AddMarker();
            var items = Step.items;
            const float gap = 24f;
            var widths = items.Select(i => i.text.Length <= 3 ? 200f : 280f).ToList();
            // Câu dài (ví dụ 8 tiếng ở bài 12) tự xuống dòng, vẫn giữ thứ tự đọc.
            var centers = FlowLayout.Place(widths, 190f, FlowWidth, gap, 20f);
            for (var j = 0; j < items.Count; j++)
            {
                var index = j;
                // Bài vần: tô vần mới như sách (dữ liệu chỉ có hl ở bài vần).
                var tile = AddTile(TextStyler.Apply(items[j].text, items[j].hl), new Vector2(widths[j], 190f), centers[j] + new Vector2(0f, 115f), 110f);
                tile.Tapped += () => OnTokenTapped(index);
                _tokens.Add(tile);
            }

            // Nút loa to ngay dưới câu (chạm là nghe ngay, không có tiếng tách); nút "Con đọc xong rồi" có dấu tích, nền cam.
            var listen = UiKit.CreateIconButton(Root.transform, Ctx.Assets, SystemIcons.Speaker, UiText.ListenSentence, OnListen);
            Place(listen, new Vector2(-120f, -180f), new Vector2(BigButton, BigButton));
            _doneButton = UiKit.CreateIconButton(Root.transform, Ctx.Assets, SystemIcons.Check, UiText.DoneReading, Complete,
                Palette.Orange);
            _doneButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;
            Place(_doneButton, new Vector2(120f, -180f), new Vector2(BigButton, BigButton));
        }

        private static void Place(Button b, Vector2 pos, Vector2 size)
        {
            var rt = (RectTransform)b.transform;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = size;
            rt.anchoredPosition = pos;
        }

        private void OnTokenTapped(int index)
        {
            _listenGeneration++;
            Highlight(-1);
            var item = Step.items[index];
            var ids = item.spells.SelectMany(s => s.parts).Select(p => p.audio).ToList();
            // Mảnh cuối của chuỗi đánh vần đã là tiếng đó: không đọc lại.
            if (ids.Count == 0 || ids[ids.Count - 1] != item.audio) ids.Add(item.audio);
            _ = Ctx.Speech.PlaySequenceAsync(ids);
        }

        private async void OnListen()
        {
            var gen = ++_listenGeneration;
            var clip = Ctx.Assets.Audio(Step.audio);
            var play = Ctx.Speech.PlayAsync(Step.audio);
            if (clip != null && _tokens.Count > 0)
            {
                var starts = SequenceTimeline.EvenStarts(clip.length * Ctx.Speech.WaitScale, _tokens.Count);
                var t0 = Time.realtimeSinceStartup;
                for (var k = 0; k < starts.Length; k++)
                {
                    while (Time.realtimeSinceStartup - t0 < starts[k])
                    {
                        await Awaitable.NextFrameAsync();
                        if (!IsAlive || gen != _listenGeneration) return;
                    }
                    Highlight(k);
                }
            }
            await play;
            if (IsAlive && gen == _listenGeneration) Highlight(-1);
        }

        private void Highlight(int index)
        {
            for (var k = 0; k < _tokens.Count; k++) _tokens[k].SetHighlighted(k == index);
        }

        public override void Replay() => OnListen();

        protected override void ActForTest() => _doneButton.onClick.Invoke();
    }
}
