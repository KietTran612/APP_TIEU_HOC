using NUnit.Framework;
using UnityEditor;

namespace TapDoc.Tests
{
    /// <summary>Clip trong Resources/clips được nhập nguyên bản, có tiếng (thiết kế tranh động mục 12).</summary>
    public class ClipImportTests
    {
        [Test]
        public void ClipImporter_KeepsOriginalFileWithAudio()
        {
            var importer = AssetImporter.GetAtPath("Assets/Content/Resources/clips/img_b01_bof.mp4") as VideoClipImporter;
            if (importer == null) Assert.Inconclusive("Chưa chép clip vào Resources/clips (python tools/run_unity_media.py clips)");
            Assert.IsFalse(importer.defaultTargetSettings.enableTranscoding, "không chuyển mã");
            Assert.IsTrue(importer.importAudio, "giữ tiếng");
        }
    }
}
