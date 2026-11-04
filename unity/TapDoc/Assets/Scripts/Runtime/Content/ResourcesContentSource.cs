using UnityEngine;

namespace TapDoc
{
    /// <summary>Nguồn dữ liệu đọc từ <c>Resources/</c> theo đường dẫn của <see cref="ContentPaths"/>.</summary>
    public sealed class ResourcesContentSource : IContentSource
    {
        public async Awaitable<Object> LoadAsync(ContentKind kind, string id)
        {
            var request = Resources.LoadAsync(ContentPaths.PathOf(kind, id), ContentPaths.TypeOf(kind));
            await request;
            return request.asset;
        }

        public Object Load(ContentKind kind, string id) =>
            Resources.Load(ContentPaths.PathOf(kind, id), ContentPaths.TypeOf(kind));

        /// <summary>Resources không nhả từng file: catalog bỏ tham chiếu rồi nhờ <c>Resources.UnloadUnusedAssets</c> dọn.</summary>
        public void Release(ContentKind kind, string id, Object asset)
        {
        }

        public void ReleaseUnused() => Resources.UnloadUnusedAssets();
    }
}
