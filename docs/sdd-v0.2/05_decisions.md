# 05 — Quyết định và phần chưa biết

Ngày: 06/10/2026. Câu trả lời của chủ đồ án không thay phê duyệt từ trường.

## Đã được chủ đồ án xác nhận

| ID | Quyết định | Căn cứ |
|---|---|---|
| D14 | Ưu tiên kiểm soát ngân sách, nhắc gần/vượt | Vòng mục tiêu câu1 C |
| D15 | Công khai nhiều người đăng ký/dùng | Vòng mục tiêu câu2 C |
| D16 | Website máy tính và điện thoại | Vòng nền tảng câu1 A |
| D17 | Ngân sách tháng tổng và từng nhóm | Vòng nền tảng câu2 C |
| D18 | Cảnh báo thực tế và dự báo cuối tháng | Vòng nền tảng câu3 C |
| D19 | Bắt buộc Deep Learning | Vòng AI câu1 B; rubric chi tiết chưa có |
| D20 | Chưa có lịch sử chi tiêu bản thân, cần bắt đầu thu | Vòng AI câu2 C; không phủ nhận seed/nguồn tham khảo đã có |
| D21 | Windows, RAM 32 GB, RTX 3080 10 GB, làm một mình | Vòng nguồn lực; user báo, CUDA chưa smoke |
| D22 | Chưa deadline hoặc giờ/tuần cố định | Hai vòng làm rõ; không tự gán10–12 tuần |

D01…13 về hai nhóm người dùng/manual/CSV/tự train/0 đồng/hai repo vẫn hiệu lực ở phần không xung đột. Nhóm vai trò AI không đồng nghĩa có thêm nhân sự; dữ liệu/nhãn người duyệt vẫn cần con người thật.

## Thiết kế đề xuất để tiến triển

- Django templates/PostgreSQL/allauth thay mục tiêu single-user local; email xác minh/reset, in-app alerts.
- Char-CNN PyTorch train từ đầu là neural bắt buộc; traditional ML giữ baseline.
- Pace-v1 là forecast có công thức, không neural thứ hai; đối chiếu rubric thật trước khóa nghiên cứu.
- VND/tiếng Việt/Asia Ho Chi Minh; tám nhãn tạm giữ, khóa sau pilot; cảnh báo80% / 100%.
- Dự báo từ ≥ 7 ngày đã kết thúc và user xác nhận ghi đủ; thiếu trả null/reason.
- Python3.12 chỉ là ứng viên env mới; provider chưa chọn, không đảm bảo free tier/unlimited.

Đây không phải các chi tiết user đã tự chọn. Thay ADR có lý do/tác động REQ/TASK/dataset/model và kiểm tra. Không cần xác nhận hình thức từng file cho công việc thường lệ đã giao.

## Chưa biết / thời điểm cần giải quyết

| Nội dung | Ai / mốc cần | Có thể làm độc lập |
|---|---|---|
| Rubric neural/train-from-scratch/fine-tune/report | Chủ đồ án hỏi giảng viên trước khóa nghiên cứu | Web/core/annotation/neural smoke |
| Người tự nguyện và annotator độc lập | Chủ đồ án, task08/09 | Web/seed smoke; real nghiên cứu pending |
| Driver/wheel/VRAM/latency thật | Task02 | Budget pure task03 |
| Host/DB/SMTP0 đồng có durability/backup/quota | Task15 trước public | Local; public chưa Verified |
| Giờ tuần/deadline | Chủ đồ án khi có lịch | Theo mốc |
| Chính sách dữ liệu áp dụng khi vận hành thật | Trước public theo vùng/người dùng | Thiết kế minimization/consent/delete; chưa xác nhận tuân thủ pháp lý |
| Chất lượng neural/forecast/usefulness | Thí nghiệm/pilot thật | Không bịa metric hoặc coi mục tiêu là kết quả |

## Trạng thái lượt này

Chỉ viết tài liệu/prompt v0.2 và kiểm tra tĩnh. Mọi SW-TASK mới Planned; chưa cài stack mới, code web/neural, thu mẫu Việt thực mới, train hoặc deploy. Mức hiểu học viên chưa có bằng chứng tự làm mới.
