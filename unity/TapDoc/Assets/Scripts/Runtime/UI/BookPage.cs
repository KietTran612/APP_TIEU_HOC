using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Một trang của Sổ bé ngoan, ứng với một bài: đầu trang ghi "Bài N · tên bài", phía trên là
    /// <see cref="FlowerBook.FlowersPerLesson"/> ô hoa, phía dưới (<see cref="Content"/>) là tem bài học: tranh của bài
    /// dán nghiêng trên giấy trắng, chữ dưới tranh (bản thiết kế nâng cấp UI mục 4.3). Bài chưa học có khung tem trống
    /// nhạt. Tem nạp nền (dữ liệu bài và tranh) để lật sổ không phải chờ.
    /// </summary>
    public class BookPage : MonoBehaviour
    {
        public const float SlotSize = 180f;

        /// <summary>Dòng đầu trang Sổ bé ngoan: nhãn bài như trên thẻ ("Bài 1", "Chính tả") và tên bài.</summary>
        internal static string HeaderText(LessonEntry entry) =>
            string.Format(UiText.BookPageFormat, LessonListScreen.LabelOf(entry), entry.title);
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

        public const float StickerSize = 250f;
        private const float StickerTilt = -4f;

        /// <summary>Tem bài học (bài đã học); <c>null</c> khi bài chưa học hay trang trống.</summary>
        public RectTransform Sticker { get; private set; }

        /// <summary>Khung tem trống nhạt của bài chưa học.</summary>
        public RectTransform StickerSlot { get; private set; }

        public bool StickerVisible => Sticker != null && Sticker.gameObject.activeSelf;

        /// <summary>Tem đã nạp xong (tranh hoặc chữ).</summary>
        public bool StickerLoaded { get; private set; }

        public string StickerImageId { get; private set; }
        public string StickerCaption { get; private set; }

        private Image _stickerPicture;
        private TMP_Text _stickerCaption;
        private ContentSet _stickerSet;
        private LessonEntry _entry;

        /// <summary>Dựng trang phủ kín <paramref name="parent"/>. <paramref name="entry"/> <c>null</c> là trang trống.</summary>
        public static BookPage Create(RectTransform parent, LessonEntry entry, int flowers, AssetCatalog assets,
            LessonRepository lessons = null)
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
            if (entry != null) page.BuildSticker(entry, lessons);
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

            var header = UiKit.CreateLabel(transform, HeaderText(entry), 40f);
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

        private void BuildSticker(LessonEntry entry, LessonRepository lessons)
        {
            _entry = entry;
            if (FlowerCount <= 0)
            {
                // Bài chưa học: khung tem trống nhạt, hé lộ chỗ dán tem.
                var slot = new GameObject("StickerSlot", typeof(RectTransform), typeof(Image));
                slot.transform.SetParent(Content, false);
                StickerSlot = (RectTransform)slot.transform;
                Center(StickerSlot);
                var img = slot.GetComponent<Image>();
                UiKit.SetRounded(img, new Color(Palette.LockedInk.r, Palette.LockedInk.g, Palette.LockedInk.b, .55f));
                img.raycastTarget = false;
                UiKit.AddFill(slot.transform, UiShapes.Rounded, Palette.PaperLight);
                return;
            }

            var go = new GameObject("Sticker", typeof(RectTransform), typeof(Image));
            go.transform.SetParent(Content, false);
            Sticker = (RectTransform)go.transform;
            Center(Sticker);
            Sticker.localRotation = Quaternion.Euler(0f, 0f, StickerTilt);
            var border = go.GetComponent<Image>();
            UiKit.SetRounded(border, Palette.Ink);
            border.raycastTarget = false;
            UiKit.AddFill(go.transform, UiShapes.Rounded, Color.white);

            var picGo = new GameObject("Picture", typeof(RectTransform), typeof(Image));
            picGo.transform.SetParent(go.transform, false);
            var prt = (RectTransform)picGo.transform;
            prt.anchorMin = new Vector2(.07f, .26f);
            prt.anchorMax = new Vector2(.93f, .93f);
            prt.offsetMin = prt.offsetMax = Vector2.zero;
            _stickerPicture = picGo.GetComponent<Image>();
            _stickerPicture.preserveAspect = true;
            _stickerPicture.raycastTarget = false;
            _stickerPicture.enabled = false;

            _stickerCaption = UiKit.CreateLabel(go.transform, entry.title ?? string.Empty, 40f);
            _stickerCaption.name = "Caption";
            _stickerCaption.raycastTarget = false;
            var crt = _stickerCaption.rectTransform;
            crt.anchorMin = new Vector2(.05f, .03f);
            crt.anchorMax = new Vector2(.95f, .26f);
            crt.offsetMin = crt.offsetMax = Vector2.zero;

            // Băng dính giấy ở mép trên.
            var tape = new GameObject("Tape", typeof(RectTransform), typeof(Image));
            tape.transform.SetParent(go.transform, false);
            var trt = (RectTransform)tape.transform;
            trt.anchorMin = trt.anchorMax = new Vector2(.5f, 1f);
            trt.sizeDelta = new Vector2(90f, 28f);
            trt.localRotation = Quaternion.Euler(0f, 0f, 6f);
            var timg = tape.GetComponent<Image>();
            timg.sprite = UiKit.WhiteSprite;
            timg.color = new Color(Palette.OrangeLight.r, Palette.OrangeLight.g, Palette.OrangeLight.b, .85f);
            timg.raycastTarget = false;

            StickerCaption = entry.title;
            if (lessons != null) LoadSticker(lessons);
            else ShowText(entry.title);
        }

        private void Center(RectTransform rt)
        {
            rt.anchorMin = rt.anchorMax = new Vector2(.5f, .5f);
            var side = Mathf.Min(StickerSize, Content.rect.height > 1f ? Content.rect.height - 8f : StickerSize);
            rt.sizeDelta = new Vector2(side, side);
            rt.anchoredPosition = Vector2.zero;
        }

        /// <summary>Hiện hay ẩn tem (màn Xong bài dán tem vào lúc cảnh xong).</summary>
        public void SetStickerVisible(bool visible)
        {
            if (Sticker != null) Sticker.gameObject.SetActive(visible);
        }

        /// <summary>Nạp nền dữ liệu bài và tranh của tem; trang bị huỷ giữa chừng thì thôi.</summary>
        private async void LoadSticker(LessonRepository lessons)
        {
            Lesson lesson;
            try
            {
                lesson = await lessons.LoadAsync(_entry.lesson_id);
            }
            catch (System.IO.InvalidDataException)
            {
                lesson = null;
            }
            if (this == null) return;
            var (image, caption) = LessonSticker.For(lesson, _entry.title);
            StickerCaption = caption;
            if (string.IsNullOrEmpty(image) || _assets == null)
            {
                ShowText(caption);
                return;
            }
            var set = await _assets.PrepareAsync(new[] { (ContentKind.Image, image) });
            if (this == null)
            {
                set.Dispose();
                return;
            }
            _stickerSet = set;
            var sprite = _assets.Image(image);
            if (sprite == null)
            {
                ShowText(caption);
                return;
            }
            StickerImageId = image;
            _stickerPicture.sprite = sprite;
            _stickerPicture.enabled = true;
            _stickerCaption.text = caption;
            StickerLoaded = true;
        }

        /// <summary>Bài không có tranh: tem là chữ viết to (tên bài), tự co, tối đa hai dòng.</summary>
        private void ShowText(string text)
        {
            _stickerPicture.enabled = false;
            var crt = _stickerCaption.rectTransform;
            crt.anchorMin = new Vector2(.08f, .1f);
            crt.anchorMax = new Vector2(.92f, .9f);
            _stickerCaption.text = text ?? string.Empty;
            _stickerCaption.fontSizeMax = 64f;
            StickerLoaded = true;
        }

        private void OnDestroy()
        {
            _stickerSet?.Dispose();
            _stickerSet = null;
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
