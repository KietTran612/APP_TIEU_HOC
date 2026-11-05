using System.Collections;
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>Dữ liệu giả cho các màn Tập đọc: bài thơ "Trường em" (tr.91) và một đoạn văn dài.</summary>
    internal static class ReadingFixtures
    {
        public static readonly string[] TruongEm =
        {
            "Trường em ngói mới đỏ hồng", "Mọc lên tươi thắm giữa đồng lúa xanh.",
            "Gió về đồng lúa reo quanh", "Vẫy chào những bước chân nhanh tới trường.",
        };

        private static readonly char[] Punct = { ',', '.', '!', '?', ':', ';', '"' };

        public static List<string> Words(string sentence) =>
            sentence.Split(' ').Select(w => w.Trim(Punct)).Where(w => w.Length > 0).ToList();

        /// <summary>Hàng câu và tiếng như công cụ dựng ra (<c>rows</c>, <c>items</c>).</summary>
        public static Step Reading(string type, IReadOnlyList<string> sentences, IReadOnlyList<int> paragraphs = null)
        {
            var step = new Step { type = type };
            for (var s = 0; s < sentences.Count; s++)
            {
                step.rows.Add(new Item { text = sentences[s], audio = $"cau_b126_{s + 2:00}", row = paragraphs?[s] ?? s });
                var words = Words(sentences[s]);
                for (var c = 0; c < words.Count; c++)
                {
                    var key = words[c].ToLowerInvariant();
                    step.items.Add(new Item
                    {
                        text = words[c], audio = "tieng_" + key, row = s, col = c,
                        level = c == 0 ? 0 : 1 + (c - 1) % 3,
                        spells = new List<Spell> { new() { parts = new List<Part> { new() { text = key, audio = "tieng_" + key } } } },
                    });
                }
            }
            return step;
        }

        public static Step Passage(bool poem = true) =>
            With(Reading("passage", TruongEm, new[] { 0, 0, 0, 0 }), s => s.labels = new List<string> { "NGUYỄN BÙI VỢI", poem ? "poem" : "prose" });

        public static Step LongProse(int words)
        {
            var sentences = new List<string>();
            for (var k = 0; k < words / 8; k++) sentences.Add("Sáng nào Chim non cũng dậy sớm học bài.");
            return With(Reading("passage", sentences, sentences.Select(_ => 0).ToList()),
                s => s.labels = new List<string> { "Theo THANH MAI", "prose" });
        }

        /// <summary>Tìm tiếng có vần ương, ươi ở hai câu đầu: Trường, tươi.</summary>
        public static Step FindRime()
        {
            var step = Reading("find_words", TruongEm.Take(2).ToList());
            step.text = "Trong hai câu đầu, tiếng nào có vần ương, tiếng nào có vần ươi?";
            step.audio = "hoi_b126_01";
            foreach (var item in step.items)
            {
                var hit = item.text == "Trường" || item.text == "tươi";
                item.role = hit ? "target" : "other";
                if (hit) item.hl = new List<Span> { new() { s = item.text == "Trường" ? 2 : 1, n = item.text == "Trường" ? 4 : 3 } };
            }
            step.need = 2;
            return step;
        }

        public static T With<T>(T value, System.Action<T> change)
        {
            change(value);
            return value;
        }
    }

    public class ReadingStepTests : ViewTestBase
    {
        [UnityTest]
        public IEnumerator Title_PlaysThenCompletes_TapReplays()
        {
            var v = CreateTrackedStep(new Step { type = "title", text = "Cô dạy", audio = "cau_b128_01", labels = new List<string> { "Học thuộc lòng" } });
            Assert.That(Labels(v), Has.Member("(Học thuộc lòng)"));
            yield return WaitCompleted(v);
            TileWithText(v, "Cô dạy").SimulateTap();
            yield return null;
            Assert.AreEqual("cau_b128_01", Ctx.Speech.History.Last());
        }

        [UnityTest]
        public IEnumerator Question_ShowsHintAndDoneButton_NoAnswer()
        {
            var v = CreateTrackedStep(new Step { type = "question", marker = "?", text = "Vì sao Chim non được thưởng?", audio = "hoi_b129_03" });
            yield return new WaitForSeconds(.3f);
            Assert.That(Labels(v), Has.Member(UiText.AnswerWithParent));
            CollectionAssert.IsSubsetOf(new[] { "hoi_b129_03", SystemAudio.hd_tra_loi_mieng }, Ctx.Speech.History.ToList());
            Assert.AreEqual(SystemImages.CauHoi, MarkerOf(v));
            Assert.IsFalse(Done(v));
            ButtonWithText(v, UiText.Answered).onClick.Invoke();
            Assert.IsTrue(Done(v));
            LayoutProbe.AssertFits(Canvas);
        }

        [UnityTest]
        public IEnumerator Memorize_HideLevels_1_2_3()
        {
            var v = (MemorizeView)CreateTrackedStep(ReadingFixtures.Reading("memorize", ReadingFixtures.TruongEm));
            yield return null;
            var items = ReadingFixtures.Reading("memorize", ReadingFixtures.TruongEm).items;
            int Hidden() => Enumerable.Range(0, items.Count).Count(v.IsHidden);
            Assert.AreEqual(0, Hidden());
            var counts = new List<int>();
            for (var level = 1; level <= MemorizeView.MaxLevel; level++)
            {
                v.NextLevel();
                counts.Add(Hidden());
            }
            Assert.That(counts[0], Is.GreaterThan(0));
            Assert.That(counts[1], Is.GreaterThan(counts[0]));
            Assert.AreEqual(items.Count(i => i.col > 0), counts[2], "Mức 3: chỉ còn tiếng đầu mỗi dòng");
            Assert.IsTrue(Enumerable.Range(0, items.Count).Where(i => items[i].col == 0).All(i => !v.IsHidden(i)));
            Assert.That(Labels(v), Has.Member(UiText.ShowAll));
            v.NextLevel();
            Assert.AreEqual(0, Hidden(), "Bấm ở mức cao nhất thì hiện hết");
            LayoutProbe.AssertFits(Canvas);
        }

        [UnityTest]
        public IEnumerator Memorize_TapBlank_RevealsAndPlays()
        {
            var v = (MemorizeView)CreateTrackedStep(ReadingFixtures.Reading("memorize", ReadingFixtures.TruongEm));
            yield return null;
            v.NextLevel();
            var hidden = Enumerable.Range(0, 30).First(v.IsHidden);
            Assert.That(v.Text.RenderedText, Does.Contain("<alpha=#00>"));
            v.Text.SimulateTapWord(hidden);
            yield return null;
            Assert.IsFalse(v.IsHidden(hidden));
            Assert.AreEqual("tieng_" + ReadingFixtures.Words(ReadingFixtures.TruongEm[0])[1].ToLowerInvariant(), Ctx.Speech.History.Last());
        }

        [UnityTest]
        public IEnumerator Memorize_ShowsBookInstruction()
        {
            var step = ReadingFixtures.Reading("memorize", ReadingFixtures.TruongEm, new[] { 0, 0, 0, 0 });
            step.text = "Học thuộc lòng cả bài.";
            step.audio = "hoi_b128_04";
            step.marker = "?";
            var v = CreateTrackedStep(step);
            yield return new WaitForSeconds(.2f);
            Assert.That(Labels(v), Has.Member("Học thuộc lòng cả bài."));
            Assert.That(Ctx.Speech.History, Has.Member("hoi_b128_04"));
            LayoutProbe.AssertFits(Canvas);
        }

        [UnityTest]
        public IEnumerator Memorize_DoneAtAnyLevel()
        {
            var v = (MemorizeView)CreateTrackedStep(ReadingFixtures.Reading("memorize", ReadingFixtures.TruongEm));
            yield return null;
            v.NextLevel();
            ButtonWithText(v, UiText.Memorized).onClick.Invoke();
            Assert.IsTrue(Done(v));
        }

        private static Step Fill(bool tone) => tone
            ? new Step
            {
                type = "fill_blank", labels = new List<string> { "huyền", "sắc", "hỏi", "ngã", "nặng" },
                items = new List<Item> { new() { role = "blank", text = "thoang thoảng", audio = "tu_thoang_thoangr", answer = "hỏi", hl = new List<Span> { new() { s = 7, n = 6 } } } },
            }
            : new Step
            {
                type = "fill_blank", labels = new List<string> { "l", "n" },
                items = new List<Item>
                {
                    new() { role = "blank", text = "chạy lon ton", audio = "tu_chayj_lon_ton", answer = "l", hl = new List<Span> { new() { s = 5, n = 1 } } },
                    new() { role = "blank", text = "Chim non", audio = "tu_chim_non", answer = "n", hl = new List<Span> { new() { s = 5, n = 1 } } },
                },
            };

        [UnityTest]
        public IEnumerator FillBlank_DragRight_ShowsWordAndPlays()
        {
            var v = (FillBlankView)CreateTrackedStep(Fill(false));
            yield return null;
            Assert.IsNotNull(TileWithText(v, "chạy"));
            Assert.IsNotNull(TileWithText(v, "on ton"));
            LayoutProbe.AssertFits(Canvas);
            DragWithText(v, "l").SimulateDropOn(RootOf(v).GetComponentInChildren<DropSlot>());
            for (var i = 0; i < 200 && v.Current == 0; i++) yield return null;
            Assert.AreEqual(1, v.Current);
            Assert.That(Ctx.Speech.History, Has.Member("tu_chayj_lon_ton"));
            yield return ((ITestCompletable)v).CompleteForTest();
            Assert.IsTrue(Done(v));
        }

        [UnityTest]
        public IEnumerator FillBlank_ReplayDuringWord_StillAdvances()
        {
            var v = (FillBlankView)CreateTrackedStep(Fill(false));
            yield return null;
            TileWithText(v, "l").SimulateTap();
            // Chờ tới lúc app đọc cả từ rồi bấm "Nghe lại" cắt ngang.
            for (var i = 0; i < 200 && !Ctx.Speech.History.Contains("tu_chayj_lon_ton"); i++) yield return null;
            v.Replay();
            for (var i = 0; i < 200 && v.Current == 0; i++) yield return null;
            Assert.AreEqual(1, v.Current, "Điền đúng mà không sang mục sau");
        }

        [UnityTest]
        public IEnumerator FillBlank_DragWrong_StaysAndHintsAfterTwo()
        {
            var v = (FillBlankView)CreateTrackedStep(Fill(false));
            yield return null;
            var slot = RootOf(v).GetComponentInChildren<DropSlot>();
            DragWithText(v, "n").SimulateDropOn(slot);
            yield return new WaitForSeconds(.3f);
            DragWithText(v, "n").SimulateDropOn(slot);
            yield return new WaitForSeconds(.3f);
            Assert.AreEqual(0, v.Current);
            Assert.IsTrue(TileWithText(v, "l").IsHinted);
            Assert.IsFalse(Done(v));
        }

        [UnityTest]
        public IEnumerator FillBlank_Tone_ShowsWordWithoutTone()
        {
            var v = (FillBlankView)CreateTrackedStep(Fill(true));
            yield return null;
            Assert.IsTrue(v.IsToneMode);
            Assert.IsNotNull(TileWithText(v, "thoang"));
            Assert.AreEqual(2, RootOf(v).GetComponentsInChildren<Tile>().Count(t => t.PlainText == "thoang"),
                "Phần trước và chỗ trống (chữ in nghiêng hiện không dấu)");
            TileWithText(v, "hỏi").SimulateTap();
            yield return WaitCompleted(v);
        }

        private static Step Riddle() => new()
        {
            type = "riddle_answer", text = "Cái tẩy", audio = "tu_cais_taayr", image = "img_b137_cais_taayr",
            items = new List<Item>
            {
                new() { role = "option", image = "img_b137_buts_chif" },
                new() { role = "option", image = "img_b137_cais_taayr" },
                new() { role = "option", image = "img_b137_quar_cam" },
            },
        };

        [UnityTest]
        public IEnumerator Riddle_ChooseRight_RevealsAnswer()
        {
            var v = (RiddleAnswerView)CreateTrackedStep(Riddle());
            yield return null;
            Assert.IsFalse(v.AnswerShown);
            TileWithImage(v, "img_b137_cais_taayr").SimulateTap();
            yield return WaitCompleted(v);
            Assert.IsTrue(v.AnswerShown);
            Assert.That(Labels(v), Has.Member("Cái tẩy"));
            Assert.That(Ctx.Speech.History, Has.Member("tu_cais_taayr"));
        }

        [UnityTest]
        public IEnumerator Riddle_TwoMisses_Hints()
        {
            var v = (RiddleAnswerView)CreateTrackedStep(Riddle());
            yield return null;
            TileWithImage(v, "img_b137_quar_cam").SimulateTap();
            yield return new WaitForSeconds(.3f);
            TileWithImage(v, "img_b137_buts_chif").SimulateTap();
            yield return new WaitForSeconds(.3f);
            Assert.IsTrue(TileWithImage(v, "img_b137_cais_taayr").IsHinted);
            Assert.IsFalse(Done(v));
        }
    }

    public class PassageViewTests : ViewTestBase
    {
        [UnityTest]
        public IEnumerator ListenAll_PlaysSentencesInOrder_HighlightsCurrent()
        {
            var v = (PassageView)CreateTrackedStep(ReadingFixtures.Passage());
            yield return null;
            ButtonWithText(v, UiText.ListenAll).onClick.Invoke();
            // Câu đầu được tô ngay khi bắt đầu đọc (trong test âm thanh phát xong rất nhanh nên kiểm ngay).
            Assert.AreEqual(0, v.ReadingSentence);
            Assert.That(v.Text.RenderedText, Does.Contain("<mark="));
            for (var i = 0; i < 400 && v.ReadingSentence >= 0; i++) yield return null;
            var history = Ctx.Speech.History.ToList();
            var played = history.Where(id => id.StartsWith("cau_b126_")).ToList();
            CollectionAssert.AreEqual(new[] { "cau_b126_02", "cau_b126_03", "cau_b126_04", "cau_b126_05" }, played);
        }

        [UnityTest]
        public IEnumerator TapWord_PlaysSpelling()
        {
            var v = (PassageView)CreateTrackedStep(ReadingFixtures.Passage());
            yield return null;
            v.Text.SimulateTapWord(1);
            yield return new WaitForSeconds(.2f);
            Assert.AreEqual("tieng_em", Ctx.Speech.History.Last());
        }

        [UnityTest]
        public IEnumerator PoemLayout_OneLinePerSentence()
        {
            var v = (PassageView)CreateTrackedStep(ReadingFixtures.Passage());
            yield return null;
            var text = v.Text.RenderedText;
            var label = v.Text.Label;
            var full = string.Join("\n", ReadingFixtures.TruongEm);
            var dbg = $"pages={v.Text.PageCount} rect={((RectTransform)v.Text.transform).rect.size} " +
                      $"pref1={label.GetPreferredValues(ReadingFixtures.TruongEm[0], 1120f, 0f)} " +
                      $"prefAll={label.GetPreferredValues(full, 1120f, 0f)} size={label.fontSize} lines={label.textInfo.lineCount}";
            Assert.AreEqual(3, text.Count(c => c == '\n'), dbg);
            Assert.That(Labels(v), Has.Member("NGUYỄN BÙI VỢI"));
            LayoutProbe.AssertFits(Canvas);
        }

        [UnityTest]
        public IEnumerator ProseLayout_ParagraphBreaks()
        {
            var step = ReadingFixtures.Reading("passage", ReadingFixtures.TruongEm, new[] { 0, 0, 1, 1 });
            step.labels = new List<string> { "", "prose" };
            var v = (PassageView)CreateTrackedStep(step);
            yield return null;
            Assert.AreEqual(1, v.Text.RenderedText.Count(c => c == '\n'));
        }

        [UnityTest]
        public IEnumerator TapOnScreen_FindsWord()
        {
            var v = (PassageView)CreateTrackedStep(ReadingFixtures.Passage());
            yield return null;
            var label = v.Text.Label;
            label.ForceMeshUpdate();
            var word = label.textInfo.wordInfo[0];
            var ch = label.textInfo.characterInfo[word.firstCharacterIndex];
            var local = (ch.bottomLeft + ch.topRight) / 2f;
            var world = label.rectTransform.TransformPoint(local);
            var screen = RectTransformUtility.WorldToScreenPoint(Cam, world);
            var hit = -1;
            v.Text.WordTapped += i => hit = i;
            v.Text.OnPointerClick(new UnityEngine.EventSystems.PointerEventData(UnityEngine.EventSystems.EventSystem.current) { position = screen });
            Assert.AreEqual(0, hit, "Chạm vào chữ đầu tiên phải ra tiếng đầu tiên");
        }

        [UnityTest]
        public IEnumerator LongestPassage_FitsBothFrames()
        {
            foreach (var size in new[] { new Vector2Int(1600, 720), new Vector2Int(1440, 1080) })
            {
                Cam.targetTexture = null;
                Object.Destroy(TargetTex);
                TargetTex = new RenderTexture(size.x, size.y, 24);
                Cam.targetTexture = TargetTex;
                var v = (PassageView)CreateTrackedStep(ReadingFixtures.LongProse(160));
                yield return null;
                Assert.That(v.Text.PageCount, Is.GreaterThan(1), "Bài dài phải chia trang");
                for (var p = 0; p < v.Text.PageCount; p++)
                {
                    v.Text.ShowPage(p);
                    yield return null;
                    Assert.That(v.Text.Label.fontSize, Is.GreaterThanOrEqualTo(UiKit.MinFontSize));
                    var rect = ((RectTransform)v.Text.transform).rect;
                    Assert.That(v.Text.Label.preferredHeight, Is.LessThanOrEqualTo(rect.height + 1f), $"Trang {p} tràn ({size})");
                }
                LayoutProbe.AssertFits(Canvas);
                Object.Destroy(RootOf(v));
                yield return null;
            }
        }
    }

    public class FindWordsViewTests : ViewTestBase
    {
        [UnityTest]
        public IEnumerator TapTarget_LightsAndSpells()
        {
            var v = (FindWordsView)CreateTrackedStep(ReadingFixtures.FindRime());
            yield return null;
            v.Text.SimulateTapWord(0); // "Trường"
            yield return new WaitForSeconds(.2f);
            Assert.AreEqual(1, v.FoundCount);
            Assert.That(v.Text.RenderedText, Does.Contain("<mark="));
            Assert.That(Ctx.Speech.History, Has.Member("tieng_trường"));
            Assert.That(Labels(v), Has.Member(string.Format(UiText.FoundFormat, 1, 2)));
            LayoutProbe.AssertFits(Canvas);
        }

        [UnityTest]
        public IEnumerator TapOther_OnlyReads_NoPenalty()
        {
            var v = (FindWordsView)CreateTrackedStep(ReadingFixtures.FindRime());
            yield return null;
            v.Text.SimulateTapWord(1); // "em"
            yield return null;
            Assert.AreEqual(0, v.FoundCount);
            Assert.AreEqual("tieng_em", Ctx.Speech.History.Last());
            Assert.IsNull(v.HintWord);
        }

        [UnityTest]
        public IEnumerator RepeatedWord_FoundOnce()
        {
            var step = ReadingFixtures.Reading("find_words", new[] { "Chim non chăm học.", "Chim non hát hay." });
            step.text = "Tìm tiếng có vần on.";
            step.audio = "hoi_b129_01";
            foreach (var item in step.items) item.role = item.text == "non" ? "target" : "other";
            step.need = 1;
            var v = (FindWordsView)CreateTrackedStep(step);
            yield return null;
            v.Text.SimulateTapWord(1);
            yield return WaitCompleted(v);
            Assert.AreEqual(1, v.FoundCount);
            Assert.That(v.Text.RenderedText.Split(new[] { "<mark=" }, System.StringSplitOptions.None).Length - 1, Is.EqualTo(2),
                "Cả hai chữ \"non\" cùng sáng");
        }

        [UnityTest]
        public IEnumerator AllFound_Completes()
        {
            var v = (FindWordsView)CreateTrackedStep(ReadingFixtures.FindRime());
            yield return null;
            v.Text.SimulateTapWord(0);
            yield return new WaitForSeconds(.2f);
            Assert.IsFalse(Done(v));
            var tuoi = ReadingFixtures.FindRime().items.FindIndex(i => i.text == "tươi");
            v.Text.SimulateTapWord(tuoi);
            yield return WaitCompleted(v);
        }

        [UnityTest]
        public IEnumerator TwoMisses_HintsMissingWord()
        {
            var v = (FindWordsView)CreateTrackedStep(ReadingFixtures.FindRime());
            yield return null;
            v.Text.SimulateTapWord(1);
            v.Text.SimulateTapWord(2);
            yield return null;
            Assert.AreEqual("trường", v.HintWord);
            Assert.That(v.Text.RenderedText, Does.Contain("FFE08A"));
        }

        [UnityTest]
        public IEnumerator LastWord_ReplayDuringSpelling_StillCompletes()
        {
            // Bấm "Nghe lại" khi app đang đánh vần tiếng cuối: âm thanh bị cắt nhưng bước vẫn phải xong.
            var step = ReadingFixtures.FindRime();
            var v = (FindWordsView)CreateTrackedStep(step);
            yield return null;
            v.Text.SimulateTapWord(0);
            yield return new WaitForSeconds(.3f);
            v.Text.SimulateTapWord(step.items.FindIndex(i => i.text == "tươi"));
            v.Replay();
            yield return WaitCompleted(v);
        }

        [UnityTest]
        public IEnumerator NeedOne_StopsAtOne()
        {
            var step = ReadingFixtures.FindRime();
            step.need = 1;
            var v = (FindWordsView)CreateTrackedStep(step);
            yield return null;
            var tuoi = step.items.FindIndex(i => i.text == "tươi");
            v.Text.SimulateTapWord(tuoi);
            yield return WaitCompleted(v);
        }
    }
}
