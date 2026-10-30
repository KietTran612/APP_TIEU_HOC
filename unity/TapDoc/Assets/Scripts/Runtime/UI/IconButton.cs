using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Đánh dấu một nút của bé: nút tròn có biểu tượng, không có chữ. <see cref="Label"/> là chữ của nút theo
    /// <see cref="UiText"/> (cũng nằm trong tên GameObject <c>Button_&lt;nhãn&gt;</c>), để test và người đọc code biết
    /// nút làm gì.
    /// </summary>
    public class IconButton : MonoBehaviour
    {
        public string IconId { get; internal set; }
        public string Label { get; internal set; }
    }
}
