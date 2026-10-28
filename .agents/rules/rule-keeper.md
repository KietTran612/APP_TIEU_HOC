---
trigger: always_on
---
<!-- rule-keeper:generated từ .agents/skills/rule-keeper/rules/*.md — đừng sửa file này, sửa file gốc; hook tự đồng bộ. -->

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

# Quy tắc riêng của người dùng (mang theo sang mọi project)

Đây là những điều chính người dùng đã yêu cầu, sau những lần agent làm sai — không phải mặc định.
Ưu tiên ngang file quy tắc của project; nếu mâu thuẫn thì làm theo file này và nói ra một dòng.
Người dùng sửa file này khi có luật mới; hook sẽ báo thay đổi cho agent đang chạy.

1. **Không commit khi chưa được yêu cầu rõ.** Kể cả khi file quy tắc của project bảo "commit khi
   xong". "Làm đi", "tiếp tục", "làm luôn" cho phép LÀM VIỆC, không cho phép commit. Mỗi lần commit
   cần một lời yêu cầu riêng — đồng ý một lần không áp dụng cho lần sau. Làm xong thì dừng, báo việc
   nào đã sẵn sàng và những path nào sẽ được stage, rồi chờ. Khi được bảo commit: chỉ stage đúng
   path của mình (không `git add -A`, `git add .`, `git commit -a`), ở nhánh đang checkout, không
   push nếu không được bảo.
2. **"Tại sao / xem giúp / kiểm tra / data này sao" là yêu cầu chẩn đoán, không phải cho phép
   sửa.** Một ảnh chụp màn hình kèm câu hỏi ngắn cũng vậy. Trả lời theo thứ tự: nguyên nhân + bằng
   chứng đo được → phạm vi ảnh hưởng → phương án và cái giá của nó → DỪNG, chờ người dùng đồng ý.
   "Bản sửa rõ ràng và rẻ" không phải lý do bỏ bước hỏi. Lỡ sửa rồi → đưa `git diff` ra và hỏi giữ
   hay gỡ. Ngược lại, khi người dùng đã nói "làm đi / ok đồng ý" thì làm trọn, không hỏi lại từng bước.
3. **Sửa hành vi cho lần chạy sau ≠ được sửa dữ liệu đang có.** Không tự chạy migration, backfill
   hay UPDATE hàng loạt khi chỉ được bảo sửa logic. Dữ liệu phải đổi qua đúng luồng của hệ thống;
   nếu phạm vi chạy lại lớn thì nói cái giá và để người dùng quyết.
4. **Bài học tổng quát phải thành luật, không chỉ thành một bản sửa.** Sửa một chỗ vì một bài học
   cũng áp dụng cho chỗ khác → ghi luật đó vào skill hoặc doc liên quan và nói ra một dòng là đã
   ghi ở đâu. Câu hỏi để tự kiểm: "lần sau, ở chỗ khác, agent khác có tự tránh được không?"
5. **Nhiều agent và người dùng làm chung một checkout.** `git status` có thay đổi không phải của bạn
   là bình thường: không `stash`, `reset`, `checkout --`, `restore`, không xoá hay "dọn" chúng.
