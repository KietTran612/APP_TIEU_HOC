using NUnit.Framework;
using TapDoc.EditorTools;

namespace TapDoc.Tests
{
    /// <summary>
    /// Tắt sao lưu Android cho dữ liệu của bé (bản thiết kế màn mở đầu, cảnh báo, cài đặt mục 5.2): manifest sinh ra khi
    /// build phải có <c>android:allowBackup="false"</c> trên thẻ application.
    /// </summary>
    public class AndroidNoBackupTests
    {
        private const string Head =
            "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\" xmlns:tools=\"http://schemas.android.com/tools\">\n";

        [Test]
        public void Patch_AddsAllowBackupFalse()
        {
            var result = AndroidNoBackup.Patch(Head + "  <application android:label=\"x\">\n  </application>\n</manifest>");
            StringAssert.Contains("android:allowBackup=\"false\"", result);
            StringAssert.Contains("android:label=\"x\"", result);
        }

        [Test]
        public void Patch_ReplacesTrue()
        {
            var result = AndroidNoBackup.Patch(Head + "  <application android:allowBackup=\"true\" android:label=\"x\" />\n</manifest>");
            StringAssert.Contains("android:allowBackup=\"false\"", result);
            StringAssert.DoesNotContain("android:allowBackup=\"true\"", result);
        }

        [Test]
        public void Patch_Idempotent()
        {
            var once = AndroidNoBackup.Patch(Head + "  <application android:label=\"x\">\n  </application>\n</manifest>");
            Assert.AreEqual(once, AndroidNoBackup.Patch(once));
        }

        [Test]
        public void Patch_NoApplicationTag_Unchanged()
        {
            var xml = Head + "</manifest>";
            Assert.AreEqual(xml, AndroidNoBackup.Patch(xml));
        }
    }
}
