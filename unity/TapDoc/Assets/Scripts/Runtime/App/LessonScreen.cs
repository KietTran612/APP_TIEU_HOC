using System;
using System.Linq;
using TMPro;
using UnityEngine;
using UnityEngine.InputSystem;
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

        /// <summary>Mã bài đang học (phiên Ôn lại là mã của phiên).</summary>
        internal string LessonId => _lesson?.lesson_id;
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

        /// <summary>Nhắc khi bé ngồi im (bản thiết kế nâng cấp UI mục 4.1.3).</summary>
        public IdleNudge Nudge { get; private set; }

        /// <summary>Bàn tay gợi ý.</summary>
        public HintHand Hand { get; private set; }

        /// <summary>Bong bóng loa cạnh gà con khi giọng đọc đang chạy.</summary>
        public TalkBubble Talk { get; private set; }

        /// <summary>Cỡ nút Tiếp và Nghe lại: to hơn ở điện thoại dài (mục 4.1.5).</summary>
        public float KidButtonSize { get; private set; } = UiKit.MinTouch;

        /// <summary>Đồng hồ của bộ nhắc (test thay bằng đồng hồ giả).</summary>
        internal Func<float> Clock = () => Time.unscaledTime;

        private const float TargetRefreshSeconds = .25f;
        private const float PhoneKidButton = 180f;
        private RectTransform _nudgeTarget;
        private float _nudgeTargetAt = float.NegativeInfinity;

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

            Dots = ProgressDots.Create(transform, Flow.TotalCount, app.Assets);
            var dotsRt = (RectTransform)Dots.transform;
            dotsRt.anchorMin = dotsRt.anchorMax = new Vector2(.5f, 1f);
            dotsRt.anchoredPosition = new Vector2(0f, -UiKit.StageTopInset / 2f);

            Mascot = Mascot.Create(transform, app.Assets);
            var mascotRt = (RectTransform)Mascot.transform;
            mascotRt.anchorMin = mascotRt.anchorMax = mascotRt.pivot = new Vector2(1f, 0f);
            mascotRt.anchoredPosition = new Vector2(-(2f * Margin + UiKit.MinTouch), Margin);
            Talk = TalkBubble.Attach(Mascot, app.Speech, app.Assets);

            var overlay = new GameObject("FxOverlay", typeof(RectTransform));
            overlay.transform.SetParent(transform, false);
            var overlayRt = (RectTransform)overlay.transform;
            overlayRt.anchorMin = Vector2.zero;
            overlayRt.anchorMax = Vector2.one;
            overlayRt.offsetMin = Vector2.zero;
            overlayRt.offsetMax = Vector2.zero;
            _fx = new LessonFx(overlayRt, app.Assets, app.Sfx, Mascot);
            Hand = HintHand.Create(transform, app.Assets);
            Nudge = new IdleNudge(Reprompt, t => Hand.Show(t), () => Hand.Hide());

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
                var band = ScreenLayout.SideBandFor(size);
                area.offsetMin = new Vector2(band, ScreenLayout.WideBottom);
                area.offsetMax = new Vector2(-band, -ScreenLayout.WideTopBand);
            }
            // Nút của bé chừa ít nhất 48 tới mép dưới và mép bên của màn thật (mục 4.1.5): phần lề an toàn của máy (thanh
            // home, tai thỏ) đã tính vào khoảng chừa. Điện thoại dài: Tiếp, Nghe lại to 180.
            KidButtonSize = IsWideLayout && ScreenLayout.IsPhone(size) ? PhoneKidButton : UiKit.MinTouch;
            var (edgeLeft, edgeRight, edgeBottom) = DistanceToScreenEdges();
            var gapLeft = Mathf.Max(Margin, ScreenLayout.EdgeGap - edgeLeft);
            var gapRight = Mathf.Max(Margin, ScreenLayout.EdgeGap - edgeRight);
            var gapBottom = Mathf.Max(Margin, ScreenLayout.EdgeGap - edgeBottom);
            if (!IsWideLayout)
            {
                area.anchorMin = area.anchorMax = new Vector2(.5f, .5f);
                area.sizeDelta = ScreenLayout.StageSize;
                // Phần học nằm giữa hàng nút trên (lề 20) và hàng nút dưới (chừa tới mép): dời lên bằng nửa phần chênh.
                var bottomNeed = gapBottom + KidButtonSize;
                var topNeed = Margin + UiKit.MinTouch;
                area.anchoredPosition = new Vector2(0f, (bottomNeed - topNeed) / 2f);
            }
            FitStage();

            Corner(BackButton, new Vector2(0f, 1f), new Vector2(gapLeft, -Margin));
            Corner(ReplayButton, Vector2.zero, new Vector2(gapLeft, gapBottom));
            Corner(NextButton, new Vector2(1f, 0f), new Vector2(-gapRight, gapBottom));
            ((RectTransform)ReplayButton.transform).sizeDelta = Vector2.one * KidButtonSize;
            ((RectTransform)NextButton.transform).sizeDelta = Vector2.one * KidButtonSize;

            ((RectTransform)Dots.transform).anchoredPosition = new Vector2(0f, IsWideLayout
                ? -ScreenLayout.WideTopBand / 2f
                : -(size.y / 2f - (area.anchoredPosition.y + ScreenLayout.StageSize.y / 2f)) / 2f);

            // Một gà con duy nhất: giữa dải mép phải, trên nút Tiếp (kiểu mép); bên trái nút Tiếp (kiểu góc).
            var mascotRt = (RectTransform)Mascot.transform;
            if (IsWideLayout)
            {
                var band = ScreenLayout.SideBandFor(size);
                var mascotSize = Mathf.Min(band - 40f, PhoneKidButton);
                mascotRt.sizeDelta = Vector2.one * mascotSize;
                mascotRt.anchoredPosition = new Vector2(-(band - mascotSize) / 2f, gapBottom + KidButtonSize + Margin);
            }
            else
            {
                mascotRt.sizeDelta = Vector2.one * Mascot.DefaultSize;
                mascotRt.anchoredPosition = new Vector2(-(gapRight + KidButtonSize + Margin), gapBottom);
            }
            Talk.SetAbove(IsWideLayout);
            if (NotesButton != null)
            {
                Corner(NotesButton, Vector2.one, new Vector2(-gapRight, -Margin));
                ((RectTransform)NotesButton.transform).sizeDelta =
                    new Vector2(IsWideLayout ? UiKit.MinTouch : NotesWidth, UiKit.MinTouch);
            }
            if (Hand != null && Hand.IsShown) Hand.Show(Hand.Target);
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

        /// <summary>Khoảng từ khung màn học tới mép trái, phải, dưới của màn thật (đơn vị canvas).</summary>
        private (float left, float right, float bottom) DistanceToScreenEdges()
        {
            // Khung bé tính sẵn theo cỡ máy (không phụ thuộc lúc bố cục đã cập nhật hay chưa).
            if (_app != null && _app.Frames.Canvas.x > 0f && transform.parent == _app.KidRoot)
            {
                var kid = _app.Frames.Kid;
                return (Mathf.Max(0f, kid.xMin), Mathf.Max(0f, _app.Frames.Canvas.x - kid.xMax), Mathf.Max(0f, kid.yMin));
            }
            var canvas = GetComponentInParent<Canvas>()?.rootCanvas;
            if (canvas == null) return (0f, 0f, 0f);
            var canvasRt = (RectTransform)canvas.transform;
            var corners = new Vector3[4];
            ((RectTransform)transform).GetWorldCorners(corners);
            Vector2 min = canvasRt.InverseTransformPoint(corners[0]), max = canvasRt.InverseTransformPoint(corners[2]);
            var r = canvasRt.rect;
            return (Mathf.Max(0f, min.x - r.xMin), Mathf.Max(0f, r.xMax - max.x), Mathf.Max(0f, min.y - r.yMin));
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
            Nudge?.ResetStep(Clock());
            _nudgeTargetAt = float.NegativeInfinity;

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
            Nudge?.NoteActivity(Clock());
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
            Nudge?.NoteActivity(Clock());
            ReplayCurrent();
        }

        /// <summary>Bé ngồi im ở bước bấm chọn: gà con nhảy gọi bé và đọc lại lời dẫn của bước.</summary>
        private void Reprompt()
        {
            if (Mascot != null) Mascot.Bounce();
            ReplayCurrent();
        }

        private void Update()
        {
            if (!IdleNudge.Enabled || Nudge == null || Flow == null || Flow.Phase == Phase.Done || _app == null) return;
            var now = Clock();
            var pointer = Pointer.current;
            if (pointer != null && pointer.press.wasPressedThisFrame) Nudge.NoteActivity(now);
            var busy = _app.Speech.IsBusy || _advancing || TurningPage != null
                || (NotesPanel != null && NotesPanel.activeSelf);
            Nudge.Tick(now, busy, NudgeKindNow(), NudgeTargetNow(now));
        }

        /// <summary>
        /// Kiểu nhắc của bước đang học: Phần 2 và bước bấm chọn là <see cref="NudgeKind.Tap"/>; bước tự đọc, hoặc bước
        /// đã xong chỉ còn bấm Tiếp, là <see cref="NudgeKind.Read"/>.
        /// </summary>
        internal NudgeKind NudgeKindNow()
        {
            if (CurrentView == null) return NudgeKind.None;
            if (Flow.Phase == Phase.Part2) return NudgeKind.Tap;
            if (NextButton != null && NextButton.gameObject.activeSelf) return NudgeKind.Read;
            return IdleNudge.SelfReadTypes.Contains(Flow.CurrentStep?.type) ? NudgeKind.Read : NudgeKind.Tap;
        }

        /// <summary>
        /// Chỗ bàn tay chỉ: Phần 2 là nút Nghe lại (không chỉ đáp án); nút Tiếp đang hiện thì chỉ nút Tiếp; bước bấm chọn
        /// chỉ phần tử bấm được đầu tiên của bước (không có thì giữa phần học); bước tự đọc chưa xong thì không chỉ.
        /// </summary>
        internal RectTransform NudgeTargetNow(float now = float.PositiveInfinity)
        {
            if (CurrentView == null) return null;
            if (Flow.Phase == Phase.Part2) return (RectTransform)ReplayButton.transform;
            if (NextButton != null && NextButton.gameObject.activeSelf) return (RectTransform)NextButton.transform;
            if (NudgeKindNow() != NudgeKind.Tap) return null;
            if (_nudgeTarget != null && now - _nudgeTargetAt < TargetRefreshSeconds) return _nudgeTarget;
            _nudgeTargetAt = now;
            var root = CurrentView switch
            {
                IStepView sv => sv.Root,
                IRoundView rv => rv.Root,
                _ => null
            };
            RectTransform found = null;
            if (root != null)
            {
                Component first = root.GetComponentsInChildren<Selectable>().FirstOrDefault(x => x.IsInteractable());
                if (first == null) first = root.GetComponentsInChildren<Tile>().FirstOrDefault();
                if (first == null) first = root.GetComponentsInChildren<DragTile>().FirstOrDefault();
                if (first != null) found = (RectTransform)first.transform;
            }
            _nudgeTarget = found != null ? found : _stage;
            return _nudgeTarget;
        }

        private void ReplayCurrent()
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
