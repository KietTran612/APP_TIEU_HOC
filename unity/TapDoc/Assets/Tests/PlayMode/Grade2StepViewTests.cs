using System.Collections;
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    /// <summary>
    /// Các màn mới của lớp 2 (thiết kế TV2 tập một, mục 6–7): ghép chữ, điền từ vào đoạn, chọn dòng; câu hỏi có câu
    /// kèm theo; kí hiệu giải nghĩa từ.
    /// </summary>
    public class Grade2StepViewTests : ViewTestBase
    {
        private static readonly string[] Bank = { "vui sướng", "khai trường", "năm học", "siêng học" };

        private static Step Combine() => new Step
        {
            type = "combine_words", text = "dúm", audio = "tieng_dums",
            items = new List<Item>
            {
                new() { text = "dúm lông", audio = "tu_dums_loong", part = "lông", role = "after" },
                new() { text = "dúm muối", audio = "tu_dums_muoois", part = "muối", role = "after" },
            }
        };

        // Đề bài Tập làm văn tr.11 "Niềm vui ngày khai trường": bốn ô, bốn từ cho sẵn.
        private static Step Passage()
        {
            var step = new Step { type = "fill_passage", labels = Bank.ToList() };
            step.rows.Add(new Item { text = "Sắp đến ngày khai trường, nhận được quà của bố, Lan càng thêm náo nức.", audio = "cau_b179_01", row = 0 });
            step.rows.Add(new Item { text = "Hôm nay đã bắt đầu năm học mới: Lan vui sướng khi cắp chiếc cặp mới đi học.", audio = "cau_b179_02", row = 1 });
            step.rows.Add(new Item { text = "Lan hứa với bố sẽ siêng học, siêng làm như lời Bác Hồ khuyên.", audio = "cau_b179_03", row = 2 });
            void T(string t, int r) => step.items.Add(new Item { text = t, row = r, role = "text" });
            void B(string a, int r) => step.items.Add(new Item { text = a, row = r, role = "blank", answer = a, choices = Bank.ToList() });
            T("Sắp đến ngày", 0); B("khai trường", 0); T(", nhận được quà của bố, Lan càng thêm náo nức.", 0);
            T("Hôm nay đã bắt đầu", 1); B("năm học", 1); T("mới: Lan", 1); B("vui sướng", 1);
            T("khi cắp chiếc cặp mới đi học.", 1);
            T("Lan hứa với bố sẽ", 2); B("siêng học", 2); T(", siêng làm như lời Bác Hồ khuyên.", 2);
            return step;
        }

        private static Step OwnChoices()
        {
            var step = new Step { type = "fill_passage" };
            step.rows.Add(new Item { text = "Một năm có mười hai tháng.", audio = "cau_b177_05", row = 0 });
            step.items.Add(new Item { text = "Một năm có", row = 0, role = "text" });
            step.items.Add(new Item { text = "mười hai", row = 0, role = "blank", answer = "mười hai",
                choices = new List<string> { "mười hai", "mười", "mười một" } });
            step.items.Add(new Item { text = "tháng.", row = 0, role = "text" });
            return step;
        }

        private static Step Lines() => new Step
        {
            type = "choose_line", text = "Dòng nào viết chưa thành câu?", audio = "hoi_b178_01", need = 2,
            items = new List<Item>
            {
                new() { text = "Ngày khai trường", audio = "cau_b178_02", role = "target" },
                new() { text = "Bác rất vui lòng.", audio = "cau_b178_03", role = "other" },
                new() { text = "Trong cặp có bốn quyển vở.", audio = "cau_b178_04", role = "other" },
                new() { text = "Lan chưa", audio = "cau_b178_05", role = "target" },
            }
        };

        // ---- ghép chữ ----

        [UnityTest]
        public IEnumerator CombineWordsTapShowsPhraseAndPlays()
        {
            var v = (CombineWordsView)CreateTrackedStep(Combine());
            LayoutProbe.AssertFits(Canvas);
            TileWithText(v, "lông").SimulateTap();
            yield return new WaitForSeconds(.3f);
            Assert.IsNotNull(TileWithText(v, "dúm lông"));
            LayoutProbe.AssertFits(Canvas);
            Assert.That(Ctx.Speech.History, Has.Member("tu_dums_loong"));
            Assert.AreEqual(1, v.Revealed);
            Assert.IsFalse(Done(v));
            TileWithText(v, "muối").SimulateTap();
            yield return new WaitForSeconds(.5f);
            Assert.IsTrue(Done(v));
        }

        [UnityTest]
        public IEnumerator CombineWordsCompleteForTest()
        {
            var v = CreateTrackedStep(Combine());
            yield return ((ITestCompletable)v).CompleteForTest();
            Assert.IsTrue(Done(v));
        }

        // ---- điền từ vào đoạn ----

        [UnityTest]
        public IEnumerator FillPassageCorrectFillsAndPlaysSentence()
        {
            var v = (FillPassageView)CreateTrackedStep(Passage());
            Assert.AreEqual(0, v.Selected);
            v.ChoiceTile("khai trường").SimulateTap();
            yield return new WaitForSeconds(.4f);
            Assert.AreEqual(1, v.FilledCount);
            Assert.AreEqual("khai trường", v.FilledText(0));
            Assert.That(Ctx.Speech.History, Has.Member("cau_b179_01"));
            Assert.AreEqual(1, v.Selected, "Điền xong thì sang ô kế tiếp");
        }

        [UnityTest]
        public IEnumerator FillPassageWrongCardReturns()
        {
            var v = (FillPassageView)CreateTrackedStep(Passage());
            var wrong = v.CurrentChoices.First(c => c != "khai trường");
            v.ChoiceTile(wrong).SimulateTap();
            yield return new WaitForSeconds(.4f);
            Assert.AreEqual(0, v.FilledCount);
            Assert.IsNull(v.FilledText(0));
            Assert.IsTrue(v.ChoiceTile(wrong).gameObject.activeSelf, "Thẻ sai vẫn còn để chọn lại");
        }

        [UnityTest]
        public IEnumerator FillPassageHintAfterTwoWrong()
        {
            var v = (FillPassageView)CreateTrackedStep(Passage());
            var wrong = v.CurrentChoices.Where(c => c != "khai trường").ToList();
            v.ChoiceTile(wrong[0]).SimulateTap();
            yield return new WaitForSeconds(.4f);
            v.ChoiceTile(wrong[wrong.Count - 1]).SimulateTap();
            yield return new WaitForSeconds(.4f);
            Assert.IsTrue(v.ChoiceTile("khai trường").IsHinted);
        }

        [UnityTest]
        public IEnumerator TapCardWithoutBlankFillsFirstEmpty()
        {
            var v = (FillPassageView)CreateTrackedStep(Passage());
            // Bé chưa chạm ô nào: thẻ điền vào ô trống đầu tiên còn lại.
            v.ChoiceTile("khai trường").SimulateTap();
            yield return new WaitForSeconds(.4f);
            Assert.AreEqual("khai trường", v.FilledText(0));
        }

        [UnityTest]
        public IEnumerator FillPassageChoicesFitOneRow()
        {
            var v = (FillPassageView)CreateTrackedStep(Passage());
            Assert.That(v.CurrentChoices.Count, Is.InRange(2, 3));
            Assert.That(v.CurrentChoices, Has.Member("khai trường"));
            yield return null;
            LayoutProbe.AssertFits(Canvas);
        }

        [UnityTest]
        public IEnumerator FillPassageCompletesWhenAllFilled()
        {
            var v = CreateTrackedStep(Passage());
            yield return ((ITestCompletable)v).CompleteForTest();
            Assert.IsTrue(Done(v));
        }

        [UnityTest]
        public IEnumerator FillPassageOwnChoicesAnswerNotAlwaysFirst()
        {
            // Lựa chọn riêng trong dữ liệu luôn đặt đáp án đầu tiên: màn phải xáo theo ô để bé không chỉ chạm thẻ trái.
            var step = new Step { type = "fill_passage" };
            step.rows.Add(new Item { text = "a b c.", audio = "cau_b177_09", row = 0 });
            foreach (var (ans, d1, d2) in new[] { ("mười hai", "mười", "chín"), ("một", "hai", "chín"), ("tám", "năm", "sáu") })
                step.items.Add(new Item { text = ans, row = 0, role = "blank", answer = ans, choices = new List<string> { ans, d1, d2 } });
            var v = (FillPassageView)CreateTrackedStep(step);
            var positions = new List<int>();
            for (var k = 0; k < 3; k++)
            {
                var answer = step.items[k].answer;
                positions.Add(v.CurrentChoices.ToList().IndexOf(answer));
                v.ChoiceTile(answer).SimulateTap();
                yield return new WaitForSeconds(.4f);
            }
            Assert.That(positions, Has.Some.Not.EqualTo(0), string.Join(",", positions));
            Assert.That(positions.Distinct().Count(), Is.GreaterThan(1));
        }

        [UnityTest]
        public IEnumerator FillPassageOwnChoicesPerBlank()
        {
            var v = (FillPassageView)CreateTrackedStep(OwnChoices());
            Assert.IsNotNull(v.ChoiceTile("mười một"));
            v.ChoiceTile("mười hai").SimulateTap();
            yield return new WaitForSeconds(.6f);
            Assert.IsTrue(Done(v));
        }

        // ---- chọn dòng ----

        [UnityTest]
        public IEnumerator ChooseLineMarksCorrectOnly()
        {
            var v = (ChooseLineView)CreateTrackedStep(Lines());
            yield return null;
            LayoutProbe.AssertFits(Canvas);
            v.LineTile(1).SimulateTap();
            yield return new WaitForSeconds(.3f);
            Assert.AreEqual(0, v.FoundCount);
            Assert.AreEqual("cau_b178_03", Ctx.Speech.History.Last());
            v.LineTile(2).SimulateTap();
            yield return new WaitForSeconds(.3f);
            Assert.AreEqual(0, v.HintIndex, "Sai hai lần thì gợi ý dòng đúng đầu tiên");
            v.LineTile(0).SimulateTap();
            yield return new WaitForSeconds(.3f);
            Assert.AreEqual(1, v.FoundCount);
            Assert.IsFalse(Done(v));
        }

        [UnityTest]
        public IEnumerator ChooseLineCompletesWhenAllCorrectFound()
        {
            var v = (ChooseLineView)CreateTrackedStep(Lines());
            v.LineTile(0).SimulateTap();
            yield return new WaitForSeconds(.3f);
            v.LineTile(3).SimulateTap();
            yield return new WaitForSeconds(.6f);
            Assert.IsTrue(Done(v));
            AssertTilesInside(v);
        }

        [UnityTest]
        public IEnumerator ChooseLineManyLinesPagedAndFit()
        {
            var step = Lines();
            for (var k = 0; k < 4; k++)
                step.items.Add(new Item { text = $"Dòng thêm số {k + 1} khá dài để thử xuống dòng.", audio = $"cau_b178_1{k}", role = "other" });
            var v = (ChooseLineView)CreateTrackedStep(step);
            yield return null;
            Assert.That(v.PageCount, Is.GreaterThan(1));
            LayoutProbe.AssertFits(Canvas);
            yield return ((ITestCompletable)v).CompleteForTest();
            Assert.IsTrue(Done(v));
        }

        // ---- câu hỏi có câu kèm theo, kí hiệu giải nghĩa ----

        [UnityTest]
        public IEnumerator QuestionShowsLinesTappable()
        {
            var step = new Step
            {
                type = "question", text = "Đặt câu hỏi để tìm bộ phận chính thứ nhất trong hai câu sau:", audio = "hoi_b178_02",
                rows = new List<Item>
                {
                    new() { text = "Con chìa vôi vừa hót vừa bay.", audio = "cau_b178_06" },
                    new() { text = "Hoa mướp nở vàng rực.", audio = "cau_b178_07" },
                }
            };
            var v = CreateTrackedStep(step);
            TileWithText(v, "Hoa mướp nở vàng rực.").SimulateTap();
            yield return new WaitForSeconds(.3f);
            Assert.AreEqual("cau_b178_07", Ctx.Speech.History.Last());
            AssertTilesInside(v);
            LayoutProbe.AssertFits(Canvas);
        }

        [Test]
        public void RuleShowsColonMarker()
        {
            Assert.AreEqual(SystemImages.GiaiNghia, SystemImages.ForMarker(":"));
            Assert.AreEqual(SystemImages.CauHoi, SystemImages.ForMarker("?"));
            Assert.That(SystemImages.All, Has.Member(SystemImages.GiaiNghia));
        }

        /// <summary>Mọi thẻ đang hiện nằm trong khung của màn (không tràn ra ngoài Stage).</summary>
        private static void AssertTilesInside(object view)
        {
            var root = (RectTransform)RootOf(view).transform;
            var box = new Vector3[4];
            root.GetWorldCorners(box);
            var corners = new Vector3[4];
            foreach (var tile in root.GetComponentsInChildren<Tile>(false))
            {
                ((RectTransform)tile.transform).GetWorldCorners(corners);
                Assert.That(corners[0].x, Is.GreaterThanOrEqualTo(box[0].x - 1f), tile.PlainText);
                Assert.That(corners[0].y, Is.GreaterThanOrEqualTo(box[0].y - 1f), tile.PlainText);
                Assert.That(corners[2].x, Is.LessThanOrEqualTo(box[2].x + 1f), tile.PlainText);
                Assert.That(corners[2].y, Is.LessThanOrEqualTo(box[2].y + 1f), tile.PlainText);
            }
        }
    }
}
