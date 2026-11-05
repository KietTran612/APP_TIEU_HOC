using System.Collections;
using System.Linq;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// Đi hết Phần 1 và Phần 2 của mọi bài tập 2 trên dữ liệu thật (tranh, âm thanh giả): mỗi màn dựng được, vừa khung
    /// hình, không chữ tràn, và làm xong được. Chạy riêng theo phần để biết phần nào hỏng.
    /// </summary>
    public class Tap2LessonSmokeTests : ViewTestBase
    {
        private static string[] Ids(int from, int to) => TestLessons.Real.Index.lessons
            .Where(e => e.book == "tv1_t2_1996" && e.lesson_no >= from && e.lesson_no <= to)
            .Select(e => e.lesson_id).ToArray();

        private void UseFrame(int w, int h)
        {
            Cam.targetTexture = null;
            Object.Destroy(TargetTex);
            TargetTex = new RenderTexture(w, h, 24);
            Cam.targetTexture = TargetTex;
        }

        private IEnumerator WalkLessons(int from, int to)
        {
            var ids = Ids(from, to);
            Assert.That(ids.Length, Is.EqualTo(to - from + 1), "Thiếu bài trong index");
            foreach (var frame in new[] { new Vector2Int(1600, 720), new Vector2Int(1440, 1080) })
            {
                UseFrame(frame.x, frame.y);
                foreach (var id in ids)
                {
                    var lesson = TestLessons.Real.Get(id);
                    for (var i = 0; i < lesson.part1.Count; i++)
                    {
                        var v = Bind(id, i);
                        yield return null;
                        var where = $"{id} part1[{i}] {lesson.part1[i].type} {frame}";
                        try
                        {
                            LayoutProbe.AssertFits(Canvas);
                        }
                        catch (AssertionException e)
                        {
                            throw new AssertionException($"{where}: {e.Message}");
                        }
                        yield return ((ITestCompletable)v).CompleteForTest();
                        Assert.IsTrue(Done(v), where);
                        Object.Destroy(RootOf(v));
                        Ctx.Speech.Stop();
                    }
                    if (frame.x != 1600) continue; // Phần 2 dùng màn của tập 1, chỉ cần đi một khung hình
                    for (var r = 0; r < lesson.part2.Count; r++)
                    {
                        var v = BindRound(id, r);
                        yield return null;
                        yield return ((ITestCompletable)v).CompleteForTest();
                        Assert.IsTrue(Done(v), $"{id} part2[{r}]");
                        Object.Destroy(RootOf(v));
                        Ctx.Speech.Stop();
                    }
                }
            }
        }

        [UnityTest, Timeout(600000)] public IEnumerator Rimes81To99() => WalkLessons(81, 99);
        [UnityTest, Timeout(600000)] public IEnumerator Rimes100To125() => WalkLessons(100, 125);
        [UnityTest, Timeout(600000)] public IEnumerator Reading126To151() => WalkLessons(126, 151);
        [UnityTest, Timeout(600000)] public IEnumerator Reading152To171() => WalkLessons(152, 171);

        /// <summary>Bài dài nhất (Người nông dân và con gấu) chia trang, mỗi trang không tràn.</summary>
        [UnityTest]
        public IEnumerator LongestPassage_PagesFit()
        {
            UseFrame(1600, 720);
            var lesson = TestLessons.Real.Get("tv1_t2_b169");
            var index = lesson.part1.FindIndex(s => s.type == "passage");
            var v = (PassageView)Bind("tv1_t2_b169", index);
            yield return null;
            Assert.That(v.Text.PageCount, Is.GreaterThan(1));
            for (var p = 0; p < v.Text.PageCount; p++)
            {
                v.Text.ShowPage(p);
                yield return null;
                var rect = ((RectTransform)v.Text.transform).rect;
                Assert.That(v.Text.Label.preferredHeight, Is.LessThanOrEqualTo(rect.height + 1f), $"trang {p}");
            }
        }
    }
}
