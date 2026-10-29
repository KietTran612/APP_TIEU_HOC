using System.Collections;
using System.Linq;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    /// <summary>Màn của ba loại bước mới (bảng dấu, khung chữ, bảng ghép) và thẻ kí hiệu dấu.</summary>
    public class NewStepViewTests : ViewTestBase
    {
        [UnityTest]
        public IEnumerator ToneTable_FillAllFive()
        {
            var v = Bind("tv1_t1_b06", 6);
            DragForTone(v, "hoi").SimulateDropOn(SlotForTone(v, "huyen"));   // sai ô: không nhận, không phạt
            yield return null;
            Assert.IsFalse(Done(v));
            Assert.That(Labels(v), Has.No.Member("đỏ"));
            foreach (var t in new[] { "huyen", "sac", "hoi", "nga", "nang" })
            {
                DragForTone(v, t).SimulateDropOn(SlotForTone(v, t));
                yield return new WaitForSeconds(.3f);
            }
            yield return WaitCompleted(v);
            Assert.That(Labels(v), Is.SupersetOf(new[] { "đò", "đó", "đỏ", "đõ", "đọ" }));
            Assert.That(Ctx.Speech.History, Has.Member("dau_nga"));
        }

        [UnityTest]
        public IEnumerator ToneTable_MarksSitLikeTheBook()
        {
            // Như sách: dấu huyền, sắc, hỏi, ngã in phía trên ô; dấu nặng in phía dưới ô.
            var v = Bind("tv1_t1_b06", 6);
            yield return null;
            var root = RootOf(v).transform;
            var marks = RootOf(v).GetComponentsInChildren<TMP_Text>(true).Where(t => t.GetComponentInParent<Tile>() == null).ToList();
            foreach (var tone in new[] { "huyen", "sac", "hoi", "nga", "nang" })
            {
                var cell = (RectTransform)SlotForTone(v, tone).transform;
                var glyph = Ctx.Lesson.part1[6].items.First(i => i.tone == tone).glyph;
                var mark = marks.Single(t => t.text == glyph);
                var ink = InkBounds(mark, root);
                var top = cell.anchoredPosition.y + cell.rect.height / 2f;
                var bottom = cell.anchoredPosition.y - cell.rect.height / 2f;
                if (tone == "nang") Assert.Less(ink.max.y, bottom, "dấu nặng phải nằm dưới ô");
                else Assert.Greater(ink.min.y, top, $"dấu {tone} phải nằm trên ô");
                Assert.AreEqual(cell.anchoredPosition.x, ink.center.x, 12f, $"dấu {tone} phải ở giữa ô");
            }
        }

        [UnityTest]
        public IEnumerator ToneTable_FilledCellIsNotRefilled()
        {
            var v = Bind("tv1_t1_b06", 6);
            DragForTone(v, "sac").SimulateDropOn(SlotForTone(v, "sac"));
            yield return new WaitForSeconds(.3f);
            Assert.IsFalse(DragForTone(v, "sac").gameObject.activeInHierarchy);
            Assert.IsFalse(Done(v));
        }

        [UnityTest]
        public IEnumerator LetterGrid_AllTapped()
        {
            var v = Bind("tv1_t1_b07", 0);
            yield return ((ITestCompletable)v).CompleteForTest();
            Assert.IsTrue(Done(v));
        }

        [UnityTest]
        public IEnumerator LetterGrid_NotDoneUntilEveryTileTapped()
        {
            var v = Bind("tv1_t1_b07", 0);
            TileWithText(v, "o").SimulateTap();
            yield return new WaitForSeconds(.5f);
            Assert.IsFalse(Done(v));
            Assert.AreEqual("van_o", Ctx.Speech.History.Last());
        }

        [UnityTest]
        public IEnumerator CombineTable_EachOnsetOnce()
        {
            var v = Bind("tv1_t1_b07", 1);
            TileWithText(v, "c").SimulateTap();
            TileWithText(v, "o").SimulateTap();
            yield return new WaitForSeconds(.5f);
            Assert.That(Ctx.Speech.History, Has.Member("tieng_co"));
            Assert.That(Labels(v), Has.Member("có"));
            Assert.IsFalse(Done(v));
            TileWithText(v, "d").SimulateTap();
            TileWithText(v, "a").SimulateTap();
            yield return new WaitForSeconds(.5f);
            TileWithText(v, "đ").SimulateTap();
            TileWithText(v, "o").SimulateTap();
            yield return WaitCompleted(v);
            Assert.AreEqual(SystemImages.ForMarker("●"), MarkerOf(v));   // sách in ● trước bảng ghép
        }

        [UnityTest]
        public IEnumerator CombineTable_FormTapPlaysItsSpelling()
        {
            var v = Bind("tv1_t1_b07", 1);
            TileWithText(v, "c").SimulateTap();
            TileWithText(v, "a").SimulateTap();
            yield return new WaitForSeconds(.5f);
            TileWithText(v, "cả").SimulateTap();
            yield return new WaitForSeconds(.5f);
            Assert.AreEqual(new[] { "tieng_ca", "dau_hoi", "tieng_car" }, Ctx.Speech.History.Skip(Ctx.Speech.History.Count - 3).ToArray());
        }

        [UnityTest]
        public IEnumerator CombineTable_17_FitsStage()
        {
            var v = Bind("tv1_t1_b17", 1);
            yield return null;
            var stage = Ctx.Stage.rect;
            foreach (var t in RootOf(v).GetComponentsInChildren<Tile>(true))
            {
                var rt = (RectTransform)t.transform;
                var c = rt.anchoredPosition;
                Assert.LessOrEqual(Mathf.Abs(c.x) + rt.rect.width / 2f, stage.width / 2f + .5f, t.PlainText);
                Assert.LessOrEqual(Mathf.Abs(c.y) + rt.rect.height / 2f, stage.height / 2f + .5f, t.PlainText);
            }
        }

        [UnityTest]
        public IEnumerator GlyphTile_IsCenteredAndLarge()   // việc tồn: dấu nhỏ và nằm cao
        {
            var v = Bind("tv1_t1_b06", 0);
            yield return null;
            var tile = RootOf(v).GetComponentsInChildren<Tile>(true).First(t => t.Tone == "hoi");
            // Đo nét chữ thật: textBounds của TMP là chiều cao dòng, không phải nét kí hiệu.
            var ink = InkBounds(tile.GetComponentInChildren<TMP_Text>(), tile.transform);
            var h = ((RectTransform)tile.transform).rect.height;
            Assert.LessOrEqual(Mathf.Abs(ink.center.y), .15f * h);
            Assert.GreaterOrEqual(ink.size.y, .3f * h);
        }

        /// <summary>Mọi thẻ kí hiệu dấu trong màn: nét kí hiệu to và nằm giữa thẻ.</summary>
        private static void AssertGlyphTilesLarge(object view)
        {
            var tiles = RootOf(view).GetComponentsInChildren<Tile>(true).Where(t => !string.IsNullOrEmpty(t.Tone) && t.PlainText.Length == 1).ToList();
            Assert.IsNotEmpty(tiles, "Màn không có thẻ kí hiệu dấu");
            foreach (var tile in tiles)
            {
                var ink = InkBounds(tile.GetComponentInChildren<TMP_Text>(), tile.transform);
                var h = ((RectTransform)tile.transform).rect.height;
                var w = ((RectTransform)tile.transform).rect.width;
                Assert.LessOrEqual(Mathf.Abs(ink.center.y), .15f * h, $"dấu {tile.Tone} lệch khỏi giữa thẻ");
                Assert.GreaterOrEqual(Mathf.Max(ink.size.y / h, ink.size.x / w), .3f, $"dấu {tile.Tone} quá nhỏ ({ink.size})");
            }
        }

        [UnityTest]
        public IEnumerator LookTone_GlyphOptionsAreLarge()
        {
            var r = BindRound("tv1_t1_b17", 5);   // nhìn "mỡ", kéo dấu ngã hay dấu hỏi
            yield return null;
            AssertGlyphTilesLarge(r);
        }

        [UnityTest]
        public IEnumerator LetterGrid_GlyphTilesAreLarge()
        {
            var v = Bind("tv1_t1_b07", 0);
            yield return null;
            AssertGlyphTilesLarge(v);
        }

        [UnityTest]
        public IEnumerator Spell_ToneTileIsLarge()
        {
            var v = Bind("tv1_t1_b06", 1);   // gắn dấu hỏi: "co – hỏi – cỏ"
            yield return null;
            AssertGlyphTilesLarge(v);
        }

        [UnityTest]
        public IEnumerator Reading_LongRowWrapsInsideStage()
        {
            var v = Bind("tv1_t1_b15", 6);
            yield return null;
            var stage = Ctx.Stage.rect;
            var tiles = RootOf(v).GetComponentsInChildren<Tile>(true);
            Assert.AreEqual(13, tiles.Length);
            foreach (var t in tiles)
            {
                var rt = (RectTransform)t.transform;
                Assert.LessOrEqual(Mathf.Abs(rt.anchoredPosition.x) + rt.rect.width / 2f, stage.width / 2f, t.PlainText);
            }
            Assert.Greater(tiles.Select(t => ((RectTransform)t.transform).anchoredPosition.y).Distinct().Count(), 2);
        }

        [UnityTest]
        public IEnumerator Sentence_LongSentenceWraps()
        {
            var v = Bind("tv1_t1_b12", 10);
            yield return null;
            var stage = Ctx.Stage.rect;
            var tokens = RootOf(v).GetComponentsInChildren<Tile>(true);
            foreach (var t in tokens)
            {
                var rt = (RectTransform)t.transform;
                Assert.LessOrEqual(Mathf.Abs(rt.anchoredPosition.x) + rt.rect.width / 2f, stage.width / 2f, t.PlainText);
            }
        }
    }
}
