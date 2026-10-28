using System;
using System.IO;
using NUnit.Framework;
using UnityEditor;
using UnityEngine;

namespace TapDoc.Tests
{
    /// <summary>Ghi đè file có cùng mã trong project thì app dùng bản mới, không phải sửa code.</summary>
    public class AssetSwapTests
    {
        private const string ImagePath = "Assets/Content/Resources/images/img_test_swap.png";
        private const string AudioPath = "Assets/Content/Resources/audio/aud_test_swap.wav";

        [Test]
        public void SwapImageAndAudio_SameId_UsesNewFile()
        {
            WritePng(ImagePath, 1);
            Assert.AreEqual(1, new AssetCatalog().Image("img_test_swap").texture.width);
            WritePng(ImagePath, 2);
            Assert.AreEqual(2, new AssetCatalog().Image("img_test_swap").texture.width);

            WriteWav(AudioPath, .1f);
            var a = new AssetCatalog().Audio("aud_test_swap").length;
            WriteWav(AudioPath, .3f);
            var b = new AssetCatalog().Audio("aud_test_swap").length;
            Assert.Greater(b, a + .1f);
        }

        [TearDown]
        public void Cleanup()
        {
            AssetDatabase.DeleteAsset(ImagePath);
            AssetDatabase.DeleteAsset(AudioPath);
        }

        private static void WritePng(string path, int size)
        {
            var tex = new Texture2D(size, size, TextureFormat.RGBA32, false);
            var px = new Color32[size * size];
            for (var i = 0; i < px.Length; i++) px[i] = new Color32(200, 120, 40, 255);
            tex.SetPixels32(px);
            tex.Apply();
            File.WriteAllBytes(path, tex.EncodeToPNG());
            UnityEngine.Object.DestroyImmediate(tex);
            AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceUpdate);
        }

        /// <summary>WAV PCM 16-bit mono 44,1 kHz, im lặng.</summary>
        private static void WriteWav(string path, float seconds)
        {
            const int rate = 44100;
            var samples = (int)(rate * seconds);
            using (var fs = new FileStream(path, FileMode.Create))
            using (var w = new BinaryWriter(fs))
            {
                var dataBytes = samples * 2;
                w.Write(System.Text.Encoding.ASCII.GetBytes("RIFF"));
                w.Write(36 + dataBytes);
                w.Write(System.Text.Encoding.ASCII.GetBytes("WAVE"));
                w.Write(System.Text.Encoding.ASCII.GetBytes("fmt "));
                w.Write(16);
                w.Write((short)1);
                w.Write((short)1);
                w.Write(rate);
                w.Write(rate * 2);
                w.Write((short)2);
                w.Write((short)16);
                w.Write(System.Text.Encoding.ASCII.GetBytes("data"));
                w.Write(dataBytes);
                w.Write(new byte[dataBytes]);
            }
            AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceUpdate);
        }
    }
}
