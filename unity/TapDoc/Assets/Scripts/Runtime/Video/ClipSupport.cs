using UnityEngine;
using UnityEngine.Rendering;

namespace TapDoc
{
    /// <summary>Máy có được thử phát clip không (thiết kế tranh động mục 10); không thì app dùng tranh tĩnh.</summary>
    public static class ClipSupport
    {
        /// <summary>Máy có RAM dưới mức này (máy 2 GB trở xuống) không phát clip.</summary>
        public const int MinMemoryMb = 2000;

        public static bool CanPlay(int systemMemoryMb, bool hasGraphics, bool renderTextureOk) =>
            hasGraphics && renderTextureOk && systemMemoryMb >= MinMemoryMb;

        /// <summary>Máy đang chạy app.</summary>
        public static bool CurrentDevice() => CanPlay(
            SystemInfo.systemMemorySize,
            SystemInfo.graphicsDeviceType != GraphicsDeviceType.Null,
            SystemInfo.SupportsRenderTextureFormat(RenderTextureFormat.ARGB32));
    }
}
