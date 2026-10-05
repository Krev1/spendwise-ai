# Grouped split prototype — TASK-08

[Bundle seed-v0.1-prototype](seed-v0.1-prototype/lock.json) chỉ dùng kiểm tra kỹ thuật trên dữ liệu hư cấu/nhãn AI dự thảo. Dataset/provenance gốc giữ nguyên byte. Chưa có test thật hoặc nhãn/quan hệ được người duyệt.

Protocol A13: sort ID, union group/family/lineage/folded và ba link bảo thủ AI, rồi SGKF 7 fold/seed42 một lần. Fold0 test prototype, fold1 validation, còn lại train. Không chọn lại seed hoặc chuyển mẫu để đủ lớp.

| Tập | Hàng | Nhóm hiệu lực | Unique folded | Lớp thiếu |
|---|---:|---:|---:|---|
| Train | 256 | 20 | 129 | Không |
| Validation | 50 | 5 | 25 | an_uong, di_chuyen, suc_khoe |
| Test prototype | 50 | 5 | 25 | an_uong, di_chuyen, khac |

Tỷ lệ thực 71,91%/14,04%/14,04%; chênh mục tiêu +1,91/-0,96/-0,96 điểm phần trăm. Tổng 30 nhóm hiệu lực, nhóm lớn nhất 67 hàng; 51 family và 179 lineage/unique folded. Có 12 candidate gần trùng theo heuristic; 3 link giao nguồn được giữ chung. Chín candidate còn lại chưa có bằng chứng quan hệ để tự nối; bốn cặp giao partition. Kiểm tra không giao chỉ áp dụng khóa/quan hệ đã khai báo, không chứng nhận sạch mọi rò rỉ ngữ nghĩa.

```powershell
.\.venv\Scripts\python.exe -B scripts/split_dataset.py
.\.venv\Scripts\python.exe -B scripts/split_dataset.py --write
```

Mặc định preview nếu chưa có output, verify nếu đã có. `--write` chỉ tạo mới hoặc xác minh bundle khớp; không overwrite. Mỗi bundle đúng ba file: manifest, audit và lock. Lock gồm hash snapshot/provenance/relations/guideline section, môi trường/config, implementation và đầu ra. Đọc lại tái tạo expected từ đầu vào tin cậy, so từng byte kể cả lock; tự sửa manifest và hash trong lock vẫn bị từ chối. Không thêm README vào bên trong bundle.

`load_split_ids(output, expected)` chỉ trả ID sau verify; TASK-09–10 phải dùng riêng ID train để fit. Mô tả, metadata và assignment không phải feature classifier. Thay input/protocol/môi trường/implementation cần phiên bản mới được rà soát; không dùng `--force`, không đổi nhãn seed hiện tại để hợp kết quả.

[Task card](../../docs/tasks/TASK-08.md) và [evidence](../../docs/evidence/TASK-08-2026-10-05/qa_review.md) ghi kiểm tra và giới hạn. Không fit vectorizer/model, không lưu model binary hoặc đo metric ML ở mốc này.
