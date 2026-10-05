# Tiến độ ban đầu

Cập nhật: 05/10/2026. Đọc cùng [bằng chứng kiểm tra](VERIFICATION.md) và [kế hoạch](docs/03_implementation_plan.md).

| Mốc | Trạng thái | Bằng chứng hiện có / việc tiếp theo |
|---|---|---|
| P0 — Bộ SDD phiên bản 0.1 | Verified | Có bộ SDD, sổ quyết định và prompt; tài liệu học/bảo vệ được chuyển sang Learn; đã đối chiếu hợp đồng và liên kết. Đây là draft kỹ thuật, chưa phải phê duyệt đề tài của trường. |
| P1 — Môi trường app và ôn Python | In progress | TASK-02 phần kỹ thuật đã kiểm tra: `.venv`, import package, pip check, dependency lock. 14 test PASS trong môi trường này. Bài 00/01 và CSV luyện tập ở repo Learn. TASK-03 chờ người học tự thực hiện/giải thích. |
| P2 — Dữ liệu và baseline | Planned | Chưa thu dữ liệu thật, chưa có baseline đã chạy. |
| P3 — Huấn luyện và validation | Planned | Chưa có dataset/split/artifact và chưa có số đo mô hình. |
| P4 — SQLite và nghiệp vụ | Planned | Chưa có database hoặc services của ứng dụng. |
| P5 — Giao diện và tích hợp AI | Planned | Chưa có ứng dụng Streamlit. |
| P6 — Pilot, test cuối và bảo vệ | Planned | Chưa có kết quả test/pilot hoặc báo cáo đồ án hoàn chỉnh. |

Các task chi tiết dùng trạng thái trong tài liệu nhóm. `Verified` của một mốc chỉ áp dụng cho đầu ra được ghi ở cột bằng chứng; không có nghĩa người học đã hiểu hoặc giảng viên đã duyệt.

## Việc tiếp theo

1. Đọc [GitHub và môi trường Python](https://github.com/Krev1/Learn/blob/main/spendwise-ai/lessons/00_git_and_environment.md).
2. Người học thực hiện [buổi học đầu tiên](https://github.com/Krev1/Learn/blob/main/spendwise-ai/lessons/01_python_and_money.md): chạy ví dụ, sửa CSV luyện tập và giải thích kết quả. Sau đó Mentor hỗ trợ ôn hàm/list/dict; tiếp tục P2 theo kế hoạch.
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
