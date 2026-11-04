# Thiết kế: Dọn cách app đọc dữ liệu (chuẩn bị cho Addressables)

> **Ngày:** 04/11/2026 · **Trạng thái:** chủ dự án đã duyệt ngày 04/11/2026 · Repo: https://github.com/KietTran612/APP_TIEU_HOC, chỉ dùng branch `main`, giữ nguyên lịch sử
> **Thiết kế gốc của app:** [2026-10-28-app-tap-doc-mvp-design.md](2026-10-28-app-tap-doc-mvp-design.md). Mọi điều ở đó vẫn giữ, trừ những chỗ tài liệu này nói rõ là thay.
>
> Cách đánh dấu:
> - **[Chốt]**: chủ dự án đã quyết.
> - **[Đề xuất]**: người viết tự quyết. Chủ dự án có thể đổi; builder không cần hỏi lại.
> - **[Builder]**: builder tự quyết.

---

## 1. Mục đích và lý do

Sau này app sẽ chuyển sang **Addressables** để giảm dung lượng bản cài và bộ nhớ khi chạy. **Đợt này chưa làm Addressables [Chốt]**. Đợt này chỉ dọn cách app đọc dữ liệu (bài học, danh sách bài, Phụ lục, tranh, âm thanh phát âm, tiếng động, font), để đến lúc chuyển thì chỉ cần thay một lớp, còn các màn giữ nguyên.

Hiện trạng có các vấn đề sau:
- `Resources.Load` nằm rải rác ở 5 chỗ: `AssetCatalog`, `LessonRepository`, `AppendixData`, `FontProvider` và một chỗ trong `ProfileScreen` đi vòng qua catalog để kiểm tra ảnh đại diện. Tên thư mục `"audio/"`, `"images/"`, `"sfx/"`, `"lessons/"`, `"appendix/"`, `"fonts/"` được ghi cứng ở nhiều nơi, kể cả trong test.
- Mọi thứ được nạp **ngay lúc màn cần** (đồng bộ). Addressables thì luôn nạp kiểu "xin rồi chờ", kể cả khi file nằm sẵn trong máy, nên các màn cần làm quen với việc chờ ngay từ bây giờ.
- **Không có gì được nhả.** Bé học càng nhiều bài trong một lần mở app thì bộ nhớ càng tăng.
- `LessonRepository` đọc lại file mỗi lần gọi. Mỗi lần mở Phụ lục, màn Phụ huynh đọc và phân tích lại cả 80 bài.
- Tranh động chưa có đường vào app.

## 2. Đích lâu dài (để hiểu vì sao thiết kế như dưới)

- App nhắm Android trước. **Cài một lần là có đủ 80 bài, học không cần mạng, không có bước tải thêm [Chốt].**
- Addressables dùng để: chỉ đóng vào app những file thật sự được dùng, nén theo nhóm, nạp và nhả theo từng bài. Nếu bản cài vượt giới hạn file gốc của Google Play thì ghép với gói nội dung cài cùng app của Play, vẫn là cài một lần [Đề xuất].
- Gợi ý chia nhóm khi làm Addressables (không làm đợt này): tranh bài chia theo bài, vì mỗi tranh thuộc đúng một bài; âm thanh phát âm để chung một nhóm, vì 723 trong 1.926 file được nhiều bài dùng.

## 3. Mục tiêu, việc không làm, điều coi là thất bại

### Mục tiêu
1. Một lớp nguồn dữ liệu duy nhất biết đọc mọi loại dữ liệu theo **loại + mã**. Tên thư mục chỉ ghi ở một chỗ. Đợt này có một bản đọc Resources; sau này thêm bản Addressables thay vào mà không sửa màn nào.
2. Nạp có chờ ở những lúc nặng (mở app, mở bài, ôn lại, màn Phụ huynh). Trong lúc bé đang học thì không phải chờ gì.
3. Nạp theo bộ và nhả theo bộ: bộ chung giữ suốt, bộ của bài nhả khi xong.
4. Có sẵn chỗ cho tranh động trong lớp đọc dữ liệu.
5. Test thay cách nạp bằng một nguồn dữ liệu giả, không còn tự ghép đường dẫn Resources.

### Việc không làm
- Không làm Addressables, không cài gói Addressables [Chốt].
- Không tải qua mạng, không có giao diện tải [Chốt].
- Không đưa clip tranh động vào Unity, không hiện clip trong bài [Chốt].
- Không đổi định dạng JSON bài học và Phụ lục, không đổi công cụ Python `tools/tapdoc`, không đổi mã tranh, mã âm thanh [Đề xuất].
- Không đổi cấu trúc thư mục `Assets/Content/Resources/` (`audio/`, `images/`, `sfx/`, `lessons/`, `appendix/`, `fonts/`). Nhờ vậy gói media trên Google Drive, `run_unity_media.py` và `media_lock.json` không bị ảnh hưởng [Đề xuất].
- Không đổi giao diện các màn, trừ màn chuyển có gà con ở mục 5.2.

### Coi là thất bại nếu
- Phải sửa các màn bước học hoặc lượt luyện tập (`Steps/`, `Exercises/`) chỉ vì đổi cách nạp.
- Trong lúc học một bài, bé phải chờ tranh hoặc âm thanh.
- Bé chạm hai lần vào một bài thì mở hai lần, hoặc app bị treo.
- Gói media hoặc máy mới phải giải nén khác đi.

## 4. Dữ liệu hiện có (giữ nguyên)

- **Bài học:** `Resources/lessons/index.json` (80 bài) và `tv1_t1_bNN.json`, được `tools/tapdoc build` dựng từ `content/src/`. Mỗi file bài chỉ ghi **mã** tranh và âm thanh, ví dụ `"image": "img_b01_bof"`, `"audio": "van_o"`; không ghi đường dẫn.
- **Phụ lục:** `Resources/appendix/tv1_t1_1990.json`.
- **Tranh:** `Resources/images/`, 213 file PNG 1254×1254. 190 tranh bài (`img_bNN_*`, mỗi tranh thuộc đúng một bài, mỗi bài 1–4 tranh) và 23 tranh chung (`img_chung_*`, `img_ui_*`).
- **Âm thanh phát âm:** `Resources/audio/`, 1.926 file mp3 đặt tên theo loại và chữ (`tieng_*`, `tu_*`, `cau_*`, `van_*`…). Mỗi bài dùng 7–158 file, nhiều file được dùng chung giữa các bài.
- **Tiếng động:** `Resources/sfx/`, 6 file. **Font:** `Resources/fonts/Andika-Regular`.
- **Mã do code đặt:** `SystemAudio`, `SystemImages`, `SystemIcons`, `SystemSfx` (trong `Content/SystemAssets.cs`) và `ProfileScreen.Avatars`.

## 5. Cách nạp và nhả

### 5.1 Lúc mở app: nạp bộ chung [Đề xuất]
Bộ chung gồm:
- font Andika;
- mọi mã trong `SystemSfx.All`, `SystemAudio.All`, `SystemImages.All` (đã gồm `SystemIcons.All`) và `ProfileScreen.Avatars`;
- `lessons/index.json`;
- Phụ lục của sách.

Bộ chung được nạp **một lần khi mở app**, trước khi hiện màn chọn bé. Lúc đó màn chỉ có nền giấy, chưa có chữ. Bộ chung được giữ đến khi app tắt và không bao giờ nhả.

Ảnh đại diện là thứ **không bắt buộc**: thiếu thì im lặng (không báo lỗi), màn chọn bé hiện ô màu kèm chữ đầu của tên như bây giờ.

Màn chọn bé, danh sách bài, Sổ bé ngoan và màn kết quả chỉ dùng bộ chung, nên hiện ngay như hiện nay.

### 5.2 Mở bài: màn chuyển có gà con [Chốt]
Khi bé chạm vào một bài:
1. **Hiện ngay một màn chuyển có gà con** [Chốt], dùng tranh `img_chung_ga_con` có sẵn trong bộ chung. Trong lúc màn chuyển đang hiện, mọi lần chạm khác đều bị bỏ qua.
2. Đọc file bài qua kho bài (mục 6.3).
3. Lập **bộ của bài**: các mã trong `LessonAssets.AudioIds(lesson)` và `LessonAssets.ImageIds(lesson)`. Mã nào đã có trong bộ chung thì không nạp lại.
4. Nạp tất cả cùng lúc, kiểu có chờ. **Với âm thanh, "nạp xong" nghĩa là đã có cả dữ liệu tiếng trong bộ nhớ**, không chỉ có đối tượng `AudioClip`. Âm thanh được nhập với `preloadAudioData` tắt và `DecompressOnLoad` (`Scripts/Editor/ContentImportRules.cs`), nên sau khi nạp đối tượng, catalog gọi `LoadAudioData()` và chờ `loadState` thành `Loaded` (hoặc `Failed`, coi như thiếu file). Khi nhả thì gọi `UnloadAudioData()`. Không đổi cách nhập âm thanh, để file `.meta` trong gói media giữ nguyên [Đề xuất].
5. Nạp xong thì màn chuyển khép lại và màn bài hiện ra.
   - Màn chuyển hiện tối thiểu khoảng 0,4 giây để không bị chớp [Đề xuất; Builder chỉnh con số]. Khi tắt hiệu ứng (`Motion`, như trong test) thì không có thời gian tối thiểu.
   - Cách vẽ gà con và kiểu chuyển (mờ dần, lật trang…) do Claude tự làm khi làm giao diện, theo phong cách đã chốt ở [thiết kế giao diện](2026-10-30-ui-hieu-ung-design.md) [Builder].
6. **Trong bài**, các bước và lượt luyện tập vẫn gọi `Assets.Image(mã)`, `Assets.Audio(mã)` như bây giờ. Catalog trả ngay từ thứ đã nạp, không đọc đĩa.

**Ôn lại** (`ShowReview`) đi đúng các bước trên. Bộ cần nạp là mã của bài tạm do `ReviewSession` dựng, tức các lượt được gom từ nhiều bài.

### 5.3 Nhả [Đề xuất]
- Mỗi file trong catalog có **số chỗ đang giữ**. Một bộ (bài, ôn lại, màn Phụ huynh) giữ file nào thì số đó tăng 1; nhả bộ thì giảm 1; về 0 thì catalog thôi giữ file.
- **Bộ của bài được giữ qua màn kết quả**: bấm "Bài tiếp" thì âm thanh dùng chung giữa hai bài không phải nạp lại. Bộ được nhả khi:
  - bé mở bài khác hoặc ôn lại: nhả **sau khi** bộ mới đã nạp xong, nên âm thanh dùng chung giữa hai bài liền nhau không bị nhả rồi nạp lại;
  - hoặc bé về danh sách bài, màn chọn bé, Sổ bé ngoan, màn Phụ huynh.
- Với Resources, "nhả" nghĩa là catalog bỏ tham chiếu. Sau khi màn cũ đã bị huỷ, gọi `Resources.UnloadUnusedAssets()` một lần để Unity dọn [Đề xuất; Builder chọn chỗ gọi, miễn là không chạy giữa lúc bé đang học]. Với Addressables sau này, đây là `Release` của từng tay cầm (handle).

### 5.4 Màn Phụ huynh [Đề xuất]
- Bảng chữ cái của Phụ lục và danh sách chữ hay nhầm cần **chữ** của cả 80 bài. Khi mở màn Phụ huynh, app nạp đủ 80 file bài qua kho bài (có chờ, dùng cùng màn chuyển gà con). Màn Phụ huynh có khoá phép tính ở đầu, nên chờ thêm một chút ở đây không ảnh hưởng gì. Bài đã đọc thì được giữ lại, các lần sau không đọc lại.
- Phụ huynh chạm vào một chữ để nghe: `SpeechPlayer` thấy âm thanh chưa nạp thì nạp lẻ file đó (có chờ, rất ngắn) rồi phát. File lẻ này thuộc bộ của màn Phụ huynh và được nhả khi rời màn.

### 5.5 Hỏi một thứ chưa chuẩn bị [Đề xuất]
Nếu màn gọi `Assets.Image(mã)` hoặc `Assets.Audio(mã)` với một mã không nằm trong bộ nào đang giữ:
- catalog vẫn nạp ngay (bản Resources dùng `Resources.Load`; bản Addressables sau này dùng `WaitForCompletion`) và trả kết quả, để app không hỏng;
- ghi **cảnh báo** một lần cho mỗi mã: `[TapDoc] Chưa chuẩn bị trước: <mã>`;
- ghi mã đó vào danh sách "hỏi khi chưa chuẩn bị" để test kiểm tra (mục 8).

File nạp kiểu này được tính vào bộ đang hiện (bộ của bài, hoặc của màn Phụ huynh) để vẫn được nhả.

## 6. Các lớp mới và lớp được sửa

Tên lớp là đề xuất [Builder có thể đổi tên, giữ đúng vai trò].

### 6.1 Loại dữ liệu và đường dẫn: một chỗ duy nhất
- `enum ContentKind { LessonIndex, Lesson, Appendix, Image, Speech, Sfx, Font, Clip }`.
- `ContentPaths` là chỗ **duy nhất** biết tên thư mục: `Image → "images/"`, `Speech → "audio/"`, `Sfx → "sfx/"`, `Lesson → "lessons/"`, `LessonIndex → "lessons/index"`, `Appendix → "appendix/"`, `Font → "fonts/"`, `Clip → "clips/"` (để dành). Kiểu Unity ứng với từng loại (`Sprite`, `AudioClip`, `TextAsset`, `Font`, `VideoClip`) cũng khai báo ở đây.
- Không còn chuỗi `"audio/"`, `"images/"`… nào ở nơi khác trong Runtime và Tests. Ngoại lệ: các test cố ý kiểm tra file trong project (ví dụ `AssetSwapTests` ghi file vào thư mục thật) thì lấy đường dẫn từ `ContentPaths`.

### 6.2 Nguồn dữ liệu: `IContentSource`
Giao diện tầng dưới, **không có bộ nhớ đệm, không đếm**:
- `Awaitable<T> LoadAsync<T>(ContentKind kind, string id)`: trả `null` khi không có file, không ghi log;
- `T Load<T>(ContentKind kind, string id)`: bản nạp ngay, chỉ dùng cho mục 5.5;
- `void Release(ContentKind kind, string id, Object asset)`: bản Resources không làm gì; bản Addressables sau này gọi `Addressables.Release`.

Các bản cài đặt:
- `ResourcesContentSource`: dùng `Resources.LoadAsync` / `Resources.Load` với đường dẫn từ `ContentPaths`;
- `FakeContentSource`, **chỉ trong test**: từ điển trong bộ nhớ, đếm số lần nạp và nhả, có thể giả lập chậm (chờ vài khung hình) và thiếu file;
- `AddressablesContentSource`: **không làm đợt này**.

### 6.3 Kho bài: `LessonRepository` thành lớp có đối tượng
- Nhận `IContentSource` khi tạo.
- Giữ bộ nhớ đệm: danh sách bài (`index`) đọc một lần; mỗi bài sau khi phân tích được giữ đến khi app tắt (chỉ là chữ, cả 80 bài khoảng 2,6 MB JSON).
- `Awaitable<Lesson> LoadAsync(id)` và `Awaitable<LessonIndex> LoadIndexAsync()`. Ngoài ra có `Lesson Get(id)` và `LessonIndex Index`, trả ngay từ bộ nhớ đệm; nếu chưa có thì nạp ngay và cảnh báo như mục 5.5.
- Giữ nguyên: `Parse(json)`, chuẩn hoá NFC, các thông điệp lỗi `InvalidDataException` (`Không tìm thấy bài học: …`, `Bài <mã>: …`). `Parse` vẫn là hàm tĩnh để test cũ dùng được.
- `AppendixData` đọc qua cùng nguồn dữ liệu và cũng được giữ trong bộ nhớ đệm. Phần chuẩn hoá giữ nguyên.
- `AppRoot` có thuộc tính `Lessons`. Mọi chỗ đang gọi `LessonRepository.LoadIndex()` / `Load(id)` (AppRoot, BookScreen, LessonListScreen, ParentScreen, ResultScreen) chuyển sang `app.Lessons`.
- `LetterAudio.FromLessons` không đổi.

### 6.4 Catalog: `AssetCatalog` giữ tên, thêm bộ và đếm
Giữ nguyên với các màn:
- `Image(id)`, `Audio(id)`, `Sfx(id)`: trả ngay; thiếu thì trả `null`;
- cách báo thiếu không đổi [Chốt]: `[TapDoc] Thiếu âm thanh: …` và `[TapDoc] Thiếu tranh: …` là **lỗi**, `[TapDoc] Thiếu tiếng động: …` là **cảnh báo**, mỗi mã chỉ báo một lần; tranh để trống, âm thanh bỏ qua, bé vẫn học tiếp.

Thêm mới:
- tạo bằng `new AssetCatalog(IContentSource source)`. Các tham số `audioLoader` / `imageLoader` / `sfxLoader` bị bỏ, test chuyển sang `FakeContentSource`;
- `Awaitable PrepareCommonAsync()`: nạp bộ chung (mục 5.1), kèm font;
- `Awaitable<ContentSet> PrepareAsync(IEnumerable<(ContentKind, string)> ids)`: nạp và giữ một bộ, trả về `ContentSet` (một tay cầm, `IDisposable`). `Dispose` là nhả bộ. Thiếu file thì báo như trên rồi tiếp tục, không làm hỏng cả bộ;
- `Image(id)` / `Audio(id)` không ghi log khi mã nằm trong danh sách không bắt buộc. Có thêm cách hỏi "có tranh này không" mà không ghi log (cho ảnh đại diện);
- `Awaitable<AudioClip> AudioAsync(id)` cho trường hợp 5.4;
- danh sách "hỏi khi chưa chuẩn bị" (mục 5.5), chỉ để test đọc.

Thêm `LessonAssets.ContentIds(lesson)`, trả về mã tranh và mã âm thanh kèm loại, dùng cho bước 3 ở mục 5.2.

**Sửa `LessonAssets.AudioIds` cho đủ [Đề xuất]:** hiện hàm này bỏ sót `step.readings[].audio`, là âm thanh từng cách đọc ở bước giới thiệu chữ do `UnitView` phát. Có 23 bước như vậy, dùng 47 file, cả 47 đều có trên máy (kiểm tra ngày 04/11/2026). Đây là sửa code đọc mã, không đổi dữ liệu bài. Sau khi sửa, `AllReferencedAssetsExist` cũng kiểm tra luôn các file này.

Ngoài các mã trong JSON bài, các màn bước học còn tự gọi mã chung (`SystemAudio.hd_danh_van_theo`, `hd_keo_dau_vao_chu`, `hd_thu_lai`, `khen_01`, `khen_02`…). Các mã này đã nằm trong bộ chung.

### 6.5 Ai giữ bộ nào: `AppRoot`
- `InitIfNeeded` tạo `ResourcesContentSource` (hoặc nguồn do test đưa vào qua móc `SourceFactory`, thay cho `CatalogFactory`), rồi tạo kho bài và catalog từ nguồn đó.
- Khởi động: `TryBootMainScene` chờ `PrepareCommonAsync` xong rồi mới `ShowProfiles`.
- `ShowLesson(id)`, `ShowReview()`, `ShowParent()` thành luồng có chờ, theo mục 5.2 và 5.4. `AppRoot` giữ bộ hiện tại và nhả theo mục 5.3. Các nút bấm vẫn gọi được như cũ (không cần `await`); trong lúc đang chuẩn bị thì bỏ qua lần gọi mới.
- Có cách để test chờ đến khi chuẩn bị xong, ví dụ `AppRoot.IsPreparing` hoặc trả về `Awaitable` [Builder].

### 6.6 Font, giọng đọc, tiếng động
- `FontProvider` lấy font từ catalog (font đã nạp trong bộ chung), không tự gọi `Resources.Load`. Nếu bị hỏi trước khi bộ chung xong (ví dụ trong test EditMode dựng giao diện) thì nạp ngay và cảnh báo như mục 5.5 [Đề xuất].
- `SpeechPlayer` và `SfxPlayer` không còn tự `new AssetCatalog()` khi không được truyền vào: phải được `Init` với catalog. Thiếu catalog là lỗi lập trình, báo rõ [Đề xuất]. `SpeechPlayer.PlayAsync` dùng `AudioAsync` khi mã chưa nạp (mục 5.4).
- `ProfileScreen.AvatarSprite` hỏi catalog, không gọi thẳng `Resources.Load`.

### 6.7 Tranh động: chỉ chừa chỗ [Chốt]
Chỉ có `ContentKind.Clip`, đường dẫn `clips/` và kiểu `VideoClip` trong `ContentPaths`. Không có file, không có màn nào dùng, không thêm vào bộ của bài. Khi nào đưa clip vào app sẽ có thiết kế riêng.

## 7. Thiếu file và lỗi

| Trường hợp | Cách xử lý |
|---|---|
| Thiếu tranh hoặc âm thanh của bài | Giữ như hiện tại [Chốt]: báo lỗi `[TapDoc] Thiếu …` một lần, tranh trống, âm thanh bỏ qua, vẫn vào bài |
| Thiếu tiếng động | Cảnh báo một lần, không có tiếng |
| Thiếu ảnh đại diện | Im lặng, hiện ô màu kèm chữ đầu |
| Thiếu hoặc hỏng file bài | Như hiện tại: `InvalidDataException` kèm mã bài. Trong luồng mở bài (hoặc ôn lại): tắt màn chuyển, **ở lại màn đang hiện** (danh sách bài, hoặc màn kết quả nếu bé bấm "Bài tiếp"), không nhả bộ cũ, ghi lỗi ra Console [Đề xuất] |
| Thiếu `index.json`, font hoặc Phụ lục lúc khởi động | Ghi lỗi rõ ra Console. Đây là lỗi đóng gói, test chặn từ trước |

Lỗi đóng gói được chặn **trước khi build** bằng test `AllReferencedAssetsExist`.

## 8. Test

Claude viết và review mọi test. Worker chỉ viết code để test chạy xanh. Chỉ chạy các lớp test liên quan, bằng `python tools/run_unity_tests.py editmode|playmode --filter <lớp>`, đóng Unity Editor trước khi chạy. Không chạy `MvpEndToEndTests` hay toàn bộ PlayMode khi chủ dự án chưa nói "test all" [Chốt].

**EditMode (mới):**
- `ContentPaths`: mỗi loại ứng với đúng thư mục và kiểu.
- `ResourcesContentSource`: nạp được một file có thật của mỗi loại; mã không có thì trả `null`, không ghi log.
- `AssetCatalog` với `FakeContentSource`:
  - `PrepareAsync` nạp mỗi mã đúng một lần, kể cả khi hai bộ cùng giữ;
  - nhả bộ thì giảm số chỗ giữ; về 0 thì gọi `Release` của nguồn; bộ chung không bao giờ bị nhả;
  - thiếu file thì ghi đúng thông điệp, đúng mức (lỗi hoặc cảnh báo), một lần;
  - mã không bắt buộc thì không ghi log;
  - hỏi mã chưa chuẩn bị thì vẫn trả kết quả, ghi cảnh báo một lần và có trong danh sách.
- Kho bài: đọc mỗi bài một lần (đếm qua nguồn giả); NFC và thông điệp lỗi như cũ.
- `LessonAssets.ContentIds` của một bài trùng với hợp của `AudioIds` và `ImageIds`.

**EditMode (sửa):**
- `AllReferencedAssetsExist` đi qua `ResourcesContentSource` và `ContentPaths`, không tự ghép đường dẫn.
- `AssetCatalog_Missing_LogsOnceAndReturnsNull`, `AssetSwapTests`, `UiStyleTests`, `SetupTests.AndikaFontLoads` chuyển sang cách tạo mới.

**PlayMode (mới, lọc theo lớp):**
- Mở bài: màn chuyển hiện, nguồn giả cho chậm vài khung hình, màn bài chỉ hiện khi nạp xong; chạm hai lần chỉ mở một bài.
- Nhả: về danh sách bài thì bộ của bài được nhả; mở bài kế tiếp thì file dùng chung không bị nhả rồi nạp lại.
- Màn bước học và lượt luyện tập (dựng trên `ViewTestBase` từ một bài đã được chuẩn bị) **không hỏi mã nào chưa chuẩn bị**. Phạm vi [Đề xuất]: không đi hết 80 bài, vì như vậy là test đi hết bài, chỉ chạy khi chủ dự án nói "test all". Test tự chọn từ dữ liệu một nhóm bài nhỏ sao cho **mỗi loại bước** (`step.type`) và **mỗi loại lượt** (`round.kind`) có ít nhất một bài, ưu tiên bài có `readings`. Mỗi bước chỉ cần dựng và phát hết (đặt `WaitScale` nhỏ), không cần bé thao tác đúng hết.
- Âm thanh trong bộ đã chuẩn bị có `loadState == Loaded`; nhả bộ thì dữ liệu tiếng được giải phóng (`UnloadAudioData`).

**PlayMode (sửa):** `AppTestBase`, `ViewTestBase`, `AppFlowTests` chuyển từ loader giả sang `FakeContentSource` và chờ chuẩn bị xong. Riêng `UseStubsForMissingAssets` thành một nguồn dữ liệu "có thật thì dùng, không có thì trả hình trơn và clip ngắn".

## 9. Những gì giữ nguyên

- Cấu trúc `Assets/Content/Resources/`, gói media trên Google Drive, `run_unity_media.py`, `media_lock.json`, `content/manifests/`.
- Định dạng JSON bài học và Phụ lục, công cụ Python, mã tranh và mã âm thanh, các hằng trong `SystemAssets.cs`.
- Cách chuẩn hoá NFC, thông điệp lỗi `[TapDoc] Thiếu …` và `InvalidDataException`.
- Giao diện mọi màn, trừ màn chuyển có gà con.
- API các màn dùng: `Assets.Image/Audio/Sfx`, `SpeechPlayer.PlayAsync`, `SfxPlayer`.
- `ProgressStore` và các móc test của nó (`StoreFactory`).

## 10. Để lại cho builder

- Tên lớp, chia file, chia bước kế hoạch và commit (mỗi task một commit hoặc vài commit rõ ràng, chỉ trên `main`, không push).
- Con số thời gian tối thiểu của màn chuyển; hình và chuyển động của màn chuyển (Claude tự làm, không giao worker).
- Chỗ gọi `Resources.UnloadUnusedAssets()`.
- Cách cho test chờ chuẩn bị xong.
- Phần code đơn giản có test của Claude đi kèm (ví dụ `ContentPaths`, `ResourcesContentSource`, kho bài có bộ nhớ đệm) có thể giao Codex hoặc Antigravity, sau khi hỏi chủ dự án. Phần giao diện và hiệu ứng thì không giao.
