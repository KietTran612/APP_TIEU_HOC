using System;
using UnityEditor;
using UnityEngine;

namespace TapDoc.EditorTools
{
    /// <summary>
    /// Xuất tranh và âm thanh của bài học (cùng file .meta, giữ GUID) ra một .unitypackage. Hai thư mục này không nằm
    /// trong git; gói được đưa lên Google Drive để máy khác nhập lại (tools/run_unity_media.py).
    ///
    /// Gọi bằng: -batchmode -executeMethod TapDoc.EditorTools.MediaPackage.Export -mediaOut &lt;đường dẫn gói&gt;
    /// </summary>
    public static class MediaPackage
    {
        public static readonly string[] Folders =
        {
            "Assets/Content/Resources/images",
            "Assets/Content/Resources/audio",
        };

        public static void Export()
        {
            var output = ArgumentAfter("-mediaOut");
            if (string.IsNullOrEmpty(output))
            {
                Fail("thiếu tham số -mediaOut <đường dẫn gói>");
                return;
            }
            try
            {
                AssetDatabase.ExportPackage(Folders, output, ExportPackageOptions.Recurse);
            }
            catch (Exception e)
            {
                Fail(e.Message);
                return;
            }
            Debug.Log($"[TapDoc] Đã xuất gói media: {output}");
            if (Application.isBatchMode) EditorApplication.Exit(0);
        }

        private static string ArgumentAfter(string name)
        {
            var args = Environment.GetCommandLineArgs();
            var i = Array.IndexOf(args, name);
            return i >= 0 && i + 1 < args.Length ? args[i + 1] : null;
        }

        private static void Fail(string reason)
        {
            Debug.LogError($"[TapDoc] Xuất gói media thất bại: {reason}");
            if (Application.isBatchMode) EditorApplication.Exit(1);
        }
    }
}
