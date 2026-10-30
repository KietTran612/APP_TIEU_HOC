using System.Linq;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Màn kết thúc bài: cảnh dán hoa vào Sổ bé ngoan (bản thiết kế giao diện mục 8.4). Sổ mở ở trang của bài; các bông
    /// hoa mới lần lượt bay vào ô, đóng dấu "Bé ngoan", gà con khen cùng giọng đọc, rồi mới hiện nút "Về danh sách" và
    /// "Học bài tiếp". Chạm màn khi cảnh đang chạy thì nhảy tới cuối. Khi mở màn này bài được ghi là đã học xong và tiến
    /// độ được lưu ngay. Phiên "Ôn lại" (<see cref="ReviewSession.LessonId"/>) không phải một bài: không có sổ, không ghi
    /// đã học, không có nút "Học bài tiếp".
    /// </summary>
    public class ResultScreen : MonoBehaviour
    {
        private const float TopBand = 200f;
        private const float BottomBand = 200f;
        private const float Margin = 20f;
        private const float FlySeconds = .35f;
        private const float FlyGap = .3f;
        private const float StampSeconds = .25f;
        private const int PetalsPerFlower = 3;

        private AppRoot _app;
        private BookPage _page;
        private RectTransform _overlay;
        private SceneSkipper _skipper;
        private Stamp _stamp;
        private int _before;
        private int _after;
        private bool _praised;

        public Button NextLessonButton { get; private set; }
        public Button ToListButton { get; private set; }

        /// <summary>Quyển sổ của cảnh; <c>null</c> ở phiên ôn.</summary>
        public BookSpread Spread { get; private set; }

        public Mascot Mascot { get; private set; }

        /// <summary>Cảnh đã xong (hoa đã dán, nút đã hiện).</summary>
        public bool IsSceneDone { get; private set; }

        /// <summary>Số bông hoa mới được dán lần này (học lại bài đã đủ hoa thì 0).</summary>
        public int FlownFlowers { get; private set; }

        public void Build(AppRoot app, string lessonId)
        {
            _app = app;
            var isReview = lessonId == ReviewSession.LessonId;
            var isLesson = !string.IsNullOrEmpty(lessonId) && !isReview;
            if (isLesson)
            {
                _before = FlowerBook.FlowersFor(app.Progress, lessonId);
                app.Progress.MarkCompleted(lessonId);
                app.SaveProgress();
                _after = FlowerBook.FlowersFor(app.Progress, lessonId);
            }

            var praise = UiKit.CreateLabel(transform, UiText.Praise, 64f);
            var prt = praise.rectTransform;
            prt.anchorMin = prt.anchorMax = prt.pivot = new Vector2(.5f, 1f);
            prt.sizeDelta = new Vector2(800f, UiKit.MinTouch);
            prt.anchoredPosition = new Vector2(0f, -Margin);

            if (isLesson) BuildBook(lessonId);

            _overlay = Stretched("Overlay");
            _skipper = SceneSkipper.Create(transform, SkipScene);

            Mascot = Mascot.Create(transform, app.Assets);
            var mrt = (RectTransform)Mascot.transform;
            mrt.anchorMin = mrt.anchorMax = mrt.pivot = new Vector2(1f, 0f);
            mrt.anchoredPosition = new Vector2(-(2f * Margin + UiKit.MinTouch), Margin);

            ToListButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Home, UiText.ToList,
                () => app.ShowLessonList());
            Corner(ToListButton, Vector2.zero, new Vector2(Margin, Margin));
            var nextLessonId = isLesson ? FindNextLessonId(app.Progress, lessonId) : null;
            if (!string.IsNullOrEmpty(nextLessonId))
            {
                NextLessonButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Forward, UiText.NextLesson,
                    () => app.ShowLesson(nextLessonId), Palette.Orange);
                Corner(NextLessonButton, new Vector2(1f, 0f), new Vector2(-Margin, Margin));
            }
            SetButtonsVisible(false);

            RunScene();
        }

        private void BuildBook(string lessonId)
        {
            var area = Stretched("BookArea");
            area.offsetMin = new Vector2(Margin, BottomBand);
            area.offsetMax = new Vector2(-Margin, -TopBand);
            var entries = LessonRepository.LoadIndex().lessons;
            Spread = BookSpread.Create(area, entries, _app.Progress, _app.Assets);
            Spread.ShowPage(FlowerBook.PageOf(entries.Select(e => e.lesson_id).ToList(), lessonId));
            _page = Spread.PageFor(lessonId);
            if (_page == null) return;
            _page.SetFlowers(_before);
            foreach (var slot in _page.Slots) slot.GetComponent<Image>().color = Palette.Orange; // ô sáng viền cam
        }

        private RectTransform Stretched(string name)
        {
            var go = new GameObject(name, typeof(RectTransform));
            go.transform.SetParent(transform, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            return rt;
        }

        private static void Corner(Button button, Vector2 corner, Vector2 offset)
        {
            var rt = (RectTransform)button.transform;
            rt.anchorMin = rt.anchorMax = rt.pivot = corner;
            rt.anchoredPosition = offset;
        }

        private void SetButtonsVisible(bool visible)
        {
            ToListButton.gameObject.SetActive(visible);
            if (NextLessonButton != null) NextLessonButton.gameObject.SetActive(visible);
        }

        private async void RunScene()
        {
            if (_page != null)
            {
                for (var k = _before; k < _after; k++)
                {
                    if (k > _before && Motion.Scale > 0f) await Awaitable.WaitForSecondsAsync(FlyGap * Motion.Scale);
                    if (this == null || IsSceneDone) return;
                    await FlyFlower(k);
                    if (this == null || IsSceneDone) return;
                }
                await StampDown();
                if (this == null || IsSceneDone) return;
            }
            Praise();
            Finish();
        }

        /// <summary>Một bông hoa bay từ trên xuống ô <paramref name="slot"/>, nảy nhẹ, cánh hoa rơi ra.</summary>
        private async Awaitable FlyFlower(int slot)
        {
            var target = (RectTransform)_page.Slots[slot].transform;
            var targetPos = (Vector2)_overlay.InverseTransformPoint(target.TransformPoint(target.rect.center));
            Sfx(SystemSfx.FlowerFly);

            var flower = Picture(FlowerBook.FlowerImage(_page.LessonId, slot), BookPage.SlotSize, "FlyingFlower");
            flower.anchoredPosition = new Vector2(0f, _overlay.rect.height / 2f + BookPage.SlotSize);
            flower.localScale = Vector3.one * 1.6f;
            _ = Motion.ScaleTo(flower, 1f, FlySeconds);
            await Motion.MoveTo(flower, targetPos, FlySeconds);
            if (flower != null) Destroy(flower.gameObject);
            if (this == null || IsSceneDone) return;

            FlownFlowers++;
            _page.SetFlowers(slot + 1);
            _ = Motion.Punch(target, 1.15f, .2f);
            for (var i = 0; i < PetalsPerFlower; i++) DropPetal(targetPos, i);
        }

        private async void DropPetal(Vector2 from, int index)
        {
            var petal = Picture(SystemIcons.Petal, 36f, "Petal");
            petal.anchoredPosition = from;
            var group = petal.gameObject.AddComponent<CanvasGroup>();
            var side = (index - (PetalsPerFlower - 1) / 2f) * 70f;
            _ = Motion.Wiggle(petal, 40f, .6f);
            _ = Motion.Fade(group, 0f, .6f);
            await Motion.MoveTo(petal, from + new Vector2(side, -110f), .6f);
            if (petal != null) Destroy(petal.gameObject);
        }

        private RectTransform Picture(string imageId, float size, string name)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(Image));
            go.transform.SetParent(_overlay, false);
            var rt = (RectTransform)go.transform;
            rt.sizeDelta = new Vector2(size, size);
            var img = go.GetComponent<Image>();
            img.sprite = _app.Assets.Image(imageId);
            img.preserveAspect = true;
            img.raycastTarget = false;
            img.enabled = img.sprite != null;
            return rt;
        }

        /// <summary>Con dấu "Bé ngoan" đóng xuống phần trống phía dưới trang, sổ rung nhẹ.</summary>
        private async Awaitable StampDown()
        {
            _stamp = Stamp.Create(_page.Content);
            _stamp.transform.localScale = Vector3.one * 2.6f;
            Sfx(SystemSfx.Stamp);
            await Motion.ScaleTo(_stamp.transform, 1f, StampSeconds);
            if (this == null || IsSceneDone) return;
            _ = Motion.Shake((RectTransform)Spread.transform, 6f, .25f);
        }

        private void Praise()
        {
            if (_praised) return;
            _praised = true;
            Mascot.Cheer(UiText.MascotLessonDone, keepBubble: true);
            _ = _app.Speech.PlayAsync(SystemAudio.khen_hoan_thanh);
        }

        /// <summary>Bé chạm màn khi cảnh đang chạy: hoa đã dán, dấu đã đóng, nút đã hiện.</summary>
        internal void SkipScene()
        {
            if (IsSceneDone) return;
            foreach (Transform child in _overlay) Destroy(child.gameObject);
            if (_page != null)
            {
                FlownFlowers = _after - _before;
                if (_stamp == null) _stamp = Stamp.Create(_page.Content);
                _stamp.transform.localScale = Vector3.one;
            }
            Praise();
            Finish();
        }

        private void Finish()
        {
            if (IsSceneDone) return;
            IsSceneDone = true;
            if (_page != null) _page.SetFlowers(_after);
            if (_skipper != null) Destroy(_skipper.gameObject);
            SetButtonsVisible(true);
            _ = Motion.Punch(ToListButton.transform, 1.15f, .25f);
            if (NextLessonButton != null) _ = Motion.Punch(NextLessonButton.transform, 1.15f, .25f);
            if (_stamp != null) _ = Motion.Fade(_stamp.Group, 0f, .5f);
        }

        private static void Sfx(string id)
        {
            if (SfxPlayer.Instance != null) SfxPlayer.Instance.Play(id);
        }

        /// <summary>Bài đứng sau <paramref name="currentLessonId"/> trong danh sách, nếu bài đó đã mở cho bé.</summary>
        private static string FindNextLessonId(ProgressStore progress, string currentLessonId)
        {
            if (string.IsNullOrEmpty(currentLessonId)) return null;
            try
            {
                var ordered = LessonRepository.LoadIndex().lessons.Select(e => e.lesson_id).ToList();
                var idx = ordered.IndexOf(currentLessonId);
                if (idx >= 0 && idx + 1 < ordered.Count && progress.IsUnlocked(ordered, ordered[idx + 1]))
                {
                    return ordered[idx + 1];
                }
            }
            catch
            {
                // Ignore if index not available in synthetic test
            }
            return null;
        }
    }
}
