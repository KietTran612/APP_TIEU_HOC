# Bản đầu tiên — TV1 T1 bài 1–17 — Kế hoạch triển khai

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task (chủ dự án yêu cầu không dùng subagent). Steps use checkbox (`- [ ]`) syntax for tracking.

**Mục tiêu:** Có app chạy đủ 17 bài đầu của TV1 T1. App có:
- hồ sơ bé, lưu tiến độ, khóa bài theo thứ tự;
- mục "Ôn lại" lấy đúng các lượt bé đã nhầm;
- màn phụ huynh có khóa.

Âm thanh tạm và tranh đã qua trang duyệt của chủ dự án.

**Kiến trúc:** Kế hoạch xây tiếp trên bản mẫu (commit `fc0c75d`). Công cụ Python và hợp đồng dữ liệu được mở rộng thêm 3 loại bước mới: `tone_table`, `letter_grid` và `combine_table`. Riêng bước `picture` được phép kèm thêm `word`. Phía Unity thêm:
- 3 màn ứng với 3 loại bước mới;
- cách xếp tự xuống dòng khi dòng chữ quá dài;
- kho tiến độ là file JSON trong `persistentDataPath`, ghi theo kiểu ghi file tạm rồi đổi tên (không bao giờ ghi dở);
- các màn hồ sơ bé, danh sách bài có khóa, Ôn lại và phụ huynh.

**Công nghệ:** như bản mẫu: Unity 6.6 (`6000.6.5f1`), uGUI và TMP, `JsonUtility`; Python 3.14 với thư viện chuẩn và `unittest`.

**Bản thiết kế:** [docs/superpowers/specs/2026-10-28-app-tap-doc-mvp-design.md](../specs/2026-10-28-app-tap-doc-mvp-design.md). Các mục liên quan: 2, 5, 6, 12 (bước 2), 13 (phần "Bản đầu tiên") và 15. Kế hoạch bản mẫu: [2026-10-28-ban-mau-3-bai.md](2026-10-28-ban-mau-3-bai.md).

## Global Constraints

Mọi ràng buộc của kế hoạch bản mẫu vẫn giữ nguyên. Sau đây là các điểm mới hoặc đã đổi.

**Cách làm và git**
- **Không dùng subagent** (chủ dự án yêu cầu ngày 29/10/2026). Claude tự làm, tự review và chạy toàn bộ test sau mỗi task.
- **Git:**
  - Chỉ dùng branch `main`, commit tạm từng task.
  - Khi xong, gom mọi commit mới thành **1 commit** nằm trên `fc0c75d`, rồi push thường, không force.
  - Nếu GitHub đã có commit lạ thì dừng lại và hỏi chủ dự án.

**Thử, build và tài nguyên**
- **Thử trên máy tính:** test chạy batchmode. Đến bước chủ dự án thử, Claude build bản Windows và mở ở hai khung 1600×720 và 1440×1080. **Không build Android khi chủ dự án chưa yêu cầu.**
- **Tài nguyên:**
  - Chỉ điều khiển **Edge trên máy này**. Trước mọi thao tác phải kiểm tra `list_connected_browsers` có `onThisComputer: true` và `navigator.userAgentData.brands` có "Microsoft Edge".
  - Hỏi chủ dự án **một lần cho mỗi lô** trước khi tải về, nêu tên file, nguồn và dung lượng.

**Phạm vi nội dung**
- **Bản đầu tiên gồm bài 1–17.** Bài 42 vẫn được dựng (vì test dùng tới) nhưng **không hiện trong danh sách bài** [Chốt, mục 2].
- **Đánh vần, không phạt, phương án nhiễu, kí hiệu sách:** như bản mẫu. Nhắc lại vài điểm:
  - Bé sai lần đầu thì mời thử lại; sai lần hai thì gợi ý.
  - Phương án nhiễu chỉ dùng chữ đã học.
  - Các cặp giọng miền Nam đọc giống nhau không làm nhiễu của nhau trong bài nghe.
- **Nút và thẻ:** cạnh nhỏ nhất ≥ 160 đơn vị canvas. Bố cục vừa khung 1440×1080. Mọi dòng chữ hay dòng thẻ dài hơn vùng Stage phải tự xuống dòng.

**Hồ sơ bé và tiến độ**
- **Hồ sơ bé:** chỉ lưu tên gọi ở nhà (tối đa 20 ký tự) và hình đại diện do bé chọn. Không lưu thông tin định danh nào khác [Chốt, mục 3].
- **Phần thưởng [Đề xuất, mục 15]:**
  - Học xong một bài được 3 sao, không phụ thuộc số lần sai, không xếp hạng.
  - Chưa có nhân vật dẫn dắt.

## Review Focus

1. **File tiến độ hỏng hoặc bị ghi dở** (mất điện, JSON hỏng).
   - App không được dừng. App đổi tên file hỏng thành `.bak` và bắt đầu lại với dữ liệu trống. Mọi lần ghi đều qua file tạm rồi `File.Replace`/`Move`.
   - Test: `ProgressStoreTests.CorruptFile_IsBackedUpAndStartsFresh`, `ProgressStoreTests.Save_IsAtomic` (Task 7).
2. **Tên bé rỗng, toàn khoảng trắng hoặc quá dài.**
   - Tên được cắt khoảng trắng hai đầu và giới hạn 20 ký tự. Tên rỗng thì nút "Xong" không bấm được.
   - Test: `ProfileScreenTests.EmptyName_CannotCreate`, `ProgressStoreTests.Name_IsTrimmedAndCapped` (Task 7–8).
3. **Lượt bé nhầm đã lỗi thời trong "Ôn lại"** (bài được dựng lại khiến chỉ số lượt không còn, hoặc kiểu bài khác đi).
   - Lượt lỗi thời bị bỏ qua và xóa khỏi danh sách nhầm, không làm hỏng phiên ôn.
   - Test: `ReviewSessionTests.StaleMistake_IsDropped` (Task 9).
4. **Bé bấm bừa ở khóa phụ huynh.**
   - Bấm sai thì đổi sang phép tính mới. Không mở được nếu không có đáp án đúng, và cũng không bị khóa cứng.
   - Test: `ParentGateTests.WrongAnswer_ChangesQuestion`, `ParentGateTests.RightAnswer_Opens` (Task 10).
5. **Dòng đọc thêm hoặc câu dài tràn khung 4:3.** Ví dụ bài 15 có 9 tiếng một dòng, bài 12 câu có 8 tiếng.
   - Thẻ tự xuống dòng, không thẻ nào ra ngoài Stage.
   - Test: `FlowLayoutTests.WrapsWithinWidth` (Task 6), cùng `Layout_AllSteps_FitAndNoOverflow` cho cả 17 bài (Task 11).

## Việc tồn từ bản mẫu

Sổ ghi bản mẫu (`.superpowers/sdd/2026-10-28-ban-mau-3-bai/progress.md`) còn một số việc nhỏ. Kế hoạch này chỉ nhận các việc chạm tới bài 1–17:

| Việc | Task |
|---|---|
| `manifest.save_rows` chưa ghi qua file tạm, trong khi trang duyệt cũng ghi vào cùng file | 1 |
| `tieng_y` phải đọc là tiếng "i", không đọc tên chữ "i dài" | 5 |
| Thẻ kí hiệu dấu: dấu nhỏ và nằm cao | 6 |
| Thiếu tranh ngôi sao thì hiện ô vàng; còn chữ viết cứng ngoài `UiText` | 8 |

Các việc khác trong sổ không chạm tới bài 1–17 nên để sau. Ví dụ: chữ hoa ở bài 41, vần iê, cặp gi/v/s/x, script test chưa có giới hạn thời gian.

Màn rộng còn khoảng trống hai bên: giữ SafeWidth 1440 [Đề xuất], xem lại khi thử trên máy thật.

---

## Hợp đồng dữ liệu — phần mở rộng

Chỉ ghi phần thêm so với hợp đồng của kế hoạch bản mẫu.

**Item có thêm 4 trường**, không dùng thì để rỗng hoặc 0:

| Trường | Kiểu | Ý nghĩa |
|---|---|---|
| `col` | int | cột |
| `role` | string | `letter`, `tone`, `onset`, `vowel`, `base`, `form` hoặc `cell` |
| `tone` | string | dấu |
| `glyph` | string | kí hiệu dấu |

**Bước mới** (nguồn ở bên trái, bản dựng ở bên phải):

| Nguồn | Bản dựng |
|---|---|
| `{"type":"picture","image","say","word"?}` | Như cũ. `word` (không bắt buộc) không được xuất ra, chỉ đưa vào bảng tranh→chữ (R6) để tranh không chữ dùng được trong `listen_picture`. |
| `{"type":"tone_table","base":"đo","results":["đò","đó","đỏ","đõ","đọ"]}` | Bước gồm `text`=base, `audio` của base, và `items` là các ô. Mỗi ô: `role:"cell"`, `text`=kết quả, `audio`, `tone`, `glyph`, `spells`=[`[join base, tone, join kết quả]`]. Báo `BuildError` nếu `strip_tone(kết quả) != base`, hoặc hai ô trùng dấu. |
| `{"type":"letter_grid","letters":["o","a"…],"tones":["sac"…]}` | `items`: chữ cái có `role:"letter"`, `row` 0, `audio_for`. Dấu có `role:"tone"`, `row` 1, `text`=`glyph`, `tone`, `audio` `dau_*`. |
| `{"type":"combine_table","rows":[{"onset":"c","cells":{"o":["co","có","cò"],"a":["ca","cà","cả"]}}]}` | `items` gồm 4 vai: `role:"onset"` (`row`=i, `audio_for`); `role:"vowel"` (`col`=j, thứ tự gặp đầu tiên); `role:"base"` (`row`, `col`, `text`=phần tử đầu, `audio`, `spells`=[`spell_syllable`]); `role:"form"` (các phần tử còn lại, cùng `row`/`col`). Báo `BuildError` nếu base không bằng âm đầu + nguyên âm. |

**Bài:** thêm khóa `"in_app": true|false` (mặc định `true`). `index.json` chỉ liệt kê các bài có `in_app`. Bài 42 đặt `"in_app": false`.

**Kiểm tra dữ liệu:** thêm `python -m tapdoc validate --release`. Ngoài các kiểm tra cũ, lệnh này báo lỗi khi:
- có bài `in_app` mà `review.status` khác `da_duyet`;
- có âm thanh hoặc tranh ở trạng thái `chua_co` hay `cho_duyet` (`khong_dat` vẫn chấp nhận).

## Cấu trúc file (phần thêm)

```
content/src/tv1_t1_b01.json … b17.json      # bài mới: 01–03, 05–12, 14–17
tools/tapdoc/build.py, validate.py           # thêm 3 loại bước, `word`, `in_app`, `--release`
tools/tapdoc/manifest.py                     # save_rows ghi qua file tạm
tools/tests/test_build_mvp.py, test_mvp_content.py
unity/TapDoc/Assets/Scripts/Runtime/
  Steps/LetterGridView.cs, ToneTableView.cs, CombineTableView.cs
  UI/FlowLayout.cs
  Progress/ProgressData.cs, ProgressStore.cs
  App/ProfileScreen.cs, ParentScreen.cs, ParentGate.cs, ReviewSession.cs
  (sửa) Data/LessonData.cs, UI/Tile.cs, Text/UiText.cs, App/AppRoot.cs, App/LessonListScreen.cs,
        App/LessonScreen.cs, App/ResultScreen.cs, App/LessonContext.cs, Exercises/RoundViewBase.cs,
        Exercises/LookToneView.cs, Steps/ItemsView.cs, Steps/SentenceView.cs, Steps/SpellView.cs,
        Steps/ToneIntroView.cs, Steps/StepViewRegistry.cs
unity/TapDoc/Assets/Tests/EditMode/ProgressStoreTests.cs, FlowLayoutTests.cs, ParentGateTests.cs
unity/TapDoc/Assets/Tests/PlayMode/AppTestBase.cs, NewStepViewTests.cs, ProfileScreenTests.cs,
  ReviewSessionTests.cs, ParentScreenTests.cs, MvpEndToEndTests.cs
```

---

## Task 1: Công cụ — 3 loại bước mới, `word`, `in_app`, `--release`

**Files:**
- Modify: `tools/tapdoc/build.py`, `tools/tapdoc/validate.py`, `tools/tapdoc/__main__.py`, `tools/tapdoc/manifest.py` (`save_rows`)
- Modify: `content/src/tv1_t1_b42.json` (thêm `"in_app": false`)
- Test: `tools/tests/test_build_mvp.py`, thêm vào `tools/tests/test_validate.py` và `tools/tests/test_manifest.py`. Sửa `tools/tests/test_prototype_content.py`: danh sách bài không còn bài 42.

**Interfaces:**
- Consumes: `spell_syllable`, `strip_tone`, `split_syllable`, `TONE_INFO`, `audio_for`, `text_audio`, `tone_audio` (bản mẫu).
- Produces: bản dựng theo phần mở rộng hợp đồng ở trên; `validate_all(allow_missing=False, release=False)`; CLI `validate --release`.

- [ ] **Step 1: Viết test**

```python
def test_tone_table(self):
    s = mini(part1=[{"type": "tone_table", "base": "đo", "results": ["đò", "đó", "đỏ", "đõ", "đọ"]}])
    st = build_lesson(s).lesson["part1"][0]
    self.assertEqual((st["type"], st["text"], st["audio"]), ("tone_table", "đo", "tieng_ddo"))
    self.assertEqual([i["tone"] for i in st["items"]], ["huyen", "sac", "hoi", "nga", "nang"])
    self.assertEqual([p["audio"] for p in st["items"][3]["spells"][0]["parts"]], ["tieng_ddo", "dau_nga", "tieng_ddox"])
def test_tone_table_rejects_wrong_base(self):
    with self.assertRaises(BuildError): build_lesson(mini(part1=[{"type": "tone_table", "base": "đo", "results": ["đà"]}]))
def test_letter_grid(self):
    st = build_lesson(mini(part1=[{"type": "letter_grid", "letters": ["o", "c"], "tones": ["sac"]}])).lesson["part1"][0]
    self.assertEqual([(i["role"], i["text"], i["audio"], i["row"]) for i in st["items"]],
                     [("letter", "o", "van_o", 0), ("letter", "c", "am_c", 0), ("tone", "ˊ", "dau_sac", 1)])
def test_combine_table(self):
    st = build_lesson(mini(part1=[{"type": "combine_table", "rows": [
        {"onset": "c", "cells": {"o": ["co", "có"], "a": ["ca"]}}, {"onset": "d", "cells": {"o": ["do"]}}]}])).lesson["part1"][0]
    roles = [(i["role"], i["text"], i["row"], i["col"]) for i in st["items"]]
    self.assertIn(("onset", "c", 0, 0), roles); self.assertIn(("onset", "d", 1, 0), roles)
    self.assertIn(("vowel", "o", 0, 0), roles); self.assertIn(("vowel", "a", 0, 1), roles)
    self.assertIn(("base", "co", 0, 0), roles); self.assertIn(("form", "có", 0, 0), roles); self.assertIn(("base", "do", 1, 0), roles)
def test_picture_word_usable_in_listen_picture(self):
    s = mini(images={"img_b02_cof": "con cò", "img_b02_keos_co": "kéo co"},
             part1=[{"type": "keyword", "text": "kéo co", "image": "img_b02_keos_co"},
                    {"type": "picture", "image": "img_b02_cof", "say": "con cò", "word": "con cò"}],
             part2=[{"kind": "listen_picture", "word": "con cò", "answer": "img_b02_cof", "options": ["img_b02_keos_co", "img_b02_cof"]}])
    r = build_lesson(s); self.assertEqual(r.lesson["part2"][0]["options"][1]["text"], "con cò")
    self.assertNotIn("word", r.lesson["part1"][1])
def test_in_app_false_excluded_from_index(self):   # build_all vào thư mục tạm
    ids = [e["lesson_id"] for e in json.loads((out / "index.json").read_text("utf-8"))["lessons"]]
    self.assertNotIn("tv1_t1_b99", ids); self.assertTrue((out / "tv1_t1_b99.json").exists())
# test_validate.py
def test_release_rejects_unreviewed(self): ...  # bài in_app có review.status "chua_duyet" thì có Issue chứa "chưa duyệt"
def test_release_rejects_pending_assets(self): ...  # dòng âm thanh "cho_duyet" thì có Issue; dòng "khong_dat" thì không
# test_manifest.py
def test_save_rows_is_atomic(self):   # os.replace bị lỗi giữa chừng thì file cũ còn nguyên, không còn file .tmp
    save_rows(p, [{"id": "a"}])
    with mock.patch("tapdoc.manifest.os.replace", side_effect=OSError):
        with self.assertRaises(OSError): save_rows(p, [{"id": "b"}])
    self.assertEqual(load_rows(p), [{"id": "a"}]); self.assertEqual(list(p.parent.glob("*.tmp")), [])
```

  `mini(**kw)` là hàm dựng nguồn tối thiểu đặt trong file test. Nó có sẵn các trường bắt buộc và `part2=[]`; kiểm tra số lượt 6–10 thuộc `validate`, không thuộc `build`.
- [ ] **Step 2: Chạy test.** Từ thư mục `tools`: `python -m unittest tests.test_build_mvp tests.test_validate -v`. Phải FAIL.
- [ ] **Step 3: Cài đặt** theo phần "Hợp đồng dữ liệu — phần mở rộng".
  - Thứ tự `role:"vowel"` theo lần gặp đầu tiên khi duyệt `rows`.
  - Âm thanh của base và form lấy từ `text_audio`, ô lấy từ `spell_syllable`.
  - Gắn `"in_app": false` cho bài 42. Bài 42 vẫn được dựng ra JSON, vì nhiều test Unity của bản mẫu nạp thẳng bài này.
  - `save_rows`: ghi `<file>.tmp` rồi `os.replace`; lỗi giữa chừng thì xóa file tạm và báo lại lỗi.
- [ ] **Step 4: Chạy lại.** `python -m unittest discover -s tests -t .` phải PASS. `python -m tapdoc build` rồi `python -m tapdoc validate` phải ra `OK`.
- [ ] **Step 5: Commit** `feat(tools): bảng dấu, khung chữ, bảng ghép, tranh có từ, in_app và kiểm tra phát hành (MVP Task 1)`.

## Task 2: Nội dung bài 1, 2, 3, 5, 6

**Files:** Create `content/src/tv1_t1_b01.json`, `b02`, `b03`, `b05`, `b06`; Test `tools/tests/test_mvp_content.py`

**Quy tắc chung cho mọi bài trong Task 2–4:**
- Theo đúng khuôn của bài 4 và bài 13. Bước `spell` và `tone_attach` dùng `target`, có `then`. Bước `analyze` và `reading` dùng `rows`. Phần 2 gom theo `kind`, lượt cùng kiểu đặt trong `rounds`. Các bảng dưới chỉ viết tắt.
- `source.verification = "page_verified"`, `review.status = "chua_duyet"`.
- Phần ▨ "Em viết" bỏ qua.
- Tranh không có chữ trên trang dùng bước `picture`, có `say` (lời dẫn, gắn `can_duyet`) và `word` (để làm bài nghe chọn tranh).
- Đặt mã tranh theo quy ước `img_b<NN>_<telex>`. Mô tả tranh viết lại từ tranh gốc trên trang.

**Phần 1, chép từ trang sách** (đã xem ngày 29/10/2026):

| Bài | Trang (ảnh) | Các bước Phần 1 theo thứ tự |
|---|---|---|
| 1 "o" | 6 (004) | unit "o" → keyword "ò ó o... o!" (tranh gà trống gáy, mặt trời) → analyze ["ò ó o... o!","o","o"] → picture chùm nho (`word` "chùm nho") → picture con bò (`word` "con bò"; cần duyệt: tranh giống con trâu). Bài này **không có bước đánh vần** |
| 2 "c" | 7 (004) | unit "c" → keyword "kéo co" (tranh trẻ em kéo co, có con mèo) → analyze ["kéo co","co","c"] → spell "co" (then "kéo co") → picture con cò (`word` "con cò") → words ●▨ ["co"] |
| 3 "a" | 8 (005) | unit "a" → keyword "cái ca" → analyze ["cái ca","ca","a"] → spell "ca" (then "cái ca") → picture bà (`word` "bà") → picture quả cà (`word` "quả cà"; cần duyệt: quả cà hay quả bí) → words ●▨ ["ca"] |
| 5 "d đ" | 10 (006) | unit "d" → keyword "cặp da" → analyze ["cặp da","da","d"] → spell "da" (then "cặp da") → unit "đ" → keyword "cây đa" → analyze ["cây đa","đa","đ"] → spell "đa" (then "cây đa") → picture con dê (`word` "con dê") → picture con đò (`word` "con đò") → words ●▨ ["da","đò"] → reading ⌂ [["do","dò","dó"],["đa","đò","đá"]] |
| 6 "Dấu hỏi - Dấu ngã - Dấu nặng" | 11 (006) | tone_intro hoi → tone_attach "cỏ" (tranh bụi cỏ) → tone_intro nga → tone_attach "ngã" (tranh em bé ngã; "ng" chưa học nên bản dựng tự gắn `can_duyet` tên tạm "ngờ đơn", giống bài 42) → tone_intro nang → tone_attach "cọ" (tranh cây cọ) → tone_table "đo" ["đò","đó","đỏ","đõ","đọ"] → words ●▨ ["cò","cỏ","cọ"] → reading ⌂ [["đo","đò","đó","đỏ","đõ","đọ"],["đo đỏ","dạ"]] |

**Phần 2.** Đủ 6–10 lượt và phải qua `validate`. Kí hiệu:
- LC: `listen_choose` (đáp án | phương án)
- LA: `listen_choose` có `tag` `look_alike`
- LT: `look_tone` (chữ mẫu | dấu)
- CP: `compose` (từ, khuôn ← đáp án | phương án)
- LP: `listen_picture` (từ → tranh | các tranh của bài)

| Bài | Các lượt |
|---|---|
| 1 | LP ×6, mỗi lượt đủ 3 tranh. Từ đề lần lượt: "ò ó o... o!" (tranh gà gáy), "chùm nho", "con bò", "chùm nho", "con bò", "ò ó o... o!". Tranh gà gáy gắn với chữ của bước keyword, nên từ đề phải đúng chữ đó, không dùng "gà" (bản dựng báo lỗi khi từ đề khác chữ của tranh đáp án) |
| 2 | LC c\|[c,o]; LC o\|[o,c]; LA c\|[c,o], o\|[c,o], c\|[c,o]; CP "co" "c_"←"o"\|[o,c]; LP "kéo co", "con cò". Bé mới học 2 chữ nên mỗi lượt chỉ có 2 thẻ |
| 3 | LC a\|[a,o,c]; LC o\|[o,a,c]; LA a\|[a,o] ×3 (a, o, a); CP "ca" "c_"←"a"\|[a,o]; LP "cái ca", "bà" |
| 5 | LC d\|[d,đ,c]; LC đ\|[đ,d,o]; LA da\|[da,đa], đa\|[da,đa], dó\|[dó,đó]; CP "đò" "đ_"←"ò"\|[ò,ó,o]; LP "cặp da", "con đò" |
| 6 | LT đỏ\|[hoi,nga]; LT đõ\|[hoi,nga]; LT cọ\|[nang,sac]; LC đò\|[đò,đó,đọ]; LC đó\|[đó,đò,đọ]; CP "cỏ" "c_"←"ỏ"\|[ỏ,ọ,ó]; LP "cỏ", "cọ" |

- [ ] **Step 1: Viết test** `test_mvp_content.py`. Test dựng mọi nguồn trong `CONTENT_SRC`, rồi kiểm tra:

```python
self.assertEqual([s["type"] for s in L["tv1_t1_b01"]["part1"]], ["unit", "keyword", "analyze", "picture", "picture"])
self.assertFalse(any(s["type"] == "spell" for s in L["tv1_t1_b01"]["part1"]))
self.assertEqual([p["audio"] for p in L["tv1_t1_b02"]["part1"][3]["spell"]["parts"]], ["am_c", "van_o", "tieng_co"])
self.assertEqual([i["text"] for i in L["tv1_t1_b06"]["part1"][6]["items"]], ["đò", "đó", "đỏ", "đõ", "đọ"])
self.assertEqual([i["text"] for i in L["tv1_t1_b05"]["part1"][-1]["items"]], ["do", "dò", "dó", "đa", "đò", "đá"])
for lid in ("tv1_t1_b01", "tv1_t1_b02", "tv1_t1_b03", "tv1_t1_b05", "tv1_t1_b06"):
    self.assertTrue(6 <= len(L[lid]["part2"]) <= 10, lid)
```

- [ ] **Step 2: Viết 5 file nguồn.** Chạy `python -m tapdoc build` rồi `python -m tapdoc validate --allow-missing`, phải ra `OK`.
- [ ] **Step 3: Chạy test** `python -m unittest tests.test_mvp_content -v`. Phải PASS.
- [ ] **Step 4: Commit** `feat(content): nguồn bài 1, 2, 3, 5, 6 (MVP Task 2)`.

## Task 3: Nội dung bài 7, 8, 9, 10, 11

**Files:** Create `content/src/tv1_t1_b07.json` … `b11`; Modify `tools/tests/test_mvp_content.py`

| Bài | Trang (ảnh) | Phần 1 |
|---|---|---|
| 7 Ôn tập | 12 (007) | letter_grid ["o","a","c","d","đ"] + dấu [sac,huyen,hoi,nga,nang] → combine_table: c {o:[co,có,cò], a:[ca,cà,cả]}; d {o:[do,dó,dò], a:[da,dạ]}; đ {o:[đo,đó,đỏ], a:[đa,đá]} |
| 8 "ô ơ" | 13 (007) | unit "ô" → keyword "cái ô" → analyze ["cái ô","ô","ô"] → unit "ơ" → keyword "lá cờ" → analyze ["lá cờ","cờ","ơ"] → spell "cờ" (then "lá cờ") → picture ba lô (`word` "ba lô") → picture quyển vở (`word` "quyển vở") → words ●▨ ["cô","cờ"] → reading ⌂ [["cổ","cớ","dỗ","dở","đỗ"],["đơ đã","cá cờ"]] |
| 9 "e ê" | 14 (008) | unit "e" → keyword "cái đe" → analyze ["cái đe","đe","e"] → spell "đe" (then "cái đe") → unit "ê" → keyword "con dế" → analyze ["con dế","dế","ê"] → spell "dế" (then "con dế") → picture con ve (`word` "con ve") → picture búp bê (`word` "búp bê") → words ●▨ ["đe","dế"] → reading ⌂ [["de","đe","dê","đê"],["e dè","dê dễ"]] |
| 10 "i t" | 15 (008) | unit "i" → keyword "đi đò" → analyze ["đi đò","đi","i"] → spell "đi" (then "đi đò") → unit "t" → keyword "ô tô" → analyze ["ô tô","tô","t"] → spell "tô" (then "ô tô") → picture hòn bi (`word` "hòn bi") → picture cái tủ (`word` "cái tủ") → sentence ●▨ "tí đi ô tô" → reading ⌂ [["di","đi","ta","tô","tơ","tê","ti"],["tí ti","cá to","tổ dế"]] |
| 11 Ôn tập | 16 (009) | letter_grid ["ô","ơ","e","ê","i","t"] (không có dấu) → combine_table: 3 hàng t/d/đ × nguyên âm [a,o,ô,ơ,e,ê,i], mỗi ô chỉ có base (ta…ti, da…di, đa…đi). Dòng ghi chú cho giáo viên ("Học sinh giỏi có thể ghép thêm dấu thanh") không đưa vào app |

| Bài | Phần 2 |
|---|---|
| 7 | LC c\|[c,d,đ]; LA do\|[do,đo], đa\|[da,đa]; CP "dạ" "d_"←"ạ"\|[ạ,á,à]; LT cả\|[hoi,nga]; LT đỏ\|[hoi,nga]; LC cò\|[cò,có,co]; LC dạ\|[dạ,da,dà] |
| 8 | LC ô\|[ô,ơ,o]; LC ơ\|[ơ,ô,a]; LA cô\|[cô,cơ], cơ\|[cô,cơ], đô\|[đô,đơ]; CP "cờ" "c_"←"ờ"\|[ờ,ồ,ò]; LP "cái ô", "lá cờ" |
| 9 | LC e\|[e,ê,a]; LC ê\|[ê,e,ô]; LA de\|[de,dê], đê\|[đe,đê], dê\|[de,dê]; CP "dế" "d_"←"ế"\|[ế,ề,ể]; LP "cái đe", "con ve" |
| 10 | LC i\|[i,t,e]; LC t\|[t,đ,i]; LA tô\|[tô,đô], đi\|[đi,ti], ta\|[ta,đa]; CP "tô" "t_"←"ô"\|[ô,ơ,o]; LP "đi đò", "cái tủ" |
| 11 | LC ô\|[ô,ơ,o]; LC ê\|[ê,e,i]; LA tê\|[tê,te], đơ\|[đơ,đô]; CP "tơ" "t_"←"ơ"\|[ơ,ô,a]; LT đỗ\|[hoi,nga]; LC di\|[di,đi,ti]; LC tô\|[tô,to,tơ] |

- [ ] **Step 1: Thêm test.**

```python
st = L["tv1_t1_b07"]["part1"][1]
self.assertEqual(st["type"], "combine_table")
self.assertEqual(sorted(i["text"] for i in st["items"] if i["role"] == "base"), ["ca", "co", "da", "do", "đa", "đo"])
self.assertEqual(len([i for i in L["tv1_t1_b11"]["part1"][1]["items"] if i["role"] == "base"]), 21)
self.assertEqual(L["tv1_t1_b10"]["part1"][-2]["text"], "tí đi ô tô")
self.assertTrue(any(n["where"].startswith("part1[3]") for n in L["tv1_t1_b10"]["review"]["can_duyet"]))   # i đọc "i ngắn"
```

- [ ] **Step 2: Viết 5 file nguồn.** `build` rồi `validate --allow-missing` phải ra `OK`.
- [ ] **Step 3: Chạy test.** Phải PASS.
- [ ] **Step 4: Commit** `feat(content): nguồn bài 7–11 (MVP Task 3)`.

## Task 4: Nội dung bài 12, 14, 15, 16, 17; cập nhật mức xác minh

**Files:**
- Create `content/src/tv1_t1_b12.json`, `b14`, `b15`, `b16`, `b17`
- Modify `docs/source-inventory/LESSON_INDEX.csv`: đổi `muc_xac_minh` của bài 9, 10, 11, 12, 15, 16, 17 thành `page_verified`
- Modify `tools/tests/test_mvp_content.py`

| Bài | Trang (ảnh) | Phần 1 |
|---|---|---|
| 12 "n m" | 17 (009) | unit "n" → keyword "ca nô" → analyze ["ca nô","nô","n"] → spell "nô" (then "ca nô") → unit "m" → keyword "quả mơ" → analyze ["quả mơ","mơ","m"] → spell "mơ" (then "quả mơ") → picture nụ hoa (`word` "nụ hoa") → picture quả me (`word` "quả me") → sentence ● "tí đi ô tô, má đi ca nô" → reading ⌂ [["no","nô","nơ"],["me","mê","mi"],["na ná","nơ đỏ","tò mò"]] |
| 14 "y" | 19 (010) | unit "y" → keyword "cô y tá" → analyze ["cô y tá","y","y"] → spell "y" (then "cô y tá") → words ["y tế","y tá","tỉ tê","tỉ mỉ"] (bảng so sánh y/i; spell mặc định) → sentence ● "tổ y tế có cô y tá" → reading ⌂ [["y tế","y tá"],["tỉ tê","tỉ mỉ"]] |
| 15 "l" | 20 (011) | unit "l" → keyword "cái lọ" → analyze ["cái lọ","lọ","l"] → spell "lọ" (then "cái lọ") → words [{"lá", tranh chiếc lá}, {"xe lu", tranh xe lu, spell ["lu"]}] → sentence ● "tí có lá cờ đỏ" → reading ⌂ [["la","lo","lô","lơ","le","lê","li","lu","lư"],["lơ là","lí lẽ","lá đa","lọ mỡ"]] |
| 16 "b" | 21 (011) | unit "b" → keyword "ba ba" → analyze ["ba ba","ba","b"] → spell "ba" (then "ba ba") → words [{"bò", tranh bò và bê}, {"bê"}] → sentence ● "bà bế bé" → sentence ● "bé bá cổ bà." → reading ⌂ [["ba","bo","bô","be","bê","bi","bu","bư"],["bé bi bô","ba bó lá"]] |
| 17 Ôn tập | 22 (012) | letter_grid ["u","ư","y","n","m","l","b"] → combine_table: 4 hàng n/m/l/b × [a,o,ô,ơ,e,ê,i,u,ư], chỉ có base → words ["y tế","y tá","y bạ"] |

| Bài | Phần 2 |
|---|---|
| 12 | LC n\|[n,m,t]; LC m\|[m,n,đ]; LA nô\|[nô,mô], mơ\|[mơ,nơ], me\|[me,ne]; CP "mơ" "m_"←"ơ"\|[ơ,ô,o]; LP "ca nô", "quả me" |
| 14 | LC y\|[y,u,ư]; LC i\|[i,e,ê]; LA tí\|[tí,tú]; LA y\|[y,u]; CP "tá" "t_"←"á"\|[á,à,ả]; LT tỉ\|[hoi,nga]; LT mỉ\|[hoi,nga]; LC tế\|[tế,tê,tề] |
| 15 | LC l\|[l,t,i]; LC lá\|[lá,lọ,lu]; LA lo\|[lo,to], lê\|[tê,lê], li\|[li,ti]; CP "lọ" "l_"←"ọ"\|[ọ,ó,ỏ]; LP "lá", "xe lu" |
| 16 | LC b\|[b,d,đ]; LA ba\|[ba,da], bô\|[bô,dô], be\|[be,de]; LC bé\|[bé,bè,bẻ]; CP "bê" "b_"←"ê"\|[ê,e,ô]; LP "ba ba", "bò" |
| 17 | LC u\|[u,ư,y]; LC n\|[n,m,l]; LA bi\|[bi,di]; LA lu\|[lu,tu]; CP "bơ" "b_"←"ơ"\|[ơ,ô,o]; LT mỡ\|[hoi,nga]; LC lá\|[lá,là,lạ]; LC mù\|[mù,mú,mụ] |

- [ ] **Step 1: Thêm test.**

```python
self.assertEqual([s["type"] for s in L["tv1_t1_b16"]["part1"]].count("sentence"), 2)
self.assertEqual([p["audio"] for p in L["tv1_t1_b14"]["part1"][3]["spell"]["parts"]], ["van_y", "tieng_y"])
self.assertEqual(len(L["tv1_t1_b15"]["part1"][-1]["items"]), 13)
ids = [e["lesson_id"] for e in json.loads((UNITY_RES / "lessons" / "index.json").read_text("utf-8"))["lessons"]]
self.assertEqual(ids, [f"tv1_t1_b{n:02d}" for n in range(1, 18)])          # 17 bài, không có bài 42
for lid, lesson in L.items():   # y và i cùng đọc /i/: không làm nhiễu của nhau trong bài nghe
    for r in lesson["part2"]:
        if r["kind"] == "listen_choose":
            self.assertFalse({"i", "y"} <= {o["text"] for o in r["options"]}, lid)
```

- [ ] **Step 2: Viết 5 file nguồn và sửa CSV.** `build` rồi `validate --allow-missing` phải ra `OK`.
- [ ] **Step 3: Chạy toàn bộ test Python và Unity.** Python, `editmode`, `playmode` đều phải PASS. Danh sách bài giờ bắt đầu bằng bài 1, nên sửa test Unity nào giả định bài đầu danh sách là bài 4 (ví dụ `AppFlowTests`).
- [ ] **Step 4: Commit** `feat(content): nguồn bài 12, 14–17; 17 bài trong danh sách (MVP Task 4)`.

## Task 5: Âm thanh tạm và tranh cho bài 1–17, cùng hình đại diện

**Files:**
- Modify `tools/tapdoc/system_assets.py`: thêm 6 hình đại diện `img_chung_avatar_01` … `_06` ("con mèo", "con chó", "con thỏ", "con gà con", "con cá", "con voi"), cùng phong cách sách.
- Tạo bằng công cụ: `unity/TapDoc/Assets/Content/Resources/audio/*.mp3`, `images/*.png`.

**Cách làm:** Claude tự làm trong phiên chính, giống Task 11–12 của bản mẫu.
1. **Kiểm tra trình duyệt:** chỉ dùng Edge của máy này (Global Constraints).
2. **Sinh gói yêu cầu:** `python -m tapdoc requests`.
3. **Âm thanh:** dán từng lô vào một cuộc trò chuyện mới trong dự án Kiet_1.
4. **Tranh:** dùng đoạn JS gửi lần lượt từng yêu cầu. Nút đang vẽ có nhãn `aria-label="Ngừng"`, nút gửi có nhãn `"Gửi"`.
5. **Ghép tranh với mã:** cuộn hết cuộc trò chuyện, ghép mỗi khung `generated-image-gallery` với dòng "Mã tranh:" đứng ngay trước nó.
6. **Xin phép tải:** hỏi chủ dự án **một lần cho cả lô**, nêu tên file, nguồn và dung lượng.
7. **Tải tranh:** dùng `fetch` → blob → thẻ `<a download="<mã>.png">` ngay khi vừa lấy link, vì link có hạn ngắn.
8. **Nhập vào project:** `import-audio` và `import-image`.
9. **Kiểm tra tranh khớp mã:** ghép ảnh lưới có nhãn bằng `System.Drawing` rồi xem.

- [ ] **Step 1:** Thêm 6 hình đại diện vào `SYSTEM_IMAGES`. Chạy `build`, rồi `requests`, và ghi lại số mã `chua_co`.
- [ ] **Step 2:** Tạo âm thanh theo từng lô, xin phép rồi tải, `import-audio`. Mã nào bị bỏ qua thì gom vào lô sau.
  - Lời nhắc trong lô có `tieng_y`: đọc là tiếng "i" (như trong "y tá"), không đọc tên chữ "i dài".
- [ ] **Step 3:** Tạo tranh, xem ảnh lưới để kiểm tra mã, xin phép rồi tải, `import-image`.
- [ ] **Step 4:** `python -m tapdoc build` rồi `python -m tapdoc validate`. Phải ra `OK`, không còn mã `chua_co`.
- [ ] **Step 5: Commit** `feat(content): âm thanh tạm và tranh bài 1–17, hình đại diện (MVP Task 5)`.

## Task 6: Màn cho 3 loại bước mới; tự xuống dòng

**Files:**
- Create `Runtime/Steps/LetterGridView.cs`, `ToneTableView.cs`, `CombineTableView.cs`, `Runtime/UI/FlowLayout.cs`
- Modify `Runtime/Data/LessonData.cs` (Item thêm `col`, `role`, `tone`, `glyph`), `UI/Tile.cs`, `Steps/ItemsView.cs`, `Steps/SentenceView.cs`, `Steps/StepViewRegistry.cs`, `Steps/ToneIntroView.cs`, `Steps/SpellView.cs`, `Exercises/LookToneView.cs`
- Test `Tests/EditMode/FlowLayoutTests.cs`, `Tests/PlayMode/NewStepViewTests.cs`

**Interfaces:**
- Produces: `static List<Vector2> FlowLayout.Place(IReadOnlyList<float> widths, float height, float maxWidth, float gap, float lineGap)`. Hàm trả tâm của từng ô, các dòng căn giữa, khối căn giữa theo chiều dọc quanh (0,0).
- Ba màn:

| Màn | Hiển thị và thao tác | Báo `Completed` khi |
|---|---|---|
| `LetterGridView` | Hàng chữ và hàng dấu; chạm để nghe | Bé đã chạm mọi thẻ |
| `ToneTableView` | Tiếng gốc; 5 ô có sẵn kí hiệu dấu như trong sách; 5 thẻ dấu kéo được (xáo thứ tự) | Đủ 5 ô. Kéo đúng ô thì ô hiện tiếng có dấu và app làm mẫu đánh vần; sai ô thì thẻ trượt về, không phạt |
| `CombineTableView` | Cột âm đầu và hàng nguyên âm; chọn âm đầu rồi nguyên âm thì app làm mẫu đánh vần base và hiện các thẻ tiếng có dấu (chạm để nghe đánh vần) [Đề xuất: chạm, chưa kéo dấu] | Mỗi âm đầu đã được ghép ít nhất một lần |

- `ItemsView` (bước `reading`, và bước `words` không có tranh) cùng `SentenceView` dùng `FlowLayout` với `maxWidth` = bề rộng Stage − 40.
- `internal void Tile.SetTone(string tone)`: ghi `Tone` và bật kiểu thẻ kí hiệu dấu. Ở kiểu này, cỡ chữ gấp 1,6 lần cỡ tối đa của thẻ và kí hiệu nằm giữa thẻ theo chiều dọc. Mọi thẻ chỉ chứa một kí hiệu dấu đều gọi hàm này: `ToneIntroView`, mảnh dấu trong `SpellView`, phương án của `LookToneView`, và các thẻ dấu của hai màn mới.

- [ ] **Step 1: Viết test.**

```csharp
// EditMode
[Test] public void WrapsWithinWidth() {
    var w = Enumerable.Repeat(190f, 9).ToList(); var p = FlowLayout.Place(w, 170f, 1360f, 24f, 20f);
    Assert.That(p.Select(v => v.y).Distinct().Count(), Is.EqualTo(2));
    for (var i = 0; i < 9; i++) { Assert.LessOrEqual(Mathf.Abs(p[i].x) + 95f, 680f); } }
[Test] public void SingleLine_IsCentered() { var p = FlowLayout.Place(new[] { 200f, 200f }, 100f, 1360f, 20f, 20f);
    Assert.AreEqual(-110f, p[0].x, .01f); Assert.AreEqual(110f, p[1].x, .01f); Assert.AreEqual(0f, p[0].y, .01f); }
// PlayMode (ViewTestBase)
[UnityTest] public IEnumerator ToneTable_FillAllFive() {
    var v = Bind("tv1_t1_b06", 6);
    DragForTone(v, "hoi").SimulateDropOn(SlotForTone(v, "huyen")); yield return null; Assert.IsFalse(Done(v));   // sai ô
    foreach (var t in new[] { "huyen", "sac", "hoi", "nga", "nang" }) { DragForTone(v, t).SimulateDropOn(SlotForTone(v, t)); yield return new WaitForSeconds(.3f); }
    yield return WaitCompleted(v); Assert.That(Labels(v), Is.SupersetOf(new[] { "đò", "đó", "đỏ", "đõ", "đọ" })); }
[UnityTest] public IEnumerator LetterGrid_AllTapped() { var v = Bind("tv1_t1_b07", 0); yield return ((ITestCompletable)v).CompleteForTest(); Assert.IsTrue(Done(v)); }
[UnityTest] public IEnumerator CombineTable_EachOnsetOnce() {
    var v = Bind("tv1_t1_b07", 1);
    TileWithText(v, "c").SimulateTap(); TileWithText(v, "o").SimulateTap(); yield return new WaitForSeconds(.5f);
    Assert.That(Ctx.Speech.History, Has.Member("tieng_co")); Assert.That(Labels(v), Has.Member("có")); Assert.IsFalse(Done(v));
    TileWithText(v, "d").SimulateTap(); TileWithText(v, "a").SimulateTap(); yield return new WaitForSeconds(.5f);
    TileWithText(v, "đ").SimulateTap(); TileWithText(v, "o").SimulateTap(); yield return WaitCompleted(v); }
[UnityTest] public IEnumerator GlyphTile_IsCenteredAndLarge() {   // việc tồn: dấu nhỏ và nằm cao
    var v = Bind("tv1_t1_b06", 0); yield return null;
    var tile = RootOf(v).GetComponentsInChildren<Tile>(true).First(t => t.Tone == "hoi");
    var tmp = tile.GetComponentInChildren<TMP_Text>(); tmp.ForceMeshUpdate(); var h = ((RectTransform)tile.transform).rect.height;
    Assert.LessOrEqual(Mathf.Abs(tmp.textBounds.center.y), .15f * h); Assert.GreaterOrEqual(tmp.textBounds.size.y, .3f * h); }
```

  `SlotForTone`, `DragForTone` là các hàm hỗ trợ trong `ViewTestBase`: tìm `DropSlot` hoặc `DragTile` có `Tile.Tone == t`. `Tile.Tone` là `internal string`, do `SetTone` ghi.
- [ ] **Step 2: Chạy test.** `python run_unity_tests.py editmode --filter FlowLayoutTests` và `playmode --filter NewStepViewTests` phải FAIL.
- [ ] **Step 3: Cài đặt.** Viết 3 màn và `FlowLayout`, đăng ký `letter_grid`, `tone_table`, `combine_table`. Cho `ItemsView` và `SentenceView` dùng `FlowLayout`. Thêm `Tile.SetTone` và gọi ở các màn đã nêu.
- [ ] **Step 4: Chạy toàn bộ EditMode và PlayMode.** Phải PASS.
- [ ] **Step 5: Commit** `feat(unity): bảng dấu, khung chữ, bảng ghép; tự xuống dòng (MVP Task 6)`.

## Task 7: Kho tiến độ — hồ sơ bé, sao, khóa bài, lượt nhầm

**Files:**
- Create `Runtime/Progress/ProgressData.cs`, `ProgressStore.cs`
- Test `Tests/EditMode/ProgressStoreTests.cs`

**Interfaces (namespace `TapDoc`):**
- **DTO (JsonUtility):**
  - `ProgressFile{int schema=1; List<Profile> profiles; string current}`
  - `Profile{string id; string name; string avatar; List<LessonProgress> lessons; List<Mistake> mistakes}`
  - `LessonProgress{string lesson_id; bool completed; int stars}`
  - `Mistake{string lesson_id; int round; int count; long last_ticks}`
- **`ProgressStore`:**
  - Khởi tạo: `ProgressStore(string path)`.
  - Mặc định dùng `Path.Combine(Application.persistentDataPath, "tapdoc_progress.json")` qua `ProgressStore.Default()`.
  - `Profile Current` (null khi chưa có hồ sơ), `IReadOnlyList<Profile> Profiles`.
  - `Profile CreateProfile(string name, string avatar)`: cắt khoảng trắng hai đầu, tối đa 20 ký tự; tên rỗng thì báo `ArgumentException`. Hồ sơ mới thành `Current`.
  - `void Select(string profileId)`.
  - `bool IsUnlocked(IReadOnlyList<string> orderedLessonIds, string lessonId)`: bài đầu luôn mở; bài k mở khi bài k−1 đã `completed`.
  - `void MarkCompleted(string lessonId, int stars = 3)`.
  - `void RecordMistake(string lessonId, int round)`, `void ClearMistake(string lessonId, int round)`.
  - `IReadOnlyList<Mistake> Mistakes(int max = 8)`: sắp theo `count` giảm dần rồi `last_ticks` giảm dần.
  - `void Save()`: ghi `<path>.tmp`, rồi `File.Replace` (hoặc `Move` nếu chưa có file).
  - `static ProgressStore Load(string path)`: file hỏng thì đổi tên thành `<path>.bak` và trả về kho trống.

- [ ] **Step 1: Viết test.**

```csharp
[Test] public void CreateSelectAndPersist() { var s = new ProgressStore(P); var p = s.CreateProfile("  Bông  ", "img_chung_avatar_01");
    Assert.AreEqual("Bông", p.name); s.MarkCompleted("tv1_t1_b01"); s.Save();
    var t = ProgressStore.Load(P); Assert.AreEqual("Bông", t.Current.name); Assert.IsTrue(t.Current.lessons.Single().completed); }
[Test] public void Name_IsTrimmedAndCapped() { var s = new ProgressStore(P);
    Assert.AreEqual(20, s.CreateProfile(new string('a', 30), "x").name.Length); Assert.Throws<ArgumentException>(() => s.CreateProfile("   ", "x")); }
[Test] public void UnlockInOrder() { var s = new ProgressStore(P); s.CreateProfile("A", "x"); var ids = new[] { "b01", "b02", "b03" };
    Assert.IsTrue(s.IsUnlocked(ids, "b01")); Assert.IsFalse(s.IsUnlocked(ids, "b02")); s.MarkCompleted("b01"); Assert.IsTrue(s.IsUnlocked(ids, "b02")); }
[Test] public void Mistakes_CountAndClear() { var s = new ProgressStore(P); s.CreateProfile("A", "x");
    s.RecordMistake("b13", 2); s.RecordMistake("b13", 2); s.RecordMistake("b04", 0);
    Assert.AreEqual(("b13", 2, 2), (s.Mistakes()[0].lesson_id, s.Mistakes()[0].round, s.Mistakes()[0].count));
    s.ClearMistake("b13", 2); Assert.AreEqual(1, s.Mistakes().Count); }
[Test] public void ProfilesAreSeparate() { var s = new ProgressStore(P); var a = s.CreateProfile("A", "x"); s.MarkCompleted("b01");
    s.CreateProfile("B", "y"); Assert.IsEmpty(s.Current.lessons); s.Select(a.id); Assert.AreEqual(1, s.Current.lessons.Count); }
[Test] public void CorruptFile_IsBackedUpAndStartsFresh() { File.WriteAllText(P, "{hỏng");
    var s = ProgressStore.Load(P); Assert.IsEmpty(s.Profiles); Assert.IsTrue(File.Exists(P + ".bak")); }
[Test] public void Save_IsAtomic() { var s = new ProgressStore(P); s.CreateProfile("A", "x"); s.Save();
    Assert.IsFalse(File.Exists(P + ".tmp")); StringAssert.Contains("\"A\"", File.ReadAllText(P)); }
```

  `P` là đường dẫn trong `Path.GetTempPath()`, được xóa ở TearDown.
- [ ] **Step 2: Chạy test.** Phải FAIL. **Step 3: Cài đặt.** **Step 4: Chạy lại.** Phải PASS.
- [ ] **Step 5: Commit** `feat(unity): kho tiến độ, hồ sơ bé, khóa bài, lượt nhầm (MVP Task 7)`.

## Task 8: Màn chọn bé, danh sách bài có khóa và sao, ghi tiến độ khi học xong

**Files:**
- Create `Runtime/App/ProfileScreen.cs`
- Modify `App/AppRoot.cs`, `App/LessonListScreen.cs`, `App/ResultScreen.cs`, `App/LessonContext.cs`, `Exercises/RoundViewBase.cs`, `App/LessonScreen.cs`, `Text/UiText.cs`
- Test: Create `Tests/PlayMode/AppTestBase.cs`, `Tests/PlayMode/ProfileScreenTests.cs`; sửa `AppFlowTests`, `PrototypeEndToEndTests` cho hợp

**Interfaces:**
- **`AppRoot`:**
  - Thêm `ProgressStore Progress` và `internal static Func<ProgressStore> StoreFactory`, dùng để test chèn kho tạm.
  - Khởi động: chưa có hồ sơ thì hiện `ProfileScreen` (tạo hồ sơ). Có hồ sơ thì hiện `ProfileScreen` (chọn bé).
  - `ShowLessonList()` dùng `Progress.Current`.
- **`ProfileScreen`:**
  - Mỗi hồ sơ là một thẻ (hình đại diện và tên). Thêm một thẻ "+ Bé mới".
  - Màn tạo hồ sơ: ô nhập tên (`TMP_InputField`, giới hạn 20 ký tự), 6 hình đại diện, nút "Xong". Nút "Xong" chỉ bấm được khi tên không rỗng và đã chọn hình.
- **`LessonListScreen`:**
  - 17 thẻ xếp 6 cột. Thẻ bị khóa thì hiện mờ và không bấm được; bài đã học hiện "★★★" bằng `MarkerIcon` sao.
  - Có nút "Ôn lại", chỉ bật khi `Progress.Mistakes().Count > 0`.
  - Có nút "Phụ huynh", nằm ở góc và vẫn ≥ 160 đơn vị.
  - Có nút "Đổi bé".
- **Ghi kết quả:**
  - `LessonContext` thêm `Action<Round, int> RoundFinished`.
  - `RoundViewBase` gọi `RoundFinished(round, Feedback.Mistakes)` ngay trước khi báo `Completed`.
  - `LessonScreen` ghi vào kho: nhầm > 0 thì `RecordMistake(lesson_id, chỉ số lượt)` rồi `Save()` ngay, để bé thoát giữa bài vẫn không mất lượt nhầm.
  - `ResultScreen` gọi `MarkCompleted` rồi `Save()`. Nút "Học bài tiếp" đi tới bài kế tiếp vừa được mở.
- **`UiText`** thêm: `ReviewMistakes="Ôn lại"`, `Parent="Phụ huynh"`, `SwitchChild="Đổi bé"`, `NewChild="Bé mới"`, `Done="Xong"`, `NamePrompt="Tên ở nhà của bé"`. Chuyển các chữ còn viết cứng trong `App/` vào `UiText` (việc tồn).
- **Sao** (việc tồn): thiếu tranh `img_chung_sao` thì vẽ chữ "★" màu vàng, không vẽ ô vàng. Dùng chung cho `ResultScreen` và `LessonListScreen`.
- **`AppTestBase`** (lớp cơ sở cho test màn app):
  - SetUp: đặt `AppRoot.StoreFactory` trỏ tới file tạm. TearDown: xóa file tạm, trả `StoreFactory` về mặc định.
  - `IEnumerator LoadMain()`: kho trống, rồi nạp scene `Main`.
  - `IEnumerator LoadMainWithProfile(bool unlockAll = false)`: kho có sẵn một hồ sơ. `unlockAll` thì mọi bài đã `completed`.
  - `static string[] Ordered()`: mã bài theo `LessonRepository.LoadIndex()`.
  - `IEnumerator WalkAll(LessonScreen s)`: đi hết bài bằng `CompleteForTest`, lấy từ hàm `Walk` của `PrototypeEndToEndTests`.
  - `IEnumerator WalkWithOneMistake(LessonScreen s)`: như `WalkAll`, nhưng ở lượt Phần 2 đầu tiên chạm một phương án sai trước.
  - `static List<string> LabelsUnder(Component c)`: mọi chữ `TMP_Text` bên trong.

- [ ] **Step 1: Viết test** (kho tạm qua `StoreFactory`).

```csharp
[UnityTest] public IEnumerator FirstRun_CreatesProfile() { yield return LoadMain();
    var ps = Object.FindAnyObjectByType<ProfileScreen>(); Assert.IsNotNull(ps);
    ps.SimulateCreate("Bông", "img_chung_avatar_02"); yield return null;
    Assert.IsNotNull(Object.FindAnyObjectByType<LessonListScreen>()); Assert.AreEqual("Bông", AppRoot.Instance.Progress.Current.name); }
[UnityTest] public IEnumerator EmptyName_CannotCreate() { yield return LoadMain();
    var ps = Object.FindAnyObjectByType<ProfileScreen>(); ps.OpenCreate(); ps.SetName("   "); ps.PickAvatar("img_chung_avatar_01");
    Assert.IsFalse(ps.DoneButton.interactable); }
[UnityTest] public IEnumerator List_LocksAfterFirstIncomplete() { yield return LoadMainWithProfile();
    var list = Object.FindAnyObjectByType<LessonListScreen>();
    Assert.IsTrue(list.ButtonFor("tv1_t1_b01").interactable); Assert.IsFalse(list.ButtonFor("tv1_t1_b02").interactable);
    Assert.IsFalse(list.ReviewButton.interactable); }
[UnityTest] public IEnumerator FinishingLesson_UnlocksNextAndRecordsMistake() { yield return LoadMainWithProfile();
    AppRoot.Instance.Speech.WaitScale = .02f; AppRoot.Instance.ShowLesson("tv1_t1_b01"); yield return null;
    var screen = Object.FindAnyObjectByType<LessonScreen>();
    // làm sai một lần ở lượt đầu Phần 2, rồi đi hết bài
    yield return WalkWithOneMistake(screen);
    Assert.IsTrue(AppRoot.Instance.Progress.IsUnlocked(Ordered(), "tv1_t1_b02"));
    Assert.AreEqual(1, AppRoot.Instance.Progress.Mistakes().Count); }
```

  `SimulateCreate`, `OpenCreate`, `SetName`, `PickAvatar`, `DoneButton` (của `ProfileScreen`) và `ButtonFor(lessonId)`, `ReviewButton` (của `LessonListScreen`) là thành viên `internal`. Các hàm còn lại lấy từ `AppTestBase`.
- [ ] **Step 2: FAIL. Step 3: Cài đặt. Step 4: chạy toàn bộ PlayMode** (`AppFlowTests` và `PrototypeEndToEndTests` chuyển sang `AppTestBase`, dùng `LoadMainWithProfile(unlockAll: true)`). Phải PASS.
- [ ] **Step 5: Commit** `feat(unity): hồ sơ bé, danh sách bài có khóa và sao, ghi tiến độ (MVP Task 8)`.

## Task 9: Ôn lại

**Files:**
- Create `Runtime/App/ReviewSession.cs`
- Modify `App/AppRoot.cs`, `App/LessonListScreen.cs`, `App/LessonScreen.cs`, `App/ResultScreen.cs`
- Test `Tests/PlayMode/ReviewSessionTests.cs`

**Interfaces:**
- `static ReviewSession ReviewSession.Build(ProgressStore store, Func<string, Lesson> load)`:
  - Lấy tối đa 8 lượt từ `store.Mistakes()`, nạp lại lượt gốc bằng `lesson.part2[round]`.
  - Lượt không còn tồn tại (sai chỉ số hoặc bài không nạp được) thì `ClearMistake` và bỏ qua.
  - Trả về `Lesson Lesson`: `lesson_id` là `"on_lai"`, `title` "Ôn lại", `part1` rỗng, `part2` là các lượt. Trả kèm `List<(string lessonId, int round)> Sources`.
- `LessonScreen` khi đang ở phiên Ôn lại:
  - lượt có nhầm = 0 thì `ClearMistake` theo `Sources`;
  - lượt có nhầm > 0 thì `RecordMistake` (tăng `count`).
  - Mỗi lần ghi hoặc xóa lượt nhầm đều `Save()`.
  - Hết phiên thì về màn kết quả. Với `lesson_id` "on_lai", `ResultScreen` không gọi `MarkCompleted` và ẩn nút "Học bài tiếp".

- [ ] **Step 1: Viết test.**

```csharp
[UnityTest] public IEnumerator Review_PlaysMistakenRoundsAndClearsThem() {
    yield return LoadMainWithProfile(); var s = AppRoot.Instance.Progress;
    s.RecordMistake("tv1_t1_b13", 0); s.RecordMistake("tv1_t1_b04", 3);
    AppRoot.Instance.ShowReview(); yield return null; var screen = Object.FindAnyObjectByType<LessonScreen>();
    Assert.AreEqual(2, screen.Flow.TotalCount); yield return WalkAll(screen); Assert.AreEqual(0, s.Mistakes().Count); }
[UnityTest] public IEnumerator StaleMistake_IsDropped() {
    yield return LoadMainWithProfile(); var s = AppRoot.Instance.Progress;
    s.RecordMistake("tv1_t1_b13", 99); s.RecordMistake("tv1_t1_b99", 0); s.RecordMistake("tv1_t1_b13", 1);
    var r = ReviewSession.Build(s, LessonRepository.Load); Assert.AreEqual(1, r.Lesson.part2.Count); Assert.AreEqual(1, s.Mistakes().Count); }
```

  `ReviewSessionTests` kế thừa `AppTestBase` (Task 8).
- [ ] **Step 2: FAIL. Step 3: Cài đặt** (`AppRoot.ShowReview()`; nút "Ôn lại" gọi hàm này). **Step 4: PASS.**
- [ ] **Step 5: Commit** `feat(unity): ôn lại các lượt bé nhầm (MVP Task 9)`.

## Task 10: Màn phụ huynh có khóa

**Files:**
- Create `Runtime/App/ParentGate.cs`, `Runtime/App/ParentScreen.cs`
- Modify `App/AppRoot.cs` (`ShowParent`), `App/LessonListScreen.cs` (nút "Phụ huynh")
- Test `Tests/EditMode/ParentGateTests.cs`, `Tests/PlayMode/ParentScreenTests.cs`

**Interfaces:**
- **`ParentGate`** (C# thuần):
  - `ParentGate(System.Random rng)`.
  - `string Question`: dạng "a + b = ?", với a, b trong khoảng 11–49.
  - `IReadOnlyList<int> Choices`: 3 số, có đúng một đáp án đúng, thứ tự xáo.
  - `bool Answer(int value)`: đúng thì trả `true`; sai thì trả `false` và sinh câu hỏi mới.
- **`ParentScreen`:**
  - `AppRoot.ShowParent()` mở màn này; nút "Phụ huynh" ở danh sách bài gọi hàm đó. Trước hết màn hiện khóa phép tính với 3 nút đáp án. `internal void SimulateUnlock()` mở khóa trong test.
  - Mở khóa xong, mỗi hồ sơ có một khối gồm:
    - tên bé;
    - dòng "Đã học n/17 bài", với 17 là số bài trong `index.json`;
    - tối đa 5 "chữ hay nhầm", mỗi chữ là một thẻ riêng, xếp theo `count` giảm dần. Chữ lấy từ `options[answer].text` của lượt nhầm.
  - Có nút "Về".

- [ ] **Step 1: Viết test.**

```csharp
// EditMode
[Test] public void WrongAnswer_ChangesQuestion() { var g = new ParentGate(new System.Random(1)); var q = g.Question;
    var wrong = g.Choices.First(c => c != g.Expected); Assert.IsFalse(g.Answer(wrong)); Assert.AreNotEqual(q, g.Question); }
[Test] public void RightAnswer_Opens() { var g = new ParentGate(new System.Random(2)); Assert.IsTrue(g.Answer(g.Expected));
    Assert.AreEqual(1, g.Choices.Count(c => c == g.Expected)); }
// PlayMode
[UnityTest] public IEnumerator Parent_ShowsProgressAndConfusions() {
    yield return LoadMainWithProfile(); var s = AppRoot.Instance.Progress; s.MarkCompleted("tv1_t1_b01"); s.RecordMistake("tv1_t1_b13", 0);
    AppRoot.Instance.ShowParent(); yield return null; var p = Object.FindAnyObjectByType<ParentScreen>();
    p.SimulateUnlock(); yield return null;
    Assert.That(LabelsUnder(p), Has.Some.Contains("1/17")); Assert.That(LabelsUnder(p), Has.Member("u")); }   // lượt 0 bài 13: đáp án "u"
```

  `Expected` là thuộc tính `internal`. `ParentScreenTests` kế thừa `AppTestBase`.
- [ ] **Step 2: FAIL. Step 3: Cài đặt. Step 4: PASS.**
- [ ] **Step 5: Commit** `feat(unity): màn phụ huynh có khóa phép tính (MVP Task 10)`.

## Task 11: Chạy trọn 17 bài, bố cục, build cho chủ dự án thử

**Files:**
- Create `Tests/PlayMode/MvpEndToEndTests.cs`
- Modify `Tests/PlayMode/PrototypeEndToEndTests.cs`: chỉ giữ bài 42. Bài 4 và 13 đã có trong test mới, còn bài 42 không nằm trong danh sách bài nên chỉ test này chạy tới.

- [ ] **Step 1: Viết test.** Hai test chạy trên các bài lấy từ `LessonRepository.LoadIndex()`, tức 17 bài:
  - `AllLessons_EndToEnd`: kiểm tra giống bản mẫu.
  - `Layout_AllSteps_FitAndNoOverflow`: chạy ở 2400×1080 và 2048×1536, lưu ảnh chụp vào `TestOutput/screens/`.

  `MvpEndToEndTests` kế thừa `AppTestBase` và mở app bằng `LoadMainWithProfile(unlockAll: true)`. Cả hai test có `LogAssert.NoUnexpectedReceived()`.
- [ ] **Step 2: Chạy, xem ảnh lưới, sửa.**
  - Chạy `python run_unity_tests.py playmode --filter MvpEndToEndTests`.
  - Ghép ảnh chụp thành ảnh lưới và xem. Kiểm tra: dấu không bị xén, không có chữ đè nhau, thứ tự đọc đúng.
  - Sửa đến khi PASS.
- [ ] **Step 3: Chạy toàn bộ.** EditMode, PlayMode và Python đều phải PASS.
- [ ] **Step 4: Build và mở cho chủ dự án thử.**
  - `python run_unity_build.py`, rồi `--launch 1600x720` và `--launch 1440x1080`.
  - Chủ dự án thử: tạo hồ sơ, học bài 1–3, xem khóa bài, ôn lại, vào màn phụ huynh.
  - Sửa theo ý kiến chủ dự án, rồi chạy lại Step 3.
- [ ] **Step 5: Commit** `test(unity): chạy trọn 17 bài và kiểm tra bố cục (MVP Task 11)`.

## Task 12: Nghiệm thu bản đầu tiên, gom commit, push

**Files:** Modify `content/src/*.json` (`review.status`), `content/manifests/*.json` (qua trang duyệt), mục 15 của bản thiết kế.

- [ ] **Step 1: Chủ dự án duyệt âm thanh và tranh.**
  - Chạy `python -m tapdoc review` và gửi link cho chủ dự án.
  - Tranh không đạt thì tạo lại theo cách của Task 5.
  - Âm thanh `khong_dat` vẫn dùng tạm.
- [ ] **Step 2: Chủ dự án duyệt nội dung từng bài.**
  - Duyệt nội dung và các mục `can_duyet` (in ra bằng `build`).
  - Bài đã duyệt thì đặt `review.status = "da_duyet"`.
- [ ] **Step 3: Kiểm tra phát hành.** `python -m tapdoc validate --release` phải ra `OK`.
- [ ] **Step 4: Đối chiếu tiêu chí "Bản đầu tiên" ở mục 13:**

| Tiêu chí | Bằng chứng |
|---|---|
| Đạt mọi tiêu chí của bản mẫu cho 17 bài | `MvpEndToEndTests`, cùng lượt chủ dự án thử |
| Có trang nguồn và mức xác minh; mọi `can_duyet` đã xử lý | `validate --release` |
| Mọi âm thanh đã qua duyệt; không còn `chua_co` | `validate --release` |
| Tiến độ, sao và lượt nhầm lưu riêng từng bé; Ôn lại lấy đúng | `ProgressStoreTests`, `ReviewSessionTests` |
| Màn phụ huynh có khóa, hiện đúng tiến độ | `ParentGateTests`, `ParentScreenTests` |
| Không có ảnh scan trong project hay bản build | `validate` (`check_no_scans`), `git ls-files` |

- [ ] **Step 5: Gom commit và push.**
  - Ghi kết quả thử vào mục 15 của bản thiết kế.
  - Gom mọi commit sau `fc0c75d` thành **1 commit**: `git reset --soft fc0c75d`, rồi `git commit`.
  - `git fetch` rồi so `origin/main` với `fc0c75d`:
    - Nếu khớp: `git push origin main`.
    - Nếu khác: dừng lại và hỏi chủ dự án.
