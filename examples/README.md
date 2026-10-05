# CSV validator và tổng hợp thu chi

- `csv_contract.py`: wrapper tương thích, gọi domain/services trong `src/spendwise/`.
- `transactions_sample.csv`: 10 giao dịch hư cấu dùng để chạy thử và đối chiếu test.
- `test_csv_contract.py`: 14 test giữ hợp đồng và lệnh cũ; mốc TASK-04 đạt 50 tests và 11 subtests. Bộ kiểm tra đầy đủ hiện tại đạt 139 tests và 11 subtests, gồm dataset/baseline.

Từ thư mục gốc dự án:

```powershell
.\.venv\Scripts\python.exe -B examples/csv_contract.py examples/transactions_sample.csv --month 2026-10
.\.venv\Scripts\python.exe -B -m pytest -q
```

File mẫu cho tháng 10: 9 giao dịch, thu 5.000.000, chi 2.593.000, chênh lệch 2.407.000 VND; một khoản chi chưa có nhãn. `can_xac_nhan` là nhóm preview cho khoản chi thiếu nhãn. Các tổng này không phải metric AI.

CSV parser hiện tại chưa ghi SQLite, chưa có UI, gợi ý AI trong app, lịch sử sửa nhãn hoặc chống trùng giữa các lần import. Xem [thiết kế](../docs/02_design.md) cho các phần sẽ triển khai.

## Demo baseline riêng — TASK-07

`baseline_demo.json` là fixture `author_synthetic`, nhãn AI dự thảo: 10 ví dụ fit có 8 nhãn, 13 câu probe không có nhãn đánh giá. Fixture khác CSV giao dịch và dataset nghiên cứu sáu cột. B0 luôn chọn lớp phổ biến trong fixture (`an_uong`, 3 ví dụ); không học quan hệ mô tả/nhãn. B1 dùng keyword có version/hash, cụm chứa keyword chung và xung đột có kết quả truy vết.

```powershell
.\.venv\Scripts\python.exe -B scripts/demo_baselines.py
```

Lệnh chỉ in JSON, không sửa fixture hoặc tạo model/database/split/metric. `cơm trưa và vé phim` trả `khac/conflict`; `endgame` không khớp `game`; `thuốc lá` khớp rule `khac` khác với fallback không keyword. Alias không dấu được khai báo rõ; chưa bao phủ mọi cách viết. B1 không hiểu ngữ nghĩa hoặc nhận diện mọi dữ liệu ngoài miền. Không coi demo là bằng chứng AI với người thật. [Task card](../docs/tasks/TASK-07.md) và [bằng chứng](../VERIFICATION.md) ghi phạm vi đã kiểm tra.

Giải thích và bài tập nằm ở [Learn/spendwise-ai](https://github.com/Krev1/Learn/tree/main/spendwise-ai). CSV luyện tập nằm trong repo Learn; CSV mẫu ở đây giữ ổn định cho test.
