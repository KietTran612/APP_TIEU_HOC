using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Nhún chậm lặp lại (bài đang học tới, nút "Tiếp", thẻ gợi ý). Khi <see cref="Motion.Scale"/> bằng 0 thì vẫn ghi
    /// nhận là đang nhún nhưng không đổi cỡ, để ảnh chụp trong test ổn định.
    /// </summary>
    public class Pulse : MonoBehaviour
    {
        private float _amplitude;
        private float _period;
        private float _time;

        /// <summary>Bắt đầu nhún <paramref name="t"/>: cỡ dao động quanh 1 với biên độ <paramref name="amplitude"/>.</summary>
        public static Pulse StartOn(Transform t, float amplitude = .06f, float period = 1.6f)
        {
            var pulse = t.GetComponent<Pulse>();
            if (pulse == null) pulse = t.gameObject.AddComponent<Pulse>();
            pulse._amplitude = amplitude;
            pulse._period = Mathf.Max(period, .01f);
            pulse._time = 0f;
            pulse.enabled = true;
            return pulse;
        }

        /// <summary>Dừng nhún và trả cỡ về 1.</summary>
        public static void StopOn(Transform t)
        {
            var pulse = t != null ? t.GetComponent<Pulse>() : null;
            if (pulse == null) return;
            pulse.enabled = false;
            t.localScale = Vector3.one;
        }

        public static bool IsRunning(Transform t)
        {
            var pulse = t != null ? t.GetComponent<Pulse>() : null;
            return pulse != null && pulse.enabled;
        }

        private void Update()
        {
            if (Motion.Scale <= 0f) return;
            _time += Time.unscaledDeltaTime;
            transform.localScale = Vector3.one * (1f + _amplitude * Mathf.Sin(2f * Mathf.PI * _time / _period));
        }
    }
}
