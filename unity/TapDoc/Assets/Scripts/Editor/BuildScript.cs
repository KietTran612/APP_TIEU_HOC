using System.IO;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEngine;

namespace TapDoc.EditorTools
{
    public static class BuildScript
    {
        public static void BuildWindows()
        {
            var outDir = Path.Combine(Directory.GetCurrentDirectory(), "Builds", "Windows");
            Directory.CreateDirectory(outDir);
            var exePath = Path.Combine(outDir, "TapDoc.exe");

            var options = new BuildPlayerOptions
            {
                scenes = new[] { "Assets/Scenes/Main.unity" },
                locationPathName = exePath,
                target = BuildTarget.StandaloneWindows64,
                options = BuildOptions.None
            };

            var report = BuildPipeline.BuildPlayer(options);
            if (report.summary.result != BuildResult.Succeeded)
            {
                Debug.LogError($"[TapDoc] Build Windows thất bại: {report.summary.result}");
                if (Application.isBatchMode)
                {
                    EditorApplication.Exit(1);
                }
                return;
            }

            Debug.Log($"[TapDoc] Build Windows thành công: {exePath}");
            if (Application.isBatchMode)
            {
                EditorApplication.Exit(0);
            }
        }
    }
}
