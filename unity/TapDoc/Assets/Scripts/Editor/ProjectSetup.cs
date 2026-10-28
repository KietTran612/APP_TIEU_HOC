using System;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

namespace TapDoc.EditorTools
{
    /// <summary>
    /// Thiết lập project TapDoc về trạng thái chuẩn. Chạy nhiều lần vẫn an toàn:
    /// không nhập lại TMP nếu đã có, không ghi đè scene Main nếu đã tồn tại.
    ///
    /// Gọi bằng: -batchmode -executeMethod TapDoc.EditorTools.ProjectSetup.Run (KHÔNG kèm -quit).
    /// Unity 6 nhập gói .unitypackage bất đồng bộ, sau khi hàm gọi trả về; -quit sẽ tắt Unity
    /// trước khi TMP kịp nhập. Vì vậy Run() tự thoát khi nhập xong (hoặc thất bại).
    /// </summary>
    public static class ProjectSetup
    {
        const string TmpFolder = "Assets/TextMesh Pro";
        const string UguiPackage = "Packages/com.unity.ugui";
        const string TmpEssentials = "Package Resources/TMP Essential Resources.unitypackage";
        const string ScenesFolder = "Assets/Scenes";
        const string MainScenePath = "Assets/Scenes/Main.unity";

        public static void Run()
        {
            CreateMainScene();
            ConfigurePlayerSettings();
            EditorSettings.defaultBehaviorMode = EditorBehaviorMode.Mode2D;
            AssetDatabase.SaveAssets();

            if (AssetDatabase.IsValidFolder(TmpFolder))
            {
                Finish(0);
                return;
            }
            if (Application.isBatchMode && Environment.GetCommandLineArgs().Contains("-quit"))
            {
                Debug.LogError("TapDoc: cần nhập TMP Essentials nhưng Unity đang chạy với -quit nên sẽ tắt trước khi nhập xong. Chạy lại không kèm -quit.");
                Finish(1);
                return;
            }
            ImportTmpEssentials();
        }

        static void ImportTmpEssentials()
        {
            AssetDatabase.importPackageCompleted += OnImportCompleted;
            AssetDatabase.importPackageFailed += OnImportFailed;
            AssetDatabase.importPackageCancelled += OnImportCancelled;

            // Gói ugui nằm trong Library/PackageCache nên phải lấy đường dẫn thật từ Package Manager.
            var package = UnityEditor.PackageManager.PackageInfo.FindForAssetPath(UguiPackage);
            var unityPackage = Path.GetFullPath(Path.Combine(package.resolvedPath, TmpEssentials));
            UnityEditor.AssetPackage.Package.Import(unityPackage, false);
        }

        static void OnImportCompleted(string packageName)
        {
            UnsubscribeImportEvents();
            Debug.Log($"TapDoc: đã nhập {packageName}.");
            Finish(0);
        }

        static void OnImportFailed(string packageName, string errorMessage)
        {
            UnsubscribeImportEvents();
            Debug.LogError($"TapDoc: nhập {packageName} thất bại: {errorMessage}");
            Finish(1);
        }

        static void OnImportCancelled(string packageName)
        {
            UnsubscribeImportEvents();
            Debug.LogError($"TapDoc: nhập {packageName} bị huỷ.");
            Finish(1);
        }

        static void UnsubscribeImportEvents()
        {
            AssetDatabase.importPackageCompleted -= OnImportCompleted;
            AssetDatabase.importPackageFailed -= OnImportFailed;
            AssetDatabase.importPackageCancelled -= OnImportCancelled;
        }

        static void Finish(int exitCode)
        {
            if (exitCode == 0) Debug.Log("TapDoc: ProjectSetup.Run xong.");
            if (Application.isBatchMode) EditorApplication.Exit(exitCode);
        }

        static void CreateMainScene()
        {
            if (!File.Exists(MainScenePath))
            {
                if (!AssetDatabase.IsValidFolder(ScenesFolder)) AssetDatabase.CreateFolder("Assets", "Scenes");
                var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
                EditorSceneManager.SaveScene(scene, MainScenePath);
            }
            EditorBuildSettings.scenes = new[] { new EditorBuildSettingsScene(MainScenePath, true) };
        }

        static void ConfigurePlayerSettings()
        {
            PlayerSettings.companyName = "AURA";
            PlayerSettings.productName = "Tập đọc";

            // Chỉ xoay ngang (trái và phải).
            PlayerSettings.defaultInterfaceOrientation = UIOrientation.AutoRotation;
            PlayerSettings.allowedAutorotateToPortrait = false;
            PlayerSettings.allowedAutorotateToPortraitUpsideDown = false;
            PlayerSettings.allowedAutorotateToLandscapeLeft = true;
            PlayerSettings.allowedAutorotateToLandscapeRight = true;

            // Bản Windows: cửa sổ co giãn được.
            PlayerSettings.fullScreenMode = FullScreenMode.Windowed;
            PlayerSettings.resizableWindow = true;
            PlayerSettings.defaultScreenWidth = 1600;
            PlayerSettings.defaultScreenHeight = 720;
        }
    }
}
