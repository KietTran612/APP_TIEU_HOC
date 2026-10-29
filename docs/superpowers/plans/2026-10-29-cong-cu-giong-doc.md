# Giọng đọc edge-tts và công cụ chỉnh âm thanh — Kế hoạch triển khai

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Chủ dự án cho phép giao việc code có phạm vi rõ cho Codex/Antigravity (theo dõi định kỳ bằng `watch-workers.sh`); Claude luôn tự review diff và tự chạy test. Steps use checkbox (`- [ ]`) syntax for tracking.

**Mục tiêu:** tạo lại toàn bộ âm thanh bằng edge-tts giọng HoaiMy, kèm một công cụ trên máy để chủ dự án nghe, chỉnh và duyệt từng mã.

**Kiến trúc:**
- **Cấu hình:** file `content/tts/settings.json` giữ giọng, mặc định theo loại và các mã chỉnh tay.
- **Ghi nhận lần tạo:** mỗi dòng của danh mục âm thanh có thêm trường `tts`, lưu cách đọc và thông số đã dùng cho file hiện tại.
- **Bộ đọc thay được:** mã gọi `edge-tts` và trả về mp3 kèm mốc thời gian của lời đọc. Một hàm thuần Python cắt khoảng lặng hai đầu file mp3 theo khung.
- **Một lõi dùng chung:** máy chủ duyệt hiện có thêm các đường dẫn cho công cụ, còn lệnh `python -m tapdoc tts` tạo hàng loạt. Cả hai gọi chung một lõi tạo, khôi phục và duyệt.

**Công nghệ:**
- Python 3.14. Phần dựng bài và kiểm tra giữ thư viện chuẩn. Riêng `edge-tts==7.3.1` cài theo `tools/requirements-tts.txt`, chỉ import khi tạo âm thanh.
- Trang HTML thuần như trang duyệt hiện có.

**Bản thiết kế:** [2026-10-28-app-tap-doc-mvp-design.md](../specs/2026-10-28-app-tap-doc-mvp-design.md), mục 17 (cùng mục 7.1–7.4).

## Global Constraints

**Mã, file và đóng gói**
- Mã âm thanh và tên file `unity/TapDoc/Assets/Content/Resources/audio/<id>.mp3` giữ nguyên. Chỉ ghi đè nội dung file.
- App phát file mp3 đóng gói sẵn. Không gọi bộ đọc khi chạy app, không cần mạng.

**Bộ đọc và thông số**
- Giọng `vi-VN-HoaiMyNeural`. `source` của file tạo ra là `tts_edge_hoaimy`.
- Tốc độ mặc định:
  - `am`, `van`, `dau`: −30%;
  - `tieng`: −25%;
  - `tu`, `cau`, `huong_dan`, `khen`: −15%.

  Cao độ 0 Hz, âm lượng 0%.
- Giới hạn nhận: tốc độ −60…+30 (%), cao độ −30…+30 (Hz), âm lượng −50…+50 (%).

**Trạng thái và bản trước**
- Sau khi tạo: `status = cho_duyet`.
- Mã `dat` không bị tạo lại, trừ khi yêu cầu rõ: nút trong công cụ, hoặc `--gom-da-duyet` ở dòng lệnh.
- "Bản trước" chỉ giữ một bản, ở `content/tts/prev/` (không vào git, không vào bản build). Bấm Đạt thì xoá bản trước.

**Xử lý lỗi**
- Cắt khoảng lặng còn 0,1 giây mỗi đầu, theo mốc lời đọc. Không cắt được thì giữ nguyên file và ghi `trimmed: false`.
- Lỗi mạng hoặc dịch vụ trả rỗng: thử lại tối đa 4 lần, chờ tăng dần. Sau đó báo đúng mã lỗi. **Không ghi đè file cũ khi tạo thất bại.**

**Test và git**
- Test không gọi mạng: luôn dùng bộ đọc giả.
- Chỉ branch `main`, commit theo task. Các commit này gom cùng đợt 2 khi phát hành.
- Không build bản thử.

## Review Focus

1. **Mạng rớt giữa lô tạo hàng loạt:** mã lỗi giữ file, dòng và `tts` cũ; lô chạy tiếp các mã khác và cuối cùng liệt kê mã lỗi.
   - Test: `test_tts_generate.BatchTest.test_failure_keeps_old_file_and_continues` (Task 3).
2. **Bấm "Tạo lại" hai lần liên tiếp:** bản trước là bản ngay trước lần tạo gần nhất, không phải bản gốc.
   - Test: `test_tts_generate.GenerateTest.test_prev_is_the_take_before_last` (Task 3).
3. **Chạy `tapdoc build` sau khi đã chỉnh:** danh mục giữ `tts`, `source` và `status`.
   - Test: `test_manifest.TtsFieldTest.test_build_keeps_tts_record` (Task 4).
4. **Đổi mặc định của một loại:** chỉ các mã chưa `dat` của loại đó thành "cần tạo lại". Mã `dat` chỉ báo "khác mặc định mới", lô không đụng tới.
   - Test: `test_tts_settings.StaleTest.test_default_change_marks_only_unapproved` (Task 1).
5. **Dùng lại bản trước:** file, `tts` và mục chỉnh tay trong cấu hình cùng trở về bản trước, nên mã không còn "cần tạo lại".
   - Test: `test_tts_generate.RestoreTest.test_restore_brings_back_file_and_settings` (Task 3).

---

## Cấu trúc file

```
tools/requirements-tts.txt                 edge-tts==7.3.1
tools/tapdoc/tts_settings.py               đọc/ghi settings.json, thông số thực dùng, dấu nhận dạng, "cần tạo lại"
tools/tapdoc/mp3trim.py                    tách khung mp3, cắt hai đầu theo mốc thời gian
tools/tapdoc/tts_engine.py                 giao diện bộ đọc + EdgeEngine (import edge_tts khi dùng)
tools/tapdoc/tts_generate.py               tạo một mã, khôi phục bản trước, duyệt, chạy lô
tools/tapdoc/manifest.py, __main__.py, review_server.py, review/index.html   (sửa)
content/tts/settings.json                  cấu hình (trong git)
content/tts/prev/                          bản trước (gitignore)
content/review/chain_notes.json            ghi chú chuỗi đánh vần (trong git)
tools/tests/test_tts_settings.py, test_mp3trim.py, test_tts_generate.py, test_tts_server.py, tts_fakes.py
```

## Hợp đồng dữ liệu

`content/tts/settings.json`:
```json
{"voice": "vi-VN-HoaiMyNeural",
 "defaults": {"am": {"rate": -30, "pitch": 0, "volume": 0}, "...": "một mục cho mỗi loại ở mục 7.1"},
 "overrides": {"am_q": {"doc": "cu", "rate": -40}}}
```
- `overrides` chỉ lưu khác biệt so với mặc định. `doc` rỗng hoặc bằng `text` thì không lưu.

Trường mới `tts` trên dòng danh mục âm thanh, chỉ có khi file do bộ đọc tạo:
`{"doc": str, "rate": int, "pitch": int, "volume": int, "voice": str, "sig": str, "trimmed": bool}`.

---

### Task 1: Cấu hình giọng đọc

**Files:** Create `tools/tapdoc/tts_settings.py`, `content/tts/settings.json` (giá trị mặc định ở Global Constraints), test `tools/tests/test_tts_settings.py`. Modify `.gitignore` (thêm `content/tts/prev/`).

**Interfaces (Produces):**
- `@dataclass(frozen=True) class TtsParams: doc: str; rate: int; pitch: int; volume: int; voice: str`
- `load_settings(path) -> dict`, `save_settings(path, settings: dict) -> None` (ghi nguyên tử như `manifest.save_rows`)
- `effective_params(settings: dict, row: dict) -> TtsParams` — mặc định theo `row["kind"]`, đè bằng `overrides[row["id"]]`; `doc` mặc định là `row["text"]`
- `signature(p: TtsParams) -> str` — sha1 của JSON đã sắp khoá
- `set_override(settings, row, *, doc=None, rate=None, pitch=None, volume=None) -> None` — lưu chỉ phần khác mặc định, chuẩn hoá NFC, kiểm tra giới hạn (`ValueError`)
- `needs_regen(settings, row) -> bool` — `status != "dat"` và (`tts` thiếu hoặc `tts["sig"] != signature(effective_params(...))`)
- `differs_from_settings(settings, row) -> bool` — như trên nhưng cho cả mã `dat`

- [ ] **Step 1: Test.** `ParamsTest.test_defaults_by_kind` (`am` −30, `tieng` −25, `cau` −15, `doc == text`); `test_override_wins_and_only_diff_is_stored`; `test_limits_raise`; `StaleTest.test_default_change_marks_only_unapproved` (Review Focus 4); `test_missing_tts_record_needs_regen`.
- [ ] **Step 2:** `python -m unittest tests.test_tts_settings` → FAIL. **Step 3:** cài đặt. **Step 4:** PASS + toàn bộ test Python PASS.
- [ ] **Step 5: Commit** `feat(tools): cấu hình giọng đọc edge-tts (Giọng đọc Task 1)`.

### Task 2: Cắt khoảng lặng mp3  [có thể giao: Codex]

**Files:** Create `tools/tapdoc/mp3trim.py`, `tools/tests/test_mp3trim.py`, `tools/tests/tts_fakes.py`.

**Interfaces (Produces):**
- `fake_mp3(seconds: float) -> bytes` (trong `tts_fakes.py`) — chuỗi khung MPEG-2 Layer III 24 kHz 48 kbps hợp lệ về đầu khung (144 byte, 24 ms mỗi khung), phần dữ liệu toàn 0
- `trim_mp3(data: bytes, speech_start: float, speech_end: float, pad: float = 0.1) -> tuple[bytes, bool]`
  - Giữ các khung giao với `[start − pad, end + pad]`, thêm 1 khung trước để giữ bit reservoir. Bỏ qua thẻ ID3v2 ở đầu.
  - Hỗ trợ MPEG-1/2/2.5 Layer III (độ dài khung từ bảng bitrate/tần số, bit padding).
  - Dữ liệu không đọc được khung → `(data, False)`.

- [ ] **Step 1: Test.**
  - `test_trims_to_speech_plus_pad`: `fake_mp3(1.2)`, mốc 0,5–0,7 → giữ khung từ ⌊0,4/0,024⌋−1 đến ⌈0,8/0,024⌉, `True`.
  - `test_not_mp3_returned_unchanged`.
  - `test_id3_header_skipped`.
  - `test_pad_clamped_at_edges`: mốc 0,0–1,2 → giữ nguyên số khung.
- [ ] **Step 2–4:** FAIL → cài đặt → PASS. **Step 5: Commit** `feat(tools): cắt khoảng lặng mp3 theo khung (Giọng đọc Task 2)`.

### Task 3: Bộ đọc và lõi tạo / khôi phục / duyệt

**Files:** Create `tools/tapdoc/tts_engine.py`, `tools/tapdoc/tts_generate.py`, `tools/tests/test_tts_generate.py`, `tools/requirements-tts.txt`; mở rộng `tts_fakes.py`.

**Interfaces:**
- Consumes: Task 1 (`TtsParams`, `effective_params`, `signature`, `set_override`), Task 2 (`trim_mp3`, `fake_mp3`).
- Produces:
  - `class SynthResult: audio: bytes; speech_start: float | None; speech_end: float | None`
  - `class TtsError(Exception)`, `class TtsUnavailable(TtsError)` (thông điệp có lệnh `python -m pip install -r tools/requirements-tts.txt`)
  - `class EdgeEngine: synthesize(self, p: TtsParams) -> SynthResult` — `edge_tts.Communicate(p.doc, p.voice, rate=f"{p.rate:+d}%", pitch=f"{p.pitch:+d}Hz", volume=f"{p.volume:+d}%", boundary="WordBoundary")`, mốc từ sự kiện `WordBoundary` (đơn vị 100 ns), thử lại 4 lần
  - `class FakeEngine` (trong `tts_fakes.py`): trả `fake_mp3`, ghi lại các lần gọi, lỗi được theo mã
  - `generate_one(row, settings, engine, audio_dir, prev_dir) -> dict` — trả dòng đã cập nhật (`tts`, `source="tts_edge_hoaimy"`, `status="cho_duyet"`); file cũ chuyển sang `prev_dir/<id>.mp3` kèm `prev_dir/<id>.json` (dòng `tts` + `status` + `source` cũ)
  - `restore_previous(row, settings, audio_dir, prev_dir) -> dict` — đổi file về bản trước, gọi `set_override` để cấu hình khớp
  - `approve(row, prev_dir) -> dict` — `status="dat"`, xoá bản trước
  - `run_batch(rows, settings, engine, audio_dir, prev_dir, *, lesson=None, kind=None, ids=None, include_approved=False, on_progress=None, save=None) -> BatchReport(done: list[str], failed: dict[str, str], skipped: int)` — chọn mã `needs_regen` (hoặc mọi mã khi `include_approved`), gọi `save(rows)` sau mỗi mã

- [ ] **Step 1: Test.**
  - `GenerateTest.test_writes_file_row_and_prev`.
  - `test_prev_is_the_take_before_last` (Review Focus 2).
  - `test_engine_error_leaves_everything`.
  - `test_trim_applied_and_flag`.
  - `RestoreTest.test_restore_brings_back_file_and_settings` (Review Focus 5).
  - `ApproveTest.test_approve_deletes_prev`.
  - `BatchTest.test_failure_keeps_old_file_and_continues` (Review Focus 1).
  - `test_skips_approved_unless_asked`.
  - `test_filters_lesson_kind`.
- [ ] **Step 2–4:** FAIL → cài đặt → PASS + toàn bộ. **Step 5: Commit** `feat(tools): lõi tạo âm thanh edge-tts (Giọng đọc Task 3)`.

### Task 4: Lệnh `tts`, danh mục giữ trường `tts`, cảnh báo khi phát hành  [có thể giao: Codex]

**Files:** Modify `tools/tapdoc/manifest.py` (`update_audio_manifest` giữ `tts`), `tools/tapdoc/__main__.py`, `tools/tapdoc/validate.py`. Test: thêm vào `tools/tests/test_manifest.py`, `test_validate.py`, `test_tts_generate.py`.

**Interfaces (Produces):**
- `python -m tapdoc tts [--bai ID] [--loai KIND] [--ma ID ...] [--gom-da-duyet] [--thu]`
  - `--thu`: chỉ in danh sách sẽ tạo.
  - In "Đã tạo N, lỗi M, bỏ qua K", liệt kê mã lỗi; có lỗi thì trả mã 1.
  - Thiếu `edge-tts` thì in lệnh cài và trả mã 2.
- `release_warnings(rows) -> list[str]` trong `validate.py`; `validate --release` in cảnh báo cho `source` bắt đầu bằng `tts_edge_` nhưng không tính là lỗi.

- [ ] **Step 1: Test.**
  - `TtsFieldTest.test_build_keeps_tts_record` (Review Focus 3).
  - `test_cli_tts_dry_run_lists_ids` (dùng `FakeEngine` qua tham số ẩn `engine_factory` của `main`).
  - `test_cli_tts_missing_package_exit_2`.
  - `test_release_warns_on_edge_source_without_error`.
- [ ] **Step 2–4:** FAIL → cài đặt → PASS. **Step 5: Commit** `feat(tools): lệnh tts và cảnh báo nguồn edge-tts (Giọng đọc Task 4)`.

### Task 5: Máy chủ cho công cụ  [có thể giao: Antigravity]

**Files:** Modify `tools/tapdoc/review_server.py` (`make_server(port, manifests_dir, res_dir, *, settings_path, prev_dir, lessons_dir, notes_path, engine_factory)`), `tools/tapdoc/__main__.py` (truyền đường dẫn thật). Test `tools/tests/test_tts_server.py`.

**Đường dẫn mới** (JSON; lỗi đầu vào → 400; mọi ghi trong khoá `server.lock`):
- **Đọc:**
  - `GET /api/tts` → `{voice, defaults, rows: [{id, text, kind, bai, status, source, ghi_chu, params, needs_regen, differs, has_prev}]}`.
  - `GET /media/prev/<id>.mp3` → bản trước.
  - `GET /api/lessons` → danh sách bài.
  - `GET /api/lesson/<lesson_id>` → bài đã dựng.
  - `GET /api/chain-notes`.
- **Cấu hình:**
  - `POST /api/tts/defaults {kind, rate, pitch, volume}` → lưu, trả số mã cần tạo lại.
  - `POST /api/tts/row {id, doc?, rate?, pitch?, volume?}` → `set_override`.
- **Tạo, khôi phục, duyệt:**
  - `POST /api/tts/generate {id}` → `generate_one`, chạy đồng bộ, trả dòng mới; lỗi bộ đọc → 502 kèm thông điệp.
  - `POST /api/tts/restore {id}`.
  - `/api/review` với `status: "dat"` trên âm thanh thì gọi `approve`.
- **Lô:**
  - `POST /api/tts/batch {lesson?, kind?, include_approved?}` → chạy `run_batch` trong luồng nền; đang chạy thì 409.
  - `GET /api/tts/job` → `{running, total, done, current, failed}`.
- **Ghi chú chuỗi:** `POST /api/chain-notes {lesson, where, chain, note}` → lưu vào `content/review/chain_notes.json`; `note` rỗng thì xoá.

- [ ] **Step 1: Test** (máy chủ thật trên cổng 0, `FakeEngine`, thư mục tạm):
  - `test_generate_then_prev_served`;
  - `test_row_override_marks_needs_regen`;
  - `test_defaults_change_counts`;
  - `test_restore_and_approve`;
  - `test_batch_job_progress_and_409`;
  - `test_engine_failure_502_keeps_file`;
  - `test_chain_note_roundtrip`;
  - `test_bad_input_400`.
- [ ] **Step 2–4:** FAIL → cài đặt → PASS. **Step 5: Commit** `feat(tools): máy chủ công cụ giọng đọc (Giọng đọc Task 5)`.

### Task 6: Giao diện công cụ  [có thể giao: Codex]

**Files:** Modify `tools/tapdoc/review/index.html`. Test: thêm `test_tts_server.test_index_has_tts_controls` (trang có các phần tử theo `id` dưới đây).

**Tab "Âm thanh" mở rộng:**
- **Khung "Mặc định theo loại"** (`#tts-defaults`): mỗi loại một dòng tốc độ/cao độ/âm lượng và nút Lưu. Kèm số mã cần tạo lại, nút "Tạo lại các mã cần tạo lại" (`#tts-batch`) và thanh tiến độ hỏi `/api/tts/job` mỗi giây.
- **Bộ lọc thêm:** "Cần tạo lại", "Đã chỉnh tay".
- **Mỗi dòng** (`.tts-row`):
  - chữ;
  - ô "Cách đọc";
  - ba ô số tốc độ/cao độ/âm lượng;
  - nút Tạo lại, Nghe, Nghe bản trước (khi `has_prev`), Dùng lại bản trước, Đạt, Không đạt;
  - ô ghi chú;
  - nhãn "cần tạo lại" / "khác mặc định mới".

  Cập nhật tại chỗ, không vẽ lại cả trang (giữ cách làm của `saveReview`).

**Tab mới "Nghe theo bài"** (`#tab-lesson`):
- Chọn bài.
- Mỗi bước có chuỗi đánh vần (`spell`, `spells` của từng mục, câu): nút ▶ phát lần lượt các mảnh, nghỉ 0,5 giây như app.
- Bấm một mảnh thì nhảy sang tab Âm thanh, lọc đúng mã đó.
- Ô ghi chú cho chuỗi, lưu qua `/api/chain-notes`.

- [ ] **Step 1–4:** test FAIL → cài đặt → PASS. **Claude tự mở trang** bằng trình duyệt trong app với máy chủ thật và bộ đọc thật, rồi thử một vòng:
  - tạo lại `am_q`;
  - nghe bản trước;
  - dùng lại bản trước;
  - đổi mặc định `am`;
  - nghe chuỗi "sàn" ở bài 42.
- [ ] **Step 5: Commit** `feat(tools): giao diện chỉnh giọng đọc (Giọng đọc Task 6)`.

### Task 7: Tạo toàn bộ âm thanh mới

- [ ] **Step 1:** `python -m pip install --user -r tools/requirements-tts.txt`. Sau đó `python -m tapdoc tts --thu` phải liệt kê 1.317 mã.
- [ ] **Step 2:** Chạy `python -m tapdoc tts` ở chế độ nền, theo dõi. Mã lỗi thì chạy lại lệnh, vì lệnh chỉ tạo các mã còn cần.
- [ ] **Step 3:** Kiểm tra:
  - `python -m tapdoc validate` → `OK`;
  - EditMode `DataTests.AllReferencedAssetsExist` PASS;
  - PlayMode `MvpEndToEndTests` PASS (bài 1–64);
  - nghe ngẫu nhiên 10 file trên trang công cụ để chắc file phát được.
- [ ] **Step 4: Commit** `feat(content): âm thanh edge-tts HoaiMy cho bài 1–64 (Giọng đọc Task 7)`.
- [ ] **Step 5:** Báo chủ dự án mở công cụ (`python -m tapdoc review`) để nghe, chỉnh và duyệt.
