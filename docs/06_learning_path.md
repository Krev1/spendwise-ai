# Lộ trình vừa làm vừa học

Mỗi mốc có bốn đầu ra: code chạy được, giải thích bằng tiếng Việt, một bài tập bạn tự sửa và bằng chứng kiểm tra. Không đánh dấu “đã hiểu” chỉ vì chạy được lệnh.

## Cách học trong một buổi

1. Đọc mục tiêu và dự đoán chương trình sẽ làm gì.
2. Chạy ví dụ nhỏ, quan sát đầu vào/đầu ra.
3. Tự thay đổi một yêu cầu hoặc một trường hợp lỗi.
4. Viết lại lời giải thích bằng cách nói của bạn, kèm kết quả chạy.
5. Nhờ Mentor kiểm tra giải thích và chỉ ra chỗ còn nhầm.

Bạn có thể bắt đầu bằng buổi 45–90 phút. Đây là gợi ý tổ chức, không phải yêu cầu thời gian của dự án.

## Bài 1 — Python và tiền VND

**Liên quan:** P1, REQ nhập liệu và tổng hợp thu chi.

Ôn biến, chuỗi, list, dict, hàm, điều kiện, vòng lặp, exception và module. Dùng `int` cho VND nguyên trong phạm vi MVP. `10000 + 25000` có kết quả `35000`; không cần mô hình học máy để tính tổng.

Chạy `examples/csv_contract.py`. Tìm hàm `parse_amount` và giải thích vì sao kiểm tra chuỗi trước khi chuyển thành số. Tìm hàm `summarize` và giải thích tại sao thu và chi không cộng chung.

**Tự làm:** thêm một khoản chi học tập 45.000 đồng trong tháng 10, dự đoán tổng trước khi chạy. Đổi nó thành `-45000` và giải thích vì sao bị từ chối. Viết hàm `net_cashflow(total_income, total_expense)`.

**Tự trả lời:** kiểu dữ liệu khác nhau thế nào? Hàm có thể trả về gì? Khi input sai, nên báo lỗi ở đâu? Vì sao ví dụ này chưa phải một ứng dụng đầy đủ?

**File giải thích khi triển khai:** `docs/learning/01_python_and_money.md`, gồm sơ đồ gọi hàm, hai ví dụ đúng và hai ví dụ sai.

## Bài 2 — CSV, dữ liệu và hợp đồng

**Liên quan:** P2 và phần nhập CSV của P4–P5.

Hiểu sự khác nhau giữa dòng dữ liệu và cột, UTF-8, ngày ISO, trường bắt buộc và giá trị thiếu. CSV giao dịch để ứng dụng lưu thu chi; dataset gán nhãn để nghiên cứu mô hình. Một giao dịch có số tiền nhưng mẫu phân loại chỉ cần mô tả và nhãn.

**Tự làm:** đọc file mẫu bằng `csv.DictReader`; in số dòng chưa có category. Thử CSV sai header, ngày 30/02, hai dòng cùng ID và mô tả có dấu phẩy được đặt trong dấu nháy.

**Tự trả lời:** vì sao ID trùng có thể làm tổng chi tăng sai? Vì sao không tự động sửa ngày hoặc số tiền đoán được? Vì sao gán nhãn phải có quy tắc?

**File giải thích:** `docs/learning/02_csv_and_labels.md`, kèm bảng lỗi, hướng dẫn nhãn và nguồn dữ liệu.

## Bài 3 — Từ mô tả tiếng Việt đến đặc trưng

**Liên quan:** P2–P3, [tài liệu ML](05_data_and_ml.md).

Mô hình không trực tiếp tính toán trên câu chữ như con người đọc. Vectorizer biến văn bản thành các đặc trưng số. Đặc trưng theo từ có thể phân biệt “học phí” với “cơm trưa”; đặc trưng theo chuỗi ký tự có thể hỗ trợ những biến thể như thiếu dấu hoặc cách viết khác nhau. Đây là giả thuyết cần thí nghiệm.

TF-IDF kết hợp mức xuất hiện của một đặc trưng trong câu với mức độ phổ biến của nó trong tập học. Đọc ví dụ của `TfidfVectorizer`, in `get_feature_names_out()` và số chiều của ma trận. Không gọi `.toarray()` trên toàn bộ dataset lớn chỉ để xem dữ liệu.

**Tự làm:** vector hóa 5 câu tự viết; quan sát kết quả khi câu mới chứa từ chưa từng thấy. Dùng hai cấu hình word n-gram và char n-gram rồi so sánh số đặc trưng.

**Tự trả lời:** vocabulary được học ở tập nào? Vì sao không fit vectorizer trên toàn bộ dữ liệu trước khi chia tập? Unicode khác dấu ảnh hưởng ra sao?

**File giải thích:** `docs/learning/03_text_features.md`, kèm 5 câu ví dụ và nhận xét của bạn. Tham khảo [API TF-IDF chính thức](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html).

## Bài 4 — Huấn luyện và đánh giá

**Liên quan:** P3.

Phân biệt `fit` học tham số, `predict` sinh nhãn, `predict_proba` trả điểm theo lớp trong mô hình có hỗ trợ. Logistic Regression là mô hình phân loại; Naive Bayes là phương pháp so sánh khác. Tự huấn luyện nghĩa là tham số được học từ dataset của bạn, không yêu cầu mô hình phải là mạng neural.

Train dùng để học; validation dùng để chọn cấu hình và ngưỡng; test được giữ lại để đánh giá cuối. Chia theo người/nhóm nguồn khi muốn kiểm tra khả năng dùng cho người chưa có trong train. Lưu manifest chia tập, seed, hash dữ liệu và phiên bản thư viện.

**Tự làm:** tạo ví dụ 100 nhãn với 90 mẫu cùng lớp; giải thích tại sao đoán một lớp có thể accuracy cao nhưng phân loại kém. Tính precision, recall và F1 của một lớp từ TP/FP/FN. Đọc confusion matrix và tìm hai cặp nhãn nhầm nhiều.

**Tự trả lời:** một score 0.80 có bảo đảm đúng 80% không? Vì sao sửa model nhiều lần dựa trên test làm kết quả thiếu tin cậy? Mô hình thua baseline có phải là dữ liệu thất bại cần che đi không?

**File giải thích:** `docs/learning/04_training_and_evaluation.md`, ghi công thức, ví dụ tự tính và số đo từ lần chạy thực. Tham khảo [quy tắc tránh rò rỉ dữ liệu](https://scikit-learn.org/stable/common_pitfalls.html).

## Bài 5 — SQLite và giao dịch

**Liên quan:** P4.

Học bảng, khóa chính, SELECT/INSERT/UPDATE/DELETE, câu SQL có tham số và transaction. Một batch CSV phải được kiểm tra trước rồi ghi như một đơn vị: có xung đột thì không lưu một phần.

**Tự làm:** lưu ba giao dịch vào database dùng riêng cho bài học, tổng hợp theo tháng và category. Import lại cùng ID cùng nội dung; chứng minh số dòng không tăng. Thử cùng ID khác số tiền; chứng minh batch bị từ chối.

**Tự trả lời:** database khác file CSV ở đâu? Vì sao kiểm tra ID trong bộ nhớ chưa đủ bảo vệ database? Vì sao lịch sử sửa nhãn nên lưu lại?

**File giải thích:** `docs/learning/05_sqlite_and_import.md`, gồm schema, câu truy vấn và thử nghiệm atomic import. Đọc [sqlite3 của Python](https://docs.python.org/3/library/sqlite3.html).

## Bài 6 — Giao diện, mô hình và lỗi

**Liên quan:** P5.

Học form, trạng thái phiên làm việc, rerun của Streamlit, bảng preview và cache model. Tách tính tiền, truy cập database và gọi model khỏi phần hiển thị để dễ kiểm tra.

**Tự làm:** tạo form nhập một khoản chi; hiển thị gợi ý và cho sửa nhãn trước lưu. Thử khởi động khi chưa có file model; nhập tay vẫn phải dùng được. Model version và category gợi ý phải được lưu đúng khi người dùng xác nhận.

**Tự trả lời:** vì sao không lưu giao dịch chỉ vì model đoán nhãn? Rerun có thể gây lưu hai lần thế nào? Lỗi giao diện khác lỗi dữ liệu và lỗi mô hình ở đâu?

**File giải thích:** `docs/learning/06_app_and_model.md`, gồm luồng một lần nhập và ba tình huống lỗi. Tham khảo [kiến trúc chạy ứng dụng Streamlit](https://docs.streamlit.io/develop/concepts/architecture/run-your-app).

## Bài 7 — Nghiên cứu và bảo vệ

**Liên quan:** P6, [hướng dẫn bảo vệ](07_defense_guide.md).

Viết câu hỏi nghiên cứu trước khi xem kết quả: mô hình văn bản có hỗ trợ phân loại tốt hơn baseline không; loại đặc trưng nào phù hợp; lựa chọn ngưỡng tác động đến tỷ lệ gợi ý và tỷ lệ sai ra sao?

**Tự làm:** chạy lại một experiment từ môi trường sạch; so manifest và kết quả. Viết một trang phân tích 10 lỗi thật. Quay demo bằng dữ liệu hư cấu, chuẩn bị bản chạy local và báo cáo có số đo thực tế.

**Tự trả lời:** đóng góp của bạn là gì? Dữ liệu có đại diện cho người dùng mục tiêu không? Nếu chưa đạt mục tiêu macro-F1, giới hạn và bước cải thiện có bằng chứng nào?

**File giải thích:** `docs/learning/07_experiments_and_defense.md`, gồm script chạy lại, lỗi đã phân tích và phần bạn tự trình bày.

## Mẫu bắt buộc cho một file giải thích

```markdown
# Tên bài / nhiệm vụ
## Vấn đề và đầu vào, đầu ra
## Kiến thức cần hiểu
## Luồng xử lý và vai trò từng hàm/module
## Vì sao chọn cách làm này
## Lệnh chạy và kết quả thực đã quan sát
## Một tình huống lỗi và cách xử lý
## Bài tập tự sửa
## Câu hỏi tự giải thích và câu trả lời của tôi
## Giới hạn và việc còn lại
```

Mentor nên giải thích theo lớp: một ví dụ cụ thể → ý tưởng → đoạn code → cách kiểm tra. Bạn nên thử giải thích trước khi đọc đáp án mẫu; câu trả lời mẫu không thay thế khả năng trình bày của bạn.
