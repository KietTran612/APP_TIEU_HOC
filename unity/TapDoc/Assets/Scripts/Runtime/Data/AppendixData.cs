using System;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

namespace TapDoc
{
    [Serializable]
    public class Appendix
    {
        public string book;
        public string title;
        public AppendixText chu_y = new();
        public AlphabetTable alphabet = new();
        public DigraphTable digraphs = new();
        public List<string> app_notes = new();
    }

    [Serializable]
    public class AppendixText
    {
        public int page;
        public string title;
        public List<string> paragraphs = new();
    }

    [Serializable]
    public class AlphabetTable
    {
        public int page;
        public string title;
        public List<string> columns = new();
        public List<AlphabetRow> rows = new();
    }

    [Serializable]
    public class AlphabetRow
    {
        public int no;
        public string lower;
        public string upper;
        public string name;
        public string sound;
    }

    [Serializable]
    public class DigraphTable
    {
        public int page;
        public string title;
        public List<string> columns = new();
        public List<DigraphRow> rows = new();
    }

    [Serializable]
    public class DigraphRow
    {
        public string letters;
        public string reading;
    }

    /// <summary>Phụ lục cuối sách (tr.120–122) cho phụ huynh: <c>Resources/appendix/&lt;mã sách&gt;.json</c>.</summary>
    public static class AppendixData
    {
        public static Appendix Load(string book)
        {
            if (string.IsNullOrWhiteSpace(book)) throw new InvalidDataException("Mã sách rỗng");
            var asset = Resources.Load<TextAsset>($"appendix/{book}");
            if (asset == null || string.IsNullOrWhiteSpace(asset.text))
                throw new InvalidDataException($"Không tìm thấy phụ lục: {book}");
            Appendix appendix;
            try
            {
                appendix = JsonUtility.FromJson<Appendix>(asset.text);
            }
            catch (Exception ex)
            {
                throw new InvalidDataException($"Phụ lục {book} không hợp lệ", ex);
            }
            if (appendix == null) throw new InvalidDataException($"Phụ lục {book} rỗng");
            appendix.book = LessonRepository.Nfc(appendix.book);
            appendix.title = LessonRepository.Nfc(appendix.title);
            appendix.chu_y ??= new AppendixText();
            appendix.chu_y.title = LessonRepository.Nfc(appendix.chu_y.title);
            appendix.chu_y.paragraphs = Normalize(appendix.chu_y.paragraphs);
            appendix.alphabet ??= new AlphabetTable();
            appendix.alphabet.title = LessonRepository.Nfc(appendix.alphabet.title);
            appendix.alphabet.columns = Normalize(appendix.alphabet.columns);
            appendix.alphabet.rows ??= new List<AlphabetRow>();
            foreach (var row in appendix.alphabet.rows)
            {
                if (row == null) continue;
                row.lower = LessonRepository.Nfc(row.lower);
                row.upper = LessonRepository.Nfc(row.upper);
                row.name = LessonRepository.Nfc(row.name);
                row.sound = LessonRepository.Nfc(row.sound);
            }
            appendix.digraphs ??= new DigraphTable();
            appendix.digraphs.title = LessonRepository.Nfc(appendix.digraphs.title);
            appendix.digraphs.columns = Normalize(appendix.digraphs.columns);
            appendix.digraphs.rows ??= new List<DigraphRow>();
            foreach (var row in appendix.digraphs.rows)
            {
                if (row == null) continue;
                row.letters = LessonRepository.Nfc(row.letters);
                row.reading = LessonRepository.Nfc(row.reading);
            }
            appendix.app_notes = Normalize(appendix.app_notes);
            return appendix;
        }

        private static List<string> Normalize(List<string> values)
        {
            values ??= new List<string>();
            for (var i = 0; i < values.Count; i++) values[i] = LessonRepository.Nfc(values[i]);
            return values;
        }
    }
}
