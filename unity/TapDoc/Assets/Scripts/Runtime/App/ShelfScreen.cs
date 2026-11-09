using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>Trạng thái một quyển trên kệ.</summary>
    public enum ShelfBookState
    {
        /// <summary>Chưa mở: bìa mờ, ổ khoá, chạm thì lắc.</summary>
        Locked,

        /// <summary>Quyển đang học: viền cam, nhún nhẹ.</summary>
        Current,

        /// <summary>Đã học xong mọi bài: dấu "Đã học xong" và bông hoa.</summary>
        Done,

        /// <summary>Đã mở (ví dụ phụ huynh bật "Mở mọi bài") nhưng không phải quyển đang học.</summary>
        Open,
    }

    /// <summary>
    /// Tủ sách (bản thiết kế Tủ sách mục 5): các quyển đứng trên kệ theo thứ tự học, mỗi quyển một bìa (ảnh bìa không
    /// chữ, tên quyển do app viết), dưới bìa là tiến độ. Chạm quyển đã mở thì vào danh sách bài của quyển đó.
    /// </summary>
    public class ShelfScreen : MonoBehaviour
    {
        private const float Margin = 20f;
        private const float CoverWidth = 300f;
        private const float CoverHeight = 400f;
        private const float CoverGap = 60f;
        private const float ProgressHeight = 90f;
        private const float GlowWidth = 10f;

        // Nền dự phòng khi quyển chưa có ảnh bìa, theo thứ tự quyển (như bìa tạm của công cụ Python).
        private static readonly Color[] FallbackColors =
        {
            Palette.OrangeLight, Palette.TealLight, Palette.Hex("#DDCDE8"), Palette.Hex("#C4E1BE"), Palette.Hex("#F5E2A0"),
        };

        private AppRoot _app;
        private readonly List<string> _bookIds = new();
        private readonly Dictionary<string, Button> _covers = new();
        private readonly Dictionary<string, ShelfBookState> _states = new();
        private readonly Dictionary<string, TMP_Text> _titles = new();
        private readonly Dictionary<string, TMP_Text> _progress = new();

        public IReadOnlyList<string> BookIds => _bookIds;
        public TMP_Text Title { get; private set; }
        public Button SwitchChildButton { get; private set; }
        public Button SettingsButton { get; private set; }

        /// <summary>Quyển vừa mở khoá đang chạy hiệu ứng mở; <c>null</c> khi không có.</summary>
        public string CelebratedBookId { get; private set; }

        public Button CoverButton(string bookId) => bookId != null && _covers.TryGetValue(bookId, out var b) ? b : null;
        public ShelfBookState StateOf(string bookId) => _states.TryGetValue(bookId, out var s) ? s : ShelfBookState.Locked;
        public TMP_Text TitleOf(string bookId) => bookId != null && _titles.TryGetValue(bookId, out var t) ? t : null;
        public TMP_Text ProgressOf(string bookId) => bookId != null && _progress.TryGetValue(bookId, out var t) ? t : null;

        public void Build(AppRoot app, string celebrateBookId = null)
        {
            _app = app;
            var progress = app.Progress;
            var index = app.Lessons.Index;

            SwitchChildButton = UiKit.CreateIconButton(transform, app.Assets, progress.Current?.avatar, UiText.SwitchChild,
                app.ShowProfiles, Palette.PaperLight);
            Corner(SwitchChildButton, new Vector2(0f, 1f), new Vector2(Margin, -Margin));
            SwitchChildButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;

            SettingsButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Settings, UiText.Settings,
                () => app.ShowSettings(app.ShowShelf), Palette.PaperLight);
            Corner(SettingsButton, Vector2.one, new Vector2(-Margin, -Margin));
            SettingsButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;

            Title = UiKit.CreateLabel(transform, string.Format(UiText.ShelfTitleFormat, progress.Current?.name), 64f);
            var trt = Title.rectTransform;
            trt.anchorMin = new Vector2(0f, 1f);
            trt.anchorMax = Vector2.one;
            trt.pivot = new Vector2(.5f, 1f);
            trt.offsetMin = new Vector2(UiKit.MinTouch + 2f * Margin, -Margin - UiKit.MinTouch);
            trt.offsetMax = new Vector2(-(UiKit.MinTouch + 2f * Margin), -Margin);

            var shelf = BuildShelfRow();
            var current = BookShelf.CurrentBookId(index, progress);
            var ids = BookShelf.BookIds(index);
            for (var k = 0; k < ids.Count; k++)
            {
                var id = ids[k];
                _bookIds.Add(id);
                var state = !BookShelf.IsBookUnlocked(index, progress, id) ? ShelfBookState.Locked
                    : BookShelf.IsBookDone(index, progress, id) ? ShelfBookState.Done
                    : id == current ? ShelfBookState.Current
                    : ShelfBookState.Open;
                _states[id] = state;
                AddBook(shelf, index, id, k, state);
            }

            var mascot = Mascot.Create(transform, app.Assets);
            var mrt = (RectTransform)mascot.transform;
            mrt.anchorMin = mrt.anchorMax = mrt.pivot = new Vector2(1f, 0f);
            mrt.anchoredPosition = new Vector2(-Margin, Margin);

            if (!string.IsNullOrEmpty(celebrateBookId)) Celebrate(celebrateBookId);
        }

        /// <summary>Hàng bìa cuộn ngang được (khi nhiều quyển hơn chỗ trống), đặt giữa vùng dưới tiêu đề, có vạch kệ.</summary>
        private RectTransform BuildShelfRow()
        {
            var scrollGo = new GameObject("Shelf", typeof(RectTransform), typeof(ScrollRect), typeof(Image), typeof(RectMask2D));
            scrollGo.transform.SetParent(transform, false);
            var srt = (RectTransform)scrollGo.transform;
            srt.anchorMin = new Vector2(0f, .5f);
            srt.anchorMax = new Vector2(1f, .5f);
            srt.pivot = new Vector2(.5f, .5f);
            srt.offsetMin = new Vector2(Margin, -(CoverHeight + ProgressHeight) / 2f - 30f);
            srt.offsetMax = new Vector2(-Margin, (CoverHeight + ProgressHeight) / 2f + 10f);
            srt.anchoredPosition = new Vector2(0f, -40f);
            scrollGo.GetComponent<Image>().color = Color.clear;

            var content = new GameObject("Books", typeof(RectTransform), typeof(HorizontalLayoutGroup), typeof(ContentSizeFitter));
            content.transform.SetParent(scrollGo.transform, false);
            var crt = (RectTransform)content.transform;
            crt.anchorMin = crt.anchorMax = crt.pivot = new Vector2(.5f, .5f);
            var hlg = content.GetComponent<HorizontalLayoutGroup>();
            hlg.spacing = CoverGap;
            hlg.padding = new RectOffset((int)CoverGap / 2, (int)CoverGap / 2, 20, 0);
            hlg.childAlignment = TextAnchor.UpperCenter;
            hlg.childControlWidth = hlg.childControlHeight = false;
            hlg.childForceExpandWidth = hlg.childForceExpandHeight = false;
            var fitter = content.GetComponent<ContentSizeFitter>();
            fitter.horizontalFit = ContentSizeFitter.FitMode.PreferredSize;
            fitter.verticalFit = ContentSizeFitter.FitMode.PreferredSize;

            var scroll = scrollGo.GetComponent<ScrollRect>();
            scroll.viewport = srt;
            scroll.content = crt;
            scroll.horizontal = true;
            scroll.vertical = false;
            scroll.movementType = ScrollRect.MovementType.Clamped;

            // Vạch kệ dưới chân các bìa.
            var plank = new GameObject("Plank", typeof(RectTransform), typeof(Image));
            plank.transform.SetParent(transform, false);
            var prt = (RectTransform)plank.transform;
            prt.anchorMin = new Vector2(.5f, .5f);
            prt.anchorMax = new Vector2(.5f, .5f);
            prt.sizeDelta = new Vector2(UiKit.SafeWidth - 4f * Margin, 14f);
            prt.anchoredPosition = new Vector2(0f, -40f + (CoverHeight + ProgressHeight) / 2f - CoverHeight - 30f);
            var plankImg = plank.GetComponent<Image>();
            plankImg.sprite = UiShapes.Rounded;
            plankImg.type = Image.Type.Sliced;
            plankImg.color = Palette.Ink;
            plankImg.raycastTarget = false;
            plank.transform.SetSiblingIndex(scrollGo.transform.GetSiblingIndex());
            return crt;
        }

        private void AddBook(RectTransform shelf, LessonIndex index, string bookId, int order, ShelfBookState state)
        {
            var item = new GameObject($"Book_{bookId}", typeof(RectTransform));
            item.transform.SetParent(shelf, false);
            ((RectTransform)item.transform).sizeDelta = new Vector2(CoverWidth, CoverHeight + ProgressHeight);

            // Bìa: nút có viền mực, bên trong là ảnh bìa (hoặc nền màu dự phòng).
            var coverGo = new GameObject("Cover", typeof(RectTransform), typeof(Image), typeof(Button), typeof(TapFeedback));
            coverGo.transform.SetParent(item.transform, false);
            var crt = (RectTransform)coverGo.transform;
            crt.anchorMin = crt.anchorMax = crt.pivot = new Vector2(.5f, 1f);
            crt.sizeDelta = new Vector2(CoverWidth, CoverHeight);
            crt.anchoredPosition = Vector2.zero;
            UiKit.SetRounded(coverGo.GetComponent<Image>(), Palette.Ink);
            UiKit.AddHatchShadow(crt);

            var art = UiKit.AddFill(coverGo.transform, UiShapes.Rounded, FallbackColors[order % FallbackColors.Length]);
            var sprite = _app.Assets.HasImage(SystemImages.CoverOf(bookId)) ? _app.Assets.Image(SystemImages.CoverOf(bookId)) : null;
            if (sprite != null)
            {
                art.sprite = sprite;
                art.type = Image.Type.Simple;
                art.preserveAspect = false;
                art.color = Color.white;
            }

            // Tên quyển do app viết trên vùng trống phía trên của bìa.
            var title = UiKit.CreateLabel(coverGo.transform, (BookShelf.Book(index, bookId)?.title ?? bookId).Replace(" – ", "\n"), 44f);
            var trt = title.rectTransform;
            trt.anchorMin = new Vector2(0f, 1f);
            trt.anchorMax = Vector2.one;
            trt.pivot = new Vector2(.5f, 1f);
            // Trùng khung giấy sáng phía trên của bìa (bìa tạm vẽ khung ở 1/6–9/10 bề ngang, 1/10–2/5 bề cao).
            trt.offsetMin = new Vector2(CoverWidth / 6f + 8f, -CoverHeight * 2f / 5f + 8f);
            trt.offsetMax = new Vector2(-CoverWidth / 10f - 8f, -CoverHeight / 10f - 8f);
            _titles[bookId] = title;

            var button = coverGo.GetComponent<Button>();
            button.targetGraphic = coverGo.GetComponent<Image>();
            coverGo.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;
            _covers[bookId] = button;
            var id = bookId;
            button.onClick.AddListener(() => OnCover(id));

            var (done, total) = BookShelf.Progress(index, _app.Progress.Current, bookId);
            var label = UiKit.CreateLabel(item.transform, string.Format(UiText.BookProgressFormat, done, total), 36f);
            var lrt = label.rectTransform;
            lrt.anchorMin = lrt.anchorMax = lrt.pivot = new Vector2(.5f, 0f);
            lrt.sizeDelta = new Vector2(CoverWidth, ProgressHeight - 30f);
            lrt.anchoredPosition = new Vector2(0f, 24f);
            _progress[bookId] = label;
            AddBar(item.transform, total > 0 ? (float)done / total : 0f);

            switch (state)
            {
                case ShelfBookState.Locked:
                    // Lớp giấy mờ phủ lên bìa (giữ màu bìa nhạt đi), chữ màu khoá, ổ khoá ở giữa.
                    var veil = UiKit.AddFill(coverGo.transform, UiShapes.Rounded, new Color(Palette.LockedFill.r,
                        Palette.LockedFill.g, Palette.LockedFill.b, .7f));
                    veil.transform.SetSiblingIndex(art.transform.GetSiblingIndex() + 1);
                    title.color = Palette.LockedInk;
                    AddIcon(coverGo.transform, SystemIcons.Lock, 110f, new Vector2(.5f, .35f));
                    break;
                case ShelfBookState.Current:
                    AddGlow(crt);
                    Pulse.StartOn(coverGo.transform, .04f, 1.6f);
                    break;
                case ShelfBookState.Done:
                    AddIcon(coverGo.transform, SystemImages.Flower, 72f, new Vector2(.24f, .17f));
                    var stamp = UiKit.CreateLabel(coverGo.transform, UiText.BookDone, 36f);
                    stamp.color = Palette.StampRed;
                    var srt = stamp.rectTransform;
                    srt.anchorMin = srt.anchorMax = new Vector2(.64f, .17f);
                    srt.sizeDelta = new Vector2(180f, 60f);
                    srt.localRotation = Quaternion.Euler(0f, 0f, 8f);
                    break;
            }
        }

        private void OnCover(string bookId)
        {
            if (StateOf(bookId) == ShelfBookState.Locked)
            {
                _ = Motion.Shake((RectTransform)_covers[bookId].transform, 10f, .3f);
                return;
            }
            _app.OpenBook(bookId);
        }

        /// <summary>Viền cam phía sau bìa của quyển đang học.</summary>
        private static void AddGlow(RectTransform cover)
        {
            var glow = new GameObject("Glow", typeof(RectTransform), typeof(Image));
            glow.transform.SetParent(cover, false);
            glow.transform.SetAsFirstSibling();
            var rt = (RectTransform)glow.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = new Vector2(-GlowWidth, -GlowWidth);
            rt.offsetMax = new Vector2(GlowWidth, GlowWidth);
            var img = glow.GetComponent<Image>();
            img.sprite = UiShapes.Rounded;
            img.type = Image.Type.Sliced;
            img.color = Palette.Orange;
            img.raycastTarget = false;
        }

        private void AddIcon(Transform parent, string imageId, float size, Vector2 anchor)
        {
            var go = new GameObject(imageId, typeof(RectTransform), typeof(Image));
            go.transform.SetParent(parent, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = rt.anchorMax = anchor;
            rt.sizeDelta = new Vector2(size, size);
            var img = go.GetComponent<Image>();
            img.sprite = _app.Assets.HasImage(imageId) ? _app.Assets.Image(imageId) : null;
            img.enabled = img.sprite != null;
            img.preserveAspect = true;
            img.raycastTarget = false;
        }

        /// <summary>Thanh tiến độ dưới bìa: khung viền mực, phần đã học màu cam.</summary>
        private static void AddBar(Transform parent, float fraction)
        {
            var bar = new GameObject("Bar", typeof(RectTransform), typeof(Image));
            bar.transform.SetParent(parent, false);
            var rt = (RectTransform)bar.transform;
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(.5f, 0f);
            rt.sizeDelta = new Vector2(CoverWidth - 40f, 18f);
            rt.anchoredPosition = new Vector2(0f, 4f);
            UiKit.SetRounded(bar.GetComponent<Image>(), Palette.Ink);
            bar.GetComponent<Image>().raycastTarget = false;
            var fill = UiKit.AddFill(bar.transform, UiShapes.Rounded, Palette.PaperLight);
            var done = UiKit.AddFill(fill.transform, UiShapes.Rounded, Palette.Orange);
            var drt = done.rectTransform;
            drt.anchorMin = Vector2.zero;
            drt.anchorMax = new Vector2(Mathf.Clamp01(fraction), 1f);
            drt.offsetMin = drt.offsetMax = Vector2.zero;
            done.enabled = fraction > 0f;
        }

        /// <summary>Quyển vừa mở khoá: ổ khoá rơi xuống rồi mờ đi, bìa nảy nhẹ, có tiếng "ting".</summary>
        private async void Celebrate(string bookId)
        {
            var cover = CoverButton(bookId);
            if (cover == null) return;
            CelebratedBookId = bookId;
            var lockGo = new GameObject("FallingLock", typeof(RectTransform), typeof(Image), typeof(CanvasGroup));
            lockGo.transform.SetParent(cover.transform, false);
            var rt = (RectTransform)lockGo.transform;
            rt.anchorMin = rt.anchorMax = new Vector2(.5f, .35f);
            rt.sizeDelta = new Vector2(110f, 110f);
            var img = lockGo.GetComponent<Image>();
            img.sprite = _app.Assets.HasImage(SystemIcons.Lock) ? _app.Assets.Image(SystemIcons.Lock) : null;
            img.enabled = img.sprite != null;
            img.preserveAspect = true;
            img.raycastTarget = false;
            if (SfxPlayer.Instance != null) SfxPlayer.Instance.Play(SystemSfx.Correct);
            _ = Motion.Fade(lockGo.GetComponent<CanvasGroup>(), 0f, .6f);
            _ = Motion.Punch(cover.transform, 1.12f, .35f);
            await Motion.MoveTo(rt, rt.anchoredPosition + new Vector2(0f, -220f), .6f);
            if (lockGo != null) Destroy(lockGo);
        }

        private static void Corner(Button button, Vector2 corner, Vector2 offset)
        {
            var rt = (RectTransform)button.transform;
            rt.anchorMin = rt.anchorMax = rt.pivot = corner;
            rt.anchoredPosition = offset;
        }
    }
}
