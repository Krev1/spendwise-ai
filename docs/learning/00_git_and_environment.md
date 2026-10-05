# Buổi khởi động — GitHub và môi trường Python

Ngày: 05/10/2026. Liên quan TASK-01–03, REQ-11–13.

## Đã thực hiện

- Tạo repository riêng tư [Krev1/spendwise-ai](https://github.com/Krev1/spendwise-ai). Đây là tài khoản kết nối mà người học chọn; username hiện hành được GitHub xác nhận là `Krev1`.
- Chuyển bộ SDD và ví dụ thành thư mục dự án độc lập.
- Tạo `.venv`, cài thư viện, kiểm tra import và kiểm tra xung đột dependency.
- Chạy ví dụ CSV và 14 kiểm tra bằng Python trong `.venv`.
- Tạo file giữ phiên bản dependency thực và quy tắc Git bỏ qua môi trường, dữ liệu riêng tư, database.

Các bước này chuẩn bị nền tảng. Chưa có giao diện ứng dụng hoàn chỉnh, dataset thật hoặc mô hình đã huấn luyện. Người học cần tự chạy và giải thích bài 1 để hoàn tất mục tiêu học của P1.

## 1. Git và GitHub khác nhau ở đâu?

Git lưu lịch sử thay đổi của các file trên máy. GitHub chứa một bản repository để lưu trữ và cộng tác qua mạng.

| Khái niệm | Ví dụ dễ hiểu |
|---|---|
| Working tree | Những file bạn đang mở và sửa |
| Staging area | Những thay đổi bạn chọn đưa vào lần lưu tiếp theo |
| Commit | Một mốc thay đổi có thông điệp và mã SHA |
| Branch `main` | Nhánh chứa trạng thái chính của dự án |
| Remote `origin` | Tên thường dùng cho địa chỉ repository trên GitHub |
| Push | Đưa commit local lên remote, cần quyền tài khoản phù hợp |

Thư mục `.git` giữ thông tin quản lý lịch sử. `.gitignore` liệt kê các file không nên thêm vào Git, ví dụ `.venv/`, `data/private/` và `local/`.

Một tài khoản GitHub kết nối trong công cụ AI và tài khoản đăng nhập Git trên máy có thể khác nhau. Phiên này dùng kết nối GitHub đã được người học chọn để xuất bản. Khi chạy `git clone`, `git fetch` hoặc `git push` trực tiếp, cần đăng nhập tài khoản có quyền repository; đây là xác thực riêng của Git trên máy.

Các lệnh đọc để học:

```powershell
git status
git log --oneline -5
git remote -v
```

`git status` cho biết file thay đổi. `git log` xem các mốc đã có. `git remote -v` xem địa chỉ kết nối; đọc chúng không thay đổi code.

Tham khảo cấu trúc repository trong [tài liệu Git chính thức](https://git-scm.com/docs/gitrepository-layout).

## 2. Vì sao cần .venv?

Mỗi dự án có thể cần phiên bản thư viện khác nhau. `.venv` chứa Python và thư viện riêng cho dự án. Python trong `.venv` dùng bộ thư viện đó, thay vì phụ thuộc vào mọi package đã cài trên máy.

Trong PowerShell, từ thư mục gốc dự án:

```powershell
.\.venv\Scripts\python.exe -B scripts/check_environment.py
```

Kết quả cần có `isolated_environment: true`. Script kiểm tra import và phiên bản; nó không huấn luyện mô hình hoặc gọi API tài chính.

## 3. Các thư viện dùng để làm gì?

| Package | Vai trò trong kế hoạch |
|---|---|
| scikit-learn | Vector hóa mô tả, train classifier, tính metric |
| pandas | Làm việc với bảng dữ liệu khi triển khai |
| Streamlit | Tạo giao diện chạy local trong các mốc sau |
| joblib | Lưu/tải pipeline được tạo bởi dự án |
| pytest | Chạy kiểm tra phần mềm |

`requirements.in` ghi thư viện cần dùng; `requirements.lock.txt` ghi phiên bản thực đã cài và kiểm tra. File lock là ảnh chụp môi trường Windows/Python trong phiên này, chưa chứng minh tương thích với mọi hệ điều hành hoặc phiên bản Python.

Nếu clone sang máy khác có Python tương thích:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock.txt
.\.venv\Scripts\python.exe -m pip check
```

Không cần activate để chạy: đường dẫn `.venv\Scripts\python.exe` đã chỉ đúng interpreter của dự án.

## 4. Bạn thực hiện ngay

1. Đọc [buổi 1](01_python_and_money.md).
2. Chạy CSV bằng interpreter riêng:

```powershell
.\.venv\Scripts\python.exe -B examples/csv_contract.py examples/transactions_sample.csv --month 2026-10
```

3. Chạy các kiểm tra:

```powershell
.\.venv\Scripts\python.exe -B -m pytest -q
```

4. Thực hiện bài thêm khoản chi trong `transactions_practice.csv`, dự đoán trước và ghi kết quả vào nhật ký bài 1.

## 5. Câu hỏi để bạn tự giải thích

- GitHub đã có repository thì máy tính còn cần Git để làm gì?
- `.venv` và `.git` giữ hai loại thông tin nào?
- Vì sao không đưa `.venv` và dữ liệu tài chính thật lên repository?
- Python của dự án nằm ở đâu?
- Khi một bài kiểm tra pass, điều gì đã được kiểm chứng và điều gì chưa được kiểm chứng?

## Nhật ký học

```text
Lệnh tôi đã tự chạy:
Kết quả tôi thấy:
Câu trả lời của tôi:
Điểm tôi chưa hiểu:
```

Giữ phần này trống cho đến khi bạn thực hiện. Mốc kỹ thuật chạy được và mức hiểu của người học được ghi riêng.
