# SpendWise AI — dự án đồ án Trí tuệ nhân tạo

Khởi động: 05/10/2026. Repository riêng tư: [Krev1/spendwise-ai](https://github.com/Krev1/spendwise-ai).

**Đề tài đề xuất:** Xây dựng ứng dụng quản lý thu chi cá nhân tích hợp mô hình học máy tự huấn luyện để phân loại mô tả khoản chi tiếng Việt.

Người dùng đầu tiên: sinh viên và người mới đi làm. Nhập giao dịch bằng tay hoặc CSV theo mẫu. Ngân sách phí phần mềm/API của MVP: 0 đồng, chạy trên máy sẵn có.

## Trạng thái hiện tại

Đã bắt đầu P1: tạo môi trường Python riêng, cài và kiểm tra dependency, chuẩn bị hướng dẫn học Git/Python, chạy ví dụ CSV và 14 test. Có bộ đặc tả, thiết kế, kế hoạch và tài liệu học. Chưa có ứng dụng hoàn chỉnh, dữ liệu thực đã thu thập, mô hình đã huấn luyện hay kết quả ML.

Các chỉ số chất lượng trong tài liệu là mục tiêu đề xuất; không phải kết quả đã đạt. Cấu trúc `src/`, `artifacts/` hoặc `tests/` được nhắc trong thiết kế là cấu trúc sẽ tạo khi triển khai. Thư mục `examples/` là ví dụ hiện có.

Xem [tiến độ](progress.md) và [bằng chứng kiểm tra](VERIFICATION.md). Ví dụ hiện có đã đạt 14 test trên môi trường kiểm tra của phiên này.

## Đọc theo thứ tự

| Thứ tự | File | Bạn sẽ hiểu được gì? |
|---|---|---|
| 0 | [DECISIONS.md](DECISIONS.md) | Điều gì đã được bạn chọn, điều gì đang là đề xuất |
| 1 | [Đặc tả yêu cầu](docs/01_requirements.md) | Người dùng, phạm vi, hành vi và tiêu chí chấp nhận |
| 2 | [Thiết kế](docs/02_design.md) | Luồng dữ liệu, kiến trúc, CSV, SQLite và mô hình |
| 3 | [Kế hoạch triển khai](docs/03_implementation_plan.md) | Các nhiệm vụ, phụ thuộc, đầu ra và cách kiểm tra |
| 4 | [Nhóm và workflow](docs/04_team_workflow.md) | Vai trò của bạn và các vai trò AI hỗ trợ |
| 5 | [Dữ liệu và học máy](docs/05_data_and_ml.md) | Gán nhãn, chống rò rỉ dữ liệu, huấn luyện và đánh giá |
| 6 | [Lộ trình vừa làm vừa học](docs/06_learning_path.md) | Bài học, bài tập, sản phẩm và câu hỏi tự giải thích |
| 7 | [Chuẩn bị bảo vệ](docs/07_defense_guide.md) | Cấu trúc báo cáo, bằng chứng và câu hỏi hội đồng |
| 8 | [Chi phí và nguồn](docs/08_costs_and_sources.md) | Điều kiện giữ phí phần mềm/API ở 0 đồng |
| 9 | [Prompt bắt đầu](prompts/START_HERE.md) | Nội dung có thể sao chép để giao việc cho AI |
| 10 | [Prompt theo vai trò](prompts/ROLE_PROMPTS.md) | Cách dùng riêng từng vai trò khi cần |

## Thử một bài học ngay trên Windows

Bắt đầu từ [buổi khởi động: GitHub và môi trường](docs/learning/00_git_and_environment.md), sau đó [buổi 1: chạy chương trình và hiểu thu–chi](docs/learning/01_python_and_money.md). Đã có bản sao CSV luyện tập để bạn tự sửa; nhật ký học để trống cho bạn điền khi thực hiện.

Mở PowerShell trong thư mục chứa README này:

```powershell
.\.venv\Scripts\python.exe -B scripts/check_environment.py
.\.venv\Scripts\python.exe -B examples/csv_contract.py examples/transactions_sample.csv --month 2026-10
.\.venv\Scripts\python.exe -B -m pytest -q
```

Ví dụ chỉ dùng thư viện chuẩn Python. File CSV chứa giao dịch **hư cấu**. Đây là minh họa nhập liệu, không phải dataset để báo cáo độ chính xác AI.

Đọc [hướng dẫn ví dụ](examples/README.md), sau đó thử đổi một số tiền thành `12.5` hoặc nhập trùng ID để quan sát thông báo lỗi.

## Bắt đầu dự án chính

Nếu tải dự án sang máy khác, đăng nhập Git bằng tài khoản có quyền repository rồi chạy:

```powershell
git clone https://github.com/Krev1/spendwise-ai.git
Set-Location -LiteralPath spendwise-ai
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock.txt
.\.venv\Scripts\python.exe -B scripts/check_environment.py
.\.venv\Scripts\python.exe -B -m pytest -q
```

Lock hiện được kiểm tra trên Windows 11, Python 3.14.7; tương thích ở môi trường khác cần được xác minh. Trên máy đã có `.venv` của dự án, dùng các lệnh kiểm tra/chạy ví dụ ở trên.

Tiếp tục theo [progress.md](progress.md) và [kế hoạch](docs/03_implementation_plan.md); prompt điều phối ở [START_HERE.md](prompts/START_HERE.md). Nhờ giảng viên xác nhận phạm vi nghiên cứu, cách đánh giá và yêu cầu báo cáo của trường trong khi học.

Bạn giữ vai trò chủ đồ án: thực hiện bài tập, hiểu code, quyết định nhãn và trình bày bằng chứng. AI hỗ trợ soạn, lập trình, giải thích và rà soát; các kết quả nghiên cứu phải đến từ lần chạy thực tế.
