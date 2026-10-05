# Buổi 1 — Chạy chương trình và hiểu thu–chi

Ngày chuẩn bị: 05/10/2026. Thời lượng gợi ý: 30–45 phút, có thể chia thành hai buổi. Bài học này được chuẩn bị sẵn; chưa xác nhận người học đã thực hiện hoặc hiểu bài.

## 1. Mục tiêu hôm nay

Bạn làm được ba việc:

1. Chạy một chương trình Python bằng lệnh.
2. Giải thích dữ liệu đi từ CSV tới kết quả tổng thu, tổng chi và chênh lệch.
3. Tự thêm một giao dịch, dự đoán kết quả rồi kiểm tra bằng chương trình.

Đây là phần đầu của P1. Môi trường riêng và dependency đã được chuẩn bị trong phiên khởi động. Ví dụ dùng thư viện chuẩn; thực hành bằng Python trong `.venv` để quen cách chạy dự án.

## 2. Hiểu dự án bằng một câu

Ứng dụng giúp sinh viên và người mới đi làm nhập thu–chi, xem tổng hợp và nhận gợi ý danh mục khoản chi tiếng Việt từ mô hình tự huấn luyện.

Ví dụ: `ăn trưa cơm gà` → gợi ý `an_uong` → người dùng xác nhận → lưu giao dịch → tổng hợp tháng.

Bạn hãy viết lại mục tiêu này bằng lời của mình trước khi học tiếp.

## 3. Chạy ví dụ gốc

Mở PowerShell tại thư mục gốc `spendwise-ai`, nơi có README và `.venv`. Kiểm tra vị trí:

```powershell
Get-Location
```

Kiểm tra Python và chạy ví dụ:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -B examples/csv_contract.py examples/transactions_sample.csv --month 2026-10
```

Nếu bạn chuyển dự án sang thư mục khác, chạy từ thư mục chứa README. Có thể dùng `Set-Location -LiteralPath` với đường dẫn nơi bạn lưu dự án.

Lệnh thứ hai gồm:

| Phần lệnh | Ý nghĩa |
|---|---|
| `.\.venv\Scripts\python.exe` | Python riêng của dự án |
| `-B` | Không tạo file bytecode cache khi chạy bài học |
| `examples/csv_contract.py` | File mã nguồn cần chạy |
| `examples/transactions_sample.csv` | File dữ liệu đầu vào |
| `--month 2026-10` | Chỉ tổng hợp giao dịch tháng 10/2026 |

Bạn sẽ thấy kết quả dạng JSON: dữ liệu có tên trường và giá trị, tương tự một dict của Python. Các giá trị chính của file gốc:

```json
{
  "rows": 9,
  "income_vnd": 5000000,
  "expense_vnd": 2593000,
  "net_vnd": 2407000,
  "pending_expense_categories": 1
}
```

Chương trình còn hiển thị tổng chi theo danh mục. CSV gốc có 10 dòng giao dịch, nhưng một dòng thuộc tháng 9 nên không được tính ở tháng 10.

Tất cả giao dịch của bài học là hư cấu. `net_vnd` là chênh lệch thu–chi đã ghi trong tháng, chưa phải số dư tài khoản ngân hàng. Một khoản chi chưa có danh mục vẫn được tính trong **preview**; ứng dụng tương lai cần người dùng xác nhận danh mục trước khi lưu.

## 4. Xem dữ liệu

Mở [CSV luyện tập](../../examples/transactions_practice.csv). Đây là bản sao được chuẩn bị từ [CSV gốc](../../examples/transactions_sample.csv), để bạn sửa mà vẫn giữ file mẫu ban đầu.

Header:

```csv
transaction_id,date,transaction_type,amount_vnd,description,category
```

| Cột | Ý nghĩa | Ví dụ |
|---|---|---|
| `transaction_id` | Mã ổn định phân biệt từng giao dịch | `practice_01` |
| `date` | Ngày giao dịch | `2026-10-08` |
| `transaction_type` | Khoản thu hoặc chi | `income` / `expense` |
| `amount_vnd` | Số tiền nguyên dương bằng VND | `45000` |
| `description` | Mô tả bạn ghi | `Mua vở học tập` |
| `category` | Mã danh mục khoản chi | `hoc_tap` |

Khoản thu có category trống. Khoản chi có thể chưa có nhãn trong file khi chuẩn bị preview. Số tiền không có dấu chấm/phẩy phân cách: viết `45000`, không viết `45.000`.

## 5. Kiến thức Python cần hiểu ngay

### Chuỗi và số nguyên

`"45000"` là chuỗi ký tự; `45000` là số nguyên. CSV chứa văn bản nên chương trình phải kiểm tra rồi chuyển cột số tiền sang `int` để tính toán.

Ví dụ:

```python
amount_text = "45000"
amount_vnd = int(amount_text)
new_total = amount_vnd + 10000
print(new_total)  # 55000
```

### Hàm và return

Hàm nhận đầu vào, xử lý một việc và có thể trả kết quả:

```python
def net_cashflow(total_income, total_expense):
    return total_income - total_expense

result = net_cashflow(5000000, 2593000)
print(result)
```

`return` đưa giá trị về nơi gọi hàm. `print` hiển thị thông tin. Hàm chỉ `print` chưa chắc cung cấp giá trị để hàm khác tiếp tục tính.

### Kiểm tra dữ liệu và báo lỗi

Ứng dụng cần từ chối số tiền âm, 0 hoặc số thập phân vì chúng trái hợp đồng của MVP. Gặp input sai, chương trình báo lỗi để sửa nguồn; nó không đoán số tiền rồi tính tiếp.

Mở [mã ví dụ](../../examples/csv_contract.py), tìm ba hàm sau:

- `read_transactions`: đọc file và kiểm tra các dòng.
- `parse_amount`: kiểm tra và chuyển tiền sang số nguyên.
- `summarize`: lọc tháng rồi tính tổng.

Luồng chính:

```text
Lệnh chạy → main → read_transactions → parse_row / parse_amount
          → summarize → hiển thị kết quả
```

Buổi này hãy tập trung vào luồng dữ liệu và ba hàm đó. Các khái niệm như dataclass, argparse và unittest sẽ được giải thích sâu dần trong những bài tiếp theo.

## 6. Bài tập của bạn

Trong `transactions_practice.csv`, thêm dòng cuối với ID chưa từng có:

```csv
practice_01,2026-10-08,expense,45000,Mua vở học tập,hoc_tap
```

**Trước khi chạy**, ghi dự đoán của bạn:

```text
Số giao dịch tháng 10:
Tổng thu:
Tổng chi:
Chênh lệch thu–chi:
```

Sau khi lưu file, chạy:

```powershell
.\.venv\Scripts\python.exe -B examples/csv_contract.py examples/transactions_practice.csv --month 2026-10
```

So sánh dự đoán với kết quả thực. Nếu khác, tìm dòng nào hoặc phép tính nào gây ra khác biệt.

Sau đó đổi riêng số tiền của `practice_01` từ `45000` thành `-45000`, chạy lại và ghi thông báo lỗi. Cuối cùng sửa lại `45000` để file luyện tập hợp lệ.

Không sửa CSV gốc: một bài kiểm tra đang đối chiếu đúng kết quả của file mẫu đó.

## 7. Câu hỏi tự giải thích

1. Vì sao file có 10 giao dịch nhưng tổng hợp tháng 10 chỉ có 9 trước bài tập?
2. Sau khi thêm khoản chi, trường nào tăng, trường nào giảm, trường nào giữ nguyên?
3. Vì sao `"45000"` cần được chuyển sang số để tính tổng?
4. Mô hình AI sẽ làm bước nào trong dự án? Phép cộng tiền có cần mô hình không?
5. Nếu nhập cùng giao dịch hai lần mà không kiểm tra ID, tổng chi có thể bị ảnh hưởng thế nào?

Gửi kết quả chạy và câu trả lời của bạn để Mentor kiểm tra. Chưa cần có câu trả lời hoàn hảo; phần bạn đang nhầm sẽ quyết định ví dụ tiếp theo.

## 8. Nhật ký của người học

Bạn tự điền sau khi thực hiện; hiện để trống:

```text
Ngày thực hiện:
Lệnh tôi đã chạy:
Dự đoán trước khi sửa CSV:
Kết quả sau khi sửa:
Thông báo khi thử số tiền âm:
Điều tôi hiểu được:
Điều tôi chưa hiểu:
Trả lời 5 câu hỏi:
```

Hoàn thành buổi này khi bạn chạy được ví dụ, tự sửa CSV và giải thích được thay đổi tổng tiền. Bước kế tiếp: ôn hàm/list/dict qua một bài tập nhỏ rồi bắt đầu validator dữ liệu và hướng dẫn gán nhãn ở P2.
