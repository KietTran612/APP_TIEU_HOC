using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// Đợt 5 (bản thiết kế nâng cấp UI mục 4.5, 4.6): nghỉ mắt sau khi xong đủ số bài, ghi thời gian học, màn Phụ huynh
    /// có các mục Tuần này, Chơi cùng con, Thời lượng.
    /// </summary>
    public class RestAndParentTests : AppTestBase
    {
        private const string LessonId = "tv1_t1_b01";

        private IEnumerator FinishLesson(string lessonId)
        {
            AppRoot.Instance.Speech.WaitScale = .02f;
            AppRoot.Instance.ShowLesson(lessonId);
            yield return WaitPrepared();
            yield return WalkAll(Object.FindAnyObjectByType<LessonScreen>());
            var result = Object.FindAnyObjectByType<ResultScreen>();
            Assert.IsNotNull(result);
            result.SkipScene();
            yield return null;
        }

        [UnityTest]
        public IEnumerator Break_AfterSessionLessons_GoodbyeOrParentMore()
        {
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            app.Progress.Current.session_lessons = 1;
            yield return FinishLesson(LessonId);
            Assert.AreEqual(1, app.SessionLessons);
            Assert.IsTrue(app.BreakDue);
            Press(Object.FindAnyObjectByType<ResultScreen>().NextLessonButton);
            yield return null;
            var rest = Object.FindAnyObjectByType<BreakScreen>();
            Assert.IsNotNull(rest, "Học đủ số bài: qua màn nghỉ mắt");
            StringAssert.Contains("1", rest.TodayLabel.text);
            Assert.AreEqual(UiText.BreakMascot, rest.Mascot.BubbleText);
            Assert.IsNotEmpty(rest.Suggestion.text);
            // Phụ huynh cho học thêm qua khoá phép tính: lần học mới, đi tiếp tới bài sau.
            rest.OpenGate();
            yield return null;
            rest.Gate.SimulateUnlock();
            yield return WaitPrepared();
            Assert.IsNotNull(Object.FindAnyObjectByType<LessonScreen>(), "Học thêm: vào bài sau");
            Assert.AreEqual(0, app.SessionLessons, "Bắt đầu lần học mới");
            Assert.AreEqual(Ordered()[1], Object.FindAnyObjectByType<LessonScreen>().LessonId);
        }

        [UnityTest]
        public IEnumerator Break_Goodbye_GoesToProfiles()
        {
            yield return LoadMainWithProfile();
            AppRoot.Instance.Progress.Current.session_lessons = 1;
            yield return FinishLesson(LessonId);
            Press(Object.FindAnyObjectByType<ResultScreen>().ToListButton);
            yield return null;
            var rest = Object.FindAnyObjectByType<BreakScreen>();
            Assert.IsNotNull(rest, "Nút Về danh sách cũng qua màn nghỉ mắt");
            Press(rest.GoodbyeButton);
            yield return null;
            Assert.IsNotNull(Object.FindAnyObjectByType<ProfileScreen>(), "Tạm biệt: về màn chọn bé");
        }

        [UnityTest]
        public IEnumerator NoBreak_WhenOff()
        {
            yield return LoadMainWithProfile(); // AppTestBase: 0 = không nhắc
            yield return FinishLesson(LessonId);
            Assert.IsFalse(AppRoot.Instance.BreakDue);
            Press(Object.FindAnyObjectByType<ResultScreen>().NextLessonButton);
            yield return WaitPrepared();
            Assert.IsNull(Object.FindAnyObjectByType<BreakScreen>());
            Assert.IsNotNull(Object.FindAnyObjectByType<LessonScreen>());
        }

        [UnityTest]
        public IEnumerator StudyTime_RecordedWhenLeavingLesson()
        {
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            app.ShowLesson(LessonId);
            yield return WaitPrepared();
            yield return new WaitForSecondsRealtime(1.3f);
            Press(Object.FindAnyObjectByType<LessonScreen>().BackButton);
            yield return null;
            var today = ProgressStore.DayOf(app.Progress.Current, System.DateTime.Now);
            Assert.GreaterOrEqual(today.seconds, 1, "Thời gian ở màn học được ghi");
            Assert.AreEqual(0, today.lessons, "Chưa xong bài thì chưa tính bài");
        }

        [UnityTest]
        public IEnumerator Parent_Tabs_WeekPlayTime()
        {
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            yield return FinishLesson("tv1_t1_b13");
            app.Progress.RecordMistake("tv1_t1_b13", 0);
            app.ShowParent();
            yield return WaitPrepared();
            var p = Object.FindAnyObjectByType<ParentScreen>();
            p.SimulateUnlock();
            yield return null;
            var id = app.Progress.Current.id;
            Assert.AreEqual(ParentScreen.ParentTab.Week, p.CurrentTab);
            StringAssert.Contains("1 bài", p.WeekLineFor(id).text);
            var chip = p.ChipButtonsFor(id).First();
            Assert.IsTrue(chip.interactable, "Chữ hay nhầm có tiếng: chạm để nghe");
            var round = app.Lessons.Get("tv1_t1_b13").part2[0];
            var expected = round.kind == "look_tone" ? round.prompt_audio : round.options[round.answer].audio;
            Press(chip);
            yield return null;
            Assert.AreEqual(expected, app.Speech.History.Last(), "Chạm thẻ thì đọc đúng chữ");

            Press(p.TabButton(ParentScreen.ParentTab.Play));
            yield return null;
            Assert.AreEqual(ParentScreen.ParentTab.Play, p.CurrentTab);
            var entry = app.Lessons.Index.lessons.First(e => e.lesson_id == "tv1_t1_b13");
            CollectionAssert.AreEqual(ParentSuggestions.For(entry, app.Lessons.Get(entry.lesson_id)), p.PlayLinesFor(id));

            Press(p.TabButton(ParentScreen.ParentTab.Time));
            yield return null;
            Press(p.SessionButtonFor(id, 5));
            Assert.AreEqual(5, app.Progress.Current.session_lessons);
            Assert.AreEqual(5, ProgressStore.Load(StorePath).Current.session_lessons, "Lưu xuống file");
            Press(p.SessionButtonFor(id, 0));
            Assert.AreEqual(0, app.Progress.Current.session_lessons, "Phụ huynh tắt được");
        }

        [UnityTest, Timeout(600000)]
        public IEnumerator Screens_ParentAndBreak_FourSizes()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile();
            var app = AppRoot.Instance;
            app.Progress.Current.session_lessons = 1;
            yield return FinishLesson("tv1_t1_b13");
            app.Progress.RecordMistake("tv1_t1_b13", 0);
            app.Progress.CreateProfile("Na", ProfileScreen.Avatars[1]);
            app.Progress.Select(app.Progress.Profiles[0].id);
            foreach (var size in new[] { ScreenSizes.Phone20x9, ScreenSizes.IPad43, ScreenSizes.Tablet16x10, ScreenSizes.TabletPortrait })
            {
                var rt = ScreenSizes.Apply(app, size);
                app.ShowBreak(() => { });
                yield return null;
                Canvas.ForceUpdateCanvases();
                ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.Name}/app_dot5_nghi_mat.png");
                LayoutProbe.AssertFits(app.Canvas);

                app.ShowParent();
                yield return WaitPrepared();
                var p = Object.FindAnyObjectByType<ParentScreen>();
                p.SimulateUnlock();
                yield return null;
                foreach (var tab in new[] { ParentScreen.ParentTab.Week, ParentScreen.ParentTab.Play, ParentScreen.ParentTab.Time })
                {
                    p.ShowTab(tab);
                    yield return null;
                    Canvas.ForceUpdateCanvases();
                    ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.Name}/app_dot5_phu_huynh_{tab}.png");
                    LayoutProbe.AssertFits(app.Canvas);
                }
                ScreenSizes.Reset(app, rt);
            }
        }
    }
}
