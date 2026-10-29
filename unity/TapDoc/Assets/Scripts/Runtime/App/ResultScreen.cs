using System.Linq;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Màn kết thúc bài: khen, 3 sao (không phụ thuộc số lần sai), nút "Học bài tiếp" và "Về danh sách".
    /// Khi mở màn này bài được ghi là đã học xong và tiến độ được lưu ngay. Phiên "Ôn lại"
    /// (<see cref="ReviewSession.LessonId"/>) không phải một bài: không ghi đã học và không có nút "Học bài tiếp".
    /// </summary>
    public class ResultScreen : MonoBehaviour
    {
        private const float StarSize = 180f;

        public Button NextLessonButton { get; private set; }
        public Button ToListButton { get; private set; }

        public void Build(AppRoot app, string lessonId)
        {
            var isReview = lessonId == ReviewSession.LessonId;
            if (!string.IsNullOrEmpty(lessonId) && !isReview)
            {
                app.Progress.MarkCompleted(lessonId);
                app.SaveProgress();
            }

            var praise = UiKit.CreateLabel(transform, UiText.Praise, 72f);
            var praiseRt = praise.GetComponent<RectTransform>();
            praiseRt.anchorMin = new Vector2(0.5f, 1f);
            praiseRt.anchorMax = new Vector2(0.5f, 1f);
            praiseRt.pivot = new Vector2(0.5f, 1f);
            praiseRt.sizeDelta = new Vector2(800f, 140f);
            praiseRt.anchoredPosition = new Vector2(0f, -80f);

            var starsRow = new GameObject("Stars", typeof(RectTransform), typeof(HorizontalLayoutGroup));
            starsRow.transform.SetParent(transform, false);
            var starsRt = starsRow.GetComponent<RectTransform>();
            starsRt.anchorMin = new Vector2(0.5f, 0.5f);
            starsRt.anchorMax = new Vector2(0.5f, 0.5f);
            starsRt.sizeDelta = new Vector2(720f, 220f);
            starsRt.anchoredPosition = new Vector2(0f, 60f);

            var starsHlg = starsRow.GetComponent<HorizontalLayoutGroup>();
            starsHlg.spacing = 40f;
            starsHlg.childAlignment = TextAnchor.MiddleCenter;
            starsHlg.childControlWidth = false;
            starsHlg.childControlHeight = false;

            for (var i = 0; i < ProgressStore.MaxStars; i++)
            {
                MarkerIcon.CreateStar(starsRow.transform, app.Assets, StarSize).name = $"Star_{i}";
            }

            var btnRow = new GameObject("Buttons", typeof(RectTransform), typeof(HorizontalLayoutGroup));
            btnRow.transform.SetParent(transform, false);
            var btnRt = btnRow.GetComponent<RectTransform>();
            btnRt.anchorMin = new Vector2(0.5f, 0f);
            btnRt.anchorMax = new Vector2(0.5f, 0f);
            btnRt.pivot = new Vector2(0.5f, 0f);
            btnRt.sizeDelta = new Vector2(900f, 200f);
            btnRt.anchoredPosition = new Vector2(0f, 80f);

            var btnHlg = btnRow.GetComponent<HorizontalLayoutGroup>();
            btnHlg.spacing = 40f;
            btnHlg.childAlignment = TextAnchor.MiddleCenter;
            btnHlg.childControlWidth = true;
            btnHlg.childControlHeight = true;

            var nextLessonId = isReview ? null : FindNextLessonId(app.Progress, lessonId);
            if (!string.IsNullOrEmpty(nextLessonId))
            {
                NextLessonButton = UiKit.CreateButton(btnRow.transform, UiText.NextLesson, () => app.ShowLesson(nextLessonId));
                var le = NextLessonButton.GetComponent<LayoutElement>();
                le.minWidth = 340f;
                le.preferredWidth = 380f;
            }

            ToListButton = UiKit.CreateButton(btnRow.transform, UiText.ToList, () => app.ShowLessonList());
            var listLe = ToListButton.GetComponent<LayoutElement>();
            listLe.minWidth = 340f;
            listLe.preferredWidth = 380f;

            _ = app.Speech.PlayAsync(SystemAudio.khen_hoan_thanh);
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
