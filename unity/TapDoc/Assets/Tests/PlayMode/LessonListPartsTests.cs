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
    /// Hai quyển trong một danh sách bài (thiết kế tập 2, mục 4): ba phần theo <c>part</c>, nhóm tuần ở phần Tập đọc,
    /// nhãn thẻ từ <c>index.json</c>, công tắc "Mở mọi bài" theo từng bé ở màn Phụ huynh.
    /// </summary>
    public class LessonListPartsTests : AppTestBase
    {
        // Bài tập 1 thật (có file), bài tập 2 giả: danh sách bài chỉ cần index, không mở bài.
        private const string Index =
            "{\"books\":[{\"book_id\":\"tv1_t1_1990\",\"title\":\"Tập một\",\"appendix\":\"tv1_t1_1990\"}," +
            "{\"book_id\":\"tv1_t2_1996\",\"title\":\"Tập hai\",\"appendix\":\"tv1_t1_1990\"}]," +
            "\"lessons\":[" +
            "{\"lesson_id\":\"tv1_t1_b01\",\"lesson_no\":1,\"title\":\"o\",\"type\":\"am_moi\",\"book\":\"tv1_t1_1990\",\"part\":\"chu_cai\",\"label\":\"Bài 1\",\"week\":0}," +
            "{\"lesson_id\":\"tv1_t1_b42\",\"lesson_no\":42,\"title\":\"an\",\"type\":\"van_moi\",\"book\":\"tv1_t1_1990\",\"part\":\"van\",\"label\":\"Bài 42\",\"week\":0}," +
            "{\"lesson_id\":\"tv1_t2_b81\",\"lesson_no\":81,\"title\":\"anh\",\"type\":\"van_moi\",\"book\":\"tv1_t2_1996\",\"part\":\"van\",\"label\":\"Bài 81\",\"week\":0}," +
            "{\"lesson_id\":\"tv1_t2_b126\",\"lesson_no\":126,\"title\":\"Trường em\",\"type\":\"tap_doc\",\"book\":\"tv1_t2_1996\",\"part\":\"tap_doc\",\"label\":\"Bài 1\",\"week\":27}," +
            "{\"lesson_id\":\"tv1_t2_b137\",\"lesson_no\":137,\"title\":\"Câu đố\",\"type\":\"cau_do\",\"book\":\"tv1_t2_1996\",\"part\":\"tap_doc\",\"label\":\"Câu đố\",\"week\":28}," +
            "{\"lesson_id\":\"tv1_t2_b169\",\"lesson_no\":169,\"title\":\"Người nông dân và con gấu\",\"type\":\"doc_them\",\"book\":\"tv1_t2_1996\",\"part\":\"tap_doc\",\"label\":\"Bài 35\",\"week\":33}" +
            "]}";

        private static readonly string[] Ids =
            { "tv1_t1_b01", "tv1_t1_b42", "tv1_t2_b81", "tv1_t2_b126", "tv1_t2_b137", "tv1_t2_b169" };

        private void UseTwoBookIndex()
        {
            var real = new ResourcesContentSource();
            var source = new FakeContentSource { Fallback = real.Load };
            source.Put(ContentKind.LessonIndex, null, new TextAsset(Index));
            AppRoot.SourceFactory = () => source;
        }

        // Lớp cha chỉ đặt lại nguồn dữ liệu khi dùng tranh giả; nguồn giả ở đây phải dọn riêng để không lọt sang test sau.
        [TearDown]
        public void TearDownSource() => AppRoot.SourceFactory = null;

        private static LessonListScreen List() => Object.FindAnyObjectByType<LessonListScreen>();

        private static string CardText(string lessonId) =>
            List().ButtonFor(lessonId).GetComponentInChildren<TMP_Text>().text;

        [UnityTest]
        public IEnumerator ThreeSections_ByPart()
        {
            UseTwoBookIndex();
            yield return LoadMainWithProfile();
            var labels = LabelsUnder(List());
            Assert.That(labels, Has.Member(UiText.PartLetters));
            Assert.That(labels, Has.Member(UiText.PartRimes));
            Assert.That(labels, Has.Member(UiText.PartReading));
            Assert.IsTrue(Ids.All(id => List().ButtonFor(id) != null));
        }

        [UnityTest]
        public IEnumerator ReadingCard_ShowsLabelAndTitle()
        {
            UseTwoBookIndex();
            yield return LoadMainWithProfile();
            Assert.AreEqual("Bài 1\nTrường em", CardText("tv1_t2_b126"));
            Assert.AreEqual("Câu đố\nCâu đố", CardText("tv1_t2_b137"));
            Assert.AreEqual("Bài 81\nanh", CardText("tv1_t2_b81"));
            LayoutProbe.AssertFits(AppRoot.Instance.Canvas);
        }

        [UnityTest]
        public IEnumerator LongTitle_FitsCard()
        {
            UseTwoBookIndex();
            yield return LoadMainWithProfile();
            List().ScrollTo("tv1_t2_b169");
            yield return null;
            var text = List().ButtonFor("tv1_t2_b169").GetComponentInChildren<TMP_Text>();
            text.ForceMeshUpdate();
            Assert.IsFalse(text.isTextOverflowing, "Tên bài dài tràn khỏi thẻ");
        }

        [UnityTest]
        public IEnumerator WeekHeaders_InReadingPart()
        {
            UseTwoBookIndex();
            yield return LoadMainWithProfile();
            var labels = LabelsUnder(List());
            Assert.That(labels, Has.Member(string.Format(UiText.WeekFormat, 27)));
            Assert.That(labels, Has.Member(string.Format(UiText.WeekFormat, 28)));
            Assert.That(labels, Has.Member(string.Format(UiText.WeekFormat, 33)));
            Assert.That(labels, Has.No.Member(string.Format(UiText.WeekFormat, 0)));
        }

        [UnityTest]
        public IEnumerator Tap1Progress_CurrentLessonUnchanged()
        {
            UseTwoBookIndex();
            yield return LoadMainWithProfile();
            Assert.AreEqual("tv1_t1_b01", List().CurrentLessonId);
            AppRoot.Instance.Progress.MarkCompleted("tv1_t1_b01");
            AppRoot.Instance.ShowLessonList();
            yield return null;
            Assert.AreEqual("tv1_t1_b42", List().CurrentLessonId);
            Assert.IsFalse(List().ButtonFor("tv1_t2_b126").interactable, "Bài tập 2 mở khi chưa học tới");
        }

        [UnityTest]
        public IEnumerator ParentScreen_UnlockToggle_OpensLessons()
        {
            UseTwoBookIndex();
            // Màn Phụ huynh nạp chữ mọi bài; bài tập 2 ở đây là giả (không có file) nên kho bài báo lỗi rồi bỏ qua.
            LogAssert.ignoreFailingMessages = true;
            yield return LoadMainWithProfile();
            var child = AppRoot.Instance.Progress.Current;
            AppRoot.Instance.ShowParent();
            yield return WaitPrepared();
            var parent = Object.FindAnyObjectByType<ParentScreen>();
            parent.SimulateUnlock();
            yield return null;
            var toggle = parent.UnlockToggleFor(child.id);
            Assert.IsNotNull(toggle);
            Assert.That(LabelsUnder(toggle), Has.Member(UiText.UnlockAllOff));
            Press(toggle);
            yield return null;
            Assert.That(LabelsUnder(toggle), Has.Member(UiText.UnlockAllOn));
            Assert.IsTrue(ProgressStore.Load(StorePath).Profiles.Single(p => p.id == child.id).unlock_all, "Chưa lưu");
            LayoutProbe.AssertFits(AppRoot.Instance.Canvas);

            AppRoot.Instance.ShowLessonList();
            yield return null;
            Assert.IsTrue(Ids.All(id => List().ButtonFor(id).interactable), "Bật Mở mọi bài mà còn bài khoá");
        }
    }
}
