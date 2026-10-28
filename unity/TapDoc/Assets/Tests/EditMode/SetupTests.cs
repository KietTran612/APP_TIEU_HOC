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

        [Test] public void AndikaFontLoads() => Assert.IsNotNull(Resources.Load<Font>("fonts/Andika-Regular"));

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
