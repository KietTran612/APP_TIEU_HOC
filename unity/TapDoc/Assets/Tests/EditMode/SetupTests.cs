using NUnit.Framework;
using UnityEditor;
using UnityEngine;

namespace TapDoc.Tests
{
    public class SetupTests
    {
        [Test] public void TmpSettingsExist() => Assert.IsNotNull(Resources.Load<TMPro.TMP_Settings>("TMP Settings"));

        [Test] public void MainSceneIsOnlyBuildScene()
        {
            Assert.AreEqual(1, EditorBuildSettings.scenes.Length);
            Assert.AreEqual("Assets/Scenes/Main.unity", EditorBuildSettings.scenes[0].path);
        }

        [Test] public void AndikaFontLoads() =>
            Assert.IsNotNull(new ResourcesContentSource().Load(ContentKind.Font, FontProvider.MainFontId) as Font);

        /// <summary>App có màn mở đầu riêng; tắt màn "Made with Unity" (Unity 6 cho tắt ở mọi gói giấy phép).</summary>
        [Test] public void UnitySplashScreenOff() => Assert.IsFalse(PlayerSettings.SplashScreen.show);

        [Test] public void LandscapeOnly()
        {
            Assert.IsFalse(PlayerSettings.allowedAutorotateToPortrait);
            Assert.IsFalse(PlayerSettings.allowedAutorotateToPortraitUpsideDown);
            Assert.IsTrue(PlayerSettings.allowedAutorotateToLandscapeLeft);
            Assert.IsTrue(PlayerSettings.allowedAutorotateToLandscapeRight);
            Assert.AreEqual(UIOrientation.AutoRotation, PlayerSettings.defaultInterfaceOrientation);
        }

        [Test] public void WindowsPlayerIsWindowed()
        {
            Assert.AreEqual(FullScreenMode.Windowed, PlayerSettings.fullScreenMode);
            Assert.IsTrue(PlayerSettings.resizableWindow);
            Assert.AreEqual(1600, PlayerSettings.defaultScreenWidth);
            Assert.AreEqual(720, PlayerSettings.defaultScreenHeight);
        }
    }
}
