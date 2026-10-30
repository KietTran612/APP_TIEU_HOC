using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Hình kí hiệu của sách (● Em đọc, ⌂ Luyện tập) đặt ở đầu mục; không bấm được. <see cref="ImageId"/> là mã tranh
    /// của kí hiệu, để test kiểm tra đúng kí hiệu.
    /// </summary>
    public class MarkerIcon : MonoBehaviour
    {
        internal string ImageId { get; set; }
    }
}
