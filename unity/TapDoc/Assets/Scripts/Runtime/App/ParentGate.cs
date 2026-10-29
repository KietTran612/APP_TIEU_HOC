using System;
using System.Collections.Generic;
using System.Linq;

namespace TapDoc
{
    /// <summary>
    /// Khóa màn phụ huynh bằng một phép cộng hai số có hai chữ số (11–49), chọn đáp án trong 3 số. Bấm sai thì đổi
    /// sang phép tính mới; không đếm số lần sai và không bao giờ khóa cứng.
    /// </summary>
    public class ParentGate
    {
        private const int Min = 11;
        private const int Max = 49;

        // Đáp án nhiễu: lệch vài đơn vị hoặc một chục so với đáp án đúng (dễ nhầm nếu bấm bừa, nhưng người lớn tính ra ngay).
        private static readonly int[] Offsets = { -11, -10, -9, -2, -1, 1, 2, 9, 10, 11 };

        private readonly Random _rng;
        private int _a;
        private int _b;
        private List<int> _choices = new();

        public ParentGate(Random rng)
        {
            _rng = rng ?? throw new ArgumentNullException(nameof(rng));
            NewQuestion();
        }

        /// <summary>Phép tính dạng "a + b = ?".</summary>
        public string Question => $"{_a} + {_b} = ?";

        /// <summary>3 số khác nhau, đúng một số là đáp án, thứ tự đã xáo.</summary>
        public IReadOnlyList<int> Choices => _choices;

        internal int Expected => _a + _b;

        /// <summary>Đúng thì trả <c>true</c>. Sai thì trả <c>false</c> và đổi sang phép tính mới.</summary>
        public bool Answer(int value)
        {
            if (value == Expected) return true;
            NewQuestion();
            return false;
        }

        private void NewQuestion()
        {
            var previous = _choices.Count > 0 ? Question : null;
            do
            {
                _a = _rng.Next(Min, Max + 1);
                _b = _rng.Next(Min, Max + 1);
            }
            while (Question == previous);

            var wrong = Offsets.OrderBy(_ => _rng.Next()).Take(2).Select(d => Expected + d);
            _choices = wrong.Append(Expected).OrderBy(_ => _rng.Next()).ToList();
        }
    }
}
