using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Hàng chấm tiến độ trên đầu màn học (bản thiết kế giao diện mục 4.3): mỗi bước của bài một chấm; bước đã qua tô lam
    /// ngọc, bước đang làm tô cam, bước chưa tới để trống. Bài quá nhiều bước (hàng chấm dài hơn <see cref="MaxWidth"/>)
    /// thì thành thanh tiến độ liền. Chỉ để xem, không bấm được.
    /// </summary>
    public class ProgressDots : MonoBehaviour
    {
        public const float Dot = 26f;
        public const float Gap = 12f;
        public const float MaxWidth = 880f;
        private const float BarHeight = 22f;

        private readonly List<Image> _dots = new();
        private Image _barFill;

        public int Total { get; private set; }
        public int Current { get; private set; }
        public bool IsBar { get; private set; }

        public static ProgressDots Create(Transform parent, int total)
        {
            var go = new GameObject("ProgressDots", typeof(RectTransform), typeof(ProgressDots));
            go.transform.SetParent(parent, false);
            var dots = go.GetComponent<ProgressDots>();
            dots.Build(Mathf.Max(0, total));
            return dots;
        }

        private void Build(int total)
        {
            Total = total;
            var rowWidth = total * (Dot + Gap) - Gap;
            IsBar = rowWidth > MaxWidth;
            var rt = (RectTransform)transform;
            if (IsBar)
            {
                rt.sizeDelta = new Vector2(MaxWidth, BarHeight);
                var border = Shape(transform, "Bar", UiShapes.Rounded, Palette.Ink, 0f);
                border.type = Image.Type.Sliced;
                var paper = Shape(border.transform, "Paper", UiShapes.Rounded, Palette.PaperLight, UiKit.BorderWidth);
                paper.type = Image.Type.Sliced;
                _barFill = Shape(border.transform, "Fill", UiKit.WhiteSprite, Palette.Teal, UiKit.BorderWidth);
                _barFill.type = Image.Type.Filled;
                _barFill.fillMethod = Image.FillMethod.Horizontal;
            }
            else
            {
                rt.sizeDelta = new Vector2(Mathf.Max(rowWidth, 0f), Dot);
                for (var i = 0; i < total; i++)
                {
                    var ring = Shape(transform, $"Dot_{i}", UiShapes.Circle, Palette.Ink, 0f);
                    var drt = (RectTransform)ring.transform;
                    drt.anchorMin = drt.anchorMax = new Vector2(0f, .5f);
                    drt.pivot = new Vector2(0f, .5f);
                    drt.sizeDelta = new Vector2(Dot, Dot);
                    drt.anchoredPosition = new Vector2(i * (Dot + Gap), 0f);
                    _dots.Add(Shape(ring.transform, "Fill", UiShapes.Circle, Palette.PaperLight, UiKit.BorderWidth));
                }
            }
            SetCurrent(0);
        }

        private static Image Shape(Transform parent, string name, Sprite sprite, Color color, float inset)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(Image));
            go.transform.SetParent(parent, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = new Vector2(inset, inset);
            rt.offsetMax = new Vector2(-inset, -inset);
            var img = go.GetComponent<Image>();
            img.sprite = sprite;
            img.color = color;
            img.raycastTarget = false;
            return img;
        }

        /// <summary>Đánh dấu bước <paramref name="index"/> (tính từ 0) là bước đang làm.</summary>
        public void SetCurrent(int index)
        {
            Current = index;
            if (IsBar)
            {
                _barFill.fillAmount = Total > 0 ? Mathf.Clamp01((index + 1f) / Total) : 0f;
                return;
            }
            for (var i = 0; i < _dots.Count; i++)
            {
                _dots[i].color = i < index ? Palette.Teal : i == index ? Palette.Orange : Palette.PaperLight;
            }
        }
    }
}
