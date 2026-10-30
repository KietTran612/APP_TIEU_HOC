using System;
using System.Collections.Generic;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Phát âm thanh theo mã. Mỗi lần phát mới hoặc gọi <see cref="Stop"/> thì tăng số thế hệ; vòng lặp
    /// của thế hệ cũ thoát êm. Không tự tạo AudioListener: AppRoot (và môi trường test) đặt listener.
    /// </summary>
    public class SpeechPlayer : MonoBehaviour
    {
        private const int MaxHistory = 50;

        private AssetCatalog _catalog;
        private AudioSource _audioSource;
        private int _generation;
        private readonly List<string> _history = new();

        public float WaitScale = 1f;
        public bool IsBusy { get; private set; }
        public IReadOnlyList<string> History => _history;

        public void Init(AssetCatalog catalog)
        {
            _catalog = catalog ?? new AssetCatalog();
            if (_audioSource == null)
            {
                _audioSource = GetComponent<AudioSource>();
                if (_audioSource == null)
                {
                    _audioSource = gameObject.AddComponent<AudioSource>();
                }
                _audioSource.playOnAwake = false;
            }
        }

        /// <summary>
        /// Phát một mã âm thanh.
        /// </summary>
        /// <returns>
        /// <c>true</c> khi phát hết, hoặc xong ngay vì thiếu file (catalog đã báo lỗi trong Console).
        /// <c>false</c> khi bị cắt ngang bởi lần phát mới, bởi <see cref="Stop"/>, hoặc vì SpeechPlayer bị hủy.
        /// Màn hình PHẢI kiểm tra kết quả này trước khi đụng vào giao diện hoặc báo <c>Completed</c>:
        /// <c>false</c> nghĩa là màn có thể đã bị thay hoặc bị hủy.
        /// </returns>
        public async Awaitable<bool> PlayAsync(string id)
        {
            EnsureInitialized();
            var gen = ++_generation;
            if (_audioSource != null)
            {
                _audioSource.Stop();
            }

            if (string.IsNullOrEmpty(id) || RejectSfx(id))
            {
                IsBusy = false;
                return true;
            }

            RecordHistory(id);
            var clip = _catalog.Audio(id);
            if (clip == null)
            {
                if (_generation == gen)
                {
                    IsBusy = false;
                }
                return _generation == gen;
            }

            IsBusy = true;
            if (_audioSource != null)
            {
                _audioSource.clip = clip;
                _audioSource.Play();
            }

            await WaitRealtimeAsync(clip.length * WaitScale, gen);
            if (this == null || _generation != gen)
            {
                return false;
            }

            IsBusy = false;
            return true;
        }

        /// <summary>
        /// Phát lần lượt các mã, cách nhau <paramref name="gap"/> giây; gọi <paramref name="onPart"/> khi bắt đầu mỗi mảnh
        /// và <paramref name="onGap"/>(i) khi bắt đầu khoảng nghỉ ngay trước mảnh <c>i</c> (chỉ khi <paramref name="gap"/> &gt; 0).
        /// </summary>
        /// <returns>
        /// <c>true</c> khi phát hết chuỗi (mảnh thiếu file được bỏ qua). <c>false</c> khi bị cắt ngang bởi lần
        /// phát mới, bởi <see cref="Stop"/>, hoặc vì SpeechPlayer bị hủy. Màn hình PHẢI kiểm tra kết quả này
        /// trước khi đụng vào giao diện hoặc báo <c>Completed</c>.
        /// </returns>
        public async Awaitable<bool> PlaySequenceAsync(
            IReadOnlyList<string> ids,
            Action<int> onPart = null,
            float gap = SequenceTimeline.DefaultGap,
            Action<int> onGap = null)
        {
            EnsureInitialized();
            var gen = ++_generation;
            if (_audioSource != null)
            {
                _audioSource.Stop();
            }

            if (ids == null || ids.Count == 0)
            {
                IsBusy = false;
                return true;
            }

            IsBusy = true;
            for (var i = 0; i < ids.Count; i++)
            {
                if (this == null || _generation != gen)
                {
                    return false;
                }

                onPart?.Invoke(i);
                if (this == null || _generation != gen)
                {
                    return false;
                }

                var id = ids[i];
                if (!string.IsNullOrEmpty(id) && !RejectSfx(id))
                {
                    RecordHistory(id);
                    var clip = _catalog.Audio(id);
                    if (clip != null)
                    {
                        if (_audioSource != null)
                        {
                            _audioSource.clip = clip;
                            _audioSource.Play();
                        }
                        await WaitRealtimeAsync(clip.length * WaitScale, gen);
                        if (this == null || _generation != gen)
                        {
                            return false;
                        }
                    }
                }

                if (i + 1 < ids.Count && gap > 0f)
                {
                    onGap?.Invoke(i + 1);
                    if (this == null || _generation != gen)
                    {
                        return false;
                    }
                    await WaitRealtimeAsync(gap * WaitScale, gen);
                    if (this == null || _generation != gen)
                    {
                        return false;
                    }
                }
            }

            IsBusy = false;
            return true;
        }

        public void Stop()
        {
            _generation++;
            IsBusy = false;
            if (this != null && _audioSource != null)
            {
                _audioSource.Stop();
            }
        }

        private void OnDestroy()
        {
            Stop();
        }

        private void EnsureInitialized()
        {
            if (_catalog == null || _audioSource == null)
            {
                Init(_catalog ?? new AssetCatalog());
            }
        }

        /// <summary>
        /// Giọng đọc không phát mã tiếng động (<c>sfx_*</c>): hai loại âm thanh tách hẳn nhau. Gặp thì báo lỗi và bỏ qua.
        /// </summary>
        private static bool RejectSfx(string id)
        {
            if (!SystemSfx.IsSfx(id)) return false;
            Debug.LogError($"[TapDoc] Mã tiếng động không phát bằng giọng đọc: {id}");
            return true;
        }

        private void RecordHistory(string id)
        {
            if (string.IsNullOrEmpty(id)) return;
            if (_history.Count >= MaxHistory)
            {
                _history.RemoveAt(0);
            }
            _history.Add(id);
        }

        private async Awaitable WaitRealtimeAsync(float seconds, int gen)
        {
            if (seconds <= 0f) return;
            var deadline = Time.realtimeSinceStartup + seconds;
            while (this != null && _generation == gen && Time.realtimeSinceStartup < deadline)
            {
                await Awaitable.NextFrameAsync();
            }
        }
    }
}
