# Giao diện, hiệu ứng, tiếng động và Sổ bé ngoan — Kế hoạch triển khai

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Chủ dự án cho phép tối đa 1 subagent chạy song song. Việc code đơn giản có thể giao Codex/Antigravity qua skill `delegate` (task đánh dấu **[có thể giao]**, hỏi chủ dự án trước khi giao). Claude luôn tự viết test, tự review diff và tự chạy test.

**Mục tiêu:** đổi toàn bộ giao diện sang phong cách tranh SGK 1990 (hướng A). Thêm hiệu ứng, tiếng động CC0, bạn gà con và Sổ bé ngoan (mỗi trang một bài, 3 bông hoa thay 3 ngôi sao).

**Kiến trúc:**
- Giao diện vẫn dựng bằng code.
- Phần dùng chung mới:
  - bảng màu `Palette`;
  - hình khối sinh lúc chạy `UiShapes` (khung bo góc viền mực, hình tròn, nền gạch chéo);
  - bộ chạy hiệu ứng `Motion` (có công tắc tốc độ cho test);
  - kênh tiếng động `SfxPlayer` tách khỏi `SpeechPlayer`.
- Màn học nhận hiệu ứng qua `LessonContext.Fx` (một `LessonFx`), nên luồng chấm đúng sai (`LessonFlow`, `RoundFeedback`) không đổi.
- Sổ bé ngoan:
  - phần tính toán thuần (`FlowerBook`), test được bằng EditMode;
  - một khung hai trang dùng chung (`BookSpread`) cho màn kết thúc bài và màn sổ.
- Biểu tượng, hình hoa tạm và hình gà con là file PNG có mã riêng, do một lệnh Python sinh ra. Sau này thay bằng tranh ChatGPT cùng mã.

**Công nghệ:** Unity 6.6 (`6000.6.5f1`), uGUI và TMP, `Awaitable`; Python 3.14, thư viện chuẩn, `unittest`.

**Bản thiết kế:** [2026-10-30-ui-hieu-ung-design.md](../specs/2026-10-30-ui-hieu-ung-design.md). Executor đọc cả bản thiết kế lẫn kế hoạch này.

## Global Constraints

- Chỉ branch `main`, mỗi task một commit (hoặc vài commit rõ ràng). Không squash, không force push, không push; chủ dự án tự push. Không build Windows/Android.
- Trước khi sửa code chạy `git status`. Không đụng file người khác đang sửa dở (hiện có `docs/superpowers/specs/2026-10-28-app-tap-doc-mvp-design.md` của session gốc: không sửa, không commit).
- Test Unity: `python tools/run_unity_tests.py editmode|playmode` (đóng Unity Editor trước; mỗi lúc chỉ một tiến trình dùng Unity). Test Python: `cd tools && python -m unittest discover -s tests -t .`.
- Bố cục vừa 2400×1080 và 2048×1536: vùng chạm ≥ `UiKit.MinTouch` (160), chữ không tràn (`LayoutProbe.AssertFits`).
- Không viết cứng màu (dùng `Palette`), chữ (dùng `UiText`, thêm vào `UiText.All`), mã tranh/tiếng (dùng `SystemImages`, `SystemIcons`, `SystemSfx`).
- Thiếu file thì app vẫn chạy: thiếu tranh hay biểu tượng thì `AssetCatalog` báo lỗi như hiện nay. Thiếu tiếng động thì chỉ báo **cảnh báo** một lần (`LogWarning`), để test không đỏ khi chưa nhập tiếng.
- Bé chọn sai: không màu đỏ, không dấu X, không tiếng động riêng.
- Tiếng động: âm lượng 0,45; không cắt giọng đọc; chạm làm giọng đọc phát ngay thì không có `sfx_cham` (bản thiết kế 7.2.3b).
- Tranh: ChatGPT Kiet_1 qua Edge trên máy này (kiểm tra `onThisComputer` và brand "Microsoft Edge"). Tải tiếng: chỉ file CC0. Hỏi chủ dự án một lần trước mỗi lô tải. Ảnh sổ bé ngoan chủ dự án gửi không vào repo.
- Test tắt hiệu ứng mặc định (`Motion.Scale = 0` trong lớp cơ sở test). Chỉ test hiệu ứng mới bật lại.

**Quyết định của kế hoạch (khác hoặc chi tiết hơn bản thiết kế):**
- Biểu tượng `img_ui_*`, hoa tạm `img_chung_hoa_be_ngoan` và gà con `img_chung_ga_con` là **file PNG do lệnh `python -m tapdoc ui-icons` sinh ra**. App không tự vẽ hình thay khi thiếu; thiếu thì nút vẫn bấm được, chỉ không có hình. Đây là cách làm của mục "vẽ tạm bằng code" trong bản thiết kế.
- Tiếng động nằm ở `Resources/sfx/`, giữ định dạng gốc (ogg/wav), vì máy không có công cụ chuyển sang mp3. Tiếng động **không** vào `audio_manifest.json` (danh mục đó giả định `.mp3` và là chỗ lệnh `tts` đọc). Danh sách tiếng, nguồn và giấy phép ghi trong `SYSTEM_SFX` của `tools/tapdoc/system_assets.py`. `validate` kiểm tra file và giấy phép. Nhờ vậy `tts` không bao giờ thấy tiếng động.
- Chuyển bước: nội dung cũ bỏ ngay, nội dung mới mờ sang rõ và trượt từ phải vào trong 0,3 giây. Không làm hiệu ứng mờ dần cho nội dung cũ.

## Review Focus

1. **File tiến độ cũ** (không có trường `sfx_off`, bài đã học có `stars` = 3): tiếng động bật, mỗi bài đã học hiện đủ 3 hoa ở danh sách và trong sổ.
   - Test: `ProgressStoreTests.OldFile_SfxOnAndFlowersKept` (Task 4).
2. **Bấm dồn khi hiệu ứng đang chạy** (bấm "Tiếp" hai lần, chạm thẻ liên tục): không chuyển bước hai lần; thẻ luôn về đúng cỡ 1.
   - Test: `MotionTests.NewAnimation_CancelsOld_EndsExact` (Task 3).
   - Test: `LessonChromeTests.NextTwice_AdvancesOnce` (Task 5).
3. **Rời màn giữa lúc hiệu ứng chạy** (bấm nhà khi hoa đang bay, đổi bước khi sao giấy đang bung): không có lỗi `MissingReferenceException`.
   - Test: `ResultSceneTests.LeaveMidScene_NoErrors` (Task 9).
   - Test: `LessonFeedbackFxTests.AdvanceWhileSparks_NoErrors` (Task 6).
4. **Chữ dài trên trang sổ và tiêu đề sổ:**
   - tên bài 6 "Dấu hỏi - Dấu ngã - Dấu nặng";
   - tên bé 20 kí tự.

   Chữ không tràn ở cả hai khung hình.
   - Test: `BookScreenTests.LongTitles_Fit` (Task 8).
5. **Bé đang học bài ở xa cuối danh sách** (ví dụ bài 70): mở danh sách thì thẻ bài đang học nằm trong vùng nhìn; mở sổ thì vào đúng trang của bài học xong sau cùng.
   - Test: `LessonListStyleTests.CurrentLesson_ScrolledIntoView` (Task 10).
   - Test: `FlowerBookTests.StartPage_LastCompletedInListOrder` (Task 7).

---

## Giai đoạn A — Nền móng

### Task 1: Tài nguyên hệ thống mới và lệnh `ui-icons` [có thể giao]

**Files:**
- Modify: `tools/tapdoc/system_assets.py` (thêm mục vào `SYSTEM_IMAGES`, thêm `SYSTEM_SFX`)
- Create: `tools/tapdoc/ui_icons.py`
- Modify: `tools/tapdoc/__main__.py` (lệnh `ui-icons`)
- Modify: `tools/tapdoc/validate.py` (kiểm tra tiếng động)
- Test: `tools/tests/test_ui_icons.py`, `tools/tests/test_validate.py`

**Interfaces:**
- Produces (Python):
  - `SYSTEM_IMAGES` có thêm:
    - `img_chung_hoa_be_ngoan`, `img_chung_ga_con`;
    - 12 biểu tượng: `img_ui_nha`, `img_ui_loa`, `img_ui_tiep`, `img_ui_lui`, `img_ui_so`, `img_ui_on_lai`, `img_ui_xong`, `img_ui_khoa`, `img_ui_trang_truoc`, `img_ui_trang_sau`, `img_ui_sao_giay`, `img_ui_canh_hoa`.

    Mỗi mã có mô tả để vẽ lại bằng ChatGPT sau này.
  - `SYSTEM_SFX: dict[str, dict]`: mã → `{"mo_ta", "nguon", "giay_phep"}`. Có 6 mã: `sfx_cham`, `sfx_dung`, `sfx_nhap`, `sfx_hoa_bay`, `sfx_dong_dau`, `sfx_lat_trang`. Ban đầu `nguon`, `giay_phep` rỗng.
  - `ui_icons.ICONS: dict[str, list]`: mã → danh sách nét vẽ trong khung 24×24, theo các hình ở bản mẫu `phong-cach-man-hoc.html`.
  - `ui_icons.render(shapes, size: int) -> bytes`: trả về PNG RGBA.
  - `ui_icons.write_all(image_dir: Path, force: bool = False) -> list[str]`: trả về các mã đã ghi. Hàm này:
    - ghi các file `img_ui_*.png` còn thiếu;
    - ghi `img_chung_hoa_be_ngoan.png` (hoa tạm) nếu thiếu;
    - chép `img_chung_avatar_04.png` thành `img_chung_ga_con.png` nếu thiếu.

    `force` ghi đè các biểu tượng, nhưng **không bao giờ** ghi đè hoa và gà con.
  - `validate.check_sfx(res_dir, allow_missing) -> list[Issue]`: với mỗi mã trong `SYSTEM_SFX`:
    - có đúng một file `sfx/<mã>.(ogg|wav|mp3)`;
    - nếu có file thì `giay_phep == "CC0"`.

    `allow_missing` bỏ qua lỗi thiếu file.

- [ ] **Step 1: Viết test hỏng**

```python
class RenderTest(unittest.TestCase):
    def test_png_signature_and_size(self):
        png = ui_icons.render(ui_icons.ICONS["img_ui_nha"], 64)
        self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
        w, h = struct.unpack(">II", png[16:24])
        self.assertEqual((w, h), (64, 64))
    def test_every_icon_has_ink_and_transparent_corner(self):
        for icon_id, shapes in ui_icons.ICONS.items():
            px = decode_rgba(ui_icons.render(shapes, 48))  # hàm giải nén trong test, dùng zlib
            self.assertEqual(px[0][0][3], 0, icon_id)               # góc trong suốt
            self.assertTrue(any(a > 200 for row in px for (*_, a) in row), icon_id)
    def test_ids_match_system_images(self):
        self.assertTrue(set(ui_icons.ICONS) <= set(SYSTEM_IMAGES))
        self.assertEqual(len(ui_icons.ICONS), 12)

class WriteAllTest(unittest.TestCase):
    # thư mục tạm có sẵn img_chung_avatar_04.png giả
    def test_writes_missing_copies_mascot(self): ...   # 12 icon + hoa + gà con; gà con giống hệt avatar_04
    def test_force_never_overwrites_flower_or_mascot(self): ...  # ghi chữ "x" vào 2 file đó, write_all(force=True), vẫn là "x"
    def test_keeps_existing_icon_without_force(self): ...

class SfxCheckTest(unittest.TestCase):
    def test_missing_file_reported_unless_allowed(self): ...
    def test_non_cc0_reported(self): ...      # file có, giay_phep "CC-BY" → lỗi
    def test_two_formats_same_id_reported(self): ...
```

- [ ] **Step 2: Chạy, thấy đỏ:** `cd tools && python -m unittest tests.test_ui_icons tests.test_validate -v`. Kết quả mong đợi: lỗi import `ui_icons` và `check_sfx`.
- [ ] **Step 3: Viết code**
  - Bộ vẽ chỉ dùng thư viện chuẩn: `zlib`, `struct`, lấy mẫu 4×4 trong mỗi điểm ảnh để viền mịn.
  - Có ba loại nét:
    - `("fill", points, color)`;
    - `("stroke", points, width, color, closed)`;
    - `("circle", cx, cy, r, fill, stroke_width)`.
  - Màu lấy theo bảng màu của bản thiết kế 4.1.
  - Lệnh `python -m tapdoc ui-icons [--force]` gọi `write_all(UNITY_RES / "images")` và in các mã đã ghi.
  - `validate_all` gọi `check_sfx(UNITY_RES, allow_missing)`.
- [ ] **Step 4: Chạy, thấy xanh:** chạy lại lệnh ở Step 2, rồi chạy cả bộ test Python.
- [ ] **Step 5: Sinh file thật và cập nhật danh mục:**
  - `cd tools && python -m tapdoc ui-icons`;
  - `python -m tapdoc build` (danh mục tranh có thêm 14 dòng);
  - `python -m tapdoc validate --allow-missing` ra `OK`.

  Mở vài PNG xem bằng mắt: nét mực rõ, nằm giữa khung.
- [ ] **Step 6: Commit** các file Python, test, 14 PNG mới và `content/manifests/image_manifest.json`. Lời commit: `feat(tools): biểu tượng giao diện, hoa tạm, gà con và danh sách tiếng động`.

### Task 2: Bảng màu, hình khối và bộ tạo nút/thẻ kiểu mới

**Files:**
- Create: `unity/TapDoc/Assets/Scripts/Runtime/UI/Palette.cs`, `UI/UiShapes.cs`, `UI/IconButton.cs`
- Modify: `UI/UiKit.cs`, `UI/Tile.cs`, `Content/SystemAssets.cs`, `Content/AssetCatalog.cs`, `Text/UiText.cs`, `App/AppRoot.cs` (màu nền, màu camera lấy từ `Palette.Paper`)
- Modify (test): `Tests/PlayMode/ViewTestBase.cs` (`ButtonWithText` tìm cả theo tên `Button_<nhãn>`), `Tests/PlayMode/AppTestBase.cs` (`UseStubsForMissingAssets` có thêm loader tiếng động)
- Test: `Tests/EditMode/UiStyleTests.cs`

**Interfaces:**
- Produces:
  - `Palette`: các màu `Ink`, `Paper`, `PaperLight`, `Teal`, `TealLight`, `Orange`, `OrangeLight`, `HintYellow`, `StampRed`, `LockedFill`, `LockedInk` (giá trị ở bản thiết kế 4.1), và `static Color Hex(string)`.
  - `UiShapes`:
    - `internal static Sprite Rounded` (khung bo góc trắng, 9 mảnh, bán kính 16);
    - `Circle`;
    - `Hatch` (vân gạch chéo màu mực, lặp được).
  - Hằng số của `UiKit`: `BorderWidth = 3f`, `ShadowOffset = new Vector2(10f, -10f)`.
  - `UiKit.CreateTile` vẫn giữ chữ kí cũ.
    - Gốc là `Image` màu `Ink` (nhận chạm).
    - Con `Fill` là `Image` thụt vào `BorderWidth`; đây là chỗ `Tile` đổi màu.
    - Thêm `TapFeedback` (Task 3; Task 2 chỉ chừa chỗ gắn).
  - `UiKit.CreateButton(Transform, string, Action)` là **nút của người lớn**:
    - bo góc, viền mực, nền `Teal`, chữ trắng;
    - tên GameObject `Button_<nhãn>` như cũ;
    - không còn đổi màu riêng cho `UiText.Next`.
  - `UiKit.CreateIconButton(Transform parent, AssetCatalog assets, string iconId, string label, Action onClick, Color? fill = null) -> Button`:
    - nút tròn 160×160, viền mực, nền `fill ?? Palette.Teal`;
    - con `Icon` là `Image` chiếm 58%, `preserveAspect`;
    - **không có chữ TMP**;
    - tên `Button_<label>`;
    - có component `IconButton { string IconId; string Label; }`.
  - `UiKit.CreateCardButton(Transform parent, string label, Action onClick) -> Button`: thẻ to nền `PaperLight`, chữ màu mực, có bóng gạch chéo. Dùng cho thẻ bé và thẻ bài.
  - `UiKit.AddHatchShadow(RectTransform target) -> GameObject`: tạo bóng là anh em đứng ngay trước `target`, lệch `ShadowOffset`, cùng cỡ, không nhận chạm.
  - Màu của `Tile`:
    - thường: `PaperLight`;
    - đang đọc tới (`SetHighlighted(true)`): `OrangeLight`;
    - gợi ý (`SetHint(true)`): `HintYellow`.
  - `SystemImages.Flower = "img_chung_hoa_be_ngoan"`, `SystemImages.Mascot = "img_chung_ga_con"`. Cả hai có trong `SystemImages.All`.
  - `SystemIcons`: 12 hằng `Home`, `Speaker`, `Forward`, `Backward`, `Book`, `Review`, `Check`, `Lock`, `PagePrev`, `PageNext`, `PaperStar`, `Petal` (mã như Task 1) và mảng `All`. Các mã này cũng nằm trong `SystemImages.All`, để `DataTests.AllReferencedAssetsExist` kiểm tra file.
  - `SystemSfx`: `Tap = "sfx_cham"`, `Correct = "sfx_dung"`, `Merge = "sfx_nhap"`, `FlowerFly = "sfx_hoa_bay"`, `Stamp = "sfx_dong_dau"`, `PageFlip = "sfx_lat_trang"`, và `All`.
  - `AssetCatalog`:
    - hàm khởi tạo thêm tham số cuối `Func<string, AudioClip> sfxLoader = null`, mặc định là `Resources.Load<AudioClip>($"sfx/{id}")`;
    - thêm `public AudioClip Sfx(string id)`: thiếu file thì `LogWarning("[TapDoc] Thiếu tiếng động: " + id)`, mỗi mã một lần.
  - `UiText` thêm và đưa vào `All`:
    - `Book = "Sổ bé ngoan"`, `BookTitleFormat = "Sổ bé ngoan của {0}"`, `BookPageFormat = "{0} {1} · {2}"`;
    - `StampText = "BÉ NGOAN"`, `MascotCorrect = "Đúng rồi!"`, `MascotLessonDone = "Bé ngoan quá!"`;
    - `SfxOn = "Tiếng động: Bật"`, `SfxOff = "Tiếng động: Tắt"`.

- [ ] **Step 1: Viết test hỏng** `UiStyleTests` (EditMode, tạo canvas tạm):
  - `IconButton_IsRoundWithIconAndNoText`: tên `Button_Về`; `GetComponentsInChildren<TMP_Text>()` rỗng; `IconButton.IconId == SystemIcons.Home`; cỡ 160×160.
  - `Tile_FillColors_FollowPalette`: lần lượt `PaperLight`, `OrangeLight` khi đang đọc tới, `HintYellow` khi gợi ý; gốc của thẻ màu `Palette.Ink`.
  - `AdultButton_TealWithWhiteText`.
  - `Catalog_MissingSfx_WarnsOnce`: `LogAssert.Expect(LogType.Warning, "[TapDoc] Thiếu tiếng động: khong_co")` một lần cho hai lần gọi, và không có lỗi.
  - `SystemIcons_AllInSystemImages`.
- [ ] **Step 2: Chạy, thấy đỏ:** `python tools/run_unity_tests.py editmode --filter TapDoc.Tests.UiStyleTests` báo lỗi biên dịch hoặc FAIL.
- [ ] **Step 3: Viết code** theo Interfaces.
  - Sprite của `UiShapes` sinh một lần rồi giữ lại, theo cách làm của `MarkerIcon.FallbackStar`.
  - Bóng gạch chéo: [Builder] chọn cách, ví dụ `Mask` hình bo góc chứa `Image` lặp vân `Hatch`.
- [ ] **Step 4: Chạy, thấy xanh:** chạy lại test ở Step 2, rồi chạy cả EditMode. `DataTests.FontCoversAllDisplayText` phải xanh với chữ mới; `AllReferencedAssetsExist` xanh nhờ PNG của Task 1.
- [ ] **Step 5: Chạy PlayMode đầy đủ:** `python tools/run_unity_tests.py playmode`. Chỉ được đỏ ở test kiểm tra ngôi sao (sẽ sửa ở Task 9–10); ghi lại tên các test đó.
- [ ] **Step 6: Commit** cả code, test và file `.meta` Unity sinh cho PNG. Lời commit: `feat(ui): bảng màu, khung viền mực, nút biểu tượng`.

### Task 3: Bộ chạy hiệu ứng `Motion` [có thể giao]

**Files:**
- Create: `Scripts/Runtime/UI/Motion.cs`, `UI/Pulse.cs`, `UI/TapFeedback.cs`
- Modify: `UI/UiKit.cs` (gắn `TapFeedback` cho thẻ và nút)
- Modify (test): `Tests/PlayMode/AppTestBase.cs`, `Tests/PlayMode/ViewTestBase.cs`. Trong `[SetUp]` đặt `Motion.Scale = 0f`; trong `[TearDown]` trả lại `1f`.
- Test: `Tests/PlayMode/MotionTests.cs`

**Interfaces:**
- Produces:
  - `public static class Motion`:
    - `public static float Scale = 1f;` Số này nhân vào mọi thời lượng. Bằng 0 thì hiệu ứng nhảy ngay tới trạng thái cuối, trong cùng khung hình.
    - Các hàm, đều trả về `Awaitable`:
      - `ScaleTo(Transform t, float to, float seconds)`;
      - `Punch(Transform t, float peak, float seconds)` (lên `peak` rồi về 1);
      - `Shake(RectTransform t, float amplitude, float seconds)` (lắc ngang, về đúng chỗ cũ);
      - `MoveTo(RectTransform t, Vector2 anchored, float seconds)`;
      - `Fade(CanvasGroup g, float to, float seconds)`;
      - `Wiggle(Transform t, float degrees, float seconds)` (xoay qua lại, về 0).
    - Mỗi đối tượng có 4 kênh riêng: cỡ, vị trí, độ trong, góc xoay. Hiệu ứng mới trên cùng kênh thì huỷ hiệu ứng cũ.
    - Đối tượng bị huỷ giữa chừng thì hàm thoát êm, không ném lỗi.
  - `Pulse` (MonoBehaviour):
    - `static Pulse Start(Transform t, float amplitude = .06f, float period = 1.6f)`;
    - `static void Stop(Transform t)` (trả cỡ về 1);
    - `static bool IsRunning(Transform t)`.
    - Khi `Motion.Scale == 0` thì vẫn ghi nhận là đang chạy nhưng không đổi cỡ, để ảnh chụp ổn định.
  - `TapFeedback` (MonoBehaviour, `IPointerDownHandler`, `IPointerUpHandler`):
    - nhấn: `ScaleTo(.92f, .06f)`; thả: `ScaleTo(1f, .09f)`;
    - `public string Sound` (mặc định `null`): khác `null` thì khi nhấn gọi `SfxPlayer.Instance?.Play(Sound)` (Task 4).

- [ ] **Step 1: Viết test hỏng** `MotionTests`:
  - `ScaleZero_JumpsToEnd`: `Scale = 0`; `await Motion.MoveTo(rt, (100, 0), 1)` xong trong cùng khung hình, `anchoredPosition == (100, 0)`.
  - `Punch_ReturnsToOne`: `Scale = 1`; sau `Punch(t, 1.2f, .1f)` thì `localScale == Vector3.one` (sai số 1e-4).
  - `NewAnimation_CancelsOld_EndsExact` (Review Focus 2): chạy `ScaleTo(t, 1.5f, .3f)`; sau 0,05 giây chạy `ScaleTo(t, 1f, .05f)`; chờ 0,4 giây thì cỡ đúng bằng 1.
  - `Shake_EndsAtStart`.
  - `DestroyedTarget_NoException`: huỷ đối tượng giữa lúc `MoveTo`; `LogAssert.NoUnexpectedReceived()`.
  - `Pulse_StopRestoresScale`.
  - `TapFeedback_PressShrinks_ReleaseRestores`: giả `OnPointerDown`/`OnPointerUp` với `PointerEventData`.
- [ ] **Step 2: Chạy, thấy đỏ:** `python tools/run_unity_tests.py playmode --filter TapDoc.Tests.MotionTests`.
- [ ] **Step 3: Viết code** theo Interfaces.
  - Dùng `Time.unscaledDeltaTime`. Đường cong dùng ease-out.
  - Huỷ theo kênh bằng số thế hệ lưu trong một component ẩn `MotionState` trên đối tượng.
- [ ] **Step 4: Chạy, thấy xanh:** test ở Step 2, rồi cả PlayMode. Mọi test cũ vẫn xanh, trừ các test sao đã ghi ở Task 2.
- [ ] **Step 5: Commit:** `feat(ui): bộ chạy hiệu ứng Motion, nhún khi chạm`.

### Task 4: Kênh tiếng động, công tắc lưu trong tiến độ, khoảng nghỉ của chuỗi đọc [có thể giao]

**Files:**
- Create: `Scripts/Runtime/Audio/SfxPlayer.cs`
- Modify: `Audio/SpeechPlayer.cs` (`onGap`), `Progress/ProgressData.cs`, `Progress/ProgressStore.cs`, `App/AppRoot.cs` (tạo `Sfx`), `Scripts/Editor/ContentImportRules.cs` (luật nhập cho `Resources/sfx`)
- Test: `Tests/PlayMode/SfxPlayerTests.cs`, thêm vào `Tests/EditMode/ProgressStoreTests.cs` và `Tests/PlayMode/SpeechPlayerTests.cs`

**Interfaces:**
- Produces:
  - `ProgressFile.sfx_off` (`bool`, mặc định `false`).
  - `ProgressStore.SfxEnabled { get; set; }`: bằng `!sfx_off`. Đây là cài đặt cho cả máy, không theo từng bé.
  - `public class SfxPlayer : MonoBehaviour`:
    - `const float DefaultVolume = .45f`;
    - `static SfxPlayer Instance`;
    - `bool Enabled`;
    - `IReadOnlyList<string> History` (mã đã được phép phát, kể cả khi thiếu file);
    - `void Init(AssetCatalog catalog, SpeechPlayer speech)`;
    - `void Play(string id)`: bỏ qua khi `!Enabled`; dùng `AudioSource` riêng và `PlayOneShot`;
    - `void PlayUnlessSpeaking(string id)`: bỏ qua thêm khi `speech.IsBusy`.
  - `AppRoot.Sfx` (`SfxPlayer`): tạo sau `Speech`; `Enabled = Progress.SfxEnabled`.
  - `SpeechPlayer.PlaySequenceAsync(IReadOnlyList<string> ids, Action<int> onPart = null, float gap = SequenceTimeline.DefaultGap, Action<int> onGap = null)`: gọi `onGap(i + 1)` khi bắt đầu khoảng nghỉ trước mảnh `i + 1`. Không gọi khi `gap <= 0` hoặc khi chuỗi bị cắt.

- [ ] **Step 1: Viết test hỏng:**
  - `ProgressStoreTests.SfxEnabled_DefaultOn_PersistsOff`: lưu rồi nạp lại thì vẫn tắt.
  - `ProgressStoreTests.OldFile_SfxOnAndFlowersKept` (Review Focus 1): JSON cũ không có `sfx_off`, có bài `completed: true, stars: 3`. Kết quả: `SfxEnabled == true` và `StarsFor(...) == 3`.
  - `SfxPlayerTests.Disabled_PlaysNothing`: `History` rỗng.
  - `SfxPlayerTests.PlayUnlessSpeaking_SkipsWhileBusy`: phát một clip dài bằng `SpeechPlayer`, gọi `PlayUnlessSpeaking(Tap)`; `History` không có `sfx_cham`.
  - `SfxPlayerTests.DoesNotInterruptSpeech`: đang đọc thì `Play(Correct)`; `Speech.IsBusy` vẫn `true`, và clip của `Speech` vẫn đang phát.
  - `SfxPlayerTests.MissingClip_WarningOnly`.
  - `SpeechPlayerTests.OnGap_CalledBeforeNextPart`: ba mã, `gap = .1f`; `onGap` được gọi với 1 rồi 2, mỗi lần đều trước `onPart` của mảnh đó.
- [ ] **Step 2: Chạy, thấy đỏ** (EditMode và PlayMode, lọc theo tên lớp).
- [ ] **Step 3: Viết code** theo Interfaces. Luật nhập cho `Resources/sfx`: âm thanh mono, `DecompressOnLoad`, giống luật của `audio`.
- [ ] **Step 4: Chạy, thấy xanh:** cả EditMode và PlayMode.
- [ ] **Step 5: Commit:** `feat(audio): kênh tiếng động riêng, công tắc lưu trong tiến độ`.

## Giai đoạn B — Màn học

### Task 5: Khung màn học: nút biểu tượng, chấm tiến độ, gà con, chuyển bước

**Files:**
- Create: `Scripts/Runtime/UI/ProgressDots.cs`, `UI/Mascot.cs`, `App/LessonFx.cs`
- Modify: `App/LessonScreen.cs`, `App/LessonContext.cs`, `App/AppRoot.cs` (màn mới mờ sang rõ 0,25 giây trong `Present<T>`)
- Test: `Tests/PlayMode/LessonChromeTests.cs`

**Interfaces:**
- Consumes: `UiKit.CreateIconButton`, `SystemIcons` (Task 2); `Motion`, `Pulse` (Task 3); `AppRoot.Sfx` (Task 4).
- Produces:
  - `ProgressDots` (MonoBehaviour):
    - `const float Dot = 26f, Gap = 12f, MaxWidth = 880f`;
    - `static ProgressDots Create(Transform parent, int total)`;
    - `void SetCurrent(int index)`: chấm trước `index` màu `Teal`, chấm `index` màu `Orange`, chấm sau màu `PaperLight`;
    - `int Total`, `int Current`;
    - `bool IsBar`: đúng khi `total * (Dot + Gap) - Gap > MaxWidth`. Khi đó vẽ thanh liền, tô màu tới vị trí hiện tại.
  - `Mascot` (MonoBehaviour, không nhận chạm):
    - `static Mascot Create(Transform parent, AssetCatalog assets, float size = 150f)`;
    - `void Cheer(string bubble)`: nhảy 2 nhịp, bong bóng hiện 1,5 giây;
    - `void Ponder()`: nghiêng 12° trong 0,6 giây;
    - `MascotMood LastMood` (`None`, `Cheer`, `Ponder`);
    - `string BubbleText` (chuỗi rỗng khi bong bóng ẩn).
  - `LessonFx` (lớp thường):
    - `LessonFx(RectTransform overlay, AssetCatalog assets, SfxPlayer sfx, Mascot mascot)`;
    - `void Correct(RectTransform at)`: 5 sao giấy (`SystemIcons.PaperStar`) bung ra từ `at` rồi mờ đi, `sfx.Play(SystemSfx.Correct)`, `mascot.Cheer(UiText.MascotCorrect)`;
    - `void Wrong(RectTransform chosen)`: `Motion.Shake(chosen, 18f, .3f)`, `mascot.Ponder()`, không có tiếng;
    - `void Merge()`: `sfx.Play(SystemSfx.Merge)`;
    - `int ActiveSparks` (cho test).

    Hàm nào cũng an toàn khi `sfx` hay `mascot` là `null`.
  - `LessonContext.Fx` (`LessonFx`, `null` trong test màn).
  - `LessonScreen`:
    - `BackButton` = `CreateIconButton(Home, UiText.Back)`;
    - `ReplayButton` = `CreateIconButton(Speaker, UiText.Replay)`, nhún theo nhịp khi `Speech.IsBusy`;
    - `NextButton` = `CreateIconButton(Forward, UiText.Next, fill: Palette.Orange)`, `TapFeedback.Sound = SystemSfx.Tap`. Khi hiện thì `Punch` 1,15 rồi `Pulse.Start`;
    - `NotesButton` giữ là nút của người lớn;
    - thêm `Dots` (`ProgressDots`, ở giữa phía trên) và `Mascot` (cạnh trái `NextButton`, nằm trong dải 200 đơn vị ở đáy màn, ngoài Stage).
    - `PresentCurrent()` gọi `Dots.SetCurrent(Flow.Position)`. Root của màn bước mới mờ sang rõ và trượt từ +60 về 0 trong 0,3 giây.

- [ ] **Step 1: Viết test hỏng** `LessonChromeTests` (mở app bằng `LoadMainWithProfile(unlockAll: true)`, vào `tv1_t1_b13`):
  - `Buttons_AreIconButtons`: `IconButton.IconId` của Back, Replay, Next là `Home`, `Speaker`, `Forward`.
  - `Dots_TrackPosition`: `Dots.Total == Flow.TotalCount`; sau một lần "Tiếp" thì `Dots.Current == 1`.
  - `Dots_BarWhenTooMany`: `ProgressDots.Create(parent, 40).IsBar == true`; `Create(parent, 20).IsBar == false`.
  - `NextTwice_AdvancesOnce` (Review Focus 2): làm xong bước 0, gọi `NextButton.onClick.Invoke()` hai lần trong cùng khung hình; `Flow.Position == 1`.
  - `Mascot_OutsideStageAndButtons_BothSizes`: ở 2400×1080 và 2048×1536, khung của gà con không giao với khung Stage và khung các nút; `LayoutProbe.AssertFits` xanh.
- [ ] **Step 2: Chạy, thấy đỏ.**
- [ ] **Step 3: Viết code** theo Interfaces.
- [ ] **Step 4: Chạy, thấy xanh:** `LessonChromeTests` và cả PlayMode. `MvpEndToEndTests` chạy trọn 80 bài vẫn xanh (hiệu ứng tắt trong test).
- [ ] **Step 5: Commit:** `feat(lesson): nút biểu tượng, chấm tiến độ, gà con, chuyển bước`.

### Task 6: Hiệu ứng phản hồi trong các bước và lượt luyện tập

**Files:**
- Modify:
  - `Exercises/RoundFeedback.cs`, `Exercises/RoundViewBase.cs`;
  - `UI/Tile.cs` (phồng khi đang đọc tới, nhún khi gợi ý);
  - `UI/DragTile.cs` (to lên khi kéo, bay về chỗ cũ khi thả trượt, tiếng khi nhấc);
  - `UI/PageButtons.cs` (nút biểu tượng `PagePrev`/`PageNext` nền `PaperLight`);
  - `Steps/SpellView.cs` (bản sao bay vào ô kết quả, `onGap`, tranh lắc nhẹ);
  - `Steps/SentenceView.cs` (nút loa to ngay dưới câu; nút xong là `Check` nền cam);
  - các màn bước khác chỉ khi cần gọi `Ctx.Fx` lúc xong.
- Test: `Tests/PlayMode/LessonFeedbackFxTests.cs`

**Interfaces:**
- Consumes: `LessonFx`, `LessonContext.Fx` (Task 5); `SfxPlayer.History` (Task 4); `Motion`, `Pulse` (Task 3).
- Produces:
  - `RoundFeedback.Handle(bool correct, Tile correctTile, Tile chosenTile = null)`.
    - Đúng: `Ctx.Fx?.Correct(chosenTile hoặc correctTile)`, rồi khen như cũ.
    - Sai lần đầu: `Ctx.Fx?.Wrong(chosenTile)`.
    - Sai lần hai: thêm `correctTile.SetHint(true)`.
  - `RoundViewBase.Answer(int option)` truyền thẻ của `option` vào `chosenTile`.
  - `Tile.SetHighlighted(true)`: `ScaleTo(1.1, .12)`; `false` thì về 1.
  - `Tile.SetHint(true)`: `Pulse.Start`; `false` thì `Pulse.Stop`.
  - `SpellView`:
    - trong demo và luyện, mảnh kế tiếp là `join` thì ở `onGap` có các bản sao của thẻ trong chuỗi bay vào giữa ô kết quả và mờ đi (0,3 giây), cùng `Ctx.Fx?.Merge()`. Khi mảnh `join` phát, ô kết quả `Punch(1.15)`;
    - chạm sai thứ tự: `Ctx.Fx?.Wrong(thẻ vừa chạm)`, giữ cách gợi ý cũ;
    - `Finish()`: `Ctx.Fx?.Correct(_result)`, tranh `Wiggle(3°, .4s)`.
  - Tiếng khi chạm (bản thiết kế 7.2.3b): `TapFeedback.Sound = SystemSfx.Tap` chỉ đặt cho:
    - nút điều hướng;
    - nút "Con đọc xong rồi";
    - nút lật trang trong bước;
    - lúc nhấc thẻ kéo.

    Thẻ trong bước học và nút loa (`ListenSentence`, Replay) không có tiếng.

- [ ] **Step 1: Viết test hỏng** `LessonFeedbackFxTests` (dùng `ViewTestBase`, gắn `Ctx.Fx` thật cùng `SfxPlayer` và `Mascot` tạo trong test; `Motion.Scale = 1` ở các test có hiệu ứng):
  - `Round_Correct_PlaysDingAndCheers`: `Sfx.History` có `sfx_dung`; `Mascot.LastMood == Cheer`.
  - `Round_Wrong_NoSfx_Ponders_NoRed`: `ActWrongForTest()`. `Sfx.History` không có mã nào; `LastMood == Ponder`; màu nền thẻ đã chọn vẫn là `PaperLight` (không đỏ).
  - `Round_SecondWrong_HintPulses`: `Pulse.IsRunning(answerTile.transform)`.
  - `Spell_Demo_NoTapSound_MergeInGap`:
    - suốt demo, `History` không có `sfx_cham`;
    - có đúng 1 `sfx_nhap` cho mỗi mảnh `join`;
    - tại lúc `sfx_nhap` được ghi, `Speech.History` mới chỉ có các mảnh trước `join` (ghi số lượng trong `onGap` để so).
  - `Spell_TapTile_NoTapSound`.
  - `Sentence_DoneButton_HasTapSound_ListenDoesNot`: kiểm tra `TapFeedback.Sound` của từng nút.
  - `PageButtons_AreIconButtons`: `ButtonWithText(v, UiText.PageNext)` tìm theo tên; `IconId == SystemIcons.PageNext`.
  - `AdvanceWhileSparks_NoErrors` (Review Focus 3): gọi `Correct`, rồi huỷ `Root` ngay; chờ 1 giây; `LogAssert.NoUnexpectedReceived()`.
  - `Drag_MissedDrop_ReturnsToStart`.
- [ ] **Step 2: Chạy, thấy đỏ.**
- [ ] **Step 3: Viết code** theo Interfaces.
- [ ] **Step 4: Chạy, thấy xanh:** test mới, rồi cả PlayMode. `NewStepViewTests2` và `RimeGridViewTests` dùng `ButtonWithText` cho nút trang vẫn xanh nhờ Task 2.
- [ ] **Step 5: Commit:** `feat(lesson): hiệu ứng đúng/sai, gợi ý, nhập thẻ, tiếng chạm`.

## Giai đoạn C — Sổ bé ngoan

### Task 7: Phần tính toán của sổ [có thể giao]

**Files:**
- Create: `Scripts/Runtime/Progress/FlowerBook.cs`
- Test: `Tests/EditMode/FlowerBookTests.cs`

**Interfaces:**
- Produces: `public static class FlowerBook` (trang tính từ 0, mỗi trang một bài theo thứ tự `ordered`):
  - `const int FlowersPerLesson = ProgressStore.MaxStars` (= 3);
  - `int FlowersFor(ProgressStore p, string lessonId)`: bằng `p.StarsFor(lessonId)`;
  - `int PageOf(IReadOnlyList<string> ordered, string lessonId)`: không có thì −1;
  - `int SpreadStart(int page)`: bằng `page - page % 2` (trang trái của cặp);
  - `int StartPage(ProgressStore p, IReadOnlyList<string> ordered)`: trang của bài **đứng sau cùng trong `ordered`** trong số các bài đã học xong; chưa học bài nào thì 0;
  - `string FlowerImage(string lessonId, int slot)`: tạm thời luôn trả `SystemImages.Flower`.

- [ ] **Step 1: Viết test hỏng:**
  - `PageOf_FollowsOrder`;
  - `SpreadStart_EvenLeft`: 0→0, 1→0, 5→4;
  - `StartPage_LastCompletedInListOrder` (Review Focus 5): học xong bài thứ 70 trước, rồi bài thứ 3; kết quả là trang 69;
  - `StartPage_NoneCompleted_IsZero`;
  - `FlowersFor_FromStars`: 0 khi chưa học, 3 khi đã học;
  - `FlowerImage_IsFlower`.
- [ ] **Step 2: Chạy, thấy đỏ:** `python tools/run_unity_tests.py editmode --filter TapDoc.Tests.FlowerBookTests`.
- [ ] **Step 3: Viết code** theo Interfaces.
- [ ] **Step 4: Chạy, thấy xanh.**
- [ ] **Step 5: Commit:** `feat(progress): tính trang và hoa của Sổ bé ngoan`.

### Task 8: Khung hai trang và màn Sổ bé ngoan

**Files:**
- Create: `Scripts/Runtime/UI/BookSpread.cs`, `UI/BookPage.cs`, `App/BookScreen.cs`
- Modify: `App/AppRoot.cs` (`ShowBook()`)
- Test: `Tests/PlayMode/BookScreenTests.cs`

**Interfaces:**
- Consumes: `FlowerBook` (Task 7); `UiKit`, `Palette` (Task 2); `Motion`, `TapFeedback` (Task 3); `SfxPlayer` (Task 4).
- Produces:
  - `BookPage` (MonoBehaviour):
    - `string LessonId`;
    - `IReadOnlyList<Tile> Slots` (3 thẻ hoa 180×180 xếp một hàng ở phía trên trang);
    - `RectTransform Content`: vùng trống phía dưới, tên `PageContent`, không có con;
    - `int FlowerCount`;
    - `void SetFlowers(int count)`: ô có hoa nền trắng, viền `Teal`, hình `FlowerBook.FlowerImage`; ô trống viền `TealLight`, không có hình.

    Đầu trang là `string.Format(UiText.BookPageFormat, UiText.LessonPrefix, lesson_no, title)`. Chạm vào ô thì ô `Punch(1.08)`, `Sound = SystemSfx.Tap`.
  - `BookSpread` (MonoBehaviour):
    - `static BookSpread Create(RectTransform parent, IReadOnlyList<LessonEntry> entries, ProgressStore progress, AssetCatalog assets)`;
    - `void ShowPage(int page)`: hiện cặp trang bắt đầu từ `SpreadStart(page)`; bài cuối lẻ thì trang phải để trống;
    - `int LeftPage`, `int PageCount`;
    - `BookPage PageFor(string lessonId)` (`null` khi trang không đang hiện);
    - `Awaitable FlipTo(int page)`: hiệu ứng lật trang 0,35 giây kèm `sfx_lat_trang`; `Motion.Scale == 0` thì đổi ngay.

    Quyển sổ có viền mực và bóng gạch chéo, nằm giữa vùng an toàn, chừa 200 đơn vị ở trên cho thanh tiêu đề.
  - `BookScreen` (MonoBehaviour), `void Build(AppRoot app)`:
    - tiêu đề `string.Format(UiText.BookTitleFormat, tên bé)`;
    - `HomeButton` (Home, góc trên trái);
    - `PrevButton` / `NextButton` (`Backward`/`Forward`, giữa mép trái và mép phải); hết trang thì `interactable = false` và mờ đi;
    - vuốt ngang trên quyển sổ (kéo quá 120 đơn vị) cũng lật trang;
    - mở ở `FlowerBook.StartPage`.
  - `AppRoot.ShowBook()`: `Present<BookScreen>().Build(this)`.

- [ ] **Step 1: Viết test hỏng** `BookScreenTests`:
  - `OpensAtLastCompleted`: học xong bài thứ 1 và thứ 3; `Spread.LeftPage == 2`; `PageFor(ordered[2]).FlowerCount == 3`.
  - `PrevNext_DisabledAtEnds`: ở trang 0 thì `PrevButton.interactable == false`; lật tới cuối thì `NextButton.interactable == false`.
  - `Page_HasThreeSlotsAndEmptyContent`: `Slots.Count == 3`; `Content.childCount == 0`.
  - `NotLearned_EmptySlots`.
  - `LongTitles_Fit` (Review Focus 4):
    - bé tên 20 kí tự;
    - mở cặp trang có bài 6 "Dấu hỏi - Dấu ngã - Dấu nặng";
    - ở 2400×1080 và 2048×1536, `LayoutProbe.AssertFits` xanh;
    - lưu ảnh `TestOutput/screens/<cỡ>/app_book.png`.
  - `Swipe_Flips`: giả `OnBeginDrag`/`OnDrag`/`OnEndDrag` kéo sang trái 200 đơn vị; `LeftPage` tăng 2.
- [ ] **Step 2: Chạy, thấy đỏ.**
- [ ] **Step 3: Viết code** theo Interfaces.
- [ ] **Step 4: Chạy, thấy xanh**, rồi chạy cả PlayMode.
- [ ] **Step 5: Commit:** `feat(book): màn Sổ bé ngoan, mỗi trang một bài`.

### Task 9: Cảnh học xong bài (thay màn 3 ngôi sao)

**Files:**
- Modify: `App/ResultScreen.cs` (viết lại phần dựng), `UI/MarkerIcon.cs` (bỏ `CreateStar`, `FallbackStar`, `StarYellow` khi không còn ai dùng)
- Create: `UI/Stamp.cs`
- Modify (test): `Tests/PlayMode/AppFlowTests.cs` (thay `Result_MissingStarImage_DrawsStarNotSquare` bằng test hoa), `Tests/PlayMode/ReviewSessionTests.cs` nếu cần
- Test: `Tests/PlayMode/ResultSceneTests.cs`

**Interfaces:**
- Consumes: `BookSpread`, `BookPage` (Task 8); `Mascot` (Task 5); `Motion` (Task 3); `SfxPlayer` (Task 4).
- Produces:
  - `Stamp` (MonoBehaviour): `static Stamp Create(Transform parent, float size = 220f)`. Gồm hai vòng tròn màu `Palette.StampRed` và chữ `UiText.StampText` bằng font của app. Không nhận chạm.
  - `ResultScreen`:
    - giữ `NextLessonButton` (`Forward`, nền cam, tên `Button_Học bài tiếp`) và `ToListButton` (`Home`, tên `Button_Về danh sách`);
    - thêm `BookSpread Spread` (`null` ở phiên ôn), `Mascot Mascot`, `bool IsSceneDone`, `int FlownFlowers`;
    - thêm `internal void SkipScene()`.
  - Thứ tự (bản thiết kế 8.4):
    1. đọc `before = FlowersFor` **trước** `MarkCompleted`, rồi `MarkCompleted` và `SaveProgress` như cũ;
    2. mở sổ ở trang của bài; ô hoa sáng viền cam;
    3. `after − before` bông hoa bay lần lượt vào ô `before`…`after − 1`, cách nhau 0,3 giây, mỗi bông kèm `sfx_hoa_bay` và cánh hoa (`Petal`) rơi;
    4. đóng `Stamp` xuống `PageContent` (`sfx_dong_dau`), sổ `Shake` nhẹ;
    5. `Mascot.Cheer(UiText.MascotLessonDone)` và `khen_hoan_thanh`;
    6. hiện các nút (`Punch`); dấu mờ đi; `IsSceneDone = true`.
  - Chạm bất kì chỗ nào trên màn (một `Image` trong suốt phủ màn, có `IPointerClickHandler`, không phải `Selectable`) thì gọi `SkipScene()`: mọi hoa đã dán, các nút đã hiện.
  - Phiên "Ôn lại": không có sổ. Có nhãn `UiText.Praise`, `Mascot.Cheer(UiText.MascotLessonDone)` và `ToListButton`, không có `NextLessonButton`.

- [ ] **Step 1: Viết test hỏng** `ResultSceneTests`:
  - `NewLesson_ThreeFlowersFly`: `Motion.Scale = 0`. Sau một khung hình: `IsSceneDone`, `FlownFlowers == 3`, `Spread.PageFor(id).FlowerCount == 3`, `Sfx.History` có 3 `sfx_hoa_bay` và 1 `sfx_dong_dau`.
  - `Relearn_NoFlowersFly_StampStill`: bài đã học, `FlownFlowers == 0`, vẫn có `sfx_dong_dau`.
  - `Review_NoBook_NoNextButton`: `Spread == null`, `NextLessonButton == null`.
  - `TapSkips_ShowsButtons`: `Motion.Scale = 1`; chạm lớp phủ ngay; trong khung hình sau thì `IsSceneDone` và `ToListButton.gameObject.activeInHierarchy`.
  - `LeaveMidScene_NoErrors` (Review Focus 3): `Scale = 1`; sau 0,2 giây gọi `ToListButton.onClick.Invoke()` (nút đã có nhưng ẩn, nên gọi trực tiếp); chờ 2 giây; `LogAssert.NoUnexpectedReceived()`.
  - `MissingFlowerImage_ReportsError`: catalog trả `null` cho `SystemImages.Flower`; `LogAssert.Expect(LogType.Error, "[TapDoc] Thiếu tranh: img_chung_hoa_be_ngoan")`; màn vẫn tới `IsSceneDone`.
  - `Layout_BothSizes`: ở 2400×1080 và 2048×1536, chụp `app_result.png` và `AssertFits`.
- [ ] **Step 2: Chạy, thấy đỏ.**
- [ ] **Step 3: Viết code** theo Interfaces. Xoá phần sao thừa trong `MarkerIcon`; `SystemImages.Star` giữ lại vì file và danh mục vẫn còn.
- [ ] **Step 4: Chạy, thấy xanh:** test mới, `AppFlowTests`, `ReviewSessionTests`, `MvpEndToEndTests`.
- [ ] **Step 5: Commit:** `feat(result): cảnh dán hoa vào Sổ bé ngoan khi học xong bài`.

### Task 10: Danh sách bài kiểu mới

**Files:**
- Modify: `App/LessonListScreen.cs`
- Test: `Tests/PlayMode/LessonListStyleTests.cs`; sửa `Tests/PlayMode/ProfileScreenTests.cs` và `LessonListScrollTests.cs` nếu chúng dựa vào chữ "Đổi bé" hay sao

**Interfaces:**
- Consumes: `CreateIconButton`, `CreateCardButton` (Task 2); `Pulse` (Task 3); `Mascot` (Task 5); `FlowerBook` (Task 7); `AppRoot.ShowBook` (Task 8).
- Produces:
  - `SwitchChildButton` = `CreateIconButton(iconId: avatar của bé, label: UiText.SwitchChild, fill: Palette.PaperLight)`, góc trên trái.
  - `internal Button BookButton` = `CreateIconButton(Book, UiText.Book, fill: PaperLight)`, góc trên phải, đứng trái `ParentButton`.
  - `ParentButton` vẫn là nút của người lớn.
  - Thẻ bài là `CreateCardButton`. Bên dưới có hàng `FlowerBook.FlowersFor` bông hoa nhỏ 40×40 (con tên `Flowers`, thay cho `Stars`).
  - Bài đang học tới (bài đầu tiên đã mở mà chưa học xong): nền `OrangeLight` và `Pulse`. `internal string CurrentLessonId`.
  - Bài chưa mở: nền `LockedFill`, chữ và viền `LockedInk`, biểu tượng `Lock`, `interactable = false`. Bỏ `CanvasGroup` alpha.
  - `ReviewButton` = `CreateIconButton(Review, UiText.ReviewMistakes)`, góc dưới trái; `interactable` như cũ.
  - Gà con ở góc dưới phải.
  - Mở màn thì `ScrollTo(CurrentLessonId)`.

- [ ] **Step 1: Viết test hỏng** `LessonListStyleTests`:
  - `CompletedLesson_ShowsThreeFlowers`: thẻ bài đã học có con `Flowers` gồm 3 `Image` với sprite `img_chung_hoa_be_ngoan`.
  - `CurrentLesson_OrangeAndPulsing`.
  - `Locked_HasLockIcon_NotInteractable`.
  - `BookButton_OpensBook`.
  - `CurrentLesson_ScrolledIntoView` (Review Focus 5): 69 bài đầu đã học, bài 70 đang học; thẻ của bài này nằm trong `Scroll.viewport`.
  - `Layout_BothSizes`: chụp lại `app_lesson_list.png`.
- [ ] **Step 2: Chạy, thấy đỏ.**
- [ ] **Step 3: Viết code** theo Interfaces.
- [ ] **Step 4: Chạy, thấy xanh**, rồi chạy cả PlayMode.
- [ ] **Step 5: Commit:** `feat(list): danh sách bài kiểu mới, hoa, bài đang học, nút sổ`.

## Giai đoạn D — Màn còn lại và tài nguyên thật

### Task 11: Màn chọn bé, màn Phụ huynh và công tắc tiếng động

**Files:**
- Modify: `App/ProfileScreen.cs`, `App/ParentScreen.cs`, `App/ParentGate.cs` (nếu có dựng giao diện), `UI/NotesPanel.cs`
- Test: thêm vào `Tests/PlayMode/ProfileScreenTests.cs` và `Tests/PlayMode/ParentScreenTests.cs`

**Interfaces:**
- Consumes: `CreateCardButton`, `Palette` (Task 2); `ProgressStore.SfxEnabled`, `AppRoot.Sfx` (Task 4).
- Produces:
  - Màn chọn bé:
    - thẻ bé và thẻ "+ Bé mới" dùng `CreateCardButton`, có `TapFeedback.Sound = SystemSfx.Tap`;
    - hình đại diện đang chọn có viền `Orange` dày 6 và `Punch(1.08)`;
    - "Xong" và "Về" ở phần tạo bé giữ là nút của người lớn.
  - `ParentScreen.SfxToggle` (`Button`, nút của người lớn):
    - chữ là `UiText.SfxOn` hoặc `UiText.SfxOff`;
    - bấm thì đảo `Progress.SfxEnabled`, gán `app.Sfx.Enabled`, gọi `app.SaveProgress()` và đổi chữ.
  - Màn Phụ huynh, khoá phụ huynh, khung Ghi chú, Chú ý và Phụ lục: nền `Paper`, nút của người lớn. Không gà con, không hiệu ứng vui.

- [ ] **Step 1: Viết test hỏng:**
  - `ParentScreenTests.SfxToggle_FlipsAndPersists`: mở khoá, bấm công tắc. Kết quả: chữ đổi thành `UiText.SfxOff`; `AppRoot.Instance.Sfx.Enabled == false`; nạp lại file tiến độ thì `SfxEnabled == false`.
  - `ParentScreenTests.NoMascotOnAdultScreens`: không có `Mascot` nào trong canvas.
  - `ProfileScreenTests.PickAvatar_HighlightsOrange`.
  - `ProfileScreenTests.Screens_FitPhoneAndTablet`: test đã có, chạy lại để chụp ảnh mới.
- [ ] **Step 2: Chạy, thấy đỏ.**
- [ ] **Step 3: Viết code** theo Interfaces.
- [ ] **Step 4: Chạy, thấy xanh**, rồi chạy cả PlayMode.
- [ ] **Step 5: Commit:** `feat(ui): màn chọn bé, phụ huynh kiểu mới, công tắc tiếng động`.

### Task 12: Tiếng động CC0 thật

**Files:**
- Create:
  - `unity/TapDoc/Assets/Content/Resources/sfx/<mã>.(ogg|wav)` (6 file, cùng `.meta`);
  - `docs/credits-am-thanh.md`.
- Modify: `tools/tapdoc/system_assets.py` (`nguon`, `giay_phep` của 6 mã), `Tests/EditMode/DataTests.cs` (kiểm tra đủ file tiếng động)

- [ ] **Step 1: Hỏi chủ dự án một lần trước khi tải cả lô.** Nêu tên gói, nguồn và dung lượng:
  - Kenney Interface Sounds, Impact Sounds, RPG Audio (kenney.nl, CC0);
  - OpenGameArt "Pop sounds" (CC0);
  - 1 file "whoosh" CC0 trên Freesound (tìm và nêu link cụ thể trước khi hỏi).
- [ ] **Step 2: Tải về một thư mục tạm riêng, mở ZIP.** Đọc file giấy phép trong mỗi gói; phải là CC0.
- [ ] **Step 3: Nghe và chọn mỗi mã một file** (bản thiết kế 7.1 và 7.3). Cắt hoặc giảm âm lượng nếu cần. Chép vào `Resources/sfx/` với tên `<mã>.<đuôi gốc>`.
- [ ] **Step 4: Ghi nguồn và giấy phép:**
  - điền `nguon` (gói, tên file gốc) và `giay_phep: "CC0"` vào `SYSTEM_SFX`;
  - viết `docs/credits-am-thanh.md` (bảng mã, file gốc, gói, link, giấy phép).
- [ ] **Step 5: Viết test** `DataTests.AllSfxExist`: với mỗi mã trong `SystemSfx.All` thì `Resources.Load<AudioClip>("sfx/" + id) != null`.
- [ ] **Step 6: Chạy:**
  - `cd tools && python -m tapdoc validate` phải ra `OK`;
  - EditMode và PlayMode xanh, không còn cảnh báo "Thiếu tiếng động".
- [ ] **Step 7: Nhờ chủ dự án nghe 6 tiếng** (gửi đường dẫn file). Đổi file nếu chủ dự án không ưng.
- [ ] **Step 8: Commit:** `content: tiếng động CC0 (Kenney, OpenGameArt, Freesound)`.

### Task 13: Hình bông hoa bé ngoan bằng ChatGPT

**Files:** `unity/TapDoc/Assets/Content/Resources/images/img_chung_hoa_be_ngoan.png` (ghi đè hoa tạm), `content/manifests/image_manifest.json`

- [ ] **Step 1: Dùng Edge trên máy này, dự án ChatGPT Kiet_1.** Tạo tranh theo mô tả trong `SYSTEM_IMAGES` và bản thiết kế 8.6:
  - bông hồng hồng tươi, lá xanh, có cuống;
  - viền mực đen rõ, có điểm sáng, rực rỡ hơn tranh bài học;
  - nền trong suốt hoặc giấy ngà, không chữ, không khung, vuông.

  Không đưa ảnh sổ bé ngoan chủ dự án gửi vào ChatGPT.
- [ ] **Step 2: Hỏi chủ dự án trước khi tải** (tên file, dung lượng). Tải về thư mục tạm riêng.
- [ ] **Step 3: Nhập tranh:** `cd tools && python -m tapdoc import-image <file.png> img_chung_hoa_be_ngoan`, rồi `python -m tapdoc validate` ra `OK`.
- [ ] **Step 4: Chạy PlayMode** `ResultSceneTests`, `BookScreenTests`, `LessonListStyleTests`, rồi gửi chủ dự án ảnh `app_result.png` và `app_book.png`.
- [ ] **Step 5: Commit:** `content: hình bông hoa bé ngoan`.

### Task 14: Chạy trọn và ghi lại

- [ ] **Step 1: Chạy toàn bộ test:**
  - `cd tools && python -m unittest discover -s tests -t .`;
  - `python tools/run_unity_tests.py editmode`;
  - `python tools/run_unity_tests.py playmode` (gồm `MvpEndToEndTests` 80 bài ở 2 khung hình).

  Tất cả phải xanh.
- [ ] **Step 2: Xem bằng mắt các ảnh trong `TestOutput/screens/2400x1080` và `2048x1536`:**
  - danh sách bài, sổ, kết quả;
  - vài bước học có gà con và chấm tiến độ;
  - màn Phụ huynh.

  Sửa chỗ lệch (test trước, đỏ rồi xanh).
- [ ] **Step 3: Review cả nhánh việc** bằng một người review mới (1 subagent, `superpowers:requesting-code-review`). Sửa các phát hiện quan trọng (test trước).
- [ ] **Step 4: Cập nhật tài liệu:**
  - ghi kết quả test và việc còn lại vào cuối bản thiết kế `2026-10-30-ui-hieu-ung-design.md`;
  - cập nhật ghi chú tiếp tục `docs/superpowers/notes/`.

  Commit: `docs: kết quả làm giao diện, hiệu ứng và Sổ bé ngoan`.
- [ ] **Step 5: Báo chủ dự án** để thử và chỉnh (chủ dự án đã nói "khi lên UI sẽ test và hiệu chỉnh sau").
