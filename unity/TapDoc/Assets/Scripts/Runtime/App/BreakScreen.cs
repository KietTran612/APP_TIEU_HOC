using System;
using System.Linq;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Nghỉ mắt (bản thiết kế nâng cấp UI mục 4.5): hiện sau màn Xong bài khi bé đã học đủ số bài phụ huynh đặt trong một
    /// lần học. Không đếm ngược, không khoá cứng: nút to "Tạm biệt" về màn chọn bé; "Phụ huynh: học thêm" qua khoá phép
    /// tính thì bắt đầu lần học mới và đi tiếp như nút của màn Xong bài.
    /// </summary>
    public class BreakScreen : MonoBehaviour
    {
        private const float Margin = 20f;
        private AppRoot _app;
        private Action _continue;
        private GameObject _gateOverlay;

        internal Mascot Mascot { get; private set; }
        internal Button GoodbyeButton { get; private set; }
        internal Button ParentMoreButton { get; private set; }
        internal ParentGatePanel Gate { get; private set; }
        internal TMP_Text TodayLabel { get; private set; }
        internal TMP_Text Suggestion { get; private set; }

        /// <summary>Tiếng rủ nghỉ đã phát (<c>null</c> khi chưa có file tiếng).</summary>
        internal string MascotAudio { get; private set; }

        public void Build(AppRoot app, Action continueLearning)
        {
            _app = app;
            _continue = continueLearning;
            var gap = ScreenLayout.EdgeGap;

            var title = UiKit.CreateLabel(transform, UiText.BreakTitle, 72f);
            var trt = title.rectTransform;
            trt.anchorMin = trt.anchorMax = trt.pivot = new Vector2(.5f, 1f);
            trt.sizeDelta = new Vector2(900f, UiKit.MinTouch);
            trt.anchoredPosition = new Vector2(0f, -Margin);

            // Trái: tranh nghỉ mắt (không bắt buộc) và gà con đứng trước tranh.
            var left = Box("Picture", new Vector2(0f, 0f), new Vector2(.48f, 1f), new Vector2(gap, gap + 10f), new Vector2(-10f, -200f));
            var sprite = app.Assets.Image(SystemImages.BreakPicture);
            if (sprite != null)
            {
                var pic = new GameObject("BreakPicture", typeof(RectTransform), typeof(Image));
                pic.transform.SetParent(left, false);
                var prt = (RectTransform)pic.transform;
                prt.anchorMin = new Vector2(.05f, .2f);
                prt.anchorMax = new Vector2(.95f, 1f);
                prt.offsetMin = prt.offsetMax = Vector2.zero;
                var img = pic.GetComponent<Image>();
                img.sprite = sprite;
                img.preserveAspect = true;
                img.raycastTarget = false;
            }
            Mascot = Mascot.Create(left, app.Assets, 220f);
            var mrt = (RectTransform)Mascot.transform;
            mrt.anchorMin = mrt.anchorMax = new Vector2(.5f, 0f);
            mrt.pivot = new Vector2(.5f, 0f);
            mrt.anchoredPosition = new Vector2(0f, 10f);
            Mascot.SetBubbleLayout(Mascot.BubbleSide.AboveRight, 420f);

            // Phải: hôm nay bé học mấy bài (hoa), một việc cho bố mẹ, nút Tạm biệt và Phụ huynh: học thêm.
            var right = Box("Info", new Vector2(.5f, 0f), new Vector2(1f, 1f), new Vector2(10f, gap), new Vector2(-gap, -200f));
            var today = ProgressStore.DayOf(app.Progress.Current, DateTime.Now).lessons;
            TodayLabel = Left(right, string.Format(UiText.TodayLessonsFormat, today), 44f, -10f, 64f);
            var flowers = new GameObject("Flowers", typeof(RectTransform), typeof(HorizontalLayoutGroup));
            flowers.transform.SetParent(right, false);
            var frt = (RectTransform)flowers.transform;
            frt.anchorMin = new Vector2(0f, 1f);
            frt.anchorMax = new Vector2(1f, 1f);
            frt.pivot = new Vector2(0f, 1f);
            frt.offsetMin = new Vector2(0f, -160f);
            frt.offsetMax = new Vector2(0f, -84f);
            var hlg = flowers.GetComponent<HorizontalLayoutGroup>();
            hlg.spacing = 8f;
            hlg.childAlignment = TextAnchor.MiddleLeft;
            hlg.childControlWidth = hlg.childControlHeight = false;
            hlg.childForceExpandWidth = hlg.childForceExpandHeight = false;
            for (var i = 0; i < Mathf.Min(today, 8); i++)
            {
                var f = new GameObject("Flower", typeof(RectTransform), typeof(Image));
                f.transform.SetParent(flowers.transform, false);
                ((RectTransform)f.transform).sizeDelta = new Vector2(70f, 70f);
                var img = f.GetComponent<Image>();
                img.sprite = app.Assets.Image(SystemImages.Flower);
                img.preserveAspect = true;
                img.raycastTarget = false;
            }

            var entry = app.Lessons.Index.lessons.FirstOrDefault(e => e.lesson_id == app.Progress.Current?.last_lesson_id);
            Lesson lesson = null;
            if (entry != null)
            {
                try
                {
                    lesson = app.Lessons.IsLoaded(entry.lesson_id) ? app.Lessons.Get(entry.lesson_id) : null;
                }
                catch (System.IO.InvalidDataException)
                {
                }
            }
            var suggestion = ParentSuggestions.For(entry, lesson).First();
            var note = Left(right, UiText.ForParents, 30f, -180f, 48f);
            note.color = Palette.MutedInk;
            Suggestion = Left(right, suggestion, 34f, -232f, 150f);
            Suggestion.enableAutoSizing = true;
            Suggestion.fontSizeMin = UiKit.MinFontSize;

            GoodbyeButton = UiKit.CreateButton(right, UiText.Goodbye, app.ShowProfiles);
            var grt = (RectTransform)GoodbyeButton.transform;
            grt.anchorMin = grt.anchorMax = grt.pivot = new Vector2(0f, 0f);
            grt.sizeDelta = new Vector2(360f, UiKit.MinTouch);
            grt.anchoredPosition = Vector2.zero;
            GoodbyeButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;

            ParentMoreButton = UiKit.CreateButton(right, UiText.ParentMore, OpenGate);
            var prt2 = (RectTransform)ParentMoreButton.transform;
            prt2.anchorMin = prt2.anchorMax = prt2.pivot = new Vector2(1f, 0f);
            prt2.sizeDelta = new Vector2(300f, UiKit.MinTouch);
            prt2.anchoredPosition = Vector2.zero;
            var fill = ParentMoreButton.transform.Find("Fill")?.GetComponent<Image>();
            if (fill != null) fill.color = Palette.PaperLight;
            var plabel = ParentMoreButton.GetComponentInChildren<TMP_Text>();
            plabel.color = Palette.MutedInk;
            plabel.fontSizeMax = 30f;

            Mascot.Cheer(UiText.BreakMascot, keepBubble: true);
            MascotAudio = app.Assets.Audio(SystemAudio.hd_nghi_mat) != null ? SystemAudio.hd_nghi_mat : null;
            if (MascotAudio != null) _ = app.Speech.PlayAsync(MascotAudio);
        }

        /// <summary>Khoá phép tính của phụ huynh; mở được thì bắt đầu lần học mới và đi tiếp.</summary>
        internal void OpenGate()
        {
            if (_gateOverlay != null)
            {
                _gateOverlay.SetActive(true);
                return;
            }
            _gateOverlay = new GameObject("GateOverlay", typeof(RectTransform), typeof(Image));
            _gateOverlay.transform.SetParent(transform, false);
            var ort = (RectTransform)_gateOverlay.transform;
            ort.anchorMin = Vector2.zero;
            ort.anchorMax = Vector2.one;
            ort.offsetMin = ort.offsetMax = Vector2.zero;
            _gateOverlay.GetComponent<Image>().color = Palette.Paper;
            Gate = ParentGatePanel.Create(_gateOverlay.transform, new System.Random(), () =>
            {
                _app.StartSession();
                _continue?.Invoke();
            });
            var back = UiKit.CreateButton(_gateOverlay.transform, UiText.Back, () => _gateOverlay.SetActive(false));
            var brt = (RectTransform)back.transform;
            brt.anchorMin = brt.anchorMax = brt.pivot = new Vector2(0f, 1f);
            brt.sizeDelta = new Vector2(220f, UiKit.MinTouch);
            brt.anchoredPosition = new Vector2(ScreenLayout.EdgeGap, -Margin);
        }

        private RectTransform Box(string name, Vector2 anchorMin, Vector2 anchorMax, Vector2 offsetMin, Vector2 offsetMax)
        {
            var go = new GameObject(name, typeof(RectTransform));
            go.transform.SetParent(transform, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = anchorMin;
            rt.anchorMax = anchorMax;
            rt.offsetMin = offsetMin;
            rt.offsetMax = offsetMax;
            return rt;
        }

        private static TextMeshProUGUI Left(Transform parent, string text, float size, float top, float height)
        {
            var label = UiKit.CreateLabel(parent, text, size);
            label.alignment = TextAlignmentOptions.TopLeft;
            var rt = label.rectTransform;
            rt.anchorMin = new Vector2(0f, 1f);
            rt.anchorMax = new Vector2(1f, 1f);
            rt.pivot = new Vector2(0f, 1f);
            rt.offsetMin = new Vector2(0f, top - height);
            rt.offsetMax = new Vector2(0f, top);
            return label;
        }
    }
}
