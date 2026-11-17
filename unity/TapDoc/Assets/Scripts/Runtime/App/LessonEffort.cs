namespace TapDoc
{
    /// <summary>
    /// Cách bé làm trong một bài (chỉ trong bộ nhớ), để màn Xong bài khen đúng cách làm, không khen chung chung (bản
    /// thiết kế nâng cấp UI mục 4.3; N6: khen cách làm, không khen "thông minh"; app không có micro nên không khen "đọc to").
    /// </summary>
    public sealed class LessonEffort
    {
        /// <summary>Số lượt Phần 2 đã xong.</summary>
        public int Rounds { get; private set; }

        /// <summary>Tổng số lần nhầm ở Phần 2.</summary>
        public int Mistakes { get; private set; }

        /// <summary>Số lượt bé nhầm đúng một lần rồi tự làm đúng, trước khi gợi ý hiện (gợi ý hiện từ lần nhầm thứ hai).</summary>
        public int SelfCorrected { get; private set; }

        /// <summary>Số lần bé chạm nút Nghe lại (phần 1 hay phần 2).</summary>
        public int Replays { get; private set; }

        public void RecordRound(int mistakes)
        {
            Rounds++;
            if (mistakes <= 0) return;
            Mistakes += mistakes;
            if (mistakes == 1) SelfCorrected++;
        }

        public void RecordReplay() => Replays++;

        /// <summary>
        /// Câu khen theo thứ tự: tự sửa, nghe lại, nghe kĩ (không nhầm lượt nào), còn lại "học chăm".
        /// </summary>
        public (string audio, string text) Praise()
        {
            if (SelfCorrected > 0) return (SystemAudio.khen_tu_sua, UiText.PraiseSelfFix);
            if (Replays > 0) return (SystemAudio.khen_nghe_lai, UiText.PraiseReplay);
            if (Rounds > 0 && Mistakes == 0) return (SystemAudio.khen_nghe_ki, UiText.PraiseAllRight);
            return (SystemAudio.khen_cham, UiText.PraiseHardWork);
        }
    }
}
