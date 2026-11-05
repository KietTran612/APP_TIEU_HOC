using UnityEngine;

namespace TapDoc
{
    /// <summary>
    /// Nằm trên một vùng chứa (co giãn theo màn); giữ một khối con có cỡ thiết kế cố định ở giữa vùng và phóng to
    /// đều khối đó cho vừa vùng (lấy cạnh hẹp hơn). Bên trong khối dựng theo cỡ thiết kế, không biết mình bị phóng to.
    /// Dùng cho phần học (Stage) và quyển sổ trên màn rộng (bản thiết kế tỷ lệ màn hình mục 5.2, 5.4).
    /// </summary>
    public class FitBox : MonoBehaviour
    {
        public RectTransform Content { get; private set; }
        public Vector2 DesignSize { get; private set; }

        /// <summary>Mức phóng to hiện tại của <see cref="Content"/>.</summary>
        public float Scale { get; private set; } = 1f;

        /// <summary>Thêm khối <paramref name="name"/> cỡ <paramref name="designSize"/> vào giữa <paramref name="area"/>.</summary>
        public static RectTransform Create(RectTransform area, string name, Vector2 designSize)
        {
            var go = new GameObject(name, typeof(RectTransform));
            go.transform.SetParent(area, false);
            var rt = (RectTransform)go.transform;
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(.5f, .5f);
            rt.sizeDelta = designSize;
            rt.anchoredPosition = Vector2.zero;

            var fit = area.gameObject.AddComponent<FitBox>();
            fit.Content = rt;
            fit.DesignSize = designSize;
            fit.Fit();
            return rt;
        }

        /// <summary>Phóng to khối cho vừa cỡ hiện tại của vùng.</summary>
        public void Fit()
        {
            if (Content == null || DesignSize.x <= 0f || DesignSize.y <= 0f) return;
            var size = ((RectTransform)transform).rect.size;
            if (size.x <= 0f || size.y <= 0f) return;
            Scale = Mathf.Min(size.x / DesignSize.x, size.y / DesignSize.y);
            Content.localScale = new Vector3(Scale, Scale, 1f);
        }

        private void OnRectTransformDimensionsChange() => Fit();
    }
}
