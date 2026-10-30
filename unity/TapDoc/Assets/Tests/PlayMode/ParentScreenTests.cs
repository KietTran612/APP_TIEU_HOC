using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>Màn phụ huynh: khóa bằng phép tính, rồi xem tiến độ và chữ bé hay nhầm của từng bé.</summary>
    public class ParentScreenTests : AppTestBase
    {
        [UnityTest]
        public IEnumerator Parent_ShowsProgressAndConfusions()
        {
            yield return LoadMainWithProfile();
            var s = AppRoot.Instance.Progress;
            s.MarkCompleted(Ordered()[0]);
            s.RecordMistake("tv1_t1_b13", 0);
            AppRoot.Instance.ShowParent();
            yield return null;
            var p = Object.FindAnyObjectByType<ParentScreen>();
            p.SimulateUnlock();
            yield return null;
            Assert.That(LabelsUnder(p), Has.Some.Contains($"1/{Ordered().Length}"));
            Assert.That(LabelsUnder(p), Has.Member("u")); // lượt 0 bài 13: đáp án "u"
        }

        [UnityTest]
        public IEnumerator Parent_LookToneConfusion_ShowsWordNotGlyph()
        {
            // Lượt 3 bài 4 là "nhìn chữ mẫu cá, kéo dấu": phụ huynh cần thấy chữ "cá", không phải kí hiệu dấu "ˊ".
            yield return LoadMainWithProfile();
            AppRoot.Instance.Progress.RecordMistake("tv1_t1_b04", 3);
            AppRoot.Instance.ShowParent();
            yield return null;
            var p = Object.FindAnyObjectByType<ParentScreen>();
            p.SimulateUnlock();
            yield return null;
            Assert.That(LabelsUnder(p), Has.Member("cá"));
            Assert.That(LabelsUnder(p), Has.No.Member("ˊ"));
        }

        [UnityTest]
        public IEnumerator Gate_WrongAnswer_StaysLockedAndChangesQuestion()
        {
            yield return LoadMainWithProfile();
            AppRoot.Instance.ShowParent();
            yield return null;
            var p = Object.FindAnyObjectByType<ParentScreen>();
            var question = p.Gate.Question;
            var wrong = p.ChoiceButtons.First(b => b.GetComponentInChildren<TMPro.TMP_Text>().text != p.Gate.Expected.ToString());
            Press(wrong);
            yield return null;
            Assert.IsFalse(p.IsUnlocked);
            Assert.AreNotEqual(question, p.Gate.Question);
            Assert.That(LabelsUnder(p), Has.Member(p.Gate.Question), "Phép tính mới phải hiện trên màn");
        }

        [UnityTest]
        public IEnumerator ParentButton_OpensGate_BackReturnsToList()
        {
            yield return LoadMainWithProfile();
            Press(Object.FindAnyObjectByType<LessonListScreen>().ParentButton);
            yield return null;
            var p = Object.FindAnyObjectByType<ParentScreen>();
            Assert.IsNotNull(p, "Nút Phụ huynh không mở màn phụ huynh");
            Assert.IsFalse(p.IsUnlocked);
            Press(p.BackButton);
            yield return null;
            Assert.IsNotNull(Object.FindAnyObjectByType<LessonListScreen>());
        }

        [UnityTest]
        public IEnumerator Parent_ShowsEveryChildSeparately()
        {
            yield return LoadMainWithProfile();
            var s = AppRoot.Instance.Progress;
            s.MarkCompleted(Ordered()[0]);
            s.CreateProfile("Na", ProfileScreen.Avatars[1]);
            AppRoot.Instance.ShowParent();
            yield return null;
            var p = Object.FindAnyObjectByType<ParentScreen>();
            p.SimulateUnlock();
            yield return null;
            var labels = LabelsUnder(p);
            Assert.That(labels, Has.Member(TestChildName));
            Assert.That(labels, Has.Member("Na"));
            Assert.That(labels, Has.Some.Contains($"1/{Ordered().Length}"));
            Assert.That(labels, Has.Some.Contains($"0/{Ordered().Length}"));
        }

        [UnityTest]
        public IEnumerator Parent_AppendixShowsBookPages()
        {
            // Mục "Chú ý và Phụ lục": chép đúng tr.120–122 và các điểm app làm khác sách, cuộn được, vừa màn.
            yield return LoadMainWithProfile();
            foreach (var size in new[] { new Vector2Int(2400, 1080), new Vector2Int(2048, 1536) })
            {
                var rt = new RenderTexture(size.x, size.y, 24);
                AppRoot.Instance.UiCamera.targetTexture = rt;
                AppRoot.Instance.ShowParent();
                yield return null;
                var p = Object.FindAnyObjectByType<ParentScreen>();
                p.SimulateUnlock();
                yield return null;
                var open = p.GetComponentsInChildren<UnityEngine.UI.Button>(false)
                    .FirstOrDefault(b => b.GetComponentInChildren<TMPro.TMP_Text>(true)?.text == UiText.BookAppendix);
                Press(open);
                yield return null;
                var labels = LabelsUnder(p);
                Assert.That(labels, Has.Some.Contains("phụ huynh học sinh"));      // Chú ý tr.122
                Assert.That(labels, Has.Member("ét-sì"));                        // Bảng chữ cái tr.120
                Assert.That(labels, Has.Member("ngh"));                          // Bảng gọi tên tr.121
                Assert.That(labels, Has.Member("giờ"));
                Assert.That(labels, Has.Some.Contains("Phần luyện tập"));        // app khác sách
                ScreenProbe.Save(AppRoot.Instance.UiCamera, $"TestOutput/screens/{size.x}x{size.y}/app_parent_appendix.png");
                LayoutProbe.AssertFits(AppRoot.Instance.Canvas);
                AppRoot.Instance.UiCamera.targetTexture = null;
                Object.Destroy(rt);
            }
        }

        [UnityTest]
        public IEnumerator Parent_FitsPhoneAndTablet()
        {
            yield return LoadMainWithProfile();
            var s = AppRoot.Instance.Progress;
            s.MarkCompleted(Ordered()[0]);
            s.RecordMistake("tv1_t1_b13", 0);
            s.RecordMistake("tv1_t1_b04", 3);
            s.RecordMistake("tv1_t1_b13", 7);
            s.CreateProfile("Na", ProfileScreen.Avatars[1]);
            foreach (var size in new[] { new Vector2Int(2400, 1080), new Vector2Int(2048, 1536) })
            {
                var rt = new RenderTexture(size.x, size.y, 24);
                AppRoot.Instance.UiCamera.targetTexture = rt;
                var dir = $"TestOutput/screens/{size.x}x{size.y}";

                AppRoot.Instance.ShowParent();
                yield return null;
                ScreenProbe.Save(AppRoot.Instance.UiCamera, $"{dir}/app_parent_gate.png");
                LayoutProbe.AssertFits(AppRoot.Instance.Canvas);

                Object.FindAnyObjectByType<ParentScreen>().SimulateUnlock();
                yield return null;
                ScreenProbe.Save(AppRoot.Instance.UiCamera, $"{dir}/app_parent.png");
                LayoutProbe.AssertFits(AppRoot.Instance.Canvas);

                AppRoot.Instance.UiCamera.targetTexture = null;
                Object.Destroy(rt);
            }
        }
    }
}
