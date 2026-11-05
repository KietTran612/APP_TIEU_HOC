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

        // Nút cách đọc ở bước giới thiệu chữ (Phụ lục tr.120–122).
        public const string ReadingLearn = "Đọc khi học";
        public const string ReadingStandard = "Âm chuẩn";
        public const string ReadingLetterName = "Tên chữ cái";
        public const string Why = "Vì sao?";

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

        // Phần Tập đọc (tập 2) trong danh sách bài, nhóm theo tuần; công tắc mở mọi bài của từng bé (màn Phụ huynh).
        public const string PartReading = "Tập đọc";
        public const string WeekFormat = "Tuần {0}";
        public const string UnlockAllOn = "Mở mọi bài: Bật";
        public const string UnlockAllOff = "Mở mọi bài: Tắt";

        // Các màn Tập đọc (tập 2): đọc cả bài, câu hỏi, tìm tiếng, học thuộc lòng.
        public const string ListenAll = "Nghe cả bài";
        public const string AnswerWithParent = "Con trả lời cùng bố mẹ nhé.";
        public const string Answered = "Con trả lời rồi";
        public const string FoundFormat = "Đã tìm {0}/{1}";
        public const string HideMore = "Ẩn bớt";
        public const string ShowAll = "Hiện hết";
        public const string Memorized = "Con thuộc rồi";

        // Popup "Gửi phụ huynh" (hiện một lần sau khởi động; xem lại trong Cài đặt). Sửa nội dung mà muốn mọi máy
        // thấy lại một lần thì tăng NoticeVersion.
        public const int NoticeVersion = 1;
        public const string NoticeTitle = "Gửi phụ huynh";
        public const string NoticeAccept = "Đã hiểu";
        public const string BootError = "Không mở được dữ liệu của ứng dụng. Hãy cài lại ứng dụng.";
        public const string NoticeBody = "<b>Lưu ý về ứng dụng</b>\n1. Ứng dụng chỉ mang tính chất tham khảo, hỗ trợ bé tập đọc; không thay thế việc học ở trường và hướng dẫn của thầy cô.\n2. Ứng dụng tham khảo cách dạy tập đọc từ các sách giáo khoa cũ, không dựa hoàn toàn vào một nguồn sách nào, và không liên kết với nhà xuất bản hay cơ quan quản lý giáo dục nào.\n3. Ứng dụng không chứa và không cổ xúy bất kỳ hành vi vi phạm pháp luật nào.\n4. Hình ảnh trong ứng dụng được vẽ để minh họa học tập, không liên quan đến bất kỳ cá nhân, tổ chức nào và có thể không giống thực tế.\n5. Âm thanh và cách phát âm trong ứng dụng có thể chưa chuẩn. Nếu thấy chưa chuẩn, phụ huynh hãy đọc lại hoặc phát âm lại cho bé.\n\n<b>Dữ liệu của bé</b>\nTên gọi, hình đại diện và tiến độ học của bé chỉ được lưu trên máy này; ứng dụng không gửi các thông tin này đi đâu. Xin chỉ nhập tên gọi ở nhà của bé. Phụ huynh có thể đổi hoặc xoá hồ sơ của bé trong phần Cài đặt.\n\n<b>Lời khuyên</b>\nPhụ huynh nên ngồi cùng bé khi học, mỗi lần học ngắn, để âm lượng vừa phải và giữ khoảng cách mắt với màn hình.";

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
            ReadingLearn,
            ReadingStandard,
            ReadingLetterName,
            Why,
            Book,
            BookTitleFormat,
            BookPageFormat,
            StampText,
            MascotCorrect,
            MascotLessonDone,
            SfxOn,
            SfxOff,
            PartReading,
            WeekFormat,
            UnlockAllOn,
            UnlockAllOff,
            ListenAll,
            AnswerWithParent,
            Answered,
            FoundFormat,
            HideMore,
            ShowAll,
            Memorized,
            NoticeTitle,
            NoticeAccept,
            NoticeBody,
            BootError,
        };
    }
}
