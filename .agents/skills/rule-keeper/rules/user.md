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
