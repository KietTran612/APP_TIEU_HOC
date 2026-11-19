using System;
using UnityEditor;
using UnityEngine;

namespace TapDoc.EditorTools
{
    /// <summary>Quy tắc nhập tự động cho ảnh, âm thanh và clip tranh động của nội dung bài học.</summary>
    public class ContentImportRules : AssetPostprocessor
    {
        const string ImagesFolder = "Assets/Content/Resources/images/";
        const string AudioFolder = "Assets/Content/Resources/audio/";
        const string SfxFolder = "Assets/Content/Resources/sfx/";
        const string ClipsFolder = "Assets/Content/Resources/clips/";

        /// <summary>
        /// Clip tranh động: dùng nguyên file H.264/AAC của Google Flow, không chuyển mã (không mất chất lượng, nhập
        /// nhanh); giữ tiếng. App cắt phần tranh vuông lúc hiện (thiết kế tranh động mục 7, 12).
        /// </summary>
        void OnPreprocessAsset()
        {
            if (!assetPath.StartsWith(ClipsFolder, StringComparison.Ordinal) || assetImporter is not VideoClipImporter importer)
                return;
            importer.importAudio = true;
            importer.sRGBClip = true;
            importer.keepAlpha = false;
            var settings = importer.defaultTargetSettings;
            settings.enableTranscoding = false;
            importer.defaultTargetSettings = settings;
        }

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
