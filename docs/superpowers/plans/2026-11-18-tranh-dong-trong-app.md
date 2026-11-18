# Tranh động trong app — Kế hoạch làm

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Phát clip tranh động (Google Flow, 8 s, có tiếng) trên tranh ở 4 màn Phần 1, sau khi app đọc chữ của tranh; máy không phát được thì giữ tranh tĩnh.

**Architecture:** Một `ClipPlayer` trên `AppRoot` (một `VideoPlayer`, một `AudioSource`, một `RenderTexture`), phần phát thật nằm sau `IClipBackend` để test dùng bản giả. Clip là loại dữ liệu `ContentKind.Clip`, được chuẩn bị cùng bộ của bài và luôn không bắt buộc. Lệnh `run_unity_media.py clips` chép clip `dat` và `cho_duyet` từ `content/clips/` vào `Resources/clips/`.

**Tech Stack:** Unity 6000.6.5f1, C#, uGUI (`RawImage`), module `com.unity.modules.video`, Unity Test Framework (EditMode/PlayMode); Python 3 `unittest` cho `tools/`.

**Spec:** `docs/superpowers/specs/2026-11-18-tranh-dong-trong-app-design.md` (root duyệt 18/11, commit dc8da76).

## Global Constraints

- Tập clip phát được: `status ∈ {dat, cho_duyet}` trong `content/manifests/video_manifest.json`. Không đổi trạng thái trong file đó.
- Không đụng `content/manifests/audio_manifest.json`, `image_manifest.json`, `content/tts/settings.json`, `content/style/tranh_dong_kich_ban.json`. Mọi commit đều theo đường dẫn.
- Lệnh `clips` không đụng `media_lock.json` và không đụng gói media.
- Không sửa file clip, không chuyển mã: `enableTranscoding = false`.
- Mờ vào 0,3 s; mờ ra khi hết clip 0,25 s; mờ ra khi bị dừng 0,15 s. Chờ khung đầu tối đa 3 s (giờ thật). 2 lần hỏng liên tiếp thì tắt clip đến hết lần mở app. Máy dưới 2000 MB RAM: không phát. Âm lượng clip 1,0.
- Thiếu clip: im lặng. Clip hỏng: `Debug.LogWarning` một lần cho mỗi mã. Không bao giờ `LogError` vì clip.
- Chữ trên màn hình: `"Tranh động: Bật"`, `"Tranh động: Tắt"`.
- Chỉ một tiến trình Unity trên máy: **xin root lượt Unity trước mỗi lần chạy Unity**. Chỉ chạy các lớp test liên quan, không chạy cả bộ. Test phải im lặng.
- Python: `cd tools && python -m unittest tests.<module>`.
- Unity: `cd tools && python run_unity_tests.py <editmode|playmode> --test-filter "<lớp>"`. Kiểm tên tham số bằng `python run_unity_tests.py -h` trước lần chạy đầu.

## Review Focus

1. **Bé chạm liên tục trong lúc clip đang chờ khung đầu.** Clip cũ phải bỏ, không để lại lớp phủ mồ côi hay tiếng chạy ngầm. Test: `PlayAsync_StopDuringWaitForFirstFrame_LeavesNoOverlay` (Task 4).
2. **Bước bị huỷ đúng lúc clip đang mờ ra** (bấm Tiếp ngay khi clip hết). Không được có lỗi null, và `IsPlaying` phải về `false`. Test: `TileDestroyedWhilePlaying_StopsAndClearsState` (Task 4).
3. **Hai thẻ cùng có clip trong một màn** (`words` có 2–3 tranh). Mỗi lúc chỉ một clip; clip sau thay clip trước. Test: `PlayAsync_SecondTile_StopsFirst` (Task 4).
4. **Phụ huynh tắt Tranh động rồi bật lại trong cùng lần mở app.** Phải phát lại được, và số lần hỏng không bị dính từ trước. Test: `SettingOffThenOn_PlaysAgain` (Task 4).
5. **Máy có `Resources/clips` thật khi chạy các test cũ.** Test đi hết bài không được phát video thật. `AppTestBase` tắt `ClipPlayer.Enabled`; Task 6 kiểm cờ được trả lại sau test.

---

### Task 1: Lệnh `clips` (Python): chép clip vào Resources

**Files:**
- Create: `tools/tapdoc/clip_sync.py`
- Modify: `tools/run_unity_media.py` (lệnh `clips`, gọi đồng bộ ở cuối `unpack`)
- Modify: `tools/tapdoc/__main__.py:_cmd_validate` (cảnh báo khi lệch)
- Modify: `tools/tapdoc/paths.py` (`VIDEO_MANIFEST`, `UNITY_RES_CLIPS`)
- Modify: `.gitignore` (thêm `unity/TapDoc/Assets/Content/Resources/clips/` và `.../clips.meta`)
- Modify: `SETUP-MAY-MOI.md` mục 4, `CHUYEN-MAY-MOI.md` bước B4 (một dòng về lệnh `clips`)
- Test: `tools/tests/test_clip_sync.py` (mới), `tools/tests/test_run_unity_media.py` (thêm)

**Interfaces:**
- Produces: `PLAYABLE_STATUSES = ("dat", "cho_duyet")`.
- Produces: `@dataclass ClipSyncPlan: new: list[str]; changed: list[str]; remove: list[str]; unchanged: list[str]; missing_source: list[str]`. Các danh sách là mã tranh, sắp xếp.
- Produces: `plan_sync(rows: list[dict], clips_dir: Path, res_clips_dir: Path) -> ClipSyncPlan`.
- Produces: `apply_sync(plan: ClipSyncPlan, clips_dir: Path, res_clips_dir: Path) -> None`.
- Produces: `describe(plan: ClipSyncPlan) -> str | None`, trả `None` khi không có gì phải làm.
- Produces: `run_unity_media.sync_clips() -> int`, đọc các hằng `VIDEO_MANIFEST` và `RES_CLIPS_DIR` của module để test vá được.

- [ ] **Step 1: Viết test hỏng** `tests/test_clip_sync.py`, dựng `content/clips` và `Resources/clips` trong thư mục tạm:
  - `test_plan_copies_dat_and_cho_duyet_skips_khong_dat`: dòng `a:dat`, `b:cho_duyet`, `c:khong_dat`, có đủ 3 file nguồn. Kết quả `plan.new == ["a", "b"]`, và `"c"` không có trong danh sách nào.
  - `test_plan_changed_when_content_differs_unchanged_when_same`: nguồn `a` = `b"x1"`, đích = `b"x2"`, nên `changed == ["a"]`. Nguồn `b` giống đích nên `unchanged == ["b"]`.
  - `test_plan_removes_stale_clip`: đích có `c.mp4` (`c` là `khong_dat`) và `z.mp4` (không có dòng nào), nên `remove == ["c", "z"]`.
  - `test_plan_reports_missing_source`: `d:dat` không có file nguồn, nên `missing_source == ["d"]`.
  - `test_apply_copies_overwrites_and_deletes_meta`: sau `apply_sync`, đích có nội dung bằng nguồn; `c.mp4` và `c.mp4.meta` bị xoá; `.meta` của clip giữ nguyên thì không bị đụng.
  - `test_describe_none_when_in_sync`, `test_describe_mentions_command_when_out_of_sync`: chuỗi trả về có `"run_unity_media.py clips"`.
- [ ] **Step 2: Chạy, thấy hỏng.** `cd tools && python -m unittest tests.test_clip_sync`. Mong đợi: `ModuleNotFoundError: tapdoc.clip_sync`.
- [ ] **Step 3: Viết `tapdoc/clip_sync.py`.** So nhanh bằng cỡ file trước; cùng cỡ thì so sha256. Đường dẫn file nguồn lấy từ trường `file` của dòng (`clips/<mã>.mp4`), tính từ thư mục cha của `clips_dir`. Chép bằng ghi file tạm rồi đổi tên.
- [ ] **Step 4: Chạy lại, thấy qua.**
- [ ] **Step 5: Viết test hỏng** trong `tests/test_run_unity_media.py`:
  - `test_clips_command_syncs_playable_clips`: vá `VIDEO_MANIFEST` và `RES_CLIPS_DIR`, gọi `sync_clips()`. Kết quả trả `0` và có `Resources/clips/img_b01_bof.mp4`.
  - `test_unpack_syncs_clips_at_end`: luồng `unpack` sẵn có (Unity giả). Sau khi xong thì `RES_CLIPS_DIR` có clip.
- [ ] **Step 6: Thêm `sync_clips()` và lệnh con `clips`** (Unity phải đóng: dùng `project_is_open()` như `pack`, trả `2` khi đang mở). `unpack` gọi `sync_clips()` sau khi nhập `bosung`. In số chép mới, chép đè, xoá, giữ, và mã thiếu file.
- [ ] **Step 7: Cảnh báo trong `validate`.** Khi có `content/clips/`, in `Cảnh báo: …` với chuỗi từ `describe(plan_sync(...))`.
- [ ] **Step 8: Chạy** `python -m unittest tests.test_clip_sync tests.test_run_unity_media tests.test_media_lock`. Mong đợi: OK.
- [ ] **Step 9: Sửa `.gitignore` và hai tài liệu setup, rồi commit theo đường dẫn.**

### Task 2: Lớp dữ liệu Unity — loại `Clip`

**Files:**
- Modify: `unity/TapDoc/Packages/manifest.json` (thêm `"com.unity.modules.video": "1.0.0"`; Unity tự cập nhật `packages-lock.json`, commit cả hai)
- Modify: `Assets/Scripts/Runtime/Content/ContentPaths.cs` (`TypeOf(Clip) => typeof(UnityEngine.Video.VideoClip)`)
- Modify: `Assets/Scripts/Runtime/Content/ContentKind.cs` (chú thích)
- Modify: `Assets/Scripts/Runtime/Content/AssetCatalog.cs` (`Clip(id)`, thiếu thì im lặng)
- Modify: `Assets/Scripts/Runtime/Data/LessonAssets.cs` (`ClipIds`, `ContentIds`)
- Modify: `Assets/Scripts/Editor/ContentImportRules.cs` (`OnPreprocessAsset` cho `Assets/Content/Resources/clips/`)
- Test: `Assets/Tests/EditMode/ContentPathsTests.cs`, `Assets/Tests/EditMode/DataTests.cs`, `Assets/Tests/PlayMode/AssetCatalogTests.cs`

**Interfaces:**
- Produces: `Object AssetCatalog.Clip(string id)`. Bản thật trả `VideoClip`; test được đặt bất kỳ `Object` nào làm clip giả, vì không tạo được `VideoClip` bằng code.
- Produces: `IEnumerable<string> LessonAssets.ClipIds(Lesson lesson)`. Đó là `step.image` của các bước `keyword`, `picture`, `riddle_answer`, `tone_attach` và `items[].image` của bước `words`; không trùng, bỏ mã rỗng, chỉ lấy Phần 1.

- [ ] **Step 1: Viết test hỏng.**
  - `ContentPathsTests`: `Assert.AreEqual(typeof(UnityEngine.Video.VideoClip), ContentPaths.TypeOf(ContentKind.Clip))`.
  - `DataTests.ClipIds_TakesFourPlacesOnly`: một `Lesson` dựng tay có `keyword`(img_k), `picture`(img_p), `riddle_answer`(img_r, items img_r, img_x), `tone_attach`(img_t), `words`(items img_w1, img_w2), `spell`(không ảnh) và Phần 2 có `image` img_q. Kết quả `ClipIds` tương đương `{img_k, img_p, img_r, img_t, img_w1, img_w2}`; `img_x` và `img_q` không có.
  - Đổi tên `ContentIds_IsUnionOfAudioAndImage` thành `ContentIds_IsUnionOfAudioImageAndClip`: thêm `ClipIds` với `ContentKind.Clip`.
  - Test "mọi mã có tài nguyên" trong `DataTests` (khoảng dòng 103–117): lọc bỏ `key.kind == ContentKind.Clip`.
  - `AssetCatalogTests.MissingClip_IsSilent`: nguồn giả không có clip. Sau `PrepareAsync` với `(Clip, "img_x")` thì `Clip("img_x") == null` và `LogAssert.NoUnexpectedReceived()`.
- [ ] **Step 2: Viết thân trống để biên dịch được** (`ClipIds` trả rỗng, `Clip` trả `null`). Xin root lượt Unity, chạy `editmode` lọc `ContentPathsTests|DataTests` và `playmode` lọc `AssetCatalogTests`. Mong đợi: các test mới hỏng.
- [ ] **Step 3: Làm thật.**
  - `AssetCatalog.ReportMissing`: `if (key.kind == ContentKind.Clip) return;` đặt trước `switch`.
  - Import: `VideoClipImporter`, đặt `importAudio = true`, `sRGBClip = true`, `keepAlpha = false`; lấy `defaultTargetSettings`, đặt `enableTranscoding = false`, gán lại.
- [ ] **Step 4: Chạy lại các lớp trên, thấy qua.**
- [ ] **Step 5: Commit theo đường dẫn.**

### Task 3: Hàm thuần — cắt vuông và kiểm tra máy

**Files:**
- Create: `Assets/Scripts/Runtime/Video/ClipCrop.cs`, `Assets/Scripts/Runtime/Video/ClipSupport.cs`
- Test: `Assets/Tests/EditMode/ClipCropTests.cs`

**Interfaces:**
- Produces: `static Rect ClipCrop.UvRect(int clipWidth, int clipHeight, float pictureAspect)`, tính như spec mục 7.
- Produces: `const int ClipSupport.MinMemoryMb = 2000`.
- Produces: `static bool ClipSupport.CanPlay(int systemMemoryMb, bool hasGraphics, bool renderTextureOk)`.
- Produces: `static bool ClipSupport.CurrentDevice()`, đọc `SystemInfo`.

- [ ] **Step 1: Viết test hỏng.**
  - `UvRect(1280, 720, 1f)` bằng `(0.21875, 0, 0.5625, 1)`, sai số 1e-5.
  - `UvRect(720, 720, 1f)` bằng `(0, 0, 1, 1)`.
  - `UvRect(720, 1280, 1f)` bằng `(0, 0.21875, 1, 0.5625)`.
  - `UvRect(1280, 720, 4f/3f)`: `w = 0.75`, `x = 0.125`, `h = 1`.
  - `UvRect(0, 0, 1f)` bằng `(0, 0, 1, 1)`, không chia cho 0.
  - `CanPlay(1999, true, true) == false`; `CanPlay(2000, true, true) == true`; `CanPlay(8000, false, true) == false`; `CanPlay(8000, true, false) == false`.
- [ ] **Step 2: Viết thân trống, chạy `editmode` lọc `ClipCropTests` (gộp chung lượt Unity với Task 2). Mong đợi: hỏng.**
- [ ] **Step 3: Làm thật, chạy lại, thấy qua.**
- [ ] **Step 4: Commit.**

### Task 4: `ClipPlayer` và phần phát

**Files:**
- Create: `Assets/Scripts/Runtime/Video/IClipBackend.cs`, `VideoPlayerBackend.cs`, `ClipOverlay.cs`, `ClipPlayer.cs`
- Create: `Assets/Tests/Shared/FakeClipBackend.cs`
- Test: `Assets/Tests/PlayMode/ClipPlayerTests.cs`

**Interfaces:**
- Produces: `interface IClipBackend`:
  - `void Begin(Object clip)`: chuẩn bị và phát;
  - `void Stop()`: dừng và bỏ tham chiếu clip;
  - `void Release()`: nhả `RenderTexture`;
  - `bool FirstFrameReady { get; }`, `bool Finished { get; }`, `bool Failed { get; }`;
  - `Texture Texture { get; }`, `int Width { get; }`, `int Height { get; }`.
- Produces: `VideoPlayerBackend(GameObject host)`.
  - Tạo `VideoPlayer` và `AudioSource` khi `Begin` lần đầu.
  - `renderMode = RenderTexture`, `isLooping = false`, `playOnAwake = false`, `waitForFirstFrame = true`, `skipOnDrop = true`, `audioOutputMode = AudioSource`, `SetTargetAudioSource(0, source)`, âm lượng 1.
  - `clip` không phải `VideoClip` thì `Failed = true`.
  - `FirstFrameReady` bật khi nhận `frameReady` của khung đầu (`sendFrameReadyEvents` bật trong lúc chờ rồi tắt).
  - `Finished` bật khi nhận `loopPointReached`; `Failed` bật khi nhận `errorReceived`.
  - `RenderTexture` tạo theo cỡ clip và được xoá trắng trước mỗi clip.
- Produces: `sealed class ClipOverlay : MonoBehaviour`. Dấu nhận lớp phủ, nằm trên GameObject có `RawImage`, `CanvasGroup` và `AspectRatioFitter` (`FitInParent`).
- Produces: `sealed class ClipPlayer : MonoBehaviour`:
  - `static bool Enabled = true`;
  - `static Func<GameObject, IClipBackend> BackendFactory`;
  - `static Func<bool> DeviceCheck` (mặc định `ClipSupport.CurrentDevice`);
  - hằng `FadeInSeconds = .3f`, `FadeOutSeconds = .25f`, `StopFadeSeconds = .15f`, `FirstFrameTimeout = 3f`, `MaxFailures = 2`;
  - `static float TimeoutScale = 1f`: test thu ngắn thời gian chờ khung đầu;
  - `void Init(AssetCatalog catalog, SpeechPlayer speech)`;
  - `bool SettingEnabled { get; set; }`: gán `false` thì `Stop()`; gán `true` thì đặt lại số lần hỏng;
  - `bool CanPlay(string imageId)`;
  - `Awaitable<bool> PlayAsync(Tile tile, string imageId)`;
  - `void Stop()`, `void ReleaseAll()`;
  - `bool IsPlaying`, `string CurrentId`, `int Failures`;
  - `ClipOverlay ActiveOverlay` (internal).
- Hành vi bắt buộc (spec mục 5, 6, 10):
  - `PlayAsync` trả `false` ngay nếu không `CanPlay`, thẻ `null` hay `ImageBox` không hiện, hoặc `speech.IsBusy`.
  - Clip mới dừng clip cũ.
  - Lớp phủ nằm dưới `tile.ImageBox`, `alpha = 0` cho tới `FirstFrameReady`.
  - `uvRect` lấy từ `ClipCrop` với tỉ lệ của sprite trên thẻ.
  - Mỗi khung trong `Update`: `speech.IsBusy`, hoặc lớp phủ bị huỷ hay không còn hiện, thì `Stop()`.
  - `OnApplicationPause(true)` thì `Stop()`.
  - `IsPlaying` đúng từ `Begin` cho tới khi gỡ lớp phủ, hoặc tới lúc `Stop()`.

- [ ] **Step 1: Viết `FakeClipBackend`** (Shared): đếm `BeginCount`, `StopCount`, `ReleaseCount`; giữ `LastClip`; các cờ `FirstFrameReady`, `Finished`, `Failed` gán được; `Texture` là `Texture2D` 4×4; cỡ 1280×720.
- [ ] **Step 2: Viết test hỏng** `ClipPlayerTests`. Dựng `SpeechPlayer`, catalog giả có `(Clip, "img_a")` = một `Texture2D`, một `Tile` có sprite, `Motion.Scale = 0`, `ClipPlayer.DeviceCheck = () => true`, `BackendFactory` trả bản giả. Các test:
  - `PlayAsync_WhenSpeechIdle_BeginsAndShowsOverlayAfterFirstFrame`: trước `FirstFrameReady` thì `alpha == 0`; sau đó thì `alpha == 1` và `uvRect.width ≈ .5625`.
  - `PlayAsync_WhenSpeechBusy_DoesNotBegin`.
  - `SpeechStarts_StopsClipAndRemovesOverlay`.
  - `Finished_RemovesOverlayAndReturnsTrue`.
  - `Failed_ReturnsFalseKeepsPicture_LogsWarningOnce`: dùng `LogAssert.Expect(LogType.Warning, …)`.
  - `FirstFrameTimeout_CountsAsFailure`: dùng một hằng chờ ngắn dành cho test, ví dụ `ClipPlayer.TimeoutScale`.
  - `TwoFailuresInARow_TurnsClipsOff_SuccessResetsCount`.
  - `PlayAsync_SecondTile_StopsFirst`.
  - `PlayAsync_StopDuringWaitForFirstFrame_LeavesNoOverlay`.
  - `TileDestroyedWhilePlaying_StopsAndClearsState`.
  - `ReleaseAll_StopsAndReleasesBackend`.
  - `SettingOff_CannotPlay`; `SettingOffThenOn_PlaysAgain`.
  - `DeviceUnsupported_CannotPlay`; `Disabled_CannotPlay` (`Enabled = false`).
  - `MissingClip_CannotPlay_NoLogs`.
- [ ] **Step 3: Viết thân trống, chạy `playmode` lọc `ClipPlayerTests`. Mong đợi: hỏng.**
- [ ] **Step 4: Làm `ClipPlayer`, `ClipOverlay`, `VideoPlayerBackend`.** Mờ vào, mờ ra dùng `Motion.Fade`. Mỗi lần phát có một số thế hệ (như `SpeechPlayer`), để lần phát cũ thoát êm.
- [ ] **Step 5: Chạy lại, thấy qua. Commit.**

### Task 5: Bốn màn phát clip

**Files:**
- Modify: `Assets/Scripts/Runtime/App/LessonContext.cs` (`public ClipPlayer Clips;`)
- Modify: `Assets/Scripts/Runtime/Steps/StepViewBase.cs` (`protected void PlayClip(Tile tile, string imageId)`: không chờ, bỏ qua khi `Ctx.Clips == null` hay màn đã huỷ)
- Modify: `Assets/Scripts/Runtime/Steps/KeywordView.cs`, `ItemsView.cs`, `RiddleAnswerView.cs`, `SpellView.cs`
- Test: `Assets/Tests/PlayMode/ClipInViewsTests.cs` (dựa trên `ViewTestBase`, gắn `ClipPlayer` với bản giả vào `Ctx.Clips`)

**Interfaces:**
- Consumes: `ClipPlayer.PlayAsync`, `IsPlaying`, `CurrentId` (Task 4), `FakeClipBackend` (Task 4).
- Hành vi theo spec mục 4.
  - `KeywordView`: một hàm đọc `Read(bool picture, bool completes)`. Đọc trọn rồi: nếu `completes` thì `Complete()`; sau đó, nếu `picture` hoặc chưa tự phát lần nào, thì đánh dấu đã tự phát và `PlayClip`. Gọi hàm này ở 4 chỗ:
    - mở bước: `Read(false, false)`;
    - chạm chữ: `Read(false, true)`;
    - chạm tranh: `Read(true, true)`;
    - `Replay`: `Read(false, false)`.
  - `ItemsView` (`words`): giữ thẻ tranh theo chỉ số. Sau `Play(item.audio)` trả `true` thì `PlayClip`, đặt sau `Complete()` nếu có.
  - `RiddleAnswerView`: đọc đáp án trọn thì `Complete()` rồi `PlayClip(CorrectTile, Step.image)`. Sau khi xong, chạm tranh đáp án thì `PlayClip`, không đọc.
  - `SpellView`: ở `Finish`, giữ `Awaitable` của `Wiggle`, `Complete()`, chờ lắc xong rồi `PlayClip`. Thẻ tranh có `Tapped`: đã xong thì `PlayClip`.

- [ ] **Step 1: Viết test hỏng** `ClipInViewsTests`. Mỗi test lấy một bài thật có bước đó, đặt clip giả cho mã tranh, rồi điều khiển bản giả:
  - `Keyword_AutoPlaysAfterOpeningRead`: sau lần đọc đầu, `CurrentId == step.image` và bước chưa `Done`.
  - `Keyword_OpeningInterruptedByTextTap_PlaysAfterThatRead`.
  - `Keyword_AfterAutoPlay_TextTapDoesNotPlay_PictureTapDoes`: đếm `BeginCount`.
  - `Keyword_TapStillCompletesStep`.
  - `Words_PlaysAfterWordRead`: dùng `CompleteOverlaySpell` có sẵn.
  - `Riddle_CorrectAnswer_PlaysAnswerClip_CompletesWithoutWaiting`: `Done` đúng khi `IsPlaying` còn đúng.
  - `ToneAttach_PlaysAfterPictureShown`.
  - `NoClipsOnContext_ViewsBehaveAsBefore`: `Ctx.Clips = null`, không có ngoại lệ.
- [ ] **Step 2: Viết thân trống `PlayClip`, chạy `playmode` lọc `ClipInViewsTests`. Mong đợi: hỏng.**
- [ ] **Step 3: Sửa 4 màn. Chạy lại `ClipInViewsTests` cùng các lớp test sẵn có của 4 màn**: `ReadingStepTests`, `ItemsViewTests`, `SpellViewTests`, `NewStepViewTests`, `NewStepViewTests2`, `PreparedCoverageTests`. Mong đợi: qua. (Lỗi chỉ thuộc Tập 2 thì ghi lại, không đuổi theo.)
- [ ] **Step 4: Commit.**

### Task 6: Ráp vào app — `AppRoot`, màn học, Cài đặt

**Files:**
- Modify: `Assets/Scripts/Runtime/App/AppRoot.cs`:
  - `public ClipPlayer Clips { get; private set; }`, tạo sau `Sfx`, kèm `Clips.SettingEnabled = Progress.ClipsEnabled`;
  - `Clips.ReleaseAll()` trong `Present` cạnh `Speech.Stop()`, và trong `HoldSet` trước `old.Dispose()`.
- Modify: `Assets/Scripts/Runtime/App/LessonScreen.cs`:
  - `ctx.Clips = _app.Clips`;
  - `Update` và `TrackStudyTime` coi `_app.Clips.IsPlaying` là bận;
  - `OpenNotes` gọi `_app.Clips.Stop()`;
  - `TurnCurrentPage` huỷ mọi `ClipOverlay` trong bản sao ngay sau `Instantiate`.
- Modify: `Assets/Scripts/Runtime/Progress/ProgressData.cs` (`public bool clips_off;`), `ProgressStore.cs` (`ClipsEnabled`; `ResetAll` đặt `clips_off = false`)
- Modify: `Assets/Scripts/Runtime/Text/UiText.cs`: `ClipsOn = "Tranh động: Bật"`, `ClipsOff = "Tranh động: Tắt"`, thêm cả hai vào danh sách chữ cạnh `SfxOn`/`SfxOff` (dòng khoảng 227).
- Modify: `Assets/Scripts/Runtime/App/SettingsScreen.cs`: `public Button ClipsToggle`, hàng ngay dưới `SfxToggle`, `ToggleClips()` làm như `ToggleSfx`.
- Modify: `Assets/Tests/PlayMode/AppTestBase.cs`: `ClipPlayer.Enabled = false` ở `SetUpProgressStore`, trả `true` ở `TearDownApp`.
- Test: `Assets/Tests/EditMode/ProgressStoreTests.cs` (thêm), `Assets/Tests/PlayMode/ClipAppTests.cs` (mới, dựa trên `AppTestBase`)

- [ ] **Step 1: Viết test hỏng.**
  - `ProgressStoreTests`: `ClipsEnabled_DefaultOn`; `ClipsEnabled_SavedAndReloaded`; `OldFileWithoutField_ClipsOn`; `ResetAll_TurnsClipsOn`.
  - `ClipAppTests`: mỗi test tự bật `ClipPlayer.Enabled`, đặt `BackendFactory` giả, `DeviceCheck = () => true`; nguồn có clip giả cho tranh từ khoá của một bài.
    - `KeywordStep_ClipPlays_ThenNextStopsIt`;
    - `BackToList_StopsAndReleasesBeforeSetRelease`: bọc nguồn để ghi lúc `ReleaseUnused` có được gọi khi bản giả đã `Release`/`Stop` hay chưa;
    - `OpenNotes_StopsClip`;
    - `ClipPlaying_CountsAsBusyForNudge`: `IdleNudge.Enabled = true`, đồng hồ giả, không có nhắc trong lúc clip chạy;
    - `PageTurnCopy_HasNoOverlay`;
    - `Settings_ClipsToggle_ChangesLabelSavesAndDisables`;
    - `AppTestBase_LeavesClipPlayerEnabledAfterTest`.
- [ ] **Step 2: Viết thân trống, chạy `editmode` lọc `ProgressStoreTests` và `playmode` lọc `ClipAppTests|SettingsScreenTests`. Mong đợi: hỏng.**
- [ ] **Step 3: Làm thật. Chạy lại `ClipAppTests`, `SettingsScreenTests`, `LessonChromeTests`, `LessonGuideTests`, `AppFlowTests`, `ProgressStoreTests`, `UiStyleTests`, `GlyphInAppTests`. Mong đợi: qua.**
- [ ] **Step 4: Commit.**

### Task 7: Clip thật, ảnh chụp, báo root

**Files:**
- Test: `Assets/Tests/PlayMode/ClipRealVideoTests.cs` (`[Category("Clip")]`)
- Test: `Assets/Tests/PlayMode/ClipRealVideoTests.cs` cũng chụp ảnh vào `TestOutput/screens/<máy>/clip_*.png` (không commit)

- [ ] **Step 1: Chạy `python run_unity_media.py clips`** (Unity đóng). Mong đợi: chép mới 323, thiếu 0.
- [ ] **Step 2: Viết test.**
  - `RealClip_PreparesPlaysToEndAndRemovesOverlay`:
    - nạp `img_b01_bof` bằng `ResourcesContentSource`; không có file thì `Assert.Inconclusive`;
    - dùng `VideoPlayerBackend` thật, `AudioListener.volume = 0`;
    - có khung đầu trong 3 s; `uvRect.width ≈ .5625`; phát hết trong 12 s; lớp phủ được gỡ.
  - `RealClip_ImporterKeepsOriginal`: `VideoClipImporter` của file đó có `defaultTargetSettings.enableTranscoding == false`.
  - `Screens_KeywordClip`:
    - với `ScreenSizes.Phone20x9` và `ScreenSizes.IPad43`, mở bài của `img_b01_bof` bằng app thật, đi tới bước từ khoá;
    - chụp ở khoảng 3 s (`clip_loop_3s.png`) và sau khi clip hết (`clip_loop_het.png`);
    - với một clip `build` cây hay hoa (chọn từ `tranh_dong_kich_ban.json`, `mode = build`, `status = dat`), chụp ở 0,2 s (`clip_build_0_2s.png`) và 3 s (`clip_build_3s.png`).
- [ ] **Step 3: Xin root lượt Unity.** Mở Unity batchmode để nhập clip, rồi chạy `playmode` lọc `ClipRealVideoTests`. Mong đợi: qua, có 8 ảnh. Tự xem ảnh trước khi gửi:
  - không lộ dải giấy đệm;
  - tranh trong clip trùng chỗ tranh tĩnh;
  - không có khung đen.
- [ ] **Step 4: Commit theo đường dẫn** (test, `packages-lock.json`). Gửi root:
  - mã các commit;
  - kết quả các lớp test đã chạy;
  - đường dẫn ảnh (chép ảnh vào thư mục ghi chú chung `tranh-dong-app/`);
  - nhắc root: trước khi build Windows thì chạy lệnh `clips`.
