using System;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Báo khi cỡ của một màn đổi thật sự (xoay máy, đổi cỡ cửa sổ), để màn tự chỉnh tại chỗ thay vì dựng lại.
    /// </summary>
    public class FrameWatcher : MonoBehaviour
    {
        /// <summary>Cỡ đổi quá 0,5 đơn vị canvas; tham số là cỡ mới.</summary>
        public event Action<Vector2> Changed;

        /// <summary>Cỡ đã báo gần nhất.</summary>
        public Vector2 Size { get; private set; }

        /// <summary>Lấy (hoặc thêm) bộ báo trên <paramref name="go"/>; ghi nhận cỡ hiện tại làm mốc.</summary>
        public static FrameWatcher On(GameObject go)
        {
            var watcher = go.GetComponent<FrameWatcher>();
            if (watcher == null)
            {
                watcher = go.AddComponent<FrameWatcher>();
                watcher.Size = ((RectTransform)go.transform).rect.size;
            }
            return watcher;
        }

        private void OnRectTransformDimensionsChange()
        {
            var size = ((RectTransform)transform).rect.size;
            if (Mathf.Abs(size.x - Size.x) <= .5f && Mathf.Abs(size.y - Size.y) <= .5f) return;
            Size = size;
            Changed?.Invoke(size);
        }
    }
}
