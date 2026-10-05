# TASK-08 — Audit và grouped split prototype

Ngày 05/10/2026. Trạng thái REVIEW — prototype kỹ thuật đã Verified, phần nghiên cứu thiếu human review/support; REQ-08,09,13; phụ thuộc TASK-06, A13/D13. Root sở hữu `src/spendwise/data/splitting.py`, `scripts/split_dataset.py`, recipe/bundle prototype, tests và tài liệu. Data Engineer và QA subagent chỉ đọc/audit/review; không sửa Learn hoặc nhãn.

## Đầu vào và hợp đồng

- Seed/provenance v0.1, toàn hư cấu/ai_draft; recipe link bảo thủ AI riêng. Kiểm tra ID/hash/cờ/namespace/lineage trước chia. Sai metadata hoặc dữ liệu thật bị từ chối, không echo mô tả lỗi.
- Union group gốc, family và phrase theo source ID/commit, folded key, recipe links; lấy thành phần bắc cầu làm nhóm hiệu lực. Recipe chỉ chấp nhận `ai_conservative_prototype,false`, không gán trạng thái human-reviewed.
- Screen gần trùng theo A13 trên tối đa 500 đại diện folded, ghi ID/điểm tương đồng/cross-source, không dùng similarity làm ground truth hoặc feature. Không nối tự động mọi candidate; các cặp cần con người rà soát vẫn được báo.
- ID sort trước SGKF 7 fold/seed42; fold0 test prototype, fold1 validation, phần còn lại train. Không fit model/vectorizer, không thử lại seed/fold.
- Manifest ghi ID, group, effective group, family, lineage hash, text/folded hash, label/source/cờ/status và split. Mỗi ID đúng một lần; group/family/lineage/folded/known links không giao. Báo số mẫu/nhóm/unique folded/support/missing labels và lệch70/15/15; không che lớp thiếu.
- Bundle `split_manifest.csv`, `audit.json`, `lock.json` có dataset/provenance/relations/guideline hashes, config/phiên bản môi trường và hash file đầu ra. Mặc định preview hoặc verify; `--write` ghi qua temp+rename. Existing bundle phải khớp byte, không có `--force`. Từ chối bundle thiếu/thừa/tampered hoặc stale snapshot/config; lỗi ghi không để target có vẻ locked.
- Verify bundle rồi cung cấp ID train cho task feature sau này. Khóa prototype không là khóa test thật; nhãn/quan hệ chưa người duyệt và support thiếu ngăn kết luận nghiên cứu.

## Lệnh và tiêu chí chấp nhận

```powershell
.\.venv\Scripts\python.exe -B scripts/split_dataset.py
.\.venv\Scripts\python.exe -B scripts/split_dataset.py --write
.\.venv\Scripts\python.exe -B -m pytest -q
```

Kiểm tra metadata stale/duplicate/missing/hash/source; union bắc cầu và namespace; tái lập khi đổi thứ tự input; manifest mỗi ID một split; không giao nhóm/family/lineage/folded/known links; đọc lại phát hiện thay label hoặc assignment, file thiếu/thừa, lock bị sửa; output đã có khác byte không overwrite; lỗi giữa ghi không publish bundle; CLI cwd khác/default read-only. Missing class phải xuất thật. Không tạo metric/artifact.

## Bằng chứng / phần thiếu

Code ở [b5afb11c7bfc9133d6c94d986a5727363e43e1fc](https://github.com/Krev1/spendwise-ai/commit/b5afb11c7bfc9133d6c94d986a5727363e43e1fc). Toàn bộ suite đạt **193 tests + 11 subtests**, gồm 54 case mới; [pytest](../evidence/TASK-08-2026-10-05/pytest.txt), [QA](../evidence/TASK-08-2026-10-05/qa_review.md), [bundle](../../data/splits/README.md). Metadata dòng nguồn và Windows junction đã được QA probe, sửa và xác minh lại. Không còn finding trong phạm vi review AI.

Bundle đã created và verified_existing: 356 hư cấu/0 thật, 33 nhóm gốc → 30 nhóm hiệu lực, 51 family, 179 lineage/unique folded, 12 candidate gần trùng. Train256/20groups/129unique đủ8 lớp; validation50/5/25 thiếu an_uong, di_chuyen, suc_khoe; test50/5/25 thiếu an_uong, di_chuyen, khac. Tỷ lệ71,91/14,04/14,04%, không retry. Ba link bảo thủ AI cùng component; bốn candidate chưa xác nhận vẫn giao partition và được báo rõ. Overlap check chỉ cho các khóa/quan hệ đã khai báo.

Human label/semantic relationship review, consent/dữ liệu thật và test thật đủ support vẫn thiếu. Nghiên cứu TASK-08 giữ REVIEW; prototype đã xác minh riêng. Chưa fit model/vectorizer hoặc đo metric ML. Không xác nhận mức hiểu người học hoặc trường chấp nhận. TASK-09 có thể tiếp tục feature prototype với ID train đã verify; TASK-13 SQLite đủ hợp đồng để triển khai độc lập.
