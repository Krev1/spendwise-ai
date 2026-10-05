# SpendWise AI

[Repository dự án](https://github.com/Krev1/spendwise-ai) · [Bài học trong Learn](https://github.com/Krev1/Learn/tree/main/spendwise-ai)

Ứng dụng quản lý thu chi cá nhân cho sinh viên và người mới đi làm, tích hợp mô hình tự huấn luyện để phân loại mô tả khoản chi tiếng Việt. MVP nhập tay và CSV, chạy local trên CPU; ngân sách phí phần mềm/API thêm: 0 đồng.

## Trạng thái

Đang ở P1: môi trường Python riêng và dependency đã kiểm tra; ví dụ kiểm tra CSV/tính tiền có 14 test đạt. Chưa có ứng dụng hoàn chỉnh, dataset thật, mô hình đã huấn luyện hoặc kết quả ML. Các chỉ số trong spec là mục tiêu đề xuất.

Xem [tiến độ kỹ thuật](progress.md) và [bằng chứng kiểm tra](VERIFICATION.md). Cấu trúc `src/`, `tests/` và `artifacts/` trong thiết kế là đầu ra tương lai; mã hiện có nằm trong `examples/`.

## Tài liệu dự án

| Tài liệu | Nội dung |
|---|---|
| [Quyết định](DECISIONS.md) | Yêu cầu đã chốt và đề xuất cần kiểm chứng |
| [Đặc tả yêu cầu](docs/01_requirements.md) | Phạm vi, hành vi và tiêu chí chấp nhận |
| [Thiết kế](docs/02_design.md) | Kiến trúc, CSV, SQLite và pipeline ML |
| [Kế hoạch triển khai](docs/03_implementation_plan.md) | TASK, REQ, phụ thuộc và cách kiểm tra |
| [Nhóm và workflow](docs/04_team_workflow.md) | Vai trò và quy trình SDD |
| [Dữ liệu và ML](docs/05_data_and_ml.md) | Gán nhãn, split, train và đánh giá |
| [Chi phí và nguồn](docs/08_costs_and_sources.md) | Công cụ và điều kiện giữ ngân sách |
| [Prompt bắt đầu](prompts/START_HERE.md) | Giao việc theo spec và tiến độ hiện có |
| [Prompt vai trò](prompts/ROLE_PROMPTS.md) | Phân tích, phát triển và review |

## Cài đặt trên Windows

Repository công khai nên clone không cần đăng nhập; push cần quyền ghi của tài khoản GitHub.

```powershell
git clone https://github.com/Krev1/spendwise-ai.git
Set-Location -LiteralPath spendwise-ai
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock.txt
.\.venv\Scripts\python.exe -B scripts/check_environment.py
.\.venv\Scripts\python.exe -B -m pytest -q
```

Nếu đã có `.venv` của dự án, dùng interpreter đó. Lock đã được kiểm tra trên Windows 11/Python 3.14.7; môi trường khác cần xác minh tương thích.

## Chạy code hiện có

```powershell
.\.venv\Scripts\python.exe -B examples/csv_contract.py examples/transactions_sample.csv --month 2026-10
```

Xem [hướng dẫn code CSV](examples/README.md). Dữ liệu mẫu là hư cấu; ví dụ chưa có SQLite, UI hoặc AI và không phải dataset đánh giá mô hình.

## Bài học ở repo Learn

[Learn/spendwise-ai](https://github.com/Krev1/Learn/tree/main/spendwise-ai) chứa lộ trình, bài 00/01, CSV luyện tập, nhật ký và hướng dẫn bảo vệ. Xem [hướng dẫn dùng hai repo](https://github.com/Krev1/Learn/blob/main/spendwise-ai/README.md). Code tham chiếu ở repo dự án; bài học đọc trong Learn và chạy bằng `.venv` của dự án.

Tiếp tục task theo [kế hoạch](docs/03_implementation_plan.md), đối chiếu yêu cầu đồ án với giảng viên và giữ mọi kết quả thực nghiệm có bằng chứng. Không commit dữ liệu tài chính thật, database, credentials hoặc `.venv`.
