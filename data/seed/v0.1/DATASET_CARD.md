# SpendWise Vietnamese expense descriptions — v0.1

Ngày: 05/10/2026. TASK-05–06, REQ-08/09/13. **356 mô tả hư cấu; 0 mẫu thật; toàn bộ nhãn là `ai_draft`, chưa có người duyệt độc lập.** Dùng cho học kỹ thuật, kiểm tra pipeline và demo. Không dùng làm bằng chứng phân loại chi tiêu thực tế.

## Nội dung và đầu vào

File chính: [expense_descriptions_vi.csv](expense_descriptions_vi.csv), đúng sáu cột ML. Đầu vào classifier tương lai chỉ là `description`; `label` là mục tiêu học. ID/nhóm/nguồn/cờ không phải đặc trưng. Không có số tiền, thu nhập hoặc ngày trong file này; đây không phải CSV nhập giao dịch của ứng dụng.

| Nhãn | Số mô tả, gồm biến thể |
|---|---:|
| `an_uong` | 48 |
| `di_chuyen` | 50 |
| `giai_tri` | 46 |
| `hoc_tap` | 40 |
| `khac` | 40 |
| `mua_sam` | 43 |
| `nha_o_hoa_don` | 45 |
| `suc_khoe` | 44 |

Có 319 mẫu `author_synthetic` từ 160 câu nền do trợ lý AI soạn, thuộc 32 họ kịch bản; 37 mẫu `public_synthetic` từ 19 bản chuyển ngữ. Biến thể bỏ dấu tạo thêm 177 hàng, không thêm 177 quan sát độc lập. Hai câu không có dấu sẵn không được nhân bản. 356 câu khác nhau theo NFC/lowercase/gộp khoảng trắng; 179 câu khác nhau nếu bỏ dấu. Có 33 nhóm phụ thuộc; không có người tham gia thật. Nhóm nguồn công khai duy nhất chứa nhiều lớp, nên số nhóm/lớp không cộng thành tổng nhóm.

## Thu thập và nguồn gốc

Đã lưu toàn bộ 100 hàng CSV demo tại [snapshot nguồn](../../reference/pfa_demo_transactions.csv), kèm [manifest nguồn](../../reference/source_manifest.json) và [MIT notice](../../reference/LICENSE.pfa.txt). [Repository nguồn tại commit cố định](https://github.com/lakshitrajput21/personal-finance-analyzer/tree/5d727c66bf2beba91a54d5cda043b6b2eca97ec3) mô tả demo là hư cấu. Giấy phép ở cấp repo là MIT; chưa thấy giấy phép dataset riêng. Giữ nguyên notice của tác giả khi tái phân phối. Copyright trong nguồn ghi Surabhi Pradhan; không suy ra tác giả từ tên tài khoản GitHub.

Nguồn tiếng Anh, USD, không có cột nhãn. Dự án không quy đổi tiền, không gọi nó là dữ liệu Việt Nam. Trong 100 dòng: 6 dòng thu/hoàn tiền bị loại; 52 dòng chưa đủ rõ/không có ánh xạ được loại; 23 dòng cùng mô tả sau bỏ mã demo gộp vào bản canonical; 19 dòng được chọn chuyển ngữ. Xem quyết định **từng dòng** ở [source_selection.csv](source_selection.csv). Các mô tả chỉ tên cửa hàng như CVS/Target không được tự suy ra mua thuốc/đồ gì. Tên Netflix vẫn có suy luận theo thương hiệu, nên nhãn/bản dịch cần người rà soát.

Nguồn có sẵn nhãn: **không**. Quyền tái sử dụng nguồn không chứng nhận chất lượng nhãn. Nhãn và bản dịch là dự thảo do AI hỗ trợ theo guideline của dự án; số người gán nhãn, số bất đồng được giải quyết và số người duyệt đều bằng 0. Các câu thiếu ngữ cảnh lớp `khac` giả lập tình huống đã hỏi nhưng không bổ sung được, không phải phản hồi người thật.

## Kiểm tra, phiên bản và tái lập

- [provenance.csv](provenance.csv): 356 ID khớp file chính; trạng thái nhãn, họ câu, biến đổi, hash văn bản chuẩn hóa, dòng/commit nguồn và lý do nhãn.
- [audit_report.json](audit_report.json): số lớp/nguồn/nhóm, số thật/tự tạo, hash recipe và kết quả kiểm tra cấu trúc.
- Recipes: [câu tự tạo](../../recipes/seed_phrases.csv), [ánh xạ chuyển ngữ](../../recipes/public_adaptations.csv). Các file hư cấu này được version trong Git; sửa chúng phải xây lại snapshot và rà diff.
- SHA-256 file chính UTF-8/LF: `537e48b08ba3bc6022bc09cfa8e0cf8944ea2b652a7a66906ad297d745c362f6`. Hash kiểm tra tính toàn vẹn, không chứng minh nhãn đúng.

Chạy từ root repo dự án trong `.venv`:

```powershell
.\.venv\Scripts\python.exe -B scripts/collect_reference.py
.\.venv\Scripts\python.exe -B scripts/build_seed_dataset.py
.\.venv\Scripts\python.exe -B scripts/validate_dataset.py data/seed/v0.1/expense_descriptions_vi.csv
```

Hai lệnh đầu mặc định chỉ đối chiếu, không tải mạng/ghi file. `collect_reference.py --verify-online` đọc lại đúng hai file nguồn tại commit cố định để so hash. Builder `--write` ghi lại bốn file seed/audit khi chủ động sửa recipes; không dùng cho dữ liệu thật. Newline LF được khai báo để tái tạo trên Windows. Không có bước tải/execute code hay model pickle của bên thứ ba.

## Giới hạn và sử dụng tiếp

TASK-08 đã tạo [grouped split prototype](../../splits/README.md) riêng: 256 train/50 validation/50 test hư cấu, 30 nhóm hiệu lực; dataset/provenance v0.1 giữ nguyên byte. Validation/test thiếu lớp; nhãn và quan hệ vẫn chưa có người duyệt. Chưa train hoặc có metric. Câu do AI soạn có thể đơn giản, lặp từ đặc trưng và không đại diện ngôn ngữ sinh viên/người mới đi làm. Biến thể bỏ dấu là nhân tạo; không đại diện lỗi gõ tự nhiên. Các nhóm chỉ ngăn quan hệ đã biết; chưa có audit gần trùng ngữ nghĩa của người.

Validator đã kiểm tra ID/nhãn/nguồn/cờ, trùng chuẩn hóa, biến thể khác dấu giao nhóm và cấu trúc. Không có cảnh báo email/URL/chuỗi số dài ở file chính; bộ dò này không nhận diện được mọi PII hay chứng nhận đã ẩn danh. Nhãn cần người học rà theo [guideline](../../../docs/05_data_and_ml.md). Thu mô tả thật tự nguyện, giữ riêng người và khóa test thật trước khi kết luận chất lượng. Chi tiết phương pháp, template và bài tập ở [Learn](https://github.com/Krev1/Learn/blob/main/spendwise-ai/guides/01_dataset_collection.md).

Giấy phép cho phần dữ liệu hư cấu do dự án tạo: [MIT](../../LICENSE.txt). Phần thích nghi từ nguồn giữ thêm notice tại `data/reference/LICENSE.pfa.txt`. Dữ liệu thật tương lai có consent/quyền riêng, không tự áp dụng giấy phép của seed.
