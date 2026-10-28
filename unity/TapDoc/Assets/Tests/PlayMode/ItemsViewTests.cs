using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    public class ItemsViewTests : ViewTestBase
    {
        [UnityTest]
        public IEnumerator Words_SpellEachThenRead()
        {
            var v = Bind("tv1_t1_b13", 8);
            TileWithText(v, "đu đủ").SimulateTap();
            yield return null;
            yield return CompleteOverlaySpell(v);
            yield return CompleteOverlaySpell(v);
            yield return new WaitForSeconds(.3f);
            Assert.AreEqual("tu_ddu_ddur", Ctx.Speech.History.Last());
            Assert.IsFalse(Done(v));
            TileWithText(v, "củ từ").SimulateTap();
            yield return CompleteOverlaySpell(v);
            yield return CompleteOverlaySpell(v);
            yield return WaitCompleted(v);
        }

        [UnityTest]
        public IEnumerator Words_NoteShownForNgan()
        {
            var v = Bind("tv1_t1_b42", 5);
            TileWithText(v, "đàn ngan").SimulateTap();
            yield return CompleteOverlaySpell(v);
            yield return CompleteOverlaySpell(v);
            yield return new WaitForSeconds(.3f);
            Assert.That(Labels(v), Has.Member("ngan: ở phía Nam gọi là vịt xiêm."));
        }

        [UnityTest]
        public IEnumerator Reading_AllEightItems()
        {
            var v = Bind("tv1_t1_b13", 10);
            foreach (var t in new[] { "cù", "cừ", "dù", "tư", "nụ", "mụ", "từ từ" })
            {
                TileWithText(v, t).SimulateTap();
                yield return new WaitForSeconds(.5f);
            }
            Assert.IsFalse(Done(v));
            TileWithText(v, "tù mù").SimulateTap();
            yield return WaitCompleted(v);
        }

        [UnityTest]
        public IEnumerator Sentence_TapTokenSpells_ThenDone()
        {
            var v = Bind("tv1_t1_b13", 9);
            TileWithText(v, "củ").SimulateTap();
            yield return new WaitForSeconds(.6f);
            CollectionAssert.AreEqual(new[] { "am_c", "van_u", "tieng_cu", "dau_hoi", "tieng_cur" }, Ctx.Speech.History);
            ButtonWithText(v, "Nghe cả câu").onClick.Invoke();
            yield return new WaitForSeconds(.3f);
            Assert.AreEqual("cau_b13_01", Ctx.Speech.History.Last());
            ButtonWithText(v, "Con đọc xong rồi").onClick.Invoke();
            yield return WaitCompleted(v);
        }

        [UnityTest]
        public IEnumerator Markers_ShownLikeBook()
        {
            var reading = Bind("tv1_t1_b13", 10);
            yield return null;
            Assert.AreEqual("img_chung_luyen_tap", MarkerOf(reading));
            var sentence = Bind("tv1_t1_b13", 9);
            yield return null;
            Assert.AreEqual("img_chung_em_doc", MarkerOf(sentence));
            var words = Bind("tv1_t1_b13", 8);
            yield return null;
            Assert.IsNull(MarkerOf(words));
        }

        [UnityTest]
        public IEnumerator CompleteForTest_FinishesItemSteps()
        {
            foreach (var (lesson, index) in new[] { ("tv1_t1_b13", 8), ("tv1_t1_b13", 9), ("tv1_t1_b13", 10), ("tv1_t1_b42", 5), ("tv1_t1_b04", 7) })
            {
                var v = Bind(lesson, index);
                yield return ((ITestCompletable)v).CompleteForTest();
                Assert.IsTrue(Done(v), $"{lesson} part1[{index}]");
                Object.Destroy(RootOf(v));
            }
        }
    }
}
