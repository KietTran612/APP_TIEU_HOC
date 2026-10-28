using System.Linq;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    public class ResultScreen : MonoBehaviour
    {
        public Button NextLessonButton { get; private set; }
        public Button ToListButton { get; private set; }

        public void Build(AppRoot app, string lessonId)
        {
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

            var starSprite = app.Assets.Image(SystemImages.Star);
            for (var i = 0; i < 3; i++)
            {
                var starGo = new GameObject($"Star_{i}", typeof(RectTransform), typeof(Image));
                starGo.transform.SetParent(starsRow.transform, false);
                starGo.GetComponent<RectTransform>().sizeDelta = new Vector2(180f, 180f);
                var img = starGo.GetComponent<Image>();
                img.sprite = starSprite ?? UiKit.WhiteSprite;
                img.preserveAspect = true;
                img.color = starSprite != null ? Color.white : new Color(1f, 0.82f, 0.15f, 1f);
                img.raycastTarget = false;
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

            var nextLessonId = FindNextLessonId(lessonId);
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

        private static string FindNextLessonId(string currentLessonId)
        {
            if (string.IsNullOrEmpty(currentLessonId)) return null;
            try
            {
                var entries = LessonRepository.LoadIndex().lessons;
                var idx = entries.FindIndex(e => e.lesson_id == currentLessonId);
                if (idx >= 0 && idx + 1 < entries.Count)
                {
                    return entries[idx + 1].lesson_id;
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
