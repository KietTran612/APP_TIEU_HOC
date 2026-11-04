using System.Linq;

namespace TapDoc.Tests
{
    /// <summary>
    /// Kho bài đọc dữ liệu thật trong Resources, dùng chung cho các test cần bài thật. Nạp sẵn danh sách bài, mọi bài
    /// và Phụ lục ngay lần đầu dùng, như app chuẩn bị trước, nên đọc sau đó không có cảnh báo "chưa chuẩn bị trước".
    /// </summary>
    public static class TestLessons
    {
        private static LessonRepository _real;

        public static LessonRepository Real
        {
            get
            {
                if (_real != null) return _real;
                var resources = new ResourcesContentSource();
                // Nguồn giả không chậm: các lời nạp có chờ xong ngay, dùng được cả trong test EditMode.
                var repo = new LessonRepository(new FakeContentSource { Fallback = resources.Load });
                AwaitableTestUtil.RunNow(repo.LoadAllAsync());
                foreach (var book in repo.Index.lessons.Select(e => e.book).Distinct())
                {
                    AwaitableTestUtil.RunNow(repo.LoadAppendixAsync(book));
                }
                return _real = repo;
            }
        }
    }
}
