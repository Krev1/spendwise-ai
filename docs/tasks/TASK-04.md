# TASK-04 — Domain giao dịch và CSV preview

Ngày bắt đầu: 05/10/2026. REQ liên quan: REQ-01, REQ-04, REQ-06, REQ-13. Trạng thái: REVIEW — phần kỹ thuật đã kiểm tra; không xác nhận người học đã hiểu.

## Phạm vi lượt này

Chuyển logic đã có trong `examples/csv_contract.py` thành module của ứng dụng. Bổ sung API đọc CSV từ bytes để giao diện sau này có thể kiểm tra file upload mà không ghi ra đĩa. Giữ lệnh ví dụ cũ chạy được qua một wrapper.

Đầu vào là CSV sáu cột theo [đặc tả](../01_requirements.md), hoặc một dict gồm sáu trường văn bản. Đầu ra là danh sách giao dịch đã kiểm tra và báo cáo preview. Khoản chi chưa có category được phép xuất hiện trong preview; chưa đủ điều kiện lưu giao dịch hoàn tất.

## Phạm vi file

- `src/spendwise/domain/`: danh mục, kiểu dữ liệu, validation giao dịch.
- `src/spendwise/services/`: đọc CSV và tổng hợp tháng.
- `src/spendwise/cli.py`, `scripts/preview_transactions.py`: chạy preview từ terminal.
- `examples/csv_contract.py`: wrapper tương thích.
- `tests/`, `pytest.ini`: kiểm chứng hợp đồng và lệnh chạy.
- Repo Learn: bài 02 và bài tập đối chiếu CSV giao dịch với dataset ML.

## Tiêu chí chấp nhận

1. Chỉ có một implementation cho quy tắc ngày, tiền, ID và category; module đọc CSV gọi domain validator.
2. Tiền từ 1 đến 1.000.000.000.000 VND, ID ASCII tối đa 64 ký tự, mô tả NFC sau trim từ 1–300 ký tự; input sai báo ValidationError.
3. CSV UTF-8 có/không BOM, mô tả có dấu phẩy hoặc newline được quote, giới hạn 2.000.000 byte và 5.000 bản ghi. Header sai, dòng trống, số cột sai, lỗi encoding và ID trùng bị từ chối.
4. Lỗi nghiệp vụ trong bản ghi nhiều dòng nêu dòng bắt đầu của bản ghi; lỗi cú pháp CSV nêu dòng parser phát hiện lỗi.
5. Hai lệnh CLI cũ/mới cho cùng tổng tiền của file mẫu; input lỗi trả exit code 1 và không có traceback cho lỗi dữ liệu thông thường.
6. Đọc file hay bytes không ghi database; tổng thu, chi và chênh lệch dùng số nguyên. Bài học ghi TASK/REQ, commit tham chiếu, lệnh chạy và kết quả thực.

## Điều kiện phụ thuộc và bằng chứng

TASK-02 đã có bằng chứng môi trường. TASK-03 vẫn chờ bài tự làm của người học; lượt này chuẩn bị phần kỹ thuật TASK-04 theo yêu cầu tiếp tục làm việc, không coi đó là bằng chứng đã hiểu Python.

Chạy test hợp đồng đang có, các ranh giới bổ sung, CLI với CSV mẫu và một input sai. Ghi kết quả ở VERIFICATION.md. Chưa triển khai SQLite, xác nhận trên UI, dataset validator hoặc mô hình; không ghi hoàn thành toàn bộ REQ-01/04/06 hay mốc P2 chỉ vì có parser.


## Kết quả thực tế

- Module domain/CSV/reports và CLI đã triển khai; wrapper cũ vẫn chạy.
- pytest: 50 passed, 11 subtests passed. CSV mẫu tháng 10: 9 dòng, thu 5.000.000, chi 2.593.000, chênh lệch 2.407.000 VND.
- Bài giải thích và bài tập được chuẩn bị ở [Learn — bài 02](https://github.com/Krev1/Learn/blob/main/spendwise-ai/lessons/02_csv_and_labels.md).
- TASK-03 vẫn chờ người học thực hành; REQ liên quan chưa hoàn tất ở mức ứng dụng.
