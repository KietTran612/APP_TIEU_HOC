using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Đánh vần (dùng cho cả <c>spell</c> và <c>tone_attach</c>). App làm mẫu cả chuỗi, rồi bé tự chạm các thẻ
    /// âm/vần theo đúng thứ tự (thẻ dấu thì kéo vào vùng kết quả khi <c>drag_tone</c>). Chạm sai thứ tự chỉ làm
    /// thẻ đúng nhấp nháy, không có âm thanh chê.
    /// </summary>
    public class SpellView : StepViewBase
    {
        private const float TileSize = 220f;
        private const float TileGap = 30f;

        private readonly Dictionary<int, Tile> _tiles = new();
        private List<Part> _parts;
        private SpellPractice _practice;
        private Tile _result;
        private DropSlot _resultSlot;
        private Tile _imageTile;
        private bool _finishing;

        /// <summary>Đã làm mẫu xong và đang chờ bé làm.</summary>
        internal bool InPractice { get; private set; }

        /// <summary>Đánh vần một chuỗi không đi kèm bước bài học (Task 19: từng tiếng trong từ ứng dụng).</summary>
        public void BindSpell(Spell spell, string thenAudio, string image, LessonContext ctx) =>
            Bind(new Step { type = "spell", spell = spell, then_audio = thenAudio, image = image }, ctx);

        protected override void Build()
        {
            var spell = Step.spell ?? new Spell();
            _parts = spell.parts ?? new List<Part>();
            _practice = new SpellPractice(spell);

            // Hàng trên: thẻ âm, vần, dấu (mảnh join không có thẻ, chữ ghép hiện ở vùng kết quả).
            var actionable = Enumerable.Range(0, _parts.Count).Where(i => _parts[i].kind != "join").ToList();
            var rowWidth = actionable.Count * TileSize + (actionable.Count - 1) * TileGap;
            for (var k = 0; k < actionable.Count; k++)
            {
                var i = actionable[k];
                var x = -rowWidth / 2f + TileSize / 2f + k * (TileSize + TileGap);
                var tile = AddTile(_parts[i].text, new Vector2(TileSize, TileSize), new Vector2(x, 180f), 130f);
                _tiles[i] = tile;
                if (_parts[i].kind == "tone") tile.SetTone(_parts[i].tone);
                if (_practice.RequiresDrag(i))
                {
                    var drag = tile.gameObject.AddComponent<DragTile>();
                    drag.DroppedOn += slot => OnToneDropped(i, slot);
                }
                else
                {
                    tile.Tapped += () => OnTileTapped(i);
                }
            }

            var hasImage = !string.IsNullOrEmpty(Step.image);
            var resultX = hasImage ? -170f : 0f;
            _result = AddTile(string.Empty, new Vector2(560f, 230f), new Vector2(resultX, -150f), 150f);
            _resultSlot = _result.gameObject.AddComponent<DropSlot>();

            if (hasImage)
            {
                _imageTile = AddTile(string.Empty, new Vector2(300f, 300f), new Vector2(430f, -150f), 68f);
                _imageTile.SetSprite(null, Step.image); // tranh chỉ hiện khi bé làm xong
                _imageTile.gameObject.SetActive(false);
            }

            RunDemo();
        }

        private async void RunDemo()
        {
            var ids = _parts.Select(p => p.audio).ToList();
            await Ctx.Speech.PlaySequenceAsync(ids, ShowPart);
            if (!IsAlive) return;
            if (!await Play(SystemAudio.hd_danh_van_theo)) return;

            ResetTiles();
            var auto = _practice.Start();
            if (auto.Count > 0 && !await PlayParts(auto)) return;
            InPractice = true;
            if (_practice.IsDone) Finish();
        }

        private void ShowPart(int i)
        {
            if (!IsAlive || i < 0 || i >= _parts.Count) return;
            if (_parts[i].kind == "join")
            {
                _result.SetText(_parts[i].text);
                return;
            }
            foreach (var t in _tiles.Values) t.SetHighlighted(false);
            if (_tiles.TryGetValue(i, out var tile)) tile.SetHighlighted(true);
        }

        private void ResetTiles()
        {
            foreach (var t in _tiles.Values)
            {
                t.SetHighlighted(false);
                t.SetHint(false);
            }
            _result.SetText(string.Empty);
        }

        private void OnTileTapped(int i)
        {
            if (!InPractice) return;
            Act(i);
        }

        private void OnToneDropped(int i, DropSlot slot)
        {
            if (!InPractice || slot != _resultSlot) return;
            Act(i);
        }

        private async void Act(int i)
        {
            var result = _practice.Act(i, out var auto);
            if (result == TapResult.WrongOrder)
            {
                if (_tiles.TryGetValue(_practice.Expected, out var expected)) expected.SetHint(true);
                return;
            }
            if (result != TapResult.Accepted) return;

            foreach (var t in _tiles.Values) t.SetHint(false);
            _tiles[i].SetHighlighted(true);
            var toPlay = new List<int> { i };
            toPlay.AddRange(auto);
            var finished = await PlayParts(toPlay);
            if (finished && _practice.IsDone) Finish();
        }

        /// <summary>Đọc các mảnh theo thứ tự; mảnh join thì hiện chữ ghép ở vùng kết quả.</summary>
        private async Awaitable<bool> PlayParts(List<int> indices)
        {
            var ids = indices.Select(k => _parts[k].audio).ToList();
            var finished = await Ctx.Speech.PlaySequenceAsync(ids, n =>
            {
                if (!IsAlive) return;
                var k = indices[n];
                if (_parts[k].kind == "join") _result.SetText(_parts[k].text);
            });
            return finished && IsAlive;
        }

        private async void Finish()
        {
            if (_finishing) return;
            _finishing = true;
            if (!string.IsNullOrEmpty(Step.then_audio))
            {
                await Ctx.Speech.PlayAsync(Step.then_audio);
                if (!IsAlive) return;
            }
            if (_imageTile != null)
            {
                _imageTile.gameObject.SetActive(true);
                _imageTile.SetSprite(Ctx.Assets.Image(Step.image), Step.image);
            }
            Complete();
        }

        public override void Replay()
        {
            if (!InPractice) return;
            _ = Ctx.Speech.PlaySequenceAsync(_parts.Select(p => p.audio).ToList());
        }

        protected override void ActForTest() => RunForTest();

        /// <summary>Cho màn khác (từ ứng dụng) tự đánh vần hộ trong test.</summary>
        internal void AutoPlayForTest() => RunForTest();

        private async void RunForTest()
        {
            while (IsAlive && !InPractice) await Awaitable.NextFrameAsync();
            while (IsAlive && !_practice.IsDone)
            {
                var i = _practice.Expected;
                if (_practice.RequiresDrag(i)) OnToneDropped(i, _resultSlot);
                else OnTileTapped(i);
                await Awaitable.NextFrameAsync();
            }
        }
    }
}
