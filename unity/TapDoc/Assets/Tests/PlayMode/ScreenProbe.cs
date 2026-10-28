using System.IO;
using UnityEngine;

namespace TapDoc.Tests
{
    public static class ScreenProbe
    {
        public static void Save(Camera cam, string path)
        {
            Canvas.ForceUpdateCanvases();
            var rt = cam.targetTexture;
            var createdTemp = false;
            if (rt == null)
            {
                rt = new RenderTexture(1920, 1080, 24);
                cam.targetTexture = rt;
                createdTemp = true;
            }

            cam.Render();
            var prev = RenderTexture.active;
            RenderTexture.active = rt;

            var tex = new Texture2D(rt.width, rt.height, TextureFormat.RGB24, false);
            tex.ReadPixels(new Rect(0, 0, rt.width, rt.height), 0, 0);
            tex.Apply();

            RenderTexture.active = prev;
            if (createdTemp)
            {
                cam.targetTexture = null;
                Object.Destroy(rt);
            }

            var png = tex.EncodeToPNG();
            Object.Destroy(tex);

            var fullPath = Path.GetFullPath(path);
            var dir = Path.GetDirectoryName(fullPath);
            if (!string.IsNullOrEmpty(dir))
            {
                Directory.CreateDirectory(dir);
            }
            File.WriteAllBytes(fullPath, png);
        }
    }
}
