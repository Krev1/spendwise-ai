"""Ranh giới hợp đồng có thể làm sai tiền hoặc nhận input không hợp lệ."""

import unicodedata

import pytest

from spendwise.domain.transactions import MAX_AMOUNT, ValidationError, parse_transaction
from spendwise.services.reports import summarize


@pytest.mark.parametrize("amount", ["1", str(MAX_AMOUNT), "0" * 5000 + "1"])
def test_allowed_money_boundaries(transaction_fields, amount):
    transaction_fields["amount_vnd"] = amount
    assert parse_transaction(transaction_fields).amount_vnd == int(amount.lstrip("0"))


@pytest.mark.parametrize("amount", ["9" * 5000, "４５０００", "45000 VND"])
def test_invalid_money_reports_validation_error(transaction_fields, amount):
    transaction_fields["amount_vnd"] = amount
    with pytest.raises(ValidationError, match="amount_vnd"):
        parse_transaction(transaction_fields)


@pytest.mark.parametrize("identifier", ["", "a" * 65, "mã_1", "id with space"])
def test_reject_identifier_outside_contract(transaction_fields, identifier):
    transaction_fields["transaction_id"] = identifier
    with pytest.raises(ValidationError, match="transaction_id"):
        parse_transaction(transaction_fields)


def test_maximum_identifier_length_is_allowed(transaction_fields):
    transaction_fields["transaction_id"] = "a" * 64
    assert parse_transaction(transaction_fields).transaction_id == "a" * 64


@pytest.mark.parametrize("description", ["", "   ", "a" * 301])
def test_description_length_contract(transaction_fields, description):
    transaction_fields["description"] = description
    with pytest.raises(ValidationError, match="description"):
        parse_transaction(transaction_fields)


def test_nfc_normalization_happens_before_length_check(transaction_fields):
    transaction_fields["description"] = "  " + unicodedata.normalize("NFD", "ế" * 300) + "  "
    assert parse_transaction(transaction_fields).description == "ế" * 300


@pytest.mark.parametrize("change", ["missing", "extra", "not_text"])
def test_bad_manual_input_shape_is_validation_error(transaction_fields, change):
    if change == "missing":
        transaction_fields.pop("date")
    elif change == "extra":
        transaction_fields["unexpected"] = "x"
    else:
        transaction_fields["amount_vnd"] = 45000
    with pytest.raises(ValidationError, match="sáu trường văn bản"):
        parse_transaction(transaction_fields)


@pytest.mark.parametrize("field,value", [("transaction_type", "transfer"), ("category", "unknown")])
def test_reject_unknown_type_or_expense_label(transaction_fields, field, value):
    transaction_fields[field] = value
    with pytest.raises(ValidationError, match=field):
        parse_transaction(transaction_fields)


def test_leap_day_and_field_whitespace_are_valid(transaction_fields):
    transaction_fields.update(date=" 2024-02-29 ", amount_vnd=" 45000 ")
    transaction = parse_transaction(transaction_fields)
    assert transaction.occurred_on.isoformat() == "2024-02-29"
    assert transaction.amount_vnd == 45000


def test_report_keeps_integer_totals_above_single_transaction_limit(transaction_fields):
    transaction_fields.update(amount_vnd=str(MAX_AMOUNT), category="")
    transactions = [parse_transaction(transaction_fields),
                    parse_transaction({**transaction_fields, "transaction_id": "sample_2"})]
    result = summarize(transactions, "2026-10")
    assert result["expense_vnd"] == 2 * MAX_AMOUNT
    assert result["net_vnd"] == -2 * MAX_AMOUNT
    assert isinstance(result["net_vnd"], int)
    assert result["pending_expense_categories"] == 2
