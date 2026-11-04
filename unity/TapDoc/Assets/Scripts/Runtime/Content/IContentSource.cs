using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Tầng dưới của việc đọc dữ liệu: lấy một thứ theo loại + mã. Không có bộ nhớ đệm, không đếm, không ghi log;
    /// thiếu file thì trả <c>null</c>. Đợt này chỉ có <see cref="ResourcesContentSource"/>; sau này thêm bản
    /// Addressables thay vào mà các màn không đổi.
    /// </summary>
    public interface IContentSource
    {
        /// <summary>Nạp có chờ. Kết quả có kiểu <see cref="ContentPaths.TypeOf"/>, hoặc <c>null</c> khi không có file.</summary>
        Awaitable<Object> LoadAsync(ContentKind kind, string id);

        /// <summary>Nạp ngay. Chỉ dùng khi một thứ bị hỏi mà chưa được chuẩn bị trước.</summary>
        Object Load(ContentKind kind, string id);

        /// <summary>Báo nguồn rằng không còn ai giữ <paramref name="asset"/>.</summary>
        void Release(ContentKind kind, string id, Object asset);

        /// <summary>
        /// Dọn những gì không còn ai giữ, gọi sau khi nhả một bộ và màn cũ đã bị huỷ (không gọi giữa lúc bé đang học).
        /// </summary>
        void ReleaseUnused();
    }
}
