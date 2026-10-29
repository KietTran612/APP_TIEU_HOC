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

        /// <summary>
        /// Báo một lượt Phần 2 đã xong, kèm số lần bé chọn sai ở lượt đó. Màn lượt gọi ngay trước khi báo
        /// <c>Completed</c>. <c>null</c> khi không ai cần ghi (ví dụ trong test màn).
        /// </summary>
        public Action<Round, int> RoundFinished;
    }
}
