using System.Collections;
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    /// <summary>Màn cặp chữ, quy tắc, chọn chữ hoa và các ô không ghép được.</summary>
    public class NewStepViewTests2 : ViewTestBase
    {
        private static Step Pairs(int count = 20)
        {
            var letters = new[] { "a", "ă", "â", "b", "c", "d", "đ", "e", "ê", "g", "h", "i", "k", "l", "m", "n", "o", "ô", "ơ", "p" };
            var step = new Step { type = "letter_pairs" };
            for (var i = 0; i < count; i++)
                step.items.Add(new Item { role = "pair", text = letters[i], upper = letters[i].ToUpperInvariant(), audio = "chu_" + i, row = i / 4, col = i % 4 });
            return step;
        }

        private static Step Rules() => new Step
        {
            type = "rule", marker = "⌂",
            items = new List<Item>
            {
                new() { role = "line", text = "k chỉ ghép với e, ê, i", audio = "cau_b40_01" },
                new() { role = "line", text = "c ghép với a, o, ô, ơ, u, ư", audio = "cau_b40_02" },
                new() { role = "line", text = "Con nhớ quy tắc nhé", audio = "cau_b40_03" }
            }
        };

        [UnityTest]
        public IEnumerator LetterPairs_PagesAndComplete()
        {
            var v = (LetterPairsView)CreateTrackedStep(Pairs());
            Assert.AreEqual(2, v.PageCount);
            Assert.AreEqual(0, v.Page);
            var tiles = RootOf(v).GetComponentsInChildren<Tile>(false);
            Assert.AreEqual(16, tiles.Length);
            foreach (var tile in tiles) tile.SimulateTap();
            yield return new WaitForSeconds(.3f);
            Assert.IsFalse(Done(v));
            Assert.That(Labels(v), Has.Some.Contains("Ă"));
            Assert.IsFalse(ButtonWithText(v, UiText.PagePrev).gameObject.activeSelf);
            ButtonWithText(v, UiText.PageNext).onClick.Invoke();
            Assert.AreEqual(1, v.Page);
            Assert.AreEqual(4, RootOf(v).GetComponentsInChildren<Tile>(false).Length);
            Assert.IsFalse(ButtonWithText(v, UiText.PageNext).gameObject.activeSelf);
            ButtonWithText(v, UiText.PagePrev).onClick.Invoke();
            Assert.AreEqual(0, v.Page);
            yield return ((ITestCompletable)v).CompleteForTest();
            Assert.IsTrue(Done(v));
        }

        [UnityTest]
        public IEnumerator LetterPairs_TapPlaysAudio()
        {
            var v = CreateTrackedStep(Pairs());
            TileWithText(v, "ă   Ă").SimulateTap();
            yield return new WaitForSeconds(.3f);
            Assert.AreEqual("chu_1", Ctx.Speech.History.Last());
        }

        [UnityTest]
        public IEnumerator Rule_TapReadsLine_NotDoneUntilAll()
        {
            var v = CreateTrackedStep(Rules());
            TileWithText(v, "k chỉ ghép với e, ê, i").SimulateTap();
            yield return new WaitForSeconds(.3f);
            Assert.AreEqual("cau_b40_01", Ctx.Speech.History.Last());
            Assert.IsFalse(Done(v));
            yield return ((ITestCompletable)v).CompleteForTest();
            Assert.IsTrue(Done(v));
        }

        [UnityTest]
        public IEnumerator MatchCase_WrongThenRight()
        {
            var v = CreateTrackedRound(new Round
            {
                kind = "match_case", prompt_text = "ă", answer = 1,
                instruction_audio = "hd_nhin_chon_chu_hoa", prompt_audio = "",
                options = new List<Option> { new() { text = "A" }, new() { text = "Ă" }, new() { text = "Â" } }
            });
            yield return new WaitForSeconds(.3f);
            TileWithText(v, "A").SimulateTap();
            yield return new WaitForSeconds(.3f);
            Assert.IsFalse(Done(v));
            TileWithText(v, "Ă").SimulateTap();
            yield return WaitCompleted(v);
        }

        [UnityTest]
        public IEnumerator CombineTable_BlockedCell_DoesNothing()
        {
            var v = CreateTrackedStep(new Step
            {
                type = "combine_table",
                items = new List<Item>
                {
                    new() { role = "onset", text = "k", audio = "chu_k", row = 0 },
                    new() { role = "onset", text = "c", audio = "chu_c", row = 1 },
                    new() { role = "vowel", text = "a", audio = "van_a", col = 0 },
                    new() { role = "vowel", text = "e", audio = "van_e", col = 1 },
                    new() { role = "blocked", row = 0, col = 0, text = "", audio = "" },
                    new() { role = "base", text = "ke", audio = "tieng_ke", row = 0, col = 1 },
                    new() { role = "base", text = "ca", audio = "tieng_ca", row = 1, col = 0 }
                }
            });
            TileWithText(v, "k").SimulateTap();
            yield return new WaitForSeconds(.3f);
            var count = Ctx.Speech.History.Count;
            var vowel = TileWithText(v, "a");
            vowel.SimulateTap();
            yield return new WaitForSeconds(.3f);
            Assert.AreEqual(count, Ctx.Speech.History.Count);
            Assert.That(Labels(v), Has.No.Member("ka"));
            var blocked = vowel.transform.Find("Blocked");
            Assert.IsNotNull(blocked);
            Assert.IsTrue(blocked.gameObject.activeSelf);
            Assert.IsFalse(Done(v));
            TileWithText(v, "c").SimulateTap();
            Assert.IsFalse(blocked.gameObject.activeSelf);
            vowel.SimulateTap();
            yield return new WaitForSeconds(.3f);
            Assert.IsFalse(Done(v)); // ô bị chặn chưa tính âm đầu k là đã ghép
            TileWithText(v, "k").SimulateTap();
            TileWithText(v, "e").SimulateTap();
            yield return WaitCompleted(v);
        }

        [UnityTest]
        public IEnumerator Reading_LabelsShown()
        {
            var v = CreateTrackedStep(new Step
            {
                type = "reading", labels = new List<string> { "a – a", "" },
                items = new List<Item>
                {
                    new() { text = "ra rả", row = 0 }, new() { text = "khà khà", row = 0 },
                    new() { text = "bé đọc", row = 1 }
                }
            });
            yield return null;
            Assert.That(Labels(v), Has.Member("a – a"));
            var label = RootOf(v).GetComponentsInChildren<TMP_Text>(true).Single(t => t.text == "a – a");
            Assert.IsNull(label.GetComponentInParent<Tile>());
            Assert.IsFalse(label.raycastTarget);
        }

        [UnityTest]
        public IEnumerator LayoutFits_2048x1536()
        {
            Cam.targetTexture = null;
            Object.Destroy(TargetTex);
            TargetTex = new RenderTexture(2048, 1536, 24);
            Cam.targetTexture = TargetTex;
            var pairs = CreateTrackedStep(Pairs());
            yield return null;
            LayoutProbe.AssertFits(Canvas);
            ButtonWithText(pairs, UiText.PageNext).onClick.Invoke();
            yield return null;
            LayoutProbe.AssertFits(Canvas);
            Object.Destroy(RootOf(pairs));
            yield return null;
            CreateTrackedStep(Rules());
            yield return null;
            LayoutProbe.AssertFits(Canvas);
        }

        [UnityTest] public IEnumerator LetterPairs_AllTapped() { var v = Bind("tv1_t1_b41", 0); yield return ((ITestCompletable)v).CompleteForTest(); Assert.IsTrue(Done(v)); Assert.That(Labels(v), Has.Some.Contains("Ă")); }
        [UnityTest] public IEnumerator Rule_ReadsEachLine() { var v = Bind("tv1_t1_b40", RuleIndex("tv1_t1_b40")); TileWithText(v, "k chỉ ghép với e, ê, i").SimulateTap(); yield return new WaitForSeconds(.3f); Assert.That(Ctx.Speech.History.Last(), Does.StartWith("cau_b40_")); Assert.IsFalse(Done(v)); }
        [UnityTest] public IEnumerator CombineTable_Lesson39_KaBlocked() { var v = Bind("tv1_t1_b39", 1); yield return null; TileWithText(v, "k").SimulateTap(); TileWithText(v, "a").SimulateTap(); yield return new WaitForSeconds(.3f); Assert.That(Labels(v), Has.No.Member("ka")); Assert.IsFalse(Done(v)); }
        [UnityTest] public IEnumerator MatchCase_RightUpperCompletes() { var r = BindRound("tv1_t1_b41", MatchIndex("tv1_t1_b41")); yield return ((ITestCompletable)r).CompleteForTest(); Assert.IsTrue(Done(r)); }
        [UnityTest] public IEnumerator Reading_Lesson38_LabelsShown() { var v = Bind("tv1_t1_b38", 1); yield return null; Assert.That(Labels(v), Has.Member("a – a")); }

        /// <summary>
        /// Bảng ghép 5 âm đầu (bài 22, 27, 37) và 4 âm đầu (bài 39): mọi thẻ và kí hiệu ● nằm trọn trong Stage
        /// (không lấn sang thanh nút "Về", "Nghe lại") và không thẻ nào chồng lên thẻ khác.
        /// </summary>
        [UnityTest]
        public IEnumerator CombineTable_FitsStage_NoOverlap([Values("tv1_t1_b22", "tv1_t1_b27", "tv1_t1_b37", "tv1_t1_b39")] string lid)
        {
            var v = Bind(lid, 1);
            yield return null;
            var stage = Ctx.Stage;
            var rects = new List<(string name, Rect rect)>();
            foreach (var t in RootOf(v).GetComponentsInChildren<Tile>(false)) rects.Add((t.PlainText, RectIn(stage, (RectTransform)t.transform)));
            var marker = RootOf(v).transform.Find("Marker") as RectTransform;
            if (marker != null) rects.Add(("●", RectIn(stage, marker)));
            var bounds = stage.rect;
            foreach (var (name, r) in rects)
            {
                Assert.IsTrue(r.xMin >= bounds.xMin - 1f && r.xMax <= bounds.xMax + 1f && r.yMin >= bounds.yMin - 1f && r.yMax <= bounds.yMax + 1f,
                    $"{lid}: '{name}' ra ngoài Stage {r} / {bounds}");
            }
            for (var i = 0; i < rects.Count; i++)
                for (var j = i + 1; j < rects.Count; j++)
                {
                    var a = rects[i].rect; var b = rects[j].rect;
                    var overlap = Mathf.Min(a.xMax, b.xMax) - Mathf.Max(a.xMin, b.xMin) > 1f && Mathf.Min(a.yMax, b.yMax) - Mathf.Max(a.yMin, b.yMin) > 1f;
                    Assert.IsFalse(overlap, $"{lid}: '{rects[i].name}' chồng lên '{rects[j].name}'");
                }
        }

        private static Rect RectIn(RectTransform space, RectTransform rt)
        {
            var c = new Vector3[4];
            rt.GetWorldCorners(c);
            var min = (Vector2)space.InverseTransformPoint(c[0]);
            var max = (Vector2)space.InverseTransformPoint(c[2]);
            return Rect.MinMaxRect(min.x, min.y, max.x, max.y);
        }

        private static int RuleIndex(string lid) => LessonRepository.Load(lid).part1.FindIndex(s => s.type == "rule");
        private static int MatchIndex(string lid) => LessonRepository.Load(lid).part2.FindIndex(r => r.kind == "match_case");
    }
}
