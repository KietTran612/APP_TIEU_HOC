using System.Collections;
using System.Linq;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// Lớp 2 trong danh sách bài (thiết kế TV2 tập một, mục 4.3–4.6): hai nút lớp, phần theo chủ điểm và tuần,
    /// chuỗi mở khoá riêng mỗi lớp, nhớ lớp theo bé, tiến độ Phụ huynh theo lớp.
    /// </summary>
    public class LessonListGradeTests : AppTestBase
    {
        private const string LongTitle = "Quan sát tranh và trả lời câu hỏi: Cánh đồng lúa chín";

        // Bài lớp 1 thật (có file), bài lớp 2 giả: danh sách bài chỉ cần index.
        private const string Index =
            "{\"books\":[{\"book_id\":\"tv1_t1_1990\",\"title\":\"Tập một\",\"appendix\":\"tv1_t1_1990\",\"grade\":1}," +
            "{\"book_id\":\"tv2_t1_2001\",\"title\":\"Lớp 2\",\"appendix\":\"tv1_t1_1990\",\"grade\":2}]," +
            "\"lessons\":[" +
            "{\"lesson_id\":\"tv1_t1_b01\",\"lesson_no\":1,\"title\":\"o\",\"type\":\"am_moi\",\"book\":\"tv1_t1_1990\",\"part\":\"chu_cai\",\"label\":\"Bài 1\",\"week\":0,\"grade\":1}," +
            "{\"lesson_id\":\"tv1_t1_b02\",\"lesson_no\":2,\"title\":\"c\",\"type\":\"am_moi\",\"book\":\"tv1_t1_1990\",\"part\":\"chu_cai\",\"label\":\"Bài 2\",\"week\":0,\"grade\":1}," +
            "{\"lesson_id\":\"tv2_t1_b172\",\"lesson_no\":172,\"title\":\"Bác Hồ khuyên học sinh\",\"type\":\"tap_doc\",\"book\":\"tv2_t1_2001\",\"part\":\"lop2\",\"label\":\"Bài 1\",\"week\":1,\"grade\":2,\"theme\":\"Nhà trường\"}," +
            "{\"lesson_id\":\"tv2_t1_b173\",\"lesson_no\":173,\"title\":\"Cái trống trường em\",\"type\":\"hoc_thuoc_long\",\"book\":\"tv2_t1_2001\",\"part\":\"lop2\",\"label\":\"Bài 2\",\"week\":1,\"grade\":2,\"theme\":\"Nhà trường\"}," +
            "{\"lesson_id\":\"tv2_t1_b211\",\"lesson_no\":211,\"title\":\"Tình cảm gia đình\",\"type\":\"tap_doc\",\"book\":\"tv2_t1_2001\",\"part\":\"lop2\",\"label\":\"Bài 20\",\"week\":6,\"grade\":2,\"theme\":\"Gia đình\"}," +
            "{\"lesson_id\":\"tv2_t1_b265\",\"lesson_no\":265,\"title\":\"" + LongTitle + "\",\"type\":\"tap_lam_van\",\"book\":\"tv2_t1_2001\",\"part\":\"lop2\",\"label\":\"Tập làm văn\",\"week\":12,\"grade\":2,\"theme\":\"Đất nước ta\"}" +
            "]}";

        private void UseGradeIndex()
        {
            var real = new ResourcesContentSource();
            var source = new FakeContentSource { Fallback = real.Load };
            source.Put(ContentKind.LessonIndex, null, new TextAsset(Index));
            AppRoot.SourceFactory = () => source;
        }

        [TearDown]
        public void TearDownSource() => AppRoot.SourceFactory = null;

        private static LessonListScreen List() => Object.FindAnyObjectByType<LessonListScreen>();

        private static IEnumerator ShowGrade(int grade)
        {
            Press(List().GradeTabButton(grade));
            yield return null;
            yield return null;
        }

        [UnityTest]
        public IEnumerator TabsShowBothGrades()
        {
            UseGradeIndex();
            yield return LoadMainWithProfile();
            Assert.IsNotNull(List().GradeTabButton(1));
            Assert.IsNotNull(List().GradeTabButton(2));
            Assert.AreEqual(1, List().Grade);
            Assert.IsNotNull(List().ButtonFor("tv1_t1_b01"));
            Assert.IsNull(List().ButtonFor("tv2_t1_b172"), "Lớp 1 không hiện bài lớp 2");
            LayoutProbe.AssertFits(AppRoot.Instance.Canvas);
        }

        [UnityTest]
        public IEnumerator Grade2SectionsByTheme()
        {
            UseGradeIndex();
            yield return LoadMainWithProfile();
            yield return ShowGrade(2);
            var labels = LabelsUnder(List());
            Assert.That(labels, Has.Member("Nhà trường"));
            Assert.That(labels, Has.Member("Gia đình"));
            Assert.That(labels, Has.Member("Đất nước ta"));
            Assert.That(labels, Has.Member(string.Format(UiText.WeekFormat, 1)));
            Assert.That(labels, Has.No.Member(UiText.PartLetters));
            Assert.IsNull(List().ButtonFor("tv1_t1_b01"));
            LayoutProbe.AssertFits(AppRoot.Instance.Canvas);
        }

        [UnityTest]
        public IEnumerator FirstGrade2LessonOpenWithoutGrade1()
        {
            UseGradeIndex();
            yield return LoadMainWithProfile();
            yield return ShowGrade(2);
            Assert.IsTrue(List().ButtonFor("tv2_t1_b172").interactable);
            Assert.IsFalse(List().ButtonFor("tv2_t1_b173").interactable);
            Assert.AreEqual("tv2_t1_b172", List().CurrentLessonId);
        }

        [UnityTest]
        public IEnumerator SwitchTabRemembersPerChild()
        {
            UseGradeIndex();
            yield return LoadMainWithProfile();
            yield return ShowGrade(2);
            Assert.AreEqual(2, ProgressStore.Load(StorePath).GradeTab, "Chưa lưu lớp đang xem");
            AppRoot.Instance.ShowLessonList();
            yield return null;
            Assert.AreEqual(2, List().Grade);
            Assert.IsNotNull(List().ButtonFor("tv2_t1_b172"));
        }

        [UnityTest]
        public IEnumerator LongTitleFitsCard()
        {
            UseGradeIndex();
            yield return LoadMainWithProfile();
            yield return ShowGrade(2);
            List().ScrollTo("tv2_t1_b265");
            yield return null;
            var text = List().ButtonFor("tv2_t1_b265").GetComponentInChildren<TMP_Text>();
            text.ForceMeshUpdate();
            Assert.IsFalse(text.isTextOverflowing, "Tên bài Tập làm văn dài tràn khỏi thẻ");
        }

        [UnityTest]
        public IEnumerator ParentShowsProgressPerGrade()
        {
            UseGradeIndex();
            LogAssert.ignoreFailingMessages = true; // bài lớp 2 giả không có file
            yield return LoadMainWithProfile();
            AppRoot.Instance.Progress.MarkCompleted("tv1_t1_b01");
            AppRoot.Instance.ShowParent();
            yield return WaitPrepared();
            var parent = Object.FindAnyObjectByType<ParentScreen>();
            parent.SimulateUnlock();
            yield return null;
            var labels = LabelsUnder(parent);
            Assert.IsTrue(labels.Any(l => l.Contains(string.Format(UiText.LearnedGradeFormat, 1, 1, 2))), string.Join(" | ", labels));
            Assert.IsTrue(labels.Any(l => l.Contains(string.Format(UiText.LearnedGradeFormat, 2, 0, 4))), string.Join(" | ", labels));
            LayoutProbe.AssertFits(AppRoot.Instance.Canvas);
        }

        [UnityTest]
        public IEnumerator Grade1OnlyIndex_NoTabs()
        {
            yield return LoadMainWithProfile();
            Assert.IsNull(List().GradeTabButton(1));
            Assert.IsNull(List().GradeTabButton(2));
        }
    }
}
