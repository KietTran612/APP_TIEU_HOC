using System;
using UnityEditor;
using UnityEngine;

namespace TapDoc.EditorTools
{
    /// <summary>Quy tắc nhập tự động cho ảnh và âm thanh nội dung bài học.</summary>
    public class ContentImportRules : AssetPostprocessor
    {
        const string ImagesFolder = "Assets/Content/Resources/images/";
        const string AudioFolder = "Assets/Content/Resources/audio/";
        const string SfxFolder = "Assets/Content/Resources/sfx/";

        void OnPreprocessTexture()
        {
            if (!assetPath.StartsWith(ImagesFolder, StringComparison.Ordinal)) return;

            var importer = (TextureImporter)assetImporter;
            importer.textureType = TextureImporterType.Sprite;
            importer.spriteImportMode = SpriteImportMode.Single;
            importer.maxTextureSize = 1024;
            importer.mipmapEnabled = false;
        }

        void OnPreprocessAudio()
        {
            // Âm thanh phát âm (audio/) và tiếng động (sfx/) nằm ở hai thư mục riêng nhưng nhập cùng một cách.
            if (!assetPath.StartsWith(AudioFolder, StringComparison.Ordinal) &&
                !assetPath.StartsWith(SfxFolder, StringComparison.Ordinal)) return;

            var importer = (AudioImporter)assetImporter;
            importer.forceToMono = true;
            var settings = importer.defaultSampleSettings;
            settings.loadType = AudioClipLoadType.DecompressOnLoad;
            importer.defaultSampleSettings = settings;
        }
    }
}
