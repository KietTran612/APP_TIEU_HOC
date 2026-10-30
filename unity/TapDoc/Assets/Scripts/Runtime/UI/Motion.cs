using System;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Bộ chạy hiệu ứng nhỏ của giao diện (bản thiết kế giao diện mục 6). Mỗi đối tượng có 4 kênh riêng: cỡ, vị trí,
    /// độ trong, góc xoay; hiệu ứng mới trên cùng kênh huỷ hiệu ứng cũ và bắt đầu từ trạng thái hiện tại. Đối tượng bị
    /// huỷ giữa chừng thì hiệu ứng thoát êm. <see cref="Scale"/> nhân vào mọi thời lượng: bằng 0 thì nhảy ngay tới
    /// trạng thái cuối (test dùng để chạy nhanh và chụp ảnh ổn định).
    /// </summary>
    public static class Motion
    {
        /// <summary>Hệ số thời lượng; 0 tắt hiệu ứng (trạng thái cuối áp ngay).</summary>
        public static float Scale = 1f;

        /// <summary>Độ đậm tối đa của lớp tối phủ lên trang đang lật.</summary>
        public const float PageShadeAlpha = .35f;

        private const string PageShadeName = "PageShade";

        public static Awaitable ScaleTo(Transform t, float to, float seconds)
        {
            var from = t.localScale;
            var target = Vector3.one * to;
            return Run(t, MotionChannel.Scale, seconds, p => t.localScale = Vector3.LerpUnclamped(from, target, EaseOut(p)));
        }

        /// <summary>Phồng lên <paramref name="peak"/> rồi về cỡ 1.</summary>
        public static Awaitable Punch(Transform t, float peak, float seconds)
        {
            var from = t.localScale;
            var top = Vector3.one * peak;
            return Run(t, MotionChannel.Scale, seconds, p => t.localScale = p < .5f
                ? Vector3.LerpUnclamped(from, top, EaseOut(p * 2f))
                : Vector3.LerpUnclamped(top, Vector3.one, EaseOut((p - .5f) * 2f)));
        }

        /// <summary>
        /// Lắc ngang quanh chỗ cũ, biên độ nhỏ dần, rồi về đúng chỗ cũ. Lắc chồng lên lần lắc đang chạy (bé chạm sai liên
        /// tiếp) thì vẫn lấy chỗ gốc của lần đầu, để thẻ không bị lệch.
        /// </summary>
        public static Awaitable Shake(RectTransform t, float amplitude, float seconds)
        {
            var state = MotionState.For(t.gameObject);
            var home = state.ShakeHome ?? t.anchoredPosition;
            state.ShakeHome = home;
            return Run(t, MotionChannel.Position, seconds, p =>
            {
                if (p >= 1f)
                {
                    t.anchoredPosition = home;
                    state.ShakeHome = null;
                    return;
                }
                t.anchoredPosition = home + new Vector2(amplitude * Mathf.Sin(p * Mathf.PI * 6f) * (1f - p), 0f);
            });
        }

        public static Awaitable MoveTo(RectTransform t, Vector2 anchored, float seconds)
        {
            MotionState.For(t.gameObject).ShakeHome = null; // dời đi chỗ khác thì bỏ chỗ gốc của lần lắc dở
            var from = t.anchoredPosition;
            return Run(t, MotionChannel.Position, seconds, p => t.anchoredPosition = Vector2.LerpUnclamped(from, anchored, EaseOut(p)));
        }

        public static Awaitable Fade(CanvasGroup g, float to, float seconds)
        {
            var from = g.alpha;
            return Run(g, MotionChannel.Alpha, seconds, p => g.alpha = Mathf.Lerp(from, to, p));
        }

        /// <summary>Xoay qua lại quanh trục Z, biên độ nhỏ dần, rồi về thẳng.</summary>
        public static Awaitable Wiggle(Transform t, float degrees, float seconds) =>
            Run(t, MotionChannel.Rotation, seconds, p => t.localRotation =
                Quaternion.Euler(0f, 0f, p >= 1f ? 0f : degrees * Mathf.Sin(p * Mathf.PI * 4f) * (1f - p)));

        /// <summary>
        /// Lật trang sách: trang co dần về phía gáy (mép trái khi <paramref name="hingeLeft"/>, mép phải khi lật lùi),
        /// mép gáy đứng yên, trang tối dần. Xong thì để nguyên trạng thái đã lật; người gọi tự huỷ trang.
        /// </summary>
        public static Awaitable PageTurn(RectTransform page, float seconds, bool hingeLeft = true)
        {
            // Dời pivot về mép gáy mà không dịch hình: đo góc dưới trái trước và sau khi đổi pivot rồi bù lại (đúng cho
            // cả khung neo một điểm lẫn khung giãn theo cha).
            var corners = new Vector3[4];
            page.GetWorldCorners(corners);
            var before = corners[0];
            page.pivot = new Vector2(hingeLeft ? 0f : 1f, page.pivot.y);
            page.GetWorldCorners(corners);
            page.position += before - corners[0];

            // Không dùng ?. / ?? với đối tượng Unity (đối tượng đã huỷ vẫn khác null với C#).
            var existing = page.Find(PageShadeName);
            var shade = existing != null ? existing.GetComponent<Image>() : CreateShade(page);
            shade.transform.SetAsLastSibling();
            var from = page.localScale;
            return Run(page, MotionChannel.Scale, seconds, p =>
            {
                var e = p * p; // ease-in: lật chậm lúc đầu, nhanh dần
                page.localScale = new Vector3(Mathf.Lerp(from.x, 0f, e), from.y, from.z);
                if (shade != null) shade.color = new Color(Palette.Ink.r, Palette.Ink.g, Palette.Ink.b, PageShadeAlpha * e);
            });
        }

        private static Image CreateShade(RectTransform page)
        {
            var go = new GameObject(PageShadeName, typeof(RectTransform), typeof(Image));
            go.transform.SetParent(page, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            var img = go.GetComponent<Image>();
            img.raycastTarget = false;
            img.color = Color.clear;
            return img;
        }

        private static float EaseOut(float p) => 1f - (1f - p) * (1f - p);

        /// <summary>
        /// Chạy <paramref name="apply"/>(tiến độ 0..1) mỗi khung hình trong <paramref name="seconds"/> × <see cref="Scale"/>.
        /// Luôn gọi <c>apply(1)</c> ở cuối, trừ khi bị huỷ (đối tượng bị huỷ hoặc hiệu ứng mới trên cùng kênh).
        /// </summary>
        private static async Awaitable Run(Component target, MotionChannel channel, float seconds, Action<float> apply)
        {
            if (target == null) return;
            var state = MotionState.For(target.gameObject);
            var gen = state.Begin(channel);
            var duration = seconds * Scale;
            if (duration <= 0f)
            {
                apply(1f);
                return;
            }

            var elapsed = 0f;
            while (elapsed < duration)
            {
                await Awaitable.NextFrameAsync();
                if (target == null || state == null || !state.IsCurrent(channel, gen)) return;
                elapsed += Time.unscaledDeltaTime;
                apply(Mathf.Clamp01(elapsed / duration));
            }
        }
    }

    internal enum MotionChannel
    {
        Scale,
        Position,
        Alpha,
        Rotation
    }

    /// <summary>Số thế hệ của từng kênh hiệu ứng trên một đối tượng; hiệu ứng mới tăng số, hiệu ứng cũ thấy khác thì dừng.</summary>
    internal sealed class MotionState : MonoBehaviour
    {
        private readonly int[] _generation = new int[4];

        /// <summary>Chỗ gốc của lần lắc đang chạy; <c>null</c> khi không lắc.</summary>
        public Vector2? ShakeHome;

        public static MotionState For(GameObject go)
        {
            var state = go.GetComponent<MotionState>();
            if (state == null)
            {
                state = go.AddComponent<MotionState>();
                state.hideFlags = HideFlags.HideInInspector;
            }
            return state;
        }

        public int Begin(MotionChannel channel) => ++_generation[(int)channel];

        public bool IsCurrent(MotionChannel channel, int gen) => _generation[(int)channel] == gen;
    }
}
