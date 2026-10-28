using System.Linq;
using NUnit.Framework;

namespace TapDoc.Tests
{
    public class FlowTests
    {
        static Spell S(params (string kind, string tone)[] p) =>
            new Spell
            {
                drag_tone = true,
                parts = p.Select(x => new Part { kind = x.kind, tone = x.tone }).ToList()
            };

        [Test]
        public void Spell_Cu()
        {
            var sp = new SpellPractice(S(("unit", null), ("unit", null), ("join", null), ("tone", "hoi"), ("join", null)));
            CollectionAssert.IsEmpty(sp.Start());
            Assert.AreEqual(TapResult.WrongOrder, sp.Act(1, out _));
            Assert.AreEqual(0, sp.Expected);
            Assert.AreEqual(TapResult.Accepted, sp.Act(0, out var a0));
            CollectionAssert.IsEmpty(a0);
            Assert.AreEqual(TapResult.Ignored, sp.Act(0, out _));
            sp.Act(1, out var a1);
            CollectionAssert.AreEqual(new[] { 2 }, a1);
            Assert.IsTrue(sp.RequiresDrag(3));
            sp.Act(3, out var a3);
            CollectionAssert.AreEqual(new[] { 4 }, a3);
            Assert.IsTrue(sp.IsDone);
        }

        [Test]
        public void Spell_ToneAttach_StartsWithJoin()
        {
            var sp = new SpellPractice(S(("join", null), ("tone", "huyen"), ("join", null)));
            CollectionAssert.AreEqual(new[] { 0 }, sp.Start());
            sp.Act(1, out var a);
            CollectionAssert.AreEqual(new[] { 2 }, a);
            Assert.IsTrue(sp.IsDone);
        }

        [Test]
        public void Attempts()
        {
            var t = new AttemptTracker();
            Assert.AreEqual(Feedback.TryAgain, t.Submit(false));
            Assert.AreEqual(Feedback.ShowHint, t.Submit(false));
            Assert.AreEqual(Feedback.ShowHint, t.Submit(false));
            Assert.AreEqual(Feedback.Correct, t.Submit(true));
            Assert.AreEqual(3, t.Mistakes);
        }

        [Test]
        public void Flow_Lesson13()
        {
            var l = LessonRepository.Load("tv1_t1_b13");
            var f = new LessonFlow(l);
            Assert.AreEqual(Phase.Part1, f.Phase);
            for (int i = 0; i < 11; i++) Assert.IsTrue(f.Next());
            Assert.AreEqual(Phase.Part2, f.Phase);
            Assert.AreEqual(0, f.StepIndex);
            for (int i = 0; i < l.part2.Count; i++) f.Next();
            Assert.AreEqual(Phase.Done, f.Phase);
            Assert.IsFalse(f.Next());
            Assert.AreEqual(11 + l.part2.Count, f.TotalCount);
        }

        [Test]
        public void TapProgress_AllTapped()
        {
            var p = new TapProgress(2);
            p.Tap(1);
            p.Tap(1);
            Assert.IsFalse(p.AllTapped);
            p.Tap(0);
            Assert.IsTrue(p.AllTapped);
        }
    }
}
