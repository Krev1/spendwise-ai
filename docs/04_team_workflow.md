# 04 — Hai luồng làm việc và workflow SDD

Quyết định D13, ngày 05/10/2026: **dự án triển khai độc lập; việc học bám code và kết quả của dự án**. Các vai trò AI hỗ trợ chủ đồ án, không phải nhân sự đã được tuyển hoặc thẩm định của giảng viên.

## 1. Phạm vi và quyền ghi

| Luồng | Vai trò | Được sửa | Đầu ra |
|---|---|---|---|
| Dự án | Orchestrator, Product Analyst, Data Engineer, ML Researcher, Architect/Developer, QA | Krev1/spendwise-ai | Spec, design, task, code, test, dữ liệu được phép, bằng chứng và bàn giao |
| Học | Mentor/Defense Coach và người học | Krev1/Learn/spendwise-ai | Bài học, bài tập, lời giải của người học, nhật ký, câu hỏi bảo vệ và liên kết commit |

Project Owner quyết định phạm vi, cung cấp rubric/quyền dữ liệu và các bằng chứng cần người; đồng thời tự thực hành trong luồng học. AI soạn nhãn không trở thành người gán nhãn độc lập. Mỗi luồng chỉ đọc repo bên kia; không cùng sửa code dự án hoặc môi trường thực thi.

Trong luồng dự án có thể phân vai tuần tự; khi được giao dùng subagent, chia file sở hữu và tích hợp sau review. Không cần trả phí API để app/classifier chạy local. Mentor dùng prompt riêng; không tự triển khai tính năng sản phẩm trong chat học.

## 2. Chu trình kỹ thuật độc lập

```text
REQ/tiêu chí chấp nhận → thiết kế → task/phụ thuộc → code/dữ liệu
                     → kiểm tra → bằng chứng/commit → bàn giao
```

Trước code xác định REQ, đầu vào và hợp đồng. Đổi hành vi thì cập nhật spec/design/DECISIONS trước hoặc cùng thay đổi phụ thuộc. QA chỉ ghi pass khi có kiểm tra thật; review tĩnh phải ghi giới hạn. Có thể làm task độc lập tiếp theo khi task trước đã đủ hợp đồng kỹ thuật, dù người học chưa học phần đó.

Thiếu consent, dữ liệu thật, nhãn người duyệt, quyết định phạm vi hoặc tài nguyên vẫn là thiếu đầu vào thật. Ghi task bị ảnh hưởng, không thay bằng dữ liệu/đồng ý giả. Tiếp tục các task đủ đầu vào; không tuyên bố đạt chất lượng AI thật từ seed hư cấu.

## 3. Bàn giao từ dự án sang học

Mỗi mốc cập nhật [PROJECT_HANDOFF.md](PROJECT_HANDOFF.md): TASK/REQ, code đã có, file/hàm trọng tâm, lý do thiết kế, lệnh kiểm tra, kết quả thực, hạn chế và task tiếp theo. Thay đổi code được commit theo quyền đã được giao; người triển khai báo SHA cho người dùng. Đây là đầu vào của Mentor, không phải bài giảng hoặc bằng chứng người học hiểu.

Mentor đọc bàn giao tại một commit đã publish, đối chiếu code/test và ghi SHA đầy đủ vào lesson/nhật ký. Chọn phiên bản đang học trước khi chạy; không tự đổi phiên bản giữa buổi khi dự án tiến lên. Khi bắt đầu buổi mới, kiểm tra bàn giao/commit mới và bổ sung lộ trình. Nếu chưa truy cập nguồn thì báo rõ, không tự đoán nội dung.

Đồng bộ bằng repo/bàn giao/commit, không cần tự gửi tin nhắn qua chat khác. Đây không phải cấu hình theo dõi hay tự động chạy nền. Người dùng có thể mở chat học và yêu cầu đọc bàn giao mới.

## 4. Chu trình học theo bằng chứng dự án

```text
Bàn giao/commit → kiến thức cần ôn → giải thích code và quyết định
               → thực hành trên bản riêng → tự trình bày → phản hồi Mentor
```

Mentor có thể đi chậm hơn tiến độ code. Test dự án pass không chứng minh người học hiểu. Ghi mức hiểu chỉ sau lời giải/bài tự làm thật. Bài học tương lai chỉ soạn lý thuyết có ghi trạng thái; không viết rằng tính năng chưa có đã được triển khai.

Thực hành cần sửa code hoặc ghi database/model dùng checkout và môi trường riêng trong Learn/spendwise-ai/practice/, bị Git ignore. Giữ repo triển khai và `.venv` kỹ thuật của nó khỏi sửa đổi bởi bài tập. Quy trình chi tiết ở [Learn — hai luồng](https://github.com/Krev1/Learn/blob/main/spendwise-ai/study_workflow.md).

Nếu phát hiện lỗi, ghi ID task, commit, lệnh tái hiện, expected/actual trong phản hồi học; gửi qua người dùng để luồng dự án xử lý. Mentor không tự sửa sản phẩm. Phần bài tập nhỏ do người học viết không được ghi thành tính năng đã hoàn tất.

## 5. Trạng thái tách biệt

`progress.md` dự án phản ánh kỹ thuật: Planned/In progress/Verified theo đầu ra và bằng chứng. Task dùng TODO/DOING/REVIEW/DONE/BLOCKED; BLOCKED chỉ là task thiếu đầu vào cụ thể. Reviewer phải kiểm tra tiêu chí task, không lấy việc người học chưa trả lời làm lý do chặn code.

`Learn/spendwise-ai/progress.md` ghi tài liệu đã soạn và mức hiểu riêng. Sẵn sàng bảo vệ vẫn cần người học trình bày, kết quả nghiên cứu trung thực và rubric của trường; hoàn thành code không tự đáp ứng điều này.

## 6. Mẫu task và bàn giao

```text
TASK / REQ:
Vai trò kỹ thuật / file sở hữu:
Đầu vào và phụ thuộc kỹ thuật:
Hợp đồng / tiêu chí chấp nhận:
Lệnh đã chạy / kết quả thực:
File, hàm và quyết định trọng tâm:
Dataset/model version nếu có:
Giới hạn / thiếu đầu vào:
Commit được publish:
Task kỹ thuật tiếp theo:
```

Prompt [dự án](../prompts/START_HERE.md) và [Mentor](https://github.com/Krev1/Learn/blob/main/spendwise-ai/MENTOR_PROMPT.md) dùng riêng. Không ghi điểm số, dữ liệu thật, consent hoặc mức hiểu khi chưa có bằng chứng.

## 7. Bảng trạng thái task kỹ thuật

Cập nhật 05/10/2026. Trạng thái mốc tổng hợp ở [progress](../progress.md); bảng này giữ trạng thái chi tiết, không đánh giá mức hiểu.

| TASK | Trạng thái | Bằng chứng / đầu vào còn thiếu |
|---|---|---|
| 01 | DONE | SDD draft và D13; chưa có rubric trường |
| 02 | DONE | [VERIFICATION](../VERIFICATION.md), môi trường riêng/lock import được |
| 03 | TODO | Thuộc luồng học, không chặn code |
| 04 | REVIEW | [Task card](tasks/TASK-04.md), domain/CSV/reports; giữ trạng thái trước |
| 05 | REVIEW | [Task card](tasks/TASK-05-06.md), guideline/provenance; nhãn người duyệt chưa có |
| 06 | REVIEW | [Task card](tasks/TASK-05-06.md), seed/validator; 0 mẫu thật |
| 07 | DONE | [Task card](tasks/TASK-07.md), prototype B0/B1; 139 tests + 11 subtests, QA review; chưa đánh giá ML |
| 08 | TODO | Grouped split/audit hiệu lực, chưa có manifest |
| 09 | TODO | TF-IDF Pipeline, cần TASK-08 |
| 10 | TODO | So sánh B0/B1/NB/LR, cần 07–09 |
| 11 | TODO | Chọn model/ngưỡng bằng validation, cần 10 |
| 12 | TODO | Artifact/model card, cần 11 |
| 13 | TODO | SQLite schema/migrations, đủ hợp đồng TASK-04 |
| 14 | TODO | CRUD/reports, cần 13 |
| 15 | TODO | Atomic import/source hash, cần 13–14 |
| 16 | TODO | Backup/restore, cần 13–15 |
| 17 | TODO | Streamlit form/dashboard, cần 14 |
| 18 | TODO | Inference/fallback, cần 12/17 |
| 19 | TODO | UI import/xác nhận, cần 15/17/18 |
| 20 | TODO | Local/offline end-to-end, cần 16/18/19 |
| 21 | TODO | Pilot có consent/người thử, cần 20 |
| 22 | TODO | Test cuối đã khóa + dữ liệu thật/người duyệt, cần 08/12 |
| 23 | TODO | Tái lập và review REQ, cần 20/22 |
| 24 | TODO | Báo cáo/rubric và trình bày người học, cần 21–23 |
