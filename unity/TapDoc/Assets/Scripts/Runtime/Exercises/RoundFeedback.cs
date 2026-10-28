using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Phản hồi một lượt luyện tập, không phạt: đúng thì khen; sai lần đầu thì mời thử lại và đọc lại đề;
    /// sai từ lần hai thì gợi ý đáp án đúng.
    /// </summary>
    public class RoundFeedback
    {
        private readonly LessonContext _ctx;
        private readonly int _roundIndex;
        private readonly string _promptAudio;
        private readonly AttemptTracker _tracker = new();

        public RoundFeedback(LessonContext ctx, int roundIndex, string promptAudio = null)
        {
            _ctx = ctx;
            _roundIndex = roundIndex;
            _promptAudio = promptAudio;
        }

        public int Mistakes => _tracker.Mistakes;

        /// <summary>Trả về <c>true</c> khi bé làm đúng (sau khi đã đọc xong lời khen).</summary>
        public async Awaitable<bool> Handle(bool correct, Tile correctTile)
        {
            switch (_tracker.Submit(correct))
            {
                case Feedback.Correct:
                    if (correctTile != null) correctTile.SetHint(false);
                    await _ctx.Speech.PlayAsync(_roundIndex % 2 == 0 ? SystemAudio.khen_01 : SystemAudio.khen_02);
                    return true;
                case Feedback.TryAgain:
                    var ids = new System.Collections.Generic.List<string> { SystemAudio.hd_thu_lai };
                    if (!string.IsNullOrEmpty(_promptAudio)) ids.Add(_promptAudio);
                    _ = _ctx.Speech.PlaySequenceAsync(ids);
                    return false;
                default:
                    if (correctTile != null) correctTile.SetHint(true);
                    return false;
            }
        }
    }
}
