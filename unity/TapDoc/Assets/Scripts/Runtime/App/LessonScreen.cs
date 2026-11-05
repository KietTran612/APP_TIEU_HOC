using System;
using TMPro;
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

        /// <summary>Khối phóng to đều của vùng học (nằm trên vùng chứa <c>StageArea</c>).</summary>
        public FitBox StageFit { get; private set; }

        /// <summary>
        /// Bố cục kiểu mép (điện thoại): nút ở hai dải mép, vùng học phóng to. Ngược lại là kiểu góc như máy tính bảng
        /// (bản thiết kế tỷ lệ màn hình mục 5.2).
        /// </summary>
        public bool IsWideLayout { get; private set; }

        /// <summary>Trang của bước trước đang lật đi; <c>null</c> khi không lật.</summary>
        internal GameObject TurningPage { get; private set; }

        private const float Margin = 20f;
        private const float NotesWidth = 260f;
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
            StageFit = _stage.parent.GetComponent<FitBox>();

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
                notesRt.anchoredPosition = new Vector2(-Margin, -Margin);
            }

            // Xoay máy, đổi cỡ cửa sổ: chỉnh bố cục tại chỗ, bước học không dựng lại, giọng đọc không phát lại.
            FrameWatcher.On(gameObject).Changed += ApplyLayout;
            ApplyLayout(((RectTransform)transform).rect.size);

            PresentCurrent(turnPage: false);
        }

        /// <summary>
        /// Đặt vùng học, hàng chấm, gà con và nút Ghi chú theo kiểu góc hay kiểu mép của khung cỡ
        /// <paramref name="size"/>. Nút Về nhà, Loa, Tiếp luôn neo ở góc khung.
        /// </summary>
        private void ApplyLayout(Vector2 size)
        {
            IsWideLayout = ScreenLayout.IsWide(size);
            var area = (RectTransform)_stage.parent;
            if (IsWideLayout)
            {
                area.anchorMin = Vector2.zero;
                area.anchorMax = Vector2.one;
                area.offsetMin = new Vector2(ScreenLayout.SideBand, ScreenLayout.WideBottom);
                area.offsetMax = new Vector2(-ScreenLayout.SideBand, -ScreenLayout.WideTopBand);
            }
            else
            {
                area.anchorMin = area.anchorMax = new Vector2(.5f, .5f);
                area.sizeDelta = ScreenLayout.StageSize;
                area.anchoredPosition = Vector2.zero;
            }
            FitStage();

            ((RectTransform)Dots.transform).anchoredPosition =
                new Vector2(0f, -(IsWideLayout ? ScreenLayout.WideTopBand : UiKit.StageTopInset) / 2f);
            ((RectTransform)Mascot.transform).anchoredPosition = IsWideLayout
                ? new Vector2(-Margin, 2f * Margin + UiKit.MinTouch)
                : new Vector2(-(2f * Margin + UiKit.MinTouch), Margin);
            if (NotesButton != null)
            {
                ((RectTransform)NotesButton.transform).sizeDelta =
                    new Vector2(IsWideLayout ? UiKit.MinTouch : NotesWidth, UiKit.MinTouch);
            }
        }

        /// <summary>
        /// Kiểu góc: vùng học đúng cỡ thiết kế. Kiểu mép: phóng to tối đa mà vẫn vừa cả phần nội dung bước đang hiện vẽ
        /// ra ngoài khung 1400×680 (ví dụ bảng đọc nhiều hàng); bước gọn trong khung thì to hết cỡ. Không bao giờ nhỏ
        /// hơn máy tính bảng (mức 1), để vùng chạm luôn ≥ 160. Chỉ đo bước hiện tại (kể cả phần đang ẩn, sẽ hiện sau),
        /// không đo bước cũ đang chờ huỷ hay trang đang lật.
        /// </summary>
        private void FitStage()
        {
            if (StageFit == null) return;
            if (!IsWideLayout)
            {
                StageFit.Fit();
                return;
            }
            var root = CurrentView switch
            {
                IStepView sv => sv.Root,
                IRoundView rv => rv.Root,
                _ => null
            };
            if (root == null)
            {
                StageFit.Fit();
                return;
            }
            Canvas.ForceUpdateCanvases();
            var bounds = new Rect(-ScreenLayout.StageSize / 2f, ScreenLayout.StageSize);
            var corners = new Vector3[4];
            void Add(Vector3 world)
            {
                var p = (Vector2)_stage.InverseTransformPoint(world);
                bounds = Rect.MinMaxRect(Mathf.Min(bounds.xMin, p.x), Mathf.Min(bounds.yMin, p.y),
                    Mathf.Max(bounds.xMax, p.x), Mathf.Max(bounds.yMax, p.y));
            }
            foreach (var g in root.GetComponentsInChildren<Graphic>(true))
            {
                if (g is TMP_Text text)
                {
                    // Chữ: đo từng ký tự vẽ ra; khung RectTransform của nhãn (ví dụ nhãn dấu thanh) có thể cao hơn nhiều.
                    text.ForceMeshUpdate();
                    var info = text.textInfo;
                    for (var i = 0; i < info.characterCount; i++)
                    {
                        if (!info.characterInfo[i].isVisible) continue;
                        Add(text.transform.TransformPoint(info.characterInfo[i].bottomLeft));
                        Add(text.transform.TransformPoint(info.characterInfo[i].topRight));
                    }
                    continue;
                }
                g.rectTransform.GetWorldCorners(corners);
                foreach (var c in corners) Add(c);
            }
            StageFit.FitBounds(bounds, 1f);
        }

        private static void Corner(Button button, Vector2 corner, Vector2 offset)
        {
            var rt = (RectTransform)button.transform;
            rt.anchorMin = rt.anchorMax = rt.pivot = corner;
            rt.anchoredPosition = offset;
        }

        private void OpenNotes()
        {
            _app.Speech.Stop();
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
                RoundFinished = OnRoundFinished,
                OpenNotes = NotesButton != null ? OpenNotes : null
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
            FitStage();
            // Trang của bước trước đang lật nằm trên bước mới cho tới khi lật qua.
            if (TurningPage != null) TurningPage.transform.SetAsLastSibling();
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

            // Lật một bản sao chỉ để nhìn; bước cũ thật bị huỷ ngay, để việc dở của nó (lời đọc, hiệu ứng) dừng hẳn và
            // không chen vào bước mới.
            GameObject page = null;
            if (Motion.Scale > 0f)
            {
                page = Instantiate(root, root.transform.parent);
                page.name = "TurningPage";
                var paper = page.GetComponent<Image>();
                if (paper == null) paper = page.AddComponent<Image>();
                paper.color = Palette.Paper; // nền giấy che bước mới bên dưới cho tới khi lật qua
                paper.raycastTarget = false;
                var group = page.GetComponent<CanvasGroup>();
                if (group == null) group = page.AddComponent<CanvasGroup>();
                group.blocksRaycasts = false;
                TurningPage = page;
            }
            root.SetActive(false);
            Destroy(root);
            if (page == null) return;

            await Motion.PageTurn((RectTransform)page.transform, PageTurnSeconds);
            if (page != null) Destroy(page);
            if (this != null && TurningPage == page) TurningPage = null;
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
