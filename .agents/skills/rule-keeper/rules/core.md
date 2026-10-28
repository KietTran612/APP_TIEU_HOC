# rule-keeper — luật nền (luôn áp dụng, mọi lượt, mọi project)

Phiên làm việc dài thì ngữ cảnh bị nén và bạn sẽ quên. Vì vậy trí nhớ của bạn KHÔNG nằm trong
cuộc chat mà nằm trong file:

- **Sổ yêu cầu** của phiên (`.agent-ledger/<agent>-<phiên>.md`): mọi yêu cầu của người dùng.
- **File quy tắc** của project (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.agents/rules/*.md`, …).

Hook rule-keeper báo đường dẫn sổ, tự chép nguyên văn từng tin nhắn của người dùng vào sổ, và báo
diff khi một file quy tắc đổi. Không có hook (không thấy dòng nào bắt đầu bằng `[rule-keeper]`):
chạy `node .agents/skills/rule-keeper/bin/rk.mjs start --agent <tên của bạn>` một lần ở đầu phiên và dùng sổ nó in ra.

**Làm sai chữ của luật là làm sai tinh thần của luật.**

## 1. Thứ tự ưu tiên

1. Tin nhắn mới nhất của người dùng.
2. Các yêu cầu trước đó của người dùng (mục "Yêu cầu" của sổ) — còn hiệu lực cho tới khi chính
   người dùng thay hoặc huỷ. Bạn không được tự coi một yêu cầu là đã hết hạn.
3. File quy tắc của project và `.agents/skills/rule-keeper/rules/user.md`.
4. Skill.
5. Thói quen mặc định của bạn.

Hai nguồn cùng cấp mâu thuẫn → làm theo cái CHẶT hơn và nói ra một dòng. Yêu cầu mới của người dùng
mâu thuẫn với quy tắc project → hỏi người dùng trước khi làm.

## 2. Ghi yêu cầu vào sổ — trước khi làm

Tin nhắn có yêu cầu, ràng buộc, sửa sai, "đừng…", "luôn…", "chỉ…", hay đổi ý → thêm dòng `R#` vào
mục "Yêu cầu" của sổ (trích nguyên văn + việc cụ thể phải đạt + `(M#)` là tin nhắn gốc), RỒI mới
làm. Yêu cầu bị thay → đánh dấu `[thay bởi R#]`, không xoá dòng cũ.

## 3. Đọc lại sổ — trước mỗi bước

Đọc lại mục "Yêu cầu" trước khi: bắt đầu sửa file, chạy lệnh có tác động (xoá, migrate, publish,
commit, push, gửi tin), và trước khi trả lời. Sau khi ngữ cảnh bị nén hoặc phiên được mở lại: đọc
lại TOÀN BỘ sổ và các file quy tắc — coi như bạn vừa quên hết.

## 4. File quy tắc

- Trước lần sửa file đầu tiên của phiên: đọc HẾT mọi file quy tắc mà hook liệt kê (hoặc
  `node .agents/skills/rule-keeper/bin/rk.mjs index`). File dài: đọc theo đoạn ≤ 250 dòng cho tới dòng cuối. Output bị
  cắt KHÔNG phải là cả file.
- Thấy "QUY TẮC ĐÃ ĐỔI": đọc diff → áp dụng ngay cho phần việc còn lại → rà lại phần đã làm theo
  luật mới. Không có hook → chạy `node .agents/skills/rule-keeper/bin/rk.mjs check --ledger <sổ>` ở đầu mỗi lượt.

## 5. Không báo "xong" khi chưa qua done-gate

Trước mọi câu kiểu "xong / đã sửa / hoàn thành / chạy được rồi / tests pass / sẵn sàng": làm
done-gate theo skill **rule-keeper** (`.agents/skills/rule-keeper/SKILL.md`) và chạy
`node .agents/skills/rule-keeper/bin/rk.mjs gate --ledger <sổ>` cho tới khi nó in `GATE OK`. Câu trả lời cuối nói rõ:
việc đã làm (kèm bằng chứng ngắn), việc chưa xong, điều chưa kiểm chứng.

## 6. Phạm vi

Làm đúng cái được yêu cầu, không mở rộng sang việc không ai giao. Không xoá, revert hay ghi đè việc
không phải của bạn. Không chắc người dùng muốn gì → hỏi, đừng đoán rồi làm.
