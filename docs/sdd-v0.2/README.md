# SpendWise AI — SDD v0.2: ngân sách, web công khai và Deep Learning

Ngày: 06/10/2026. Trạng thái: đặc tả hướng phát triển; chưa triển khai các tính năng mới.

**Mục tiêu:** giúp sinh viên và người mới đi làm theo dõi ngân sách tháng, nhận cảnh báo theo số tiền đã ghi và ước tính nguy cơ vượt ngân sách cuối tháng; dùng được trên trình duyệt máy tính/điện thoại, có đăng ký tài khoản. Đồ án có mô hình Deep Learning phân loại khoản chi tiếng Việt do sinh viên tự huấn luyện.

## Đọc và thực hiện theo thứ tự

| Bước | Tài liệu | Đầu ra |
|---|---|---|
| 1. Đặc tả yêu cầu | [01_requirements.md](01_requirements.md) | Hành vi và tiêu chí chấp nhận SW-REQ-01…14 |
| 2. Thiết kế | [02_design.md](02_design.md) | Kiến trúc web, dữ liệu, ngân sách, dự báo và mô hình |
| 3. Dữ liệu và thí nghiệm | [04_data_and_experiments.md](04_data_and_experiments.md) | Quy trình thu thập, gán nhãn, split và đánh giá |
| 4. Kế hoạch triển khai | [03_implementation_plan.md](03_implementation_plan.md) | SW-TASK-01…16, phụ thuộc và bằng chứng |
| 5. Quyết định và phần chưa biết | [05_decisions.md](05_decisions.md) | Phân biệt yêu cầu đã chốt với lựa chọn kỹ thuật đề xuất |
| 6. Bắt đầu code | [Prompt dự án](../../prompts/START_HERE.md) | Đọc trạng thái thật, làm SW-TASK-01 trước |

## Quyền ưu tiên và cách kế thừa

V0.2 là đặc tả hiện hành cho **phạm vi mới**: web nhiều tài khoản, ngân sách/cảnh báo/dự báo, Deep Learning và nguồn lực GPU. Nó thay các giả định local một người, chỉ CPU, không có tài khoản và chỉ ML truyền thống trong v0.1. Những hợp đồng không đổi về tiền/CSV/8 nhãn/xác nhận và quyền dữ liệu vẫn được kế thừa, ghi rõ lại ở v0.2. Không dùng hai bản để chọn tùy ý hành vi thuận tiện.

Các tài liệu v0.1, REQ-01…13 và TASK-01…24 được giữ để truy vết code/bằng chứng cũ. Namespace mới `SW-REQ-*` / `SW-TASK-*` tránh đánh dấu task cũ DONE khi chưa làm chức năng mới. Bảng chuyển tiếp nằm trong kế hoạch.

Snapshot code đã công bố dùng làm điểm xuất phát: `1af601f813f42171e61ef36238f3f84db3178551`. Có domain/CSV/reports, seed 356 mô tả hư cấu, baseline và split prototype. **Không có dữ liệu Việt thật đủ điều kiện nghiên cứu, model Deep Learning đã train hoặc website công khai đã kiểm chứng.** Split seed cũ thiếu lớp ở validation/test; chỉ dùng thử pipeline, không dùng làm kết luận tám lớp.

Ngày soạn, checkout đang làm việc còn có thay đổi chưa commit về feature TF-IDF/demo Streamlit và MoneyVis; Learn có hướng dẫn dữ liệu đang sửa. Bản SDD được tạo ở checkout riêng, không sửa/đưa những thay đổi đó vào commit này. Lần triển khai phải đọc lại HEAD/status/handoff thực tế và tích hợp theo phạm vi; không reset, xóa demo hoặc làm lại phần đã kiểm chứng.

## Hai luồng độc lập

Dự án viết code/test/dataset được phép chia sẻ/SDD/bằng chứng trong `Krev1/spendwise-ai`. Mentor viết bài học, bài tập và nhật ký trong [Learn](https://github.com/Krev1/Learn/tree/main/spendwise-ai). Học dựa vào commit thực tế; không coi việc có thiết kế là tính năng đã được code. Không yêu cầu hoàn thành bài học mới cho phép task kỹ thuật đủ đầu vào chạy.

Mỗi task đi qua **REQ → thiết kế → TASK → code → kiểm tra → evidence → bàn giao**. Chưa có deadline hoặc giờ/tuần cố định; tiến độ theo kết quả, không cam kết lịch giả.
