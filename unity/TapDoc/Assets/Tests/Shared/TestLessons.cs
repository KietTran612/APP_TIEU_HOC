namespace TapDoc.Tests
{
    /// <summary>Kho bài đọc dữ liệu thật trong Resources, dùng chung cho các test cần bài thật (giữ bộ nhớ đệm).</summary>
    public static class TestLessons
    {
        private static LessonRepository _real;

        public static LessonRepository Real => _real ??= new LessonRepository(new ResourcesContentSource());
    }
}
