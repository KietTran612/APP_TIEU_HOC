using System.Collections;
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    /// <summary>Màn bảng nhóm vần (bài 79): 7 cột âm cuối, phân trang 3 hàng nguyên âm mỗi trang.</summary>
    public class RimeGridViewTests : ViewTestBase
    {
        private static Step Grid()
        {
            var finals = new[] { "n", "m", "c", "t", "p", "i-y", "o-u" };
            var vowels = new[] { "a", "ă", "â", "o", "ô", "ơ", "e", "ê", "i", "u", "ư" };
            var step = new Step { type = "rime_grid" };

            for (var c = 0; c < finals.Length; c++)
                step.items.Add(new Item { role = "final", col = c, text = finals[c] });
            for (var r = 0; r < vowels.Length; r++)
                step.items.Add(new Item { role = "vowel", row = r, text = vowels[r] });

            void AddCell(int row, int col, string text, params (string v, string f, string rime)[] rimes)
            {
                var item = new Item { role = "cell", row = row, col = col, text = text };
                foreach (var (v, f, rime) in rimes)
                {
                    item.spells.Add(new Spell
                    {
                        target = rime,
                        parts = new List<Part>
                        {
                            new() { kind = "vowel", text = v, audio = "van_" + v },
                            // Như công cụ dựng bài: âm cuối là phụ âm đọc "am_", là nguyên âm i/y/o/u đọc "van_".
                            new() { kind = "final", text = f, audio = ("iyou".Contains(f) ? "van_" : "am_") + f },
                            new() { kind = "join", text = rime, audio = "van_" + rime }
                        }
                    });
                }
                step.items.Add(item);
            }

            // Hàng 0: a
            AddCell(0, 0, "an", ("a", "n", "an"));
            AddCell(0, 1, "am", ("a", "m", "am"));
            AddCell(0, 2, "ac", ("a", "c", "ac"));
            AddCell(0, 3, "at", ("a", "t", "at"));
            AddCell(0, 4, "ap", ("a", "p", "ap"));
            AddCell(0, 5, "ai - ay", ("a", "i", "ai"), ("a", "y", "ay"));
            AddCell(0, 6, "ao - au", ("a", "o", "ao"), ("a", "u", "au"));

            // Hàng 1: ă
            AddCell(1, 0, "ăn", ("ă", "n", "ăn"));
            AddCell(1, 1, "ăm", ("ă", "m", "ăm"));
            AddCell(1, 2, "ăc", ("ă", "c", "ăc"));
            AddCell(1, 3, "ăt", ("ă", "t", "ăt"));
            AddCell(1, 4, "ăp", ("ă", "p", "ăp"));

            // Hàng 2: â
            AddCell(2, 0, "ân", ("â", "n", "ân"));
            AddCell(2, 1, "âm", ("â", "m", "âm"));
            AddCell(2, 2, "âc", ("â", "c", "âc"));
            AddCell(2, 3, "ât", ("â", "t", "ât"));
            AddCell(2, 4, "âp", ("â", "p", "âp"));
            AddCell(2, 5, "ây", ("â", "y", "ây"));
            AddCell(2, 6, "âu", ("â", "u", "âu"));

            // Hàng 3: o
            AddCell(3, 0, "on", ("o", "n", "on"));
            AddCell(3, 1, "om", ("o", "m", "om"));
            AddCell(3, 2, "oc", ("o", "c", "oc"));
            AddCell(3, 3, "ot", ("o", "t", "ot"));
            AddCell(3, 4, "op", ("o", "p", "op"));
            AddCell(3, 5, "oi", ("o", "i", "oi"));

            // Hàng 4: ô
            AddCell(4, 0, "ôn", ("ô", "n", "ôn"));
            AddCell(4, 1, "ôm", ("ô", "m", "ôm"));
            AddCell(4, 2, "ôc", ("ô", "c", "ôc"));
            AddCell(4, 3, "ôt", ("ô", "t", "ôt"));
            AddCell(4, 4, "ôp", ("ô", "p", "ôp"));
            AddCell(4, 5, "ôi", ("ô", "i", "ôi"));

            // Hàng 5: ơ
            AddCell(5, 0, "ơn", ("ơ", "n", "ơn"));
            AddCell(5, 1, "ơm", ("ơ", "m", "ơm"));
            AddCell(5, 3, "ơt", ("ơ", "t", "ơt"));
            AddCell(5, 4, "ơp", ("ơ", "p", "ơp"));
            AddCell(5, 5, "ơi", ("ơ", "i", "ơi"));

            // Hàng 6: e
            AddCell(6, 0, "en", ("e", "n", "en"));
            AddCell(6, 1, "em", ("e", "m", "em"));
            AddCell(6, 2, "ec", ("e", "c", "ec"));
            AddCell(6, 3, "et", ("e", "t", "et"));
            AddCell(6, 4, "ep", ("e", "p", "ep"));
            AddCell(6, 6, "eo", ("e", "o", "eo"));

            // Hàng 7: ê
            AddCell(7, 0, "ên", ("ê", "n", "ên"));
            AddCell(7, 1, "êm", ("ê", "m", "êm"));
            AddCell(7, 3, "êt", ("ê", "t", "êt"));
            AddCell(7, 4, "êp", ("ê", "p", "êp"));
            AddCell(7, 6, "êu", ("ê", "u", "êu"));

            // Hàng 8: i
            AddCell(8, 0, "in", ("i", "n", "in"));
            AddCell(8, 1, "im", ("i", "m", "im"));
            AddCell(8, 3, "it", ("i", "t", "it"));
            AddCell(8, 4, "ip", ("i", "p", "ip"));
            AddCell(8, 6, "iu", ("i", "u", "iu"));

            // Hàng 9: u
            AddCell(9, 0, "un", ("u", "n", "un"));
            AddCell(9, 1, "um", ("u", "m", "um"));
            AddCell(9, 2, "uc", ("u", "c", "uc"));
            AddCell(9, 3, "ut", ("u", "t", "ut"));
            AddCell(9, 4, "up", ("u", "p", "up"));
            AddCell(9, 5, "ui", ("u", "i", "ui"));

            // Hàng 10: ư
            AddCell(10, 2, "ưc", ("ư", "c", "ưc"));
            AddCell(10, 3, "ưt", ("ư", "t", "ưt"));
            AddCell(10, 5, "ưi", ("ư", "i", "ưi"));
            AddCell(10, 6, "ưu", ("ư", "u", "ưu"));

            return step;
        }

        [UnityTest]
        public IEnumerator RimeGrid_TapCellSpells()
        {
            var v = CreateTrackedStep(Grid());
            TileWithText(v, "ac").SimulateTap();
            yield return new WaitForSeconds(.4f);
            Assert.AreEqual(
                new[] { "van_a", "am_c", "van_ac" },
                Ctx.Speech.History.Skip(Ctx.Speech.History.Count - 3).ToArray());
            Assert.IsFalse(Done(v));
        }

        [UnityTest]
        public IEnumerator RimeGrid_TwoRimeCellSpellsBoth()
        {
            var v = CreateTrackedStep(Grid());
            TileWithText(v, "ai - ay").SimulateTap();
            yield return new WaitForSeconds(.6f);
            Assert.AreEqual(
                new[] { "van_a", "van_i", "van_ai", "van_a", "van_y", "van_ay" },
                Ctx.Speech.History.Skip(Ctx.Speech.History.Count - 6).ToArray());
        }

        [UnityTest]
        public IEnumerator RimeGrid_PagesAndComplete()
        {
            // Đi trang bằng nút thật, mỗi trang chạm một ô; chỉ xong khi trang cuối cũng đã chạm.
            var v = (RimeGridView)CreateTrackedStep(Grid());
            Assert.AreEqual(4, v.PageCount);
            for (var p = 0; p < v.PageCount; p++)
            {
                Assert.AreEqual(p, v.Page);
                ActiveTiles(v).First().SimulateTap();
                yield return new WaitForSeconds(.4f);
                if (p < v.PageCount - 1)
                {
                    Assert.IsFalse(Done(v), $"Mới chạm tới trang {p + 1} đã báo xong");
                    ButtonWithText(v, UiText.PageNext).onClick.Invoke();
                    yield return null;
                }
            }
            Assert.IsTrue(Done(v));
        }

        [UnityTest]
        public IEnumerator RimeGrid_ShowsOnlyCurrentPage()
        {
            var v = (RimeGridView)CreateTrackedStep(Grid());
            yield return null;
            // Trang 1: hàng a (7 ô), ă (5 ô), â (7 ô).
            CollectionAssert.AreEquivalent(
                new[] { "an", "am", "ac", "at", "ap", "ai - ay", "ao - au", "ăn", "ăm", "ăc", "ăt", "ăp",
                        "ân", "âm", "âc", "ât", "âp", "ây", "âu" },
                ActiveTiles(v).Select(t => t.PlainText).ToArray());
            Assert.IsFalse(ButtonWithText(v, UiText.PagePrev).gameObject.activeInHierarchy);
            Assert.IsTrue(ButtonWithText(v, UiText.PageNext).gameObject.activeInHierarchy);
            for (var p = 1; p < v.PageCount; p++) ButtonWithText(v, UiText.PageNext).onClick.Invoke();
            yield return null;
            // 11 hàng, 3 hàng mỗi trang: trang cuối còn 2 hàng u, ư.
            CollectionAssert.AreEquivalent(
                new[] { "un", "um", "uc", "ut", "up", "ui", "ưc", "ưt", "ưi", "ưu" },
                ActiveTiles(v).Select(t => t.PlainText).ToArray());
            Assert.IsTrue(ButtonWithText(v, UiText.PagePrev).gameObject.activeInHierarchy);
            Assert.IsFalse(ButtonWithText(v, UiText.PageNext).gameObject.activeInHierarchy);
        }

        [UnityTest]
        public IEnumerator RimeGrid_FitsStage_NoOverlap([Values(2400, 2048)] int width)
        {
            // Như bảng ghép (Đợt 1): mọi ô, nhãn hàng/cột và nút trang nằm trong Stage, không chồng nhau, ở mọi trang.
            Cam.targetTexture = null;
            Object.Destroy(TargetTex);
            TargetTex = new RenderTexture(width, width == 2400 ? 1080 : 1536, 24);
            Cam.targetTexture = TargetTex;
            var v = (RimeGridView)CreateTrackedStep(Grid());
            for (var p = 0; p < v.PageCount; p++)
            {
                if (p > 0) ButtonWithText(v, UiText.PageNext).onClick.Invoke();
                yield return null;
                var stage = Ctx.Stage;
                var root = RootOf(v).transform;
                var rects = new List<(string name, Rect rect)>();
                foreach (var t in ActiveTiles(v)) rects.Add(("ô " + t.PlainText, RectIn(stage, (RectTransform)t.transform)));
                foreach (var b in RootOf(v).GetComponentsInChildren<UnityEngine.UI.Button>(false))
                    if (b.GetComponent<Tile>() == null) rects.Add(("nút " + b.GetComponentInChildren<TMP_Text>().text, RectIn(stage, (RectTransform)b.transform)));
                foreach (var label in RootOf(v).GetComponentsInChildren<TMP_Text>(false))
                    if (label.transform.parent == root) rects.Add(("nhãn " + label.text, RectIn(stage, label.rectTransform)));
                var bounds = stage.rect;
                foreach (var (name, r) in rects)
                    Assert.IsTrue(r.xMin >= bounds.xMin - 1f && r.xMax <= bounds.xMax + 1f && r.yMin >= bounds.yMin - 1f && r.yMax <= bounds.yMax + 1f,
                        $"trang {p + 1}: '{name}' ra ngoài Stage {r} / {bounds}");
                for (var i = 0; i < rects.Count; i++)
                    for (var j = i + 1; j < rects.Count; j++)
                    {
                        var a = rects[i].rect; var b = rects[j].rect;
                        var overlap = Mathf.Min(a.xMax, b.xMax) - Mathf.Max(a.xMin, b.xMin) > 1f && Mathf.Min(a.yMax, b.yMax) - Mathf.Max(a.yMin, b.yMin) > 1f;
                        Assert.IsFalse(overlap, $"trang {p + 1}: '{rects[i].name}' chồng lên '{rects[j].name}'");
                    }
            }
        }

        [UnityTest]
        public IEnumerator RimeGrid_LayoutFits_2048x1536()
        {
            Cam.targetTexture = null;
            Object.Destroy(TargetTex);
            TargetTex = new RenderTexture(2048, 1536, 24);
            Cam.targetTexture = TargetTex;
            var v = (RimeGridView)CreateTrackedStep(Grid());
            for (var p = 0; p < v.PageCount; p++)
            {
                if (p > 0) ButtonWithText(v, UiText.PageNext).onClick.Invoke();
                yield return null;
                LayoutProbe.AssertFits(Canvas);
            }
        }

        [UnityTest] public IEnumerator RimeGrid_Lesson79() { var v = Bind("tv1_t1_b79", GridIndex("tv1_t1_b79")); yield return ((ITestCompletable)v).CompleteForTest(); Assert.IsTrue(Done(v)); }

        private static IEnumerable<Tile> ActiveTiles(object view) => RootOf(view).GetComponentsInChildren<Tile>(false);

        private static Rect RectIn(RectTransform space, RectTransform rt)
        {
            var c = new Vector3[4];
            rt.GetWorldCorners(c);
            var min = (Vector2)space.InverseTransformPoint(c[0]);
            var max = (Vector2)space.InverseTransformPoint(c[2]);
            return Rect.MinMaxRect(min.x, min.y, max.x, max.y);
        }

        private static int GridIndex(string lid) => LessonRepository.Load(lid).part1.FindIndex(s => s.type == "rime_grid");
    }
}
