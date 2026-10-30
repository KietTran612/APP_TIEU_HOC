namespace TapDoc
{
    public static class UiText
    {
        public const string Back = "Về";
        public const string Replay = "Nghe lại";
        public const string Next = "Tiếp";
        public const string PagePrev = "Trang trước";
        public const string PageNext = "Trang sau";
        public const string ListenSentence = "Nghe cả câu";
        public const string DoneReading = "Con đọc xong rồi";
        public const string NextLesson = "Học bài tiếp";
        public const string ToList = "Về danh sách";
        public const string LessonPrefix = "Bài";
        public const string PartLetters = "Chữ cái và âm";
        public const string PartRimes = "Vần";
        public const string Praise = "Giỏi lắm!";
        public const string AppTitle = "Tập đọc lớp 1";
        public const string ReviewMistakes = "Ôn lại";
        public const string Parent = "Phụ huynh";
        public const string SwitchChild = "Đổi bé";
        public const string NewChild = "Bé mới";
        public const string AddChild = "+ " + NewChild;
        public const string Done = "Xong";
        public const string NamePrompt = "Tên ở nhà của bé";
        public const string ParentGatePrompt = "Phụ huynh chọn đáp án đúng";

        /// <summary>Dòng tiến độ ở màn phụ huynh: {0} bài đã học trên {1} bài trong danh sách.</summary>
        public const string LearnedFormat = "Đã học {0}/{1} bài";

        public const string OftenConfused = "Chữ hay nhầm:";
        public const string NoConfusion = "Chưa có";
        public const string BookAppendix = "Chú ý và Phụ lục";

        /// <summary>Tiêu đề một mục trong Phụ lục: {0} tên mục, {1} số trang trong sách.</summary>
        public const string PageFormat = "{0} (tr.{1})";

        // Khung ghi chú trong bài: nút mở, tiêu đề từng loại ghi chú, nút đóng.
        public const string Notes = "Ghi chú";
        public const string NoteKindBook = "Sách ghi";
        public const string NoteKindReading = "Cách đọc theo sách";
        public const string NoteKindApp = "App khác sách";
        public const string Close = "Đóng";

        // Sổ bé ngoan: nút mở sổ, tiêu đề sổ ({0} tên bé), đầu trang ({0} "Bài", {1} số bài, {2} tên bài), con dấu.
        public const string Book = "Sổ bé ngoan";
        public const string BookTitleFormat = "Sổ bé ngoan của {0}";
        public const string BookPageFormat = "{0} {1} · {2}";
        public const string StampText = "BÉ NGOAN";

        // Bong bóng của bạn gà con.
        public const string MascotCorrect = "Đúng rồi!";
        public const string MascotLessonDone = "Bé ngoan quá!";

        // Công tắc tiếng động ở màn phụ huynh.
        public const string SfxOn = "Tiếng động: Bật";
        public const string SfxOff = "Tiếng động: Tắt";

        public static readonly string[] All =
        {
            Back,
            Replay,
            Next,
            PagePrev,
            PageNext,
            ListenSentence,
            DoneReading,
            NextLesson,
            ToList,
            LessonPrefix,
            PartLetters,
            PartRimes,
            Praise,
            AppTitle,
            ReviewMistakes,
            Parent,
            SwitchChild,
            NewChild,
            AddChild,
            Done,
            NamePrompt,
            ParentGatePrompt,
            LearnedFormat,
            OftenConfused,
            NoConfusion,
            BookAppendix,
            PageFormat,
            Notes,
            NoteKindBook,
            NoteKindReading,
            NoteKindApp,
            Close,
            Book,
            BookTitleFormat,
            BookPageFormat,
            StampText,
            MascotCorrect,
            MascotLessonDone,
            SfxOn,
            SfxOff,
        };
    }
}
