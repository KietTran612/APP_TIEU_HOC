using System.IO;
using System.Text.RegularExpressions;

namespace TapDoc.EditorTools
{
    /// <summary>
    /// Tắt sao lưu của Android (Auto Backup) cho dữ liệu của bé: app offline, không làm sao lưu, nên câu "chỉ được lưu
    /// trên máy này" ở popup "Gửi phụ huynh" phải đúng hoàn toàn (bản thiết kế màn mở đầu, cảnh báo, cài đặt mục 5.2).
    /// Sau khi Unity sinh project Gradle, đặt <c>android:allowBackup="false"</c> trên thẻ application của các manifest.
    /// </summary>
    public static class AndroidNoBackup
    {
        private static readonly Regex ApplicationTag = new(@"<application\b[^>]*>", RegexOptions.Singleline);
        private static readonly Regex AllowBackup = new(@"android:allowBackup\s*=\s*""[^""]*""");

        /// <summary>Đặt <c>android:allowBackup="false"</c> trên thẻ application đầu tiên; không có thẻ thì giữ nguyên.</summary>
        public static string Patch(string manifestXml)
        {
            if (string.IsNullOrEmpty(manifestXml)) return manifestXml;
            var match = ApplicationTag.Match(manifestXml);
            if (!match.Success) return manifestXml;
            var tag = match.Value;
            var patched = AllowBackup.IsMatch(tag)
                ? AllowBackup.Replace(tag, @"android:allowBackup=""false""")
                : tag.Insert("<application".Length, @" android:allowBackup=""false""");
            return manifestXml.Substring(0, match.Index) + patched + manifestXml.Substring(match.Index + match.Length);
        }

        /// <summary>Sửa file manifest nếu có.</summary>
        public static void PatchFile(string path)
        {
            if (!File.Exists(path)) return;
            var xml = File.ReadAllText(path);
            var patched = Patch(xml);
            if (patched != xml) File.WriteAllText(path, patched);
        }
    }

#if UNITY_ANDROID
    /// <summary>Gắn <see cref="AndroidNoBackup"/> vào bước sinh project Gradle (chỉ có khi cài module Android).</summary>
    internal sealed class AndroidNoBackupHook : UnityEditor.Android.IPostGenerateGradleAndroidProject
    {
        public int callbackOrder => 0;

        public void OnPostGenerateGradleAndroidProject(string path)
        {
            // path là thư mục unityLibrary; launcher nằm cạnh.
            AndroidNoBackup.PatchFile(Path.Combine(path, "src", "main", "AndroidManifest.xml"));
            AndroidNoBackup.PatchFile(Path.Combine(path, "..", "launcher", "src", "main", "AndroidManifest.xml"));
        }
    }
#endif
}
