using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.UI;
using Object = UnityEngine.Object;

namespace TapDoc.Tests
{
    /// <summary>
    /// Nâng cấp UI đợt 1, màn học (bản thiết kế nâng cấp UI mục 4.1): con đường hạt có đích, gà con nói, nhắc khi bé
    /// ngồi im, nút của bé cách mép, tiếng động nhỏ lại dưới giọng đọc.
    /// </summary>
    public class LessonGuideTests : AppTestBase
    {
        private const string LessonId = "tv1_t1_b13";
        private const string LessonWithNotes = "tv1_t1_b01";

        private float _now;

        private static LessonScreen Screen() => Object.FindAnyObjectByType<LessonScreen>();

        private IEnumerator Open(string lessonId = LessonId)
        {
            yield return LoadMainWithProfile(unlockAll: true);
            AppRoot.Instance.Speech.WaitScale = .02f;
            AppRoot.Instance.ShowLesson(lessonId);
            yield return WaitPrepared();
        }

        private static IEnumerator WaitSpeechIdle()
        {
            for (var i = 0; i < 600 && AppRoot.Instance.Speech.IsBusy; i++) yield return null;
            Assert.IsFalse(AppRoot.Instance.Speech.IsBusy, "Giọng đọc không dừng");
        }

        /// <summary>
        /// Bật nhắc (test app tắt mặc định), đồng hồ giả bắt đầu ở mốc mới; chờ một khung để bộ nhắc nhận kiểu bước, rồi
        /// bộ đếm tính từ mốc này.
        /// </summary>
        private IEnumerator UseFakeClock(LessonScreen s)
        {
            IdleNudge.Enabled = true;
            _now = 1000f;
            s.Clock = () => _now;
            yield return null;
            s.Nudge.NoteActivity(_now);
        }

        private IEnumerator Advance(float seconds)
        {
            _now += seconds;
            yield return null;
        }

        /// <summary>Khung bao (đã xoay nếu có) của <paramref name="rt"/> trong toạ độ canvas.</summary>
        private static Rect CanvasRect(RectTransform rt)
        {
            var corners = new Vector3[4];
            rt.GetWorldCorners(corners);
            var canvas = (RectTransform)AppRoot.Instance.Canvas.transform;
            var min = new Vector2(float.MaxValue, float.MaxValue);
            var max = new Vector2(float.MinValue, float.MinValue);
            foreach (var c in corners)
            {
                Vector2 p = canvas.InverseTransformPoint(c);
                min = Vector2.Min(min, p);
                max = Vector2.Max(max, p);
            }
            return Rect.MinMaxRect(min.x, min.y, max.x, max.y);
        }

        /// <summary>Tâm thật của <paramref name="rt"/> (giữa khung, kể cả khi xoay) trong toạ độ canvas.</summary>
        private static Vector2 CanvasCenter(RectTransform rt)
        {
            var corners = new Vector3[4];
            rt.GetWorldCorners(corners);
            var canvas = (RectTransform)AppRoot.Instance.Canvas.transform;
            return canvas.InverseTransformPoint((corners[0] + corners[2]) / 2f);
        }

        /// <summary><paramref name="inner"/> nằm trong <paramref name="outer"/> (dung sai làm tròn nửa đơn vị).</summary>
        private static bool Inside(Rect outer, Rect inner) =>
            inner.xMin >= outer.xMin - .5f && inner.yMin >= outer.yMin - .5f
            && inner.xMax <= outer.xMax + .5f && inner.yMax <= outer.yMax + .5f;

        private static Image FillOf(RectTransform bead) => bead.Find("Fill").GetComponent<Image>();

        [Test]
        public void Path_BeadsAndGoal()
        {
            var go = new GameObject("host", typeof(RectTransform));
            try
            {
                var dots = ProgressDots.Create(go.transform, 10);
                Assert.IsFalse(dots.IsBar);
                Assert.IsNotNull(dots.Goal, "Cuối đường có bông hoa");
                var last = (RectTransform)dots.transform.Find("Dot_9");
                Assert.Greater(dots.Goal.rectTransform.anchoredPosition.x, last.anchoredPosition.x, "Bông hoa ở cuối đường");
                dots.SetCurrent(3);
                Assert.AreEqual(ProgressDots.CurrentDot, dots.CurrentMarker.sizeDelta.x, .01f, "Hạt đang học to hơn");
                Assert.AreEqual(Palette.Orange, FillOf(dots.CurrentMarker).color);
                Assert.AreEqual(Palette.Teal, FillOf((RectTransform)dots.transform.Find("Dot_0")).color, "Hạt đã qua");
                var next = (RectTransform)dots.transform.Find("Dot_4");
                Assert.AreEqual(Palette.PaperLight, FillOf(next).color, "Hạt chưa tới");
                Assert.AreEqual(ProgressDots.Dot, next.sizeDelta.x, .01f);
                Assert.IsTrue(Pulse.IsRunning(dots.CurrentMarker), "Hạt đang học nhún nhẹ");
                Assert.IsNull(dots.GetComponentInChildren<Mascot>(true), "Không có gà con trên đường");

                Assert.IsFalse(ProgressDots.Create(go.transform, 20).IsBar, "Bài 20 bước vẫn là hạt");
                var bar = ProgressDots.Create(go.transform, 40);
                Assert.IsTrue(bar.IsBar);
                Assert.IsNotNull(bar.Goal, "Đường liền vẫn có bông hoa");
                bar.SetCurrent(19);
                Assert.Greater(bar.CurrentMarker.anchoredPosition.x, 0f, "Dấu cam ở chỗ đang học");
                Assert.LessOrEqual(((RectTransform)bar.transform).sizeDelta.x, ProgressDots.MaxWidth + .01f);
            }
            finally
            {
                Object.DestroyImmediate(go);
            }
        }

        [UnityTest]
        public IEnumerator Path_FitsTopBand_AllSizes()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            foreach (var size in ScreenSizes.All)
            {
                var rt = ScreenSizes.Apply(app, size);
                app.ShowLesson(LessonWithNotes);
                yield return WaitPrepared();
                var s = Screen();
                Canvas.ForceUpdateCanvases();
                var dots = CanvasRect((RectTransform)s.Dots.transform);
                Assert.IsFalse(dots.Overlaps(CanvasRect(s.Stage)), $"{size}: đường hạt nằm trên phần học");
                Assert.IsFalse(dots.Overlaps(CanvasRect((RectTransform)s.BackButton.transform)), $"{size}: đường hạt đè nút Về");
                Assert.IsNotNull(s.NotesButton, "Bài có Ghi chú");
                Assert.IsFalse(dots.Overlaps(CanvasRect((RectTransform)s.NotesButton.transform)), $"{size}: đường hạt đè nút Ghi chú");
                Assert.IsTrue(Inside(CanvasRect(app.KidRoot), dots),
                    $"{size}: đường hạt trong khung bé");
                ScreenSizes.Reset(app, rt);
            }
        }

        [UnityTest]
        public IEnumerator Layout_EdgeGap_AllSizes()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            const float gap = ScreenLayout.EdgeGap - .5f;
            foreach (var size in ScreenSizes.All)
            {
                var rt = ScreenSizes.Apply(app, size);
                app.ShowLesson(LessonId);
                yield return WaitPrepared();
                var s = Screen();
                s.NextButton.gameObject.SetActive(true);
                Canvas.ForceUpdateCanvases();
                var kid = CanvasRect(app.KidRoot);
                var screen = ((RectTransform)app.Canvas.transform).rect;
                var replay = CanvasRect((RectTransform)s.ReplayButton.transform);
                var next = CanvasRect((RectTransform)s.NextButton.transform);
                var back = CanvasRect((RectTransform)s.BackButton.transform);
                Assert.GreaterOrEqual(replay.xMin - screen.xMin, gap, $"{size}: Nghe lại cách mép trái");
                Assert.GreaterOrEqual(replay.yMin - screen.yMin, gap, $"{size}: Nghe lại cách mép dưới");
                Assert.GreaterOrEqual(screen.xMax - next.xMax, gap, $"{size}: Tiếp cách mép phải");
                Assert.GreaterOrEqual(next.yMin - screen.yMin, gap, $"{size}: Tiếp cách mép dưới");
                Assert.GreaterOrEqual(back.xMin - screen.xMin, gap, $"{size}: Về cách mép trái");
                foreach (var b in new[] { replay, next, back })
                {
                    Assert.IsTrue(Inside(kid, b), $"{size}: nút trong khung bé");
                }
                var phone = size.Wide && size.Pixels.x / (float)size.Pixels.y >= ScreenLayout.PhoneAspect;
                var minButton = phone ? 180f : UiKit.MinTouch;
                Assert.GreaterOrEqual(next.width, minButton - .5f, $"{size}: nút Tiếp đủ to");
                Assert.GreaterOrEqual(replay.width, minButton - .5f, $"{size}: nút Nghe lại đủ to");
                var stage = CanvasRect(s.Stage);
                var mascot = CanvasRect((RectTransform)s.Mascot.transform);
                Assert.IsFalse(stage.Overlaps(mascot), $"{size}: gà con không đè phần học");
                Assert.IsFalse(next.Overlaps(mascot), $"{size}: gà con không đè nút Tiếp");
                Assert.IsTrue(Inside(kid, mascot), $"{size}: gà con trong khung bé");
                foreach (var b in new[] { replay, next, back })
                {
                    Assert.IsFalse(stage.Overlaps(b), $"{size}: phần học đè nút");
                }
                ScreenSizes.Reset(app, rt);
            }
        }

        [UnityTest]
        public IEnumerator Mascot_TalksWhileSpeaking()
        {
            yield return Open();
            var s = Screen();
            Assert.AreEqual(1, s.GetComponentsInChildren<Mascot>(true).Length, "Màn học chỉ một gà con");
            yield return WaitSpeechIdle();
            yield return null;
            Assert.IsFalse(s.Talk.IsShown);
            _ = AppRoot.Instance.Speech.PlayAsync(SystemAudio.hd_thu_lai);
            yield return null;
            yield return null;
            Assert.IsTrue(s.Talk.IsShown, "Gà con nói khi giọng đọc chạy");
            AppRoot.Instance.Speech.Stop();
            yield return null;
            Assert.IsFalse(s.Talk.IsShown);
        }

        [UnityTest]
        public IEnumerator Nudge_ReadStep_HandOnNext()
        {
            yield return Open();
            var s = Screen();
            yield return ((ITestCompletable)s.CurrentView).CompleteForTest();
            yield return null;
            Assert.IsTrue(s.NextButton.gameObject.activeSelf);
            yield return WaitSpeechIdle();
            yield return UseFakeClock(s);
            var spoken = AppRoot.Instance.Speech.History.Count;
            yield return Advance(IdleNudge.ReadHandSeconds - .5f);
            Assert.IsFalse(s.Hand.IsShown, "Chưa tới 30 s");
            yield return Advance(.5f);
            Assert.IsTrue(s.Hand.IsShown, "30 s: bàn tay");
            Assert.AreSame(s.NextButton.transform, s.Hand.Target, "Bàn tay chỉ nút Tiếp");
            Assert.AreEqual(spoken, AppRoot.Instance.Speech.History.Count, "Bước đã xong: không đọc lại lời dẫn");

            s.Nudge.NoteActivity(_now); // bé chạm
            yield return null;
            Assert.IsFalse(s.Hand.IsShown, "Chạm thì ẩn bàn tay");
        }

        [UnityTest]
        public IEnumerator Nudge_Part2_PointsReplay()
        {
            yield return LoadMainWithProfile();
            AppRoot.Instance.Progress.RecordMistake(LessonId, 0);
            AppRoot.Instance.Speech.WaitScale = .02f;
            AppRoot.Instance.ShowReview();
            yield return WaitPrepared();
            var s = Screen();
            Assert.AreEqual(Phase.Part2, s.Flow.Phase);
            Assert.AreEqual(NudgeKind.Tap, s.NudgeKindNow());
            yield return WaitSpeechIdle();
            yield return UseFakeClock(s);
            var spoken = AppRoot.Instance.Speech.History.Count;
            yield return Advance(IdleNudge.TapRepromptSeconds);
            Assert.Greater(AppRoot.Instance.Speech.History.Count, spoken, "12 s: đọc lại lời dẫn");
            // Lời đọc lại đang chạy thì chưa tính là ngồi im; đếm tiếp từ lúc giọng đọc dừng (đồng hồ giả đứng yên).
            yield return WaitSpeechIdle();
            yield return Advance(IdleNudge.TapHandSeconds - .5f);
            Assert.IsFalse(s.Hand.IsShown);
            yield return Advance(.5f);
            Assert.IsTrue(s.Hand.IsShown, "Bàn tay hiện");
            Assert.AreSame(s.ReplayButton.transform, s.Hand.Target, "Phần 2: chỉ nút Nghe lại, không chỉ đáp án");
        }

        [UnityTest]
        public IEnumerator Nudge_OffByDefaultInTests()
        {
            // Test luồng bài (smoke, đi hết bài) không bị nhắc chen vào: ngồi im bao lâu cũng không đọc lại, không hiện tay.
            yield return Open();
            var s = Screen();
            Assert.IsFalse(IdleNudge.Enabled, "AppTestBase tắt nhắc mặc định");
            yield return WaitSpeechIdle();
            _now = 1000f;
            s.Clock = () => _now;
            var spoken = AppRoot.Instance.Speech.History.Count;
            for (var i = 0; i < 5; i++) yield return Advance(60f);
            Assert.AreEqual(spoken, AppRoot.Instance.Speech.History.Count, "Không đọc lại lời dẫn");
            Assert.IsFalse(s.Hand.IsShown, "Không hiện bàn tay");
        }

        /// <summary>
        /// Ảnh cho root soát (mỗi khung): bước từ khoá có tranh lớp 1, lượt bấm chọn Phần 2, bước đọc câu lớp 2. Đi bài
        /// tới bước cần chụp rồi dừng.
        /// </summary>
        [UnityTest, Timeout(900000)]
        public IEnumerator Screens_KeySteps_FourSizes()
        {
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            app.Speech.WaitScale = .02f;
            var sizes = new[] { ScreenSizes.Phone20x9, ScreenSizes.IPad43, ScreenSizes.Tablet16x10, ScreenSizes.TabletPortrait };
            var shots = new[]
            {
                (lesson: LessonId, part: Phase.Part1, type: "keyword", name: "app_dot1_tu_khoa"),
                (lesson: LessonId, part: Phase.Part2, type: (string)null, name: "app_dot1_phan2"),
                (lesson: "tv2_t1_b180", part: Phase.Part1, type: "sentence", name: "app_dot1_doc_cau_lop2"),
            };
            foreach (var size in sizes)
            {
                var rt = ScreenSizes.Apply(app, size);
                foreach (var shot in shots)
                {
                    app.ShowLesson(shot.lesson);
                    yield return WaitPrepared();
                    var s = Screen();
                    for (var guard = 0; guard < 80; guard++)
                    {
                        yield return null;
                        var here = s.Flow.Phase == shot.part
                            && (shot.type == null || s.Flow.CurrentStep?.type == shot.type);
                        if (here) break;
                        Assert.AreNotEqual(Phase.Done, s.Flow.Phase, $"{shot.lesson}: không có bước {shot.type}");
                        yield return ((ITestCompletable)s.CurrentView).CompleteForTest();
                        if (s.Flow.Phase == Phase.Part1) s.NextButton.onClick.Invoke();
                        yield return new WaitForSeconds(.2f);
                        s = Screen();
                    }
                    yield return WaitSpeechIdle();
                    Canvas.ForceUpdateCanvases();
                    ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.Name}/{shot.name}.png");
                    LayoutProbe.AssertFits(app.Canvas);
                }
                ScreenSizes.Reset(app, rt);
            }
        }

        /// <summary>
        /// Smoke: đi hết bài đầu của mỗi quyển qua màn học thật (khung điện thoại), nhắc tắt như mọi test luồng bài; tới
        /// màn kết quả, không lỗi, không cảnh báo.
        /// </summary>
        [UnityTest, Timeout(900000)]
        public IEnumerator Smoke_FirstLessonEachBook()
        {
            UseStubsForMissingAssets(); // tranh, tiếng của quyển chưa nhập đủ không phải điều đang kiểm
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            app.Speech.WaitScale = .02f;
            var rt = ScreenSizes.Apply(app, ScreenSizes.Phone20x9);
            var index = app.Lessons.Index;
            foreach (var book in BookShelf.BookIds(index))
            {
                var ids = BookShelf.LessonIds(index, book);
                if (ids.Count == 0) continue;
                app.ShowLesson(ids[0]);
                yield return WaitPrepared();
                yield return WalkAll(Screen());
                Assert.IsNotNull(Object.FindAnyObjectByType<ResultScreen>(), $"{ids[0]}: không tới màn kết quả");
            }
            ScreenSizes.Reset(app, rt);
            LogAssert.NoUnexpectedReceived();
        }

        [UnityTest]
        public IEnumerator Hand_FitsAllSizes()
        {
            UseStubsForMissingAssets();
            yield return LoadMainWithProfile(unlockAll: true);
            var app = AppRoot.Instance;
            foreach (var size in ScreenSizes.All)
            {
                var rt = ScreenSizes.Apply(app, size);
                app.ShowLesson(LessonId);
                yield return WaitPrepared();
                var s = Screen();
                s.NextButton.gameObject.SetActive(true);
                Canvas.ForceUpdateCanvases();
                s.Hand.Show((RectTransform)s.NextButton.transform);
                Canvas.ForceUpdateCanvases();
                var kid = CanvasRect(app.KidRoot);
                var hand = CanvasRect((RectTransform)s.Hand.transform);
                Assert.IsTrue(Inside(kid, hand), $"{size}: bàn tay trong khung bé");
                var next = CanvasRect((RectTransform)s.NextButton.transform);
                Assert.IsFalse(next.Contains(CanvasCenter((RectTransform)s.Hand.transform)),
                    $"{size}: thân bàn tay nằm ngoài nút Tiếp (không che biểu tượng)");
                Assert.IsFalse(s.Hand.GetComponent<Image>().raycastTarget, "Bàn tay không chặn chạm");
                ScreenProbe.Save(app.UiCamera, $"TestOutput/screens/{size.Name}/app_lesson_hint.png");
                LayoutProbe.AssertFits(app.Canvas);
                ScreenSizes.Reset(app, rt);
            }
        }

        [UnityTest]
        public IEnumerator Sfx_DucksUnderSpeech()
        {
            yield return Open();
            yield return WaitSpeechIdle();
            var app = AppRoot.Instance;
            _ = app.Speech.PlayAsync(SystemAudio.hd_thu_lai);
            yield return null;
            Assert.IsTrue(app.Speech.IsBusy);
            app.Sfx.Play(SystemSfx.Correct);
            Assert.AreEqual(SfxPlayer.DuckedVolume, app.Sfx.LastVolume, .001f, "Tiếng động nhỏ lại khi có giọng đọc");
            app.Speech.Stop();
            yield return null;
            app.Sfx.Play(SystemSfx.Correct);
            Assert.AreEqual(SfxPlayer.DefaultVolume, app.Sfx.LastVolume, .001f);
        }
    }
}
