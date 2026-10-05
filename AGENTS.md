# SpendWise AI — hướng dẫn làm việc

- Đọc README.md, DECISIONS.md, progress.md và các tài liệu SDD liên quan trước khi sửa.
- Triển khai theo TASK/REQ; cập nhật yêu cầu và thiết kế khi hành vi thay đổi.
- Người học có tư duy lập trình cơ bản nhưng cần ôn code. Mỗi mốc phải có giải thích tiếng Việt, ví dụ, lệnh chạy, bài tập và câu hỏi tự trình bày.
- Chưa xác nhận người học hiểu bài nếu chưa có câu trả lời hoặc sản phẩm tự làm.
- Dùng Python trong `.venv`; không cài vào Python toàn hệ thống. Dependency thực đã kiểm tra nằm trong requirements.lock.txt.
- Ngân sách phí license/API/hosting thêm là 0 đồng. Không thêm API trả phí hoặc cloud bắt buộc.
- Không commit `.venv`, credentials, database, dữ liệu tài chính thật hoặc artifact chưa rà soát. Dữ liệu real chỉ dùng theo consent và quy trình trong docs/05_data_and_ml.md.
- Tổng tiền dùng int VND, AI chỉ gợi ý nhãn khoản chi và cần người dùng xác nhận.
- Không bịa metric, kết quả test, tiến độ hay phê duyệt của trường. Synthetic chỉ là minh họa/smoke test.
- Chạy kiểm tra phù hợp với thay đổi; báo rõ lệnh và kết quả. Ưu tiên task nhỏ để người học theo kịp.
- Nếu sử dụng nhiều vai trò/agent trong phạm vi được người dùng giao, phân định file sở hữu và tích hợp trước khi commit.
