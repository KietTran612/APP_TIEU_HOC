using TMPro;
using UnityEngine;

namespace TapDoc
{
    public static class FontProvider
    {
        /// <summary>Mã font chính (Andika), nạp trong bộ chung của <see cref="AssetCatalog"/>.</summary>
        public const string MainFontId = "Andika-Regular";

        private static TMP_FontAsset _main;
        private static AssetCatalog _standalone;

        /// <summary>
        /// Font chữ của app, lấy từ catalog của <see cref="AppRoot"/> (đã nạp trong bộ chung). Khi chưa có app (ví dụ
        /// test dựng giao diện riêng), dùng một catalog đọc từ Resources; lúc đó catalog cảnh báo "chưa chuẩn bị trước".
        /// </summary>
        public static TMP_FontAsset Main
        {
            get
            {
                if (_main == null)
                {
                    var app = AppRoot.Instance;
                    var catalog = app != null && app.Assets != null && app.Assets.IsLoaded(ContentKind.Font, MainFontId)
                        ? app.Assets
                        : _standalone ??= new AssetCatalog(new ResourcesContentSource());
                    _main = TMP_FontAsset.CreateFontAsset(catalog.Font(MainFontId));
                }
                return _main;
            }
        }
    }
}
