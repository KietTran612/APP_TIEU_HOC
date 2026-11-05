# Tỷ lệ màn hình (cách B) — Kế hoạch thực hiện

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** App chạy màn ngang trên điện thoại và máy tính bảng.
- Điện thoại: nút của bé dạt ra hai mép, phần học phóng to.
- Máy tính bảng: giữ như hiện nay.
- Máy tính bảng xoay dọc, cửa sổ hẹp: hiện khung ngang ở giữa.
- Không gì nằm dưới tai thỏ hay thanh vuốt.
- Đổi cỡ màn không làm chạy lại gì.

**Architecture:**
- Một hàm tính thuần (`ScreenLayout.Compute`) đổi cỡ điểm ảnh và lề an toàn của máy ra các khung theo đơn vị canvas:
  - vùng an toàn;
  - khung của bé (rộng hết vùng an toàn khi màn đủ rộng, ngược lại 1440);
  - khung chuẩn 1440 cho màn người lớn.
- `AppRoot` mỗi khung hình tính lại; khi khác thì đặt lại hai gốc `KidRoot` và `SafeRoot`.
- Các màn **không dựng lại** khi đổi cỡ:
  - nhờ neo (anchor) của RectTransform;
  - nhờ `FrameWatcher` (báo khi cỡ đổi) để màn tự chỉnh vài thông số;
  - nhờ `FitBox` (phóng to đều một khối cỡ thiết kế cố định cho vừa chỗ).
- Phần học (`Stage`) và quyển sổ là `FitBox` cỡ 1400×680, nên các bước học bên trong không phải sửa.

**Tech Stack:** Unity 6.6, uGUI dựng bằng code, TMP (Andika), NUnit EditMode/PlayMode, `python tools/run_unity_tests.py`.

**Spec:** `docs/superpowers/specs/2026-11-05-ty-le-man-hinh-design.md`

## Global Constraints

- Màn ngang trên mọi máy; không có bố cục màn dọc riêng.
- Vùng chạm ≥ `UiKit.MinTouch` (160 đơn vị canvas); chữ không tràn; ở mọi cỡ trong `ScreenSizes.All`.
- Mọi vùng chạm và chữ đang hiện nằm trong vùng an toàn (`AppRoot.Frames.Safe`).
- Lề an toàn hai bên lấy **đối xứng** theo bên lớn hơn. Lề trên/dưới lấy đúng từng bên.
- Màn của bé: hồ sơ, danh sách bài, bài học, cảnh học xong bài, Sổ bé ngoan; dựng trong `KidRoot`.
- Màn người lớn: Phụ huynh (gồm cổng phụ huynh), màn chuẩn bị; dựng trong `SafeRoot` (1440). Khung Ghi chú rộng 1440, đặt giữa.
- Đổi cỡ màn: không dựng lại màn, không chạy lại bước học, không phát lại giọng đọc hay lời khen, không mất tiến độ.
- Không đổi phong cách, màu, hình, tiếng; không đổi bố cục bên trong từng bước học; không build bản Android/iOS.
- Chỉ nhánh `main`, commit từng task; chủ dự án tự push.
- Chạy test của task đang làm (`--filter`). Bộ đầy đủ chỉ khi chủ dự án nói "test all" (Task 8 xin lệnh).
- Test cũ gắn số đo 1920/1440 được sửa theo thiết kế mới. Không nới kiểm tra ≥ 160 và chữ không tràn.

## Review Focus

1. **Xoay hoặc đổi cỡ đúng lúc đang kéo thẻ:**
   - Thẻ không biến mất, không kẹt ngoài phần học.
   - Thả vẫn tính theo chỗ ngón tay.
   - Test: `DragTile_ResizeMidDrag_TileStaysInStage` (Task 3).
2. **Đổi cỡ trong lúc cảnh học xong bài đang chạy:**
   - Cảnh nhảy tới cuối, lời khen chỉ phát một lần.
   - Test: `Resize_DuringScene_SkipsToEnd_PraiseOnce` (Task 6).
3. **Màn mở lần đầu ngay sau khi cỡ màn vừa đổi (test đổi `targetTexture` rồi mở màn ngay):**
   - Màn phải dựng theo cỡ mới, không theo cỡ cũ một khung hình.
   - Test: `Present_UsesNewSizeImmediately` (Task 2).
4. **Bài có nút Ghi chú trên điện thoại:**
   - Nút không đè phần học, không tràn chữ.
   - Test: `Notes_Wide_InRightBand_NoOverlap` (Task 4).
5. **Máy tính bảng xoay dọc:**
   - Khung 1080 ở giữa, nền giấy phủ kín.
   - Không có nút nào bám mép trên/dưới của canvas cao 1920.
   - Test: `Portrait_KidRootCentered_ButtonsInsideFrame` (Task 7).

---

### Task 1: Hàm tính khung màn và lề an toàn của máy

**Files:**
- Create: `unity/TapDoc/Assets/Scripts/Runtime/UI/ScreenLayout.cs`
- Create: `unity/TapDoc/Assets/Scripts/Runtime/UI/DeviceSafeArea.cs`
- Test: `unity/TapDoc/Assets/Tests/EditMode/ScreenLayoutTests.cs`

**Interfaces:**
- Produces:
  - `public readonly struct Insets`
    - fields: `float Left, Right, Bottom, Top`
    - constructor: `Insets(float left, float right, float bottom, float top)`
    - `static readonly Insets None`
  - `public readonly struct ScreenFrames`
    - fields: `Vector2 Canvas`; `Rect Safe`; `Rect Kid`; `Rect Standard`; `bool Wide`
    - mọi `Rect` tính bằng đơn vị canvas, gốc ở góc dưới trái canvas
    - `bool Same(ScreenFrames other)`: so từng trường, sai số 0,01
  - `public static class ScreenLayout`
    - `static readonly Vector2 Frame = new(1440f, 1080f)`
    - `static readonly Vector2 StageSize = new(1400f, 680f)`
    - `const float SideBand = 200f`
    - `const float WideTopBand = 70f`
    - `const float WideBottom = 20f`
    - `const float WideMinGain = 1.05f`
    - `static float CanvasScale(Vector2Int pixels)` = `min(px.x/1440, px.y/1080)`
    - `static float WideStageScale(Vector2 frame)` = `min((frame.x − 2·SideBand)/1400, (frame.y − WideTopBand − WideBottom)/680)`
    - `static ScreenFrames Compute(Vector2Int pixels, Insets pixelInsets)`
    - `static bool IsWide(Vector2 frameSize)` = `frameSize.x > 1440.5f`
  - `public static class DeviceSafeArea`
    - `static Func<Vector2Int, Insets> Override` (test gán; `null` = lấy từ hệ điều hành)
    - `static Insets For(Vector2Int pixels)`

- [ ] **Step 1: Viết test hỏng** `ScreenLayoutTests`. Cỡ điểm ảnh và lề tính bằng điểm ảnh; giá trị mong đợi có sai số 0,5:

| Test | Vào | Mong đợi |
|---|---|---|
| `Phone20x9_Wide_FullWidth` | 2400×1080, không lề | Canvas 2400×1080; Kid (0,0,2400,1080); Standard.x 480; Wide |
| `Phone20x9_CameraLeft_SymmetricInsets` | 2400×1080, lề trái 110 | Safe (110,0,2180,1080); Kid.x 110, Kid.width 2180; Standard.x 480; Wide |
| `IPhone_NotchAndHomeBar` | 2556×1179, lề trái 177, phải 177, dưới 63 | Canvas.x 2341.4; Safe (162.1, 57.7, 2017.1, 1022.3); Kid = Safe; Standard.x 450.7; Wide; `WideStageScale(Kid.size)` 1.155 |
| `Phone16x9_JustWide` | 1334×750 | Canvas.x 1921; Wide; `WideStageScale` 1.086 |
| `IPadAir_Corner_HomeBar` | 2360×1640, lề dưới 40 | Canvas.x 1554.1; Kid (57.1, 26.3, 1440, 1053.7); không Wide |
| `IPad43_Corner` | 2048×1536 | Kid (0,0,1440,1080); Kid = Standard; không Wide |
| `Tablet16x10_Corner` | 2560×1600 | Canvas.x 1728; Kid.x 144; không Wide |
| `TabletPortrait_FrameCentered` | 1536×2048 | Canvas (1440,1920); Kid (0,420,1440,1080); không Wide |
| `Fold_FrameCentered` | 2208×1840 | Canvas (1440,1200); Kid (0,60,1440,1080); không Wide |
| `IsWide_Threshold` | — | `IsWide(new(1440,1080))` false; `IsWide(new(1441,1080))` true |
| `SafeArea_OverrideWins` | `DeviceSafeArea.Override = _ => new Insets(1,2,3,4)` | `For(...)` trả đúng 1,2,3,4; TearDown đặt `Override = null` |

- [ ] **Step 2: Chạy, thấy hỏng (chưa có kiểu).**
  `python tools/run_unity_tests.py editmode --filter "ScreenLayoutTests"`

- [ ] **Step 3: Viết `ScreenLayout`, `Insets`, `ScreenFrames`, `DeviceSafeArea`.**
  - `Compute`:
    1. `s = CanvasScale`; canvas = pixels / s; lề chia cho s.
    2. Lề ngang `h = max(L, R)`. `Safe = (h, B, canvas.x − 2h, canvas.y − B − T)`.
    3. Khung cao `fh = min(Safe.height, 1080)`, đặt giữa `Safe` theo chiều dọc.
    4. `Wide = WideStageScale(new(Safe.width, fh)) >= WideMinGain`.
    5. `Kid` rộng `Wide ? Safe.width : min(1440, Safe.width)`; `Standard` rộng `min(1440, Safe.width)`; cả hai đặt giữa `Safe` theo chiều ngang.
  - `DeviceSafeArea.For`:
    - có `Override` thì dùng `Override`;
    - không thì lấy lề từ `Screen.safeArea` so với `Screen.width/height`, quy theo tỷ lệ ra `pixels`, kẹp ≥ 0;
    - `Screen.width ≤ 0` thì `None`. Trong Editor `Screen.safeArea` phủ kín nên ra `None`.

- [ ] **Step 4: Chạy lại, thấy đạt.** Cùng lệnh.

- [ ] **Step 5: Commit**
  `git commit -m "feat(ui): hàm tính khung màn theo cỡ máy và lề an toàn"`

---

### Task 2: Canvas mở rộng, hai gốc màn của AppRoot, kiểm tra vùng an toàn trong test

**Files:**
- Modify: `Scripts/Runtime/UI/UiKit.cs`
  - `Reference` = `ScreenLayout.Frame`;
  - `CreateCanvas` dùng `ScreenMatchMode.Expand`.
- Modify: `Scripts/Runtime/App/AppRoot.cs`
  - `KidRoot`, `SafeRoot`, `Frames`, `RefreshFrames()`, `Update()`;
  - `Present<T>(bool kid = true)`;
  - `ShowParent` dùng `kid: false`.
- Create: `Tests/PlayMode/ScreenSizes.cs` (danh sách cỡ thử, dùng chung)
- Modify: `Tests/PlayMode/LayoutProbe.cs` (thêm kiểm tra vùng an toàn)
- Test: `Tests/PlayMode/ScreenFramesAppTests.cs`

(Các đường dẫn tính từ `unity/TapDoc/Assets/`.)

**Interfaces:**
- Consumes: Task 1.
- Produces:
  - `AppRoot.KidRoot : RectTransform`
  - `AppRoot.SafeRoot : RectTransform` (giờ là khung chuẩn 1440 theo `Frames.Standard`)
  - `AppRoot.Frames : ScreenFrames`
  - `AppRoot.RefreshFrames() : void` (public; tính từ `UiCamera.pixelWidth/pixelHeight` và `DeviceSafeArea.For`; chỉ đặt lại khi `!Frames.Same(mới)`)
  - Cả hai gốc neo góc dưới trái canvas (`anchorMin = anchorMax = pivot = 0`); `anchoredPosition` và `sizeDelta` lấy từ `Rect`.
  - `ScreenSizes.All : IReadOnlyList<ScreenSize>`, với `ScreenSize { string Name; Vector2Int Pixels; Insets Insets; bool Wide; }`, gồm 9 cỡ của Task 1. Tên dùng làm thư mục ảnh chụp: `phone_20x9`, `phone_20x9_cam`, `iphone`, `phone_16x9`, `ipad_air`, `ipad_43`, `tab_16x10`, `tab_portrait`, `fold`.
  - `ScreenSizes.Apply(AppRoot app, ScreenSize size) : RenderTexture`: đặt `DeviceSafeArea.Override`, gán `targetTexture`, gọi `app.RefreshFrames()`.
  - `ScreenSizes.Reset(AppRoot app, RenderTexture rt)`: bỏ `Override`, trả `targetTexture = null`, huỷ rt.
  - `LayoutProbe.AssertFits(Canvas c)`: nếu `c == AppRoot.Instance?.Canvas` thì thêm kiểm tra mọi vùng chạm và chữ đang hiện nằm trong `Frames.Safe` (sai số 0,5; đổi sang toạ độ gốc dưới trái bằng cách cộng nửa cỡ canvas). Vùng trong `ScrollRect` giữ luật cũ (chỉ cần nằm trong khung cuộn).

- [ ] **Step 1: Viết test hỏng** `ScreenFramesAppTests` (dùng `AppTestBase`).
  - `Roots_FollowFrames_AllSizes`: với mỗi `ScreenSizes.All`:
    - `KidRoot` và `SafeRoot` có vị trí và cỡ bằng `Frames.Kid` và `Frames.Standard` (sai số 0,5);
    - nền `Background` phủ đúng cỡ canvas;
    - `Frames.Wide == size.Wide`.
  - `Present_UsesNewSizeImmediately`:
    - đang ở `ipad_43`, đổi sang `phone_20x9` rồi gọi ngay `ShowLessonList()`;
    - cùng khung hình đó, màn mới đã nằm trong `KidRoot` rộng 2400.
  - `ParentScreen_InStandardRoot`: ở `phone_20x9`, mở màn Phụ huynh; màn nằm dưới `SafeRoot` rộng 1440.
  - `RefreshFrames_NoChange_NoRelayout`: gọi `RefreshFrames()` hai lần ở cùng cỡ; biến đếm `AppRoot.FramesApplied` (internal, tăng mỗi lần đặt lại hai gốc) không tăng ở lần thứ hai.

- [ ] **Step 2: Chạy, thấy hỏng.**
  `python tools/run_unity_tests.py playmode --filter "ScreenFramesAppTests"`

- [ ] **Step 3: Sửa code.**
  - `UiKit.CreateCanvas`: `ScreenMatchMode.Expand` với `Reference` 1440×1080.
  - `AppRoot.InitIfNeeded`:
    - tạo `KidRoot` và `SafeRoot` thay cho `UiKit.CreateSafeArea`, gọi `RefreshFrames()`;
    - `Update()` gọi `RefreshFrames()`.
  - `Present` gọi `RefreshFrames()` trước khi dựng màn.
  - `UiKit.CreateSafeArea` giữ nguyên, vì `ViewTestBase` còn dùng.

- [ ] **Step 4: Chạy lại, thấy đạt.**
  Chạy thêm các test đang dùng `SafeRoot` hay `ScreenProbe`, sửa nếu hỏng vì đổi canvas:
  `--filter "ScreenFramesAppTests|PrepareFlowTests|UiInputTests|AppBootTests"`

- [ ] **Step 5: Commit**
  `git commit -m "feat(ui): canvas mở rộng 1440×1080, hai gốc màn theo vùng an toàn của máy"`

---

### Task 3: Khối phóng to đều (FitBox), báo đổi cỡ (FrameWatcher), Stage và kéo thẻ khi bị phóng to

**Files:**
- Create: `Scripts/Runtime/UI/FitBox.cs`
- Create: `Scripts/Runtime/UI/FrameWatcher.cs`
- Modify: `Scripts/Runtime/UI/UiKit.cs` (`CreateStage`)
- Modify: `Scripts/Runtime/UI/DragTile.cs` (`OnDrag`)
- Test: `Tests/PlayMode/FitBoxTests.cs`
- Test: `Tests/PlayMode/UiInputTests.cs` (thêm test kéo trong Stage phóng to)

**Interfaces:**
- Produces:
  - `public class FitBox : MonoBehaviour`
    - nằm trên **vùng chứa** (area), không nằm trên khối;
    - `static RectTransform Create(RectTransform area, string name, Vector2 designSize)`: trả khối con cỡ `designSize`, neo giữa;
    - `RectTransform Content`; `Vector2 DesignSize`; `float Scale`;
    - `void Fit()`: `Scale = min(area.w/design.x, area.h/design.y)`, đặt `Content.localScale`; tự gọi trong `OnRectTransformDimensionsChange` và lúc tạo.
  - `public class FrameWatcher : MonoBehaviour`
    - `static FrameWatcher On(GameObject go)`;
    - `event Action<Vector2> Changed` (chỉ phát khi cỡ đổi quá 0,5);
    - `Vector2 Size`.
  - `UiKit.CreateStage(RectTransform parent)` giữ chữ ký, trả `Stage` cỡ `ScreenLayout.StageSize`:
    - `Stage` là khối của một `FitBox` trên vùng con `StageArea`;
    - `StageArea` co giãn với lề cũ (`StageSideInset`, `StageTopInset`, `StageBottomInset`).

- [ ] **Step 1: Viết test hỏng.**
  - `FitBoxTests.Fit_ScalesUniformly`:
    - vùng 2000×971 chứa khối 1400×680 thì `Scale` ≈ 1,428 (lấy cạnh nhỏ hơn) và `Content.rect.size` vẫn là 1400×680;
    - đổi vùng thành 1400×680 thì `Scale` = 1.
  - `FrameWatcherTests` (cùng file):
    - đổi `sizeDelta` thì `Changed` phát đúng một lần với cỡ mới;
    - gán lại cùng cỡ thì không phát.
  - `UiInputTests.DragTile_FollowsFinger_InScaledStage`:
    - Stage đặt `localScale` 1,4;
    - kéo bằng `PointerEventData` có `delta` (100, 0) điểm ảnh;
    - tâm thẻ trên màn hình (qua `RectTransformUtility.WorldToScreenPoint`) dịch đúng 100 ± 1 điểm ảnh.
  - `UiInputTests.DragTile_ResizeMidDrag_TileStaysInStage`:
    - bắt đầu kéo, đổi `localScale` của Stage từ 1 sang 1,4, kéo tiếp, thả ra ngoài ô;
    - thẻ về đúng `anchoredPosition` cũ, vẫn là con của cha cũ.
  - `UiInputTests.Stage_SameSizeAsLessonScreen`: giữ nguyên (Stage vẫn 1400×680).

- [ ] **Step 2: Chạy, thấy hỏng.**
  `python tools/run_unity_tests.py playmode --filter "FitBoxTests|UiInputTests"`

- [ ] **Step 3: Viết `FitBox`, `FrameWatcher`; đổi `CreateStage`; sửa `DragTile.OnDrag`.**
  `DragTile.OnDrag` đổi `eventData.delta` ra toạ độ của cha thẻ:
  - dùng `RectTransformUtility.ScreenPointToLocalPointInRectangle` cho `position` và `position − delta` trên `_rect.parent`;
  - cộng hiệu hai điểm vào `anchoredPosition`;
  - thay cho chia `canvas.scaleFactor`.

- [ ] **Step 4: Chạy lại, thấy đạt.**
  Thêm các test bước học dùng `ViewTestBase` để chắc Stage mới không đổi gì:
  `--filter "FitBoxTests|UiInputTests|SpellViewTests|RoundViewTests|Part1ViewTests"`

- [ ] **Step 5: Commit**
  `git commit -m "feat(ui): khối phóng to đều cho phần học; kéo thẻ bám ngón tay khi phần học phóng to"`

---

### Task 4: Màn học — kiểu góc và kiểu mép, chỉnh tại chỗ khi đổi cỡ

**Files:**
- Modify: `Scripts/Runtime/App/LessonScreen.cs`
  - `Build` đặt nút theo góc như cũ;
  - thêm `ApplyLayout(Vector2 size)`, `IsWideLayout`, `StageArea`;
  - `FrameWatcher` gọi lại `ApplyLayout`.
- Modify: `Scripts/Runtime/UI/NotesPanel.cs` (gốc khung Ghi chú rộng `UiKit.SafeWidth`, neo giữa, cao hết).
- Test: `Tests/PlayMode/LessonChromeTests.cs` (thêm test; đổi `Mascot_OutsideStageAndButtons_BothSizes` thành chạy qua `ScreenSizes.All`)
- Test: `Tests/PlayMode/LessonNotesTests.cs`

**Interfaces:**
- Consumes: `ScreenLayout.IsWide`, `SideBand`, `WideTopBand`, `WideBottom` (Task 1); `FitBox`, `FrameWatcher`, `UiKit.CreateStage` (Task 3); `ScreenSizes` (Task 2).
- Produces: `LessonScreen.IsWideLayout : bool`; `LessonScreen.StageFit : FitBox`.

Bố cục, tính trên cỡ màn học (= cỡ `KidRoot`):

| | Kiểu góc (`!IsWide`) | Kiểu mép (`IsWide`) |
|---|---|---|
| `StageArea` | neo giữa, `sizeDelta` 1400×680 (`FitBox.Scale` = 1) | co giãn, lề trái/phải `SideBand`, dưới `WideBottom`, trên `WideTopBand` |
| Hàng chấm | `y = −StageTopInset/2` | `y = −WideTopBand/2` |
| Gà con (pivot 1,0) | `(−(2·Margin + MinTouch), Margin)` như cũ | `(−Margin, 2·Margin + MinTouch)`: trên nút Tiếp |
| Nút Ghi chú | 260×160 góc trên phải | 160×160 góc trên phải |

Nút Về nhà, Loa, Tiếp giữ neo góc như cũ ở cả hai kiểu.

- [ ] **Step 1: Viết test hỏng** (`LessonChromeTests`).
  - `Layout_ModeFollowsScreen_AllSizes`: với mỗi `ScreenSizes.All`, mở bài:
    - `IsWideLayout == size.Wide`;
    - kiểu mép: `StageFit.Scale` ≈ `ScreenLayout.WideStageScale(KidRoot.rect.size)` (sai số 0,01), ≥ 1,05;
    - kiểu góc: `StageFit.Scale == 1`;
    - Stage không đè nút Về nhà, Loa, Tiếp, Ghi chú;
    - `LayoutProbe.AssertFits`;
    - lưu ảnh `TestOutput/screens/{size.Name}/app_lesson_chrome.png`.
  - `Mascot_OutsideStageAndButtons_AllSizes`: thay test cũ hai cỡ, cùng các khẳng định cũ.
  - `Resize_MidStep_NoRebuildNoReplay`:
    - mở bài ở `ipad_43`, ghi lại `CurrentView`, `Flow.Position`, số lần phát của `Speech`;
    - đổi sang `phone_20x9`, chờ 2 khung hình;
    - cùng `CurrentView` (cùng tham chiếu), cùng `Flow.Position`, số lần phát không tăng;
    - `IsWideLayout` true; `StageFit.Scale` > 1.
  - `LessonNotesTests.Notes_Wide_InRightBand_NoOverlap`:
    - ở `phone_20x9`, bài có ghi chú;
    - nút Ghi chú 160×160, không đè Stage, không đè gà con;
    - mở khung Ghi chú: gốc khung rộng 1440 và nằm giữa màn (tâm x = tâm `KidRoot`);
    - `LayoutProbe.AssertFits`.

- [ ] **Step 2: Chạy, thấy hỏng.**
  `python tools/run_unity_tests.py playmode --filter "LessonChromeTests|LessonNotesTests"`

- [ ] **Step 3: Viết `ApplyLayout` theo bảng trên; sửa gốc `NotesPanel`.**
  `Build` gọi `ApplyLayout(((RectTransform)transform).rect.size)` một lần sau khi tạo đủ con.

- [ ] **Step 4: Chạy lại, thấy đạt.**
  Thêm các test màn học và hiệu ứng đang có:
  `--filter "LessonChromeTests|LessonNotesTests|LessonFeedbackFxTests|ReadingButtonsTests|RimeGridViewTests"`

- [ ] **Step 5: Commit**
  `git commit -m "feat(ui): màn học trên điện thoại — nút ra hai mép, phần học phóng to; đổi cỡ không chạy lại bước"`

---

### Task 5: Danh sách bài thêm cột trên màn rộng

**Files:**
- Modify: `Scripts/Runtime/App/LessonListScreen.cs`
  - `Columns` thành số cột tính theo cỡ;
  - `FrameWatcher` gọi lại `ApplyColumns`.
- Test: `Tests/PlayMode/LessonListStyleTests.cs` (vòng cỡ chuyển sang `ScreenSizes.All`, thêm test)

**Interfaces:**
- Produces:
  - `internal static int ColumnsFor(float width)` = `max(6, floor((width − 2·Margin + CardGap) / (CardWidth + CardGap)))`;
  - `internal int Columns { get; }`.

- [ ] **Step 1: Viết test hỏng.**
  - `ColumnsFor_Values`: `ColumnsFor(1440)` = 6; `ColumnsFor(2400)` = 10; `ColumnsFor(2017.1f)` = 8.
  - `Columns_FollowFrame_AllSizes`:
    - mỗi cỡ: `Columns == ColumnsFor(KidRoot.rect.width)`;
    - mọi `GridLayoutGroup.constraintCount` của danh sách bằng `Columns`;
    - khung cuộn không đè nút Đổi bé, Sổ, Phụ huynh;
    - `LayoutProbe.AssertFits`; lưu ảnh `{size.Name}/app_lesson_list.png`.
  - `Resize_KeepsScrollPosition`:
    - ở `ipad_43` cuộn tới `verticalNormalizedPosition` 0,5;
    - đổi sang `phone_20x9`;
    - vẫn là cùng `Scroll` (không dựng lại); vị trí cuộn giữ trong khoảng ±0,1 quanh chỗ cũ, tính theo bài đang ở đầu khung.

- [ ] **Step 2: Chạy, thấy hỏng.**
  `--filter "LessonListStyleTests|LessonListScrollTests|LessonListPartsTests"`

- [ ] **Step 3: Viết `ColumnsFor` và `ApplyColumns(float width)`.**
  `ApplyColumns` đặt `constraintCount` cho mọi lưới và độ rộng khung cuộn. Giữ vị trí cuộn: ghi lại bài đang ở đầu khung trước khi đổi, đổi xong cuộn để bài đó lại ở đầu khung.

- [ ] **Step 4: Chạy lại, thấy đạt.** Cùng lệnh.

- [ ] **Step 5: Commit**
  `git commit -m "feat(ui): danh sách bài thêm cột trên màn rộng, giữ chỗ cuộn khi đổi cỡ"`

---

### Task 6: Sổ bé ngoan và cảnh học xong bài phóng to trên màn rộng

**Files:**
- Modify: `Scripts/Runtime/App/BookScreen.cs`
  - `BookArea` thành vùng của một `FitBox` cỡ 1400×680;
  - tiêu đề neo co giãn ngang thay cho `UiKit.SafeWidth`;
  - `FrameWatcher` đặt lề vùng theo kiểu.
- Modify: `Scripts/Runtime/App/ResultScreen.cs`
  - `BookArea` thành `FitBox` như trên; gà con ở kiểu mép như màn học;
  - đổi cỡ khi cảnh đang chạy thì `SkipScene()`;
  - hoa bay hạ cánh đúng cỡ ô.
- Test: `Tests/PlayMode/BookScreenTests.cs`, `Tests/PlayMode/ResultSceneTests.cs` (vòng cỡ chuyển sang `ScreenSizes.All`, thêm test)

**Interfaces:**
- Consumes: `FitBox`, `FrameWatcher` (Task 3); `ScreenLayout.IsWide`, `SideBand` (Task 1).
- Produces:
  - `BookScreen.BookFit : FitBox`; `ResultScreen.BookFit : FitBox`;
  - `ResultScreen.FlowerLandingScale : float` (internal) = `BookFit.Content.lossyScale.x / _overlay.lossyScale.x`.

Lề của vùng sổ (cả hai màn):
- kiểu góc: như cũ (`Margin`, `BottomBand`, `−Margin`, `−TopBand`);
- kiểu mép: trái/phải `SideBand`, dưới `Margin`, trên `TopBand`.

- [ ] **Step 1: Viết test hỏng.**
  - `BookScreenTests.Book_Fits_AllSizes`:
    - mỗi cỡ: `BookFit.Scale` = 1 ở kiểu góc (sai số 0,05; iPad Air có thanh vuốt cho ≈ 0,96), > 1,2 ở `phone_20x9`;
    - quyển sổ không đè nút Về nhà, lật trước, lật sau;
    - tiêu đề không đè nút;
    - `LayoutProbe.AssertFits`; lưu ảnh `{size.Name}/app_book.png`.
  - `BookScreenTests.Resize_KeepsPage`: ở trang 4, đổi `ipad_43` sang `phone_20x9`; `Spread.LeftPage` vẫn là 4, cùng tham chiếu `Spread`.
  - `ResultSceneTests.Result_Fits_AllSizes`: như trên cho cảnh đã xong (`SkipScene`); lưu ảnh `{size.Name}/app_result.png`.
  - `ResultSceneTests.Resize_DuringScene_SkipsToEnd_PraiseOnce`:
    - `Motion.Scale = 1`, mở cảnh;
    - đổi cỡ trước khi cảnh xong; chờ 2 khung hình;
    - `IsSceneDone` true; `khen_hoan_thanh` phát đúng 1 lần (đếm qua lịch sử của `Speech`).
  - `ResultSceneTests.FlowerLands_AtSlotSize_Wide`: ở `phone_20x9`, `FlowerLandingScale` ≈ `BookFit.Scale` (sai số 0,02).

- [ ] **Step 2: Chạy, thấy hỏng.**
  `--filter "BookScreenTests|ResultSceneTests"`

- [ ] **Step 3: Sửa hai màn.**
  `FlyFlower` cho hoa bắt đầu ở `1,6 × FlowerLandingScale` và co về `FlowerLandingScale`. Cánh hoa nhân cùng tỷ lệ.

- [ ] **Step 4: Chạy lại, thấy đạt.** Cùng lệnh.

- [ ] **Step 5: Commit**
  `git commit -m "feat(ui): Sổ bé ngoan và cảnh học xong bài to lên trên màn rộng; đổi cỡ giữa cảnh thì nhảy tới cuối"`

---

### Task 7: Các màn còn lại và chuyển mọi test bố cục sang đủ 9 cỡ

**Files:**
- Modify (chỉ khi test hỏng): `Scripts/Runtime/App/ProfileScreen.cs`, `Scripts/Runtime/App/ParentScreen.cs`, `Scripts/Runtime/UI/PrepareCurtain.cs`
- Test: đổi vòng `new[] { new Vector2Int(2400, 1080), new Vector2Int(2048, 1536) }` thành `ScreenSizes.All` (dùng `Apply`/`Reset`, ảnh lưu `TestOutput/screens/{size.Name}/…`) trong:
  - `AppFlowTests`, `MvpEndToEndTests`, `PrototypeEndToEndTests`;
  - `ParentScreenTests` (2 chỗ), `PrepareFlowTests`, `ProfileScreenTests`.
- Test: `Tests/PlayMode/ScreenFramesAppTests.cs` (thêm)

- [ ] **Step 1: Viết test hỏng.**
  - `Portrait_KidRootCentered_ButtonsInsideFrame`:
    - ở `tab_portrait`, mở lần lượt hồ sơ, danh sách bài, bài học, sổ;
    - mọi `Button` đang hiện nằm trong `Frames.Kid` (y từ 420 đến 1500);
    - không nút nào nằm trong 420 đơn vị trên cùng hay dưới cùng của canvas.
  - `Profile_TypedName_SurvivesResize`:
    - màn tạo bé, gõ "Na", chọn hình đại diện 3;
    - đổi `ipad_43` sang `iphone`;
    - ô nhập vẫn "Na", vẫn chọn hình 3, cùng tham chiếu màn.
  - `ParentGate_SurvivesResize`: mở màn Phụ huynh (cổng khoá), nhập một số; đổi cỡ; câu hỏi và số đã nhập còn nguyên.

- [ ] **Step 2: Đổi các vòng cỡ trong các file test trên sang `ScreenSizes.All`.**
  Chạy:
  `--filter "ScreenFramesAppTests|AppFlowTests|MvpEndToEndTests|PrototypeEndToEndTests|ParentScreenTests|PrepareFlowTests|ProfileScreenTests"`
  Ghi lại test nào hỏng, ở cỡ nào, vì sao (thường gặp: màn chọn bé hay màn Phụ huynh không vừa chiều cao 1022 của iPhone).

- [ ] **Step 3: Sửa từng màn hỏng ở chỗ hẹp nhất.**
  - Ví dụ: đặt nút theo neo thay cho số cứng; cho lưới hồ sơ co hàng.
  - Không thu nhỏ vùng chạm dưới 160, không bỏ kiểm tra.
  - Màn người lớn giữ khung 1440.

- [ ] **Step 4: Chạy lại cùng lệnh, thấy đạt.**

- [ ] **Step 5: Commit**
  `git commit -m "test(ui): mọi test bố cục chạy đủ 9 cỡ máy; sửa các màn chưa vừa"`

---

### Task 8: Ảnh cho chủ dự án, ghi chú, xin "test all"

**Files:**
- Create: `docs/superpowers/notes/2026-11-05-tiep-tuc-ty-le-man-hinh.md`, gồm:
  - đã làm gì, còn gì, các quyết định của người làm;
  - cài đặt nền tảng giữ nguyên theo bản thiết kế mục 5.7: Android khoá ngang, target API tự động; iOS khoá ngang, `UIRequiresFullScreen` bật;
  - nhắc thử trên máy thật khi build.

- [ ] **Step 1: Gom ảnh chụp.**
  Từ `TestOutput/screens/{phone_20x9,iphone,ipad_43,tab_portrait}/`, lấy các màn: học, danh sách, sổ, cảnh xong bài, chọn bé. Gửi chủ dự án xem.

- [ ] **Step 2: Viết ghi chú tiếp tục, commit.**
  `git commit -m "docs: ghi chú tiếp tục — tỷ lệ màn hình"`

- [ ] **Step 3: Xin lệnh "test all".**
  Báo chủ dự án việc đã xong và xin lệnh. Chỉ khi chủ dự án nói "test all" mới chạy:
  `python tools/run_unity_tests.py editmode` rồi `playmode`
  Lỗi thì sửa theo TDD, chạy lại test liên quan, rồi báo kết quả.
