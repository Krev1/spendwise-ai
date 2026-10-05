# 01 — Đặc tả yêu cầu: SpendWise AI

Phiên bản: 0.1 — bộ tài liệu khởi động đồ án, chưa phải ứng dụng đã hoàn thành.

## 1. Bài toán và mục tiêu

Sinh viên và người mới đi làm thường ghi chi tiêu bằng mô tả ngắn như “cơm trưa”, “đổ xăng” hoặc “tiền phòng tháng 10”. Khi tổng hợp theo tháng, họ phải tự chọn danh mục cho từng dòng. SpendWise AI hỗ trợ ghi nhận thu–chi, gợi ý danh mục cho mô tả khoản chi tiếng Việt và cho phép người dùng kiểm tra, sửa nhãn trước khi lưu.

Đồ án có hai kết quả cần đánh giá riêng:

1. **Sản phẩm:** ứng dụng chạy trên máy cá nhân, ghi nhận giao dịch đúng, cho phép sửa/xóa và tổng hợp số tiền đúng.
2. **Nghiên cứu AI:** tự xây dựng dữ liệu có nhãn, huấn luyện mô hình phân loại văn bản, so sánh với baseline và đánh giá trên tập kiểm thử độc lập.

Việc có một giao diện chạy được chưa chứng minh mô hình tốt. Việc mô hình đạt điểm cao trên dữ liệu ví dụ cũng chưa chứng minh ứng dụng phù hợp với giao dịch thực tế.

## 2. Quyết định đã chốt và giả định

| Nội dung | Trạng thái | Hệ quả |
|---|---|---|
| Người dùng đầu tiên gồm sinh viên và người mới đi làm | Đã chốt | Dữ liệu và ví dụ thử phải bao gồm cả hai nhóm |
| Nhập giao dịch bằng tay và CSV theo mẫu | Đã chốt | MVP cần biểu mẫu nhập tay và quy trình nhập CSV có xem trước |
| AI trước hết phân loại mô tả khoản chi tiếng Việt | Đã chốt | Chưa cần chatbot hay huấn luyện mô hình sinh văn bản |
| Sinh viên tự huấn luyện và giải thích được mô hình | Đã chốt | Cần lưu mã huấn luyện, cách chia dữ liệu và báo cáo đánh giá |
| Ngân sách phần mềm/API của dự án là 0 đồng | Đã chốt | Không có thành phần bắt buộc dùng API trả phí |
| Chạy local trên laptop Windows, CPU | Giả định cần kiểm tra | Kiểm tra cấu hình máy trước khi chốt khả năng vận hành |
| Python, Streamlit và SQLite | Thiết kế đề xuất | Dùng để giảm số công nghệ phải học; được chốt trong tài liệu thiết kế |
| Tám danh mục khoản chi ở mục 4 | Đề xuất cần kiểm tra bằng dữ liệu | Có thể chỉnh trước khi đóng băng bộ nhãn và huấn luyện |
| Yêu cầu và rubric của trường | Chưa có thông tin | Người học cần xác minh; bộ tài liệu này chưa chứng minh trường chấp nhận đề tài |

“0 đồng” ở đây là không yêu cầu trả phí phần mềm/API cho sản phẩm. Máy tính, điện và Internet hiện có vẫn là nguồn lực cần thiết. Công cụ AI hỗ trợ làm đồ án có thể có hạn mức hoặc phí tài khoản riêng; không coi việc sử dụng chúng là miễn phí được bảo đảm.

## 3. Người dùng và tình huống chính

**Sinh viên:** nhập các khoản ăn uống, đi lại, học tập, tiền phòng; cuối tháng xem khoản nào chiếm nhiều tiền nhất.

**Người mới đi làm:** ghi nhận thu nhập thủ công, nhập danh sách chi tiêu theo mẫu và theo dõi chênh lệch thu–chi trong tháng.

Một luồng sử dụng điển hình:

1. Người dùng nhập ngày, số tiền và mô tả “cơm trưa ở căng tin”.
2. Mô hình đề xuất `an_uong`; giao diện ghi rõ đây là gợi ý.
3. Người dùng xác nhận hoặc chọn một nhãn khác.
4. Ứng dụng lưu giao dịch cùng thông tin cần thiết để truy vết gợi ý và quyết định của người dùng.
5. Dashboard tính tổng chi theo danh mục từ các giao dịch đã lưu.

## 4. Danh mục khoản chi và quy tắc gán nhãn

Mô hình dự đoán một trong tám nhãn dưới đây. Slug là mã dùng trong dữ liệu, huấn luyện và ứng dụng; tên hiển thị dành cho người dùng.

| Slug | Tên hiển thị | Ví dụ | Quy tắc khi dễ nhầm |
|---|---|---|---|
| `an_uong` | Ăn uống | cơm trưa, cà phê, mua rau | Thực phẩm và đồ uống dùng hằng ngày |
| `di_chuyen` | Di chuyển | vé xe buýt, đổ xăng, gửi xe | Chi trực tiếp cho việc đi lại |
| `nha_o_hoa_don` | Nhà ở và hóa đơn | tiền phòng, điện, nước, Internet | Hóa đơn sinh hoạt định kỳ thuộc nhóm này |
| `hoc_tap` | Học tập | học phí, giáo trình, khóa học | Sách/tài liệu phục vụ học tập; quy tắc cần ghi trong hướng dẫn gán nhãn |
| `mua_sam` | Mua sắm | quần áo, tai nghe, đồ dùng cá nhân | Hàng hóa không thuộc nhóm chuyên biệt khác |
| `giai_tri` | Giải trí | vé phim, game, hoạt động vui chơi | Sách truyện để giải trí thuộc nhóm này nếu mục đích đã rõ |
| `suc_khoe` | Sức khỏe | khám bệnh, thuốc, xét nghiệm | Chi chăm sóc sức khỏe |
| `khac` | Khác | quà biếu, khoản chi chưa có nhóm phù hợp | Chỉ dùng theo quy tắc đã ghi, tránh biến thành nơi chứa mọi dữ liệu khó |

Mô tả mơ hồ như “chuyển khoản” hoặc “mua đồ” có thể không đủ thông tin để xác định danh mục. Người dùng chọn nhãn theo ngữ cảnh thực tế. Mô hình tám lớp vẫn có thể đưa ra một nhãn và điểm cao; điểm cao không chứng minh nó nhận biết được mô tả ngoài phân phối dữ liệu.

Khoản **thu** do người dùng nhận diện và nhập thủ công, không đưa qua mô hình tám nhãn khoản chi. Hợp đồng dữ liệu cho khoản thu phải được tài liệu thiết kế quy định riêng và không bổ sung nhãn thu vào đầu ra của bộ phân loại này.

## 5. Phạm vi phiên bản đầu

**Bao gồm:** nhập tay; xem, sửa, xóa giao dịch; CSV theo mẫu với xem trước và kiểm tra; gợi ý nhãn khoản chi; xác nhận nhãn; tổng hợp thu–chi theo tháng/danh mục; lưu lịch sử sửa nhãn; huấn luyện và đánh giá mô hình trên CPU; tài liệu học và hướng dẫn tái lập.

**Chưa bao gồm:** kết nối ngân hàng; tự đọc mọi định dạng sao kê; OCR hóa đơn; nhiều tài khoản người dùng; đồng bộ đám mây; ứng dụng di động; chatbot dùng LLM/API; dự báo giá tài sản; tư vấn đầu tư; mô hình phát hiện gian lận; tự động huấn luyện lại sau mỗi lần sửa nhãn.

Không thêm các chức năng ngoài phạm vi này vào MVP nếu chưa cập nhật yêu cầu, thiết kế, kế hoạch và tác động tới phần đánh giá đồ án.

## 6. Yêu cầu chức năng và tiêu chí chấp nhận

### REQ-01 — Nhập giao dịch bằng tay

Biểu mẫu có ngày, loại giao dịch thu/chi, số tiền VND nguyên dương từ `1` đến `1000000000000` và mô tả từ 1 đến 300 ký tự sau khi bỏ khoảng trắng đầu/cuối. Khoản chi có một danh mục thuộc tám nhãn đã chốt. Khoản thu được nhận diện thủ công, không có category của bộ phân loại khoản chi. Khoản chi chưa được xác nhận nhãn chưa được lưu thành giao dịch hoàn tất.

**Chấp nhận khi:** nhập ngày `2026-10-05`, chi `40000`, mô tả “cơm trưa”, xác nhận `an_uong` tạo đúng một giao dịch. Số tiền `0`, số âm, số thập phân, lớn hơn giới hạn, ngày không hợp lệ, mô tả trống hoặc dài hơn 300 ký tự bị từ chối với lỗi dễ hiểu và không tạo bản ghi.

### REQ-02 — Xem, lọc, sửa và xóa

Người dùng xem được danh sách giao dịch, lọc theo khoảng ngày, loại thu/chi và danh mục khoản chi. Sửa giao dịch cập nhật tổng hợp. Xóa cần một bước xác nhận trên giao diện và cập nhật tổng hợp.

**Chấp nhận khi:** đổi khoản chi từ `40000` thành `50000` làm tổng chi tăng đúng `10000`; xóa khoản `120000` làm tổng chi giảm đúng `120000`. Lọc tháng 10 không bao gồm giao dịch ngày 30/09 hoặc 01/11.

### REQ-03 — Gợi ý danh mục bằng mô hình tự huấn luyện

Ứng dụng tải một artifact mô hình đã huấn luyện. Với khoản chi có mô tả hợp lệ, nó hiển thị nhãn đề xuất, phiên bản mô hình và điểm mô hình khi có. Người dùng phải xác nhận hoặc sửa nhãn trước khi lưu; sửa mô tả thì gợi ý cũ không được âm thầm giữ như thể thuộc mô tả mới.

**Chấp nhận khi:** mô tả “tiền phòng tháng 10” tạo được một đầu ra thuộc tám nhãn; giao diện cho phép chọn nhãn khác; bản ghi cuối cùng dùng nhãn người dùng xác nhận. Nếu chưa có artifact, nhập tay vẫn hoạt động và giao diện giải thích rằng gợi ý AI chưa khả dụng.

Đúng/sai của từng câu ví dụ được đánh giá trong báo cáo mô hình. Không yêu cầu mọi mô tả đều được dự đoán đúng để coi pipeline kỹ thuật là hoạt động.

### REQ-04 — Xem trước và kiểm tra CSV theo mẫu

Ứng dụng cung cấp mẫu CSV UTF-8 với header thống nhất:

```csv
transaction_id,date,transaction_type,amount_vnd,description,category
```

`transaction_id` phải ổn định và không trống; không tạo ID mới cho cùng dòng nguồn mỗi lần import. Ngày dùng `YYYY-MM-DD`, loại là `income` hoặc `expense`, VND nguyên nằm trong giới hạn REQ-01 và mô tả theo giới hạn REQ-01. `category` để trống với `income`; với `expense` có thể để trống trong file để nhận gợi ý, nhưng cần xác nhận trước khi lưu. Nhãn nhập sẵn của khoản chi cũng phải được người dùng xem xét trong bước xác nhận batch.

Trước khi lưu, người dùng nhìn thấy số dòng, lỗi theo dòng, dữ liệu đã chuẩn hóa và danh mục được đề xuất hoặc nhập sẵn. Giới hạn đề xuất là 5.000 dòng dữ liệu và 2 MB mỗi file, cần xác minh bằng thử nghiệm trên máy thật.

**Chấp nhận khi:** một file có ba dòng hợp lệ hiển thị đúng ba dòng; một file có ngày `2026-02-30`, số tiền `12.5`, ID trống, ID lặp trong cùng batch hoặc danh mục không hợp lệ báo chính xác dòng lỗi. File vượt giới hạn bị từ chối rõ ràng. Toàn bộ batch chưa được ghi vào cơ sở dữ liệu khi còn dòng lỗi hoặc còn khoản chi chưa xác nhận danh mục.

### REQ-05 — Nhập CSV nguyên tử và không thêm lại cùng batch

Sau khi kiểm tra và xác nhận, toàn bộ thay đổi của batch được lưu trong một giao dịch cơ sở dữ liệu. Nếu có lỗi khi lưu, không để lại một phần batch. Hệ thống lưu fingerprint payload nguồn đã chuẩn hóa **trước gợi ý AI và trước sửa nhãn của người dùng**, gắn với ID nguồn ổn định. Với ID đã tồn tại: payload nguồn giống nhau thì bỏ qua; payload nguồn khác nhau thì báo xung đột và từ chối toàn batch. Không dùng import để âm thầm ghi đè giao dịch đã lưu.

**Chấp nhận khi:** import file ba ID mới thành công làm số giao dịch tăng ba; import lại cùng nội dung, kể cả đổi tên file, làm số giao dịch tăng không. Người dùng sửa nhãn một giao dịch sau lần import đầu rồi import lại cùng nguồn thì vẫn bỏ qua và giữ nhãn đã sửa. Batch gồm một ID mới và một ID cũ có payload nguồn khác bị từ chối toàn bộ, không ghi ID mới. Lỗi được mô phỏng khi ghi dòng thứ hai không để lại dòng thứ nhất. Hai dòng có ID khác nhau nhưng cùng ngày/số tiền/mô tả có thể là hai giao dịch thực và không bị tự động gộp chỉ vì giống nhau.

Cơ chế trên cũng bảo vệ batch chồng lấn nếu các giao dịch nguồn giữ nguyên ID. File khác tạo ID mới cho các giao dịch cũ không được tự nhận diện chắc chắn; MVP không hứa phát hiện mọi giao dịch trùng khi nguồn không duy trì ID ổn định. Tài liệu thiết kế quy định chính xác canonical payload và phạm vi định danh.

### REQ-06 — Dashboard thu–chi chính xác

Dashboard hiển thị tổng thu, tổng chi, chênh lệch thu–chi trong kỳ và tổng chi theo danh mục. Bộ lọc tháng/năm dùng ngày của giao dịch. Mọi tổng số tiền được tính bằng mã chương trình với số nguyên VND, không dùng đầu ra mô hình để cộng hoặc diễn giải thành số dư tài khoản ngân hàng.

**Chấp nhận khi:** dữ liệu tháng 10 có thu `2000000`, chi `40000` và `120000` cho tổng thu `2000000`, tổng chi `160000`, chênh lệch `1840000`. Sau khi đổi `40000` thành `50000`, tổng chi là `170000`. Tháng không có dữ liệu hiển thị giá trị 0 và trạng thái trống rõ ràng.

### REQ-07 — Truy vết gợi ý và sửa nhãn

Mỗi khoản chi lưu được nguồn nhập, nhãn mô hình đề xuất nếu có, điểm mô hình nếu có, phiên bản mô hình nếu có, nhãn người dùng xác nhận và thời điểm xác nhận. Khi người dùng đổi nhãn đã lưu, lịch sử ghi nhãn cũ, nhãn mới, thời điểm và hành động xác nhận của người dùng.

**Chấp nhận khi:** mô hình đề xuất `mua_sam`, người dùng xác nhận `hoc_tap`; giao dịch cuối cùng là `hoc_tap` và thông tin gợi ý vẫn truy vết được. Lần sửa tiếp theo sang `giai_tri` tạo một sự kiện lịch sử mới. Dữ liệu chỉ do AI dự đoán không được đánh dấu là đã được con người gán nhãn.

### REQ-08 — Chuẩn bị dữ liệu huấn luyện có nguồn gốc

Mỗi mẫu huấn luyện có ID, mô tả, nhãn, nguồn, trạng thái kiểm tra nhãn và thông tin nhóm cần thiết để chia dữ liệu. Dữ liệu tự tạo được đánh dấu là tự tạo. Dữ liệu thực chỉ được dùng khi người cung cấp có quyền chia sẻ và đồng ý với mục đích sử dụng. Xóa tên người, số tài khoản và thông tin nhận diện không cần thiết trước khi đưa vào bộ dữ liệu đồ án.

**Chấp nhận khi:** đọc một mẫu bất kỳ biết nó là dữ liệu tự viết hay dữ liệu thực đã được phép; nhãn thuộc đúng bộ nhãn; có hướng dẫn xử lý câu mơ hồ và bảng phân bố nhãn. CSV giao dịch không tự động trở thành dữ liệu huấn luyện nếu chưa qua quy trình lựa chọn, kiểm tra và làm sạch.

### REQ-09 — Huấn luyện, so sánh và đánh giá có thể tái lập

Pipeline chạy được trên CPU, tách train/validation/test trước khi fit đặc trưng và có seed cố định. Các mô tả trùng, gần trùng hoặc biến thể của cùng một mẫu phải được xem xét theo nhóm để giảm rò rỉ giữa các tập. Chọn mô hình và tham số bằng train/validation; giữ test để đánh giá cuối cùng.

So sánh ít nhất baseline đơn giản với mô hình văn bản được tự huấn luyện. Báo cáo macro-F1, precision/recall/F1 theo lớp, confusion matrix, số mẫu từng tập, phân tích lỗi và thời gian suy luận trên máy được ghi cấu hình. Accuracy có thể bổ sung nhưng không thay thế các chỉ số theo lớp.

**Chấp nhận khi:** một người khác làm theo lệnh và phiên bản phụ thuộc được ghi có thể tái tạo mô hình và báo cáo trong sai số đã mô tả; có kiểm tra giao cắt dữ liệu giữa các tập; test không được dùng chọn ngưỡng hoặc hyperparameter. Nếu test chỉ gồm câu tự tạo, báo cáo phải nói rõ chưa có bằng chứng khả năng tổng quát hóa trên giao dịch thực.

Các mục tiêu chất lượng ban đầu do nhóm đề xuất là macro-F1 từ `0.80`, coverage của nhóm trên ngưỡng từ `0.60` và selective accuracy trong nhóm đó từ `0.85`. Đây là **mục tiêu thiết kế chưa đo, chưa có baseline và chưa được người dùng hoặc giảng viên phê duyệt**, không phải kết quả đã đạt. Đánh giá khả năng dùng trên dữ liệu thực cần tập test thực được phép sử dụng, giữ độc lập, có ít nhất 20 mẫu mỗi lớp; số lượng này vẫn là quy mô đánh giá ban đầu và chưa bảo đảm kết luận mạnh.

Hoàn tất phần nghiên cứu dựa vào quy trình, báo cáo trung thực, khả năng tái lập và phân tích, kể cả khi không đạt mục tiêu. Khi chưa đạt các mục tiêu hoặc chưa có test thực phù hợp, ghi “chưa đủ bằng chứng đạt chất lượng dự kiến trên dữ liệu thực”. Không sửa tập test để làm đẹp điểm số. Rubric trường có thể yêu cầu tiêu chí khác và cần được đối chiếu riêng.

### REQ-10 — Điểm mô hình và xử lý gợi ý yếu

Nếu sử dụng `predict_proba`, giao diện gọi giá trị đó là **điểm mô hình**, không gọi là “xác suất dự đoán đúng”. Giá trị chưa được calibration. Ngưỡng `0.60` chỉ là giá trị thử ban đầu; ngưỡng vận hành cần chọn bằng validation và ghi lại trong cấu hình/báo cáo. Dưới ngưỡng, giao diện nhắc người dùng tự xem xét danh mục; trên ngưỡng vẫn cần xác nhận.

**Chấp nhận khi:** khi thử ép điểm `0.40`, giao diện hiện trạng thái cần kiểm tra; khi thử điểm `0.85`, vẫn có bước xác nhận. Báo cáo nêu coverage (số mẫu trên ngưỡng / số mẫu đánh giá) và selective accuracy (số mẫu đúng trên ngưỡng / số mẫu trên ngưỡng). Nếu không có mẫu trên ngưỡng, selective accuracy là chưa xác định, không ghi 100%. Không tuyên bố cơ chế này bảo đảm phát hiện dữ liệu ngoài phân phối.

## 7. Yêu cầu vận hành và chất lượng

### REQ-11 — Hoạt động local và suy luận offline

Sau khi cài phụ thuộc và có artifact, nhập tay, xem/sửa/xóa, CSV, dashboard và suy luận không cần Internet. Không có lệnh gọi API trả phí trong luồng vận hành. Tải bộ cài hoặc thư viện lần đầu có thể cần Internet.

**Chấp nhận khi:** ngắt Internet vẫn hoàn thành luồng nhập khoản chi, nhận gợi ý, xác nhận và xem dashboard. Ghi cấu hình máy đo thử và thời gian suy luận; chưa cam kết một con số hiệu năng khi chưa đo.

### REQ-12 — Lưu bền vững và kiểm soát dữ liệu

Giao dịch được lưu trong SQLite tại vị trí local rõ ràng. Đóng và mở lại ứng dụng vẫn còn dữ liệu. Hướng dẫn chỉ rõ cách sao lưu database, khôi phục bản sao, xóa dữ liệu thử và tránh đưa dữ liệu cá nhân vào Git. Không gửi giao dịch tới dịch vụ bên ngoài bằng mặc định.

**Chấp nhận khi:** thêm giao dịch rồi khởi động lại vẫn nhìn thấy bản ghi; sao lưu và khôi phục đưa lại đúng dữ liệu; repository mẫu chứa dữ liệu demo vô danh và không chứa database cá nhân.

### REQ-13 — Học tập và giải thích được

Bài học, bài tập, nhật ký và hướng dẫn bảo vệ được lưu tại [Krev1/Learn — spendwise-ai](https://github.com/Krev1/Learn/tree/main/spendwise-ai); repo dự án giữ code, test và tài liệu SDD. Theo D13, hai luồng làm việc độc lập: dự án cập nhật bàn giao kỹ thuật theo mốc; Mentor tạo/cập nhật bài học trong Learn từ commit đã chọn. Mỗi bài học ghi TASK/REQ và commit code tham chiếu. Việc người học chưa hoàn thành bài không chặn task kỹ thuật đủ đầu vào; mức hiểu chỉ được ghi trong Learn sau bằng chứng thực hành.

Mỗi giai đoạn có tệp giải thích bằng tiếng Việt: mục tiêu, kiến thức cần học, đầu vào/đầu ra, lệnh thực hành, cách kiểm tra và lỗi thường gặp. Tài liệu cần giải thích TF-IDF, mô hình phân loại, split dữ liệu, leakage, metric, ngưỡng điểm và giới hạn của dữ liệu tự tạo. Người học tự chạy và ghi lại kết quả, không chỉ sao chép câu trả lời AI.

**Chấp nhận khi:** người học giải thích được một giao dịch từ lúc nhập đến lúc xuất hiện trên dashboard, và giải thích được một mẫu từ lúc gán nhãn đến lúc góp vào kết quả test. Có ví dụ tính hoặc diễn giải chỉ số bằng dữ liệu nhỏ để chuẩn bị bảo vệ.

## 8. Những quy tắc phải giữ xuyên suốt

- Số tiền VND là số nguyên dương; loại thu/chi quyết định ý nghĩa của giao dịch.
- Tám nhãn khoản chi có một nơi định nghĩa thống nhất cho dữ liệu, mô hình và giao diện.
- AI chỉ gợi ý; nhãn cuối cùng của giao dịch phải có xác nhận của người dùng.
- Số tiền và tổng hợp được tính bằng code từ dữ liệu đã lưu.
- Import chưa được commit không được tính trên dashboard.
- Nhãn dự đoán, nhãn được xác nhận và dữ liệu được duyệt để huấn luyện là các trạng thái khác nhau.
- Kết quả test, dữ liệu thật và việc trường chấp nhận đề tài chỉ được ghi khi có bằng chứng tương ứng.

## 9. Điều kiện hoàn tất theo từng mức

| Mức | Hoàn tất khi | Bằng chứng cần lưu |
|---|---|---|
| Bộ SDD khởi động | Yêu cầu, thiết kế, kế hoạch, workflow và prompt nhất quán; giả định còn lại được ghi | Phiên bản tài liệu và danh sách quyết định |
| MVP ứng dụng | Các REQ chức năng/vận hành đã được thực hiện và tiêu chí chấp nhận đã chạy | Mã nguồn, hướng dẫn chạy, kết quả kiểm tra và ảnh/luồng demo |
| Phần nghiên cứu | Có dữ liệu có nguồn gốc, baseline, mô hình tự huấn luyện, đánh giá tái lập và phân tích giới hạn | Dataset card, cấu hình, artifact, báo cáo và nhật ký thực nghiệm |
| Sẵn sàng bảo vệ | Người học hiểu phương pháp, demo được và đối chiếu được rubric của trường | Slide/dàn ý, câu hỏi luyện tập, báo cáo theo mẫu trường |

Tài liệu hiện tại đáp ứng vai trò khởi động. Nó không tự chứng nhận ba mức còn lại đã hoàn tất.

## 10. Việc cần xác minh trước khi đóng băng spec

1. Rubric, yêu cầu báo cáo, yêu cầu tự huấn luyện và tiêu chuẩn đánh giá của trường.
2. Cấu hình laptop, phiên bản Python phù hợp và thời gian có thể dành mỗi tuần.
3. Tám danh mục có bao phủ nhu cầu của người thử hay cần điều chỉnh.
4. Khả năng lấy dữ liệu thực được phép sử dụng; nếu chưa có, phạm vi kết luận chỉ trên dữ liệu tự tạo.

Các mục này được cập nhật thành quyết định có ngày và lý do. Tiến hành các bước học, dựng baseline và thiết kế độc lập trong khi chờ thông tin, tránh biến điều chưa xác minh thành cam kết.
