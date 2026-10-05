# TASK-07 — QA và bằng chứng

Ngày: 05/10/2026 (Asia/Saigon). REQ-09,13; A12/D13. Code: `b331e5f078a07a73e34d44f22da69d89774eae96`.

QA subagent được giao chỉ đọc/probe trong repo dự án. Root sở hữu và tích hợp toàn bộ thay đổi. Đây là review bởi AI, không thay nhãn người duyệt hoặc phản biện giảng viên.

## Đã chạy

- `.venv` Python `-B`: probe Unicode NFC/NFD/hoa/thường/khoảng trắng, cụm lồng nhau, keyword độc lập xung đột, no-match, equal-span/overlap.
- B0 fit với majority lệch lớp; probe không đổi majority; invalid fit không thay model đã fit; chưa fit báo NotFittedError. Review code xác nhận chỉ descriptions/labels cho Dummy, không metadata/probes.
- CLI subprocess từ cwd khác exit 0/stderr rỗng, 10 fit_examples/13 probes. score null, confirmation true, chưa split/chưa đánh giá; file thiếu exit 1/stdout rỗng, không lộ đường dẫn riêng.
- Root chạy toàn suite sau sửa: **139 passed, 11 subtests passed in 16.53s**, [log](pytest.txt). Thời gian này thuộc test phần mềm, không phải latency mô hình.
- [Demo](demo_baselines.json), [environment](environment.json), [pip check](pip_check.txt), [seed reproduction](seed_reproduction.json), [dataset validation](dataset_validation.json), [CSV preview](csv_preview.json), [hardware](hardware.json) lưu kết quả thực.

## Lỗi đã phát hiện và sửa

1. Ranh giới regex `\w` bỏ qua combining mark còn lại sau NFC: `game\u0338xyz` khớp sai `game`. Sửa kiểm tra token chữ/số/`_`/mark hai phía; QA xác minh ba probe có mark trả no_match, dấu câu hợp lệ vẫn khớp.
2. JSON với escaped surrogate `game\ud800xyz` gây UnicodeEncodeError khi in UTF-8. Từ chối mã Unicode category Cs trước predict/report; kiểm tra lỗi không echo mô tả hoặc in thành công một phần.
3. Test parametrized với bytes 100.001 ký tự tạo `PYTEST_CURRENT_TEST` vượt giới hạn biến môi trường Windows 32.767 ký tự. Rút gọn test ID; payload lớn vẫn được kiểm tra. Lần lỗi: 138 passed/2 errors trước sửa; log cuối chỉ ghi lần thành công.

Không còn finding cần sửa trong phạm vi đã review. B1 chưa đo hiệu quả, rule ngữ cảnh và alias còn giới hạn. B0 chỉ fit fixture demo; chưa có manifest/train nghiên cứu/test thật. Không tạo hoặc nạp model binary, không gửi dữ liệu tài chính ra ngoài.
