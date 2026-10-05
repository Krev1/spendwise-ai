# Kiểm tra bộ SDD v0.2 — 06/10/2026

Phạm vi: đặc tả, thiết kế, kế hoạch, tài liệu thí nghiệm và prompt. Không đổi runtime code/dependency/model trong lượt này.

| Kiểm tra | Kết quả |
|---|---|
| UTF-8 và code fence Markdown | PASS |
| Link file nội bộ và giữa hai repo đối chiếu với cây local | PASS, 144 link trong tập tài liệu đã thay |
| SW-REQ có SW-TASK tương ứng | PASS, 14 yêu cầu / 16 task |
| Namespace mới và trạng thái | SW-TASK đều Planned, REQ/TASK v0.1 giữ lịch sử |
| Work đang sửa ở hai checkout ban đầu | Không chỉnh sửa; đối chiếu inventory/hash PASS |
| Git staged diff whitespace | Kiểm tra bằng `git diff --cached --check` trước publish |

Lệnh kiểm tra tĩnh: `python work/check_public_sdd.py` từ workspace soạn tài liệu. Script scratch không phải dependency runtime hoặc test suite của sản phẩm. Báo cáo kiểm tra tĩnh không chứng minh app an toàn hoặc model tốt.

Không chạy lại tests runtime vì chỉ sửa tài liệu/prompt. Chưa cài stack Django/PyTorch mới, chưa neural train, thu nhãn Việt thật mới hoặc deploy public. Các số test/mốc v0.1 được giữ theo evidence cũ, không gán cho tính năng v0.2. Cấu hình Windows/RAM32GB/3080 10GB do user báo; CUDA/VRAM/latency mới còn cần SW-TASK-02.

Tài liệu chuẩn được đọc để chọn thiết kế và điều kiện kiểm tra: Django auth/deployment/email, django-allauth requirements/configuration, PyTorch installation/Conv1d/reproducibility; link và giới hạn nằm ở thiết kế. Provider hosting/DB/email chưa chọn, không có cam kết free tier hoặc capacity.
