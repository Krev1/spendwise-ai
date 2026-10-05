# CSV validator và tổng hợp thu chi

- `csv_contract.py`: đọc CSV theo hợp đồng, kiểm tra từng dòng và tổng hợp theo tháng.
- `transactions_sample.csv`: 10 giao dịch hư cấu dùng để chạy thử và đối chiếu test.
- `test_csv_contract.py`: 14 test cho validation, Unicode, lọc tháng và số tiền.

Từ thư mục gốc dự án:

```powershell
.\.venv\Scripts\python.exe -B examples/csv_contract.py examples/transactions_sample.csv --month 2026-10
.\.venv\Scripts\python.exe -B -m pytest -q
```

File mẫu cho tháng 10: 9 giao dịch, thu 5.000.000, chi 2.593.000, chênh lệch 2.407.000 VND; một khoản chi chưa có nhãn. `can_xac_nhan` là nhóm preview cho khoản chi thiếu nhãn. Các tổng này không phải metric AI.

Code hiện tại chưa ghi SQLite, chưa có UI, AI, lịch sử sửa nhãn hoặc chống trùng giữa các lần import. Xem [thiết kế](../docs/02_design.md) cho các phần sẽ triển khai.

Giải thích và bài tập nằm ở [Learn/spendwise-ai](https://github.com/Krev1/Learn/tree/main/spendwise-ai). CSV luyện tập nằm trong repo Learn; CSV mẫu ở đây giữ ổn định cho test.
