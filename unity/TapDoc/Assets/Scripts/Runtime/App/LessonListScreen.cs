using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    public class LessonListScreen : MonoBehaviour
    {
        public void Build(AppRoot app)
        {
            var header = UiKit.CreateLabel(transform, "Tập đọc lớp 1", 64f);
            var headerRt = header.GetComponent<RectTransform>();
            headerRt.anchorMin = new Vector2(0.5f, 1f);
            headerRt.anchorMax = new Vector2(0.5f, 1f);
            headerRt.pivot = new Vector2(0.5f, 1f);
            headerRt.sizeDelta = new Vector2(1200f, 140f);
            headerRt.anchoredPosition = new Vector2(0f, -60f);

            var rowGo = new GameObject("LessonButtons", typeof(RectTransform), typeof(HorizontalLayoutGroup));
            rowGo.transform.SetParent(transform, false);
            var rowRt = rowGo.GetComponent<RectTransform>();
            rowRt.anchorMin = new Vector2(0.5f, 0.5f);
            rowRt.anchorMax = new Vector2(0.5f, 0.5f);
            rowRt.sizeDelta = new Vector2(1340f, 360f);
            rowRt.anchoredPosition = new Vector2(0f, -40f);

            var hlg = rowGo.GetComponent<HorizontalLayoutGroup>();
            hlg.spacing = 40f;
            hlg.childAlignment = TextAnchor.MiddleCenter;
            hlg.childControlWidth = true;
            hlg.childControlHeight = true;
            hlg.childForceExpandWidth = true;
            hlg.childForceExpandHeight = true;

            var index = LessonRepository.LoadIndex();
            foreach (var entry in index.lessons)
            {
                var lessonId = entry.lesson_id;
                var label = $"{UiText.LessonPrefix} {entry.lesson_no}\n{entry.title}";
                var btn = UiKit.CreateButton(rowGo.transform, label, () => app.ShowLesson(lessonId));
                var le = btn.GetComponent<LayoutElement>();
                le.minWidth = 360f;
                le.minHeight = 280f;
                le.preferredWidth = 400f;
                le.preferredHeight = 320f;
            }
        }
    }
}
