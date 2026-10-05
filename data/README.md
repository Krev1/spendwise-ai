# Dữ liệu SpendWise AI

TASK-05–06 / REQ-08,09,13. Snapshot công khai chỉ chứa dữ liệu hư cấu đã rà nội dung; **nhãn vẫn là dự thảo AI**. [Dataset card v0.1](seed/v0.1/DATASET_CARD.md) ghi số lượng, phạm vi dùng và giới hạn.

| Vị trí | Vai trò |
|---|---|
| `reference/` | Snapshot CSV hư cấu đã thu, MIT notice, URL/commit/hash |
| `recipes/` | 160 câu tiếng Việt tự tạo và 19 ánh xạ chuyển ngữ có version |
| `seed/v0.1/` | 356 mô tả, provenance, audit và quyết định từng dòng nguồn |
| `private/` | Dữ liệu thật/consent/annotation/split riêng; bị Git ignore, không công khai |

Code xây/kiểm tra dữ liệu nằm trong `scripts/` và `src/spendwise/data/`; tài liệu dạy học, template trống và phương pháp nằm ở [Learn](https://github.com/Krev1/Learn/blob/main/spendwise-ai/guides/01_dataset_collection.md). Dataset ML sáu cột khác CSV giao dịch sáu cột; không đưa file này vào transaction preview.

MIT của seed không cấp quyền công khai dữ liệu người tự nguyện về sau. Snapshot nguồn có notice riêng; không gọi tên repo nguồn là tác giả trong khi license ghi người khác. Không đưa dữ liệu nguồn chưa kiểm tra quyền, bí mật hay sao kê cá nhân vào cây này.
