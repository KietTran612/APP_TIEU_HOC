using System;
using System.Collections.Generic;

namespace TapDoc
{
    /// <summary>Nội dung file tiến độ (JsonUtility). Một máy có nhiều hồ sơ bé; <c>current</c> là mã bé đang học.</summary>
    [Serializable]
    public class ProgressFile
    {
        public int schema = 1;
        public List<Profile> profiles = new();
        public string current;

        /// <summary>
        /// Phụ huynh tắt tiếng động (cài đặt cho cả máy, không theo từng bé). File cũ không có trường này thì
        /// đọc ra <c>false</c>, tức là tiếng động bật.
        /// </summary>
        public bool sfx_off;
    }

    /// <summary>
    /// Hồ sơ một bé: chỉ có tên gọi ở nhà và hình đại diện bé chọn, không lưu thông tin định danh nào khác.
    /// </summary>
    [Serializable]
    public class Profile
    {
        public string id;
        public string name;
        public string avatar;
        public List<LessonProgress> lessons = new();
        public List<Mistake> mistakes = new();
    }

    [Serializable]
    public class LessonProgress
    {
        public string lesson_id;
        public bool completed;
        public int stars;
    }

    /// <summary>Một lượt Phần 2 bé đã nhầm: <c>round</c> là chỉ số trong <c>part2</c> của bài.</summary>
    [Serializable]
    public class Mistake
    {
        public string lesson_id;
        public int round;
        public int count;
        public long last_ticks;
    }
}
