using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// Đi hết Phần 1 và Phần 2 của mọi mục Tiếng Việt 2 tập hai ("Bé tập đọc 4", mục 305–434) trên dữ liệu thật (tranh,
    /// âm thanh giả): mỗi màn dựng được, vừa hai khung hình thử, không chữ tràn, và làm xong được. Chia theo đợt để biết
    /// đợt nào hỏng (thiết kế TV2 tập hai, mục 11). Cùng cách đi như <see cref="Grade2LessonSmokeTests"/> của tập một.
    /// </summary>
    public class Grade2Tap2LessonSmokeTests : ViewTestBase
    {
        private static string[] Ids(int from, int to) => TestLessons.Real.Index.lessons
            .Where(e => e.book == "tv2_t2_2002" && e.lesson_no >= from && e.lesson_no <= to)
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

        [UnityTest, Timeout(900000)] public IEnumerator Weeks18To21() => WalkLessons(305, 338);
        [UnityTest, Timeout(900000)] public IEnumerator Weeks22To25() => WalkLessons(339, 370);
        [UnityTest, Timeout(900000)] public IEnumerator Weeks26To29() => WalkLessons(371, 402);
        [UnityTest, Timeout(900000)] public IEnumerator Weeks30To33() => WalkLessons(403, 434);
    }
}
