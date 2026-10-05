"""Ví dụ học Python: validate CSV trước khi dùng dữ liệu để tính tổng.

Chỉ dùng thư viện chuẩn. Chưa ghi database hoặc dự đoán bằng mô hình.
"""

import argparse
import csv
import io
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import date
from pathlib import Path


COLUMNS = (
    "transaction_id", "date", "transaction_type", "amount_vnd",
    "description", "category",
)
CATEGORIES = frozenset({
    "an_uong", "di_chuyen", "nha_o_hoa_don", "hoc_tap",
    "mua_sam", "giai_tri", "suc_khoe", "khac",
})
MAX_ROWS = 5_000
MAX_BYTES = 2_000_000
MAX_AMOUNT = 1_000_000_000_000


class ValidationError(ValueError):
    """Input không đúng hợp đồng; gọi chương trình có thể hiển thị lỗi này."""


@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    occurred_on: date
    transaction_type: str
    amount_vnd: int
    description: str
    category: str


def parse_amount(value: str) -> int:
    """Chấp nhận số nguyên dương VND, không đoán dấu phân cách hay số lẻ."""
    if not re.fullmatch(r"[0-9]+", value):
        raise ValidationError("amount_vnd phải là số nguyên dương, không dấu phân cách")
    canonical = value.lstrip("0") or "0"
    if len(canonical) > 13:
        raise ValidationError(f"amount_vnd phải từ 1 đến {MAX_AMOUNT}")
    amount = int(canonical)
    if not 1 <= amount <= MAX_AMOUNT:
        raise ValidationError(f"amount_vnd phải từ 1 đến {MAX_AMOUNT}")
    return amount


def parse_row(row: dict[str, str], row_number: int) -> Transaction:
    """Validate một dòng; thông báo gắn với số dòng CSV để người học tìm lỗi."""
    try:
        if None in row or any(value is None for value in row.values()):
            raise ValidationError("số cột trong dòng không đúng header")
        values = {key: unicodedata.normalize("NFC", value.strip()) for key, value in row.items()}
        identifier = values["transaction_id"]
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", identifier):
            raise ValidationError("transaction_id cần 1–64 ký tự chữ ASCII, số, _ hoặc -")
        raw_date = values["date"]
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", raw_date):
            raise ValidationError("date cần định dạng YYYY-MM-DD")
        try:
            occurred_on = date.fromisoformat(raw_date)
        except ValueError as error:
            raise ValidationError("date không phải ngày tồn tại") from error
        kind = values["transaction_type"]
        if kind not in {"income", "expense"}:
            raise ValidationError("transaction_type chỉ nhận income hoặc expense")
        amount = parse_amount(values["amount_vnd"])
        description = values["description"]
        if not 1 <= len(description) <= 300:
            raise ValidationError("description cần 1–300 ký tự")
        category = values["category"]
        if kind == "income" and category:
            raise ValidationError("category của khoản thu phải trống")
        if kind == "expense" and category and category not in CATEGORIES:
            raise ValidationError("category khoản chi không thuộc bộ nhãn")
        return Transaction(identifier, occurred_on, kind, amount, description, category)
    except ValidationError as error:
        raise ValidationError(f"Dòng {row_number}: {error}") from error


def read_transactions(path: Path) -> list[Transaction]:
    """Đọc toàn bộ batch vào bộ nhớ sau validate; chưa có side effect lưu tiền."""
    with path.open("rb") as source:
        raw = source.read(MAX_BYTES + 1)
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
        for fields in reader:
            if len(transactions) >= MAX_ROWS:
                raise ValidationError(f"CSV vượt {MAX_ROWS} dòng dữ liệu")
            if len(fields) != len(COLUMNS):
                raise ValidationError(f"Dòng {reader.line_num}: số cột không đúng header hoặc dòng trống")
            row = dict(zip(COLUMNS, fields))
            transaction = parse_row(row, reader.line_num)
            if transaction.transaction_id in seen_ids:
                raise ValidationError(f"Dòng {reader.line_num}: transaction_id trùng trong batch")
            seen_ids.add(transaction.transaction_id)
            transactions.append(transaction)
    except csv.Error as error:
        raise ValidationError(f"CSV sai cú pháp: {error}") from error
    if not transactions:
        raise ValidationError("CSV cần ít nhất một dòng dữ liệu")
    return transactions


def summarize(transactions: list[Transaction], month: str | None = None) -> dict:
    """Tổng hợp tất định; khoản thiếu nhãn xuất hiện trong preview cần xác nhận."""
    if month is not None:
        try:
            if not re.fullmatch(r"[0-9]{4}-[0-9]{2}", month):
                raise ValueError
            date.fromisoformat(month + "-01")
        except ValueError as error:
            raise ValidationError("month cần tháng tồn tại theo YYYY-MM") from error
    selected = [item for item in transactions
                if month is None or item.occurred_on.isoformat()[:7] == month]
    income = sum(item.amount_vnd for item in selected if item.transaction_type == "income")
    expense = sum(item.amount_vnd for item in selected if item.transaction_type == "expense")
    categories = {}
    pending = 0
    for item in selected:
        if item.transaction_type == "expense":
            key = item.category or "can_xac_nhan"
            categories[key] = categories.get(key, 0) + item.amount_vnd
            pending += int(not item.category)
    return {
        "month": month or "all", "rows": len(selected),
        "income_vnd": income, "expense_vnd": expense,
        "net_vnd": income - expense, "expense_by_category": categories,
        "pending_expense_categories": pending,
        "note": "Chỉ preview; khoản chi thiếu nhãn cần xác nhận trước khi lưu app.",
    }


def main() -> int:
    # Một số terminal Windows dùng encoding không biểu diễn đủ tiếng Việt.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Kiểm tra CSV mẫu và tổng hợp thu chi")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--month", help="Lọc YYYY-MM, ví dụ 2026-10")
    arguments = parser.parse_args()
    try:
        result = summarize(read_transactions(arguments.csv_path), arguments.month)
    except (ValidationError, OSError) as error:
        print(f"Lỗi: {error}")
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
