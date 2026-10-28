using System;
using UnityEngine;
using UnityEngine.UI;

namespace TapDoc
{
    public class LessonScreen : MonoBehaviour
    {
        private AppRoot _app;
        private Lesson _lesson;
        private RectTransform _stage;
        private int _stepToken;
        private bool _advancing;

        public LessonFlow Flow { get; private set; }
        public object CurrentView { get; private set; }
        public Button NextButton { get; private set; }
        public Button ReplayButton { get; private set; }
        public Button BackButton { get; private set; }

        public void Build(AppRoot app, Lesson lesson)
        {
            _app = app;
            _lesson = lesson;
            Flow = new LessonFlow(lesson);

            BackButton = UiKit.CreateButton(transform, UiText.Back, OnBackClicked);
            var backRt = BackButton.GetComponent<RectTransform>();
            backRt.anchorMin = new Vector2(0f, 1f);
            backRt.anchorMax = new Vector2(0f, 1f);
            backRt.pivot = new Vector2(0f, 1f);
            backRt.sizeDelta = new Vector2(220f, UiKit.MinTouch);
            backRt.anchoredPosition = new Vector2(20f, -20f);

            ReplayButton = UiKit.CreateButton(transform, UiText.Replay, OnReplayClicked);
            var replayRt = ReplayButton.GetComponent<RectTransform>();
            replayRt.anchorMin = new Vector2(0f, 0f);
            replayRt.anchorMax = new Vector2(0f, 0f);
            replayRt.pivot = new Vector2(0f, 0f);
            replayRt.sizeDelta = new Vector2(260f, UiKit.MinTouch);
            replayRt.anchoredPosition = new Vector2(20f, 20f);

            NextButton = UiKit.CreateButton(transform, UiText.Next, OnNextClicked);
            var nextRt = NextButton.GetComponent<RectTransform>();
            nextRt.anchorMin = new Vector2(1f, 0f);
            nextRt.anchorMax = new Vector2(1f, 0f);
            nextRt.pivot = new Vector2(1f, 0f);
            nextRt.sizeDelta = new Vector2(260f, UiKit.MinTouch);
            nextRt.anchoredPosition = new Vector2(-20f, 20f);
            NextButton.gameObject.SetActive(false);

            _stage = UiKit.CreateStage((RectTransform)transform);

            PresentCurrent();
        }

        private void PresentCurrent()
        {
            _stepToken++;
            var token = _stepToken;
            _advancing = false;

            if (NextButton != null)
            {
                NextButton.gameObject.SetActive(false);
            }

            ClearCurrentView();

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
                Stage = _stage
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
                }
            }
            else if (Flow.Phase == Phase.Part2 && !_advancing)
            {
                // Phần 2 tự chuyển lượt khi màn báo xong (màn chỉ báo sau khi đọc xong lời khen).
                _advancing = true;
                AdvanceFlow();
            }
        }

        private void OnNextClicked()
        {
            if (_advancing || NextButton == null || !NextButton.gameObject.activeSelf)
            {
                return;
            }
            _advancing = true;
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
                PresentCurrent();
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
