using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Con đường bài học trên đầu màn học (bản thiết kế nâng cấp UI mục 4.1.1): mỗi bước một hạt xếp lượn nhẹ, nối bằng
    /// nét mực mảnh; bước đã qua tô lam ngọc, bước đang làm là hạt cam to hơn nhún nhẹ, bước chưa tới để trống. Cuối đường
    /// là bông hoa của Sổ bé ngoan. Bài quá nhiều bước (đường dài hơn <see cref="MaxWidth"/>) thì thành đường liền có dấu
    /// cam ở chỗ đang học. Chỉ để xem, không bấm được; không có gà con trên đường (màn học chỉ một gà con).
    /// </summary>
    public class ProgressDots : MonoBehaviour
    {
        public const float Dot = 32f;
        public const float Gap = 7f;
        public const float CurrentDot = 48f;
        public const float Flower = 40f;
        public const float MaxWidth = 820f;
        public const float WaveAmplitude = 6f;
        private const float BarHeight = 28f;
        private const float LineWidth = 3f;

        private readonly List<RectTransform> _rings = new();
        private readonly List<Image> _fills = new();
        private Image _barFill;
        private RectTransform _barMarker;
        private float _barWidth;

        public int Total { get; private set; }
        public int Current { get; private set; }
        public bool IsBar { get; private set; }

        /// <summary>Bông hoa cuối đường.</summary>
        public Image Goal { get; private set; }

        /// <summary>Hạt của bước đang làm (hoặc dấu cam trên đường liền).</summary>
        public RectTransform CurrentMarker => IsBar
            ? _barMarker
            : Current >= 0 && Current < _rings.Count ? _rings[Current] : null;

        public static ProgressDots Create(Transform parent, int total, AssetCatalog assets = null)
        {
            var go = new GameObject("ProgressDots", typeof(RectTransform), typeof(ProgressDots));
            go.transform.SetParent(parent, false);
            var dots = go.GetComponent<ProgressDots>();
            dots.Build(Mathf.Max(0, total), assets);
            return dots;
        }

        /// <summary>Toạ độ tâm hạt <paramref name="i"/> tính từ mép trái đường, theo đường lượn.</summary>
        private static Vector2 BeadCenter(int i) =>
            new(i * (Dot + Gap) + Dot / 2f, WaveAmplitude * Mathf.Sin(i * .9f));

        private void Build(int total, AssetCatalog assets)
        {
            Total = total;
            var rowWidth = total * (Dot + Gap) + Flower;
            IsBar = rowWidth > MaxWidth;
            var rt = (RectTransform)transform;
            rt.sizeDelta = new Vector2(IsBar ? MaxWidth : rowWidth, CurrentDot + 2f * WaveAmplitude);
            if (IsBar)
            {
                _barWidth = MaxWidth - Flower - Gap;
                var border = Shape(transform, "Bar", UiShapes.Rounded, Palette.Ink, 0f);
                border.type = Image.Type.Sliced;
                Place(border.rectTransform, new Vector2(_barWidth / 2f, 0f), new Vector2(_barWidth, BarHeight));
                var paper = Shape(border.transform, "Paper", UiShapes.Rounded, Palette.PaperLight, UiKit.BorderWidth);
                paper.type = Image.Type.Sliced;
                _barFill = Shape(border.transform, "Fill", UiKit.WhiteSprite, Palette.Teal, UiKit.BorderWidth);
                _barFill.type = Image.Type.Filled;
                _barFill.fillMethod = Image.FillMethod.Horizontal;
                var marker = Shape(transform, "Marker", UiShapes.Circle, Palette.Ink, 0f);
                _barMarker = marker.rectTransform;
                Place(_barMarker, Vector2.zero, new Vector2(CurrentDot, CurrentDot));
                Shape(marker.transform, "Fill", UiShapes.Circle, Palette.Orange, UiKit.BorderWidth);
                AddGoal(assets, new Vector2(_barWidth + Gap + Flower / 2f, 0f));
            }
            else
            {
                for (var i = 0; i + 1 < total; i++) AddLine(BeadCenter(i), BeadCenter(i + 1));
                if (total > 0) AddLine(BeadCenter(total - 1), new Vector2(total * (Dot + Gap) + Flower / 2f, 0f));
                for (var i = 0; i < total; i++)
                {
                    var ring = Shape(transform, $"Dot_{i}", UiShapes.Circle, Palette.Ink, 0f);
                    Place(ring.rectTransform, BeadCenter(i), new Vector2(Dot, Dot));
                    _rings.Add(ring.rectTransform);
                    _fills.Add(Shape(ring.transform, "Fill", UiShapes.Circle, Palette.PaperLight, UiKit.BorderWidth));
                }
                AddGoal(assets, new Vector2(total * (Dot + Gap) + Flower / 2f, WaveAmplitude * Mathf.Sin(total * .9f)));
            }
            Current = -1;
            SetCurrent(0);
        }

        private void AddGoal(AssetCatalog assets, Vector2 center)
        {
            var sprite = assets?.Image(SystemImages.Flower);
            Goal = Shape(transform, "Goal", sprite != null ? sprite : UiShapes.Circle,
                sprite != null ? Color.white : Palette.HintYellow, 0f);
            Goal.preserveAspect = true;
            Place(Goal.rectTransform, center, new Vector2(Flower, Flower));
        }

        /// <summary>Nét mực mảnh nối hai tâm (nằm dưới các hạt).</summary>
        private void AddLine(Vector2 from, Vector2 to)
        {
            var line = Shape(transform, "Line", UiKit.WhiteSprite, Palette.Ink, 0f);
            var lrt = line.rectTransform;
            var d = to - from;
            Place(lrt, (from + to) / 2f, new Vector2(d.magnitude, LineWidth));
            lrt.localRotation = Quaternion.Euler(0f, 0f, Mathf.Atan2(d.y, d.x) * Mathf.Rad2Deg);
        }

        /// <summary>Đặt tâm <paramref name="rt"/> tại <paramref name="center"/> tính từ mép trái giữa của đường.</summary>
        private static void Place(RectTransform rt, Vector2 center, Vector2 size)
        {
            rt.anchorMin = rt.anchorMax = new Vector2(0f, .5f);
            rt.pivot = new Vector2(.5f, .5f);
            rt.sizeDelta = size;
            rt.anchoredPosition = center;
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
            if (IsBar)
            {
                Current = index;
                var amount = Total > 0 ? Mathf.Clamp01((index + 1f) / Total) : 0f;
                _barFill.fillAmount = amount;
                _barMarker.anchoredPosition = new Vector2(_barWidth * amount, 0f);
                Pulse.StartOn(_barMarker, .08f, 1.2f);
                return;
            }
            if (Current >= 0 && Current < _rings.Count) Pulse.StopOn(_rings[Current]);
            Current = index;
            for (var i = 0; i < _rings.Count; i++)
            {
                var size = i == index ? CurrentDot : Dot;
                _rings[i].sizeDelta = new Vector2(size, size);
                _fills[i].color = i < index ? Palette.Teal : i == index ? Palette.Orange : Palette.PaperLight;
            }
            if (index >= 0 && index < _rings.Count)
            {
                _rings[index].SetAsLastSibling(); // hạt to nằm trên nét nối và hạt bên cạnh
                Pulse.StartOn(_rings[index], .08f, 1.2f);
            }
        }
    }
}
