using System;
using System.Collections.Generic;
using System.Linq;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    /// <summary>
    /// Khung chữ cho phụ huynh phủ kín màn, có nút "Đóng" và phần nội dung cuộn được. Dùng cho ghi chú trong bài
    /// (<see cref="ForLesson"/>) và mục "Chú ý và Phụ lục" ở màn Phụ huynh (<see cref="ForAppendix"/>).
    /// </summary>
    public sealed class NotesPanel
    {
        private static readonly Color Background = new(0.965f, 0.933f, 0.863f, 1f);
        private static readonly Color TapCell = new(1f, 1f, 1f, 0.6f);

        public GameObject Root { get; }
        private readonly RectTransform _content;

        public NotesPanel(Transform parent, string title)
        {
            Root = new GameObject("NotesPanel", typeof(RectTransform), typeof(Image));
            Root.transform.SetParent(parent, false);
            Stretch((RectTransform)Root.transform, Vector2.zero, Vector2.zero);
            var background = Root.GetComponent<Image>();
            background.sprite = UiKit.WhiteSprite;
            background.color = Background;

            var heading = UiKit.CreateLabel(Root.transform, title, 52f);
            var headingRt = heading.rectTransform;
            headingRt.anchorMin = new Vector2(0f, 1f);
            headingRt.anchorMax = Vector2.one;
            headingRt.pivot = new Vector2(0.5f, 1f);
            headingRt.offsetMin = new Vector2(40f, -180f);
            headingRt.offsetMax = new Vector2(-340f, -20f);

            var close = UiKit.CreateButton(Root.transform, UiText.Close, () => Root.SetActive(false));
            var closeRt = (RectTransform)close.transform;
            closeRt.anchorMin = closeRt.anchorMax = closeRt.pivot = Vector2.one;
            closeRt.sizeDelta = new Vector2(260f, UiKit.MinTouch);
            closeRt.anchoredPosition = new Vector2(-40f, -20f);

            var scrollGo = new GameObject("Scroll", typeof(RectTransform), typeof(ScrollRect));
            scrollGo.transform.SetParent(Root.transform, false);
            Stretch((RectTransform)scrollGo.transform, new Vector2(40f, 30f), new Vector2(-40f, -200f));
            var viewport = new GameObject("Viewport", typeof(RectTransform), typeof(Image), typeof(RectMask2D));
            viewport.transform.SetParent(scrollGo.transform, false);
            var viewportRt = (RectTransform)viewport.transform;
            Stretch(viewportRt, Vector2.zero, Vector2.zero);
            viewport.GetComponent<Image>().color = Color.clear;

            var content = new GameObject("Content", typeof(RectTransform), typeof(VerticalLayoutGroup), typeof(ContentSizeFitter));
            content.transform.SetParent(viewport.transform, false);
            _content = (RectTransform)content.transform;
            _content.anchorMin = new Vector2(0f, 1f);
            _content.anchorMax = Vector2.one;
            _content.pivot = new Vector2(0.5f, 1f);
            _content.sizeDelta = Vector2.zero;
            var layout = content.GetComponent<VerticalLayoutGroup>();
            layout.spacing = 20f;
            layout.padding = new RectOffset(12, 12, 12, 12);
            layout.childControlWidth = layout.childControlHeight = true;
            layout.childForceExpandWidth = true;
            layout.childForceExpandHeight = false;
            content.GetComponent<ContentSizeFitter>().verticalFit = ContentSizeFitter.FitMode.PreferredSize;
            var scroll = scrollGo.GetComponent<ScrollRect>();
            scroll.viewport = viewportRt;
            scroll.content = _content;
            scroll.horizontal = false;
            scroll.vertical = true;
            scroll.movementType = ScrollRect.MovementType.Clamped;
        }

        public void AddText(string text, bool heading = false)
        {
            var label = UiKit.CreateLabel(_content, text, heading ? 44f : 36f);
            // Cỡ chữ cố định để TMP báo đúng chiều cao cho layout khi chữ xuống dòng.
            label.enableAutoSizing = false;
            label.alignment = TextAlignmentOptions.TopLeft;
            label.richText = false;
            if (heading) label.fontStyle = FontStyles.Bold;
        }

        public void AddRow(IEnumerable<string> cells) => AddRow(cells.Select(c => (c, (Action)null)));

        /// <summary>Một hàng bảng; ô có <c>onTap</c> là nút (hàng cao bằng vùng chạm tối thiểu), chạm thì gọi <c>onTap</c>.</summary>
        public void AddRow(IEnumerable<(string text, Action onTap)> cells)
        {
            var list = cells.ToList();
            var row = new GameObject("TableRow", typeof(RectTransform), typeof(HorizontalLayoutGroup), typeof(LayoutElement));
            row.transform.SetParent(_content, false);
            row.GetComponent<LayoutElement>().preferredHeight = list.Any(c => c.onTap != null) ? UiKit.MinTouch : 110f;
            var layout = row.GetComponent<HorizontalLayoutGroup>();
            layout.spacing = 12f;
            layout.childControlWidth = layout.childControlHeight = true;
            layout.childForceExpandWidth = layout.childForceExpandHeight = true;
            foreach (var (text, onTap) in list)
            {
                // Ô bấm được là một khung nền nhạt (để phụ huynh thấy chạm được) chứa nhãn; ô thường chỉ là nhãn.
                Transform cell = row.transform;
                if (onTap != null)
                {
                    var go = new GameObject("TableCell", typeof(RectTransform), typeof(Image), typeof(Button));
                    go.transform.SetParent(row.transform, false);
                    var hit = go.GetComponent<Image>();
                    hit.sprite = UiKit.WhiteSprite;
                    hit.color = TapCell;
                    go.GetComponent<Button>().onClick.AddListener(() => onTap());
                    cell = go.transform;
                }
                var label = UiKit.CreateLabel(cell, text, 36f);
                label.richText = false;
                if (onTap != null) Stretch(label.rectTransform, Vector2.zero, Vector2.zero);
                var size = (onTap != null ? cell.gameObject : label.gameObject).AddComponent<LayoutElement>();
                size.minWidth = 0f;
                size.preferredWidth = 0f;
                size.flexibleWidth = 1f;
            }
        }

        public static GameObject ForLesson(Transform parent, Lesson lesson)
        {
            var panel = new NotesPanel(parent, UiText.Notes);
            foreach (var (kind, title) in new[]
            {
                ("sach", UiText.NoteKindBook),
                ("ten_doc", UiText.NoteKindReading),
                ("khac_sach", UiText.NoteKindApp)
            })
            {
                var notes = lesson.notes.Where(n => n != null && n.kind == kind).ToList();
                if (notes.Count == 0) continue;
                panel.AddText(title, true);
                foreach (var note in notes) panel.AddText(note.text);
            }
            return panel.Root;
        }

        /// <summary>
        /// Mục "Chú ý và Phụ lục". Ô "Tên chữ cái", "Ghi âm" (tr.120) và "Đọc là" (tr.121) có âm thanh trong
        /// <paramref name="audio"/> thì chạm vào sẽ <paramref name="play"/> đúng cách đọc đó.
        /// </summary>
        public static GameObject ForAppendix(Transform parent, Appendix appendix, LetterAudio audio, Action<string> play)
        {
            (string, Action) Cell(string text, string letter, string kind)
            {
                var id = audio?.Of(letter, kind);
                return (text, id == null || play == null ? null : () => play(id));
            }

            var panel = new NotesPanel(parent, UiText.BookAppendix);
            panel.AddText(appendix.title, true);
            panel.AddText(string.Format(UiText.PageFormat, appendix.chu_y.title, appendix.chu_y.page), true);
            foreach (var paragraph in appendix.chu_y.paragraphs) panel.AddText(paragraph);
            panel.AddText(string.Format(UiText.PageFormat, appendix.alphabet.title, appendix.alphabet.page), true);
            panel.AddRow(appendix.alphabet.columns);
            foreach (var row in appendix.alphabet.rows)
            {
                if (row == null) continue;
                panel.AddRow(new[]
                {
                    (row.no.ToString(), null), (row.lower, null), (row.upper, null),
                    Cell(row.name, row.lower, LetterAudio.LetterName), Cell(row.sound, row.lower, LetterAudio.Sound)
                });
            }
            panel.AddText(string.Format(UiText.PageFormat, appendix.digraphs.title, appendix.digraphs.page), true);
            panel.AddRow(appendix.digraphs.columns);
            foreach (var row in appendix.digraphs.rows)
            {
                if (row == null) continue;
                panel.AddRow(new[] { (row.letters, null), Cell(row.reading, row.letters, LetterAudio.Sound) });
            }
            panel.AddText(UiText.NoteKindApp, true);
            foreach (var note in appendix.app_notes) panel.AddText(note);
            return panel.Root;
        }

        private static void Stretch(RectTransform rt, Vector2 min, Vector2 max)
        {
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = min;
            rt.offsetMax = max;
        }
    }
}
