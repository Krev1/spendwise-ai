# SpendWise AI

[Repository dự án](https://github.com/Krev1/spendwise-ai) · [Bài học trong Learn](https://github.com/Krev1/Learn/tree/main/spendwise-ai)

Ứng dụng quản lý thu chi cá nhân cho sinh viên và người mới đi làm, tích hợp mô hình tự huấn luyện để phân loại mô tả khoản chi tiếng Việt. MVP nhập tay và CSV, chạy local trên CPU; ngân sách phí phần mềm/API thêm: 0 đồng.

## Trạng thái

Đã chuẩn bị P1 và bắt đầu phần kỹ thuật P2: có domain giao dịch, CSV parser từ file/bytes, tổng hợp tháng và CLI preview. Bộ kiểm tra hiện tại đạt **86 tests, 11 subtests**; TASK-04 và phần kỹ thuật TASK-05–06 đang REVIEW. Có seed 356 mô tả hư cấu, nhãn AI dự thảo, chưa có người duyệt. Việc thực hành Python của người học vẫn chưa được xác nhận. Chưa có ứng dụng hoàn chỉnh, dataset thật, mô hình đã huấn luyện hoặc kết quả ML. Các chỉ số trong spec là mục tiêu đề xuất.

Xem [tiến độ kỹ thuật](progress.md) và [bằng chứng kiểm tra](VERIFICATION.md). Code hiện có nằm trong `src/spendwise/`, tests trong `tests/` và `examples/`. `examples/csv_contract.py` là wrapper của code mới. Các phần SQLite, UI, ML và `artifacts/` trong thiết kế vẫn là đầu ra tương lai.

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
.\.venv\Scripts\python.exe -B scripts/preview_transactions.py examples/transactions_sample.csv --month 2026-10
```

Xem [hướng dẫn code CSV](examples/README.md). Dữ liệu mẫu là hư cấu; ví dụ chưa có SQLite, UI hoặc AI và không phải dataset đánh giá mô hình.

## Bài học ở repo Learn

[Learn/spendwise-ai](https://github.com/Krev1/Learn/tree/main/spendwise-ai) chứa lộ trình, bài 00/01/02, bài tập, nhật ký và hướng dẫn bảo vệ. Xem [hướng dẫn dùng hai repo](https://github.com/Krev1/Learn/blob/main/spendwise-ai/README.md). Code tham chiếu ở repo dự án; bài học đọc trong Learn và chạy bằng `.venv` của dự án.

Tiếp tục task theo [kế hoạch](docs/03_implementation_plan.md), đối chiếu yêu cầu đồ án với giảng viên và giữ mọi kết quả thực nghiệm có bằng chứng. Không commit dữ liệu tài chính thật, database, credentials hoặc `.venv`.

## Dataset khởi đầu

[Dataset card](data/seed/v0.1/DATASET_CARD.md) và [CSV tiếng Việt](data/seed/v0.1/expense_descriptions_vi.csv): 356 mô tả, 8 nhãn, 0 mẫu thật. Có nguồn/commit/hash, provenance và audit từng dòng; toàn bộ nhãn chưa được con người kiểm tra độc lập. Dùng để học và thử pipeline; chưa chứng minh chất lượng thực tế.

```powershell
.\.venv\Scripts\python.exe -B scripts/build_seed_dataset.py
.\.venv\Scripts\python.exe -B scripts/validate_dataset.py data/seed/v0.1/expense_descriptions_vi.csv
```

[Phương pháp thu thập/xây dữ liệu](https://github.com/Krev1/Learn/blob/main/spendwise-ai/guides/01_dataset_collection.md), [guideline nhãn](https://github.com/Krev1/Learn/blob/main/spendwise-ai/guides/02_labeling_manual.md) và bài thực hành nằm trong Learn. Không commit mô tả thật hoặc sổ đồng ý; lưu riêng ở `data/private/`.

## Dự án và học hoạt động độc lập

Theo D13, chat dự án chỉ triển khai trong repo này và tiếp tục task đủ đầu vào, không chờ hoàn thành bài học. [Prompt dự án](prompts/START_HERE.md) và [bàn giao kỹ thuật](docs/PROJECT_HANDOFF.md) là điểm bắt đầu. Code/test/SDD/tiến độ kỹ thuật do luồng dự án quản lý.

Chat học dùng [prompt Mentor](https://github.com/Krev1/Learn/blob/main/spendwise-ai/MENTOR_PROMPT.md), đọc bàn giao/code theo commit và chỉ viết Learn/spendwise-ai. Người học thực hành trên checkout riêng; mức hiểu ghi ở Learn. [Quy trình hai luồng](docs/04_team_workflow.md) mô tả quyền ghi và cách đồng bộ.
