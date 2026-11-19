using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Dấu nhận lớp phủ clip (<c>RawImage</c> trên tranh của thẻ). Màn học tìm dấu này để bỏ lớp phủ khỏi bản sao trang
    /// đang lật, để trang lật chỉ còn tranh tĩnh. Lớp phủ đang giữ khung cuối của clip "tiếp" sở hữu
    /// <see cref="HeldFrame"/> và nhả nó khi bị huỷ.
    /// </summary>
    public sealed class ClipOverlay : MonoBehaviour
    {
        /// <summary>Khung cuối đã chép riêng (clip "tiếp"); <c>null</c> khi lớp phủ đang phát.</summary>
        internal RenderTexture HeldFrame;

        private void OnDestroy()
        {
            if (HeldFrame == null) return;
            HeldFrame.Release();
            Destroy(HeldFrame);
            HeldFrame = null;
        }
    }
}
