using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    public class RoundViewTests : ViewTestBase
    {
        [UnityTest]
        public IEnumerator ListenChoose_HintAfterTwoWrong()
        {
            var r = BindRound("tv1_t1_b13", 0); // đáp án "u"
            yield return new WaitForSeconds(.3f);
            TileWithText(r, "ư").SimulateTap();
            yield return new WaitForSeconds(.3f);
            Assert.That(Ctx.Speech.History, Has.Member("hd_thu_lai"));
            TileWithText(r, "o").SimulateTap();
            yield return new WaitForSeconds(.3f);
            Assert.IsTrue(TileWithText(r, "u").IsHinted);
            TileWithText(r, "u").SimulateTap();
            yield return WaitCompleted(r);
            Assert.That(Ctx.Speech.History.Last(), Does.StartWith("khen_"));
        }

        [UnityTest]
        public IEnumerator LookTone_DragCorrectTone()
        {
            var r = BindRound("tv1_t1_b04", 3); // chữ mẫu "cá"
            yield return new WaitForSeconds(.3f);
            DragWithText(r, "ˋ").SimulateDropOn(Slot(r));
            yield return new WaitForSeconds(.3f);
            Assert.IsFalse(Done(r));
            DragWithText(r, "ˊ").SimulateDropOn(Slot(r));
            yield return WaitCompleted(r);
            Assert.That(Labels(r), Has.Member("cá"));
        }

        [UnityTest]
        public IEnumerator Compose_FillsTemplate()
        {
            var r = BindRound("tv1_t1_b13", 6); // "củ t_" ← "ừ"
            yield return new WaitForSeconds(.3f);
            DragWithText(r, "ù").SimulateDropOn(Slot(r));
            yield return new WaitForSeconds(.3f);
            Assert.IsFalse(Done(r));
            DragWithText(r, "ừ").SimulateDropOn(Slot(r));
            yield return WaitCompleted(r);
            Assert.That(Labels(r), Has.Member("củ từ"));
        }

        [UnityTest]
        public IEnumerator ListenPicture_TapCorrect()
        {
            var r = BindRound("tv1_t1_b42", 6); // "đàn ngan"
            yield return new WaitForSeconds(.3f);
            TileWithImage(r, "img_b42_ddanf_ngan").SimulateTap();
            yield return WaitCompleted(r);
        }

        [UnityTest]
        public IEnumerator CompleteForTest_FinishesEveryRound()
        {
            foreach (var lesson in new[] { "tv1_t1_b04", "tv1_t1_b13", "tv1_t1_b42" })
            {
                var count = LessonRepository.Load(lesson).part2.Count;
                for (var i = 0; i < count; i++)
                {
                    var r = BindRound(lesson, i);
                    yield return ((ITestCompletable)r).CompleteForTest();
                    Assert.IsTrue(Done(r), $"{lesson} part2[{i}]");
                    Object.Destroy(RootOf(r));
                }
            }
        }
    }
}
