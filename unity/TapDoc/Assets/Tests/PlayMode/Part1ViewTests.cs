using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    public class Part1ViewTests : ViewTestBase
    {
        [UnityTest]
        public IEnumerator Unit_CompletesAfterTap()
        {
            var v = Bind("tv1_t1_b13", 0);
            yield return new WaitForSeconds(.2f);
            Assert.IsFalse(Done(v));
            TileWithText(v, "u").SimulateTap();
            yield return WaitCompleted(v);
            Assert.AreEqual("van_u", Ctx.Speech.History.Last());
        }

        [UnityTest]
        public IEnumerator Keyword_ShowsHighlight()
        {
            var v = Bind("tv1_t1_b13", 1);
            yield return null;
            Assert.That(Labels(v), Has.Member("cái đ<color=#1F8A9E>u</color>"));
        }

        [UnityTest]
        public IEnumerator Keyword_MissingImage_HidesImageBox()
        {
            UseImageLoader(id => null);
            LogAssert.Expect(LogType.Error, "[TapDoc] Thiếu tranh: img_b13_cais_ddu");
            var v = Bind("tv1_t1_b13", 1);
            yield return null;
            Assert.IsFalse(ImageBox(v).activeSelf);
        }

        [UnityTest]
        public IEnumerator Analyze_NeedsAllRows()
        {
            var v = Bind("tv1_t1_b13", 2);
            TileWithText(v, "cái đu").SimulateTap();
            TileWithText(v, "đu").SimulateTap();
            yield return new WaitForSeconds(.3f);
            Assert.IsFalse(Done(v));
            TileWithText(v, "u").SimulateTap();
            yield return WaitCompleted(v);
            Assert.That(Ctx.Speech.History, Is.SupersetOf(new[] { "tu_cais_ddu", "tieng_ddu", "van_u" }));
        }

        [UnityTest]
        public IEnumerator ToneIntro_CompletesAfterAudio()
        {
            var v = Bind("tv1_t1_b04", 2);
            yield return WaitCompleted(v);
            Assert.AreEqual("dau_huyen", Ctx.Speech.History[0]);
        }

        [UnityTest]
        public IEnumerator Picture_CompletesAfterTap()
        {
            var v = Bind("tv1_t1_b04", 6);
            yield return new WaitForSeconds(.2f);
            Assert.IsFalse(Done(v));
            TileWithImage(v, "img_b04_mua").SimulateTap();
            yield return WaitCompleted(v);
            Assert.AreEqual("hd_b04_tranh_01", Ctx.Speech.History.Last());
        }
    }
}
