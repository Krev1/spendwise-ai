# Tiến độ ban đầu

Cập nhật: 05/10/2026. Đọc cùng [bằng chứng kiểm tra](VERIFICATION.md) và [kế hoạch](docs/03_implementation_plan.md).

| Mốc | Trạng thái | Bằng chứng hiện có / việc tiếp theo |
|---|---|---|
| P0 — Bộ SDD phiên bản 0.1 | Verified | Có bộ SDD, sổ quyết định và prompt; tài liệu học/bảo vệ được chuyển sang Learn; đã đối chiếu hợp đồng và liên kết. Đây là draft kỹ thuật, chưa phải phê duyệt đề tài của trường. |
| P1 — Môi trường app và ôn Python | In progress | TASK-02 phần kỹ thuật đã kiểm tra: `.venv`, import package, pip check, dependency lock. 14 test PASS trong môi trường này. Bài 00/01 và CSV luyện tập ở repo Learn. TASK-03 chờ người học tự thực hiện/giải thích. |
| P2 — Dữ liệu và baseline | In progress | TASK-04 phần kỹ thuật đã kiểm tra: domain, CSV file/bytes, reports, CLI; 50 tests và 11 subtests PASS. TASK-04 đang REVIEW; TASK-05–06 kỹ thuật đã có seed 356 câu hư cấu/0 thật, provenance và validator, tổng kiểm tra hiện tại 86 tests + 11 subtests. REVIEW nhãn do người và thu dữ liệu thật còn chờ; TASK-07 baseline chưa triển khai. |
| P3 — Huấn luyện và validation | Planned | Có seed hư cấu cho P2; chưa có split/artifact hoặc số đo mô hình. |
| P4 — SQLite và nghiệp vụ | Planned | Chưa có database hoặc services của ứng dụng. |
| P5 — Giao diện và tích hợp AI | Planned | Chưa có ứng dụng Streamlit. |
| P6 — Pilot, test cuối và bảo vệ | Planned | Chưa có kết quả test/pilot hoặc báo cáo đồ án hoàn chỉnh. |

Các task chi tiết dùng trạng thái trong tài liệu nhóm. `Verified` của một mốc chỉ áp dụng cho đầu ra được ghi ở cột bằng chứng; không có nghĩa người học đã hiểu hoặc giảng viên đã duyệt.

## Việc tiếp theo

1. Đọc [GitHub và môi trường Python](https://github.com/Krev1/Learn/blob/main/spendwise-ai/lessons/00_git_and_environment.md).
2. Người học thực hiện [buổi học đầu tiên](https://github.com/Krev1/Learn/blob/main/spendwise-ai/lessons/01_python_and_money.md): chạy ví dụ, sửa CSV luyện tập và giải thích kết quả. Sau đó đọc [bài 02 — CSV và validation](https://github.com/Krev1/Learn/blob/main/spendwise-ai/lessons/02_csv_and_labels.md), đối chiếu code mới; đọc [bài 02b — xây dữ liệu](https://github.com/Krev1/Learn/blob/main/spendwise-ai/lessons/02b_dataset_construction.md), tự rà 20 nhãn seed và chuẩn bị pilot thu thật theo template.
3. Người học xác minh rubric của trường; việc học và chuẩn bị môi trường vẫn tiếp tục được trong lúc bổ sung thông tin đó.

## Nhật ký cập nhật tiếp theo

Ghi ngày, TASK/REQ, file thay đổi, lệnh chạy, kết quả thực, kiến thức tự giải thích và việc còn lại. Giữ lịch sử thay vì thay mọi ô thành `Verified` khi chỉ mới tạo file.

## Khởi động GitHub — 05/10/2026

- Người học chọn tài khoản kết nối có ID `293179070`; username GitHub hiện hành `Krev1`.
- Repository lúc khởi tạo còn riêng tư: `https://github.com/Krev1/spendwise-ai`.
- Môi trường local Windows 11 Pro 64-bit, AMD Ryzen 5 7500F (6 core/12 thread), RAM khoảng 31,7 GiB hiển thị, Python 3.14.7.
- Import các dependency thành công; `pip check` không báo xung đột.
- pytest: 14 passed; unittest: 14 tests OK; CSV tháng 10 cho tổng đã ghi trong VERIFICATION.
- Chưa có câu trả lời/bài tự làm từ người học, chưa train mô hình hoặc đánh giá chất lượng AI.


## Tách bài học — 05/10/2026

- Theo D11/D12, bài học, lộ trình, hướng dẫn bảo vệ, bài tập và nhật ký học chuyển sang [Krev1/Learn](https://github.com/Krev1/Learn/tree/main/spendwise-ai).
- Repo dự án giữ code, test, SDD, dependency, prompt kỹ thuật và bằng chứng; cập nhật các tham chiếu sang Learn.
- Thay đổi này chỉ tổ chức tài liệu; trạng thái ứng dụng, dữ liệu và mô hình vẫn như bảng mốc ở trên.


## TASK-04 — Domain và CSV preview — 05/10/2026

- [Task card](docs/tasks/TASK-04.md) ghi phạm vi, REQ và tiêu chí chấp nhận; trạng thái REVIEW.
- Tách implementation sang `src/spendwise/domain/` và `src/spendwise/services/`; thêm CLI, API đọc bytes, test ranh giới hợp đồng và vị trí dòng CSV.
- Có bài 02/bài tập trong Learn. Chưa có bài tự làm hoặc câu trả lời từ người học; không đánh dấu TASK-03 DONE.
- Hướng dẫn tiếp theo: người học làm bài 01; phần kỹ thuật tiếp theo là TASK-05–06.

## TASK-05–06 — Dataset khởi đầu — 05/10/2026

- Thu snapshot 100 hàng hư cấu có MIT notice tại commit nguồn cố định; 19 mô tả được chuyển ngữ. 160 câu nền tự tạo, biến thể bỏ dấu giữ cùng nhóm.
- Seed v0.1: 356 mô tả, 33 nhóm, 0 thật, nhãn `ai_draft`; không có người duyệt độc lập. Có recipes, provenance, audit và source selection từng dòng.
- Builder tái tạo offline khớp byte; kiểm tra nguồn trực tuyến khớp hai hash. Test hiện tại 86 passed, 11 subtests passed; không sinh model/metric/split.
- [Task card](docs/tasks/TASK-05-06.md) đang REVIEW phần kỹ thuật. Learn có phương pháp, quy tắc nhãn, template trống và bài thực hành.
- Tiếp theo: người học rà 20 câu và giải thích, pilot thu thật riêng tư, gán nhãn độc lập. TASK-07 baseline tiếp tục sau khi hiểu hợp đồng; không chờ đủ 1.200 thật mới học kỹ thuật.
