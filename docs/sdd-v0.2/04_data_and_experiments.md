# 04 — Dữ liệu và thí nghiệm v0.2

Ngày: 06/10/2026. Chưa có mẫu Việt thực mới, nhãn người duyệt mới, train neural hoặc điểm thực nghiệm trong lần lập đặc tả này.

## 1. Tách hai nhu cầu dữ liệu

| Mục đích | Dữ liệu cần | Không thay thế được bằng |
|---|---|---|
| Phân loại khoản chi | Mô tả Việt + nhãn đã rà + nhóm/phả hệ/nguồn/quyền dùng | Một lịch sử toàn khoản giống nhau hoặc 356 câu hư cấu gán nhãn AI |
| Kiểm tra dự báo ngân sách | Lịch sử ngày/số tiền/nhãn của cùng người, các ngày ghi đầy đủ, nhiều tháng đã kết thúc | Danh sách mô tả rời rạc, sao kê một người bằng ngoại tệ chưa ánh xạ |

User chưa có lịch sử riêng. Repo có seed 356 câu/8 nhãn, toàn hư cấu, nhãn ai_draft; dùng smoke pipeline. Nguồn MoneyVis có thể đã được luồng khác thu thập nhưng cần đọc manifest/quyền dùng thật trước; dữ liệu Anh/GBP không tự thành dữ liệu VND/Việt đủ điều kiện. Không dịch rồi gọi bản dịch là lời mô tả tự nhiên từ người Việt, không đổi GBP thành VND chỉ bằng đổi tên cột.

## 2. Thu thập không mất phí

1. Bắt đầu nhật ký chi tiêu **private** của bản thân ngay, gồm ngày, loại, int VND, mô tả ngắn và nhãn; cuối ngày xác nhận đã ghi đủ hoặc ghi chưa đủ. Ngày chi 0 vẫn được đánh dấu rõ. Chưa cần đợi website.
2. Hoàn thiện guideline tám nhãn và biểu mẫu đồng ý tách việc thử app / sử dụng mô tả nghiên cứu / sử dụng lịch sử dự báo. Người tham gia tự nguyện, biết mục đích và cách rút. Người triển khai không tự gửi lời mời hoặc lấy sao kê của ai.
3. Pilot mục tiêu 50–100 mô tả thật từ vài người, ưu tiên hai nhóm người dùng. Mời người thứ hai gán nhãn độc lập cho pilot/holdout; AI là trợ lý, không là người gán nhãn thứ hai. Nếu chỉ một người rà được, ghi giới hạn và chưa khẳng định độ tin cậy liên người.
4. Ghi bất đồng, điều chỉnh guideline trước khóa dataset. Câu mơ hồ hỏi chủ giao dịch; khoản chuyển giữa ví của chính mình, thu/refund và mô tả vô nghĩa không đưa vào tám lớp chi một cách máy móc. Khoản nhiều mục đích tách có căn cứ hoặc loại; không nhân bản thành nhiều nhãn để tăng số mẫu.
5. Mở rộng theo phân bố thật; khoảng 1.200 mô tả/150 mỗi lớp chỉ là mục tiêu thu ban đầu từ v0.1, không ép nhân bản cho đủ. Ghi số người, mô tả khác nhau, lớp hiếm, tỉ lệ synthetic, trạng thái người duyệt và missingness.
6. Có thể phát triển web/ngân sách/AI smoke trong lúc thu, nhưng không đánh dấu thí nghiệm thật hoặc pilot xong chỉ vì có code. Thử app và quyền train luôn là hai lựa chọn riêng.

Hướng dẫn/biểu mẫu chi tiết cho người học nằm trong [Learn](https://github.com/Krev1/Learn/tree/main/spendwise-ai); tài liệu này là hợp đồng kỹ thuật, không đặt bài tập học trong repo sản phẩm.

## 3. Schema nghiên cứu và provenance

Giữ dataset sáu cột `record_id,description,label,group_id,source,is_synthetic`. Train chỉ đọc description/label và ID để nối manifest. Có sidecar private theo record_id: participant pseudonym, consent/version, annotator IDs, independent labels, adjudication, guideline version, original/family IDs, source/time và human_review_status. Không publish pseudonym/participant/time thật vì vẫn có thể liên kết người.

Lịch sử dự báo ở file private khác có date/type/amount/category/coverage/account pseudonym. Không gộp tiền thành feature classifier. Dataset được đăng công khai chỉ là ví dụ hư cấu hoặc nguồn có quyền tái phân phối đã rà privacy; “đã ẩn danh” không là giấy phép tự đăng giao dịch cá nhân.

Giữ consent ledger riêng; rút đồng ý loại mẫu khỏi snapshot tương lai. Nếu mẫu đã ở artifact đang phục vụ, cách an toàn là ngừng artifact đó và retrain từ snapshot đã loại mẫu trước thay lại; không hứa xóa ảnh hưởng khỏi weights chỉ bằng xóa CSV. Backups private đề xuất hết hạn tối đa 30 ngày, có tombstone để restore không tái đưa dữ liệu đã xóa vào hoạt động. Phải công bố chính sách/được rà trước public, không coi con số này là kết luận pháp lý.

## 4. Nhóm, split và chống leakage

Xác minh near-duplicate/family/biến thể không dấu/bản dịch và lineage bằng người rà. Union dependency graph gồm participant + lineage/duplicate để cùng người hoặc cùng mẫu phụ thuộc không qua các tập khi đánh giá người mới. Không group đơn giản chỉ bởi cùng nhãn hoặc từ “cơm”. Nếu toàn dataset chỉ có một người, không thể tuyên bố đánh giá người dùng mới.

Chọn train/validation/test xấp xỉ 70/15/15 theo group, audit coverage trước train; không cố định kỹ thuật SGKF cũ nếu không đáp ứng real/group/8 lớp. Chỉ finalize test khi có đủ người độc lập và đủ lớp theo mục tiêu đã ghi trước; 20 mô tả khác nhau mỗi lớp test là mức khởi đầu, không bảo đảm đại diện. Thiếu lớp ghi rõ và tiếp tục thu, không sao chép để đủ.

Vocab/TF-IDF/scaler/class weights fit train-only; synthetic/AI variants nếu dùng chỉ ở train và nối group gốc. Test thật được phép độc lập; chọn hyperparameter và threshold bằng validation. Lưu private manifest/hash, public chỉ schema/config và thống kê đã rà. Split 256/50/50 seed cũ có validation/test thiếu lớp: smoke kỹ thuật, không official score của v0.2.

## 5. Thí nghiệm Deep Learning có thể bảo vệ

| ID | Model | Mục đích |
|---|---|---|
| B0 | Dummy most_frequent | Mốc đo phân bố lớp |
| B1 | Rule từ khóa version cố định | Mốc không học |
| B2 | TF-IDF + Logistic Regression | Baseline học máy truyền thống |
| N1 | Char-CNN weights khởi tạo ngẫu nhiên | Deep Learning bắt buộc, tự train từ đầu |
| Optional | TF-IDF + NB hoặc pretrained fine-tuning | Chỉ thêm sau N1/dữ liệu/rubric, phân biệt fine-tuning với train từ đầu |

Cùng split/cohort/guideline và báo mọi thay đổi tiền xử lý. N1 có smoke vài batch hư cấu để chứng minh backward/loss/serialization; smoke không đo chất lượng thật. Chạy thí nghiệm real khi nhãn/split đủ điều kiện; báo loss curves, train–val gap, macro-F1/per-class metrics/confusion, lỗi đặc trưng, ba seeds 42/43/44 và thời gian/VRAM thật. Tolerance tái lập phải ghi vì seed không bảo đảm bit-identical giữa hệ điều hành/GPU/phien bản.

Không lấy macro-F1 0,80 từ v0.1 làm điểm đã có hoặc điều kiện bắt neural thắng. Trước test chốt kế hoạch đo và rubric thực; nếu neural kém B2, phân tích dữ liệu/overfit và vẫn báo kết quả. Phần serving có thể giữ nhập tay/baseline gắn nhãn rõ trong beta khi N1 chưa đủ bằng chứng, nhưng kết quả đồ án vẫn phải có nghiên cứu N1. Không tuyên bố app đang dùng Deep Learning khi chỉ bật rule.

## 6. Backtest dự báo xu hướng

Chưa train mạng dự báo ở MVP. Với người/tháng đã kết thúc và nhật ký xác nhận đủ, tạo các điểm chốt ngày 7,14,21 (nếu hợp lệ). Chỉ dùng dữ liệu tới điểm chốt để ước tính; tổng thực cuối tháng là outcome. Không nhìn khoản tương lai khi tính forecast. Chia cohort/time trước đánh giá; giữ tháng sau/người mới cho kiểm chứng tương lai, không random các ngày từ cùng tháng vào train/test.

Báo MAE VND và WAPE với denominator >0; nếu tổng thực 0 ghi WAPE undefined. Báo số người/tháng, độ lệch theo nhóm/thời điểm, lỗi cảnh báo nguy cơ (false positive/negative) và missingness/coverage. So sánh pace-v1 với “giữ số đã chi” và “tổng tháng trước” khi tháng trước đủ dữ liệu; các baseline cùng cohort. Nếu chưa đủ lịch sử, chỉ có test công thức hư cấu, chưa có bằng chứng dự báo hữu ích thực tế. Mục tiêu thu ít nhất vài tháng đầy đủ và nhiều người là kế hoạch, không số đã có hoặc bảo đảm thống kê.

## 7. Public artifacts và model card

Model card ghi intended use, taxonomy, provenance/consent/PII review, train/val/test support, real/synthetic, kiến trúc, preprocessing, môi trường/seeds, hashes, metrics thật, latency/VRAM, score threshold, lỗi, ai kiểm nhãn và giới hạn. Artifact binary private/ignored cho tới rà soát; không đóng gói raw text thật/participant IDs trong checkpoint/report/demo.

Report công khai dùng thống kê và ví dụ hư cấu/minh họa đã được phép; không đưa mẫu lỗi thật lên GitHub chỉ vì đã bỏ tên. Không commit dataset real, consent ledger, DB, backup, credentials hoặc log request. Trước khi xuất nghiên cứu từ app, có test consent/owner; trước share report có review thực và evidence.
