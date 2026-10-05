# TASK-07 — Prototype baseline

Ngày: 05/10/2026. Trạng thái: DONE — phần kỹ thuật prototype. Vai trò chính: ML Researcher/Developer; QA subagent review chỉ đọc. REQ-09,13; phụ thuộc kỹ thuật TASK-05–06, A12 và D13.

## Phạm vi và đầu vào

Root sở hữu `src/spendwise/ml/`, `scripts/demo_baselines.py`, `examples/baseline_demo.json`, tests và tài liệu/bằng chứng. QA chỉ đọc, không sửa file. Chỉ sửa repo dự án, không viết Learn.

Bảng rule từ guideline miền; không đọc test nghiên cứu. Fixture tự tạo có descriptions/labels cho fit B0, probes không nhãn để quan sát B0/B1. Seed 356 câu chưa human-reviewed, đã được validator kiểm tra cấu trúc, chưa dùng fit ở task này. Không thêm dependency, split, model binary, metric, SQLite hoặc UI.

## Hợp đồng

`KeywordBaseline.explain(description)` nhận chuỗi có chữ, NFC 1–300 ký tự sau trim. NFC/lowercase/gộp khoảng trắng giữ dấu. Khớp keyword theo ranh giới Unicode. Xét hit dài trước (số token, số ký tự, thứ tự rule); loại hit ngắn nằm hoàn toàn trong hit đã giữ. Còn một lớp trả `matched`, nhiều lớp trả `khac/conflict`, không hit trả `khac/no_match`. Kết quả có hit/vị trí trong văn bản chuẩn hóa, version/hash rule, `score=null`, `requires_confirmation=true`, `needs_review` cho conflict/no_match. `predict(descriptions)` trả nhãn để dùng so sánh sau này.

`MostFrequentBaseline.fit(train_descriptions, train_labels)` kiểm tra toàn bộ mô tả, nhãn và độ dài batch trước fit. B0 chỉ truyền descriptions/labels cho `DummyClassifier(most_frequent, seed=42)`. `predict` không fit lại; chưa fit báo lỗi. Tie theo thứ tự lớp sklearn được kiểm tra với lock. Không diễn giải phân bố B0 thành độ tin cậy mô tả. Caller TASK-10 chịu trách nhiệm chọn train đúng manifest.

CLI chỉ đọc fixture có `is_synthetic=true` và nguồn `author_synthetic`, chạy được từ cwd khác; in JSON có fixture/rule hash, Python/sklearn version và trạng thái chưa đánh giá. Lỗi file/schema/mô tả/nhãn trả exit 1/stderr, không in thành công một phần hoặc echo mô tả lỗi. CLI không nhận dataset nghiên cứu thật hoặc artifact.

## Tiêu chí chấp nhận và lệnh

1. NFC/NFD, hoa/thường, khoảng trắng cho cùng kết quả; không bỏ dấu ngầm; alias khai báo mới khớp không dấu.
2. Không khớp chuỗi con (`game` trong `endgame`); cụm dài chứa keyword chung ưu tiên đúng. Hai khoản chi độc lập trả conflict; không keyword trả no_match; score null và cần xác nhận.
   Ranh giới token gồm chữ, số, `_` và combining mark Unicode còn lại sau NFC; dấu câu không nối thành cụm từ.
3. B0 chỉ phụ thuộc lớp phổ biến trong dữ liệu fit. Input sai/nhãn lạ/batch lệch bị từ chối trước fit; tie và predict trước fit kiểm tra rõ.
4. CLI fixture hư cấu tái lập, read-only, cwd khác; lỗi không lộ mô tả/JSON thành công; không báo accuracy/F1/coverage.
5. Kiểm tra phù hợp, QA review, cập nhật VERIFICATION/progress/bảng task/PROJECT_HANDOFF, commit/publish theo quyền đã giao.

```powershell
.\.venv\Scripts\python.exe -B scripts/demo_baselines.py
.\.venv\Scripts\python.exe -B -m pytest -q
```

## Bằng chứng và giới hạn

Code ở [commit b331e5f](https://github.com/Krev1/spendwise-ai/commit/b331e5f078a07a73e34d44f22da69d89774eae96). Kiểm tra toàn bộ: **139 passed, 11 subtests passed**; [log](../evidence/TASK-07-2026-10-05/pytest.txt). [Demo JSON](../evidence/TASK-07-2026-10-05/demo_baselines.json) ghi 10 ví dụ fit hư cấu/13 probes, score null, chưa split/chưa đánh giá. [QA review](../evidence/TASK-07-2026-10-05/qa_review.md) xác minh lỗi combining mark/surrogate đã sửa; lỗi tên param quá dài trên Windows sửa bằng test ID ngắn. [Bàn giao](../PROJECT_HANDOFF.md) ghi hàm/lý do/lệnh/giới hạn.

Tiếp theo TASK-08 grouped split prototype. Consent, nhãn người duyệt và test thật còn thiếu cho đánh giá chính thức; không chứng nhận chất lượng ML, mức hiểu hoặc phê duyệt trường. Rule cần ngữ cảnh đủ cụ thể; alias không dấu không bao phủ mọi cách viết. B0 chỉ fit demo, chưa phải baseline đã đánh giá trên train/validation nghiên cứu.
