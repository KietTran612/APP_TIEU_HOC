using System;
using System.Collections;
using UnityEngine;

namespace TapDoc
{
    public interface IStepView
    {
        GameObject Root { get; }
        event Action Completed;
        void Bind(Step step, LessonContext ctx);
        void Replay();
    }

    public interface IRoundView
    {
        GameObject Root { get; }
        event Action Completed;
        void Bind(Round round, LessonContext ctx);
        void Replay();
    }

    internal interface ITestCompletable
    {
        IEnumerator CompleteForTest();
    }
}
