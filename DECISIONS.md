# Sổ quyết định — phiên bản 0.1

Ngày: 05/10/2026. Dùng file này để tránh biến một đề xuất kỹ thuật thành yêu cầu đã được xác nhận.

## Đã được người dùng xác nhận

| ID | Quyết định | Căn cứ |
|---|---|---|
| D01 | Làm sản phẩm giải quyết nhu cầu thực tế và phục vụ đồ án tốt nghiệp | Câu trả lời vòng 1 |
| D02 | Lĩnh vực tài chính, chọn trợ lý quản lý chi tiêu cá nhân | Chọn phương án A |
| D03 | Người dùng đầu tiên gồm sinh viên và người mới đi làm | Trả lời vòng 2: nhóm 1 và 2 |
| D04 | MVP nhập tay và nhập CSV theo mẫu | Trả lời vòng 2 |
| D05 | AI chính: phân loại mô tả khoản chi tiếng Việt | Trả lời vòng 2 |
| D06 | Cần tự huấn luyện mô hình, ngành học Trí tuệ nhân tạo | Thông tin học tập |
| D07 | Ngân sách hiện tại 0 đồng; cần kế hoạch dùng công cụ miễn phí | Ràng buộc người dùng |
| D08 | Có nhiều thời gian; chưa có hạn nộp hoặc số giờ/tuần cụ thể | Thông tin thời gian |
| D09 | Cần nhóm với vai trò khác nhau và tài liệu giải thích để học, bảo vệ | Yêu cầu người dùng |
| D10 | Có tư duy lập trình cơ bản nhưng cần ôn kỹ thuật code | Thông tin năng lực |
| D11 | Bài học/bài tập/nhật ký ở Krev1/Learn; repo Krev1/spendwise-ai giữ phần dự án | Yêu cầu phân tách repo ngày 05/10/2026 |
| D12 | Chuyển repository dự án sang công khai | Yêu cầu người dùng ngày 05/10/2026 |

## Đề xuất kỹ thuật cho bản khởi đầu

| ID | Đề xuất/giả định | Cách kiểm chứng hoặc thay đổi |
|---|---|---|
| A01 | Tên tạm SpendWise AI | Có thể đổi tên, giữ nguyên mục tiêu |
| A02 | MVP local, một người dùng trên mỗi bản cài; máy có CPU và quyền cài Python | P1 kiểm tra máy; chưa giả định RAM/GPU cụ thể |
| A03 | Python + Streamlit + SQLite + scikit-learn | P1 kiểm tra phiên bản tương thích, khóa dependency sau lần cài thành công |
| A04 | 8 danh mục khoản chi | Pilot với 3–5 người; nếu thay nhãn phải cập nhật dataset, spec và model version |
| A05 | Baseline từ khóa và DummyClassifier; thử TF-IDF + Naive Bayes, Logistic Regression | Đánh giá cùng split và bộ nhãn, chọn bằng validation |
| A06 | Ngưỡng điểm mô hình khởi đầu 0.60 | Chọn trên validation, ghi coverage và sai số; không gọi là xác suất dự đoán đúng |
| A07 | Mục tiêu nghiên cứu ban đầu: macro-F1 ≥0.80; coverage ≥0.60; selective accuracy ≥0.85 | Chưa đo; thảo luận lại dựa trên pilot, dữ liệu và rubric trước khi khóa test |
| A08 | Mục tiêu thu thập khoảng 1.200 mô tả, khoảng 150/lớp; test thực tối thiểu 20 mô tả khác nhau/lớp | Phụ thuộc quyền dữ liệu, người tham gia và phân bố; không nhân bản mẫu để đủ số |
| A09 | Lộ trình tham khảo khoảng 10–12 tuần | Chạy theo mốc, kéo dài hoặc rút gọn sau P1; không phải cam kết thời hạn |
| A10 | “Nhóm” là các vai trò hỗ trợ AI cộng với bạn là chủ đồ án | Có thể phân vai cho người thật nếu bạn có nhóm; chưa tuyển hoặc liên hệ ai |

P1 đã kiểm tra môi trường local: Windows 11 Pro 64-bit, Ryzen 5 7500F, RAM khoảng 31,7 GiB hiển thị, Python 3.14.7. Bộ thư viện trong requirements.lock.txt import được và ví dụ đạt 14 test. Đây là xác minh setup; chưa đo tốc độ train/inference hoặc độ chính xác AI.

Người học đã chọn tài khoản GitHub kết nối thứ hai. GitHub xác nhận ID `293179070`, username hiện hành `Krev1`. Ban đầu tạo repository riêng tư `Krev1/spendwise-ai`; người dùng sau đó yêu cầu chuyển công khai và tách bài học sang `Krev1/Learn`.

## Hợp đồng chung giữa các tài liệu

- **Danh mục khoản chi:** `an_uong`, `di_chuyen`, `nha_o_hoa_don`, `hoc_tap`, `mua_sam`, `giai_tri`, `suc_khoe`, `khac`.
- **CSV giao dịch:** `transaction_id,date,transaction_type,amount_vnd,description,category`.
- `transaction_type`: `income` hoặc `expense`; `amount_vnd` là số nguyên dương VND, tối đa `1_000_000_000_000`; ngày `YYYY-MM-DD`.
- Khoản thu có `category` trống. Khoản chi có thể chưa có nhãn khi nhập, nhưng phải có nhãn được người dùng xác nhận trước khi lưu.
- Gợi ý AI luôn cần xác nhận. Nhãn `khac` không đồng nghĩa mô hình đã nhận biết được mọi đầu vào ngoài miền.
- **Dataset nghiên cứu riêng:** `record_id,description,label,group_id,source,is_synthetic`; không lấy số tiền hoặc thu nhập làm đầu vào mô hình phân loại văn bản.
- CSV hợp lệ tối đa 5.000 dòng dữ liệu, 2.000.000 byte; ID ổn định dài 1–64 ký tự chữ ASCII, số, `_`, `-`; mô tả 1–300 ký tự sau loại khoảng trắng ở đầu/cuối.
- Import lại so `source_payload_hash` của input canonical trước AI/xác nhận; không so nhãn hiện tại sau người dùng sửa. Cùng ID/cùng nguồn thì bỏ qua; cùng ID/nguồn khác thì từ chối toàn batch.
- Các danh mục, giới hạn dữ liệu và mục tiêu chất lượng trên là thiết kế đề xuất, có thể sửa có ghi lý do.

## Thông tin cần bổ sung khi làm

1. Rubric, format báo cáo và yêu cầu thí nghiệm của giảng viên/trường.
2. CPU, RAM, dung lượng đĩa và giờ học mỗi tuần.
3. Người tự nguyện thử ứng dụng và cung cấp mô tả đã ẩn danh.
4. Kết quả pilot: người dùng có tiết kiệm thời gian phân loại không, nhãn nào khó phân biệt?

Các thông tin này không ngăn việc ôn Python, tạo môi trường và thử định dạng CSV. Khi ảnh hưởng đến phạm vi, cập nhật đúng tài liệu liên quan trước khi viết phần code phụ thuộc.

## Mẫu ghi thay đổi

```text
Ngày:
Quyết định cũ:
Quyết định mới:
Lý do và bằng chứng:
REQ / TASK / dataset / model bị ảnh hưởng:
Ai quyết định:
Cách kiểm tra sau thay đổi:
```

## A11 — Seed dữ liệu hư cấu có nguồn — 05/10/2026

Người dùng yêu cầu thu thập/xây dataset và hướng dẫn ở Learn. Chọn seed nhỏ có truy vết, không thay mục tiêu dữ liệu thật bằng hàng loạt câu AI. Đã thu 100 hàng demo hư cấu từ nguồn MIT tại commit cố định; chuyển ngữ 19 mô tả được chọn, tự soạn 160 câu nền và thêm biến thể không dấu. Tổng 356 câu, 0 thật; mọi nhãn `ai_draft`. Giữ 33 nhóm phụ thuộc, chưa split/train.

Thêm `public_synthetic` với cờ `true` vào schema nguồn. Nguồn hư cấu không có nhãn sẵn; bản dịch/nhãn chưa được con người duyệt. Repo dự án giữ dataset/build/validate/provenance, Learn giữ phương pháp, biểu mẫu và bài tập. Đây là lựa chọn khởi động kỹ thuật, chưa xác nhận taxonomy với pilot hoặc dữ liệu thật đủ đại diện.

## D13 — Triển khai độc lập, học bám dự án — 05/10/2026

Người dùng yêu cầu tách việc làm dự án và việc học. Luồng kỹ thuật tiếp tục SDD trong spendwise-ai, không chờ người học hoàn thành bài và không viết bài học trong Learn. Luồng học chỉ ghi Learn/spendwise-ai, đọc code/bàn giao theo commit để giải thích, tạo bài tập và phản biện. Mỗi mốc kỹ thuật cập nhật docs/PROJECT_HANDOFF.md; Mentor chọn SHA cố định cho buổi học và thực hành trên checkout riêng.

Tiến độ kỹ thuật và mức hiểu độc lập. Consent, nhãn người duyệt và quyết định phạm vi vẫn cần bằng chứng; không thay bằng AI. REQ-13 được hoàn tất qua luồng học và bàn giao, không còn là điều kiện chờ bài tự làm trước mỗi task kỹ thuật. Sẵn sàng bảo vệ vẫn phụ thuộc hiểu của người học và rubric thật. Không tạo chat/automation hoặc nhắn sang chat khác trong lần cập nhật này.

## A12 — Hợp đồng prototype baseline TASK-07 — 05/10/2026

B1 dùng guideline miền; B0 là `DummyClassifier(strategy="most_frequent", random_state=42)`. Đây là lựa chọn kỹ thuật của luồng dự án, không thay consent hoặc nhãn người duyệt.

B1 giữ NFC/chữ thường/gộp khoảng trắng và giữ dấu; không dấu chỉ khớp alias khai báo. Khớp nguyên từ/cụm theo ranh giới Unicode. Xét hit dài trước (số token, số ký tự, thứ tự rule); loại hit ngắn bị chứa hoàn toàn trong hit đã giữ. Hit độc lập thuộc nhiều lớp trả `khac/conflict`; không hit trả `khac/no_match`. Hai trường hợp cần xem lại, không phải bằng chứng nhận biết ngoài miền. Rule có version và hash nội dung/thứ tự. Không sửa rule theo test.

B0 chỉ nhận descriptions/labels do caller chỉ định, không nhận ID/nguồn/nhóm/tiền làm feature; kiểm tra trước fit. TASK-07 chỉ fit fixture hư cấu riêng trong bộ nhớ, không fit toàn seed, không sinh split/model binary/metric. TASK-10 phải dùng train của manifest TASK-08. Cả hai baseline không xuất score giả hoặc xác nhận thay người dùng; chưa tích hợp app.

Ảnh hưởng: REQ-09,13; design 9.2; data_and_ml 6; TASK-07. Kiểm chứng Unicode, cụm lồng nhau, xung đột, không khớp, B0 và CLI read-only; bàn giao theo D13.

## A13 — Grouped split prototype TASK-08 — 05/10/2026

Chỉ khóa partition kỹ thuật của seed hư cấu, không khóa test thật hoặc xác nhận nhãn. Audit 356 hàng/33 nhóm/51 họ câu cho thấy biến thể khác dấu giữ nhóm; thiếu dữ liệu thật và người rà soát gần trùng. CLI chỉ đọc seed/provenance/recipe trong repo, không nhận dataset riêng.

Nhóm hiệu lực là union bắc cầu của group gốc, family và original phrase có namespace `(source_id, source_commit)`, folded text và quan hệ ghi trong recipe riêng. Ba cặp cùng dịch vụ qua nguồn được giữ chung để tránh tách biến thể có thể phụ thuộc; status `ai_conservative_prototype`, `human_reviewed=false`. Đây là ngoại lệ chỉ cho prototype hư cấu: không gọi là người đã xác nhận quan hệ, không áp dụng cho nghiên cứu thật. Không nối các câu chỉ vì cùng lớp hoặc vài từ chung.

Screen gần trùng trên đại diện folded: SequenceMatcher ≥0.70 hoặc token Jaccard ≥0.50 hoặc char-3 Jaccard ≥0.40; bổ sung chứa nguyên cụm từ ít nhất 2 token/8 ký tự. Đại diện chọn theo ID sort, cặp so theo folded lexicographic; SequenceMatcher có thể phụ thuộc chiều so sánh, nên thứ tự này là một phần protocol. Đây là heuristic để lập danh sách cần người rà soát, không chứng minh quan hệ ngữ nghĩa. Prototype giới hạn 500 văn bản folded để chặn chi phí audit cặp tăng bậc hai. Rule/recipe và ngưỡng được khóa trước fit; chưa có fit hoặc metric ở task này.

Chia một lần bằng `StratifiedGroupKFold(n_splits=7, shuffle=True, random_state=42)` trên ID đã sort và nhóm hiệu lực: fold 0 là test prototype, fold 1 validation, 5 fold còn lại train. Tỷ lệ danh nghĩa 5/7,1/7,1/7 gần 70/15/15; báo tỷ lệ thực và support/missing labels, không đổi seed/fold để làm đẹp điểm. Nhóm quan trọng hơn tỷ lệ; đủ 8 lớp ở các holdout với tỷ lệ 15% không khả thi với cấu trúc nhóm seed hiện tại.

Bundle có input hashes, config/môi trường/guideline version/hash, manifest và audit; ghi qua thư mục tạm rồi rename, không overwrite bundle khác nội dung. Mặc định chỉ preview/verify; `--write` mới tạo bundle. Đọc lại phải đối chiếu hash và partition tái tạo, phát hiện file thiếu/thừa/sửa; không tin lock đã bị sửa cùng manifest. Đường dẫn bundle/cha và file con không dùng symlink, Windows junction hoặc reparse point. Dòng nguồn công khai cần số dòng CSV canonical từ 2, tối đa 9 chữ số. Không nạp model binary. TASK-08 giữ REVIEW cho nghiên cứu nếu còn thiếu human review hoặc support; prototype có thể kiểm chứng riêng. Ảnh hưởng REQ-08,09,13 và TASK-08–12/22.
