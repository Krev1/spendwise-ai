# SpendWise AI — Hướng dẫn nghiên cứu và bảo vệ đồ án

Ngày lập: 05/10/2026. **Đây là khung chuẩn bị, chưa phải báo cáo kết quả hoàn thành.** Đề tài và tiêu chí tốt nghiệp còn cần đối chiếu với quy định thực tế của trường và giảng viên hướng dẫn.

Mục tiêu của tài liệu là giúp bạn giải thích sản phẩm, dữ liệu, phương pháp, thí nghiệm và phần code mình đã hiểu. Không học thuộc các câu trả lời mẫu thay cho việc kiểm tra bằng chứng của dự án.

## 1. Tên và câu chuyện của đề tài

Tên đề tài đề xuất:

**“Nghiên cứu phân loại mô tả khoản chi tiếng Việt bằng học máy có giám sát và xây dựng ứng dụng quản lý chi tiêu cá nhân.”**

Tên sản phẩm: **SpendWise AI**.

Câu giới thiệu khi chưa triển khai:

> Em đề xuất xây ứng dụng cho sinh viên và người mới đi làm ghi nhận khoản chi bằng tay hoặc CSV. Phần nghiên cứu tập trung tự huấn luyện mô hình phân loại mô tả tiếng Việt, so sánh với từ khóa và baseline đơn giản, rồi đánh giá trên mô tả của người chưa có trong tập train. Người dùng xác nhận danh mục trước khi lưu.

Khi hoàn thành, thay “đề xuất” bằng hành động đã có bằng chứng; thêm số mẫu và kết quả đo thật. Không chuyển các mục tiêu 1.200 mẫu, macro-F1 0,80 thành thành tích nếu chưa đạt.

Vấn đề thực tế cần kiểm chứng: người dùng có thấy việc tự chọn danh mục cho từng khoản chi tốn công và một gợi ý có ích không? Có thể phỏng vấn một nhóm nhỏ, ghi câu trả lời và bối cảnh; không tuyên bố nhu cầu đã được chứng minh chỉ từ ý tưởng ban đầu.

## 2. Việc cần xác nhận với giảng viên trước khi mở rộng

Mang bộ đặc tả đến giảng viên và ghi quyết định vào nhật ký dự án:

- Đồ án ngành AI có chấp nhận mô hình học máy truyền thống tự huấn luyện và thí nghiệm có kiểm soát không?
- Có yêu cầu thuật toán mới, mô hình sâu hoặc so sánh với phương pháp hiện đại nào không?
- Dữ liệu tự thu thập, quy trình đồng ý sử dụng và mức công khai nào được chấp nhận?
- Có giới hạn số trang, mẫu báo cáo, thời gian thuyết trình, yêu cầu demo hay quy trình duyệt đề tài không?
- Cách ghi nhận công cụ AI hỗ trợ viết code/tài liệu và phần đóng góp cá nhân được yêu cầu như thế nào?

Đây là các điều chưa biết của đề tài, không phải lý do dừng các bước học Python, thiết kế nhãn hay dựng pipeline thử nghiệm. Nếu trường yêu cầu thêm phương pháp, cập nhật phạm vi và kế hoạch trước khi nhận thêm công việc.

## 3. Câu hỏi nghiên cứu và giả thuyết

| Mã | Câu hỏi | Thí nghiệm/cách trả lời |
|---|---|---|
| RQ1 | Mô hình tự huấn luyện có giúp phân loại tốt hơn baseline từ khóa trên người mới không? | So B0, B1, NB, LR cùng test; báo macro-F1 và chênh lệch |
| RQ2 | Word, character hay union phù hợp hơn với mô tả tiếng Việt ngắn? | Ablation cùng split và protocol chọn tham số, khi đủ dữ liệu |
| RQ3 | Đặt ngưỡng score làm thay đổi tỷ lệ gợi ý và độ đúng như thế nào? | Chốt threshold trên validation; đo coverage/accepted accuracy trên test |
| RQ4 | Mô hình thường sai ở kiểu mô tả nào và dữ liệu còn thiếu gì? | Rà lỗi theo nhóm, ví dụ đã ẩn danh, confusion matrix |
| RQ5 | Người dùng có hoàn thành được nhập tay/CSV và kiểm tra danh mục? | Thử tác vụ nhỏ, đo hoàn thành/lỗi và phản hồi; tách khỏi điểm classifier |

Giả thuyết khởi đầu để **kiểm chứng**, chưa phải kết luận:

- H1: TF-IDF + classifier có macro-F1 cao hơn B0 và có thể vượt B1 khi cách viết đa dạng.
- H2: Character n-gram có thể giúp ở lỗi gõ/viết tắt; union có thể thêm lợi ích nhưng tăng số đặc trưng.
- H3: Tăng threshold có thể giảm coverage và tăng độ đúng trong phần được gợi ý; hiệu ứng phải đo, không bảo đảm đơn điệu với mọi mẫu nhỏ.
- H4: Mô tả chỉ có tên cửa hàng hoặc mô tả ghép sẽ khó phân loại hơn mô tả rõ mục đích.

Trước thí nghiệm, ghi giả thuyết, metric, cấu hình được phép thử và quy tắc chọn model. Sau thí nghiệm, có thể kết luận giả thuyết không được dữ liệu hỗ trợ. Nếu model thua từ khóa, phân tích tại sao; không giấu baseline.

## 4. Đóng góp có thể bảo vệ

Bạn có thể đóng góp một hệ thống dữ liệu và thực nghiệm phù hợp ngữ cảnh, dù không phát minh thuật toán mới:

1. Bộ nhãn và hướng dẫn gán nhãn tiếng Việt, xử lý mô tả mơ hồ có quy tắc.
2. Dataset do nhóm xây dựng đúng quyền sử dụng, có nguồn, phiên bản và audit.
3. Protocol giữ người mới riêng, tránh trùng/khuôn câu và TF-IDF rò rỉ.
4. So sánh baseline và classifier; ablation biểu diễn nếu thực hiện.
5. Cơ chế gợi ý theo threshold, luôn có xác nhận; giải thích tradeoff coverage–accuracy.
6. Ứng dụng nối mô hình với nhập tay/CSV, lưu SQLite và báo cáo chi tiêu.
7. Artifacts tái lập, phân tích lỗi và giới hạn sử dụng.

Chỉ đưa vào mục “đóng góp đã thực hiện” những mục đã làm. Chưa khảo sát người dùng thì ghi “dự kiến khảo sát”. Chưa có dataset thật thì ghi “prototype với câu tự tạo”. Chưa đo vượt baseline thì không viết “phương pháp đề xuất cải thiện độ chính xác”.

Đặc biệt, TF-IDF, Naive Bayes, Logistic Regression, Streamlit và SQLite là công cụ/phương pháp có sẵn. Đóng góp của bạn là cách chọn, thực hiện và kiểm chứng trong đề tài; không nhận mình đã sáng tạo các thuật toán này.

## 5. Dàn ý báo cáo tốt nghiệp

| Phần | Nội dung cần viết | Bằng chứng nên dẫn |
|---|---|---|
| Mở đầu | Vấn đề, đối tượng, mục tiêu, phạm vi và câu hỏi nghiên cứu | Đặc tả, phỏng vấn ban đầu nếu có |
| Cơ sở lý thuyết và công trình liên quan | Text classification, TF-IDF, NB/LR, baseline, chỉ số và dữ liệu nhóm | Tài liệu gốc/chính thức; bài nghiên cứu đã thực sự đọc |
| Phân tích yêu cầu và thiết kế | Use case, luồng nhập, xác nhận, schema, kiến trúc và quyết định | Sơ đồ và bảng truy vết yêu cầu–thiết kế |
| Dữ liệu và phương pháp | Thu thập, consent, nhãn, audit, split, train/tune/test | Hướng dẫn nhãn, dataset/split manifest |
| Triển khai | Module và luồng code, tích hợp pipeline, xử lý lỗi, lưu nhãn | Code, commit, kiểm tra và ảnh demo |
| Thực nghiệm và thảo luận | Cấu hình, baseline, kết quả theo lớp, threshold, lỗi, thời gian | File metrics, bảng thí nghiệm, confusion matrix |
| Kết luận và hướng tiếp | Trả lời RQ bằng kết quả; mục tiêu chưa đạt; việc có căn cứ cần bổ sung | Tổng hợp chứng cứ, model card |
| Phụ lục | Môi trường, lệnh tái lập, mẫu CSV, hướng dẫn sử dụng, nhật ký | Lockfile, README, run artifacts |

Đề cương trên là khung nội dung, cần chuyển sang mẫu trường. Viết chương phương pháp trước khi chạy test; điền chương kết quả sau khi có dữ liệu đo thật. Không tạo các bảng có số giả để “tạm dùng” rồi quên thay.

## 6. Hồ sơ bằng chứng cần giữ từ đầu

| Bằng chứng | Giúp trả lời câu hỏi nào? |
|---|---|
| Phiên bản đặc tả và tiêu chí chấp nhận | Sản phẩm phải làm được gì, đã hoàn thành đến đâu? |
| Nhật ký quyết định | Vì sao chọn stack, nhãn, split, model, threshold? |
| Hướng dẫn nhãn và audit bất đồng | Nhãn thật được quyết định thế nào? |
| Sổ thu thập/quyền sử dụng riêng | Nguồn dữ liệu có đúng phạm vi đồng ý không? |
| Dataset manifest + hash | Điểm được đo trên phiên bản nào? |
| Split manifest + seed | Có trùng người/văn bản/khuôn giữa các tập không? |
| Config từng run | Có đổi nhiều thành phần cùng lúc không? |
| Python/dependency/OS/hardware | Có chạy lại được và latency được đo trên máy nào? |
| Commit mã nguồn | Kết quả gắn với code nào? |
| Predictions/metrics/confusion/error analysis | Kết luận có thể kiểm tra lại không? |
| Model card | Mô hình dùng cho ai và còn giới hạn gì? |
| Nhật ký học và hỗ trợ AI | Phần nào bạn đã hiểu, kiểm tra và tự sửa? |

Hash giúp xác định phiên bản, không bảo đảm dữ liệu đúng, không thay quyền sử dụng và không tự làm dữ liệu trở nên ẩn danh. Seed giúp tái lập các bước có ngẫu nhiên trong cùng protocol; một seed cố định không chứng minh mô hình tổng quát tốt.

Khi nhờ AI viết code, ghi yêu cầu, bản code đã nhận, những điều đã kiểm tra và lỗi mình đã sửa. Bạn phải giải thích được code được nộp; AI hỗ trợ không làm thay trách nhiệm hiểu thiết kế và kết quả.

## 7. Cách thực hiện một vòng nghiên cứu

1. Viết câu hỏi và mục tiêu của vòng, ví dụ “so word LR với word NB”.
2. Kiểm tra dataset/split hash và đảm bảo test vẫn giữ nguyên.
3. Chạy đúng baseline/cấu hình đã cho phép; lưu mọi run, cả run điểm thấp.
4. Dùng validation chọn model/threshold; viết lý do trước khi mở test.
5. Chạy test theo kế hoạch đã chốt và lưu kết quả. Đánh giá các baseline đã định trước trên cùng test.
6. Tính chênh lệch, đọc lớp yếu, rà lỗi và viết kết luận giới hạn theo số người/số mẫu.
7. Tích hợp artifact đã đánh giá; kiểm tra ứng dụng và tách kết quả UI khỏi classifier.

Nếu xem test rồi sửa model, ghi đây là vòng phát triển tiếp. Một kết luận chính thức mới cần tập đánh giá độc lập mới hoặc protocol nghiên cứu khác được chốt rõ; không gọi việc chạy đi chạy lại một test là “test cuối” độc lập.

Không xóa run chỉ vì kết quả không đẹp. Lỗi train do đầu vào hoặc cấu hình sai có thể đánh dấu failed; giữ thông tin lỗi để giải thích khác với một run hợp lệ có điểm thấp.

## 8. Dàn thuyết trình khoảng 10–12 phút

Điều chỉnh theo thời lượng trường yêu cầu. Mỗi slide có một ý chính và một bằng chứng đọc được.

| Slide | Nội dung | Thời lượng gợi ý |
|---|---|---|
| 1 | Tên đề tài, đối tượng và vấn đề | 30 giây |
| 2 | Một use case từ mô tả tới danh mục đã xác nhận | 45 giây |
| 3 | Phạm vi MVP và câu hỏi nghiên cứu | 45 giây |
| 4 | Dữ liệu: nguồn thật/tự tạo, nhãn, consent | 60 giây |
| 5 | Split giữ người riêng và phòng leakage | 60 giây |
| 6 | Baseline, TF-IDF, NB/LR và lý do chọn | 75 giây |
| 7 | Cấu hình và quy tắc chọn trên validation | 45 giây |
| 8 | Kết quả thật: bảng baseline, macro-F1, confusion | 90 giây |
| 9 | Threshold: coverage và accepted accuracy | 45 giây |
| 10 | Demo ngắn nhập tay/CSV, sửa và xác nhận | 90 giây |
| 11 | Lỗi tiêu biểu và giới hạn | 45 giây |
| 12 | Trả lời RQ, đóng góp và hướng tiếp | 30 giây |

Chưa có kết quả thì slide 8–9 ghi kế hoạch đánh giá; bản này phù hợp bảo vệ đề cương, không được trình bày như bảo vệ sản phẩm hoàn thành.

Một ví dụ sai có giải thích thường giúp hội đồng hiểu phạm vi hơn nhiều ảnh demo đúng. Chọn ví dụ đã ẩn danh; ghi rõ câu nào lấy từ test, câu nào tự tạo để demo.

## 9. Kịch bản demo có thể tái lập

1. Khởi động app và cho thấy phiên bản model được tải. Tắt kết nối mạng sau khi môi trường đã cài đặt để kiểm tra chế độ chạy local nếu đặc tả yêu cầu.
2. Nhập một khoản chi có mô tả rõ; xem gợi ý, chỉnh nếu cần và xác nhận. Kiểm tra nhãn cuối lưu đúng.
3. Nhập mô tả mơ hồ như `Grab`. Quan sát output thực tế; giải thích score cao vẫn có thể sai và người dùng còn quyền chọn.
4. Nhập CSV có một dòng hợp lệ và một dòng thiếu/sai dữ liệu. Cho thấy dòng lỗi có thông tin sửa, dữ liệu hợp lệ vẫn phải được review theo hợp đồng nhập của app.
5. Sửa nhãn của một giao dịch rồi xem tổng hợp thay đổi. Giải thích biểu đồ dùng nhãn cuối do người dùng xác nhận.
6. Mở một run artifact và chỉ rõ dataset/split hash, config, macro-F1, lớp yếu và threshold. Không huấn luyện lại tùy hứng trong buổi demo.

Giữ bộ demo tự tạo, dữ liệu kiểm tra có phiên bản và hướng dẫn reset DB demo. Không dùng DB chi tiêu cá nhân thật khi chiếu màn hình. Có thể chuẩn bị ảnh/video demo dự phòng; video không thay bằng chứng metrics.

## 10. Những câu hỏi thường gặp và cách trả lời

Các câu trả lời dưới đây là khung lập luận. Khi trả lời thật, bổ sung đường dẫn artifact và số liệu đã đo.

### “Đây có thật là đồ án AI hay chỉ là ứng dụng CRUD?”

Phần nghiên cứu là mô hình học có giám sát từ mô tả và nhãn, kèm so sánh baseline, đánh giá người mới và phân tích lỗi. CRUD là lớp sản phẩm để sử dụng kết quả. Chứng minh bằng pipeline train, trọng số học được và báo cáo thực nghiệm; không chỉ bằng giao diện.

### “Dùng scikit-learn có tính là tự huấn luyện không?”

Có: bạn chuẩn bị dữ liệu, fit vocabulary/IDF và tham số classifier, chọn cấu hình, đánh giá và lưu model của mình. Thư viện cung cấp implementation thuật toán. Yêu cầu tốt nghiệp cụ thể về độ mới hoặc mô hình sâu vẫn cần xác nhận với trường.

### “Vì sao không dùng ChatGPT hoặc LLM?”

Mục tiêu MVP là bài toán tám lớp với ngân sách phí API bằng 0, tự huấn luyện và chạy CPU. Mô hình tuyến tính cho một điểm khởi đầu có thể giải thích, đo và tái lập. Đây là lựa chọn thiết kế; chưa có thí nghiệm thì không nói nó tốt hơn mọi LLM. Một baseline mô hình pretrained chỉ thêm khi có tài nguyên và protocol công bằng.

### “Tại sao phải có DummyClassifier và từ khóa?”

Dummy cho thấy mốc không dùng thông tin văn bản. Từ khóa đại diện giải pháp đơn giản có thể dùng ngay. Nếu ML không cải thiện đáng kể, cần giải thích chất lượng dữ liệu, độ đa dạng và chi phí vận hành; không mặc định ML luôn đáng dùng.

### “TF-IDF học gì? Vì sao không fit cả dataset?”

Nó học vocabulary và độ phổ biến của đặc trưng từ train. Fit cả test tiết lộ thông tin của dữ liệu kiểm tra vào biểu diễn. Pipeline giữ quá trình này nhất quán; kiểm tra bằng code và split manifest.

### “Word TF-IDF của bạn có tách từ tiếng Việt không?”

Nếu dùng tokenizer theo khoảng trắng, nói rõ đó là tokenization cơ bản, chưa phải bộ tách từ tiếng Việt đầy đủ. Character n-gram là một hướng so sánh để giảm phụ thuộc vào token nguyên vẹn. Kết luận phương pháp nào tốt hơn phải dựa vào ablation đã đo.

### “Tại sao Logistic Regression trong bài phân loại?”

Tên có chữ Regression nhưng phương pháp này dùng để phân loại; ở bài nhiều lớp, ánh xạ score tuyến tính thành phân bố điểm theo lớp. Trọng số được tối ưu từ nhãn, có regularization. Bạn cần giải thích `w`, `b`, loss và `C` bằng một ví dụ của mình.

### “Giả định của Naive Bayes có đúng với ngôn ngữ không?”

Các đặc trưng ngôn ngữ có thể phụ thuộc nhau, nên giả định độc lập có điều kiện là xấp xỉ. Vì vậy NB là mô hình cần kiểm chứng bằng thực nghiệm, không phải chân lý về dữ liệu. So với LR cùng biểu diễn để xem độ phù hợp thực tế.

### “Vì sao không random chia từng hàng?”

Nhiều mô tả từ cùng người hoặc khuôn có quan hệ. Random hàng có thể đo khả năng nhớ cách ghi cũ thay vì dùng cho người mới. Đề tài ưu tiên split giữ người và họ khuôn riêng; tỷ lệ 70/15/15 gần đúng được chấp nhận để giữ protocol.

### “Nếu test thiếu lớp thì làm sao?”

Kiểm tra support trước freeze, thu thập thêm hoặc ghi chưa đủ điều kiện đánh giá tám lớp. Không dùng score để chọn lại seed. Nếu phải đổi bộ nhãn, cập nhật đặc tả, data/model version và protocol; không gộp lớp sau khi thấy model đoán sai rồi giữ nguyên claim.

### “1.200 mẫu có đủ không?”

Đó là mục tiêu khởi đầu, không một bảo đảm thống kê. Cần xem độ đa dạng, số người, độ khó và số mẫu mỗi lớp; test ≥20 mô tả khác nhau/lớp vẫn có bất định. Báo điều kiện lấy mẫu và giới hạn, có thể làm learning curve trên train/validation nếu còn thời gian.

### “Dữ liệu tự tạo có đại diện thực tế không?”

Nó giúp kiểm tra đường đi kỹ thuật nhưng có thể quá sạch và lặp khuôn. Chỉ báo cáo như demo/smoke test. Kết luận về người dùng thực cần test thật được đồng ý sử dụng và giữ riêng. Nếu chưa thu được, thừa nhận nghiên cứu chưa kiểm chứng bên ngoài tập tự tạo.

### “Vì sao dùng macro-F1 thay accuracy?”

Accuracy có thể cao khi đoán tốt lớp đông nhưng bỏ lớp ít. Macro-F1 cho tám lớp trọng số ngang nhau; kết hợp support, precision/recall và confusion matrix. Nó cũng không giải quyết mọi vấn đề: lớp không có mẫu và chi phí sai khác nhau vẫn cần được giải thích.

### “0,80 là kết quả hay mục tiêu?”

Trong bộ đặc tả là mục tiêu cần đo. Khi bảo vệ, chỉ gọi là kết quả nếu có `metrics_test.json` tương ứng dataset/split/model đã chốt. Nếu chưa đạt, nêu điểm thật, lớp yếu và tác động đến tính năng gợi ý.

### “Score 0,9 có nghĩa 90% đúng không?”

Không khi score chưa hiệu chuẩn. Dự án dùng nó để phân nhóm gợi ý theo một threshold được kiểm chứng trên validation. Muốn diễn giải xác suất đúng cần hiệu chuẩn và đánh giá riêng; trên giao diện gọi là điểm mô hình và vẫn yêu cầu xác nhận.

### “Tại sao chọn threshold 0,60?”

Đây là điểm khởi đầu của đặc tả, không chứng cứ. Threshold triển khai phải được chọn từ dãy và quy tắc validation đã chốt; test chỉ kiểm tra chính sách ấy. Nếu không đạt cả coverage và accepted accuracy mục tiêu, ghi chưa đạt.

### “Chọn threshold cao có làm metric đẹp giả không?”

Có thể làm phần gợi ý rất nhỏ nhưng chính xác. Vì thế báo đồng thời coverage, accepted accuracy, mẫu số và macro-F1 trên toàn bộ test. Không trình bày accepted accuracy riêng như độ chính xác toàn hệ thống.

### “Mô hình từ chối mọi câu ngoài miền được không?”

Không được bảo đảm bởi `predict_proba` hay lớp `khac`. Có thể nhận score cao với câu ngoài phạm vi. Bộ nhập kiểm tra loại giao dịch, thử bộ ngoài miền riêng và người dùng xác nhận là các phần bổ sung; cần báo lỗi còn tồn tại.

### “Người dùng sửa nhãn thì model có học ngay không?”

V1 chỉ lưu nhãn cuối của giao dịch, không tự train lại. Muốn dùng feedback cần đồng ý nghiên cứu, rà nhãn/ẩn danh, tạo dataset mới và đánh giá model mới. Giữ quyền sửa trong app giúp người dùng nhưng không biến accuracy của model thành 100%.

### “Kết quả có chạy lại được không?”

Trình bày dataset hash, split manifest, seed, config, code commit và môi trường. Chạy lại cùng protocol và đối chiếu metric. Không hứa mọi máy/phiên bản thư viện tạo kết quả nhị phân giống hệt; ghi sai khác thực tế và xử lý nếu có.

### “Phần nào bạn tự làm khi có trợ lý AI?”

Nêu đúng sự thật theo quy định trường: bạn quyết định bài toán, dữ liệu, đánh giá; công cụ hỗ trợ bản code/tài liệu nào; bạn đã đọc, chạy, sửa và kiểm chứng gì. Mở một hàm cụ thể và giải thích đầu vào, xử lý, đầu ra cùng một lỗi. Không nhận toàn bộ code do mình viết tay nếu không phải vậy.

## 11. Chuẩn bị để giải thích code

Chọn một giao dịch minh họa và đi từng bước:

```text
Mô tả người dùng
  → kiểm tra loại giao dịch / đầu vào
  → chuẩn hóa theo pipeline đã chốt
  → vector TF-IDF theo vocabulary train
  → classifier và thứ tự classes_
  → nhãn đề xuất + score + threshold
  → người dùng xem/sửa/xác nhận
  → SQLite lưu nhãn cuối
  → tổng hợp chi tiêu dùng nhãn cuối
```

Bạn cần tự trả lời được:

- Module nào đọc CSV và xử lý lỗi từng dòng? Có phân biệt CSV app với CSV ML không?
- Vì sao `fit` chỉ nằm ở code train, còn app chỉ tải model và dự đoán?
- Vì sao lưu cả vectorizer và classifier cùng pipeline?
- Cột xác suất thứ ba ứng với nhãn nào? Có đọc `classes_` không?
- Score dưới threshold đi vào trạng thái nào? Ai xác nhận nhãn cuối?
- Nếu chưa có model artifact, ứng dụng thông báo và cho chọn tay thế nào?
- Nếu người dùng sửa mô tả, gợi ý cũ có được tính lại và xác nhận lại không?
- Nhãn do người dùng sửa có nằm trong phép tính accuracy của classifier không?
- Biểu đồ dùng dữ liệu nào, và phần nào chỉ là phép tổng hợp?

Nếu không giải thích được một hàm, quay lại bài tập nhỏ; yêu cầu trợ lý chú giải và tự sửa một trường hợp trước khi dùng hàm đó trong đồ án.

## 12. Mẫu nhật ký để vừa làm vừa học

Chép mẫu này cho mỗi nhiệm vụ; ghi ngắn nhưng bằng lời của mình:

```markdown
Ngày / mã nhiệm vụ:
Mục tiêu và yêu cầu liên quan:
Khái niệm mới đã học:
File/hàm đã thay đổi:
Đầu vào → xử lý → đầu ra:
Vì sao chọn cách này:
Kiểm tra đã chạy và kết quả thực tế:
Một lỗi đã gặp và cách sửa:
AI/công cụ hỗ trợ phần nào:
Điểm chưa hiểu / giới hạn:
Bằng chứng: commit, run_id hoặc file báo cáo
```

Nhật ký không cần kể lại mọi thao tác. Nó giúp chứng minh sự hiểu biết, quyết định và nguồn kết quả. Mỗi tuần thử trình bày một nhiệm vụ trong 2 phút mà không đọc code.

## 13. Đánh giá sản phẩm và mô hình là hai việc khác nhau

| Loại đánh giá | Câu hỏi | Bằng chứng |
|---|---|---|
| Mô hình | Nhãn dự đoán ban đầu đúng bao nhiêu, với ai và dữ liệu nào? | Test độc lập, macro-F1, confusion, coverage/accuracy |
| Ứng dụng | Dữ liệu có nhập/sửa/lưu/tổng hợp đúng không? | Kiểm tra use case và dữ liệu đã xác nhận |
| Khả dụng | Người dùng có hoàn thành tác vụ và hiểu gợi ý không? | Kịch bản thử người dùng, thời gian/lỗi/phản hồi |
| Khả năng tái lập | Có chạy lại nghiên cứu và demo không? | Môi trường, manifest, code và hướng dẫn |

Một app chạy tốt không chứng minh model đạt 0,80. Một model đạt 0,80 cũng không chứng minh CSV không làm mất dữ liệu. Một nhóm thử người dùng nhỏ chưa chứng minh tác động tài chính lâu dài.

Nếu thử khả dụng, đề xuất 5–8 người phù hợp trong một pilot với tác vụ định sẵn; báo đúng số người, cách chọn và tính chất thăm dò. Không dùng số lượng này để claim kết quả đại diện cho toàn bộ sinh viên/người đi làm.

## 14. Tự rà trước buổi bảo vệ

- [ ] Đề tài và tiêu chí đã được đối chiếu với giảng viên.
- [ ] Mục tiêu, việc đã làm và việc chưa làm được tách rõ.
- [ ] Nguồn dữ liệu, consent, số người/mẫu/lớp thật/tự tạo được báo cáo.
- [ ] Giải thích được một ví dụ gán nhãn mơ hồ.
- [ ] Giải thích được split và một tình huống leakage.
- [ ] Hiểu TF-IDF, NB/LR, baseline và lựa chọn tham số.
- [ ] Bảng kết quả dẫn đúng run artifact; không có số giả.
- [ ] Báo metric theo lớp, mẫu số coverage/accuracy và score chưa calibrated.
- [ ] Có ít nhất ba lỗi thật cùng lời giải thích, nếu đã đánh giá.
- [ ] Demo có dữ liệu tự tạo, có trường hợp sửa/xác nhận và CSV lỗi.
- [ ] Có khả năng chạy local và hướng dẫn môi trường đã kiểm chứng.
- [ ] Ghi đúng vai trò AI hỗ trợ và phần đóng góp cá nhân.
- [ ] Nêu giới hạn, điều chưa đạt và hướng tiếp dựa trên lỗi đã đo.

## 15. Tài liệu và nguồn để đọc khi chuẩn bị

Phần công thức, schema, protocol và các liên kết chính thức nằm trong [tài liệu dữ liệu và ML](05_data_and_ml.md). Khi trích vào luận văn, lập danh mục tài liệu tham khảo theo mẫu trường, ghi ngày truy cập và phiên bản phần mềm thực tế.

Chương công trình liên quan cần được nghiên cứu thêm sau khi giảng viên chốt phạm vi. Tài liệu API không thay cho tổng quan nghiên cứu. Với mỗi bài được đưa vào luận văn, tự ghi: bài toán, dataset, cách chia tập, baseline, metric, giới hạn và liên hệ với đề tài; không đưa một trích dẫn chưa đọc chỉ vì AI gợi ý.
