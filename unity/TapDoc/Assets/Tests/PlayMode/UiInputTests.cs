using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.TestTools;

namespace TapDoc.Tests
{
    public class UiInputTests : ViewTestBase
    {
        [UnityTest]
        public IEnumerator Tile_ClickWhileDragging_DoesNotTap()
        {
            var tile = UiKit.CreateTile(Ctx.Stage, "u");
            var taps = 0;
            tile.Tapped += () => taps++;
            yield return null;

            var dragClick = new PointerEventData(EventSystem.current) { dragging = true };
            ExecuteEvents.Execute(tile.gameObject, dragClick, ExecuteEvents.pointerClickHandler);
            Assert.AreEqual(0, taps, "Thả tay sau khi kéo không được tính là chạm");

            var click = new PointerEventData(EventSystem.current) { dragging = false };
            ExecuteEvents.Execute(tile.gameObject, click, ExecuteEvents.pointerClickHandler);
            Assert.AreEqual(1, taps);
        }

        [UnityTest]
        public IEnumerator DragTile_BeginDrag_DrawsOnTop_ThenRestoresOrder()
        {
            var row = new GameObject("Row", typeof(RectTransform));
            row.transform.SetParent(Ctx.Stage, false);
            var first = UiKit.CreateTile(row.transform, "a");
            UiKit.CreateTile(row.transform, "b");
            UiKit.CreateTile(row.transform, "c");
            var drag = first.gameObject.AddComponent<DragTile>();
            var home = first.GetComponent<RectTransform>().anchoredPosition;
            yield return null;

            var ped = new PointerEventData(EventSystem.current)
            {
                position = new Vector2(-10000f, -10000f), // ngoài mọi ô nhận
                delta = new Vector2(50f, 30f)
            };
            ExecuteEvents.Execute(drag.gameObject, ped, ExecuteEvents.beginDragHandler);
            Assert.AreEqual(2, first.transform.GetSiblingIndex(), "Thẻ đang kéo phải vẽ trên cùng");
            ExecuteEvents.Execute(drag.gameObject, ped, ExecuteEvents.dragHandler);
            ExecuteEvents.Execute(drag.gameObject, ped, ExecuteEvents.endDragHandler);

            Assert.AreEqual(0, first.transform.GetSiblingIndex(), "Về chỗ cũ thì trả lại thứ tự cũ");
            Assert.AreEqual(home, first.GetComponent<RectTransform>().anchoredPosition);
        }

        [UnityTest]
        public IEnumerator Stage_SameSizeAsLessonScreen()
        {
            yield return null;
            Canvas.ForceUpdateCanvases();
            var size = Ctx.Stage.rect.size;
            var expected = new Vector2(
                UiKit.SafeWidth - 2f * UiKit.StageSideInset,
                UiKit.Reference.y - UiKit.StageTopInset - UiKit.StageBottomInset);
            Assert.AreEqual(expected.x, size.x, 0.5f);
            Assert.AreEqual(expected.y, size.y, 0.5f);
        }
    }
}
