"""Đọc toàn batch sau validation; không ghi hoặc sửa dữ liệu nguồn."""

import csv
import io
from pathlib import Path

from spendwise.domain.transactions import COLUMNS, Transaction, ValidationError, parse_row


MAX_ROWS = 5_000
MAX_BYTES = 2_000_000


def read_transactions_bytes(raw: bytes) -> list[Transaction]:
    """Kiểm tra bytes nhận từ file upload, không cần lưu file tạm."""
    if len(raw) > MAX_BYTES:
        raise ValidationError(f"CSV vượt giới hạn {MAX_BYTES} byte")
    try:
        decoded = raw.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise ValidationError("CSV cần mã hóa UTF-8, có thể có BOM") from error
    reader = csv.reader(io.StringIO(decoded, newline=""), strict=True)
    transactions = []
    seen_ids = set()
    try:
        if tuple(next(reader, ())) != COLUMNS:
            raise ValidationError("Header cần đúng thứ tự: " + ",".join(COLUMNS))
        while True:
            row_number = reader.line_num + 1
            fields = next(reader, None)
            if fields is None:
                break
            if len(transactions) >= MAX_ROWS:
                raise ValidationError(f"Dòng {row_number}: CSV vượt {MAX_ROWS} dòng dữ liệu")
            if len(fields) != len(COLUMNS):
                raise ValidationError(f"Dòng {row_number}: số cột không đúng header hoặc dòng trống")
            transaction = parse_row(dict(zip(COLUMNS, fields)), row_number)
            if transaction.transaction_id in seen_ids:
                raise ValidationError(f"Dòng {row_number}: transaction_id trùng trong batch")
            seen_ids.add(transaction.transaction_id)
            transactions.append(transaction)
    except csv.Error as error:
        raise ValidationError(f"Dòng {reader.line_num}: CSV sai cú pháp: {error}") from error
    if not transactions:
        raise ValidationError("CSV cần ít nhất một dòng dữ liệu")
    return transactions


def read_transactions(path: Path | str) -> list[Transaction]:
    """Giới hạn lượng byte đọc ngay tại file, rồi dùng chung parser bytes."""
    with Path(path).open("rb") as source:
        raw = source.read(MAX_BYTES + 1)
    return read_transactions_bytes(raw)
