# Bàn giao kỹ thuật cho Mentor

> **Bàn giao mới:** [SDD v0.2](sdd-v0.2/README.md), [kế hoạch](sdd-v0.2/03_implementation_plan.md). Lượt này chỉ docs/prompt, chưa code/train/deploy; giữ SHA/evidence v0.1 bên dưới. SW-TASK-01 đọc lại work/HEAD thật.


Ngày cập nhật: 05/10/2026. Quyết định D13/A12/A13. Bản này ghi đầu vào học; không xác nhận người học hiểu. Code TASK-08 ở [commit b5afb11c7bfc9133d6c94d986a5727363e43e1fc](https://github.com/Krev1/spendwise-ai/tree/b5afb11c7bfc9133d6c94d986a5727363e43e1fc); TASK-07 vẫn ở [b331e5f](https://github.com/Krev1/spendwise-ai/tree/b331e5f078a07a73e34d44f22da69d89774eae96). Mentor khóa SHA theo mốc đang học; bằng chứng từng mốc giữ riêng.

## Hiện trạng kỹ thuật

| TASK / REQ | Đầu ra đã có | File/hàm trọng tâm | Bằng chứng |
|---|---|---|---|
| TASK-02 / REQ-11,12,13 | Môi trường riêng, dependency lock | scripts/check_environment.py, requirements.lock.txt | Setup đã kiểm tra trong VERIFICATION.md |
| TASK-04 / REQ-01,04,06 | Domain, CSV file/bytes, tổng tháng, CLI | domain/transactions.py: parse_amount/parse_transaction; services/csv_reader.py: read_transactions; services/reports.py: summarize | 50 tests + 11 subtests ở mốc TASK-04 |
| TASK-05–06 / REQ-08,09,13 | Seed, source snapshot, provenance, builder/validator | data/dataset.py: read_dataset_bytes/audit_dataset; scripts/build_seed_dataset.py; data/seed/v0.1/ | Toàn bộ kiểm tra ở mốc này: 86 tests + 11 subtests |
| TASK-07 / REQ-09,13 | Baseline từ khóa có giải thích, Dummy most_frequent, CLI demo hư cấu | ml/baselines.py: normalize_description, KeywordBaseline.explain/predict, MostFrequentBaseline.fit/predict; scripts/demo_baselines.py: read_fixture/main | [139 tests + 11 subtests](evidence/TASK-07-2026-10-05/pytest.txt), [demo](evidence/TASK-07-2026-10-05/demo_baselines.json), [QA](evidence/TASK-07-2026-10-05/qa_review.md); DONE prototype |
| TASK-08 / REQ-08,09,13 | Grouped split prototype bất biến; audit, manifest/lock, ID loader sau verify | data/splitting.py: read_provenance, effective_groups, build_bundle, verify_bundle, write_bundle, load_split_ids; scripts/split_dataset.py; data/splits/ | [193 tests + 11 subtests](evidence/TASK-08-2026-10-05/pytest.txt), [QA](evidence/TASK-08-2026-10-05/qa_review.md); prototype Verified, nghiên cứu REVIEW |

Đường dẫn module tương đối trong bảng nằm dưới `src/spendwise/`. [Bằng chứng](../VERIFICATION.md), [task 04](tasks/TASK-04.md), [task 05–06](tasks/TASK-05-06.md) và [dataset card](../data/seed/v0.1/DATASET_CARD.md) ghi chi tiết phạm vi.

## Quyết định cần hiểu từ code

- Tiền VND là int dương; tính tổng bằng code, không dùng model. Domain kiểm tra trước khi reports cộng.
- CSV giao dịch và dataset ML đều sáu cột nhưng khác header/hợp đồng. Parser dataset độc lập với parser giao dịch.
- CSV preview không ghi DB; khoản chi chưa nhãn được preview nhưng ứng dụng tương lai phải xác nhận trước lưu.
- Dataset seed: 356 hư cấu (319 tự tạo, 37 chuyển ngữ), 0 thật, 33 nhóm; 179 câu nếu gộp khác dấu. Các biến thể cùng nhóm.
- Mọi nhãn seed là ai_draft, 0 human-reviewed. Hash/cấu trúc pass không xác nhận đúng nhãn, sạch mọi PII hay hiệu quả thực tế.
- Source công khai đã khóa commit, có MIT notice và hash; builder tái tạo offline, mặc định chỉ so byte.
- B1 giữ dấu/NFC/chữ thường/khoảng trắng; keyword có ranh giới token chữ/số/`_`/mark. Cụm dài loại hit ngắn bị chứa, nên `nước giặt` không thành ăn uống. Hit độc lập nhiều lớp như `cơm trưa và vé phim` trả `khac/conflict`; no-match cũng fallback `khac` nhưng có status riêng. Rule khớp `thuốc lá` thuộc `khac` là trường hợp khác. Không có score giả, mọi nhãn vẫn cần người xác nhận.
- Rule version/hash giữ cấu hình/thứ tự để tái lập. Alias không dấu khai báo rõ; B1 không hiểu ngữ nghĩa và không bảo đảm nhận biết ngoài miền. Không nối cụm qua dấu câu. Validation từ chối Unicode surrogate trước report để lỗi không làm CLI dừng bất ngờ.
- B0 dùng sklearn DummyClassifier most_frequent, seed 42; fit chỉ descriptions/labels. TASK-07 fit 10 ví dụ hư cấu riêng trong bộ nhớ, probe chỉ predict. `an_uong` là lớp phổ biến của fixture với 3 ví dụ; các câu probe đều được B0 trả lớp đó, không phải độ chính xác. Tie theo thứ tự lớp của sklearn 1.9.1 đã test.
- Fixture `examples/baseline_demo.json` là AI soạn, nguồn author_synthetic, chưa human-reviewed. CLI kiểm tra toàn fixture trước fit/in kết quả, chỉ read-only và không tạo artifact. Ở TASK-10 phải chọn train từ manifest TASK-08; API B0 không tự chứng nhận train đã giữ test độc lập.
- TASK-08 union group/family/lineage/folded bắc cầu, namespace source ID/commit tránh nối ID trùng tên qua nguồn. Ba link Steam/phim/clinic được co-locate bảo thủ AI; không gán human-reviewed. Near-duplicate heuristic chỉ tạo danh sách cần rà, không nối mọi câu chung từ/lớp.
- ID sort, SGKF7/seed42 một lần: fold0 test prototype, fold1 validation, còn lại train. 256/50/50, 30 nhóm hiệu lực; tỷ lệ71,91/14,04/14,04%. Train đủ8 lớp; validation thiếu an_uong/di_chuyen/suc_khoe, test thiếu an_uong/di_chuyen/khac. Không retry fold/seed hoặc phá nhóm để đủ lớp.
- Lock bám raw snapshot/provenance/recipe, guideline section2, config/môi trường và implementation. Đọc lại recompute expected và so byte cả lock; sửa hash trong lock không hợp thức hóa manifest đã sửa. `--write` temp+rename, không overwrite; lỗi giữa ghi không để target locked. Từ chối symlink/junction/reparse point trước resolve. `load_split_ids` chỉ cấp train IDs sau verify; feature tiếp theo phải fit riêng train.
- 12 candidate gần trùng, chưa người duyệt; bốn cặp chưa xác nhận vẫn giao partition. Audit overlap pass chỉ cho khóa/quan hệ đã khai báo, không chứng nhận mọi rò rỉ ngữ nghĩa. Khóa prototype không khóa test thật, không đủ kết luận nghiên cứu tám lớp.

## Lệnh đã dùng ở mốc code hiện tại

Chạy trong checkout riêng của phiên bản học, dùng `.venv` của checkout đó:

```powershell
.\.venv\Scripts\python.exe -B scripts/check_environment.py
.\.venv\Scripts\python.exe -B scripts/preview_transactions.py examples/transactions_sample.csv --month 2026-10
.\.venv\Scripts\python.exe -B scripts/build_seed_dataset.py
.\.venv\Scripts\python.exe -B scripts/validate_dataset.py data/seed/v0.1/expense_descriptions_vi.csv
.\.venv\Scripts\python.exe -B scripts/demo_baselines.py
.\.venv\Scripts\python.exe -B scripts/split_dataset.py
.\.venv\Scripts\python.exe -B -m pytest -q
```

CSV mẫu: 9 giao dịch tháng 10, thu 5.000.000, chi 2.593.000, chênh lệch 2.407.000 VND; một khoản chi cần xác nhận danh mục. Builder báo reproduced_exactly và 356/0 thật. Tests đã chạy được ghi ở VERIFICATION; người học chạy lại là bằng chứng thực hành mới, không sửa kết quả mốc cũ.

Mốc TASK-07: suite đạt 139 tests + 11 subtests; 10 fit_examples/13 probes, score null, chưa split/chưa đánh giá. QA xác minh lỗi combining mark/surrogate đã sửa; test fixture 100.001 byte dùng ID ngắn để không vượt giới hạn biến môi trường Windows. Fixture/rule hash, môi trường, seed và kết quả chi tiết ở [evidence](evidence/TASK-07-2026-10-05/qa_review.md). Kiểm tra phần mềm này không đo hiệu quả mô hình hoặc mức hiểu.

Mốc TASK-08: suite đạt **193 tests + 11 subtests**, thêm54 case. `split_dataset.py --write` thực trả created, chạy mặc định sau đó verified_existing; bundle có356 mô tả hư cấu, không fit/metric. QA đóng finding dòng nguồn0 và Windows junction; full suite kiểm tra namespace/bắc cầu/tái lập, tamper manifest+lock, stale snapshot, không overwrite, fsync failure, staging collision, CLI preview và guideline thiếu marker. [Evidence](evidence/TASK-08-2026-10-05/qa_review.md) ghi giới hạn và support thật của prototype. `.venv` import/pip check vẫn PASS, không thêm dependency.

Máy được đọc lại local: Windows 11 Pro 64-bit, Ryzen 5 7500F 6 core/12 thread, RAM khoảng 31,7 GiB. [Hardware/environment](evidence/TASK-07-2026-10-05/hardware.json) ghi dung lượng trống và lock hash; `.venv` Python 3.14.7/sklearn 1.9.1 import/pip check đạt, không thêm dependency hoặc sửa Python toàn hệ thống. Chưa benchmark train/inference.

## Chưa triển khai và đầu vào còn thiếu

TASK-07 DONE và TASK-08 split prototype Verified; chưa có TF-IDF + NB/LR, model binary/card nghiên cứu, SQLite hoặc Streamlit UI; chưa có dữ liệu/test thật và metric ML. Consent, nhãn/quan hệ người duyệt, rubric trường, thời gian mỗi tuần và chính sách máy dùng chung còn thiếu. TASK-03 do luồng học quản lý, không chặn code. TASK-04/05–06/08 giữ REVIEW phần thiếu; P2/P3 In progress, P4–P6 Planned.

## Hướng tiếp theo

Dự án: TASK-09 TF-IDF feature/Pipeline prototype đủ hợp đồng đầu vào; lấy ID train qua verify rồi fit, giữ rõ nhãn AI/holdout thiếu lớp và chưa test thật. Không gọi audit bởi AI là người đã duyệt quan hệ/nhãn. Đánh giá chính thức vẫn cần dữ liệu được phép/người duyệt. TASK-13 SQLite đủ hợp đồng từ TASK-04 để tiếp tục độc lập khi thu dữ liệu nghiên cứu còn chờ.

Mentor: chọn SHA cố định, đọc `ml/baselines.py`, CLI/fixture và tests mới để tạo phần học riêng; không cần gửi tin nhắn sang chat khác. Các mục tiêu `.80/.60/.85` chưa đo. Không tự train lại từ sửa nhãn app và không nạp joblib không rõ nguồn.

Khi dự án thay đổi, cập nhật bảng đầu ra, các quyết định/lệnh/kết quả/giới hạn và thông báo commit mới. Mentor khóa SHA của buổi học trong Learn để tránh học nhầm phiên bản. Bàn giao không bao gồm dữ liệu thật, credentials hay binary model riêng tư.
