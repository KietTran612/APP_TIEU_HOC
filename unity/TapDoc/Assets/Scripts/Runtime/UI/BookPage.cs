using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Một trang của Sổ bé ngoan, ứng với một bài: đầu trang ghi "Bài N · tên bài", phía trên là
    /// <see cref="FlowerBook.FlowersPerLesson"/> ô hoa, phía dưới là vùng nội dung (<see cref="Content"/>) để trống cho
    /// nội dung sau này (bản thiết kế giao diện mục 8.3).
    /// </summary>
    public class BookPage : MonoBehaviour
    {
        public const float SlotSize = 180f;
        private const float SlotGap = 24f;
        private const float Padding = 28f;
        private const float HeaderHeight = 70f;

        private readonly List<Tile> _slots = new();
        private AssetCatalog _assets;

        /// <summary>Mã bài của trang; <c>null</c> với trang trống (bài cuối lẻ).</summary>
        public string LessonId { get; private set; }

        public IReadOnlyList<Tile> Slots => _slots;

        /// <summary>Vùng phía dưới trang, hiện để trống.</summary>
        public RectTransform Content { get; private set; }

        public int FlowerCount { get; private set; }

        /// <summary>Dựng trang phủ kín <paramref name="parent"/>. <paramref name="entry"/> <c>null</c> là trang trống.</summary>
        public static BookPage Create(RectTransform parent, LessonEntry entry, int flowers, AssetCatalog assets)
        {
            var go = new GameObject("BookPage", typeof(RectTransform), typeof(BookPage));
            go.transform.SetParent(parent, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            var page = go.GetComponent<BookPage>();
            page._assets = assets;
            page.Build(entry, flowers);
            return page;
        }

        private void Build(LessonEntry entry, int flowers)
        {
            LessonId = entry?.lesson_id;

            var contentGo = new GameObject("PageContent", typeof(RectTransform));
            contentGo.transform.SetParent(transform, false);
            Content = (RectTransform)contentGo.transform;
            Content.anchorMin = Vector2.zero;
            Content.anchorMax = Vector2.one;
            Content.offsetMin = new Vector2(Padding, Padding);
            Content.offsetMax = new Vector2(-Padding, -(Padding + HeaderHeight + SlotSize + SlotGap));

            if (entry == null) return;

            var header = UiKit.CreateLabel(transform, string.Format(UiText.BookPageFormat, UiText.LessonPrefix,
                entry.lesson_no, entry.title), 40f);
            header.alignment = TextAlignmentOptions.Left;
            header.textWrappingMode = TextWrappingModes.NoWrap;
            var hrt = header.rectTransform;
            hrt.anchorMin = new Vector2(0f, 1f);
            hrt.anchorMax = new Vector2(1f, 1f);
            hrt.pivot = new Vector2(.5f, 1f);
            hrt.offsetMin = new Vector2(Padding, -(Padding + HeaderHeight));
            hrt.offsetMax = new Vector2(-Padding, -Padding);

            var count = FlowerBook.FlowersPerLesson;
            var rowWidth = count * SlotSize + (count - 1) * SlotGap;
            for (var i = 0; i < count; i++)
            {
                var slot = UiKit.CreateTile(transform, string.Empty);
                slot.name = $"FlowerSlot_{i}";
                var srt = (RectTransform)slot.transform;
                srt.anchorMin = srt.anchorMax = new Vector2(.5f, 1f);
                srt.pivot = new Vector2(.5f, 1f);
                srt.sizeDelta = new Vector2(SlotSize, SlotSize);
                srt.anchoredPosition = new Vector2(-rowWidth / 2f + SlotSize / 2f + i * (SlotSize + SlotGap),
                    -(Padding + HeaderHeight));
                var box = (RectTransform)slot.ImageBox.transform;
                box.anchorMin = new Vector2(.12f, .12f);
                box.anchorMax = new Vector2(.88f, .88f);
                slot.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;
                var target = srt;
                slot.Tapped += () => _ = Motion.Punch(target, 1.08f, .2f);
                _slots.Add(slot);
            }
            SetFlowers(flowers);
        }

        /// <summary>
        /// Hiện <paramref name="count"/> bông hoa ở các ô đầu: ô có hoa viền lam ngọc và có hình hoa; ô trống viền lam
        /// ngọc nhạt, không có hình.
        /// </summary>
        public void SetFlowers(int count)
        {
            FlowerCount = Mathf.Clamp(count, 0, _slots.Count);
            for (var i = 0; i < _slots.Count; i++)
            {
                var slot = _slots[i];
                var has = i < FlowerCount;
                slot.GetComponent<Image>().color = has ? Palette.Teal : Palette.TealLight;
                var imageId = FlowerBook.FlowerImage(LessonId, i);
                // Ô trống không nạp hình; ô có hoa mà thiếu file thì catalog báo lỗi và ô để trống.
                slot.SetSprite(has ? _assets?.Image(imageId) : null, imageId);
            }
        }
    }
}
