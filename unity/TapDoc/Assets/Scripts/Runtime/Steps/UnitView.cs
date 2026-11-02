using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Âm hoặc vần mới: một thẻ chữ thật to. Tự đọc một lần; bé chạm và nghe xong thì báo xong.
    /// Chữ có nhiều cách đọc (Phụ lục tr.120–122) thì thẻ nhỏ lại, dưới thẻ có một nút cho mỗi cách đọc (ghi rõ đọc
    /// khi học, âm chuẩn hay tên chữ cái) và nút "Vì sao?" mở Ghi chú của bài.
    /// </summary>
    public class UnitView : StepViewBase
    {
        private const float TileSize = 460f;
        private const float SmallTileSize = 320f;
        private const float SmallTileY = 165f;
        private const float RowY = -245f;
        private const float RowHeight = 170f;
        private const float ReadingWidth = 330f;
        private const float WhyWidth = 200f;
        private const float RowGap = 20f;

        private static readonly Dictionary<string, string> KindLabels = new()
        {
            ["hoc"] = UiText.ReadingLearn,
            ["chuan"] = UiText.ReadingStandard,
            ["tenchu"] = UiText.ReadingLetterName,
        };

        private Tile _tile;

        protected override void Build()
        {
            var readings = Step.readings.Where(r => r != null && !string.IsNullOrEmpty(r.audio)).ToList();
            if (readings.Count == 0)
            {
                _tile = AddTile(TextStyler.Apply(Step.text, Step.hl), new Vector2(TileSize, TileSize), Vector2.zero, 300f);
            }
            else
            {
                _tile = AddTile(TextStyler.Apply(Step.text, Step.hl), new Vector2(SmallTileSize, SmallTileSize),
                    new Vector2(0f, SmallTileY), 220f);
                BuildReadingRow(readings);
            }
            _tile.Tapped += OnTapped;
            _ = Ctx.Speech.PlayAsync(Step.audio);
        }

        private void BuildReadingRow(List<Reading> readings)
        {
            var buttons = new List<(Button button, float width)>();
            foreach (var reading in readings)
            {
                var audio = reading.audio;
                var button = UiKit.CreateCardButton(Root.transform, Caption(reading), () => _ = Ctx.Speech.PlayAsync(audio));
                button.name = $"Reading_{audio}";
                buttons.Add((button, ReadingWidth));
            }
            if (Ctx.OpenNotes != null)
            {
                var notes = Ctx.OpenNotes;
                buttons.Add((UiKit.CreateButton(Root.transform, UiText.Why, () => notes()), WhyWidth));
            }

            var total = buttons.Sum(b => b.width) + RowGap * (buttons.Count - 1);
            var x = -total / 2f;
            foreach (var (button, width) in buttons)
            {
                var rt = (RectTransform)button.transform;
                rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
                rt.sizeDelta = new Vector2(width, RowHeight);
                rt.anchoredPosition = new Vector2(x + width / 2f, RowY);
                x += width + RowGap;
            }
        }

        /// <summary>Dòng to là chữ đọc; dòng nhỏ là loại cách đọc, kèm lý do nếu đọc khi học để phân biệt chữ.</summary>
        private static string Caption(Reading reading)
        {
            var kinds = string.Join(" · ", reading.kinds.Select(k => KindLabels.TryGetValue(k, out var label) ? label : k));
            var detail = string.IsNullOrEmpty(reading.hint) ? kinds : $"{kinds}\n{reading.hint}";
            return $"<b>{reading.text}</b>\n<size=50%>{detail}</size>";
        }

        private async void OnTapped()
        {
            if (await Play(Step.audio)) Complete();
        }

        public override void Replay() => _ = Ctx.Speech.PlayAsync(Step.audio);

        protected override void ActForTest() => _tile.SimulateTap();
    }
}
