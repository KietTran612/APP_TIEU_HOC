using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc.Tests
{
    public static class LayoutProbe
    {
        /// <summary>
        /// Mọi vùng bé chạm được (Selectable, Tile, DropSlot) đang bật phải nằm trọn trong canvas và có cạnh
        /// nhỏ nhất ≥ <see cref="UiKit.MinTouch"/>; mọi chữ TMP đang bật không được tràn.
        /// </summary>
        public static void AssertFits(Canvas c)
        {
            Assert.IsNotNull(c, "Canvas is null");
            Canvas.ForceUpdateCanvases();

            var canvasRect = c.GetComponent<RectTransform>();

            foreach (var sel in c.GetComponentsInChildren<Selectable>(false))
            {
                AssertTouchTarget(canvasRect, sel, "Selectable");
            }

            foreach (var tile in c.GetComponentsInChildren<Tile>(false))
            {
                AssertTouchTarget(canvasRect, tile, "Tile");
            }

            foreach (var slot in c.GetComponentsInChildren<DropSlot>(false))
            {
                AssertTouchTarget(canvasRect, slot, "DropSlot");
            }

            foreach (var tmp in c.GetComponentsInChildren<TMP_Text>(false))
            {
                if (!tmp.gameObject.activeInHierarchy) continue;
                tmp.ForceMeshUpdate();
                Assert.IsFalse(
                    tmp.isTextOverflowing,
                    $"Chữ bị tràn trên '{tmp.name}': \"{tmp.text}\"");
            }
        }

        private static void AssertTouchTarget(RectTransform canvasRect, Component target, string kind)
        {
            if (!target.gameObject.activeInHierarchy) return;
            var rt = target.GetComponent<RectTransform>();
            if (rt == null) return;

            var cBounds = canvasRect.rect;
            var corners = new Vector3[4];
            rt.GetWorldCorners(corners);
            float minX = float.MaxValue, minY = float.MaxValue;
            float maxX = float.MinValue, maxY = float.MinValue;
            for (var i = 0; i < 4; i++)
            {
                var local = canvasRect.InverseTransformPoint(corners[i]);
                if (local.x < minX) minX = local.x;
                if (local.y < minY) minY = local.y;
                if (local.x > maxX) maxX = local.x;
                if (local.y > maxY) maxY = local.y;
            }

            var w = maxX - minX;
            var h = maxY - minY;
            var name = target.name;
            Assert.GreaterOrEqual(
                Mathf.Min(w, h),
                UiKit.MinTouch - 0.5f,
                $"{kind} '{name}' quá nhỏ: {w:F1}x{h:F1}");

            var scroll = target.GetComponentInParent<ScrollRect>();
            if (scroll != null && scroll.transform != target.transform)
            {
                AssertInsideScroll(canvasRect, rt, scroll, kind);
                return;
            }

            Assert.GreaterOrEqual(minX, cBounds.xMin - 1f, $"{kind} '{name}' tràn trái ({minX:F1} < {cBounds.xMin:F1})");
            Assert.LessOrEqual(maxX, cBounds.xMax + 1f, $"{kind} '{name}' tràn phải ({maxX:F1} > {cBounds.xMax:F1})");
            Assert.GreaterOrEqual(minY, cBounds.yMin - 1f, $"{kind} '{name}' tràn dưới ({minY:F1} < {cBounds.yMin:F1})");
            Assert.LessOrEqual(maxY, cBounds.yMax + 1f, $"{kind} '{name}' tràn trên ({maxY:F1} > {cBounds.yMax:F1})");
        }

        /// <summary>Kiểm tra vùng nhìn trong canvas và thẻ còn hiện, cho phép cắt dọc theo trục cuộn.</summary>
        private static void AssertInsideScroll(RectTransform canvasRect, RectTransform target, ScrollRect scroll, string kind)
        {
            var viewport = scroll.viewport;
            var corners = new Vector3[4];
            viewport.GetWorldCorners(corners);
            foreach (var corner in corners)
            {
                var local = canvasRect.InverseTransformPoint(corner);
                Assert.That(local.x, Is.InRange(canvasRect.rect.xMin - 1f, canvasRect.rect.xMax + 1f), "Vùng cuộn tràn canvas");
                Assert.That(local.y, Is.InRange(canvasRect.rect.yMin - 1f, canvasRect.rect.yMax + 1f), "Vùng cuộn tràn canvas");
            }
            target.GetWorldCorners(corners);
            var min = new Vector2(float.MaxValue, float.MaxValue);
            var max = new Vector2(float.MinValue, float.MinValue);
            foreach (var corner in corners)
            {
                var local = (Vector2)viewport.InverseTransformPoint(corner);
                min = Vector2.Min(min, local);
                max = Vector2.Max(max, local);
            }
            var rect = viewport.rect;
            if (max.x <= rect.xMin || min.x >= rect.xMax || max.y <= rect.yMin || min.y >= rect.yMax) return;
            if (!scroll.horizontal)
            {
                Assert.GreaterOrEqual(min.x, rect.xMin - 1f, $"{kind} '{target.name}' tràn trái vùng cuộn");
                Assert.LessOrEqual(max.x, rect.xMax + 1f, $"{kind} '{target.name}' tràn phải vùng cuộn");
            }
            if (!scroll.vertical)
            {
                Assert.GreaterOrEqual(min.y, rect.yMin - 1f, $"{kind} '{target.name}' tràn dưới vùng cuộn");
                Assert.LessOrEqual(max.y, rect.yMax + 1f, $"{kind} '{target.name}' tràn trên vùng cuộn");
            }
        }
    }
}
