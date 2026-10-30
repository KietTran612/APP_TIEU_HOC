using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Phần dùng chung của các màn luyện tập (Phần 2): đọc lời hướng dẫn rồi đề khi mở, xáo thứ tự phương án,
    /// chấm qua <see cref="RoundFeedback"/> và báo <c>Completed</c> sau khi đã khen.
    /// </summary>
    public abstract class RoundViewBase : IRoundView, ITestCompletable
    {
        private static readonly System.Random Shuffler = new();

        public GameObject Root { get; private set; }
        public event Action Completed;

        protected LessonContext Ctx { get; private set; }
        protected Round Round { get; private set; }
        protected RoundFeedback Feedback { get; private set; }

        /// <summary>Thứ tự hiển thị: vị trí k trên màn hình là phương án <c>Order[k]</c> trong dữ liệu.</summary>
        protected List<int> Order { get; private set; }

        /// <summary>Thẻ của từng phương án, theo chỉ số trong dữ liệu.</summary>
        protected readonly Dictionary<int, Tile> OptionTiles = new();

        private bool _answered;
        private bool _completed;

        protected bool IsAlive => Root != null;

        public void Bind(Round round, LessonContext ctx)
        {
            Round = round;
            Ctx = ctx;
            var index = ctx.Lesson != null ? ctx.Lesson.part2.IndexOf(round) : 0;
            Feedback = new RoundFeedback(ctx, Math.Max(index, 0), round.prompt_audio);
            Order = Enumerable.Range(0, round.options.Count).OrderBy(_ => Shuffler.Next()).ToList();

            Root = new GameObject(GetType().Name, typeof(RectTransform));
            Root.transform.SetParent(ctx.Stage, false);
            var rt = (RectTransform)Root.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            Build();
            Replay();
        }

        protected abstract void Build();

        /// <summary>Đọc lời hướng dẫn rồi đề.</summary>
        public void Replay()
        {
            var ids = new List<string>();
            if (!string.IsNullOrEmpty(Round.instruction_audio)) ids.Add(Round.instruction_audio);
            if (!string.IsNullOrEmpty(Round.prompt_audio)) ids.Add(Round.prompt_audio);
            if (ids.Count > 0) _ = Ctx.Speech.PlaySequenceAsync(ids);
        }

        /// <summary>Chấm phương án <paramref name="option"/> (chỉ số trong dữ liệu).</summary>
        protected async void Answer(int option)
        {
            if (_answered || !IsAlive) return;
            var correct = option == Round.answer;
            if (correct)
            {
                _answered = true;
                await OnCorrect();
                if (!IsAlive) return;
            }
            OptionTiles.TryGetValue(Round.answer, out var answerTile);
            OptionTiles.TryGetValue(option, out var chosenTile);
            if (!await Feedback.Handle(correct, answerTile, chosenTile)) return;
            if (!IsAlive || _completed) return;
            _completed = true;
            ReportFinished();
            Completed?.Invoke();
        }

        /// <summary>Báo lượt xong kèm số lần nhầm. Lỗi khi ghi tiến độ không được chặn việc chuyển lượt.</summary>
        private void ReportFinished()
        {
            try
            {
                Ctx.RoundFinished?.Invoke(Round, Feedback.Mistakes);
            }
            catch (Exception ex)
            {
                Debug.LogException(ex);
            }
        }

        /// <summary>Việc riêng khi bé làm đúng, trước lời khen (ví dụ hiện đủ chữ). Mặc định không làm gì.</summary>
        protected virtual Awaitable OnCorrect() => Done();

        private static async Awaitable Done() => await Awaitable.NextFrameAsync();

        protected Tile AddTile(string richText, Vector2 size, Vector2 offset, float fontSize, Sprite image = null)
        {
            var tile = UiKit.CreateTile(Root.transform, richText, image);
            var rt = (RectTransform)tile.transform;
            rt.anchorMin = new Vector2(0.5f, 0.5f);
            rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = size;
            rt.anchoredPosition = offset;
            tile.SetFontSize(fontSize);
            return tile;
        }

        /// <summary>Hoành độ của ô thứ <paramref name="k"/> trong hàng <paramref name="count"/> ô rộng <paramref name="width"/>.</summary>
        protected static float RowX(int k, int count, float width, float gap) =>
            -((count - 1) * (width + gap)) / 2f + k * (width + gap);

        protected abstract void ActForTest();

        /// <summary>
        /// Móc cho test: chọn một phương án sai theo đúng cách bé thao tác ở màn này (chạm thẻ, hoặc kéo thẻ vào ô nhận).
        /// </summary>
        internal void ActWrongForTest()
        {
            var wrong = Enumerable.Range(0, Round.options.Count).First(i => i != Round.answer);
            var tile = OptionTiles[wrong];
            var drag = tile.GetComponent<DragTile>();
            if (drag != null)
            {
                drag.SimulateDropOn(Root.GetComponentInChildren<DropSlot>(true));
            }
            else
            {
                tile.SimulateTap();
            }
        }

        public IEnumerator CompleteForTest()
        {
            if (_completed) yield break;
            var done = false;
            Action mark = () => done = true;
            Completed += mark;
            try
            {
                ActForTest();
                while (!done) yield return null;
            }
            finally
            {
                Completed -= mark;
            }
        }
    }
}
