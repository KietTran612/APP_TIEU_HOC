---
name: rule-keeper
description: Use when about to tell the user a task is done, fixed, finished, ready or passing ("xong", "hoàn thành", "đã sửa", "tests pass"); when a "[rule-keeper]" message blocks the end of a turn or reports changed rules; when the user states a requirement, constraint, correction or preference; and after context compaction or a resumed session.
---

# rule-keeper — sổ yêu cầu và done-gate

## Tổng quan

Ngữ cảnh chat sẽ quên; file thì không. Mọi yêu cầu của người dùng sống trong **sổ yêu cầu** của
phiên, và mọi lần báo "xong" phải đi qua **done-gate**: từng yêu cầu được đối chiếu với bằng chứng
quan sát được, rồi lệnh `gate` kiểm tra lại sổ trước khi bạn được trả lời.

Đường dẫn sổ và lệnh đầy đủ nằm trong các dòng `[rule-keeper]` mà hook chèn vào. Không thấy dòng
nào: `node .agents/skills/rule-keeper/bin/rk.mjs start --agent <tên của bạn>` (một lần mỗi phiên), hoặc
`node .agents/skills/rule-keeper/bin/rk.mjs where --agent <tên>` để tìm lại sổ. Mọi lệnh chạy ở thư mục gốc project.

**Làm sai chữ của luật là làm sai tinh thần của luật.**

## Sổ yêu cầu

| Mục | Ai ghi | Nội dung |
|---|---|---|
| `## Yêu cầu` | bạn | `- R3 (M2) "trích nguyên văn" → việc cụ thể phải đạt` |
| `## Tin nhắn của người dùng` | hook (Codex, Antigravity) | `### M2 · <giờ>` + nguyên văn tin nhắn |
| `## Done-gate` | bạn, trước khi báo xong | một dòng cho mỗi R# và M# — xem dưới; là của LƯỢT hiện tại |
| `## Lịch sử done-gate` | hook | Done-gate của các lượt trước, hook tự dời xuống khi có tin nhắn mới; gate không đọc |

- Ghi R# **trước khi làm**, ngay khi tin nhắn có yêu cầu, ràng buộc, sửa sai, sở thích, đổi ý.
- Không có hook (bạn tự chạy `start`): tự ghi mỗi tin nhắn của người dùng thành `### M# · <giờ>` +
  nguyên văn vào mục "Tin nhắn của người dùng", trước khi ghi R#.
- Người dùng đổi ý: thêm R# mới, đánh dấu dòng cũ `[thay bởi R5]` hoặc `[huỷ: <lý do, M#>]`, đặt
  sau phần trích dẫn. Không xoá. Chỉ hai dạng đó đóng được yêu cầu: `[huỷ]` trần, hay chữ `[huỷ]`
  nằm trong lời người dùng trích nguyên văn (ví dụ "thêm nút [huỷ]"), không tính.
- Một tin nhắn có nhiều ý → nhiều R#, cùng `(M#)`.
- Người dùng có thể tự sửa sổ. Dòng R# do người dùng thêm có giá trị như lời nói trong chat.

## Khi quy tắc đổi giữa chừng

Thấy `QUY TẮC ĐÃ ĐỔI` (hoặc `check` báo đổi):

1. Đọc diff. Diff bị cắt → mở file và đọc quanh các dòng được nêu.
2. Áp dụng cho phần việc còn lại.
3. Rà lại phần ĐÃ làm theo luật mới; sửa chỗ vi phạm hoặc nói rõ là chưa sửa.
4. Luật mới mâu thuẫn một R# → hỏi người dùng, đừng tự chọn.

## Done-gate — bắt buộc trước mọi câu "xong"

Làm đủ, theo thứ tự:

1. `node .agents/skills/rule-keeper/bin/rk.mjs check --ledger <sổ>` — quy tắc có đổi không. Đổi thì làm mục trên trước.
2. Đọc lại **nguyên văn** mục "Tin nhắn của người dùng" trong sổ — không làm theo trí nhớ.
3. Mỗi R# còn hiệu lực, một dòng trong `## Done-gate`:
   - `- R1 ✅ <đã làm gì> — bằng chứng: <lệnh đã chạy + kết quả đọc được | file:dòng | kết quả truy vấn>`
   - `- R2 ⚠️ <mới xong phần nào> — còn thiếu: <gì, vì sao>` hoặc `- R2 ❌ chưa làm: <vì sao>`

   Bằng chứng là thứ bạn **quan sát được trong phiên này**. "Chắc là chạy", "theo logic thì đúng",
   "đã sửa code" không phải bằng chứng.
4. Mỗi M# không sinh R# nào: `- M4 — không có yêu cầu mới`.
5. `- Diff: …` — chạy `git status` và `git diff -- <file của bạn>`, đọc TỪNG hunk: thuộc R# nào?
   có thay đổi không ai yêu cầu? log/debug tạm còn sót? có đụng file của người khác? Không sửa file
   nào thì ghi `- Diff: không sửa file`.
6. `- Quy tắc: …` — nêu những quy tắc của project (và `rules/user.md`) áp dụng cho việc này mà bạn
   đã đối chiếu, kể cả checklist "trước khi xong" nếu project có.
7. `- Kiểm tra: <lệnh> → <kết quả>` — chạy lệnh kiểm tra mà project quy định (lint, typecheck,
   test…) cho phần đã đụng và ĐỌC output. Không chạy được thì ghi lý do; không được ghi "pass".
8. Đúng yêu cầu chưa? Đọc lại M1… và trả lời thật: làm đúng cái được hỏi hay một cái gần giống?
   còn gì được hỏi mà chưa làm? có làm gì không ai hỏi? Câu trả lời đổi dòng nào ở bước 3 thì sửa.
9. `node .agents/skills/rule-keeper/bin/rk.mjs gate --ledger <sổ>` → phải in `GATE OK`. `GATE FAILED` → sửa sổ
   hoặc công việc theo danh sách nó in, chạy lại.
10. Mới trả lời người dùng: ✅ gì (bằng chứng ngắn), ⚠️/❌ gì, điều gì chưa kiểm chứng.

Đang báo tiến độ, chưa xong? Vẫn làm gate, đánh ⚠️ cho phần dở. Gate đo sự trung thực của báo cáo,
không đòi mọi việc phải xong.

## Ngụy biện thường gặp

| Ý nghĩ | Thực tế |
|---|---|
| "Việc nhỏ, khỏi gate" | Việc nhỏ cũng bị báo sai. Gate của việc nhỏ mất một phút. |
| "Mình nhớ yêu cầu rồi" | Bạn nhớ bản tóm tắt; sổ giữ nguyên văn. Đọc sổ. |
| "Test chắc pass" | Chưa chạy là chưa biết. Ghi "chưa chạy" chứ không ghi "pass". |
| "Gate chặn phiền, điền đại cho qua" | Sổ điền sai thành báo cáo sai gửi người dùng. Tệ hơn là không có gate. |
| "Luật vừa đổi chắc không liên quan" | Đọc diff rồi mới được kết luận. |
| "File quy tắc dài, đọc lướt phần đầu là đủ" | Luật quan trọng thường nằm ở cuối. Đọc tới dòng cuối. |
| "Làm gần giống rồi, coi như xong" | Gần giống là ⚠️, kèm chỗ khác. |
| "Người dùng đang vội" | Vội thì càng cần báo đúng cái gì chưa xong. |
| "Hook chặn nhầm, file đó không phải của mình" | Ghi đúng điều đó vào dòng Diff rồi chạy gate. |

## Dấu hiệu phải dừng lại

- Sắp viết "xong / đã sửa / hoàn thành / pass" mà chưa thấy `GATE OK` sau lần sửa cuối.
- Sửa file khi chưa đọc hết file quy tắc của project.
- Làm theo trí nhớ về yêu cầu thay vì mở sổ.
- Có `QUY TẮC ĐÃ ĐỔI` mà chưa đọc diff.
- Sửa sổ để gate qua, trong khi công việc không như sổ ghi.
- Tin nhắn mới có yêu cầu mà chưa có dòng R#.

Gặp một trong số đó: dừng, quay lại bước tương ứng ở trên.
