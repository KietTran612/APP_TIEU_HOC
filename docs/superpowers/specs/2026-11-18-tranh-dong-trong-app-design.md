# Thiết kế: Phát tranh động (clip) trong app

> **Ngày:** 18/11/2026 · **Trạng thái:** root đã duyệt ngày 18/11/2026, giữ cả 9 lựa chọn [Đề xuất] (chủ dự án giao root duyệt mọi việc cho tới khi app hoàn chỉnh) · Repo: https://github.com/KietTran612/APP_TIEU_HOC, chỉ dùng branch `main`
> **Thiết kế liên quan:** [app gốc](2026-10-28-app-tap-doc-mvp-design.md), [đọc dữ liệu](2026-11-04-doc-du-lieu-design.md) (mục 7.6 chừa chỗ `ContentKind.Clip`), [tỷ lệ màn hình](2026-11-05-ty-le-man-hinh-design.md), [nâng cấp UI](2026-11-17-nang-cap-ui-design.md). Cách làm clip: `content/style/tranh_dong_huong_dan.md`.
>
> Cách đánh dấu:
> - **[Chốt]**: chủ dự án hoặc root đã quyết.
> - **[Đề xuất]**: người viết tự quyết. Root có thể đổi; builder không cần hỏi lại.
> - **[Builder]**: builder tự quyết.

---

## 1. Mục đích

Từ 30/10, các session tranh động đã làm clip cho tranh bài học trên Google Flow, nhưng chưa clip nào vào app. Ngày 17/11 chủ dự án yêu cầu app "hoàn chỉnh đầy đủ mọi thứ", kể cả tranh động [Chốt]. Tài liệu này mô tả clip phát ở đâu, lúc nào, phát thế nào, và clip đi từ `content/clips/` vào bản build Windows ra sao.

Ý của chủ dự án về tranh động (theo `tranh_dong_huong_dan.md` mục 1): mỗi tranh có một hành động có ý nghĩa và âm thanh thật (con vật kêu, cây lớn lên, đồ vật lắp ghép). Clip là phần thưởng nhìn và nghe gắn với chữ bé vừa đọc. Clip không thay việc học đọc.

## 2. Dữ liệu clip hiện có (đo ngày 18/11)

- Danh mục: `content/manifests/video_manifest.json`, 401 dòng `{id, file, source, status, ghi_chu}`. `id` trùng mã tranh (`img_b01_bof`). Trạng thái: `dat` 243, `cho_duyet` 80, `khong_dat` 78.
- File: `content/clips/<mã tranh>.mp4`, nằm ngoài git (`.gitignore`). Clip đi giữa các máy trong `dist/TapDoc-clips-<ngày>.zip` và các gói `bosung` (`tools/run_unity_media.py`).
- **Clip được phát:** `dat` và `cho_duyet` [Chốt, root 18/11]: 323 clip, đủ file, tổng 885 MB.
  - Tất cả cùng định dạng: H.264 1280×720 và âm thanh AAC, dài 7,93 s hoặc 8,0 s.
  - Clip `khong_dat` không vào app; ở chỗ đó app hiện tranh tĩnh.
- **Khung hình:** tranh vuông được đệm giấy hai bên thành 16:9 và đặt giữa khung. Phần tranh là hình vuông 720×720 ở giữa, nên app chỉ hiện hình vuông đó.
- **Hai kiểu clip** (`tranh_dong_kich_ban.json`, trường `mode`):
  - `loop` (247 clip): khung đầu và khung cuối đều là tranh gốc.
  - `build` (76 clip): khung đầu là lúc trước (mầm cây, người đứng xa hơn), khung cuối là tranh gốc.
  - Ở cả hai kiểu, khung cuối đã được soát là khớp tranh tĩnh (`endDiff`, `picDiff` trong lúc duyệt). Vì vậy hết clip quay về tranh tĩnh mà không giật.
- **Độ to:** đo 30 clip và 30 file giọng đọc, lấy RMS của 1/3 đoạn to nhất. Clip có trung vị −28 dBFS (10% to nhất từ −19 dBFS). Giọng đọc có trung vị −16,5 dBFS. Clip vốn nhỏ hơn giọng đọc khoảng 12 dB, nên không cần giảm âm lượng clip.
- **Chỗ tranh có clip xuất hiện trong bài** (đếm từ `Resources/lessons/*.json`):

| Chỗ | Màn | Số clip phát được | Chỉ có ở chỗ này |
|---|---|---|---|
| Bước `keyword` và `picture` (`step.image`) | `KeywordView` | 281 | 279 |
| Bước `words` (`items[].image`) | `ItemsView` | 28 | 27 |
| Bước `riddle_answer` (`step.image`, tranh đáp án) | `RiddleAnswerView` | 11 | 8 |
| Bước `tone_attach` (`step.image`) | `SpellView` | 5 | 5 |
| Chỉ là phương án sai trong `riddle_answer` | — | 1 (`img_b137_cais_thuwowcs`) | — |

- Ba tranh đáp án câu đố còn xuất hiện ở chỗ khác: `img_b55_chumf_vair` (`keyword`), `img_b08_quyeenr_vowr` (`picture`), `img_b13_ddu_ddur` (`words`).
- Tranh nào có clip cũng xuất hiện thêm ở Phần 2 (`listen_picture`, `compose`).
- Bốn chỗ phát cộng lại phủ **322/323 clip**.

## 3. Mục tiêu, việc không làm, điều coi là thất bại

### Mục tiêu
1. Bé thấy tranh chuyển động, có tiếng, ngay sau khi nghe chữ của tranh đó, ở 4 màn của bảng trên.
2. Clip phát một lần, hết thì trở về đúng tranh tĩnh, không có khung đen, không giật.
3. Tiếng clip không bao giờ chồng lên giọng đọc hay lời dẫn.
4. Máy không phát được (máy yếu, thiếu bộ giải mã, lỗi) thì hiện tranh tĩnh như hiện nay và bé không thấy lỗi gì.
5. Mỗi lúc chỉ có một clip; bộ nhớ dùng cho clip được nhả khi rời bài.
6. Clip đi vào `Resources/` bằng một lệnh của `run_unity_media.py`, rồi vào bản build Windows.

### Việc không làm
- Không phát clip ở Phần 2: `listen_picture` có nhiều tranh để chọn, `compose` có tranh đề. Clip làm bé phân tâm, và tiếng con vật có thể lộ đáp án [Đề xuất].
- Không phát clip ở danh sách bài, tem bài, màn kết quả, tủ sách, màn phụ huynh, ôn lại [Đề xuất].
- Không lặp clip, không phát tự động nhiều lần [Đề xuất].
- Không sửa file clip: không cắt, không nén lại, không lồng tiếng. Clip chỉ làm bằng Google Flow (quy định của chủ dự án 12/11). App chỉ cắt phần vuông khi hiện [Chốt].
- Không vẽ biểu tượng mới (ví dụ nút ▶ trên tranh) đợt này. Clip tự phát ở mỗi chỗ nên bé không cần tìm nút [Đề xuất].
- Không làm Addressables, không tải clip qua mạng (thiết kế đọc dữ liệu [Chốt]).
- Không đổi `audio_manifest.json`, `image_manifest.json`, `content/tts/settings.json` và trạng thái trong `video_manifest.json` [Chốt].
- Bản cho điện thoại (dung lượng, nén lại clip): để quyết sau, xem mục 13.

### Coi là thất bại nếu
- Tiếng clip và giọng đọc cùng kêu, dù chỉ một lúc.
- Bé thấy khung đen hay khung của clip trước; tranh nhảy hình lúc clip kết thúc; hoặc lúc bắt đầu, hình đổi đột ngột thay vì mờ chuyển (mục 5).
- Thiếu clip hay clip hỏng làm app báo lỗi đỏ, treo, hoặc làm hỏng bước học.
- Bé phải chờ clip mới được đi tiếp, hoặc nút Tiếp hiện chậm hơn hiện nay.
- Bộ nhớ tăng dần khi học nhiều bài liên tiếp.
- Clip lộ phần giấy đệm hai bên (khung 16:9), hoặc tranh trong clip lệch so với tranh tĩnh.

## 4. Clip phát ở đâu, lúc nào

Quy tắc chung [Đề xuất]: **clip phát ngay sau khi app đọc xong chữ của chính tranh đó.** Nghe chữ trước rồi xem tranh sống động, để chữ gắn với hình. Tranh tự động lên, bé không phải chạm. Bé chạm lại tranh thì được xem lại.

| Màn | Lúc clip tự phát | Chạm để xem lại |
|---|---|---|
| `KeywordView` (`keyword`, `picture`) | Sau **lần đọc trọn đầu tiên** của bước, dù lần đọc đó do app tự đọc lúc mở bước hay do bé chạm chữ hay chạm tranh. Thường là lần app tự đọc. Nếu lần đó bị cắt ngang (bé chạm ngay), clip phát sau lần đọc trọn kế tiếp. Mỗi lần dựng bước chỉ tự phát một lần. | Chạm **tranh**: đọc chữ như hiện nay, rồi phát clip. Chạm **chữ** hoặc nút Nghe lại: chỉ đọc. Ngoại lệ: lần đọc đó là lần đọc trọn đầu tiên của bước thì clip tự phát như cột bên. |
| `ItemsView` bước `words` | Sau khi bé đánh vần xong và app đọc trơn từ có tranh (`item.audio` đọc trọn). | Chạm lại từ hay tranh của từ: chạy lại cả lượt như hiện nay, xong thì phát clip. |
| `RiddleAnswerView` | Bé đoán đúng, app hiện chữ và đọc đáp án xong: tranh đáp án (tranh còn lại duy nhất) phát clip, coi như phần thưởng. Bước báo xong ngay lúc clip bắt đầu, không chờ clip. | Sau khi bước đã xong, chạm tranh đáp án: phát lại clip, không đọc. |
| `SpellView` bước `tone_attach` | Bé ghép xong, tranh hiện ra và lắc nhẹ như hiện nay. Hết nhịp lắc thì phát clip. Bước báo xong như hiện nay, không chờ clip. | Chạm tranh: phát lại clip, không đọc. |

- Những việc của bước giữ nguyên: khi nào báo xong, khi nào hiện nút Tiếp, bé được chạm gì. Clip chỉ chen vào sau một lần đọc và không làm bước chờ [Đề xuất].
- Ở `KeywordView`, lần app tự đọc lúc mở bước không làm bước xong; chỉ lần chạm đầu tiên (đọc trọn) mới làm bước xong, như hiện nay (`KeywordView.cs` dòng 47 và 50–52).
  - Vì vậy clip tự phát thường chạy **khi nút Tiếp chưa hiện**. Bé không phải chờ: chạm lúc nào cũng được, giọng đọc bắt đầu thì clip dừng (mục 6).
  - Bé thường chạm tranh để làm bước xong: app đọc chữ, nút Tiếp hiện, rồi clip phát lần nữa. **Phát hai lần là chủ ý** [Đề xuất]: lần sau là bé tự chạm tranh để xem lại.
  - Bé bấm Tiếp giữa chừng thì clip dừng.
- Ở `KeywordView` bước `picture` (tranh không chữ), "đọc chữ" là `Step.audio` của bước.
- Tranh thiếu clip (`khong_dat`, chưa có file, máy không phát được, cài đặt tắt): mọi thứ như hiện nay, không có dấu hiệu gì khác.

## 5. Phát một lần rồi về tranh

- **Lớp phủ:** clip hiện trên một `RawImage` phủ đúng vùng tranh đang hiện trong thẻ. Tranh tĩnh vẫn nằm bên dưới. Lớp phủ là con của khung tranh (`Tile.ImageBox`), nên tự theo khi thẻ nảy, phóng hay lật trang [Đề xuất].
- **Bắt đầu:** nạp clip và chờ có **khung hình đầu tiên đã vẽ xong** mới hiện lớp phủ, mờ dần vào trong 0,3 s (`Motion.Fade`). Trong lúc chờ, bé vẫn thấy tranh tĩnh. Không bao giờ hiện khung đen hay khung còn sót của clip trước [Đề xuất].
  - Clip `loop`: khung đầu là tranh gốc, nên lúc mờ vào bé không thấy đổi.
  - Clip `build` (76 clip): khung đầu là lúc trước, ví dụ mầm cây. Bé sẽ thấy tranh hoàn chỉnh mờ chuyển về lúc trước, rồi lớn lên hoặc đi tới thành tranh. Đây là chủ ý, giống kiểu "xem cây mọc", và không tính là lỗi nhảy hình [Đề xuất].
  - App không cần biết kiểu của clip: mọi clip mờ vào cùng một cách. Nhờ vậy không phải chép trường `mode` vào dữ liệu của app [Đề xuất].
- **Kết thúc:** clip hết thì giữ khung cuối, rồi lớp phủ mờ đi trong 0,25 s để lộ tranh tĩnh bên dưới. Khung cuối gần như trùng tranh nên bé không thấy đổi. Xong thì gỡ lớp phủ [Đề xuất].
- **Dừng giữa chừng** (mục 6): tắt tiếng clip ngay, lớp phủ mờ đi trong 0,15 s, rồi gỡ [Đề xuất].
- Test đặt `Motion.Scale = 0` nên mờ vào, mờ ra xảy ra tức thì, giống các hiệu ứng khác.
- **Lật trang:** `LessonScreen.TurnCurrentPage` nhân bản bước cũ để lật. Bản sao không được giữ lớp phủ clip mà chỉ hiện tranh tĩnh. Bước thật bị huỷ thì clip dừng (mục 6) [Đề xuất].

## 6. Tiếng clip và tiếng đọc

Nguyên tắc: **giọng đọc luôn được ưu tiên; clip nhường** [Đề xuất].

- Clip chỉ bắt đầu khi `SpeechPlayer` rảnh (`IsBusy == false`). Màn gọi phát clip sau khi đã chờ lần đọc xong. Nếu lúc ấy giọng đọc lại đang chạy (một lần đọc khác vừa bắt đầu), clip không phát.
- Giọng đọc bắt đầu khi clip đang chạy thì clip dừng ngay (cắt tiếng, mờ hình như mục 5). Cách này phủ mọi nguồn: bé chạm chữ hay thẻ khác, nút Nghe lại, nhắc khi ngồi im (`IdleNudge` đọc lại lời dẫn), lời khen.
- Những lúc khác cũng dừng clip:
  - bấm Tiếp, bấm về danh sách: bước bị huỷ;
  - mở khung Ghi chú (`OpenNotes` đã gọi `Speech.Stop()`, nay gọi thêm dừng clip);
  - app bị tạm dừng (`OnApplicationPause(true)`);
  - rời màn học.
- **Tiếng động** (chạm, lật trang, đúng): giữ như hiện nay, có thể kêu cùng clip vì rất ngắn. `SfxPlayer` chỉ nhỏ tiếng lại khi giọng đọc chạy, không vì clip [Đề xuất].
- **Nhắc khi ngồi im và thời gian học:** khi clip đang chạy, `LessonScreen` coi như "đang bận" (cùng chỗ với `Speech.IsBusy` trong `Update` và `TrackStudyTime`). Nhờ vậy không có lời nhắc chen vào giữa clip, và 8 s xem clip được tính là thời gian học [Đề xuất].
- **Âm lượng:** clip phát qua một `AudioSource` riêng, âm lượng 1,0 (clip đã nhỏ hơn giọng đọc khoảng 12 dB, mục 2). Âm lượng là một hằng số, đổi được [Đề xuất].
- Nút loa (Nghe lại) không nhún theo clip; `SpeakingBob` vẫn chỉ theo giọng đọc [Đề xuất].

## 7. Cắt phần vuông

- `RawImage.uvRect` chỉ lấy phần giữa clip, có cùng tỉ lệ với tranh đang hiện. Với clip `W×H` và tranh có tỉ lệ `a = rộng/cao` (tranh bài hiện nay vuông, `a = 1`):
  - `w = min(1, H·a / W)`, `h = min(1, W / (H·a))`
  - `uvRect = (x = (1 − w)/2, y = (1 − h)/2, w, h)`
  - Với 1280×720 và `a = 1`: `uvRect = (0,21875; 0; 0,5625; 1)`.
- Hàm tính là một hàm thuần (ví dụ `ClipCrop.UvRect(int clipW, int clipH, float pictureAspect)`) để test EditMode [Đề xuất].
- **Bổ sung 19/11, sau khi duyệt** [Chốt, root 19/11]: app cắt thêm 4 điểm ảnh ở mỗi mép phần tranh (trên khung 720, `ClipCrop.EdgeInsetPx`), nên `uvRect` là `(0,221875; 0,00556; 0,55625; 0,98889)`.
  - Lý do: quét 327 clip phát được thì 37 clip có 3 hàng đen ở mép trên và mép dưới phần vuông, tranh tĩnh không có (ví dụ `img_b01_chumf_nho`, ảnh chụp có hai đường kẻ đen).
  - Cái giá: tranh trong clip to hơn tranh tĩnh khoảng 1,1%. Lúc mờ về tranh tĩnh hầu như không thấy.
  - Muốn bỏ thì đặt `EdgeInsetPx = 0`.
- **Lớp phủ trùng đúng chỗ tranh hiện**, không phải cả `ImageBox`. Tranh dùng `preserveAspect`, nên trong thẻ không vuông (thẻ tranh 320×280 ở `words`) tranh chỉ chiếm một hình vuông ở giữa. Lớp phủ phải trùng hình vuông đó, ví dụ dùng `AspectRatioFitter` (`FitInParent`, tỉ lệ `a`) [Builder chọn cách].
- Không tô viền, không bo góc thêm. Nền giấy của clip cùng màu nền giấy của tranh.

## 8. Thành phần trong code

### 8.1 Đọc dữ liệu
- `ContentPaths.TypeOf(ContentKind.Clip)` trả `typeof(UnityEngine.Video.VideoClip)`. Cần thêm module `com.unity.modules.video` vào `Packages/manifest.json`. Đường dẫn vẫn là `clips/<mã>`.
- Sửa chú thích `ContentKind.Clip`, bỏ ý "chưa nạp".
- `AssetCatalog.Clip(string id)` trả `VideoClip` hoặc `null`.
  - Clip **luôn là thứ không bắt buộc**: thiếu file thì im lặng, không báo lỗi, không cảnh báo, vì thiếu clip là chuyện thường (`khong_dat`). Cần sửa `AssetCatalog.ReportMissing`: hiện nay nhánh `default` gửi mọi loại khác Image, Speech, Sfx sang `Debug.LogError`. Loại `Clip` phải thoát im lặng trước nhánh đó.
  - Hỏi một clip chưa chuẩn bị thì xử lý như các loại khác: vẫn nạp ngay, cảnh báo "Chưa chuẩn bị trước" một lần.
- `LessonAssets.ClipIds(lesson)`: mã tranh ở 4 chỗ phát (mục 4). Đó là `step.image` của `keyword`, `picture`, `riddle_answer`, `tone_attach` và `items[].image` của `words`; không trùng, bỏ mã rỗng. `LessonAssets.ContentIds` thêm các cặp `(ContentKind.Clip, id)`, nên clip được chuẩn bị cùng bộ của bài và nhả cùng bộ đó.
  - Nạp một `VideoClip` từ Resources chỉ nạp đối tượng mô tả. Dữ liệu hình và tiếng do `VideoPlayer` đọc dần từ file khi phát, nên chuẩn bị 1–5 clip mỗi bài không tốn bộ nhớ đáng kể [Builder kiểm lại khi làm].

### 8.2 Bộ phát clip (`ClipPlayer`)
- Một `MonoBehaviour` duy nhất trên `AppRoot`, đặt cạnh `SpeechPlayer` và `SfxPlayer` (`AppRoot.Clips`). `LessonContext` có thêm trường `Clips`, có thể là `null` trong test màn. Màn gọi qua `Ctx.Clips?…`.
- Giữ **một** `VideoPlayer`, **một** `AudioSource` và **một** `RenderTexture`. `RenderTexture` tạo lần đầu cần, theo cỡ clip (1280×720, không có depth). Bắt đầu clip mới thì clip cũ dừng trước.
- API gợi ý [Builder được đổi tên]:
  - `bool CanPlay(string imageId)`: cài đặt bật, máy hỗ trợ, chưa bị tắt vì lỗi, và catalog có clip.
  - `Awaitable<bool> PlayAsync(Tile tile, string imageId)`: phát trên thẻ `tile`. Trả `true` khi phát hết; `false` khi không phát được, bị dừng, hay thẻ bị huỷ.
  - `void Stop()`.
  - `bool IsPlaying`, `string CurrentId` (cho test và `LessonScreen`).
  - `void ReleaseAll()`: dừng, bỏ tham chiếu clip, nhả `RenderTexture`.
- **Phần phát thật tách sau một giao diện** (ví dụ `IClipBackend`: chuẩn bị, phát, dừng, có khung đầu chưa, hết chưa, lỗi chưa, texture, cỡ). Bản thật dùng `VideoPlayer` với các thiết lập:
  - `renderMode = RenderTexture`, `isLooping = false`, `playOnAwake = false`, `waitForFirstFrame = true`, `skipOnDrop = true`;
  - `audioOutputMode = AudioSource`, gắn track 0.
  Test dùng bản giả, điều khiển được từng khung. Nhờ vậy logic phát được test mà không cần giải mã video thật [Đề xuất].
- `ClipPlayer` tự theo dõi giọng đọc mỗi khung: `Speech.IsBusy` thành `true` thì gọi `Stop()` (mục 6).
- Thẻ đang phát bị huỷ hay bị tắt (bước bị huỷ, trang lật) thì clip dừng; `ClipPlayer` không giữ thẻ đã chết.

### 8.3 Các màn
- `KeywordView`, `ItemsView` (`words`), `RiddleAnswerView`, `SpellView` (`tone_attach`): mỗi màn thêm một lần gọi `PlayAsync` đúng lúc ở mục 4, và nối thêm tranh đã có `Tapped` (hoặc thêm `Tapped` cho tranh chưa có) để xem lại. Không đổi bố cục.
- `LessonScreen`:
  - `Update` và `TrackStudyTime` coi `Clips.IsPlaying` là đang bận;
  - `OpenNotes` dừng clip.
- `AppRoot`:
  - tạo `ClipPlayer`; đặt cài đặt từ hồ sơ (mục 11); dừng clip khi app tạm dừng;
  - gọi `Clips.ReleaseAll()` ở `Present` (cạnh `Speech.Stop()`) và ở `HoldSet` **trước** khi nhả bộ cũ (mục 9).

## 9. Nạp và nhả bộ nhớ

- `VideoClip` của bài được chuẩn bị cùng bộ của bài (`AppRoot.ShowLesson` → `PrepareAsync(LessonAssets.ContentIds(...))`), nên bé không phải chờ nạp giữa bài. Lúc phát chỉ còn bước `VideoPlayer.Prepare()`, thường dưới nửa giây trên máy tính. Trong lúc đó bé vẫn thấy tranh tĩnh.
- Rời bài: `AppRoot` gọi `ReleaseAll()`. Bộ phát dừng, đặt `clip = null` và `targetTexture = null`, rồi nhả và huỷ `RenderTexture`. Sau đó bộ của bài được nhả như hiện nay (`ContentSet.Dispose` → `ReleaseUnused` → `Resources.UnloadUnusedAssets`). Vì bộ phát đã bỏ tham chiếu nên `VideoClip` được dọn.
  - **Thứ tự quan trọng.** `ShowLessonList` gọi `ReleaseCurrentSet()` (`AppRoot.cs` khoảng dòng 368, dọn ở dòng 542–543) **trước** `Present`. `Destroy` của màn học lại chạy trễ, nên `LessonScreen.OnDestroy` chạy sau `UnloadUnusedAssets`. Gọi `ReleaseAll` từ `LessonScreen.OnDestroy` thì `VideoClip` còn bị giữ lúc dọn và chỉ được nhả khi mở bài sau.
  - Vì vậy `ReleaseAll` phải gọi từ `AppRoot`: trong `HoldSet` trước `old.Dispose()`, và trong `Present` cạnh `Speech.Stop()`. Gọi nhiều lần không sao.
- `RenderTexture` 1280×720 RGBA tốn khoảng 3,5 MB, chỉ tồn tại khi đang ở màn học. Không bao giờ có hai `VideoPlayer` cùng lúc.
- Test đi qua nhiều bài liên tiếp (mục 14) kiểm tra: sau khi rời bài, không còn `RenderTexture` của bộ phát và không còn tham chiếu `VideoClip` nào.

## 10. Máy yếu, lỗi: dùng tranh tĩnh

- **Không thử phát** khi [Đề xuất, ngưỡng là hằng số]:
  - `SystemInfo.graphicsDeviceType == Null` (ví dụ chạy `-nographics`);
  - máy không tạo được `RenderTexture` ARGB32;
  - `SystemInfo.systemMemorySize < 2000` MB (máy 2 GB trở xuống).
- **Lỗi lúc chạy:**
  - `VideoPlayer.errorReceived`, hoặc quá 3 s (giờ thật) mà chưa có khung đầu: coi là hỏng. Clip đó dừng, tranh tĩnh vẫn hiện, ghi `Debug.LogWarning` một lần cho mỗi mã.
  - **2 lần hỏng liên tiếp** thì tắt clip đến hết lần mở app. Ví dụ: Windows bản N chưa cài Media Feature Pack nên không giải mã được H.264.
  - Phát thành công một lần thì đếm lại từ 0.
- Không bao giờ dùng `Debug.LogError` cho chuyện clip: thiếu clip hay máy không phát được là trạng thái bình thường, không phải lỗi dữ liệu.

## 11. Cài đặt cho phụ huynh

- Màn Cài đặt có thêm hàng **"Tranh động: Bật" / "Tranh động: Tắt"**, ngay dưới hàng tiếng động. Hàng này làm giống hệt nút tiếng động (`SfxToggle`, `ToggleSfx`) [Đề xuất].
- Lưu chung cho cả app như `sfx_off`: trường mới `clips_off` (mặc định `false`, tức là bật) trong `ProgressFile`, kèm thuộc tính `ProgressStore.ClipsEnabled`. Đặt lại dữ liệu thì về bật. File tiến độ cũ không có trường này thì đọc ra `false`, không cần đổi `schema`.
- Chữ hiện trên màn nằm trong `UiText` (`ClipsOn`, `ClipsOff`).
- Tắt giữa lúc đang học (ít xảy ra, vì phải vào màn phụ huynh) thì clip đang chạy dừng ngay.
- Hàng "Tiếng động" giữ nguyên nghĩa (tiếng chạm, lật trang, đúng) và **không** tắt tiếng clip. Tiếng clip là một phần của tranh động, nên chỉ theo hàng "Tranh động". Hai hàng độc lập [Đề xuất].

## 12. Đưa clip vào `Resources/`

- **Chỗ để:** `unity/TapDoc/Assets/Content/Resources/clips/<mã>.mp4`. Bỏ vào `.gitignore` cả thư mục và `clips.meta`, như `images/` và `audio/` [Đề xuất].
- **Đây là bản chép ra từ `content/clips/`**, không phải nguồn. Vì vậy:
  - không ghi vào `media_lock.json`;
  - không đóng vào `.unitypackage`; `media_lock.MEDIA_DIRS` vẫn chỉ là `images` và `audio`;
  - clip vẫn đi giữa các máy bằng zip clip và gói `bosung` như hiện nay;
  - `.meta` của clip không cần giữ GUID, vì app nạp theo đường dẫn. Thiết lập nhập do quy tắc nhập tự đặt (dưới).
- **Lệnh mới:** `python tools/run_unity_media.py clips` (Unity phải đóng, giống các lệnh khác của file này) [Đề xuất]:
  1. Đọc `video_manifest.json`. Clip phát được là clip có `status` thuộc `{dat, cho_duyet}` và có file. Tập trạng thái là một hằng số trong code.
  2. Chép vào `Resources/clips/`: thiếu thì chép; khác nội dung (so cỡ, rồi sha256) thì chép đè.
  3. Xoá khỏi `Resources/clips/` các `.mp4` (và `.meta`) không còn trong tập phát được. Đó là clip bị chuyển sang `khong_dat` hoặc bị bỏ.
  4. In số clip chép mới, chép đè, xoá, giữ nguyên, và các mã phát được mà thiếu file.
- `unpack` gọi bước đồng bộ này ở cuối, sau khi giải nén clip và nhập các gói `bosung`. Máy mới nhờ vậy có đủ clip.
- `tapdoc validate` thêm một cảnh báo (không phải lỗi) khi `Resources/clips/` lệch tập phát được, kèm gợi ý chạy lệnh `clips`.
- Ghi thêm một dòng về lệnh `clips` vào `SETUP-MAY-MOI.md` và `CHUYEN-MAY-MOI.md`, ở chỗ nói về nhập gói media.
- **Quy tắc nhập** (`ContentImportRules.OnPreprocessAsset`, hoặc hàm tiền xử lý video, cho `Assets/Content/Resources/clips/`) [Đề xuất]:
  - `VideoClipImporter`: **không chuyển mã** (`enableTranscoding = false`). File H.264/AAC gốc được dùng nguyên, nên không mất chất lượng và nhập nhanh.
  - `importAudio = true`, `sRGBClip = true`.
  - Lần nhập đầu của 323 clip có thể mất vài phút, và thư mục `Library/` lớn thêm khoảng 0,9 GB.
- **Quy trình khi clip đổi** (session tranh động làm lại clip, root đổi trạng thái): chạy `run_unity_media.py clips` trước khi build. Lệnh không đụng `content/`, không đụng danh mục.

## 13. Build Windows và về sau

- `BuildScript.BuildWindows` không cần đổi: clip trong `Resources/` tự vào bản build. Bản build lớn thêm khoảng 0,9 GB, chấp nhận được cho bản Windows chủ dự án dùng thử [Đề xuất].
- Trước khi build: chạy lệnh `clips`, rồi chạy các test của mục 14. Sau khi build: mở bản build, vào một bài có clip, xem clip chạy và nghe tiếng.
- **Bản điện thoại (không làm đợt này):** 885 MB clip vượt xa giới hạn file cài gốc của Google Play. Khi làm bản Android, root hoặc chủ dự án chọn một trong hai:
  - chuyển mã bằng chính bộ nhập của Unity (bitrate thấp hơn, cùng 720p);
  - giữ nguyên và dùng gói nội dung cài cùng app của Play (Play Asset Delivery, vẫn "cài một lần").
  Thiết kế này không chặn lựa chọn nào: chỉ đổi thiết lập nhập và cách build.

## 14. Test (làm theo TDD: viết test trước)

Chỉ chạy các lớp test liên quan, không chạy cả bộ [Chốt, quy định test có chọn lọc]. Test phải im lặng: tắt tiếng như các test hiện có.

**Giữ các test hiện có không bị clip làm phiền** [Đề xuất]:
- `AppTestBase.UseStubsForMissingAssets` nạp thật từ Resources trước khi dùng hình giả. Máy có `Resources/clips/` thì các test đi hết bài sẽ gặp `VideoClip` thật và phát video thật: chậm và có tiếng. Vì vậy `ClipPlayer` có cờ tĩnh `Enabled`, giống `IdleNudge.Enabled`. `AppTestBase` tắt cờ này khi bắt đầu và bật lại khi xong. Test của clip tự bật cờ và dùng bộ phát giả.
- `DataTests.ContentIds_IsUnionOfAudioAndImage` sửa thành hợp của âm thanh, tranh và clip.
- Test "mọi mã có tài nguyên" trong `DataTests` (khoảng dòng 100) bỏ qua loại `Clip`, vì thiếu clip là bình thường.

**EditMode**
- `ClipCropTests`: `uvRect` cho 1280×720 với `a = 1` là `(0,21875; 0; 0,5625; 1)`; clip vuông; clip dọc; `a ≠ 1`.
- `ContentPathsTests` (sửa): `Clip` → `clips/<mã>`, kiểu `VideoClip`.
- `LessonAssets` (thêm vào lớp test dữ liệu sẵn có): `ClipIds` lấy đúng 4 chỗ, bỏ Phần 2, không trùng; `ContentIds` có cặp `Clip`.
- `ProgressStoreTests` (thêm): `ClipsEnabled` mặc định bật, lưu và đọc lại, file cũ thiếu trường.
- Kiểm tra máy: hàm thuần nhận RAM và kiểu đồ hoạ, trả có phát hay không.

**PlayMode** (dùng bộ phát giả, trừ test cuối)
- `ClipPlayerTests`:
  - phát khi giọng đọc rảnh; không phát khi giọng đọc đang chạy;
  - giọng đọc bắt đầu thì clip dừng và lớp phủ được gỡ;
  - mỗi lúc một clip;
  - chỉ hiện lớp phủ khi đã có khung đầu;
  - hết clip thì gỡ lớp phủ và trả `true`;
  - lỗi hay quá giờ thì trả `false`, tranh tĩnh còn nguyên; 2 lần hỏng liên tiếp thì tắt; thành công thì đếm lại;
  - thẻ bị huỷ giữa chừng thì dừng;
  - `ReleaseAll` nhả `RenderTexture` và bỏ clip;
  - cài đặt tắt hay máy không hỗ trợ thì `CanPlay` là `false`;
  - thiếu clip không ghi lỗi nào (`LogAssert.NoUnexpectedReceived`).
- Test theo màn, dựa trên `ViewTestBase` và bộ phát giả:
  - `KeywordView`: tự phát sau lần app tự đọc; lần đó bị cắt bởi một lần chạm chữ thì phát sau khi đọc trọn lần chạm chữ đó; đã tự phát rồi thì chạm chữ không phát; chạm tranh luôn đọc rồi phát; bước vẫn báo xong như cũ (chỉ khi bé chạm);
  - `ItemsView` `words`: phát sau khi đọc trơn từ có tranh;
  - `RiddleAnswerView`: đoán đúng thì phát tranh đáp án, bước báo xong không chờ clip;
  - `SpellView` `tone_attach`: phát sau khi tranh hiện.
- `LessonScreen`: bấm Tiếp, về danh sách hay mở Ghi chú thì clip dừng; clip đang chạy thì không có lời nhắc khi ngồi im; bản sao lúc lật trang không có lớp phủ.
- `AppRoot`: rời bài (về danh sách, sang màn kết quả) thì `ReleaseAll` chạy **trước** khi bộ của bài được nhả. Dùng `FakeContentSource` ghi thứ tự: lúc nguồn được nhờ dọn, bộ phát không còn giữ `VideoClip` hay `RenderTexture`.
- `SettingsScreen`: hàng Tranh động đổi chữ, lưu lại, và tắt được clip.
- **Một test với `VideoPlayer` thật** (chỉ chạy khi có `Resources/clips/img_b01_bof.mp4`, không có thì `Inconclusive`):
  - nạp clip thật, chuẩn bị, có khung đầu trong 3 s, phát tới hết, tự gỡ lớp phủ;
  - `uvRect` đúng phần giữa.
  Test có thể chậm (khoảng 8 s), nên đánh dấu `Category("Clip")`.

**Python**
- `tools/tests/test_run_unity_media.py` (thêm), lệnh `clips` trên thư mục tạm:
  - chép `dat` và `cho_duyet`, bỏ `khong_dat`;
  - chép đè khi nội dung khác, để yên khi giống;
  - xoá clip đã thành `khong_dat` cùng `.meta`;
  - báo mã thiếu file;
  - `unpack` có gọi bước đồng bộ.

**Ảnh chụp cho root soát:** test chụp `phone_20x9` và `ipad_43`, mỗi máy 2 ảnh: giữa clip (khoảng 3 s, `KeywordView` của một bài có clip) và sau khi clip hết (tranh tĩnh). Lưu ở `TestOutput/screens/<máy>/clip_*.png`. Ảnh được gửi root soát; không đưa vào git.

## 15. Builder tự quyết và còn để ngỏ

- [Builder] Tên lớp, tên hàm, chia file; cách nhận "đã có khung đầu" (sự kiện `frameReady` cho khung 0, hay chờ `frame ≥ 0` sau `started`); cách xoá `RenderTexture` giữa hai clip.
- [Builder] Bài cụ thể dùng cho ảnh chụp và cho test với `VideoPlayer` thật, miễn là clip `dat` có sẵn.
- [Chốt, root 18/11] `img_b137_cais_thuwowcs` (cái thước) chỉ là phương án sai trong câu đố bài 137: để vậy, clip của nó không phát.
- [Chốt, root 18/11] Không làm dấu ▶ trên tranh có clip.
- [Chốt, root 18/11] Ảnh chụp soát (mục 14) có thêm một clip `build` (cây hay hoa) ở khoảng 0,2 s và 3 s, để root xem lúc chuyển có gắt không.
- [Để ngỏ, cho chủ dự án khi làm bản điện thoại] Dung lượng clip (mục 13).
