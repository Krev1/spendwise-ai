# Tiến độ ban đầu

Cập nhật: 05/10/2026. Đọc cùng [bằng chứng kiểm tra](VERIFICATION.md) và [kế hoạch](docs/03_implementation_plan.md).

| Mốc | Trạng thái | Bằng chứng hiện có / việc tiếp theo |
|---|---|---|
| P0 — Bộ SDD phiên bản 0.1 | Verified | Có bộ SDD, sổ quyết định và prompt; tài liệu học/bảo vệ được chuyển sang Learn; đã đối chiếu hợp đồng và liên kết. Đây là draft kỹ thuật, chưa phải phê duyệt đề tài của trường. |
| P1 — Môi trường kỹ thuật | Verified | TASK-02 đã kiểm tra `.venv`, import, pip check, dependency lock và ví dụ. 14 test PASS ở mốc setup. TASK-03/mức hiểu theo dõi riêng ở Learn, không chặn triển khai. |
| P2 — Dữ liệu và baseline | In progress | TASK-07 prototype B0/B1 DONE; [bằng chứng](docs/evidence/TASK-07-2026-10-05/pytest.txt): 139 tests + 11 subtests, seed 356 hư cấu/0 thật tái tạo đúng byte. TASK-04/05–06 giữ REVIEW; nhãn người duyệt và dữ liệu thật còn thiếu. Xem [bảng task](docs/04_team_workflow.md#7-bảng-trạng-thái-task-kỹ-thuật) và [bàn giao](docs/PROJECT_HANDOFF.md). |
| P3 — Huấn luyện và validation | In progress | [TASK-08](docs/tasks/TASK-08.md) prototype Verified: train256/validation50/test50, 30 nhóm hiệu lực; 193 tests + 11 subtests. Nghiên cứu giữ REVIEW vì nhãn/quan hệ chưa người duyệt và holdout thiếu lớp. Chưa có Pipeline NB/LR hoặc điểm ML. |
| P4 — SQLite và nghiệp vụ | Planned | Chưa có database hoặc services của ứng dụng. |
| P5 — Giao diện và tích hợp AI | Planned | Chưa có ứng dụng Streamlit. |
| P6 — Pilot, test cuối và bảo vệ | Planned | Chưa có kết quả test/pilot hoặc báo cáo đồ án hoàn chỉnh. |

Các task chi tiết dùng trạng thái trong tài liệu nhóm. `Verified` của một mốc chỉ áp dụng cho đầu ra được ghi ở cột bằng chứng; không có nghĩa người học đã hiểu hoặc giảng viên đã duyệt.

## Việc tiếp theo

1. TASK-08 prototype đã Verified, nghiên cứu giữ REVIEW. Tiếp theo TASK-09: TF-IDF feature/Pipeline prototype, fit riêng ID train từ bundle đã verify. Chưa đủ consent/nhãn người duyệt/test thật cho đánh giá chính thức; TASK-13 SQLite có thể tiếp tục độc lập sau TASK-04.
2. Cập nhật [bàn giao kỹ thuật](docs/PROJECT_HANDOFF.md) sau mỗi mốc và báo commit cho người dùng/Mentor.
3. Consent, dữ liệu thật, nhãn người duyệt và rubric cần được cung cấp thực tế. Tiếp tục task độc lập đủ đầu vào; không bịa phần thiếu.
4. Luồng học riêng dùng [prompt Mentor](https://github.com/Krev1/Learn/blob/main/spendwise-ai/MENTOR_PROMPT.md); mức hiểu/bài tự làm chỉ ghi trong Learn.

## Nhật ký cập nhật tiếp theo

Ghi ngày, TASK/REQ, file thay đổi, lệnh chạy, kết quả thực, kiến thức tự giải thích và việc còn lại. Giữ lịch sử thay vì thay mọi ô thành `Verified` khi chỉ mới tạo file.

## Khởi động GitHub — 05/10/2026

- Người học chọn tài khoản kết nối có ID `293179070`; username GitHub hiện hành `Krev1`.
- Repository lúc khởi tạo còn riêng tư: `https://github.com/Krev1/spendwise-ai`.
- Môi trường local Windows 11 Pro 64-bit, AMD Ryzen 5 7500F (6 core/12 thread), RAM khoảng 31,7 GiB hiển thị, Python 3.14.7.
- Import các dependency thành công; `pip check` không báo xung đột.
- pytest: 14 passed; unittest: 14 tests OK; CSV tháng 10 cho tổng đã ghi trong VERIFICATION.
- Chưa có câu trả lời/bài tự làm từ người học, chưa train mô hình hoặc đánh giá chất lượng AI.


## Tách bài học — 05/10/2026

- Theo D11/D12, bài học, lộ trình, hướng dẫn bảo vệ, bài tập và nhật ký học chuyển sang [Krev1/Learn](https://github.com/Krev1/Learn/tree/main/spendwise-ai).
- Repo dự án giữ code, test, SDD, dependency, prompt kỹ thuật và bằng chứng; cập nhật các tham chiếu sang Learn.
- Thay đổi này chỉ tổ chức tài liệu; trạng thái ứng dụng, dữ liệu và mô hình vẫn như bảng mốc ở trên.


## TASK-04 — Domain và CSV preview — 05/10/2026

- [Task card](docs/tasks/TASK-04.md) ghi phạm vi, REQ và tiêu chí chấp nhận; trạng thái REVIEW.
- Tách implementation sang `src/spendwise/domain/` và `src/spendwise/services/`; thêm CLI, API đọc bytes, test ranh giới hợp đồng và vị trí dòng CSV.
- Có bài 02/bài tập trong Learn. Chưa có bài tự làm hoặc câu trả lời từ người học; không đánh dấu TASK-03 DONE.
- Hướng dẫn tiếp theo: người học làm bài 01; phần kỹ thuật tiếp theo là TASK-05–06.

## TASK-05–06 — Dataset khởi đầu — 05/10/2026

- Thu snapshot 100 hàng hư cấu có MIT notice tại commit nguồn cố định; 19 mô tả được chuyển ngữ. 160 câu nền tự tạo, biến thể bỏ dấu giữ cùng nhóm.
- Seed v0.1: 356 mô tả, 33 nhóm, 0 thật, nhãn `ai_draft`; không có người duyệt độc lập. Có recipes, provenance, audit và source selection từng dòng.
- Builder tái tạo offline khớp byte; kiểm tra nguồn trực tuyến khớp hai hash. Test hiện tại 86 passed, 11 subtests passed; không sinh model/metric/split.
- [Task card](docs/tasks/TASK-05-06.md) đang REVIEW phần kỹ thuật. Learn có phương pháp, quy tắc nhãn, template trống và bài thực hành.
- Tiếp theo: người học rà 20 câu và giải thích, pilot thu thật riêng tư, gán nhãn độc lập. TASK-07 baseline tiếp tục sau khi hiểu hợp đồng; không chờ đủ 1.200 thật mới học kỹ thuật.

## D13 — Tách luồng dự án và học — 05/10/2026

Cập nhật AGENTS, prompt, SDD/REQ-13, phụ thuộc TASK-04 và bàn giao kỹ thuật. Tiến độ dự án chỉ ghi kỹ thuật; học theo commit ở Learn. Mốc P1 kỹ thuật Verified dựa bằng chứng đã có, không xác nhận TASK-03 hoặc mức hiểu. Lần này chỉ đổi workflow/tài liệu; không thêm baseline/model/DB/UI và không chạy lại kiểm tra code không đổi. Hai prompt thuộc hai luồng, không tự tạo chat hoặc automation.

## TASK-07 — Baseline prototype — 05/10/2026

- Đọc đủ tài liệu bắt buộc/SDD/examples trong checkout dự án mới nhất `6d28c6a`; không thiếu tài liệu ở checkout được chọn, không sửa checkout cũ hoặc Learn.
- Trước code: 86 tests + 11 subtests; builder khớp byte; seed 356 hư cấu, 33 nhóm, 0 thật, hash giữ nguyên. Sau code: 139 tests + 11 subtests PASS, QA review/probe hoàn tất.
- B1 có version/hash, Unicode boundary, ưu tiên hit dài chứa hit ngắn, conflict/no_match cần review. B0 chỉ fit 10 ví dụ hư cấu riêng, không fit seed/probes. CLI chỉ đọc/in JSON, không metric/split/model binary.
- [Evidence](docs/evidence/TASK-07-2026-10-05/qa_review.md), [task card](docs/tasks/TASK-07.md), [bàn giao](docs/PROJECT_HANDOFF.md), [code commit b331e5f](https://github.com/Krev1/spendwise-ai/commit/b331e5f078a07a73e34d44f22da69d89774eae96). P2 chưa Verified vì dữ liệu người duyệt/thu thật còn thiếu; P3–P6 vẫn Planned.
- Máy được đọc local: Windows 11 Pro 64-bit, Ryzen 5 7500F 6 core/12 thread, RAM khoảng 31,7 GiB; dung lượng trống lúc kiểm tra ở [hardware.json](docs/evidence/TASK-07-2026-10-05/hardware.json). `.venv` Python 3.14.7, lock import/pip check PASS. Chưa đo tốc độ train/inference; còn thiếu rubric, thời gian mỗi tuần và chính sách máy dùng chung.

## TASK-08 — Grouped split prototype — 05/10/2026

- A13/design/task contract ghi trước implementation; chỉ sửa repo dự án, không viết Learn hoặc đổi nhãn seed. Root sở hữu file, Data Engineer/QA chỉ đọc/probe.
- Union bắc cầu namespace family/lineage/folded/ba link AI bảo thủ; SGKF7/seed42 một lần. Bundle manifest/audit/lock đã tạo và verify lại; code [b5afb11c7bfc9133d6c94d986a5727363e43e1fc](https://github.com/Krev1/spendwise-ai/commit/b5afb11c7bfc9133d6c94d986a5727363e43e1fc).
- **193 tests + 11 subtests PASS**, 54 case mới; source_row và Windows junction finding đã sửa/probe lại. [Evidence](docs/evidence/TASK-08-2026-10-05/qa_review.md) ghi kết quả thật.
- Seed356/0 thật/0human-reviewed giữ nguyên hash. Split256/50/50,30 nhóm hiệu lực; train đủ8 lớp, validation thiếu an_uong/di_chuyen/suc_khoe, test thiếu an_uong/di_chuyen/khac. Có12 candidate gần trùng còn pending human review, trong đó4 cặp chưa xác nhận giao partition; không gọi overlap pass là chứng nhận ngữ nghĩa.
- Prototype Verified; TASK-08 REVIEW nghiên cứu, P2/P3 In progress. Không fit model/vectorizer hoặc đo metric, không đánh dấu mức hiểu. Tiếp theo TASK-09 feature prototype với train đã verify hoặc TASK-13 SQLite độc lập.
