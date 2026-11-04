using System;
using UnityEngine;
using Object = UnityEngine.Object;

namespace TapDoc
{
    /// <summary>
    /// Chỗ duy nhất biết dữ liệu nằm ở thư mục nào (tính từ <c>Resources/</c>) và có kiểu Unity gì. Nơi khác chỉ nói
    /// loại + mã. Khi chuyển sang Addressables, đường dẫn ở đây có thể dùng làm địa chỉ.
    /// </summary>
    public static class ContentPaths
    {
        public static string PathOf(ContentKind kind, string id) => kind switch
        {
            ContentKind.LessonIndex => "lessons/index",
            ContentKind.Lesson => "lessons/" + id,
            ContentKind.Appendix => "appendix/" + id,
            ContentKind.Image => "images/" + id,
            ContentKind.Speech => "audio/" + id,
            ContentKind.Sfx => "sfx/" + id,
            ContentKind.Font => "fonts/" + id,
            ContentKind.Clip => "clips/" + id,
            _ => throw new ArgumentOutOfRangeException(nameof(kind), kind, null),
        };

        public static Type TypeOf(ContentKind kind) => kind switch
        {
            ContentKind.LessonIndex or ContentKind.Lesson or ContentKind.Appendix => typeof(TextAsset),
            ContentKind.Image => typeof(Sprite),
            ContentKind.Speech or ContentKind.Sfx => typeof(AudioClip),
            ContentKind.Font => typeof(Font),
            // Chưa có module video trong project: kiểu cụ thể (VideoClip) gắn khi đưa tranh động vào app.
            ContentKind.Clip => typeof(Object),
            _ => throw new ArgumentOutOfRangeException(nameof(kind), kind, null),
        };
    }
}
