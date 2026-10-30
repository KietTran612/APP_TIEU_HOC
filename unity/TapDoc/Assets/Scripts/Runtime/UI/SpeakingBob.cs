using UnityEngine;

namespace TapDoc
{
    /// <summary>Nút loa nhún nhẹ theo nhịp trong lúc giọng đọc đang phát; im thì về cỡ 1.</summary>
    public class SpeakingBob : MonoBehaviour
    {
        private const float Amplitude = .06f;
        private const float Rate = 2f; // nhịp mỗi giây

        private SpeechPlayer _speech;
        private float _time;
        private bool _bobbing;

        public void Init(SpeechPlayer speech) => _speech = speech;

        private void Update()
        {
            var speaking = _speech != null && _speech.IsBusy && Motion.Scale > 0f;
            if (speaking)
            {
                _time += Time.unscaledDeltaTime;
                transform.localScale = Vector3.one * (1f + Amplitude * Mathf.Abs(Mathf.Sin(Mathf.PI * Rate * _time)));
                _bobbing = true;
            }
            else if (_bobbing)
            {
                _bobbing = false;
                _time = 0f;
                transform.localScale = Vector3.one;
            }
        }
    }
}
