using System;
using System.Collections;
using UnityEngine;

namespace TapDoc.Tests
{
    /// <summary>Chờ một <see cref="Awaitable"/> trong <c>[UnityTest]</c> (coroutine): mỗi khung kiểm tra một lần.</summary>
    public static class AwaitableTestUtil
    {
        /// <summary>Số khung tối đa chờ một awaitable trước khi coi là treo.</summary>
        public const int MaxFrames = 600;

        public static IEnumerator Wait(Awaitable awaitable)
        {
            var awaiter = awaitable.GetAwaiter();
            for (var i = 0; !awaiter.IsCompleted; i++)
            {
                if (i >= MaxFrames) throw new TimeoutException($"Awaitable chưa xong sau {MaxFrames} khung");
                yield return null;
            }
            awaiter.GetResult(); // ném lại lỗi (nếu có) ra test
        }

        public static IEnumerator Wait<T>(Awaitable<T> awaitable, Action<T> done)
        {
            var awaiter = awaitable.GetAwaiter();
            for (var i = 0; !awaiter.IsCompleted; i++)
            {
                if (i >= MaxFrames) throw new TimeoutException($"Awaitable chưa xong sau {MaxFrames} khung");
                yield return null;
            }
            done?.Invoke(awaiter.GetResult());
        }
    }
}
