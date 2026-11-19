using System;
using System.Collections.Generic;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Đọc <c>Resources/clips/index.json</c> (lệnh <c>run_unity_media.py clips</c> ghi): <c>{"giu": [mã tranh…]}</c> là các
    /// clip "tiếp" — bắt đầu từ tranh, khung cuối khác tranh — nên hết clip thì giữ khung cuối (thiết kế tranh động mục
    /// 4.1, 5). Thiếu hay hỏng thì danh sách rỗng: mọi clip theo cách cũ.
    /// </summary>
    public static class ClipIndex
    {
        [Serializable]
        private class Data
        {
            public List<string> giu = new();
        }

        public static HashSet<string> Parse(string json)
        {
            var hold = new HashSet<string>();
            if (string.IsNullOrWhiteSpace(json)) return hold;
            Data data;
            try
            {
                data = JsonUtility.FromJson<Data>(json);
            }
            catch (ArgumentException)
            {
                return hold;
            }
            if (data?.giu == null) return hold;
            foreach (var id in data.giu)
            {
                if (!string.IsNullOrEmpty(id)) hold.Add(id);
            }
            return hold;
        }
    }
}
