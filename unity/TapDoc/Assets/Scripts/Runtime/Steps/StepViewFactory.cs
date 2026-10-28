using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace TapDoc
{
    public static class StepViewFactory
    {
        private static readonly Dictionary<string, Func<IStepView>> StepMakers = new();
        private static readonly Dictionary<string, Func<IRoundView>> RoundMakers = new();

        public static void Register(string type, Func<IStepView> make)
        {
            if (!string.IsNullOrEmpty(type) && make != null)
            {
                StepMakers[type] = make;
            }
        }

        public static void RegisterRound(string kind, Func<IRoundView> make)
        {
            if (!string.IsNullOrEmpty(kind) && make != null)
            {
                RoundMakers[kind] = make;
            }
        }

        /// <summary>
        /// Xóa đăng ký của <paramref name="type"/> ở cả màn Phần 1 lẫn lượt Phần 2. Dùng để test dọn dẹp.
        /// </summary>
        internal static void Unregister(string type)
        {
            if (string.IsNullOrEmpty(type)) return;
            StepMakers.Remove(type);
            RoundMakers.Remove(type);
        }

        /// <summary>
        /// Tạo màn cho <paramref name="s"/>. <paramref name="onCompleted"/> được gắn vào <c>Completed</c>
        /// TRƯỚC khi gọi <c>Bind</c>, nên màn báo xong ngay trong <c>Bind</c> (ví dụ âm thanh thiếu file
        /// xong tức thì) vẫn có người nghe.
        /// </summary>
        public static IStepView CreateStep(Step s, LessonContext ctx, Action onCompleted)
        {
            var type = s?.type ?? string.Empty;
            IStepView view;
            if (StepMakers.TryGetValue(type, out var make) && make != null)
            {
                view = make();
            }
            else
            {
                Debug.LogError($"[TapDoc] Chưa có màn cho: {type}");
                view = new FallbackView();
            }

            if (onCompleted != null) view.Completed += onCompleted;
            view.Bind(s, ctx);
            return view;
        }

        /// <summary>Như <see cref="CreateStep"/>, cho lượt Phần 2.</summary>
        public static IRoundView CreateRound(Round r, LessonContext ctx, Action onCompleted)
        {
            var kind = r?.kind ?? string.Empty;
            IRoundView view;
            if (RoundMakers.TryGetValue(kind, out var make) && make != null)
            {
                view = make();
            }
            else
            {
                Debug.LogError($"[TapDoc] Chưa có màn cho: {kind}");
                view = new FallbackView();
            }

            if (onCompleted != null) view.Completed += onCompleted;
            view.Bind(r, ctx);
            return view;
        }

        private class FallbackView : IStepView, IRoundView, ITestCompletable
        {
            public GameObject Root { get; private set; }
            public event Action Completed;
            private Tile _tile;

            public void Bind(Step step, LessonContext ctx) => Build(ctx, step?.text ?? step?.type ?? "Chạm");
            public void Bind(Round round, LessonContext ctx) => Build(ctx, round?.prompt_text ?? round?.kind ?? "Chạm");

            private void Build(LessonContext ctx, string label)
            {
                Root = new GameObject("FallbackView", typeof(RectTransform));
                Root.transform.SetParent(ctx.Stage, false);
                var rt = Root.GetComponent<RectTransform>();
                rt.anchorMin = Vector2.zero;
                rt.anchorMax = Vector2.one;
                rt.offsetMin = Vector2.zero;
                rt.offsetMax = Vector2.zero;

                _tile = UiKit.CreateTile(Root.transform, label);
                var tileRt = _tile.GetComponent<RectTransform>();
                tileRt.anchorMin = new Vector2(0.5f, 0.5f);
                tileRt.anchorMax = new Vector2(0.5f, 0.5f);
                tileRt.sizeDelta = new Vector2(360f, 220f);
                tileRt.anchoredPosition = Vector2.zero;
                _tile.Tapped += () => Completed?.Invoke();
            }

            public void Replay() { }

            public IEnumerator CompleteForTest()
            {
                var done = false;
                Action mark = () => done = true;
                Completed += mark;
                try
                {
                    _tile?.SimulateTap();
                    while (!done) yield return null;
                }
                finally
                {
                    Completed -= mark;
                }
            }
        }
    }
}
