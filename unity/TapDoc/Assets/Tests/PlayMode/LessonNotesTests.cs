using System.Collections;
using System.Linq;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.UI;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>Nút "Ghi chú" trong màn bài: chỉ hiện khi bài có ghi chú; khung ghi chú chia theo loại, đóng lại được.</summary>
    public class LessonNotesTests : AppTestBase
    {
        /// <summary>Mở bài và chờ chuẩn bị xong; <see cref="Opened"/> là màn bài vừa mở.</summary>
        private IEnumerator Open(string lessonId)
        {
            AppRoot.Instance.ShowLesson(lessonId);
            yield return WaitPrepared();
            Opened = Object.FindAnyObjectByType<LessonScreen>();
        }

        private LessonScreen Opened { get; set; }

        private static Button ButtonUnder(Component root, string label) =>
            root.GetComponentsInChildren<Button>(false)
                .FirstOrDefault(b => b.GetComponentInChildren<TMP_Text>(true)?.text == label);

        [UnityTest]
        public IEnumerator Notes_ButtonOnlyWhenLessonHasNotes()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            yield return Open("tv1_t1_b20");
            var withNotes = Opened;
            yield return null;
            Assert.IsNotNull(withNotes.NotesButton);
            Assert.IsTrue(withNotes.NotesButton.gameObject.activeInHierarchy);
            Assert.AreEqual(UiText.Notes, withNotes.NotesButton.GetComponentInChildren<TMP_Text>().text);

            yield return Open("tv1_t1_b13");
            var without = Opened;
            yield return null;
            Assert.IsTrue(without.NotesButton == null || !without.NotesButton.gameObject.activeInHierarchy,
                "Bài 13 không có ghi chú mà vẫn hiện nút Ghi chú");
        }

        [UnityTest]
        public IEnumerator Notes_OpenShowsGroupedTextsAndCloses()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            yield return Open("tv1_t1_b68");
            var s = Opened;
            yield return null;
            Press(s.NotesButton);
            yield return null;
            Assert.IsNotNull(s.NotesPanel);
            Assert.IsTrue(s.NotesPanel.activeInHierarchy);
            var labels = LabelsUnder(s.NotesPanel.transform);
            Assert.That(labels, Has.Member(UiText.NoteKindBook));
            Assert.That(labels, Has.Member(UiText.NoteKindApp));
            Assert.That(labels, Has.No.Member(UiText.NoteKindReading)); // bài 68 không có tên đọc riêng
            Assert.That(labels, Has.Some.Contains("Vần ec rất ít gặp"));
            Assert.That(labels, Has.Some.Contains("chân dung"));

            Press(ButtonUnder(s.NotesPanel.transform, UiText.Close));
            yield return null;
            Assert.IsTrue(s.NotesPanel == null || !s.NotesPanel.activeInHierarchy, "Bấm Đóng mà khung ghi chú vẫn mở");
        }

        [UnityTest]
        public IEnumerator Notes_OpeningStopsSpeech()
        {
            // Phụ huynh mở ghi chú để đọc: giọng đọc của bước đang học phải dừng.
            yield return LoadMainWithProfile(unlockAll: true);
            yield return Open("tv1_t1_b20");
            var s = Opened;
            yield return null;
            Press(s.ReplayButton);
            yield return null;
            Assert.IsTrue(AppRoot.Instance.Speech.IsBusy, "Bấm Nghe lại mà không có giọng đọc");
            Press(s.NotesButton);
            yield return null;
            Assert.IsFalse(AppRoot.Instance.Speech.IsBusy);
        }

        [UnityTest]
        public IEnumerator Notes_WhyButtonOpensReadingNotes()
        {
            // Nút "Vì sao?" dưới các nút cách đọc mở khung Ghi chú có phần "Cách đọc theo sách".
            yield return LoadMainWithProfile(unlockAll: true);
            yield return Open("tv1_t1_b25");
            var s = Opened;
            yield return null;
            Press(ButtonUnder(s, UiText.Why));
            yield return null;
            Assert.IsNotNull(s.NotesPanel);
            Assert.IsTrue(s.NotesPanel.activeInHierarchy);
            Assert.That(LabelsUnder(s.NotesPanel.transform), Has.Member(UiText.NoteKindReading));
        }

        [UnityTest]
        public IEnumerator Notes_ReadingNamesShownForLetterLesson()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            yield return Open("tv1_t1_b25");
            var s = Opened;
            yield return null;
            Press(s.NotesButton);
            yield return null;
            var labels = LabelsUnder(s.NotesPanel.transform);
            Assert.That(labels, Has.Member(UiText.NoteKindReading));
            Assert.That(labels, Has.Some.Contains("\"gh\" khi học đọc là \"gờ kép\""));
        }

        [UnityTest]
        public IEnumerator Notes_PanelFitsPhoneAndTablet()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            foreach (var size in new[] { new Vector2Int(2400, 1080), new Vector2Int(2048, 1536) })
            {
                var rt = new RenderTexture(size.x, size.y, 24);
                AppRoot.Instance.UiCamera.targetTexture = rt;
                yield return Open("tv1_t1_b80"); // bài có nhiều ghi chú dài nhất
                var s = Opened;
                yield return null;
                Press(s.NotesButton);
                yield return null;
                ScreenProbe.Save(AppRoot.Instance.UiCamera, $"TestOutput/screens/{size.x}x{size.y}/app_lesson_notes.png");
                LayoutProbe.AssertFits(AppRoot.Instance.Canvas);
                AppRoot.Instance.UiCamera.targetTexture = null;
                Object.Destroy(rt);
            }
        }
    }
}
