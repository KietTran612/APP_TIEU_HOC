using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// Đi hết Phần 1 và Phần 2 của mọi mục lớp 2 (Tiếng Việt 2 tập một, mục 172–304) trên dữ liệu thật (tranh, âm thanh
    /// giả): mỗi màn dựng được, vừa hai khung hình thử, không chữ tràn, và làm xong được. Chia theo đợt để biết đợt nào
    /// hỏng (thiết kế TV2 tập một, mục 11).
    /// </summary>
    public class Grade2LessonSmokeTests : ViewTestBase
    {
        private static string[] Ids(int from, int to) => TestLessons.Real.Index.lessons
            .Where(e => e.book == "tv2_t1_2001" && e.lesson_no >= from && e.lesson_no <= to)
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
            Assert.That(ids.Length, Is.EqualTo(to - from + 1), "Thiếu mục trong index");
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
                    if (frame.x != 1600) continue; // Phần 2 dùng màn có sẵn, chỉ cần một khung hình
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

        [UnityTest, Timeout(900000)] public IEnumerator Weeks1To3() => WalkLessons(172, 195);
        [UnityTest, Timeout(900000)] public IEnumerator Weeks4To8() => WalkLessons(196, 234);
        [UnityTest, Timeout(900000)] public IEnumerator Weeks9To13() => WalkLessons(235, 273);
        [UnityTest, Timeout(900000)] public IEnumerator Weeks14To17() => WalkLessons(274, 304);
    }
}
