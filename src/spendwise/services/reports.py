"""Tổng hợp thu chi bằng số nguyên, độc lập với mô hình phân loại."""

import re
from datetime import date

from spendwise.domain.transactions import Transaction, ValidationError


def summarize(transactions: list[Transaction], month: str | None = None) -> dict:
    """Tổng hợp preview; dòng thiếu category vẫn được tính và đánh dấu."""
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
