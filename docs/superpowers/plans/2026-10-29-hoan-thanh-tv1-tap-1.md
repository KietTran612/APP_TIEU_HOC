# Hoàn thành TV1 Tập 1 (bài 18–80) — Kế hoạch triển khai

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Chủ dự án cho phép: tối đa 1 subagent chạy song song; giao việc code đơn giản cho Codex/Antigravity qua skill `delegate`. Claude luôn tự review diff và tự chạy test. Steps use checkbox (`- [ ]`) syntax for tracking.

**Mục tiêu:** app chạy đủ 80 bài của TV1 Tập 1. Làm thành 3 đợt; mỗi đợt kết thúc bằng bản build Windows cho chủ dự án thử và 1 commit trên `main`.

**Kiến trúc:**
- Xây tiếp trên bản đầu tiên (`f792778`); giữ nguyên hợp đồng dữ liệu, chỉ mở rộng.
- Thêm 5 loại bước Phần 1 (`letter_pairs`, `rule`, `rime_table`, `rime_grid`, cùng nhãn hàng cho `reading`) và ô bị chặn cho `combine_table`.
- Thêm 1 kiểu lượt Phần 2 (`match_case`). `listen_picture` có thêm lời đề riêng (dùng cho câu đố).
- Màn danh sách bài cuộn được 80 bài và chia phần.
- Nội dung chép từ trang sách theo từng lô; tranh và âm thanh tạo trong ChatGPT Kiet_1.

**Công nghệ:** như bản đầu tiên: Unity 6.6 (`6000.6.5f1`), uGUI và TMP, `JsonUtility`; Python 3.14 với thư viện chuẩn và `unittest`.

**Bản thiết kế:** [2026-10-28-app-tap-doc-mvp-design.md](../specs/2026-10-28-app-tap-doc-mvp-design.md), chủ yếu mục 16, cùng mục 5, 6 và 13. Kế hoạch trước: [2026-10-29-ban-dau-tien-bai-1-17.md](2026-10-29-ban-dau-tien-bai-1-17.md).

## Global Constraints

Mọi ràng buộc của hai kế hoạch trước vẫn giữ nguyên. Sau đây là các điểm mới hoặc đã đổi.

**Cách làm**
- Claude tự làm nội dung, tài nguyên, chẩn đoán lỗi và review.
- Việc code có phạm vi file rõ và có lệnh kiểm tra chạy được thì có thể giao Codex/Antigravity. Các task như vậy được đánh dấu "[có thể giao]". Claude đọc diff, chạy lại test, sửa hoặc bỏ phần sai, và ghi vào sổ.
- Không giao việc test, review hay việc dùng browser.
- Tối đa 1 subagent cùng lúc. Mỗi lúc chỉ một tiến trình dùng Unity (project bị khóa khi Unity mở).

**Git**
- Chỉ branch `main`, commit tạm từng task.
- Cuối mỗi đợt gom thành **1 commit** nằm trên commit phát hành trước, rồi push thường.
- Nếu `origin/main` khác với commit phát hành trước thì dừng lại và hỏi chủ dự án.

**Thử, build và tài nguyên**
- Thử trên máy tính, build Windows mở ở 1600×720 và 1440×1080. Không build Android khi chủ dự án chưa yêu cầu.
- Tài nguyên: chỉ dùng Edge trên máy này (kiểm tra `onThisComputer` và brand "Microsoft Edge"). Hỏi chủ dự án một lần cho mỗi lô tải.
- Mỗi lần gọi công cụ trình duyệt phải ngắn hơn 2 phút. Việc dài (vẽ hàng loạt tranh) chạy nền trong trang, rồi hỏi trạng thái theo từng đợt ngắn.

**Nội dung**
- Phần 1 khớp trang sách và đúng thứ tự (mục 2, "Coi là thất bại").
- Đánh vần đúng mục 5.1. Phương án nhiễu chỉ dùng chữ đã học. Các cặp giọng miền Nam không làm nhiễu của nhau trong bài nghe, kể cả khi phương án là phụ âm đứng riêng (s/x, d/gi/v, ch/tr).
- Đoạn đọc nhiều câu và bài thơ: mỗi câu hoặc dòng thơ là một bước `sentence` (mục 16).
- Ảnh scan không bao giờ vào repo hay bản build.
- Tên file ảnh scan không trùng số trang. Lấy theo cột `file_anh` của `docs/source-inventory/LESSON_INDEX.csv`. Ví dụ bài 79–80 nằm ở file `060_…_Trang_59.jpg`.
- Bài 60–61: ảnh 041 và 042 bị đảo thứ tự (ghi chú trong CSV).

## Review Focus

1. **Phương án là phụ âm đứng riêng ở bài nghe** (bài 18 v, 23 x, 24 s, 26 gi, 33 ch, 34 tr).
   - Hiện nay `southern_key("s") != southern_key("x")`, nên bộ kiểm tra không chặn lượt nghe có cả "s" lẫn "x".
   - Test: `test_validate.SouthernConsonantTest.test_lone_consonants_merge` (Task 1.1).
2. **Danh sách 80 bài.** Bài ở dưới cùng phải cuộn tới và bấm được; thẻ vẫn ≥ 160.
   - Test: `LessonListScrollTests.LastLesson_ReachableByScroll` (Task 1.5).
3. **Chạm vào ô bị chặn** (k + a, gh + o): không đọc, không báo lỗi, không tính là đã ghép.
   - Test: `NewStepViewTests2.CombineTable_BlockedCell_DoesNothing` (Task 1.5).
4. **Câu viết hoa, tên riêng, dấu câu** ("Mẹ", "Lan", "Cô ân cần đón bé."): mã âm thanh không đổi theo chữ hoa, tô màu phần vần mới vẫn đúng, kiểm tra "chữ đã học" không phân biệt hoa thường.
   - Test: `test_build_vowel_part.CapitalsTest` (Task 2.1).
5. **Câu đố: lời đề không được lộ đáp án.** Lời đề phát bài thơ, không phát "con lợn".
   - Test: `test_build_book_end.RiddleRoundTest.test_prompt_is_riddle_not_answer` (Task 3.1).

---

## Hợp đồng dữ liệu — phần mở rộng

**Item có thêm 1 trường:** `upper` (string), chữ hoa của cặp chữ.

**Step có thêm 1 trường:** `labels` (danh sách string), nhãn của từng hàng `reading` (rỗng nếu không có).

| Nguồn | Bản dựng |
|---|---|
| `{"type":"letter_pairs","letters":["a","ă",…,"y"]}` | `items`: `role:"pair"`, `text`=chữ thường, `upper`=chữ hoa (`str.upper()`), `audio`=`audio_for(chữ)` (chữ "q" ra mã có sẵn `am_q`, đọc "cu"; gắn `can_duyet` về tên đọc của q). Cột `col` 0–3 và hàng `row` theo thứ tự đọc của bảng 4 cột trong sách. |
| `{"type":"rule","lines":["k chỉ ghép với e, ê, i", …]}` | `items`: `role:"line"`, `text`=dòng, `audio`=`cau_bNN_kk` (cùng bộ đếm với câu). |
| `reading` nhận thêm hàng dạng `{"label":"a – a","items":["ra rả","khà khà"]}` | như cũ, thêm `labels` (hàng không có nhãn thì là `""`) |
| `combine_table`: mỗi hàng có thể thêm `"blocked":["a","o",…]` | thêm item `role:"blocked"` (`row`, `col`, `text` rỗng). Báo `BuildError` nếu nguyên âm vừa có ô vừa bị chặn. Nguyên âm chỉ có ở `blocked` vẫn có cột. |
| `{"type":"rime_table","rows":[{"rime":"an","word":"nhà sàn"},…]}` | Mỗi hàng 2 item. `role:"rime"` (`row`, `text`, `audio` `van_*`, `spells`=[`spell_rime`]). `role:"word"` (`row`, `text`, `audio`=`text_audio`, `spells` mỗi tiếng). Báo `BuildError` nếu `spell_rime` của vần không ra đúng 2 mảnh trước mảnh ghép (nguyên âm + âm cuối). |
| `{"type":"rime_grid","finals":["n","m","c","t","p","i-y","o-u"],"rows":[{"vowel":"a","cells":["an","am","ac","at","ap","ai - ay","ao - au"]},…]}` | Item `role:"final"` (`col`), `role:"vowel"` (`row`), `role:"cell"` (`row`, `col`, `text`, `spells` mỗi vần trong ô, tách theo " - "). Ô rỗng `""` không sinh item. |
| Lượt `{"kind":"match_case","rounds":[{"model":"a","answer":"A","options":["A","Ă","Â"]}]}` | `prompt_text`=model, `options` (`text`), `answer`; `instruction_audio`=`hd_nhin_chon_chu_hoa`. Không có `prompt_audio`. |
| `listen_picture` có thêm `"prompt":"Con gì ăn no…"` | `prompt_audio`=`cau_bNN_kk`, lời đọc là `prompt`. Vẫn kiểm tra `word` khớp chữ của tranh đáp án. |

**Âm thanh hệ thống mới:** `hd_nhin_chon_chu_hoa` = "Con nhìn chữ thường rồi chọn chữ hoa đúng nhé.", `hd_nghe_do_chon_tranh` = "Con nghe câu đố rồi chọn tranh đúng nhé." (dùng làm `instruction_audio` của `listen_picture` khi có `prompt`).

## Cấu trúc file (phần thêm)

```
tools/tapdoc/build.py, validate.py, system_assets.py
tools/tests/test_build_letter_part.py, test_build_vowel_part.py, test_build_book_end.py, test_book_content.py
content/src/tv1_t1_b18.json … b80.json
unity/TapDoc/Assets/Scripts/Runtime/
  Steps/LetterPairsView.cs, RuleView.cs, RimeTableView.cs, RimeGridView.cs
  Exercises/MatchCaseView.cs
  (sửa) Data/LessonData.cs, Steps/CombineTableView.cs, Steps/ItemsView.cs, Steps/StepViewRegistry.cs,
        App/LessonListScreen.cs
unity/TapDoc/Assets/Tests/PlayMode/NewStepViewTests2.cs, LessonListScrollTests.cs
```

## Khuôn chung cho mọi task nội dung (1.2–1.4, 2.2–2.4, 3.2–3.3)

**Cách làm một bài:**
1. Mở ảnh scan theo `file_anh`, chép Phần 1 đúng thứ tự trang theo khuôn của các bài đã làm:
   - **Âm mới:** `unit` → `keyword` → `analyze` → `spell`, lặp cho từng âm; rồi tranh không chữ (`picture` có `say` và `word`), từ ứng dụng `words`, câu `sentence`, đọc thêm `reading`.
   - **Vần mới:** với từng vần: `unit` (vần) → `keyword` → `analyze` → `spell` (`rime: true`) → `spell` tiếng (`then` là từ khoá); rồi `words` (●), tranh cảnh (`picture`), câu hoặc thơ (`sentence`, mỗi câu một bước).
   - **Ôn tập:** `letter_grid` / `combine_table` / `reading` có nhãn / `tone_table` / `rule` / `rime_table` / `rime_grid`, theo đúng trang.
2. Mã tranh `img_bNN_<telex>`. Mô tả tranh viết lại từ tranh gốc, không có khung viền, không có chữ.
3. **Phần 2: 6–10 lượt.**
   - Âm mới: nghe chọn chữ ×2, phân biệt chữ dễ nhầm ×3, ghép tiếng ×1, nghe chọn tranh ×2.
   - Vần mới: thay chữ bằng vần; ghép tiếng thì kéo vần hoặc dấu vào chỗ trống.
   - Ôn tập: trộn các kiểu, ưu tiên phân biệt chữ dễ nhầm và nhìn chữ kéo dấu.
   - Nếu `validate` báo phương án chưa học hoặc cặp giọng miền Nam thì đổi phương án, không tắt kiểm tra.
4. `source.verification = "page_verified"`, `review.status = "chua_duyet"`. Mọi điều chưa chắc ghi vào `review.notes`.
5. Mỗi task nội dung thêm một lớp test trong `tools/tests/test_book_content.py`:
   - **Kiểm tra chung** `assert_lesson_basics(lid)`: dựng được, `page_verified`, Phần 2 có 6–10 lượt, mọi `spell` không rỗng.
   - **Mỗi bài có ít nhất 1 điểm đối chiếu với trang sách,** viết lúc chép, ví dụ "từ khoá là …", "đọc thêm có N mục".
   - Các điểm đã biết ghi sẵn trong từng task.
6. Lệnh kiểm tra: `python -m tapdoc build`, rồi `python -m tapdoc validate --allow-missing` phải ra `OK`, và `python -m unittest discover -s tests -t .` phải PASS.

---

# Đợt 1 — bài 18–41 (Chữ cái và âm)

## Task 1.1: Công cụ cho đợt 1

**Files:**
- Modify: `tools/tapdoc/validate.py` (`_southern_token`), `tools/tapdoc/build.py`, `tools/tapdoc/system_assets.py`
- Test: `tools/tests/test_build_letter_part.py`, thêm vào `tools/tests/test_validate.py`

**Interfaces:**
- Produces: phần mở rộng hợp đồng cho `letter_pairs`, `rule`, nhãn của `reading`, `blocked` của `combine_table`, `match_case`, cùng mã `hd_nhin_chon_chu_hoa`.
- `southern_key` gộp được phụ âm đứng riêng.

- [ ] **Step 1: Viết test.**

```python
# test_validate.py
class SouthernConsonantTest(unittest.TestCase):
    def test_lone_consonants_merge(self):
        self.assertEqual(southern_key("s"), southern_key("x"))
        self.assertEqual(southern_key("d"), southern_key("gi")); self.assertEqual(southern_key("v"), southern_key("d"))
        self.assertEqual(southern_key("tr"), southern_key("ch"))
        self.assertNotEqual(southern_key("s"), southern_key("t"))
    def test_listen_round_with_s_and_x_is_rejected(self): ...  # lượt listen_choose {"answer":"s","options":["s","x"]} ở bài 24 → có Issue nhắc "giọng miền Nam"
# test_build_letter_part.py
def test_letter_pairs(self):
    st = build_lesson(mini(part1=[{"type": "letter_pairs", "letters": ["a", "đ", "q"]}])).lesson["part1"][0]
    self.assertEqual([(i["text"], i["upper"], i["audio"]) for i in st["items"]], [("a", "A", "van_a"), ("đ", "Đ", "am_dd"), ("q", "Q", "am_q")])
    self.assertTrue(any("'q'" in n["note"] for n in build_lesson(...).lesson["review"]["can_duyet"]))
def test_rule_lines_get_sentence_audio(self):
    st = ...{"type": "rule", "lines": ["k chỉ ghép với e, ê, i", "gh chỉ ghép với e, ê, i"]}...
    self.assertEqual([i["audio"] for i in st["items"]], ["cau_b99_01", "cau_b99_02"])
def test_reading_labels(self):
    st = ...{"type": "reading", "rows": [{"label": "a – a", "items": ["ra rả", "khà khà"]}, ["lò dò"]]}...
    self.assertEqual(st["labels"], ["a – a", ""]); self.assertEqual([i["row"] for i in st["items"]], [0, 0, 1])
def test_combine_blocked(self):
    st = ...{"type": "combine_table", "rows": [{"onset": "k", "cells": {"e": ["ke"]}, "blocked": ["a", "o"]}]}...
    self.assertIn(("blocked", 0, 1), [(i["role"], i["row"], i["col"]) for i in st["items"]])   # cột theo thứ tự gặp: e, a, o
def test_combine_blocked_conflict(self):  # nguyên âm vừa có ô vừa bị chặn → BuildError
def test_match_case_round(self):
    rd = ...{"kind": "match_case", "rounds": [{"model": "a", "answer": "A", "options": ["Ă", "A", "Â"]}]}...
    self.assertEqual((rd["prompt_text"], rd["answer"], rd["instruction_audio"]), ("a", 1, "hd_nhin_chon_chu_hoa"))
```

- [ ] **Step 2:** Chạy `python -m unittest tests.test_build_letter_part tests.test_validate`. Phải FAIL.
- [ ] **Step 3: Cài đặt.**
  - `_southern_token`: phụ âm đứng riêng cũng đổi qua `_SOUTHERN_ONSET` (x→s, v→d, gi→d, tr→ch).
  - Các loại bước và lượt theo bảng hợp đồng ở trên.
  - Thêm `hd_nhin_chon_chu_hoa` và `hd_nghe_do_chon_tranh` vào `SYSTEM_AUDIO`, kèm `INSTRUCTION_AUDIO["match_case"]`.
  - `validate`:
    - `match_case` không có đề bằng âm thanh, nên không áp dụng luật giọng miền Nam;
    - phương án chữ hoa coi là đã học nếu chữ thường đã học.
- [ ] **Step 4:** Chạy toàn bộ test Python, `build`, rồi `validate`. Phải PASS và `OK`.
- [ ] **Step 5: Commit** `feat(tools): cặp chữ hoa, luật chính tả, nhãn hàng, ô bị chặn, match_case, giọng miền Nam cho phụ âm (Đợt 1 Task 1)`.

## Task 1.2: Nội dung bài 18–27

**Files:** Create `content/src/tv1_t1_b18.json` … `b27`; Test `tools/tests/test_book_content.py` (lớp `Lessons18To27Test`)

**Ảnh scan:** 012–017 (bài 18: tr.23 … bài 27: tr.32). Có 2 bài ôn tập: 22 và 27.

**Điểm đối chiếu đã biết:**
- bài 18 "v", từ khoá "tò vò", đọc thêm 2 hàng, hàng đầu có 9 mục;
- bài 20 có 2 âm: k, kh;
- bài 25 có 2 âm: g, gh;
- bài 26 "gi": đánh vần dùng tên tạm "di", gắn `can_duyet`.

- [ ] **Step 1:** Viết lớp test với các điểm trên và `assert_lesson_basics` cho 10 bài. Chạy, phải FAIL.
- [ ] **Step 2:** Chép 10 bài theo khuôn chung. Chạy `build`, rồi `validate --allow-missing`, phải ra `OK`.
- [ ] **Step 3:** Chạy toàn bộ test Python. Phải PASS.
- [ ] **Step 4: Commit** `feat(content): bài 18–27 (Đợt 1 Task 2)`.

## Task 1.3: Nội dung bài 28–36

**Files:** `b28` … `b36`; lớp test `Lessons28To36Test`

**Ảnh scan:** 017–021. Có 1 bài ôn tập: 32.

**Điểm đối chiếu đã biết:**
- bài 29 "ngh" và bài 35 "q qu": tên đọc tạm "ngờ kép", "quờ", gắn `can_duyet`;
- bài 33 "ch" và bài 34 "tr": không có lượt nghe nào đặt ch cạnh tr (Review Focus 1).

- [ ] **Step 1–4:** như Task 1.2. Commit `feat(content): bài 28–36 (Đợt 1 Task 3)`.

## Task 1.4: Nội dung bài 37–41

**Files:** `b37` … `b41`; lớp test `Lessons37To41Test`

**Ảnh scan:** 022–024. Trang đã xem ngày 29/10/2026.

**Điểm đối chiếu đã biết:**
- **Bài 37:** khung chữ `ch tr qu p ph`; bảng ghép 5 hàng. Hàng qu chỉ có `a ơ e ê i y`.
- **Bài 38:**
  - khung chữ có 10 nguyên âm `a o ô ơ e ê i y u ư`;
  - `reading` 12 hàng có nhãn, từ "a – a: ra rả, khà khà" đến "u – i: xù xì, rủ rỉ rù rì".
- **Bài 39:**
  - khung chữ 17 phụ âm `b c d đ g h k l m n p q r s t v x`;
  - bảng ghép b/c/k/d × 9 nguyên âm. c bị chặn ở e ê i; k bị chặn ở a o ô ơ u ư;
  - 3 bước `tone_table`: ba, ca, ke.
- **Bài 40:**
  - khung chữ `ch th nh kh gh ng ngh tr gi ph qu`;
  - bảng ghép ch/gh/ng/ngh, có ô bị chặn;
  - 2 bước `tone_table`: cha, ghe;
  - `rule` 3 dòng: "k chỉ ghép với e, ê, i"; "gh chỉ ghép với e, ê, i"; "ngh chỉ ghép với e, ê, i".
- **Bài 41:** `letter_pairs` 29 chữ, đúng thứ tự bảng; Phần 2 có `match_case` và nghe chọn chữ (chữ hoa).

- [ ] **Step 1–4:** như Task 1.2. Commit `feat(content): bài 37–41 (Đợt 1 Task 4)`.

## Task 1.5: Màn mới đợt 1 và danh sách bài cuộn  [có thể giao: Codex cho `LessonListScreen`, Claude review]

**Files:**
- Create `Steps/LetterPairsView.cs`, `Steps/RuleView.cs`, `Exercises/MatchCaseView.cs`
- Modify `Data/LessonData.cs` (`Item.upper`, `Step.labels`), `Steps/CombineTableView.cs`, `Steps/ItemsView.cs`, `Steps/StepViewRegistry.cs`, `App/LessonListScreen.cs`
- Test `Tests/PlayMode/NewStepViewTests2.cs`, `Tests/PlayMode/LessonListScrollTests.cs`

**Interfaces:**

| Màn | Hành vi | Báo `Completed` khi |
|---|---|---|
| `LetterPairsView` | Lưới 4 cột như sách. Mỗi thẻ có chữ thường và chữ hoa, cao ≥ 160, tự xuống trang nếu không vừa (2 trang, có nút "Trang sau"). Chạm thẻ thì đọc âm. | Bé đã chạm mọi thẻ |
| `RuleView` | Mỗi dòng một thẻ rộng. Chạm thì đọc dòng. | Bé đã chạm mọi dòng |
| `MatchCaseView` (`RoundViewBase`) | Chữ thường to ở trên, 3 thẻ chữ hoa ở dưới. Chạm để chọn. Phản hồi như các lượt khác. | (theo `RoundViewBase`) |

- `CombineTableView`: ô `blocked` vẽ gạch chéo, không bấm được. Ghép một âm đầu với nguyên âm bị chặn thì không đọc và không tính là đã ghép.
- `ItemsView`: hàng có nhãn thì hiện nhãn ở đầu hàng (thẻ không bấm được, nằm trên cùng dòng).
- `LessonListScreen`:
  - thẻ bài nằm trong `ScrollRect` dọc, 6 cột;
  - có 2 tiêu đề phần: "Chữ cái và âm" (bài 1–41) và "Vần" (bài 42–80). Thêm `UiText.PartLetters`, `UiText.PartRimes`;
  - `internal void ScrollTo(string lessonId)`.

- [ ] **Step 1: Viết test.**

```csharp
[UnityTest] public IEnumerator LetterPairs_AllTapped() { var v = Bind("tv1_t1_b41", 0); yield return ((ITestCompletable)v).CompleteForTest(); Assert.IsTrue(Done(v));
    Assert.That(Labels(v), Has.Some.Contains("Ă")); }
[UnityTest] public IEnumerator Rule_ReadsEachLine() { var v = Bind("tv1_t1_b40", RuleIndex("tv1_t1_b40")); TileWithText(v, "k chỉ ghép với e, ê, i").SimulateTap();
    yield return new WaitForSeconds(.3f); Assert.That(Ctx.Speech.History.Last(), Does.StartWith("cau_b40_")); Assert.IsFalse(Done(v)); }
[UnityTest] public IEnumerator CombineTable_BlockedCell_DoesNothing() {   // Review Focus 3
    var v = Bind("tv1_t1_b39", 1); var before = Ctx.Speech.History.Count;
    TileWithText(v, "k").SimulateTap(); TileWithText(v, "a").SimulateTap(); yield return new WaitForSeconds(.3f);
    Assert.That(Labels(v), Has.No.Member("ka")); Assert.IsFalse(Done(v)); }
[UnityTest] public IEnumerator MatchCase_RightUpperCompletes() { var r = BindRound("tv1_t1_b41", MatchIndex("tv1_t1_b41")); yield return ((ITestCompletable)r).CompleteForTest(); Assert.IsTrue(Done(r)); }
[UnityTest] public IEnumerator Reading_LabelsShown() { var v = Bind("tv1_t1_b38", 1); yield return null; Assert.That(Labels(v), Has.Member("a – a")); }
// LessonListScrollTests (AppTestBase)
[UnityTest] public IEnumerator LastLesson_ReachableByScroll() {   // Review Focus 2
    yield return LoadMainWithProfile(unlockAll: true); var list = Object.FindAnyObjectByType<LessonListScreen>();
    var last = Ordered().Last(); list.ScrollTo(last); yield return null;
    Assert.IsTrue(IsOnScreen(list.ButtonFor(last))); LayoutProbe.AssertFits(AppRoot.Instance.Canvas); }
```

  Các hàm `RuleIndex`, `MatchIndex` và `IsOnScreen` là hàm hỗ trợ trong test.
  - `RuleIndex(lid)` trả chỉ số bước `rule` đầu tiên của bài.
  - `MatchIndex(lid)` trả chỉ số lượt `match_case` đầu tiên của bài.
  - `IsOnScreen(button)`: 4 góc của thẻ nằm trong vùng hiện của ScrollRect.
- [ ] **Step 2: Chạy test.** `python tools/run_unity_tests.py playmode --filter "NewStepViewTests2;LessonListScrollTests"` phải FAIL.
- [ ] **Step 3: Cài đặt** theo bảng trên. Đăng ký `letter_pairs`, `rule` và `match_case`.
- [ ] **Step 4: Chạy toàn bộ EditMode và PlayMode.** Phải PASS.
- [ ] **Step 5: Commit** `feat(unity): cặp chữ hoa, luật chính tả, chọn chữ hoa, ô bị chặn, nhãn hàng, danh sách bài cuộn (Đợt 1 Task 5)`.

## Task 1.6: Tài nguyên đợt 1 (Claude làm trong Edge)

Làm như Task 5 của kế hoạch trước:
- `requests`, rồi gửi lô âm thanh theo giọng `vi-sgn+f3`, ghi rõ cấu hình trong lời nhắc;
- vẽ tranh bằng job chạy nền trong trang;
- ghép ảnh lưới để kiểm tra tranh đúng mã;
- xin phép tải một lần, rồi `import-audio` và `import-image`.

Ước lượng: khoảng 45 tranh và 300 âm thanh.

- [ ] **Step 1:** `build`, rồi `requests`. Ghi lại số mã `chua_co`.
- [ ] **Step 2:** Tạo âm thanh, tải về, nhập.
- [ ] **Step 3:** Vẽ tranh, kiểm tra trên ảnh lưới, tải về, nhập.
- [ ] **Step 4:** `validate` (không `--allow-missing`) phải ra `OK`. EditMode `DataTests.AllReferencedAssetsExist` phải PASS.
- [ ] **Step 5: Commit** `feat(content): âm thanh và tranh bài 18–41 (Đợt 1 Task 6)`.

## Task 1.7: Chạy trọn, xem bố cục, build cho chủ dự án thử

- [ ] **Step 1:** Chạy `MvpEndToEndTests` (đã lấy bài từ `index.json`, nay là 41 bài) và `GlyphInAppTests`. Phải PASS.
- [ ] **Step 2: Xem ảnh lưới** ở 2048×1536 của các bài 37–41. Kiểm tra:
  - thẻ không tràn;
  - dấu không bị xén;
  - ô gạch chéo rõ;
  - bảng 29 cặp chữ đọc được.
- [ ] **Step 3:** Build, mở ở 1600×720 và 1440×1080. Chủ dự án thử bài 18–41 và sửa theo ý kiến chủ dự án.
- [ ] **Step 4: Commit** `test(unity): chạy trọn bài 1–41 (Đợt 1 Task 7)`.

## Task 1.8: Phát hành đợt 1

- [ ] **Step 1:** Chủ dự án duyệt tài nguyên và các mục `can_duyet` của đợt. Bài đã duyệt chuyển `da_duyet`.
- [ ] **Step 2:** Ghi kết quả vào mục 15 của bản thiết kế.
- [ ] **Step 3:** Gom các commit của đợt thành 1 commit trên `f792778`, `git fetch`, so `origin/main`, rồi push.
  - Nếu chủ dự án chưa duyệt xong, vẫn push như bản đầu tiên. Kết quả duyệt vào commit sau.

---

# Đợt 2 — bài 42–64 (vần có âm cuối n, m, i/y, o/u)

## Task 2.1: Công cụ cho đợt 2

**Files:** Modify `tools/tapdoc/build.py`; Test `tools/tests/test_build_vowel_part.py`

**Interfaces:** Produces `rime_table` (theo bảng hợp đồng).

- [ ] **Step 1: Viết test.**

```python
class RimeTableTest(unittest.TestCase):
    def test_rows(self):
        st = ...{"type": "rime_table", "rows": [{"rime": "an", "word": "nhà sàn"}, {"rime": "ăn", "word": "củ sắn"}]}...
        self.assertEqual([(i["role"], i["row"], i["text"]) for i in st["items"]],
                         [("rime", 0, "an"), ("word", 0, "nhà sàn"), ("rime", 1, "ăn"), ("word", 1, "củ sắn")])
        self.assertEqual([p["audio"] for p in st["items"][0]["spells"][0]["parts"]], ["van_a", "am_n", "van_an"])
class AllRimesTest(unittest.TestCase):   # chốt cách đánh vần mọi vần của tập 1 (danh sách vần lấy từ LESSON_INDEX bài 42–78)
    def test_every_rime_spells_vowel_final_join(self): ...   # mỗi vần: 3 mảnh, mảnh cuối là join đúng vần; "ay" đọc "a – i dài – ay" (can_duyet)
class CapitalsTest(unittest.TestCase):   # Review Focus 4
    def test_sentence_with_capitals_and_names(self):
        st = ...{"type": "sentence", "text": "Lan cho ngan ăn giun, bà khen Lan."}...  new_units ["an", "en", "un"]
        self.assertEqual(st["items"][0]["audio"], "tieng_lan"); self.assertTrue(st["items"][0]["hl"])   # "Lan" vẫn tô vần an
    def test_capitals_count_as_learned(self): ...   # validate: phương án "Lan" ở bài 48 coi là đã học
```

- [ ] **Step 2:** Chạy test, phải FAIL. **Step 3:** Cài đặt. **Step 4:** Chạy toàn bộ, phải PASS.
- [ ] **Step 5: Commit** `feat(tools): bảng ôn vần, chốt đánh vần mọi vần tập 1, chữ hoa trong câu (Đợt 2 Task 1)`.

## Task 2.2: Nội dung bài 42–47

**Ảnh scan:** 024–028.

- **Bài 42:**
  - bỏ `"in_app": false`;
  - đối chiếu lại với tr.47: tranh lan can, đàn ngan, bàn ghế vẫn là tranh vẽ thêm, giữ `can_duyet`;
  - nếu chủ dự án đã duyệt thì giữ theo kết quả duyệt.
- **Bài 45** (tr.50–51, đã xem):
  - 3 vần on, ôn, ơn; từ khoá "quả bồ hòn", "con chồn", "cá thờn bơn";
  - từ ● theo từng vần;
  - tranh cảnh nhà trẻ;
  - 3 bước `sentence`: "Mẹ bế bé đi nhà trẻ.", "Cô ân cần đón bé.", "Cô hôn bé."

- [ ] **Step 1–4:** như Task 1.2. Test thêm: `index.json` có bài 42, và đọc thêm của bài 45 là 3 bước `sentence` liên tiếp. Commit `feat(content): bài 42–47 (Đợt 2 Task 2)`.

## Task 2.3: Nội dung bài 48–54

**Ảnh scan:** 029–035.

**Bài 48** (tr.56–57, đã xem):
- `rime_table` 10 hàng: an–nhà sàn, ăn–củ sắn, ân–quả cân, on–cỏ non, ôn–con chồn, ơn–đàn lợn, en–mũ len, ên–ngọn nến, in–bản tin, un–con giun;
- tranh cảnh;
- 1 câu: "Lan cho ngan ăn giun, bà khen Lan."

- [ ] **Step 1–4:** như Task 1.2. Commit `feat(content): bài 48–54 (Đợt 2 Task 3)`.

## Task 2.4: Nội dung bài 55–64

**Ảnh scan:** 036–045.
- Bài 60 nằm ở ảnh 042, bài 61 ở ảnh 041: hai ảnh bị đảo thứ tự. Tr.82–83 lấy từ bản scan khác; xem ghi chú trong CSV.
- Các vần ai, ay, ây, oi, ôi, ơi, ui, ưi, iu đọc "i ngắn/i dài" tạm. Bản dựng tự gắn `can_duyet`.

- [ ] **Step 1–4:** như Task 1.2. Commit `feat(content): bài 55–64 (Đợt 2 Task 4)`.

## Task 2.5: Màn bảng ôn vần  [có thể giao: Codex, Claude review]

**Files:** Create `Steps/RimeTableView.cs`; Modify `Steps/StepViewRegistry.cs`; Test `Tests/PlayMode/NewStepViewTests2.cs`

**Interfaces:**
- `RimeTableView` hiện từng hàng gồm: [vần] [nguyên âm → âm cuối] [từ ví dụ]. Chạm hàng thì đánh vần vần rồi đọc từ.
- Có 10 hàng, nên xếp 2 cột × 5 hàng, mỗi hàng cao 120, thẻ chạm ≥ 160 theo chiều ngang.
- Báo `Completed` khi bé đã chạm mọi hàng.

- [ ] **Step 1: Test.**
  - `RimeTable_RowSpellsThenReadsWord`: ở bài 48, chạm hàng "an" thì `History` có lần lượt `van_a, am_n, van_an, tu_nhaf_sanf`.
  - `RimeTable_AllRowsTapped`: `CompleteForTest`, rồi `Done`.
  - Thêm một test bố cục ở 2048×1536 bằng `LayoutProbe` trong `MvpEndToEndTests` (đã có sẵn).
- [ ] **Step 2–4:** FAIL, rồi cài đặt, rồi PASS toàn bộ. **Step 5: Commit** `feat(unity): bảng ôn vần (Đợt 2 Task 5)`.

## Task 2.6–2.8: Tài nguyên, chạy trọn và build, phát hành đợt 2

Làm như Task 1.6–1.8 cho bài 42–64. Ước lượng khoảng 110 tranh (3 từ khoá và 1 tranh cảnh mỗi bài) và 450 âm thanh. Commit phát hành nằm trên commit phát hành đợt 1.

---

# Đợt 3 — bài 65–80 (vần có âm cuối c, t, p; ôn tập cuối học kì)

## Task 3.1: Công cụ cho đợt 3

**Files:** Modify `tools/tapdoc/build.py`, `tools/tapdoc/validate.py`; Test `tools/tests/test_build_book_end.py`

**Interfaces:** Produces `rime_grid` và `listen_picture.prompt` (theo bảng hợp đồng).

- [ ] **Step 1: Viết test.**

```python
class RimeGridTest(unittest.TestCase):
    def test_grid(self):
        st = ...{"type": "rime_grid", "finals": ["n", "i-y"], "rows": [{"vowel": "a", "cells": ["an", "ai - ay"]}, {"vowel": "ư", "cells": ["", "ưi"]}]}...
        cells = [(i["row"], i["col"], i["text"], len(i["spells"])) for i in st["items"] if i["role"] == "cell"]
        self.assertEqual(cells, [(0, 0, "an", 1), (0, 1, "ai - ay", 2), (1, 1, "ưi", 1)])
class RiddleRoundTest(unittest.TestCase):   # Review Focus 5
    def test_prompt_is_riddle_not_answer(self):
        rd = ...{"kind": "listen_picture", "word": "con lợn", "prompt": "Con gì ăn no, má to mắt híp, mồm kêu ụt ịt, nằm thở phì phò?", "answer": "img_b80_con_lownj", "options": [...]}...
        self.assertTrue(rd["prompt_audio"].startswith("cau_b80_")); self.assertNotEqual(rd["prompt_audio"], "tu_con_lownj")
        self.assertEqual(rd["instruction_audio"], "hd_nghe_do_chon_tranh")
```

- [ ] **Step 2–4:** FAIL, rồi cài đặt, rồi PASS. **Step 5: Commit** `feat(tools): bảng nhóm vần, lượt câu đố (Đợt 3 Task 1)`.

## Task 3.2: Nội dung bài 65–73

**Ảnh scan:** 046–054.
- **Bài 65** (tr.90–91, đã xem):
  - 3 vần ac, ăc, âc; từ khoá "củ lạc", "con tắc kè", "quả gấc";
  - thơ 2 dòng: "Mặc gió núi đèo cao" / "Quân đi như thác chảy."
- **Luật giọng miền Nam** t/c và n/ng đã có. Lượt nghe không đặt ac cạnh at.

- [ ] **Step 1–4:** như Task 1.2. Commit `feat(content): bài 65–73 (Đợt 3 Task 2)`.

## Task 3.3: Nội dung bài 74–80

**Ảnh scan:** 055–060. Bài 79–80 nằm ở file `060_…_Trang_59.jpg`.
- **Bài 79:** `rime_grid`: 11 hàng nguyên âm (a ă â o ô ơ e ê i u ư) × 7 cột (n m c t p i-y o-u). Ô trống đúng như trang.
- **Bài 80** (tr.119, đã xem):
  - "Tìm tiếng có vần đã học (theo mẫu)": `reading` 7 hàng có nhãn (1)…(7), mỗi hàng là các từ trong một cột của trang;
  - "Đố em": 4 bước `sentence`, một bước một dòng thơ;
  - Phần 2 có lượt `listen_picture` kèm `prompt` là cả bài thơ, đáp án "con lợn". Tranh con lợn và 2 tranh nhiễu là vẽ thêm, gắn `can_duyet`.

- [ ] **Step 1–4:** như Task 1.2. Commit `feat(content): bài 74–80 (Đợt 3 Task 3)`.

## Task 3.4: Màn bảng nhóm vần  [có thể giao: Codex, Claude review]

**Files:** Create `Steps/RimeGridView.cs`; Modify `Steps/StepViewRegistry.cs`; Test `Tests/PlayMode/NewStepViewTests2.cs`

**Interfaces:**
- `RimeGridView` có 12 hàng (tiêu đề và 11 hàng nguyên âm) × 8 cột. Bảng này không vừa Stage nếu thẻ cao 160.
- Màn chia 2 trang: hàng a–ơ và hàng e–ư, có nút "Trang sau" và "Trang trước". Ô cao 110 nhưng vùng chạm của mỗi ô ≥ 160 nhờ `LayoutElement`, trong khi khoảng cách giữa các ô vẫn đủ.
  - **[Đề xuất thay thế]** nếu LayoutProbe không cho vùng chạm chồng nhau: chia 3 trang với ô cao 160. Claude chọn khi làm và ghi vào sổ.
- Chạm ô thì đánh vần (ô "ai - ay" đánh vần cả hai vần). Báo `Completed` khi bé đã chạm ít nhất một ô ở mỗi trang.

- [ ] **Step 1: Test.**
  - `RimeGrid_TapCellSpells`: chạm "ac" thì `History` có `van_a, am_c, van_ac`.
  - `RimeGrid_PagesAndComplete`: chạm ở cả các trang, rồi `Done`.
  - `LayoutProbe` ở 2048×1536.
- [ ] **Step 2–5:** như Task 2.5. Commit `feat(unity): bảng nhóm vần (Đợt 3 Task 4)`.

## Task 3.5–3.7: Tài nguyên, chạy trọn và build, phát hành đợt 3 và nghiệm thu cả quyển

Làm như Task 1.6–1.8 cho bài 65–80. Ước lượng khoảng 75 tranh và 350 âm thanh.

Nghiệm thu cả quyển:
- `MvpEndToEndTests` chạy trọn 80 bài ở 2 khung hình;
- `validate --release` ra `OK` sau khi chủ dự án duyệt hết;
- bảng tiêu chí mục 13 (bản mẫu và bản đầu tiên) đúng cho cả 80 bài;
- ghi kết quả vào mục 15 và 16 của bản thiết kế, gom 1 commit, push.
