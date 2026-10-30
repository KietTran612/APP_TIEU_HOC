using System;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    public class LessonScreen : MonoBehaviour
    {
        private AppRoot _app;
        private Lesson _lesson;
        private ReviewSession _review;
        private RectTransform _stage;
        private int _stepToken;
        private bool _advancing;

        public LessonFlow Flow { get; private set; }
        public object CurrentView { get; private set; }
        public Button NextButton { get; private set; }
        public Button ReplayButton { get; private set; }
        public Button BackButton { get; private set; }
        public Button NotesButton { get; private set; }
        public GameObject NotesPanel { get; private set; }

        /// <summary>Hàng chấm tiến độ của bài.</summary>
        public ProgressDots Dots { get; private set; }

        /// <summary>Bạn gà con, cạnh nút "Tiếp".</summary>
        public Mascot Mascot { get; private set; }

        /// <summary>Vùng học (các bước đặt trong đây).</summary>
        internal RectTransform Stage => _stage;

        /// <summary>Trang của bước trước đang lật đi; <c>null</c> khi không lật.</summary>
        internal GameObject TurningPage { get; private set; }

        private const float Margin = 20f;
        private const float PageTurnSeconds = .4f;
        private LessonFx _fx;

        /// <summary>
        /// Mở bài <paramref name="lesson"/>. <paramref name="review"/> khác <c>null</c> khi đây là phiên "Ôn lại"
        /// (<paramref name="lesson"/> là <see cref="ReviewSession.Lesson"/>).
        /// </summary>
        public void Build(AppRoot app, Lesson lesson, ReviewSession review = null)
        {
            _app = app;
            _lesson = lesson;
            _review = review;
            Flow = new LessonFlow(lesson);

            BackButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Home, UiText.Back, OnBackClicked);
            Corner(BackButton, new Vector2(0f, 1f), new Vector2(Margin, -Margin));
            BackButton.GetComponent<TapFeedback>().Sound = SystemSfx.Tap;

            // Nút loa làm giọng đọc phát ngay: không có tiếng chạm; nhún theo nhịp khi giọng đọc đang phát.
            ReplayButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Speaker, UiText.Replay, OnReplayClicked);
            Corner(ReplayButton, Vector2.zero, new Vector2(Margin, Margin));
            ReplayButton.gameObject.AddComponent<SpeakingBob>().Init(app.Speech);

            // Nút "Tiếp" dùng tiếng lật trang của bước mới, không có tiếng chạm riêng.
            NextButton = UiKit.CreateIconButton(transform, app.Assets, SystemIcons.Forward, UiText.Next, OnNextClicked,
                Palette.Orange);
            Corner(NextButton, new Vector2(1f, 0f), new Vector2(-Margin, Margin));
            NextButton.gameObject.SetActive(false);

            _stage = UiKit.CreateStage((RectTransform)transform);

            Dots = ProgressDots.Create(transform, Flow.TotalCount);
            var dotsRt = (RectTransform)Dots.transform;
            dotsRt.anchorMin = dotsRt.anchorMax = new Vector2(.5f, 1f);
            dotsRt.anchoredPosition = new Vector2(0f, -UiKit.StageTopInset / 2f);

            Mascot = Mascot.Create(transform, app.Assets);
            var mascotRt = (RectTransform)Mascot.transform;
            mascotRt.anchorMin = mascotRt.anchorMax = mascotRt.pivot = new Vector2(1f, 0f);
            mascotRt.anchoredPosition = new Vector2(-(2f * Margin + UiKit.MinTouch), Margin);

            var overlay = new GameObject("FxOverlay", typeof(RectTransform));
            overlay.transform.SetParent(transform, false);
            var overlayRt = (RectTransform)overlay.transform;
            overlayRt.anchorMin = Vector2.zero;
            overlayRt.anchorMax = Vector2.one;
            overlayRt.offsetMin = Vector2.zero;
            overlayRt.offsetMax = Vector2.zero;
            _fx = new LessonFx(overlayRt, app.Assets, app.Sfx, Mascot);

            if (lesson.notes != null && lesson.notes.Count > 0)
            {
                NotesButton = UiKit.CreateButton(transform, UiText.Notes, OpenNotes);
                var notesRt = (RectTransform)NotesButton.transform;
                notesRt.anchorMin = notesRt.anchorMax = notesRt.pivot = Vector2.one;
                notesRt.sizeDelta = new Vector2(260f, UiKit.MinTouch);
                notesRt.anchoredPosition = new Vector2(-20f, -20f);
            }

            PresentCurrent(turnPage: false);
        }

        private static void Corner(Button button, Vector2 corner, Vector2 offset)
        {
            var rt = (RectTransform)button.transform;
            rt.anchorMin = rt.anchorMax = rt.pivot = corner;
            rt.anchoredPosition = offset;
        }

        private void OpenNotes()
        {
            if (NotesPanel == null) NotesPanel = TapDoc.NotesPanel.ForLesson(transform, _lesson);
            NotesPanel.transform.SetAsLastSibling();
            NotesPanel.SetActive(true);
        }

        private void PresentCurrent(bool turnPage)
        {
            _stepToken++;
            var token = _stepToken;
            _advancing = false;

            if (NextButton != null)
            {
                NextButton.gameObject.SetActive(false);
            }

            if (turnPage) TurnCurrentPage();
            else ClearCurrentView();
            if (Dots != null) Dots.SetCurrent(Flow.Position);

            if (Flow.Phase == Phase.Done)
            {
                _app.ShowResult(_lesson.lesson_id);
                return;
            }

            var ctx = new LessonContext
            {
                Lesson = _lesson,
                Speech = _app.Speech,
                Assets = _app.Assets,
                Stage = _stage,
                Fx = _fx,
                RoundFinished = OnRoundFinished
            };

            // Handler gắn trước Bind (qua StepViewFactory). Nếu màn báo xong ngay trong Bind thì ghi nhận
            // lại và xử lý sau khi CurrentView đã gán, để không chuyển bước lồng nhau giữa lúc đang tạo màn.
            var binding = true;
            var completedDuringBind = false;
            void OnViewCompleted()
            {
                if (this == null || token != _stepToken) return;
                if (binding)
                {
                    completedDuringBind = true;
                    return;
                }
                HandleViewCompleted();
            }

            if (Flow.Phase == Phase.Part1)
            {
                CurrentView = StepViewFactory.CreateStep(Flow.CurrentStep, ctx, OnViewCompleted);
            }
            else
            {
                CurrentView = StepViewFactory.CreateRound(Flow.CurrentRound, ctx, OnViewCompleted);
            }

            binding = false;
            if (completedDuringBind && this != null && token == _stepToken)
            {
                HandleViewCompleted();
            }
        }

        private void HandleViewCompleted()
        {
            if (Flow.Phase == Phase.Part1)
            {
                if (NextButton != null)
                {
                    NextButton.gameObject.SetActive(true);
                    ShowNextButton();
                }
            }
            else if (Flow.Phase == Phase.Part2 && !_advancing)
            {
                // Phần 2 tự chuyển lượt khi màn báo xong (màn chỉ báo sau khi đọc xong lời khen).
                _advancing = true;
                AdvanceFlow();
            }
        }

        /// <summary>
        /// Một lượt Phần 2 vừa xong. Bài thường: bé có nhầm thì ghi lượt nhầm. Phiên "Ôn lại": nhầm thì tăng số lần
        /// nhầm của lượt gốc, làm đúng ngay thì xóa lượt gốc khỏi danh sách nhầm. Mọi thay đổi được lưu ngay, để bé
        /// thoát giữa chừng vẫn không mất.
        /// </summary>
        private void OnRoundFinished(Round round, int mistakes)
        {
            if (this == null || _lesson == null) return;
            var index = _lesson.part2.IndexOf(round);
            if (index < 0) return;

            if (_review != null)
            {
                if (index >= _review.Sources.Count) return;
                var (lessonId, sourceRound) = _review.Sources[index];
                if (mistakes > 0) _app.Progress.RecordMistake(lessonId, sourceRound);
                else _app.Progress.ClearMistake(lessonId, sourceRound);
            }
            else
            {
                if (mistakes <= 0) return;
                _app.Progress.RecordMistake(_lesson.lesson_id, index);
            }
            _app.SaveProgress();
        }

        private void OnNextClicked()
        {
            if (_advancing || NextButton == null || !NextButton.gameObject.activeSelf)
            {
                return;
            }
            _advancing = true;
            Pulse.StopOn(NextButton.transform);
            NextButton.gameObject.SetActive(false);
            _app.Speech.Stop();
            AdvanceFlow();
        }

        private void AdvanceFlow()
        {
            Flow.Next();
            if (Flow.Phase == Phase.Done)
            {
                _app.ShowResult(_lesson.lesson_id);
            }
            else
            {
                PresentCurrent(turnPage: true);
            }
        }

        private void OnReplayClicked()
        {
            if (CurrentView is IStepView sv)
            {
                sv.Replay();
            }
            else if (CurrentView is IRoundView rv)
            {
                rv.Replay();
            }
        }

        private void OnBackClicked()
        {
            _stepToken++;
            _app.Speech.Stop();
            ClearCurrentView();
            _app.ShowLessonList();
        }

        /// <summary>Nút "Tiếp" phóng lên, nảy nhẹ rồi nhún chậm mời bé bấm.</summary>
        private async void ShowNextButton()
        {
            var t = NextButton.transform;
            t.localScale = Vector3.one * .4f;
            await Motion.Punch(t, 1.15f, .25f);
            if (NextButton != null && NextButton.gameObject.activeSelf && !_advancing) Pulse.StartOn(t);
        }

        /// <summary>
        /// Sang bước mới như lật trang sách: trang của bước cũ không nhận chạm nữa, lật quanh mép trái rồi bị huỷ; bước
        /// mới được dựng ngay bên dưới. Kèm tiếng lật trang.
        /// </summary>
        private async void TurnCurrentPage()
        {
            if (TurningPage != null) Destroy(TurningPage);
            TurningPage = null;
            var root = CurrentView switch
            {
                IStepView sv => sv.Root,
                IRoundView rv => rv.Root,
                _ => null
            };
            CurrentView = null;
            if (root == null) return;
            if (_app.Sfx != null) _app.Sfx.Play(SystemSfx.PageFlip);
            if (Motion.Scale <= 0f)
            {
                root.SetActive(false);
                Destroy(root);
                return;
            }

            var group = root.GetComponent<CanvasGroup>();
            if (group == null) group = root.AddComponent<CanvasGroup>();
            group.blocksRaycasts = false;
            root.transform.SetAsLastSibling();
            TurningPage = root;
            await Motion.PageTurn((RectTransform)root.transform, PageTurnSeconds);
            if (root != null) Destroy(root);
            if (this != null && TurningPage == root) TurningPage = null;
        }

        private void ClearCurrentView()
        {
            var root = CurrentView switch
            {
                IStepView sv => sv.Root,
                IRoundView rv => rv.Root,
                _ => null
            };
            CurrentView = null;
            if (root != null)
            {
                root.SetActive(false);
                Destroy(root);
            }
        }
    }
}
