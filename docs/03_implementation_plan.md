# SpendWise AI — Kế hoạch triển khai

Ngày soạn: 05/10/2026. Phiên bản: 0.1. Trạng thái: kế hoạch cho việc viết code sau bộ SDD; chưa tuyên bố ứng dụng hay mô hình đã hoàn thành.

Kế hoạch nối `01_requirements.md` → `02_design.md` → task nhỏ → code/dữ liệu → kiểm tra → bằng chứng → giải thích bằng tiếng Việt. Cách phối hợp các vai trò nằm trong `04_team_workflow.md`; nội dung AI chi tiết trong `05_data_and_ml.md`; bài học được lưu riêng ở Learn, xem [tài liệu học trong Learn](https://github.com/Krev1/Learn/blob/main/spendwise-ai/learning_path.md).

## 1. Cách triển khai

Người học là Project Owner và tác giả đồ án. Các vai trò AI hỗ trợ phân tích, thiết kế, viết code, review và giải thích; chúng không thay thế việc người học chạy thử, kiểm tra nhãn, hiểu thuật toán hoặc xác minh rubric với giảng viên. Có thể dùng một AI lần lượt đóng các vai trò, không bắt buộc trả phí hoặc chạy nhiều agent đồng thời.

Mỗi lượt làm một task nhỏ hoặc một nhóm task có chung hợp đồng. Trước khi code, đọc REQ, design và tiêu chí chấp nhận của task. Sau khi code, chạy kiểm tra phù hợp, ghi kết quả thật, cập nhật trạng thái và tạo phần học tương ứng. Nếu bằng chứng yêu cầu đổi hợp đồng, sửa spec/design/task trước hoặc cùng lúc với code liên quan.

**Có sẵn trong bộ khởi động:** tài liệu SDD và ví dụ Python thư viện chuẩn kiểm tra CSV/tính tổng để ôn lập trình. Ví dụ này chỉ đọc/kiểm tra file và tính số liệu; chưa nhập SQLite, chưa huấn luyện mô hình và chưa phải ứng dụng Streamlit. Kiểm tra README để chạy đúng file thực tế trong bộ khởi động.

**Sẽ tạo khi triển khai:** môi trường riêng, mã nguồn ứng dụng, database, scripts ML, mô hình, báo cáo thí nghiệm và bảy file giải thích theo task. Không coi file có tên trong cây thiết kế là file đã tồn tại.

## 2. Các mốc P0–P6

| Mốc | Kết quả chính | Điều kiện ra khỏi mốc |
|---|---|---|
| P0 — Đặc tả và thiết kế | Bộ SDD, scope, schema, vai trò, giả định | Các tài liệu dùng cùng 8 slug, CSV contract, quy tắc xác nhận và REQ IDs; task đầu có thể thực hiện |
| P1 — Môi trường và Python | Chạy ví dụ nhỏ, hiểu hàm/exception/số nguyên | Tạo được venv, chạy ví dụ, giải thích được vì sao tổng tiền không dùng AI |
| P2 — Dữ liệu và baseline | Guideline nhãn, dữ liệu có nguồn, validator, baseline prototype | Dataset được kiểm tra; synthetic/real được phân biệt; baseline giải thích được; chưa dùng điểm demo để kết luận thực tế |
| P3 — Split, train và validation | Pipeline tự train, thí nghiệm so sánh, chọn model/ngưỡng bằng validation | Có manifest split, kết quả validation thật, artifact và model card; không xem test để chọn cấu hình |
| P4 — SQLite và nghiệp vụ | Nhập/sửa/xoá, tổng hợp, import nguyên tử | Các invariant tiền/danh mục/ID giữ đúng, rollback và reimport được kiểm chứng |
| P5 — Ứng dụng và AI | Streamlit nối nghiệp vụ, mô hình và CSV preview | Luồng sử dụng chạy được trên máy, AI lỗi vẫn nhập tay, rerun không tạo dòng trùng |
| P6 — Kiểm chứng và bảo vệ | Pilot, test cuối, tái lập, báo cáo và demo | Đối chiếu REQ bằng bằng chứng; phân tích kết quả thật, giới hạn và đóng góp của người học |

Chưa biết số giờ mỗi tuần hoặc cấu hình máy, nên chưa gắn deadline. Có thể hình dung khung học 10–12 tuần để chia nhỏ công việc, rồi kéo dài từng mốc theo tốc độ học và dữ liệu thu thập được. Đây là nhịp tham khảo, không phải cam kết tiến độ. Tiến độ thu dữ liệu thật cần được theo dõi riêng; nhiều thời gian code không tự tạo ra tập test đại diện.

## 3. Danh sách task và phụ thuộc

Các vai trò dưới đây dùng cùng định nghĩa trong `04_team_workflow.md`. Với mỗi task, người triển khai mở rộng thành một task card có phạm vi file, lệnh chạy và nơi lưu bằng chứng. Những task chưa thực hiện có trạng thái `TODO`; bản kế hoạch không đánh dấu `DONE` thay cho kết quả chạy.

### P0 — Đặc tả trước khi viết app

| Task | Vai trò chính | Phụ thuộc / REQ | Đầu ra và tiêu chí hoàn tất |
|---|---|---|---|
| TASK-01 — Rà soát SDD và giả định | Orchestrator + Architect | Các câu trả lời của người học; REQ-01…13 | Kiểm tra yêu cầu, design và kế hoạch cùng schema/slug; ghi máy và rubric chưa biết. Mỗi REQ có ít nhất một task và cách kiểm chứng. |

**Phạm vi file:** tài liệu SDD, task registry, nhật ký quyết định. Chưa tạo app đầy đủ. Nếu chưa có rubric, ghi việc người học cần đối chiếu; vẫn tiếp tục setup và kiến thức nền độc lập.

### P1 — Môi trường và ôn Python

| Task | Vai trò chính | Phụ thuộc / REQ | Đầu ra và tiêu chí hoàn tất |
|---|---|---|---|
| TASK-02 — Kiểm tra máy, tạo venv và khoá phụ thuộc | Developer + Mentor | TASK-01; REQ-11,12,13 | Ghi OS/CPU/RAM/Python; tạo venv trong project; kiểm tra import thư viện đã chọn; lưu phiên bản thực tế sau kiểm tra vào lock file. Không cài vào Python hệ thống để giải quyết lỗi project. |
| TASK-03 — Ôn Python qua giao dịch nhỏ | Mentor | TASK-02; REQ-01,06,13 | Chạy ví dụ CSV có sẵn; tự thêm/sửa khoản chi và dự đoán tổng trước khi chạy; xử lý tiền âm/0/thập phân. Viết `Learn/spendwise-ai/lessons/01_python_and_money.md` bằng kết quả thực. |

**Phạm vi file:** cấu hình môi trường, requirements, ví dụ học, file giải thích 01. Chỉ chốt phiên bản Python/package khi đã thử môi trường thật. Lưu lệnh Windows PowerShell có thể sao chép; nếu activate bị policy chặn, dùng đường dẫn `venv` Python trực tiếp thay vì hướng dẫn tắt bảo vệ toàn máy.

### P2 — Hợp đồng dữ liệu và dữ liệu có nhãn

| Task | Vai trò chính | Phụ thuộc / REQ | Đầu ra và tiêu chí hoàn tất |
|---|---|---|---|
| TASK-04 — Tạo domain và validator giao dịch | Developer | TASK-03; REQ-01,04,06 | Quy tắc ngày, VND, mô tả, thu/chi, ID 1–64 ký tự ASCII chữ/số/`_`/`-` và 8 slug nằm trong domain. CSV parser hỗ trợ UTF-8/BOM và dấu nháy; trả lỗi theo dòng; không ghi database. Kiểm tra các ranh giới hợp đồng. |
| TASK-05 — Guideline nhãn và provenance | Data Engineer + ML Researcher | TASK-04; REQ-08,13 | Quy định 8 danh mục và trường hợp mơ hồ; schema dataset 6 cột; quy trình đồng ý, loại PII và kiểm tra nhãn. Bài 02b và phương pháp/guideline trong `Learn/spendwise-ai/`; bài 02 trước đó giải thích CSV giao dịch. |
| TASK-06 — Dataset validator và thu thập phiên bản đầu | Data Engineer | TASK-05; REQ-08,09 | Script xác thực ID/label/group/source/is_synthetic; báo phân bố lớp, số nhóm phụ thuộc, số mẫu thật/tự viết/công khai hư cấu. Nhãn AI dự thảo ghi riêng, không tự coi là người duyệt. Dataset demo đánh dấu synthetic; ghi snapshot/hash. Tiếp tục thu dữ liệu thật được đồng ý trong các mốc sau. |
| TASK-07 — Prototype baseline | ML Researcher + Mentor | TASK-05,06; REQ-09,13 | Viết bộ từ khoá có thứ tự ưu tiên và `DummyClassifier`. Dùng ví dụ nhỏ để hiểu hành vi; chưa báo điểm test. Giải thích câu có nhiều từ khoá, câu không có từ khoá và lớp phổ biến. |

**Phạm vi file:** `src/spendwise/domain/`, `src/spendwise/data/`, parser/service kiểm tra CSV, scripts build/collect/validate, dữ liệu demo/provenance/manifest; phương pháp/guideline và bài 02b trong Learn. Dữ liệu thật nằm ngoài Git.

**Điểm kiểm tra dữ liệu:** không bắt buộc có ngay đủ dữ liệu thật để chạy smoke test. Tuy nhiên thí nghiệm trên câu tự viết chỉ là bước học kỹ thuật. Trước kết luận về dùng thực tế cần holdout thật theo `05_data_and_ml.md`; nếu chưa đủ, trạng thái bằng chứng phải ghi đúng.

### P3 — Tự huấn luyện và lựa chọn bằng validation

| Task | Vai trò chính | Phụ thuộc / REQ | Đầu ra và tiêu chí hoàn tất |
|---|---|---|---|
| TASK-08 — Đóng băng grouped split | Data Engineer + ML Researcher | TASK-06; REQ-08,09 | `group_id` của real là mã người, synthetic là nguồn/khuôn; audit `pattern_family_id` trong manifest riêng; hợp nhất nhóm liên quan thành thành phần hiệu lực. Chia train/validation/test khoảng 70/15/15, seed 42; khóa test ID/nhóm; báo số mẫu/lớp và sai lệch tỷ lệ. Kiểm tra người/nhóm/ID/trùng/gần trùng không giao nhau. |
| TASK-09 — TF-IDF và pipeline | ML Researcher + Mentor | TASK-08; REQ-09,13 | Chuẩn hoá văn bản nhất quán; thử word/char features trên train/validation theo recipe nhỏ. Vocabulary/IDF chỉ fit train. Tạo `Learn/spendwise-ai/lessons/03_text_features.md` với ví dụ ma trận nhỏ. |
| TASK-10 — Train và so sánh các ứng viên | ML Researcher | TASK-07,08,09; REQ-09 | Chạy rules, Dummy, TF-IDF + NB, TF-IDF + LR trên cùng split. Lưu cấu hình, seed, môi trường và metrics validation thực. Không chọn sẵn model thắng hoặc tự điền metrics. |
| TASK-11 — Chọn ngưỡng và phân tích lỗi validation | ML Researcher + QA Reviewer | TASK-10; REQ-09,10 | Dùng validation chọn model/tham số/ngưỡng; phân tích lỗi theo lớp và coverage/selective accuracy. 0,60 là khởi điểm thử, không ngưỡng có sẵn bằng chứng. Tạo `Learn/spendwise-ai/lessons/04_training_and_evaluation.md`. |
| TASK-12 — Xuất artifact và khoá recipe | ML Researcher + Architect | TASK-11; REQ-03,07,09,10 | Lưu pipeline + metadata/hash/class order và model card; chạy load/predict round-trip. Chọn artifact để tích hợp. Ghi rõ chưa đánh giá test cuối nếu chưa chạy; không tạo số test giả để đủ file. |

**Phạm vi file:** `src/spendwise/ml/`, scripts split/train/evaluate, config/manifest/artifact báo cáo và file giải thích 03–04. Không sửa kết quả test để thuận tiện train. Các artifact có dự đoán/mô tả thật cần kiểm tra quyền riêng tư trước khi chia sẻ.

**Giới hạn thí nghiệm:** khởi đầu grid nhỏ, dữ liệu nhỏ và một run đơn giản; đo thời gian/RAM thực rồi mới mở rộng. Không dùng transformer/GPU hoặc dịch vụ cloud trong MVP. Model đã train ở đây phục vụ thử luồng; test cuối và kết luận nghiên cứu là TASK-22.

### P4 — SQLite và logic tài chính

| Task | Vai trò chính | Phụ thuộc / REQ | Đầu ra và tiêu chí hoàn tất |
|---|---|---|---|
| TASK-13 — Schema, migrations và repository | Developer + Architect | TASK-04; REQ-01,02,07,12 | Bảng giao dịch/batch/prediction/lịch sử theo design; bật FK; SQL có tham số; CHECK invariant; migration chạy được trên database trống và không làm mất bản cũ. |
| TASK-14 — CRUD và báo cáo tiền | Developer | TASK-13; REQ-01,02,06,07 | Nhập/sửa/xoá mềm; lọc khoảng ngày/loại/danh mục; tổng theo tháng bằng số nguyên; lưu lịch sử sửa nhãn. Mở lại database còn dữ liệu, khoản thu không có nhãn khoản chi. |
| TASK-15 — Import service nguyên tử và idempotent | Developer + QA Reviewer | TASK-04,13,14; REQ-04,05,07 | Canonical source hash trước AI/confirmation; preview không ghi DB; duplicate ID nội bộ lỗi; existing same source skip; diff source rollback cả batch. Thử lỗi giữa chừng và reimport sau sửa nhãn. |
| TASK-16 — Backup, restore và giải thích SQLite | Developer + Mentor | TASK-13,14,15; REQ-12,13 | Hướng dẫn backup nhất quán/restore bản copy, `.gitignore` dữ liệu cá nhân, log không chứa mô tả đầy đủ. Tạo `Learn/spendwise-ai/lessons/05_sqlite_and_import.md`. |

**Phạm vi file:** repositories/migrations, services giao dịch/import/report, tests nghiệp vụ, hướng dẫn backup và file giải thích 05. Không dùng model để tạo số tiền, sửa ngày hoặc xác định tổng.

P4 có thể bắt đầu sau TASK-04 khi việc thu dữ liệu/huấn luyện P3 còn đang diễn ra, vì chỉ phụ thuộc hợp đồng. Nếu làm song song, phần SQLite và phần ML có chủ sở hữu file riêng; cùng thống nhất slug/schema trước khi ghép.

### P5 — Giao diện và tích hợp mô hình

| Task | Vai trò chính | Phụ thuộc / REQ | Đầu ra và tiêu chí hoàn tất |
|---|---|---|---|
| TASK-17 — Form, danh sách và dashboard Streamlit | Developer | TASK-14; REQ-01,02,06,13 | UI tiếng Việt gọi services; form nhập tay và xác nhận; lọc danh sách; sửa/xoá; dashboard/tháng trống. Rerun không lặp thao tác ghi. |
| TASK-18 — Inference, phiên bản và fallback | Developer + ML Researcher | TASK-12,17; REQ-03,07,10,11 | Cache model theo version/hash, trả đúng slug từ `classes_`; score/threshold/model version hiển thị và audit; lỗi model vẫn chọn thủ công. Sửa mô tả làm gợi ý/xác nhận cũ hết hiệu lực. |
| TASK-19 — CSV preview, chọn nhãn và commit | Developer + QA Reviewer | TASK-15,17,18; REQ-04,05,07 | UI kết nối import service; dòng lỗi hiển thị rõ; mọi khoản chi được rà soát trước commit; file/input đổi làm draft cũ hết hiệu lực. Skip không chạy AI lại và không ghi đè nhãn đã sửa. |
| TASK-20 — Thử luồng local/offline và hướng dẫn app | QA Reviewer + Mentor | TASK-16,18,19; REQ-01…07,10,11,12,13 | Thử luồng tổng thể với dữ liệu demo, Internet tắt, model thiếu/hỏng, khởi động lại và backup. Ghi kết quả thực, đo latency trên máy, tạo `Learn/spendwise-ai/lessons/06_app_and_model.md`. |

**Phạm vi file:** `app.py`, `src/spendwise/ui/`, inference adapter và tests tích hợp cần thiết; cập nhật README/cấu hình local. Không thêm API, ngân hàng hay tính năng đăng nhập để hoàn tất mốc.

### P6 — Đánh giá cuối và bảo vệ

| Task | Vai trò chính | Phụ thuộc / REQ | Đầu ra và tiêu chí hoàn tất |
|---|---|---|---|
| TASK-21 — Pilot chức năng với người dùng mục tiêu | Product Analyst + QA Reviewer | TASK-20; REQ-01…07,11,12 | Nhờ người thử là sinh viên/người mới đi làm, có đồng ý; quan sát nhập/CSV/sửa nhãn/đọc báo cáo. Ghi lỗi và nhận xét thực, không tự tạo phản hồi người dùng. Dữ liệu pilot không tự trở thành train/test. |
| TASK-22 — Đánh giá model trên test đã khoá | ML Researcher + QA Reviewer | TASK-08,12; REQ-08,09,10 | Chạy recipe đã khoá trên holdout độc lập; báo toàn test và từng lớp, baseline, confusion matrix, coverage/selective accuracy, số mẫu thật/lớp và giới hạn. Nếu test chưa đủ, ghi chưa đủ bằng chứng; không điều chỉnh ngưỡng theo test. |
| TASK-23 — Tái lập và review theo REQ | QA Reviewer + Architect | TASK-20,22; REQ-01…13 | Dựng lại venv từ lock, chạy train/evaluate và app bằng hướng dẫn; so manifest/metric trong sai số được mô tả; đối chiếu từng REQ với bằng chứng. Lỗi quan trọng được sửa và chỉ chạy lại phần bị tác động. |
| TASK-24 — Báo cáo, demo và luyện bảo vệ | Project Owner + Mentor | TASK-21,22,23; REQ-09,13 | Báo cáo có vấn đề, liên quan, dataset, thuật toán, thí nghiệm, sản phẩm, giới hạn/đóng góp; demo dùng dữ liệu hư cấu; đối chiếu rubric thật; tạo `Learn/spendwise-ai/lessons/07_experiments_and_defense.md`. Người học tự trình bày và trả lời câu hỏi bằng code/kết quả. |

**Phạm vi file:** báo cáo/pilot được đồng ý, kết quả đánh giá, model card, task registry, checklist demo và file giải thích 07. Không sửa corpus test hoặc dùng mục tiêu `.80/.60/.85` như số đo. Nếu sau test có thay đổi model để nghiên cứu tiếp, ghi đó là vòng mới và chuẩn bị một holdout mới cho kết luận độc lập.

## 4. Ma trận kiểm chứng có ý nghĩa

Đây là các tình huống cần viết test hoặc thực hiện có bằng chứng khi triển khai, chưa phải danh sách test đã chạy. Unit tests kiểm tra quy tắc xác định; integration tests kiểm tra SQLite và luồng UI; đánh giá AI dùng dataset riêng và metrics, không thay thế bằng test một vài câu ví dụ.

| Nhóm | Tình huống và kết quả cần chứng minh | Task / REQ |
|---|---|---|
| Tiền | `0`, âm, thập phân, ký hiệu tiền, vượt `1e12` bị từ chối; `1` và `1e12` hợp lệ; tổng thu/chi/chênh lệch đúng bằng số nguyên | 04,14 / 01,06 |
| Ngày và lọc | 30/02 bị từ chối; ngày nhuận hợp lệ; ranh giới 30/09, 01/10, 31/10, 01/11; tháng trống bằng 0; ngày tương lai hợp lệ vẫn lưu theo hợp đồng | 04,14,17 / 01,02,06 |
| Loại và danh mục | Income không có category; expense phải được xác nhận; slug sai bị từ chối; score thấp không tự gán `khac` | 04,18,19 / 01,03,04,10 |
| CSV cấu trúc | BOM, LF/CRLF, mô tả dấu phẩy có nháy; header sai/thừa/thiếu, ID thiếu, mô tả rỗng/dài, dòng trống, encoding lỗi và quá 2 MB/5.000 dòng | 04,19 / 04 |
| Chống trùng | Cùng ID trong batch bị từ chối; cùng nguồn đổi tên file skip; cùng ID khác amount/date/description/input category thì cả batch lỗi; hai ID khác cùng nội dung vẫn là hai dòng | 15,19 / 05 |
| Nhãn đã sửa | CSV ban đầu category rỗng → xác nhận → sửa nhãn → reimport nguồn giống: số dòng không tăng, nhãn đã sửa giữ nguyên | 15,19 / 05,07 |
| Nguyên tử | Batch có một dòng mới và một xung đột không ghi dòng mới; ép lỗi khi ghi dòng thứ hai rollback tất cả; lịch sử/batch không tồn tại một phần | 15 / 05,07 |
| Lưu bền và backup | Đóng/mở app còn giao dịch; backup/restore bản copy ra cùng danh sách và tổng; dữ liệu riêng không nằm trong Git | 16,20 / 12 |
| UI và audit | Rerun không lưu hai lần; đổi mô tả xoá gợi ý cũ; xác nhận khác predicted label vẫn giữ cả hai; đổi nhãn tạo thêm lịch sử | 17,18,19 / 02,03,07 |
| AI fallback | Model thiếu/hỏng/schema sai vẫn nhập tay/CSV được; không gọi dịch vụ ngoài; offline chạy đủ luồng chính | 18,20 / 03,11 |
| Leakage | Người cung cấp/ID/nhóm hiệu lực không giao nhau; câu gần trùng/template chung được audit và gom; feature chỉ fit train; seed/manifest tái lập; test không tham gia chọn model/ngưỡng | 08,09,23 / 08,09 |
| Metrics thật | Báo support từng lớp; macro-F1 gồm mọi mẫu, cả score thấp; coverage riêng; accepted set rỗng thì selective accuracy chưa xác định; không dùng nhãn cuối đã sửa làm accuracy dự đoán thô | 11,22 / 09,10 |

Không cần viết test cho mỗi câu chữ tài liệu hoặc mỗi widget hiển thị đơn giản. Tập trung test vào tiền, lưu dữ liệu, chống trùng, atomicity, trạng thái xác nhận và leakage. Sau khi kiểm tra phù hợp đã pass, chỉ mở rộng/chạy lại khi có thay đổi, lỗi hoặc vấn đề chưa giải quyết.

## 5. Quy tắc bằng chứng và hoàn tất task

Một task được đánh dấu `DONE` khi có kết quả đáp ứng tiêu chí, đã chạy kiểm tra cần thiết, tài liệu khớp code và người học có file giải thích/bài tập phù hợp. Nếu chưa có dữ liệu, môi trường hoặc người thử, ghi đầu vào còn thiếu và tiếp tục task độc lập; không điền dữ liệu/feedback/metric tưởng tượng.

Mỗi task lưu bằng chứng tối thiểu:

- Task ID và REQ liên quan; phạm vi file thay đổi.
- Lệnh hoặc thao tác đã chạy, ngày chạy, phiên bản môi trường/dataset/model khi liên quan.
- Kết quả thực, vị trí log/báo cáo hoặc ảnh demo được phép chia sẻ.
- Một giải thích bằng lời của người học, một bài tập tự sửa và điểm còn chưa hiểu.
- Vấn đề còn lại và ảnh hưởng đến task tiếp theo.

Mẫu file học bắt buộc lấy từ [tài liệu học trong Learn](https://github.com/Krev1/Learn/blob/main/spendwise-ai/learning_path.md). Đặt cùng nội dung giải thích từng module/hàm trọng tâm, vì sao chọn cách làm, lỗi thường gặp, lệnh Windows và kết quả quan sát. Không viết sẵn câu trả lời “tôi đã hiểu” thay người học.

## 6. Điều kiện hoàn tất dự án

**Sản phẩm:** các REQ nhập/sửa/xoá/CSV/dashboard/audit/local đã kiểm chứng trên máy mục tiêu; import không làm tăng tổng do reimport; mô hình lỗi vẫn nhập thủ công; hướng dẫn setup/backup hoạt động.

**Nghiên cứu:** có dữ liệu với provenance, grouped split và holdout độc lập, baseline, mô hình tự train, recipe tái lập, metrics thực, phân tích lỗi và model card. Không đạt mục tiêu chất lượng vẫn phải được phân tích trung thực. Nếu thiếu test thật đại diện, kết luận giới hạn ở bằng chứng hiện có và ghi chưa đủ bằng chứng dùng thực tế.

**Học và bảo vệ:** đủ bảy file giải thích tạo theo tiến độ; người học chạy lại được thí nghiệm và demo, giải thích kiến trúc/TF-IDF/mô hình/leakage/metrics/transaction và xác định đóng góp của mình. Yêu cầu chính thức của trường phải được đối chiếu, vì chưa có rubric trong cuộc trao đổi.

Hoàn thành bộ SDD khởi động không đồng nghĩa hoàn thành các điều kiện trên. Code và các kết quả đánh giá được tạo theo từng mốc sau khi dùng prompt khởi động của bộ tài liệu.


Bài tập theo mốc nằm ở [Learn/spendwise-ai/mentor_guide.md](https://github.com/Krev1/Learn/blob/main/spendwise-ai/mentor_guide.md). Các đường dẫn `Learn/spendwise-ai/lessons/` trong task là đầu ra ở repo Learn, không phải thư mục con của repo dự án. Bài 00/01 đã soạn; các bài còn lại tạo khi triển khai task.


## Tiến độ TASK-04

Xem [task card](tasks/TASK-04.md): phần kỹ thuật đã kiểm tra, đang REVIEW. TASK-03 vẫn cần bài tự làm của người học; phần kỹ thuật TASK-04 được chuẩn bị theo yêu cầu bắt đầu triển khai, không thay bằng chứng học tập. Kế hoạch mốc P2 gồm cả guideline, dataset và baseline nên chưa hoàn tất.
