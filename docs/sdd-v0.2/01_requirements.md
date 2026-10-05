# 01 — Đặc tả yêu cầu v0.2

Ngày: 06/10/2026. Đây là yêu cầu cho phiên bản đang chuẩn bị xây dựng, không phải báo cáo chức năng đã có.

## 1. Bài toán, người dùng và thành công

Sinh viên/người mới đi làm muốn biết còn bao nhiêu ngân sách trong tháng, nhóm nào gần giới hạn, và nếu tiếp tục tốc độ hiện tại thì cuối tháng có thể vượt mức nào. Họ ghi khoản chi bằng tay/CSV; AI giảm việc chọn danh mục nhưng người dùng quyết định nhãn cuối cùng.

Đánh giá riêng ba kết quả: (1) tiền, quyền truy cập, ngân sách/cảnh báo tính đúng; (2) người thử dùng hiểu cảnh báo và thấy hữu ích; (3) thí nghiệm Deep Learning có dữ liệu được phép, baseline, đánh giá độc lập và giải thích được. Một kết quả không tự chứng minh hai kết quả còn lại.

## 2. Yêu cầu đã chốt và mặc định thiết kế

Đã chốt: website responsive công khai có đăng ký; ngân sách tháng tổng và theo nhóm; cảnh báo thực tế và dự báo; nhập tay/CSV; phân loại mô tả khoản chi tiếng Việt; bắt buộc Deep Learning; một người làm; ngân sách phí thêm 0 đồng; Windows/RAM 32 GB/RTX 3080 VRAM 10 GB do người dùng báo; chưa có lịch sử chi tiêu bản thân; chưa có hạn nộp/giờ mỗi tuần.

Mặc định đề xuất để bắt đầu: tiếng Việt, VND, múi giờ `Asia/Ho_Chi_Minh`, tám nhãn hiện có, cảnh báo trong ứng dụng ở 80%/100%, dự báo xu hướng có giải thích, email/mật khẩu và xác minh email trước khi dùng. Django/PyTorch là lựa chọn kỹ thuật, không phải lựa chọn người dùng đã tự xác nhận. Có thể thay bằng quyết định có ghi tác động.

Bao gồm đăng ký/đăng nhập/khôi phục mật khẩu, giao dịch, CSV, dashboard, ngân sách, hai loại cảnh báo, AI gợi ý, xuất/xóa dữ liệu và đồng ý nghiên cứu tách biệt. Chưa có ngân hàng tự động, OCR, đa tiền tệ, ngân sách hộ gia đình, chatbot, đầu tư, thông báo email/push ngân sách, tự retrain hoặc dự báo bằng mạng neural thứ hai. Email phục vụ tài khoản, không phải kênh cảnh báo chi tiêu của MVP.

## 3. Hợp đồng chung

- Slug: `an_uong,di_chuyen,nha_o_hoa_don,hoc_tap,mua_sam,giai_tri,suc_khoe,khac`.
- CSV UTF-8/BOM: `transaction_id,date,transaction_type,amount_vnd,description,category`; tối đa 2.000.000 byte / 5.000 dòng dữ liệu.
- ID nguồn ASCII chữ/số/`_`/`-`, dài 1–64; ngày ISO thực; type `income|expense`; tiền int VND dương ≤ 1.000.000.000.000; mô tả NFC/trim 1–300 ký tự. Giao dịch thực không được ghi ngày tương lai; đây là kiểm tra ứng dụng bổ sung, không đổi việc parser cũ đọc ngày ISO hợp lệ.
- Khoản thu không có nhãn khoản chi, không gọi classifier, không làm giảm số tiền đã chi ngân sách. Khoản chi phải có nhãn người dùng xác nhận trước khi lưu.
- Trong sản phẩm nhiều người, ID import và mọi phép đọc/ghi luôn có phạm vi **người dùng đăng nhập**. Client không tự chọn chủ sở hữu bằng trường `user_id`.

## 4. Yêu cầu và tiêu chí chấp nhận

### SW-REQ-01 — Tài khoản và phân tách dữ liệu

Đăng ký email/mật khẩu, xác minh email, đăng nhập/đăng xuất, khôi phục mật khẩu. Không dùng mật khẩu rõ trong DB/log. Mỗi người chỉ xem/sửa/xóa/import/xuất ngân sách và giao dịch của mình.

**Chấp nhận:** A và B có dữ liệu khác nhau; B đổi ID trong URL/form/preview/export của A vẫn không lấy hoặc thay đổi dữ liệu A (404/403 theo hợp đồng), kể cả dashboard/dự báo. Link xác minh/reset hết hạn hoặc đã dùng không dùng lại được. Phản hồi reset không tiết lộ email đã đăng ký. Tài khoản chưa xác minh không vào dữ liệu tài chính. Có kiểm tra rate limit và đăng xuất.

### SW-REQ-02 — Nhập, sửa, xóa giao dịch

Giữ các ràng buộc mục 3, bước xác nhận nhãn, lịch sử đổi nhãn và chống gửi form hai lần. Xóa có xác nhận; cập nhật/xóa làm dashboard, ngân sách và dự báo tính lại.

**Chấp nhận:** khoản chi 40.000 sửa thành 50.000 làm tổng tăng đúng 10.000; xóa 120.000 làm tổng giảm đúng 120.000. Double submit chỉ tạo một bản ghi. Sửa đồng thời có phát hiện version cũ, không âm thầm ghi đè. Ngày tương lai, thu có nhãn, mô tả trống và tiền không hợp lệ bị từ chối mà không ghi DB.

### SW-REQ-03 — CSV xem trước, nguyên tử và không nhập lại

Parse/validate cả batch trước ghi. Preview gắn tài khoản và payload; sửa input/nhãn sau xác nhận làm xác nhận cũ hết hiệu lực. Nhãn chi có sẵn cũng cần người dùng duyệt. Với `(owner, transaction_id)`, payload nguồn canonical **trước AI/trước sửa nhãn** giống thì bỏ qua, khác thì từ chối toàn batch. File không duy trì ID ổn định không được hứa phát hiện mọi trùng lặp.

**Chấp nhận:** batch có lỗi hoặc chi chưa xác nhận ghi 0 hàng; lỗi DB ở hàng thứ hai rollback hàng thứ nhất. Import lại không thêm hàng và giữ nhãn người dùng đã sửa. Hai tài khoản dùng cùng ID nguồn được phép; preview của A không dùng bởi B. Hai import đồng thời không vượt unique constraint hoặc để lại một phần batch.

### SW-REQ-04 — Tổng hợp theo tháng

Tổng thu/chi/chênh lệch và chi theo nhóm dùng số nguyên, ngày giao dịch theo múi giờ đã quy định. Không gọi chênh lệch thu–chi là số dư ngân hàng.

**Chấp nhận:** thu 2.000.000, chi 40.000 + 120.000 cho chi 160.000, chênh lệch 1.840.000. Lọc tháng không lấy ngày tháng liền kề; tháng trống trả 0; số tổng không trộn tài khoản.

### SW-REQ-05 — Ngân sách tổng và theo nhóm

Mỗi tài khoản có tối đa một kế hoạch cho một tháng. Tổng ngân sách và mỗi giới hạn nhóm là int VND dương trong giới hạn tiền. Nhóm không đặt giới hạn có trạng thái “chưa đặt”, không coi ngân sách là 0. Tổng các giới hạn nhóm ≤ tổng ngân sách; phần còn lại được hiển thị là chưa phân bổ. Cho phép lập ngân sách tháng tương lai, không tự tạo lệnh chuyển tiền.

**Chấp nhận:** tổng 5.000.000, ăn uống 2.000.000, di chuyển 1.000.000 → chưa phân bổ 2.000.000. Lưu 6.000.000 giới hạn nhóm trong tổng 5.000.000 bị từ chối toàn bộ. Không đặt hai ngân sách cho cùng owner/tháng. Đổi tổng xuống dưới tổng nhóm báo lỗi; thay đổi nhiều nhóm lưu nguyên tử.

### SW-REQ-06 — Cảnh báo theo thực tế

Với ngân sách đã đặt, số đã chi `S` so với ngân sách `B`: dưới 80% bình thường; từ 80% đến dưới 100% gần giới hạn; bằng 100% đã chạm; trên 100% đã vượt. Cả tổng và từng nhóm dùng giao dịch chi đã xác nhận. Tính bằng integer comparison, không làm tròn phần trăm trước khi xét ngưỡng.

**Chấp nhận:** `B=1.000.000`: 799.999 bình thường, 800.000 gần giới hạn, 1.000.000 chạm, 1.000.001 vượt. Khoản thu không giảm `S`. Đổi nhãn chuyển số chi giữa nhóm và cập nhật cảnh báo. Reload không sinh cảnh báo lặp như giao dịch mới. Chưa đặt ngân sách thì không có cảnh báo vượt giả.

### SW-REQ-07 — Ước tính cuối tháng và cảnh báo dự báo

Hiển thị riêng số thực tế và ước tính, phương pháp, ngày chốt, lịch sử được người dùng xác nhận đầy đủ và giới hạn phương pháp. Đầu kỳ hoặc lịch sử thiếu hiển thị “chưa đủ dữ liệu để ước tính”; cảnh báo thực tế vẫn hoạt động. Không suy ra ngày không có giao dịch là ngày không chi khi chưa có xác nhận.

**Chấp nhận:** tháng 30 ngày, hết ngày 10 đã chi 1.000.000, người dùng xác nhận ghi đủ ngày 1–10 → xu hướng 3.000.000; với ngân sách 2.500.000 có cảnh báo nguy cơ vượt. Thiếu xác nhận hoặc chưa đủ 7 ngày đã kết thúc không xuất số dự báo. Nhóm chưa đặt ngân sách không có cảnh báo vượt; không đưa giao dịch tương lai vào số thực tế.

### SW-REQ-08 — Gợi ý phân loại bằng Deep Learning tự huấn luyện

Có pipeline neural train từ đầu, artifact version và suy luận cho tám nhãn. Khoản chi hiển thị gợi ý/điểm mô hình/phiên bản; người dùng xác nhận. Thu không qua mô hình. Mô tả thay đổi làm gợi ý và xác nhận cũ hết hiệu lực. Không có artifact hoặc inference lỗi thì nhập tay vẫn hoạt động.

**Chấp nhận:** kiểm tra neural forward/train/checkpoint/reload và cùng đầu vào sau reload theo tolerance; có loss/lệnh train thực được ghi. UI không lưu nhãn AI chưa xác nhận. Điểm softmax được gọi là điểm mô hình, không phải xác suất chắc chắn đúng; ngưỡng vận hành chọn bằng validation. Mô hình ngoài miền vẫn có thể sai với điểm cao.

### SW-REQ-09 — Dữ liệu và sự đồng ý riêng

Dùng ứng dụng không mặc định đồng ý dùng giao dịch để train. Có lựa chọn nghiên cứu riêng, mặc định tắt; không giảm quyền dùng app khi từ chối. Dữ liệu thật/consent/bản gán nhãn ở vùng private; dataset model chỉ dùng mô tả, không lấy tiền/email/ID người dùng làm feature.

**Chấp nhận:** tài khoản từ chối không xuất hiện trong snapshot nghiên cứu. Có provenance, trạng thái người gán nhãn, phiên bản guideline, nhóm chống leakage và quy trình rút đồng ý; log không ghi mô tả tài chính/email/token. Nhãn AI và sửa của chủ giao dịch là nguồn tham khảo, không tự coi là nhãn độc lập đã kiểm chứng.

### SW-REQ-10 — Thí nghiệm và bằng chứng AI

So sánh Dummy, từ khóa, TF-IDF + Logistic Regression với ít nhất một neural model tự train. Fit vocab/vectorizer/model trên train; chọn cấu hình/ngưỡng bằng validation; test khóa trước lựa chọn và không dùng chỉnh rule. Cùng cohort/split và báo coverage lớp. Dữ liệu hư cấu chỉ dùng smoke/augmentation train được ghi rõ.

**Chấp nhận:** report macro-F1, từng lớp, confusion matrix, số mẫu/người/nhóm, leakage audit, coverage/selective accuracy, thời gian/VRAM và phân tích lỗi với config/hash/seed/môi trường. Chưa có test thật đủ lớp thì ghi chưa đủ bằng chứng chất lượng thật. Không yêu cầu neural thắng baseline hoặc bịa điểm 0,80; điểm thấp vẫn phân tích trung thực theo rubric.

### SW-REQ-11 — Website dùng trên điện thoại và máy tính

Luồng đăng nhập → đặt ngân sách → nhập chi/xác nhận → xem cảnh báo/ước tính dùng được bằng trình duyệt. Form có label, lỗi rõ và thao tác bàn phím; bảng lớn có cách xem trên điện thoại.

**Chấp nhận:** kiểm tra viewport 360 px và 1280 px, không tràn ngang toàn trang, không che nút lưu/cảnh báo; quy trình CSV dài có phân trang nhưng xác nhận bao phủ toàn batch. Dữ liệu chưa lưu không biến mất âm thầm khi inference lỗi.

### SW-REQ-12 — Xuất và xóa dữ liệu

Người dùng xuất giao dịch/ ngân sách của mình; xuất bảng an toàn với spreadsheet formula injection, có mô tả cách escape và giới hạn round-trip. Xóa tài khoản sau xác thực lại xóa dữ liệu online và token/session liên quan. Rút đồng ý nghiên cứu được xử lý theo mục 04.

**Chấp nhận:** không xuất dữ liệu A khi đăng nhập B; mô tả bắt đầu `=,+,-,@` không chạy công thức khi mở bản xuất spreadsheet-safe; có test ký tự điều khiển. Xóa không để bản ghi tài chính mồ côi; backup có lịch hết hạn đã công bố và không khôi phục dữ liệu đã yêu cầu xóa vào hệ thống hoạt động.

### SW-REQ-13 — Vận hành công khai với phí thêm 0 đồng

Mục tiêu phát hành công khai có nhiều tài khoản. Trước mở đăng ký phải có TLS, production settings, session/CSRF, hạn chế abuse, PostgreSQL bền vững, backup/restore và email tài khoản đã kiểm tra. Không dùng database tạm của free runtime làm lưu trữ lâu dài. Chọn nhà cung cấp theo điều kiện miễn phí thực tại thời điểm triển khai; không tự đăng ký gói tính phí.

**Chấp nhận:** có URL HTTPS thật, kiểm tra restart vẫn giữ dữ liệu, restore thành công, reset/xác minh email end-to-end, test cách ly hai tài khoản và báo cấu hình/capacity đã đo. Nếu chưa có hạ tầng 0 đồng đáp ứng, vẫn làm local/pilot nhưng mốc public giữ chưa hoàn tất; không thay mục tiêu công khai bằng demo local. Mục tiêu thử tải ban đầu 10 người hoạt động đồng thời phải đo, không là cam kết tải lớn hoặc uptime.

### SW-REQ-14 — Tái lập, bàn giao và học riêng

Mỗi SW-TASK có REQ, thiết kế, code/test/evidence và bàn giao theo SHA. Môi trường web và train có lock đã kiểm tra; không phá môi trường v0.1. Mentor theo commit và ghi mức hiểu thật trong Learn; code không chờ bài học.

**Chấp nhận:** người khác dùng dữ liệu hư cấu công khai tái lập kiểm tra phần mềm; train thật cần quyền dữ liệu được nêu. Bàn giao phân biệt tính năng đã chạy/mới thiết kế, synthetic/real và mục tiêu/kết quả. Không commit secret, DB, participant ledger hoặc model binary chưa rà soát.
