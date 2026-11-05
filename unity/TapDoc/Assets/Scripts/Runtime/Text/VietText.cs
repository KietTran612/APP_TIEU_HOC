using System.Text;

namespace TapDoc
{
    /// <summary>Tiện ích chữ tiếng Việt dùng ở màn: bỏ dấu thanh (giữ dấu mũ, dấu móc, dấu trăng).</summary>
    public static class VietText
    {
        // Dấu thanh ở dạng tổ hợp sau khi phân rã NFD: huyền, sắc, ngã, hỏi, nặng.
        private static bool IsToneMark(char c) => c == '̀' || c == '́' || c == '̃' || c == '̉' || c == '̣';

        public static string StripTone(string text)
        {
            if (string.IsNullOrEmpty(text)) return text ?? string.Empty;
            var decomposed = text.Normalize(NormalizationForm.FormD);
            var sb = new StringBuilder(decomposed.Length);
            foreach (var c in decomposed)
            {
                if (!IsToneMark(c)) sb.Append(c);
            }
            return sb.ToString().Normalize(NormalizationForm.FormC);
        }
    }
}
