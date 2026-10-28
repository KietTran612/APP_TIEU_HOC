using System;
using System.Collections;
using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Phần dùng chung của các màn Phần 1: dựng Root phủ kín Stage, phát âm thanh an toàn và báo
    /// <c>Completed</c> đúng một lần.
    /// </summary>
    public abstract class StepViewBase : IStepView, ITestCompletable
    {
        public GameObject Root { get; private set; }
        public event Action Completed;

        protected LessonContext Ctx { get; private set; }
        protected Step Step { get; private set; }

        /// <summary>Đã báo <c>Completed</c> chưa.</summary>
        protected bool IsCompleted { get; private set; }

        /// <summary>Màn còn trên màn hình không (Root bị hủy khi bé đi tiếp hoặc về danh sách).</summary>
        protected bool IsAlive => Root != null;

        public void Bind(Step step, LessonContext ctx)
        {
            Step = step;
            Ctx = ctx;
            Root = new GameObject(GetType().Name, typeof(RectTransform));
            Root.transform.SetParent(ctx.Stage, false);
            var rt = (RectTransform)Root.transform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
            Build();
        }

        /// <summary>Dựng giao diện và bắt đầu (ví dụ tự đọc âm thanh). Gọi trong <see cref="Bind"/>.</summary>
        protected abstract void Build();

        public abstract void Replay();

        /// <summary>Thao tác đúng cho test: chạm các thẻ cần chạm.</summary>
        protected abstract void ActForTest();

        public IEnumerator CompleteForTest()
        {
            if (IsCompleted) yield break;
            var done = false;
            Action mark = () => done = true;
            Completed += mark;
            try
            {
                ActForTest();
                while (!done) yield return null;
            }
            finally
            {
                Completed -= mark;
            }
        }

        /// <summary>Báo <c>Completed</c> một lần, chỉ khi màn còn trên màn hình.</summary>
        protected void Complete()
        {
            if (IsCompleted || !IsAlive) return;
            IsCompleted = true;
            Completed?.Invoke();
        }

        /// <summary>
        /// Phát một mã âm thanh. Trả về <c>true</c> khi phát hết và màn vẫn còn; <c>false</c> khi bị cắt ngang
        /// hoặc màn đã bị hủy, khi đó không được đụng vào giao diện nữa.
        /// </summary>
        protected async Awaitable<bool> Play(string audioId)
        {
            var finished = await Ctx.Speech.PlayAsync(audioId);
            return finished && IsAlive;
        }

        /// <summary>Hiện kí hiệu của sách (●, ⌂) ở góc trên trái nếu bước có <c>marker</c>.</summary>
        protected void AddMarker()
        {
            var id = SystemImages.ForMarker(Step.marker);
            if (id == null) return;
            var go = new GameObject("Marker", typeof(RectTransform), typeof(UnityEngine.UI.Image), typeof(MarkerIcon));
            go.transform.SetParent(Root.transform, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = new Vector2(0f, 1f);
            rt.anchorMax = new Vector2(0f, 1f);
            rt.pivot = new Vector2(0f, 1f);
            rt.sizeDelta = new Vector2(80f, 80f);
            rt.anchoredPosition = new Vector2(10f, -10f);
            var img = go.GetComponent<UnityEngine.UI.Image>();
            img.sprite = Ctx.Assets.Image(id);
            img.preserveAspect = true;
            img.raycastTarget = false;
            img.enabled = img.sprite != null;
            go.GetComponent<MarkerIcon>().ImageId = id;
        }

        /// <summary>Tạo một thẻ đặt giữa Root, lệch <paramref name="offset"/>, kích thước <paramref name="size"/>.</summary>
        protected Tile AddTile(string richText, Vector2 size, Vector2 offset, float fontSize, Sprite image = null)
        {
            var tile = UiKit.CreateTile(Root.transform, richText, image);
            var rt = (RectTransform)tile.transform;
            rt.anchorMin = new Vector2(0.5f, 0.5f);
            rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = size;
            rt.anchoredPosition = offset;
            tile.SetFontSize(fontSize);
            return tile;
        }
    }
}
