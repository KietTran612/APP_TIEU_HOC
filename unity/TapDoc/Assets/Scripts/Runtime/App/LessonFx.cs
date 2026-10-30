using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Hiệu ứng phản hồi trong màn học (bản thiết kế giao diện mục 6): bé làm đúng thì sao giấy bung ra, tiếng "ting" và gà
    /// con khen; bé chọn sai thì thẻ lắc nhẹ và gà con nghiêng đầu, không màu đỏ, không tiếng chê. Chỉ là lớp trang trí:
    /// không đổi cách chấm đúng sai hay luồng bài. Mọi hàm an toàn khi thiếu kênh tiếng hay gà con.
    /// </summary>
    public class LessonFx
    {
        public const int SparkCount = 5;
        private const float SparkSize = 56f;
        private const float SparkDistance = 150f;
        private const float SparkSeconds = .6f;

        private readonly RectTransform _overlay;
        private readonly AssetCatalog _assets;
        private readonly SfxPlayer _sfx;
        private readonly Mascot _mascot;

        public LessonFx(RectTransform overlay, AssetCatalog assets, SfxPlayer sfx, Mascot mascot)
        {
            _overlay = overlay;
            _assets = assets;
            _sfx = sfx;
            _mascot = mascot;
        }

        /// <summary>Số sao giấy đang bay (cho test).</summary>
        public int ActiveSparks { get; private set; }

        /// <summary>Bé làm đúng: sao giấy bung ra từ <paramref name="at"/>, tiếng "ting", gà con khen.</summary>
        public void Correct(RectTransform at)
        {
            if (_sfx != null) _sfx.Play(SystemSfx.Correct);
            if (_mascot != null) _mascot.Cheer(UiText.MascotCorrect);
            if (_overlay == null || at == null) return;
            var center = (Vector2)_overlay.InverseTransformPoint(at.TransformPoint(at.rect.center));
            for (var i = 0; i < SparkCount; i++) Spark(center, 90f + i * 360f / SparkCount);
        }

        /// <summary>Bé chọn sai: thẻ lắc nhẹ về chỗ cũ, gà con nghiêng đầu; không có tiếng.</summary>
        public void Wrong(RectTransform chosen)
        {
            if (chosen != null) _ = Motion.Shake(chosen, 18f, .3f);
            if (_mascot != null) _mascot.Ponder();
        }

        /// <summary>Các thẻ nhập thành tiếng: tiếng "bụp" (gọi trong khoảng nghỉ trước mảnh tiếng đã ghép).</summary>
        public void Merge()
        {
            if (_sfx != null) _sfx.Play(SystemSfx.Merge);
        }

        private async void Spark(Vector2 center, float angleDeg)
        {
            var go = new GameObject("Spark", typeof(RectTransform), typeof(Image), typeof(CanvasGroup));
            go.transform.SetParent(_overlay, false);
            var rt = (RectTransform)go.transform;
            rt.sizeDelta = new Vector2(SparkSize, SparkSize);
            rt.anchoredPosition = center;
            var img = go.GetComponent<Image>();
            img.sprite = _assets?.Image(SystemIcons.PaperStar);
            img.preserveAspect = true;
            img.raycastTarget = false;
            img.enabled = img.sprite != null;
            ActiveSparks++;
            var dir = new Vector2(Mathf.Cos(angleDeg * Mathf.Deg2Rad), Mathf.Sin(angleDeg * Mathf.Deg2Rad));
            _ = Motion.Wiggle(rt, 30f, SparkSeconds);
            _ = Motion.Fade(go.GetComponent<CanvasGroup>(), 0f, SparkSeconds);
            await Motion.MoveTo(rt, center + dir * SparkDistance, SparkSeconds);
            ActiveSparks--;
            if (go != null) Object.Destroy(go);
        }
    }
}
