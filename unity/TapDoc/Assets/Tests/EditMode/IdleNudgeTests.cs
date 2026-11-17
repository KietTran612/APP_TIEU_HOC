using System.Collections.Generic;
using NUnit.Framework;
using UnityEngine;

namespace TapDoc.Tests
{
    /// <summary>Nhắc khi bé ngồi im (bản thiết kế nâng cấp UI mục 4.1.3; root 17/11: 12 s / 24 s / 30 s).</summary>
    public class IdleNudgeTests
    {
        private int _reprompts;
        private readonly List<RectTransform> _shown = new();
        private int _hides;
        private GameObject _go;
        private RectTransform _target;
        private RectTransform _next;
        private IdleNudge _nudge;

        [SetUp]
        public void SetUp()
        {
            _reprompts = 0;
            _hides = 0;
            _shown.Clear();
            _go = new GameObject("t", typeof(RectTransform));
            _target = (RectTransform)_go.transform;
            _next = (RectTransform)new GameObject("next", typeof(RectTransform)).transform;
            _next.SetParent(_target, false);
            _nudge = new IdleNudge(() => _reprompts++, t => _shown.Add(t), () => _hides++);
        }

        [TearDown]
        public void TearDown() => Object.DestroyImmediate(_go);

        private void Tick(float t, NudgeKind kind = NudgeKind.Tap, RectTransform target = null, bool speaking = false) =>
            _nudge.Tick(t, speaking, kind, target ?? _target);

        [Test]
        public void Nudge_Tap_RepromptAt12_HandAt24()
        {
            Tick(0f);
            Tick(11.9f);
            Assert.AreEqual(0, _reprompts);
            Tick(12f);
            Assert.AreEqual(1, _reprompts, "12 s: đọc lại lời dẫn");
            Assert.IsEmpty(_shown);
            Tick(23.9f);
            Assert.IsEmpty(_shown);
            Tick(24f);
            CollectionAssert.AreEqual(new[] { _target }, _shown, "24 s: bàn tay");
            Assert.IsTrue(_nudge.HandShown);
            Tick(100f);
            Assert.AreEqual(1, _reprompts, "Tối đa hai lần nhắc");
            Assert.AreEqual(1, _shown.Count);
            Assert.AreEqual(IdleNudge.MaxNudges, _nudge.Count);
        }

        [Test]
        public void Nudge_Read_HandOnlyAt30()
        {
            Tick(0f, NudgeKind.Read);
            Tick(29.9f, NudgeKind.Read);
            Assert.IsEmpty(_shown);
            Tick(30f, NudgeKind.Read);
            Assert.AreEqual(1, _shown.Count, "30 s: bàn tay");
            Tick(200f, NudgeKind.Read);
            Assert.AreEqual(0, _reprompts, "Bước tự đọc không đọc lại lời dẫn");
            Assert.AreEqual(1, _shown.Count);
        }

        [Test]
        public void Nudge_DoneStep_UsesReadTiming()
        {
            Tick(0f);
            Tick(5f);
            Tick(6f, NudgeKind.Read, _next); // nút Tiếp vừa hiện
            Tick(35.9f, NudgeKind.Read, _next);
            Assert.IsEmpty(_shown, "Đếm lại từ lúc nút Tiếp hiện");
            Tick(36f, NudgeKind.Read, _next);
            CollectionAssert.AreEqual(new[] { _next }, _shown);
            Assert.AreEqual(0, _reprompts);
        }

        [Test]
        public void Nudge_PausesWhileSpeaking()
        {
            for (var t = 0f; t <= 20f; t += 1f) Tick(t, speaking: true);
            Assert.AreEqual(0, _reprompts, "Không nhắc khi giọng đọc đang chạy");
            Tick(20f);
            Tick(31.9f);
            Assert.AreEqual(0, _reprompts, "Đếm từ lúc giọng đọc dừng");
            Tick(32f);
            Assert.AreEqual(1, _reprompts);
        }

        [Test]
        public void Nudge_ActivityClears()
        {
            Tick(0f);
            Tick(12f);
            Tick(24f);
            Assert.IsTrue(_nudge.HandShown);
            _nudge.NoteActivity(30f);
            Assert.AreEqual(1, _hides, "Chạm thì ẩn bàn tay");
            Assert.IsFalse(_nudge.HandShown);
            Assert.AreEqual(0, _nudge.Count);
            Tick(41.9f);
            Assert.AreEqual(1, _reprompts);
            Tick(42f);
            Assert.AreEqual(2, _reprompts, "Đếm lại từ lần chạm");
        }

        [Test]
        public void Nudge_NoneKind_DoesNothing()
        {
            Tick(0f, NudgeKind.None);
            Tick(500f, NudgeKind.None);
            Assert.AreEqual(0, _reprompts);
            Assert.IsEmpty(_shown);
        }

        [Test]
        public void Nudge_NoTarget_RepromptButNoHand()
        {
            _nudge.Tick(0f, false, NudgeKind.Tap, null);
            _nudge.Tick(12f, false, NudgeKind.Tap, null);
            _nudge.Tick(24f, false, NudgeKind.Tap, null);
            Assert.AreEqual(1, _reprompts);
            Assert.IsEmpty(_shown);
            Assert.IsFalse(_nudge.HandShown);
        }

        [Test]
        public void SelfReadTypes_CoverReadingSteps()
        {
            foreach (var type in new[] { "sentence", "passage", "memorize", "reading", "words", "title", "question" })
            {
                Assert.That(IdleNudge.SelfReadTypes, Has.Member(type));
            }
            Assert.That(IdleNudge.SelfReadTypes, Has.No.Member("find_words"));
        }
    }
}
