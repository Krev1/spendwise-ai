# SpendWise AI — hướng dẫn làm việc

- Phạm vi hiện hành: `docs/sdd-v0.2/README.md` và tài liệu liên kết, ưu tiên web nhiều tài khoản/ngân sách/dự báo/Deep Learning/GPU. `prompts/START_HERE.md` đã đổi. REQ/TASK cũ giữ truy vết; không reset code hoặc ghi DONE SW-TASK chưa chạy.


- Đọc README.md, DECISIONS.md, progress.md và các tài liệu SDD liên quan trước khi sửa.
- Triển khai theo TASK/REQ; cập nhật yêu cầu và thiết kế khi hành vi thay đổi.
- Repo Krev1/spendwise-ai giữ code, test và tài liệu SDD. Bài học, bài tập, nhật ký và hướng dẫn bảo vệ phải lưu ở Krev1/Learn, thư mục spendwise-ai; không tạo docs/learning trong repo dự án. Mỗi lesson ghi TASK/REQ và commit code tham chiếu.
- Theo D13, luồng dự án triển khai độc lập với luồng học. Chỉ sửa repo spendwise-ai; đọc Learn nếu cần nhưng không viết bài học/nhật ký ở đó trong vai trò dự án. Mỗi mốc cập nhật docs/PROJECT_HANDOFF.md: TASK/REQ, code, lý do thiết kế, lệnh, bằng chứng và giới hạn để Mentor tạo bài học riêng.
- Chưa xác nhận người học hiểu bài nếu chưa có câu trả lời hoặc sản phẩm tự làm.
- Dùng Python trong `.venv`; không cài vào Python toàn hệ thống. Dependency thực đã kiểm tra nằm trong requirements.lock.txt.
- Ngân sách phí license/API/hosting thêm là 0 đồng. Không thêm API trả phí hoặc cloud bắt buộc.
- Không commit `.venv`, credentials, database, dữ liệu tài chính thật hoặc artifact chưa rà soát. Dữ liệu real chỉ dùng theo consent và quy trình trong docs/05_data_and_ml.md.
- Tổng tiền dùng int VND, AI chỉ gợi ý nhãn khoản chi và cần người dùng xác nhận.
- Không bịa metric, kết quả test, tiến độ hay phê duyệt của trường. Synthetic chỉ là minh họa/smoke test.
- Chạy kiểm tra phù hợp với thay đổi; báo rõ lệnh và kết quả. Chia task để review được; không chờ người học hoàn thành bài mới triển khai task kỹ thuật đủ đầu vào. Quyền dữ liệu, nhãn người duyệt và phê duyệt phạm vi vẫn cần bằng chứng thật.
- Nếu sử dụng nhiều vai trò/agent trong phạm vi được người dùng giao, phân định file sở hữu và tích hợp trước khi commit.

- Tiến độ dự án trong progress.md chỉ phản ánh kỹ thuật. Mức hiểu/bài tự làm được ghi riêng trong Learn/spendwise-ai/progress.md; không lấy một bên làm bằng chứng cho bên kia.
- Prompt triển khai: prompts/START_HERE.md. Mentor ở chat học dùng Learn/spendwise-ai/MENTOR_PROMPT.md, đọc code theo commit và thực hành trong checkout riêng. Không điều khiển tiến độ bằng việc gửi tin nhắn sang chat khác; cập nhật file bàn giao cho người dùng/Mentor đọc.
