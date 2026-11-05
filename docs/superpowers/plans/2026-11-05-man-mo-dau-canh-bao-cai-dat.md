# Màn mở đầu, popup cảnh báo, menu Cài đặt — Kế hoạch thực hiện

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** thêm màn mở đầu, popup "Gửi phụ huynh" (hiện một lần), và menu Cài đặt mở bằng nút bánh răng. Cài đặt gồm: tiếng động, xem lại lưu ý, thông tin; sau khoá phụ huynh: đổi/xoá hồ sơ, xoá toàn bộ. Tắt sao lưu của hệ điều hành cho dữ liệu của bé.

**Architecture:**
- Dữ liệu mới nằm trong `ProgressStore`: phiên bản cảnh báo đã xem, đổi/xoá hồ sơ, xoá hết.
- Ba khối giao diện mới dựng bằng code, theo `UiKit`:
  - `SplashScreen`: lớp phủ trên cùng canvas trong lúc khởi động;
  - `NoticePopup`: popup phủ kín canvas, nội dung rộng 1440;
  - `SettingsScreen`: màn của bé, nằm trong `KidRoot`.
- Khoá phép tính tách ra `ParentGatePanel`, dùng chung cho màn Phụ huynh và Cài đặt.
- `AppRoot` nối luồng: màn mở đầu → (lần đầu) popup → màn chọn bé.

**Tech Stack:** Unity 6.6, uGUI dựng bằng code, TMP (Andika), NUnit EditMode/PlayMode, Python stdlib (công cụ biểu tượng). Chạy test bằng `python tools/run_unity_tests.py`.

**Spec:** `docs/superpowers/specs/2026-11-05-man-mo-dau-canh-bao-cai-dat-design.md`

## Global Constraints

- Chữ đặt trong `UiText` (có trong `UiText.All`). Hình theo mã trong `SystemIcons` / `SystemImages` và `SYSTEM_IMAGES` (Python).
- Màn của bé nằm trong `AppRoot.KidRoot`. Popup, màn mở đầu và nền chặn chạm phủ kín canvas; phần nội dung người lớn rộng `UiKit.SafeWidth` (1440), đặt giữa.
- Vùng chạm ≥ 160, chữ không tràn, mọi thứ trong vùng an toàn ở cả 9 cỡ `ScreenSizes.All`.
- Hiệu ứng nhân với `Motion.Scale`; popup cảnh báo không phát giọng đọc hay tiếng động khi hiện.
- Mọi thao tác xoá phải qua khoá phụ huynh và hỏi xác nhận; "Xoá toàn bộ" xác nhận hai lần.
- Lời cảnh báo không nhắc tên một bộ sách hay nhà xuất bản cụ thể. Không viết câu "app không có quảng cáo". Phần ghi công chỉ có font Andika (SIL OFL) và tiếng động CC0 (Kenney, OpenGameArt).
- Nút "Đã hiểu" không khoá.
- Không làm trang web chính sách, khai báo trên kho, nhắc học, liên hệ.
- Tranh và âm thanh không nằm trong git. Hình mới phải đóng gói bằng `tools/run_unity_media.py pack` (Unity đóng), commit `content/manifests/media_lock.json`, rồi báo chủ dự án đưa file trong `dist/` lên Drive.
- Không sửa, không commit thay đổi dở của session khác: hiện `content/manifests/*.json`, `content/style/tranh_dong_kich_ban.json`, `content/tts/settings.json`, `unity/TapDoc/Assets/Content/Resources/lessons/tv1_t2_b97.json` đang dở.
- Chỉ nhánh `main`, commit từng task, không push.
- Chỉ chạy test của task (`--filter`); bộ đầy đủ chỉ khi chủ dự án nói "test all". Không test nội dung Tập 2.

## Review Focus

1. **Xoá hồ sơ của bé đang học** rồi bấm Về: không màn nào dùng `Progress.Current` cũ (`null`). App về màn chọn bé, hoặc màn tạo bé nếu hết hồ sơ.
   Test: `Settings_DeleteCurrentChild_BackGoesToProfiles` (Task 6).
2. **Mở Cài đặt từ màn chọn bé khi chưa có hồ sơ nào** (mới cài): mọi mục chạy được, không lỗi null.
   Test: `Settings_FromProfiles_NoChild_Works` (Task 5).
3. **Bấm nhanh hai lần "Đã hiểu"**, hoặc bấm khi màn mở đầu chưa tắt hẳn: popup đóng một lần, cờ được ghi, không mở hai popup.
   Test: `Notice_DoubleTap_ClosesOnce` (Task 2).
4. **File tiến độ cũ**, có hồ sơ nhưng không có `notice_version`: vẫn đọc được hồ sơ, và popup hiện một lần.
   Test: `OldFile_NoNoticeVersion_ShowsNoticeKeepsProfiles` (Task 2).
5. **"Xoá toàn bộ" khi đang có file `.bak` / `.tmp`:** các file đó bị xoá; lần mở sau như mới cài.
   Test: `ResetAll_DeletesSideFiles` (Task 1).

---

### Task 1: Dữ liệu — phiên bản cảnh báo đã xem, đổi/xoá hồ sơ, xoá toàn bộ

**Files:**
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/Progress/ProgressData.cs` (thêm `public int notice_version;` vào `ProgressFile`, cạnh `sfx_off`)
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/Progress/ProgressStore.cs`
- Test: `unity/TapDoc/Assets/Tests/EditMode/ProgressStoreTests.cs`

**Interfaces — Produces:**
- `ProgressStore.NoticeVersion : int` (get/set; đọc ghi `notice_version`)
- `bool ProgressStore.RenameProfile(string profileId, string name)`: dùng `CleanName`; tên rỗng sau khi làm sạch thì trả `false` và không đổi
- `bool ProgressStore.SetAvatar(string profileId, string avatar)`
- `bool ProgressStore.DeleteProfile(string profileId)`: xoá bé đang học thì `current = null`
- `void ProgressStore.ResetAll()`: dữ liệu trong bộ nhớ về như kho trống (`sfx_off = false`, `notice_version = 0`); xoá `FilePath`, `FilePath + ".tmp"`, `FilePath + ".bak"` nếu có

- [ ] **Step 1: Viết test hỏng** (EditMode, file tạm trong `Path.GetTempPath()`):
  - `NoticeVersion_DefaultZero_RoundTrips`: kho mới có `NoticeVersion == 0`; đặt 1, `Save`, `Load` lại thì được 1.
  - `OldFile_NoNoticeVersion_ReadsZero`: ghi tay JSON `{"schema":1,"profiles":[{"id":"a","name":"Na","avatar":"img_chung_avatar_01","lessons":[],"mistakes":[]}],"current":"a","sfx_off":false}`; `Load` cho `NoticeVersion == 0` và vẫn 1 hồ sơ "Na".
  - `RenameProfile_CleansName`: đổi thành "  Bông  " thì tên là "Bông"; đổi thành "   " thì trả `false`, giữ tên cũ; mã bé không có thì trả `false`.
  - `SetAvatar_ChangesAvatar`.
  - `DeleteProfile_Current_ClearsCurrent`: hai bé A (đang học) và B; xoá A thì `Current == null`, còn 1 hồ sơ; xoá B (không phải bé đang học) thì `Current` không đổi.
  - `ResetAll_DeletesSideFiles`: tạo file chính, `.tmp`, `.bak`; `ResetAll()` thì cả ba file không còn; `Profiles.Count == 0`, `NoticeVersion == 0`, `SfxEnabled == true`.
- [ ] **Step 2: Chạy, thấy hỏng.**
  `python tools/run_unity_tests.py editmode --filter "ProgressStoreTests"`
- [ ] **Step 3: Viết code theo phần Interfaces.**
- [ ] **Step 4: Chạy lại, thấy đạt.** Cùng lệnh.
- [ ] **Step 5: Commit**
  `git commit -m "feat(progress): phiên bản cảnh báo đã xem, đổi/xoá hồ sơ bé, xoá toàn bộ dữ liệu"`

---

### Task 2: Popup "Gửi phụ huynh" và hiện một lần sau khởi động

**Files:**
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/Text/UiText.cs`
- Create: `unity/TapDoc/Assets/Scripts/Runtime/UI/NoticePopup.cs`
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/App/AppRoot.cs`
- Modify: `unity/TapDoc/Assets/Tests/PlayMode/AppTestBase.cs` (mặc định "đã xem")
- Test: `unity/TapDoc/Assets/Tests/PlayMode/NoticePopupTests.cs`

**Interfaces:**
- Consumes: `ProgressStore.NoticeVersion` (Task 1).
- Produces:
  - Chữ trong `UiText`, đều có trong `UiText.All`:
    - `const int NoticeVersion = 1`;
    - `NoticeTitle = "Gửi phụ huynh"`;
    - `NoticeBody`: chép nguyên văn khối nội dung ở bản thiết kế mục 5.2 (các tiêu đề nhỏ in đậm bằng thẻ `<b>`);
    - `NoticeAccept = "Đã hiểu"`.
    - Dùng `UiText.Close` có sẵn cho nút "Đóng".
  - `NoticePopup : MonoBehaviour`:
    - `static NoticePopup Show(Transform canvas, AssetCatalog assets, bool firstRun, Action onClosed)`;
    - `Button CloseButton` (chữ `NoticeAccept` khi `firstRun`, ngược lại `Close`);
    - `bool IsOpen`.
    - Gốc phủ kín canvas, nền giấy chặn chạm. Con `Frame` rộng `UiKit.SafeWidth`, cao 1080, đặt giữa vùng an toàn (`AppRoot.Frames.Standard`). Gồm tiêu đề, khung cuộn có nội dung, nút, gà con nhỏ ở góc.
  - `AppRoot.Notice : NoticePopup` (đang mở, hoặc `null`)
  - `AppRoot.ShowNotice(bool firstRun)`: mở popup; khi `firstRun` và bấm nút thì đặt `Progress.NoticeVersion = UiText.NoticeVersion` rồi `SaveProgress()`.
  - Trong `BootAsync`, sau `ShowProfiles()`: nếu `Progress.NoticeVersion < UiText.NoticeVersion` thì `ShowNotice(firstRun: true)`.
  - `AppTestBase`: thêm `protected bool NoticeSeen = true;`. `StoreFactory` bọc `Load`: nếu `NoticeSeen` thì đặt `NoticeVersion = UiText.NoticeVersion` trước khi trả kho. Test cũ vì vậy chạy như trước.

- [ ] **Step 1: Viết test hỏng** (`NoticePopupTests : AppTestBase`, các test đặt `NoticeSeen = false` trước khi nạp):
  - `FirstRun_ShowsNoticeOverProfiles`: sau `LoadMain()` có `AppRoot.Notice != null`, `IsOpen`, chữ nút là "Đã hiểu"; bên dưới là `ProfileScreen`. Bấm vào nút tạo bé phía sau thì không có gì xảy ra: raycast tại tâm nút trúng popup.
  - `Accept_SavesVersion_NotShownAgain`: bấm "Đã hiểu" thì popup đóng, `Progress.NoticeVersion == UiText.NoticeVersion`. Huỷ app, nạp lại với cùng file tiến độ: không có popup.
  - `Notice_DoubleTap_ClosesOnce`: gọi `CloseButton.onClick.Invoke()` hai lần liên tiếp. Chỉ một lần đóng (đếm qua `onClosed`), `AppRoot.Notice == null`, không còn đối tượng `NoticePopup` nào.
  - `OldFile_NoNoticeVersion_ShowsNoticeKeepsProfiles`: ghi file tiến độ kiểu cũ có một hồ sơ, không có `notice_version`; nạp app thì popup hiện và màn chọn bé có thẻ của bé đó.
  - `Notice_Text_HasOwnerWarnings`: chữ trong popup chứa "chỉ mang tính chất tham khảo", "không dựa hoàn toàn vào một nguồn sách nào", "không cổ xúy", "không liên quan đến bất kỳ cá nhân, tổ chức nào", "có thể chưa chuẩn", "chỉ được lưu trên máy này"; không chứa "1996", "quảng cáo".
  - `Notice_FitsAllSizes`: mỗi cỡ `ScreenSizes.All` đều qua `LayoutProbe.AssertFits`; lưu ảnh `TestOutput/screens/{size.Name}/app_notice.png`.
- [ ] **Step 2: Chạy, thấy hỏng.**
  `python tools/run_unity_tests.py playmode --filter "NoticePopupTests"`
- [ ] **Step 3: Viết code theo phần Interfaces.**
- [ ] **Step 4: Chạy lại, thấy đạt.** Chạy thêm các test khởi động cũ để chắc `NoticeSeen` mặc định giữ chúng như trước:
  `--filter "NoticePopupTests|AppBootTests|ProfileScreenTests|ScreenFramesAppTests"`
- [ ] **Step 5: Commit**
  `git commit -m "feat(ui): popup Gửi phụ huynh hiện một lần sau khởi động"`

---

### Task 3: Màn mở đầu, báo lỗi khi nạp hỏng, tắt màn "Made with Unity"

**Files:**
- Create: `unity/TapDoc/Assets/Scripts/Runtime/UI/SplashScreen.cs`
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/App/AppRoot.cs` (`BootAsync`)
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/Text/UiText.cs` (`BootError = "Không mở được dữ liệu của ứng dụng. Hãy cài lại ứng dụng."`)
- Modify: `unity/TapDoc/ProjectSettings/ProjectSettings.asset` (`m_ShowUnitySplashScreen: 0`; chỉ sửa khi Unity đóng)
- Test: `unity/TapDoc/Assets/Tests/PlayMode/SplashScreenTests.cs`
- Test: `unity/TapDoc/Assets/Tests/EditMode/SetupTests.cs` (thêm một test)

**Interfaces:**
- Produces:
  - `SplashScreen : MonoBehaviour`:
    - `static SplashScreen Create(Transform canvas, AssetCatalog assets)`;
    - `bool IsShowing`;
    - `Awaitable HideAsync()`: chờ đủ `MinSeconds = 1f` nhân `Motion.Scale` kể từ lúc hiện, rồi mờ đi;
    - `void ShowError(string message)`: hiện dòng chữ, không tắt màn;
    - `TMP_Text ErrorLabel`.
  - Gốc phủ kín canvas, là con cuối của canvas (trên cả popup). Nền giấy, gà con nhún (`Pulse`), tên `UiText.AppTitle`, ba chấm.
  - `AppRoot.Splash : SplashScreen`. `BootAsync` tạo màn mở đầu ngay khi bắt đầu nạp. Nạp xong thì `ShowProfiles()`, rồi popup (Task 2), rồi `await Splash.HideAsync()`. Nạp lỗi thì `Splash.ShowError(UiText.BootError)` cùng log lỗi như cũ.
- Lưu ý gỡ lỗi: popup phải mở trước khi màn mở đầu mờ đi, để không chớp màn chọn bé. Màn mở đầu là con cuối nên luôn che popup cho tới khi mờ.

- [ ] **Step 1: Viết test hỏng.**
  - `Splash_ShownDuringBoot_HiddenAfterReady` (PlayMode):
    - nạp scene `Main` bằng một nguồn nội dung giả chậm (`FakeContentSource` có `Delay` khung hình nếu có; không có thì đếm qua `AppRoot.Splash` ngay khung đầu sau `LoadScene`);
    - ngay sau khi nạp scene: `AppRoot.Instance.Splash.IsShowing`;
    - sau `IsReady` và vài khung hình: `!Splash.IsShowing`.
  - `Splash_BootError_ShowsMessage`:
    - `AppRoot.SourceFactory` trả nguồn ném lỗi khi đọc danh sách bài;
    - `LogAssert.Expect(LogType.Error, new Regex("Không khởi động được"))`;
    - sau vài khung: `Splash.IsShowing`, `ErrorLabel.text == UiText.BootError`, `IsReady == false`.
  - `Splash_FitsAllSizes`: gọi trực tiếp `SplashScreen.Create` trên canvas của app ở từng cỡ, `LayoutProbe.AssertFits`, lưu ảnh `{size.Name}/app_splash.png`.
  - `SetupTests.UnitySplashScreenOff` (EditMode): `Assert.IsFalse(PlayerSettings.SplashScreen.show)`.
- [ ] **Step 2: Chạy, thấy hỏng.**
  `--filter "SplashScreenTests"` (PlayMode) và `--filter "SetupTests"` (EditMode)
- [ ] **Step 3: Viết code; sửa `ProjectSettings.asset` khi Unity đóng.**
- [ ] **Step 4: Chạy lại, thấy đạt.** Thêm `|NoticePopupTests|PrepareFlowTests`.
- [ ] **Step 5: Commit**
  `git commit -m "feat(ui): màn mở đầu trong lúc nạp, báo lỗi khi nạp hỏng; tắt màn Made with Unity"`

---

### Task 4: Biểu tượng bánh răng `img_ui_cai_dat` (hình tạm)

**Files:**
- Modify: `tools/tapdoc/ui_icons.py` (thêm `"img_ui_cai_dat"` vào `ICONS`: bánh răng viền mực, nền trắng, cùng nét với các biểu tượng khác)
- Modify: `tools/tapdoc/system_assets.py` (`SYSTEM_IMAGES["img_ui_cai_dat"] = "Biểu tượng cài đặt: bánh răng"`)
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/Content/SystemAssets.cs` (`SystemIcons.Settings = "img_ui_cai_dat"`, thêm vào `All`)
- Test:
  - `tools/tests/test_ui_icons.py` (số biểu tượng 12 → 13);
  - `tools/tests/test_build.py` (tập `ui` thêm `cai_dat`);
  - `unity/TapDoc/Assets/Tests/EditMode/UiStyleTests.cs` (`SystemIcons.All.Length` 12 → 13).

**Interfaces — Produces:** `SystemIcons.Settings`.

- [ ] **Step 1: Sửa ba test cho con số và tập mới;** thêm `test_settings_icon_has_ink`, kiểm hình có nét mực và góc trong suốt như các biểu tượng khác.
- [ ] **Step 2: Chạy, thấy hỏng.**
  - `cd tools && python -m unittest tests.test_ui_icons tests.test_build`
  - `python tools/run_unity_tests.py editmode --filter "UiStyleTests"`
- [ ] **Step 3: Thêm hình bánh răng vào `ICONS`, mã vào `SYSTEM_IMAGES` và `SystemIcons`.**
  Sinh file: `cd tools && python -m tapdoc ui-icons`. **Không dùng `--force`**: tuỳ chọn này ghi đè biểu tượng chính thức. Lệnh không có `--force` chỉ ghi file còn thiếu.
- [ ] **Step 4: Chạy lại, thấy đạt.** Cùng các lệnh.
- [ ] **Step 5: Danh mục tranh.**
  - Kiểm `git status content/manifests/image_manifest.json`.
  - Nếu file còn thay đổi dở của session khác: không chạy lệnh dựng lại danh mục và không commit file này. Nhắn session gốc (`local_0cefca18-12fb-4d82-a1d6-a65ff28a9bed`) hỏi ai đang giữ file và khi nào commit, rồi thêm mục `img_ui_cai_dat` sau khi họ commit.
  - Nếu file sạch: thêm mục bằng lệnh dựng danh mục của công cụ, rồi commit cùng task.
- [ ] **Step 6: Commit code và test** (không gồm file PNG; tranh không nằm trong git)
  `git commit -m "feat(assets): biểu tượng cài đặt (bánh răng, hình tạm)"`

---

### Task 5: Menu Cài đặt — nhóm không khoá, nút bánh răng, chuyển công tắc tiếng động

**Files:**
- Create: `unity/TapDoc/Assets/Scripts/Runtime/App/SettingsScreen.cs`
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/App/AppRoot.cs`
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/App/LessonListScreen.cs`
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/App/ProfileScreen.cs`
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/App/ParentScreen.cs` (bỏ công tắc tiếng động)
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/Text/UiText.cs`
- Test: `unity/TapDoc/Assets/Tests/PlayMode/SettingsScreenTests.cs`
- Test: `unity/TapDoc/Assets/Tests/PlayMode/ParentScreenTests.cs` (chuyển `SfxToggle_FlipsAndPersists` sang Cài đặt)

**Interfaces:**
- Consumes: `SystemIcons.Settings` (Task 4), `AppRoot.ShowNotice(false)` (Task 2).
- Produces:
  - Chữ trong `UiText`:
    - `Settings = "Cài đặt"`;
    - `ReviewNotice = "Xem lại lưu ý"`;
    - `AppInfo = "Thông tin ứng dụng"`;
    - `VersionFormat = "Phiên bản {0}"`;
    - `Credits` = "Phông chữ Andika (SIL Open Font License). Tiếng động: Kenney, OpenGameArt (CC0)."
  - `AppRoot.ShowSettings(Action back)`: `Present<SettingsScreen>()` trong `KidRoot`, rồi `Build(this, back)`.
  - `SettingsScreen`:
    - `Build(AppRoot app, Action back)`;
    - `Button BackButton`, `Button SfxToggle`, `Button ReviewNoticeButton`, `TMP_Text InfoLabel` (tên app, `string.Format(VersionFormat, Application.version)`, `Credits`);
    - `Button ManageButton`: mở nhóm có khoá, Task 6.
    - Các hàng là nút người lớn có chữ, trong khung cuộn rộng 1440.
  - `LessonListScreen.SettingsButton`: nút biểu tượng `SystemIcons.Settings`, nền `Palette.PaperLight`.
    - Đặt ở hàng trên, bên trái nút Sổ: góc `(1,1)`, vị trí `(-(3·Margin + ParentWidth + MinTouch), -Margin)`.
    - Tiêu đề danh sách thu lại: rộng 540, `anchoredPosition.x = -240`.
    - Bấm thì `app.ShowSettings(app.ShowLessonList)`.
  - `ProfileScreen.SettingsButton`: góc trên phải của màn (`(1,1)`, `(-Margin,-Margin)`), hiện ở cả phần chọn lẫn phần tạo bé. Bấm thì `app.ShowSettings(app.ShowProfiles)`.
  - `ParentScreen` không còn `SfxToggle`.

- [ ] **Step 1: Viết test hỏng** (`SettingsScreenTests : AppTestBase`):
  - `Gear_OnListAndProfiles_OpensSettings`: từ danh sách bài bấm `SettingsButton`, có `SettingsScreen`; bấm Về thì có `LessonListScreen`. Từ màn chọn bé: bấm Về thì có `ProfileScreen`.
  - `SfxToggle_SharesFlag`: bấm thì `Progress.SfxEnabled` đổi, `Sfx.Enabled` đổi theo, chữ nút đổi giữa `SfxOn` và `SfxOff`, `Load` lại file vẫn giữ. `ParentScreen` sau khi mở khoá không có nút chữ `SfxOn` hay `SfxOff`.
  - `ReviewNotice_OpensPopup_KeepsVersion`: đặt `NoticeVersion` = `UiText.NoticeVersion`; bấm `ReviewNoticeButton` thì popup mở, nút là "Đóng"; bấm Đóng thì popup đóng, `NoticeVersion` không đổi.
  - `Info_ShowsVersionAndCredits`: `InfoLabel.text` chứa `Application.version`, "Andika", "CC0".
  - `Settings_FromProfiles_NoChild_Works`: `LoadMain()` (chưa có hồ sơ), bấm bánh răng ở màn tạo bé; bấm tiếng động, xem lại lưu ý, Đóng, Về: không lỗi, về `ProfileScreen`.
  - `Settings_FitsAllSizes`: `LayoutProbe.AssertFits` ở 9 cỡ; nút bánh răng không đè nút khác và không đè tiêu đề ở danh sách bài và màn chọn bé; lưu ảnh `{size.Name}/app_settings.png`.
- [ ] **Step 2: Chạy, thấy hỏng.**
  `--filter "SettingsScreenTests"`
- [ ] **Step 3: Viết code theo phần Interfaces; chuyển test tiếng động của `ParentScreenTests`.**
- [ ] **Step 4: Chạy lại, thấy đạt.**
  `--filter "SettingsScreenTests|ParentScreenTests|LessonListStyleTests|ProfileScreenTests"`
- [ ] **Step 5: Commit**
  `git commit -m "feat(ui): menu Cài đặt (tiếng động, xem lại lưu ý, thông tin) mở bằng nút bánh răng"`

---

### Task 6: Cài đặt — nhóm có khoá phụ huynh: đổi/xoá hồ sơ, xoá toàn bộ

**Files:**
- Create: `unity/TapDoc/Assets/Scripts/Runtime/UI/ParentGatePanel.cs` (tách giao diện khoá phép tính ra khỏi `ParentScreen`)
- Create: `unity/TapDoc/Assets/Scripts/Runtime/UI/ConfirmDialog.cs`
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/App/ParentScreen.cs`
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/App/SettingsScreen.cs`
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/App/AppRoot.cs` (`ResetAllData`)
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/Text/UiText.cs`
- Test: `unity/TapDoc/Assets/Tests/PlayMode/SettingsScreenTests.cs`, `ParentScreenTests.cs` (phải giữ nguyên kết quả)

**Interfaces:**
- Consumes: `ProgressStore.RenameProfile/SetAvatar/DeleteProfile/ResetAll` (Task 1).
- Produces:
  - `ParentGatePanel : MonoBehaviour`:
    - `static ParentGatePanel Create(Transform parent, System.Random rng, Action onUnlocked)`;
    - `ParentGate Gate`, `IReadOnlyList<Button> ChoiceButtons`, `void SimulateUnlock()`.
    - `ParentScreen` dùng lớp này. Các thuộc tính `Gate`, `ChoiceButtons`, `SimulateUnlock` của `ParentScreen` giữ nguyên tên.
  - `ConfirmDialog : MonoBehaviour`:
    - `static ConfirmDialog Show(Transform canvas, string message, string confirmLabel, Action onConfirm)`;
    - `Button ConfirmButton`, `Button CancelButton`;
    - phủ kín canvas, khung 1440 ở giữa.
  - Chữ trong `UiText`:
    - `ManageProfiles = "Quản lý hồ sơ bé"`;
    - `Rename = "Đổi tên"`, `ChangeAvatar = "Đổi hình"`, `DeleteProfile = "Xoá hồ sơ"`;
    - `DeleteProfileConfirmFormat = "Xoá hồ sơ của bé {0}? Tiến độ của bé sẽ mất."`;
    - `DeleteAll = "Xoá toàn bộ dữ liệu"`;
    - `DeleteAllConfirm1 = "Xoá mọi hồ sơ và tiến độ học trên máy này?"`;
    - `DeleteAllConfirm2 = "Chắc chắn xoá? Không lấy lại được."`;
    - `Delete = "Xoá"`, `Cancel = "Huỷ"`, `Save = "Lưu"`.
  - `SettingsScreen`:
    - `ManageButton` mở `ParentGatePanel`. Mở khoá xong thì hiện danh sách bé; mỗi hàng có hình, tên và 3 nút `Rename`, `ChangeAvatar`, `DeleteProfile`. Cuối danh sách là nút `DeleteAll`.
    - `internal` hooks cho test: `ParentGatePanel GatePanel`, `Button RenameButtonFor(string id)`, `AvatarButtonFor(id)`, `DeleteButtonFor(id)`, `Button DeleteAllButton`.
    - Sửa hồ sơ: một khung gồm ô nhập tên (`TMP_InputField`, `characterLimit = ProgressStore.MaxNameLength`), 6 hình đại diện (`ProfileScreen.Avatars`, vẽ bằng `ProfileScreen.AddAvatar`) và nút `Save`.
  - Thoát Cài đặt sau khi xoá:
    - Sau khi xoá một bé, nút Về: nếu `Progress.Current == null` thì `ShowProfiles()`, ngược lại gọi `back` như thường.
    - `AppRoot.ResetAllData()`: `Progress.ResetAll()`, `Sfx.Enabled = true`, `SaveProgress()`, `ShowProfiles()`, rồi `ShowNotice(firstRun: true)`.
- [ ] **Step 1: Viết test hỏng:**
  - `Locked_NoEditButtons_UntilGate`: bấm `ManageButton` thì có `GatePanel`, chưa có nút đổi, xoá nào. `GatePanel.SimulateUnlock()` thì có các nút của mỗi bé và `DeleteAllButton`.
  - `Rename_And_ChangeAvatar_Persist`: đổi tên thành "Su" và chọn hình 3, Lưu; `Load` lại file thấy đúng.
  - `DeleteOtherChild_StaysInSettings`: hai bé, đang học bé A; xoá B rồi xác nhận: còn 1 hồ sơ, vẫn ở `SettingsScreen`, `Current` vẫn là A.
  - `Settings_DeleteCurrentChild_BackGoesToProfiles`: xoá A rồi xác nhận, `Current == null`; bấm Về thì có `ProfileScreen`, không có `LessonListScreen`, không có lỗi trong log.
  - `DeleteProfile_Cancel_KeepsChild`: bấm Huỷ thì không mất gì.
  - `DeleteAll_TwoConfirms_ResetsLikeFreshInstall`: bấm `DeleteAll`, xác nhận lần một thì vẫn còn dữ liệu và hiện hộp thứ hai; xác nhận lần hai thì `Profiles.Count == 0`, `SfxEnabled`, popup cảnh báo mở với nút "Đã hiểu", bên dưới là màn tạo bé; file `.bak`, `.tmp` không còn.
  - `ParentScreenTests` chạy lại không đổi (khoá dùng `ParentGatePanel`).
  - `Manage_FitsAllSizes`: sau khi mở khoá, có 3 bé; `LayoutProbe.AssertFits` ở 9 cỡ; lưu ảnh `{size.Name}/app_settings_manage.png`.
- [ ] **Step 2: Chạy, thấy hỏng.**
  `--filter "SettingsScreenTests"`
- [ ] **Step 3: Viết code theo phần Interfaces.**
- [ ] **Step 4: Chạy lại, thấy đạt.**
  `--filter "SettingsScreenTests|ParentScreenTests|NoticePopupTests"`
- [ ] **Step 5: Commit**
  `git commit -m "feat(ui): Cài đặt — đổi, xoá hồ sơ bé và xoá toàn bộ dữ liệu sau khoá phụ huynh"`

---

### Task 7: Tắt sao lưu của hệ điều hành cho dữ liệu của bé

**Files:**
- Create: `unity/TapDoc/Assets/Scripts/Editor/AndroidNoBackup.cs`: `IPostGenerateGradleAndroidProject`. Mở `src/main/AndroidManifest.xml` của module `unityLibrary` và `launcher`, đặt `android:allowBackup="false"` trên thẻ `<application>` (thêm `tools:replace="android:allowBackup"` khi cần).
- Modify: `unity/TapDoc/Assets/Scripts/Runtime/Progress/ProgressStore.cs`: sau mỗi lần `Save`, gọi `ExcludeFromBackup(FilePath)`. Trên iOS gọi `UnityEngine.iOS.Device.SetNoBackupFlag(path)` (`#if UNITY_IOS && !UNITY_EDITOR`); nền khác không làm gì.
- Test: `unity/TapDoc/Assets/Tests/EditMode/AndroidNoBackupTests.cs`

**Interfaces — Produces:** `internal static string AndroidNoBackup.Patch(string manifestXml)` (hàm thuần, test được).

- [ ] **Step 1: Viết test hỏng:**
  - `Patch_AddsAllowBackupFalse`: manifest có `<application android:label="x">` thì kết quả có `android:allowBackup="false"`.
  - `Patch_ReplacesTrue`: `android:allowBackup="true"` thì thành `"false"`.
  - `Patch_Idempotent`: patch hai lần cho cùng kết quả.
- [ ] **Step 2: Chạy, thấy hỏng.**
  `python tools/run_unity_tests.py editmode --filter "AndroidNoBackupTests"`
- [ ] **Step 3: Viết code.**
- [ ] **Step 4: Chạy lại, thấy đạt.** Thêm `|ProgressStoreTests`.
- [ ] **Step 5: Commit**
  `git commit -m "feat(platform): tắt sao lưu Android/iCloud cho dữ liệu của bé"`

---

### Task 8: Đóng gói hình, ảnh cho chủ dự án, ghi chú, review

- [ ] **Step 1: Đóng gói biểu tượng mới.**
  Đóng Unity, chạy `cd tools && python run_unity_media.py pack`, commit `content/manifests/media_lock.json`. Ghi lại tên 2 file mới trong `dist/` để báo chủ dự án đưa lên Drive.
- [ ] **Step 2: Gom ảnh chụp cho chủ dự án** từ `TestOutput/screens/{phone_20x9,iphone,ipad_43}/`: `app_splash`, `app_notice`, `app_settings`, `app_settings_manage`.
- [ ] **Step 3: Viết ghi chú tiếp tục** `docs/superpowers/notes/2026-11-05-tiep-tuc-mo-dau-cai-dat.md`: đã làm gì, các quyết định, việc còn lại (vẽ biểu tượng bằng ChatGPT, các việc để lúc phát hành). Commit.
- [ ] **Step 4: Review độc lập toàn bộ thay đổi; sửa Critical/Important theo TDD.**
- [ ] **Step 5: Xin chủ dự án lệnh "test all".**
