# Nâng cấp UI đợt 1 — màn học: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Màn học dẫn bé rõ hơn: con đường hạt có đích, gà con "nói" khi có giọng đọc, nhắc khi bé ngồi im theo loại bước, nút của bé to và cách mép, tiếng động nhỏ lại dưới giọng đọc.

**Architecture:** Sửa tại chỗ `ProgressDots` (giữ API `Total/Current/IsBar` mà test cũ dùng). Bộ nhắc là lớp C# thuần `IdleNudge` (đồng hồ truyền vào, test EditMode được), `LessonScreen` cấp dữ liệu và gọi `Tick` mỗi khung hình. Bàn tay `HintHand` và bong bóng nói `TalkBubble` là thành phần UI nhỏ. Dải bên kiểu mép đổi theo tỉ lệ khung qua `ScreenLayout.SideBandFor`.

**Tech Stack:** Unity 6 uGUI dựng bằng code, TMP, Input System (đã tham chiếu trong `TapDoc.Runtime`), NUnit/UnityTest; Python (`tools/tapdoc/ui_icons.py`) cho hình tạm.

**Spec:** [2026-11-17-nang-cap-ui-design.md](../specs/2026-11-17-nang-cap-ui-design.md) mục 4.1, đợt 1, kèm 7 chỉnh sửa của root (17/11).

## Global Constraints

- Màn học chỉ một gà con, ở dải bên (kiểu mép) hoặc góc (kiểu góc); không gà con trên đường hạt.
- Nhắc: bước bấm chọn và mọi lượt Phần 2 — 12 s đọc lại lời dẫn, 24 s bàn tay; bước tự đọc — chỉ bàn tay sau 30 s; tối đa 2 lần mỗi bước; Phần 2 bàn tay chỉ nút Nghe lại, không chỉ đáp án. Ngưỡng là hằng số một chỗ.
- Không nhắc khi giọng đọc đang chạy; chạm bất kỳ thì xoá nhắc.
- Vùng chạm nút của bé chừa ≥ 48 đơn vị tới mép dưới và mép bên của khung bé (`KidRoot`). Khung tỉ lệ ≥ 1,9: nút Tiếp, Nghe lại 180.
- Khung bước học không thu nhỏ quá mức cần cho nút (dải bên kiểu mép: 240 khi tỉ lệ ≥ 1,9, 220 khi khác).
- Tiếng động 0,45; khi giọng đọc đang chạy 0,2.
- Test im lặng; chỉ chạy test màn học + smoke mỗi quyển; xin root lượt Unity.
- Git: main, `git add` đúng đường dẫn, dòng danh mục ảnh qua chỉ mục tạm, không push.

## Review Focus

- Bước Phần 1 đã xong (nút Tiếp đang hiện) ở bước bấm chọn: phải theo nhịp bước tự đọc (30 s, chỉ Tiếp), không đọc lại lời dẫn — test `Nudge_DoneStep_UsesReadTiming` (Task 2).
- Bé bấm Nghe lại ở Phần 2: giọng đọc chạy, bộ đếm phải dừng và tính lại từ khi giọng dừng — test `Nudge_PausesWhileSpeaking` (Task 2).
- Xoay máy hoặc đổi cỡ giữa bước: nút và đường hạt đặt lại đúng chỗ, bàn tay theo nút mới — test `Layout_EdgeGap_AllSizes` chạy sau `ScreenSizes.Apply` (Task 3).
- Bài nhiều bước (> 20) ở khung hẹp nhất: đường liền + bông hoa không đè nút Ghi chú — `Path_FitsTopBand_AllSizes` (Task 1).
- Ôn lại (phiên `ReviewSession`) dùng cùng màn học: nhắc Phần 2 vẫn chạy, không lỗi khi bài không có Phần 1 — có trong `Nudge_Part2_PointsReplay` (Task 4, mở bằng `ShowReview`).

---

### Task 1: Đường hạt có đích (`ProgressDots`)

**Files:**
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/UI/ProgressDots.cs`
- Test: `unity/TapDoc/Assets/Tests/PlayMode/LessonChromeTests.cs` (thêm test; test `Dots_*` cũ giữ nguyên)

**Interfaces:**
- Produces: `ProgressDots.Dot = 32f`, `Gap = 7f`, `CurrentDot = 48f`, `Flower = 40f`, `MaxWidth = 820f`, `WaveAmplitude = 6f`; `Image Goal { get; }` (bông hoa cuối đường, `SystemImages.Flower`); `RectTransform CurrentMarker { get; }` (hạt đang học, hoặc dấu trên đường liền); giữ `Total`, `Current`, `IsBar`, `SetCurrent(int)`.

- [ ] **Step 1: Test** `Path_BeadsAndGoal`: `Create(parent, 10)` → không `IsBar`, 10 hạt, `Goal` khác null và nằm bên phải hạt cuối; `SetCurrent(3)`: `CurrentMarker` cỡ 48, màu cam, hạt 0–2 lam ngọc, hạt 4+ giấy sáng. `Create(parent, 20)` không `IsBar`; `Create(parent, 40)` `IsBar` và vẫn có `Goal`, `CurrentMarker` nằm ở đầu phần tô. `Path_FitsTopBand_AllSizes`: mọi `ScreenSizes`, bài `tv1_t1_b13`, khung `Dots` nằm trong dải trên (không chồng `Stage`) và không chồng `BackButton`, `NotesButton` (nếu có).
- [ ] **Step 2:** chạy, thấy hỏng (`Goal` chưa có).
- [ ] **Step 3:** Hạt xếp theo hàng, toạ độ y lượn `WaveAmplitude * sin(i * .9)`; nét đứt nối hạt (ảnh nhỏ `UiKit.WhiteSprite` mảnh màu `Palette.Ink` giữa hai hạt); hạt đang học to hơn, `Pulse.StartOn(marker, .08f, 1.2f)` khi đổi bước, dừng pulse ở hạt cũ. `rowWidth = n*(Dot+Gap) + Flower`; `IsBar = rowWidth > MaxWidth`. Kiểu đường liền: thanh như cũ cao 28, rộng `MaxWidth - Flower - Gap`, dấu tròn cam 48 ở mép phần tô.
- [ ] **Step 4:** chạy lại `LessonChromeTests`, đạt.
- [ ] **Step 5:** commit (gộp với Task 3 nếu cùng lượt Unity).

### Task 2: Bộ nhắc khi ngồi im (`IdleNudge`, EditMode)

**Files:**
- Create: `unity/TapDoc/Assets/Scripts/Runtime/App/IdleNudge.cs`
- Test: `unity/TapDoc/Assets/Tests/EditMode/IdleNudgeTests.cs`

**Interfaces:**
- Produces:
  - `public enum NudgeKind { None, Tap, Read }`
  - `public sealed class IdleNudge` với `public const float TapRepromptSeconds = 12f, TapHandSeconds = 24f, ReadHandSeconds = 30f; public const int MaxNudges = 2;`
  - `public static readonly IReadOnlyCollection<string> SelfReadTypes` = `sentence, passage, memorize, reading, words, title, question`
  - ctor `IdleNudge(Action reprompt, Action<RectTransform> showHand, Action hideHand)`
  - `void Tick(float now, bool speaking, NudgeKind kind, RectTransform handTarget)`; `void NoteActivity(float now)`; `void ResetStep(float now)`; `int Count { get; }`; `bool HandShown { get; }`
  - Đổi `kind` hoặc `handTarget` (khác tham chiếu) giữa hai lần `Tick` thì tính lại từ `now` (đếm lại `Count`).

- [ ] **Step 1: Test** (đồng hồ là số truyền vào):
  - `Nudge_Tap_RepromptAt12_HandAt24`: Tick(11.9) không gì; Tick(12) gọi reprompt 1 lần; Tick(23.9) chưa tay; Tick(24) showHand(target); Tick(100) không thêm (Count = 2).
  - `Nudge_Read_HandOnlyAt30`: kind Read: Tick(29.9) không; Tick(30) showHand; reprompt không bao giờ gọi.
  - `Nudge_DoneStep_UsesReadTiming`: Tick(5, Tap) rồi Tick(6, Read, next) → mốc tính lại từ 6: Tick(35.9) không, Tick(36) tay chỉ next, không reprompt.
  - `Nudge_PausesWhileSpeaking`: Tick(0..20, speaking: true) không gì; Tick(20, false) rồi Tick(31.9) không, Tick(32) reprompt.
  - `Nudge_ActivityClears`: sau khi tay hiện, NoteActivity(30) → hideHand gọi, Count về 0, Tick(41.9) không, Tick(42) reprompt.
  - `Nudge_NoneKind_DoesNothing` và `handTarget == null` thì không hiện tay (vẫn reprompt với Tap).
- [ ] **Step 2:** chạy EditMode, hỏng (lớp chưa có).
- [ ] **Step 3:** cài `IdleNudge` theo interface.
- [ ] **Step 4:** chạy, đạt.

### Task 3: Nút cách mép, dải bên theo tỉ lệ, gà con nói

**Files:**
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/UI/ScreenLayout.cs` (`SideBandFor`, `WideStageScale` dùng nó)
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/App/LessonScreen.cs` (`ApplyLayout`, vị trí nút, kích thước nút, gà con, `TalkBubble`)
- Create: `unity/TapDoc/Assets/Scripts/Runtime/UI/TalkBubble.cs`
- Modify: `unity/TapDoc/Assets/Tests/EditMode/ScreenLayoutTests.cs` (cập nhật số 1.155/1.086 theo dải 220; thêm `SideBand_ByAspect`)
- Test: `unity/TapDoc/Assets/Tests/PlayMode/LessonChromeTests.cs`

**Interfaces:**
- Produces: `ScreenLayout.SideBandFor(Vector2 frame)` → 240 nếu `frame.x / frame.y >= PhoneAspect (1.9f)`, ngược lại 220; `ScreenLayout.EdgeGap = 48f`; `LessonScreen.KidButtonSize` (180 khi tỉ lệ ≥ 1,9, ngược lại `UiKit.MinTouch`); `TalkBubble.Attach(Mascot mascot, SpeechPlayer speech, AssetCatalog assets)` → bong bóng nhỏ có `SystemIcons.Speaker`, hiện khi `speech.IsBusy` và bong bóng khen của gà con đang ẩn, nhún bằng `SpeakingBob`; `TalkBubble.IsShown`.

- [ ] **Step 1: Test**
  - `SideBand_ByAspect` (EditMode): 2400×1080 → 240; 1920×1080 → 220; `WideStageScale(2400×1080) == (2400-480)/1400`.
  - `Layout_EdgeGap_AllSizes`: mọi `ScreenSizes`: `ReplayButton`, `NextButton` (bật lên) cách mép dưới và mép bên của `KidRoot` ≥ 48; `BackButton` cách mép bên ≥ 48; ở `Phone20x9`, `Phone20x9Camera`, `IPhone`: Tiếp và Nghe lại rộng ≥ 180; phần học không đè nút (test cũ vẫn chạy).
  - `Mascot_TalksWhileSpeaking`: phát `hd_thu_lai`, khung kế tiếp `TalkBubble.IsShown`; `Speech.Stop()` → ẩn; gà con không chồng phần học và nằm trong khung bé ở mọi cỡ.
  - Sửa kỳ vọng cũ ở `Layout_ModeFollowsScreen_AllSizes` không cần: test đó so với `WideStageScale` nên tự theo.
- [ ] **Step 2:** chạy, hỏng.
- [ ] **Step 3:** Kiểu mép: vùng học `offsetMin.x = SideBandFor(size)`; nút góc dưới đặt `(EdgeGap, EdgeGap)` từ góc, nút trên `(EdgeGap, -20)`; cỡ nút `KidButtonSize`; gà con giữa dải bên phải, trên nút Tiếp 20, cỡ `min(SideBandFor - 40, 180)`. Kiểu góc: nút góc dưới `(EdgeGap, EdgeGap)`, nút trên `(EdgeGap, -20)`; vùng học dời lên 10 (`anchoredPosition.y = 10`) để không chồng nút dưới; Ghi chú `(-EdgeGap, -20)`.
- [ ] **Step 4:** chạy `LessonChromeTests`, `ScreenLayoutTests`, đạt; xem ảnh `app_lesson_chrome.png` 4 khung.

### Task 4: Nối bộ nhắc và bàn tay vào màn học

**Files:**
- Create: `unity/TapDoc/Assets/Scripts/Runtime/UI/HintHand.cs`
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/App/LessonScreen.cs` (`Update`, `PresentCurrent`, `OnNextClicked`, `OnReplayClicked`)
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/Content/SystemAssets.cs` (`SystemIcons.PointHand = "img_ui_tay_chi"`)
- Modify: `tools/tapdoc/ui_icons.py` (hình tạm bàn tay chỉ), `tools/tapdoc/system_assets.py` (mô tả), `tools/tests/test_ui_icons.py` (14 → 15)
- Modify: `content/manifests/image_manifest.json` (dòng `img_ui_tay_chi`, qua chỉ mục tạm)
- Test: `unity/TapDoc/Assets/Tests/PlayMode/LessonGuideTests.cs`

**Interfaces:**
- Consumes: `IdleNudge` (Task 2), `LessonScreen.KidButtonSize` (Task 3).
- Produces: `LessonScreen.Nudge` (`IdleNudge`), `LessonScreen.Hand` (`HintHand`), `LessonScreen.NudgeKindNow()` (`NudgeKind`), `LessonScreen.NudgeTargetNow()` (`RectTransform`); `HintHand.Show(RectTransform target)`, `Hide()`, `IsShown`, `Target`. `internal Func<float> LessonScreen.Clock` (mặc định `Time.unscaledTime`) để test đẩy thời gian.
- Luật chọn: Phần 2 → `Tap`, đích `ReplayButton`. Phần 1: nút Tiếp đang hiện → `Read`, đích `NextButton`; loại bước trong `SelfReadTypes` → `Read`, đích null (chưa có gì để chỉ); còn lại → `Tap`, đích là `Selectable`/`Tile`/`DragTile` đầu tiên đang bật trong `Root` của bước, không có thì `Stage`. Reprompt = `OnReplayClicked` + gà con `Cheer(null)` (nhảy, không bong bóng). Chạm màn hình (Input System `Pointer.current.press.wasPressedThisFrame`), bấm Tiếp, bấm Nghe lại → `NoteActivity`.

- [ ] **Step 1: Test** (`Speech.WaitScale = .02f`, `Clock` giả):
  - `Nudge_ReadStep_HandOnNext`: bài `tv1_t1_b13`, hoàn tất bước đầu (`CompleteForTest`), đợi giọng xong; đẩy đồng hồ +29.9 → `Hand.IsShown` false; +30 → true, `Hand.Target == NextButton`; Speech.History không thêm lời dẫn.
  - `Nudge_Part2_PointsReplay`: mở `ShowReview` với một lượt nhầm của `tv1_t1_b13`; đợi giọng xong; +12 → Speech.History thêm lời dẫn lượt; +24 → tay chỉ `ReplayButton`, không chỉ thẻ đáp án.
  - `Nudge_TouchClears`: tay đang hiện, gọi `Nudge.NoteActivity(Clock())` → tay ẩn ngay khung sau.
  - `Hand_FitsAllSizes`: tay hiện ở mọi cỡ nằm trong khung bé, LayoutProbe đạt.
- [ ] **Step 2:** chạy, hỏng.
- [ ] **Step 3:** `HintHand`: `Image` 140×140 `SystemIcons.PointHand`, không nhận chạm, đặt chóp tay ở góc trên phải của đích (lệch vào trong cho khỏi tràn khung bé), `Pulse` nhún; thiếu ảnh thì vẽ vòng tròn cam nhấp nháy quanh đích. Hình tạm bàn tay trong `ui_icons.py` (ngón trỏ chỉ lên trái, nền giấy viền mực), thêm vào `SYSTEM_IMAGES`; chạy `python -m tapdoc ui-icons` (không `--force`).
- [ ] **Step 4:** chạy `LessonGuideTests`, `LessonChromeTests`, `python -m pytest tools/tests/test_ui_icons.py -q`, đạt.

### Task 5: Tiếng động nhỏ lại dưới giọng đọc

**Files:**
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/Audio/SfxPlayer.cs`
- Test: `unity/TapDoc/Assets/Tests/PlayMode/LessonGuideTests.cs`

**Interfaces:**
- Produces: `SfxPlayer.DuckedVolume = .2f`; `float LastVolume { get; }` (âm lượng lần phát gần nhất).

- [ ] **Step 1: Test** `Sfx_DucksUnderSpeech`: `Speech.PlayAsync("hd_thu_lai")` (không chờ) rồi `Sfx.Play(SystemSfx.Correct)` → `LastVolume == .2f`; `Speech.Stop()` rồi phát lại → `.45f`.
- [ ] **Step 2:** hỏng. **Step 3:** `PlayOneShot(clip, vol / DefaultVolume)`. **Step 4:** đạt.

### Task 6: Kiểm cả đợt, ảnh chụp, commit, báo root

- [ ] Xin root lượt Unity. Chạy PlayMode `LessonChromeTests;LessonGuideTests;ReadingStepTests;LessonNotesTests;PrepareFlowTests;Grade2LessonSmokeTests;Grade2Tap2LessonSmokeTests` và smoke một bài mỗi quyển (lọc theo tên bài có sẵn trong `MvpEndToEndTests`/`PrototypeEndToEndTests`), EditMode `IdleNudgeTests;ScreenLayoutTests`. Không có cảnh báo lạ.
- [ ] Xem ảnh `app_lesson_chrome.png` và vài bước bài ở `phone_20x9`, `ipad_43`, `tab_16x10`, `tab_portrait`.
- [ ] Commit theo đường dẫn; dòng `img_ui_tay_chi` qua chỉ mục tạm. Báo root: mã commit, kết quả test, ảnh 4 khung, ghi chú lệch spec (hạt 32/48 thay 40/56 để bài 20 bước vẫn là hạt và không chồng nút Ghi chú).
