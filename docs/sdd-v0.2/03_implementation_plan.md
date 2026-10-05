# 03 — Kế hoạch triển khai v0.2

Ngày: 06/10/2026. Các SW-TASK mới đều **Planned**. Tiến độ theo mốc, chưa có deadline/giờ tuần cố định.

## 1. Workflow và vai trò

Mỗi task: REQ/thiết kế → card có file/phụ thuộc/kiểm tra → code nhỏ → evidence → tiến độ/handoff. Thay hành vi cập nhật tài liệu trước hoặc cùng code. Quyền dữ liệu/nhãn con người cần bằng chứng, không thay bằng AI; thiếu đầu vào này vẫn làm task độc lập.

Bạn là chủ đồ án và làm một mình. AI lần lượt đóng vai Product Analyst, Architect, Data Engineer, ML Engineer, Developer và QA Reviewer. Mentor là luồng Learn riêng. Phân vai không có nghĩa đã tuyển người hoặc chạy agent; không cần nhiều agent/API trả phí. Người học quyết định phạm vi, quyền dữ liệu và tự bảo vệ.

## 2. Task, phụ thuộc và tiêu chí hoàn tất

| Task | Phụ thuộc | SW-REQ | Đầu ra / bằng chứng |
|---|---|---|---|
| SW-TASK-01 — Kiểm kê/chuyển SDD | HEAD/status/code/handoff thật | 14 | Card riêng; ma trận keep/adapt/retire; trạng thái cả work chưa commit; cập nhật tiến độ/handoff không mất work. Lượt đầu chưa cài/train. |
| SW-TASK-02 — Môi trường web/train/GPU | 01 | 08,10,14 | Ignore môi trường mới, kiểm tra compatibility/driver, lock sau smoke CPU/CUDA forward/backward; ghi VRAM/package thật, giữ .venv cũ. |
| SW-TASK-03 — Budget/alert/forecast core | 01 | 04,05,06,07 | Pure services int/month/timezone; test biên 80% / 100%, tháng 28/29/30/31 ngày, missing coverage/income/invalid sum/reconfirm. Chưa cần real data/web. |
| SW-TASK-04 — Django/auth/schema | 02 | 01,09,13 | Custom user ngay migration đầu, allauth/session, owner-FK/constraints, dev/prod settings; auth/CSRF/owner tests, email backend thử. |
| SW-TASK-05 — Persisted transactions | 04 | 01,02,04 | CRUD/idempotency/revision/audit/aggregate theo owner; PostgreSQL integration và hai account cách ly. |
| SW-TASK-06 — CSV atomic import | 05 | 01,03 | Adapter parser cũ, owner/expiry/revision preview; rollback/reimport/source conflict/concurrent imports trên PostgreSQL. |
| SW-TASK-07 — Web ngân sách/cảnh báo | 03,05 | 05,06,07,11 | Form tổng/nhóm, dashboard, coverage/forecast riêng; E2E sửa giao dịch/ngân sách, responsive 360/1280 px px. |
| SW-TASK-08 — Thu/annotation pilot | 01 + người tham gia/consent | 09,10 | Guideline/sidecar private, pilot 50–100 là mục tiêu; agreement thật/near-dup review; dataset card với số thực. Tiến hành khi làm web. |
| SW-TASK-09 — Dataset nghiên cứu/split | 08 + dữ liệu đủ | 09,10 | Snapshot/hash/participant+lineage groups, human audit, train/val/test đủ lớp; test khóa. Seed split không thành official split. |
| SW-TASK-10 — Baselines | 02,09 cho real; seed cho smoke | 10 | B0/B1/B2 cùng cohort, train-only vectorizer, validation thật/config fixed; smoke và real report tách rõ. |
| SW-TASK-11 — Char-CNN tự train | 02; 09 cho real | 08,10 | Model/vocab/train/eval/checkpoint CLI, seed/loss/early-stop; synthetic smoke trước real; PAD/UNK/leakage/save-load checks. |
| SW-TASK-12 — Chọn/integrate model | 10,11,05,06 | 02,03,08,10 | Chọn bằng validation, threshold/model card; UI confirm/input invalidate/fallback; test cuối sau khóa quyết định. |
| SW-TASK-13 — Backtest/pilot thực | 07 + lịch sử đủ/consent | 07,09,11 | Chronological backtest/baseline/error/missingness; pilot usability/bugs. Thiếu lịch sử chỉ Verified công thức, nghiên cứu pending. |
| SW-TASK-14 — Data rights/release tests | 04–07,12 | 01,03,09,11,12,13 | Opt-in/export safe/delete/revocation/backup policy, isolation/concurrency, PostgreSQL/browser tests; không public raw/logs. |
| SW-TASK-15 — Hạ tầng/public beta | 14 + provider/quota/email/backup đạt | 01,11,13 | Official free terms tại thời điểm chọn; staging→HTTPS public, durable DB/SMTP, restart/restore/rate-limit/load thật; URL/capacity report. Không tự mua dịch vụ. |
| SW-TASK-16 — Đồ án/bàn giao cuối | 09–15 theo evidence + rubric | 10,14 | Traceability/report/model card/setup/demo an toàn theo SHA; Mentor bảo vệ riêng, không tự ghi học viên hiểu. |

Mỗi task tạo card `docs/tasks/SW-TASK-*.md`: owner, trạng thái Planned/In progress/Verified/Review, file scope, lệnh/kết quả, limits và commit. Verified chỉ cho đầu ra đã kiểm chứng; không chuyển phần real/public pending thành Done để đủ bảng.

## 3. Mốc theo kết quả

- M0 (01): chuyển phạm vi khớp hiện trạng, giữ work cũ.
- M1 (02–05): môi trường mới/core ngân sách/tài khoản/persistence có kiểm tra.
- M2 (06–07): website thủ công local dùng được, có CSV/ngân sách/hai cảnh báo.
- M3 (08–12): dữ liệu và neural thật, baseline/evaluation hoặc giới hạn thiếu được ghi rõ.
- M4 (13–15): dự báo đo bằng lịch sử thật, public release có evidence.
- M5 (16): đồ án/code/report nhất quán; mức hiểu theo Learn riêng.

Thu dữ liệu M3 diễn ra khi làm M1/M2; không đợi hết code mới ghi chi. Không hứa số tuần; thiếu provider không thay mục tiêu public bằng demo local mà giữ mốc chưa đạt.

## 4. Kế thừa code v0.1

| Phần cũ | Cách chuyển |
|---|---|
| REQ-01/02/04/05/06/07; TASK-04 domain/CSV/reports | Giữ core/contract; thêm owner/DB/idempotency/revision/preview expiry |
| REQ-03/09/10; TASK-07 baseline và TF-IDF nếu đã có | Giữ làm đối chứng, thêm neural bắt buộc; không gọi TF-IDF là Deep Learning |
| TASK-05/06 seed 356; TASK-08 split prototype | Giữ version/hash/smoke, không dùng holdout thiếu lớp kết luận real |
| Streamlit DEMO-01 nếu hiện có | Kiểm tra code thật, dùng tham khảo luồng; không coi session-memory là public persistence |
| SQLite/Streamlit task chưa Verified | Rà trạng thái mới; chuyển kế hoạch sang Django/PostgreSQL, không đánh dấu task cũ DONE thay |
| REQ-11 local/CPU | Web nhiều account là đích mới; GPU local train/CPU serving; local là bước thử |
| REQ-12/13 và D13 | Giữ privacy/học riêng, thêm consent/export/delete/handoff |

## 5. Bắt đầu

Chat dự án dùng [START_HERE](../../prompts/START_HERE.md), làm **SW-TASK-01** trước. Không khởi tạo lại repo/cài cả stack/train seed rồi báo real performance. Chủ đồ án bắt đầu nhật ký private và hỏi giảng viên rubric; hướng dẫn người học ở [Learn guide05](https://github.com/Krev1/Learn/blob/main/spendwise-ai/guides/05_public_web_and_deep_learning.md).
