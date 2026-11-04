# Dọn cách app đọc dữ liệu — Kế hoạch triển khai

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Mục tiêu:** mọi chỗ đọc bài học, Phụ lục, tranh, âm thanh, tiếng động và font đi qua một lớp nguồn dữ liệu duy nhất. Nạp theo bộ, có chờ, có nhả. Màn chuyển gà con khi mở bài. Chưa làm Addressables.

**Kiến trúc:**
- `IContentSource` là tầng dưới: nạp theo loại + mã, không có bộ nhớ đệm. Đợt này chỉ có bản Resources.
- `AssetCatalog` (giữ tên) và `LessonRepository` (thành lớp có đối tượng) là tầng trên: có bộ nhớ đệm và đếm chỗ giữ.
- `AppRoot` giữ bộ chung và bộ của màn hiện tại, nạp có chờ khi mở bài, ôn lại và màn Phụ huynh.
- Các màn bước học và lượt luyện tập (`Steps/`, `Exercises/`) không đổi.

**Công nghệ:** Unity 6.6 (`6000.6.5f1`), C# `Awaitable`, `Resources.LoadAsync`, Unity Test Framework (EditMode, PlayMode).

**Bản thiết kế:** [2026-11-04-doc-du-lieu-design.md](../specs/2026-11-04-doc-du-lieu-design.md), đã được duyệt ngày 04/11/2026. Executor đọc cả bản thiết kế lẫn kế hoạch này.

## Global Constraints

- Chỉ dùng branch `main`, mỗi task một commit (hoặc vài commit rõ ràng). Không squash, không force push, không push; chủ dự án tự push. Không build Windows/Android.
- Trước khi sửa thì chạy `git status`. Chỉ commit file của task mình; không đụng file session khác đang sửa dở.
- Chạy test bằng `python tools/run_unity_tests.py editmode|playmode --filter <Lớp>` (gõ từ thư mục gốc repo), sau khi đã đóng Unity Editor. Mỗi lúc chỉ một tiến trình dùng Unity.
  - **Chỉ chạy các lớp test liên quan.** Không chạy `MvpEndToEndTests`, `PrototypeEndToEndTests` hay toàn bộ PlayMode khi chủ dự án chưa nói "test all".
- Claude viết và review mọi test. Worker (Codex/Antigravity) chỉ viết code cho test của Claude chạy xanh, không sửa test. Phần giao diện và hiệu ứng (Task 7) Claude tự làm.
- Không đổi:
  - cấu trúc `Assets/Content/Resources/`, file `.meta` của tranh và âm thanh, cài đặt nhập trong `Scripts/Editor/ContentImportRules.cs`;
  - định dạng JSON, công cụ Python, mã tranh và mã âm thanh.
- Thông điệp giữ nguyên từng chữ:
  - `[TapDoc] Thiếu âm thanh: <mã>` (lỗi);
  - `[TapDoc] Thiếu tranh: <mã>` (lỗi);
  - `[TapDoc] Thiếu tiếng động: <mã>` (cảnh báo);
  - các `InvalidDataException` của `LessonRepository` và `AppendixData`.
- Thông điệp mới: `[TapDoc] Chưa chuẩn bị trước: <mã>` (cảnh báo, mỗi mã một lần).
- Sau Task 9, `Resources.Load` và tên thư mục `"audio/"`, `"images/"`, `"sfx/"`, `"lessons/"`, `"appendix/"`, `"fonts/"` chỉ còn trong `ContentPaths.cs` và `ResourcesContentSource.cs`. Ngoại lệ: `TMP Settings` của TextMeshPro trong `SetupTests`.
- Test PlayMode tắt hiệu ứng (`Motion.Scale = 0`) như hiện nay.

## Review Focus

1. **Chạm lần nữa trong lúc đang chuẩn bị** (chạm lại bài, bấm nút khác): bị bỏ qua, chỉ mở một màn. Test ở Task 6.
2. **AppRoot bị huỷ giữa lúc đang chuẩn bị** (đổi scene, test dọn dẹp): phần chạy tiếp sau `await` không đụng vào đối tượng đã huỷ, không ném lỗi. Test ở Task 6.
3. **Một mã vừa nằm trong bộ chung vừa nằm trong bộ bài** (ví dụ `hd_nghe_chon_tranh` là `instruction_audio` trong JSON): nhả bộ bài thì mã đó không bị nhả. Test ở Task 3.
4. **"Bài tiếp" ở màn kết quả mà bài sau hỏng file:** ở lại màn kết quả, bộ cũ vẫn giữ, nút vẫn bấm được. Test ở Task 6.
5. **Bộ có file thiếu:** bộ vẫn chuẩn bị xong, báo lỗi một lần, vẫn vào bài. Test ở Task 3 (catalog) và Task 6 (luồng mở bài).

---

## Cấu trúc file

| File | Việc |
|---|---|
| Tạo `Scripts/Runtime/Content/ContentKind.cs` | `enum ContentKind { LessonIndex, Lesson, Appendix, Image, Speech, Sfx, Font, Clip }` |
| Tạo `Scripts/Runtime/Content/ContentPaths.cs` | Chỗ duy nhất biết thư mục và kiểu Unity của từng loại |
| Tạo `Scripts/Runtime/Content/IContentSource.cs` | Giao diện nguồn dữ liệu |
| Tạo `Scripts/Runtime/Content/ResourcesContentSource.cs` | Bản đọc Resources |
| Tạo `Scripts/Runtime/Content/ContentSet.cs` | Tay cầm của một bộ đang giữ (`IDisposable`) |
| Sửa `Scripts/Runtime/Content/AssetCatalog.cs` | Nạp qua nguồn, bộ nhớ đệm, đếm, bộ chung, cảnh báo chưa chuẩn bị |
| Sửa `Scripts/Runtime/Data/LessonRepository.cs`, `AppendixData.cs`, `LessonAssets.cs` | Kho bài có đối tượng; `ContentIds`; `readings` |
| Sửa `Scripts/Runtime/Text/FontProvider.cs` | Lấy font từ catalog |
| Sửa `Scripts/Runtime/App/AppRoot.cs` | Khởi động có chờ, luồng chuẩn bị, giữ và nhả bộ |
| Tạo `Scripts/Runtime/UI/PrepareCurtain.cs` | Màn chuyển gà con |
| Sửa các màn gọi `LessonRepository` tĩnh, `ProfileScreen`, `ParentScreen`, `SpeechPlayer`, `SfxPlayer` | Theo từng task |
| Tạo `Tests/Shared/TapDoc.Tests.Shared.asmdef`, `Tests/Shared/FakeContentSource.cs`, `Tests/Shared/AwaitableTestUtil.cs` | Đồ dùng test chung cho EditMode và PlayMode |

(Mọi đường dẫn tính từ `unity/TapDoc/Assets/`.)

---

### Task 1: Loại dữ liệu, đường dẫn, nguồn Resources, nguồn giả cho test

**Files:**
- Create: `Scripts/Runtime/Content/ContentKind.cs`, `ContentPaths.cs`, `IContentSource.cs`, `ResourcesContentSource.cs`
- Create: `Tests/Shared/TapDoc.Tests.Shared.asmdef` (tham chiếu `TapDoc.Runtime`; `defineConstraints: ["UNITY_INCLUDE_TESTS"]`; `autoReferenced: false`), `Tests/Shared/FakeContentSource.cs`, `Tests/Shared/AwaitableTestUtil.cs`
- Modify: hai asmdef `Tests/EditMode/TapDoc.Tests.EditMode.asmdef` và `Tests/PlayMode/TapDoc.Tests.PlayMode.asmdef`: thêm tham chiếu `TapDoc.Tests.Shared`
- Test: `Tests/EditMode/ContentPathsTests.cs`, `Tests/PlayMode/ResourcesContentSourceTests.cs`

**Interfaces:**
- Produces:
  - `static class ContentPaths { string PathOf(ContentKind kind, string id); Type TypeOf(ContentKind kind); }`
    - `LessonIndex` → `"lessons/index"`, bỏ qua `id`;
    - `Lesson` → `"lessons/" + id`; `Appendix` → `"appendix/" + id`; `Image` → `"images/" + id`; `Speech` → `"audio/" + id`; `Sfx` → `"sfx/" + id`; `Font` → `"fonts/" + id`; `Clip` → `"clips/" + id`;
    - kiểu: `TextAsset` cho ba loại chữ, `Sprite`, `AudioClip` (Speech và Sfx), `Font`, `UnityEngine.Video.VideoClip`.
  - `interface IContentSource`:
    - `Awaitable<Object> LoadAsync(ContentKind kind, string id)`;
    - `Object Load(ContentKind kind, string id)`;
    - `void Release(ContentKind kind, string id, Object asset)`;
    - trả `null` khi không có file, không ghi log.
  - `sealed class ResourcesContentSource : IContentSource`: dùng `Resources.LoadAsync(path, type)` và `Resources.Load(path, type)`; `Release` không làm gì.
  - Trong test, `FakeContentSource : IContentSource`:
    - `void Put(ContentKind kind, string id, Object asset)`;
    - `int DelayFrames { get; set; }`: `LoadAsync` chờ ngần ấy khung hình (`Awaitable.NextFrameAsync`) trước khi trả;
    - `int LoadCount(ContentKind, string)`, `int ReleaseCount(ContentKind, string)`;
    - `Func<ContentKind, string, Object> Fallback { get; set; }`: dùng khi không có mã đã `Put`;
    - helper tĩnh `static Sprite NewSprite()` và `static AudioClip NewClip()`.
  - Trong test, `AwaitableTestUtil`:
    - `IEnumerator Wait(Awaitable a)`;
    - `IEnumerator Wait<T>(Awaitable<T> a, Action<T> done)`: `yield return null` đến khi `GetAwaiter().IsCompleted`, rồi `GetResult()` (để lỗi trong awaitable ném ra test).

- [ ] **Step 1: Viết test (FAIL vì chưa có lớp)**

`ContentPathsTests`:
- `PathOf_EachKind`: assert từng ánh xạ ở trên. Ví dụ `PathOf(ContentKind.Speech, "van_o") == "audio/van_o"` và `PathOf(ContentKind.LessonIndex, null) == "lessons/index"`.
- `TypeOf_EachKind`: `TypeOf(Image) == typeof(Sprite)`, `TypeOf(Clip) == typeof(VideoClip)`, …

`ResourcesContentSourceTests` (`[UnityTest]`):
- `LoadAsync_RealFiles_EachKind`: dùng `AwaitableTestUtil.Wait`. Mỗi loại nạp được một file thật và đúng kiểu:
  - `Image "img_chung_ga_con"` → `Sprite`;
  - `Speech "am_b"` → `AudioClip`;
  - `Sfx "sfx_cham"` → `AudioClip`;
  - `Lesson "tv1_t1_b01"`, `LessonIndex`, `Appendix "tv1_t1_1990"` → `TextAsset`;
  - `Font "Andika-Regular"` → `Font`.
- `LoadAsync_Missing_ReturnsNullWithoutLog`: `Image "khong_co"` → `null`, `LogAssert.NoUnexpectedReceived()`.
- `Load_Sync_SameAsAsync`: `Load(Speech,"am_b")` là cùng đối tượng với bản async.

- [ ] **Step 2:** Chạy `python tools/run_unity_tests.py editmode --filter ContentPathsTests`. Kỳ vọng FAIL (lỗi biên dịch).
- [ ] **Step 3:** Viết các lớp ở mục Interfaces.
- [ ] **Step 4:** Chạy `editmode --filter ContentPathsTests` và `playmode --filter ResourcesContentSourceTests`. Kỳ vọng PASS.
- [ ] **Step 5:** Commit `feat(content): nguồn dữ liệu theo loại và mã, bản đọc Resources`.

---

### Task 2: `LessonAssets` đủ mã (`readings`) và `ContentIds`

**Files:**
- Modify: `Scripts/Runtime/Data/LessonAssets.cs`
- Test: `Tests/EditMode/DataTests.cs` (thêm test)

**Interfaces:**
- Produces: `static IEnumerable<(ContentKind kind, string id)> ContentIds(Lesson lesson)`. Gồm `(Speech, id)` cho mọi `AudioIds` và `(Image, id)` cho mọi `ImageIds`, không trùng.
- `AudioIds` thêm `step.readings[].audio`.

- [ ] **Step 1: Test**
- `AudioIds_IncludesReadings`: dựng một `Lesson` trong bộ nhớ, có một bước `unit` với hai `readings` có audio `"r1"`, `"r2"`. Assert `AudioIds` chứa cả hai.
- `ContentIds_IsUnionOfAudioAndImage`: với `tv1_t1_b17` đọc bằng `LessonRepository.Parse(((TextAsset)new ResourcesContentSource().Load(ContentKind.Lesson, "tv1_t1_b17")).text)` (chưa đổi kho ở task này), assert tập `ContentIds` bằng `AudioIds` gắn `Speech` hợp với `ImageIds` gắn `Image`.
- [ ] **Step 2:** `editmode --filter DataTests` FAIL.
- [ ] **Step 3:** Sửa `LessonAssets`.
- [ ] **Step 4:** `editmode --filter DataTests` PASS. Lúc này `AllReferencedAssetsExist` đã kiểm tra cả 47 âm thanh `readings`, và các file này đều có.
- [ ] **Step 5:** Commit `fix(data): danh sách âm thanh của bài gồm cả các cách đọc (readings)`.

---

### Task 3: `AssetCatalog` nạp qua nguồn, bộ, đếm, bộ chung

**Files:**
- Create: `Scripts/Runtime/Content/ContentSet.cs`
- Modify: `Scripts/Runtime/Content/AssetCatalog.cs`
- Modify (để biên dịch được, chưa đổi hành vi):
  - `App/AppRoot.cs`: thay `CatalogFactory` bằng `internal static Func<IContentSource> SourceFactory`;
  - `Audio/SpeechPlayer.cs`, `Audio/SfxPlayer.cs`: bỏ `?? new AssetCatalog()`; `Init(null)` thì `throw new ArgumentNullException`;
  - `App/ProfileScreen.cs:123`: thay bằng `assets.HasImage(avatarId)`;
  - các test `Tests/PlayMode/ViewTestBase.cs`, `AppTestBase.cs` (gồm `UseStubsForMissingAssets` qua `FakeContentSource.Fallback`), `AppFlowTests.cs`, `Tests/EditMode/UiStyleTests.cs`, `AssetSwapTests.cs`, `DataTests.AssetCatalog_Missing_LogsOnceAndReturnsNull`.
- Test: `Tests/PlayMode/AssetCatalogTests.cs`

**Interfaces:**
- Consumes: `IContentSource`, `ContentKind` (Task 1). Trong test: `FakeContentSource`, `AwaitableTestUtil`.
- Produces:
  - `AssetCatalog(IContentSource source)`;
  - `Sprite Image(string id)`, `AudioClip Audio(string id)`, `AudioClip Sfx(string id)`: hành vi khi thiếu như cũ;
  - `bool HasImage(string id)`: không ghi log;
  - `Awaitable PrepareCommonAsync()`: nạp bộ chung, giữ mãi. Gồm `SystemAudio.All`, `SystemImages.All`, `SystemSfx.All`, `ProfileScreen.Avatars` (không bắt buộc) và `(Font, "Andika-Regular")`. Hằng tên font đặt ở `FontProvider.MainFontId`;
  - `Awaitable<ContentSet> PrepareAsync(IEnumerable<(ContentKind kind, string id)> ids)`;
  - `Awaitable<AudioClip> AudioAsync(string id, ContentSet holder)`: nạp lẻ, tính vào `holder`;
  - `Font Font(string id)`;
  - `IReadOnlyCollection<string> UnpreparedAsks`;
  - `ContentSet CurrentHolder { get; set; }`: bộ nhận các file nạp lẻ (`AudioAsync`, hỏi khi chưa chuẩn bị). `PrepareAsync` với danh sách rỗng trả một bộ rỗng, dùng được làm `CurrentHolder`;
  - `ContentSet : IDisposable`: `Dispose()` nhả mỗi mã một lần, gọi lại không có tác dụng.
- Quy tắc:
  - mỗi `(kind, id)` có một bản ghi `{ asset, refCount }`. Nạp nguồn đúng một lần khi `refCount` đi từ 0 lên 1. Về 0 thì gọi `source.Release`, và với `AudioClip` gọi thêm `UnloadAudioData()`;
  - bộ chung giữ thêm một chỗ vĩnh viễn;
  - âm thanh (`Speech`, `Sfx`) nạp xong thì gọi `LoadAudioData()` và chờ `loadState != Loading`. Nếu `Failed` thì coi như thiếu;
  - hỏi `Image/Audio/Sfx` khi chưa giữ: nạp ngay bằng `source.Load`, ghi `[TapDoc] Chưa chuẩn bị trước: <mã>` (cảnh báo, một lần), thêm vào `UnpreparedAsks`. Bản ghi này được tính vào `ContentSet` đang làm "bộ hiện tại" (`CurrentHolder`, do `AppRoot` đặt ở Task 6). Không có bộ hiện tại thì giữ đến khi app tắt;
  - mã không bắt buộc thì không ghi log khi thiếu.

- [ ] **Step 1: Test `AssetCatalogTests`** (`[UnityTest]`, nguồn giả):
  - `Prepare_LoadsEachIdOnce_EvenWhenTwoSetsHoldIt`: hai bộ cùng chứa `img_a` → `LoadCount == 1`.
  - `Dispose_ReleasesAtZero`: nhả bộ thứ nhất thì `ReleaseCount == 0`; nhả bộ thứ hai thì `== 1`; `Dispose` lần nữa vẫn `== 1`.
  - `CommonSet_NeverReleased_EvenIfLessonSetHasSameId` (Review Focus 3): sau `PrepareCommonAsync`, một bộ bài chứa `(Speech,"hd_nghe_chon_tranh")`; nhả bộ bài → `ReleaseCount == 0`; `Audio("hd_nghe_chon_tranh")` không ghi cảnh báo.
  - `Prepare_MissingFile_LogsOnceAndCompletes` (Review Focus 5): `LogAssert.Expect(Error, "[TapDoc] Thiếu tranh: img_x")`; bộ vẫn xong; `Image("img_x") == null` mà không log thêm.
  - `MissingSfx_IsWarning`: `"[TapDoc] Thiếu tiếng động: sfx_x"` ở mức cảnh báo.
  - `OptionalAvatar_Missing_NoLog`: sau `PrepareCommonAsync` với nguồn thiếu `img_chung_avatar_03`, `HasImage` trả `false`, `NoUnexpectedReceived`.
  - `UnpreparedAsk_StillReturns_WarnsOnce_Recorded`: `Image("img_b")` (nguồn có) khi chưa chuẩn bị → khác `null`, `LogAssert.Expect(Warning, "[TapDoc] Chưa chuẩn bị trước: img_b")` một lần dù gọi hai lần, `UnpreparedAsks` chứa `img_b`.
  - `PreparedAudio_IsLoaded`: clip trong bộ có `loadState == AudioDataLoadState.Loaded`.
  - `AudioAsync_CountsIntoHolder`: nạp lẻ `am_b` vào `holder`; `holder.Dispose()` → `ReleaseCount == 1`.
  - `Prepare_WaitsForSlowSource`: `DelayFrames = 3` → sau 1 khung chưa xong, sau 3 khung thì xong.

  Chuyển `DataTests.AssetCatalog_Missing_LogsOnceAndReturnsNull` sang `new AssetCatalog(new FakeContentSource())`. Hỏi mã chưa giữ mà nguồn không có thì chỉ có lỗi "Thiếu", không có cảnh báo "Chưa chuẩn bị".
- [ ] **Step 2:** `playmode --filter AssetCatalogTests` FAIL.
- [ ] **Step 3:** Viết `ContentSet`, `AssetCatalog`, rồi sửa các chỗ gọi đã liệt kê. `AppRoot` tạm thời: `var source = SourceFactory?.Invoke() ?? new ResourcesContentSource(); Assets = new AssetCatalog(source);`.
- [ ] **Step 4:** Chạy:
  - `playmode --filter AssetCatalogTests;AppFlowTests;ProfileScreenTests;SpeechPlayerTests;SfxPlayerTests;Part1ViewTests;RoundViewTests`;
  - `editmode --filter DataTests;UiStyleTests;AssetSwapTests`.

  Kỳ vọng PASS. Cảnh báo "Chưa chuẩn bị trước" là bình thường cho đến Task 6.
- [ ] **Step 5:** Commit `feat(content): AssetCatalog nạp qua nguồn dữ liệu, theo bộ, có đếm và nhả`.

---

### Task 4: Kho bài có đối tượng, Phụ lục qua nguồn

**Files:**
- Modify: `Scripts/Runtime/Data/LessonRepository.cs`, `Data/AppendixData.cs`, `App/AppRoot.cs` (thuộc tính `Lessons`)
- Modify (đổi chỗ gọi tĩnh sang `app.Lessons`): `App/BookScreen.cs:50`, `LessonListScreen.cs:104`, `ParentScreen.cs:164,191-193,284`, `ResultScreen.cs:96,262`, `AppRoot.cs:183,199`
- Modify test: `Tests/EditMode/DataTests.cs`, `NotesDataTests.cs`, `FlowTests.cs`, `Tests/PlayMode/AppTestBase.cs` (`Ordered()`), `ReviewSessionTests.cs`, `ParentScreenTests.cs` và các lớp còn gọi `LessonRepository.Load`/`LoadIndex` tĩnh hoặc `AppendixData.Load` (dùng `grep` để tìm)
- Test: `Tests/EditMode/LessonRepositoryTests.cs`

**Interfaces:**
- Consumes: `IContentSource`, `ContentKind`.
- Produces:
  - `LessonRepository(IContentSource source)`;
  - `Awaitable<LessonIndex> LoadIndexAsync()`, `LessonIndex Index { get; }`;
  - `Awaitable<Lesson> LoadAsync(string id)`, `Lesson Get(string id)`;
  - `Awaitable LoadAllAsync()`: nạp đủ các bài trong `Index`;
  - `Awaitable<Appendix> LoadAppendixAsync(string book)`, `Appendix Appendix(string book)`;
  - giữ `static Lesson Parse(string json)` và `internal static string Nfc(string)`.
  - `AppendixData` giữ các lớp dữ liệu. `Load(string)` thành `internal static Appendix Parse(string json, string book)` (chuẩn hoá như cũ).
  - `AppRoot.Lessons`.
- Quy tắc:
  - `Get` và `Index` đọc từ bộ nhớ đệm. Chưa có thì nạp ngay bằng `source.Load` và ghi `[TapDoc] Chưa chuẩn bị trước: <mã>` một lần (với danh sách bài dùng mã `"lessons/index"`);
  - thiếu hoặc hỏng file thì ném đúng các `InvalidDataException` cũ, ở cả bản có chờ lẫn bản nạp ngay;
  - mỗi file chỉ được đọc qua nguồn một lần.
- Trong test EditMode cần dữ liệu thật, dùng `new LessonRepository(new ResourcesContentSource())` với `Get`/`Index`; cảnh báo "Chưa chuẩn bị" ở đây chấp nhận được. Gom vào một helper tĩnh `TestLessons.Real` trong `Tests/Shared`.

- [ ] **Step 1: Test `LessonRepositoryTests`** (EditMode, nguồn giả với `TextAsset` dựng từ chuỗi JSON):
  - `Get_ReadsSourceOnce`: gọi `Get("b")` hai lần → `LoadCount(Lesson,"b") == 1`.
  - `Get_NormalizesNfc`: JSON có tiêu đề ở dạng NFD → `title` ra NFC.
  - `Get_Missing_ThrowsOldMessage`: `"Không tìm thấy bài học: x"`.
  - `Get_Broken_PrefixesLessonId`: thông điệp bắt đầu bằng `"Bài x: "`.
  - `Appendix_ReadsOnce_AndNormalizes`.
  - `Index_Missing_ThrowsOldMessage`: `"Không tìm thấy hoặc hỏng lessons/index.json"`.

  Sửa `AllReferencedAssetsExist`: đi qua `ResourcesContentSource.Load(kind, id)` theo `LessonAssets.ContentIds` của mọi bài, cộng thêm mã chung. Không còn chuỗi `"audio/"`, `"images/"`, `"sfx/"` trong `DataTests`; kiểm tra "tiếng động không nằm trong audio/" dùng `Load(ContentKind.Speech, id) == null`.
- [ ] **Step 2:** `editmode --filter LessonRepositoryTests` FAIL.
- [ ] **Step 3:** Sửa kho bài, Phụ lục và các chỗ gọi.
- [ ] **Step 4:** Chạy:
  - `editmode --filter LessonRepositoryTests;DataTests;NotesDataTests;FlowTests`;
  - `playmode --filter ReviewSessionTests;ParentScreenTests;LessonListScrollTests;BookScreenTests;ResultSceneTests`.

  Kỳ vọng PASS.
- [ ] **Step 5:** Commit `refactor(data): kho bài có bộ nhớ đệm, đọc bài và Phụ lục qua nguồn dữ liệu`.

---

### Task 5: Khởi động chờ bộ chung, font qua catalog

**Files:**
- Modify: `Scripts/Runtime/Text/FontProvider.cs`, `App/AppRoot.cs` (`TryBootMainScene`)
- Modify test: `Tests/PlayMode/AppTestBase.cs` (`LoadMainScene` chờ đến khi có `ProfileScreen`, tối đa 120 khung), `Tests/EditMode/SetupTests.cs` (`AndikaFontLoads` dùng `ResourcesContentSource`)
- Test: `Tests/PlayMode/AppBootTests.cs`

**Interfaces:**
- Consumes: `AssetCatalog.PrepareCommonAsync`, `AssetCatalog.Font`, `LessonRepository.LoadIndexAsync`, `LoadAppendixAsync`.
- Produces:
  - `FontProvider.MainFontId = "Andika-Regular"`;
  - `FontProvider.Main` lấy `AppRoot.Instance?.Assets.Font(MainFontId)`. Khi chưa có `AppRoot` (test EditMode dựng giao diện), dùng một `AssetCatalog` riêng trên `ResourcesContentSource`, tạo một lần. `TMP_FontAsset` vẫn tạo một lần;
  - `AppRoot.IsReady { get; }`: `true` sau khi bộ chung, danh sách bài và Phụ lục của sách đã nạp.
- Khởi động:
  - `TryBootMainScene` chạy một `async Awaitable`: chờ `PrepareCommonAsync`, `Lessons.LoadIndexAsync()` và `Lessons.LoadAppendixAsync(index.lessons[0].book)`, rồi `ShowProfiles()`;
  - sau mỗi `await`, nếu `this == null` thì dừng (Review Focus 2);
  - lỗi nạp thì `Debug.LogError` kèm thông điệp, không ném ra ngoài.

- [ ] **Step 1: Test `AppBootTests`:**
  - `Boot_ShowsProfiles_OnlyAfterCommonReady`: nguồn giả với `DelayFrames = 5` (`Fallback` trả sprite/clip trơn, có `index` và Phụ lục thật). Ở khung 1 chưa có `ProfileScreen`; khi `IsReady` thì có `ProfileScreen`.
  - `Boot_NoUnpreparedAsks_OnProfileAndList`: dùng nguồn Resources thật; vào màn chọn bé rồi danh sách bài → `Assets.UnpreparedAsks` rỗng.
- [ ] **Step 2:** `playmode --filter AppBootTests` FAIL.
- [ ] **Step 3:** Sửa `FontProvider`, `AppRoot`, `AppTestBase.LoadMainScene`.
- [ ] **Step 4:**
  - `playmode --filter AppBootTests;ProfileScreenTests;AppFlowTests;LessonListStyleTests`;
  - `editmode --filter SetupTests;UiStyleTests`.

  Kỳ vọng PASS.
- [ ] **Step 5:** Commit `feat(app): khởi động chờ nạp bộ chung; font lấy qua catalog`.

---

### Task 6: Luồng chuẩn bị bài và ôn lại, giữ và nhả bộ

**Files:**
- Modify: `Scripts/Runtime/App/AppRoot.cs`
- Create: `Scripts/Runtime/UI/PrepareCurtain.cs`. Ở task này chỉ là lớp phủ trơn chặn chạm (`Image` trong suốt có `raycastTarget`, đặt trên cùng `SafeRoot`) với `Show()` và `Hide()`. Hình gà con làm ở Task 7.
- Modify test: thêm vào `AppTestBase` helper `protected IEnumerator OpenLesson(string id)`, gọi `ShowLesson` rồi chờ `!AppRoot.Instance.IsPreparing`. Chuyển các chỗ đang `ShowLesson(...); yield return null;` sang helper này: `GlyphInAppTests`, `LessonChromeTests`, `LessonNotesTests`, `ProfileScreenTests`, `ItemsViewTests`, `LessonFeedbackFxTests`, `ResultSceneTests`, `AppFlowTests`, `NewStepViewTests2`, `RimeGridViewTests`, `RoundViewTests` (lấy danh sách bằng `grep "ShowLesson\|ShowReview"`). `MvpEndToEndTests` và `PrototypeEndToEndTests` sửa cho biên dịch được nhưng **không chạy**.
- Test: `Tests/PlayMode/PrepareFlowTests.cs`

**Interfaces:**
- Consumes: `AssetCatalog.PrepareAsync`, `ContentSet`, `CurrentHolder`, `LessonRepository.LoadAsync`, `LessonAssets.ContentIds`, `ReviewSession.Build`.
- Produces:
  - `bool AppRoot.IsPreparing { get; }`;
  - `void ShowLesson(string id)`, `void ShowLesson(Lesson lesson)`, `void ShowReview()`: chữ ký giữ nguyên (nút vẫn gọi được), bên trong chạy luồng có chờ. Đang chuẩn bị thì lời gọi mới bị bỏ qua.
- Luồng `ShowLesson(id)`:
  1. bật `IsPreparing`, `PrepareCurtain.Show()`;
  2. `await Lessons.LoadAsync(id)`;
  3. `await Assets.PrepareAsync(LessonAssets.ContentIds(lesson))`;
  4. dựng màn bài;
  5. nhả bộ cũ, đặt bộ mới làm `_currentSet` và `Assets.CurrentHolder`;
  6. `Hide()`, tắt `IsPreparing`, rồi gọi `Resources.UnloadUnusedAssets()` (không chờ).
- Lỗi ở bước 2–3 (`InvalidDataException`): `Debug.LogError`, `Hide()`, giữ nguyên màn và bộ hiện tại (Review Focus 4).
- `ShowReview`: nạp có chờ các bài mà các lượt cần ôn trỏ tới, rồi `ReviewSession.Build(Progress, Lessons.Get)`, rồi đi tiếp như bước 3–6 với `ContentIds(session.Lesson)`. Không còn lượt nào thì về danh sách bài như cũ.
- Nhả bộ hiện tại (đặt `Assets.CurrentHolder = null`) khi gọi `ShowLessonList`, `ShowProfiles`, `ShowBook`, `ShowParent`. **`ShowResult` không nhả.**
- Sau mỗi `await`, nếu `this == null` thì nhả bộ vừa nạp (nếu có) rồi dừng.

- [ ] **Step 1: Test `PrepareFlowTests`** (nguồn giả `DelayFrames = 3`, tranh và âm thanh trơn qua `Fallback`, bài thật qua `Fallback` sang Resources cho loại chữ):
  - `ShowLesson_ScreenAppearsOnlyAfterPrepared`: khung 1 có `PrepareCurtain` đang hiện và chưa có `LessonScreen`; khi `!IsPreparing` thì có `LessonScreen` và lớp phủ đã ẩn.
  - `DoubleTap_OpensOnce` (Review Focus 1): gọi `ShowLesson` hai lần liền → chỉ một `LessonScreen`; mỗi mã của bài có `LoadCount == 1`.
  - `BackToList_ReleasesLessonSet`: mở bài rồi `ShowLessonList` → mọi mã của bài có `ReleaseCount == 1`.
  - `ResultScreen_KeepsSet_NextLessonReusesShared`: mở `tv1_t1_b16`, `ShowResult`, rồi `ShowLesson("tv1_t1_b17")` → mã chung của hai bài (ví dụ `am_b`) có `LoadCount == 1` và `ReleaseCount == 0`; mã chỉ có ở bài 16 có `ReleaseCount == 1`.
  - `NextLesson_Broken_StaysOnResult` (Review Focus 4): nguồn trả JSON hỏng cho bài sau → `LogAssert.Expect(Error, …)`, vẫn ở `ResultScreen`, lớp phủ ẩn, bộ bài trước chưa bị nhả, nút "Bài tiếp" vẫn bấm được.
  - `MissingPicture_StillEntersLesson` (Review Focus 5): nguồn thiếu một tranh của bài → có `LessonScreen`, đúng một lỗi `[TapDoc] Thiếu tranh: …`.
  - `AppDestroyedWhilePreparing_NoErrors` (Review Focus 2): `ShowLesson` rồi huỷ `AppRoot` ở khung 1, chờ 5 khung → không có lỗi.
  - `Review_PreparesRoundsFromSeveralLessons`: kho có lỗi ở hai bài → mở ôn lại xong thì `UnpreparedAsks` rỗng.
- [ ] **Step 2:** `playmode --filter PrepareFlowTests` FAIL.
- [ ] **Step 3:** Sửa `AppRoot`, tạo `PrepareCurtain` trơn, chuyển test sang `OpenLesson`.
- [ ] **Step 4:** Chạy `playmode --filter PrepareFlowTests;AppFlowTests;ReviewSessionTests;ResultSceneTests;LessonChromeTests;LessonNotesTests;GlyphInAppTests;ProfileScreenTests;ItemsViewTests;LessonFeedbackFxTests;NewStepViewTests2;RimeGridViewTests;RoundViewTests`. Kỳ vọng PASS.
- [ ] **Step 5:** Commit `feat(app): chuẩn bị bài và ôn lại có chờ, giữ và nhả bộ tranh, âm thanh`.

---

### Task 7: Màn chuyển gà con (Claude tự làm)

**Files:**
- Modify: `Scripts/Runtime/UI/PrepareCurtain.cs`
- Test: `Tests/PlayMode/PrepareFlowTests.cs` (thêm)

**Interfaces:**
- Consumes: `SystemImages.Mascot` (đã có trong bộ chung), `Palette`, `Motion`, `UiKit`, `Mascot` nếu dùng lại được.
- Produces:
  - `PrepareCurtain.Show()` / `Hide()` như cũ;
  - `const float MinSeconds = .4f`: `Hide()` chờ đủ `MinSeconds * Motion.Scale` kể từ lúc `Show()`;
  - `bool IsShowing`.
- Hình và chuyển động theo phong cách của [thiết kế giao diện](../specs/2026-10-30-ui-hieu-ung-design.md): nền giấy, gà con giữa màn, chuyển mờ vào và mờ ra.

- [ ] **Step 1: Test:**
  - `Curtain_ShowsMascot`: lúc đang chuẩn bị, trong lớp phủ có `Image` dùng sprite `img_chung_ga_con`.
  - `Curtain_MinDuration_WhenMotionOn`: `Motion.Scale = 1`, nguồn không chậm → lớp phủ còn hiện ở 0,2 giây và đã ẩn ở 0,8 giây.
  - `Curtain_FitsBothFrames`: `LayoutProbe` ở 2400×1080 và 2048×1536, gà con nằm trọn trong vùng an toàn.
- [ ] **Step 2:** FAIL. **Step 3:** Làm giao diện. **Step 4:** `playmode --filter PrepareFlowTests;MotionTests` PASS.
- [ ] **Step 5:** Chụp màn ở hai khung, gửi chủ dự án xem. Commit `feat(ui): màn chuyển gà con khi chuẩn bị bài`.

---

### Task 8: Màn Phụ huynh: chuẩn bị chữ 80 bài, âm thanh nạp khi chạm

**Files:**
- Modify: `App/AppRoot.cs` (`ShowParent` có chờ), `App/ParentScreen.cs` (đọc bài qua `Lessons.Get` và Phụ lục qua `Lessons.Appendix(book)`), `Audio/SpeechPlayer.cs`
- Test: `Tests/PlayMode/ParentScreenTests.cs` (thêm), `SpeechPlayerTests.cs` (thêm)

**Interfaces:**
- Consumes: `LessonRepository.LoadAllAsync`, `AssetCatalog.AudioAsync`, `CurrentHolder`, `PrepareCurtain`.
- Produces:
  - `ShowParent()`: luồng như Task 6 nhưng bước 2–3 là `await Lessons.LoadAllAsync()`. Bộ của màn Phụ huynh là một `ContentSet` rỗng làm `CurrentHolder`;
  - `SpeechPlayer.PlayAsync(id)`: mã chưa giữ thì `await _catalog.AudioAsync(id, _catalog.CurrentHolder)` thay cho nạp ngay. Trả về và cách bị cắt ngang giữ như cũ (kiểm tra thế hệ sau `await`).

- [ ] **Step 1: Test:**
  - `ParentScreenTests.Appendix_TapLetter_PlaysWithoutUnpreparedWarning`: mở Phụ lục, chạm ô âm của chữ "b" → `Speech.History` có `am_b`; `UnpreparedAsks` không chứa `am_b`.
  - `ParentScreenTests.Leave_ReleasesTappedAudio`: rời màn → `ReleaseCount(Speech,"am_b") == 1`.
  - `ParentScreenTests.OpenTwice_ReadsLessonsOnce`: `LoadCount(Lesson, "tv1_t1_b01") == 1` sau hai lần mở.
  - `SpeechPlayerTests.Play_UnheldId_InterruptedDuringLoad_ReturnsFalse`: nguồn chậm 3 khung, `Stop()` ở khung 1 → `false`, không phát.
- [ ] **Step 2:** FAIL. **Step 3:** Sửa. **Step 4:** `playmode --filter ParentScreenTests;SpeechPlayerTests` PASS.
- [ ] **Step 5:** Commit `feat(app): màn Phụ huynh chuẩn bị chữ các bài, âm thanh nạp khi chạm`.

---

### Task 9: Màn học không hỏi mã chưa chuẩn bị; dọn chuỗi đường dẫn

**Files:**
- Modify: `Tests/PlayMode/ViewTestBase.cs`: catalog trên nguồn giả có `Fallback` (sprite/clip trơn), có helper `PrepareFor(Lesson)` gọi `PrepareAsync(ContentIds)` cùng `PrepareCommonAsync`.
- Test: `Tests/PlayMode/PreparedCoverageTests.cs`

**Interfaces:**
- Consumes: `LessonAssets.ContentIds`, `AssetCatalog.UnpreparedAsks`, `StepViewFactory`, cách `Part1ViewTests` / `RoundViewTests` dựng màn.

- [ ] **Step 1: Test `PreparedCoverageTests.EveryStepTypeAndRoundKind_AsksOnlyPrepared`:**
  - Chọn bài từ dữ liệu thật: duyệt `index` theo thứ tự, lấy bài đầu tiên có mỗi `step.type` và mỗi `round.kind` còn thiếu. Bài có `readings` ưu tiên cho loại `unit`.
  - Với mỗi bài được chọn: `PrepareFor(lesson)`, dựng từng bước và từng lượt của **chỉ loại cần phủ**, rồi chờ phát hết (`WaitScale = 0.05`). Không cần thao tác đúng.
  - Assert `UnpreparedAsks` rỗng. Thông điệp lỗi liệt kê mã và bài.
  - Assert số loại đã phủ bằng số loại xuất hiện trong dữ liệu.
- [ ] **Step 2:** Chạy. Nếu FAIL do mã thật bị sót (như `readings` trước đây) thì sửa `LessonAssets` cho đủ; không nới test.
- [ ] **Step 3:** `grep -rn "Resources.Load\|\"audio/\|\"images/\|\"sfx/\|\"lessons/\|\"appendix/\|\"fonts/" unity/TapDoc/Assets/Scripts unity/TapDoc/Assets/Tests` chỉ còn kết quả trong `ContentPaths.cs`, `ResourcesContentSource.cs` và `SetupTests` (`TMP Settings`). Còn chỗ khác thì chuyển sang `ContentPaths`/nguồn.
- [ ] **Step 4:** Chạy:
  - `playmode --filter PreparedCoverageTests;Part1ViewTests;RoundViewTests;SpellViewTests;NewStepViewTests;NewStepViewTests2;ReadingButtonsTests`;
  - `editmode --filter DataTests;ContentPathsTests;LessonRepositoryTests`.

  Kỳ vọng PASS.
- [ ] **Step 5:** Commit `test: màn học chỉ hỏi tranh, âm thanh đã chuẩn bị; dọn đường dẫn ghi cứng`.
- [ ] **Step 6:** Báo chủ dự án: đã xong, danh sách lớp test đã chạy. Đề nghị "test all" nếu chủ dự án muốn chạy cả test đi hết bài.
