using System.Collections;
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.UI;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// Chữ có nhiều cách đọc (Phụ lục tr.120–122): dưới thẻ chữ có một nút cho mỗi cách đọc, ghi rõ cách nào đọc
    /// khi học (để phân biệt chữ), cách nào là âm chuẩn, cách nào là tên chữ cái.
    /// </summary>
    public class ReadingButtonsTests : ViewTestBase
    {
        private static Button ReadingButton(object view, string audio) =>
            RootOf(view).GetComponentsInChildren<Button>(true).FirstOrDefault(b => b.name == $"Reading_{audio}");

        private static string TextOf(Button b) => b.GetComponentInChildren<TMP_Text>(true).text;

        [UnityTest]
        public IEnumerator Unit_WithManyReadings_ShowsLabelledButtons()
        {
            var v = Bind("tv1_t1_b25", 0); // g
            yield return null;
            var learn = ReadingButton(v, "am_g");
            var standard = ReadingButton(v, "ghiam_g");
            var letterName = ReadingButton(v, "tenchu_g");
            Assert.IsNotNull(learn);
            Assert.IsNotNull(standard);
            Assert.IsNotNull(letterName);
            Assert.That(TextOf(learn), Does.Contain("gờ đơn").And.Contain(UiText.ReadingLearn).And.Contain("để phân biệt g và gh"));
            Assert.That(TextOf(standard), Does.Contain("gờ").And.Contain(UiText.ReadingStandard));
            Assert.That(TextOf(letterName), Does.Contain("giê").And.Contain(UiText.ReadingLetterName));
        }

        [UnityTest]
        public IEnumerator Unit_SharedReading_NamesEveryKind()
        {
            var v = Bind("tv1_t1_b20", 0); // k: "ca" vừa là cách đọc khi học vừa là tên chữ cái
            yield return null;
            Assert.That(TextOf(ReadingButton(v, "am_k")), Does.Contain(UiText.ReadingLearn).And.Contain(UiText.ReadingLetterName));
            Assert.That(TextOf(ReadingButton(v, "ghiam_k")), Does.Contain("cờ").And.Contain(UiText.ReadingStandard));
        }

        [UnityTest]
        public IEnumerator ReadingButton_PlaysItsAudio_WithoutFinishingStep()
        {
            var v = Bind("tv1_t1_b25", 0);
            yield return null;
            ReadingButton(v, "ghiam_g").onClick.Invoke();
            yield return null;
            Assert.AreEqual("ghiam_g", Ctx.Speech.History.Last());
            Assert.IsFalse(Done(v), "Bấm nút cách đọc không phải là đọc xong chữ");
        }

        [UnityTest]
        public IEnumerator Unit_WithOneReading_HasNoReadingButtons()
        {
            var v = Bind("tv1_t1_b01", 0); // o
            yield return null;
            Assert.IsFalse(RootOf(v).GetComponentsInChildren<Button>(true).Any(b => b.name.StartsWith("Reading_")));
            Assert.IsFalse(RootOf(v).GetComponentsInChildren<Button>(true).Any(b => b.name == $"Button_{UiText.Why}"));
        }

        [UnityTest]
        public IEnumerator WhyButton_AsksToOpenReadingNotes()
        {
            string asked = null;
            Ctx.OpenNotes = () => asked = "opened";
            var v = Bind("tv1_t1_b25", 0);
            yield return null;
            ButtonWithText(v, UiText.Why).onClick.Invoke();
            Assert.AreEqual("opened", asked);
        }

        [UnityTest]
        public IEnumerator ReadingRow_FitsStage_NoOverlap([Values(2400, 2048)] int width)
        {
            Cam.targetTexture = null;
            Object.Destroy(TargetTex);
            TargetTex = new RenderTexture(width, width == 2400 ? 1080 : 1536, 24);
            Cam.targetTexture = TargetTex;
            Ctx.OpenNotes = () => { };
            var v = Bind("tv1_t1_b25", 0); // 3 cách đọc + nút "Vì sao?": hàng dài nhất
            yield return null;
            var stage = Ctx.Stage;
            var rects = new List<(string name, Rect rect)>();
            foreach (var t in RootOf(v).GetComponentsInChildren<Tile>()) rects.Add(("thẻ chữ", RectIn(stage, (RectTransform)t.transform)));
            foreach (var b in RootOf(v).GetComponentsInChildren<Button>()) rects.Add((b.name, RectIn(stage, (RectTransform)b.transform)));
            var bounds = stage.rect;
            foreach (var (name, r) in rects)
            {
                Assert.IsTrue(bounds.Contains(r.min) && bounds.Contains(r.max), $"{name} ra ngoài Stage: {r} / {bounds}");
                Assert.GreaterOrEqual(r.height, UiKit.MinTouch - 0.5f, $"{name} thấp hơn vùng chạm tối thiểu");
            }
            for (var i = 0; i < rects.Count; i++)
            for (var j = i + 1; j < rects.Count; j++)
                Assert.IsFalse(rects[i].rect.Overlaps(rects[j].rect), $"{rects[i].name} chồng lên {rects[j].name}");
            LayoutProbe.AssertFits(Canvas);
        }

        private static Rect RectIn(RectTransform space, RectTransform rt)
        {
            var corners = new Vector3[4];
            rt.GetWorldCorners(corners);
            var min = (Vector2)space.InverseTransformPoint(corners[0]);
            var max = (Vector2)space.InverseTransformPoint(corners[2]);
            return Rect.MinMaxRect(min.x, min.y, max.x, max.y);
        }
    }
}
