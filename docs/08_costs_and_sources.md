# Chi phí, môi trường và nguồn tham khảo

## Giữ phí phần mềm/API của MVP ở 0 đồng

| Thành phần | Lựa chọn đề xuất | Chi phí và điều kiện |
|---|---|---|
| Máy chạy | Laptop/PC sẵn có, CPU | Chưa đánh giá cấu hình; không mua máy/GPU trong kế hoạch này |
| Ngôn ngữ | Python | Phần mềm miễn phí; dùng môi trường riêng của dự án |
| ML | scikit-learn, mô hình tự train | Chạy local, không cần API trả phí |
| Giao diện | Streamlit | Framework mã nguồn mở, chạy local |
| Lưu trữ | SQLite | File local; dùng module sqlite3 của Python |
| Dữ liệu | Mô tả tự viết để học; mô tả tự nguyện đã ẩn danh cho nghiên cứu | Không mua dữ liệu; phải ghi nguồn và quyền sử dụng |
| Quản lý phiên bản | Git local | Không cần mua dịch vụ để dùng Git local |
| Tài liệu | Markdown và biểu đồ Mermaid | Không cần phần mềm văn phòng trả phí |

“0 đồng” ở đây là không thêm phí license/API/hosting cho MVP trên máy bạn đã có. Điện, kết nối Internet và công cụ AI bạn đang dùng có thể có chi phí hoặc hạn mức riêng. Nhóm role AI không phải nhân sự được tuyển và không bảo đảm nền tảng AI miễn phí vô hạn.

MVP chạy local. Chỉ xem xét public hosting khi có nhu cầu cụ thể, đã kiểm tra điều khoản và hạn mức tại thời điểm triển khai. Nếu hết quota dịch vụ miễn phí, bản local vẫn là đường chạy chính. Không gắn thông tin thanh toán hoặc tự kích hoạt dịch vụ có phí.

## Môi trường khi triển khai

1. Kiểm tra Python đã cài, không đoán cấu hình RAM/GPU.
2. Tạo `.venv` trong dự án; không cài package vào môi trường Python toàn hệ thống.
3. Thử cài bộ thư viện cần thiết; ghi chính xác phiên bản cài và chạy được. Nếu phiên bản Python không tương thích, tạo môi trường phiên bản được tài liệu hiện hành hỗ trợ.
4. Sau lần chạy thành công, lưu file dependency có phiên bản để tái lập. Không điền phiên bản tưởng tượng vào báo cáo.
5. Các ví dụ hiện có trong `examples/` chỉ dùng thư viện chuẩn. Mô hình và giao diện sẽ được cài ở P1–P3.

PowerShell có thể chạy trực tiếp `.venv\Scripts\python.exe`; không cần thay chính sách thực thi toàn máy chỉ để activate môi trường.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install scikit-learn pandas streamlit joblib
.\.venv\Scripts\python.exe -m pip freeze > requirements.lock.txt
```

P1 đã tạo `.venv`, cài bộ thư viện, kiểm tra import, `pip check` và 14 test của ví dụ. Phiên bản thực được lưu ở `requirements.lock.txt`; xem VERIFICATION.md. Pipeline ML và app vẫn chưa được triển khai, nên lock hiện xác nhận môi trường khởi động, chưa xác nhận toàn bộ sản phẩm.

## Nguồn chính thức để học và kiểm chứng

| Chủ đề | Nguồn | Dùng để làm gì? |
|---|---|---|
| Ôn Python | [Python tutorial](https://docs.python.org/3/tutorial/) | Hàm, cấu trúc dữ liệu, exception, module |
| CSV | [Python csv](https://docs.python.org/3/library/csv.html) | Đọc/ghi dữ liệu có cột và dấu nháy |
| Database | [Python sqlite3](https://docs.python.org/3/library/sqlite3.html) | SQL có tham số và transaction |
| Giao diện | [Streamlit documentation](https://docs.streamlit.io/) | Framework và cách tạo app dữ liệu |
| Cài môi trường | [Streamlit installation](https://docs.streamlit.io/get-started/installation/command-line) | Phiên bản Python và hướng dẫn venv hiện hành |
| Đặc trưng văn bản | [TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) | API vector hóa |
| Phân loại | [LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html), [MultinomialNB](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html) | Tham số và API mô hình |
| Đối chiếu tối thiểu | [DummyClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html) | Kiểm tra có vượt được dự đoán đơn giản không |
| Chống leakage | [Common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html) | Fit tiền xử lý đúng tập dữ liệu |
| Chia theo nhóm | [Cross-validation guide](https://scikit-learn.org/stable/modules/cross_validation.html) | Thiết kế đánh giá với nhóm người/nguồn |
| Bài toán sản phẩm | [CFPB — Your Money, Your Goals](https://www.consumerfinance.gov/consumer-tools/educator-tools/your-money-your-goals/toolkit/) | Tham khảo nhu cầu theo dõi chi tiêu, không phải dataset tiếng Việt |

Ngày kiểm tra nguồn cho bộ khởi đầu: 05/10/2026. Khi trích báo cáo, ghi ngày truy cập và mô tả bạn đã sử dụng gì. Các tài liệu thư viện giúp dùng công cụ đúng; cơ sở nghiên cứu và related work của đồ án cần bổ sung bài báo phù hợp, đọc trực tiếp và không tự tạo trích dẫn.
