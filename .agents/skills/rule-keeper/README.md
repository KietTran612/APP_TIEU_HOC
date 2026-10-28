# rule-keeper

Bộ công cụ nhỏ (chỉ cần Node ≥ 18) để **Codex** và **Antigravity** không quên yêu cầu của bạn và
quy tắc của project trong phiên dài, nhận ra khi quy tắc đổi giữa chừng, và không được báo "xong"
khi chưa tự đối chiếu công việc với từng yêu cầu.

Nó không thay đổi cách bạn làm việc: cài một lần, rồi dùng Codex/Antigravity như bình thường.

**Hướng dẫn dùng từng bước cho Codex và Antigravity: [HUONG-DAN.md](HUONG-DAN.md).** File này là
phần kỹ thuật.

## Cài vào một project

1. Chép nguyên thư mục này vào `<project>/.agents/skills/rule-keeper/`. Gốc project được suy ra từ
   chính vị trí này (thư mục chứa `.agents`), nên project dùng git hay không đều được.
2. Bấm đúp `setup-codex.cmd` và/hoặc `setup-antigravity.cmd`. Cả hai gọi `setup.mjs <công cụ>`:
   kiểm tra máy → `install.mjs --only <công cụ>` → chạy thử hook đúng như công cụ gọi rồi dọn phiên
   thử → kiểm tra công cụ có trên máy → in (và mở sẵn) bước người dùng phải tự làm.

Cài tay, không qua setup: `node .agents/skills/rule-keeper/install.mjs [--only codex|antigravity]`.

Install chỉ **tạo** bốn file trỏ, không sửa file nào có sẵn:

| File | Cho ai | Nội dung |
|---|---|---|
| `.agents/rules/rule-keeper.md` | Antigravity | luật luôn bật, sinh từ `rules/core.md` + `rules/user.md` (hook tự đồng bộ khi bạn sửa hai file đó) |
| `.agents/hooks.json` | Antigravity | hook `PreInvocation` + `Stop` |
| `.codex/hooks.json` | Codex | hook `SessionStart` + `UserPromptSubmit` + `Stop` |
| `.agent-ledger/.gitignore` | git | thư mục sổ tự loại mình khỏi git |

Nếu project đã có `.agents/hooks.json` hoặc `.codex/hooks.json` của người khác, install **từ chối
ghi đè** và in nội dung để bạn tự gộp.

**Một việc phải làm tay, một lần:** Codex chỉ chạy hook của project sau khi bạn tin cậy chúng. Mở
Codex trong project, gõ `/hooks`, tin cậy ba hook `rule-keeper`. Mỗi lần `.codex/hooks.json` đổi
(ví dụ chạy lại install sau khi dời thư mục kit) phải tin cậy lại. Antigravity không cần bước này.

Kiểm tra: `node .agents/skills/rule-keeper/install.mjs --check`. Gỡ: `--uninstall` (chỉ xoá file do
nó tạo; sổ trong `.agent-ledger/` và `.gitignore` của nó giữ lại để sổ không lộ ra git). Cả hai
nhận `--only codex|antigravity`.

## Nó làm gì

```
người dùng gõ ──► hook ──► ghi NGUYÊN VĂN vào sổ (.agent-ledger/<agent>-<phiên>.md)
                     │        + nhắc agent: "có yêu cầu mới? ghi thành dòng R#"
                     │        + so file quy tắc với bản đã đọc → có đổi thì chèn DIFF
                     ▼
                  agent làm việc, đọc lại sổ trước mỗi bước
                     │
agent định dừng ──► hook Stop: có file đổi / có nói "xong" mà chưa GATE OK?
                     │        → không cho dừng, bắt điền Done-gate và chạy `rk.mjs gate`
                     ▼
              `rk.mjs gate` đọc sổ: mỗi R# có ✅+bằng chứng hoặc ⚠️/❌+lý do?
              mọi M# được tính? có dòng Quy tắc / Diff / Kiểm tra? quy tắc có đổi?
                     │
                  GATE OK ──► agent mới được trả lời, và phải nói rõ cái gì chưa xong
```

- **Sổ yêu cầu** là trí nhớ ngoài ngữ cảnh. Ba mục: `Yêu cầu` (agent ghi, dạng `R#`), `Tin nhắn của
  người dùng` (hook ghi, dạng `M#`, nguyên văn), `Done-gate` (agent điền trước khi báo xong). Khi có
  tin nhắn mới, Done-gate cũ được dời xuống `Lịch sử done-gate`.
- **Bạn có thể sửa sổ trực tiếp** — thêm một dòng R#, gạch một yêu cầu — lượt sau agent thấy ngay.
- **Quy tắc đổi giữa chừng**: hook chụp bản agent đã đọc; file đổi thì lượt kế agent nhận diff và
  phải rà lại cả phần đã làm. Áp dụng cho `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.agents/rules/*.md`
  và chính `rules/*.md` của kit (danh sách trong `config.json`).
- **Sau khi ngữ cảnh bị nén / phiên mở lại** (Codex): hook chèn lại đường dẫn sổ, các yêu cầu còn hiệu
  lực và ba tin nhắn gần nhất, kèm lệnh "coi như vừa quên hết, đọc lại sổ".
- **Stop-gate chặn tối đa 2 lần liên tiếp** rồi thôi, để agent không bị kẹt vô hạn — nhưng không
  im lặng: Codex hiện cảnh báo cho bạn; Antigravity (không có kênh đó) bị ép thêm một bước cuối mà
  việc duy nhất là nói với bạn rằng việc chưa qua gate. Ở tin nhắn kế, hook còn nhắc agent điều đó
  cho tới khi gate qua. Agent đang hỏi bạn (không kể việc đã làm) thì không bị chặn.

## Thêm luật của riêng bạn

- Luật mang theo mọi project: sửa `rules/user.md` (rồi chép thư mục kit sang project khác).
- Luật nền của cơ chế: `rules/core.md`. Luật riêng project: `AGENTS.md` / `.agents/rules/*.md` như bình thường.
- Ba file đó đều được hook theo dõi; sửa xong không cần chạy lại install (bản luôn bật cho Antigravity
  được hook đồng bộ ở lần gọi kế). Antigravity cắt file luật ở 24.000 byte — `--check` in kích thước.

## Dùng không có hook (Claude Code, agent khác, hoặc hook chưa được tin cậy)

Mọi lệnh chạy ở thư mục gốc project:

```bash
node .agents/skills/rule-keeper/bin/rk.mjs start --agent <tên>         # tạo sổ, in quy tắc + mục lục file quy tắc
node .agents/skills/rule-keeper/bin/rk.mjs where --agent <tên>         # sổ gần nhất của agent đó
node .agents/skills/rule-keeper/bin/rk.mjs check --ledger <sổ>         # quy tắc nào đã đổi (kèm diff)
node .agents/skills/rule-keeper/bin/rk.mjs gate  --ledger <sổ>         # done-gate
node .agents/skills/rule-keeper/bin/rk.mjs index                       # chỉ in mục lục file quy tắc
```

Không có hook thì agent phải tự ghi M# (hook mới ghi hộ) — `SKILL.md` nói rõ cách làm.

## Cấu hình — `config.json`

| Khoá | Mặc định | Ý nghĩa |
|---|---|---|
| `ledgerDir` | `.agent-ledger` | thư mục sổ |
| `ruleFiles` | AGENTS/CLAUDE/GEMINI.md mọi cấp, `.agents/rules/*.md`, `.agent/rules/*.md` | file quy tắc theo dõi (glob của git) |
| `exclude` | `.agents/rules/rule-keeper.md` | bỏ theo dõi (bản sinh tự động) |
| `stopGate` | `true` | `false` = không chặn cuối lượt, chỉ còn nhắc + lệnh gate chạy tay |
| `maxConsecutiveStopBlocks` | `2` | chặn tối đa bao nhiêu lần liên tiếp |
| `anchorEvery` | `15` | Antigravity: nhắc lại yêu cầu sau mỗi bao nhiêu lần gọi model trong một lượt dài |
| `maxDiffLines` | `120` | diff quy tắc dài hơn thì cắt, kèm số dòng để agent tự mở file |
| `maxContextChars` | `24000` | trần một lần chèn ngữ cảnh |
| `maxMessageChars` | `4000` | tin nhắn dài hơn thì cắt khi ghi sổ |

Project có `CLAUDE.md` rất dài (ở đây ~110 KB) sẽ khiến agent đọc nó theo 8–9 đoạn ở đầu phiên. Đó là
chủ ý — luật nằm ở đó — nhưng nếu muốn tiết kiệm, bỏ `**/CLAUDE.md` khỏi `ruleFiles`.

## Giới hạn đã biết

- **Codex trên Windows chạy lệnh qua PowerShell 5.1**, nên output tiếng Việt của *mọi* lệnh (kể cả
  `rk.mjs check/gate`) về tới model dạng mojibake. Nội dung hook chèn vào thì đúng UTF-8 (đã kiểm
  trong transcript). Model vẫn hiểu được trong hai lượt thử; để chắc, mã kết quả gate là ASCII
  (`GATE OK` / `GATE FAILED`).
- Hook là **cơ chế nhắc + chặn**, không phải chứng minh: agent cố tình điền sổ sai vẫn qua được gate.
  Nó loại bỏ cái "quên" và cái "báo bừa", không loại bỏ cái "nói dối".
- Antigravity: chỉ thử trên CLI `agy` (1.2.5, 1.3.4). IDE và Antigravity 2.0 dùng cùng
  `.agents/hooks.json` theo tài liệu, chưa chạy thử. Hook đọc tin nhắn của bạn từ transcript
  Antigravity ghi (`transcriptPath` trong payload), vì hook của nó không nhận prompt.
- Codex: đã thử `codex` 0.147.0 (`exec`, `exec resume`) và 0.162.1 (`exec`, project không git). Hook
  của project không chạy trong project chưa được tin cậy (`trust_level`) và hook chưa được tin cậy
  qua `/hooks`. Lệnh hook tự dò ngược từ thư mục của phiên lên tìm kit, nên mở Codex ở thư mục con
  vẫn chạy.
- Project không dùng git (hoặc máy không có git): mọi thứ chạy, trừ việc phát hiện file đã đổi — gate
  cuối lượt chỉ được đòi khi agent nói "xong" — và diff quy tắc (đổi thì agent được bảo đọc lại cả file).
- Câu hỏi "mở công cụ ngay? (Y/n)" ở cuối setup cần bàn phím thật nên không có test tự động; lệnh mở
  cửa sổ (`start /D "<project>"`) đã được kiểm với đường dẫn có dấu cách và tiếng Việt.
- Không có gì chạy cho Claude Code (chưa được yêu cầu); Claude Code vẫn dùng được các lệnh tay ở trên.

## Kiểm thử

```bash
node --test .agents/skills/rule-keeper/test/rk.test.mjs
```

Mỗi test dựng một project tạm (có và không có git), cài kit, gọi hook đúng như hai công cụ gọi (JSON
trên stdin), rồi đọc lại sổ và output; hai file `setup-*.cmd` được chạy thật qua `cmd.exe`. Cuối cùng kit được chạy thật qua `codex exec` và `agy -p` hai lượt, lượt hai
sau khi đổi `AGENTS.md`: cả hai agent đều nhận diff, rà lại file đã tạo và dừng hỏi khi luật mới mâu
thuẫn yêu cầu cũ.
