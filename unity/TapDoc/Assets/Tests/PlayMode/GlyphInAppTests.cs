using System.Collections;
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>Thẻ kí hiệu dấu trong app thật (mở bài từ màn bài học): nét kí hiệu to và nằm giữa thẻ ở mọi màn.</summary>
    public class GlyphInAppTests : AppTestBase
    {
        [UnityTest]
        public IEnumerator Lesson17_GlyphTilesLargeOnEveryScreen()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            AppRoot.Instance.Speech.WaitScale = .02f;
            AppRoot.Instance.ShowLesson("tv1_t1_b17");
            yield return null;
            var problems = new List<string>();
            var metrics = new List<string>();
            AppRoot.Instance.UiCamera.targetTexture = new RenderTexture(2048, 1536, 24);
            yield return WalkAll(Object.FindAnyObjectByType<LessonScreen>(), (screen, n) =>
            {
                LayoutProbe.AssertFits(AppRoot.Instance.Canvas);   // thẻ dấu phóng to vẫn không được tràn chữ
                foreach (var tile in screen.GetComponentsInChildren<Tile>(true).Where(t => !string.IsNullOrEmpty(t.Tone) && t.PlainText.Length == 1))
                {
                    var tmp = tile.GetComponentInChildren<TMP_Text>();
                    var ink = ViewTestBase.InkBounds(tmp, tile.transform);
                    var h = ((RectTransform)tile.transform).rect.height;
                    var w = ((RectTransform)tile.transform).rect.width;
                    var line = $"màn {n} dấu {tile.Tone}: tâm nét {ink.center.y:0}, nét {ink.size.x:0}x{ink.size.y:0}, thẻ {w:0}x{h:0}, cỡ {tmp.fontSize:0}";
                    metrics.Add(line);
                    ScreenProbe.Save(AppRoot.Instance.UiCamera, $"TestOutput/glyph/b17_{n:00}.png");
                    if (Mathf.Abs(ink.center.y) > .15f * h || Mathf.Max(ink.size.y / h, ink.size.x / w) < .3f) problems.Add(line);
                }
            });
            System.IO.Directory.CreateDirectory("TestOutput");
            System.IO.File.WriteAllLines("TestOutput/glyph_metrics.txt", metrics);
            Assert.IsEmpty(problems, string.Join("\n", problems));
        }
    }
}
