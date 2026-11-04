using TMPro;
using UnityEngine;

namespace TapDoc
{
    public static class FontProvider
    {
        /// <summary>Mã font chính (Andika), nạp trong bộ chung của <see cref="AssetCatalog"/>.</summary>
        public const string MainFontId = "Andika-Regular";

        private static TMP_FontAsset _main;

        public static TMP_FontAsset Main
        {
            get
            {
                if (_main == null)
                {
                    var font = Resources.Load<Font>("fonts/Andika-Regular");
                    _main = TMP_FontAsset.CreateFontAsset(font);
                }
                return _main;
            }
        }
    }
}
