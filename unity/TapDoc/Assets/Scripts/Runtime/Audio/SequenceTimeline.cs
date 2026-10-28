using System;
using System.Collections.Generic;

namespace TapDoc
{
    public static class SequenceTimeline
    {
        public const float DefaultGap = 0.5f;

        public static float[] StartTimes(IReadOnlyList<float> durations, float gap = DefaultGap)
        {
            if (durations == null || durations.Count == 0)
            {
                return Array.Empty<float>();
            }

            var starts = new float[durations.Count];
            var time = 0f;
            for (var i = 0; i < durations.Count; i++)
            {
                starts[i] = time;
                time += durations[i] + gap;
            }
            return starts;
        }

        public static float[] EvenStarts(float total, int count)
        {
            if (count <= 0)
            {
                return Array.Empty<float>();
            }

            var starts = new float[count];
            var step = total / count;
            for (var i = 0; i < count; i++)
            {
                starts[i] = i * step;
            }
            return starts;
        }
    }
}
