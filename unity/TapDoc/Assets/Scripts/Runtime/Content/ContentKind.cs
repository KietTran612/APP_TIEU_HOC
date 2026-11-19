namespace TapDoc
{
    /// <summary>Loại dữ liệu app đọc. Mỗi loại ứng với một thư mục và một kiểu Unity (<see cref="ContentPaths"/>).</summary>
    public enum ContentKind
    {
        /// <summary>Danh sách bài (<c>lessons/index</c>).</summary>
        LessonIndex,
        Lesson,

        /// <summary>Phụ lục cuối sách, theo mã sách.</summary>
        Appendix,
        Image,

        /// <summary>Âm thanh phát âm (giọng đọc), tách khỏi <see cref="Sfx"/>.</summary>
        Speech,

        /// <summary>Tiếng động khi tương tác (<c>sfx_*</c>).</summary>
        Sfx,
        Font,

        /// <summary>
        /// Tranh động (clip) theo mã tranh. Không bắt buộc: tranh không có clip phát được thì app dùng tranh tĩnh.
        /// </summary>
        Clip,
    }
}
