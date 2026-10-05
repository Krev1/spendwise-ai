# TASK-08 — QA và audit thực chạy

Ngày 05/10/2026; code [b5afb11c7bfc9133d6c94d986a5727363e43e1fc](https://github.com/Krev1/spendwise-ai/commit/b5afb11c7bfc9133d6c94d986a5727363e43e1fc). Root tích hợp, Data Engineer và QA subagent chỉ đọc/probe trong tempfile. Đây là review AI/phần mềm, không phải human annotation hoặc thẩm định của trường.

## Kết quả kiểm tra

- `.venv\Scripts\python.exe -B -m pytest -q`: **193 passed, 11 subtests passed**; [log đầy đủ](pytest.txt). Riêng 54 case mới của split/CLI đạt trước suite đầy đủ.
- Case có ý nghĩa: metadata thiếu/trùng/stale hash/nhãn lineage xung đột; source commit/dòng/transformation; UTF-8/header/size và giới hạn CPU; nhóm family–lineage bắc cầu, namespace khác nguồn; dữ liệu thật bị từ chối; mỗi ID một split và khóa quan hệ không giao; đổi thứ tự input tái lập manifest/audit, lock vẫn bám raw snapshot.
- Bundle tạo/verify/load ID; sửa assignment/label, sửa cả manifest và hash lock, file thiếu/thừa/stale input đều bị từ chối. Existing bundle khác byte giữ nguyên. Disk failure ở lần fsync thứ hai không publish target; target xuất hiện lúc staging được giữ nguyên. CLI preview từ cwd khác không ghi, lỗi không in success hoặc echo nội dung file bị sửa; không có override input private.
- Windows junction được tạo thật trong tempfile để kiểm tra root/ancestor bị từ chối trước resolve. QA từng tái hiện source_row=0 và junction vượt is_symlink; code đã sửa, probe lại đóng hai finding. Dòng2 hợp lệ; 0/1/leading zero/non-ASCII/chuỗi số rất dài bị SplitError. Guideline thiếu một trong hai marker bị từ chối.
- QA độc lập trong nhóm chạy probe union bắc cầu/namespace, đảo input, tamper assignment và normal write/verify/load256/50/50. Không còn finding trong phạm vi đã review; chưa kiểm chứng đa nền tảng hoặc mọi tình huống filesystem đồng thời.
- [Environment](environment.json) xác nhận `.venv`, Python3.14.7/sklearn1.9.1; [pip check](pip_check.txt) không xung đột. Không thay dependency hoặc Python toàn hệ thống. Lock ghi cả numpy và hash implementation/normalizer.
- [Kiểm tra cuối](verification_checks.json): 24 file Markdown/124 liên kết file nội bộ, UTF-8/code fence và AST Python đạt; bundle sau cập nhật tài liệu vẫn verified, hash code staged/normalizer khớp lock. Không dùng việc kiểm tra tài liệu để thay test ML.

## Audit dữ liệu và giới hạn

[Creation](split_creation.json) thực trả created; [verification](split_verification.json) trả verified_existing. Bundle đúng ba file được version trong `data/splits/seed-v0.1-prototype/`. Dataset/provenance/recipes seed chính giữ nguyên; hash dataset vẫn `537e48b08ba3bc6022bc09cfa8e0cf8944ea2b652a7a66906ad297d745c362f6`.

| Tập | Hàng | Nhóm hiệu lực | Unique folded | Lớp thiếu |
|---|---:|---:|---:|---|
| Train | 256 | 20 | 129 | Không |
| Validation | 50 | 5 | 25 | an_uong, di_chuyen, suc_khoe |
| Test prototype | 50 | 5 | 25 | an_uong, di_chuyen, khac |

356 hư cấu, 0 thật/human-reviewed; 33 nhóm gốc, 30 nhóm hiệu lực, 51 family, 179 lineage/unique folded. Nhóm lớn nhất67 hàng do public group37 và ba nhóm tự tạo10 hàng được co-locate bảo thủ. Tỷ lệ71,91/14,04/14,04%; không retry seed/fold.

12 candidate gần trùng: ba giao nguồn cùng component, chín cùng nguồn chưa được người xác nhận; trong chín này, bốn giao partition và năm tình cờ cùng split. Agent audit recipe-order ban đầu thấy11; đối chiếu phát hiện SequenceMatcher phụ thuộc chiều so sánh của cặp `seed_suc_khoe_xet_nghiem_02`/`seed_suc_khoe_thuoc_05` (.642857 hoặc .75). Implementation dùng folded lexicographic cố định nên12 là số tái lập; không đổi threshold để đồng nhất audit cũ. Heuristic lexical không chứng minh quan hệ ngữ nghĩa.

Ba link Steam/phim/clinic mang `ai_conservative_prototype,false`; các câu chỉ chung từ không được tự nối. `partition_overlap_check=passed_for_declared_keys_and_links`, `semantic_relationship_review=pending_human_review`, `eight_class_partition_complete=false`, `real_evaluation_ready=false`, `research_metrics=not_run`. Không fit model/vectorizer, không dùng accuracy/macro-F1 giả.

Prototype kỹ thuật Verified; TASK-08 nghiên cứu REVIEW vì nhãn/semantic review/consent/test thật/support chưa đủ. TASK-09 có thể dùng ID train đã verify để thử feature kỹ thuật; không kết luận chất lượng tám lớp từ các holdout này.
