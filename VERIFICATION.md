# Bằng chứng kiểm tra bộ khởi đầu

Ngày kiểm tra: 05/10/2026. Môi trường kiểm tra trong phiên làm việc: Windows PowerShell, Python 3.14.7.

## Đã kiểm tra

### Ví dụ Python

Lệnh thực đã chạy từ thư mục bộ tài liệu:

```powershell
python -B examples/csv_contract.py examples/transactions_sample.csv --month 2026-10
python -B -m unittest discover -s examples -p "test_*.py" -v
```

Kết quả: **14 test PASS**. Nội dung kiểm tra bao gồm tiền sai; ngày sai; category khoản thu; khoản chi thiếu nhãn; ID trùng trong batch; BOM UTF-8 và mô tả có dấu phẩy; số cột; lọc tháng và tách thu/chi; tháng trống; tháng sai; batch trống; dòng trống; Unicode NFC; đầu ra CLI tiếng Việt và tổng của file mẫu.

Kết quả file hư cấu trong tháng 10: 9 giao dịch, thu 5.000.000 VND, chi 2.593.000 VND, chênh lệch 2.407.000 VND, một khoản chi cần xác nhận nhãn. Dòng tháng 9 không bị tính vào tháng 10.

### Tài liệu

- Kiểm tra hiện diện các tài liệu chính; đọc được bằng UTF-8, không có ký tự thay thế lỗi.
- Kiểm tra liên kết Markdown nội bộ và cặp code fence.
- Kiểm tra các tham chiếu REQ đều thuộc 13 REQ đã khai báo.
- Parse AST của hai file Python thành công.
- Đối chiếu tĩnh CSV schema, 8 danh mục, giới hạn ID, kiểu tiền và tên dependency lock.
- Đã đồng bộ `group_id` theo người cung cấp hoặc nguồn/khuôn và `source_payload_hash` trước AI/xác nhận.

Rà soát tài liệu được thực hiện bởi các vai trò AI và người điều phối trong phiên này; không gọi đó là thẩm định độc lập của giảng viên.

## Phạm vi bằng chứng

Ví dụ chỉ đọc/validate CSV và tính tổng. Chưa kiểm tra SQLite/atomic database import, Streamlit UI hoặc mô hình, vì các phần này chưa được triển khai. Không có điểm macro-F1, coverage hay selective accuracy thực nghiệm. Quy định đồ án của trường vẫn cần xác minh.

## P1 — Môi trường dự án đã kiểm tra

Trong `.venv`, đã thực hiện:

```powershell
.\.venv\Scripts\python.exe -B scripts/check_environment.py
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -B -m unittest discover -s examples -p "test_*.py" -v
.\.venv\Scripts\python.exe -B -m pytest -q
```

Import thành công, `isolated_environment = true`; pip không báo xung đột. unittest đạt 14 tests OK; pytest đạt 14 passed. Phiên bản: Python 3.14.7, scikit-learn 1.9.1, pandas 3.0.6, Streamlit 1.65.0, joblib 1.6.0, pytest 9.1.1. Dependency đầy đủ được ghi ở `requirements.lock.txt`. Đây là kiểm tra trên máy Windows của phiên này, chưa phải kiểm chứng đa nền tảng.

Các cấu trúc code, scripts và phần lớn file lesson được ghi trong thiết kế/kế hoạch là đầu ra tương lai. Bài học `docs/learning/01_python_and_money.md` và CSV luyện tập đã được chuẩn bị sau bộ khởi đầu; chưa xác nhận người học đã thực hiện. Các kiểm tra trên xác nhận bộ tài liệu có thể dùng để bắt đầu và ví dụ hiện có chạy được; không chứng minh sản phẩm đã hoàn thành.
