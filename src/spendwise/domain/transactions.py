"""Kiểm tra input giao dịch trước khi tính tiền hoặc chuẩn bị lưu."""

import re
import unicodedata
from dataclasses import dataclass
from datetime import date
from collections.abc import Mapping


COLUMNS = (
    "transaction_id", "date", "transaction_type", "amount_vnd",
    "description", "category",
)
CATEGORIES = frozenset({
    "an_uong", "di_chuyen", "nha_o_hoa_don", "hoc_tap",
    "mua_sam", "giai_tri", "suc_khoe", "khac",
})
MAX_AMOUNT = 1_000_000_000_000


class ValidationError(ValueError):
    """Input trái hợp đồng; caller có thể hiển thị thông báo cho người dùng."""


@dataclass(frozen=True)
class Transaction:
    """Dữ liệu preview; category khoản chi có thể còn chờ xác nhận.

    Tạo từ parse_transaction/parse_row để kiểm tra input. Đối tượng này chưa
    biểu diễn việc người dùng xác nhận hoặc một bản ghi được lưu vào SQLite.
    """

    transaction_id: str
    occurred_on: date
    transaction_type: str
    amount_vnd: int
    description: str
    category: str


def parse_amount(value: str) -> int:
    """Chấp nhận VND nguyên dương dạng chữ ASCII, trong giới hạn MVP."""
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]+", value):
        raise ValidationError("amount_vnd phải là số nguyên dương, không dấu phân cách")
    # Kiểm tra độ dài trước int() để input quá lớn không gây lỗi ngoài hợp đồng.
    canonical = value.lstrip("0") or "0"
    if len(canonical) > len(str(MAX_AMOUNT)):
        raise ValidationError(f"amount_vnd phải từ 1 đến {MAX_AMOUNT}")
    amount = int(canonical)
    if not 1 <= amount <= MAX_AMOUNT:
        raise ValidationError(f"amount_vnd phải từ 1 đến {MAX_AMOUNT}")
    return amount


def parse_transaction(fields: Mapping[str, str]) -> Transaction:
    """Đổi sáu trường văn bản thành dữ liệu đã kiểm tra, không có I/O."""
    if set(fields) != set(COLUMNS) or any(not isinstance(value, str) for value in fields.values()):
        raise ValidationError("giao dịch cần đúng sáu trường văn bản của hợp đồng")
    values = {key: unicodedata.normalize("NFC", value.strip()) for key, value in fields.items()}
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


def parse_row(row: Mapping[str, str], row_number: int) -> Transaction:
    """Thêm vị trí dòng CSV vào lỗi của validator dùng chung."""
    try:
        return parse_transaction(row)
    except ValidationError as error:
        raise ValidationError(f"Dòng {row_number}: {error}") from error
