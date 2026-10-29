using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Kho tiến độ: hồ sơ bé, bài đã học (sao), khóa bài theo thứ tự và các lượt Phần 2 bé đã nhầm.
    /// Lưu thành một file JSON. Mỗi lần ghi đều ghi ra <c>&lt;path&gt;.tmp</c> rồi thay file cũ, nên file
    /// không bao giờ bị ghi dở. File hỏng thì được đổi tên thành <c>&lt;path&gt;.bak</c> và kho bắt đầu lại
    /// với dữ liệu trống: app không dừng.
    /// Chưa chọn bé (<see cref="Current"/> là <c>null</c>) thì các hàm ghi tiến độ không làm gì.
    /// </summary>
    public class ProgressStore
    {
        public const string FileName = "tapdoc_progress.json";
        public const int MaxNameLength = 20;
        public const int MaxStars = 3;

        private readonly ProgressFile _data;
        private long _lastTicks;

        public ProgressStore(string path) : this(path, new ProgressFile())
        {
        }

        private ProgressStore(string path, ProgressFile data)
        {
            if (string.IsNullOrEmpty(path)) throw new ArgumentException("Thiếu đường dẫn file tiến độ", nameof(path));
            FilePath = path;
            _data = data;
        }

        public string FilePath { get; }

        /// <summary>Hồ sơ bé đang học; <c>null</c> khi chưa có hoặc chưa chọn hồ sơ nào.</summary>
        public Profile Current =>
            string.IsNullOrEmpty(_data.current) ? null : _data.profiles.Find(p => p.id == _data.current);

        public IReadOnlyList<Profile> Profiles => _data.profiles;

        /// <summary>Kho của app thật: <c>persistentDataPath/tapdoc_progress.json</c>.</summary>
        public static ProgressStore Default() => Load(Path.Combine(Application.persistentDataPath, FileName));

        /// <summary>
        /// Tên gọi ở nhà đã chuẩn hóa: dạng NFC, bỏ khoảng trắng hai đầu, tối đa <see cref="MaxNameLength"/> ký tự.
        /// Trả về chuỗi rỗng khi không còn chữ nào.
        /// </summary>
        public static string CleanName(string name)
        {
            var s = (name ?? string.Empty).Normalize(NormalizationForm.FormC).Trim();
            if (s.Length > MaxNameLength)
            {
                var cut = MaxNameLength;
                if (char.IsHighSurrogate(s[cut - 1])) cut--; // không cắt đôi một ký tự ghép cặp (ví dụ emoji)
                s = s.Substring(0, cut).TrimEnd();
            }
            return s;
        }

        /// <summary>Tạo hồ sơ mới và chọn luôn hồ sơ đó. Tên rỗng (sau khi bỏ khoảng trắng) thì báo <see cref="ArgumentException"/>.</summary>
        public Profile CreateProfile(string name, string avatar)
        {
            var clean = CleanName(name);
            if (clean.Length == 0) throw new ArgumentException("Tên bé rỗng", nameof(name));
            var profile = new Profile
            {
                id = Guid.NewGuid().ToString("N"),
                name = clean,
                avatar = avatar ?? string.Empty
            };
            _data.profiles.Add(profile);
            _data.current = profile.id;
            return profile;
        }

        public void Select(string profileId)
        {
            if (string.IsNullOrEmpty(profileId) || _data.profiles.All(p => p.id != profileId))
            {
                throw new ArgumentException($"Không có hồ sơ: {profileId}", nameof(profileId));
            }
            _data.current = profileId;
        }

        /// <summary>
        /// Bài đầu luôn mở; bài k mở khi bài k−1 đã học xong. Bài đã học xong thì luôn mở (để học lại, kể cả khi
        /// danh sách bài có thêm bài mới đứng trước). Bài không có trong danh sách thì khóa.
        /// </summary>
        public bool IsUnlocked(IReadOnlyList<string> orderedLessonIds, string lessonId)
        {
            if (orderedLessonIds == null || string.IsNullOrEmpty(lessonId)) return false;
            var k = -1;
            for (var i = 0; i < orderedLessonIds.Count; i++)
            {
                if (orderedLessonIds[i] == lessonId)
                {
                    k = i;
                    break;
                }
            }
            if (k < 0) return false;
            if (k == 0) return true;
            return IsCompleted(lessonId) || IsCompleted(orderedLessonIds[k - 1]);
        }

        public bool IsCompleted(string lessonId) => IsCompleted(Current, lessonId);

        public static bool IsCompleted(Profile profile, string lessonId) =>
            profile != null && profile.lessons.Any(l => l.lesson_id == lessonId && l.completed);

        /// <summary>Số sao của bài với bé đang học; 0 khi chưa học xong.</summary>
        public int StarsFor(string lessonId)
        {
            var entry = Current?.lessons.Find(l => l.lesson_id == lessonId);
            return entry != null && entry.completed ? entry.stars : 0;
        }

        /// <summary>Học xong bài: ghi <c>completed</c> và số sao (không bao giờ giảm số sao đã có).</summary>
        public void MarkCompleted(string lessonId, int stars = MaxStars)
        {
            var profile = Current;
            if (profile == null || string.IsNullOrEmpty(lessonId)) return;
            var entry = profile.lessons.Find(l => l.lesson_id == lessonId);
            if (entry == null)
            {
                entry = new LessonProgress { lesson_id = lessonId };
                profile.lessons.Add(entry);
            }
            entry.completed = true;
            entry.stars = Math.Max(entry.stars, Mathf.Clamp(stars, 0, MaxStars));
        }

        /// <summary>Ghi một lần nhầm ở lượt <paramref name="round"/> (chỉ số trong <c>part2</c>) của bài.</summary>
        public void RecordMistake(string lessonId, int round)
        {
            var profile = Current;
            if (profile == null || string.IsNullOrEmpty(lessonId)) return;
            var mistake = profile.mistakes.Find(m => m.lesson_id == lessonId && m.round == round);
            if (mistake == null)
            {
                mistake = new Mistake { lesson_id = lessonId, round = round };
                profile.mistakes.Add(mistake);
            }
            mistake.count++;
            mistake.last_ticks = NextTicks(profile);
        }

        public void ClearMistake(string lessonId, int round)
        {
            Current?.mistakes.RemoveAll(m => m.lesson_id == lessonId && m.round == round);
        }

        /// <summary>Tối đa <paramref name="max"/> lượt nhầm của bé đang học: nhầm nhiều trước, rồi mới nhầm trước.</summary>
        public IReadOnlyList<Mistake> Mistakes(int max = 8) => MistakesOf(Current, max);

        /// <summary>Như <see cref="Mistakes"/>, cho một hồ sơ bất kỳ (màn phụ huynh xem từng bé).</summary>
        public static IReadOnlyList<Mistake> MistakesOf(Profile profile, int max = 8)
        {
            if (profile == null || max <= 0) return Array.Empty<Mistake>();
            return profile.mistakes
                .OrderByDescending(m => m.count)
                .ThenByDescending(m => m.last_ticks)
                .Take(max)
                .ToList();
        }

        /// <summary>
        /// Ghi file: ghi trọn ra <c>&lt;path&gt;.tmp</c> (đẩy xuống đĩa), rồi <see cref="File.Replace(string, string, string)"/>
        /// (hoặc <see cref="File.Move(string, string)"/> khi chưa có file). Lỗi đĩa thì báo exception; app gọi qua
        /// một hàm bọc bắt lỗi để không dừng.
        /// </summary>
        public void Save()
        {
            var dir = Path.GetDirectoryName(FilePath);
            if (!string.IsNullOrEmpty(dir)) Directory.CreateDirectory(dir);

            var tmp = FilePath + ".tmp";
            var bytes = new UTF8Encoding(false).GetBytes(JsonUtility.ToJson(_data, true));
            using (var fs = new FileStream(tmp, FileMode.Create, FileAccess.Write, FileShare.None))
            {
                fs.Write(bytes, 0, bytes.Length);
                fs.Flush(true);
            }

            if (!File.Exists(FilePath))
            {
                File.Move(tmp, FilePath);
                return;
            }

            try
            {
                File.Replace(tmp, FilePath, null);
            }
            catch (PlatformNotSupportedException)
            {
                // Nền tảng không có Replace: xóa rồi đổi tên. Nếu dừng giữa chừng, Load lấy lại từ file tạm.
                File.Delete(FilePath);
                File.Move(tmp, FilePath);
            }
        }

        /// <summary>
        /// Đọc kho từ <paramref name="path"/>. Chưa có file thì trả kho trống. File hỏng (JSON sai, rỗng, không đọc
        /// được) thì đổi tên thành <c>&lt;path&gt;.bak</c> và trả kho trống.
        /// </summary>
        public static ProgressStore Load(string path)
        {
            if (string.IsNullOrEmpty(path)) throw new ArgumentException("Thiếu đường dẫn file tiến độ", nameof(path));
            var tmp = path + ".tmp";

            if (!File.Exists(path))
            {
                // Lần ghi trước dừng đúng lúc thay file: file tạm đã ghi trọn thì dùng nó.
                if (File.Exists(tmp) && TryRead(tmp, out var recovered))
                {
                    try
                    {
                        File.Move(tmp, path);
                    }
                    catch (Exception ex) when (ex is IOException || ex is UnauthorizedAccessException)
                    {
                        // Lần Save sau sẽ ghi lại file chính.
                    }
                    return new ProgressStore(path, recovered);
                }
                return new ProgressStore(path);
            }

            if (TryRead(path, out var data)) return new ProgressStore(path, data);

            BackUp(path);
            return new ProgressStore(path);
        }

        private static bool TryRead(string path, out ProgressFile data)
        {
            data = null;
            try
            {
                var text = File.ReadAllText(path, Encoding.UTF8);
                if (string.IsNullOrWhiteSpace(text)) return false;
                data = JsonUtility.FromJson<ProgressFile>(text);
            }
            catch (Exception)
            {
                // JSON hỏng (JsonUtility báo ArgumentException) hoặc không đọc được file: coi như file hỏng.
                return false;
            }
            if (data == null) return false;
            Normalize(data);
            return true;
        }

        private static void Normalize(ProgressFile data)
        {
            data.profiles ??= new List<Profile>();
            data.profiles.RemoveAll(p => p == null || string.IsNullOrEmpty(p.id));
            foreach (var p in data.profiles)
            {
                p.name ??= string.Empty;
                p.avatar ??= string.Empty;
                p.lessons ??= new List<LessonProgress>();
                p.lessons.RemoveAll(l => l == null || string.IsNullOrEmpty(l.lesson_id));
                p.mistakes ??= new List<Mistake>();
                p.mistakes.RemoveAll(m => m == null || string.IsNullOrEmpty(m.lesson_id));
            }
            if (data.profiles.All(p => p.id != data.current)) data.current = null;
        }

        private static void BackUp(string path)
        {
            var bak = path + ".bak";
            try
            {
                if (File.Exists(bak)) File.Delete(bak);
                File.Move(path, bak);
                Debug.LogWarning($"[TapDoc] File tiến độ hỏng, đã đổi tên thành {bak} và bắt đầu lại.");
            }
            catch (Exception ex) when (ex is IOException || ex is UnauthorizedAccessException)
            {
                Debug.LogWarning($"[TapDoc] File tiến độ hỏng và không đổi tên được ({ex.Message}); bắt đầu lại.");
            }
        }

        /// <summary>Mốc thời gian tăng dần trong kho, để lượt vừa nhầm luôn đứng trước khi số lần nhầm bằng nhau.</summary>
        private long NextTicks(Profile profile)
        {
            var floor = _lastTicks;
            foreach (var m in profile.mistakes)
            {
                if (m.last_ticks > floor) floor = m.last_ticks;
            }
            _lastTicks = Math.Max(DateTime.UtcNow.Ticks, floor + 1);
            return _lastTicks;
        }
    }
}
