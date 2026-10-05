# SpendWise AI — Dữ liệu và nghiên cứu mô hình

Ngày lập: 05/10/2026. Trạng thái: đã có seed/validator, baseline prototype TASK-07 và grouped split prototype TASK-08 với 256 train/50 validation/50 test trên 356 câu hư cấu. B0 chỉ fit fixture riêng trong bộ nhớ. **Chưa thu dữ liệu thật, chưa có TF-IDF + NB/LR hoặc đánh giá nghiên cứu.** Nhãn/quan hệ chưa người duyệt; holdout thiếu lớp. Số lượng mục tiêu bên dưới không phải số đã thu; seed và [bundle prototype](../data/splits/README.md) ghi số thực.

Tài liệu này dành cho người học ngành Trí tuệ nhân tạo muốn vừa xây sản phẩm, vừa hiểu mỗi quyết định để bảo vệ đồ án. Đọc cùng đặc tả yêu cầu và tài liệu thiết kế trong thư mục `docs/`.

## 1. Bài toán cần giải quyết

Người dùng là sinh viên và người mới đi làm. Họ nhập khoản chi bằng tay hoặc CSV theo mẫu. Mô hình đọc **mô tả khoản chi bằng tiếng Việt** và đề xuất một trong tám nhãn. Người dùng xem, sửa nếu cần và xác nhận trước khi ứng dụng lưu nhãn cuối cùng.

Ví dụ: `ăn trưa cơm gà` → `an_uong`. Mô hình chưa cần biết số tiền, ngày giao dịch, thu nhập hay danh tính để làm bài toán này.

Đây là bài toán **phân loại văn bản có giám sát, nhiều lớp, một nhãn cho mỗi mô tả**. Bạn tự xây dữ liệu có nhãn, tự chạy `fit()` để học tham số, đánh giá và lưu mô hình. Dùng scikit-learn để huấn luyện Logistic Regression hoặc Naive Bayes vẫn là tự huấn luyện mô hình học máy; không cần viết lại thuật toán tối ưu từ đầu.

Phần AI là phân loại mô tả. Tổng chi tháng, biểu đồ danh mục và kiểm tra số tiền là phép tính hoặc quy tắc của ứng dụng. Không gọi các phép cộng hay một bảng từ khóa là mô hình học máy.

Phạm vi phiên bản đầu: khoản **chi**. Khoản thu, chuyển tiền giữa tài khoản, hoàn tiền, dự báo tài chính, khuyến nghị đầu tư và phát hiện gian lận chưa thuộc bài toán này. Trước khi phân loại, bộ nhập dữ liệu phải kiểm tra loại giao dịch; không đẩy mọi dòng vào mô hình rồi kỳ vọng mô hình tự phát hiện ngoài phạm vi.

## 2. Bộ nhãn và nguyên tắc gán nhãn

Các slug dưới đây là hợp đồng giữa dữ liệu, mô hình, SQLite và giao diện. Tên hiển thị có thể đổi; slug chỉ đổi khi tăng phiên bản dữ liệu và cập nhật toàn bộ hệ thống.

| Slug | Tên hiển thị | Bao gồm | Ví dụ minh họa tự tạo |
|---|---|---|---|
| `an_uong` | Ăn uống | Bữa ăn, đồ uống, thực phẩm để ăn/nấu | `mua rau và thịt`, `cà phê sáng` |
| `di_chuyen` | Di chuyển | Vé xe, đi xe công nghệ, xăng, gửi xe, sửa phương tiện cá nhân | `đổ xăng`, `vé xe buýt` |
| `nha_o_hoa_don` | Nhà ở và hóa đơn | Tiền thuê nhà, điện, nước, internet nhà, cước điện thoại | `đóng tiền trọ`, `cước điện thoại tháng này` |
| `hoc_tap` | Học tập | Học phí, sách học, tài liệu, dụng cụ và khóa học phục vụ học tập | `mua giáo trình`, `học phí tiếng Anh` |
| `mua_sam` | Mua sắm | Quần áo, đồ dùng, mỹ phẩm, hàng hóa cá nhân không thuộc lớp chuyên biệt | `mua áo sơ mi`, `mua sữa rửa mặt` |
| `giai_tri` | Giải trí | Vé phim, trò chơi, dịch vụ nghe nhạc/xem phim, hoạt động vui chơi | `vé xem phim`, `gói nghe nhạc` |
| `suc_khoe` | Sức khỏe | Khám, thuốc, xét nghiệm, dịch vụ và vật dụng y tế có mô tả rõ | `khám răng`, `mua thuốc cảm` |
| `khac` | Khác | Khoản chi hợp lệ ngoài bảy lớp trên, hoặc mô tả thiếu ngữ cảnh sau khi đã hỏi lại | `quà mừng cưới`, `chi cá nhân` |

### Các trường hợp dễ nhầm

1. **Đặt đồ ăn và phí giao hàng:** `đặt cơm giao tận nhà` là `an_uong`. Phí giao hàng nằm chung trong hóa đơn đồ ăn giữ nhãn này. Một dòng riêng `phí gửi bưu kiện` là `khac`; đây là quyết định của bộ nhãn MVP, không có nghĩa mọi dự án phải phân loại như vậy.
2. **Tên ứng dụng không đủ:** `Grab đi làm` là `di_chuyen`; `GrabFood cơm trưa` là `an_uong`; chỉ `Grab` chưa biết dịch vụ nào → hỏi người gán nhãn hoặc `khac` nếu không bổ sung được.
3. **Nhà thuốc và mỹ phẩm:** `thuốc đau đầu` là `suc_khoe`; `kem dưỡng da mua ở nhà thuốc` là `mua_sam`. Nơi mua không quyết định mục đích chi.
4. **Cửa hàng và sàn thương mại:** chỉ `Shopee` hoặc `siêu thị` không đủ biết mua gì. `siêu thị mua thực phẩm` là `an_uong`; `siêu thị mua nước giặt` là `mua_sam`.
5. **Sách và thiết bị:** `sách luyện thi` là `hoc_tap`; `truyện đọc cuối tuần` là `giai_tri`; `mua laptop` mặc định `mua_sam`. Chỉ xếp vào `hoc_tap` khi mô tả nêu rõ mục đích học tập theo quy tắc đã thống nhất. Ghi quy tắc này trong hướng dẫn, không suy đoán theo nghề của người dùng.
6. **Khoản chi ghép:** `cơm trưa và vé phim` cần tách thành hai giao dịch trước khi gán nhãn. Không lấy nhãn đầu tiên để làm ground truth.
7. **Khoản thu và chuyển khoản:** `nhận lương`, `chuyển từ ví sang ngân hàng` cần loại khỏi dữ liệu huấn luyện khoản chi. Chúng không tự động trở thành lớp `khac`.
8. **Rỗng và vô nghĩa:** chuỗi rỗng, chỉ dấu câu hoặc văn bản lỗi là dữ liệu không hợp lệ, không phải mẫu để dạy lớp `khac`.

`khac` là một lớp có nhãn trong miền dữ liệu. Nó **không phải** cơ chế bảo đảm phát hiện mọi câu ngoài miền. Câu `đặt lịch họp nhóm` có thể bị mô hình gán nhầm vào một lớp với điểm cao; cần kiểm thử và luôn giữ quyền xác nhận của người dùng.

### Quy trình gán nhãn

1. Viết và đóng phiên bản hướng dẫn gán nhãn trước khi xử lý hàng loạt.
2. Hai người gán độc lập một tập thử 50–100 mẫu, chưa xem nhãn của nhau. Nếu chỉ có một người, mời giảng viên/bạn học rà soát một phần và ghi rõ giới hạn.
3. Ghi số lượng đồng thuận, loại bất đồng và cách giải quyết. Không sửa mô tả theo nhãn để làm cho mẫu trở nên dễ đoán.
4. Với từng bất đồng, hỏi lại người cung cấp nếu có thể; người rà soát chốt theo hướng dẫn. Nếu không đủ thông tin, ghi lý do rồi dùng `khac` hoặc loại mẫu không hợp lệ.
5. Khi đổi định nghĩa lớp, cập nhật phiên bản hướng dẫn, rà lại các mẫu liên quan và tạo phiên bản dataset mới.

Có thể báo cáo tỉ lệ đồng thuận thô và Cohen's kappa khi có hai người gán độc lập. Kappa bổ sung thông tin về đồng thuận vượt mức ngẫu nhiên; không biến một quy tắc nhãn chưa rõ thành đúng. Dùng số đo thực tế, không điền số giả để làm đẹp báo cáo. [API Cohen's kappa](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html).

## 3. Kế hoạch dữ liệu với ngân sách phí công cụ bằng 0

### Các mốc thu thập

| Mốc | Dữ liệu | Dùng để làm gì? | Chưa được kết luận gì? |
|---|---|---|---|
| Khởi động | Seed hư cấu có phiên bản; số thực ghi trong dataset card | Thử schema, bộ nhập, lệnh train, lưu/tải mô hình | Không chứng minh mô hình dùng tốt ngoài thực tế |
| Thử nghiệm sớm | Một tập mô tả thật nhỏ đã được đồng ý sử dụng | Sửa hướng dẫn gán nhãn, khảo sát sự đa dạng, kiểm tra split | Chưa suy rộng sang mọi sinh viên/người đi làm |
| Mục tiêu đồ án | Khoảng 1.200 mẫu thật hợp lệ, hướng tới 150/lớp sau làm sạch | So sánh mô hình và đánh giá trên người chưa gặp | Không bảo đảm đạt điểm chỉ vì đủ mẫu |
| Kiểm tra chính thức | Tập test thật có tối thiểu 20 mô tả khác nhau/lớp, từ người giữ lại hoàn toàn | Đánh giá một lần sau khi chốt phương pháp | Không dùng test này để chọn mô hình hay threshold |

Tỉ lệ lớp cân bằng là mục tiêu thu thập để nghiên cứu; phân bố ngoài thực tế có thể khác. Ghi rõ cách lấy mẫu để người đọc không hiểu nhầm test cân bằng phản ánh tỷ lệ giao dịch thực tế.

Hướng thu thập: người tự nguyện tự ghi mô tả khoản chi theo cách họ thường ghi. Khuyến khích nhiều người, nhiều cách viết, câu ngắn, câu không dấu, viết tắt và lỗi gõ tự nhiên. Tránh lấy toàn bộ dữ liệu từ một người hoặc yêu cầu mọi người điền đúng một khuôn câu.

Nếu không đủ mẫu, ưu tiên thu thập bổ sung. Có thể hạ phạm vi sau khi cập nhật đặc tả hoặc báo cáo nghiên cứu quy mô nhỏ với giới hạn rõ. Không gọi 80 câu tự tạo là “1.200 giao dịch thực”; không nhân bản câu để đủ số lượng. Ngân sách phí API/cloud bằng 0 giả định dùng máy tính sẵn có; vẫn cần thời gian gán nhãn và tài nguyên điện/mạng hiện có.

### Đồng ý sử dụng và giảm dữ liệu nhạy cảm

Mẫu lời mời có thể dùng:

> Tôi đang làm đồ án phân loại mô tả khoản chi. Bạn có thể tự nguyện cung cấp các mô tả đã bỏ tên, số tài khoản, địa chỉ, số điện thoại và thông tin nhận dạng. Tôi chỉ dùng chúng cho nghiên cứu đã nêu; không cần số tiền hoặc thu nhập. Bạn có thể từ chối hoặc yêu cầu rút dữ liệu trước khi phiên bản dữ liệu được khóa. Việc chia sẻ dữ liệu công khai sẽ được xin phép riêng.

Đây là mẫu giao tiếp của dự án, cần điều chỉnh theo hướng dẫn nghiên cứu của trường. Ghi hình thức đồng ý và phạm vi sử dụng trong sổ thu thập riêng. `group_id` chỉ là mã như `p001`; bảng liên hệ nếu thật sự cần phải để riêng, không vào Git hay dataset mô hình.

Không tải lên kho công khai sao kê gốc, ảnh tài khoản, chi tiêu sức khỏe có thể nhận dạng hoặc CSV người dùng. Không suy ra rằng người dùng đồng ý cho huấn luyện chỉ vì họ đã lưu giao dịch trong ứng dụng. Lần đầu đưa mô tả vào tập nghiên cứu phải có đồng ý riêng và kiểm tra lại nội dung.

Lưu dữ liệu thật trên máy có kiểm soát truy cập; bản demo và kho mã dùng dữ liệu tự tạo. Nếu có yêu cầu rút mẫu đã sử dụng trong train, ghi dataset bị ảnh hưởng, loại mẫu và huấn luyện lại phiên bản thay thế khi cần. Không hứa xóa một hàng CSV là đã xóa ảnh hưởng khỏi mô hình đã huấn luyện.

### Schema CSV dành cho huấn luyện

Đây là schema dataset ML, khác với CSV giao dịch dùng để nhập vào ứng dụng.

| Cột | Kiểu/hợp đồng | Mục đích |
|---|---|---|
| `record_id` | Chuỗi duy nhất, không chứa danh tính | Truy vết một mẫu |
| `description` | UTF-8, không rỗng, đã loại thông tin nhận dạng | Đầu vào duy nhất của classifier |
| `label` | Một trong 8 slug cố định | Nhãn mục tiêu; seed dùng nhãn AI dự thảo, ground truth thật cần người duyệt |
| `group_id` | Mã người cung cấp; với mẫu tự tạo là mã nguồn/khuôn tạo | Giữ mẫu có quan hệ cùng một tập |
| `source` | `volunteer`, `author_synthetic` hoặc `public_synthetic` | Phân biệt nguồn thật và tự tạo |
| `is_synthetic` | `true`/`false`, nhất quán với `source` | Ngăn trộn kết quả thật với demo |

Ví dụ **tự tạo**, không phải dữ liệu thật:

```csv
record_id,description,label,group_id,source,is_synthetic
demo_001,ăn trưa cơm gà,an_uong,tpl_food_meal,author_synthetic,true
demo_002,vé xe buýt đến trường,di_chuyen,tpl_transport_ticket,author_synthetic,true
demo_003,tiền điện phòng trọ,nha_o_hoa_don,tpl_home_bill,author_synthetic,true
```

Tuyệt đối không dùng `label`, `group_id`, `source`, `is_synthetic` hoặc `record_id` làm đặc trưng dự đoán. Chúng phục vụ quản trị dữ liệu và đánh giá. Mô tả do chính tác giả viết nhưng không lấy từ một khoản chi thật có đồng ý vẫn ghi `author_synthetic`.

## 4. Làm sạch và chia tập để tránh rò rỉ dữ liệu

Rò rỉ xảy ra khi quá trình học hoặc chọn phương pháp biết thông tin lẽ ra chỉ được biết lúc kiểm tra. Để ngăn lỗi thường gặp, chia dữ liệu trước khi `fit` các bước học từ dữ liệu; dùng `Pipeline` để giữ vectorizer và classifier cùng nhau. [Hướng dẫn tránh rò rỉ của scikit-learn](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage).

### Làm sạch có kiểm soát

- Chuẩn hóa Unicode NFC, chữ thường, khoảng trắng; giữ dấu tiếng Việt ở cấu hình chính.
- Bỏ thông tin nhận dạng trước khi đưa vào dataset; ghi số lượng mẫu bị loại và lý do.
- Không tự động sửa mọi lỗi chính tả: lỗi gõ là một đặc điểm người dùng thực có thể tạo.
- Tạo khóa văn bản chuẩn hóa để phát hiện trùng. Mẫu cùng nội dung nhưng nhãn khác phải được rà soát, không giữ cả hai mà bỏ qua bất đồng.
- Phát hiện họ câu cùng khuôn: ví dụ các biến thể `ăn trưa cơm gà`, `ăn trưa cơm bò` do cùng một mẫu sinh ra, biến thể của cùng một giao dịch, hoặc near-duplicate có quan hệ thực đã được audit. Dựa vào nguồn tạo và rà soát thủ công; không nối mọi câu tự nhiên chỉ vì cùng danh mục, cùng món hay vài từ chung. Không xem các biến thể do cùng một khuôn sinh ra là các quan sát độc lập.
- Lưu kết quả audit như `normalized_text_hash`, `pattern_family_id`, lý do loại trong một manifest riêng; schema CSV ML vẫn có sáu cột.

Không bỏ từ tiếng Việt bằng danh sách stop words tiếng Anh. Không đưa phương pháp tách từ mới vào đúng một mô hình rồi kết luận khác biệt chỉ đến từ thuật toán classifier.

### Đơn vị chia tập và tỷ lệ

Mục tiêu là **khả năng phân loại mô tả của người chưa xuất hiện trong train**. Vì thế ưu tiên giữ toàn bộ mô tả của cùng người trong một tập. Với dữ liệu tự tạo, giữ cùng nguồn/khuôn tạo trong một tập. Các bộ chia theo nhóm của scikit-learn được thiết kế để tách nhóm giữa train và tập kiểm tra. [Tài liệu chia tập theo nhóm](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data).

Quy tắc dự án:

1. Audit trùng và họ khuôn trước khi huấn luyện. Gộp bản trùng hệt thành một bản chuẩn theo quy tắc định sẵn, lưu lịch sử. Báo số mẫu đã gộp và thay đổi phân bố; tập văn bản unique không còn phản ánh tần suất giao dịch gốc.
2. Tạo nhóm hiệu lực: nhóm gốc là `group_id`; nối các nhóm nếu chúng còn chứa một họ khuôn có quan hệ đã được người rà soát xác nhận. Lấy các thành phần liên thông làm đơn vị chia. Mục đích là không để người cung cấp hoặc họ câu cùng khuôn chạy sang nhiều tập.
3. Chia gần **70% train / 15% validation / 15% test**, seed khởi điểm `42`. Tỷ lệ theo mẫu chỉ gần đúng vì nhóm có kích thước khác nhau. Lưu thuật toán, seed, danh sách `record_id` và nhóm hiệu lực vào `split_manifest.csv`.
4. Trước khi khóa test, kiểm tra số mẫu/lớp, số người, phân bố nguồn, giao nhóm và giao khóa văn bản/họ khuôn. Có thể điều chỉnh kế hoạch lấy mẫu dựa trên các thống kê này; không dựa trên điểm mô hình.
5. Test chính thức chỉ dùng mô tả thật đã được đồng ý; hướng tới ≥20 mô tả khác nhau cho mỗi lớp và có nhiều người giữ lại. Test chỉ gồm người từng xuất hiện trong train không đủ để tuyên bố đánh giá người mới.
6. Khóa dataset, hướng dẫn nhãn, split và test bằng phiên bản/hash trước khi lựa chọn mô hình trên validation.

Không lặp seed đến khi “test đẹp”. Không chia random từng hàng rồi cho rằng không rò rỉ chỉ vì `record_id` khác nhau. Không di chuyển mẫu sai từ test về train và tiếp tục báo cáo cùng test là độc lập.

TASK-08 prototype theo A13 dùng seed hư cấu, namespace family/original phrase theo source ID/commit và union bắc cầu. Recipe liên kết `ai_conservative_prototype` chỉ giữ một số cặp cùng dịch vụ chung partition, không thay điều kiện người rà soát cho nghiên cứu thật. Audit heuristic gần trùng vẫn ghi `human_reviewed=false`. SGKF 7 fold/seed42, fold0 test prototype/fold1 validation/còn lại train; không retry seed/fold. Báo mọi lớp thiếu và lệch tỷ lệ. Bundle khóa bằng hash để dùng kiểm tra kỹ thuật; test thật và kết luận tám lớp vẫn chưa đủ điều kiện. [Task card](tasks/TASK-08.md) ghi hợp đồng và bằng chứng.

Một họ khuôn quá phổ biến có thể nối thành nhóm lớn. Khi đó phải ghi tradeoff, audit lại việc xác định họ khuôn và thu thập dữ liệu đa dạng hơn. Nếu thiếu lớp trong một tập, chưa đủ điều kiện cho đánh giá tám lớp; báo cáo thiếu dữ liệu hoặc sửa kế hoạch trước khi xem điểm. Không phá quy tắc giữ người riêng chỉ để đạt tỷ lệ tuyệt đối.

## 5. Hiểu TF-IDF trước khi train

Mô hình cần số thay vì chuỗi. Một vocabulary là danh sách các đặc trưng học từ train; mỗi mô tả trở thành vector có một vị trí cho mỗi đặc trưng. Chỉ một phần nhỏ vị trí khác 0 nên giữ ma trận sparse.

Với cấu hình IDF có làm trơn: `idf(t) = log((1 + N) / (1 + df(t))) + 1`, trong đó `N` là số mô tả train, `df(t)` là số mô tả chứa đặc trưng `t`. TF-IDF nhân trọng số tần suất với IDF rồi chuẩn hóa vector theo cấu hình. [Giải thích TF-IDF chính thức](https://scikit-learn.org/stable/modules/feature_extraction.html#tf-idf-term-weighting).

Ví dụ minh họa: trong ba câu `ăn cơm`, `ăn phở`, `vé xe`, đặc trưng `ăn` có `df=2`, còn `vé` có `df=1`. Theo công thức trên, IDF tương ứng khoảng 1,288 và 1,693 trước chuẩn hóa. Trọng số lớn hơn không tự có nghĩa nhãn nào đúng; classifier còn phải học từ các ví dụ có nhãn.

Hai cách biểu diễn cần phân biệt:

| Cách | Ý nghĩa | Điều cần kiểm chứng |
|---|---|---|
| Word n-gram | Dãy token như `ăn`, `trưa`, `ăn trưa` | Có hiệu quả với cụm mô tả và từ vựng đã gặp không? |
| Character n-gram | Dãy ký tự ngắn bên trong/ven token | Có bền hơn với lỗi gõ, viết tắt, cách viết khác nhau không? |
| Union | Ghép cả hai loại đặc trưng | Có tăng điểm đáng kể so với tăng số chiều/thời gian không? |

Với tokenizer theo khoảng trắng, `học phí` thành hai token; không tuyên bố đó là tách từ tiếng Việt hoàn chỉnh. Character n-gram có thể giữ một phần dấu hiệu khi cả từ chưa gặp, nhưng không đảm bảo hiểu được từ mới.

`fit()` học vocabulary và IDF từ **train**. `transform()` dùng lại đúng các giá trị đó cho validation, test và ứng dụng. Fit vectorizer trên toàn bộ dữ liệu rồi mới chia là sai quy trình, dù classifier chỉ fit trên train.

## 6. Các mô hình và baseline

| Mã | Phương pháp | Vai trò |
|---|---|---|
| B0 | `DummyClassifier(strategy="most_frequent")` | Mốc đơn giản: luôn chọn lớp phổ biến trong train |
| B1 | Bộ quy tắc từ khóa/cụm từ | Kiểm tra ML có ích hơn một giải pháp dễ viết hay không |
| M1 | TF-IDF + `MultinomialNB` | Mô hình học máy nhẹ, chạy CPU |
| M2 | TF-IDF + `LogisticRegression` | Mô hình tuyến tính có regularization để so sánh |

DummyClassifier không học quan hệ giữa mô tả và nhãn. Nó là baseline có chủ đích. [Tài liệu DummyClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html).

### Baseline từ khóa phải công bằng

Viết bảng từ khóa từ hiểu biết miền và train, đóng phiên bản trước khi xem test. Ví dụ `cơm`, `phở` cho ăn uống; `vé xe`, `xăng` cho di chuyển. Quy định xử lý nhiều lớp cùng khớp: ưu tiên cụm dài, rõ ngữ cảnh; nếu vẫn mâu thuẫn thì `khac` và đánh dấu cần xem lại. Không sửa quy tắc sau khi đọc lỗi test rồi giữ nguyên báo cáo điểm.

Xuất cả kết quả trên toàn bộ test và tỷ lệ quy tắc thực sự khớp. Không gán số `0.99` cho rule và đem so như xác suất học máy. Chính sách abstain của rule cần được mô tả riêng; so sánh macro-F1 dự đoán đầy đủ giữa các phương pháp là phép so sánh chính.

Prototype TASK-07 theo A12 xét hit dài trước (số token, số ký tự, thứ tự rule), loại hit ngắn bị chứa hoàn toàn trong hit đã giữ. Hit độc lập nhiều lớp trả `khac/conflict`; không hit trả `khac/no_match`. Alias không dấu phải khai báo, không bỏ dấu input ngầm. Rule version/hash khóa nội dung và thứ tự. B0 chỉ fit fixture hư cấu riêng cho smoke test, chưa fit seed hoặc tạo split/metric. TASK-10 dùng train của manifest TASK-08; demo TASK-07 không đo chất lượng thực.

### Naive Bayes học gì?

Trực giác: mô hình tích lũy mức xuất hiện của đặc trưng theo từng lớp, kết hợp với prior của lớp. Giả định “naive” coi đặc trưng độc lập có điều kiện theo nhãn. Khi dự đoán, cộng các log-score rồi chọn lớp có score cao nhất. MultinomialNB hỗ trợ đặc trưng không âm; TF-IDF có thể dùng dù là giá trị phân số. [Tài liệu MultinomialNB](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html).

Công thức khái quát: `score(c, x) = log P(c) + Σ_j x_j log θ_cj`. Làm trơn với `alpha` tránh một đặc trưng chưa gặp trong lớp làm score bị triệt tiêu. Dãy `alpha` đề xuất để thử trên validation: `0.5, 1.0, 2.0`; đây là lựa chọn thí nghiệm của dự án.

### Logistic Regression học gì?

Mỗi lớp có trọng số `w_c` và bias `b_c`; tính `z_c = w_c · x + b_c`, rồi dùng softmax để tạo phân bố điểm cho nhiều lớp. Huấn luyện tối ưu loss từ nhãn thật, kèm regularization. `C` điều khiển nghịch đảo độ mạnh regularization trong scikit-learn. [Tài liệu LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html).

Trực giác riêng cho dự án: nếu đặc trưng `vé xe` thường xuất hiện ở lớp di chuyển, mô hình có thể học trọng số hỗ trợ lớp đó. Một trọng số không chứng minh quan hệ nhân quả; nó phản ánh dữ liệu huấn luyện. Dãy `C` đề xuất: `0.5, 1.0, 2.0`, `max_iter=1000`, solver hỗ trợ nhiều lớp và sparse như `lbfgs`. Kiểm tra API phiên bản đã khóa khi triển khai; không sao chép tham số cũ từ bài hướng dẫn mà bỏ qua cảnh báo.

### Cấu hình thử nghiệm vừa sức

- Bắt đầu word TF-IDF với `ngram_range=(1, 2)`, giữ dấu, không bỏ stop words; cấu hình token cần ghi rõ.
- Với dataset thật, thử `min_df` là 1 hoặc 2 trên validation; dataset demo ít câu dùng 1 để tránh loại hết vocabulary.
- Với character, đề xuất `analyzer="char_wb"`, `ngram_range=(3, 5)`.
- Giới hạn số đặc trưng để phù hợp RAM; nếu chọn giới hạn khác nhau, ghi vào bảng cấu hình.
- Chạy B0, B1, M1, M2 trước. Chỉ làm ablation word/char/union khi đủ dữ liệu và thời gian; không cần quét hàng trăm cấu hình.
- Nếu dữ liệu train lệch lớp rõ, có thể thêm thí nghiệm `class_weight` của LR; giữ một trục thay đổi để hiểu nguyên nhân.

Huấn luyện LLM hoặc mạng sâu từ đầu chưa cần thiết cho mục tiêu này. Một nghiên cứu tốt nằm ở dữ liệu, thiết kế đánh giá và hiểu giới hạn. Nếu sau này thêm embedding/fine-tuning tiếng Việt, phải xác nhận tài nguyên, giấy phép và cùng protocol đánh giá; không coi mô hình lớn đương nhiên tốt hơn.

## 7. Protocol huấn luyện và chọn mô hình

1. Kiểm tra schema, nhãn, nguồn, trùng và quyền sử dụng. Lưu báo cáo audit.
2. Tạo và khóa split manifest. Giữ nguyên test trong các thí nghiệm.
3. Fit B0 và các pipeline ML trên train; cấu hình B1 từ nguồn được phép.
4. Đánh giá validation: macro-F1, các lớp yếu, thời gian train/infer. Chọn model bằng quy tắc định trước: ưu tiên macro-F1; nếu chênh lệch rất nhỏ, ưu tiên model nhẹ/dễ giải thích và ghi lý do.
5. Chốt đặc trưng, hyperparameter và threshold chỉ bằng train/validation.
6. Khóa model artifact và cấu hình, chạy các báo cáo test đã lên kế hoạch. Tất cả baseline dùng đúng cùng tập test.
7. Phân tích lỗi, báo cáo đạt/chưa đạt mục tiêu. Muốn phát triển tiếp sau khi xem test thì tạo vòng nghiên cứu mới và test độc lập mới; không gọi điểm được tối ưu qua nhiều vòng là kiểm tra cuối cùng độc lập.

Trong v1, giữ model fit trên train khi chốt đánh giá và tích hợp. Không tự refit trên train+validation rồi dùng nguyên threshold được chọn từ phiên bản cũ: model mới có thể có phân bố score khác. Bước refit/deploy khác cần một protocol hiệu chỉnh và đánh giá riêng.

Ví dụ kiến trúc code **minh họa**, chưa phải một script đã chạy:

```python
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
    ("classifier", LogisticRegression(C=1.0, max_iter=1000)),
])
pipeline.fit(train_descriptions, train_labels)
validation_predictions = pipeline.predict(validation_descriptions)
# Chọn cấu hình trên validation. Test vẫn chưa được dùng ở đây.
```

Bạn cần hiểu: hai biến train chỉ chứa các `record_id` đã nằm trong tập train; Pipeline tự fit TF-IDF ở bước đầu. Sau này lưu **cả pipeline**, không chỉ classifier. Luôn lấy thứ tự nhãn xác suất từ `pipeline.classes_` hoặc lớp classifier tương ứng, không giả định trùng thứ tự slug viết trong tài liệu.

## 8. Score, threshold và quyền xác nhận

Đặt `s(x) = max(predict_proba(x))`. Giá trị này là **điểm mô hình**, chưa được hiệu chuẩn để diễn giải thành xác suất dự đoán đúng. Ví dụ 0,82 không cho phép nói “82% chắc chắn đúng”. Hiệu chuẩn xác suất là một bước riêng cần dữ liệu và đánh giá phù hợp. [Tài liệu hiệu chuẩn của scikit-learn](https://scikit-learn.org/stable/modules/calibration.html).

Chính sách đề xuất:

- Threshold `τ=0.60` là điểm khởi đầu, chưa có chứng cứ đây là ngưỡng tốt.
- Nếu `s≥τ`, hiện nhãn đề xuất để người dùng xem và xác nhận.
- Nếu `s<τ`, hiện trạng thái cần chọn danh mục; có thể cho xem các gợi ý nhưng không lưu một nhãn đã xác nhận thay người dùng.
- **Cả hai trường hợp đều cần người dùng xác nhận trước khi lưu nhãn cuối.** Batch CSV phải có bước review trước commit.
- Đầu vào rỗng/không hợp lệ được xử lý ở validation ứng dụng. Score cao không miễn trừ bước kiểm tra này.

Trên validation, thử một dãy ngưỡng định sẵn như `0.40, 0.50, 0.60, 0.70, 0.80`. Quy tắc chọn: trong các ngưỡng đạt accuracy của phần được gợi ý ≥0,85 và coverage ≥0,60, chọn ngưỡng có coverage lớn nhất; tie theo quy tắc đã ghi. Nếu không có ngưỡng đạt cả hai, ghi **chưa đạt**, không giảm tiêu chí âm thầm hoặc chọn bằng test. Dãy và quy tắc này là đề xuất của dự án, có thể chốt lại trước chạy.

Không bảo đảm threshold từ chối mọi mô tả ngoài miền. Làm một bộ kiểm tra lỗi ngoài miền riêng, gồm mô tả khoản thu, chuyển tiền, câu công việc và câu vô nghĩa; báo cáo tỷ lệ còn được gợi ý với score cao. Không trộn chúng vào test tám lớp rồi tính một ground truth tùy ý.

## 9. Đo gì và đọc kết quả thế nào?

### Chỉ số chính trên toàn bộ test khoản chi hợp lệ

Với một lớp `c`: `precision = TP/(TP+FP)`, `recall = TP/(TP+FN)`, `F1 = 2PR/(P+R)`. Macro-F1 là trung bình F1 của tám lớp, không cân theo số mẫu; support là số mẫu thật của lớp. [Định nghĩa các chỉ số trong scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html).

Ví dụ do dự án đặt ra để học: test gồm 90 mẫu ăn uống và 10 mẫu sức khỏe. Model luôn trả ăn uống có accuracy 90%, nhưng recall sức khỏe 0. F1 ăn uống khoảng 0,947; macro-F1 cho **ví dụ hai lớp** khoảng 0,474. Đây là lý do không chỉ nhìn accuracy. Ví dụ này không phải điểm của SpendWise AI.

Với tám lớp, tính macro-F1 theo danh sách tám nhãn cố định; ghi cách xử lý chia 0. Nếu một lớp không có support trong test, đánh dấu protocol tám lớp chưa đủ điều kiện, không dùng một điểm trung bình để che việc thiếu lớp.

Xuất confusion matrix cả số đếm và tỷ lệ chuẩn hóa theo hàng. Hàng là nhãn thật, cột là nhãn dự đoán; ô ngoài đường chéo giúp tìm cặp lớp thường nhầm. [Tài liệu confusion matrix](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html).

### Chỉ số cho chính sách gợi ý có threshold

Gọi `A` là tập mẫu có `s≥τ`:

- `coverage = |A| / N`: phần mô tả mô hình đủ điểm để đưa gợi ý theo chính sách.
- `accepted_accuracy = số dự đoán đúng trong A / |A|`: độ đúng của chính dự đoán mô hình trong phần này.
- Nếu `|A|=0`, accepted accuracy là **N/A**, không phải 100%.
- Luôn báo cáo tử số, mẫu số, threshold và coverage từng lớp; một điểm tổng cao có thể che việc lớp khó gần như luôn cần chọn tay.

“Accepted” ở đây là đủ threshold, không có nghĩa người dùng đã xác nhận. Không lấy nhãn đã sửa bởi người dùng để tính lại độ chính xác mô hình: cách đó đo công sức con người thay vì classifier.

Ví dụ minh họa: 200 mô tả, 130 mô tả đủ threshold, 117 dự đoán trong đó đúng → coverage 65%, accepted accuracy 90%. Nếu 40 mẫu sai nằm trong phần không đủ threshold, vẫn phải tính chúng trong macro-F1 dự đoán đầy đủ.

### Mục tiêu cần đo

| Điều kiện/chỉ số | Mục tiêu đề xuất | Phạm vi |
|---|---|---|
| Test đủ dữ liệu thật | ≥20 mô tả khác nhau/lớp và giữ riêng người dùng | Điều kiện trước đánh giá chính thức |
| Macro-F1 | ≥0,80 | Toàn bộ test hợp lệ trong miền, gồm 8 lớp |
| Coverage | ≥0,60 | Cùng test, threshold chốt từ validation |
| Accepted accuracy | ≥0,85 | Phần đủ threshold trên cùng test |
| So với baseline | Báo cáo chênh lệch macro-F1 đo được | Không hứa ML luôn vượt rule |
| Latency | Đo p50/p95 và đối chiếu NFR đặc tả | CPU/máy thực tế, có protocol |

Các mục tiêu đầu tiên phải đọc cùng nhau. Coverage 0,10 và accepted accuracy 0,99 chưa đạt mục tiêu coverage. Đạt điểm trên câu tự tạo không chứng minh đạt điểm trên mô tả thật. Không đạt ngưỡng vẫn có thể là một nghiên cứu trung thực; trạng thái tính năng gợi ý đủ chất lượng cho MVP phải ghi “chưa đạt” nếu điều kiện chưa thỏa.

### Protocol tốc độ và độ tin cậy của báo cáo

Ghi CPU, RAM, hệ điều hành, Python, scikit-learn, số mẫu và số đặc trưng. Đo riêng thời gian tải model, train, suy luận một mô tả khi model đã tải và batch CSV. Warm-up trước, dùng đồng hồ đơn điệu, lặp đủ lần, báo p50/p95 cùng số lần lặp và batch size. Không lấy một lần chạy trên máy khác để tuyên bố đạt trên máy người dùng.

Với test ít người, báo số người và giới hạn mẫu. Nếu bổ sung khoảng tin cậy bootstrap, ưu tiên lấy mẫu lại theo **nhóm người** vì nhiều mô tả từ một người có tương quan; chốt seed và số lần lặp, không dùng khoảng tin cậy để chọn lại model trên test.

## 10. Bảng thí nghiệm và phân tích lỗi

Đây là mẫu trống, sẽ điền sau khi chạy thật:

| Run | Model/đặc trưng | Seed/split | Val macro-F1 | Test macro-F1 | Test coverage/accuracy đủ ngưỡng | Ghi chú |
|---|---|---|---|---|---|---|
| B0 | Dummy | Chưa chạy | Chưa đo | Chưa đo | Theo chính sách riêng | Mốc đơn giản |
| B1 | Từ khóa | Chưa chạy | Chưa đo | Chưa đo | Không tạo score giả | Có phiên bản rule |
| M1 | TF-IDF + NB | Chưa chạy | Chưa đo | Chưa đo | Chưa đo | `alpha` chốt từ val |
| M2 | TF-IDF + LR | Chưa chạy | Chưa đo | Chưa đo | Chưa đo | `C` chốt từ val |

Mỗi lỗi được rà soát ghi: ID đã ẩn danh, nhãn thật, nhãn đoán, score, loại lỗi, cách khắc phục dự kiến. Nhóm lỗi nên gồm viết tắt/không dấu, chưa gặp từ vựng, thiếu ngữ cảnh, lỗi nhãn, câu ghép, nhầm tên cửa hàng với mục đích. Báo tỷ lệ của các nhóm sau khi rà thực tế; không chỉ chọn vài ví dụ đẹp.

Ablation là thí nghiệm thay một thành phần có chủ đích. Giữ cùng dataset, split, protocol chọn tham số và metric; thay word → char → union để khảo sát biểu diễn. Nếu union tốt hơn nhưng lớn/chậm hơn, ghi cả lợi ích lẫn chi phí. Nếu char không tốt hơn, giữ kết quả đó; giả thuyết thất bại vẫn là kết quả.

## 11. Artifacts cần sinh khi viết code

Cấu trúc **đề xuất cho code tương lai**, chưa có các kết quả này trong bộ đặc tả:

```text
artifacts/runs/<run_id>/
  config.json
  environment.txt
  dataset_manifest.json
  split_manifest.csv
  model.joblib
  metrics_validation.json
  metrics_test.json
  predictions_test.csv
  confusion_matrix.csv
  error_analysis.md
  model_card.md
```

`config.json` lưu seed, cấu hình chuẩn hóa/vectorizer/classifier, threshold và class order. Manifest lưu hash dataset, phiên bản hướng dẫn gán nhãn, phân bố nguồn/lớp và phương pháp chia tập. `metrics_test.json` chỉ được sinh ở giai đoạn test đã được phép trong protocol. Lưu commit code và lockfile để chạy lại cùng môi trường.

`model_card.md` nêu mục đích, người dùng, nhãn, nguồn dữ liệu, số mẫu thật/tự tạo, split, chỉ số theo lớp, score chưa hiệu chuẩn, hạn chế và các trường hợp không nên dùng. Không đính kèm dataset cá nhân vào artifact công khai. Với joblib/pickle, chỉ tải model do nhóm tự tạo hoặc nguồn tin cậy vì việc tải có thể thực thi mã. [Hướng dẫn lưu mô hình của scikit-learn](https://scikit-learn.org/stable/model_persistence.html).

## 12. Lộ trình học kèm thực hành

| Bước | Bạn cần hiểu | Bài tập nhỏ | Bằng chứng đã hiểu |
|---|---|---|---|
| 1 | Python hàm/list/dict, CSV và lỗi đầu vào | Đọc 8 dòng CSV, phát hiện nhãn sai/rỗng | Giải thích được vì sao một dòng bị từ chối |
| 2 | Nhãn và ground truth | Tự gán 20 câu, rà các câu mơ hồ | Viết được quy tắc xử lý `Grab` và `Shopee` |
| 3 | Train/val/test, group và leakage | Vẽ 3 tập có người giữ riêng | Chỉ ra lỗi nếu cùng người ở cả train/test |
| 4 | Vocabulary, sparse vector, TF-IDF | Tính IDF cho 3 câu minh họa | Phân biệt `fit` với `transform` |
| 5 | Baseline và classifier | So B0/B1/NB/LR trên tập thử | Nói được phần nào học từ nhãn |
| 6 | Macro-F1/confusion/coverage | Tính ví dụ hai lớp và threshold | Giải thích accuracy cao nhưng lớp yếu |
| 7 | Lưu model và tích hợp | Tải pipeline, gợi ý rồi xác nhận | Mô tả được đường đi dữ liệu tới SQLite |
| 8 | Tái lập và bảo vệ | Chạy lại một run, trình bày 3 lỗi | Dẫn được config, manifest và kết quả thật |

Sau mỗi bước, viết một đoạn bằng lời của mình vào nhật ký học. Khi dùng trợ lý AI để viết code, yêu cầu giải thích biến, đường đi dữ liệu, quyết định và một trường hợp lỗi; tự chạy và sửa một ví dụ trước khi chuyển bước.

## 13. Checklist trước khi tuyên bố kết quả

- [ ] Có đồng ý sử dụng nguồn thật và đã bỏ thông tin nhận dạng.
- [ ] Nhãn có hướng dẫn phiên bản, bất đồng đã được xử lý.
- [ ] Test thật đủ lớp; số người và mô tả khác nhau được báo cáo.
- [ ] Người, văn bản trùng và họ khuôn không giao giữa các tập.
- [ ] TF-IDF chỉ fit train; chọn model/threshold không xem test.
- [ ] Baseline dùng cùng test; score giả không được đưa vào bảng xác suất.
- [ ] Báo macro-F1 từng lớp, confusion matrix và support.
- [ ] Báo coverage và accuracy phần đủ ngưỡng cùng mẫu số.
- [ ] Báo phần chưa đạt, mô tả mơ hồ và ngoài miền.
- [ ] Có config, hash, seed, môi trường và model card để tái lập.
- [ ] Nhãn cuối chỉ lưu sau xác nhận; dữ liệu sửa không tự vào train.

## 14. Tài liệu đọc theo thứ tự

1. [Tránh rò rỉ dữ liệu](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage): đọc trước khi viết lệnh train.
2. [Trích đặc trưng văn bản](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction): đối chiếu vocabulary và cấu hình TF-IDF.
3. [MultinomialNB](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html) và [LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html): đọc API đúng phiên bản môi trường đã khóa.
4. [Chia tập theo nhóm](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data): kiểm tra đơn vị độc lập.
5. [Chỉ số phân loại](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html) và [hiệu chuẩn score](https://scikit-learn.org/stable/modules/calibration.html): tránh diễn giải quá mức.

Các liên kết chính thức được kiểm tra ngày 05/10/2026. Khi triển khai, ghi phiên bản thực tế cài đặt; đường dẫn `stable` có thể cập nhật sau này.


## 15. Dataset v0.1 — hợp đồng đã triển khai

Đọc [dataset card](../data/seed/v0.1/DATASET_CARD.md), [task card](tasks/TASK-05-06.md) và [hướng dẫn học](https://github.com/Krev1/Learn/blob/main/spendwise-ai/guides/01_dataset_collection.md). Dữ liệu công khai phiên bản này hoàn toàn hư cấu; nhãn trong `provenance.csv` ghi `ai_draft`. Chưa có người gán nhãn độc lập hoặc test thật.

`public_synthetic` chỉ dùng cho nguồn đã xác minh là hư cấu, chuyển ngữ/biên tập có lưu gốc. `author_synthetic` và `public_synthetic` bắt buộc `true`; `volunteer` bắt buộc `false`. Nhóm nguồn công khai được giữ chung một `group_id`; các mẫu tự tạo giữ cùng họ kịch bản và biến thể trong một nhóm. Đây là nhóm phụ thuộc để chia tập, không phải số người thật.

Validator kiểm tra schema sáu cột, ID/nhóm ASCII 1–64, mô tả có chữ 1–300 ký tự, tám nhãn, cờ canonical, nhất quán nhóm/nguồn, trùng chuẩn hóa và biến thể chỉ khác dấu ở khác nhóm. NFC/lowercase/gộp khoảng trắng dùng cho khóa audit; CSV giữ câu gốc. Bỏ dấu chỉ dùng để tìm biến thể và tạo demo, không thay cấu hình chuẩn hóa chính của mô hình.

Provenance bên cạnh giữ hash chuẩn hóa, họ câu, cách biến đổi, dòng nguồn, lý do nhãn và trạng thái duyệt. Rà PII bằng người vẫn bắt buộc; cảnh báo email/URL/chuỗi số dài chỉ hỗ trợ. Dữ liệu thật và ledger đồng ý ở `data/private/`, không đưa vào Git.

Builder không tải mạng và chỉ nhận recipes hư cấu đã version. Collector chỉ kiểm tra snapshot từ commit nguồn cố định; không tự thu dữ liệu tài chính người dùng. Builder/validator không huấn luyện, không chia train/test và không đánh giá khả năng tổng quát hóa.
