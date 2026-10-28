# Hướng dẫn dùng rule-keeper với Codex và Antigravity

Tài liệu này dành cho **người dùng**: cài thế nào, làm gì một lần, hằng ngày thấy gì, gặp trục trặc
thì xử lý ra sao. Phần kỹ thuật (cơ chế, cấu hình, giới hạn) nằm ở [README.md](README.md).

**Tóm tắt một câu:** cài một lần, rồi cứ chat với Codex/Antigravity như bình thường — kit ghi lại
mọi yêu cầu của bạn vào một "sổ", báo cho agent khi file quy tắc đổi, và không cho agent nói "xong"
khi chưa đối chiếu công việc với từng yêu cầu.

---

## 1. Cài vào một project

Làm một lần cho mỗi project. (Project `one-affree-collectdata` đã cài sẵn — bỏ qua bước này.)

Cần có **Node.js 18 trở lên** (cài bản LTS ở nodejs.org). Project dùng git hay không đều được.

1. Giải nén file `rule-keeper-*.7z` vào **thư mục gốc** của project. Kit sẽ nằm đúng chỗ:
   `<project>/.agents/skills/rule-keeper/`.
2. Mở thư mục `.agents\skills\rule-keeper` trong File Explorer và **bấm đúp**:
   - `setup-codex.cmd` — để dùng với Codex
   - `setup-antigravity.cmd` — để dùng với Antigravity

   Dùng cả hai công cụ thì chạy cả hai file. Mỗi file tự làm 5 bước:

   | Bước | Làm gì |
   |---|---|
   | 1 | Kiểm tra Node.js, tìm gốc project, báo nếu project không dùng git |
   | 2 | Cài các file trỏ của công cụ đó |
   | 3 | **Chạy thử hook đúng như công cụ sẽ gọi**, rồi dọn phiên thử |
   | 4 | Kiểm tra công cụ đã có trên máy chưa |
   | 5 | In việc bạn phải tự làm, và hỏi có mở công cụ ngay ở đúng thư mục không |

   Dòng cuối phải là **`Setup Codex: xong phần tự động.`** (hoặc `Setup Antigravity: …`). Có dòng
   `✗` nào thì đọc lý do in ngay tại dòng đó.

   Thích dùng terminal hơn thì chạy (ở thư mục gốc project):

```bash
node .agents/skills/rule-keeper/setup.mjs codex
```

```bash
node .agents/skills/rule-keeper/setup.mjs antigravity
```

Project **không dùng git** vẫn cài và chạy được, chỉ kém một điểm: hook không biết file nào đã đổi,
nên gate chỉ được đòi khi agent nói "xong" (setup sẽ báo điều này bằng một dòng `⚠`).

Các file setup chỉ **tạo mới** những file sau, không sửa file nào có sẵn của project:

| File | Dùng cho |
|---|---|
| `.codex/hooks.json` | Codex |
| `.agents/hooks.json` | Antigravity |
| `.agents/rules/rule-keeper.md` | Antigravity (luật luôn bật) |
| `.agent-ledger/.gitignore` | giữ thư mục sổ ngoài git |

`setup-codex.cmd` chỉ tạo dòng Codex và `.gitignore`; `setup-antigravity.cmd` chỉ tạo hai dòng
Antigravity và `.gitignore`. Nếu project đã có sẵn `.codex/hooks.json` hoặc `.agents/hooks.json` của ai
khác, setup **không ghi đè** mà in ra nội dung để bạn tự gộp vào.

3. Làm tiếp phần riêng của từng công cụ bên dưới (setup cũng in đúng phần đó ở bước 5).

Kiểm tra cài đặt bất cứ lúc nào (chạy lại file setup cũng được — chạy lại không hại gì):

```bash
node .agents/skills/rule-keeper/install.mjs --check
```

---

## 2. Codex

### 2.1. Việc phải làm một lần: cho phép hook chạy

Codex **không chạy** hook nằm trong project cho tới khi bạn duyệt — để một repo tải từ đâu về không
thể tự chạy lệnh lạ. Chưa duyệt thì kit nằm đó nhưng không làm gì với Codex. Có hai lớp duyệt:

**a) Tin cậy thư mục project.** Lần đầu mở Codex trong một thư mục, Codex hỏi:
*"Do you trust the contents of this directory?"* — chọn **tin cậy**. Không tin cậy thì Codex bỏ qua
toàn bộ cấu hình riêng của project, kể cả hook. (Project `one-affree-collectdata` đã được tin cậy.)

**b) Duyệt 3 hook của rule-keeper.**

1. Mở terminal ở **thư mục gốc** project và chạy:

```bash
codex
```

2. Codex báo: **`3 hooks need review before they can run.`**
3. Gõ `/hooks` rồi Enter. Danh sách hook hiện ra; ba hook `rule-keeper` (`SessionStart`,
   `UserPromptSubmit`, `Stop`) có nhãn **`New hook - review required`**.
4. Nhìn dòng hướng dẫn phím ở cuối màn hình và bấm phím ứng với **"to trust all"** để tin cậy cả ba.
   Muốn xem trước: chọn từng hook, xem lệnh, rồi bấm phím ứng với **"to trust"**. Lựa chọn được lưu
   tự động.
5. Thoát: `/exit`.

Làm lại bước (b) chỉ khi hook hiện nhãn **`Modified since last trusted - review required`** — xảy ra
khi `.codex/hooks.json` đổi, ví dụ bạn chạy lại setup sau khi dời thư mục kit, hoặc sau khi cập nhật
kit lên bản mới có đổi lệnh hook.

Bấm đúp `setup-codex.cmd` thì cuối cùng nó hỏi **có mở Codex ngay không** — trả lời `Y` là Codex mở
sẵn trong một cửa sổ mới, đúng thư mục project, bạn chỉ việc làm bước (b).

### 2.2. Kiểm tra đã chạy chưa

Mở Codex ở gốc project, gửi một tin nhắn bất kỳ. Trong thư mục `.agent-ledger/` phải xuất hiện file
`codex-xxxxxxxx.md` chứa **nguyên văn** tin nhắn của bạn. Có file đó là hook đang chạy.

### 2.3. Hằng ngày bạn sẽ thấy gì

- Lúc mở phiên và mỗi lần bạn gửi tin, Codex chạy hook (có thể thấy dòng trạng thái
  `rule-keeper: nạp quy tắc và sổ yêu cầu` / `rule-keeper: ghi tin nhắn vào sổ`).
- Agent tự ghi yêu cầu của bạn thành các dòng `R1, R2, …` trong sổ trước khi làm.
- Trước khi trả lời "xong", agent điền phần đối chiếu và chạy gate. Câu trả lời cuối thường có
  **`GATE OK`** kèm việc nào xong (có bằng chứng), việc nào chưa.
- Nếu agent định dừng mà chưa qua gate, hook bắt nó làm tiếp (bạn không phải làm gì). Chặn tối đa 2
  lần; sau đó Codex hiện **cảnh báo cho bạn**: *"agent kết thúc lượt mà CHƯA qua done-gate…"* — nghĩa
  là việc đó **chưa được coi là xong**.
- Phiên dài bị Codex nén ngữ cảnh, hoặc bạn mở lại phiên cũ (`codex resume`): hook tự nạp lại sổ và
  ba tin nhắn gần nhất, nên agent không mất yêu cầu cũ.

### 2.4. Lưu ý riêng với Codex

- **Mở Codex ở thư mục gốc project.** Hook vẫn chạy nếu bạn mở ở thư mục con, nhưng các lệnh mà
  agent được bảo chạy (`node .agents/skills/rule-keeper/bin/rk.mjs …`) tính từ thư mục gốc.
- Trên Windows, Codex chạy lệnh qua PowerShell nên chữ tiếng Việt trong *kết quả lệnh* có thể hiện
  thành ký tự lạ trong log. Không ảnh hưởng việc ghi sổ; kết quả gate in bằng mã không dấu
  (`GATE OK` / `GATE FAILED`) cho chắc.
- Đã thử với Codex CLI 0.147 và 0.162 (cả project có và không dùng git). **App Codex chưa được thử** — nếu dùng app mà không thấy file sổ xuất
  hiện, hãy làm bước 2.1 bằng CLI một lần rồi thử lại.

---

## 3. Antigravity

### 3.1. Việc phải làm một lần

Thường **không cần làm gì**: Antigravity tự nạp `.agents/hooks.json` và `.agents/rules/rule-keeper.md`.

Nếu Antigravity hỏi có tin cậy thư mục (workspace) không, chọn **tin cậy**. Muốn xem hook đã được
nạp chưa: gõ `/hooks` trong Antigravity (hoặc mở Settings) — phải thấy hook tên `rule-keeper` đang bật.

### 3.2. Kiểm tra đã chạy chưa

Gửi một tin nhắn bất kỳ. Trong `.agent-ledger/` phải xuất hiện file `agy-xxxxxxxx.md` chứa nguyên
văn tin nhắn của bạn.

### 3.3. Hằng ngày bạn sẽ thấy gì

- Giống Codex: agent ghi `R#` vào sổ, đọc lại sổ trước khi làm, chạy gate trước khi báo xong.
- Trong một lượt làm việc dài (nhiều bước), cứ khoảng 15 lần gọi model hook nhắc lại yêu cầu một lần.
- Agent định dừng mà chưa qua gate → hook bắt làm tiếp. Hết 2 lần chặn, Antigravity không có chỗ hiện
  cảnh báo riêng cho bạn, nên hook **buộc agent viết thêm một dòng nói với bạn** rằng việc chưa qua
  gate. Thấy dòng đó nghĩa là việc **chưa được coi là xong**.
- Ở tin nhắn kế tiếp của bạn, agent còn được nhắc lại điều đó cho tới khi gate qua.

### 3.4. Lưu ý riêng với Antigravity

- Hook của Antigravity không nhận được tin nhắn của bạn trực tiếp, nên kit đọc lịch sử hội thoại mà
  Antigravity tự lưu (ngay trước lần gọi model đầu tiên của mỗi lượt). Bạn không cần làm gì.
- Đã thử với Antigravity **CLI** (`agy` 1.2.5 và 1.3.4). **IDE và Antigravity 2.0 chưa được thử** — theo tài
  liệu chúng dùng cùng file `.agents/hooks.json`; nếu không thấy file sổ xuất hiện, báo lại.

---

## 4. Dùng chung cho cả hai

### 4.1. Thêm quy tắc

| Bạn muốn quy tắc áp dụng cho | Làm ở đâu |
|---|---|
| Chỉ phiên đang chat | Nói thẳng trong chat — agent ghi thành `R#` trong sổ |
| Cả project này | Thêm vào `AGENTS.md` (hoặc `CLAUDE.md`, `GEMINI.md`, `.agents/rules/*.md`) |
| **Mọi** project của bạn | Thêm vào `.agents/skills/rule-keeper/rules/user.md`, rồi mang kit sang project khác |

Sửa xong **không cần chạy lại install**. Ở lượt kế, agent đang chạy nhận được phần thay đổi và phải
rà lại cả việc đã làm theo luật mới. Nếu luật mới mâu thuẫn với điều bạn yêu cầu trước đó, agent
được dặn **dừng lại hỏi bạn** thay vì tự chọn.

### 4.2. Xem và sửa sổ

Sổ nằm ở `.agent-ledger/<agent>-<phiên>.md`, mở bằng editor bất kỳ. Thư mục này không vào git.

- **Thêm một yêu cầu:** thêm dòng `- R5 (M3) "lời bạn" → việc phải đạt` vào mục `## Yêu cầu`.
- **Bỏ một yêu cầu:** thêm `[huỷ: lý do]` vào cuối dòng đó (chữ `[huỷ]` trần không được tính).
- **Thay một yêu cầu:** thêm dòng mới `R6`, và ghi `[thay bởi R6]` vào cuối dòng cũ.

Lượt sau agent sẽ thấy thay đổi của bạn.

### 4.3. Những câu bạn có thể nói với agent

- *"Đọc lại sổ rồi chạy gate."* — khi thấy agent quên hoặc làm sai yêu cầu.
- *"Chạy check xem quy tắc có đổi không."* — sau khi bạn vừa sửa file quy tắc.
- *"Những yêu cầu nào còn chưa xong?"* — agent trả lời theo sổ, không theo trí nhớ.

### 4.4. Tắt hoặc gỡ

- **Chỉ nhắc, không chặn agent dừng:** mở `.agents/skills/rule-keeper/config.json`, đổi
  `"stopGate": true` thành `"stopGate": false`.
- **Gỡ khỏi project** (chỉ xoá file do kit tạo; sổ cũ giữ lại):

```bash
node .agents/skills/rule-keeper/install.mjs --uninstall
```

---

## 5. Gặp trục trặc

| Triệu chứng | Nguyên nhân thường gặp | Cách xử lý |
|---|---|---|
| Gửi tin mà không có file sổ mới trong `.agent-ledger/` (Codex) | Thư mục chưa được tin cậy, hoặc chưa duyệt hook | Làm lại mục 2.1 |
| Như trên (Antigravity) | Workspace chưa được tin cậy, hoặc hook đang tắt | Mục 3.1, xem `/hooks` |
| Có file sổ nhưng agent vẫn không theo | Hook chạy nhưng gặp lỗi | Xem `.agent-ledger/.state/hook-errors.log` |
| Agent bị chặn dừng ở mọi lượt | File do người/agent khác sửa trong cùng thư mục cũng được tính là "có thay đổi" | Bảo agent ghi rõ trong dòng `Diff:` của sổ là file đó không phải của nó, rồi chạy gate; hoặc tắt chặn (mục 4.4) |
| Agent không nhận ra quy tắc bạn vừa thêm | File quy tắc không nằm trong danh sách được theo dõi | Chạy lệnh `index` ở mục 6 xem danh sách; thêm tên file vào `ruleFiles` trong `config.json` |
| Codex báo hook "Modified since last trusted" | `.codex/hooks.json` đã đổi | Duyệt lại như mục 2.1 (b) |
| Dời thư mục kit sang chỗ khác, hoặc cập nhật kit lên bản mới | Các file trỏ vẫn theo bản cũ | Chạy lại file setup, rồi duyệt lại hook Codex |
| Bấm đúp file setup thì cửa sổ báo `Chua co Node.js` | Máy chưa cài Node.js | Cài bản LTS ở nodejs.org, chạy lại |
| Setup báo `Không xác định được gốc project` | Kit không nằm ở `<project>/.agents/skills/rule-keeper` | Giải nén lại vào đúng thư mục gốc project |

---

## 6. Khi không có hook (Claude Code, agent khác, hoặc hook chưa được duyệt)

Agent vẫn dùng được kit bằng lệnh tay — chạy ở thư mục gốc project. Bạn chỉ cần bảo agent:
*"dùng rule-keeper: chạy start rồi làm theo SKILL.md"*.

```bash
node .agents/skills/rule-keeper/bin/rk.mjs start --agent <tên>
```

```bash
node .agents/skills/rule-keeper/bin/rk.mjs check --ledger <đường dẫn sổ>
```

```bash
node .agents/skills/rule-keeper/bin/rk.mjs gate --ledger <đường dẫn sổ>
```

```bash
node .agents/skills/rule-keeper/bin/rk.mjs index
```

`start` tạo sổ và in quy tắc; `check` báo quy tắc nào đã đổi; `gate` là bước đối chiếu trước khi báo
xong; `index` liệt kê các file quy tắc đang được theo dõi. Không có hook thì agent phải tự chép tin
nhắn của bạn vào sổ — [SKILL.md](SKILL.md) có hướng dẫn cho agent.
