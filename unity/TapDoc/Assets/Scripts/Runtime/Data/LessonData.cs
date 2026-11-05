using System;
using System.Collections.Generic;

namespace TapDoc
{
    [Serializable]
    public class LessonIndex
    {
        /// <summary>Các quyển theo thứ tự học (content/books.json); index cũ không có thì rỗng.</summary>
        public List<BookEntry> books = new();
        public List<LessonEntry> lessons = new();
    }

    [Serializable]
    public class BookEntry
    {
        public string book_id;
        public string title;
        /// <summary>Mã sách có Phụ lục dùng cho quyển này (tập 2 dùng Phụ lục của tập 1).</summary>
        public string appendix;
    }

    [Serializable]
    public class LessonEntry
    {
        public string lesson_id;
        public int lesson_no;
        public string title;
        public string type;
        public string book;
        /// <summary>Phần của danh sách bài: <c>chu_cai</c>, <c>van</c>, <c>tap_doc</c>.</summary>
        public string part;
        /// <summary>Nhãn trên thẻ bài ("Bài 81", "Bài 4", "Câu đố", "Chính tả").</summary>
        public string label;
        /// <summary>Tuần (chỉ phần Tập đọc), 0 nếu không có.</summary>
        public int week;
    }

    [Serializable]
    public class Lesson
    {
        public int schema;
        public string lesson_id;
        public string book;
        public int lesson_no;
        public string type;
        public string title;
        public List<LessonNote> notes = new();
        public List<string> new_units = new();
        public LessonSource source = new();
        public LessonReview review = new();
        public List<Step> part1 = new();
        public List<Round> part2 = new();
    }

    [Serializable]
    public class LessonNote
    {
        public string kind;
        public string text;
    }

    [Serializable]
    public class LessonSource
    {
        public List<int> pages = new();
        public string scan_file;
        public string verification;
    }

    [Serializable]
    public class LessonReview
    {
        public string status;
        public List<ReviewNote> can_duyet = new();
    }

    [Serializable]
    public class ReviewNote
    {
        public string where;
        public string note;
    }

    [Serializable]
    public class Step
    {
        public string type;
        public string text;
        public string audio;
        public string image;
        public string tone;
        public string glyph;
        public string marker;
        public string then_text;
        public string then_audio;
        public Spell spell = new();
        public List<Span> hl = new();
        public List<string> labels = new();
        public List<Item> rows = new();
        public List<Item> items = new();
        /// <summary>Số tiếng cần tìm ở bước <c>find_words</c>.</summary>
        public int need;
        public List<Reading> readings = new();
    }

    /// <summary>
    /// Một cách đọc của chữ ở bước giới thiệu chữ (Phụ lục tr.120–122). <see cref="kinds"/>: "hoc" (đọc khi học, để
    /// phân biệt chữ), "chuan" (âm chuẩn), "tenchu" (tên chữ cái); cách đọc trùng chữ gộp nhiều loại.
    /// </summary>
    [Serializable]
    public class Reading
    {
        public List<string> kinds = new();
        public string text;
        public string audio;
        public string hint;
    }

    [Serializable]
    public class Item
    {
        public string text;
        public string upper;
        public string audio;
        public string image;
        public string note;
        public int row;
        public int col;
        /// <summary>Mức ẩn khi học thuộc lòng (<c>memorize</c>): 0 luôn hiện, 1–3 ẩn từ mức đó.</summary>
        public int level;
        /// <summary>Đáp án điền vào chỗ trống (<c>fill_blank</c>): chữ hoặc tên dấu.</summary>
        public string answer;
        public string role;   // letter, tone, onset, vowel, base, form, cell, blocked, pair, line (khung chữ, bảng ghép, bảng dấu, quy tắc)
        public string tone;
        public string glyph;
        public List<Span> hl = new();
        public List<Spell> spells = new();
    }

    [Serializable]
    public class Spell
    {
        public string target;
        public bool drag_tone;
        public List<Part> parts = new();
    }

    [Serializable]
    public class Part
    {
        public string kind;
        public string text;
        public string audio;
        public string tone;
    }

    [Serializable]
    public class Span
    {
        public int s;
        public int n;
    }

    [Serializable]
    public class Round
    {
        public string kind;
        public string tag;
        public string instruction_audio;
        public string prompt_audio;
        public string prompt_text;
        public string base_text;
        public string image;
        public List<Option> options = new();
        public int answer;
    }

    [Serializable]
    public class Option
    {
        public string text;
        public string audio;
        public string image;
        public string tone;
    }
}
