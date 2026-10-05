# Sổ quyết định — phiên bản 0.1

Ngày: 05/10/2026. Dùng file này để tránh biến một đề xuất kỹ thuật thành yêu cầu đã được xác nhận.

## Đã được người dùng xác nhận

| ID | Quyết định | Căn cứ |
|---|---|---|
| D01 | Làm sản phẩm giải quyết nhu cầu thực tế và phục vụ đồ án tốt nghiệp | Câu trả lời vòng 1 |
| D02 | Lĩnh vực tài chính, chọn trợ lý quản lý chi tiêu cá nhân | Chọn phương án A |
| D03 | Người dùng đầu tiên gồm sinh viên và người mới đi làm | Trả lời vòng 2: nhóm 1 và 2 |
| D04 | MVP nhập tay và nhập CSV theo mẫu | Trả lời vòng 2 |
| D05 | AI chính: phân loại mô tả khoản chi tiếng Việt | Trả lời vòng 2 |
| D06 | Cần tự huấn luyện mô hình, ngành học Trí tuệ nhân tạo | Thông tin học tập |
| D07 | Ngân sách hiện tại 0 đồng; cần kế hoạch dùng công cụ miễn phí | Ràng buộc người dùng |
| D08 | Có nhiều thời gian; chưa có hạn nộp hoặc số giờ/tuần cụ thể | Thông tin thời gian |
| D09 | Cần nhóm với vai trò khác nhau và tài liệu giải thích để học, bảo vệ | Yêu cầu người dùng |
| D10 | Có tư duy lập trình cơ bản nhưng cần ôn kỹ thuật code | Thông tin năng lực |

## Đề xuất kỹ thuật cho bản khởi đầu

| ID | Đề xuất/giả định | Cách kiểm chứng hoặc thay đổi |
|---|---|---|
| A01 | Tên tạm SpendWise AI | Có thể đổi tên, giữ nguyên mục tiêu |
| A02 | MVP local, một người dùng trên mỗi bản cài; máy có CPU và quyền cài Python | P1 kiểm tra máy; chưa giả định RAM/GPU cụ thể |
| A03 | Python + Streamlit + SQLite + scikit-learn | P1 kiểm tra phiên bản tương thích, khóa dependency sau lần cài thành công |
| A04 | 8 danh mục khoản chi | Pilot với 3–5 người; nếu thay nhãn phải cập nhật dataset, spec và model version |
| A05 | Baseline từ khóa và DummyClassifier; thử TF-IDF + Naive Bayes, Logistic Regression | Đánh giá cùng split và bộ nhãn, chọn bằng validation |
| A06 | Ngưỡng điểm mô hình khởi đầu 0.60 | Chọn trên validation, ghi coverage và sai số; không gọi là xác suất dự đoán đúng |
| A07 | Mục tiêu nghiên cứu ban đầu: macro-F1 ≥0.80; coverage ≥0.60; selective accuracy ≥0.85 | Chưa đo; thảo luận lại dựa trên pilot, dữ liệu và rubric trước khi khóa test |
| A08 | Mục tiêu thu thập khoảng 1.200 mô tả, khoảng 150/lớp; test thực tối thiểu 20 mô tả khác nhau/lớp | Phụ thuộc quyền dữ liệu, người tham gia và phân bố; không nhân bản mẫu để đủ số |
| A09 | Lộ trình tham khảo khoảng 10–12 tuần | Chạy theo mốc, kéo dài hoặc rút gọn sau P1; không phải cam kết thời hạn |
| A10 | “Nhóm” là các vai trò hỗ trợ AI cộng với bạn là chủ đồ án | Có thể phân vai cho người thật nếu bạn có nhóm; chưa tuyển hoặc liên hệ ai |

P1 đã kiểm tra môi trường local: Windows 11 Pro 64-bit, Ryzen 5 7500F, RAM khoảng 31,7 GiB hiển thị, Python 3.14.7. Bộ thư viện trong requirements.lock.txt import được và ví dụ đạt 14 test. Đây là xác minh setup; chưa đo tốc độ train/inference hoặc độ chính xác AI.

Người học đã chọn tài khoản GitHub kết nối thứ hai. GitHub xác nhận ID `293179070`, username hiện hành `Krev1`. Repository riêng tư `Krev1/spendwise-ai` được tạo cho dự án.

## Hợp đồng chung giữa các tài liệu

- **Danh mục khoản chi:** `an_uong`, `di_chuyen`, `nha_o_hoa_don`, `hoc_tap`, `mua_sam`, `giai_tri`, `suc_khoe`, `khac`.
- **CSV giao dịch:** `transaction_id,date,transaction_type,amount_vnd,description,category`.
- `transaction_type`: `income` hoặc `expense`; `amount_vnd` là số nguyên dương VND, tối đa `1_000_000_000_000`; ngày `YYYY-MM-DD`.
- Khoản thu có `category` trống. Khoản chi có thể chưa có nhãn khi nhập, nhưng phải có nhãn được người dùng xác nhận trước khi lưu.
- Gợi ý AI luôn cần xác nhận. Nhãn `khac` không đồng nghĩa mô hình đã nhận biết được mọi đầu vào ngoài miền.
- **Dataset nghiên cứu riêng:** `record_id,description,label,group_id,source,is_synthetic`; không lấy số tiền hoặc thu nhập làm đầu vào mô hình phân loại văn bản.
- CSV hợp lệ tối đa 5.000 dòng dữ liệu, 2.000.000 byte; ID ổn định dài 1–64 ký tự chữ ASCII, số, `_`, `-`; mô tả 1–300 ký tự sau loại khoảng trắng ở đầu/cuối.
- Import lại so `source_payload_hash` của input canonical trước AI/xác nhận; không so nhãn hiện tại sau người dùng sửa. Cùng ID/cùng nguồn thì bỏ qua; cùng ID/nguồn khác thì từ chối toàn batch.
- Các danh mục, giới hạn dữ liệu và mục tiêu chất lượng trên là thiết kế đề xuất, có thể sửa có ghi lý do.

## Thông tin cần bổ sung khi làm

1. Rubric, format báo cáo và yêu cầu thí nghiệm của giảng viên/trường.
2. CPU, RAM, dung lượng đĩa và giờ học mỗi tuần.
3. Người tự nguyện thử ứng dụng và cung cấp mô tả đã ẩn danh.
4. Kết quả pilot: người dùng có tiết kiệm thời gian phân loại không, nhãn nào khó phân biệt?

Các thông tin này không ngăn việc ôn Python, tạo môi trường và thử định dạng CSV. Khi ảnh hưởng đến phạm vi, cập nhật đúng tài liệu liên quan trước khi viết phần code phụ thuộc.

## Mẫu ghi thay đổi

```text
Ngày:
Quyết định cũ:
Quyết định mới:
Lý do và bằng chứng:
REQ / TASK / dataset / model bị ảnh hưởng:
Ai quyết định:
Cách kiểm tra sau thay đổi:
```
