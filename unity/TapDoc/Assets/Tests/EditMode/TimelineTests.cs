using NUnit.Framework;

namespace TapDoc.Tests
{
    public class TimelineTests
    {
        [Test]
        public void StartTimes() =>
            CollectionAssert.AreEqual(
                new[] { 0f, 1.5f, 2.5f },
                SequenceTimeline.StartTimes(new[] { 1f, .5f, 2f }, .5f));

        [Test]
        public void EvenStarts() =>
            CollectionAssert.AreEqual(
                new[] { 0f, .5f, 1f, 1.5f },
                SequenceTimeline.EvenStarts(2f, 4));
    }
}
