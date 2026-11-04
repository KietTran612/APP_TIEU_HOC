using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using Object = UnityEngine.Object;

namespace TapDoc
{
    /// <summary>
    /// Tranh, âm thanh phát âm, tiếng động và font của app, nạp qua một <see cref="IContentSource"/>.
    /// <list type="bullet">
    /// <item>Màn chỉ hỏi <see cref="Image"/>, <see cref="Audio"/>, <see cref="Sfx"/>: trả ngay từ thứ đã chuẩn bị.</item>
    /// <item>Chuẩn bị trước theo bộ: <see cref="PrepareCommonAsync"/> (giữ mãi) và <see cref="PrepareAsync"/>
    /// (trả <see cref="ContentSet"/>, nhả khi <c>Dispose</c>). Mỗi mã có số chỗ giữ; về 0 thì nhả về nguồn.</item>
    /// <item>Thiếu file: âm thanh và tranh báo lỗi, tiếng động báo cảnh báo, mỗi mã một lần; mã không bắt buộc
    /// (ảnh đại diện) thì im lặng.</item>
    /// <item>Hỏi thứ chưa chuẩn bị: vẫn nạp ngay và trả, cảnh báo một lần, ghi vào <see cref="UnpreparedAsks"/>.</item>
    /// </list>
    /// </summary>
    public class AssetCatalog
    {
        /// <summary>Số khung tối đa chờ dữ liệu tiếng của một âm thanh trước khi coi là hỏng.</summary>
        private const int MaxAudioDataFrames = 600;

        private sealed class Entry
        {
            public Object Asset;
            public int Refs;
            public bool Loading;
        }

        private readonly IContentSource _source;
        private readonly Dictionary<(ContentKind, string), Entry> _entries = new();
        private readonly HashSet<(ContentKind, string)> _optional = new();
        private readonly HashSet<(ContentKind, string)> _loggedMissing = new();
        private readonly HashSet<string> _unprepared = new();
        private ContentSet _common;

        public AssetCatalog(IContentSource source)
        {
            _source = source ?? throw new ArgumentNullException(nameof(source));
        }

        /// <summary>Bộ nhận những thứ nạp lẻ (hỏi khi chưa chuẩn bị); <c>null</c> thì giữ đến khi app tắt.</summary>
        public ContentSet CurrentHolder { get; set; }

        /// <summary>Các mã màn đã hỏi khi chưa được chuẩn bị trước (để test kiểm tra).</summary>
        public IReadOnlyCollection<string> UnpreparedAsks => _unprepared;

        public AudioClip Audio(string id) => Get(ContentKind.Speech, id) as AudioClip;

        public AudioClip Sfx(string id) => Get(ContentKind.Sfx, id) as AudioClip;

        public Sprite Image(string id) => Get(ContentKind.Image, id) as Sprite;

        public Font Font(string id) => Get(ContentKind.Font, id) as Font;

        /// <summary>Có tranh này không. Không ghi log, kể cả khi chưa chuẩn bị hay thiếu file.</summary>
        public bool HasImage(string id)
        {
            if (string.IsNullOrEmpty(id)) return false;
            var key = (ContentKind.Image, id);
            if (!_entries.TryGetValue(key, out var entry)) entry = LoadNow(key);
            return entry.Asset != null;
        }

        /// <summary>
        /// Nạp bộ chung: giọng hướng dẫn và khen, tranh và biểu tượng chung, ảnh đại diện (không bắt buộc), tiếng
        /// động, font. Giữ đến khi app tắt. Gọi lần nữa không nạp lại.
        /// </summary>
        public async Awaitable PrepareCommonAsync()
        {
            if (_common != null) return;
            foreach (var avatar in ProfileScreen.Avatars) _optional.Add((ContentKind.Image, avatar));
            var ids = SystemAudio.All.Select(id => (ContentKind.Speech, id))
                .Concat(SystemImages.All.Select(id => (ContentKind.Image, id)))
                .Concat(ProfileScreen.Avatars.Select(id => (ContentKind.Image, id)))
                .Concat(SystemSfx.All.Select(id => (ContentKind.Sfx, id)))
                .Append((ContentKind.Font, FontProvider.MainFontId));
            _common = await PrepareAsync(ids);
        }

        /// <summary>
        /// Nạp và giữ một bộ; mã đã có thì chỉ tăng số chỗ giữ. Thiếu file thì báo như <see cref="Image"/> rồi tiếp tục.
        /// </summary>
        public async Awaitable<ContentSet> PrepareAsync(IEnumerable<(ContentKind kind, string id)> ids)
        {
            var set = new ContentSet(this);
            var pending = new List<Awaitable>();
            foreach (var key in ids ?? Enumerable.Empty<(ContentKind, string)>())
            {
                if (string.IsNullOrEmpty(key.id) || !set.Add(key)) continue;
                pending.Add(AcquireAsync(key));
            }
            foreach (var p in pending) await p;
            return set;
        }

        /// <summary>Mã đã nạp xong (đang được giữ, không còn đang nạp); thiếu file cũng tính là đã nạp.</summary>
        public bool IsLoaded(ContentKind kind, string id) =>
            !string.IsNullOrEmpty(id) && _entries.TryGetValue((kind, id), out var entry) && !entry.Loading;

        /// <summary>
        /// Âm thanh phát âm nạp lẻ có chờ (ví dụ phụ huynh chạm vào một chữ), tính vào <paramref name="holder"/>.
        /// Không cảnh báo; mã chưa có thì vẫn được ghi vào <see cref="UnpreparedAsks"/>.
        /// </summary>
        public async Awaitable<AudioClip> AudioAsync(string id, ContentSet holder)
        {
            if (string.IsNullOrEmpty(id)) return null;
            var key = (ContentKind.Speech, id);
            if (!_entries.ContainsKey(key)) _unprepared.Add(id);
            if (holder == null || holder.IsDisposed)
            {
                if (!_entries.ContainsKey(key)) await AcquireAsync(key); // không có bộ nào nhận: giữ đến khi app tắt
            }
            else if (holder.Add(key))
            {
                await AcquireAsync(key);
            }
            while (_entries.TryGetValue(key, out var loading) && loading.Loading) await Awaitable.NextFrameAsync();
            return _entries.TryGetValue(key, out var entry) ? entry.Asset as AudioClip : null;
        }

        internal void Release((ContentKind kind, string id) key)
        {
            if (!_entries.TryGetValue(key, out var entry)) return;
            entry.Refs--;
            if (entry.Refs > 0) return;
            _entries.Remove(key);
            if (entry.Asset is AudioClip clip && clip != null) clip.UnloadAudioData();
            _source.Release(key.kind, key.id, entry.Asset);
        }

        private Object Get(ContentKind kind, string id)
        {
            if (string.IsNullOrEmpty(id)) return null;
            var key = (kind, id);
            if (_entries.TryGetValue(key, out var entry))
            {
                if (entry.Asset == null && !entry.Loading) ReportMissing(key);
                return entry.Asset;
            }

            entry = LoadNow(key);
            if (entry.Asset == null)
            {
                ReportMissing(key);
            }
            else if (_unprepared.Add(id))
            {
                Debug.LogWarning($"[TapDoc] Chưa chuẩn bị trước: {id}");
            }
            return entry.Asset;
        }

        /// <summary>Nạp ngay một mã chưa có (không ghi log), giữ trong <see cref="CurrentHolder"/> nếu có.</summary>
        private Entry LoadNow((ContentKind kind, string id) key)
        {
            var entry = new Entry { Asset = _source.Load(key.kind, key.id), Refs = 1 };
            _entries[key] = entry;
            var holder = CurrentHolder;
            if (holder != null && !holder.IsDisposed) holder.Add(key);
            return entry;
        }

        private async Awaitable AcquireAsync((ContentKind kind, string id) key)
        {
            if (_entries.TryGetValue(key, out var existing))
            {
                existing.Refs++;
                while (existing.Loading) await Awaitable.NextFrameAsync();
                return;
            }

            var entry = new Entry { Refs = 1, Loading = true };
            _entries[key] = entry;
            var asset = await _source.LoadAsync(key.kind, key.id);
            if (asset is AudioClip clip && !await LoadAudioDataAsync(clip)) asset = null;
            entry.Asset = asset;
            entry.Loading = false;
            if (asset == null) ReportMissing(key);
        }

        /// <summary>Nạp dữ liệu tiếng vào bộ nhớ (âm thanh được nhập với preloadAudioData tắt).</summary>
        private static async Awaitable<bool> LoadAudioDataAsync(AudioClip clip)
        {
            if (clip.loadState != AudioDataLoadState.Loaded) clip.LoadAudioData();
            for (var i = 0; clip.loadState == AudioDataLoadState.Loading && i < MaxAudioDataFrames; i++)
            {
                await Awaitable.NextFrameAsync();
            }
            return clip.loadState == AudioDataLoadState.Loaded;
        }

        private void ReportMissing((ContentKind kind, string id) key)
        {
            if (_optional.Contains(key) || !_loggedMissing.Add(key)) return;
            switch (key.kind)
            {
                case ContentKind.Sfx:
                    Debug.LogWarning($"[TapDoc] Thiếu tiếng động: {key.id}");
                    break;
                case ContentKind.Speech:
                    Debug.LogError($"[TapDoc] Thiếu âm thanh: {key.id}");
                    break;
                case ContentKind.Image:
                    Debug.LogError($"[TapDoc] Thiếu tranh: {key.id}");
                    break;
                default:
                    Debug.LogError($"[TapDoc] Thiếu {key.kind}: {key.id}");
                    break;
            }
        }
    }
}
