using System;

namespace TapDoc
{
    public enum Phase
    {
        Part1,
        Part2,
        Done
    }

    public class LessonFlow
    {
        private readonly Lesson _lesson;

        public LessonFlow(Lesson lesson)
        {
            _lesson = lesson ?? throw new ArgumentNullException(nameof(lesson));
            var p1Count = _lesson.part1?.Count ?? 0;
            var p2Count = _lesson.part2?.Count ?? 0;

            if (p1Count > 0)
            {
                Phase = Phase.Part1;
                StepIndex = 0;
            }
            else if (p2Count > 0)
            {
                Phase = Phase.Part2;
                StepIndex = 0;
            }
            else
            {
                Phase = Phase.Done;
                StepIndex = 0;
            }
        }

        public Phase Phase { get; private set; }
        public int StepIndex { get; private set; }

        public Step CurrentStep =>
            Phase == Phase.Part1 && _lesson.part1 != null && StepIndex >= 0 && StepIndex < _lesson.part1.Count
                ? _lesson.part1[StepIndex]
                : null;

        public Round CurrentRound =>
            Phase == Phase.Part2 && _lesson.part2 != null && StepIndex >= 0 && StepIndex < _lesson.part2.Count
                ? _lesson.part2[StepIndex]
                : null;

        public int TotalCount => (_lesson.part1?.Count ?? 0) + (_lesson.part2?.Count ?? 0);

        public int Position
        {
            get
            {
                var p1Count = _lesson.part1?.Count ?? 0;
                return Phase switch
                {
                    Phase.Part1 => StepIndex,
                    Phase.Part2 => p1Count + StepIndex,
                    _ => TotalCount
                };
            }
        }

        public bool Next()
        {
            if (Phase == Phase.Done)
            {
                return false;
            }

            var p1Count = _lesson.part1?.Count ?? 0;
            var p2Count = _lesson.part2?.Count ?? 0;

            if (Phase == Phase.Part1)
            {
                if (StepIndex + 1 < p1Count)
                {
                    StepIndex++;
                    return true;
                }

                if (p2Count > 0)
                {
                    Phase = Phase.Part2;
                    StepIndex = 0;
                    return true;
                }

                Phase = Phase.Done;
                StepIndex = 0;
                return true;
            }

            if (Phase == Phase.Part2)
            {
                if (StepIndex + 1 < p2Count)
                {
                    StepIndex++;
                    return true;
                }

                Phase = Phase.Done;
                StepIndex = 0;
                return true;
            }

            return false;
        }
    }
}
