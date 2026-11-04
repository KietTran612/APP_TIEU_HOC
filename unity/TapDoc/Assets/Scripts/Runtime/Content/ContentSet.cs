using System;
using System.Collections.Generic;

namespace TapDoc
{
    /// <summary>
    /// Tay cầm của một bộ tranh, âm thanh đang được giữ (bộ của bài, của lượt ôn, của màn Phụ huynh).
    /// <see cref="Dispose"/> nhả mỗi mã trong bộ đúng một lần; gọi lại không có tác dụng.
    /// </summary>
    public sealed class ContentSet : IDisposable
    {
        private readonly AssetCatalog _catalog;
        private readonly HashSet<(ContentKind, string)> _keys = new();
        private bool _disposed;

        internal ContentSet(AssetCatalog catalog)
        {
            _catalog = catalog;
        }

        public bool IsDisposed => _disposed;

        /// <summary>Bộ đang giữ mã này chưa.</summary>
        public bool Holds(ContentKind kind, string id) => _keys.Contains((kind, id));

        /// <summary>Thêm mã vào bộ; <c>false</c> khi bộ đã giữ mã đó (người gọi không được tăng số chỗ giữ lần nữa).</summary>
        internal bool Add((ContentKind, string) key) => !_disposed && _keys.Add(key);

        public void Dispose()
        {
            if (_disposed) return;
            _disposed = true;
            foreach (var key in _keys) _catalog.Release(key);
            _keys.Clear();
            if (_catalog.CurrentHolder == this) _catalog.CurrentHolder = null;
        }
    }
}
