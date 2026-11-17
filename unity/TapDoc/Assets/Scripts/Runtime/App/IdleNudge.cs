using System;
using System.Collections.Generic;
using UnityEngine;

namespace TapDoc
{
    /// <summary>Kiểu nhắc của bước đang học (bản thiết kế nâng cấp UI mục 4.1.3).</summary>
    public enum NudgeKind
    {
        /// <summary>Không nhắc.</summary>
        None,

        /// <summary>Bước bấm chọn và mọi lượt Phần 2: đọc lại lời dẫn rồi mới hiện bàn tay.</summary>
        Tap,

        /// <summary>Bước bé tự đọc (hoặc bước đã xong, chỉ còn bấm Tiếp): không đọc lại lời dẫn, chỉ hiện bàn tay.</summary>
        Read
    }

    /// <summary>
    /// Nhắc khi bé ngồi im (bản thiết kế nâng cấp UI mục 4.1.3). Bộ đếm tính từ lần chạm cuối hoặc từ lúc giọng đọc
    /// dừng; không nhắc khi giọng đọc đang chạy; tối đa <see cref="MaxNudges"/> lần mỗi bước. Lớp thuần, đồng hồ do
    /// người gọi truyền vào (màn học gọi <see cref="Tick"/> mỗi khung hình).
    /// </summary>
    public sealed class IdleNudge
    {
        public const float TapRepromptSeconds = 12f;
        public const float TapHandSeconds = 24f;
        public const float ReadHandSeconds = 30f;
        public const int MaxNudges = 2;

        /// <summary>
        /// Bật nhắc ở màn học. Test của app tắt mặc định (<c>AppTestBase</c>) để nhắc theo thời gian thật không chen
        /// vào luồng test; test của nhắc bật lại và dùng đồng hồ giả.
        /// </summary>
        public static bool Enabled = true;

        /// <summary>Các loại bước bé tự đọc: nhắc kiểu <see cref="NudgeKind.Read"/>, không đọc lại lời dẫn.</summary>
        public static readonly IReadOnlyCollection<string> SelfReadTypes = new HashSet<string>
        {
            "sentence", "passage", "memorize", "reading", "words", "title", "question"
        };

        private readonly Action _reprompt;
        private readonly Action<RectTransform> _showHand;
        private readonly Action _hideHand;

        private float _since;
        private NudgeKind _kind;
        private RectTransform _target;
        private bool _started;

        public IdleNudge(Action reprompt, Action<RectTransform> showHand, Action hideHand)
        {
            _reprompt = reprompt;
            _showHand = showHand;
            _hideHand = hideHand;
        }

        /// <summary>Số lần đã nhắc ở bước này (kể từ lần chạm cuối).</summary>
        public int Count { get; private set; }

        /// <summary>Bàn tay gợi ý đang hiện.</summary>
        public bool HandShown { get; private set; }

        /// <summary>Bước mới: đếm lại từ <paramref name="now"/>.</summary>
        public void ResetStep(float now) => Restart(now);

        /// <summary>Bé vừa chạm: ẩn bàn tay, đếm lại từ <paramref name="now"/>.</summary>
        public void NoteActivity(float now) => Restart(now);

        /// <summary>
        /// Gọi mỗi khung hình. Đổi <paramref name="kind"/> hay <paramref name="handTarget"/> (ví dụ nút Tiếp vừa hiện)
        /// thì đếm lại từ <paramref name="now"/>.
        /// </summary>
        public void Tick(float now, bool speaking, NudgeKind kind, RectTransform handTarget)
        {
            if (!_started || kind != _kind || handTarget != _target)
            {
                Restart(now);
                _kind = kind;
                _target = handTarget;
                _started = true;
            }
            if (speaking)
            {
                // Giọng đọc đang chạy: chưa tính là ngồi im.
                _since = now;
                return;
            }
            if (_kind == NudgeKind.None || Count >= MaxNudges) return;

            var idle = now - _since;
            if (_kind == NudgeKind.Tap)
            {
                if (Count == 0 && idle >= TapRepromptSeconds)
                {
                    Count = 1;
                    _reprompt?.Invoke();
                }
                else if (Count == 1 && idle >= TapHandSeconds)
                {
                    Count = 2;
                    ShowHand();
                }
            }
            else if (Count == 0 && idle >= ReadHandSeconds)
            {
                // Bước tự đọc chỉ có một lần nhắc (bàn tay); coi như đã dùng hết lượt nhắc.
                Count = MaxNudges;
                ShowHand();
            }
        }

        private void ShowHand()
        {
            if (_target == null) return;
            HandShown = true;
            _showHand?.Invoke(_target);
        }

        private void Restart(float now)
        {
            _since = now;
            Count = 0;
            if (HandShown)
            {
                HandShown = false;
                _hideHand?.Invoke();
            }
        }
    }
}
