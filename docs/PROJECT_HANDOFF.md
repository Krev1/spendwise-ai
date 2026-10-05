# Bàn giao kỹ thuật cho Mentor

Ngày cập nhật: 05/10/2026. Quyết định D13. Bản này ghi đầu vào học; không xác nhận người học hiểu. [Code hiện có tại commit 9ac8ed0](https://github.com/Krev1/spendwise-ai/tree/9ac8ed0c4702b30ce4a26b980595526c4031e03a) không thay đổi trong lần tách workflow này.

## Hiện trạng kỹ thuật

| TASK / REQ | Đầu ra đã có | File/hàm trọng tâm | Bằng chứng |
|---|---|---|---|
| TASK-02 / REQ-11,12,13 | Môi trường riêng, dependency lock | scripts/check_environment.py, requirements.lock.txt | Setup đã kiểm tra trong VERIFICATION.md |
| TASK-04 / REQ-01,04,06 | Domain, CSV file/bytes, tổng tháng, CLI | domain/transactions.py: parse_amount/parse_transaction; services/csv_reader.py: read_transactions; services/reports.py: summarize | 50 tests + 11 subtests ở mốc TASK-04 |
| TASK-05–06 / REQ-08,09,13 | Seed, source snapshot, provenance, builder/validator | data/dataset.py: read_dataset_bytes/audit_dataset; scripts/build_seed_dataset.py; data/seed/v0.1/ | Toàn bộ kiểm tra ở mốc này: 86 tests + 11 subtests |

Đường dẫn module tương đối trong bảng nằm dưới `src/spendwise/`. [Bằng chứng](../VERIFICATION.md), [task 04](tasks/TASK-04.md), [task 05–06](tasks/TASK-05-06.md) và [dataset card](../data/seed/v0.1/DATASET_CARD.md) ghi chi tiết phạm vi.

## Quyết định cần hiểu từ code

- Tiền VND là int dương; tính tổng bằng code, không dùng model. Domain kiểm tra trước khi reports cộng.
- CSV giao dịch và dataset ML đều sáu cột nhưng khác header/hợp đồng. Parser dataset độc lập với parser giao dịch.
- CSV preview không ghi DB; khoản chi chưa nhãn được preview nhưng ứng dụng tương lai phải xác nhận trước lưu.
- Dataset seed: 356 hư cấu (319 tự tạo, 37 chuyển ngữ), 0 thật, 33 nhóm; 179 câu nếu gộp khác dấu. Các biến thể cùng nhóm.
- Mọi nhãn seed là ai_draft, 0 human-reviewed. Hash/cấu trúc pass không xác nhận đúng nhãn, sạch mọi PII hay hiệu quả thực tế.
- Source công khai đã khóa commit, có MIT notice và hash; builder tái tạo offline, mặc định chỉ so byte.

## Lệnh đã dùng ở mốc code hiện tại

Chạy trong checkout riêng của phiên bản học, dùng `.venv` của checkout đó:

```powershell
.\.venv\Scripts\python.exe -B scripts/check_environment.py
.\.venv\Scripts\python.exe -B scripts/preview_transactions.py examples/transactions_sample.csv --month 2026-10
.\.venv\Scripts\python.exe -B scripts/build_seed_dataset.py
.\.venv\Scripts\python.exe -B scripts/validate_dataset.py data/seed/v0.1/expense_descriptions_vi.csv
.\.venv\Scripts\python.exe -B -m pytest -q
```

CSV mẫu: 9 giao dịch tháng 10, thu 5.000.000, chi 2.593.000, chênh lệch 2.407.000 VND; một khoản chi cần xác nhận danh mục. Builder báo reproduced_exactly và 356/0 thật. Tests đã chạy được ghi ở VERIFICATION; người học chạy lại là bằng chứng thực hành mới, không sửa kết quả mốc cũ.

## Chưa triển khai và đầu vào còn thiếu

Chưa có TASK-07 baseline, split/train/model, SQLite hoặc Streamlit UI; chưa có dữ liệu/test thật và metric ML. Consent, nhãn người duyệt và rubric trường còn cần thực tế. TASK-03 học Python do Mentor/người học thực hiện, không chặn code đủ đầu vào. TASK-04/05–06 vẫn giữ trạng thái REVIEW đã ghi; tách workflow không tự chuyển task thành DONE.

## Hướng tiếp theo

Dự án: đọc kế hoạch/task/bằng chứng và xem TASK-07 baseline có đủ đầu vào prototype. Không chờ bài học; dùng seed cho demo kỹ thuật, không báo chất lượng real. Mentor: học 00 → 01 → 02 → 02b trên commit đã chọn; cập nhật mapping khi nhận mốc baseline/model/app mới.

Khi dự án thay đổi, cập nhật bảng đầu ra, các quyết định/lệnh/kết quả/giới hạn và thông báo commit mới. Mentor khóa SHA của buổi học trong Learn để tránh học nhầm phiên bản. Bàn giao không bao gồm dữ liệu thật, credentials hay binary model riêng tư.
