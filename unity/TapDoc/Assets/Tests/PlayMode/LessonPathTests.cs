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
    /// Con đường bài học (bản thiết kế nâng cấp UI mục 4.2, đợt 2): trạm theo thứ tự, biển chặng, gà con ở bài đang học,
    /// nút "Học tiếp", nút lật chặng, trạm lớp 2 có nhãn ngắn và tên bài dưới trạm.
    /// </summary>
    public class LessonPathTests : AppTestBase
    {
        private static LessonListScreen List() => Object.FindAnyObjectByType<LessonListScreen>();

        private static float Left(LessonListScreen list) => -list.Scroll.content.anchoredPosition.x;

        /// <summary>Bài của quyển đầu (danh sách mở mặc định), theo thứ tự.</summary>
        private static string[] FirstBook()
        {
            var index = AppRoot.Instance.Lessons.Index;
            return BookShelf.LessonIds(index, BookShelf.BookIds(index)[0]).ToArray();
        }

        [Test]
        public void TitleAndIconRules()
        {
            Assert.IsTrue(LessonListScreen.TitleInCircle(new LessonEntry { title = "u ư" }, 1), "Lớp 1 tên ngắn: trong trạm");
            Assert.IsFalse(LessonListScreen.TitleInCircle(new LessonEntry { title = "Dấu hỏi - Dấu ngã - Dấu nặng" }, 1),
                "Tên dài: dưới trạm");
            Assert.IsFalse(LessonListScreen.TitleInCircle(new LessonEntry { title = "Bé" }, 2), "Lớp 2: tên dưới trạm");
            Assert.AreEqual(SystemImages.Star, LessonListScreen.TypeIcon("on_tap_am"));
            Assert.AreEqual(SystemImages.EmDoc, LessonListScreen.TypeIcon("tap_doc"));
            Assert.IsNull(LessonListScreen.TypeIcon("tap_lam_van"), "Tập làm văn: chỉ chữ (ngôi nhà dễ lẫn với nút Về)");
            Assert.IsNull(LessonListScreen.TypeIcon("tap_chep_chinh_ta"));
            Assert.AreEqual(SystemImages.CauHoi, LessonListScreen.TypeIcon("cau_do"));
            Assert.IsNull(LessonListScreen.TypeIcon("am_moi"));
        }

        [UnityTest]
        public IEnumerator Stations_InOrder_LeftToRight()
        {
            yield return LoadMainWithProfile();
            yield return null;
            var list = List();
            var ordered = FirstBook();
            var xs = ordered.Select(id => ((RectTransform)list.ButtonFor(id).transform).anchoredPosition.x).ToList();
            for (var i = 1; i < xs.Count; i++) Assert.Greater(xs[i], xs[i - 1], $"{ordered[i]} nằm sau {ordered[i - 1]}");
            Assert.AreEqual(2, list.SectionCount, "Tập một: hai chặng (Chữ cái và âm, Vần)");
        }

        [UnityTest]
        public IEnumerator Mascot_OnCurrentStation_Single()
        {
            yield return LoadMainWithProfile();
            for (var i = 0; i < 5; i++) AppRoot.Instance.Progress.MarkCompleted(Ordered()[i]);
            AppRoot.Instance.ShowLessonList();
            yield return null;
            var list = List();
            Assert.AreEqual(Ordered()[5], list.CurrentLessonId);
            Assert.AreEqual(1, list.GetComponentsInChildren<Mascot>(true).Length, "Một gà con");
            var station = (RectTransform)list.ButtonFor(Ordered()[5]).transform;
            var mascot = (RectTransform)list.Mascot.transform;
            Assert.AreEqual(station.anchoredPosition.x, mascot.anchoredPosition.x, .5f, "Gà con đứng trên bài đang học");
            Assert.Greater(mascot.anchoredPosition.y, station.anchoredPosition.y);
            Assert.AreEqual(LessonListScreen.CurrentNodeSize, station.sizeDelta.x, .5f, "Bài đang học to hơn");
        }

        [UnityTest]
        public IEnumerator Continue_OpensCurrentLesson()
        {
            yield return LoadMainWithProfile();
            AppRoot.Instance.Progress.MarkCompleted(Ordered()[0]);
            AppRoot.Instance.ShowLessonList();
            yield return null;
            var list = List();
            Assert.IsTrue(list.ContinueButton.gameObject.activeSelf);
            Press(list.ContinueButton);
            yield return WaitPrepared();
            var lesson = Object.FindAnyObjectByType<LessonScreen>();
            Assert.IsNotNull(lesson, "Học tiếp mở màn học");
            Assert.AreEqual(Ordered()[1], lesson.LessonId, "Mở đúng bài đang học tới");
        }

        [UnityTest]
        public IEnumerator Continue_HiddenWhenAllDone()
        {
            yield return LoadMainWithProfile();
            foreach (var id in BookShelf.LessonIds(AppRoot.Instance.Lessons.Index, BookShelf.BookIds(AppRoot.Instance.Lessons.Index)[0]))
                AppRoot.Instance.Progress.MarkCompleted(id);
            AppRoot.Instance.OpenBook(BookShelf.BookIds(AppRoot.Instance.Lessons.Index)[0]);
            yield return null;
            var list = List();
            Assert.IsNull(list.CurrentLessonId);
            Assert.IsFalse(list.ContinueButton.gameObject.activeSelf, "Học hết quyển: không có Học tiếp");
            Assert.IsNotNull(list.Mascot, "Gà con vẫn đứng trên bài cuối");
        }

        [UnityTest]
        public IEnumerator Arrows_JumpOneSection()
        {
            yield return LoadMainWithProfile();
            yield return null;
            var list = List();
            Canvas.ForceUpdateCanvases();
            Assert.AreEqual(0f, Left(list), .5f, "Bài đầu: đường ở đầu");
            Assert.IsFalse(list.PrevButton.interactable, "Ở đầu đường: không lật lùi");
            Assert.IsTrue(list.NextButton.interactable);
            Assert.IsTrue(Pulse.IsRunning(list.NextButton.transform), "Mũi tên gợi ý còn đường phía sau");
            Press(list.NextButton);
            yield return null;
            Assert.Greater(Left(list), 0f, "Lật sang chặng sau");
            Assert.IsFalse(Pulse.IsRunning(list.NextButton.transform), "Bấm lật thì thôi gợi ý");
            Assert.IsTrue(list.PrevButton.interactable);
            var afterOne = Left(list);
            Press(list.PrevButton);
            yield return null;
            Assert.AreEqual(0f, Left(list), .5f, "Lật về chặng đầu");
            for (var i = 0; i < 10 && list.NextButton.interactable; i++) Press(list.NextButton);
            Assert.IsFalse(list.NextButton.interactable, "Tới cuối đường thì thôi lật");
            Assert.GreaterOrEqual(Left(list), afterOne);
            var last = (RectTransform)list.ButtonFor(FirstBook().Last()).transform;
            Assert.That(last.anchoredPosition.x + last.sizeDelta.x / 2f - Left(list),
                Is.LessThanOrEqualTo(list.Scroll.viewport.rect.width + 1f), "Bài cuối thấy được ở cuối đường");
        }

        [UnityTest, Timeout(600000)]
        public IEnumerator Grade2Books_Fit()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            foreach (var bookId in new[] { "tv2_t1_2001", "tv2_t2_2002" })
            {
                var ids = BookShelf.LessonIds(app.Lessons.Index, bookId);
                Assume.That(ids.Count, Is.GreaterThan(0), $"{bookId} chưa có bài");
                foreach (var size in new[] { ScreenSizes.Phone20x9, ScreenSizes.IPad43 })
                {
                    var rt = ScreenSizes.Apply(app, size);
                    app.OpenBook(bookId);
                    yield return null;
                    var list = List();
                    Canvas.ForceUpdateCanvases();
                    Assert.AreEqual(ids.Count, list.LessonCount, bookId);
                    Assert.AreEqual(3, list.SectionCount, $"{bookId}: ba chủ điểm");
                    foreach (var id in ids)
                    {
                        var station = list.ButtonFor(id);
                        var label = station.GetComponentInChildren<TMP_Text>();
                        label.ForceMeshUpdate();
                        Assert.IsFalse(label.isTextOverflowing, $"{id}: nhãn trong trạm tràn");
                        var caption = station.transform.Find("Caption")?.GetComponent<TMP_Text>();
                        Assert.IsNotNull(caption, $"{id}: lớp 2 có tên bài dưới trạm");
                        caption.ForceMeshUpdate();
                        Assert.LessOrEqual(caption.textInfo.lineCount, 2, $"{id}: tên bài tối đa 2 dòng");
                    }
                    list.ScrollTo(ids[ids.Count / 2]);
                    yield return null;
                    ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.Name}/app_con_duong_{bookId}.png");
                    LayoutProbe.AssertFits(app.Canvas);
                    ScreenSizes.Reset(app, rt);
                }
            }
        }
    }
}
