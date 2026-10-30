using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    public enum MascotMood
    {
        None,
        Cheer,
        Ponder
    }

    /// <summary>
    /// Bạn gà con đồng hành (bản thiết kế giao diện mục 5): hình tròn viền mực, không nhận chạm. Khen thì nhảy hai nhịp
    /// và hiện bong bóng chữ; khi bé chọn sai thì nghiêng đầu như đang nghĩ. Lời khen bé nghe vẫn là giọng đọc.
    /// </summary>
    public class Mascot : MonoBehaviour
    {
        public const float DefaultSize = 150f;
        public const float BubbleSeconds = 1.5f;

        private RectTransform _body;
        private GameObject _bubble;
        private TMP_Text _bubbleText;
        private int _bubbleGeneration;

        public MascotMood LastMood { get; private set; }

        /// <summary>Chữ trong bong bóng đang hiện; chuỗi rỗng khi bong bóng ẩn.</summary>
        public string BubbleText => _bubble != null && _bubble.activeSelf ? _bubbleText.text : string.Empty;

        public static Mascot Create(Transform parent, AssetCatalog assets, float size = DefaultSize)
        {
            var go = new GameObject("Mascot", typeof(RectTransform), typeof(Mascot));
            go.transform.SetParent(parent, false);
            ((RectTransform)go.transform).sizeDelta = new Vector2(size, size);
            var mascot = go.GetComponent<Mascot>();
            mascot.Build(assets, size);
            return mascot;
        }

        private void Build(AssetCatalog assets, float size)
        {
            var body = new GameObject("Body", typeof(RectTransform), typeof(Image));
            body.transform.SetParent(transform, false);
            _body = (RectTransform)body.transform;
            _body.anchorMin = Vector2.zero;
            _body.anchorMax = Vector2.one;
            _body.offsetMin = Vector2.zero;
            _body.offsetMax = Vector2.zero;
            var ring = body.GetComponent<Image>();
            ring.sprite = UiShapes.Circle;
            ring.color = Palette.Ink;
            ring.raycastTarget = false;

            var paper = Child(_body, "Paper", UiShapes.Circle, UiKit.BorderWidth);
            paper.color = Palette.PaperLight;
            // Tranh vuông thụt 15% để góc tranh nằm trong vòng tròn.
            var picture = Child(_body, "Picture", assets?.Image(SystemImages.Mascot), size * .15f);
            picture.preserveAspect = true;
            picture.enabled = picture.sprite != null;

            _bubble = new GameObject("Bubble", typeof(RectTransform), typeof(Image));
            _bubble.transform.SetParent(transform, false);
            var brt = (RectTransform)_bubble.transform;
            brt.anchorMin = brt.anchorMax = new Vector2(.5f, 1f);
            brt.pivot = new Vector2(.85f, 0f);
            brt.sizeDelta = new Vector2(330f, 86f);
            brt.anchoredPosition = new Vector2(0f, 10f);
            var bubbleBorder = _bubble.GetComponent<Image>();
            bubbleBorder.sprite = UiShapes.Rounded;
            bubbleBorder.type = Image.Type.Sliced;
            bubbleBorder.color = Palette.Ink;
            bubbleBorder.raycastTarget = false;
            var bubbleFill = Child(brt, "Fill", UiShapes.Rounded, UiKit.BorderWidth);
            bubbleFill.type = Image.Type.Sliced;
            bubbleFill.color = Palette.PaperLight;
            _bubbleText = UiKit.CreateLabel(_bubble.transform, string.Empty, 40f);
            var trt = _bubbleText.rectTransform;
            trt.anchorMin = Vector2.zero;
            trt.anchorMax = Vector2.one;
            trt.offsetMin = new Vector2(14f, 6f);
            trt.offsetMax = new Vector2(-14f, -6f);
            _bubble.SetActive(false);
        }

        private static Image Child(RectTransform parent, string name, Sprite sprite, float inset)
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
            img.raycastTarget = false;
            return img;
        }

        /// <summary>
        /// Nhảy hai nhịp và hiện bong bóng <paramref name="bubble"/> trong <see cref="BubbleSeconds"/> giây
        /// (<paramref name="keepBubble"/>: để bong bóng ở lại, như ở cuối cảnh học xong bài).
        /// </summary>
        public void Cheer(string bubble, bool keepBubble = false)
        {
            LastMood = MascotMood.Cheer;
            Hop();
            ShowBubble(bubble, keepBubble);
        }

        /// <summary>Nghiêng đầu như đang nghĩ (khi bé chọn sai); không có bong bóng, không có tiếng.</summary>
        public void Ponder()
        {
            LastMood = MascotMood.Ponder;
            HideBubble();
            _ = Motion.Wiggle(_body, 12f, .6f);
        }

        private async void Hop()
        {
            var height = ((RectTransform)transform).rect.height;
            foreach (var jump in new[] { .18f, .1f })
            {
                await Motion.MoveTo(_body, new Vector2(0f, height * jump), .12f);
                if (this == null) return;
                await Motion.MoveTo(_body, Vector2.zero, .12f);
                if (this == null) return;
            }
        }

        private async void ShowBubble(string text, bool keep)
        {
            var gen = ++_bubbleGeneration;
            _bubbleText.text = text ?? string.Empty;
            _bubble.SetActive(true);
            _bubble.transform.localScale = Vector3.one * .3f;
            _ = Motion.ScaleTo(_bubble.transform, 1f, .15f);
            if (keep) return;
            await Awaitable.WaitForSecondsAsync(BubbleSeconds * Motion.Scale);
            if (this != null && gen == _bubbleGeneration) HideBubble();
        }

        private void HideBubble()
        {
            _bubbleGeneration++;
            if (_bubble != null) _bubble.SetActive(false);
        }
    }
}
