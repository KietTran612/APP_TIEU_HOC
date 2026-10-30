using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Quyển Sổ bé ngoan mở hai trang (trang trái là trang chẵn, tính từ 0), dùng chung cho màn sổ và màn kết thúc bài.
    /// Mỗi trang một bài theo thứ tự danh sách bài; lật trang như sách thật (<see cref="Motion.PageTurn"/>).
    /// </summary>
    public class BookSpread : MonoBehaviour
    {
        public const float FlipSeconds = .4f;

        private IReadOnlyList<LessonEntry> _entries;
        private ProgressStore _progress;
        private AssetCatalog _assets;
        private RectTransform _left;
        private RectTransform _right;
        private readonly List<BookPage> _pages = new();

        /// <summary>Trang bên trái của cặp trang đang mở.</summary>
        public int LeftPage { get; private set; }

        public int PageCount => _entries.Count;

        /// <summary>Trang cũ đang lật (để test kiểm tra); <c>null</c> khi không lật.</summary>
        public GameObject TurningPage { get; private set; }

        /// <summary>
        /// Dựng quyển sổ phủ kín <paramref name="parent"/>: hai trang giấy viền mực có gáy ở giữa và bóng gạch chéo.
        /// </summary>
        public static BookSpread Create(RectTransform parent, IReadOnlyList<LessonEntry> entries, ProgressStore progress,
            AssetCatalog assets)
        {
            var go = new GameObject("BookSpread", typeof(RectTransform), typeof(BookSpread));
            go.transform.SetParent(parent, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            UiKit.AddHatchShadow(rt);

            var spread = go.GetComponent<BookSpread>();
            spread._entries = entries;
            spread._progress = progress;
            spread._assets = assets;
            spread._left = spread.Sheet("PageLeft", 0f);
            spread._right = spread.Sheet("PageRight", .5f);
            spread.ShowPage(0);
            return spread;
        }

        /// <summary>Một tờ giấy chiếm nửa quyển sổ, bắt đầu ở <paramref name="x"/> (tỉ lệ bề ngang).</summary>
        private RectTransform Sheet(string name, float x)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(Image));
            go.transform.SetParent(transform, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = new Vector2(x, 0f);
            rt.anchorMax = new Vector2(x + .5f, 1f);
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            var border = go.GetComponent<Image>();
            border.sprite = UiShapes.Rounded;
            border.type = Image.Type.Sliced;
            border.color = Palette.Ink;
            border.raycastTarget = false;

            var fill = new GameObject("Paper", typeof(RectTransform), typeof(Image));
            fill.transform.SetParent(rt, false);
            var frt = (RectTransform)fill.transform;
            frt.anchorMin = Vector2.zero;
            frt.anchorMax = Vector2.one;
            frt.offsetMin = new Vector2(UiKit.BorderWidth, UiKit.BorderWidth);
            frt.offsetMax = new Vector2(-UiKit.BorderWidth, -UiKit.BorderWidth);
            var paper = fill.GetComponent<Image>();
            paper.sprite = UiShapes.Rounded;
            paper.type = Image.Type.Sliced;
            paper.color = Palette.PaperLight;
            paper.raycastTarget = false;
            return rt;
        }

        /// <summary>Mở cặp trang chứa <paramref name="page"/> (không có hiệu ứng).</summary>
        public void ShowPage(int page)
        {
            LeftPage = FlowerBook.SpreadStart(Mathf.Clamp(page, 0, Mathf.Max(0, PageCount - 1)));
            foreach (var p in _pages)
            {
                if (p != null) Destroy(p.gameObject);
            }
            _pages.Clear();
            _pages.Add(Fill(_left, LeftPage));
            _pages.Add(Fill(_right, LeftPage + 1));
        }

        private BookPage Fill(RectTransform sheet, int page)
        {
            var entry = page < PageCount ? _entries[page] : null;
            var flowers = entry != null ? FlowerBook.FlowersFor(_progress, entry.lesson_id) : 0;
            return BookPage.Create(sheet, entry, flowers, _assets);
        }

        /// <summary>Trang của bài <paramref name="lessonId"/> nếu đang mở; <c>null</c> nếu không.</summary>
        public BookPage PageFor(string lessonId) =>
            lessonId == null ? null : _pages.FirstOrDefault(p => p != null && p.LessonId == lessonId);

        /// <summary>
        /// Lật tới cặp trang chứa <paramref name="page"/> như lật sách: cặp mới hiện ngay bên dưới, một bản sao của tờ cũ
        /// (tờ phải khi lật tới, tờ trái khi lật lùi) lật quanh gáy sổ rồi bị huỷ; kèm tiếng lật trang.
        /// </summary>
        public async Awaitable FlipTo(int page)
        {
            var target = FlowerBook.SpreadStart(Mathf.Clamp(page, 0, Mathf.Max(0, PageCount - 1)));
            if (target == LeftPage) return;
            var forward = target > LeftPage;
            if (SfxPlayer.Instance != null) SfxPlayer.Instance.Play(SystemSfx.PageFlip);

            if (TurningPage != null) Destroy(TurningPage);
            TurningPage = null;
            GameObject turning = null;
            if (Motion.Scale > 0f)
            {
                var source = forward ? _right : _left;
                turning = Instantiate(source.gameObject, transform);
                turning.name = "TurningPage";
                var trt = (RectTransform)turning.transform;
                trt.anchorMin = source.anchorMin;
                trt.anchorMax = source.anchorMax;
                trt.offsetMin = source.offsetMin;
                trt.offsetMax = source.offsetMax;
                turning.transform.SetAsLastSibling();
                foreach (var g in turning.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;
                TurningPage = turning;
            }

            ShowPage(target);
            if (turning == null) return;
            await Motion.PageTurn((RectTransform)turning.transform, FlipSeconds, hingeLeft: forward);
            if (turning != null) Destroy(turning);
            if (this != null && TurningPage == turning) TurningPage = null;
        }
    }
}
