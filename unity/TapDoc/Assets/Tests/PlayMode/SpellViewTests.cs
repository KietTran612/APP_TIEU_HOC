using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    public class SpellViewTests : ViewTestBase
    {
        [UnityTest]
        public IEnumerator Du_TapInOrder()
        {
            var v = Bind("tv1_t1_b13", 3);
            yield return WaitPracticeReady(v);
            CollectionAssert.AreEqual(new[] { "am_dd", "van_u", "tieng_ddu", "hd_danh_van_theo" }, Ctx.Speech.History);
            TileWithText(v, "u").SimulateTap();
            yield return null;
            Assert.IsTrue(TileWithText(v, "đ").IsHinted);
            TileWithText(v, "đ").SimulateTap();
            yield return new WaitForSeconds(.1f);
            TileWithText(v, "u").SimulateTap();
            yield return WaitCompleted(v);
            CollectionAssert.AreEqual(new[] { "am_dd", "van_u", "tieng_ddu", "tu_cais_ddu" }, Ctx.Speech.History.Skip(4));
        }

        [UnityTest]
        public IEnumerator DoubleTap_SameTile_PlaysOnce()
        {
            var v = Bind("tv1_t1_b13", 3);
            yield return WaitPracticeReady(v);
            TileWithText(v, "đ").SimulateTap();
            TileWithText(v, "đ").SimulateTap();
            yield return new WaitForSeconds(.2f);
            Assert.AreEqual(1, Ctx.Speech.History.Skip(4).Count(id => id == "am_dd"));
        }

        [UnityTest]
        public IEnumerator Cu_ToneMustBeDragged()
        {
            var v = Bind("tv1_t1_b13", 7);
            yield return WaitPracticeReady(v);
            TileWithText(v, "c").SimulateTap();
            yield return new WaitForSeconds(.1f);
            TileWithText(v, "ư").SimulateTap();
            yield return new WaitForSeconds(.3f);
            var tone = DragWithText(v, "ˀ");
            tone.GetComponent<Tile>().SimulateTap();
            yield return null;
            Assert.IsFalse(Done(v));
            tone.SimulateDropNowhere();
            yield return null;
            Assert.IsFalse(Done(v));
            tone.SimulateDropOn(ResultSlot(v));
            yield return WaitCompleted(v);
            Assert.That(Ctx.Speech.History.TakeLast(3), Is.EqualTo(new[] { "dau_hoi", "tieng_cuwr", "tu_cuwr_taj" }));
        }

        [UnityTest]
        public IEnumerator ToneAttach_ShowsImageWhenDone()
        {
            var v = Bind("tv1_t1_b04", 3);
            yield return WaitPracticeReady(v);
            Assert.IsFalse(ImageBox(v).activeSelf);
            DragWithText(v, "ˋ").SimulateDropOn(ResultSlot(v));
            yield return WaitCompleted(v);
            Assert.IsTrue(ImageBox(v).activeSelf);
        }

        [UnityTest]
        public IEnumerator CompleteForTest_FinishesEverySpellStep()
        {
            foreach (var (lesson, index) in new[] { ("tv1_t1_b13", 3), ("tv1_t1_b13", 7), ("tv1_t1_b42", 3), ("tv1_t1_b42", 4), ("tv1_t1_b04", 5) })
            {
                var v = Bind(lesson, index);
                yield return ((ITestCompletable)v).CompleteForTest();
                Assert.IsTrue(Done(v), $"{lesson} part1[{index}]");
                Object.Destroy(RootOf(v));
            }
        }
    }
}
