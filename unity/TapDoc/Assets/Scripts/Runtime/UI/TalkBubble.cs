using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Bong bóng nhỏ cạnh gà con khi giọng đọc đang chạy: chỉ có hình loa, không có chữ, nhún theo nhịp đọc (bản thiết kế
    /// nâng cấp UI mục 4.1.2). Ẩn khi bong bóng khen của gà con đang hiện.
    /// </summary>
    public class TalkBubble : MonoBehaviour
    {
        public static readonly Vector2 Size = new(110f, 84f);

        private SpeechPlayer _speech;
        private Mascot _mascot;
        private GameObject _body;

        public bool IsShown => _body != null && _body.activeSelf;

        public static TalkBubble Attach(Mascot mascot, SpeechPlayer speech, AssetCatalog assets)
        {
            var bubble = mascot.gameObject.AddComponent<TalkBubble>();
            bubble._speech = speech;
            bubble._mascot = mascot;
            bubble.Build(assets);
            return bubble;
        }

        private void Build(AssetCatalog assets)
        {
            _body = new GameObject("TalkBubble", typeof(RectTransform), typeof(Image));
            _body.transform.SetParent(transform, false);
            var border = _body.GetComponent<Image>();
            border.sprite = UiShapes.Rounded;
            border.type = Image.Type.Sliced;
            border.color = Palette.Ink;
            border.raycastTarget = false;
            var fill = UiKit.AddFill(_body.transform, UiShapes.Rounded, Palette.PaperLight);
            fill.raycastTarget = false;
            var icon = new GameObject("Speaker", typeof(RectTransform), typeof(Image));
            icon.transform.SetParent(_body.transform, false);
            var irt = (RectTransform)icon.transform;
            irt.anchorMin = irt.anchorMax = new Vector2(.5f, .5f);
            irt.sizeDelta = new Vector2(64f, 64f);
            var img = icon.GetComponent<Image>();
            img.sprite = assets?.Image(SystemIcons.Speaker);
            img.preserveAspect = true;
            img.raycastTarget = false;
            img.enabled = img.sprite != null;
            if (_speech != null) _body.AddComponent<SpeakingBob>().Init(_speech);
            SetAbove(true);
            _body.SetActive(false);
        }

        /// <summary>
        /// <paramref name="above"/>: bong bóng nằm trên đầu gà con (gà con ở dải mép); ngược lại nằm bên trái gà con
        /// (gà con ở góc dưới, phía trên là phần học).
        /// </summary>
        public void SetAbove(bool above)
        {
            var rt = (RectTransform)_body.transform;
            rt.sizeDelta = Size;
            if (above)
            {
                rt.anchorMin = rt.anchorMax = new Vector2(.5f, 1f);
                rt.pivot = new Vector2(.5f, 0f);
                rt.anchoredPosition = new Vector2(0f, 8f);
            }
            else
            {
                rt.anchorMin = rt.anchorMax = new Vector2(0f, .5f);
                rt.pivot = new Vector2(1f, .5f);
                rt.anchoredPosition = new Vector2(-8f, 0f);
            }
        }

        private void Update()
        {
            var show = _speech != null && _speech.IsBusy && (_mascot == null || !_mascot.IsBubbleShown);
            if (_body.activeSelf != show) _body.SetActive(show);
        }
    }
}
