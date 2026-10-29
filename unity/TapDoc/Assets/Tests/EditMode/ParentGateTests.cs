using System.Linq;
using System.Text.RegularExpressions;
using NUnit.Framework;

namespace TapDoc.Tests
{
    /// <summary>Khóa phụ huynh bằng phép cộng: bấm sai thì đổi phép tính, không bao giờ khóa cứng.</summary>
    public class ParentGateTests
    {
        [Test]
        public void WrongAnswer_ChangesQuestion()
        {
            var g = new ParentGate(new System.Random(1));
            var q = g.Question;
            var wrong = g.Choices.First(c => c != g.Expected);
            Assert.IsFalse(g.Answer(wrong));
            Assert.AreNotEqual(q, g.Question);
        }

        [Test]
        public void RightAnswer_Opens()
        {
            var g = new ParentGate(new System.Random(2));
            Assert.IsTrue(g.Answer(g.Expected));
            Assert.AreEqual(1, g.Choices.Count(c => c == g.Expected));
        }

        [Test]
        public void Question_InRange_ThreeDistinctChoices([Range(0, 40)] int seed)
        {
            var g = new ParentGate(new System.Random(seed));
            var m = Regex.Match(g.Question, @"^(\d+) \+ (\d+) = \?$");
            Assert.IsTrue(m.Success, g.Question);
            var a = int.Parse(m.Groups[1].Value);
            var b = int.Parse(m.Groups[2].Value);
            Assert.That(a, Is.InRange(11, 49));
            Assert.That(b, Is.InRange(11, 49));
            Assert.AreEqual(a + b, g.Expected);
            Assert.AreEqual(3, g.Choices.Count);
            Assert.AreEqual(3, g.Choices.Distinct().Count());
            Assert.AreEqual(1, g.Choices.Count(c => c == g.Expected));
            Assert.That(g.Choices, Is.All.GreaterThan(0));
        }

        [Test]
        public void ManyWrongAnswers_NeverLockOut()
        {
            var g = new ParentGate(new System.Random(3));
            for (var i = 0; i < 50; i++)
            {
                Assert.IsFalse(g.Answer(g.Choices.First(c => c != g.Expected)));
            }
            Assert.IsTrue(g.Answer(g.Expected));
        }
    }
}
