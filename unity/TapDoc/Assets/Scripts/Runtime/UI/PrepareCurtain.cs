using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Màn chuyển phủ lên trên cùng trong lúc app chuẩn bị bài (nạp tranh, âm thanh): nền giấy, bạn gà con ở giữa.
    /// Hiện mờ vào, chặn mọi lần chạm; <see cref="HideAsync"/> chờ đủ <see cref="MinSeconds"/> kể từ lúc hiện (để
    /// không chớp khi nạp quá nhanh) rồi mờ ra. Tắt hiệu ứng (<see cref="Motion.Scale"/> = 0) thì hiện, tắt ngay.
    /// </summary>
    public sealed class PrepareCurtain : MonoBehaviour
    {
        public const float MinSeconds = .4f;
        public const float FadeSeconds = .15f;
        public const float MascotSize = 280f;

        private CanvasGroup _group;
        private Mascot _mascot;
        private float _shownAt;
        private int _generation;

        public bool IsShowing => gameObject.activeSelf;

        internal static PrepareCurtain Create(Transform parent, AssetCatalog assets)
        {
            var go = new GameObject("PrepareCurtain", typeof(RectTransform), typeof(Image), typeof(CanvasGroup));
            go.transform.SetParent(parent, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            var paper = go.GetComponent<Image>();
            paper.sprite = UiKit.WhiteSprite;
            paper.color = Palette.Paper;
            paper.raycastTarget = true; // chặn chạm trong lúc chuẩn bị

            var curtain = go.AddComponent<PrepareCurtain>();
            curtain._group = go.GetComponent<CanvasGroup>();
            curtain._mascot = Mascot.Create(go.transform, assets, MascotSize);
            var mrt = (RectTransform)curtain._mascot.transform;
            mrt.anchorMin = mrt.anchorMax = new Vector2(.5f, .5f);
            mrt.anchoredPosition = Vector2.zero;
            go.SetActive(false);
            return curtain;
        }

        public void Show()
        {
            _generation++;
            _shownAt = Time.realtimeSinceStartup;
            transform.SetAsLastSibling();
            gameObject.SetActive(true);
            _group.alpha = 0f;
            _ = Motion.Fade(_group, 1f, FadeSeconds);
            _ = Motion.Punch(_mascot.transform, 1.08f, .3f);
        }

        /// <summary>Tắt ngay, không chờ.</summary>
        public void Hide()
        {
            _generation++;
            gameObject.SetActive(false);
        }

        /// <summary>Chờ đủ thời gian tối thiểu, mờ ra rồi tắt. Bị <see cref="Show"/> lần nữa chen ngang thì thôi.</summary>
        public async Awaitable HideAsync()
        {
            var gen = ++_generation;
            transform.SetAsLastSibling(); // màn mới vừa dựng nằm trên cùng: đưa màn chuyển lên lại để mờ ra
            var remaining = MinSeconds * Motion.Scale - (Time.realtimeSinceStartup - _shownAt);
            while (remaining > 0f)
            {
                await Awaitable.NextFrameAsync();
                if (this == null || gen != _generation) return;
                remaining = MinSeconds * Motion.Scale - (Time.realtimeSinceStartup - _shownAt);
            }
            await Motion.Fade(_group, 0f, FadeSeconds);
            if (this == null || gen != _generation) return;
            gameObject.SetActive(false);
        }
    }
}
