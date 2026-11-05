using System;
using System.Collections.Generic;
using System.Text;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>Cách hiện một tiếng trong bài đọc.</summary>
    public enum WordLook
    {
        Normal,
        /// <summary>Câu đang được đọc: nền cam nhạt.</summary>
        Reading,
        /// <summary>Tiếng bé đã tìm đúng: tô phần được hỏi (vần, âm đầu, dấu) và nền cam nhạt.</summary>
        Found,
        /// <summary>Tiếng gợi ý sau hai lần chạm chưa đúng: nền vàng.</summary>
        Hint,
        /// <summary>Tiếng bị che khi học thuộc lòng: ô màu giấy đậm, chữ trong suốt (giữ chỗ, không xô dòng).</summary>
        Hidden,
    }

    /// <summary>
    /// Bài đọc hiện như chữ trên trang sách (thiết kế tập 2, mục 7.2): câu văn nối nhau thành đoạn, thơ mỗi dòng một câu.
    /// Bé chạm vào tiếng nào thì báo <see cref="WordTapped"/> với chỉ số tiếng trong bước. Bài dài tự chia trang theo
    /// chiều cao vùng chữ; cả một câu luôn nằm trên cùng một trang.
    /// </summary>
    public class ReadingText : MonoBehaviour, IPointerClickHandler
    {
        private const string ReadingMark = "<mark=#F6C77A88>";
        private const string FoundMark = "<mark=#F6C77A55>";
        private const string HintMark = "<mark=#FFE08ACC>";
        private const string HiddenMark = "<mark=#D9C9A8FF>";

        public event Action<int> WordTapped;

        private TextMeshProUGUI _label;
        private List<Item> _rows;
        private List<Item> _words;
        private bool _poem;
        private readonly List<List<int>> _pages = new();      // mỗi trang: các chỉ số câu
        private readonly List<int> _tmpToWord = new();        // từ thứ k của TMP trên trang -> chỉ số tiếng
        private Func<int, WordLook> _look = _ => WordLook.Normal;

        public int PageCount => _pages.Count;
        public int Page { get; private set; }
        internal TextMeshProUGUI Label => _label;

        /// <summary>Tạo khối chữ phủ vùng <paramref name="area"/> (kích thước, tâm lệch so với giữa cha).</summary>
        public static ReadingText Create(Transform parent, List<Item> rows, List<Item> words, bool poem,
            Vector2 size, Vector2 center, float fontSize)
        {
            var go = new GameObject("ReadingText", typeof(RectTransform), typeof(Image), typeof(ReadingText));
            go.transform.SetParent(parent, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = size;
            rt.anchoredPosition = center;
            var hit = go.GetComponent<Image>();
            hit.color = Color.clear; // chỉ để nhận chạm
            var label = UiKit.CreateLabel(go.transform, string.Empty, fontSize);
            var lrt = label.rectTransform;
            lrt.anchorMin = Vector2.zero;
            lrt.anchorMax = Vector2.one;
            lrt.offsetMin = lrt.offsetMax = Vector2.zero;
            label.enableAutoSizing = false;
            label.fontSize = fontSize;
            label.alignment = poem ? TextAlignmentOptions.Top : TextAlignmentOptions.TopLeft;
            label.lineSpacing = -14f;
            label.textWrappingMode = TextWrappingModes.Normal;
            label.overflowMode = TextOverflowModes.Overflow;
            label.raycastTarget = false;
            var reading = go.GetComponent<ReadingText>();
            reading._label = label;
            reading._rows = rows;
            reading._words = words;
            reading._poem = poem;
            reading.Paginate(size);
            reading.ShowPage(0);
            return reading;
        }

        /// <summary>Đặt cách hiện từng tiếng rồi vẽ lại trang đang mở.</summary>
        public void SetLook(Func<int, WordLook> look)
        {
            _look = look ?? (_ => WordLook.Normal);
            Render();
        }

        public void Refresh() => Render();

        public void ShowPage(int page)
        {
            Page = Mathf.Clamp(page, 0, Mathf.Max(0, _pages.Count - 1));
            Render();
        }

        public int PageOfSentence(int sentence)
        {
            for (var p = 0; p < _pages.Count; p++)
                if (_pages[p].Contains(sentence)) return p;
            return 0;
        }

        public int PageOfWord(int word) => PageOfSentence(_words[word].row);

        /// <summary>Các tiếng của câu <paramref name="sentence"/>, theo thứ tự.</summary>
        public IEnumerable<int> WordsOf(int sentence)
        {
            for (var i = 0; i < _words.Count; i++)
                if (_words[i].row == sentence) yield return i;
        }

        public void OnPointerClick(PointerEventData eventData)
        {
            if (eventData == null || _label == null) return;
            var canvas = _label.canvas;
            var cam = canvas == null || canvas.renderMode == RenderMode.ScreenSpaceOverlay ? null : canvas.worldCamera;
            var k = TMP_TextUtilities.FindIntersectingWord(_label, eventData.position, cam);
            if (k < 0 || k >= _tmpToWord.Count || _tmpToWord[k] < 0) return;
            WordTapped?.Invoke(_tmpToWord[k]);
        }

        /// <summary>Cho test: chạm vào tiếng thứ <paramref name="word"/> (mở đúng trang trước).</summary>
        internal void SimulateTapWord(int word)
        {
            if (PageOfWord(word) != Page) ShowPage(PageOfWord(word));
            WordTapped?.Invoke(word);
        }

        /// <summary>Chuỗi có thẻ định dạng của trang đang mở (cho test).</summary>
        internal string RenderedText => _label.text;

        internal bool OnCurrentPage(int word) => _pages.Count > 0 && _pages[Page].Contains(_words[word].row);

        // ---- chia trang ----

        private void Paginate(Vector2 size)
        {
            _pages.Clear();
            var current = new List<int>();
            for (var s = 0; s < _rows.Count; s++)
            {
                current.Add(s);
                var height = _label.GetPreferredValues(Compose(current, plain: true), size.x, 0f).y;
                if (height > size.y && current.Count > 1)
                {
                    current.RemoveAt(current.Count - 1);
                    _pages.Add(current);
                    current = new List<int> { s };
                }
            }
            if (current.Count > 0) _pages.Add(current);
        }

        // ---- vẽ ----

        private void Render()
        {
            if (_label == null || _pages.Count == 0) return;
            _label.text = Compose(_pages[Page], plain: false);
            _label.ForceMeshUpdate();
            MapWords();
        }

        /// <summary>
        /// Ghép các câu của trang: thơ mỗi câu một dòng; văn nối câu trong cùng đoạn, đoạn mới (<c>row</c> khác) xuống dòng.
        /// </summary>
        private string Compose(List<int> sentences, bool plain)
        {
            var sb = new StringBuilder();
            for (var k = 0; k < sentences.Count; k++)
            {
                var s = sentences[k];
                if (k > 0)
                {
                    var newParagraph = _rows[s].row != _rows[sentences[k - 1]].row;
                    sb.Append(_poem ? (newParagraph ? "\n\n" : "\n") : (newParagraph ? "\n" : " "));
                }
                sb.Append(plain ? _rows[s].text : StyledSentence(s));
            }
            return sb.ToString();
        }

        /// <summary>Câu gốc (giữ dấu câu như sách), mỗi tiếng bọc thẻ theo <see cref="WordLook"/>.</summary>
        private string StyledSentence(int sentence)
        {
            var text = _rows[sentence].text;
            var sb = new StringBuilder();
            var cursor = 0;
            foreach (var w in WordsOf(sentence))
            {
                var word = _words[w];
                var at = text.IndexOf(word.text, cursor, StringComparison.Ordinal);
                if (at < 0) continue;
                sb.Append(text, cursor, at - cursor);
                sb.Append(Styled(word, _look(w)));
                cursor = at + word.text.Length;
            }
            sb.Append(text, cursor, text.Length - cursor);
            return sb.ToString();
        }

        private static string Styled(Item word, WordLook look)
        {
            switch (look)
            {
                case WordLook.Reading: return ReadingMark + word.text + "</mark>";
                case WordLook.Found: return FoundMark + TextStyler.Apply(word.text, word.hl) + "</mark>";
                case WordLook.Hint: return HintMark + word.text + "</mark>";
                case WordLook.Hidden: return HiddenMark + "<alpha=#00>" + word.text + "<alpha=#FF></mark>";
                default: return word.text;
            }
        }

        /// <summary>Ghép từng từ TMP nhận ra với tiếng của bước (so chữ, không phân biệt hoa thường).</summary>
        private void MapWords()
        {
            _tmpToWord.Clear();
            var onPage = new List<int>();
            foreach (var s in _pages[Page]) onPage.AddRange(WordsOf(s));
            var next = 0;
            var info = _label.textInfo;
            for (var k = 0; k < info.wordCount; k++)
            {
                var tmpWord = info.wordInfo[k].GetWord();
                var match = -1;
                for (var j = next; j < onPage.Count; j++)
                {
                    if (string.Equals(_words[onPage[j]].text, tmpWord, StringComparison.OrdinalIgnoreCase))
                    {
                        match = onPage[j];
                        next = j + 1;
                        break;
                    }
                }
                _tmpToWord.Add(match);
            }
        }
    }
}
