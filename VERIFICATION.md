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

Các cấu trúc code, scripts và phần lớn file lesson được ghi trong thiết kế/kế hoạch là đầu ra tương lai. Bài học trong repo Learn và CSV luyện tập đã được chuẩn bị sau bộ khởi đầu; chưa xác nhận người học đã thực hiện. Các kiểm tra trên xác nhận bộ tài liệu có thể dùng để bắt đầu và ví dụ hiện có chạy được; không chứng minh sản phẩm đã hoàn thành.

## Kiểm tra sau khi tách repo bài học — 05/10/2026

- Bài học đã được xuất bản ở [Learn, commit 2e99d53](https://github.com/Krev1/Learn/commit/2e99d53a2689b25c46d43f78c36120dce0ece95a); fetch lại và đối chiếu toàn bộ Git tree với bản local khớp nhau.
- Kiểm tra UTF-8, code fence và liên kết file nội bộ/chéo repo trên 23 file dự án và 12 file Learn: PASS. Tham chiếu vẫn thuộc 13 REQ đã khai báo.
- Chạy lại `.\.venv\Scripts\python.exe -B -m pytest -q`: **14 passed, 11 subtests passed**.
- Chạy validator của dự án trực tiếp với `..\Learn\spendwise-ai\exercises\transactions_practice.csv`: tổng tháng 10 khớp file mẫu — thu 5.000.000, chi 2.593.000, chênh lệch 2.407.000 VND. Đây là kiểm tra khả năng dùng bài tập giữa hai repo, không phải bài tự làm của người học.
- Rà soát snapshot đã xuất bản: không thấy chuỗi khớp mẫu credential hoặc file môi trường/database/dữ liệu riêng; commit ban đầu chỉ chứa README. Dữ liệu CSV hiện có là hư cấu.


## TASK-04 — Domain, CSV và CLI — 05/10/2026

Từ repo dự án, dùng Python trong `.venv`:

```powershell
.\.venv\Scripts\python.exe -B -m pytest -q
.\.venv\Scripts\python.exe -B scripts/preview_transactions.py examples/transactions_sample.csv --month 2026-10
```

Kết quả thực: **50 passed, 11 subtests passed**. Bao gồm 14 test hợp đồng cũ qua wrapper, cộng kiểm tra giới hạn tiền/ID/mô tả, NFC trước đo độ dài, input dict thiếu/thừa/sai kiểu, header, encoding, quote lỗi, CSV nhiều dòng, chính xác 5.000 bản ghi và 2.000.000 byte, file quá lớn và CLI từ cwd ngoài dự án.

CSV mẫu trả 9 giao dịch, thu 5.000.000, chi 2.593.000, chênh lệch 2.407.000 VND, một khoản chi thiếu nhãn. Tests xác minh input sai trả exit 1, thông báo stderr, không in báo cáo thành công; preview không sửa file hoặc tạo database.

Không có dependency mới. Chưa có kiểm chứng SQLite, UI, baseline hoặc model. Test phần mềm không chứng minh chất lượng AI hoặc mức hiểu của người học.

## TASK-05–06 — Dataset hư cấu, provenance và validator — 05/10/2026

```powershell
.\.venv\Scripts\python.exe -B scripts/collect_reference.py --verify-online
.\.venv\Scripts\python.exe -B scripts/build_seed_dataset.py
.\.venv\Scripts\python.exe -B scripts/validate_dataset.py data/seed/v0.1/expense_descriptions_vi.csv
.\.venv\Scripts\python.exe -B -m pytest -q
```

Đã đối chiếu CSV nguồn và MIT notice tại commit `5d727c66bf2beba91a54d5cda043b6b2eca97ec3` với hash raw và UTF-8/LF: khớp. Builder đối chiếu bốn file seed/audit khớp byte. Validator cấu trúc pass: 356 hư cấu, 0 thật, đủ 8 nhãn, 33 nhóm, 179 câu sau gộp khác dấu; 0 cảnh báo PII theo các mẫu kỹ thuật được cài, không có chứng nhận ẩn danh.

Toàn bộ tests: **86 passed, 11 subtests passed**. Test mới bao gồm source/cờ, ID/nhóm, encoding/header/quote/giới hạn, nhãn xung đột, trùng chuẩn hóa, biến thể khác dấu giao nhóm, nhóm lẫn nguồn, cảnh báo PII, provenance đủ ID/hash, từng dòng nguồn, tính tái tạo, nguồn bị sửa và CLI read-only từ cwd khác. Đã sửa output stderr UTF-8 trên Windows theo lỗi thực từ test. SHA-256 dataset: `537e48b08ba3bc6022bc09cfa8e0cf8944ea2b652a7a66906ad297d745c362f6`.

Seed dùng nhãn AI dự thảo, chưa được người duyệt; validator không đo chất lượng nhãn. Có 0 người tham gia/0 mẫu human-reviewed. Chưa train/split và không có điểm ML. Việc thu thập thật và làm bài của người học còn chờ.

## D13 — Tách triển khai và học — 05/10/2026

Lần này chỉ sửa hướng dẫn, prompt, SDD, bàn giao và mapping/ignore; không đổi Python, dữ liệu, dependency hoặc test implementation. Đã kiểm tra UTF-8/code fence/liên kết trên 57 file dự án và 28 file Learn: PASS, 159 liên kết file nội bộ/chéo repo. Tham chiếu REQ vẫn thuộc 13 yêu cầu.

Mapping có 4 bài đã tồn tại, 10 đường dẫn code/file được xác minh tại commit 9ac8ed0c4702b30ce4a26b980595526c4031e03a bằng git cat-file. Mức hiểu giữ not_verified; chưa tạo checkout/môi trường practice. git check-ignore xác nhận practice, .venv, DB và private input thuộc vùng ignore của Learn. git diff --cached --check không báo lỗi.

Không chạy lại pytest vì code/dữ liệu không đổi. 86 tests và 11 subtests là bằng chứng mốc code trước, không phải test mới hoặc bằng chứng người học hoàn thành bài. Dự án và học dùng hai prompt/phạm vi ghi khác nhau, đồng bộ bằng bàn giao/commit ở đầu buổi; chưa tạo chat, automation hoặc nhắn sang chat khác.
