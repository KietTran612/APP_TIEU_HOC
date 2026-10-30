using System;
using UnityEngine;

namespace TapDoc
{
    public class LessonContext
    {
        public Lesson Lesson;
        public SpeechPlayer Speech;
        public AssetCatalog Assets;
        public RectTransform Stage;

        /// <summary>Hiệu ứng phản hồi (sao giấy, gà con, tiếng động); <c>null</c> trong test màn không có khung bài.</summary>
        public LessonFx Fx;

        /// <summary>
        /// Báo một lượt Phần 2 đã xong, kèm số lần bé chọn sai ở lượt đó. Màn lượt gọi ngay trước khi báo
        /// <c>Completed</c>. <c>null</c> khi không ai cần ghi (ví dụ trong test màn).
        /// </summary>
        public Action<Round, int> RoundFinished;
    }
}
