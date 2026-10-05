# 04 — Nhóm hỗ trợ AI và workflow SDD

SpendWise AI được thực hiện bởi người học, với các vai trò hỗ trợ AI để chia nhỏ công việc và phản biện kết quả. Đây là mô hình làm việc cho một người chủ đồ án; danh sách vai trò không có nghĩa cần tuyển bảy nhân sự.

Người dùng đầu tiên đã chốt là sinh viên **và** người mới đi làm. Phương thức nhập đã chốt là nhập tay **và** CSV theo mẫu. Bài toán AI đầu tiên đã chốt là phân loại mô tả khoản chi tiếng Việt bằng mô hình người học tự huấn luyện.

## 1. Vai trò và trách nhiệm

| Vai trò | Việc chịu trách nhiệm | Sản phẩm bàn giao | Câu hỏi phải trả lời |
|---|---|---|---|
| **Project Owner — bạn, người chủ đồ án** | Xác định mục tiêu, lấy rubric trường, cho phép sử dụng dữ liệu, chạy bài thực hành và quyết định phạm vi | Quyết định, dữ liệu được phép dùng, nhật ký học và bằng chứng chạy | Tôi có hiểu và tự giải thích được kết quả không? |
| **Orchestrator — AI điều phối** | Giữ tài liệu nhất quán, chia task, xử lý phụ thuộc, ghép kết quả và duy trì trạng thái | Kế hoạch cập nhật, bảng truy vết, tổng hợp vấn đề | Task tiếp theo dựa trên spec nào và đã đủ đầu vào chưa? |
| **Product Analyst — AI phân tích yêu cầu** | Biến nhu cầu thành luồng sử dụng, phạm vi và tiêu chí chấp nhận | Đặc tả yêu cầu, tình huống sử dụng, quyết định phạm vi | Tính năng giải quyết việc cụ thể nào cho ai? |
| **Data Engineer / Annotator — AI hỗ trợ dữ liệu** | Đề xuất schema, quy tắc gán nhãn, làm sạch, tìm trùng và thống kê dữ liệu | Hướng dẫn gán nhãn, dataset card, script kiểm tra, split manifest | Mẫu này có nguồn gì, nhãn vì sao đúng và có leakage không? |
| **ML Researcher — AI hỗ trợ nghiên cứu** | Dựng baseline, chọn đặc trưng/mô hình CPU, thiết kế thực nghiệm và phân tích lỗi | Mã huấn luyện, cấu hình, artifact, báo cáo và model card | Mô hình tốt hơn baseline ở đâu, kém ở đâu và bằng chứng là gì? |
| **Architect / Developer — AI hỗ trợ thiết kế và code** | Thiết kế hợp đồng dữ liệu, database, pipeline; triển khai từng task nhỏ | Tài liệu thiết kế, code, migration/hướng dẫn nếu cần | Quyết định thiết kế đáp ứng REQ nào và có thể kiểm tra thế nào? |
| **QA Reviewer — AI hỗ trợ kiểm tra** | Đọc spec, xem diff, kiểm tra tiêu chí chấp nhận và các trường hợp lỗi | Kết quả kiểm tra, lỗi cụ thể, yêu cầu sửa | Có bằng chứng cho hành vi này hay mới chỉ có lời khẳng định? |
| **Mentor / Defense Coach — AI hỗ trợ học và bảo vệ** | Giải thích kiến thức, tạo bài thực hành, hỏi phản biện theo kết quả thật | Tệp học, câu hỏi luyện tập, dàn ý bảo vệ | Người học có hiểu lựa chọn, metric, giới hạn và luồng dữ liệu không? |

AI giúp soạn nhãn và tài liệu, nhưng dữ liệu được công bố là “người gán nhãn” cần có kiểm tra thực sự của con người. AI tự đóng nhiều vai phản biện không thay thế đánh giá của giảng viên, người thử hoặc kiểm chứng độc lập.

## 2. Cách sử dụng nhóm mà không phát sinh API bắt buộc

Nếu công cụ đang dùng hỗ trợ subagent, AI điều phối có thể giao các phần độc lập cho các vai trò và tổng hợp lại. Cần giới hạn các tệp mỗi vai trò được phép sửa để tránh ghi đè nhau. Phần có phụ thuộc làm theo thứ tự, không chạy song song chỉ để có thêm vai trò.

Nếu công cụ không hỗ trợ agent đồng thời, dùng cùng một cuộc trò chuyện và lần lượt chuyển vai. Chức năng dự án không phụ thuộc vào khả năng agent: mô hình phân loại và ứng dụng chạy local, không cần API cho việc suy luận.

Ví dụ lệnh chuyển vai:

```text
Bạn hãy đóng vai Product Analyst cho SpendWise AI.
Đọc đặc tả hiện tại và các quyết định đã chốt.
Chỉ làm rõ yêu cầu đang mơ hồ, bổ sung tiêu chí chấp nhận và liệt kê tác động.
Không tự thêm tính năng vào MVP và không tuyên bố đã kiểm thử khi chưa chạy.
```

```text
Bạn hãy đóng vai QA Reviewer.
Đọc REQ liên quan, thiết kế và diff của task vừa thực hiện.
Tìm lỗi dữ liệu, logic và điểm thiếu bằng chứng; đưa ví dụ tái hiện cụ thể.
Phân biệt kết quả đã chạy, nhận xét từ đọc code và việc chưa kiểm chứng.
```

```text
Bạn hãy đóng vai Mentor.
Giải thích task vừa làm bằng tiếng Việt cho người còn nhớ tư duy lập trình
nhưng cần ôn kỹ thuật. Tạo tệp bài học trong thư mục học đã thống nhất.
Cho tôi một bài thực hành nhỏ, đáp án kiểm tra và ba câu hỏi bảo vệ.
```

Không cần tạo chat riêng cho từng vai trò. Không cấu hình hay mua API trả phí để vận hành nhóm này. Công cụ AI hiện dùng vẫn có thể chịu hạn mức hoặc phí tài khoản sẵn có; workflow không bảo đảm quyền sử dụng vô hạn với chi phí 0 đồng.

## 3. Nguyên tắc Spec-Driven Development

Mọi thay đổi đi theo chuỗi:

```text
Nhu cầu → REQ và tiêu chí chấp nhận → Thiết kế → Task triển khai
        → Code/dữ liệu → Kiểm tra → Bằng chứng → Cập nhật tài liệu
```

Một task không chỉ ghi “làm dashboard”. Nó cần biết phục vụ REQ nào, dùng hợp đồng dữ liệu nào, nhận đầu vào gì và kiểm tra kết quả ra sao.

**Ví dụ truy vết:** REQ-06 yêu cầu tổng thu–chi chính xác → thiết kế dùng `amount_vnd` kiểu số nguyên và loại thu/chi → task viết truy vấn tổng hợp theo tháng → code → kiểm tra mẫu thu `2000000`, chi `40000` và `120000` → ghi kết quả tổng chi `160000`, chênh lệch `1840000` sau khi thực sự chạy.

Chưa có bằng chứng chạy thì trạng thái là “chưa kiểm chứng”, không phải “pass”.

## 4. Các bước và điều kiện chuyển giao

### Bước A — Đặc tả yêu cầu

Product Analyst và Project Owner thống nhất vấn đề, người dùng, phạm vi, đầu vào và các REQ. Mentor giải thích cách đọc spec và biến một nhu cầu thành tiêu chí chấp nhận.

**Đầu ra:** đặc tả yêu cầu; quyết định đã chốt; giả định và thông tin cần xác minh.

**Đủ để chuyển giao khi:** biết người dùng làm gì, đầu vào nào được hỗ trợ, tính năng nào chưa làm và cách biết mỗi yêu cầu đã đáp ứng. Rubric trường còn thiếu phải được ghi rõ; không suy diễn rằng trường đã duyệt.

### Bước B — Tài liệu thiết kế

Architect và ML Researcher cùng Data Engineer thống nhất giao diện, schema SQLite, mẫu CSV, tám nhãn khoản chi, xử lý xác nhận, pipeline train/inference và cách lưu artifact. Điểm `predict_proba` được ghi là chưa calibration. Ngưỡng `0.60` là đề xuất thử, cần chọn bằng validation.

**Đầu ra:** thiết kế, hợp đồng dữ liệu và quyết định kỹ thuật có lý do.

**Đủ để chuyển giao khi:** từ một mô tả khoản chi có thể chỉ ra cách chuẩn hóa, dự đoán, xác nhận, lưu và tổng hợp. Từ một mẫu huấn luyện có thể chỉ ra nguồn, nhãn, split và bước đánh giá. CSV nguyên tử và nhận diện import lại cùng batch có thiết kế kiểm chứng được.

### Bước C — Kế hoạch triển khai

Orchestrator chia thành các task vừa sức, mỗi task liên kết tới REQ và có thứ tự phụ thuộc. Mentor bổ sung kiến thức cần ôn ngay trước task đó.

**Đầu ra:** kế hoạch task, mục tiêu học và tiêu chí hoàn tất từng task.

**Đủ để chuyển giao khi:** mỗi task có đầu vào, tệp được phép sửa, bước thực hiện, kiểm tra phù hợp và đầu ra. Các task huấn luyện có budget CPU/dữ liệu hợp lý, không ngầm yêu cầu GPU hoặc API trả phí.

### Bước D — Code theo từng phần

Developer thực hiện một task hoặc một nhóm task nhỏ có liên quan. Data Engineer và ML Researcher làm phần dữ liệu/thực nghiệm theo cùng hợp đồng. Người học chạy lệnh, quan sát kết quả và trả lời câu hỏi trước khi chuyển sang phần khó hơn.

**Đầu ra:** code hoặc dữ liệu, hướng dẫn thực hành, kết quả kiểm tra và vấn đề còn lại.

**Đủ để chuyển giao khi:** task đáp ứng tiêu chí đã viết, hoặc có báo cáo thất bại cụ thể và kế hoạch sửa. Chạy baseline và đánh giá một mẫu dữ liệu nhỏ trước khi mở rộng; dữ liệu demo không được coi là bằng chứng mô hình tổng quát hóa tốt.

### Bước E — Review và luyện bảo vệ

QA Reviewer xem thay đổi theo spec. Mentor yêu cầu người học giải thích quyết định bằng kết quả thật. AI điều phối cập nhật kế hoạch và liên kết bằng chứng.

**Đầu ra:** lỗi cần sửa, bản review, nhật ký học và phần giải thích phục vụ báo cáo.

**Đủ để hoàn tất task khi:** lỗi trọng yếu đã xử lý, kiểm tra cần thiết đã chạy và tài liệu khớp code. Nếu review chỉ dựa trên đọc code, ghi rõ hạn chế đó.

## 5. Quy tắc phối hợp và ghi tệp

1. Một task có một vai trò chịu trách nhiệm chính; vai trò khác có thể review.
2. Chốt hợp đồng dữ liệu trước khi giao các phần cùng sử dụng nó.
3. Nếu chạy song song, chia tệp theo vùng rõ ràng; không để hai agent cùng sửa một tệp.
4. Không dùng dữ liệu cá nhân thật làm ví dụ mặc định, không commit database cá nhân hoặc thông tin truy cập.
5. Tạo dữ liệu giả có nhãn nguồn `synthetic`/tự viết và ghi giới hạn. Không gọi dữ liệu giả là giao dịch thực.
6. Khi yêu cầu thay đổi, cập nhật spec và tác động trước hoặc cùng lúc với task sửa code.
7. Không tự động lấy nhãn AI dự đoán để làm “ground truth”, không chọn model/ngưỡng trên test.
8. Nhật ký phân biệt “đã làm”, “đã chạy”, “đã đạt” và “chưa kiểm chứng”.

## 6. Mẫu task có thể dùng lại

```text
Task ID: TASK-xx
Tên: <một kết quả nhỏ, cụ thể>
Vai trò chính: <Developer / Data Engineer / ML Researcher...>
REQ liên quan: <REQ-xx>
Phụ thuộc: <task hoặc hợp đồng cần có trước>
Tệp được phép sửa: <danh sách>
Đầu vào: <schema, dữ liệu, cấu hình>
Mục tiêu học: <khái niệm cần hiểu sau task>
Các bước: <thứ tự thực hiện ngắn>
Tiêu chí chấp nhận: <ví dụ có thể kiểm tra>
Kiểm tra cần chạy: <lệnh hoặc thao tác thực tế>
Bằng chứng: <log, metric, ảnh hoặc tệp kết quả>
Vấn đề còn lại: <ghi rõ nếu có>
Trạng thái: TODO / DOING / REVIEW / DONE / BLOCKED
```

`BLOCKED` ở bảng task nghĩa là task đang thiếu đầu vào cụ thể, không phải toàn bộ dự án phải dừng. AI điều phối tiếp tục phần độc lập và ghi việc cần người học/giảng viên cung cấp.

## 7. Tài liệu đào tạo ở repo riêng

Mentor lưu bài học, bài tập, nhật ký và hướng dẫn bảo vệ tại [Learn/spendwise-ai](https://github.com/Krev1/Learn/blob/main/spendwise-ai/README.md). Mẫu nhật ký và nhịp học nằm trong [mentor_guide.md](https://github.com/Krev1/Learn/blob/main/spendwise-ai/mentor_guide.md). Repo dự án giữ đặc tả, thiết kế, kế hoạch, code, test và bằng chứng kỹ thuật.
