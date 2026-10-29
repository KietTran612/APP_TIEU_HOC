using System;
using System.Collections.Generic;

namespace TapDoc
{
    [Serializable]
    public class LessonIndex
    {
        public List<LessonEntry> lessons = new();
    }

    [Serializable]
    public class LessonEntry
    {
        public string lesson_id;
        public int lesson_no;
        public string title;
        public string type;
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
        public List<string> new_units = new();
        public LessonSource source = new();
        public LessonReview review = new();
        public List<Step> part1 = new();
        public List<Round> part2 = new();
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
        public List<Item> rows = new();
        public List<Item> items = new();
    }

    [Serializable]
    public class Item
    {
        public string text;
        public string audio;
        public string image;
        public string note;
        public int row;
        public int col;
        public string role;   // letter, tone, onset, vowel, base, form, cell (khung chữ, bảng ghép, bảng dấu)
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
