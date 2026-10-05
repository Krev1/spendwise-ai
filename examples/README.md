# Bài học nhỏ: kiểm tra CSV và tổng tiền

Các file ở đây đã được tạo trong bộ khởi đầu:

- `csv_contract.py`: đọc CSV chuẩn, kiểm tra từng giao dịch và tổng hợp theo tháng.
- `transactions_sample.csv`: 10 giao dịch hư cấu, không chứa dữ liệu người thật.
- `test_csv_contract.py`: kiểm tra các trường hợp lỗi có thể làm sai tiền hoặc dữ liệu.

Ví dụ này chưa có SQLite, UI, AI, lịch sử chỉnh nhãn hoặc cơ chế reimport vào database. ID trùng chỉ được phát hiện trong file đang đọc. Đọc thiết kế để triển khai những phần còn lại.

## Chạy

```powershell
python examples/csv_contract.py examples/transactions_sample.csv --month 2026-10
python -m unittest discover -s examples -p "test_*.py" -v
```

Kết quả tháng 10 của file gốc: thu `5.000.000`, chi `2.593.000`, chênh lệch `2.407.000` VND. Có một khoản chi chưa có nhãn. Con số này được tính từ giao dịch hư cấu, không phải metric AI. Tổng theo category dùng `can_xac_nhan` cho dòng thiếu nhãn, chỉ để preview.

## Bài tập

1. Thêm giao dịch chi 45.000 VND với ID mới; dự đoán tổng trước khi chạy.
2. Đổi ngày sang `2026-02-30`; đọc lỗi và tìm hàm kiểm tra ngày.
3. Nhập ID trùng; giải thích ảnh hưởng nếu hệ thống bỏ qua lỗi này.
4. Sửa hàm tổng hợp để hiển thị tỷ trọng từng danh mục; xử lý tháng không có khoản chi.
5. Giải thích vì sao mô hình dự đoán nhãn không được quyết định cách cộng số tiền.

Tạo bản sao file CSV trước khi sửa. Ghi câu trả lời của bạn trong file lesson tương ứng khi bắt đầu triển khai.
