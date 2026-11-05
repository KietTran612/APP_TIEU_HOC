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

        private Vector2 ScreenCenter(RectTransform rt) =>
            RectTransformUtility.WorldToScreenPoint(Cam, rt.TransformPoint(rt.rect.center));

        [UnityTest]
        public IEnumerator DragTile_FollowsFinger_InScaledStage()
        {
            Ctx.Stage.localScale = Vector3.one * 1.4f;
            var tile = UiKit.CreateTile(Ctx.Stage, "a");
            var drag = tile.gameObject.AddComponent<DragTile>();
            yield return null;
            Canvas.ForceUpdateCanvases();

            var rt = (RectTransform)tile.transform;
            var start = ScreenCenter(rt);
            var ped = new PointerEventData(EventSystem.current) { position = start, delta = Vector2.zero };
            ExecuteEvents.Execute(drag.gameObject, ped, ExecuteEvents.beginDragHandler);
            ped.delta = new Vector2(100f, 0f);
            ped.position = start + ped.delta;
            ExecuteEvents.Execute(drag.gameObject, ped, ExecuteEvents.dragHandler);

            var moved = ScreenCenter(rt) - start;
            Assert.AreEqual(100f, moved.x, 1f, "Thẻ phải bám ngón tay khi phần học phóng to");
            Assert.AreEqual(0f, moved.y, 1f);
            ped.position = new Vector2(-10000f, -10000f);
            ExecuteEvents.Execute(drag.gameObject, ped, ExecuteEvents.endDragHandler);
        }

        [UnityTest]
        public IEnumerator DragTile_ResizeMidDrag_TileStaysInStage()
        {
            var tile = UiKit.CreateTile(Ctx.Stage, "a");
            var drag = tile.gameObject.AddComponent<DragTile>();
            var rt = (RectTransform)tile.transform;
            var home = rt.anchoredPosition;
            yield return null;
            Canvas.ForceUpdateCanvases();

            var start = ScreenCenter(rt);
            var ped = new PointerEventData(EventSystem.current) { position = start, delta = Vector2.zero };
            ExecuteEvents.Execute(drag.gameObject, ped, ExecuteEvents.beginDragHandler);
            ped.delta = new Vector2(60f, 20f);
            ped.position = start + ped.delta;
            ExecuteEvents.Execute(drag.gameObject, ped, ExecuteEvents.dragHandler);

            Ctx.Stage.localScale = Vector3.one * 1.4f; // máy xoay, phần học phóng to giữa lúc kéo
            yield return null;
            ped.delta = new Vector2(40f, 0f);
            ped.position += ped.delta;
            ExecuteEvents.Execute(drag.gameObject, ped, ExecuteEvents.dragHandler);
            ped.position = new Vector2(-10000f, -10000f); // thả ngoài mọi ô
            ExecuteEvents.Execute(drag.gameObject, ped, ExecuteEvents.endDragHandler);

            Assert.AreSame(Ctx.Stage, tile.transform.parent, "Thẻ vẫn ở trong phần học");
            Assert.AreEqual(home, rt.anchoredPosition, "Thả ngoài ô thì thẻ về chỗ cũ");
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
