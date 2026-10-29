using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Xếp các thẻ thành dòng, tự xuống dòng khi dòng dài hơn bề rộng cho phép. Giữ thứ tự đọc: trái sang phải,
    /// trên xuống dưới. Mỗi dòng căn giữa; cả khối căn giữa theo chiều dọc quanh (0, 0).
    /// </summary>
    public static class FlowLayout
    {
        /// <summary>
        /// Chia chỉ số các thẻ thành dòng (tham lam: thêm thẻ vào dòng đang xếp khi còn vừa). Thẻ rộng hơn
        /// <paramref name="maxWidth"/> đứng một mình một dòng.
        /// </summary>
        public static List<List<int>> Lines(IReadOnlyList<float> widths, float maxWidth, float gap)
        {
            var lines = new List<List<int>>();
            var current = new List<int>();
            var used = 0f;
            for (var i = 0; i < widths.Count; i++)
            {
                var need = current.Count == 0 ? widths[i] : used + gap + widths[i];
                if (current.Count > 0 && need > maxWidth)
                {
                    lines.Add(current);
                    current = new List<int>();
                    need = widths[i];
                }
                current.Add(i);
                used = need;
            }
            if (current.Count > 0) lines.Add(current);
            return lines;
        }

        /// <summary>Tâm của từng thẻ (cùng thứ tự với <paramref name="widths"/>), mọi thẻ cao <paramref name="height"/>.</summary>
        public static List<Vector2> Place(IReadOnlyList<float> widths, float height, float maxWidth, float gap, float lineGap)
        {
            var centers = new Vector2[widths.Count];
            var lines = Lines(widths, maxWidth, gap);
            var blockHeight = lines.Count * height + (lines.Count - 1) * lineGap;
            var y = blockHeight / 2f - height / 2f;
            foreach (var line in lines)
            {
                var lineWidth = line.Sum(i => widths[i]) + (line.Count - 1) * gap;
                var x = -lineWidth / 2f;
                foreach (var i in line)
                {
                    centers[i] = new Vector2(x + widths[i] / 2f, y);
                    x += widths[i] + gap;
                }
                y -= height + lineGap;
            }
            return centers.ToList();
        }
    }
}
