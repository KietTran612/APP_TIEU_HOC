using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace TapDoc
{
    public static class TextStyler
    {
        public const string HighlightColor = "#1F8A9E";

        public static string Apply(string text, List<Span> hl)
        {
            if (string.IsNullOrEmpty(text) || hl == null || hl.Count == 0)
            {
                return text ?? string.Empty;
            }

            var ordered = hl
                .Where(span => span != null && span.n > 0 && span.s >= 0 && span.s + span.n <= text.Length)
                .OrderBy(span => span.s)
                .ToList();

            if (ordered.Count == 0)
            {
                return text;
            }

            var sb = new StringBuilder();
            var cursor = 0;
            foreach (var span in ordered)
            {
                if (span.s < cursor) continue;
                if (span.s > cursor)
                {
                    sb.Append(text, cursor, span.s - cursor);
                }
                sb.Append($"<color={HighlightColor}>");
                sb.Append(text, span.s, span.n);
                sb.Append("</color>");
                cursor = span.s + span.n;
            }

            if (cursor < text.Length)
            {
                sb.Append(text, cursor, text.Length - cursor);
            }

            return sb.ToString();
        }
    }
}
